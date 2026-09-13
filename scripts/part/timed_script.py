# -*- coding: utf-8 -*-
"""대본에 **합성 단위별 실측 시각**을 달아 검토용 판을 낸다.

원본 대본의 `**Time:**` 은 Line 단위다 — 한 줄이 3분이면 그 안에서 어느 말이
언제 나오는지 알 수 없다. 일반 구간은 문단 첫 줄에 시각을 붙인다. 녹화 구간은
여러 문단을 한 단계로 합성하므로 단계 제목 아래에 **단계 전체** 시각만 붙인다.
개별 문단의 시각을 추정하지 않는다. 실측값은 `narration-timing.json` 에 있다.

    python scripts/part/timed_script.py                여덟 차시 국문
    python scripts/part/timed_script.py --lang en --root <영문 사본 묶음>

    <차시>/SCRIPT.timed.ko.md      원본에 [m:ss–m:ss] 를 얹은 것

생성물이다. 원본을 고친 뒤 다시 뽑는다. 여기서 대본을 고치면 안 된다.
"""
import argparse
import io
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import narrate_tts as N

COURSE = HERE.parents[1] / 'projects' / 'autocad-technician'
SCRIPTS = {'ko': 'SCRIPT.md', 'en': 'SCRIPT.en.md'}
HEAD = N.beats._LINE_HEAD


def clock(seconds):
    m, s = divmod(int(round(seconds)), 60)
    return '%d:%02d' % (m, s)


def source_units(text):
    """합성 입력에 대응하는 (삽입할 줄, 단계 여부, 읽을 글).

    단계는 parse_steps처럼 묶고, 나머지는 빈 줄로 나눈 문단으로 묶는다.
    convert에서 synthesis_plan과 글자까지 대조하므로 파서가 달라지면 멈춘다.
    """
    lines = text.split('\n')
    heads = [i for i, line in enumerate(lines) if HEAD.match(line)]
    out = []
    for start, end in zip(heads, heads[1:] + [len(lines)]):
        steps = [i for i in range(start + 1, end) if N.beats._STEP_HEAD.match(lines[i])]
        if steps:
            for first, last in zip(steps, steps[1:] + [end]):
                body = ' '.join(line.strip() for line in lines[first + 1:last]
                                if line.startswith(('    ', '\t')))
                if N.speakable(body):
                    out.append((first, True, N.speakable(body)))
        else:
            paragraph = []
            for i in range(start + 1, end + 1):
                if i == end or not lines[i].strip():
                    if paragraph:
                        raw = ' '.join(lines[j].strip() for j in paragraph)
                        body = '' if raw.startswith('>') else N.speakable(raw)
                        if body:
                            out.append((paragraph[0], False, body))
                        paragraph = []
                elif lines[i].startswith(('    ', '\t')):
                    paragraph.append(i)
    return out


def convert(lesson, lang, script_name):
    src = lesson / script_name
    timing_path = lesson / 'narration-timing.json'
    if not src.is_file() or not timing_path.is_file():
        return None
    timing = json.loads(timing_path.read_text(encoding='utf-8'))
    if timing.get('spokenTextSha256') != N.spoken_hash(str(src)):
        raise ValueError('%s: 대본/음성 해시 불일치. 해당 언어의 실측 시각이 필요합니다.' % lesson.name)
    jobs, units, order = N.synthesis_plan(str(src))
    if len(timing['frames']) != len(order):
        raise ValueError('%s: 프레임 수 불일치' % lesson.name)
    times = {}
    for seq, (line_no, part, fid) in enumerate(order):
        frame = timing['frames'][seq]
        if frame['id'] != fid or frame['line'] != line_no:
            raise ValueError('%s: 프레임 식별정보 불일치' % lesson.name)
        if len(frame['units']) != len(units[(line_no, part)]):
            raise ValueError('%s: 합성 단위 수 불일치' % lesson.name)
        base = float(frame['start'])
        previous = 0.0
        for (key, beat), unit in zip(units[(line_no, part)], frame['units']):
            a, b = float(unit['start']), float(unit['end'])
            if (unit['beat'] != beat or not all(math.isfinite(v) for v in (base, a, b))
                    or base < 0 or a < previous or b <= a):
                raise ValueError('%s: 합성 단위 시각/비트 불일치' % lesson.name)
            times[key] = (base + a, base + b)
            previous = b

    text = src.read_text(encoding='utf-8').replace('\r\n', '\n')
    targets = source_units(text)
    if [body for _, _, body in targets] != [body for _, body in jobs]:
        raise ValueError('%s: 원본 위치와 합성 단위 대응 불일치' % lesson.name)
    inserts = {index: (step, times[key])
               for (index, step, _), (key, _) in zip(targets, jobs)}
    out = []
    for index, line in enumerate(text.split('\n')):
        if index in inserts:
            step, (a, b) = inserts[index]
            stamp = '`[%s–%s]`' % (clock(a), clock(b))
            if step:
                label = '단계 전체 · 개별 문단 시각 아님' if lang == 'ko' else 'entire step; not individual paragraph times'
                out.extend([line, '> <!-- timed-step --> %s %s' % (stamp, label)])
            else:
                indent = line[:len(line) - len(line.lstrip())]
                out.append(indent + stamp + ' ' + line[len(indent):])
            continue
        out.append(line)

    dest = lesson / ('SCRIPT.timed.%s.md' % lang)
    note = ('<!-- 생성물이다. 손으로 고치지 말고 원본 %s 를 고친 뒤 다시 뽑아라.\n'
            '     python scripts/part/timed_script.py\n'
            '     일반 구간은 문단, 녹화 구간은 단계 전체의 실측 시각이다.\n'
            '     음성 연결 시간축 기준이다. 화면 유지 시간을 포함한 **Time:** 과는 다르다.\n'
            '     전체 %s · 합성 단위 %d개 -->\n\n'
            % (script_name, clock(timing['totalSeconds']), len(jobs)))
    with io.open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(note + '\n'.join(out))
    return dest, len(jobs), timing['totalSeconds']


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
            print('%-34s 합성 단위 %3d · %s' % (lesson.name, n, clock(total)))
            made += 1
    print('시각본 %d개' % made)
    return 0


if __name__ == '__main__':
    sys.exit(main())
