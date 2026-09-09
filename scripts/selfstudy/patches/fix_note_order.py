# -*- coding: utf-8 -*-
"""표가 다 채워지기 전에 아래 노트가 먼저 뜨던 것을 고친다.

검수 메모 12: "이 화면의 에니메이션 순서가 잘못됐어."

「오늘 친 것」 화면은 명령 표를 한 줄씩 채우고 맨 아래에 한 마디를 붙인다.
그런데 그 한 마디가 12번째 줄을 읽는 도중에 떠서, 아직 두 줄이 남았는데
마무리 말이 먼저 나왔다. 표 계열은 다시 잰 박자에 맞췄지만 `.note` 는
계열에 안 속해 손으로 넣은 시각 그대로 남아 있었다 — 113.00 처럼 딱 떨어지는
숫자가 그 흔적이다.

마지막 줄이 켜진 뒤로 옮긴다. 프레임이 끝나기 전이어야 하므로 마지막 줄의
구간 안에 넣는다.

    python fix_note_order.py [--dry]
"""
import io
import os
import re
import sys
import glob
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ROOT = os.path.join(REPO, 'projects', 'autocad-technician')
FAM = re.compile(r'#\w+ \.([a-z][a-z-]*?)(\d+)\b')
CALL = re.compile(r'tl\.(?:fromTo|to|from)\("(?P<sel>[^"]+)"(?P<mid>[^;]*?,\s*)'
                  r'(?P<time>[\d.]+)\s*\);', re.S)
# 계열에 안 속하고 화면 아래에 붙는 것들. 표가 다 차기 전에 뜨면 안 된다.
TAIL = re.compile(r'#\w+ \.(note\d*|tip\d*)$')


def main(dry=False):
    fixed = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'lesson-0*', 'compositions',
                                           'frames', '*.html'))):
        s0 = io.open(p, encoding='utf-8').read()
        if 'class="film"' in s0:
            continue
        calls = list(CALL.finditer(s0))
        fam = {}
        for m in calls:
            sel = m.group('sel')
            if ',' in sel:
                continue
            g = FAM.search(sel)
            if g:
                fam.setdefault(g.group(1), set()).add(int(g.group(2)))
        if not fam:
            continue
        key = max(fam, key=lambda k: len(fam[k]))
        if len(fam[key]) < 4:
            continue
        # 계열의 각 항이 켜지는 시각 — 같은 항의 두 번째 등장은 꺼짐이다.
        on, seen = {}, set()
        for m in sorted(calls, key=lambda x: float(x.group('time'))):
            sel = m.group('sel')
            if ',' in sel:
                continue
            g = FAM.search(sel)
            if not g or g.group(1) != key:
                continue
            i = int(g.group(2))
            if i not in seen:
                seen.add(i)
                on[i] = float(m.group('time'))
        order = sorted(on.items())
        first, last = order[0][1], order[-1][1]
        end = None
        for m in calls:
            if '.body' in m.group('sel') or '.topline,' in m.group('sel'):
                end = float(m.group('time'))
        room = (end if end else last + 6.0) - last

        stray = []
        for m in calls:
            sel = m.group('sel')
            if ',' in sel or not TAIL.search(sel):
                continue
            t = float(m.group('time'))
            if first < t < last:
                stray.append(m)
        if not stray:
            continue

        # 마지막 줄이 켜진 뒤, 프레임이 닫히기 전에 차례로 놓는다.
        step = max(0.6, min(2.0, room / (len(stray) + 1.0)))
        newt = {}
        for k, m in enumerate(sorted(stray, key=lambda x: float(x.group('time')))):
            newt[m.start()] = round(last + step * (k + 1), 2)

        out, prev = [], 0
        for m in calls:
            if m.start() not in newt:
                continue
            out.append(s0[prev:m.start('time')])
            out.append('%g' % newt[m.start()])
            prev = m.end('time')
        out.append(s0[prev:])
        s = ''.join(out)
        if not dry:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
        fixed += len(stray)
        print('  %s차시 %-22s .%s%d 뒤로: %s'
              % (p.split('lesson-')[1][:2], os.path.basename(p)[:-5], key, order[-1][0],
                 ', '.join('%s %.2f→%.2f' % (m.group('sel').split('.')[-1],
                                             float(m.group('time')), newt[m.start()])
                           for m in sorted(stray, key=lambda x: float(x.group('time'))))))
    print('\n옮긴 요소 %d개' % fixed)
    return 0


if __name__ == '__main__':
    sys.exit(main('--dry' in sys.argv))
