"""Where a lesson is cut into episodes, and what each one is called.

A lesson is one continuous piece of teaching; an episode is one video. Twenty
minutes is the cap, which the drawing lessons pass on the recording alone — so
the recording frame is cut too, at a step boundary chosen for where the work
finishes rather than where the clock runs out. `episodes.json` holds both the
cut points and the grouping, because those are decisions somebody made about
the material, not values a program can derive.

The grouping is written out as frame names rather than counts or ranges. It is
longer to read and it is the reason `verify_course` can state a real invariant:
every frame of the lesson appears in exactly one episode, in order, and no
episode runs over the cap.
"""

import io
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DOC = json.load(io.open(os.path.join(_HERE, "episodes.json"), encoding="utf-8"))

CAP_SEC = _DOC["capSec"]


def _lesson(slug):
    try:
        return _DOC["lessons"][slug]
    except KeyError:
        raise SystemExit("episodes.json 에 %s 가 없다. 편을 선언해야 빌드된다." % slug)


def cuts_for(slug):
    """Step numbers to cut the recording after. Empty means one recording frame."""
    return list(_lesson(slug)["demoCuts"])


def episodes_for(slug):
    """[{title, frames: [stem, ...]}, ...] in play order."""
    return [dict(e) for e in _lesson(slug)["episodes"]]


def frames_for(slug):
    """Every frame the lesson's episodes claim, in order."""
    return [f for e in _lesson(slug)["episodes"] for f in e["frames"]]


def slugs():
    return sorted(_DOC["lessons"])
