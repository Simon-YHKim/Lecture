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
# 굵게 표시는 화면의 강조 표기다. `speakable()` 은 백틱만 걷어내므로 여기까지
# 별표가 따라온다. 규칙 기반 음성은 별표를 흘려 버렸지만 신경망 음성은 그걸
# 소리로 만들거나 그 자리에서 발음이 흔들린다. 국문 7문단·영문 1문단이다.
BOLD = re.compile(r'\*\*([^*]*)\*\*')
# 괄후 표기만 떼고 안의 말은 먹지 않는다.



BACKREF = r'\1'


def spoken(text):
    """엔진에 실제로 넘기는 글. 감정 태그와 굵게 표시는 말이 아니다."""
    return BOLD.sub(BACKREF, TAG.sub('', text)).strip()

# 한 번에 읽힐 길이. 한국어 합성은 초당 5~6자쯤이라 100자면 20초 아래다.
# 영어는 글자가 잘게 쪼개져 같은 시간에 두 배 반쯤 들어간다.
SIZE = {'ko': (100, 150), 'en': (260, 380)}
SENT = re.compile(r'(?<=[.!?])\s+')
CLAUSE = re.compile(r'(?<=[,;:])\s+')

# tone 을 음성 엔진에 어떻게 말해 주는가. 지시를 받는 체크포인트(CustomVoice ·
# VoiceDesign)에는 이 문장을 그대로 넘긴다. 목소리를 복제하는 Base 에는 지시
# 인자가 없어서, 어느 참조 음성을 고를지 가르는 이름으로만 쓴다.
INSTRUCT = {
    'ko': {'calm': '차분하고 안정된 강의 말투로 말해',
           'point': '화면의 한 곳을 가리키며 짚어 주듯 말해',
           'stress': '중요한 대목이라 힘을 주어 말해',
           'slow': '숫자를 또박또박 천천히 끊어 읽어',
           'ask': '학습자에게 묻듯 끝을 살짝 올려 말해',
           'warn': '실수를 주의시키듯 낮고 단단하게 말해',
           'light': '가볍고 짧게 툭 던지듯 말해',
           'warm': '따뜻하게 격려하듯 말해'},
    'en': {'calm': 'speak in a calm, steady lecturing voice',
           'point': 'speak as if pointing at one spot on the screen',
           'stress': 'stress this; it is the important part',
           'slow': 'read the numbers slowly and distinctly',
           'ask': 'ask the learner, lifting the end slightly',
           'warn': 'warn against a mistake, low and firm',
           'light': 'toss this off lightly and briefly',
           'warm': 'speak warmly, encouraging them'},
}

# 참조 음성을 네 개만 녹음할 때 여덟 tone 을 어디에 묶는가. 녹음 하나에 열두
# 마디씩이면 1분이면 끝나고, 네 시간 반짜리 낭독 전체의 굴곡이 생긴다.
MOOD = {'calm': 'base', 'point': 'base', 'slow': 'careful', 'stress': 'firm',
        'warn': 'firm', 'ask': 'light', 'light': 'light', 'warm': 'light'}

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


def lesson_rows(script, lang):
    """한 차시의 문단 목록. **작업 목록과 받아쓰기가 같은 함수를 쓴다** —
    두 곳에서 따로 쪼개면 토막 번호가 어긋나 엉뚱한 소리가 붙는다."""
    jobs, _units, _order = N.synthesis_plan(str(script))
    steps = step_keys(script)
    rows = []
    for key, text in jobs:
        clean = spoken(text)
        in_step = clean[:24] in steps
        lead = bool(tts_script.STAGE.match(text))
        tone = tone_of(clean, lang, in_step)
        # **말투는 토막마다 고른다.** 토막이 대충 한 문장이고, 참조 음성도
        # 토막 하나에 하나씩 붙는다. 문단 전체를 한 말투로 묶으면 값을 읽는
        # 문장이 주변 설명에 묻혀 여덟 차시가 한 가지 톤으로 나온다.
        pieces = []
        for i, body in enumerate(chunks_of(clean, lang), 1):
            name = tts_script.pick(body, lang, in_step, i == 1 and lead)
            pieces.append({'n': i, 'tone': name, 'mood': MOOD[name], 'text': body})
        rows.append({'key': key, 'tone': tone, 'mood': MOOD[tone],
                     'chars': len(clean), 'chunks': pieces})
    return rows


def collect(lang):
    out = []
    for lesson in sorted(p for p in COURSE.glob('lesson-*') if p.is_dir()):
        src = lesson / SCRIPTS[lang]
        if src.is_file():
            out.append({'slug': lesson.name, 'jobs': lesson_rows(src, lang)})
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
           'tones': list(PRIORITY), 'moods': sorted(set(MOOD.values())),
           'instruct': INSTRUCT[a.lang],
           'note': ('본문에 태그는 없다. Base 체크포인트에는 감정 인자가 없어서 '
                    'mood 에 맞는 참조 음성의 말투로 감정을 낸다(ICL). instruct 는 '
                    '지시를 받는 체크포인트로 옮길 때 쓴다. '
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
    print('   토막 말투:')
    for name, n in Counter(c['tone'] for c in parts).most_common():
        print('     %-8s %4d  %4.1f%%  → %s' % (name, n, 100.0 * n / len(parts), MOOD[name]))
    print('   참조 음성이 맡는 몫:')
    for name, n in Counter(c['mood'] for c in parts).most_common():
        print('     %-9s 토막 %4d  %4.1f%%' % (name, n, 100.0 * n / len(parts)))
    over = [c for c in parts if len(c['text']) > hard]
    if over:
        print('   ! 상한 넘는 토막 %d개 (공백 없는 덩어리)' % len(over))
    return 0


if __name__ == '__main__':
    sys.exit(main())
