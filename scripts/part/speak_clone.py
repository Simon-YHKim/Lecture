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

# 초당 몇 글자를 읽는가. 한국어 낭독은 5~6자쯤이고, 영어는 글자가 잘게
# 쪼개져 두 배 반쯤 들어간다. 아래위로 넉넉히 잡아 잘림만 잡는다.
RATE = {'ko': 5.5, 'en': 14.5}
# 한 번에 몇 토막을 같이 만드는가. 8 로 두니 호스트 RAM 이 터져 프로세스가
# 죽었다(31.6GB 중 여유 10GB 에서). 배치는 가장 긴 토막에 맞춰 패딩되므로
# 길이를 섞으면 낭비가 크다 — 그래서 길이순으로 정렬해 묶는다.
BATCH = 4
BAND = (0.45, 2.2)          # 기대 길이의 몇 배까지 받아들이는가
TRIES = 3
SILENCE = 0.008             # 이 아래는 소리가 없는 것으로 본다 (정규화 진폭)
MARGIN = 0.04               # 앞뒤로 남겨 두는 여유 (초)

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


def trim(wav, sr):
    """앞뒤 무음을 잘라낸다. 토막을 이어 붙일 때 쉼이 들쭉날쭉해지지 않게."""
    import numpy as np
    x = np.asarray(wav, dtype=np.float32).reshape(-1)
    peak = float(np.max(np.abs(x))) or 1.0
    loud = np.abs(x) > SILENCE * peak
    if not loud.any():
        return x
    first, last = int(np.argmax(loud)), len(x) - int(np.argmax(loud[::-1]))
    pad = int(MARGIN * sr)
    return x[max(0, first - pad):min(len(x), last + pad)]


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


def plan(doc, done, outdir, only):
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


def speak(model, texts, language, mood, refs, prompts):
    """토막 여러 개를 한 번에. 배치가 이 작업의 유일한 속도 수단이다 —
    4070 에서 낱개로 돌리면 0.28배속이라 국문만 아홉 시간이 걸린다."""
    n = len(texts)
    call = {'text': list(texts), 'language': [language] * n, 'non_streaming_mode': True}
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
    todo = plan(doc, done, outdir, a.lesson)
    total = sum(len(j['chunks']) for l in doc['lessons'] for j in l['jobs']
                if not a.lesson or a.lesson in l['slug'])
    log(outdir, '남은 토막 %d / %d' % (len(todo), total))
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

    rate, (low, high) = RATE[a.lang], BAND
    began, made, suspect, seconds_made = time.time(), 0, 0, 0.0
    batches = groups(todo, refs, a.batch)
    log(outdir, '배치 %d개 · 한 묶음 최대 %d토막' % (len(batches), a.batch))
    for bi, batch in enumerate(batches, 1):
        mood = batch[0]['ref']
        wavs, sr = speak(model, [x['text'] for x in batch], doc['language'], mood, refs, prompts)
        for item, raw in zip(batch, wavs):
            audio = trim(raw, sr)
            got = len(audio) / float(sr)
            want = len(item['text']) / rate
            tries = 1
            # 잘렸거나 늘어진 것만 낱개로 다시 만든다. 배치 전체를 버리지 않는다.
            while not (low * want <= got <= high * want) and tries < TRIES:
                tries += 1
                one, sr = speak(model, [item['text']], doc['language'], mood, refs, prompts)
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
        if bi % 4 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
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
