# -*- coding: utf-8 -*-
"""설명하는 대목에서도 상대좌표를 걷어낸다.

조작은 앞 스크립트가 바꿨다. 남은 것은 「이렇게 하는 겁니다」라고 가르치는
대목이다. 조작만 바꾸고 설명을 두면 배우는 사람이 두 가지를 배운다.

특히 3차시의 「베이스 여섯 꼭짓점과 모따기 산술」은 대놓고 "오늘은 모따기
명령을 따로 쓰지 않습니다. 좌표로 직접 그립니다" 라고 적혀 있었다. 방법이
바뀌었으니 이 절이 통째로 옛말이 된다. 11·115·110 같은 계산값도 새 방법에는
아예 필요가 없다 — 그 자체가 새 방법이 나은 이유다.

    python drop_relcoord2.py [--dry]
"""
import io
import json
import os
import sys
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SRC = os.path.join(REPO, 'scripts', 'selfstudy', 'source')


def bi(k, e):
    return {'ko': k, 'en': e}


def load(n):
    return json.load(io.open(os.path.join(SRC, 'lesson-%02d.json' % n), encoding='utf-8'))


def dump(n, d, dry):
    if not dry:
        io.open(os.path.join(SRC, 'lesson-%02d.json' % n), 'w', encoding='utf-8',
                newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1))


def main(dry=False):
    log = []

    # ── 2차시 「점을 찍는 네 가지 방법」 ─────────────────────────
    d = load(2)
    sec = d['sections'][8]
    b = sec['blocks']

    b[1]['rows'][3][1] = bi('`60,62` · `0,0` — 원점에서 잰 값을 그대로',
                            '`60,62`, `0,0` - the value measured from the origin, as it is')
    b[1]['rows'][3][2] = bi('도면이 **원점 기준** 값을 줄 때. 이 과정에서는 용지선 두 구석뿐이에요',
                            'When the drawing gives a value **from the origin**. In this '
                            'course that is only the two sheet corners.')

    # 표기 표 — 실제로 쓰는 세 가지로 바꾼다.
    b[5]['head'] = [bi('방법', 'Way'), bi('무엇을 주나', 'What you give'),
                    bi('이 차시의 예', 'Example in this lesson')]
    b[5]['rows'] = [
        [bi('절대좌표 `x,y`', 'Absolute `x,y`'),
         bi('원점에서 잰 가로·세로', 'Across and up, measured from the origin'),
         bi('`0,0` · `420,297` — 용지선 두 구석', '`0,0`, `420,297` - the two sheet corners')],
        [bi('직접 거리 입력', 'Direct distance entry'),
         bi('방향은 커서, 거리는 숫자', 'Direction from the cursor, distance as a number'),
         bi('직교를 켜고 오른쪽으로 끈 뒤 `10`', 'Ortho on, drag right, type `10`')],
        [bi('치수 옵션 `D`', 'The `D` option'),
         bi('가로와 세로를 숫자 두 개로', 'The two sizes as two numbers'),
         bi('`REC` → `D` → `200` → `30` — 표제란', '`REC`, `D`, `200`, `30` - the title block')],
    ]
    b[6] = {'type': 'p', **bi(
        '절대좌표는 도면에 원점 기준으로 위치가 적혀 있을 때만 씁니다. 용지선 두 구석이 '
        '그렇습니다. 그 밖에는 쓰지 않아요 — 원점이 어디인지 화면에 안 보이니 값이 맞는지 '
        '눈으로 확인할 수가 없습니다.',
        'Absolute coordinates are for the few places the drawing states a position from the '
        'origin - the two sheet corners here. Nowhere else: the origin is not on screen, so '
        'you cannot see whether the number landed where you meant.')}
    b[7] = {'type': 'p', **bi(
        '나머지는 전부 마우스와 숫자입니다. 방향은 커서가 정하고, 거리만 숫자로 줍니다. '
        '기계 도면의 치수는 대부분 「여기서 저기까지 얼마」라서, 도면에 적힌 숫자가 그대로 '
        '입력값이 돼요. 계산을 안 하면 계산 실수도 없습니다. 게다가 그리는 동안 도형이 '
        '미리 보이니 틀렸으면 누르기 전에 압니다.',
        'Everything else is the mouse and a number. The cursor sets the direction; you type '
        'only the distance. Mechanical dimensions mostly read from here to there is this '
        'much, so the printed number goes straight in. No arithmetic means no arithmetic '
        'mistakes - and the shape previews as you go, so a wrong value shows before you '
        'commit it.')}
    b[8]['head'] = [bi('각도', 'Angle'), bi('극좌표 추적이 잡아 주는 방향',
                                            'Direction the polar tracking guide holds')]
    b[9] = {'type': 'note', 'tone': 'why',
            'label': bi('골뱅이는 왜 안 쓰나', 'Why no @'),
            **bi('상대좌표라는 표기가 있습니다. 앞에 골뱅이를 붙여 `@120,0` 처럼 씁니다. '
                 '앞에 찍은 점에서 얼마 갔는지를 적는 방식이에요. 이 과정에서는 쓰지 '
                 '않습니다. 부호를 한 번 틀리면 반대로 그려지는데 화면을 봐도 왜 틀렸는지 '
                 '모르고, 45도 모따기 같은 곳에서는 도면에 없는 계산값을 만들어 내야 합니다. '
                 '직교로 방향을 잡고 거리만 치면 부호가 아예 없어요.',
                 'There is a notation called a relative coordinate, written with an @ as in '
                 '`@120,0`: how far you went from the point before. This course does not use '
                 'it. One wrong sign draws the opposite way and the screen does not tell you '
                 'why, and at a 45-degree chamfer it forces you to compute values the drawing '
                 'never states. Lock the direction with ortho and type the distance, and '
                 'there is no sign to get wrong.')}
    log.append('2차시 「점을 찍는 네 가지 방법」 — 표기 표와 설명을 다시 씀')
    dump(2, d, dry)

    # ── 3차시 「베이스 여섯 꼭짓점과 모따기 산술」 ────────────────
    d = load(3)
    sec = d['sections'][4]
    sec['label'] = bi('베이스 외곽 — 사각형 하나와 모따기 둘',
                      'The base outline - one rectangle and two chamfers')
    sec['lede'] = bi('모따기 때문에 꼭짓점은 여섯 개지만, 그리는 것은 사각형 하나와 모따기 둘입니다.',
                     'The chamfers make six vertices, but what you draw is one rectangle '
                     'and two chamfers.')
    b = sec['blocks']
    b[2]['head'] = [bi('차례', 'Step'), bi('무엇을 주나', 'What you give'),
                    bi('어디서 나온 값인가', 'Where the value comes from')]
    b[2]['rows'] = [
        [bi('1 · 첫 구석', '1 - first corner'), bi('자유 클릭', 'Just click'),
         bi('도면틀 안 빈자리를 그냥 클릭합니다. 도면 치수에 안 걸리는 점이에요',
            'Click any empty spot inside the border. This point is not on any dimension')],
        [bi('2 · 사각형', '2 - the rectangle'), bi('`D` → `120` → `16`', '`D`, `120`, `16`'),
         bi('베이스 폭 120과 정면에서 본 높이 16. 둘 다 도면에 그대로 적혀 있습니다',
            'The 120 base width and the 16 height in the front view - both printed on the '
            'drawing')],
        [bi('3 · 방향', '3 - direction'), bi('커서를 오른쪽 위로', 'Cursor up and right'),
         bi('숫자는 이미 줬으니 어느 쪽으로 펼지만 정합니다',
            'The numbers are given; you only choose which way it opens')],
        [bi('4 · 모따기', '4 - the chamfers'), bi('`CHA` → `D` → `5` → `5`', '`CHA`, `D`, `5`, `5`'),
         bi('도면의 2-C5 입니다. 위 두 구석의 두 변씩 클릭합니다',
            'The 2-C5 on the drawing. Click the two edges at each of the top corners')],
    ]
    b[5] = {'type': 'note', 'tone': 'why',
            'label': bi('계산할 값이 없습니다', 'Nothing to compute'),
            **bi('모따기를 그리면서 넣으려면 11(16−5), 115(120−5), 110(120−5−5) 을 손으로 '
                 '계산해야 합니다. 셋 다 도면에 없는 값이에요. 사각형을 먼저 그리고 CHAMFER '
                 '로 내면 도면에 적힌 120, 16, 5, 5 네 숫자로 끝납니다. 계산이 없으면 계산 '
                 '실수도 없습니다.',
                 'Cutting the chamfers as you draw would mean working out 11 (16-5), 115 '
                 '(120-5) and 110 (120-5-5) by hand - none of which the drawing states. '
                 'Rectangle first, then CHAMFER, and the four printed numbers 120, 16, 5 and '
                 '5 are the whole job. No arithmetic, no arithmetic mistakes.')}
    b[7]['ko'] = b[7]['ko'].replace(
        '오늘은 모따기 명령을 따로 쓰지 않습니다. 좌표로 직접 그립니다.',
        '오늘은 사각형을 먼저 그리고 모따기 명령으로 두 구석을 냅니다.')
    b[7]['en'] = b[7]['en'].replace(
        'Today you do not use a separate chamfer command; you draw them straight from '
        'coordinates.',
        'Today you draw the rectangle first and cut the two corners with the chamfer command.')
    b[3]['alt'] = bi(
        '베이스 외곽을 확대한 그림입니다. 아래변이 120, 왼쪽 높이가 16으로 적혀 있고, 위 두 '
        '구석에 45도로 잘린 자리가 각각 5, 5 로 표시돼 있습니다. 아래 두 구석은 직각 그대로예요.',
        'A magnified view of the base outline. The bottom reads 120 and the left height 16, '
        'and each of the two top corners shows a 45-degree cut marked 5 and 5. The bottom two '
        'corners stay square.')
    log.append('3차시 「베이스 외곽」 절 — 사각형+모따기로 다시 씀, 계산값 표 제거')
    dump(3, d, dry)

    # ── 4차시 요약 표 ──────────────────────────────────────────
    d = load(4)
    d['sections'][2]['blocks'][1]['rows'][4][2] = bi(
        '`O` → `8` → 밑변을 위로, `O` → `29` → 왼쪽 변을 오른쪽으로. 두 보조선의 교차점을 '
        '스냅으로 잡고 `C` → 반지름 `5`. 그리고 보조선을 지웁니다.',
        '`O`, `8`, offset the bottom edge up; `O`, `29`, offset the left edge right. Snap to '
        'where the two guides cross, then `C` and radius `5`. Erase the guides after.')
    log.append('4차시 요약 표 — 장공 끝원을 OFFSET 교차점으로')
    dump(4, d, dry)

    for l in log:
        print(' ·', l)
    return 0


if __name__ == '__main__':
    sys.exit(main('--dry' in sys.argv))
