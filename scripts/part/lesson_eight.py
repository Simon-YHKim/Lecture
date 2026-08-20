"""Lesson 8 — the exam briefing and the questions that keep coming up.

The only lesson with no recording. It answers what happens on the day, the five
questions the review meeting reported hearing repeatedly, what a technician
actually does with this skill, and the commands that matter off the exam paper.

One frame carries a deliberate hole: the marking scheme has not been shared
yet. It is drawn as a reserved panel rather than filled with a guess, because a
plausible invented criterion is the worst thing this screen could contain
(LESSON_STYLE.md 28).

    python scripts/part/lesson_eight.py
"""

import io
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import lesson_build as lb  # noqa: E402
import lesson_kit as kit  # noqa: E402

ROOT = "projects/autocad-technician"
LESSON = ROOT + "/lesson-08-exam-and-qa"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_data_8.json")


# --------------------------------------------------------------- frames
def f_title(comp, dur, spans, L):
    return (kit.title_card(comp, dur, "시험 안내와 Q&amp;A", "AutoCAD 기본 과정 · 8차시"),
            [{"kind": "appearsBy", "selector": "#%s .brand" % comp, "bySec": 3},
             {"kind": "before", "a": "#%s .brand" % comp, "b": "#%s h2" % comp},
             {"kind": "staysInFrame", "selector": "#%s .title" % comp}])


def f_exam(comp, dur, spans, L):
    """Six rows on the left, the part the exam hands you on the right."""
    rows = "".join(
        '<tr class="ex ex%d"><td style="color:#C7004C;white-space:nowrap">%s</td>'
        '<td style="color:#111;white-space:nowrap">%s</td>'
        '<td style="color:#666;font-size:21px">%s</td></tr>'
        % (i, r["col1"], r["col2"], r["col3"]) for i, r in enumerate(L["exam"], 1))
    body = (kit.header("01 · EXAM", L["examTitle"], "대면 · 40분 · 제3각법")
            + '\n      <main class="body" '
              'style="grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)">'
            + '<section><table class="spec"><thead><tr><th>항목</th><th>무엇</th>'
              '<th>세부</th></tr></thead><tbody>' + rows + '</tbody></table></section>'
            + '<section class="panel" style="padding:26px">'
            + lb.part_svg("full") + '</section></main>')
    items = [beats.item(".ex%d" % i, kind="row") for i in range(1, 7)]
    tl = "\n".join([
        beats.chrome(comp, drawing=60),
        beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_qa(comp, dur, spans, L):
    """One question per card, in the card grammar the rest of the course uses:
    pink eyebrow, question, answer.

    The marking-scheme card is left open on purpose — see the module docstring.
    """
    def card(i, q, a, hold):
        inner = '<b>Q%d</b><strong style="font-size:26px">%s</strong>' % (i, q)
        if hold:
            inner += ('<div style="margin-top:12px;border:2px dashed #A4A3A4;'
                      'padding:14px 16px">'
                      '<span style="color:#C7004C;font-size:19px;letter-spacing:.06em">'
                      '채점 기준 표 &#183; 공유 예정</span>'
                      '<span style="margin-top:6px">%s</span></div>' % a)
        else:
            inner += '<span style="margin-top:10px">%s</span>' % a
        return '<div class="card qa qa%d" style="padding:24px 26px">%s</div>' % (i, inner)

    cards = "".join(card(i, x["q"], x["a"], i == 1) for i, x in enumerate(L["qa"], 1))
    body = (kit.header("02 · Q&amp;A", L["qaTitle"], "검토 회의에서 자주 나온 다섯 가지")
            + '\n      <main class="body">'
              '<section style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
              'gap:18px;align-content:center">' + cards + '</section></main>')
    items = [beats.item(".qa%d" % i) for i in range(1, 6)]
    tl = "\n".join([beats.chrome(comp), beats.read_along(comp, items, spans),
                    beats.outro(comp, dur)])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_work(comp, dur, spans, L):
    """The three jobs this skill is actually for (LESSON_STYLE.md 25)."""
    cc = "".join('<div class="card wk wk%d" style="padding:28px">%s'
                 '<b style="margin-top:18px">%s</b><strong>%s</strong><span>%s</span></div>'
                 % (i, kit.icon(x["icon"], 58), x["eyebrow"], x["heading"], x["desc"])
                 for i, x in enumerate(L["work"], 1))
    body = (kit.header("03 · WORK", L["workTitle"], "시험이 끝나도 남는 것")
            + '\n      <main class="body">'
              '<section style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
              'gap:20px;align-content:center">' + cc + '</section></main>')
    items = [beats.item(".wk%d" % i) for i in range(1, 4)]
    tl = "\n".join([beats.chrome(comp), beats.read_along(comp, items, spans),
                    beats.outro(comp, dur)])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_field(comp, dur, spans, L):
    """Commands the exam never asks for and the job does."""
    rows = "".join(
        '<tr class="fk fk%d">'
        '<td style="color:#C7004C;white-space:nowrap;'
        'font-family:ui-monospace,Consolas,monospace;font-size:23px">%s</td>'
        '<td style="color:#111;white-space:nowrap">%s</td>'
        '<td style="color:#666;font-size:21px">%s</td></tr>'
        % (i, x["cmd"], x["where"], x["why"]) for i, x in enumerate(L["keys"], 1))
    body = (kit.header("04 · FIELD", L["keysTitle"], "작도 밖에서 쓰이는 것들")
            + '\n      <main class="body" style="grid-template-rows:1fr auto">'
            + '<section><table class="spec"><thead><tr><th>명령</th><th>어디서 쓰나</th>'
              '<th>왜 쓰나</th></tr></thead><tbody>' + rows + '</tbody></table></section>'
            + '<div class="note"><b>외우지 않아도 됩니다</b> '
            + L["practiceNote"] + '</div></main>')
    items = [beats.item(".fk%d" % i, kind="row") for i in range(1, 7)]
    tl = "\n".join([
        beats.chrome(comp),
        beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
        beats.read_along(comp, items, spans),
        beats.cue(comp, ".note", max(dur - 14.0, 4.0), dy=12),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_recap(comp, dur, spans, L):
    bs = beats.beat_spans(spans)
    done = (L["done"]["eyebrow"], L["done"]["heading"], L["done"]["lines"])
    nxt = (L["next"]["eyebrow"], L["next"]["heading"], L["next"]["lines"])
    return (kit.recap_card(comp, dur, "05 · RECAP", "정리하며", "AutoCAD 기본 과정",
                           done, nxt, spans),
            [{"kind": "appearsBy", "selector": "#%s h1" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s .p-done" % comp,
              "bySec": round(bs[0][1] + 3, 1)},
             {"kind": "before", "a": "#%s .p-done" % comp, "b": "#%s .p-next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .body" % comp}])


def f_closing(comp, dur, spans, L):
    return (kit.closing_card(comp, dur, spans, final=L["final"]),
            [{"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": 5},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .close" % comp}])


# stem, builder, SCRIPT.md line, expected item count, storyboard description
PLAN = [
    ("01-title", f_title, 1, 0, "검정 타이틀 · **시험 안내와 Q&A**"),
    ("02-exam", f_exam, 2, 6, "왼쪽 시험 안내 표 6행 / 오른쪽 3뷰 도면"),
    ("03-qa", f_qa, 3, 5, "질문 카드 5장 — 첫 장은 채점 기준이 들어올 빈자리"),
    ("04-technician-work", f_work, 4, 3, "테크니션 업무 카드 3장 (마크 포함)"),
    ("05-field-commands", f_field, 5, 6, "실무 명령 표 6행 + 하단 연습 안내"),
    ("06-recap", f_recap, 6, 2, "2분할 마무리"),
    ("07-closing", f_closing, 7, 2, "인사 — 검정 바탕 · 「고생하셨습니다」 · 과정 완료"),
]


# ----------------------------------------------------------------- docs
def clock(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def put(path, text):
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


MUST_HAVE = [
    "시험 형식·시간·제출 방법·파일 이름 양식을 한 표에 모은다",
    "질문마다 답을 붙인다. 답을 못 받은 것은 「공유 예정」으로 자리를 남긴다 (원칙 28)",
    "테크니션 업무 셋 — 지그 제안 · 레이아웃 확인 · 스페어 파트 긴급 공수 (원칙 25)",
    "작도에는 잘 안 쓰지만 실무 레이아웃에서 쓰는 명령을 따로 다룬다",
]

MUST_NOT = [
    "채점 기준을 지어내지 않는다. 공유받은 표가 들어올 자리만 비워 둔다",
    "시험 일시와 장소를 특정하지 않는다. 별도 공지 사항이다",
    "실제 시험 도면을 그리거나 옮기지 않는다",
    "1~7차시에서 이미 가르친 명령을 다시 설명하지 않는다",
]


def write_docs(rows, total):
    """BRIEF.md and STORYBOARD.md, derived from what was actually built."""
    put(os.path.join(LESSON, "BRIEF.md"), "\n".join([
        "---",
        "workflow: general-video",
        "flow: automation",
        "storyboard: yes",
        'message: "시험이 어떻게 진행되는지 알려 주고, 자주 나온 질문에 답한다"',
        "destination: desktop-course",
        "aspect: 1920x1080",
        "language: ko",
        'audience: "AutoCAD 기본 과정 1~7차시를 마친 Technician 인증 응시자"',
        "length: %dm%02ds" % (total // 60, total % 60),
        "angle: lesson-08-exam-and-qa",
        "narration: user-recorded",
        "style_preset: lg-training",
        "part_id: EDU-IB-02",
        "paper: A3-landscape",
        "projection: third-angle",
        "recording_slots: 0",
        "---",
        "",
        "## Intent",
        "",
        "마지막 차시다. 새로 그리는 것은 없다. 시험 당일에 무엇이 어떻게 진행되는지",
        "한 화면에 모으고, 검토 회의에서 반복해 나온 질문 다섯 개에 답한다.",
        "그리고 이 기능이 시험 뒤 현장 어디에 쓰이는지 세 가지로 남긴다.",
        "",
        "## Must have",
        "",
    ] + ["- " + m for m in MUST_HAVE] + [
        "",
        "## Must not",
        "",
    ] + ["- " + m for m in MUST_NOT] + [
        "",
        "## Frames",
        "",
        "| # | 파일 | 길이 | 비트 |",
        "| --- | --- | --- | --- |",
    ] + ["| %d | `%s` | %ds | %s |" % (i, stem, dur, n or "—")
         for i, stem, _c, _s, dur, n, _d in rows] + [
        "",
        "프레임 길이와 비트 시각은 `SCRIPT.md` 에서 계산된다",
        "(`LESSON_STYLE.md` 13·14번). 이 표는 손으로 고치지 않는다.",
        "",
    ]))

    put(os.path.join(LESSON, "STORYBOARD.md"), "\n".join([
        "# STORYBOARD — 8차시 · 시험 안내와 Q&A",
        "",
        "전체 %s · 1920×1080 · **녹화 구간 없음**" % clock(total),
        "",
        "**모든 시각은 `SCRIPT.md` 에서 계산된다.** 문단 앞 `(N …)` 이 N번째 항목의 비트다.",
        "아래 값은 `python scripts/part/lesson_eight.py` 의 출력이지 사람이 정한 값이 아니다.",
        "",
        "| # | 컴포지션 | 시작 | 길이 | 화면 | 비트 |",
        "| --- | --- | --- | --- | --- | --- |",
    ] + ["| %d | `%s` | %s | %ds | %s | %s |" % (i, comp, clock(st), dur, d, n or "—")
         for i, _stem, comp, st, dur, n, d in rows] + [
        "",
        "## 비워 둔 자리",
        "",
        "Q1 채점 기준은 아직 공유받지 못했다. 점선 테두리로 자리만 잡아 두었다",
        "(`LESSON_STYLE.md` 28번). 표를 받으면 `scripts/part/lesson_data_8.json` 의",
        "`qa[0].a` 를 채우고 이 스크립트를 다시 돌린다.",
        "",
        "## 검증",
        "",
        "    cd %s" % LESSON,
        "    npm run check",
        "",
    ]))


# ----------------------------------------------------------------- build
def main():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)
    L = json.load(io.open(DATA, encoding="utf-8"))
    frames_dir = os.path.join(LESSON, "compositions", "frames")
    os.makedirs(frames_dir, exist_ok=True)
    script = beats.parse_script(os.path.join(LESSON, "SCRIPT.md"))

    rows, slots, start, ranges = [], [], 0, []
    for i, (stem, fn, line_no, n, desc) in enumerate(PLAN, 1):
        spans, dur = beats.plan(script[line_no], duration=12 if line_no == 1 else None)
        comp = "l8f%d" % i
        html, asserts = fn(comp, dur, spans, L)
        put(os.path.join(frames_dir, stem + ".html"), html)
        put(os.path.join(frames_dir, stem + ".motion.json"),
            json.dumps({"duration": dur, "assertions": asserts}, ensure_ascii=False))
        rows.append((i, stem, comp, start, dur, len(beats.beat_spans(spans)), desc))
        slots.append(("l8-slot-%02d" % i, comp, stem, start, dur))
        ranges.append((start, start + dur))
        start += dur
        print(beats.report(stem, spans, dur))
        for w in beats.audit([1] * n, spans, dur):
            print("      ! " + w)

    beats.stamp_times(os.path.join(LESSON, "SCRIPT.md"), ranges, start)
    kit.write_project(LESSON, os.path.basename(LESSON), slots, start, os, json)
    write_docs(rows, start)
    # The house sheet and the agent notes are the same for every lesson.
    for f in ("frame.md", "AGENTS.md", "CLAUDE.md"):
        src = os.path.join(ROOT, "lesson-07-dimensioning-release", f)
        if os.path.isfile(src) and not os.path.isfile(os.path.join(LESSON, f)):
            shutil.copyfile(src, os.path.join(LESSON, f))

    print("\n%s — 프레임 %d개, 전체 %ds = %s"
          % (os.path.basename(LESSON), len(rows), start, clock(start)))


if __name__ == "__main__":
    main()
