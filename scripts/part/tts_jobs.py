# -*- coding: utf-8 -*-
"""바깥 음성 엔진에 넘길 합성 작업 목록을 뽑는다.

`narrate_tts.py` 는 Windows SAPI 를 직접 부른다. 복제 음성은 Colab 의 GPU 에서
돌아가므로 그럴 수 없다. 그래서 **무엇을 어떤 이름으로 읽어야 하는지**만 적어
내보내고, 돌아온 WAV 를 `ingest_voice.py` 가 받는다.

    python scripts/part/tts_jobs.py <나갈 폴더> [--lang ko|en]

    <나갈 폴더>/jobs-ko.json   여덟 차시의 문단 전부

두 가지를 바꾼다.

**문단을 토막으로 쪼갠다.** 합성 단위인 문단은 최대 1,493자다. SAPI 는 규칙
기반이라 길이를 타지 않지만, Qwen3-TTS 같은 자기회귀 모델은 긴 입력에서 문장을
삼키거나 끝을 잘라먹는다 — 그리고 **잘린 채로도 소리는 난다.** 선생님 목소리로
문장 반쪽이 나가는 사고다. 그래서 문장 경계에서 토막을 내 각각 합성하고, 다시
이어 붙여 원래 문단 하나를 만든다. 문단 경계는 화면과 묶여 있으니 그대로 둔다.
토막을 공백 하나로 이으면 원문이 글자까지 복원된다 — `speakable()` 이 이미 모든
공백을 하나로 줄여 놓기 때문이다. `test_tts_jobs.py` 가 그것을 지킨다.

**태그는 본문에서 뺀다.** Qwen3-TTS 의 `generate_voice_clone` 에는 감정 인자가
없다(`instruct` 는 목소리를 고정으로 쓰는 CustomVoice 쪽에만 있다). 본문에
「[차분하게]」가 남아 있으면 엔진이 그 글자를 소리로 읽는다. 대신 문단마다
`tone` 을 따로 적어, 참조 음성을 골라 쓰는 열쇠로 남긴다 — 이 모델에서 감정은
참조 음성의 말투에서 온다.
"""
import argparse
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import narrate_tts as N
import tts_script

COURSE = HERE.parents[1] / 'projects' / 'autocad-technician'
SCRIPTS = {'ko': 'SCRIPT.md', 'en': 'SCRIPT.en.md'}
TAG = re.compile(r'\[[^\[\]]{1,12}\]\s*')

# 한 번에 읽힐 길이. 한국어 합성은 초당 5~6자쯤이라 100자면 20초 아래다.
# 영어는 글자가 잘게 쪼개져 같은 시간에 두 배 반쯤 들어간다.
SIZE = {'ko': (100, 150), 'en': (260, 380)}
SENT = re.compile(r'(?<=[.!?])\s+')
CLAUSE = re.compile(r'(?<=[,;:])\s+')

# 같은 수로 갈리면 값과 경고가 이긴다. 색이 아니라 정확도의 문제다.
PRIORITY = ('warn', 'slow', 'ask', 'stress', 'point', 'warm', 'light', 'calm')


def tone_of(text, lang, in_step):
    """문단을 대표하는 말투. 문장별 판정에서 가장 많은 것을 고른다."""
    names = [tts_script.pick(s, lang, in_step, i == 0)
             for i, s in enumerate(tts_script.sentences(text))]
    if not names:
        return 'calm'
    order = Counter(names)
    top = max(order.values())
    for name in PRIORITY:
        if order[name] == top:
            return name
    return 'calm'


def _split_space(piece, hard):
    """쉼표도 없는 긴 한 덩어리. 마지막 공백에서 자른다."""
    out = []
    while len(piece) > hard:
        cut = piece.rfind(' ', 0, hard + 1)
        if cut <= 0:
            break               # 공백 없는 덩어리는 쪼갤 자리가 없다
        out.append(piece[:cut])
        piece = piece[cut + 1:]
    out.append(piece)
    return out


def chunks_of(text, lang):
    """문단을 합성 토막으로. 공백 하나로 이으면 원문이 그대로 복원된다."""
    target, hard = SIZE[lang]
    pieces = []
    for sentence in SENT.split(text):
        if len(sentence) <= hard:
            pieces.append(sentence)
            continue
        for clause in CLAUSE.split(sentence):
            pieces.extend(_split_space(clause, hard) if len(clause) > hard else [clause])
    out = []
    for piece in pieces:
        if out and len(out[-1]) + 1 + len(piece) <= target:
            out[-1] = out[-1] + ' ' + piece
        else:
            out.append(piece)
    joined = ' '.join(out)
    if joined != text:
        raise SystemExit('토막을 이어도 원문이 안 나온다:\n  %r\n  %r' % (text, joined))
    return out


def step_keys(path):
    """녹화 단계 안의 문단 열쇠. 그 안은 실제로 조작하는 줄이다."""
    inside = set()
    text = Path(path).read_text(encoding='utf-8').replace('\r\n', '\n')
    depth = 0
    for line in text.split('\n'):
        m = re.match(r'^(#{1,4})\s', line)
        if m:
            depth = len(m.group(1))
        elif line.startswith('    ') and depth >= 3:
            inside.add(line[4:].strip()[:24])
    return inside


def collect(lang):
    out = []
    for lesson in sorted(p for p in COURSE.glob('lesson-*') if p.is_dir()):
        src = lesson / SCRIPTS[lang]
        if not src.is_file():
            continue
        jobs, _units, _order = N.synthesis_plan(str(src))
        steps = step_keys(src)
        rows = []
        for key, text in jobs:
            clean = TAG.sub('', text).strip()
            in_step = clean[:24] in steps
            rows.append({'key': key, 'tone': tone_of(clean, lang, in_step),
                         'chars': len(clean),
                         'chunks': [{'n': i, 'text': c}
                                    for i, c in enumerate(chunks_of(clean, lang), 1)]})
        out.append({'slug': lesson.name, 'jobs': rows})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('out')
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'))
    a = ap.parse_args(argv)
    lessons = collect(a.lang)
    target, hard = SIZE[a.lang]
    doc = {'schemaVersion': 1, 'lang': a.lang,
           'language': 'Korean' if a.lang == 'ko' else 'English',
           'chunkTarget': target, 'chunkHard': hard,
           'tones': list(PRIORITY),
           'note': ('본문에 태그는 없다. 감정은 tone 에 맞는 참조 음성으로 낸다. '
                    'WAV 는 out/<slug>/<key>#<n>.wav 로 하나씩 저장하고, 한 문단의 '
                    '토막들은 받는 쪽에서 공백 하나만큼의 쉼으로 이어 붙인다.'),
           'lessons': lessons}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / ('jobs-%s.json' % a.lang)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')

    rows = [j for l in lessons for j in l['jobs']]
    parts = [c for j in rows for c in j['chunks']]
    sizes = sorted(len(c['text']) for c in parts)
    print('%s · 차시 %d · 문단 %d · 토막 %d · 글자 %d'
          % (path.name, len(lessons), len(rows), len(parts), sum(j['chars'] for j in rows)))
    print('   토막 길이  중간 %d · 최대 %d (상한 %d)'
          % (sizes[len(sizes) // 2], sizes[-1], hard))
    for name, n in Counter(j['tone'] for j in rows).most_common():
        print('   %-8s %4d' % (name, n))
    over = [c for c in parts if len(c['text']) > hard]
    if over:
        print('   ! 상한 넘는 토막 %d개 (공백 없는 덩어리)' % len(over))
    return 0


if __name__ == '__main__':
    sys.exit(main())
