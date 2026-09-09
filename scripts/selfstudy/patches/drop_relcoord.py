# -*- coding: utf-8 -*-
"""상대좌표로 그리던 자리를 마우스·스냅·수치입력으로 바꾼다.

검수 메모 16: "베이스를 먼저 그린 다음에 chamfer 명령어를 사용해서 모따기를
해야해. 그리고 모든 슬라이드에 걸쳐서 '@'를 사용했는데, 이러면 안돼."

바꾸는 방법은 자리마다 다르다.

  · 한 축으로만 떨어진 자리 (`@0,-5`, `@40,0`) — 직교를 켜고 커서로 방향을
    정한 뒤 거리만 친다. FROM 은 그대로 쓴다. 기준점에서 떨어진 자리를 찍는
    기능 자체는 스냅으로 잡은 점을 쓰므로 좌표가 아니다.
  · 두 축으로 떨어진 자리 (`@29,8`, `@-33,62`) — 잡을 것이 없어서 좌표를
    썼던 자리다. 잡을 것을 만든다. 이미 있는 변을 OFFSET 해서 만나게 하고
    그 교차점을 스냅으로 집은 뒤 보조선을 지운다. 사각형이면 MOVE 로 옮긴다.
  · 사각형 (`@-200,30`, `@120,0`부터 시작하는 베이스 외곽) — REC 의 치수(D)
    옵션. 길이와 폭을 숫자로 주고 방향만 마우스로 정한다. 모따기는 그리는
    중에 넣지 않고 CHAMFER 로 따로 낸다.

    python drop_relcoord.py [--dry]
"""
import io
import json
import os
import re
import sys
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SRC = os.path.join(REPO, 'scripts', 'selfstudy', 'source')


def bi(k, e):
    return {'ko': k, 'en': e}


def act(kind, ko, en, typ=None):
    a = {'kind': kind, 'do': bi(ko, en)}
    if typ:
        a['type'] = typ
    return a


def load(n):
    return json.load(io.open(os.path.join(SRC, 'lesson-%02d.json' % n), encoding='utf-8'))


def dump(n, d, dry):
    if not dry:
        io.open(os.path.join(SRC, 'lesson-%02d.json' % n), 'w', encoding='utf-8',
                newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1))


def at(d, path):
    o = d
    for k in path:
        o = o[k]
    return o


# ── 2차시 · 표제란 ────────────────────────────────────────────
def lesson2(d, log):
    st = at(d, ['sections', 11, 'blocks', 1, 'items', 2])
    i = next(k for k, a in enumerate(st['actions']) if a.get('type') == '@-200,30')
    st['actions'][i:i + 1] = [
        act('type', '입력하고 엔터. 치수 옵션입니다. 반대 구석을 찍는 대신 '
                    '가로세로를 숫자로 주겠다는 뜻이에요.',
            'then Enter. The Dimensions option: instead of clicking the far corner '
            'you give the two sizes as numbers.', 'D'),
        act('type', '가로를 묻습니다. 입력하고 엔터.',
            'It asks for the length. Type it and press Enter.', '200'),
        act('type', '세로를 묻습니다. 입력하고 엔터.',
            'It asks for the width. Type it and press Enter.', '30'),
        act('move', '이제 방향만 남았습니다. 커서를 그 모서리의 왼쪽 위로 옮기면 '
                    '사각형이 그쪽으로 미리 보입니다.',
            'Only the direction is left. Move the cursor up and to the left of that '
            'corner and the rectangle previews that way.'),
        act('click', '클릭합니다. 가로 200, 세로 30 사각형이 도면선 오른쪽 아래에 붙습니다.',
            'Click. A 200 by 30 rectangle lands on the lower-right corner of the border.'),
    ]
    log.append('2차시 표제란 — REC 치수 옵션으로')


# ── 3차시 · 베이스 외곽 · 중심선 · 목 접선 ─────────────────────
def lesson3(d, log):
    st = at(d, ['sections', 6, 'blocks', 0, 'items', 3])
    st['title'] = bi('베이스 외곽 — 사각형을 먼저, 모따기는 나중에',
                     'The base outline - rectangle first, chamfers after')
    st['actions'] = [
        act('type', '입력하고 엔터. 사각형 명령이에요.',
            'then Enter. The rectangle command.', 'REC'),
        act('ask', '첫 번째 구석점을 묻습니다.', 'It asks for the first corner.'),
        act('click', '확대해 둔 자리의 왼쪽 아래쯤을 그냥 클릭합니다. '
                     '여기가 베이스의 왼쪽 아래 구석이 됩니다.',
            "Just click near the lower left of the area you zoomed into. That becomes "
            "the base's lower-left corner."),
        act('see', '이 점의 절대 위치는 도면 치수가 아닙니다. 부품이 도면틀 안에 '
                   '들어갈 자리인지만 봅니다.',
            'Where this point sits is not a dimension. All that matters is that the '
            'part will land inside the border.'),
        act('type', '입력하고 엔터. 치수 옵션입니다. 반대 구석을 찍는 대신 '
                    '가로세로를 숫자로 줍니다.',
            'then Enter. The Dimensions option: give the two sizes as numbers instead '
            'of clicking the far corner.', 'D'),
        act('type', '가로를 묻습니다. 베이스 폭이에요. 입력하고 엔터.',
            'It asks for the length - the base width. Type it and press Enter.', '120'),
        act('type', '세로를 묻습니다. 베이스 높이예요. 입력하고 엔터.',
            'It asks for the width - the base height. Type it and press Enter.', '16'),
        act('move', '커서를 그 점의 오른쪽 위로 옮깁니다. 사각형이 그쪽으로 미리 보여요.',
            'Move the cursor up and to the right. The rectangle previews that way.'),
        act('click', '클릭합니다. 120 × 16 사각형이 생깁니다. 모따기는 아직 없습니다.',
            'Click. A 120 by 16 rectangle appears. No chamfers yet.'),
        act('type', '입력하고 엔터. 모따기 명령이에요.',
            'then Enter. The chamfer command.', 'CHA'),
        act('type', '입력하고 엔터. 거리 옵션입니다.',
            'then Enter. The Distance option.', 'D'),
        act('type', '첫 번째 거리를 묻습니다. 입력하고 엔터.',
            'It asks for the first distance. Type it and press Enter.', '5'),
        act('type', '두 번째 거리를 묻습니다. 같은 값이라 그냥 엔터를 눌러도 됩니다.',
            'It asks for the second distance. It is the same, so Enter alone will do.', '5'),
        act('click', '왼쪽 위 구석을 이루는 두 변을 차례로 클릭합니다. '
                     '윗변 먼저, 왼쪽 변 다음이에요. 순서는 상관없습니다.',
            'Click the two edges that meet at the top-left corner - the top edge, then '
            'the left edge. The order does not matter.'),
        act('see', '구석이 45도로 잘립니다. 가로 5 세로 5라 정확히 45도예요.',
            'The corner is cut at 45 degrees. Five across and five up is exactly 45.'),
        act('type', '다시 입력하고 엔터. 거리는 그대로 5, 5 로 남아 있습니다.',
            'Run it again. The distances are still 5 and 5.', 'CHA'),
        act('click', '오른쪽 위 구석의 두 변을 클릭합니다. 이제 여섯 변짜리 윤곽입니다.',
            'Click the two edges at the top-right corner. Now the outline has six edges.'),
        act('alt', '두 구석을 한 번에 하려면 `CHA` 에서 `P` 를 누르고 사각형을 클릭합니다. '
                   '다만 이러면 네 구석이 전부 잘려요. 아래 두 구석은 살려야 하니 여기서는 '
                   '하나씩 집습니다.',
            'To do both at once press `P` in `CHA` and click the rectangle - but that '
            'chamfers all four corners. The bottom two must stay square, so pick them '
            'one at a time here.'),
    ]
    st['expect'] = bi('여섯 변이 한 바퀴 돌아 닫힌 윤곽이 됩니다. 위 두 구석만 잘려 있어요.',
                      'Six edges close into one ring, with only the top two corners cut.')
    st['why'] = bi('사각형은 도면에 적힌 120과 16 두 숫자면 끝납니다. 모따기를 그리는 '
                   '중에 넣으려면 11이니 110이니 하는 계산한 값이 필요한데, 그 값은 도면에 '
                   '없어요. 나중에 CHAMFER 로 내면 도면에 적힌 5와 5를 그대로 씁니다.',
                   'The rectangle needs only the two numbers the drawing gives: 120 and 16. '
                   'Cutting the chamfers as you draw would need 11 and 110 - values the '
                   'drawing never states. Chamfering afterwards uses the 5 and 5 it does.')
    st['pitfall'] = bi('모따기가 안 들어가면 거리가 0일 때가 많습니다. `CHA` 를 누르고 '
                       '명령행에 「거리1 = 0.0000」 이 보이면 `D` 로 다시 5, 5 를 넣습니다. '
                       '아래 구석까지 잘렸다면 `P` 옵션으로 사각형 전체를 집은 겁니다.',
                       'A chamfer that does nothing usually means the distance is zero: '
                       'run `CHA` and if the prompt reads "Dist1 = 0.0000", set 5 and 5 '
                       'again with `D`. If the bottom corners were cut too, you picked the '
                       'whole rectangle with the `P` option.')
    st['spots'] = [
        {'x': 0, 'y': 0, 'hover': bi('여기쯤을 클릭합니다. 자리는 자유예요',
                                     'Click about here. The position is yours to choose')},
        {'x': 0, 'y': 16, 'snap': 'end',
         'hover': bi('왼쪽 위 구석 — 여기 두 변을 집어 모따기',
                     'Top-left corner - chamfer these two edges')},
        {'x': 120, 'y': 16, 'snap': 'end',
         'hover': bi('오른쪽 위 구석 — 같은 방법으로',
                     'Top-right corner - the same again')},
    ]
    log.append('3차시 4단계 — 사각형 + CHAMFER 로 다시 씀')

    # 세로 중심선 — 한 축이라 직교 + 거리로 충분하다.
    st = at(d, ['sections', 7, 'blocks', 0, 'items', 1])
    i = next(k for k, a in enumerate(st['actions']) if a.get('type') == '@0,-5')
    st['actions'][i:i + 1] = [
        act('move', '커서를 그 점보다 아래에 둡니다. 직교가 켜져 있어 아래로 고정돼요.',
            'Put the cursor below that point. With ortho on it locks downward.'),
        act('type', '입력하고 엔터. 기준점에서 아래로 5입니다. 중심선이 형상 밖으로 '
                    '나오는 몫이에요. 방향은 커서가, 거리는 숫자가 정합니다.',
            'then Enter. Five below the base point - how far the centerline runs past '
            'the shape. The cursor gives the direction, the number the distance.', '5'),
    ]
    log.append('3차시 세로 중심선 — 직교 + 거리')

    # 가로 중심선 — 두 축이라 잡을 것이 없다. 66 짜리 선을 만들어 옮긴다.
    st = at(d, ['sections', 7, 'blocks', 0, 'items', 2])
    st['title'] = bi('가로 중심선 — 길이부터 만들고 자리로 옮기기',
                     'The horizontal centerline - make the length, then move it home')
    st['actions'] = [
        act('type', '입력하고 엔터.', 'then Enter.', 'L'),
        act('click', '빈 자리를 아무 데나 클릭합니다. 길이부터 만들 거예요.',
            'Click anywhere empty. You are making the length first.'),
        act('move', '직교를 켠 채 커서를 오른쪽으로 끕니다.',
            'With ortho on, drag the cursor to the right.'),
        act('type', '입력하고 엔터, 다시 엔터. 33의 두 배입니다. 원 반지름 28에 '
                    '내미는 5를 더한 값이 33이에요.',
            'then Enter, and Enter again. Twice 33 - the 28 radius plus the 5 it runs '
            'past.', '66'),
        act('type', '입력하고 엔터. 이동 명령이에요.',
            'then Enter. The move command.', 'M'),
        act('click', '방금 그린 선을 클릭하고 엔터.',
            'Click the line you just drew, then Enter.'),
        act('move', '기준점을 묻습니다. 커서를 그 선의 한가운데에 올립니다.',
            'It asks for a base point. Hover over the middle of that line.'),
        act('snap', '세모 표식이 뜨면 클릭합니다. 중간점이에요.',
            'Click when the triangle shows - the midpoint.'),
        act('type', '두 번째 점에서 입력하고 엔터. 스냅으로 잡은 점에서 떨어진 자리를 '
                    '찍겠다는 뜻입니다.',
            'At the second point type this and press Enter: it places a point measured '
            'from one you snap to.', 'FROM'),
        act('move', '커서를 세로 중심선과 베이스 밑변이 만나는 자리에 올립니다.',
            'Hover where the vertical centerline crosses the base bottom.'),
        act('snap', '가위표 표식이 뜨면 클릭합니다. 교차점이에요.',
            'Click when the cross shows - the intersection.'),
        act('move', '커서를 그 점보다 위에 둡니다. 직교가 수직으로 잡아 줍니다.',
            'Put the cursor above that point; ortho holds it vertical.'),
        act('type', '입력하고 엔터. 보스 중심 높이입니다. 선의 한가운데가 그 자리에 '
                    '가서 앉습니다.',
            'then Enter - the boss center height. The middle of the line lands there.',
            '62'),
    ]
    st['expect'] = bi('길이 66짜리 가로 중심선이 보스 중심 높이에 좌우 대칭으로 놓입니다.',
                      'A 66-long horizontal centerline sits at the boss center height, '
                      'even on both sides.')
    st['why'] = bi('중심에서 왼쪽으로 33 떨어진 자리에는 잡을 것이 없습니다. 없는 자리를 '
                   '좌표로 부르는 대신, 길이를 먼저 만들고 그 중간점을 잡아 옮깁니다. '
                   '중간점은 스냅이 잡아 주니 좌우가 저절로 같아져요.',
                   'There is nothing to snap to 33 left of the center. Rather than naming '
                   'that spot with coordinates, make the length first and move it by its '
                   'midpoint. The snap finds the midpoint, so both sides come out equal.')
    st['pitfall'] = bi('한쪽이 길면 기준점을 중간점이 아니라 끝점으로 잡은 겁니다. '
                       '세모 표식과 네모 표식을 구분해서 누르세요.',
                       'One side longer means you grabbed an endpoint instead of the '
                       'midpoint. Watch for the triangle, not the square.')
    log.append('3차시 가로 중심선 — 길이 먼저, 중간점으로 이동')

    # 목 접선 — 한 축이라 직교 + 거리
    for idx, side, dirn, dirn_en in ((2, '왼쪽', '왼쪽', 'left'), (3, '오른쪽', '오른쪽', 'right')):
        st = at(d, ['sections', 8, 'blocks', 0, 'items', idx])
        i = next((k for k, a in enumerate(st['actions'])
                  if str(a.get('type', '')).startswith('@')), None)
        if i is None:
            continue
        st['actions'][i:i + 1] = [
            act('move', '커서를 그 점의 %s에 둡니다. 직교가 수평으로 잡아 줍니다.' % dirn,
                'Put the cursor to the %s of that point; ortho holds it level.' % dirn_en),
            act('type', '입력하고 엔터. 밑동 80의 절반입니다. 방향은 커서가 정하고 '
                        '숫자는 거리만 줍니다.',
                'then Enter - half of the 80 root width. The cursor gives the direction, '
                'the number only the distance.', '40'),
        ]
    st = at(d, ['sections', 8, 'blocks', 0, 'items', 3])
    st['pitfall'] = bi('두 선이 달라 보이면 시작점부터 봅니다. 기준점이 같은 교차점이었는지, '
                       '커서를 반대쪽에 두고 40을 쳤는지 확인해요.',
                       'If they differ, check the start points: the same intersection as '
                       'base point, and the cursor on the correct side when you typed 40.')
    at(d, ['verify', 5])['how'] = bi(
        '세로 중심선을 기준으로 좌우 대칭인지 봅니다. 한쪽만 기울기가 다르면 기준으로 삼은 '
        '교차점과 40을 칠 때 커서가 어느 쪽에 있었는지 다시 봅니다.',
        'Check they mirror about the vertical centerline. If one slope differs, check the '
        'intersection you stepped off from and which side the cursor was on for the 40.')
    log.append('3차시 목 접선 두 개 — 직교 + 거리')


# ── 4차시 · 장공 끝원 · 45도 보조선 ────────────────────────────
def lesson4(d, log):
    st = at(d, ['sections', 7, 'blocks', 1, 'items', 0])
    i = next(k for k, a in enumerate(st['actions']) if a.get('type') == '@29,8')
    # 잡을 것이 없으면 만든다. 이미 있는 두 변을 옮겨 만나게 한다.
    st['actions'][:i + 1] = [
        act('see', '도면층(레이어)이 외형선인지 확인합니다.',
            'Check the current layer is the visible-outline layer.'),
        act('see', '장공 중심은 베이스 왼쪽 아래 구석에서 오른쪽 29, 위 8입니다. '
                   '그 자리에는 잡을 것이 없어요. 그래서 잡을 것을 먼저 만듭니다.',
            "The slot center is 29 right and 8 up from the base's lower-left corner. "
            'There is nothing to snap to there, so make something first.'),
        act('type', '입력하고 엔터. 간격 띄우기 명령이에요.',
            'then Enter. The offset command.', 'O'),
        act('type', '거리를 묻습니다. 입력하고 엔터.',
            'It asks for the distance. Type it and press Enter.', '8'),
        act('click', '베이스 밑변을 클릭하고, 그 위쪽을 한 번 더 클릭합니다. '
                     '밑변이 8만큼 위로 복사됩니다.',
            'Click the base bottom edge, then click above it. The edge is copied 8 up.'),
        act('type', '엔터로 명령을 되부르고 거리를 다시 줍니다. 입력하고 엔터.',
            'Press Enter to repeat the command and give a new distance.', '29'),
        act('click', '베이스 왼쪽 변을 클릭하고, 그 오른쪽을 한 번 더 클릭합니다.',
            'Click the base left edge, then click to the right of it.'),
        act('see', '보조선 두 개가 만나는 자리가 장공 왼쪽 끝원의 중심입니다.',
            "Where the two guides cross is the center of the slot's left end circle."),
        act('type', '입력하고 엔터. 원 명령입니다.',
            'then Enter. The circle command.', 'C'),
        act('move', '커서를 두 보조선이 만나는 자리에 올립니다.',
            'Hover where the two guides cross.'),
        act('snap', '가위표 표식이 뜨면 클릭합니다. 교차점이에요.',
            'Click when the cross shows - the intersection.'),
    ]
    j = next(k for k, a in enumerate(st['actions']) if a.get('type') == '5')
    st['actions'][j]['do'] = bi(
        '반지름을 물어봅니다. 도면에 R5로 적혀 있으니 `D` 를 누르지 않습니다. '
        '그대로 입력하고 엔터.',
        'It asks for the radius. The drawing says R5, so do not press `D`. '
        'Type it and press Enter.')
    st['actions'].append(
        act('type', '보조선 두 개를 지웁니다. 입력하고 엔터, 두 선을 클릭하고 엔터. '
                    '자리를 잡으려고 그은 선은 도면에 남기지 않습니다.',
            'Erase the two guides: type this, Enter, click both lines, Enter. Lines drawn '
            'only to find a position do not belong on the drawing.', 'E'))
    st['pitfall'] = bi(
        '원이 엉뚱한 데 생기면 OFFSET 을 어느 쪽으로 했는지 봅니다. 밑변은 위로, 왼쪽 변은 '
        '오른쪽으로예요. 보조선을 지우는 것도 잊지 마세요. 남으면 외형선으로 읽힙니다.',
        'A circle in the wrong place means the offsets went the wrong way: the bottom edge '
        'goes up, the left edge goes right. And do erase the guides - left behind, they read '
        'as real edges.')
    log.append('4차시 장공 끝원 — OFFSET 교차점 + 보조선 지우기')

    st = at(d, ['sections', 6, 'blocks', 2, 'items', 3])
    i = next(k for k, a in enumerate(st['actions']) if a.get('type') == '@22<45')
    st['actions'][i:i + 1] = [
        act('key', '상태 막대의 극좌표 추적을 켭니다. 각도 증분이 45도인지 확인해요.',
            'Turn on polar tracking in the status bar and check the increment is 45 degrees.',
            'F10'),
        act('move', '커서를 오른쪽 위로 끕니다. 45도에 닿으면 점선 안내선과 '
                    '「극좌표: 45도」 가 뜹니다.',
            'Drag up and to the right. At 45 degrees a dotted guide appears with '
            '"Polar: 45".'),
        act('type', '안내선이 뜬 상태에서 입력하고 엔터. 방향은 안내선이 잡고 거리만 '
                    '숫자로 줍니다. 정확히 45도예요.',
            'With the guide showing, type this and press Enter. The guide holds the '
            'direction; the number gives only the distance. Exactly 45 degrees.', '22'),
    ]
    st['pitfall'] = bi(
        '각도를 손으로 대충 맞추면 44.9도나 45.2도가 됩니다. 안내선이 뜬 것을 보고 눌러야 '
        '정확히 45도예요. 안내선이 안 뜨면 극좌표 추적이 꺼져 있거나 각도 증분이 45가 '
        '아닙니다.',
        'Nudge the angle by hand and you get 44.9 or 45.2 degrees. Wait for the guide before '
        'you type. No guide means polar tracking is off, or its increment is not 45.')
    at(d, ['objectives', 5]).update(bi(
        '극좌표 추적 45도 안내선 위에서 거리 22만 입력해 45도 보조선을 긋고 탭 첫 구멍 '
        '자리를 정확히 잡을 수 있습니다.',
        'You can draw the 45-degree construction line by typing only the distance 22 on the '
        'polar tracking guide, and so locate the first tapped hole exactly.'))
    log.append('4차시 45도 보조선 — 극좌표 추적 안내선 + 거리')


# ── 5차시 · 중심선 세 개 ───────────────────────────────────────
def lesson5(d, log):
    st = at(d, ['sections', 8, 'blocks', 1, 'items', 3])
    acts, out = st['actions'], []
    k = 0
    while k < len(acts):
        a = acts[k]
        t = str(a.get('type', ''))
        if t.startswith('@'):
            down = t == '@0,-5'
            out.append(act('move',
                           '커서를 그 점의 %s에 둡니다. 직교가 방향을 잡아 줍니다.'
                           % ('아래' if down else '왼쪽'),
                           'Put the cursor %s of that point; ortho holds the direction.'
                           % ('below' if down else 'to the left')))
            out.append(act('type', '입력하고 엔터. 중심선이 형상 밖으로 나오는 몫입니다.',
                           'then Enter - how far the centerline runs past the shape.', '5'))
            # 뒤따르던 alt 는 이제 본문과 같은 말이라 뺀다.
            if k + 1 < len(acts) and acts[k + 1].get('kind') == 'alt':
                k += 1
        else:
            out.append(a)
        k += 1
    st['actions'] = out
    st['pitfall'] = bi(
        '레이어를 안 바꾸면 흰 실선이 되어 형상 모서리로 읽힙니다. 커서를 반대쪽에 두고 5를 '
        '치면 중심선이 형상 안에서 시작해 한쪽만 삐져나와요. 5를 치기 전에 커서가 어느 쪽에 '
        '있는지 보세요.',
        'Without the center layer these come out white and solid and read as real edges. '
        'With the cursor on the wrong side, the centerline starts inside the shape and '
        'overruns one end only. Check which side the cursor is on before you type the 5.')
    log.append('5차시 중심선 세 개 — 직교 + 거리')


def main(dry=False):
    log = []
    for n, fn in ((2, lesson2), (3, lesson3), (4, lesson4), (5, lesson5)):
        d = load(n)
        fn(d, log)
        dump(n, d, dry)
    for l in log:
        print(' ·', l)

    left = 0
    for n in (2, 3, 4, 5):
        s = json.dumps(load(n), ensure_ascii=False)
        for m in re.finditer(r'"type": "(@[^"]*)"', s):
            left += 1
            print('   남음(조작):', n, m.group(1))
    print('\n조작에 남은 상대좌표 %d개' % left)
    return 0


if __name__ == '__main__':
    sys.exit(main('--dry' in sys.argv))
