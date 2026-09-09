# -*- coding: utf-8 -*-
"""여덟 차시를 한 파일로 엮는다.

차시마다 주소가 다르면 사람에게 건넬 때 링크를 여덟 개 보내야 한다. 하나로
엮고 아래 막대에 차시 고르는 칸을 둔다.

시계는 손대지 않는다. 재생기는 조각 시각에서 그 장면의 `data-start` 를 빼서
프레임 안 시각을 얻으므로, 파일마다 0부터 시작하는 시계를 그대로 이어 붙여도
빼는 값이 같이 따라온다.

내려받아 여는 판은 `--standalone` 으로 만든다. 바깥에서 가져오는 것이 하나도
없어야 인터넷 없이도 열리므로 GSAP 을 파일 안에 넣고, 검수 메모까지 붙인다.

    python scripts/selfstudy/build_deck_all.py <출력 파일> [작업폴더] [--standalone <gsap.min.js>]
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_deck_selfstudy as B

ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
LESSONS = [
 (1, 'lesson-01-orientation', '오리엔테이션'),
 (2, 'lesson-02-part-and-template', '부품 이해와 도면 환경'),
 (3, 'lesson-03-baseline-profile', '기준선과 외곽'),
 (4, 'lesson-04-circles-arcs', '원 · 호 · 오프셋'),
 (5, 'lesson-05-three-views', '제3각법 3뷰와 반복'),
 (6, 'lesson-06-editing-symbols', '편집과 표현'),
 (7, 'lesson-07-dimensioning-release', '치수와 출도'),
 (8, 'lesson-08-exam-and-qa', '시험 안내와 Q&A'),
]

ISLAND = re.compile(
    r'<script type="application/hyperframes-slideshow\+json">(.*?)</script>', re.S)


def parts(path):
    """한 차시 파일에서 섬·본문·타임라인을 꺼낸다."""
    doc = io.open(path, encoding='utf-8').read()
    m = ISLAND.search(doc)
    island = json.loads(m.group(1))
    body = doc[m.end():doc.rindex('</body>')]
    # 재생기와 그 스타일은 마지막에 한 번만 붙인다.
    cut = body.find('<style>\nhtml,body{height:100%')
    if cut < 0:
        raise SystemExit('%s 에서 재생기 시작점을 못 찾았다' % path)
    return island, body[:cut]


def main(outpath, tmpdir, gsap=None):
    if not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)
    slides, bodies, lessons = [], [], []
    for no, slug, title in LESSONS:
        src = os.path.join(ROOT, 'projects', 'autocad-technician', slug)
        js = os.path.join(HERE, 'source', 'lesson-%02d.json' % no)
        one = os.path.join(tmpdir, 'deck-l%02d.html' % no)
        B.main(src, js, one)
        island, body = parts(one)
        lessons.append({'no': no, 'title': title, 'at': len(slides) + 1,
                        'count': len(island['slides'])})
        slides += island['slides']
        bodies.append('<!-- ===== %d차시 %s ===== -->\n%s' % (no, title, body))

    manifest = json.dumps({'slides': slides, 'slideSequences': [],
                           'lessons': lessons}, ensure_ascii=False, indent=1)
    nav = io.open(os.path.join(HERE, 'assets', 'deck_nav.html'), encoding='utf-8').read()
    memo = io.open(os.path.join(HERE, 'assets', 'deck_memo.html'), encoding='utf-8').read()
    if gsap:
        # 내려받은 파일은 인터넷 없이도 열려야 한다. 애니메이션 엔진이 없으면
        # 프레임의 스크립트가 첫 줄에서 멎고 화면이 통째로 빈다.
        lib = ('<script>%s</script>'
               % io.open(gsap, encoding='utf-8').read().replace('</script>', '<\\/script>'))
        banner = ('<div id="dl">이 파일은 <b>내려받아 브라우저로 열면</b> 메모가 저장됩니다. '
                  '인터넷 없이도 열려요. <button type="button" id="dlx">닫기</button></div>'
                  '<style>#dl{position:fixed;top:0;left:0;right:0;z-index:50;padding:9px 16px;'
                  'background:#F7E9EC;color:#5c0021;border-bottom:1px solid #C7004C;'
                  'font:14px/1.5 "LG EI Text TTF Regular","Malgun Gothic",system-ui,sans-serif}'
                  '#dl button{font:inherit;margin-left:10px;padding:3px 9px;border:1px solid #C7004C;'
                  'border-radius:4px;background:#fff;color:#C7004C;cursor:pointer}'
                  '@media print{#dl{display:none}}</style>'
                  # 띠가 메모 패널 머리를 덮는다. 띠 높이만큼 패널을 내리고,
                  # 띠를 닫으면 되돌린다.
                  '<script>(function(){var d=document.getElementById("dl"),'
                  'm=document.getElementById("mm");'
                  'function fit(){var h=(d?d.offsetHeight:0);if(m)m.style.top=h+"px";'
                  'document.documentElement.style.setProperty("--dltop",h+"px");'
                  'if(window.__deckLayout)window.__deckLayout();}fit();'
                  'window.addEventListener("resize",fit);'
                  'document.getElementById("dlx").onclick=function(){'
                  'd.remove();if(m)m.style.top="0px";'
                  'document.documentElement.style.setProperty("--dltop","0px");'
                  'if(window.__deckLayout)window.__deckLayout();};})();</script>')
    else:
        lib = ('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js">'
               '</script>')
        banner = ''
    doc = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>AutoCAD Technician 자습 슬라이드 · 여덟 차시</title>
%s
<style>
  *{box-sizing:border-box}
  html,body{margin:0;background:#0B0A0A}
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
%s
</body>
</html>
""" % (lib, B.STYLE, manifest, '\n'.join(bodies), nav, memo, banner)
    io.open(outpath, 'w', encoding='utf-8', newline='\n').write(doc)
    print('\n엮음 %d차시 · 슬라이드 %d장 · %.1f MB'
          % (len(lessons), len(slides), os.path.getsize(outpath) / 1048576.0))
    for l in lessons:
        print('  %d차시 %-18s %3d장 (%d~%d)'
              % (l['no'], l['title'], l['count'], l['at'], l['at'] + l['count'] - 1))
    return 0


if __name__ == '__main__':
    av = sys.argv[1:]
    gsap = None
    if '--standalone' in av:
        k = av.index('--standalone')
        gsap = av[k + 1]
        del av[k:k + 2]
    out = av[0] if av else os.path.join(ROOT, 'deck-all.html')
    tmp = av[1] if len(av) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(out)), '_decks')
    sys.exit(main(out, tmp, gsap))
