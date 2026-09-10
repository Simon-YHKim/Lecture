# -*- coding: utf-8 -*-
"""Shared frame and SCRIPT readers for the Korean self-study deck.

The former frames-only command delegates to build_deck_selfstudy so it cannot
create a second, incomplete deck that omits the practice instructions. The
frame readers stay here for the canonical builder's imports.

    python scripts/selfstudy/build_deck_frames.py <lesson-dir> [output file]
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
    """기존 명령 진입점도 같은 자습 덱 생성기를 사용한다."""
    import build_deck_selfstudy as builder
    match = re.match(r'lesson-(\d+)-', os.path.basename(lesson_dir.rstrip('/\\')))
    if not match:
        raise SystemExit('차시 번호가 있는 폴더를 지정하세요: ' + lesson_dir)
    lesson_json = os.path.join(HERE, 'source', 'lesson-%02d.json' % int(match[1]))
    if not os.path.isfile(lesson_json):
        raise SystemExit('차시 자습 원본이 없습니다: ' + lesson_json)
    return builder.main(lesson_dir, lesson_json, outpath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__.splitlines()[0])
    lesson = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(lesson, "deck.html")
    sys.exit(main(lesson, out))
