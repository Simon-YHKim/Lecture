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
    """한 자리를 그 바탕의 SVG 좌표로 옮긴다.

    `view` 가 `raw` 면 x·y 를 SVG 좌표 그대로 쓴다. 투상선끼리 만나는 자리처럼
    **부품 위에 없는 점**을 찍을 때 쓴다 — 45도 선의 원점이 그렇다. 부품 좌표로
    억지로 환산해 적으면 그 숫자가 무엇인지 아무도 못 읽는다.
    """
    x = float(spot.get('x', 0))
    y = float(spot.get('y', 0))
    view = spot.get('view', 'front')
    if view == 'raw':
        return x, y
    if surface == 'sheet':
        return SHEET_X0 + x * SHEET_KX, SHEET_Y0 + (297.0 - y) * SHEET_KY
    if surface == 'three' and view == 'top':
        # 평면도는 가로가 부품 x, 세로가 깊이 z 다. z=0(앞면)이 아래쪽이고
        # 정면도에 가까운 변이 앞면이라는 제3각법의 규칙이 이 부호에 들어 있다.
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
    a = 'class="mk"'
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


def marks(spots, surface, only=None):
    """자리 표시 무리와 그 설명 목록을 만든다. (svg 조각, [(번호, 설명, 표식이름)])

    표시 크기는 **자리끼리 얼마나 붙어 있는지**로 정한다. 평면도는 깊이가 20 밖에
    안 돼서, 앞면·판앞면·뒷면 세 자리를 같은 크기로 찍으면 고리 셋이 겹쳐 어느
    것이 어느 것인지 안 보인다. 붙어 있으면 작게 찍는다.
    """
    # `only` 가 있으면 그 번호만 그린다. 단계가 두 장으로 쪼개졌을 때 이 장에
    # 설명이 있는 자리만 도면에 뜬다 — 설명 없는 번호가 도면에 남으면 학습자가
    # 그것을 찾아 헤맨다.
    keep = [(i + 1, sp) for i, sp in enumerate(spots)
            if only is None or (i + 1) in only]
    pts = [place(sp, surface) for _n, sp in keep]
    r = 8.6
    if len(pts) > 1:
        near = min(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5
                   for i, a in enumerate(pts) for b in pts[i + 1:]) or r * 2
        r = max(3.4, min(8.6, near * 0.46))
    k = r / 8.6
    out, caps = [], []
    for (i, sp), (x, y) in zip(keep, pts):
        kind = sp.get('snap')
        out.append('<g class="cm">'
                   '<circle class="ring" cx="%.2f" cy="%.2f" r="%.2f"/>'
                   '%s'
                   '<circle class="bg" cx="%.2f" cy="%.2f" r="%.2f"/>'
                   '<text class="bn" x="%.2f" y="%.2f" font-size="%.2f">%d</text>'
                   '</g>'
                   % (x, y, r,
                      snap_glyph(kind, x, y, 4.2 * k) if kind else '',
                      x + 10.2 * k, y - 10.2 * k, 5.4 * k,
                      x + 10.2 * k, y - 8.5 * k, 7 * k, i))
        caps.append((i, sp.get('hover'), SNAP_NAME.get(kind)))
    return ''.join(out), caps


VIEWBOX = re.compile(r'<svg[^>]*viewBox="([^"]+)"')
HL_OF = re.compile(r'<(?:path|rect|circle|line|polyline) class="hl" data-feature="(?P<f>[^"]+)"[^>]*/>')


def viewbox(svg):
    m = VIEWBOX.search(svg)
    return m.group(1) if m else '0 0 100 100'


def use_tag(sid, svg):
    """`<symbol>` 을 부르는 태그. viewBox 의 원점까지 맞춰 준다.

    `<use>` 는 x·y 를 안 주면 (0,0) 에 심볼 뷰포트를 놓는다. 그런데 정면도의
    viewBox 는 `48 108 140 110` 이라 바깥 좌표계의 (0,0) 이 보이는 영역 밖이다.
    그래서 도면이 화면 왼쪽 위로 밀려 나가 **보이지 않는다** — 검수에서 「도면
    누락」으로 올라온 여덟 장이 전부 이것이었다.

    원점이 0 인 도해(세 뷰 `0 0 296 274`, A3 `0 0 560 400`)는 우연히 맞아서
    멀쩡해 보였고, 그래서 원점이 있는 도해만 골라 틀렸다.
    """
    x, y, w, h = viewbox(svg).split()
    return '<use href="#%s" x="%s" y="%s" width="%s" height="%s"/>' % (sid, x, y, w, h)


# 선 종류별 표현. `<use>` 안쪽은 바깥 CSS 가 닿지 않으므로 속성으로 박아 둔다.
# 색은 `currentColor` 라 바탕 테마(밝은/어두운)를 그대로 따라간다.
PRESENT = {
    'outline': 'fill="none" stroke="currentColor" stroke-width=".55" '
               'stroke-linejoin="round" stroke-linecap="round"',
    'hidden': 'fill="none" stroke="currentColor" stroke-width=".3" opacity=".6" '
              'stroke-dasharray="2.4 1.2" stroke-linecap="butt"',
    'center': 'fill="none" stroke="currentColor" stroke-width=".28" opacity=".72" '
              'stroke-dasharray="6 1.2 1 1.2" stroke-linecap="butt"',
    'dim': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'ext': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'tangent': 'fill="none" stroke="currentColor" stroke-width=".26" opacity=".55"',
    'arrow': 'fill="currentColor" stroke="none" opacity=".55"',
    'chk': 'fill="none" stroke="currentColor" stroke-width=".18" opacity=".4"',
    'hl': 'fill="none" stroke="none"',
    'hl hot': 'fill="none" stroke="#C7004C" stroke-width="1.9" stroke-linejoin="round" '
              'stroke-linecap="round"',
    # A3 도면틀 도해 쪽 이름
    'si': 'fill="none" stroke="currentColor" stroke-width="1.4"',
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


# `<symbol>` 안에 넣는 스타일. 그림자 트리에는 바깥 CSS 가 닿지 않지만 **안에 든
# `<style>` 은 함께 복제되어 적용된다.** 요소마다 속성을 박으면 정면도가 14KB 에서
# 19KB 로, 세 뷰가 26KB 에서 42KB 로 불어난다 — 한 쪽 100KB 한도에서 그 차이가 쪽
# 하나를 통째로 먹는다. 규칙 한 벌이면 600바이트다.
SYMBOL_CSS = (
    '<style>'
    '.outline{fill:none;stroke:currentColor;stroke-width:.55;stroke-linejoin:round;'
    'stroke-linecap:round}'
    '.hidden{fill:none;stroke:currentColor;stroke-width:.3;opacity:.6;'
    'stroke-dasharray:2.4 1.2;stroke-linecap:butt}'
    '.center{fill:none;stroke:currentColor;stroke-width:.28;opacity:.72;'
    'stroke-dasharray:6 1.2 1 1.2;stroke-linecap:butt}'
    '.dim,.ext,.tangent{fill:none;stroke:currentColor;stroke-width:.26;opacity:.55}'
    '.arrow{fill:currentColor;stroke:none;opacity:.55}'
    '.chk{fill:none;stroke:currentColor;stroke-width:.18;opacity:.4}'
    '.hl{fill:none;stroke:none}'
    'text{fill:currentColor;opacity:.6}'
    '.si{fill:none;stroke:currentColor;stroke-width:1.4}'
    '.sh{fill:none;stroke:currentColor;stroke-width:1.4;opacity:.8;'
    'vector-effect:non-scaling-stroke}'
    '.sd{fill:none;stroke:currentColor;stroke-width:1;opacity:.5;stroke-dasharray:4 3}'
    '.sl,.slh{fill:currentColor;font-size:11px}.slh{opacity:.85}'
    '</style>')


def to_symbol(svg, sid, css=True):
    """도해 하나를 `<symbol>` 로 바꾼다. 한 벌만 두고 `<use>` 로 부른다.

    자습 교재는 한 쪽이 100KB 를 넘으면 안 된다(지침 §2). 정면도가 14KB 라
    단계마다 복사해 넣으면 열네 단계에서 이미 한도를 넘는다.

    `css` 를 끄면 표현을 속성으로 박는다. `<use>` 는 심볼 안을 **통째로 복제**하는데,
    안에 `<style>` 이 있으면 그 스타일시트까지 인스턴스 수만큼 복제돼 파싱된다.
    여덟 차시 묶음(`<use>` 82개)에서 그것 때문에 첫 화면이 40초 걸렸다. 인스턴스가
    몇 개뿐인 자습 교재는 켜 두고(파일이 작아진다), 묶음 데크는 끈다.
    """
    body = svg[svg.index('>', svg.index('<svg')) + 1:]
    body = body[:body.rindex('</svg>')]
    inner = (SYMBOL_CSS + body) if css else stylize(body)
    return '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, viewbox(svg), inner)


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


def spot_badges(a):
    """조작 한 줄이 짚는 자리 번호들. 정수 하나도, 여럿도 받는다."""
    v = a.get('spot')
    if v is None:
        return []
    return [v] if isinstance(v, int) else list(v)
