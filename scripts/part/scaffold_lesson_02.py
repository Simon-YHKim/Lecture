"""Scaffold lesson-02, the part and the drawing environment. RUN ONCE.

After this the frames are authored compositions edited in HyperFrames Studio;
re-running discards Studio's data-hf-id stamps and any edits.

Frame lengths and every cue come from SCRIPT.md. A paragraph opening with
"(N ...)" is beat N and drives the Nth entry of that frame's item list, the Nth
drawing highlight, and the Nth generated assertion together. Hand-typed stagger
numbers drift out of sync with the words the moment a paragraph is rewritten,
and nothing complains.

Sheet and layer values follow the instructor material, not invention: the sheet
frame sits 10 mm inside the paper edge on all four sides, the title block is
200 x 30 at the bottom right split into two 100 mm cells holding name then
employee number, character height is 10 mm, and only four layers are used.

    python scripts/part/scaffold_lesson_02.py projects/autocad-technician/lesson-02-part-and-template
"""

import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import lesson_kit as kit  # noqa: E402

LESSON = sys.argv[1] if len(sys.argv) > 1 else "projects/autocad-technician/lesson-02-part-and-template"
NAME = os.path.basename(os.path.normpath(LESSON))
FRAMES = os.path.join(LESSON, "compositions", "frames")
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(FRAMES, exist_ok=True)

SCRIPT = beats.parse_script(os.path.join(LESSON, "SCRIPT.md"))
STEPS = beats.parse_steps(os.path.join(LESSON, "SCRIPT.md"), 8)
built = []


def part_svg(profile):
    tmp = os.path.join(tempfile.mkdtemp(), "part.svg")
    subprocess.run([sys.executable, os.path.join(HERE, "edu_ib_02.py"), tmp, "--profile", profile],
                   check=True, capture_output=True)
    with open(tmp, encoding="utf-8") as fh:
        return fh.read()


SVG_FRONT = part_svg("front")
SVG_FULL = part_svg("full")


def put(name, text):
    with open(os.path.join(FRAMES, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


MEASURED = beats.load_measured(LESSON)
_at = [0.0]


def frame(stem, comp, line_no, items, build, fixed=None):
    spans, dur = beats.plan(SCRIPT[line_no], duration=fixed)
    # A recorded and aligned narration replaces the syllable estimate.
    if MEASURED.get(line_no):
        got = beats.measured_plan(SCRIPT[line_no], MEASURED[line_no],
                                  _at[0], _at[0] + dur)
        if got:
            spans = got
    _at[0] += dur
    html, asserts = build(comp, dur, spans)
    put(stem + ".html", html)
    with open(os.path.join(FRAMES, stem + ".motion.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"duration": dur, "assertions": asserts}, fh, ensure_ascii=False)
    built.append((stem, comp, dur))
    print(beats.report(stem, spans, dur))
    for w in beats.audit(items, spans, dur):
        print("      ! " + w)
    return spans, dur


# ---------------------------------------------------------------- 1 title
def build_title(comp, dur, spans):
    return (kit.title_card(comp, dur, "부품 이해와 도면 환경", "AutoCAD 기본 과정 · 2차시"),
            [{"kind": "appearsBy", "selector": "#%s .brand" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": round(dur * .33 + 3, 1)},
             {"kind": "before", "a": "#%s .brand" % comp, "b": "#%s h2" % comp},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .sub" % comp},
             {"kind": "staysInFrame", "selector": "#%s .title" % comp}])


frame("01-title", "l2f1", 1, [], build_title, fixed=12)

# ------------------------------------------------------- 2 what the part is
PART = [("idler", "아이들러 풀리 브래킷", "용도",
         "V-벨트 구동계에서 벨트를 옆에서 눌러 장력을 잡아 주는 바퀴, 아이들러 풀리의 축을 붙든다. "
         "기계 프레임의 수직면에 볼트 두 개로 고정한다."),
        ("slip", "실제 역할", "벨트가 미끄러지지 않게 한다",
         "벨트는 쓰다 보면 늘어난다. 늘어난 채로 두면 풀리 위에서 미끄러져 동력이 제대로 전달되지 않고, "
         "미끄러지는 동안 발열과 마모가 함께 일어난다."),
        ("conveyor", "적용 예시", "물류·생산 설비의 벨트 컨베이어",
         "모터에서 롤러로 동력을 넘기는 구간에 들어간다. 장공으로 브래킷을 옆으로 밀어 장력을 맞추고 "
         "그 자리에서 볼트를 조여 고정한다."),
        ("wedge", "그 효과", "동력 전달률과 부품 수명",
         "장력이 맞으면 미끄러짐이 없어 동력이 그대로 전달되고, 벨트와 풀리가 덜 닳아 교체 주기가 길어진다. "
         "반대로 너무 조이면 베어링에 무리가 간다.")]


def build_part(comp, dur, spans):
    # Marks go beside the text here, not above it: four stacked cards have the
    # height for a column but not for another row each. The drawing on the right
    # is of the part, not of what these cards claim about it, so the cards still
    # need their own graphic.
    cards = "".join('<div class="card wide c%d" style="padding:16px 20px">%s<div><b>%s</b><strong>%s</strong>'
                    '<span>%s</span></div></div>'
                    % (i, kit.icon(ic, 58), a, b, c) for i, (ic, a, b, c) in enumerate(PART, 1))
    body = (kit.header("01 · PART", "벨트 장력을 잡아 주는 바퀴를 붙드는 부품", "EDU-IB-02")
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">'
            + '<section style="display:grid;gap:12px;align-content:center">' + cards + '</section>'
            + '<section class="panel">' + SVG_FRONT + '</section></main>')
    # Four tall cards, each read for fifteen to thirty seconds: revealing them
    # one at a time keeps the screen from opening as a wall of text.
    items = [beats.item(".c%d" % i, mode="reveal", dx=26, dy=0) for i in range(1, 5)]
    # The outline draws while the narrator says "지금 보시는 것이". It used to
    # finish four seconds before that sentence began.
    draw_at = beats.segment_at(spans, 1)
    tl = "\n".join([
        beats.chrome(comp, drawing=70),
        '    const ps=document.querySelectorAll("#%s .panel .outline");' % comp,
        '    ps.forEach(p=>{const l=p.getTotalLength();'
        'p.style.strokeDasharray=`${l}`;p.style.strokeDashoffset=`${l}`});',
        '    tl.to(ps,{strokeDashoffset:0,duration:3.4,ease:"power2.inOut"},%s);' % round(draw_at, 2),
        # Centre lines belong after the outline they refer to, not complete
        # before it.
        '    tl.fromTo("#%s .panel .center",{opacity:0},{opacity:1,duration:1.2,'
        'ease:"power2.out"},%s);' % (comp, round(draw_at + 3.0, 2)),
        '    tl.fromTo("#%s .panel .dim,#%s .panel .ext,#%s .panel .arrow,#%s .panel text",'
        '{opacity:0},{opacity:1,duration:1.2,ease:"power2.out"},%s);'
        % (comp, comp, comp, comp, round(draw_at + 4.0, 2)),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("02-what-is-this-part", "l2f2", 2, PART, build_part)

# ---------------------------------------------------- 3 surfaces and machining
SURF = [
    ("bore", "축 구멍 Ø25 H7", "드릴 Ø24 → 리머", "곱게 (Ra 1.6)",
     "회전하는 축이 들어가는 자리다. 표면이 거칠면 축과 구멍이 서로 긁으며 마찰과 발열이 늘고, "
     "둘 다 닳아 끼워맞춤이 헐거워진다. 곱게 다듬으면 마찰이 줄어 축이 매끄럽게 돌고 부품 수명이 유지된다. "
     "H7은 드릴만으로는 낼 수 없는 등급이라 리머로 한 번 더 다듬는다."),
    ("tap", "탭 4-M5 깊이 10", "드릴 Ø4.2 → 탭", "지정 없음",
     "축 커버를 고정하는 나사 자리다. 나사산이 직접 하중을 받으므로 드릴 지름이 정확해야 산이 제대로 남는다. "
     "네 개를 균등 배치해 커버가 한쪽으로 기울지 않게 한다."),
    ("slot", "장착 장공 2-R5", "Ø10 드릴 2회 → 엔드밀 연결", "거칠어도 됨 (Ra 12.5)",
     "볼트가 통과만 하는 구멍이다. 볼트는 머리와 프레임 사이에서 눌러 잡는 것이지 구멍 벽에 닿아 힘을 받지 않는다. "
     "그래서 벽면을 곱게 다듬을 이유가 없다. 곱게 하면 가공비만 오른다."),
    ("boss", "보스 앞면 Ø56", "단차 밀링", "보통 (Ra 6.3)",
     "커버가 덮이는 면이다. 평평하면 되고 곱기까지 요구하지 않는다. 판 전체를 두껍게 하는 대신 "
     "필요한 곳만 앞으로 8 키워 축 둘레 살 두께를 확보했다."),
    ("profile", "목과 외곽", "윤곽 밀링", "거칠어도 됨 (Ra 12.5)",
     "다른 부품과 닿지 않고 힘만 전달하는 면이다. 형상만 맞으면 되고 표면 상태는 문제되지 않는다."),
    ("fillet", "필렛 R10", "엔드밀 코너 R", "지정 없음",
     "목이 베이스로 꺾이는 안쪽 모서리다. 각지게 만나면 그 한 점에 힘이 몰려 거기서부터 금이 간다. "
     "라운드로 힘을 퍼뜨린다. 하중이 가장 큰 자리라 R을 크게 잡았다."),
]


def build_surfaces(comp, dur, spans):
    rows = "".join('<tr class="sf sf%d"><td style="color:#111;font-size:23px;white-space:nowrap">%s</td>'
                   '<td style="color:#666;white-space:nowrap">%s</td>'
                   '<td style="color:#C7004C;white-space:nowrap">%s</td></tr>'
                   % (i, n, m, r) for i, (_k, n, m, r, _w) in enumerate(SURF, 1))
    # Stacked and cross-faded. These used to be display:none toggled from a
    # timeline callback, and a callback does not fire when the renderer seeks to
    # a timestamp — the reasons could have been absent from the finished video.
    whys = "".join('<div class="wy wy%d" style="position:absolute;inset:0;opacity:0">%s</div>'
                   % (i, w) for i, (_k, _n, _m, _r, w) in enumerate(SURF, 1))
    body = (kit.header("02 · SURFACE", "면마다 다르게 깎습니다", "무엇이 닿느냐가 가공을 정한다")
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1fr) minmax(0,1.05fr)">'
            + '<section class="panel">' + SVG_FRONT + '</section>'
            + '<section style="display:grid;grid-template-rows:auto 1fr;gap:18px">'
            + '<table class="spec"><thead><tr><th>부위</th><th>가공</th><th>표면 거칠기</th></tr></thead>'
            + '<tbody>' + rows + '</tbody></table>'
            + '<div class="card" style="position:relative;padding:24px 26px;font-size:23px;'
              'line-height:1.5;color:#666">' + whys + '</div></section></main>')
    items = [beats.item(".sf%d" % i, kind="row") for i in range(1, 7)]
    tl = "\n".join([
        beats.chrome(comp, drawing=-60),
        beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
        beats.read_along(comp, items, spans),
        beats.feature_highlight(comp, [k for k, *_ in SURF], spans),
        beats.read_along(comp, [beats.item(".wy%d" % i, kind="plain", mode="reveal", dy=10, read=0)
                                for i in range(1, 7)], spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("03-surfaces", "l2f3", 3, SURF, build_surfaces)

# --------------------------------------------------------- 4 why this shape
SHAPE = [("profile", "베이스 120 × 16", "축이 만드는 비트는 힘을 두 볼트가 멀리 벌어져 받아낸다"),
         ("slot", "장공 중심거리 12", "벨트를 끼운 뒤 장력을 보며 좌우로 12 만큼 조정할 수 있다"),
         ("profile", "목 밑동 80 → 54", "굽힘 모멘트가 가장 큰 밑동이 가장 두껍고 위로 갈수록 좁아진다"),
         ("boss", "보스 Ø56 · 앞으로 8", "뒷면은 프레임에 밀착해야 하므로 평면으로 두고 돌출은 앞으로만"),
         ("bore", "축 구멍 Ø25", "보스 중심과 같은 축에 두어 힘이 한쪽으로 쏠리지 않는다")]


def build_shape(comp, dur, spans):
    cards = "".join('<div class="card sh%d"><b>%s</b><span>%s</span></div>' % (i, t, d)
                    for i, (_k, t, d) in enumerate(SHAPE, 1))
    body = (kit.header("03 · SHAPE", "형상마다 이유가 있습니다", "기능이 형상을 결정한다")
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)">'
            + '<section class="panel">' + SVG_FRONT + '</section>'
            + '<section style="display:grid;gap:14px;align-content:center">' + cards + '</section></main>')
    items = [beats.item(".sh%d" % i) for i in range(1, 6)]
    tl = "\n".join([
        beats.chrome(comp, drawing=-60),
        beats.read_along(comp, items, spans),
        beats.feature_highlight(comp, [k for k, *_ in SHAPE], spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("04-why-this-shape", "l2f4", 4, SHAPE, build_shape)

# ------------------------------------------------- 5 / 6 reading the drawing
# Thirteen notations do not fit one screen at a readable size, so the dimensions
# and the symbols get one frame each. The first column of each row is the set of
# drawing handles the narrator is pointing at while that row is lit.
DIMS = [(["w120", "h90"], "120 · 90", "전체 크기", "가로 세로 바깥 치수. 재료를 얼마나 잘라야 하는지 정한다"),
        (["c60", "c62"], "60 · 62", "보스 중심 위치", "왼쪽 끝과 바닥에서 잰 값. 이 두 값이 축의 자리를 확정한다"),
        (["h16"], "16", "베이스 높이", "프레임에 닿는 판의 두께가 아니라 정면에서 본 높이"),
        (["w80"], "80", "목 밑동 폭", "필렛이 지워 버린 이론 모서리까지의 거리. 목 선을 그릴 시작점"),
        (["s29", "s50", "s12"], "29 · 50 · 12", "장공 위치와 중심거리",
         "왼쪽 끝에서 첫 끝원까지 29, 두 장공의 끝원 사이 50, 한 장공의 두 끝원 간격 12"),
        (["s8"], "8", "장공 중심 높이", "바닥에서 잰 값. 볼트 머리가 판 안에 들어오는지 여기서 정해진다"),
        (["f26", "f95"], "26 · (95.7)", "필렛 중심", "R10의 중심이 놓이는 높이와, 참고 치수로 표기한 가로 위치"),
        (["t12", "t20"], "12 · 20", "두께", "평면도에서 읽는다. 판은 12, 보스가 있는 자리는 20")]
SYMS = [(["d25"], "Ø25 H7", "축 구멍과 끼워맞춤",
         "Ø는 지름. H7은 헐겁지도 억지도 아닌 등급으로, 드릴로는 못 내고 리머가 필요하다"),
        (["d56"], "Ø56", "보스 지름", "축 둘레에 남길 살의 바깥 지름"),
        (["pcd"], "PCD Ø44", "피치원 지름", "네 탭 구멍의 중심이 놓이는 원의 지름. 구멍 자체의 지름이 아니다"),
        (["a45"], "45°", "탭의 시작 각도", "피치원 위에서 첫 구멍이 놓이는 각도. 나머지는 90°씩 돌아간다"),
        (["m5"], "4-M5 깊이 10", "수량 · 나사 · 깊이", "앞의 숫자가 개수다. M5는 나사 규격, 10은 뚫는 깊이"),
        (["sr5"], "2-장공 R5", "수량 · 끝단 반지름", "끝이 반원인 긴 구멍. R5와 중심거리 12가 형상을 확정한다"),
        (["r10"], "2-R10", "라운드", "R은 둥글리기의 반지름. 앞 숫자는 개수"),
        (["c5"], "2-C5", "모따기", "C는 45도로 잘라내기. 5는 잘라내는 변의 길이")]


def reader(index, title, prompt, table):
    def build(comp, dur, spans):
        rows = "".join('<tr class="nt nt%d">'
                       '<td style="color:#C7004C;white-space:nowrap;font-size:22px">%s</td>'
                       '<td style="color:#111;white-space:nowrap">%s</td>'
                       '<td style="color:#666;font-size:21px">%s</td></tr>'
                       % (i, a, b, c) for i, (_d, a, b, c) in enumerate(table, 1))
        body = (kit.header(index, title, prompt)
                + '\n      <main class="body" '
                  'style="grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr)">'
                + '<section class="panel" style="padding:22px">' + SVG_FULL + '</section>'
                + '<section><table class="spec"><thead><tr><th>표기</th><th>무엇인가</th>'
                + '<th>무엇을 지시하는가</th></tr></thead><tbody>' + rows + '</tbody></table>'
                + '</section></main>')
        items = [beats.item(".nt%d" % i, kind="row") for i in range(1, len(table) + 1)]
        tl = "\n".join([
            beats.chrome(comp, drawing=-60),
            beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
            beats.read_along(comp, items, spans),
            # Without this the drawing sat frozen for a minute while the
            # narrator walked through eight of its dimensions.
            beats.dim_highlight(comp, [d for d, *_ in table], spans),
            beats.outro(comp, dur),
        ])
        return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)
    return build


frame("05-reading-dimensions", "l2f5", 5, DIMS,
      reader("04 · READ 1", "치수가 형상을 확정합니다", "숫자 하나하나가 무엇을 재는가", DIMS))
frame("06-reading-symbols", "l2f6", 6, SYMS,
      reader("05 · READ 2", "기호가 가공을 지시합니다", "Ø · R · C · M · PCD 가 무엇인가", SYMS))

# ------------------------------------------------------- 7 sheet and layers
SHEET = (
    '<svg viewBox="-34 -30 488 372" style="width:100%;height:auto;max-height:100%">'
    '<g stroke="#111" fill="none">'
    '<rect class="sh-paper" x="0" y="0" width="420" height="297" stroke-width="1.6"/>'
    '<rect class="sh-frame" x="10" y="10" width="400" height="277" stroke-width="1.6" stroke="#C7004C"/>'
    '<g class="sh-mark" stroke="#C7004C" stroke-width="1.6">'
    '<line x1="210" y1="0" x2="210" y2="10"/><line x1="210" y1="287" x2="210" y2="297"/>'
    '<line x1="0" y1="148.5" x2="10" y2="148.5"/><line x1="410" y1="148.5" x2="420" y2="148.5"/></g>'
    '<g class="sh-title" stroke="#C7004C" stroke-width="1.6">'
    '<rect x="210" y="257" width="200" height="30"/><line x1="310" y1="257" x2="310" y2="287"/></g>'
    '</g>'
    '<g font-family="Malgun Gothic,sans-serif" fill="#111">'
    '<text class="sh-title" x="260" y="277" font-size="13" text-anchor="middle">홍길동</text>'
    '<text class="sh-title" x="360" y="277" font-size="13" text-anchor="middle">사번</text>'
    '<text class="sh-gap" x="210" y="-10" font-size="13" fill="#666" text-anchor="middle">'
    '용지선과 도면선 간격 · 사방 10</text>'
    '<text class="sh-title" x="260" y="252" font-size="12" fill="#666" text-anchor="middle">100</text>'
    '<text class="sh-title" x="360" y="252" font-size="12" fill="#666" text-anchor="middle">100</text>'
    '<text class="sh-title" x="196" y="277" font-size="12" fill="#666" text-anchor="end">30</text>'
    '<text class="sh-size" x="210" y="322" font-size="14" text-anchor="middle">'
    'A3  420 × 297 · 문자 높이 10</text>'
    '</g></svg>')
LAYERS = [("외형선", "Continuous", "1", "흰색 (7)", "보이는 모양"),
          ("중심선", "Center", "0.5", "빨강 (1)", "중심과 대칭축"),
          ("숨은선", "Hidden", "0.5", "노랑 (2)", "가려진 모양"),
          ("치수선", "Continuous", "1", "보라 (6)", "치수 기입")]


def build_sheet(comp, dur, spans):
    rows = "".join('<tr class="ly ly%d"><td style="color:#111">%s</td><td style="color:#666">%s</td>'
                   '<td style="color:#666">%s</td><td style="color:#666">%s</td>'
                   '<td style="color:#666;font-size:20px">%s</td></tr>'
                   % (i, a, b, c, d, e) for i, (a, b, c, d, e) in enumerate(LAYERS, 1))
    body = (kit.header("06 · SHEET", "종이와 선의 규칙을 먼저 정합니다", "A3 가로 · 레이어 네 개")
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)">'
            + '<section class="panel" style="padding:40px">' + SHEET + '</section>'
            + '<section style="display:grid;grid-template-rows:auto auto 1fr;gap:16px;align-content:start">'
            + '<table class="spec"><thead><tr><th>레이어</th><th>선 종류</th><th>축척</th><th>색상</th>'
            + '<th>용도</th></tr></thead><tbody>' + rows + '</tbody></table>'
            + '<div class="note note1" style="margin-top:4px"><b>축척</b> 선가중치가 아니라 선 종류의 '
            + '축척입니다. 중심선과 숨은선의 점선 간격이 이 값으로 정해집니다. 화면에서 점선이 실선처럼 '
            + '보이면 이 값을 조정합니다.</div>'
            + '<div class="note note2"><b>우선순위</b> 과제 지시가 다른 이름·색상·축척을 지정하면 '
            + '그 지시가 우선합니다.</div>'
            + '</section></main>')
    # The sheet is built up, so its parts hold once drawn. The layer table is a
    # reference list, so its rows recede after their turn.
    items = [beats.item(".sh-paper", kind="plain", mode="reveal", hold=True, dy=0),
             beats.item(".sh-frame", kind="plain", mode="reveal", hold=True, dy=0),
             beats.item(".sh-mark", kind="plain", mode="reveal", hold=True, dy=0),
             beats.item(".sh-title", kind="plain", mode="reveal", hold=True, dy=0),
             beats.item("thead", kind="plain", mode="reveal", hold=True, dy=8)]
    items += [beats.item(".ly%d" % i, kind="row") for i in range(1, 5)]
    items += [beats.item(".note1", kind="plain", mode="reveal", dy=12),
              beats.item(".note2", kind="plain", mode="reveal", dy=12)]
    bs = beats.beat_spans(spans)
    tl = "\n".join([
        beats.chrome(comp, drawing=-60),
        # The caption naming the 10 mm gap used to be on screen from the first
        # frame, giving the answer away half a minute before it was explained.
        beats.cue(comp, ".sh-size", bs[0][1] + 1.0, dy=6, dur=0.8),
        beats.cue(comp, ".sh-gap", bs[1][1] + 1.0, dy=6, dur=0.8),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("07-sheet-and-layers", "l2f7", 7, [1] * 11, build_sheet)

# ------------------------------------------------------------ 8 recording
STEP_LABELS = ["acadiso.dwt 새 도면", "SAVEAS · L02_TEMPLATE", "UNITS 단위 확인",
               "LIMITS 420×297", "ZOOM All", "LINETYPE 로드 · CENTER/HIDDEN",
               "LAYER 네 개 생성", "색상 · 선 종류 지정", "외형선 현재 레이어",
               "REC 용지선 · 도면선", "중심 마크 네 개", "REC 표제란 200×30",
               "DTEXT 이름 · 사번", "OSNAP · F8 · F3 · 선가중치", "Ctrl+S 저장"]
assert len(STEPS) == len(STEP_LABELS), "SCRIPT.md 단계 수와 체크리스트 항목 수가 다르다"


def build_demo(comp, dur, spans):
    chk = "".join('<li class="st st%d">%s</li>' % (i, t) for i, t in enumerate(STEP_LABELS, 1))
    body = (kit.header("07 · DEMO-01", "템플릿 만들기", "USER RECORDING · acadiso.dwt → L02_TEMPLATE")
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1.28fr) minmax(0,.72fr)">'
            + '<section class="panel rec" style="border-style:dashed;position:relative">'
              '<div style="text-align:center;color:#666">'
              '<div style="font-size:29px;letter-spacing:.12em;color:#C7004C">USER RECORDING</div>'
              '<div style="font-size:23px;margin-top:12px">DEMO-01 · 화면 녹화 삽입</div></div>'
              '<div style="position:absolute;left:0;right:0;bottom:0;height:4px;background:#DCDBD7">'
              '<div class="prog" style="height:100%;width:100%;background:#C7004C;'
              'transform-origin:left center"></div></div></section>'
            + '<section><ol style="list-style:none;margin:0;padding:0;font-size:23px;line-height:1.5">'
            + chk + '</ol>'
            + '<div class="note"><b>우선순위</b> 과제가 템플릿을 제공하면 제공 파일을 우선하고 '
            + '교육용 기본값으로 덮어쓰지 않습니다.</div></section></main>')
    items = [beats.item(".st%d" % i, kind="plain") for i in range(1, len(STEP_LABELS) + 1)]
    tl = "\n".join([
        beats.chrome(comp, drawing=0),
        beats.read_along(comp, items, spans, entrance=0.8, group_stagger=0.07),
        # The placeholder is the widest thing on screen and cannot animate. A bar
        # tracking progress through the fifteen steps stops the frame reading as
        # seven frozen minutes.
        '    tl.fromTo("#%s .prog",{scaleX:0},{scaleX:1,duration:%s,ease:"none"},1.0);'
        % (comp, round(dur - 2.0, 2)),
        beats.cue(comp, ".note", round(dur - 12.0, 2), dy=12),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


# The recording runs longer than its narration: typing, dialogs and waiting are
# not spoken. Measured narration x 1.3, rounded to the nearest ten seconds.
DEMO_SEC = int(round(sum(beats.read_seconds(t) for _, t in STEPS) * 1.3 / 10.0)) * 10
SCRIPT[8] = list(STEPS)
frame("08-build-template", "l2f8", 8, STEP_LABELS, build_demo, fixed=DEMO_SEC)

# --------------------------------------------------------------- 9 recap
DONE = ("이번에 한 일", "부품을 읽고 도면 환경을 만들었습니다",
        ["아이들러 풀리 브래킷이 벨트 장력을 잡는 바퀴의 축을 붙드는 부품이고, 장력이 맞아야 동력 전달과 부품 수명이 유지된다는 것",
         "면마다 가공과 표면 거칠기가 다른 이유 — 축이 닿는 구멍은 곱게, 볼트가 통과만 하는 장공은 거칠어도 된다는 판단 기준",
         "형상마다의 근거 — 넓은 베이스는 모멘트, 장공은 조정 여유, 굵은 밑동은 굽힘, 필렛은 응력 집중",
         "도면 위 모든 표기가 무엇을 지시하는지 — 치수 여덟 개와 기호 여덟 개",
         "A3 용지에 사방 10 도면틀과 중심 마크, 200×30 표제란을 만들고 네 개 레이어를 설정해 템플릿 파일로 저장"])
NEXT = ("다음", "3차시 · 기준선과 외곽",
        ["절대·상대·극좌표로 점을 찍는 세 가지 방법과 각각을 언제 쓰는지",
         "LINE과 PLINE의 차이 — 왜 외곽은 하나로 이어진 객체여야 하는지",
         "원점과 기준면을 정하고 120 × 16 베이스를 좌표 입력으로 작도",
         "오늘 켜 둔 접점 스냅으로 보스 원에 접하는 목 선을 그린다",
         "마치면 L03_PROFILE 상태로 저장한다"])


def build_recap(comp, dur, spans):
    bs = beats.beat_spans(spans)
    return (kit.recap_card(comp, dur, "08 · RECAP", "이번 차시와 다음 차시", "L02_TEMPLATE 완료",
                           DONE, NEXT, spans),
            [{"kind": "appearsBy", "selector": "#%s h1" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s .p-done" % comp, "bySec": round(bs[0][1] + 3, 1)},
             {"kind": "appearsBy", "selector": "#%s .p-next" % comp, "bySec": round(bs[1][1] + 3, 1)},
             {"kind": "before", "a": "#%s .p-done" % comp, "b": "#%s .p-next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .body" % comp}])


frame("09-recap", "l2f9", 9, [1, 1], build_recap)


# ------------------------------------------------------------ 10 closing
def build_closing(comp, dur, spans):
    return (kit.closing_card(comp, dur, spans, next_no=3, next_title="기준선과 외곽"),
            [{"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": 5},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .close" % comp}])


frame("10-closing", "l2f10", 10, [1, 1], build_closing)

# ------------------------------------------------------------ assemble
slots, start = [], 0
for i, (stem, comp, dur) in enumerate(built, 1):
    slots.append(("l2-slot-%02d" % i, comp, stem, start, dur))
    start += dur

ranges = []
t = 0
for _stem, _comp, _dur in built:
    ranges.append((t, t + _dur))
    t += _dur
beats.stamp_times(os.path.join(LESSON, "SCRIPT.md"), ranges, start)

kit.write_project(LESSON, NAME, slots, start, os, json)
print("\n%s — 프레임 %d개, 전체 %ds = %d:%02d" % (NAME, len(built), start, start // 60, start % 60))
