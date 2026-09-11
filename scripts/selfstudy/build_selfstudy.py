# -*- coding: utf-8 -*-
"""자습 교재 렌더러.

입력  : design/curriculum.json + content/lesson-01..08.json
출력  : docs/autocad-technician/self-study/{index,lesson-0N}.html

자체완결 HTML 하나씩. 외부 스크립트·스타일·이미지·폰트 파일 참조 0.
"""
import io, json, os, re, sys, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('SELFSTUDY_SRC') or os.path.dirname(HERE)
from minify import min_css, min_js


CSS = min_css(io.open(os.path.join(HERE, 'assets', 'base.css'), encoding='utf-8').read())
JS = min_js(io.open(os.path.join(HERE, 'assets', 'app.js'), encoding='utf-8').read())

STAMP = os.environ.get('BUILD_STAMP', '')
# 판의 언어. 영문판은 영문 도면을 받고 영문이 먼저 보인다 — figures.LANG 과 같은 값이다.
LANG = os.environ.get('SELFSTUDY_LANG', 'ko')
PAGE_CAP = 100 * 1024          # 지침 §2 — 단일 파일 100KB. 넘으면 1부/2부로 나눈다

# 정본 도면 — scripts/part/edu_ib_02.py 가 그린 것을 빌드할 때마다 다시 뽑는다.
# 저장소 가드가 이미지 파일을 확장자로 막으므로 .svg 를 커밋하지 않는다.
import figures as _figmod
import coach as _coach
from sheet_figures import SVG_A3 as _SVG_A3
_figdir = os.path.join(HERE, 'figures')
# 강조 겹선(.hl)을 남긴 채로 뽑는다. 코치 마크가 「지금 그리는 것」을 켤 때 쓴다.
# 겹선은 CSS 에서 기본이 stroke:none 이라 켜지 않으면 보이지 않는다.
if os.path.isdir(_figdir) and os.environ.get('SELFSTUDY_FIG_CACHE') == '1':
    FIGURES = {f[:-4]: io.open(os.path.join(_figdir, f), encoding='utf-8').read()
               for f in os.listdir(_figdir) if f.endswith('.svg')}
else:
    FIGURES = _figmod.build_map(keep_hl=True)
FIGURES_HL = FIGURES


# ── 인라인 마크업 ──────────────────────────────────────────────
def esc(s):
    return html.escape(s if s is not None else '', quote=False)


INLINE = re.compile(r'`([^`]+)`|\*\*([^*]+)\*\*')


def rich(s):
    """백틱 → 명령 토큰, **강조** → <b>. 그 밖에는 전부 이스케이프한다."""
    if not s:
        return ''
    out, i = [], 0
    for m in INLINE.finditer(s):
        out.append(esc(s[i:m.start()]))
        if m.group(1) is not None:
            out.append('<span class="cmd">%s</span>' % esc(m.group(1)))
        else:
            out.append('<b>%s</b>' % esc(m.group(2)))
        i = m.end()
    out.append(esc(s[i:]))
    return ''.join(out)


def bi(node, tag='span', cls='', block=False):
    """{'ko':…, 'en':…} 한 쌍을 두 언어 스팬으로 낸다."""
    if node is None:
        return ''
    if isinstance(node, str):
        node = {'ko': node, 'en': node}
    ko, en = node.get('ko', ''), node.get('en', '') or node.get('ko', '')
    c = (cls + ' ') if cls else ''
    sep = '\n' if block else ''
    return ('<%s class="%sk">%s</%s>%s<%s class="%se">%s</%s>'
            % (tag, c, rich(ko), tag, sep, tag, c, rich(en), tag))


def bi_p(node, cls=''):
    return bi(node, 'p', cls, True)


def bi_txt(node):
    """언어별 순수 텍스트 스팬 (인라인 위치용)."""
    return bi(node, 'span', 'txt')


def attr(node):
    """title/alt 등 속성용 — 국문을 쓴다."""
    if isinstance(node, str):
        return html.escape(node, quote=True)
    return html.escape((node or {}).get('ko', ''), quote=True)


# ── 블록 렌더 ──────────────────────────────────────────────────
# 조작 한 줄이 어떤 종류인지. 타이핑과 마우스 작업이 한 덩어리로 보이면
# 자습자가 「어디에 커서를 올려야 하는지」를 문장에서 찾아내야 한다.
ACT_KIND = {
    'ask': {'ko': '묻는 것', 'en': 'It asks'},
    'move': {'ko': '마우스', 'en': 'Mouse'},
    'snap': {'ko': '스냅', 'en': 'Snap'},
    'click': {'ko': '클릭', 'en': 'Click'},
    'key': {'ko': '키', 'en': 'Key'},
    'see': {'ko': '확인', 'en': 'Look'},
    # 같은 점을 다른 방법으로도 찍을 수 있을 때. 한 가지 손동작만 적어 두면
    # 절차서는 되지만 방법을 배우지는 못한다.
    'alt': {'ko': '또는', 'en': 'Or'},
}

NOTE_LABEL = {
    'why': {'ko': '왜', 'en': 'Why'},
    'warn': {'ko': '주의', 'en': 'Watch out'},
    'field': {'ko': '현장에서', 'en': 'On the floor'},
    'tip': {'ko': '도움말', 'en': 'Tip'},
    'pend': {'ko': '공유 예정', 'en': 'To be provided'},
    'recap': {'ko': '정리', 'en': 'Recap'},
}


def render_block(b, ctx):
    t = b.get('type')
    if t == 'p':
        return bi_p(b)
    if t == 'list':
        items = ''.join('<li>%s</li>' % bi(it) for it in b.get('items', []))
        return '<ul class="plain">%s</ul>' % items
    if t == 'cards':
        cs = []
        for it in b.get('items', []):
            cs.append('<div class="card">%s%s</div>'
                      % (bi(it.get('label'), 'p', 'lab', True), bi_p(it.get('body'))))
        return '<div class="cards">%s</div>' % ''.join(cs)
    if t == 'table':
        head = ''.join('<th scope="col">%s</th>' % bi(h) for h in b.get('head', []))
        rows = []
        for r in b.get('rows', []):
            rows.append('<tr>%s</tr>' % ''.join('<td>%s</td>' % bi(c) for c in r))
        cap = ('<caption>%s</caption>' % bi(b['caption'])) if b.get('caption') else ''
        return ('<div class="tw"><table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                % (cap, head, ''.join(rows)))
    if t == 'note':
        tone = b.get('tone', 'tip')
        lab = b.get('label') or NOTE_LABEL.get(tone, NOTE_LABEL['tip'])
        return ('<div class="note %s">%s%s</div>'
                % (esc(tone), bi(lab, 'span', 'lab', True), bi_p(b)))
    if t == 'figure':
        svg = b.get('svg') or FIGURES.get(b.get('ref', ''), '')
        if not svg:
            return ''
        cap = ('<figcaption>%s</figcaption>' % bi(b.get('caption'))) if b.get('caption') else ''
        role = ' role="img" aria-label="%s"' % attr(b.get('alt') or b.get('caption'))
        if svg.startswith('<svg') and 'role=' not in svg[:400]:
            svg = svg.replace('<svg', '<svg' + role, 1)
        fid = (' id="%s"' % esc(b['id'])) if b.get('id') else ''
        return '<figure%s>%s%s</figure>' % (fid, svg, cap)
    if t == 'steps':
        return render_steps(b.get('items', []), ctx)
    return ''


# ── 코치 마크 ──────────────────────────────────────────────────
# 도해는 쪽마다 한 벌만 두고 단계는 `<use>` 로 부른다. 정면도가 14KB 라 단계마다
# 복사해 넣으면 열네 단계에서 이미 100KB 한도를 넘는다(지침 §2).
_SURFACE_SVG = {'sheet': _SVG_A3}


def surface_svg(name):
    if name in _SURFACE_SVG:
        return _SURFACE_SVG[name]
    return FIGURES_HL.get(_coach.FIG_OF.get(name, name), '')


def coach_figure(st, ctx):
    """이 단계가 잡을 자리를 도면 위에 찍는다. `spots` 가 없으면 아무것도 안 낸다."""
    spots = st.get('spots')
    if not spots and not st.get('construction'):
        return ''
    spots = spots or []
    surface = st.get('on', 'front')
    svg = surface_svg(surface)
    if not svg:
        return ''
    ctx.setdefault('surfaces', set()).add(surface)
    feature = st.get('feature')
    only = {n for a in st.get('actions', []) for n in _coach.spot_badges(a)} or None
    body, _caps = _coach.marks(spots, surface, only)
    temporary = _coach.construction_for(st, surface)
    head = ('지금 그리는 것 — <b>%s</b>' % esc(_coach.FEATURE_KO[feature])) \
        if feature in _coach.FEATURE_KO else '도면 위에서 지금 잡을 자리'
    if temporary:
        head += ' · <span class="k">점선: 이 단계의 임시선·가공 전 선</span><span class="e">Dashed: temporary or pre-edit lines</span>'
    if st.get('diagramOnly'):
        head = '<span class="k">이 단계의 작도 도해 · 점선: 조작할 선</span><span class="e">Step diagram · dashed: lines to act on</span>'
    elif st.get('diagramNote'):
        head += '<br>' + bi(st['diagramNote'], 'span')
    base = '' if st.get('diagramOnly') else _coach.use_tag('sfc-' + surface, svg) + _coach.hl_for(svg, feature)
    # 자리 설명을 도면 아래에 또 적지 않는다. 같은 말이 조작 줄에 있고, 번호로
    # 서로 짚는다. 비는 자리는 도면이 가져간다.
    return ('<figure class="coachfig" data-memo="도면 코치 마크">'
            '<div class="fh">%s</div>'
            '<svg class="dwg cdwg" viewBox="%s" role="img" aria-label="%s">'
            '%s%s<g class="coach">%s</g></svg></figure>'
            % (head, _coach.figure_viewbox(st, surface, svg), attr('이 단계의 도면과 선택점'),
               base, temporary, body))


def surface_defs(used):
    """쪽에서 쓴 바탕을 `<symbol>` 로 한 번 심는다."""
    if not used:
        return ''
    syms = []
    for name in sorted(used):
        svg = surface_svg(name)
        if svg:
            syms.append(_coach.to_symbol(svg, 'sfc-' + name))
    if not syms:
        return ''
    return ('<svg class="sfcdefs" aria-hidden="true" focusable="false" '
            'style="position:absolute;width:0;height:0;overflow:hidden">%s</svg>'
            % ''.join(syms))


def render_steps(items, ctx):
    lis = []
    for st in items:
        sid = '%s-s%s' % (ctx['lesson'], st.get('n'))
        acts = []
        for a in st.get('actions', []):
            cmd = a.get('type')
            # 치는 값이 판마다 다를 수 있다 — 레이어 이름이 그렇다. `bi` 는
            # 문자열이면 두 쪽에 같은 값을, 사전이면 각 쪽에 제 값을 낸다.
            tok = ('<span class="cmd">%s</span>' % bi(cmd)) if cmd else ''
            # 마우스로 하는 일은 타이핑과 다른 종류의 동작이다. 한 줄에 뭉쳐 두면
            # 「어디에 올리고 무엇이 뜨면 누르는지」가 문장 속에 묻힌다.
            kind = a.get('kind')
            lab = ''
            if kind and kind in ACT_KIND:
                lab = bi(ACT_KIND[kind], 'span', 'kind', False)
            # 도면 위 자리 표시와 같은 번호. 도면 아래에 같은 말을 또 적는 대신
            # 여기서 대조한다.
            badge = ''.join('<span class="spotno">%d</span>' % n
                            for n in _coach.spot_badges(a))
            acts.append('<div class="act %s%s">%s%s%s%s</div>'
                        % (esc(kind or ''), ' pointed' if badge else '',
                           lab, badge, tok, bi_txt(a.get('do'))))
        foot = []
        if st.get('expect'):
            foot.append('<div><b class="k">이렇게 되면 맞습니다</b><b class="e">You did it right if</b>%s</div>'
                        % bi_txt(st['expect']))
        if st.get('why'):
            foot.append('<div><b class="k">왜 이 순서인가</b><b class="e">Why this order</b>%s</div>'
                        % bi_txt(st['why']))
        if st.get('pitfall'):
            foot.append('<div class="pit"><b class="k">안 되면 여기</b><b class="e">If it went wrong</b>%s</div>'
                        % bi_txt(st['pitfall']))
        chk = ('<label class="chk"><input type="checkbox" data-step="%s">'
               '<span class="k">완료</span><span class="e">done</span></label>' % esc(sid))
        fig = coach_figure(st, ctx)
        lis.append('<li data-memo="%s"%s><p class="st-h">%s%s</p>%s%s<div class="st-f">%s</div></li>'
                   % (attr(ctx['label'] + ' · ' + str(st.get('n')) + '단계'),
                      ' class="hasfig"' if fig else '',
                      bi(st.get('title')), chk, fig, ''.join(acts), ''.join(foot)))
    return '<ol class="steps">%s</ol>' % ''.join(lis)


# 절 하나가 쪽 예산을 통째로 넘으면 쪽 나누기가 할 수 있는 일이 없다. 따라 하기
# 절은 단계가 열일곱까지 가고 단계마다 코치 마크가 붙어서 실제로 그렇게 됐다.
# 단계를 나눠 두 절로 낸다 — 자르는 자리는 단계 경계라 절차가 끊기지 않는다.
SECTION_CAP = 44 * 1024


def render_section_split(sec, n, ctx):
    """절 하나를 렌더한다. 너무 크면 단계 경계에서 나눠 여럿으로 낸다."""
    whole = render_section(sec, n, ctx)
    if len(whole.encode('utf-8')) <= SECTION_CAP:
        return [whole]
    blocks = sec.get('blocks', [])
    idx = next((i for i, b in enumerate(blocks)
                if b.get('type') == 'steps' and len(b.get('items', [])) > 3), None)
    if idx is None:
        return [whole]
    items = blocks[idx]['items']
    parts = max(2, -(-len(whole.encode('utf-8')) // SECTION_CAP))
    parts = min(parts, len(items))
    size = -(-len(items) // parts)
    chunks = [items[i:i + size] for i in range(0, len(items), size)]
    out = []
    for k, chunk in enumerate(chunks):
        part = dict(sec)
        part['blocks'] = (list(blocks[:idx]) if k == 0 else []) \
            + [dict(blocks[idx], items=chunk)] \
            + (list(blocks[idx + 1:]) if k == len(chunks) - 1 else [])
        if k:
            part = dict(part, id='%s-%d' % (sec.get('id', 'sec'), k + 1), lede=None)
            lab = dict(sec.get('label') or {})
            for lang, tail in (('ko', ' (이어서)'), ('en', ' (continued)')):
                if lab.get(lang):
                    lab[lang] = lab[lang] + tail
            part['label'] = lab
        out.append(render_section(part, n, ctx))
    return out


def render_section(sec, n, ctx):
    ctx = dict(ctx, label=(sec.get('label') or {}).get('ko', ''))
    head = '<h2%s id="%s"><span class="num">%02d</span>%s</h2>' % (
        ' class="first"' if n == 1 else '', esc(sec.get('id', 'sec%d' % n)), n, bi(sec.get('label')))
    lede = bi_p(sec['lede'], 'lede') if sec.get('lede') else ''
    body = ''.join(render_block(b, ctx) for b in sec.get('blocks', []))
    return '<section data-memo="%s">%s%s%s</section>' % (attr(ctx['label']), head, lede, body)


# ── 문서 뼈대 ──────────────────────────────────────────────────
def shell(title, eyebrow, h1, meta, tabs, panels, pager='', grade='S', body_attrs=''):
    tabbar = ''.join(
        '<button role="tab" id="t-%s" aria-controls="%s" aria-selected="false" tabindex="-1">%s</button>'
        % (pid, pid, bi(lab)) for pid, lab in tabs)
    body = ''.join(
        '<section role="tabpanel" id="%s" aria-labelledby="t-%s" tabindex="0" hidden>%s</section>'
        % (pid, pid, content) for pid, content in panels)
    return """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="color-scheme" content="light dark">
<style>%(css)s</style>
</head>
<body data-lang="%(lang)s"%(battrs)s>
<p class="translation-status"><span class="k">국문을 먼저 검수합니다. 영문은 의미를 맞춘 초안이며 국문 완료 후 정식 제작합니다.</span><span class="e">Korean is reviewed first. English is an alignment draft; full English production follows Korean approval.</span></p>
<p class="translation-status"><span class="k">음성 구성 시간은 내레이션과 화면 전환을 합친 길이입니다. 2~7차시는 실제 녹화 후 길이가 달라질 수 있습니다.</span><span class="e">Narrated timeline duration includes narration and scene transitions. Lessons 2–7 may change in length after screen recording.</span></p>
<div class="banner"><span class="k">이 파일은 <b>내려받아 브라우저로 열어야</b> 메모 저장과 진도 저장이 동작합니다. 미리보기 창에서는 저장이 막힐 수 있어요.</span><span class="e">Download this file and open it in a browser — notes and progress only persist there. Sandboxed previews may block storage.</span></div>
<header class="top">
  <div class="bar">
    <div class="brand">
      <p class="eyebrow">%(eyebrow)s</p>
      <h1>%(h1)s</h1>
      <p class="meta">%(meta)s</p>
    </div>
    <div class="tools">
      <span class="seg" role="group" aria-label="언어 / Language">
        <button type="button" class="t" data-lang-btn="ko" aria-pressed="%(kopressed)s">국문</button>
        <button type="button" class="t" data-lang-btn="en" aria-pressed="%(enpressed)s" aria-label="English edition">EN</button>
      </span>
      <button type="button" class="t" id="theme-btn"><span class="k">자동</span><span class="e">Auto</span></button>
      <button type="button" class="t" id="memo-btn" aria-pressed="false" aria-controls="memo"><span class="k">&#128221; 메모</span><span class="e">&#128221; Notes</span></button>
    </div>
  </div>
  <nav class="tabs" role="tablist" aria-label="문서 구역 / Sections">%(tabbar)s</nav>
</header>
<main>%(body)s%(pager)s</main>
<aside id="memo" data-open="0" aria-hidden="true" aria-label="메모 / Notes">
  <div class="memo-hd">
    <h2><span class="k">메모</span><span class="e">Notes</span></h2>
    <button type="button" class="t" id="memo-close"><span class="k">닫기</span><span class="e">Close</span></button>
  </div>
  <div class="memo-list" id="memo-list"></div>
  <div class="memo-ft">
    <button type="button" class="t" id="memo-copy"><span class="k">메모 &#8594; 프롬프트 복사</span><span class="e">Notes &#8594; copy as prompt</span></button>
    <button type="button" class="t" id="memo-show"><span class="k">복사할 내용 보기</span><span class="e">Show what gets copied</span></button>
    <textarea id="memo-out" hidden aria-label="복사할 프롬프트 / Prompt to copy"></textarea>
  </div>
</aside>
<button type="button" id="pick"><span class="k">&#128221; 메모</span><span class="e">&#128221; Note</span></button>
<script>%(js)s</script>
</body>
</html>
""" % {'title': html.escape(title, quote=True), 'css': CSS, 'js': JS, 'eyebrow': eyebrow,
       'h1': h1, 'meta': meta, 'grade': grade, 'tabbar': tabbar, 'body': body,
       'pager': pager, 'battrs': body_attrs,
       'lang': LANG, 'kopressed': str(LANG == 'ko').lower(),
       'enpressed': str(LANG == 'en').lower()}


# 스타일·스크립트·헤더가 먹는 고정 비용. 쪽을 나눌 때 예산에서 먼저 뺀다.
SHELL_BYTES = len(shell('t', 'e', 'h', 'm',
                        [('p-x', {'ko': '개념', 'en': 'Concepts'})],
                        [('p-x', '')], '', 'S', '').encode('utf-8'))


# ── 차시 페이지 ────────────────────────────────────────────────
TAB_OF_KIND = {
    'orient': 'concept', 'concept': 'concept', 'onDrawing': 'concept',
    'practice': 'practice', 'verify': 'practice',
    'recap': 'check', 'shortcuts': 'check', 'checks': 'check', 'exercise': 'check',
}


def build_lesson(L, nav):
    no = L['no']
    lid = 'L%02d' % no
    ctx = {'lesson': lid, 'label': ''}

    # 요약 탭
    s = L.get('summary', {})
    sum_html = ['<h2 class="first"><span class="num">01</span><span class="k">이 차시는 무엇인가</span><span class="e">What this lesson is</span></h2>']
    sum_html.append('<div class="cards">')
    for key, lab in (('what', {'ko': '무엇을', 'en': 'What'}),
                     ('why', {'ko': '왜', 'en': 'Why'}),
                     ('where', {'ko': '지금 어디까지', 'en': 'Where you are'})):
        if s.get(key):
            sum_html.append('<div class="card">%s%s</div>' % (bi(lab, 'p', 'lab', True), bi_p(s[key])))
    sum_html.append('</div>')

    if L.get('objectives'):
        sum_html.append('<h3><span class="k">이 차시를 마치면</span><span class="e">By the end you can</span></h3>')
        sum_html.append('<ul class="plain">%s</ul>'
                        % ''.join('<li>%s</li>' % bi(o) for o in L['objectives']))

    rows = [[{'ko': '음성 구성 시간', 'en': 'Narrated timeline duration'}, {'ko': L.get('videoLength', '—'), 'en': L.get('videoLength', '—')}],
            [{'ko': '자습 소요(권장)', 'en': 'Self-study time'},
             {'ko': '약 %d분' % L.get('selfStudyMin', 0), 'en': 'about %d min' % L.get('selfStudyMin', 0)}],
            [{'ko': '여는 파일', 'en': 'Open this file'},
             {'ko': '`%s`' % L['opens'] if L.get('opens') else '없음 — 작도하지 않습니다',
              'en': '`%s`' % L['opens'] if L.get('opens') else 'none — no drawing in this lesson'}],
            [{'ko': '저장하는 상태', 'en': 'Save as'},
             {'ko': '`%s`' % L['saves'] if L.get('saves') else '없음',
              'en': '`%s`' % L['saves'] if L.get('saves') else 'none'}]]
    sum_html.append(render_block({'type': 'table',
                                  'caption': {'ko': '시작 전에 확인할 것', 'en': 'Check before you start'},
                                  'head': [{'ko': '항목', 'en': 'Item'}, {'ko': '값', 'en': 'Value'}],
                                  'rows': rows}, ctx))

    before = L.get('before', {})
    if before.get('checklist'):
        sum_html.append('<h3><span class="k">준비 확인</span><span class="e">Pre-flight</span></h3>')
        sum_html.append('<ul class="plain">%s</ul>'
                        % ''.join('<li>%s</li>' % bi(c) for c in before['checklist']))
    if before.get('recovery'):
        sum_html.append(render_block({'type': 'note', 'tone': 'tip',
                                      'label': {'ko': '앞 차시를 건너뛰었다면', 'en': 'If you skipped the previous lesson'},
                                      'ko': before['recovery'].get('ko', ''),
                                      'en': before['recovery'].get('en', '')}, ctx))
    prog_html = ''
    if boxes_count(L):
        prog_html = ('<div class="noprint">'
                     '<h3><span class="k">진도</span><span class="e">Progress</span></h3>'
                     '<p class="lede"><span class="k">단계를 체크하면 여기에 쌓입니다. 브라우저에만 저장돼요.</span>'
                     '<span class="e">Ticking the steps fills this bar. It is stored in your browser only.</span></p>'
                     '<div class="bar-wrap"><div class="bar-fill" id="prog-fill"></div></div>'
                     '<p class="meta"><span id="prog-txt">0 / 0</span> &nbsp;'
                     '<button type="button" class="t" id="reset-prog">'
                     '<span class="k">진도 초기화</span><span class="e">Reset progress</span></button></p></div>')

    # 개념 · 실습 · 점검 탭
    buckets = {'concept': [], 'practice': [], 'check': []}
    counters = {'concept': 0, 'practice': 0, 'check': 0}
    for sec in L.get('sections', []):
        tab = sec.get('tab') or TAB_OF_KIND.get(sec.get('kind'), 'concept')
        counters[tab] += 1
        for h in render_section_split(sec, counters[tab], ctx):
            buckets[tab].append(h)

    # 점검 탭 고정 구성물
    chk = list(buckets['check'])
    if L.get('verify'):
        counters['practice'] += 1
        buckets['practice'].append(render_section({
            'id': 'verify', 'kind': 'verify',
            'label': {'ko': '검산 — 맞게 그렸는지 스스로 확인합니다', 'en': 'Cross-check — confirm it yourself'},
            'lede': {'ko': '강사가 봐 주지 않습니다. 아래는 눈대중이 아니라 값으로 판정할 수 있는 것만 모았어요.',
                     'en': 'Nobody is looking over your shoulder. Every item below is decided by a number, not by eye.'},
            'blocks': [{'type': 'table',
                        'head': [{'ko': '확인할 것', 'en': 'Check'}, {'ko': '보는 방법', 'en': 'How'}],
                        'rows': [[v.get('what', v), v.get('how', {'ko': '', 'en': ''})] for v in L['verify']]}],
        }, counters['practice'], ctx))

    if L.get('checks'):
        n = counters['check'] + 1
        qs = ''.join('<details class="q"><summary>%s</summary><div class="ans">%s</div></details>'
                     % (bi(c.get('q')), bi(c.get('a'))) for c in L['checks'])
        chk.append('<section data-memo="자가 점검"><h2%s id="checks"><span class="num">%02d</span>'
                   '<span class="k">자가 점검</span><span class="e">Check yourself</span></h2>'
                   '<p class="lede"><span class="k">먼저 답해 보고 펼치세요. 막히면 그 절로 돌아가면 됩니다.</span>'
                   '<span class="e">Answer first, then open. If you are stuck, go back to that section.</span></p>%s</section>'
                   % (' class="first"' if n == 1 else '', n, qs))
        counters['check'] = n

    if L.get('exercise'):
        n = counters['check'] + 1
        ex = L['exercise']
        crit = ''
        if ex.get('criteria'):
            crit = ('<h3><span class="k">스스로 채점하는 기준</span><span class="e">Grade yourself on</span></h3>'
                    '<ul class="plain">%s</ul>' % ''.join('<li>%s</li>' % bi(c) for c in ex['criteria']))
        chk.append('<section data-memo="과제"><h2%s id="exercise"><span class="num">%02d</span>%s</h2>%s%s</section>'
                   % (' class="first"' if n == 1 else '', n, bi(ex.get('title')), bi_p(ex.get('body')), crit))
        counters['check'] = n

    if L.get('shortcuts'):
        n = counters['check'] + 1
        rows = [[{'ko': '`%s`' % sc['key'], 'en': '`%s`' % sc['key']}, sc.get('name'), sc.get('when')]
                for sc in L['shortcuts']]
        chk.append('<section data-memo="오늘 친 것"><h2%s id="keys"><span class="num">%02d</span>'
                   '<span class="k">오늘 친 것</span><span class="e">What you typed today</span></h2>%s</section>'
                   % (' class="first"' if n == 1 else '', n,
                      render_block({'type': 'table',
                                    'head': [{'ko': '명령', 'en': 'Command'}, {'ko': '이름', 'en': 'Name'},
                                             {'ko': '언제 쓰나', 'en': 'When you use it'}],
                                    'rows': rows}, ctx)))
        counters['check'] = n

    rc = L.get('recap', {})
    if rc:
        n = counters['check'] + 1
        did = ''.join('<li>%s</li>' % bi(d) for d in rc.get('did', []))
        nxt = bi_p(rc['next']) if rc.get('next') else ''
        chk.append('<section data-memo="마무리"><h2%s id="recap"><span class="num">%02d</span>'
                   '<span class="k">이번에 한 일 · 다음</span><span class="e">What you did · what is next</span></h2>'
                   '<div class="cards"><div class="card"><p class="lab k">이번에 한 일</p><p class="lab e">What you did</p>'
                   '<ul class="plain">%s</ul></div>'
                   '<div class="card"><p class="lab k">다음</p><p class="lab e">Next</p>%s</div></div></section>'
                   % (' class="first"' if n == 1 else '', n, did, nxt))
        counters['check'] = n

    buckets['check'] = chk

    meta = ('<span class="k">작성 %s · AutoCAD 교육 과정 · 자습 약 %d분 (음성 구성 시간 %s) · </span>'
            '<span class="e">Written %s · AutoCAD course · about %d min self-study (narrated timeline duration %s) · </span>'
            % (STAMP, L.get('selfStudyMin', 0), L.get('videoLength', '—'),
               STAMP, L.get('selfStudyMin', 0), L.get('videoLength', '—')))
    tko = (L.get('title') or {}).get('ko', '')
    eyebrow = 'LG이노텍 Green Star · for technician · %d차시 / 8' % no
    eyebrow_en = 'LG Innotek Green Star · for technician · Lesson %d / 8' % no
    prev_l, next_l = nav
    a_name, b_name = 'lesson-%02d.html' % no, 'lesson-%02d-2.html' % no

    def link(href, ko, en):
        return ('<a href="%s"><span class="k">%s</span><span class="e">%s</span></a>'
                % (href, ko, en))

    def pager_of(left, right):
        return ('<nav class="pager" aria-label="이동 / Navigation">%s<span class="sp"></span>'
                '%s<span class="sp"></span>%s</nav>'
                % (left or '<span></span>',
                   link('index.html', '&#9776; 과정 전체', '&#9776; All lessons'),
                   right or '<span></span>'))

    prev_link = link('lesson-%02d.html' % prev_l, '&#8592; %d차시' % prev_l,
                     '&#8592; Lesson %d' % prev_l) if prev_l else None
    next_link = link('lesson-%02d.html' % next_l, '%d차시 &#8594;' % next_l,
                     'Lesson %d &#8594;' % next_l) if next_l else None

    # ── 절을 쪽에 담는다 — 한 쪽이 100KB 를 넘지 않게 순서대로 채운다 ──
    KIND = {'concept': ('p-con', {'ko': '개념', 'en': 'Concepts'}, '개념', 'Concepts'),
            'practice': ('p-pra', {'ko': '실습', 'en': 'Practice'}, '실습', 'Practice'),
            'check': ('p-chk', {'ko': '점검', 'en': 'Check'}, '점검', 'Check')}
    units = ([('concept', h) for h in buckets['concept']]
             + [('practice', h) for h in buckets['practice']]
             + [('check', h) for h in buckets['check']])
    budget = PAGE_CAP - SHELL_BYTES - 3072
    # 코치 마크의 바탕 도해는 쪽마다 한 벌씩 들어간다. 정면도만 14KB 라 이걸
    # 빼 두지 않으면 담을 때는 들어갔다가 낼 때 한도를 넘는다.
    surfaces_used = set(re.findall(r'href="#sfc-([\w-]+)"', ''.join(h for _k, h in units)))
    budget -= len(surface_defs(surfaces_used).encode('utf-8'))
    head_b = len(''.join(sum_html).encode('utf-8')) + len(prog_html.encode('utf-8')) + 1400
    sizes = [len(h.encode('utf-8')) for _, h in units]

    def pack(soft):
        out, cur, used = [], [], head_b
        for (kind, h), n_b in zip(units, sizes):
            if cur and used + n_b > min(budget, soft):
                out.append(cur)
                cur, used = [], 0
            cur.append((kind, h))
            used += n_b
        if cur:
            out.append(cur)
        return out or [[]]

    pages = pack(budget)
    # 마지막 쪽만 얇게 남지 않도록, 필요한 쪽수 안에서 고르게 다시 담는다
    if len(pages) > 1:
        target = (head_b + sum(sizes)) // len(pages) + 1
        even = pack(max(target, max(sizes) if sizes else 0))
        if len(even) == len(pages):
            pages = even

    total = len(pages)
    names = ['lesson-%02d.html' % no] + ['lesson-%02d-%d.html' % (no, i + 1)
                                         for i in range(1, total)]
    body_attrs = ' data-progress-key="lesson-%02d" data-step-total="%d"' % (no, boxes_count(L))

    out = []
    for i, page_units in enumerate(pages):
        kinds = [k for k in ('concept', 'practice', 'check')
                 if any(u[0] == k for u in page_units)]
        tabs, panels = [], []
        has_steps = 'practice' in kinds
        if i == 0:
            note = ''
            if total > 1:
                nxt_ko = ' · '.join(KIND[k][2] for k in
                                    [kk for kk in ('concept', 'practice', 'check')
                                     if any(u[0] == kk for p in pages[1:] for u in p)])
                nxt_en = ' · '.join(KIND[k][3] for k in
                                    [kk for kk in ('concept', 'practice', 'check')
                                     if any(u[0] == kk for p in pages[1:] for u in p)])
                note = render_block({'type': 'note', 'tone': 'tip',
                                     'label': {'ko': '이 차시는 %d쪽으로 나뉩니다' % total,
                                               'en': 'This lesson runs across %d pages' % total},
                                     'ko': '분량이 커서 나눴어요. 뒤쪽에 %s이 있습니다. '
                                           '맨 아래 이동 링크로 이어서 보시면 됩니다. '
                                           '진도 체크는 어느 쪽에서 하든 한 차시로 합쳐집니다.' % nxt_ko,
                                     'en': 'It is long, so it is split. %s follow on the later pages. '
                                           'Use the links at the bottom to continue. '
                                           'Progress ticks add up across the pages of one lesson.' % nxt_en}, ctx)
            tabs.append(('p-sum', {'ko': '요약', 'en': 'Overview'}))
            panels.append(('p-sum', ''.join(sum_html) + note + (prog_html if has_steps else '')))
        elif has_steps:
            pass
        for k in kinds:
            pid, lab, _, _ = KIND[k]
            body = ''.join(h for kk, h in page_units if kk == k)
            if k == 'practice' and i > 0:
                body = prog_html + body
            tabs.append((pid, lab))
            panels.append((pid, body))

        # 코치 마크가 부르는 바탕만 이 쪽에 심는다. 쪽마다 실제로 쓴 것만 찾아
        # 넣어야 안 쓰는 도해 14KB 가 따라붙지 않는다.
        used = set(re.findall(r'href="#sfc-([\w-]+)"', ''.join(h for _p, h in panels)))
        defs = surface_defs(used)
        if defs and panels:
            panels[0] = (panels[0][0], defs + panels[0][1])

        part_ko = ' · '.join(KIND[k][2] for k in kinds)
        part_en = ' · '.join(KIND[k][3] for k in kinds)
        if total > 1:
            suffix_ko = ' — %d부 · %s' % (i + 1, part_ko)
            suffix_en = ' — Part %d · %s' % (i + 1, part_en)
            title = '%d차시 %d부 · %s — AutoCAD Technician 자습' % (no, i + 1, tko)
            eyeb = ('<span class="k">%s · %d부 %s</span><span class="e">%s · Part %d %s</span>'
                    % (eyebrow, i + 1, part_ko, eyebrow_en, i + 1, part_en))
        else:
            suffix_ko = suffix_en = ''
            title = '%d차시 · %s — AutoCAD Technician 자습' % (no, tko)
            eyeb = ('<span class="k">%s</span><span class="e">%s</span>' % (eyebrow, eyebrow_en))
        h1 = bi({'ko': tko + suffix_ko,
                 'en': (L.get('title') or {}).get('en', '') + suffix_en})

        left = (link(names[i - 1], '&#8592; %d부' % i, '&#8592; Part %d' % i)
                if i > 0 else prev_link)
        right = (link(names[i + 1], '%d부 &#8594;' % (i + 2), 'Part %d &#8594;' % (i + 2))
                 if i + 1 < total else next_link)
        out.append({'name': names[i],
                    'html': shell(title, eyeb, h1, meta, tabs, panels,
                                  pager_of(left, right), grade='S', body_attrs=body_attrs),
                    'steps': has_steps and bool(prog_html),
                    'part': i + 1, 'parts': total, 'kinds': kinds})
    return out


def boxes_count(L):
    n = 0
    for sec in L.get('sections', []):
        for b in sec.get('blocks', []):
            if b.get('type') == 'steps':
                n += len(b.get('items', []))
    return n


# ── 인덱스 ─────────────────────────────────────────────────────
def build_index(C, lessons, progress_file=None, part2=None):
    ctx = {'lesson': 'IDX', 'label': ''}
    progress_file = progress_file or {}
    part2 = part2 or {}
    total_min = sum(l.get('selfStudyMin', 0) for l in lessons)

    ov = ['<h2 class="first"><span class="num">01</span><span class="k">이 과정은 무엇인가</span><span class="e">What this course is</span></h2>']
    ov.append('<div class="cards">')
    for lab, node in (({'ko': '무엇을', 'en': 'What'}, C.get('subtitle')),
                      ({'ko': '누구를 위한 것인가', 'en': 'Who it is for'}, C.get('audience')),
                      ({'ko': '지금 어디까지', 'en': 'Where it stands'}, C.get('status'))):
        if node:
            ov.append('<div class="card">%s%s</div>' % (bi(lab, 'p', 'lab', True), bi_p(node)))
    ov.append('</div>')
    if C.get('outcomes'):
        ov.append('<h3><span class="k">과정을 마치면</span><span class="e">By the end you can</span></h3>'
                  '<ul class="plain">%s</ul>' % ''.join('<li>%s</li>' % bi(o) for o in C['outcomes']))
    if C.get('prerequisites'):
        ov.append('<h3><span class="k">시작하기 전에</span><span class="e">Before you start</span></h3>'
                  '<ul class="plain">%s</ul>' % ''.join('<li>%s</li>' % bi(o) for o in C['prerequisites']))
    if C.get('timeBasis'):
        ov.append(render_block({'type': 'note', 'tone': 'why',
                                'label': {'ko': '자습 시간 %d분(약 %.1f시간)은 이렇게 나왔습니다' % (total_min, total_min / 60.0),
                                          'en': 'How the %d-minute estimate was derived' % total_min},
                                'ko': C['timeBasis'].get('ko', ''), 'en': C['timeBasis'].get('en', '')}, ctx))
    if C.get('navigationDesign'):
        ov.append(render_block({'type': 'note', 'tone': 'tip',
                                'label': {'ko': '이 교재를 보는 법', 'en': 'How to use this material'},
                                'ko': C['navigationDesign'].get('ko', ''),
                                'en': C['navigationDesign'].get('en', '')}, ctx))

    cur = ['<h2 class="first"><span class="num">01</span><span class="k">차시</span><span class="e">Modules</span></h2>',
           '<p class="lede"><span class="k">부품 하나를 일곱 차시에 걸쳐 이어 그립니다. 차시마다 앞 차시가 저장한 파일을 열어요.</span>'
           '<span class="e">One part, drawn across seven lessons. Each lesson opens the file the previous one saved.</span></p>',
           '<ul class="mods">']
    for l in lessons:
        no = l['no']
        sub = []
        if l.get('opens'):
            sub.append('%s 열기' % l['opens'])
        if l.get('saves'):
            sub.append('%s 저장' % l['saves'])
        subk = ' · '.join(sub) if sub else '작도 없음'
        sube = ' · '.join(['open %s' % l['opens']] if l.get('opens') else []
                          + (['save %s' % l['saves']] if l.get('saves') else [])) or 'no drawing'
        cur.append('<li><a class="mod" href="lesson-%02d.html">'
                   '<span class="no">%d</span>'
                   '<span><span class="tt">%s</span><span class="sub k">%s</span><span class="sub e">%s</span></span>'
                   '<span class="rt"><span class="k">약 %d분</span><span class="e">~%d min</span>'
                   '<br><span data-prog-of="%s" data-empty="&#8212;"></span></span>'
                   '</a></li>'
                   % (no, no, bi(l.get('title')), esc(subk), esc(sube),
                      l.get('selfStudyMin', 0), l.get('selfStudyMin', 0),
                      progress_file.get(no, 'lesson-%02d' % no)))
        for p in part2.get(no, []):
            cur.append('<li><a class="mod" href="%s"><span class="no">&#8942;</span>'
                       '<span><span class="tt"><span class="k">%d차시 %d부 · %s</span>'
                       '<span class="e">Lesson %d Part %d · %s</span></span></span>'
                       '<span class="rt"></span></a></li>'
                       % (p['name'], no, p['part'], p['ko'], no, p['part'], p['en']))
    cur.append('</ul>')
    cur.append(render_block({'type': 'table',
                             'caption': {'ko': '차시가 이어지는 방식 — 파일 하나가 계속 자랍니다',
                                         'en': 'How the lessons chain — one file keeps growing'},
                             'head': [{'ko': '차시', 'en': 'Lesson'}, {'ko': '여는 파일', 'en': 'Opens'},
                                      {'ko': '저장하는 상태', 'en': 'Saves'}],
                             'rows': [[{'ko': '%d차시' % l['no'], 'en': 'Lesson %d' % l['no']},
                                       {'ko': '`%s`' % l['opens'] if l.get('opens') else '—',
                                        'en': '`%s`' % l['opens'] if l.get('opens') else '—'},
                                       {'ko': '`%s`' % l['saves'] if l.get('saves') else '—',
                                        'en': '`%s`' % l['saves'] if l.get('saves') else '—'}]
                                      for l in lessons]}, ctx))

    glo = ['<h2 class="first"><span class="num">01</span><span class="k">국문 · 영문 용어 대조</span>'
           '<span class="e">Korean / English terms</span></h2>',
           '<p class="lede"><span class="k">차시 열은 그 말이 처음 나오는 자리예요. 막히면 그 차시로 돌아가면 됩니다.</span>'
           '<span class="e">The lesson column is where the term first appears. Go back there if it does not click.</span></p>']
    if C.get('glossary'):
        glo.append(render_block({'type': 'table',
                                 'head': [{'ko': '국문', 'en': 'Korean'}, {'ko': '영문', 'en': 'English'},
                                          {'ko': '뜻', 'en': 'Meaning'}, {'ko': '차시', 'en': 'Lesson'}],
                                 'rows': [[{'ko': g['ko'], 'en': g['ko']}, {'ko': g['en'], 'en': g['en']},
                                           g.get('def', {'ko': '', 'en': ''}),
                                           {'ko': ', '.join(str(x) for x in g.get('lessons', [])),
                                            'en': ', '.join(str(x) for x in g.get('lessons', []))}]
                                          for g in C['glossary']]}, ctx))
    keys = ['<h2 class="first" id="keys"><span class="num">01</span><span class="k">과정에서 치는 명령 전부</span>'
            '<span class="e">Every command in the course</span></h2>',
            '<p class="lede"><span class="k">마지막 열은 「무엇을 하나」가 아니라 「언제 쓰나」입니다. 시험이 끝나도 남는 건 그쪽이거든요.</span>'
            '<span class="e">The last column says when you reach for it, not what it does. That is the part that survives the exam.</span></p>']
    if C.get('shortcutIndex'):
        keys.append(render_block({'type': 'table',
                                  'head': [{'ko': '명령', 'en': 'Command'}, {'ko': '이름', 'en': 'Name'},
                                           {'ko': '언제 쓰나', 'en': 'When you use it'}, {'ko': '차시', 'en': 'Lesson'}],
                                  'rows': [[{'ko': '`%s`' % s['key'], 'en': '`%s`' % s['key']},
                                            s.get('name'), s.get('when'),
                                            {'ko': ', '.join(str(x) for x in s.get('lessons', [])),
                                             'en': ', '.join(str(x) for x in s.get('lessons', []))}]
                                           for s in C['shortcutIndex']]}, ctx))

    dec = ['<h2 class="first"><span class="num">01</span><span class="k">아직 정해지지 않은 것</span>'
           '<span class="e">Not settled yet</span></h2>',
           '<p class="lede"><span class="k">지어내면 학습자가 그것을 믿고 준비합니다. 그래서 비워 두었어요. '
           '확정되면 이 자리에 채웁니다.</span>'
           '<span class="e">Inventing these would be worse than leaving them blank — a learner would prepare against them. '
           'They get filled in here once confirmed.</span></p>']
    if C.get('openQuestions'):
        dec.append(render_block({'type': 'table',
                                 'head': [{'ko': '항목', 'en': 'Item'}, {'ko': '정해지지 않으면 무엇이 막히나', 'en': 'What it blocks'}],
                                 'rows': [[q.get('item', q) if isinstance(q, dict) else {'ko': q, 'en': q},
                                           q.get('blocks', {'ko': '', 'en': ''}) if isinstance(q, dict) else {'ko': '', 'en': ''}]
                                          for q in C['openQuestions']]}, ctx))
    if C.get('settledNote'):
        dec.append('<h2 id="settled"><span class="num">02</span><span class="k">닫힌 것</span>'
                   '<span class="e">Closed</span></h2>')
        dec.append(render_block({'type': 'note', 'tone': 'why',
                                 'label': {'ko': '무엇이 어떤 근거로 정해졌나',
                                           'en': 'What was settled, and on what evidence'},
                                 'ko': C['settledNote'].get('ko', ''),
                                 'en': C['settledNote'].get('en', '')}, ctx))
    if C.get('sourceNote'):
        dec.append(render_block({'type': 'note', 'tone': 'tip',
                                 'label': {'ko': '이 교재의 출처', 'en': 'Where this came from'},
                                 'ko': C['sourceNote'].get('ko', ''), 'en': C['sourceNote'].get('en', '')}, ctx))

    cur.append(render_block({'type': 'note', 'tone': 'tip',
                             'label': {'ko': '용어와 명령은 따로 모아 두었습니다',
                                       'en': 'Glossary and command index live on their own page'},
                             'ko': '국영 용어 대조 %d개와 과정에서 치는 명령 %d개는 '
                                   '`reference.html` 한 장에 모았어요. 실습 중에 그 쪽만 따로 열어 두시면 편합니다.'
                                   % (len(C.get('glossary', [])), len(C.get('shortcutIndex', []))),
                             'en': 'The %d bilingual terms and the %d commands used in the course are on '
                                   '`reference.html`. Keep that page open in a second tab while you work.'
                                   % (len(C.get('glossary', [])), len(C.get('shortcutIndex', [])))}, ctx))

    meta = ('<span class="k">작성 %s · AutoCAD 교육 과정 · 자습 총 %d분(약 %.1f시간) · </span>'
            '<span class="e">Written %s · AutoCAD course · %d min total (about %.1f h) · </span>'
            % (STAMP, total_min, total_min / 60.0, STAMP, total_min, total_min / 60.0))
    ctitle = (C.get('courseTitle') or {}).get('ko', '자습 교재')
    eyeb = ('<span class="k">LG이노텍 Green Star · for technician · 자습 과정</span>'
            '<span class="e">LG Innotek Green Star · for technician · self-study</span>')
    pager_ref = ('<nav class="pager" aria-label="이동 / Navigation"><span></span>'
                 '<span class="sp"></span><a href="reference.html">'
                 '<span class="k">용어 · 명령 색인 &#8594;</span>'
                 '<span class="e">Glossary &amp; command index &#8594;</span></a></nav>')
    index_html = shell(ctitle, eyeb, bi(C.get('courseTitle')), meta,
                       [('p-ov', {'ko': '요약', 'en': 'Overview'}),
                        ('p-cur', {'ko': '커리큘럼', 'en': 'Curriculum'}),
                        ('p-dec', {'ko': '미결', 'en': 'Open'})],
                       [('p-ov', ''.join(ov)), ('p-cur', ''.join(cur)), ('p-dec', ''.join(dec))],
                       pager_ref, grade='M')

    ref_pager = ('<nav class="pager" aria-label="이동 / Navigation">'
                 '<a href="index.html"><span class="k">&#8592; 과정 전체</span>'
                 '<span class="e">&#8592; All lessons</span></a><span class="sp"></span></nav>')
    ref_eyeb = ('<span class="k">LG이노텍 Green Star · for technician · 참고</span>'
                '<span class="e">LG Innotek Green Star · for technician · reference</span>')
    ref_html = shell('용어와 명령 — AutoCAD Technician 자습', ref_eyeb,
                     bi({'ko': '용어와 명령', 'en': 'Glossary and commands'}), meta,
                     [('p-glo', {'ko': '용어', 'en': 'Glossary'}),
                      ('p-key', {'ko': '명령', 'en': 'Commands'})],
                     [('p-glo', ''.join(glo)), ('p-key', ''.join(keys))],
                     ref_pager, grade='S')
    return index_html, ref_html


# ── main ───────────────────────────────────────────────────────
def _find(*candidates):
    """작업 중 배치(design/·content/)와 저장소 배치(source/)를 둘 다 받는다."""
    for rel in candidates:
        p = os.path.join(SCRATCH, *rel)
        if os.path.exists(p):
            return p
    return None


def main(outdir):
    cur = _find(('design', 'curriculum.json'), ('curriculum.json',))
    if not cur:
        raise SystemExit('curriculum.json 을 찾지 못했다: %s' % SCRATCH)
    C = json.load(io.open(cur, encoding='utf-8'))
    lessons = []
    for n in range(1, 9):
        p = _find(('content', 'lesson-%02d.json' % n), ('lesson-%02d.json' % n,))
        if p:
            lessons.append(json.load(io.open(p, encoding='utf-8')))
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    written, progress_file, part2 = [], {}, {}
    nos = [l['no'] for l in lessons]
    for l in lessons:
        i = nos.index(l['no'])
        nav = (nos[i - 1] if i > 0 else None, nos[i + 1] if i + 1 < len(nos) else None)
        KLAB = {'concept': ('개념', 'Concepts'), 'practice': ('실습', 'Practice'),
                'check': ('점검', 'Check')}
        for page in build_lesson(l, nav):
            p = os.path.join(outdir, page['name'])
            io.open(p, 'w', encoding='utf-8', newline='\n').write(page['html'])
            written.append(p)
            progress_file[l['no']] = 'lesson-%02d' % l['no']
            if page['part'] > 1:
                part2.setdefault(l['no'], []).append({
                    'name': page['name'], 'part': page['part'],
                    'ko': ' · '.join(KLAB[k][0] for k in page['kinds']),
                    'en': ' · '.join(KLAB[k][1] for k in page['kinds'])})
    index_html, ref_html = build_index(C, lessons, progress_file, part2)
    for name, doc in (('index.html', index_html), ('reference.html', ref_html)):
        p = os.path.join(outdir, name)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(doc)
        written.append(p)
    for w in written:
        size = os.path.getsize(w)
        print('%8d B  %-22s %s' % (size, os.path.basename(w), '' if size <= PAGE_CAP else '<< 초과'))
    if part2:
        print('\n두 쪽으로 나눈 차시: ' + ', '.join('%d' % k for k in sorted(part2)))
    over = [w for w in written if os.path.getsize(w) > PAGE_CAP]
    if over:
        print('\n!! 100KB 초과: ' + ', '.join(os.path.basename(o) for o in over))
        return 1
    return 0


if __name__ == '__main__':
    default_out = os.path.join(
        os.path.abspath(os.path.join(HERE, os.pardir, os.pardir)),
        'docs', 'autocad-technician', 'self-study')
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_out))
