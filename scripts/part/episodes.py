"""One delivery per lesson; demo cuts are private recording assembly boundaries.

The historical module/API name remains for callers. Old episode HTML files are
historical artifacts; the current course is delivered from its master index.
"""

import io
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DOC = json.load(io.open(os.path.join(_HERE, "episodes.json"), encoding="utf-8"))

CAP_SEC = _DOC.get("capSec")


def is_unified(slug):
    return _DOC.get('deliveryMode') == 'lesson' and slug in _DOC['lessons']


def _lesson(slug):
    try:
        return _DOC["lessons"][slug]
    except KeyError:
        raise SystemExit("episodes.json 에 %s 가 없다. 차시를 선언해야 빌드된다." % slug)


def cuts_for(slug):
    """Step numbers to cut the recording after. Empty means one recording frame."""
    return list(_lesson(slug)["demoCuts"])


def episodes_for(slug):
    """Compatibility API: one complete lesson playlist in current delivery mode."""
    return [{**e, 'frames': list(e['frames'])} for e in _lesson(slug)["episodes"]]


def frames_for(slug):
    """Every frame the lesson's episodes claim, in order."""
    return [f for e in _lesson(slug)["episodes"] for f in e["frames"]]


def slugs():
    return sorted(_DOC["lessons"])
