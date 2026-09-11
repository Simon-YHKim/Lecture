# -*- coding: utf-8 -*-
"""자습용 강의 슬라이드 — 기존 프레임 위에 자습본 내용을 얹는다.

`build_deck_frames.py` 는 동영상 강의의 프레임을 그대로 덱으로 만든다. 그것만으로는
자습이 되지 않는다. 강의에는 강사가 화면을 보며 말하는 몫이 있고, 시연 프레임은
`USER RECORDING` 자리표시자라 혼자 보는 사람에게는 빈 화면이기 때문이다.

그래서 이 판은 두 가지를 한다.

  · **시연 프레임을 뺀다.** 자리에 자습본의 따라 하기 단계를 한 단계 한 장씩 깐다.
    한 장 안에 명령·묻는 것·입력값·확인이 순서대로 있고, 오른쪽에 「이렇게 되면
    맞습니다 · 왜 이 순서인가 · 안 되면 여기」가 붙는다. 강사가 말로 때우던 몫이
    화면에 남는다.
  · **개념 프레임 뒤에 보강 장을 넣는다.** 객체 스냅·방향·거리로 점을 정하는
    기준과 결과 확인을 함께 싣는다.

새로 만드는 장은 프레임의 조판을 그대로 쓴다. `.clip` · `.topline` · `.card` ·
`.note` 는 프레임 스타일시트에 이미 있는 것이고, 덱에 프레임이 함께 실리므로
그 규칙이 그대로 닿는다. 이 파일이 더하는 스타일은 조작 목록 하나뿐이다.

    python scripts/selfstudy/build_deck_selfstudy.py <lesson-dir> <lesson.json> [출력]
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_deck_frames as F
import figures as _figures
import sheet_figures as _sheet

# 녹화 자리표시자인가. 파일 이름이 아니라 안에 있는 것으로 가른다 — 2차시의
# 녹화 프레임은 08-build-template 이라 이름으로는 못 가려낸다.
FILM = re.compile(r'class="film"')

# 자습본의 어느 절이 어느 프레임 뒤에 한 장으로 붙는가.
# 차시마다 강의가 어디까지 말하고 자습본이 어디를 더 채우는지가 달라서,
# 자동으로 고를 수 있는 값이 아니다.
EXTRA = {
    # 1차시는 보강 장을 두지 않는다. 강의 프레임이 이미 같은 말을 한다.
    # 점을 찍는 방법은 도면틀을 그리기 전에 있어야 한다. 3차시에서 2차시로 옮겼다.
    2: [('07-sheet-and-layers', '점을 찍는 네 가지 방법', 'concept'),
        ('07-sheet-and-layers', '스냅 표식을 보고 누릅니다', 'concept')],
    3: [('03-concept', '다른 방법 — 보조선으로 기준 잡기', 'concept')],
    4: [('03-concept', '안쪽 형상 넷 — 축 구멍·탭·장공·필렛', 'concept'),
        ('03-concept', '계산해서 나오는 값들', 'concept')],
    5: [('03-concept', '투상선은 도면에 남지 않는 선입니다', 'concept'),
        ('03-concept', '숨은선 셋의 서로 다른 길이', 'concept')],
    6: [('03-concept', '지울까 자를까 늘릴까', 'concept'),
        ('03-concept', '레이어 점검 세 가지 방법', 'concept')],
    7: [('03-concept', '치수 다섯 종류', 'concept'),
        ('03-concept', '치수선 방향과 기준면', 'concept')],
    8: [('02-exam', '전체 작도에서 다시 확인할 세 자리', 'concept')],
}

# 녹화 프레임이 없는 차시는 따라 하기를 어느 프레임 뒤에 깔지 정해 준다.
# 1차시는 실습이 2차시로 넘어가 깔 것이 없다.
AFTER = {8: '02-exam'}

# 덱에서 빼는 강의 프레임. 오리엔테이션에서 「이번 차시와 다음 차시」는
# 바로 앞 로드맵과 같은 말을 두 번 한다.
DROP_FRAMES = {1: {'05-recap'}}

INLINE = re.compile(r'`([^`]+)`|\*\*([^*]+)\*\*')
_ACT_KO = {'ask': '묻는 것', 'move': '마우스', 'snap': '스냅', 'click': '클릭',
           'key': '키', 'see': '확인', 'alt': '또는', 'type': '입력'}
_ACT_EN = {'ask': 'Asks', 'move': 'Mouse', 'snap': 'Snap', 'click': 'Click',
           'key': 'Key', 'see': 'Check', 'alt': 'Or', 'type': 'Type'}

# 덱이 제 손으로 쓰는 이름표. 본문은 자습 원본의 `{ko, en}` 에서 오지만 이것들은
# 여기 박혀 있어서, 영문판에도 한글로 나갔다.
_UI_KO = {
    'drawing_now': '지금 그리는 것 — <b>%s</b>',
    'where': '완성 도면 위에서 지금 잡을 자리',
    'step_figure': '이 단계의 작도 도해',
    'temp_lines': '점선: 이 단계의 임시선',
    'marker': '<em> — %s 표식</em>',
    'step_action': '%s단계 · 조작 %d',
    'step_dot': '%s단계 · %s',
    'step_part': '%s단계%s · %s',
    'expect': '이렇게 되면 맞습니다',
    'why': '왜 이 순서인가',
    'pitfall': '안 되면 여기',
    'path_here': '이 과정이 걷는 길',
    'path_other': '알아만 두면 되는 길',
    'edition': '자습본',
}
_UI_EN = {
    'drawing_now': 'Drawing now — <b>%s</b>',
    'where': 'Where to catch it, on the finished drawing',
    'step_figure': 'The drawing for this step',
    'temp_lines': 'Dashed: this step&#8217;s temporary lines',
    'marker': '<em> — %s marker</em>',
    'step_action': 'Step %s · action %d',
    'step_dot': 'Step %s · %s',
    'step_part': 'Step %s%s · %s',
    'expect': 'You have it right when',
    'why': 'Why this order',
    'pitfall': 'If it does not work',
    'path_here': 'The path this course takes',
    'path_other': 'A path to know about',
    'edition': 'self-study',
}

# ── 코치 마크 ──────────────────────────────────────────────────
# 찍는 규칙은 `coach.py` 한 곳에 있다. 자습 교재와 이 데크가 같은 규칙을 써야
# 두 산출물이 갈라지지 않는다 (LESSON_STYLE 12번).
import coach as _coach

# 이 실행에서 실제로 쓴 바탕. 문서 끝에 `<symbol>` 로 한 벌씩 심는다.
USED_SURFACES = set()


def to_svg(x, y):
    return _coach.place({'x': x, 'y': y}, 'front')


SNAP_NAME = _coach.SNAP_NAME
snap_glyph = _coach.snap_glyph
FEATURE_KO = _coach.FEATURE_KO


_SURFACES = None


def surfaces():
    """바탕 묶음. 도면 생성기를 한 번만 돌린다."""
    global _SURFACES
    if _SURFACES is None:
        fm = _figures.build_map(keep_hl=True)
        _SURFACES = {'front': fm['front'], 'frontdim': fm['frontdim'],
                     'three': fm['three'], 'sheet': _sheet.SVG_A3}
    return _SURFACES


def surface_defs():
    """이 실행에서 쓴 바탕을 `<symbol>` 로 낸다. 문서에 한 번만 넣는다."""
    if not USED_SURFACES:
        return ''
    syms = ''.join(_coach.to_symbol(surfaces()[n], 'dsfc-' + n, css=False)
                   for n in sorted(USED_SURFACES) if surfaces().get(n))
    return ('<svg aria-hidden="true" focusable="false" '
            'style="position:absolute;width:0;height:0;overflow:hidden">%s</svg>' % syms)


def fig_block(spots, figs, feature=None, surface='front', only=None, step=None):
    """정면도 한 장 위에 자리 표시를 얹고, 아래에 무엇을 볼지 적는다.

    `feature` 가 있으면 그 형상의 강조 겹선을 켠다. 자리만 찍어 두면 「여기를
    누르라」는 말은 되지만 「무엇을 그리는 중인지」는 안 보인다. 단계마다 그리는
    것이 다른데 도면이 늘 같은 모습이면 도면이 지시를 따라오지 못한다.
    """
    base = figs.get(surface) if isinstance(figs, dict) else figs
    if not base:
        return ''
    step = step or {}
    marks_svg, rows = _coach.marks(spots or [], surface, only)
    caps = []
    for i, hover, snapname in rows:
        caps.append('<li><span class="bd">%d</span><span>%s%s</span></li>'
                    % (i, rich(ko(hover)),
                       (UI['marker'] % esc(snapname)) if snapname else ''))
    # 도해는 문서에 한 벌만 두고 슬라이드는 `<use>` 로 부른다. 단계마다 통째로
    # 복사하면 여덟 차시 묶음이 4MB 를 넘어 브라우저가 30초 안에 못 연다 —
    # 실제로 그렇게 됐다. 강조 겹선만 인스턴스에 직접 그린다(`<use>` 안쪽은
    # 바깥에서 켤 수 없다).
    separate = bool(step.get('diagramOnly'))
    construction = _coach.construction_for(step, surface)
    if not separate:
        USED_SURFACES.add(surface)
    viewport = _coach.figure_viewbox(step, surface, base)
    vb = viewport.split()
    body = ('<svg class="dwg cdwg" viewBox="%s" width="%s" height="%s" '
            'preserveAspectRatio="xMidYMid meet">%s%s%s'
            '<g class="coach">%s</g></svg>'
            % (viewport, vb[2], vb[3],
               '' if separate else _coach.use_tag('dsfc-' + surface, base),
               '' if separate else _coach.hl_for(base, feature), construction, marks_svg))
    # 완성 도면을 지도로 쓴다. 지금 화면에 그려져 있는 것과 다르다는 것을 밝혀 둔다.
    head = ((UI['drawing_now'] % esc(FEATURE_KO[feature]))
            if feature in FEATURE_KO else UI['where'])
    if separate:
        head = UI['step_figure']
    if construction:
        head += '<span class="construction-key">%s</span>' % UI['temp_lines']
    # 캡션 목록은 내지 않는다. 같은 말이 왼쪽 조작 줄에 이미 있고, 번호로 서로
    # 짚을 수 있게 했다. 비는 자리는 도면이 가져간다.
    return ('<figure class="fig" data-memo="도면 코치 마크">'
            '<div class="fh">%s</div>%s</figure>' % (head, body))


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def rich(s):
    """백틱은 명령 토큰, **강조**는 굵게. 나머지는 이스케이프한다."""
    out, i = [], 0
    for m in INLINE.finditer(s or ''):
        out.append(esc(s[i:m.start()]))
        out.append('<span class="cmd">%s</span>' % esc(m.group(1))
                   if m.group(1) is not None else '<b>%s</b>' % esc(m.group(2)))
        i = m.end()
    out.append(esc((s or '')[i:]))
    return ''.join(out)


def plain(s):
    """길이를 셀 때는 마크업을 뺀 글자 수가 기준이다."""
    return INLINE.sub(lambda m: m.group(1) or m.group(2), s or '')


# 자습 원본은 한 마디를 `{ko, en}` 로 갖는다. 화면에 나가는 글은 판의 언어를
# 따르고, 절을 찾는 열쇠는 언제나 국문이다 — `EXTRA` 가 국문 제목으로 적혀
# 있어서, 열쇠까지 언어를 따르면 영문 빌드가 「절이 없다」로 멎는다.
LANG = os.environ.get('SELFSTUDY_LANG', 'ko')


def ko(node):
    node = node or {}
    if LANG == 'en':
        # 영문 자리가 비면 국문으로 떨어뜨린다. 빈칸이 남는 것보다 낫고,
        # 그 자리는 `check_english.py` 가 잡는다.
        return node.get('en') or node.get('ko', '')
    return node.get('ko', '')


ACT_LAB = _ACT_EN if LANG == 'en' else _ACT_KO
UI = _UI_EN if LANG == 'en' else _UI_KO


def ident(node):
    """절을 가리키는 이름. 판이 바뀌어도 같아야 한다."""
    return (node or {}).get('ko', '')


# ── 조작 목록의 글자 크기 ──────────────────────────────────────
# 단계마다 조작이 2줄에서 11줄까지 온다. 한 크기로 박아 두면 긴 단계가 넘치고
# 짧은 단계는 허전하다. 들어갈 크기 중 가장 큰 것을 고른다.
# 글자 크기는 하나다. 줄이지 않는다.
#
# 예전에는 28에서 18까지 내려가는 사다리였고, 그래서 조작이 많은 단계는
# 18px 로 쪼그라들어 「설명 text 크기가 너무 작아져서 보기 어려워짐」이라는
# 검수 지적을 받았다. LESSON_STYLE 11번이 이미 「글자를 줄이지 말고 화면을
# 나눈다」고 정해 두었는데 사다리가 그 규칙을 어기고 있었다.
SIZES = (28,)
OPS_H = 700          # .body 안에서 조작 목록이 쓸 수 있는 높이(px)
OPS_W = 940          # 글이 놓이는 폭(px). 라벨 칸을 뺀 값이다.


def ops_font(actions, narrow=False):
    """들어가는 가장 큰 크기와, 그 크기에서 어림한 높이를 함께 준다.

    라벨 칸이 줄을 하나 더 만드는 경우가 있어 실제가 어림보다 조금 크다.
    그만큼 한도를 낮춰 잡는다.
    """
    # 도면/확인 카드는 오른쪽에 둔다. 왼쪽 조작 영역은 도면의 높이와 무관하게
    # 끝까지 쓰므로 작은 조각으로 잘라 명령과 입력값을 갈라놓을 필요가 없다.
    w, gap, cap = (900, 12, 700) if narrow else (OPS_W, 15, 700)
    last = (SIZES[-1], 0.0)
    for size in SIZES:
        cpl = max(12, int(w / (size * 0.98)))   # 한글은 글자 한 자가 약 1em
        line = size * 1.45
        h = 0.0
        for a in actions:
            txt = plain(ko(a.get('do'))) + ('  ' + (a.get('type') or ''))
            h += max(1, math.ceil(len(txt) / cpl)) * line + gap
        last = (size, h)
        if h <= cap:
            return size, h, cap
    return last[0], last[1], cap


def action_pages(actions, narrow=False):
    """28px에서 들어가는 만큼 묶되 명령·응답의 순서와 원문은 보존한다."""
    pages, start = [], 0
    while start < len(actions):
        _, first_height, first_cap = ops_font(actions[start:start + 1], narrow)
        if first_height > first_cap:
            raise ValueError('One action exceeds the readable slide area; split its explanation at source')
        end = start + 1
        while end < len(actions):
            _, height, cap = ops_font(actions[start:end + 1], narrow)
            if height > cap:
                break
            end += 1
        if end < len(actions):
            # 확인 뒤/다음 명령 앞을 우선한다. 질문 직후에는 나누지 않는다.
            candidates = [i for i in range(start + 1, end + 1)
                          if actions[i - 1].get('kind') == 'see'
                          or (i < len(actions) and actions[i].get('type')
                              and re.fullmatch(r'[A-Z][A-Z_-]{1,}', actions[i]['type']))]
            candidates = [i for i in candidates
                          if actions[i - 1].get('kind') != 'ask'
                          and ops_font(actions[start:i], narrow)[1] >= cap * .55]
            if candidates:
                end = candidates[-1]
            elif actions[end - 1].get('kind') == 'ask' and end > start + 1:
                end -= 1
        pages.append(actions[start:end])
        start = end
    return pages or [[]]


SIDE_SIZES = (21, 20, 19, 18, 17, 16)


def side_font(texts, w=600, cap=700):
    """카드 세 장이 한 칸에 세로로 설 때 들어가는 크기를 고른다.

    라벨 한 줄, 본문 몇 줄, 패딩과 사이 여백까지 세어 본다. 넘치면 잘려서
    「안 되면 여기」가 화면 밖으로 나간다 — 정확히 그 카드가 필요한 사람이
    못 보게 된다.
    """
    for size in SIDE_SIZES:
        cpl = max(10, int((w - 36) / (size * 0.98)))
        h = 0.0
        for t in texts:
            h += (size + 3) * 1.25 + max(1, math.ceil(len(t) / cpl)) * size * 1.4 + 40
        if h + 16 * (len(texts) - 1) <= cap:
            return size
    return SIDE_SIZES[-1]


def step_slide(st, cid, clock, sec_label, total, front=None, part=None, action_start=0):
    """따라 하기 한 단계를 읽을 수 있는 문맥 단위로 묶는다.

    `spots` 가 있으면 정면도가 한 칸을 차지한다. 커서를 어디에 올려야 하는지는
    글로 적어 봐야 「베이스 윗면 왼쪽에서 조금 오른쪽」 같은 말이 될 뿐이고,
    그것은 자습자가 화면에서 찾아내야 하는 탐색 지시다. 자리를 그림으로 찍어
    주면 찾을 것이 없다.
    """
    acts = st.get('actions', [])
    spots = st.get('spots') if front else None
    has_fig = bool(front and (spots or st.get('construction')))
    size, est, cap = ops_font(acts, narrow=has_fig)
    if est > cap and part is None:
        # 한 장에 안 들어가면 글자를 줄이는 대신 장을 나눈다(LESSON_STYLE 11번).
        # 두 장으로 모자란 단계가 있어 필요한 만큼 나눈다 — 조작이 스물한 줄인
        # 단계까지 있다.
        chunks = action_pages(acts, narrow=has_fig)
        parts = len(chunks)
        out = []
        offset = action_start
        for k, chunk in enumerate(chunks):
            sub = dict(st, actions=chunk)
            # 첫 장에는 「왜 이 순서인가」를, 마지막 장에는 「이렇게 되면
            # 맞습니다」와 「안 되면 여기」를 둔다. 가운데 장은 카드가 없어도
            # 조작 줄이 조각을 만들어 주므로 빈 장이 되지 않는다.
            if k != 0:
                sub.pop('why', None)
            if k != parts - 1:
                sub.pop('expect', None)
                sub.pop('pitfall', None)
            one = step_slide(sub, '%s%s' % (cid, 'abcdefgh'[k]), clock,
                             sec_label, total, front, part=(k + 1, parts),
                             action_start=offset)
            out += one
            clock += one[-1][3]
            offset += len(chunk)
        return out
    ops = []
    for k, a in enumerate(acts):
        kind = a.get('kind') or ('type' if a.get('type') else '')
        lab = ACT_LAB.get(kind, '')
        cmd = ('<span class="cmd">%s</span>' % esc(a['type'])) if a.get('type') else ''
        # 도면 위 자리 표시와 같은 번호를 이 줄에 단다. 도면 아래에 같은 말을 또
        # 적는 대신 여기서 대조하게 하는 것이 검수 요청이다.
        badge = ''.join('<span class="spotno">%d</span>' % n for n in _coach.spot_badges(a))
        ops.append('<li class="op o%d %s%s" data-memo="%s" data-action="%d"><span class="lab">%s</span>'
                   '<span class="w">%s%s%s</span></li>'
                   % (k + 1, esc(kind), ' pointed' if badge else '',
                      esc(UI['step_action'] % (st['n'], action_start + k + 1)),
                      action_start + k + 1,
                      esc(lab), badge, cmd, rich(ko(a.get('do')))))

    side, texts = [], []
    for cls, lab, key in (('', UI['expect'], 'expect'),
                          ('', UI['why'], 'why'),
                          (' pit', UI['pitfall'], 'pitfall')):
        if st.get(key):
            side.append('<div class="card sc%s" data-memo="%s"><b>%s</b>'
                        '<span>%s</span></div>'
                        % (cls, esc(UI['step_dot'] % (st['n'], lab)), lab,
                           rich(ko(st[key]))))
            texts.append(plain(ko(st[key])))
    ssz = side_font(texts) if (texts and not has_fig) else 0

    # 입력 한 줄마다 다음을 누르지 않는다. 이 장의 명령·응답·확인은 함께 읽는다.
    n_frag, dur = 1, 1.0
    body = (
      '<div id="%(c)s-root" data-composition-id="%(c)s" data-start="%(s)s" '
      'data-duration="%(d)s" data-width="1920" data-height="1080" '
      'data-label="%(lab)s">\n'
      '<section id="%(c)s" class="clip ss" data-start="%(s)s" data-duration="%(d)s" '
      'data-track-index="1">\n'
      '<header class="topline"><div><div class="index">03 · DO</div>'
      '<h1>%(title)s</h1></div><div class="prompt">%(sec)s · %(n)s / %(tot)s</div></header>\n'
      '<main class="body ssbody%(fx)s">'
      '<ol class="ops" style="font-size:%(fs)dpx">%(ops)s</ol>'
      '<div class="guide">%(fig)s'
      '<aside class="side"%(sst)s>%(side)s</aside>'
      '</div></main>\n</section>\n</div>'
      % {'c': cid, 's': clock, 'd': dur, 'fs': size,
         'fx': ' hasfig' if has_fig else '',
         'sst': (' style="font-size:%dpx"' % ssz) if ssz else '',
         'fig': fig_block(spots, front, st.get('feature'), st.get('on', 'front'),
                          only={n for a in acts for n in _coach.spot_badges(a)}, step=st)
                if has_fig else '',
         'lab': esc(UI['step_part'] % (st['n'], (' (%d/%d)' % part) if part else '',
                                       ko(st.get('title')))),
         'title': rich(ko(st.get('title'))) + (
             ' <span class="pt">%d / %d</span>' % part if part else ''),
         'sec': esc(sec_label.split('—')[0].strip()),
         'n': st['n'], 'tot': total, 'ops': ''.join(ops), 'side': ''.join(side)})

    tl = ['tl.fromTo("#%s .topline",{opacity:0,y:-18},'
          '{opacity:1,y:0,duration:.4,ease:"power3.out"},0);' % cid]
    if has_fig:
        # 자리부터 보여 준다. 어디를 잡을지 모르는 채로 명령을 치게 두지 않는다.
        tl.append('tl.fromTo("#%s .fig",{opacity:0},'
                  '{opacity:1,duration:.4,ease:"power2.out"},.1);' % cid)
    if ops:
        tl.append('tl.fromTo("#%s .op",{opacity:0,x:-14},'
                  '{opacity:1,x:0,duration:.35,ease:"power2.out"},.15);' % cid)
    if side:
        # 나눈 장의 앞쪽에는 카드가 없다. 없는 것을 향해 트윈을 걸면 GSAP 이
        # 「대상 없음」 경고를 내고, 진짜 결함이 그 경고에 묻힌다.
        tl.append('tl.fromTo("#%s .sc",{opacity:0,y:14},'
                  '{opacity:1,y:0,duration:.35,stagger:.05,ease:"power2.out"},.2);'
                  % cid)
    frags = [round(clock + k + 1.0, 2) for k in range(n_frag)]
    # 노트는 이 장이 실제로 시키는 일에서 만든다. 예전에는 `expect` 와 `why` 만
    # 썼는데, 단계를 나누면 그 둘은 첫 장과 마지막 장에만 남아 가운데 장 마흔
    # 곳이 빈 노트가 됐다 — 검수에서 「대본 누락」으로 올라온 자리다.
    said = []
    for a in acts:
        t = (a.get('type') or '').strip()
        d = plain(ko(a.get('do')))
        line = ('%s — %s' % (t, d)) if t and d else (d or t)
        if line:
            said.append(line)
    notes = ' / '.join(x for x in
                       [' '.join(said)] + [ko(st.get('expect')), ko(st.get('why')),
                                           ko(st.get('pitfall'))] if x)
    return [(body, tl, {'sceneId': cid, 'notes': notes or '—',
                        'sourceStep': st['n'],
                        'sourceActions': list(range(action_start + 1, action_start + len(acts) + 1)),
                        'fragments': frags}, dur)]


CONCEPT_W = {'cards': 2.2, 'para': 1.4, 'fig': 0.0}
CONCEPT_ROOM = 4.4          # 한 장이 감당하는 몫
CONCEPT_ROOM_FIG = 2.6      # 그림이 오른쪽 절반을 가져가면 왼쪽 몫이 줄어든다


def part_notes(sec, page, pi, pnote):
    """이 장이 실제로 담은 내용으로 발표자 노트를 만든다.

    나뉜 개념 절의 모든 장에 절의 lede 를 그대로 붙이고 있었다. 그래서 2/4, 3/4,
    4/4 가 1/4 과 똑같은 한 줄을 노트로 갖고, 검수에서 「대본 누락」으로 올라왔다.
    빈 노트가 아니라 **같은 노트**여서 빈 노트 검사에도 안 걸렸다.

    첫 장은 절을 여는 문장으로 시작하고, 뒷장은 그 장에 있는 글로만 만든다.
    """
    say = []
    if pi == 0 and ko(sec.get('lede')):
        say.append(plain(ko(sec['lede'])))
    for _kind, items in page:
        for h in items:
            t = re.sub(r'\s+', ' ', plain(re.sub(r'<[^>]+>', ' ', h))).strip()
            if t:
                say.append(t)
    if pnote:
        t = re.sub(r'\s+', ' ', plain(re.sub(r'<[^>]+>', ' ', pnote))).strip()
        if t:
            say.append(t)
    out = ' '.join(say).strip()
    return out or (ko(sec.get('lede')) or '—')


def concept_slide(sec, cid, clock):
    """개념 한 절 = 한 장, 넘치면 여러 장.

    절이 무엇으로 짜였는지는 절마다 다르다. 표로 된 절도 있고 카드로 된 절도
    있고, 문단과 그림뿐인 절도 있다. 표만 읽으면 나머지 절은 빈 화면이 된다 —
    「치수선 방향과 기준면」이 실제로 그랬다.

    있는 것을 있는 대로 싣되 한 장에 다 밀어 넣지는 않는다. 밀어 넣으면 카드가
    자기 칸을 넘겨 아래 문단 위로 겹쳐 앉는다. 그렇다고 글자만 줄이면 읽을 수
    없다. 그래서 덩어리마다 몫을 매기고 몫이 차면 장을 넘긴다.

    나누는 단위는 원문의 블록이다. 표 하나를 두 장에 걸쳐 쪼개면 넉 장짜리
    비교가 두 장 대 두 장이 되어 비교가 아니게 된다.
    """
    groups, note = [], ''
    for b in sec.get('blocks', []):
        t = b.get('type')
        if t == 'table':
            cards = []
            for row in b['rows']:
                cells = [rich(ko(c)) for c in row]
                cards.append('<div class="card cc" data-memo="%s"><b>%s</b>'
                             '<strong>%s</strong><span>%s</span></div>'
                             % (esc(ko(row[0])), cells[0],
                                cells[1] if len(cells) > 1 else '',
                                cells[2] if len(cells) > 2 else ''))
            groups.append(('cards', cards))
        elif t == 'cards':
            groups.append(('cards', [
                '<div class="card cc" data-memo="%s"><b>%s</b><span>%s</span></div>'
                % (esc(ko(it.get('label'))), rich(ko(it.get('label'))),
                   rich(ko(it.get('body')))) for it in b['items']]))
        elif t == 'list':
            groups.append(('cards', [
                '<div class="card cc" data-memo="%s"><span>%s</span></div>'
                % (esc(plain(ko(it))[:40]), rich(ko(it))) for it in b['items']]))
        elif t == 'p':
            groups.append(('para', ['<p class="cp" data-memo="%s">%s</p>'
                                    % (esc(plain(ko(b))[:40]), rich(ko(b)))]))
        elif t == 'figure' and b.get('svg') and not any(k == 'fig' for k, _ in groups):
            groups.append(('fig', ['<figure class="cfig"><div class="cfw">%s</div>'
                                   '<figcaption>%s</figcaption></figure>'
                                   % (b['svg'], esc(ko(b.get('caption'))))]))
        elif t == 'note' and not note:
            note = ('<div class="note nn" data-memo="%s"><b class="lb">%s</b>%s</div>'
                    % (esc(ko(b.get('label'))), esc(ko(b.get('label'))), rich(ko(b))))
    if not groups:
        groups = [('para', ['<p class="cp">%s</p>' % rich(ko(sec.get('lede')))])]

    pages, cur, w = [], [], 0.0
    for g in groups:
        kind, items = g
        add = CONCEPT_W[kind] * (1 if kind != 'cards' else max(1, (len(items) + 3) // 4))
        room = CONCEPT_ROOM_FIG if (kind == 'fig' or any(k == 'fig' for k, _ in cur)) \
            else CONCEPT_ROOM
        if cur and w + add > room:
            pages.append(cur)
            cur, w = [], 0.0
        cur.append(g)
        w += add
    if cur:
        pages.append(cur)

    out = []
    for pi, page in enumerate(pages):
        pcid = cid if len(pages) == 1 else '%s%s' % (cid, 'abcdefgh'[pi])
        cards = [h for k, hs in page if k == 'cards' for h in hs]
        paras = [h for k, hs in page if k == 'para' for h in hs]
        pfig = ''.join(h for k, hs in page if k == 'fig' for h in hs)
        pnote = note if pi == len(pages) - 1 else ''
        n_frag = len(cards) + len(paras) + (1 if pfig else 0) + (1 if pnote else 0)
        dur = float(max(1, n_frag))
        cols = 3 if len(cards) in (3, 5, 6) else min(4, max(1, len(cards)))
        left = ''
        if cards:
            left += ('<section class="ccrow" style="grid-template-columns:'
                     'repeat(%d,minmax(0,1fr))">%s</section>' % (cols, ''.join(cards)))
        if paras:
            left += '<div class="cps">%s</div>' % ''.join(paras)
        part = (' <span class="pt">%d / %d</span>' % (pi + 1, len(pages))) if len(pages) > 1 else ''
        body = (
          '<div id="%(c)s-root" data-composition-id="%(c)s" data-start="%(s)s" '
          'data-duration="%(d)s" data-width="1920" data-height="1080" data-label="%(lab)s">\n'
          '<section id="%(c)s" class="clip ss" data-start="%(s)s" data-duration="%(d)s" '
          'data-track-index="1">\n'
          '<header class="topline"><div><div class="index">02 · HOW</div>'
          '<h1>%(title)s</h1></div><div class="prompt">%(lede)s</div></header>\n'
          '<main class="body ccbody%(fx)s">%(main)s%(note)s</main>\n</section>\n</div>'
          % {'c': pcid, 's': clock, 'd': dur,
             'lab': esc(ko(sec.get('label')) + (' (%d/%d)' % (pi + 1, len(pages))
                                                if len(pages) > 1 else '')),
             'title': rich(ko(sec.get('label'))) + part,
             'lede': esc(ko(sec.get('lede'))),
             'fx': ' hasfig' if pfig else '',
             'main': ('<div class="ccmain">%s</div>%s' % (left, pfig)) if pfig else left,
             'note': pnote})

        tl = ['tl.fromTo("#%s .topline",{opacity:0,y:-18},'
              '{opacity:1,y:0,duration:.4,ease:"power3.out"},0);' % pcid]
        k = 0
        for j in range(len(cards)):
            k += 1
            tl.append('tl.fromTo("#%s .cc:nth-child(%d)",{opacity:0,y:16},'
                      '{opacity:1,y:0,duration:.5,ease:"power2.out"},%s);'
                      % (pcid, j + 1, k - 0.5))
        for j in range(len(paras)):
            k += 1
            tl.append('tl.fromTo("#%s .cp:nth-child(%d)",{opacity:0,y:14},'
                      '{opacity:1,y:0,duration:.5,ease:"power2.out"},%s);'
                      % (pcid, j + 1, k - 0.5))
        if pfig:
            k += 1
            tl.append('tl.fromTo("#%s .cfig",{opacity:0},'
                      '{opacity:1,duration:.5,ease:"power2.out"},%s);' % (pcid, k - 0.5))
        if pnote:
            k += 1
            tl.append('tl.fromTo("#%s .nn",{opacity:0,y:12},'
                      '{opacity:1,y:0,duration:.5,ease:"power3.out"},%s);' % (pcid, k - 0.5))
        frags = [round(clock + j + 1.0, 2) for j in range(max(1, n_frag))]
        out.append((body, tl, {'sceneId': pcid, 'notes': part_notes(sec, page, pi, pnote),
                               'fragments': frags}, dur))
        clock += dur
    return out


def split_slide(sec, cid, clock):
    """화면을 둘로 갈라 「이렇게도 됩니다」를 옆에 세운다.

    다른 방법을 본문에 섞으면 자습자는 어느 쪽을 따라가야 하는지 모른다.
    왼쪽이 이 과정이 걷는 길, 오른쪽이 알아 두면 되는 다른 길이다.
    """
    cards = []
    for b in sec.get('blocks', []):
        if b.get('type') == 'cards':
            cards = b['items'][:2]
            break
    if len(cards) != 2:
        raise SystemExit('「%s」 절에 카드가 둘이어야 한다' % ko(sec.get('label')))
    foot = ''
    for b in sec.get('blocks', []):
        if b.get('type') == 'note' and not foot:
            foot = '<b>%s</b> %s' % (esc(ko(b.get('label'))), rich(ko(b)))
    cols = []
    for k, h in enumerate(cards):
        cols.append('<div class="half h%d" data-memo="%s"><div class="tag">%s</div>'
                    '<h3>%s</h3><p class="bd">%s</p>%s</div>'
                    % (k + 1, esc(ko(h.get('label'))),
                       UI['path_here'] if k == 0 else UI['path_other'],
                       rich(ko(h.get('label'))), rich(ko(h.get('body'))),
                       ('<p class="ft">%s</p>' % foot) if (k == 1 and foot) else ''))
    dur = 2.0
    body = (
      '<div id="%(c)s-root" data-composition-id="%(c)s" data-start="%(s)s" '
      'data-duration="%(d)s" data-width="1920" data-height="1080" data-label="%(lab)s">\n'
      '<section id="%(c)s" class="clip ss" data-start="%(s)s" data-duration="%(d)s" '
      'data-track-index="1">\n'
      '<header class="topline"><div><div class="index">02 · ALSO</div><h1>%(title)s</h1></div>'
      '<div class="prompt">%(lede)s</div></header>\n'
      '<main class="body splitbody">%(cols)s</main>\n</section>\n</div>'
      % {'c': cid, 's': clock, 'd': dur, 'lab': esc(ko(sec.get('label'))),
         'title': rich(ko(sec.get('label'))), 'lede': esc(ko(sec.get('lede'))),
         'cols': ''.join(cols)})
    tl = ['tl.fromTo("#%s .topline",{opacity:0,y:-18},'
          '{opacity:1,y:0,duration:.4,ease:"power3.out"},0);' % cid,
          'tl.fromTo("#%s .h1",{opacity:0,x:-18},'
          '{opacity:1,x:0,duration:.5,ease:"power2.out"},.5);' % cid,
          'tl.fromTo("#%s .h2",{opacity:0,x:18},'
          '{opacity:1,x:0,duration:.5,ease:"power2.out"},1.5);' % cid]
    return body, tl, {'sceneId': cid, 'notes': ko(sec.get('lede')) or '—',
                      'fragments': [round(clock + 1.0, 2), round(clock + 2.0, 2)]}, dur


STYLE = """
/* 자습 장 — 프레임 조판을 그대로 쓰고, 조작 목록만 여기서 정한다. */
/* 머리글은 제 높이만, 본문이 남는 높이를 전부 가져간다. 이게 없으면 내용이
   적은 장마다 바닥에 빈 띠가 남는다. */
.ss{display:grid;grid-template-rows:auto minmax(0,1fr);gap:0}
/* 프레임 조판의 .body 는 높이가 724px 로 못 박혀 있다. 강의 프레임에는 맞는
   값이지만 자습 장에서는 그 아래가 통째로 남는다. 자습 장에서만 푼다. */
.ss>.body{min-height:0;height:auto}
.ss .ssbody{display:grid;grid-template-columns:minmax(0,1.24fr) minmax(0,.76fr);
  gap:38px;align-content:stretch;grid-template-rows:minmax(0,1fr)}
/* 한 줄짜리 격자를 본문 높이만큼 늘려 둔다. 줄 높이를 조작 목록에 맞추면
   그보다 긴 카드 칸이 그 높이에 갇혀 「안 되면 여기」가 잘린다. */
/* 프레임 스타일시트의 `.card b{display:block;color:#C7004C;font-size:28px}` 는
   카드 제목을 위한 규칙이다. 본문 안의 **강조**까지 그 규칙에 걸리면 문장 한
   토막이 큰 빨간 제목으로 튀어나온다. 본문의 굵은 글씨는 굵기만 준다. */
.ss .card span b,.ss .card strong b{display:inline;font-size:inherit;color:inherit;
  font-weight:600}
.ss .note .lb{display:block;margin-bottom:6px}
.ss .ops{margin:0;padding:0;list-style:none;display:grid;align-content:center;gap:15px}
.ss .op{display:grid;grid-template-columns:86px minmax(0,1fr);gap:16px;
  align-items:baseline;line-height:1.45;color:#111}
.ss .op .lab{font-size:.62em;color:#666;text-align:right;letter-spacing:.04em;
  white-space:nowrap}
.ss .op.snap .lab,.ss .op.click .lab,.ss .op.move .lab{color:#C7004C}
.ss .op.see{border-left:3px solid #A4A3A4;padding-left:14px;margin-left:-17px}
.ss h1 .pt{font-size:.55em;color:#8A8788;letter-spacing:0;margin-left:12px}
.ss .op.alt{color:#666}
.ss .op.alt .lab{font-style:italic;color:#A4A3A4}
.ss .cmd{display:inline-block;font-family:ui-monospace,Consolas,monospace;
  font-size:.92em;background:#F5F5F3;border:1px solid #A4A3A4;color:#111;
  padding:1px 10px;margin-right:10px;white-space:nowrap}
.ss .op.alt .cmd{background:#FFF;color:#666}
.ss .side{display:grid;align-content:center;gap:16px}
.ss .guide{min-height:0;display:grid;align-content:center;gap:16px}
.ss .side .card{padding:18px 22px}
.ss .side .card b{font-size:1.1em}
.ss .side .card span{margin-top:6px;font-size:1em;line-height:1.5}
.ss .side .card.pit{border-color:#C7004C}
.ss .side .card.pit b{color:#C7004C}
.ss .ccrow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;
  align-content:center}
.ss .ccrow .card{padding:26px 26px 24px}
.ss .ccrow .card strong{font-size:22px;line-height:1.4}
.ss .ccrow .card span{font-size:20px}
/* 개념 장 — 있는 것만 위에서부터 쌓고, 남는 높이는 문단이 가져간다. */
.ss .ccbody{display:flex;flex-direction:column;gap:20px}
.ss .ccbody>.ccrow,.ss .ccmain>.ccrow{flex:0 0 auto}
.ss .ccbody>.note{flex:0 0 auto}
.ss .ccmain{display:flex;flex-direction:column;gap:18px;min-height:0}
.ss .ccbody>.cps,.ss .ccmain>.cps{flex:1 1 auto;display:flex;flex-direction:column;
  justify-content:center;gap:18px;min-height:0}
.ss .cps .cp{margin:0;font-size:27px;line-height:1.6;color:#1A1A1A;
  word-break:keep-all;overflow-wrap:break-word}
.ss .cps .cp+.cp{padding-top:16px;border-top:1px solid #E4E3E1}
/* 그림이 있으면 왼쪽에 글, 오른쪽에 그림. 노트는 아래로 폭 전체를 쓴다. */
.ss .ccbody.hasfig{display:grid;grid-template-rows:minmax(0,1fr) auto;
  grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);column-gap:28px}
.ss .ccbody.hasfig>.note{grid-column:1/-1}
.ss .cfig{margin:0;display:grid;grid-template-rows:minmax(0,1fr) auto;
  gap:10px;min-height:0}
.ss .cfw{display:grid;place-items:center;min-height:0}
.ss .cfw svg{width:100%;height:auto;max-height:100%}
.ss .cfig figcaption{font-size:19px;line-height:1.5;color:#666;
  word-break:keep-all}
/* 자습본 그림의 선 종류. 이름이 짧아 슬라이드 쪽 클래스와 부딪히므로
   반드시 .cfw 안쪽으로만 적용한다 — sc 는 여기선 중심선, 밖에선 점검 카드다. */
.ss .cfw svg{background:#FBFAF8;border:1px solid #D8D2C8;border-radius:4px;
  padding:10px;box-sizing:border-box}
.ss .cfw .si{stroke:#1B1A18;fill:none;stroke-width:1.6}
.ss .cfw .sh{stroke:#A51C30;fill:none;stroke-width:1.9}
.ss .cfw .sd{stroke:#6F695F;fill:none;stroke-width:1}
.ss .cfw .sc{stroke:#A51C30;fill:none;stroke-width:1;
  stroke-dasharray:12 3 3 3;stroke-linecap:butt}
.ss .cfw .sn{stroke:#6F695F;fill:none;stroke-width:1;
  stroke-dasharray:6 3;stroke-linecap:butt}
.ss .cfw .sl{fill:#4A4741;stroke:none;font-size:11px;
  font-family:ui-monospace,Consolas,monospace}
.ss .cfw .slh{fill:#A51C30;stroke:none;font-size:11px;font-weight:700;
  font-family:ui-monospace,Consolas,monospace}
.ss .cfw .sf{fill:#E6E1D9;stroke:none}

/* 코치 마크 — 도면 한 장이 「어디에 올리는가」를 대신 말한다. */
.ss .ssbody.hasfig{grid-template-columns:minmax(0,1.24fr) minmax(0,.76fr);
  grid-template-rows:minmax(0,1fr);align-content:stretch}
.ss .ssbody.hasfig .ops{grid-column:1;grid-row:1;align-content:center;gap:12px}
.ss .ssbody.hasfig .guide{grid-column:2;grid-row:1;align-content:stretch;
  grid-template-rows:minmax(260px,1fr) auto}
.ss .ssbody.hasfig .side{gap:10px;align-content:start;grid-template-columns:minmax(0,1fr)}
.ss .ssbody.hasfig .side .card{padding:12px 16px}
.ss .ssbody.hasfig .side .card b{font-size:20px}
.ss .ssbody.hasfig .side .card span{margin-top:4px;font-size:20px;line-height:1.4}
.ss .fig{margin:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:10px;
  border:2px solid #A4A3A4;background:#F5F5F3;padding:12px 16px 14px}
/* 조작 줄의 코치 마크 번호. 도면 위 표시와 같은 숫자다. */
.ss .op .spotno{display:inline-grid;place-items:center;width:1.15em;height:1.15em;
  border-radius:50%;background:#C7004C;color:#FFF;font-size:.78em;font-weight:700;
  margin-right:.4em;vertical-align:.06em;
  font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif}
.ss .op.pointed .lab{color:#C7004C}
.ss .fig .fh{font-size:19px;letter-spacing:.04em;color:#666}
.ss .construction-key{display:block;margin-top:4px;color:#555;letter-spacing:0}
.ss .construction{color:#666}
.ss .cdwg{width:100%;height:100%;display:block}
.ss .cdwg .outline{fill:none;stroke:#111;stroke-width:.5;vector-effect:non-scaling-stroke}
.ss .cdwg .center{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:6 1.2 1 1.2;
  vector-effect:non-scaling-stroke}
/* 강조 겹선은 기본이 꺼짐이다. 이 단계가 그리는 형상만 켠다. */
.ss .cdwg .hl{fill:none;stroke:none}
.ss .cdwg .hl.hot{stroke:#C7004C;stroke-width:1.9;stroke-linejoin:round;stroke-linecap:round;
  vector-effect:non-scaling-stroke}
.ss .fig .fh b{color:#C7004C}
.ss .coach .ring{fill:none;stroke:#C7004C;stroke-width:1.1;stroke-dasharray:2.6 1.8;
  vector-effect:non-scaling-stroke}
.ss .coach .mk{fill:none;stroke:#C7004C;stroke-width:1.4}
.ss .coach .bg{fill:#C7004C;stroke:none}
.ss .coach .bn{fill:#FFF;font-size:7px;text-anchor:middle;
  font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif}
.ss .fig .cap{margin:0;padding:0;list-style:none;display:grid;gap:7px}
.ss .fig .cap li{display:grid;grid-template-columns:26px minmax(0,1fr);gap:10px;
  align-items:baseline;font-size:21px;line-height:1.4;color:#111}
.ss .fig .cap .bd{display:grid;place-items:center;width:26px;height:26px;border-radius:50%;
  background:#C7004C;color:#FFF;font-size:15px}
.ss .fig .cap em{font-style:normal;color:#C7004C}
/* 한 단계에서 다섯 자리 넘게 찍을 때가 있다. 그때는 목록이 도면을 밀어낸다. */
/* 자리가 다섯 곳을 넘으면 목록이 도면 높이를 다 먹는다. 두 줄로 접는다. */
.ss .fig .cap.many{gap:3px 22px;grid-template-columns:repeat(2,minmax(0,1fr))}
.ss .fig .cap.many li{font-size:17px;grid-template-columns:21px minmax(0,1fr);gap:8px}
.ss .fig .cap.many .bd{width:21px;height:21px;font-size:13px}

/* 분할 화면 — 왼쪽이 이 과정이 걷는 길, 오른쪽이 다른 길. */
.ss .splitbody{grid-template-columns:repeat(2,minmax(0,1fr));align-content:stretch}
.ss .half{border:2px solid #A4A3A4;background:#FFF;padding:30px 34px;
  display:grid;align-content:start;gap:14px}
.ss .half.h2{background:#F5F5F3}
.ss .half .tag{font-size:22px;letter-spacing:.08em;color:#8A8788}
.ss .half.h1 .tag{color:#C7004C}
.ss .half h3{margin:0;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;
  font-size:40px;letter-spacing:-.03em;line-height:1.18;color:#111}
.ss .half .bd{margin:0;font-size:27px;line-height:1.5;color:#111}
.ss .half .ft b{color:#C7004C}
.ss .half .ft{margin:6px 0 0;padding-top:14px;border-top:2px solid #A4A3A4;
  font-size:22px;line-height:1.45;color:#666}
"""


def main(lesson_dir, lesson_json, outpath, include_symbols=True):
    index = io.open(os.path.join(lesson_dir, 'index.html'), encoding='utf-8').read()
    slots = F.slots_of(index)
    if not slots:
        raise SystemExit('index.html 에서 프레임 슬롯을 못 찾았다: %s' % lesson_dir)
    notes = F.notes_for(os.path.join(lesson_dir, 'SCRIPT.md'))
    # 강의 프레임은 자기 대본의 박자에서 조각 자리를 얻는다. 그래야 「다음」이
    # 강의가 걷던 순서 그대로 걷는다.
    tpath = os.path.join(lesson_dir, 'narration-timing.json')
    timing = json.load(io.open(tpath, encoding='utf-8')) if os.path.exists(tpath) else None
    beats, f_start = {}, {}
    if timing:
        for f in timing['frames']:
            f_start[f['frame']] = f['start']
        for b in timing['beats']:
            beats.setdefault(b['frame'], []).append(b['observedStart'])
    script = io.open(os.path.join(lesson_dir, 'SCRIPT.md'), encoding='utf-8').read()
    heads = {int(m.group(3)): m.group(2) for m in F.LINE_HEAD.finditer(script)}

    L = json.load(io.open(lesson_json, encoding='utf-8'))
    steps, sec_of = [], {}
    for s in L['sections']:
        if s.get('kind') != 'practice':
            continue
        for b in s.get('blocks', []):
            if b.get('type') != 'steps':
                continue
            for st in b['items']:
                steps.append(st)
                sec_of[st['n']] = ko(s.get('label'))
    extra = {}
    for name, label, kind in EXTRA.get(L['no'], []):
        extra.setdefault(name, []).append((label, kind))
    by_label = {ident(s.get('label')): s for s in L['sections']}
    # 코치 마크가 앉을 정면도. 도면을 그리는 코드가 하나뿐이라 자습본 쪽
    # 그림과 어긋날 수 없다.
    front = surfaces()

    bodies, tls, slides, clock = [], [], [], 0.0
    dropped = 0
    after = AFTER.get(L['no'])

    def lay_steps():
        """따라 하기를 한 단계 한 장씩 깐다. 차시마다 한 번만 부른다."""
        nonlocal clock
        for st in steps:
            scid = 'ss%dp%02d' % (L['no'], st['n'])
            for b, t, sl, dd in step_slide(st, scid, clock, sec_of[st['n']],
                                           len(steps), front):
                bodies.append(b); tls.append((sl['sceneId'], t))
                slides.append(sl); clock += dd

    for n, (cid, src, _s, dur) in enumerate(slots, 1):
        base = os.path.basename(src)[:-5]
        path = os.path.join(lesson_dir, src.replace('/', os.sep))
        body = F.frame_body(path)
        if base in DROP_FRAMES.get(L['no'], ()):
            continue
        if after is None and FILM.search(body):
            # 시연은 자습본에서 단계 장이 대신한다.
            if dropped == 0:
                lay_steps()
            dropped += 1
            continue
        body = re.sub(r'(id="%s-root"[^>]*?)data-start="0"' % re.escape(cid),
                      r'\1data-start="%s"' % clock, body, count=1)
        # 대본은 프레임 파일 이름으로 번호를 매기고, 시각표는 슬롯 차례로 매긴다.
        # 시연이 05-demo-a·b·c 로 셋인 차시에서는 이 둘이 두 칸 어긋난다. 노트를
        # 슬롯 차례로 찾으면 「확인」 화면에 「오늘 친 것」 대본이 붙고, 마지막 두
        # 화면은 노트가 아예 비어 버린다.
        fnum = int(base[:2]) if base[:2].isdigit() else n
        if 'data-label=' not in body[:400] and heads.get(fnum):
            body = body.replace('data-composition-id="%s"' % cid,
                                'data-composition-id="%s" data-label="%s"'
                                % (cid, esc(heads[fnum])), 1)
        bodies.append('<!-- %s · %s -->\n%s' % (cid, base, body))
        entry = {'sceneId': cid, 'notes': notes.get(fnum, '') or '—'}
        bts, f0 = beats.get(n) or [], f_start.get(n)
        if bts and f0 is not None:
            frag = [round(clock + (t - f0), 2) for t in bts]
            frag = [t for t in frag if clock <= t <= clock + dur]
            if frag:
                entry['fragments'] = frag
        slides.append(entry)
        clock += dur

        for label, kind in extra.get(base, []):
            sec = by_label.get(label)
            if sec is None:
                raise SystemExit('자습본에 「%s」 절이 없다' % label)
            scid = 'ss%dc%d' % (L['no'], len(slides))
            if kind == 'split':
                made = [split_slide(sec, scid, clock)]
            else:
                # 내용이 한 장에 안 들어가면 개념 장은 스스로 여러 장으로 나뉜다.
                made = concept_slide(sec, scid, clock)
            for b, t, sl, d in made:
                bodies.append(b); tls.append((sl['sceneId'], t))
                slides.append(sl); clock += d

        if base == after and not dropped:
            # 녹화 프레임이 없는 차시. 지정한 프레임 뒤에 단계를 깐다.
            lay_steps()
            dropped = 1

    if steps and not dropped:
        raise SystemExit('%d차시 따라 하기를 놓을 자리를 못 찾았다' % L['no'])

    island = json.dumps({'slides': slides, 'slideSequences': [], 'language': 'ko',
                        'practiceSteps': len(steps),
                        'practiceActions': sum(len(st.get('actions', [])) for st in steps)},
                        ensure_ascii=False, indent=1)
    nav = io.open(os.path.join(HERE, 'assets', 'deck_nav.html'), encoding='utf-8').read()
    title = re.search(r'#\s*SCRIPT\s*—\s*(.*)', script)
    title = title.group(1).strip() if title else os.path.basename(lesson_dir)
    made = '\n'.join('<script>(function(){var tl=gsap.timeline({paused:true});%s'
                     'window.__timelines=window.__timelines||{};'
                     'window.__timelines["%s"]=tl;})();</script>' % (''.join(t), cid)
                     for cid, t in tls)

    doc = """<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="UTF-8">
<title>%s · %s</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  *{box-sizing:border-box}
  html,body{margin:0;background:#0B0A0A}
  /* 프레임은 자기가 화면의 전부라고 보고 inset:0 으로 앉는다. 덱에서는 형제라
     무대가 자리를 정해야 하므로 이 세 줄이 이겨야 한다. inset 은 네 변을 한
     번에 쓰는 축약이라 left/top 보다 먼저 지워야 한다. */
  #stage [data-composition-id]{inset:auto!important;position:absolute!important;
    left:50%%!important;top:50%%!important}
%s</style>
</head>
<body>
<script type="application/hyperframes-slideshow+json">
%s
</script>
%s
<script>window.__timelines = window.__timelines || {};</script>
%s
%s
</body>
</html>
""" % (LANG, title, UI['edition'], STYLE, island,
       (surface_defs() if include_symbols else '') + '\n'.join(bodies), made, nav)

    outdir = os.path.dirname(os.path.abspath(outpath))
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    io.open(outpath, 'w', encoding='utf-8', newline='\n').write(doc)
    print('%-30s 슬라이드 %2d (강의 %2d · 자습 %2d) · %.0f초 · %d B'
          % (os.path.basename(lesson_dir.rstrip('/\\')), len(slides),
             len(slides) - len(tls), len(tls), clock, os.path.getsize(outpath)))
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit(__doc__.strip().splitlines()[-1].strip())
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(sys.argv[1], 'deck-selfstudy.html')
    sys.exit(main(sys.argv[1], sys.argv[2], out))
