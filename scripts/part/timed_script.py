# -*- coding: utf-8 -*-
"""대본에 **문단마다 실측 시각**을 달아 검토용 판을 낸다.

원본 대본의 `**Time:**` 은 Line 단위다 — 한 줄이 3분이면 그 안에서 어느 말이
언제 나오는지 알 수 없다. 검토자가 호흡과 분량을 보려면 문단마다 시각이 있어야
한다. 그 값은 추정이 아니라 합친 음성을 다시 재서 얻은 것이고
`narration-timing.json` 에 들어 있다.

    python scripts/part/timed_script.py                여덟 차시 두 판
    python scripts/part/timed_script.py --lang en --root <영문 사본 묶음>

    <차시>/SCRIPT.timed.ko.md      원본에 [m:ss–m:ss] 를 얹은 것

생성물이다. 원본을 고친 뒤 다시 뽑는다. 여기서 대본을 고치면 안 된다.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import narrate_tts as N

COURSE = HERE.parents[1] / 'projects' / 'autocad-technician'
SCRIPTS = {'ko': 'SCRIPT.md', 'en': 'SCRIPT.en.md'}
HEAD = re.compile(r'^##\s+Line\s+(\d+)')


def clock(seconds):
    m, s = divmod(int(round(seconds)), 60)
    return '%d:%02d' % (m, s)


def spans_by_key(timing):
    """{열쇠: (시작, 끝)} — 프레임 시작을 더한 전체 시간축의 값."""
    out = {}
    for frame in timing['frames']:
        base = float(frame['start'])
        for unit in frame['units']:
            out.setdefault(frame['id'], []).append(
                (base + float(unit['start']), base + float(unit['end'])))
    return out


def convert(lesson, lang, script_name):
    src = lesson / script_name
    timing_path = lesson / 'narration-timing.json'
    if not src.is_file() or not timing_path.is_file():
        return None
    timing = json.loads(timing_path.read_text(encoding='utf-8'))
    jobs, units, order = N.synthesis_plan(str(src))
    # 시각은 프레임 순서대로 쌓여 있다. 같은 순서로 열쇠에 붙인다.
    times, i = {}, 0
    for seq, (line_no, part, _fid) in enumerate(order):
        frame = timing['frames'][seq]
        base = float(frame['start'])
        for (key, _beat), unit in zip(units[(line_no, part)], frame['units']):
            times[key] = (base + float(unit['start']), base + float(unit['end']))
        i += 1

    text = src.read_text(encoding='utf-8').replace('\r\n', '\n')
    keys = [k for k, _ in jobs]
    out, cursor = [], 0
    for line in text.split('\n'):
        if line.startswith('    ') and line.strip():
            body = line[4:]
            if N.speakable(body) and cursor < len(keys):
                a, b = times.get(keys[cursor], (0.0, 0.0))
                out.append('    `[%s–%s]` %s' % (clock(a), clock(b), body))
                cursor += 1
                continue
        out.append(line)
    if cursor != len(keys):
        raise SystemExit('%s: 문단 %d개에 시각 %d개가 붙었다' % (lesson.name, len(keys), cursor))

    dest = lesson / ('SCRIPT.timed.%s.md' % lang)
    note = ('<!-- 생성물이다. 손으로 고치지 말고 원본 %s 를 고친 뒤 다시 뽑아라.\n'
            '     python scripts/part/timed_script.py\n'
            '     `[m:ss–m:ss]` 는 합친 음성을 다시 재서 얻은 실측 시각이다.\n'
            '     전체 %s · 문단 %d개 -->\n\n'
            % (script_name, clock(timing['totalSeconds']), len(keys)))
    with io.open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(note + '\n'.join(out))
    return dest, len(keys), timing['totalSeconds']


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'))
    ap.add_argument('--root', default=None, help='영문은 저장소 밖 사본 묶음')
    ap.add_argument('--script', default=None, help='사본 안에서 읽을 대본 이름')
    a = ap.parse_args(argv)

    root = Path(a.root) if a.root else COURSE
    name = a.script or ('SCRIPT.md' if a.root else SCRIPTS[a.lang])
    made = 0
    for lesson in sorted(p for p in root.glob('lesson-*') if p.is_dir()):
        got = convert(lesson, a.lang, name)
        if got:
            dest, n, total = got
            print('%-34s 문단 %3d · %s' % (lesson.name, n, clock(total)))
            made += 1
    print('시각본 %d개' % made)
    return 0


if __name__ == '__main__':
    sys.exit(main())
