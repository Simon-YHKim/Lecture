# -*- coding: utf-8 -*-
"""공유용 한 장짜리 판.

여덟 차시가 22쪽에 나뉘어 있으면 링크를 스물두 개 보내야 한다. 사람에게 건네려면
주소 하나여야 한다. 그래서 같은 내용을 파일 하나로 다시 엮는다.

쪽으로 나눈 판과 다른 점은 셋뿐이다.
  · 차시 사이 이동이 링크가 아니라 탭이다
  · 진도 막대가 차시마다가 아니라 과정 전체로 하나다
  · 용어·명령·미결이 같은 파일 안에 들어온다

본문·도해·검사 결과는 쪽 판과 같은 원본에서 나오므로 둘이 어긋날 수 없다.

    python scripts/selfstudy/build_single.py [출력 파일]
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_selfstudy as B

PANEL_OPEN = re.compile(r'<section role="tabpanel" id="([^"]+)"[^>]*>')
PROGRESS = re.compile(r'<div class="noprint"><h3>.*?</div>\s*(?=<h2|<section|$)', re.S)
ID_ATTR = re.compile(r'(<(?:h2|h3|figure)\b[^>]*?)\sid="([^"]+)"')


def panels_of(html):
    """생성된 쪽에서 탭 패널 알맹이만 꺼낸다.

    패널 안에 `<section data-memo>` 이 중첩돼 있어 게으른 정규식으로는 첫 번째
    닫는 태그에서 끊긴다. 여는 태그 위치를 모아 다음 패널(또는 본문 끝)까지
    잘라 내고, 꼬리의 닫는 태그 하나만 떼는 방식으로 자른다.
    """
    starts = [(m.start(), m.end(), m.group(1)) for m in PANEL_OPEN.finditer(html)]
    if not starts:
        return {}
    # 마지막 패널 뒤에는 이동 링크가 붙는다. 한 장짜리 판에는 필요 없으니 잘라 낸다.
    tail = len(html)
    for marker in ('<nav class="pager"', '</main>'):
        if marker in html:
            tail = min(tail, html.index(marker))
    out = {}
    for i, (s, e, pid) in enumerate(starts):
        stop = starts[i + 1][0] if i + 1 < len(starts) else tail
        body = html[e:stop].rstrip()
        # 패널을 닫는 마지막 </section> 하나만 떼어 낸다
        if body.endswith('</section>'):
            body = body[:-len('</section>')]
        out[pid] = body
    return out


def strip_progress(html):
    return PROGRESS.sub('', html)


def prefix_ids(html, prefix):
    """차시를 한 문서에 모으면 절 id 가 겹칠 수 있다. 차시 번호를 앞에 붙인다."""
    return ID_ATTR.sub(lambda m: '%s id="%s-%s"' % (m.group(1), prefix, m.group(2)), html)


def consolidate_surfaces(html):
    """Shared SVG symbols must be defined once, outside any hideable tab."""
    html = re.sub(r'<svg\b[^>]*class="sfcdefs"[^>]*>.*?</svg>', '', html, flags=re.S)
    used = set(re.findall(r'href="#sfc-([\w-]+)"', html))
    return re.sub(r'(<body\b[^>]*>)', lambda m: m[1] + B.surface_defs(used), html, count=1)


ARTIFACT_TITLE = 'AutoCAD 브래킷 자습 과정'
ARTIFACT_BANNER = (
    '<div class="banner"><span class="k">메모와 진도는 이 페이지를 여는 브라우저에만 저장됩니다. '
    '기기를 바꾸면 따라오지 않아요.</span>'
    '<span class="e">Notes and progress are stored in the browser you open this page in. '
    'They do not follow you to another device.</span></div>')


def to_artifact(html):
    """아티팩트는 문서 껍데기를 직접 씌운다. 알맹이만 넘기고 body 속성은 스크립트로 심는다."""
    style = re.search(r'<style>.*?</style>', html, re.S).group(0)
    body_open = re.search(r'<body([^>]*)>', html)
    attrs = dict(re.findall(r'data-([a-z-]+)="([^"]*)"', body_open.group(1)))
    inner = html[body_open.end():html.rindex('</body>')]
    inner = re.sub(r'<div class="banner">.*?</div>', ARTIFACT_BANNER, inner, count=1, flags=re.S)
    stamp = ';'.join("document.body.setAttribute('data-%s','%s')" % (k, v)
                     for k, v in attrs.items())
    return ('<title>%s</title>\n%s\n<script>%s</script>\n%s'
            % (ARTIFACT_TITLE, style, stamp, inner))


def main(outpath):
    src = B.SCRATCH
    cur = B._find(('design', 'curriculum.json'), ('curriculum.json',))
    C = json.load(io.open(cur, encoding='utf-8'))
    lessons = []
    for n in range(1, 9):
        p = B._find(('content', 'lesson-%02d.json' % n), ('lesson-%02d.json' % n,))
        if p:
            lessons.append(json.load(io.open(p, encoding='utf-8')))

    total_steps = sum(B.boxes_count(L) for L in lessons)
    total_min = sum(l.get('selfStudyMin', 0) for l in lessons)

    # 쪽 판을 한 차시 한 쪽으로 뽑아 알맹이만 가져온다
    saved_cap, B.PAGE_CAP = B.PAGE_CAP, 10 ** 9
    try:
        tabs, panels = [], []
        first = ('<h2 class="first"><span class="num">00</span><span class="k">시작하기</span>'
                 '<span class="e">Start here</span></h2>')
        idx_html, ref_html = B.build_index(C, lessons, {}, {})
        ip, rp = panels_of(idx_html), panels_of(ref_html)

        start = [first]
        start.append(re.sub(r'^<h2[^>]*>.*?</h2>', '', ip.get('p-ov', ''), count=1, flags=re.S))
        if total_steps:
            start.append(
                '<h2 id="progress"><span class="num">01</span><span class="k">진도</span>'
                '<span class="e">Progress</span></h2>'
                '<p class="lede"><span class="k">여덟 차시의 따라 하기 단계를 모두 합쳐 %d개입니다. '
                '체크하면 여기에 쌓이고, 브라우저에만 저장돼요.</span>'
                '<span class="e">%d practice steps across the eight lessons. Ticking them fills this bar, '
                'and it is stored in your browser only.</span></p>'
                '<div class="noprint"><div class="bar-wrap"><div class="bar-fill" id="prog-fill"></div></div>'
                '<p class="meta"><span id="prog-txt">0 / 0</span> &nbsp;'
                '<button type="button" class="t" id="reset-prog">'
                '<span class="k">진도 초기화</span><span class="e">Reset progress</span></button></p></div>'
                % (total_steps, total_steps))
        start.append(re.sub(r'^<h2[^>]*>.*?</h2>', '', ip.get('p-cur', ''), count=1, flags=re.S))
        tabs.append(('p-start', {'ko': '시작', 'en': 'Start'}))
        panels.append(('p-start', ''.join(start)))

        for L in lessons:
            no = L['no']
            pages = B.build_lesson(L, (None, None))
            body = []
            for pg in pages:
                pp = panels_of(pg['html'])
                for pid in ('p-sum', 'p-con', 'p-pra', 'p-chk'):
                    if pid in pp:
                        body.append(strip_progress(pp[pid]) if pid == 'p-sum' else pp[pid])
            html = prefix_ids(''.join(body), 'l%02d' % no)
            head = ('<h2 class="first"><span class="num">%02d</span>%s</h2>'
                    '<p class="lede"><span class="k">영상 %s · 자습 약 %d분</span>'
                    '<span class="e">Video %s · about %d min of self-study</span></p>'
                    % (no, B.bi(L.get('title')), L.get('videoLength', '—'),
                       L.get('selfStudyMin', 0), L.get('videoLength', '—'), L.get('selfStudyMin', 0)))
            tabs.append(('p-l%02d' % no, {'ko': '%d차시' % no, 'en': 'L%d' % no}))
            panels.append(('p-l%02d' % no, head + html))

        for pid, lab, src_panels, key in (
                ('p-glo', {'ko': '용어', 'en': 'Glossary'}, rp, 'p-glo'),
                ('p-key', {'ko': '명령', 'en': 'Commands'}, rp, 'p-key'),
                ('p-dec', {'ko': '미결', 'en': 'Open'}, ip, 'p-dec')):
            if src_panels.get(key):
                tabs.append((pid, lab))
                panels.append((pid, src_panels[key]))
    finally:
        B.PAGE_CAP = saved_cap

    meta = ('<span class="k">작성 %s · 발행 Claude Code · 8차시 한 파일 · 자습 총 %d분(약 %.1f시간) · </span>'
            '<span class="e">Written %s · Claude Code · eight lessons in one file · '
            '%d min total (about %.1f h) · </span>'
            % (B.STAMP, total_min, total_min / 60.0, B.STAMP, total_min, total_min / 60.0))
    eyeb = ('<span class="k">LG이노텍 Green Star · for technician · 자습 과정 전체</span>'
            '<span class="e">LG Innotek Green Star · for technician · the whole self-study course</span>')
    body_attrs = ' data-progress-key="course-single" data-step-total="%d"' % total_steps

    html = B.shell((C.get('courseTitle') or {}).get('ko', '자습 교재'), eyeb,
                   B.bi(C.get('courseTitle')), meta, tabs, panels, '',
                   grade='M', body_attrs=body_attrs)
    html = consolidate_surfaces(html)

    if os.environ.get('SELFSTUDY_ARTIFACT') == '1':
        html = to_artifact(html)

    outdir = os.path.dirname(os.path.abspath(outpath))
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    io.open(outpath, 'w', encoding='utf-8', newline='\n').write(html)
    size = os.path.getsize(outpath)
    print('%9d B (%.2f MB)  %s' % (size, size / 1048576.0, os.path.basename(outpath)))
    print('탭 %d개 · 차시 %d · 따라 하기 단계 %d' % (len(tabs), len(lessons), total_steps))
    return 0


if __name__ == '__main__':
    default = os.path.join(os.path.abspath(os.path.join(HERE, os.pardir, os.pardir)),
                           'docs', 'autocad-technician', 'self-study',
                           'autocad-self-study-all-in-one.html')
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default))
