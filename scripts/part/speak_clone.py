# -*- coding: utf-8 -*-
"""복제 음성으로 대본을 읽는다. 끊겨도 이어서 한다.

이 컴퓨터의 GPU 로도, Colab 으로도 같은 스크립트가 돈다. 저장소의 다른 모듈을
불러오지 않는다 — 작업 목록 JSON 과 참조 음성만 있으면 된다.

    python scripts/part/speak_clone.py --work local-materials/qwen-narration --lang ko

작업 폴더:

    qwen-narration/
      jobs-ko.json          ← tts_jobs.py 가 낸 것 (토막마다 mood 가 적혀 있다)
      refs/refs.json        ← mood 별 참조 음성. 없으면 틀을 만든다
      refs/*.wav            ← 선생님 목소리
      out/ko/<차시>/<열쇠>#<번호>.wav
      out/ko/done.jsonl     ← 끝난 토막
      out/ko/suspect.jsonl  ← 길이가 수상한 토막. 사람이 들어봐야 한다

**감정은 참조 음성에서 온다.** `generate_voice_clone` 에는 감정 인자가 없다 —
확인한 사실이다(`instruct` 는 목소리가 고정된 CustomVoice · VoiceDesign 쪽에만
있다). 대신 `ref_text` 를 함께 주면 모델이 ICL 로 **참조 음성의 말투까지** 따라
간다. 그래서 mood 마다 다른 짧은 녹음을 두면 그 말투로 읽는다. `refs.json` 에
`_` 하나만 두면 전체가 한 말투로 나온다 — 그래도 돌아간다.

**길이를 재서 의심스러운 것을 남긴다.** 자기회귀 음성 모델은 문장을 삼키거나
끝을 잘라먹는데, 잘려도 소리는 정상으로 난다. 글자 수로 기대 길이를 잡고 그
밖으로 벗어나면 다시 만든다. 세 번 해도 안 되면 가장 가까운 것을 남기고
`suspect.jsonl` 에 적는다 — 조용히 버리지 않는다.
"""
import argparse
import gc
import hashlib
import io
import json
import os
import sys
import time
import wave

# 초당 몇 글자를 읽는가. **씨앗값일 뿐이다** — 실제 속도는 목소리마다 다르다.
# 국문 267토막을 재 보니 중간값이 7.21자/초였다. 5.5 로 가정하면 31% 어긋나고,
# 그러면 기대 길이가 22% 길게 잡혀 대역이 실제로는 2.50~12.22자/초를 다 받아
# 준다 — 본문의 3분의 1만 읽은 토막도 통과한다. 그래서 만든 것이 쌓이면
# `done.jsonl` 의 중간값으로 갈아탄다.
RATE = {'ko': 5.5, 'en': 14.5}
CALIBRATE = 40              # 이만큼 쌓이면 실측 중간값을 쓴다
# 한 번에 몇 토막을 같이 만드는가. 8 로 두니 호스트 RAM 이 터져 프로세스가
# 죽었다(31.6GB 중 여유 10GB 에서). 배치는 가장 긴 토막에 맞춰 패딩되므로
# 길이를 섞으면 낭비가 크다 — 그래서 길이순으로 정렬해 묶는다.
BATCH = 4
# 기대 길이의 몇 배까지 받아들이는가. 실측 중간값을 쓰면 좁혀도 안전하다 —
# 국문 267토막에서 [0.65, 1.60] 이 걸러 낸 것은 5개(1.9%)였고 그 다섯은 모두
# 실제로 수상했다(가장 느린 것이 2.60자/초 · 중간값의 2.8배 느림).
BAND = (0.65, 1.6)
TRIES = 3
# 1초 음성에 토큰이 몇 개 드는가. 재 보니 1,200토큰으로 100자(13.6초)를 자르지
# 않고 다 읽었으므로 88개 아래다 — 여유를 두어 120으로 잡는다.
#
# **상한이 없으면 한 토막이 폭주해 몇십 분을 잡아먹는다.** 실제로 그랬다:
# VRAM 이 2.74GB 에서 10.8/12GB 로 불고 22분간 파일 하나도 안 나왔다. 대역
# 위끝(1.6배)을 넘는 음성은 어차피 버리므로, 그 길이까지만 만들게 한다 —
# 잘라 버릴 것을 끝까지 만들 이유가 없다.
TOKENS_PER_SEC = 120
TOKEN_FLOOR = 300           # 짧은 토막도 이만큼은 준다


def token_cap(chars, rate):
    """이 글자 수에 허용할 토큰 상한."""
    return int(TOKENS_PER_SEC * BAND[1] * chars / rate) + TOKEN_FLOOR
FRAME = 0.02                # 소리를 재는 창 (초)
GATE = 0.04                 # 큰 소리의 이 비율 아래는 무음으로 본다
FLOOR_MULT = 3.0            # 잡음 바닥(10분위)의 이 배수까지 문턱을 올린다
MARGIN = 0.06               # 앞뒤로 남겨 두는 여유 (초)
MAX_GAP = 0.8               # 토막 안에서 이보다 긴 구멍은 줄인다 (초)
KEEP_GAP = 0.3              # 줄인 뒤 남기는 한 호흡 (초)

# 녹음할 때 어떤 말투인지. 이 글은 참조 음성의 대사가 아니라 **안내문**이다.
MOOD_HINT = {
    'base': '평소 강의하듯 차분하게',
    'careful': '치수를 또박또박 천천히 끊어 읽듯',
    'firm': '실수를 주의시키듯 낮고 단단하게',
    'light': '가볍게 말을 걸듯, 질문하듯',
}


def log(work, message):
    line = '%s  %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), message)
    print(line, flush=True)
    with io.open(os.path.join(work, 'log.txt'), 'a', encoding='utf-8') as fh:
        fh.write(line + '\n')


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def wav_seconds(path):
    with wave.open(path, 'rb') as fh:
        return fh.getnframes() / float(fh.getframerate())


def _voiced(x, sr):
    """20밀리초 창마다 말이 있는지. 큰 소리의 한 줌을 기준으로 잰다.

    최대 진폭을 기준으로 잡으면 안 된다 — 한 번의 파열음이 기준을 끌어올려
    잡음 바닥이 소리로 세어진다. 실제로 그래서 앞에 10.5초 무음이 붙은 토막이
    통과했다. 큰 쪽 20% 창의 평균을 기준으로 삼으면 그 일이 없다.
    """
    import numpy as np
    win = max(1, int(FRAME * sr))
    m = len(x) // win
    if m == 0:
        return None, win
    rms = np.sqrt((x[:m * win].reshape(m, win) ** 2).mean(axis=1))
    loud = float(np.sort(rms)[int(m * 0.8):].mean()) or 1e-9
    # 바닥을 따로 잰다. 잡음 바닥이 말의 5%쯤 되면 `GATE * loud` 하나로는
    # 넘어서지 못한다 — 바닥의 세 배까지 올려 그 위만 말로 센다. 위쪽은
    # 막아 둔다: 거의 쉼이 없는 토막은 10분위가 이미 말소리라서, 그 세 배를
    # 문턱으로 쓰면 토막이 통째로 무음이 되어 버린다.
    floor = float(np.percentile(rms, 10))
    gate = min(max(GATE * loud, FLOOR_MULT * floor), 0.5 * loud)
    return rms > gate, win


def trim(wav, sr):
    """앞뒤 무음을 걷고 **안쪽의 긴 구멍도 줄인다.**

    구멍은 그냥 조용한 게 아니다. 문단 경계 시각을 실측으로 잡으므로, 토막
    안의 10초 무음은 시각 파일에 그대로 실려 화면이 멈춘 채 말이 늦게
    시작하게 만든다. 문장 사이 한 호흡(0.3초)보다 긴 구멍은 그만큼으로 줄인다.
    """
    import numpy as np
    x = np.asarray(wav, dtype=np.float32).reshape(-1)
    mask, win = _voiced(x, sr)
    if mask is None or not mask.any():
        return x
    idx = np.flatnonzero(mask)
    pad = int(MARGIN * sr)
    x = x[max(0, int(idx[0]) * win - pad):min(len(x), (int(idx[-1]) + 1) * win + pad)]

    mask, win = _voiced(x, sr)
    if mask is None or not mask.any():
        return x
    keep, gap, limit = [], 0, int(round(MAX_GAP / FRAME))
    for i, voiced in enumerate(mask):
        if voiced:
            if gap > limit:
                # 구멍의 앞뒤를 남기고 가운데를 버린다. 꼬리와 머리의 잔향이
                # 남아 이어 붙인 자리가 뚝 끊기지 않는다.
                half = int(round(KEEP_GAP / FRAME / 2))
                keep.extend(range(i - gap, i - gap + half))
                keep.extend(range(i - half, i))
            else:
                keep.extend(range(i - gap, i))
            gap = 0
            keep.append(i)
        else:
            gap += 1
    pieces = [x[j * win:(j + 1) * win] for j in keep]
    return np.concatenate(pieces) if pieces else x


def refs_template(moods):
    doc = {'_note': ('열쇠는 mood 다. `_` 는 짝이 없는 mood 가 쓰는 기본 음성이다. '
                     'text 는 그 wav 에서 **실제로 들리는 말과 글자까지 같아야** 한다 — '
                     '다르면 복제 품질이 떨어진다. 하나(`_`)만 채워도 돌아가고, '
                     'mood 마다 채우면 그 말투로 읽는다.')}
    doc['_'] = {'audio': 'base.wav', 'text': '', 'howToRead': MOOD_HINT['base']}
    for mood in moods:
        doc[mood] = {'audio': '%s.wav' % mood, 'text': '',
                     'howToRead': MOOD_HINT.get(mood, '')}
    return doc


def load_refs(work, moods):
    folder = os.path.join(work, 'refs')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, 'refs.json')
    if not os.path.exists(path):
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(refs_template(moods), ensure_ascii=False, indent=1) + '\n')
        raise SystemExit('참조 음성 목록의 틀을 만들었다. 최소한 `_` 를 채운 뒤 다시 돌려라:\n  ' + path)
    with io.open(path, encoding='utf-8') as fh:
        raw = json.load(fh)
    refs = {}
    for mood, entry in raw.items():
        if mood.startswith('_note'):
            continue
        audio = os.path.join(folder, entry.get('audio') or '')
        text = (entry.get('text') or '').strip()
        if not entry.get('audio') or not os.path.exists(audio) or not text:
            continue                        # 아직 안 녹음한 mood — 기본 음성이 맡는다
        seconds = wav_seconds(audio)
        if seconds < 3:
            raise SystemExit('%s 가 %.1f초다. 복제는 3초 이상이 필요하다.' % (entry['audio'], seconds))
        if seconds > 30:
            print('! %s 가 %.0f초다. 10~15초로 줄이면 대개 더 안정적이다.'
                  % (entry['audio'], seconds), flush=True)
        refs[mood] = (audio, text)
    if '_' not in refs:
        raise SystemExit('짝 없는 mood 가 쓸 기본 음성 `_` 항목을 채워라: %s'
                         % os.path.join(folder, 'refs.json'))
    missing = sorted(set(moods) - set(refs))
    print('참조 음성 %d개: %s%s'
          % (len(refs), ', '.join(sorted(refs)),
             (' · 기본이 맡는 mood: ' + ', '.join(missing)) if missing else ''), flush=True)
    return refs


def measured_rate(done, seed):
    """지금까지 만든 것에서 실제 낭독 속도를 구한다. 모자라면 씨앗값."""
    rates = sorted(r['chars'] / r['sec'] for r in done.values()
                   if r.get('ok') and r.get('sec', 0) > 0.5 and r.get('chars', 0) >= 10)
    if len(rates) < CALIBRATE:
        return seed, len(rates)
    return rates[len(rates) // 2], len(rates)


def load_done(path):
    done = {}
    if os.path.exists(path):
        with io.open(path, encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if line:
                    row = json.loads(line)
                    done[(row['slug'], row['key'], row['n'])] = row
    return done


def plan(doc, done, outdir, only, redo=False):
    """아직 안 만든 토막만. 대본이 바뀐 토막은 sha 가 달라 다시 만든다."""
    todo = []
    for lesson in doc['lessons']:
        slug = lesson['slug']
        if only and only not in slug:
            continue
        for job in lesson['jobs']:
            for chunk in job['chunks']:
                dest = os.path.join(outdir, slug, '%s#%02d.wav' % (job['key'], chunk['n']))
                row = done.get((slug, job['key'], chunk['n']))
                if row and row.get('sha') == sha(chunk['text']) and os.path.exists(dest):
                    if not (redo and not row.get('ok')):
                        continue
                todo.append({'slug': slug, 'key': job['key'], 'n': chunk['n'],
                             'mood': chunk.get('mood', '_'), 'tone': chunk.get('tone', ''),
                             'text': chunk['text'], 'dest': dest})
    return todo


def build_prompts(model, refs):
    """참조 음성을 한 번만 부호화한다. 천 번 넘게 다시 읽을 이유가 없다."""
    prompts = {}
    for mood, (audio, text) in sorted(refs.items()):
        try:
            prompts[mood] = model.create_voice_clone_prompt(ref_audio=audio, ref_text=text)
        except Exception as exc:
            print('! 참조 음성 캐시 실패(%s) — 매번 다시 읽는다: %s'
                  % (mood, type(exc).__name__), flush=True)
            return None
    return prompts


def speak(model, texts, language, mood, refs, prompts, cap=None):
    """토막 여러 개를 한 번에. 배치가 이 작업의 유일한 속도 수단이다 —
    4070 에서 낱개로 돌리면 0.28배속이라 국문만 아홉 시간이 걸린다."""
    n = len(texts)
    call = {'text': list(texts), 'language': [language] * n, 'non_streaming_mode': True}
    if cap:
        call['max_new_tokens'] = cap
    if prompts:
        call['voice_clone_prompt'] = prompts[mood] * n
    else:
        audio, ref = refs[mood]
        call['ref_audio'], call['ref_text'] = [audio] * n, [ref] * n
    wavs, sr = model.generate_voice_clone(**call)
    if len(wavs) != n:
        raise RuntimeError('토막 %d개를 넣었는데 %d개가 돌아왔다' % (n, len(wavs)))
    return wavs, sr


def groups(todo, refs, size):
    """같은 참조 음성을 쓰는 토막끼리, **길이가 비슷한 것끼리** 묶는다.

    배치는 가장 긴 토막 길이로 패딩된다. 24자와 100자를 같이 넣으면 짧은 쪽
    계산이 네 배로 낭비되고 메모리도 그만큼 더 쓴다. 만드는 순서는 아무래도
    좋다 — 토막마다 제 파일에 따로 쓴다.
    """
    by_ref = {}
    for item in todo:
        mood = item['mood'] if item['mood'] in refs else '_'
        item['ref'] = mood
        by_ref.setdefault(mood, []).append(item)
    out = []
    for mood in sorted(by_ref):
        rows = sorted(by_ref[mood], key=lambda x: len(x['text']))
        out.extend(rows[i:i + size] for i in range(0, len(rows), size))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--work', required=True, help='작업 폴더')
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'))
    ap.add_argument('--lesson', default='', help='한 차시만 (예: lesson-02)')
    ap.add_argument('--limit', type=int, default=0, help='이번에 만들 토막 수 상한')
    ap.add_argument('--model', default='Qwen/Qwen3-TTS-12Hz-0.6B-Base')
    ap.add_argument('--batch', type=int, default=BATCH, help='한 번에 만들 토막 수')
    ap.add_argument('--redo-suspect', action='store_true',
                    help='길이가 수상하다고 표시된 토막을 다시 만든다')
    a = ap.parse_args(argv)

    work = os.path.abspath(a.work)
    with io.open(os.path.join(work, 'jobs-%s.json' % a.lang), encoding='utf-8') as fh:
        doc = json.load(fh)
    outdir = os.path.join(work, 'out', a.lang)
    os.makedirs(outdir, exist_ok=True)
    donefile = os.path.join(outdir, 'done.jsonl')
    suspectfile = os.path.join(outdir, 'suspect.jsonl')

    refs = load_refs(work, doc.get('moods') or [])
    done = load_done(donefile)
    rate, samples = measured_rate(done, RATE[a.lang])
    # 대역이 바뀌었으면 옛 판정을 그 대역으로 다시 본다. 느슨한 대역에서
    # 통과한 토막이 새 대역에서는 수상할 수 있다 — 그걸 놓치면 선생님 목소리로
    # 반쪽 문장이 나간다.
    low, high = BAND
    for row in done.values():
        if row.get('sec', 0) > 0 and row.get('chars', 0) >= 10:
            want = row['chars'] / rate
            row['ok'] = low * want <= row['sec'] <= high * want
    todo = plan(doc, done, outdir, a.lesson, a.redo_suspect)
    total = sum(len(j['chunks']) for l in doc['lessons'] for j in l['jobs']
                if not a.lesson or a.lesson in l['slug'])
    log(outdir, '남은 토막 %d / %d · 속도 %.2f자/초 (%s) · 대역 [%.2f, %.2f]'
        % (len(todo), total, rate,
           '실측 %d개' % samples if samples >= CALIBRATE else '씨앗값', low, high))
    if not todo:
        log(outdir, '다 만들었다.')
        return 0
    if a.limit:
        todo = todo[:a.limit]

    import numpy as np
    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    big = torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8
    kwargs = {'device_map': 'cuda:0' if torch.cuda.is_available() else 'cpu',
              'dtype': torch.bfloat16 if big else torch.float16}
    try:
        model = Qwen3TTSModel.from_pretrained(a.model, attn_implementation='flash_attention_2',
                                              **kwargs)
    except Exception as exc:
        log(outdir, 'flash_attention_2 없음 → sdpa (%s)' % type(exc).__name__)
        model = Qwen3TTSModel.from_pretrained(a.model, attn_implementation='sdpa', **kwargs)
    log(outdir, '%s · %s · %s' % (a.model, kwargs['device_map'], kwargs['dtype']))
    prompts = build_prompts(model, refs)

    began, made, suspect, seconds_made = time.time(), 0, 0, 0.0
    batches = groups(todo, refs, a.batch)
    log(outdir, '배치 %d개 · 한 묶음 최대 %d토막 · 토큰 상한 %d~%d'
        % (len(batches), a.batch,
           token_cap(min(len(x['text']) for x in todo), rate),
           token_cap(max(len(x['text']) for x in todo), rate)))
    for bi, batch in enumerate(batches, 1):
        mood = batch[0]['ref']
        cap = token_cap(max(len(x['text']) for x in batch), rate)
        wavs, sr = speak(model, [x['text'] for x in batch], doc['language'],
                         mood, refs, prompts, cap)
        for item, raw in zip(batch, wavs):
            audio = trim(raw, sr)
            got = len(audio) / float(sr)
            want = len(item['text']) / rate
            tries = 1
            # 잘렸거나 늘어진 것만 낱개로 다시 만든다. 배치 전체를 버리지 않는다.
            while not (low * want <= got <= high * want) and tries < TRIES:
                tries += 1
                one, sr = speak(model, [item['text']], doc['language'], mood, refs,
                                prompts, token_cap(len(item['text']), rate))
                again = trim(one[0], sr)
                if abs(len(again) / float(sr) - want) < abs(got - want):
                    audio, got = again, len(again) / float(sr)
            ok = low * want <= got <= high * want
            os.makedirs(os.path.dirname(item['dest']), exist_ok=True)
            sf.write(item['dest'], np.asarray(audio, dtype=np.float32), sr, subtype='PCM_16')
            row = {'slug': item['slug'], 'key': item['key'], 'n': item['n'],
                   'sha': sha(item['text']), 'sec': round(got, 3), 'sr': sr,
                   'chars': len(item['text']), 'tone': item['tone'], 'mood': item['mood'],
                   'ref': mood, 'tries': tries, 'ok': ok}
            with io.open(donefile, 'a', encoding='utf-8') as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + '\n')
            made += 1
            seconds_made += got
            if not ok:
                suspect += 1
                with io.open(suspectfile, 'a', encoding='utf-8') as fh:
                    fh.write(json.dumps(dict(row, want=round(want, 2), text=item['text']),
                                        ensure_ascii=False) + '\n')
                log(outdir, '? %s#%02d  %.1f초 (기대 %.1f초) · %d자'
                    % (item['key'], item['n'], got, want, len(item['text'])))
        del wavs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if bi % 8 == 0:
            gc.collect()
        if bi % 5 == 0 or bi == len(batches):
            spent = time.time() - began
            left = (len(todo) - made) * spent / made
            log(outdir, '%d/%d · %.0f분 경과 · 실시간 %.2f배 · 남은 시간 %.0f분 · 의심 %d'
                % (made, len(todo), spent / 60, seconds_made / spent, left / 60, suspect))
    log(outdir, '이번에 %d개 만들었다(%.0f분 분량). 의심 %d개. 다시 돌리면 이어서 한다.'
        % (made, seconds_made / 60, suspect))
    return 0


if __name__ == '__main__':
    sys.exit(main())
