"""Scaffold a lesson's HyperFrames compositions. RUN ONCE PER LESSON.

This writes a first draft of the frame HTML with the part outline injected from
edu_ib_02.py, so the drawing starts out agreeing with master-part-geometry.json.

After that the frames are ordinary authored compositions: preview them with
`npm run dev` and edit them in HyperFrames Studio, which is the framework's
own authoring loop. Studio stamps data-hf-id attributes and writes edits back
into these files, and re-running this scaffold would discard both.

    python scripts/part/scaffold_lesson_frames.py projects/autocad-technician/lesson-01-part-and-template

If the part geometry itself changes, regenerate the SVG separately and paste it
into the affected frame rather than re-scaffolding the whole lesson.
"""

import os
import subprocess
import sys
import tempfile

LESSON = sys.argv[1] if len(sys.argv) > 1 else "projects/autocad-technician/lesson-01-part-and-template"
FRAMES = os.path.join(LESSON, "compositions", "frames")
HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = (
    '<style>@font-face{font-family:"LG EI Text TTF Regular";src:local("LG EI Text TTF Regular");font-weight:400}'
    '@font-face{font-family:"LG EI Headline TTF Semibold";src:local("LG EI Headline TTF Semibold");font-weight:600}'
    '@font-face{font-family:"Malgun Gothic";src:local("Malgun Gothic");font-weight:400}</style>'
)

BASE_CSS = """
#root{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;color:#111;
 font-family:"LG EI Text TTF Regular","Malgun Gothic",sans-serif}
*{box-sizing:border-box}
.clip{position:absolute;inset:0;width:100%;height:100%;padding:72px 96px 64px;background:#FFF}
.topline{display:flex;justify-content:space-between;align-items:end;padding-bottom:18px;border-bottom:2px solid #A4A3A4}
.index{color:#C7004C;font-size:24px;font-weight:600;letter-spacing:.08em}
h1{margin:0;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;font-size:64px;letter-spacing:-.035em}
.prompt{color:#666;font-size:28px}
.body{display:grid;gap:44px;height:724px;padding-top:40px}
.panel{background:#F5F5F3;border:2px solid #A4A3A4;display:grid;place-items:center;overflow:hidden}
.panel svg{width:100%;height:100%}
.dwg .outline{fill:none;stroke:#111;stroke-width:.5;stroke-linejoin:round;stroke-linecap:round}
.dwg .hidden{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:2.4 1.2}
.dwg .center{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:6 1.2 1 1.2}
.dwg .dim,.dwg .ext,.dwg .tangent{fill:none;stroke:#111;stroke-width:.25}
.dwg .arrow{fill:#111;stroke:none}
.dwg [data-feature].hot{stroke:#C7004C}
.dwg [data-feature].hot.arrow{fill:#C7004C}
.card{border:2px solid #A4A3A4;background:#FFF;padding:20px 24px}
.card b{display:block;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;color:#C7004C;font-size:30px}
.card strong{display:block;margin:6px 0 4px;color:#111;font-size:26px}
.card span{color:#666;font-size:22px;line-height:1.4}
.chain{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:20px;color:#6F6D70;letter-spacing:.04em}
.chain i{font-style:normal;padding:6px 14px;border:2px solid #DCDBD7}
.chain i.done{color:#111;border-color:#111}
.chain i.now{color:#C7004C;border-color:#C7004C;font-weight:600}
.note{margin-top:16px;padding-top:16px;border-top:4px solid #111;font-size:26px;line-height:1.45}
.note b{color:#C7004C}
"""

HEAD = ('<!DOCTYPE html>\n<html lang="ko"><head><meta charset="UTF-8"></head><body><template>'
        + FONTS + "\n  <style>" + BASE_CSS + "  </style>\n")
TAIL = "</template></body></html>\n"


def part_svg(profile="front"):
    tmp = os.path.join(tempfile.mkdtemp(), "part.svg")
    subprocess.run([sys.executable, os.path.join(HERE, "edu_ib_02.py"), tmp, "--profile", profile],
                   check=True, capture_output=True)
    with open(tmp, encoding="utf-8") as fh:
        svg = fh.read()
    return svg.replace('<rect x=', '<rect data-bg="1" x=', 1)


def write(name, comp_id, duration, body, timeline):
    html = (HEAD
            + f'  <div id="{comp_id}-root" data-composition-id="{comp_id}" data-start="0" data-duration="{duration}"'
              f' data-width="1920" data-height="1080">\n'
            + f'    <section id="{comp_id}" class="clip" data-start="0" data-duration="{duration}"'
              f' data-track-index="1">\n{body}\n    </section>\n  </div>\n'
            + '  <script>\n    window.__timelines=window.__timelines||{};\n'
              '    const tl=gsap.timeline({paused:true});\n'
            + timeline
            + f'\n    window.__timelines["{comp_id}"]=tl;\n  </script>\n'
            + TAIL)
    with open(os.path.join(FRAMES, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return name


def header(index, title, prompt):
    return (f'      <header class="topline"><div><div class="index">{index}</div>'
            f'<h1>{title}</h1></div><div class="prompt">{prompt}</div></header>')


CHAIN = ['REFERENCE_READONLY', 'L01_TEMPLATE', 'L02_PROFILE', 'L03_FEATURES',
         'L04_VIEWS', 'L05_REPRESENTED', 'L06_RELEASE']


def chain_html(done_upto, now):
    out = []
    for i, c in enumerate(CHAIN):
        cls = "done" if i <= done_upto else ("now" if c == now else "")
        out.append(f'<i class="{cls}">{c}</i>')
    return '<div class="chain">' + "".join(out) + "</div>"


os.makedirs(FRAMES, exist_ok=True)
svg_front = part_svg("front")
S = "#" + "{}"

# ---------------------------------------------------------------- frame 1
body = (header("01 · PART", "부품 하나를 여섯 차시에 걸쳐 만듭니다", "EDU-IB-02 · 아이들러 풀리 브래킷")
        + '\n      <main class="body" style="grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr)">'
        + '<section class="left">'
        + '<div class="card"><b>무엇인가</b><strong>아이들러 풀리 브래킷</strong>'
        + '<span>벨트를 옆에서 눌러 장력을 잡는 바퀴의 축을 잡고, 프레임 수직면에 볼트 두 개로 붙는다.</span></div>'
        + '<div class="card" style="margin-top:20px"><b>오늘</b><strong>선은 긋지 않습니다</strong>'
        + '<span>형상의 이유를 읽고, 그림을 그릴 종이와 레이어 규칙을 준비한다.</span></div>'
        + f'<div style="margin-top:28px">{chain_html(0, "L01_TEMPLATE")}</div>'
        + '</section>'
        + f'<section class="panel">{svg_front}</section></main>')
tl = ('    const s="#l1f1";\n'
      '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);\n'
      '    tl.fromTo(`${s} .panel`,{opacity:0,x:80},{opacity:1,x:0,duration:.7,ease:"power4.out"},.8);\n'
      '    const ps=document.querySelectorAll("#l1f1 .panel .outline");\n'
      '    ps.forEach(p=>{const l=p.getTotalLength();p.style.strokeDasharray=`${l}`;p.style.strokeDashoffset=`${l}`});\n'
      '    tl.to(ps,{strokeDashoffset:0,duration:1.2,ease:"power2.out"},1.2);\n'
      '    tl.fromTo(`${s} .card`,{opacity:0,y:28},{opacity:1,y:0,duration:.5,stagger:.5,ease:"power3.out"},2.6);\n'
      '    tl.fromTo(`${s} .chain i`,{opacity:0},{opacity:1,duration:.28,stagger:.1},4.2);')
write("01-what-is-this-part.html", "l1f1", 50, body.replace('id="l1f1"', 'id="l1f1"'), tl)

# ---------------------------------------------------------------- frame 2
feat = [("base", "베이스 120", "넓게 벌린 두 볼트가 축이 만드는 비트는 힘을 버틴다"),
        ("slot", "장공 · 중심거리 12", "벨트를 끼운 뒤 장력을 보며 좌우로 미세 조정한다"),
        ("profile", "목 · 밑동 80", "힘이 가장 큰 밑동이 가장 두껍고 위로 좁아진다"),
        ("fillet", "필렛 R10", "각지면 그 모서리에 힘이 몰려 거기부터 금이 간다"),
        ("boss", "보스 Ø56", "축 구멍 둘레의 살 두께를 필요한 곳만 키운다")]
cards = "".join(f'<div class="card f-{k}"><b>{t}</b><span>{d}</span></div>' for k, t, d in feat)
body = (header("02 · WHY", "형상마다 이유가 있습니다", "기능이 형상을 결정한다")
        + '\n      <main class="body" style="grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)">'
        + f'<section class="panel">{svg_front}</section>'
        + f'<section style="display:grid;gap:14px;align-content:center">{cards}</section></main>')
steps = []
for i, (k, _, _) in enumerate(feat):
    at = 4 + i * 10
    steps.append(f'    tl.add(()=>{{document.querySelectorAll("#l1f2 .dwg [data-feature]")'
                 f'.forEach(e=>e.classList.remove("hot"));'
                 f'document.querySelectorAll("#l1f2 [data-feature=\\"{k}\\"]")'
                 f'.forEach(e=>e.classList.add("hot"))}},{at});')
    steps.append(f'    tl.to("#l1f2 .card",{{borderColor:"#A4A3A4",backgroundColor:"#FFF",'
                 f'duration:.3,ease:"power1.inOut"}},{at});')
    steps.append(f'    tl.to("#l1f2 .f-{k}",{{borderColor:"#C7004C",backgroundColor:"#F5F5F3",'
                 f'duration:.4,ease:"power1.inOut"}},{at});')
tl = ('    const s="#l1f2";\n'
      '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);\n'
      '    tl.fromTo(`${s} .panel`,{opacity:0,x:-70},{opacity:1,x:0,duration:.66,ease:"power4.out"},.8);\n'
      '    tl.fromTo(`${s} .card`,{opacity:0,x:60},{opacity:1,x:0,duration:.5,stagger:.14,ease:"power3.out"},1.2);\n'
      + "\n".join(steps))
write("02-why-this-shape.html", "l1f2", 60, body, tl)

# ---------------------------------------------------------------- frame 3
concepts = [("표면 거칠기", "면을 얼마나 곱게 다듬을지", "축이 닿는 안쪽은 곱게, 볼트로 눌리는 바닥은 거칠어도 된다"),
            ("기하 공차", "치수로는 못 막는 자세와 위치", "구멍이 판에 비스듬히 뚫리면 축이 기울고 벨트가 쏠린다"),
            ("재질", "어떤 강재로 만드는지", "큰 힘을 받지 않고 깎기 쉬워야 하니 일반 구조용이면 충분하다"),
            ("열처리", "가열·냉각으로 굳기를 바꾸는 공정", "이 브래킷에는 하지 않는다. 도는 축은 겉만 단단하게 한다")]
cc = "".join(f'<div class="card c{i}"><b>{t}</b><strong>{s}</strong><span>{d}</span></div>'
             for i, (t, s, d) in enumerate(concepts))
body = (header("03 · READ", "숫자 하나가 공정을 결정합니다", "Ø25 H7 · 드릴로는 못 낸다")
        + '\n      <main class="body" style="grid-template-rows:auto 1fr">'
        + '<section style="display:flex;align-items:center;gap:28px;font-size:34px">'
        + '<span class="fitcode" style="font-size:56px;color:#C7004C;'
          'font-family:\'LG EI Headline TTF Semibold\',\'Malgun Gothic\',sans-serif">Ø25 H7</span>'
        + '<span class="arrowline" style="flex:0 0 120px;height:2px;background:#111"></span>'
        + '<span class="proc">드릴 Ø24 → 리머 Ø25 H7</span></section>'
        + '<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;align-content:start">'
        + cc + '</section>'
        + '<div class="note"><b>개념만</b> 아래 네 가지는 뜻과 이유만 알고 넘어갑니다. 이 과정의 작도 대상이 아닙니다.</div>'
        + '</main>')
tl = ('    const s="#l1f3";\n'
      '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);\n'
      '    tl.fromTo(`${s} .fitcode`,{opacity:0,scale:.9},{opacity:1,scale:1,duration:.5,ease:"power3.out"},1);\n'
      '    tl.fromTo(`${s} .arrowline`,{scaleX:0,transformOrigin:"left center"},'
      '{scaleX:1,duration:.4,ease:"power2.out"},1.6);\n'
      '    tl.fromTo(`${s} .proc`,{opacity:0,x:-20},{opacity:1,x:0,duration:.4,ease:"power2.out"},1.9);\n'
      '    tl.fromTo(`${s} .card`,{opacity:0,y:30},{opacity:1,y:0,duration:.46,stagger:.18,ease:"power3.out"},20);\n'
      '    tl.fromTo(`${s} .note`,{opacity:0},{opacity:1,duration:.5},44);')
write("03-reading-the-drawing.html", "l1f3", 55, body, tl)

# ---------------------------------------------------------------- frame 4
layers = [("OUTLINE", "흰색 7", "Continuous", "0.50"), ("CENTER", "빨강 1", "CENTER2", "0.25"),
          ("HIDDEN", "초록 3", "HIDDEN2", "0.25"), ("DIM", "노랑 2", "Continuous", "0.25"),
          ("BORDER", "흰색 7", "Continuous", "0.50"), ("TITLE", "흰색 7", "Continuous", "0.25"),
          ("HATCH", "회색 8", "Continuous", "0.18"), ("CONSTRUCTION", "9", "Continuous", "0.18")]
rows = "".join(f'<tr class="lr"><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in layers)
sheet = ('<svg viewBox="0 0 460 330" style="width:100%;height:auto;max-height:100%">'
         '<rect class="sh-out" x="10" y="10" width="420" height="297" fill="none" stroke="#111" stroke-width="2"/>'
         '<rect class="sh-brd" x="20" y="20" width="400" height="277" fill="none" stroke="#C7004C" stroke-width="2"/>'
         '<rect class="sh-ttl" x="220" y="267" width="200" height="30" fill="none" stroke="#C7004C" stroke-width="2"/>'
         '<line class="sh-ttl" x1="320" y1="267" x2="320" y2="297" stroke="#C7004C" stroke-width="2"/>'
         '<text x="240" y="287" font-size="14" fill="#666">사번</text>'
         '<text x="340" y="287" font-size="14" fill="#666">이름</text>'
         '<text x="220" y="322" font-size="15" fill="#111" text-anchor="middle">A3  420 × 297</text></svg>')
body = (header("04 · SHEET", "종이와 규칙을 먼저 정합니다", "A3 가로 · 사방 10 · 표제란 200×30")
        + '\n      <main class="body" style="grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)">'
        + f'<section class="panel" style="padding:56px">{sheet}</section>'
        + '<section><table style="width:100%;border-collapse:collapse;font-size:23px">'
        + '<thead><tr style="color:#666;font-size:19px;letter-spacing:.08em">'
          '<th style="text-align:left;padding:8px 10px">LAYER</th><th style="text-align:left;padding:8px 10px">색</th>'
          '<th style="text-align:left;padding:8px 10px">선종류</th><th style="text-align:left;padding:8px 10px">굵기</th>'
          '</tr></thead><tbody>' + rows + '</tbody></table>'
        + '<div class="note"><b>우선순위</b> 시험 문제지가 다른 이름·색·굵기를 지정하면 그 지시가 우선합니다.</div>'
        + '</section></main>')
tl = ('    const s="#l1f4";\n'
      '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);\n'
      '    tl.fromTo(`${s} .sh-out`,{opacity:0},{opacity:1,duration:.4},1);\n'
      '    tl.fromTo(`${s} .sh-brd`,{opacity:0},{opacity:1,duration:.4},1.8);\n'
      '    tl.fromTo(`${s} .sh-ttl`,{opacity:0},{opacity:1,duration:.4},2.6);\n'
      '    tl.fromTo(`${s} .lr`,{opacity:0,x:40},{opacity:1,x:0,duration:.34,stagger:.16,ease:"power2.out"},22);\n'
      '    tl.fromTo(`${s} .note`,{opacity:0},{opacity:1,duration:.5},46);')
write("04-sheet-and-layers.html", "l1f4", 55, body, tl)

# ---------------------------------------------------------------- frame 5
steps5 = ["acadiso.dwt 선택", "SAVEAS · 파일명", "UNITS 확인", "LIMITS 420×297",
          "LAYER 8개 생성", "BORDER 도면틀", "TITLE 표제란", "객체 스냅 · 직교"]
chk = "".join(f'<li class="st">{t}</li>' for t in steps5)
body = (header("05 · DEMO-01", "템플릿 만들기", "USER RECORDING · acadiso.dwt → L01_TEMPLATE")
        + '\n      <main class="body" style="grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr)">'
        + '<section class="panel rec" style="border-style:dashed">'
          '<div style="text-align:center;color:#666"><div style="font-size:30px;letter-spacing:.12em;'
          'color:#C7004C">USER RECORDING</div><div style="font-size:24px;margin-top:12px">DEMO-01 · 화면 녹화 삽입</div></div>'
          '</section>'
        + '<section><ol style="list-style:none;margin:0;padding:0;font-size:25px;line-height:1.5">'
        + chk + '</ol>'
        + '<div class="note"><b>감점 위험</b> 시험이 템플릿을 제공하면 제공 파일을 우선하고 교육용 기본값으로 덮어쓰지 않습니다.</div>'
        + '</section></main>')
lines5 = ['    const s="#l1f5";',
          '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);',
          '    tl.fromTo(`${s} .rec`,{opacity:0},{opacity:1,duration:.5},.8);',
          '    tl.set(`${s} .st`,{opacity:.32},0);']
for i in range(len(steps5)):
    lines5.append(f'    tl.to("#l1f5 .st:nth-child({i + 1})",{{opacity:1,color:"#111",'
                  f'duration:.35,ease:"power1.inOut"}},{14 + i * 44});')
lines5.append('    tl.fromTo(`${s} .note`,{opacity:0},{opacity:1,duration:.5},366);')
write("05-build-template.html", "l1f5", 380, body, "\n".join(lines5))

# ---------------------------------------------------------------- frame 6
body = (header("06 · RECAP", "문서가 아니라 파일이 남았습니다", "L01_TEMPLATE 완료")
        + '\n      <main class="body" style="grid-template-rows:auto auto 1fr;align-content:start">'
        + f'<div style="margin-top:12px">{chain_html(1, "L02_PROFILE")}</div>'
        + '<section style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:34px">'
        + '<div class="card"><b>남은 것</b><strong>템플릿 파일</strong><span>A3 도면틀 · 표제란 · 레이어 8개 · 스냅 설정</span></div>'
        + '<div class="card"><b>다음</b><strong>L02_PROFILE</strong><span>좌표를 입력해 베이스와 목의 외곽을 그린다</span></div>'
        + '<div class="card"><b>미리</b><strong>접점 스냅</strong><span>목은 보스 원에 접하게 그린다. 오늘 켜 둔 TAN을 쓴다</span></div>'
        + '</section></main>')
tl = ('    const s="#l1f6";\n'
      '    tl.fromTo(`${s} .topline`,{opacity:0,y:-24},{opacity:1,y:0,duration:.58,ease:"power3.out"},.2);\n'
      '    tl.fromTo(`${s} .chain i`,{opacity:0},{opacity:1,duration:.24,stagger:.09},.8);\n'
      '    tl.fromTo(`${s} .card`,{opacity:0,y:30},{opacity:1,y:0,duration:.46,stagger:.22,ease:"power3.out"},2.2);')
write("06-recap.html", "l1f6", 30, body, tl)

print("frames written to", FRAMES)
for f in sorted(os.listdir(FRAMES)):
    print("  ", f, os.path.getsize(os.path.join(FRAMES, f)), "bytes")
