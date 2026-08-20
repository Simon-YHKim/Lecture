"""Verify the eight-lesson course against its own scripts.

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
import episodes  # noqa: E402

ROOT = "projects/autocad-technician"

LESSONS = [
    ("lesson-01-orientation", None, None),
    ("lesson-02-part-and-template", None, "L02_TEMPLATE"),
    ("lesson-03-baseline-profile", "L02_TEMPLATE", "L03_PROFILE"),
    ("lesson-04-circles-arcs", "L03_PROFILE", "L04_FEATURES"),
    ("lesson-05-three-views", "L04_FEATURES", "L05_VIEWS"),
    ("lesson-06-editing-symbols", "L05_VIEWS", "L06_REPRESENTED"),
    ("lesson-07-dimensioning-release", "L06_REPRESENTED", "L07_RELEASE"),
    # No CAD work of its own: the exam briefing and the questions that follow it.
    ("lesson-08-exam-and-qa", None, None),
]

REQUIRED = ("BRIEF.md", "SCRIPT.md", "STORYBOARD.md", "frame.md",
            "index.html", "meta.json", "hyperframes.json", "package.json")

PALETTE = {"#111", "#111111", "#666", "#666666", "#a4a3a4", "#c7004c", "#f5f5f3",
           "#fff", "#ffffff", "#dcdbd7", "#fdfafb", "#8a8788", "#6f6d70",
           # the recording strip's own neutrals, dark enough to sit on #111
           # without competing with the video behind it
           "#333032", "#626061", "#4a4749"}

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
_SLOT_EP = re.compile(
    r'data-composition-src="compositions/frames/([^"]+)\.html"'
    r'[^>]*data-start="([\d.]+)"\s+data-duration="([\d.]+)"')
_CUE = re.compile(r",\s*(-?\d+(?:\.\d+)?)\s*\)\s*;")

fails, notes = [], []


def fail(where, msg):
    fails.append("%s :: %s" % (where, msg))



def check_episodes(slug):
    """Every frame in exactly one episode, in order, and none over the cap.

    An episode is a playlist over the lesson's own frames, so there is nothing
    to fall out of date — but there is plenty to get wrong: a frame in two
    episodes, a frame in none, an episode that quietly runs past twenty
    minutes because a paragraph grew.
    """
    d = os.path.join(ROOT, slug)
    index = io.open(os.path.join(d, "index.html"), encoding="utf-8").read()
    master = {stem: float(dur) for stem, _s, dur in _SLOT.findall(index)}
    order = [stem for stem, _s, _d in _SLOT.findall(index)]

    claimed = episodes.frames_for(slug)
    if claimed != order:
        missing = [s for s in order if s not in claimed]
        extra = [s for s in claimed if s not in master]
        dup = sorted({s for s in claimed if claimed.count(s) > 1})
        return fail(slug, "episodes.json 의 프레임 목록이 index 와 다르다"
                          "%s%s%s"
                          % (" · 빠짐 %s" % ", ".join(missing) if missing else "",
                             " · 없는 것 %s" % ", ".join(extra) if extra else "",
                             " · 중복 %s" % ", ".join(dup) if dup else ""))

    eps = episodes.episodes_for(slug)
    ed = os.path.join(d, "compositions", "episodes")
    have = sorted(n for n in os.listdir(ed)) if os.path.isdir(ed) else []
    if have != ["ep%d.html" % i for i in range(1, len(eps) + 1)]:
        return fail(slug, "편 파일이 %d개여야 하는데 %s" % (len(eps), have or "없다"))

    for i, ep in enumerate(eps, 1):
        want = sum(master[s] for s in ep["frames"])
        if want > episodes.CAP_SEC:
            fail(slug, "%d편 「%s」 가 %d:%02d 로 상한 %d분을 넘는다"
                 % (i, ep["title"], int(want) // 60, int(want) % 60,
                    episodes.CAP_SEC // 60))
        html = io.open(os.path.join(ed, "ep%d.html" % i), encoding="utf-8").read()
        got = _SLOT_EP.findall(html)
        if [g[0] for g in got] != ep["frames"]:
            fail(slug, "%d편 파일의 프레임이 선언과 다르다" % i)
            continue
        run = 0.0
        for stem, start, dur in got:
            if abs(float(start) - run) > 0.01:
                fail(slug, "%d편 %s 시작이 %s 인데 앞 합은 %.0f" % (i, stem, start, run))
            if abs(float(dur) - master[stem]) > 0.01:
                fail(slug, "%d편 %s 길이가 마스터와 다르다" % (i, stem))
            run += float(dur)
        m = re.search(r'id="root"[^>]*data-duration="([\d.]+)"', html)
        if not m or abs(float(m.group(1)) - want) > 0.01:
            fail(slug, "%d편 전체 길이가 슬롯 합과 다르다" % i)


def check_frame_headings(slug):
    """The `(Frame N)` in a script heading is what narration-timing keys on.

    If it drifts from the frame it names, measured narration lands on a
    different frame and nothing complains — the motion still plays, it just
    stops matching the words.
    """
    d = os.path.join(ROOT, slug)
    text = io.open(os.path.join(d, "SCRIPT.md"), encoding="utf-8").read()
    heads = [(int(a), int(b)) for a, b in
             re.findall(r"^## Line (\d+)[^\n]*\(Frame (\d+)\)\s*$", text, re.M)]
    for line_no, frame_no in heads:
        if line_no != frame_no:
            fail(slug, "Line %d 의 제목이 (Frame %d) 다 — 실측 나레이션이 "
                       "엉뚱한 프레임에 붙는다" % (line_no, frame_no))

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
    cuts = episodes.cuts_for(slug)

    # Once a recording exists its own length is the answer, and the builder uses
    # it. The guard has to use the same number or a correct build fails here.
    demo_total, demo_parts = None, None
    if steps:
        rec = os.path.join(d, "recording.json")
        if os.path.isfile(rec):
            doc = json.load(io.open(rec, encoding="utf-8"))
            demo_total = int(round(doc["durationSec"]))
            if doc.get("parts"):
                demo_parts = [int(round(p["durationSec"])) for p in doc["parts"]]
        else:
            demo_total = int(round(sum(beats.read_seconds(t) for _, t in steps)
                                   * beats.DEMO_FACTOR / 10.0)) * 10

    # One Line can stand behind several frames now: the recording, cut at the
    # step boundaries the lesson declares.
    expect = []
    for line_no in lines:
        if steps and line_no == demo_line and cuts:
            sl = beats.split_steps(steps, cuts)
            lens = demo_parts or beats.split_lengths(
                demo_total, [sum(beats.read_seconds(t) for _, t in x[1])
                             for x in sl])
            for segs, dur in zip([x[1] for x in sl], lens):
                expect.append((line_no, segs, dur))
        else:
            expect.append((line_no, script[line_no], None))
    if len(expect) != len(slots):
        return fail(slug, "대본이 내놓는 프레임 %d개 vs index %d개"
                    % (len(expect), len(slots)))

    total = 0
    for (stem, start, dur), (line_no, segs, part_sec) in zip(slots, expect):
        start, dur = float(start), float(dur)
        if abs(start - total) > 0.01:
            fail(slug, "%s 시작이 %.1f 인데 앞 프레임 합은 %.1f" % (stem, start, total))
        total += dur

        fixed = part_sec
        if fixed is None:
            fixed = 12 if line_no == 1 else None
            if steps and line_no == demo_line:
                fixed = demo_total
        spans, want = beats.plan(segs, duration=fixed)
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

    # A frame file nothing plays. Adding a frame renumbers the stems, and the
    # old file survives the rebuild with no slot pointing at it — five stale
    # 08-closing.html sat in the tree from before the keys frame, still
    # carrying Studio edits, invisible to every check that starts from a slot.
    fdir = os.path.join(d, "compositions", "frames")
    played = {stem for stem, _s, _dur in slots}
    for f in sorted(os.listdir(fdir)):
        stem = re.sub(r"\.(?:html|motion\.json)$", "", f)
        if stem not in played:
            fail(slug, "%s 은 어느 슬롯도 재생하지 않는다 — 옛 프레임 파일" % f)

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

    for slug, _a, _b in LESSONS:
        check_episodes(slug)
        check_frame_headings(slug)

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
