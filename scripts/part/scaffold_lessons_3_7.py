"""Scaffold lessons 3 through 7. RUN ONCE per lesson.

After this the frames are authored compositions edited in HyperFrames Studio;
re-running discards Studio's data-hf-id stamps and any edits.

These five lessons share one skeleton (`lesson_build.PLAN`), so the shape lives
in that module and only the content lives here. Frame lengths and every cue come
from each lesson's SCRIPT.md — nothing below picks a time.

The screen text is derived from the narration, not written beside it: a card
that claims something the narrator never says is a card nobody reads out.

    python scripts/part/scaffold_lessons_3_7.py            # all five
    python scripts/part/scaffold_lessons_3_7.py 5          # just lesson 5
"""

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lesson_build as lb  # noqa: E402

ROOT = "projects/autocad-technician"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_data_3_7.json")

SLUG = {3: "lesson-03-baseline-profile", 4: "lesson-04-circles-arcs",
        5: "lesson-05-three-views", 6: "lesson-06-editing-symbols",
        7: "lesson-07-dimensioning-release"}


def spec(no, d):
    """Turn the derived data into what lesson_build.build expects."""
    s = d["spec"]
    x = d["data"]
    L = {
        "no": no,
        "title": s["title"],
        "cp": s["cp"],
        "cp_out": s["cpOut"],
        "view": s.get("view", "full"),
        "attr": s.get("attr", "dim"),
        "today_title": x["todayTitle"],
        "today": [(c["icon"], c["eyebrow"], c["heading"], c["desc"]) for c in x["today"]],
        "concept_title": x["conceptTitle"],
        "concept_prompt": x["conceptPrompt"],
        "concept_note": x["conceptNote"],
        "concept": [(c["icon"], c["eyebrow"], c["heading"], c["desc"]) for c in x["concept"]],
        "ondrawing_title": x["ondrawingTitle"],
        "ondrawing_prompt": x["ondrawingPrompt"],
        "ondrawing_head": tuple(x["ondrawingHead"]),
        "ondrawing": [(r["targets"], r["col1"], r["col2"], r["col3"]) for r in x["ondrawing"]],
        "demo_title": x["demoTitle"],
        "steps": x["steps"],
        "check_title": x["checkTitle"],
        "check_note": x["checkNote"],
        "check": [(c["icon"], c["eyebrow"], c["heading"], c["desc"]) for c in x["check"]],
        "done": (x["done"]["eyebrow"], x["done"]["heading"], x["done"]["lines"]),
        "next": (x["next"]["eyebrow"], x["next"]["heading"], x["next"]["lines"]),
    }
    if s.get("nextNo"):
        L["next_no"] = s["nextNo"]
        L["next_title"] = s["nextTitle"]
    else:
        L["final"] = ('이것으로 <em>AutoCAD 기본 과정</em> 을 마칩니다<br>'
                      '도면 한 장을 처음부터 끝까지 그려 보셨습니다')
    return L


def main():
    with io.open(DATA, encoding="utf-8") as fh:
        derived = {int(k): v for k, v in json.load(fh).items()}

    want = [int(a) for a in sys.argv[1:]] or sorted(derived)
    total = 0
    for no in want:
        print("\n=== %d차시 · %s ===" % (no, derived[no]["spec"]["title"]))
        total += lb.build(os.path.join(ROOT, SLUG[no]), spec(no, derived[no]))
    print("\n합계 %ds = %d:%02d" % (total, total // 60, total % 60))


if __name__ == "__main__":
    main()
