# -*- coding: utf-8 -*-
"""Turn a lesson's own video frames into a navigable deck.

The first deck built slides from the self-study JSON and threw away what the
course already had: seventy-eight frames authored in Studio, with the LG type
system, the canonical drawing, feature highlighting and real motion. That was
the wrong call. This one mounts those frames as the slides.

Each frame is already a HyperFrames composition with its own `data-composition-id`
and its own paused timeline, so a deck is mostly bookkeeping: place them on one
clock, list them in the slideshow island, and turn the narration beats that were
measured from the script into fragment hold-points, so pressing Next walks the
same reveal the video walks.

The frames carry Korean text. An English deck cannot be made by mounting them —
that needs either translated frames or an English layer over them, which is a
decision, not a build step.

    python scripts/selfstudy/build_deck_frames.py <lesson-dir> [출력 파일]

**폐기.** 2세대. 기존 78프레임을 그대로 마운트하는 방식이라 영어 덱을 만들 수
없어 접었다. 현행 정본은 `build_deck_selfstudy.py` 다.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SLOT = re.compile(
    r'data-composition-id="(?P<cid>[^"]+)"\s+data-composition-src="(?P<src>[^"]+)"'
    r'\s+data-start="(?P<start>[\d.]+)"\s+data-duration="(?P<dur>[\d.]+)"')
TEMPLATE = re.compile(r"<template>(.*)</template>", re.S)
LINE_HEAD = re.compile(r"^##\s*Line\s*(\d+)\s*—\s*(.*?)\s*\(Frame\s*(\d+)\)", re.M)


def slots_of(index_html):
    """[(cid, src, start, duration)] in the order the lesson plays them."""
    out = []
    for m in SLOT.finditer(index_html):
        out.append((m.group("cid"), m.group("src"),
                    float(m.group("start")), float(m.group("dur"))))
    return out


SCRIPT_BLOCK = re.compile(r"(<script[^>]*>)(.*?)(</script>)", re.S)


def frame_body(path):
    """The frame's own markup and script, without its document wrapper.

    Each frame declares `const tl` at the top level of its own document, which
    is fine while it is the only thing on the page. Ten of them on one deck is
    ten redeclarations, and the browser stops at the first. Wrapping each block
    in its own function keeps every frame's script exactly as authored — they
    publish through `window.__timelines`, which does not care about scope.
    """
    doc = io.open(path, encoding="utf-8").read()
    m = TEMPLATE.search(doc)
    body = (m.group(1) if m else doc).strip()
    return SCRIPT_BLOCK.sub(
        lambda s: "%s(function(){%s})();%s" % (s.group(1), s.group(2), s.group(3)),
        body)


def notes_for(script_md):
    """{frame_number: presenter note} — the narration, minus stage directions."""
    txt = io.open(script_md, encoding="utf-8").read()
    heads = list(LINE_HEAD.finditer(txt))
    out = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(txt)
        block = txt[m.end():end]
        say = []
        for raw in block.splitlines():
            if not (raw.startswith("    ") or raw.startswith("\t")):
                continue
            s = raw.strip()
            if not s or s.startswith(">"):
                continue
            s = re.sub(r"^\([^)]*\)\s*", "", s)
            s = re.sub(r"`([^`]*)`", r"\1", s)
            if s:
                say.append(s)
        out[int(m.group(3))] = " ".join(say)
    return out


def main(lesson_dir, outpath):
    index = io.open(os.path.join(lesson_dir, "index.html"), encoding="utf-8").read()
    slots = slots_of(index)
    if not slots:
        raise SystemExit("index.html 에서 프레임 슬롯을 못 찾았다: %s" % lesson_dir)

    timing_path = os.path.join(lesson_dir, "narration-timing.json")
    timing = json.load(io.open(timing_path, encoding="utf-8")) if os.path.exists(timing_path) else None
    beats_by_frame = {}
    frame_start = {}
    if timing:
        for f in timing["frames"]:
            frame_start[f["frame"]] = f["start"]
        for b in timing["beats"]:
            beats_by_frame.setdefault(b["frame"], []).append(b["observedStart"])

    notes = notes_for(os.path.join(lesson_dir, "SCRIPT.md"))

    bodies, slides, clock = [], [], 0.0
    for n, (cid, src, _s, dur) in enumerate(slots, 1):
        path = os.path.join(lesson_dir, src.replace("/", os.sep))
        body = frame_body(path)
        # The frame's root sits at data-start 0 in its own file; on the deck's
        # clock it has to say where it actually is.
        body = re.sub(r'(id="%s-root"[^>]*?)data-start="0"' % re.escape(cid),
                      r'\1data-start="%s"' % clock, body, count=1)
        bodies.append('<!-- %s · %s -->\n%s' % (cid, os.path.basename(src), body))

        entry = {"sceneId": cid, "notes": notes.get(n, "")[:900] or "—"}
        bts = beats_by_frame.get(n) or []
        f0 = frame_start.get(n)
        if bts and f0 is not None:
            frag = [round(clock + (t - f0), 2) for t in bts]
            frag = [t for t in frag if clock <= t <= clock + dur]
            if frag:
                entry["fragments"] = frag
        slides.append(entry)
        clock += dur

    island = json.dumps({"slides": slides, "slideSequences": []},
                        ensure_ascii=False, indent=1)
    nav = io.open(os.path.join(HERE, "assets", "deck_nav.html"), encoding="utf-8").read()
    lesson = os.path.basename(lesson_dir.rstrip("/\\"))
    title = re.search(r"#\s*SCRIPT\s*—\s*(.*)", io.open(
        os.path.join(lesson_dir, "SCRIPT.md"), encoding="utf-8").read())
    title = title.group(1).strip() if title else lesson

    doc = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>%s</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  *{box-sizing:border-box}
  html,body{margin:0;background:#0B0A0A}
  /* The frames position themselves at inset:0 and expect to be the only thing
     on the page. On a deck they are siblings, so the stage places them and
     these three properties have to win. */
  /* inset is a shorthand for all four sides, so it has to be cleared *before*
     left/top are set — put it after and it wipes the two values just given. */
  #stage [data-composition-id]{inset:auto!important;position:absolute!important;
    left:50%%!important;top:50%%!important}
</style>
</head>
<body>
<script type="application/hyperframes-slideshow+json">
%s
</script>
%s
<script>window.__timelines = window.__timelines || {};</script>
%s
</body>
</html>
""" % (title, island, "\n".join(bodies), nav)

    outdir = os.path.dirname(os.path.abspath(outpath))
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    io.open(outpath, "w", encoding="utf-8", newline="\n").write(doc)
    size = os.path.getsize(outpath)
    withfrag = sum(1 for s in slides if s.get("fragments"))
    print("%-32s 슬라이드 %2d · 프래그먼트 %2d장 · %.0f초 · %d B"
          % (lesson, len(slides), withfrag, clock, size))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__.splitlines()[0])
    lesson = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(lesson, "deck.html")
    sys.exit(main(lesson, out))
