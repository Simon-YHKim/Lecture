"""The shared skeleton for lessons 3 through 7.

Every drawing lesson has the same eight frames — title, what we draw today, the
concept behind it, where it lives on the drawing, the recording, the checks, the
two-panel recap, the sign-off. Copying that eight times would mean eight places
to fix the next time a rule changes, so the shape lives here once and each
lesson supplies only its content.

Frame lengths and cues come from SCRIPT.md through `beats`; nothing here picks
a time.
"""

import json
import os
import subprocess
import sys
import tempfile

import beats
import episodes
import lesson_docs
import lesson_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
_SVG = {}


def part_svg(profile):
    if profile not in _SVG:
        tmp = os.path.join(tempfile.mkdtemp(), "part.svg")
        subprocess.run([sys.executable, os.path.join(HERE, "edu_ib_02.py"), tmp,
                        "--profile", profile], check=True, capture_output=True)
        with open(tmp, encoding="utf-8") as fh:
            _SVG[profile] = fh.read()
    return _SVG[profile]


# --------------------------------------------------------------- frames
def f_title(comp, dur, spans, L):
    return (kit.title_card(comp, dur, L["title"], "AutoCAD 기본 과정 · %d차시" % L["no"]),
            [{"kind": "appearsBy", "selector": "#%s .brand" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": round(dur * .33 + 3, 1)},
             {"kind": "before", "a": "#%s .brand" % comp, "b": "#%s h2" % comp},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .sub" % comp},
             {"kind": "staysInFrame", "selector": "#%s .title" % comp}])


def f_today(comp, dur, spans, L):
    """Four cards beside the drawing, each with its own mark, revealed as read.

    The drawing is of the part, not of what these cards claim about it, so the
    cards carry marks (LESSON_STYLE 20).
    """
    cards = "".join('<div class="card wide c%d" style="padding:16px 20px">%s<div><b>%s</b>'
                    '<strong>%s</strong><span>%s</span></div></div>'
                    % (i, kit.icon(ic, 58), a, b, c)
                    for i, (ic, a, b, c) in enumerate(L["today"], 1))
    body = (kit.header("01 · TODAY", L["today_title"], L["cp_out"])
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">'
            + '<section style="display:grid;gap:12px;align-content:center">' + cards + '</section>'
            + '<section class="panel">' + part_svg("front") + '</section></main>')
    items = [beats.item(".c%d" % i, mode="reveal", dx=26, dy=0) for i in range(1, 5)]
    draw_at = beats.segment_at(spans, 0)
    tl = "\n".join([
        beats.chrome(comp, drawing=70),
        '    const ps=document.querySelectorAll("#%s .panel .outline");' % comp,
        '    ps.forEach(p=>{const l=p.getTotalLength();'
        'p.style.strokeDasharray=`${l}`;p.style.strokeDashoffset=`${l}`});',
        '    tl.to(ps,{strokeDashoffset:0,duration:3.4,ease:"power2.inOut"},%s);' % round(draw_at, 2),
        '    tl.fromTo("#%s .panel .center",{opacity:0},{opacity:1,duration:1.2,'
        'ease:"power2.out"},%s);' % (comp, round(draw_at + 3.0, 2)),
        '    tl.fromTo("#%s .panel .dim,#%s .panel .ext,#%s .panel .arrow,#%s .panel text",'
        '{opacity:0},{opacity:1,duration:1.2,ease:"power2.out"},%s);'
        % (comp, comp, comp, comp, round(draw_at + 4.0, 2)),
        beats.read_along(comp, items, spans),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_concept(comp, dur, spans, L):
    """Four concept cards, no drawing. Marks do the work the drawing would."""
    cc = "".join('<div class="card tk tk%d" style="padding:26px 26px 24px">%s'
                 '<b style="margin-top:16px">%s</b><strong>%s</strong><span>%s</span></div>'
                 % (i, kit.icon(ic, 58), a, b, c)
                 for i, (ic, a, b, c) in enumerate(L["concept"], 1))
    body = (kit.header("02 · HOW", L["concept_title"], L["concept_prompt"])
            + '\n      <main class="body" style="grid-template-rows:1fr auto">'
            + '<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;'
              'align-content:center">' + cc + '</section>'
            + '<div class="note"><b>기억할 것</b> ' + L["concept_note"] + '</div></main>')
    items = [beats.item(".tk%d" % i) for i in range(1, 5)]
    tl = "\n".join([beats.chrome(comp), beats.read_along(comp, items, spans),
                    beats.cue(comp, ".note", max(dur - 14.0, 4.0), dy=12),
                    beats.outro(comp, dur)])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_ondrawing(comp, dur, spans, L):
    """Six rows walked one at a time, each lighting what it names on the drawing.

    A lesson with nothing to point at (the symbols lesson) passes no targets and
    the table simply reads along on its own.
    """
    rows = "".join('<tr class="nt nt%d">'
                   '<td style="color:#C7004C;white-space:nowrap;font-size:22px">%s</td>'
                   '<td style="color:#111;white-space:nowrap">%s</td>'
                   '<td style="color:#666;font-size:21px">%s</td></tr>'
                   % (i, a, b, c) for i, (_t, a, b, c) in enumerate(L["ondrawing"], 1))
    body = (kit.header("03 · WHERE", L["ondrawing_title"], L["ondrawing_prompt"])
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr)">'
            + '<section class="panel" style="padding:22px">' + part_svg(L.get("view", "full"))
            + '</section>'
            + '<section><table class="spec"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>'
              '<tbody>' % L["ondrawing_head"] + rows + '</tbody></table></section></main>')
    items = [beats.item(".nt%d" % i, kind="row") for i in range(1, 7)]
    tgt = [t for t, *_ in L["ondrawing"]]
    tl = [beats.chrome(comp, drawing=-60),
          beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
          beats.read_along(comp, items, spans)]
    if any(tgt):
        tl.append(beats.attr_highlight(comp, L.get("attr", "dim"), tgt, spans))
    tl.append(beats.outro(comp, dur))
    return kit.frame_html(comp, dur, body, "\n".join(tl)), beats.assertions(comp, items, spans)


def f_demo(comp, dur, spans, L):
    """The recording fills the frame; a strip along the bottom carries the step.

    Only one step is on screen at a time, so the strip stays short enough to
    read at a glance while the video behind it keeps every pixel it was filmed
    with.

    When the recording is cut into parts, `L["stepSlice"]` says which steps this
    frame shows and where they start. The strip goes on counting against the
    whole lesson — part two opens at 「07 / 16」, not at 「01 / 10」 — but the
    class names restart at 1, because the beats handed to read_along are
    numbered within this frame.
    """
    lo, hi = L.get("stepSlice", (0, len(L["steps"])))
    n = len(L["steps"])
    titles = L["steps"][lo:hi]
    keys = L["stepKeys"][lo:hi]
    # Only one step is meant to be readable at a time; the pair overlaps only
    # during the crossfade between them, which is the intent.
    strips = "".join(
        '<div class="sp sp%d" data-layout-allow-overlap>'
        '<span class="no">%02d<i>&#8201;/&#8201;%02d</i></span>'
        '<span class="key">%s</span><span class="what">%s</span></div>'
        % (i, lo + i, n, k or "&#183;", t)
        for i, (t, k) in enumerate(zip(titles, keys), 1))

    body = ('      <div class="film">'
            '<div class="rec"><div class="recmark">USER RECORDING</div>'
            '<div class="recsub">%s &#183; %s</div></div>'
            '<div class="tag">%s</div>'
            '<div class="strip">%s'
            '<div class="track"><i class="prog"></i></div></div></div>'
            % (L.get("demoId", "DEMO-01"), L["cp"], L["demo_title"], strips))

    items = [beats.item(".sp%d" % i, kind="plain", mode="reveal", dy=12, read=0)
             for i in range(1, len(titles) + 1)]
    tl = "\n".join([
        '    tl.fromTo("#%s .tag",{opacity:0,y:-14},{opacity:1,y:0,duration:.8,'
        'ease:"power3.out"},.35);' % comp,
        '    tl.fromTo("#%s .strip",{opacity:0,y:26},{opacity:1,y:0,duration:.9,'
        'ease:"power3.out"},.7);' % comp,
        beats.read_along(comp, items, spans),
        '    tl.fromTo("#%s .prog",{scaleX:0},{scaleX:1,duration:%s,ease:"none"},1.2);'
        % (comp, round(dur - 2.4, 2)),
        # the title tag is orientation, not something to read for seven minutes
        '    tl.to("#%s .tag",{opacity:0,duration:1.0,ease:"power2.in"},%s);'
        % (comp, round(min(dur * .06, 30.0), 2)),
        '    tl.to("#%s .strip",{opacity:0,y:18,duration:.9,ease:"power2.in"},%s);'
        % (comp, round(dur - 1.05, 2)),
    ])
    return kit.frame_html(comp, dur, body, tl), [
        {"kind": "appearsBy", "selector": "#%s .strip" % comp, "bySec": 3},
        {"kind": "staysInFrame", "selector": "#%s .strip" % comp},
    ]


def f_check(comp, dur, spans, L):
    cc = "".join('<div class="card ck ck%d" style="padding:26px 26px 24px">%s'
                 '<b style="margin-top:16px">%s</b><strong>%s</strong><span>%s</span></div>'
                 % (i, kit.icon(ic, 58), a, b, c)
                 for i, (ic, a, b, c) in enumerate(L["check"], 1))
    body = (kit.header("05 · CHECK", L["check_title"], "저장하기 전에 확인합니다")
            + '\n      <main class="body" style="grid-template-rows:1fr auto">'
            + '<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;'
              'align-content:center">' + cc + '</section>'
            + '<div class="note"><b>고치는 법</b> ' + L["check_note"] + '</div></main>')
    items = [beats.item(".ck%d" % i) for i in range(1, 5)]
    tl = "\n".join([beats.chrome(comp), beats.read_along(comp, items, spans),
                    beats.cue(comp, ".note", max(dur - 14.0, 4.0), dy=12),
                    beats.outro(comp, dur)])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_keys(comp, dur, spans, L):
    """What was typed today, with the situation it belongs to.

    A learner who only ever draws the exam part forgets the command. One who
    knows the situation reaches for it again, which is the point — the last
    column is the part that survives the exam.

    A long lesson types sixteen commands, and sixteen rows at reading size do
    not fit under the function-key note; the first version of this frame ran
    250px past the bottom of the body and simply lost its last five rows. Past
    nine the table splits into two columns instead of shrinking further.
    """
    keys = L["keys"]

    def table(part, first):
        rows = "".join(
            '<tr class="ky ky%d"><td style="color:#C7004C;white-space:nowrap;'
            'font-family:ui-monospace,Consolas,monospace;font-size:22px">%s</td>'
            '<td style="color:#111;white-space:nowrap">%s</td>'
            '<td style="color:#666;font-size:19px">%s</td></tr>'
            % (first + j, key, kit.COMMANDS[key][1], kit.COMMANDS[key][2])
            for j, key in enumerate(part))
        return ('<table class="spec tight" style="font-size:20px">'
                '<thead><tr><th>입력</th><th>무엇을 하나</th><th>언제 쓰나</th>'
                '</tr></thead><tbody>' + rows + '</tbody></table>')

    if len(keys) > 9:
        half = (len(keys) + 1) // 2
        inner = table(keys[:half], 1) + table(keys[half:], half + 1)
        sec = ('<section style="display:grid;grid-template-columns:1fr 1fr;gap:26px;'
               'align-content:start;overflow:hidden">' + inner + '</section>')
    else:
        sec = '<section style="overflow:hidden">' + table(keys, 1) + '</section>'

    fk = "".join('<span style="display:inline-block;margin:0 22px 8px 0">'
                 '<b style="font-family:ui-monospace,Consolas,monospace;color:#C7004C">%s</b>'
                 ' <span style="color:#666">%s</span></span>' % (k, what)
                 for k, what, _why in kit.FUNCTION_KEYS)
    body = (kit.header("07 · KEYS", "오늘 친 것", "명령보다 상황을 기억하세요")
            + '\n      <main class="body" style="grid-template-rows:1fr auto">'
            + sec
            + '<div class="note"><b>기능키</b> ' + fk + '</div></main>')
    items = [beats.item(".ky%d" % i, kind="row") for i in range(1, len(keys) + 1)]
    tl = "\n".join([
        beats.chrome(comp),
        beats.cue(comp, "thead", 1.5, dy=8, dur=0.7, ease="power2.out"),
        beats.read_along(comp, items, spans),
        beats.cue(comp, ".note", max(dur - 12.0, 4.0), dy=12),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


def f_recap(comp, dur, spans, L):
    bs = beats.beat_spans(spans)
    return (kit.recap_card(comp, dur, "06 · RECAP", "이번 차시와 다음 차시",
                           "%s 완료" % L["cp_out"], L["done"], L["next"], spans),
            [{"kind": "appearsBy", "selector": "#%s h1" % comp, "bySec": 3},
             {"kind": "appearsBy", "selector": "#%s .p-done" % comp, "bySec": round(bs[0][1] + 3, 1)},
             {"kind": "appearsBy", "selector": "#%s .p-next" % comp, "bySec": round(bs[1][1] + 3, 1)},
             {"kind": "before", "a": "#%s .p-done" % comp, "b": "#%s .p-next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .body" % comp}])


def f_closing(comp, dur, spans, L):
    return (kit.closing_card(comp, dur, spans, next_no=L.get("next_no"),
                             next_title=L.get("next_title"), final=L.get("final")),
            [{"kind": "appearsBy", "selector": "#%s h2" % comp, "bySec": 5},
             {"kind": "before", "a": "#%s h2" % comp, "b": "#%s .next" % comp},
             {"kind": "staysInFrame", "selector": "#%s .close" % comp}])


PLAN = [("01-title", f_title, 1, None),
        ("02-today", f_today, 2, "today"),
        ("03-concept", f_concept, 3, "concept"),
        ("04-on-the-drawing", f_ondrawing, 4, "ondrawing"),
        ("05-demo", f_demo, 5, "steps"),
        ("06-check", f_check, 6, "check"),
        ("07-recap", f_recap, 7, None),
        ("08-keys", f_keys, 8, "keys"),
        ("09-closing", f_closing, 9, None)]

# Narration x beats.DEMO_FACTOR, rounded to the nearest ten seconds.
DEMO_FACTOR = beats.DEMO_FACTOR

# One line per frame in PLAN order. lesson_docs.refresh() refuses to run if the
# two lists disagree, so a frame cannot be added without saying what is on it.
DESCS = [
    "검정 타이틀 · **%s**",
    "왼쪽 카드 4장(마크 포함) / 오른쪽 정면도",
    "개념 카드 4장 + 하단 문단",
    "왼쪽 도면 / 오른쪽 표 6행 — 행마다 도면의 해당 위치가 붉어진다",
    "전체화면 **녹화 삽입 영역** — 하단 띠에 진행 중인 단계와 단축키",
    "확인 카드 4장 + 하단 문단",
    "2분할 마무리",
    "오늘 친 단축키 표 + 기능키",
    "인사 — 검정 바탕 · 「고생하셨습니다」 · 다음 차시",
]


def build(lesson_dir, L):
    name = os.path.basename(os.path.normpath(lesson_dir))
    frames_dir = os.path.join(lesson_dir, "compositions", "frames")
    os.makedirs(frames_dir, exist_ok=True)
    script_path = os.path.join(lesson_dir, "SCRIPT.md")
    script = beats.parse_script(script_path)
    steps = beats.parse_steps(script_path, 5)
    assert len(steps) == len(L["steps"]), (
        "%s: SCRIPT.md 단계 %d개, 체크리스트 %d개" % (name, len(steps), len(L["steps"])))
    script[5] = list(steps)
    # The commands the recording actually types, read from the script itself so
    # the summary table cannot list one the demo never used.
    L["keys"] = beats.shortcuts_in(script_path, 5)
    L["stepKeys"] = beats.step_keys(script_path, 5)

    # Once a recording exists its real length replaces the estimate, and once the
    # narration is aligned the beats sit where they were actually spoken.
    rec = os.path.join(lesson_dir, "recording.json")
    demo_sec, demo_parts = None, None
    if os.path.isfile(rec):
        with open(rec, encoding="utf-8") as fh:
            doc = json.load(fh)
        demo_sec = int(round(doc["durationSec"]))
        if doc.get("parts"):
            demo_parts = [int(round(p["durationSec"])) for p in doc["parts"]]
    measured = beats.load_measured(lesson_dir)

    cuts = episodes.cuts_for(name)
    demo_total = demo_sec or int(round(
        sum(beats.read_seconds(t) for _, t in steps) * DEMO_FACTOR / 10.0)) * 10

    # One script Line can now produce several frames. The frame *number* stays
    # what the script's "(Frame N)" heading says, because narration-timing is
    # keyed by it — the parts of the recording share number 5 and differ by
    # letter. Nothing after the recording moves.
    sched = []
    for i, (stem, fn, line_no, key) in enumerate(PLAN, 1):
        if line_no != 5 or not cuts:
            sched.append((stem, fn, line_no, key, i, "", None, None))
            continue
        slices = beats.split_steps(steps, cuts)
        # Weight is only how you guess. Real takes are measured.
        lens = demo_parts or beats.split_lengths(
            demo_total, [sum(beats.read_seconds(t) for _, t in sl)
                         for _off, sl in slices])
        if len(lens) != len(slices):
            raise SystemExit("%s: 녹화 %d개인데 컷은 %d조각이다"
                             % (name, len(lens), len(slices)))
        for k, ((off, sl), d) in enumerate(zip(slices, lens)):
            sched.append((stem + "-" + "abcdefgh"[k], fn, line_no, key, i,
                          "abcdefgh"[k], (off, off + len(sl), sl), d))

    built, warn = [], []
    frame_start = 0.0
    for stem, fn, line_no, key, idx, suffix, part, fixed in sched:
        if line_no == 1:
            fixed = 12
        elif line_no == 5 and fixed is None:
            fixed = demo_total
        segs = script[line_no] if part is None else part[2]
        spans, dur = beats.plan(segs, duration=fixed)
        # The recording has no narration to align against; its own file length
        # is the measurement, and that arrives through recording.json.
        if part is None and measured.get(idx):
            got = beats.measured_plan(script[line_no], measured[idx],
                                      frame_start, frame_start + dur)
            if got:
                spans = got
        frame_start += dur
        comp = "l%df%d%s" % (L["no"], idx, suffix)
        if part is None:
            L.pop("stepSlice", None)
            L.pop("demoId", None)
        else:
            L["stepSlice"] = (part[0], part[1])
            L["demoId"] = "DEMO-01" + suffix.upper()
        html, asserts = fn(comp, dur, spans, L)
        with open(os.path.join(frames_dir, stem + ".html"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        with open(os.path.join(frames_dir, stem + ".motion.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump({"duration": dur, "assertions": asserts}, fh, ensure_ascii=False)
        built.append((stem, comp, dur, line_no))
        print(beats.report(stem, spans, dur))
        want = L.get(key)
        if part is not None:
            want = [1] * len(part[2])
        for w in beats.audit(want or [1] * len(beats.beat_spans(spans)), spans, dur):
            warn.append("%s: %s" % (stem, w))
    L.pop("stepSlice", None)
    L.pop("demoId", None)

    slots, start, ranges = [], 0, []
    for i, (stem, comp, dur, line_no) in enumerate(built, 1):
        slots.append(("l%d-slot-%02d" % (L["no"], i), comp, stem, start, dur))
        # One Time line per script Line, so the parts of the recording report
        # as the single span they add up to.
        if ranges and ranges[-1][2] == line_no:
            ranges[-1] = (ranges[-1][0], start + dur, line_no)
        else:
            ranges.append((start, start + dur, line_no))
        start += dur

    beats.stamp_times(script_path, [(a, b) for a, b, _ln in ranges], start)
    kit.write_project(lesson_dir, name, slots, start, os, json)
    eps = kit.write_episodes(lesson_dir, slots, episodes.episodes_for(name), os)
    for n, (_f, title, sec, _fr) in enumerate(eps, 1):
        print("    %d편 %-22s %d:%02d" % (n, title, int(sec) // 60, int(sec) % 60))
    descs = list(DESCS)
    descs[0] = descs[0] % L["title"]
    if cuts:
        demo_at = [i for i, p in enumerate(PLAN) if p[2] == 5][0]
        descs[demo_at:demo_at + 1] = [
            descs[demo_at] + " (%d/%d)" % (k + 1, len(cuts) + 1)
            for k in range(len(cuts) + 1)]
    lesson_docs.refresh(lesson_dir, descs)
    for w in warn:
        print("      ! " + w)
    print("\n%s — 프레임 %d개, 전체 %ds = %d:%02d"
          % (name, len(built), start, start // 60, start % 60))
    return start
