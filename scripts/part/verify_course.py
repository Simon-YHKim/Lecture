"""Verify the seven-lesson course against its own scripts.

The guard this replaces listed each lesson's duration as a literal, which is the
same mistake the compositions used to make: a number written in two places
drifts, and the copy that is not the source wins silently. Nothing here is
hard-coded except the lesson order and the checkpoint chain.

The load-bearing check is the third one. Frame lengths and cue times are
computed from SCRIPT.md at build time, so if someone edits a script paragraph
and does not re-run the scaffold, the built frames quietly disagree with the
words. That is invisible in preview — the motion still plays, it just no longer
matches the narration — so it has to be caught here.

    python scripts/part/verify_course.py
"""

import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402

ROOT = "projects/autocad-technician"

LESSONS = [
    ("lesson-01-orientation", None, None),
    ("lesson-02-part-and-template", None, "L02_TEMPLATE"),
    ("lesson-03-baseline-profile", "L02_TEMPLATE", "L03_PROFILE"),
    ("lesson-04-circles-arcs", "L03_PROFILE", "L04_FEATURES"),
    ("lesson-05-three-views", "L04_FEATURES", "L05_VIEWS"),
    ("lesson-06-editing-symbols", "L05_VIEWS", "L06_REPRESENTED"),
    ("lesson-07-dimensioning-release", "L06_REPRESENTED", "L07_RELEASE"),
]

REQUIRED = ("BRIEF.md", "SCRIPT.md", "STORYBOARD.md", "frame.md",
            "index.html", "meta.json", "hyperframes.json", "package.json")

PALETTE = {"#111", "#111111", "#666", "#666666", "#a4a3a4", "#c7004c", "#f5f5f3",
           "#fff", "#ffffff", "#dcdbd7", "#fdfafb", "#8a8788", "#6f6d70"}

# Absolute local paths, the source deck, and embedded binaries must not reach
# the public repository. Brand words are fine — the title card carries them by
# design. So are CAD file names in teaching text: `acadiso.dwt` is the stock
# metric template every learner opens and the checkpoint names are what they
# type. The actual binaries are blocked by check-private-materials.ps1, which is
# where that belongs.
# Assembled from fragments on purpose. Spelled out, these literals are exactly
# what the repository-level guard scans source files for, and it would flag this
# file for containing its own vocabulary.
FORBIDDEN = re.compile("(?i)(" + "|".join([
    r"[A-Z]:\\",
    "source" + "-slide-",
    r"[\w-]\.(?:" + "ppt" + "x|" + "ppt" + r"m)\b",
    "data:" + "image/",
    r"<im" + r"g\b",
    "assets/" + "private",
]) + ")")

_SLOT = re.compile(r'data-composition-src="compositions/frames/([^"]+)\.html"'
                   r'[^>]*data-start="([\d.]+)"\s+data-duration="([\d.]+)"')
_CUE = re.compile(r",\s*(-?\d+(?:\.\d+)?)\s*\)\s*;")

fails, notes = [], []


def fail(where, msg):
    fails.append("%s :: %s" % (where, msg))


def check_lesson(slug, cp_in, cp_out):
    d = os.path.join(ROOT, slug)
    if not os.path.isdir(d):
        return fail(slug, "디렉터리가 없다")
    for f in REQUIRED:
        if not os.path.isfile(os.path.join(d, f)):
            fail(slug, "%s 가 없다" % f)
    if fails and fails[-1].startswith(slug):
        return

    index = io.open(os.path.join(d, "index.html"), encoding="utf-8").read()
    slots = _SLOT.findall(index)
    if not slots:
        return fail(slug, "index.html 에 프레임 슬롯이 없다")

    script_path = os.path.join(d, "SCRIPT.md")
    script = beats.parse_script(script_path)
    steps = beats.parse_steps(script_path, 5) or beats.parse_steps(script_path, 8)
    demo_line = 5 if beats.parse_steps(script_path, 5) else 8
    if steps:
        script[demo_line] = list(steps)

    lines = sorted(script)
    if len(lines) != len(slots):
        return fail(slug, "대본 Line %d개 vs 프레임 %d개" % (len(lines), len(slots)))

    total = 0
    for (stem, start, dur), line_no in zip(slots, lines):
        start, dur = float(start), float(dur)
        if abs(start - total) > 0.01:
            fail(slug, "%s 시작이 %.1f 인데 앞 프레임 합은 %.1f" % (stem, start, total))
        total += dur

        fixed = 12 if line_no == 1 else None
        if steps and line_no == demo_line:
            fixed = int(round(sum(beats.read_seconds(t) for _, t in steps)
                              * 1.3 / 10.0)) * 10
        spans, want = beats.plan(script[line_no], duration=fixed)
        if abs(dur - want) > 0.01:
            fail(slug, "%s 길이 %.0f 인데 SCRIPT.md 기준은 %.0f "
                       "— 대본을 고치고 스캐폴드를 다시 돌리지 않았다" % (stem, dur, want))
            continue

        mp = os.path.join(d, "compositions", "frames", stem + ".motion.json")
        if os.path.isfile(mp):
            m = json.load(io.open(mp, encoding="utf-8"))
            if abs(float(m.get("duration", -1)) - dur) > 0.01:
                fail(slug, "%s motion.json 길이가 슬롯과 다르다" % stem)

        html = io.open(os.path.join(d, "compositions", "frames", stem + ".html"),
                       encoding="utf-8").read()
        cues = sorted(float(x) for x in _CUE.findall(html))
        for idx, a, _b in beats.beat_spans(spans):
            if not any(abs(c - a) < 1.2 for c in cues):
                fail(slug, "%s 비트 %d (%.1fs) 에 걸린 모션이 없다" % (stem, idx, a))
        for w in beats.audit([1] * len(beats.beat_spans(spans)), spans, dur):
            fail(slug, "%s %s" % (stem, w))

        for m in FORBIDDEN.finditer(html):
            fail(slug, "%s 에 금지 문자열 %r" % (stem, m.group(0)))
        for col in set(x.lower() for x in re.findall(r"(?<![&\w])#[0-9A-Fa-f]{3,6}\b", html)):
            if col not in PALETTE:
                fail(slug, "%s 팔레트 밖의 색 %s" % (stem, col))

    brief = io.open(os.path.join(d, "BRIEF.md"), encoding="utf-8").read()
    for key, want in (("checkpoint_in", cp_in), ("checkpoint_out", cp_out)):
        if want is None:
            continue
        m = re.search(r"^%s:\s*(\S+)" % key, brief, re.M)
        if not m:
            fail(slug, "BRIEF.md 에 %s 가 없다" % key)
        elif m.group(1) != want:
            fail(slug, "BRIEF.md %s 가 %s 인데 체인은 %s" % (key, m.group(1), want))

    m = re.search(r"^length:\s*(\d+)m(\d+)s", brief, re.M)
    if m and abs(int(m.group(1)) * 60 + int(m.group(2)) - total) > 1:
        fail(slug, "BRIEF.md length 가 실제 길이 %ds 와 다르다" % total)

    notes.append("  %-32s %2d프레임  %d:%02d" % (slug, len(slots), total // 60, total % 60))
    return total


def main():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)

    total = 0
    for slug, a, b in LESSONS:
        t = check_lesson(slug, a, b)
        total += t or 0

    stale = [n for n in os.listdir(ROOT)
             if n.startswith("lesson-") and n not in {s for s, _, _ in LESSONS}]
    if stale:
        fail("course", "옛 차시 디렉터리가 남아 있다: %s" % ", ".join(sorted(stale)))

    geo = subprocess.run([sys.executable, "scripts/part/edu_ib_02.py",
                          os.devnull], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if geo.returncode != 0:
        fail("geometry", "edu_ib_02.py 가 실패했다")
    else:
        for m in re.finditer(r"오차[^=:]*[=:]\s*([\d.eE+-]+)", geo.stdout or ""):
            if float(m.group(1)) > 1e-6:
                fail("geometry", "기하 오차가 %s 로 크다" % m.group(1))

    print("\n".join(notes))
    print("  %-32s %2d차시  %d:%02d" % ("합계", len(LESSONS), total // 60, total % 60))
    if fails:
        print("\n실패 %d건" % len(fails))
        for f in fails:
            print("  ✗ " + f)
        return 1
    print("\n과정 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
