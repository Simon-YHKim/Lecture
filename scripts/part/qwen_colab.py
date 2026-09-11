# -*- coding: utf-8 -*-
"""Colab 의 GPU 에서 복제 음성으로 대본을 읽는다. 중간에 끊겨도 이어서 한다.

Colab 무료 한도는 몇 시간 만에 끊긴다. 1,185 토막을 한 번에 다 읽을 수는 없다고
보고 만들었다 — 끝난 토막은 `done.jsonl` 에 남기고, 다시 켜면 남은 것부터 한다.

    !python qwen_colab.py --work /content/drive/MyDrive/autocad-narration

작업 폴더(구글 드라이브에 두면 세션이 끊겨도 결과가 남는다):

    autocad-narration/
      jobs-ko.json          ← tts_jobs.py 가 낸 것
      refs/refs.json        ← 참조 음성 목록. 없으면 이 스크립트가 틀을 만든다
      refs/*.wav            ← 선생님 목소리
      out/ko/<차시>/<열쇠>#<번호>.wav
      out/ko/done.jsonl     ← 끝난 토막
      out/ko/suspect.jsonl  ← 길이가 수상한 토막. 사람이 들어봐야 한다

**길이를 재서 의심스러운 것을 남긴다.** 자기회귀 음성 모델은 문장을 삼키거나
끝을 잘라먹는데, 잘려도 소리는 정상으로 난다. 글자 수로 기대 길이를 잡고 그
밖으로 벗어나면 다시 만든다. 세 번 해도 안 되면 가장 가까운 것을 남기고
`suspect.jsonl` 에 적는다 — 조용히 버리지 않는다. 들어보고 고칠 수 있게.

이 스크립트는 저장소의 다른 모듈을 불러오지 않는다. Colab 에 파일 하나만
올라가면 돌아야 한다.
"""
import argparse
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
BAND = (0.45, 2.2)          # 기대 길이의 몇 배까지 받아들이는가
TRIES = 3
SILENCE = 0.008             # 이 아래는 소리가 없는 것으로 본다 (정규화 진폭)
MARGIN = 0.04               # 앞뒤로 남겨 두는 여유 (초)

REFS_TEMPLATE = {
    '_': {'audio': 'base.wav',
          'text': '여기에 base.wav 에서 실제로 들리는 말을 글자까지 그대로 적는다.'},
    '_note': ('열쇠는 tone 이름이다. `_` 는 짝이 없는 tone 이 쓰는 기본 음성이다. '
              'tone 마다 다른 음성을 두면 말투가 갈리고, `_` 하나만 두면 한 말투로 '
              '전체가 나온다. text 는 audio 에서 들리는 말과 정확히 같아야 한다 — '
              '다르면 복제 품질이 떨어진다.'),
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


def load_refs(work):
    folder = os.path.join(work, 'refs')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, 'refs.json')
    if not os.path.exists(path):
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(REFS_TEMPLATE, ensure_ascii=False, indent=1) + '\n')
        raise SystemExit('참조 음성 목록의 틀을 만들었다. 채운 뒤 다시 돌려라:\n  ' + path)
    with io.open(path, encoding='utf-8') as fh:
        raw = json.load(fh)
    refs = {}
    for tone, entry in raw.items():
        if tone.startswith('_note'):
            continue
        audio = os.path.join(folder, entry['audio'])
        if not os.path.exists(audio):
            raise SystemExit('참조 음성이 없다: ' + audio)
        text = (entry.get('text') or '').strip()
        if not text or text.startswith('여기에'):
            raise SystemExit('%s 의 text 를 실제로 들리는 말로 채워라.' % entry['audio'])
        seconds = wav_seconds(audio)
        if seconds < 3:
            raise SystemExit('%s 가 %.1f초다. 복제는 3초 이상이 필요하다.'
                             % (entry['audio'], seconds))
        if seconds > 30:
            print('! %s 가 %.0f초다. 10~15초로 줄이면 대개 더 안정적이다.'
                  % (entry['audio'], seconds), flush=True)
        refs[tone] = (audio, text)
    if '_' not in refs:
        raise SystemExit('짝 없는 tone 이 쓸 기본 음성 `_` 항목이 필요하다.')
    print('참조 음성 %d개: %s' % (len(refs), ', '.join(sorted(refs))), flush=True)
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
                ident = (slug, job['key'], chunk['n'])
                dest = os.path.join(outdir, slug, '%s#%02d.wav' % (job['key'], chunk['n']))
                row = done.get(ident)
                if row and row.get('sha') == sha(chunk['text']) and os.path.exists(dest):
                    continue
                todo.append((slug, job['key'], job['tone'], chunk['n'], chunk['text'], dest))
    return todo


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--work', required=True, help='작업 폴더 (구글 드라이브 권장)')
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'))
    ap.add_argument('--lesson', default='', help='한 차시만 (예: lesson-02)')
    ap.add_argument('--limit', type=int, default=0, help='이번에 만들 토막 수 상한')
    ap.add_argument('--model', default='Qwen/Qwen3-TTS-12Hz-0.6B-Base')
    a = ap.parse_args(argv)

    work = os.path.abspath(a.work)
    with io.open(os.path.join(work, 'jobs-%s.json' % a.lang), encoding='utf-8') as fh:
        doc = json.load(fh)
    outdir = os.path.join(work, 'out', a.lang)
    os.makedirs(outdir, exist_ok=True)
    donefile = os.path.join(outdir, 'done.jsonl')
    suspectfile = os.path.join(outdir, 'suspect.jsonl')

    refs = load_refs(work)
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
    dtype = torch.bfloat16 if big else torch.float16
    kwargs = {'device_map': 'cuda:0' if torch.cuda.is_available() else 'cpu', 'dtype': dtype}
    try:
        model = Qwen3TTSModel.from_pretrained(a.model, attn_implementation='flash_attention_2',
                                              **kwargs)
    except Exception as exc:                      # T4 에는 flash-attn 이 없다
        log(outdir, 'flash_attention_2 없음 → sdpa (%s)' % type(exc).__name__)
        model = Qwen3TTSModel.from_pretrained(a.model, attn_implementation='sdpa', **kwargs)
    log(outdir, '%s · %s · %s' % (a.model, kwargs['device_map'], dtype))

    rate, (low, high) = RATE[a.lang], BAND
    began, made, suspect = time.time(), 0, 0
    for i, (slug, key, tone, n, text, dest) in enumerate(todo, 1):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        ref_audio, ref_text = refs.get(tone, refs['_'])
        want = len(text) / rate
        best = None
        for attempt in range(1, TRIES + 1):
            wavs, sr = model.generate_voice_clone(text=text, language=doc['language'],
                                                  ref_audio=ref_audio, ref_text=ref_text)
            audio = trim(wavs[0], sr)
            seconds = len(audio) / float(sr)
            if best is None or abs(seconds - want) < abs(best[1] - want):
                best = (audio, seconds, sr, attempt)
            if low * want <= seconds <= high * want:
                break
        audio, seconds, sr, attempt = best
        ok = low * want <= seconds <= high * want
        sf.write(dest, np.asarray(audio, dtype=np.float32), sr, subtype='PCM_16')
        row = {'slug': slug, 'key': key, 'n': n, 'sha': sha(text), 'sec': round(seconds, 3),
               'sr': sr, 'chars': len(text), 'tone': tone, 'tries': attempt, 'ok': ok}
        with io.open(donefile, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
        made += 1
        if not ok:
            suspect += 1
            with io.open(suspectfile, 'a', encoding='utf-8') as fh:
                fh.write(json.dumps(dict(row, want=round(want, 2), text=text),
                                    ensure_ascii=False) + '\n')
            log(outdir, '? %s#%02d  %.1f초 (기대 %.1f초) · %d자' % (key, n, seconds, want, len(text)))
        if i % 25 == 0 or i == len(todo):
            spent = time.time() - began
            log(outdir, '%d/%d · %.0f초 경과 · 토막당 %.1f초 · 의심 %d'
                % (i, len(todo), spent, spent / made, suspect))
    log(outdir, '이번에 %d개 만들었다. 의심 %d개. 남은 것은 다시 돌리면 이어서 한다.'
        % (made, suspect))
    return 0


if __name__ == '__main__':
    sys.exit(main())
