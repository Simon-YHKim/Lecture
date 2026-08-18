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
    chk = "".join('<li class="st st%d">%s</li>' % (i, t) for i, t in enumerate(L["steps"], 1))
    body = (kit.header("04 · DEMO-01", L["demo_title"], L["cp"])
            + '\n      <main class="body" style="grid-template-columns:minmax(0,1.28fr) minmax(0,.72fr)">'
            + '<section class="panel rec" style="border-style:dashed;position:relative">'
              '<div style="text-align:center;color:#666">'
              '<div style="font-size:29px;letter-spacing:.12em;color:#C7004C">USER RECORDING</div>'
              '<div style="font-size:23px;margin-top:12px">DEMO-01 · 화면 녹화 삽입</div></div>'
              '<div style="position:absolute;left:0;right:0;bottom:0;height:4px;background:#DCDBD7">'
              '<div class="prog" style="height:100%;width:100%;background:#C7004C;'
              'transform-origin:left center"></div></div></section>'
            + '<section><ol style="list-style:none;margin:0;padding:0;font-size:21px;line-height:1.5">'
            + chk + '</ol>'
            + '<div class="note"><b>우선순위</b> 과제 지시가 다른 값을 지정하면 그 지시가 우선합니다. '
              '여기 값은 이 과정의 연습용 기본값입니다.</div></section></main>')
    items = [beats.item(".st%d" % i, kind="plain") for i in range(1, len(L["steps"]) + 1)]
    tl = "\n".join([
        beats.chrome(comp, drawing=0),
        beats.read_along(comp, items, spans, entrance=0.8, group_stagger=0.06),
        '    tl.fromTo("#%s .prog",{scaleX:0},{scaleX:1,duration:%s,ease:"none"},1.0);'
        % (comp, round(dur - 2.0, 2)),
        beats.cue(comp, ".note", round(dur - 12.0, 2), dy=12),
        beats.outro(comp, dur),
    ])
    return kit.frame_html(comp, dur, body, tl), beats.assertions(comp, items, spans)


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
        ("08-closing", f_closing, 8, None)]

# The recording runs longer than its narration: typing, dialogs and waiting are
# not spoken. Measured narration x 1.3, rounded to the nearest ten seconds.
DEMO_FACTOR = 1.3


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

    built, warn = [], []
    for i, (stem, fn, line_no, key) in enumerate(PLAN, 1):
        fixed = 12 if line_no == 1 else None
        if line_no == 5:
            fixed = int(round(sum(beats.read_seconds(t) for _, t in steps)
                              * DEMO_FACTOR / 10.0)) * 10
        spans, dur = beats.plan(script[line_no], duration=fixed)
        comp = "l%df%d" % (L["no"], i)
        html, asserts = fn(comp, dur, spans, L)
        with open(os.path.join(frames_dir, stem + ".html"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        with open(os.path.join(frames_dir, stem + ".motion.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump({"duration": dur, "assertions": asserts}, fh, ensure_ascii=False)
        built.append((stem, comp, dur))
        print(beats.report(stem, spans, dur))
        for w in beats.audit(L.get(key) or [1] * len(beats.beat_spans(spans)), spans, dur):
            warn.append("%s: %s" % (stem, w))

    slots, start, ranges = [], 0, []
    for i, (stem, comp, dur) in enumerate(built, 1):
        slots.append(("l%d-slot-%02d" % (L["no"], i), comp, stem, start, dur))
        ranges.append((start, start + dur))
        start += dur

    beats.stamp_times(script_path, ranges, start)
    kit.write_project(lesson_dir, name, slots, start, os, json)
    for w in warn:
        print("      ! " + w)
    print("\n%s — 프레임 %d개, 전체 %ds = %d:%02d"
          % (name, len(built), start, start // 60, start % 60))
    return start
