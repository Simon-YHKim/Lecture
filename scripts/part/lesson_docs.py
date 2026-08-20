"""Refresh the derived parts of a lesson's BRIEF.md and STORYBOARD.md.

Both documents used to be written once and then left. Every rebuild moved the
frame lengths and every added frame moved the row numbering, so by the time
anyone read them they described a video that no longer existed — lesson 3's
storyboard still listed eight frames for a nine-frame lesson, with the last two
rows one off, and every BRIEF carried a `length:` from an earlier script.

So the numbers are taken from the built artifacts, not recomputed: the slot
table in `index.html` is what the renderer will actually play. Only the derived
blocks are replaced — the intent, the must-haves, and everything a person wrote
around the table stay exactly as they are.

Each lesson passes its own screen descriptions, declared beside the frame
builders so a frame cannot be added without one.
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402

_SLOT = re.compile(r'data-composition-id="([^"]+)"\s+'
                   r'data-composition-src="compositions/frames/([^"]+)\.html"'
                   r'[^>]*data-start="([\d.]+)"\s+data-duration="([\d.]+)"')


def clock(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def slots(lesson_dir):
    """(comp, stem, start, duration) for every frame, in play order."""
    html = io.open(os.path.join(lesson_dir, "index.html"), encoding="utf-8").read()
    return [(c, s, float(a), float(d)) for c, s, a, d in _SLOT.findall(html)]


def beat_counts(lesson_dir, n):
    """How many beats each frame's narration carries.

    The demo frame is the exception: its beats are the numbered steps, not the
    `(N …)` markers — the same rule the builder and the guard use.
    """
    path = os.path.join(lesson_dir, "SCRIPT.md")
    script = beats.parse_script(path)
    for line in (5, 8):
        steps = beats.parse_steps(path, line)
        if steps:
            script[line] = list(steps)
            break
    out = [len(beats.beat_spans(beats.plan(script[ln])[0])) for ln in sorted(script)]
    if len(out) != n:
        raise SystemExit("%s: 대본 Line %d개 vs 프레임 %d개"
                         % (os.path.basename(lesson_dir), len(out), n))
    return out


def _replace_table(text, anchor, new_lines, where):
    """Swap the first markdown table after `anchor` for new_lines."""
    m = re.search(anchor, text, re.M) if anchor else None
    if anchor and not m:
        raise SystemExit("%s: 표 위치를 찾지 못했다 (%s)" % (where, anchor))
    at = m.end() if m else 0
    lines = text[at:].split("\n")
    head = next((i for i, ln in enumerate(lines) if ln.startswith("|")), None)
    if head is None:
        raise SystemExit("%s: 표가 없다" % where)
    tail = head
    while tail < len(lines) and lines[tail].startswith("|"):
        tail += 1
    return text[:at] + "\n".join(lines[:head] + new_lines + lines[tail:])


def refresh(lesson_dir, descs):
    """Rewrite the frame tables and the length figures from what was built."""
    name = os.path.basename(os.path.normpath(lesson_dir))
    sl = slots(lesson_dir)
    if len(descs) != len(sl):
        raise SystemExit("%s: 화면 설명 %d개 vs 프레임 %d개 — PLAN 과 맞춘다"
                         % (name, len(descs), len(sl)))
    nb = beat_counts(lesson_dir, len(sl))
    total = int(round(sum(d for _c, _s, _a, d in sl)))

    bp = os.path.join(lesson_dir, "BRIEF.md")
    t = io.open(bp, encoding="utf-8").read()
    t = re.sub(r"^length:.*$", "length: %dm%02ds" % (total // 60, total % 60),
               t, count=1, flags=re.M)
    rows = (["| # | 파일 | 길이 | 화면 | 비트 |", "| --- | --- | --- | --- | --- |"]
            + ["| %d | `%s` | %ds | %s | %s |" % (i, stem, round(d), desc, n or "—")
               for i, ((_c, stem, _a, d), desc, n) in enumerate(zip(sl, descs, nb), 1)])
    t = _replace_table(t, r"^## Frames\s*$", rows, name + " BRIEF")
    io.open(bp, "w", encoding="utf-8", newline="\n").write(t)

    sp = os.path.join(lesson_dir, "STORYBOARD.md")
    t = io.open(sp, encoding="utf-8").read()
    t = re.sub(r"^전체 [^·]*·", "전체 %s ·" % clock(total), t, count=1, flags=re.M)
    demo = [d for _c, s, _a, d in sl if "demo" in s or "build-template" in s]
    if demo:
        t = re.sub(r"\(`DEMO-01`[^)]*\)", "(`DEMO-01`, %s)" % clock(demo[0]), t, count=1)
    rows = (["| # | 컴포지션 | 시작 | 길이 | 화면 | 비트 |",
             "| --- | --- | --- | --- | --- | --- |"]
            + ["| %d | `%s` | %s | %ds | %s | %s |"
               % (i, comp, clock(a), round(d), desc, n or "—")
               for i, ((comp, _s, a, d), desc, n) in enumerate(zip(sl, descs, nb), 1)])
    t = _replace_table(t, None, rows, name + " STORYBOARD")
    io.open(sp, "w", encoding="utf-8", newline="\n").write(t)
    return total
