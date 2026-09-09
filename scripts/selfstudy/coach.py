# -*- coding: utf-8 -*-
"""코치 마크 — 도면 위에 「여기에 커서를 올리라」를 찍는다.

사용자 정책 2번이다.

    작도 실습 슬라이드라면 도면을 띄우고 코치마크를 띄워서 위치를 찾기 쉽게 하는
    표현을 모두 적용해야 함 … 슬라이드별로 현재 지시하는 작업이 다른데 반해
    코치마크는 그대로인 상태임

그동안 이 그림은 **검수용 데크에만** 있었다. 정작 학생이 읽는 자습 교재
(`build_selfstudy.py`)는 `spots` 를 아예 렌더하지 않았다. 두 산출물이 같은
원본을 쓰는데 한쪽만 그리고 있었던 것이다. 그리는 규칙을 여기 한 곳에 두고
양쪽이 불러 쓴다.

바탕이 셋이다. 단계마다 무엇 위에 찍는지가 다르기 때문이다.

    front  정면도            부품 좌표 (x, y) 를 그대로
    three  제3각법 세 뷰      view 로 정면·평면·우측면을 고른다
    sheet  A3 도면틀          용지 좌표 (mm). 도면틀 만드는 차시가 쓴다

`sheet` 가 없어서 2차시의 용지선·중심 마크·표제란·이름 넣기 네 단계가 코치 마크
없이 남아 있었다. 검수 메모 8~11 이 그 자리다.
"""
import re

# ── 바탕과 좌표 ────────────────────────────────────────────────
# 정면도 SVG 는 부품 좌표를 그대로 쓴다. 베이스 왼쪽 아래 구석 (0,0) 이 SVG 의
# (58,208) 이고 y 는 아래로 자란다.
FRONT_X0, FRONT_Y0 = 58.0, 208.0
# 세 뷰 도해 안에서 평면도는 위(깊이 z 가 위로), 우측면도는 오른쪽에 있다.
TOP_Y0 = 84.0            # z=0(앞면)이 여기, z 가 커질수록 위로
SIDE_X0 = 224.0          # z=0(앞면)이 여기, z 가 커질수록 오른쪽으로
# A3 도해는 실치수가 아니라 줄인 값이다. 용지선 rect(30,30,462,327) 이 420×297.
SHEET_X0, SHEET_Y0 = 30.0, 30.0
SHEET_KX = 462.0 / 420.0
SHEET_KY = 327.0 / 297.0


def place(spot, surface):
    """한 자리를 그 바탕의 SVG 좌표로 옮긴다."""
    x = float(spot.get('x', 0))
    y = float(spot.get('y', 0))
    if surface == 'sheet':
        return SHEET_X0 + x * SHEET_KX, SHEET_Y0 + (297.0 - y) * SHEET_KY
    view = spot.get('view', 'front')
    if surface == 'three' and view == 'top':
        # 평면도는 가로가 부품 x, 세로가 깊이 z 다.
        return FRONT_X0 + x, TOP_Y0 - float(spot.get('z', y))
    if surface == 'three' and view == 'side':
        # 우측면도는 가로가 깊이 z, 세로가 부품 y 다.
        return SIDE_X0 + float(spot.get('z', x)), FRONT_Y0 - y
    return FRONT_X0 + x, FRONT_Y0 - y


# 바탕 이름 → figures.build_map() 의 열쇠. sheet 만 다른 곳에서 온다.
FIG_OF = {'front': 'front', 'frontdim': 'frontdim', 'three': 'three'}


# ── 스냅 표식 ──────────────────────────────────────────────────
# 오토캐드가 커서 옆에 띄우는 표식. 모양이 곧 스냅 종류다.
SNAP_NAME = {'end': '끝점', 'mid': '중간점', 'cen': '중심', 'qua': '사분점',
             'int': '교차점', 'tan': '접점', 'per': '직교', 'nea': '근처점'}


def snap_glyph(kind, x, y, r=4.2):
    """표식 하나를 도면 좌표 위에 그린다. 획 굵기는 배율과 무관하게 둔다."""
    a = 'class="mk" vector-effect="non-scaling-stroke"'
    if kind == 'end':
        return '<rect %s x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>' % (
            a, x - r, y - r, r * 2, r * 2)
    if kind == 'mid':
        return '<path %s d="M%.2f %.2f L%.2f %.2f L%.2f %.2f Z"/>' % (
            a, x, y - r, x + r, y + r, x - r, y + r)
    if kind == 'qua':
        return '<path %s d="M%.2f %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f Z"/>' % (
            a, x, y - r, x + r, y, x, y + r, x - r, y)
    if kind == 'int':
        return '<path %s d="M%.2f %.2f L%.2f %.2f M%.2f %.2f L%.2f %.2f"/>' % (
            a, x - r, y - r, x + r, y + r, x + r, y - r, x - r, y + r)
    if kind == 'tan':
        return ('<circle %s cx="%.2f" cy="%.2f" r="%.2f"/>'
                '<path %s d="M%.2f %.2f L%.2f %.2f"/>'
                % (a, x, y, r, a, x - r, y - r, x + r, y - r))
    if kind == 'per':
        return '<path %s d="M%.2f %.2f L%.2f %.2f L%.2f %.2f M%.2f %.2f L%.2f %.2f"/>' % (
            a, x - r, y - r, x - r, y + r, x + r, y + r,
            x - r, y + r * .35, x - r * .35, y + r * .35)
    return '<circle %s cx="%.2f" cy="%.2f" r="%.2f"/>' % (a, x, y, r)


FEATURE_KO = {'profile': '베이스와 목의 바깥 윤곽', 'boss': '보스 원', 'bore': '축 구멍',
              'fillet': '필렛', 'slot': '장공', 'tap': '탭 구멍',
              # 같은 형상이라도 재는 곳이 다르면 켜는 것도 다르다.
              'basehl': '베이스 윤곽', 'neck': '목과 밑동 라운드',
              'bossc': '보스 중심선', 'filletc': '필렛 중심선',
              'slotc': '장공 중심선', 'thick': '옆면도의 두께',
              # 도면틀 쪽 강조. sheet 바탕에서만 쓴다.
              'sh-paper': '용지선', 'sh-frame': '도면선', 'sh-mark': '중심 마크',
              'sh-title': '표제란'}


def marks(spots, surface):
    """자리 표시 무리와 그 설명 목록을 만든다. (svg 조각, [(번호, 설명, 표식이름)])"""
    out, caps = [], []
    for i, sp in enumerate(spots, 1):
        x, y = place(sp, surface)
        kind = sp.get('snap')
        out.append('<g class="cm">'
                   '<circle class="ring" cx="%.2f" cy="%.2f" r="8.6"/>'
                   '%s'
                   '<circle class="bg" cx="%.2f" cy="%.2f" r="5.4"/>'
                   '<text class="bn" x="%.2f" y="%.2f">%d</text>'
                   '</g>'
                   % (x, y, snap_glyph(kind, x, y) if kind else '',
                      x + 10.2, y - 10.2, x + 10.2, y - 8.5, i))
        caps.append((i, sp.get('hover'), SNAP_NAME.get(kind)))
    return ''.join(out), caps


VIEWBOX = re.compile(r'<svg[^>]*viewBox="([^"]+)"')
HL_OF = re.compile(r'<(?:path|rect|circle|line|polyline) class="hl" data-feature="(?P<f>[^"]+)"[^>]*/>')


def viewbox(svg):
    m = VIEWBOX.search(svg)
    return m.group(1) if m else '0 0 100 100'


# 선 종류별 표현. `<use>` 안쪽은 바깥 CSS 가 닿지 않으므로 속성으로 박아 둔다.
# 색은 `currentColor` 라 바탕 테마(밝은/어두운)를 그대로 따라간다.
PRESENT = {
    'outline': 'fill="none" stroke="currentColor" stroke-width=".55" '
               'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"',
    'hidden': 'fill="none" stroke="currentColor" stroke-width=".3" opacity=".6" '
              'stroke-dasharray="2.4 1.2" stroke-linecap="butt" vector-effect="non-scaling-stroke"',
    'center': 'fill="none" stroke="currentColor" stroke-width=".28" opacity=".72" '
              'stroke-dasharray="6 1.2 1 1.2" stroke-linecap="butt" vector-effect="non-scaling-stroke"',
    'dim': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'ext': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'tangent': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'arrow': 'fill="currentColor" stroke="none" opacity=".55"',
    'chk': 'fill="none" stroke="currentColor" stroke-width=".18" opacity=".4"',
    'hl': 'fill="none" stroke="none"',
    'hl hot': 'fill="none" stroke="#C7004C" stroke-width="1.9" stroke-linejoin="round" '
              'stroke-linecap="round" vector-effect="non-scaling-stroke"',
    # A3 도면틀 도해 쪽 이름
    'si': 'fill="none" stroke="currentColor" stroke-width="1.4" vector-effect="non-scaling-stroke"',
    'sh': 'fill="none" stroke="currentColor" stroke-width="1.4" opacity=".8" '
          'vector-effect="non-scaling-stroke"',
    'sd': 'fill="none" stroke="currentColor" stroke-width="1" opacity=".5" stroke-dasharray="4 3"',
    'sl': 'fill="currentColor" opacity=".6" font-size="11"',
    'slh': 'fill="currentColor" opacity=".85" font-size="11"',
}
_CLS = re.compile(r'<(?P<tag>path|rect|circle|line|polyline|polygon|text|g)\s+class="(?P<cls>[\w -]+)"')


def stylize(svg):
    """클래스별 표현을 속성으로 박는다.

    `<use>` 가 만드는 그림자 트리에는 문서의 CSS 선택자가 닿지 않는다. 클래스만
    두고 CSS 에 맡기면 채우기가 기본값(검정)으로 남아 도면이 까만 상자가 된다 —
    실제로 A3 도면틀이 그렇게 나왔다. 물려받는 속성(fill·stroke·color)만으로는
    선 종류를 구분할 수 없으므로 요소마다 직접 적는다.
    """
    def one(m):
        raw = m.group('cls').strip()
        extra = PRESENT.get(raw) or PRESENT.get(raw.split()[0])
        return m.group(0) + (' ' + extra if extra else '')
    return _CLS.sub(one, svg)


def to_symbol(svg, sid):
    """도해 하나를 `<symbol>` 로 바꾼다. 쪽마다 한 벌만 두고 `<use>` 로 부른다.

    자습 교재는 한 쪽이 100KB 를 넘으면 안 된다(지침 §2). 정면도가 14KB 라
    단계마다 복사해 넣으면 열네 단계에서 이미 한도를 넘는다.
    """
    body = svg[svg.index('>', svg.index('<svg')) + 1:]
    body = body[:body.rindex('</svg>')]
    return '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, viewbox(svg), stylize(body))


def hl_for(svg, feature):
    """그 형상의 강조 겹선만 뽑아 켠 채로 돌려준다.

    `<use>` 안쪽은 바깥 CSS 로 켜고 끌 수 없다. 그래서 겹선은 인스턴스에 직접
    그린다 — 경로 몇 줄이라 크기에 영향이 없다.
    """
    if not feature:
        return ''
    got = [m.group(0).replace('class="hl"', 'class="hl hot"')
           for m in HL_OF.finditer(svg) if m.group('f') == feature]
    return ''.join(got)
