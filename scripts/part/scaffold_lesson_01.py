"""Scaffold lesson-01, the orientation. RUN ONCE.

After this the frames are authored compositions edited in HyperFrames Studio;
re-running discards Studio's data-hf-id stamps and any edits.

Frame lengths and every item's cue come from SCRIPT.md, not from numbers typed
here. A paragraph that opens with "(N ...)" is beat N and belongs to the Nth
item in that frame's ITEMS list. Rewrite a paragraph and the motion re-times
itself; type a stagger by hand and it silently drifts out of sync with the
words the moment the script changes.

Content is grounded in the instructor deck held in the approved private
location: the certification name, the course table of contents, the stated
purpose and requirements of a drawing, and the practice-task format. Nothing is
copied from the deck into this repository.

    python scripts/part/scaffold_lesson_01.py projects/autocad-technician/lesson-01-orientation
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import lesson_docs  # noqa: E402
import lesson_kit as kit  # noqa: E402

LESSON = sys.argv[1] if len(sys.argv) > 1 else "projects/autocad-technician/lesson-01-orientation"
NAME = os.path.basename(os.path.normpath(LESSON))
FRAMES = os.path.join(LESSON, "compositions", "frames")
os.makedirs(FRAMES, exist_ok=True)

SCRIPT = beats.parse_script(os.path.join(LESSON, "SCRIPT.md"))
built = []


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
    return spans, dur


# ---------------------------------------------------------------- 1 title
def build_title(comp, dur, spans):
    return (kit.title_card(comp, dur, "오리엔테이션", "AutoCAD 기본 과정 · 1차시"),
            [{"kind": "appearsBy", "selector": "#%s .brand" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": round(dur * .33 + 3, 1)},
             {"kind": "before", "a": "#%s .brand" % comp, "b": "#%s h2" % comp},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .sub" % comp},
             {"kind": "staysInFrame", "selector": "#%s .title" % comp}])


frame("01-title", "l1f1", 1, [], build_title, fixed=12)

# ------------------------------------------------------- 2 why the course
REQ = [("shape", "도형·크기·모양", "대상물의 형태와 치수를 담는다"),
       ("pose", "자세·위치", "어디에 어떤 방향으로 놓이는지 담는다"),
       ("surface", "표면·재료·가공", "필요하면 어떻게 만드는지까지 담는다"),
       ("same", "모호하지 않게", "읽는 사람마다 다르게 해석되면 도면이 아니다"),
       ("archive", "보존·검색·이용", "나중에 찾아 쓸 수 있는 양식을 갖춘다")]


def build_why(comp, dur, spans):
    # A row of five text blocks does not read at a glance. Each card carries a
    # mark drawn in the same pen as the part drawing; where the subject already
    # has a symbol for the idea — the roughness tick, the title block — that
    # symbol is used instead of a picture invented for it.
    cards = "".join('<div class="card rq rq%d">%s<b style="margin-top:12px">%s</b>'
                    '<span>%s</span></div>' % (i, kit.icon(ic, 58), a, b)
                    for i, (ic, a, b) in enumerate(REQ, 1))
    body = (kit.header("01 · WHY", "도면은 말을 대신합니다", "작성자의 의도를 정확하게 전달하기 위해")
            + '\n      <main class="body" style="grid-template-rows:auto 1fr auto">'
            + '<section class="lead" style="font-size:34px;line-height:1.5;color:#111;max-width:1500px">'
            + '설비 앞에서 “여기를 이만큼 깎아 주세요”라고 말로 전하면 사람마다 다르게 알아듣습니다. '
            + '도면은 그 말을 <b style="color:#C7004C">누가 읽어도 같게</b> 만드는 수단입니다. '
            + '그래서 도면에는 갖춰야 할 요건이 있습니다.</section>'
            + '<section style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;'
              'align-content:start">' + cards + '</section>'
            + '<div class="note"><b>테크니션에게</b> 설비를 다루는 사람이 도면을 읽고 그릴 수 있으면, '
            + '현장에서 본 문제를 정확한 치수와 형상으로 설계·제작 부서에 전달할 수 있습니다.</div>'
            + '</main>')
    # Five short cards side by side: showing the whole row at once tells the
    # viewer the answer has five parts, and the emphasis then carries the words.
    items = [beats.item(".rq%d" % i) for i in range(1, 6)]
    items.append(beats.item(".note", kind="plain", mode="reveal", dy=12))
    # The lead is the framing the narrator reads before reaching the cards, so
    # it is cued to that paragraph rather than to t=0.
    tl = "\n".join([
        beats.chrome(comp),
        beats.cue(comp, ".lead", beats.segment_at(spans, 1), dy=16),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("02-why-drawings", "l1f2", 2, REQ, build_why)

# ------------------------------------------------------------ 3 the task
TASKS = [("iso", "주어지는 것", "형상과 치수", "3D 형상 또는 도면 조각과 필요한 치수가 함께 주어진다"),
         ("crosshair", "해야 하는 것", "치수에 맞게 작성", "주어진 치수 그대로 작도한다. 눈대중으로 맞추지 않는다"),
         ("thirdangle", "또는", "정투상으로 투상", "한 방향만 주어지고 정면도·평면도·우측면도로 투상해 그린다"),
         ("linetypes", "보는 것", "선이 제자리에 있는가",
          "외형선·중심선·숨은선·치수선이 각자의 레이어에 맞게 들어갔는가")]


def build_task(comp, dur, spans):
    # The third card's mark is the third-angle projection symbol itself and the
    # fourth's is the four line types — the things the card is talking about,
    # not illustrations of them.
    cc = "".join('<div class="card tk tk%d" style="padding:26px 26px 24px">%s<b style="margin-top:16px">%s</b>'
                 '<strong>%s</strong><span>%s</span></div>'
                 % (i, kit.icon(ic, 58), a, b, c) for i, (ic, a, b, c) in enumerate(TASKS, 1))
    body = (kit.header("02 · TASK", "실습 과제로 확인합니다", "형상을 치수에 맞게 작성하거나 투상한다")
            + '\n      <main class="body" style="grid-template-rows:1fr auto">'
            + '<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;'
              'align-content:center">' + cc + '</section>'
            + '<div class="note"><b>우선순위</b> 과제마다 지시하는 용지·레이어·색상이 다를 수 있습니다. '
            + '이 과정에서 정하는 값은 연습용 기본값이고, 실제 과제 지시가 언제나 우선합니다.</div>'
            + '</main>')
    items = [beats.item(".tk%d" % i) for i in range(1, 5)]
    items.append(beats.item(".note", kind="plain", mode="reveal", dy=12))
    tl = "\n".join([beats.chrome(comp), beats.read_along(comp, items, spans),
                    beats.outro(comp, dur)])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("03-how-assessed", "l1f3", 3, TASKS, build_task)

# ------------------------------------------------------------- 4 roadmap
# No checkpoint column. The file names are bookkeeping the learner types in the
# lesson that produces them; on the roadmap they are a fourth column nobody
# reads and nobody acts on.
ROAD = [("1", "오리엔테이션", "지금 보고 있는 차시"),
        ("2", "부품 이해와 도면 환경", "부품이 왜 그 모양인지 읽고 A3 템플릿을 만든다"),
        ("3", "기준선과 외곽", "좌표를 입력해 베이스와 목의 외곽을 그린다"),
        ("4", "원·호·오프셋", "축 구멍, 보스, 장공, 필렛을 넣는다"),
        ("5", "제3각법 3뷰와 반복", "투상해 세 뷰를 만들고 탭을 배열한다"),
        ("6", "편집과 표현", "남은 보조선을 정리하고 도면 기호를 읽는다"),
        ("7", "치수와 출도", "치수를 기입하고 축척을 확인해 내보낸다"),
        ("8", "시험 안내와 Q&amp;A", "시험이 어떻게 진행되는지와 자주 나온 질문")]


def build_roadmap(comp, dur, spans):
    rows = "".join('<tr class="rd rd%d"><td style="color:#C7004C;font-weight:600;width:74px">%s</td>'
                   '<td style="color:#111;font-size:26px;width:34%%">%s</td>'
                   '<td style="color:#666;font-size:24px">%s</td></tr>'
                   % (i, n, t, d) for i, (n, t, d) in enumerate(ROAD, 1))
    body = (kit.header("03 · ROADMAP", "부품 하나를 끝까지 그리고 시험을 준비합니다",
                       "EDU-IB-02 아이들러 풀리 브래킷")
            + '\n      <main class="body" style="grid-template-rows:auto 1fr">'
            + '<section class="lead" style="font-size:30px;color:#666;max-width:1500px">'
            + '차시마다 새 파일을 여는 것이 아니라, 지난 시간에 저장한 파일을 열어 이어 그립니다. '
            + '한 차시를 놓치더라도 그 지점부터 이어 갈 수 있습니다.</section>'
            + '<section><table class="spec"><thead><tr><th>차시</th><th>주제</th><th>하는 일</th>'
            + '</tr></thead><tbody>' + rows + '</tbody></table></section></main>')
    items = [beats.item(".rd%d" % i, kind="row") for i in range(1, len(ROAD) + 1)]
    # The lead sentence is the third framing paragraph. Showing it at t=0 let the
    # viewer finish reading it seventeen seconds before it was spoken, and the
    # table header sat complete above an empty body for the same stretch.
    lead_at = beats.segment_at(spans, 2)
    tl = "\n".join([
        beats.chrome(comp),
        beats.cue(comp, ".lead", lead_at, dy=16),
        beats.cue(comp, "thead", lead_at + 1.4, dy=8, dur=0.7, ease="power2.out"),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


frame("04-roadmap", "l1f4", 4, ROAD, build_roadmap)

# --------------------------------------------------------------- 5 recap
DONE = ("이번에 한 일", "이 과정을 이해했습니다",
        ["도면은 작성자의 의도를 누가 읽어도 같게 전달하기 위한 수단이라는 것",
         "도면이 갖춰야 할 다섯 가지 요건 — 형상·치수, 자세·위치, 표면·재료·가공, 모호하지 않을 것, 찾아 쓸 수 있을 것",
         "실습 과제는 주어진 형상을 치수에 맞게 작성하거나 정투상으로 투상하는 방식이라는 것",
         "일곱 차시에 걸쳐 부품 하나를 누적해 완성한다는 전체 흐름"])
NEXT = ("다음", "2차시 · 부품 이해와 도면 환경",
        ["아이들러 풀리 브래킷이 무엇이고 각 면을 어떤 방법으로 가공하는지",
         "면마다 왜 그 가공을 선택했는지와 그것이 부품 수명·성능에 미치는 영향",
         "도면의 표기 하나하나가 무엇을 지시하는지",
         "A3 용지에 도면틀과 표제란을 만들고 네 개 레이어를 설정해 템플릿 파일을 남긴다"])


def build_recap(comp, dur, spans):
    bs = beats.beat_spans(spans)
    return (kit.recap_card(comp, dur, "04 · RECAP", "이번 차시와 다음 차시", "오리엔테이션 완료",
                           DONE, NEXT, spans),
            [{"kind": "appearsBy", "selector": "#%s h1" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s .p-done" % comp, "bySec": round(bs[0][1] + 3, 1)},
             {"kind": "appearsBy", "selector": "#%s .p-next" % comp, "bySec": round(bs[1][1] + 3, 1)},
             {"kind": "before", "a": "#%s .p-done" % comp, "b": "#%s .p-next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .body" % comp}])


frame("05-recap", "l1f5", 5, [], build_recap)


# ------------------------------------------------------------- 6 closing
def build_closing(comp, dur, spans):
    return (kit.closing_card(comp, dur, spans, next_no=2, next_title="부품 이해와 도면 환경"),
            [{"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": 5},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .close" % comp}])


frame("06-closing", "l1f6", 6, [1, 1], build_closing)

# ------------------------------------------------------------ assemble
slots, start = [], 0
for i, (stem, comp, dur) in enumerate(built, 1):
    slots.append(("l1-slot-%02d" % i, comp, stem, start, dur))
    start += dur

ranges = []
t = 0
for _stem, _comp, _dur in built:
    ranges.append((t, t + _dur))
    t += _dur
beats.stamp_times(os.path.join(LESSON, "SCRIPT.md"), ranges, start)

kit.write_project(LESSON, NAME, slots, start, os, json)

# One line per frame, in the order they play. lesson_docs.refresh() refuses to
# run if this list and the built slots disagree.
DESCS = [
    "검정 타이틀 · **오리엔테이션**",
    "도입 문장 + 요건 카드 5장 + 하단 문단",
    "과제 카드 4장 + 하단 문단",
    "안내 문장 + 로드맵 표(차시·주제·하는 일)",
    "2분할 마무리",
    "인사 — 검정 바탕 · 「고생하셨습니다」 · 다음 차시",
]
lesson_docs.refresh(LESSON, DESCS)

print("\n%s — 프레임 %d개, 전체 %ds = %d:%02d" % (NAME, len(built), start, start // 60, start % 60))
