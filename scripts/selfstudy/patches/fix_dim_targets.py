# -*- coding: utf-8 -*-
"""치수 강조가 엉뚱한 것을 가리키던 것을 고친다.

검수에서 나온 여섯 건은 원인이 둘이다.

  · 강조가 너무 넓다 — 「60·62 보스 중심 위치」에서 부품 바깥 윤곽이 통째로
    붉어진다. 재는 것은 중심의 위치인데 중심선은 그대로 두고 외형을 칠하니
    무엇을 보라는 것인지 알 수 없다. 「26 필렛 중심」도, 「16 베이스 높이」도
    같은 겹선 하나를 나눠 쓰고 있었다.
  · 강조가 남의 박자에 켜진다 — 표의 행과 도면의 치수선이 서로 다른 시각표를
    쓰고 있어서, 「8 장공 중심 높이」를 읽는 동안 옆의 26이 먼저 켜진다.

여기서는 첫째만 다룬다. 겹선을 형상별로 쪼개고, 각 트윈이 자기 치수가 재는
곳을 가리키게 한다. 어느 치수가 어디를 재는지는 도면에 적힌 사실이라 짐작이
아니다. 둘째(시각)는 retime_frames.py 가 맡는다.

    python fix_dim_targets.py [--dry]
"""
import io
import os
import re
import sys
import glob
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ROOT = os.path.join(REPO, 'projects', 'autocad-technician')

# 치수 이름 → 그 치수가 재고 있는 곳.
DIM2HL = {
    'w120': 'profile', 'h90': 'profile',      # 전체 크기 — 바깥 윤곽 전부
    'c60': 'bossc', 'c62': 'bossc', 'a45': 'bossc',   # 보스 중심의 위치 — 중심선
    'h16': 'basehl', 'c5': 'basehl',          # 베이스 높이·모따기 — 베이스 윤곽
    'w80': 'neck',                            # 목 밑동 폭 — 목과 그 밑 라운드
    'r10': 'fillet',                          # 라운드 반지름 — 호 자체
    'f26': 'filletc', 'f95': 'filletc',       # 필렛 중심 — 십자 중심선
    's29': 'slot', 's50': 'slot', 's12': 'slot', 'sr5': 'slot',
    's8': 'slotc',                            # 장공 중심 높이 — 장공 중심선
    't12': 'thick', 't20': 'thick',           # 두께 — 옆면도
    'd25': 'bore', 'd56': 'boss',
    'pcd': 'tap', 'm5': 'tap',
}

# 새로 만들 겹선. (형상 이름, 원본을 찾는 정규식, 원본에서 겹선으로 바꾸는 법)
# 좌표를 다시 계산하지 않고 이미 그려진 것을 그대로 복제하므로 형상과 어긋날 수 없다.
CLONES = [
    ('basehl',  r'<path class="hl" data-feature="profile" d="M63\.000 192\.000[^"]*"/>'),
    ('neck',    r'<path class="hl" data-feature="profile" d="M156\.143[^"]*"/>'),
    ('neck',    r'<path class="hl" data-feature="profile" d="M90\.793[^"]*"/>'),
    ('neck',    r'<path class="hl" data-feature="fillet" d="[^"]*"/>'),
    ('filletc', r'<line class="center" data-feature="fillet"[^>]*/>'),
    ('bossc',   r'<line class="center" data-feature="bore"[^>]*/>'),
    ('slotc',   r'<line class="center" data-feature="slot"[^>]*/>'),
    ('thick',   r'<path class="outline" d="M58\.000 76\.000[^"]*"/>'),
    ('thick',   r'<path class="outline" d="M90\.000 84\.000[^"]*"/>'),
]

LAST_HL = re.compile(r'<(?:circle|path|line) class="hl"[^>]*/>')
TWEEN = re.compile(r'tl\.(?:fromTo|to|from)\("(?P<sel>[^"]+)"', re.S)
DIMNAME = re.compile(r"\[data-dim='([a-z0-9]+)'\]")


def clones_for(svg):
    out, seen = [], set()
    for feat, pat in CLONES:
        for m in re.finditer(pat, svg):
            el = m.group(0)
            el = re.sub(r'class="(?:hl|center|outline)"', 'class="hl"', el, count=1)
            el = re.sub(r'data-feature="[a-z]+"', 'data-feature="%s"' % feat, el, count=1)
            if 'data-feature=' not in el:
                el = el.replace('class="hl"', 'class="hl" data-feature="%s"' % feat, 1)
            if el not in seen:
                seen.add(el)
                out.append(el)
    return out


def main(dry=False):
    total_add = total_fix = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'lesson-0*', 'compositions',
                                           'frames', '*.html'))):
        s0 = io.open(p, encoding='utf-8').read()
        if "data-dim='w120'" not in s0 and 'data-dim="w120"' not in s0:
            continue
        s = s0

        # ── 겹선을 형상별로 쪼갠다 ────────────────────────────────
        add = [e for e in clones_for(s) if e not in s]
        if add:
            hits = list(LAST_HL.finditer(s))
            at = hits[-1].end()
            s = s[:at] + ''.join(add) + s[at:]

        # ── 트윈이 자기 치수가 재는 곳을 가리키게 한다 ────────────
        # 파일 안에서 치수선 트윈이 먼저 오고 겹선 트윈이 뒤따른다. 바로 앞의
        # 치수 이름이 이 겹선이 무엇을 위한 것인지 말해 준다.
        fid = re.search(r'#(\w+) \.', s)
        fid = fid.group(1) if fid else None
        pending, fixed, orphan = None, 0, 0
        pieces, last = [], 0
        for m in TWEEN.finditer(s):
            sel = m.group('sel')
            names = DIMNAME.findall(sel)
            if names and 'text[' not in sel:
                pending = names
                continue
            if '.hl[data-feature=' not in sel:
                continue
            if not pending or not fid:
                orphan += 1
                continue
            # 그 프레임에 실제로 있는 형상만 가리킨다. 3차시 도면에는 옆면도가
            # 없어 두께를 가리킬 곳이 없다 — 없는 것을 부르면 트윈이 헛돈다.
            here = set(__import__('re').findall(r'class="hl" data-feature="([a-z0-9]+)"', s))
            want, seen = [], set()
            for n in pending:
                f = DIM2HL.get(n)
                if f and f in here and f not in seen:
                    seen.add(f)
                    want.append(f)
            if not want:
                orphan += 1
                continue
            new = ','.join("#%s .hl[data-feature='%s']" % (fid, f) for f in want)
            if new != sel:
                a, b = m.start('sel'), m.end('sel')
                pieces.append(s[last:a])
                pieces.append(new)
                last = b
                fixed += 1
        if pieces:
            pieces.append(s[last:])
            s = ''.join(pieces)

        if s != s0:
            total_add += len(add)
            total_fix += fixed
            if not dry:
                io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
            tag = p.split('lesson-')[1].replace(os.sep + 'compositions' + os.sep + 'frames' + os.sep, ' / ')
            print('  %-46s 겹선 +%-3d 트윈 %-3d%s'
                  % (tag, len(add), fixed, '  대상 못 찾음 %d' % orphan if orphan else ''))
    print('\n겹선 %d개 추가 · 트윈 %d개 재조준' % (total_add, total_fix))
    return 0


if __name__ == '__main__':
    sys.exit(main('--dry' in sys.argv))
