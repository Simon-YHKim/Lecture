# -*- coding: utf-8 -*-
"""낭독 대본에 문장마다 감정 태그를 달아 별도 파일로 낸다.

음성 복제 서비스에 넣을 판이다. 원본 `SCRIPT.md` 는 손대지 않는다 — 원본은
덱의 발표자 노트로도 실리고, 문단 수와 비트 번호가 화면·음성과 묶여 있다.

    python scripts/part/tts_script.py               여덟 차시 두 판 전부
    python scripts/part/tts_script.py <차시 디렉터리>  한 차시만

    <차시>/SCRIPT.md    →  <차시>/SCRIPT.tts.ko.md
    <차시>/SCRIPT.en.md →  <차시>/SCRIPT.tts.en.md

태그는 **문장이 무엇을 하는 문장인가**로 고른다. 손으로 사천 문장에 달면 아무도
다시 못 읽고, 대본을 한 줄 고칠 때마다 어긋난다. 규칙으로 달면 대본이 바뀌어도
다시 뽑으면 그만이고, 규칙 자체를 고쳐 전체를 한 번에 바꿀 수 있다.

**낭독되지 않는 것에는 태그를 달지 않는다.** 문단 첫머리의 `(1번 카드 …)` 는
화면의 몇 번째 항목을 가리키는 표식이고, `(무음)` 은 소리가 없다는 뜻이다.
둘 다 음성 엔진에 넘어가지 않으므로 그대로 둔다.
"""
import argparse
import io
import os
import re
import sys
from collections import Counter
from pathlib import Path

COURSE = Path('projects/autocad-technician')

# 태그말. 강의를 끌고 가는 여덟 가지 말투로 좁혔다. 종류가 많으면 목소리가
# 문장마다 튀어 한 사람이 말하는 것처럼 안 들린다.
TAGS = {
    'ko': {'calm': '차분하게', 'point': '짚어주듯', 'stress': '힘주어',
           'slow': '또박또박', 'ask': '묻듯이', 'warn': '주의를 주듯',
           'light': '가볍게', 'warm': '따뜻하게'},
    'en': {'calm': 'calm', 'point': 'pointing', 'stress': 'emphatic',
           'slow': 'measured', 'ask': 'asking', 'warn': 'cautionary',
           'light': 'light', 'warm': 'warm'},
}

HEAD = re.compile(r'^(#{1,4})\s')
STAGE = re.compile(r'^\s*\([^)]*\)\s*')
TICK = re.compile(r'`([^`]*)`')
SENT = re.compile(r'(?<=[.!?])\s+')
NUM = re.compile(r'\d')

# 문장이 무엇을 하는가. 위에서부터 먼저 맞는 것을 쓴다.
WARN_KO = re.compile(r'안 됩니다|안 돼요|하지 마|마세요|틀립니다|틀린|실수|주의|조심|'
                     r'잃|깨집니다|못 |없어집니다|사라집니다|위험')
WARN_EN = re.compile(r'\bdo not\b|\bnever\b|\bmust not\b|\bwrong\b|\bmistake\b|'
                     r'\bcareful\b|\bbreaks?\b|\bfails?\b|\blose\b', re.I)
ASK_KO = re.compile(r'\?|까요[.?]|나요[.?]|일까요|을까요|ㄹ까요')
ASK_EN = re.compile(r'\?')
STRESS_KO = re.compile(r'\*\*|반드시|절대|꼭 |가장 |한 번만|이것만|여기가')
STRESS_EN = re.compile(r'\*\*|\balways\b|\bnever\b|\bonly\b|\bmost\b|\bexactly\b', re.I)
WARM_KO = re.compile(r'고생하셨습니다|뵙겠습니다|반갑습니다|시작하겠습니다|잘 오셨')
WARM_EN = re.compile(r'\bwell done\b|\bsee you\b|\bwelcome\b', re.I)


def sentences(text):
    return [s for s in SENT.split(text.strip()) if s.strip()]


def pick(sentence, lang, in_step, pointing):
    """이 문장에 맞는 태그 이름."""
    warn, ask, stress, warm = ((WARN_KO, ASK_KO, STRESS_KO, WARM_KO) if lang == 'ko'
                               else (WARN_EN, ASK_EN, STRESS_EN, WARM_EN))
    if warm.search(sentence):
        return 'warm'
    if ask.search(sentence):
        return 'ask'
    if warn.search(sentence):
        return 'warn'
    # 실제로 치는 값이 든 문장. 잘못 들으면 그 단계가 통째로 어긋난다.
    # 녹화 구간이라고 전부 또박또박 읽으면 강의에 굴곡이 없어진다 — 값이 든
    # 문장만 고른다.
    digits = len(NUM.findall(sentence))
    if TICK.search(sentence) or digits >= (2 if in_step else 3):
        return 'slow'
    if stress.search(sentence):
        return 'stress'
    # 「엔터.」처럼 짧게 던지는 말. 차분하게 읽으면 늘어진다.
    short = len(sentence) <= 14 if lang == 'ko' else len(sentence.split()) <= 4
    if short:
        return 'light'
    if pointing:
        return 'point'
    return 'calm'


def convert(path, lang, counts):
    raw = path.read_bytes()
    text = raw.decode('utf-8').replace('\r\n', '\n')
    words = TAGS[lang]
    out, in_step = [], False
    for line in text.split('\n'):
        m = HEAD.match(line)
        if m:
            # `### 3단계` 안쪽은 실제로 조작하는 줄이다.
            in_step = len(m.group(1)) >= 3
            out.append(line)
            continue
        if not line.startswith('    '):
            out.append(line)
            continue
        body = line[4:]
        lead = ''
        stage = STAGE.match(body)
        if stage:
            # 화면 표식과 (무음) 은 읽히지 않는다. 그대로 두고 뒤부터 단다.
            lead = stage.group(0)
            body = body[stage.end():]
        if not body.strip():
            out.append(line)
            continue
        marked = []
        for i, s in enumerate(sentences(body)):
            # 화면 표식이 붙은 문단의 첫 문장이 「저기를 보라」는 문장이다.
            name = pick(s, lang, in_step, i == 0 and bool(lead))
            counts[name] += 1
            marked.append('[%s] %s' % (words[name], s))
        out.append('    ' + lead + ' '.join(marked))
    dest = path.with_name('SCRIPT.tts.%s.md' % lang)
    note = ('<!-- 생성물이다. 손으로 고치지 말고 원본 %s 를 고친 뒤 다시 뽑아라.\n'
            '     python scripts/part/tts_script.py %s\n'
            '     태그: %s -->\n'
            % (path.name, path.parent.name, ' · '.join(sorted(words.values()))))
    with io.open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(note + '\n'.join(out))
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('lesson', nargs='?', help='한 차시만 (비우면 여덟 차시)')
    a = ap.parse_args(argv)
    lessons = ([Path(a.lesson)] if a.lesson
               else sorted(p for p in COURSE.glob('lesson-*') if p.is_dir()))
    counts = Counter()
    made = 0
    for lesson in lessons:
        for name, lang in (('SCRIPT.md', 'ko'), ('SCRIPT.en.md', 'en')):
            src = lesson / name
            if not src.is_file():
                continue
            convert(src, lang, counts)
            made += 1
    total = sum(counts.values())
    print('태그본 %d개 · 문장 %d개' % (made, total))
    for key in ('calm', 'slow', 'point', 'stress', 'warn', 'ask', 'light', 'warm'):
        if counts[key]:
            print('   %-8s %5d  %4.1f%%' % (key, counts[key], 100.0 * counts[key] / total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
