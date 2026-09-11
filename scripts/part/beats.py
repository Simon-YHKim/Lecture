"""Narration-derived timing for lesson compositions.

Hand-picked stagger numbers drift out of sync with the script the moment a
paragraph is rewritten, and nothing complains. These functions read SCRIPT.md
itself, so the narration is the single source of truth for *when* things move as
well as for what is said.

A script Line is split into segments. A paragraph that opens with a bracketed
number — "(1번 카드)", "(3행)", "(2 도면선)" — is a beat and belongs to the
matching on-screen item. A paragraph without one is a gap: the narrator is
talking about the screen as a whole, so nothing is emphasised.

Every emitted animation is a tween, never a callback. GSAP records tweens in the
timeline, so scrubbing backwards in Studio unwinds them; a callback only fires
when time moves forward past it and leaves the frame stuck in a later state.
"""

import json
import math
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import speech  # noqa: E402

# How long the words take is measured, not assumed — see speech.py. What is
# left here is what happens around them on screen.
#
# There is no gap between paragraphs any more. There used to be, because the
# old estimate ended on the last syllable and something had to stand in for the
# breath. The measured model already includes a paragraph's own edges, so a gap
# on top would be the same silence counted twice.
GAP_SEC = 0.0
LEAD_SEC = 1.6          # header lands before the first beat
TAIL_SEC = 1.2          # the frame does not cut on the last syllable
MIN_BEAT_SEC = 1.2      # a card has to be readable, however briefly it is named

# The recording runs longer than its narration: typing, dialog boxes and mouse
# work are not spoken. This is the one timing number still not measured — the
# first real recording replaces it, since ingest reads the file's own length.
DEMO_FACTOR = 1.3

# Read-along states. The contrast is deliberately mild — the ask was for
# emphasis that reads as natural, not a spotlight.
UNREAD, READ, ACTIVE = 0.34, 0.64, 1.0
FADE = 0.8              # state change duration
EASE = "power2.inOut"

ACCENT = "#C7004C"
INK = "#111"
ROW_BG = "#F5F5F3"
CARD_BG = "#FDFAFB"
LINE = "#A4A3A4"

_BEAT = re.compile(r"^\((\d+)")
_LINE_HEAD = re.compile(r"^##+\s*Line\s+(\d+)")
# 녹화 Line 의 단계 제목. 국문은 「### 3단계」, 영문은 「### Step 3」 이다.
_STEP_HEAD = re.compile(r"^###\s+(?:Step\s+)?(\d+)(?:단계)?\b")


def syllables(text):
    """Rough spoken length. Hangul blocks dominate; digits and latin get their
    own weight because they are read out as words, not skipped."""
    n = 0
    for tok in re.findall(r"[가-힣]|[0-9]|[A-Za-z]+", text):
        if tok.isdigit():
            n += 1
        elif tok.isascii() and tok.isalpha():
            n += max(2, len(tok) // 2)      # "acadiso" reads longer than "REC"
        elif unicodedata.category(tok) == "Lo":
            n += 1
    return n


def read_seconds(text):
    """Seconds to say this paragraph, from the measured model in speech.py."""
    return speech.read_seconds(text)


# --------------------------------------------------------------- parsing
def _paragraphs(block):
    out, cur = [], []
    for raw in block:
        if raw.strip() == "":
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        if raw.startswith("    ") or raw.startswith("\t"):
            cur.append(raw.strip())
    if cur:
        out.append(" ".join(cur))
    return out


def parse_script(path):
    """{line_number: [(beat_index_or_None, text), ...]} in reading order."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    sections, cur_no, buf = {}, None, []
    for raw in lines:
        m = _LINE_HEAD.match(raw)
        if m:
            if cur_no is not None:
                sections[cur_no] = buf
            cur_no, buf = int(m.group(1)), []
            continue
        if cur_no is not None:
            buf.append(raw)
    if cur_no is not None:
        sections[cur_no] = buf

    out = {}
    for no, block in sections.items():
        segs = []
        for para in _paragraphs(block):
            if para.startswith(">"):
                continue
            m = _BEAT.match(para)
            segs.append((int(m.group(1)) if m else None, para))
        out[no] = segs
    return out


def parse_steps(path, line_no):
    """The recording Line is written as '### N단계' headings, not paragraphs."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    inside, cur, out = False, None, []
    for raw in lines:
        m = _LINE_HEAD.match(raw)
        if m:
            inside = int(m.group(1)) == line_no
            continue
        if not inside:
            continue
        s = _STEP_HEAD.match(raw)
        if s:
            cur = [int(s.group(1)), ""]
            out.append(cur)
            continue
        if cur is not None and (raw.startswith("    ") or raw.startswith("\t")):
            cur[1] += " " + raw.strip()
    return [(i, t.strip()) for i, t in out]


# --------------------------------------------------------------- planning
def plan(segments, duration=None, lead=LEAD_SEC, tail=TAIL_SEC):
    """Lay segments out in time.

    Returns (spans, duration). spans is [(beat_or_None, start, end), ...].
    With duration=None the frame is as long as the narration needs; with a
    duration given, the segments are scaled to fill it so a fixed-length frame
    (a screen recording) still tracks the script's proportions.
    """
    raw = [max(read_seconds(t), MIN_BEAT_SEC) + GAP_SEC for _, t in segments]
    need = sum(raw)
    if duration is None:
        duration = math.ceil(need + lead + tail)
    span = max(duration - lead - tail, 1.0)
    k = span / need if need else 1.0

    spans, t = [], lead
    for (idx, _), r in zip(segments, raw):
        d = r * k
        spans.append((idx, round(t, 2), round(t + d, 2)))
        t += d
    return spans, duration


def beat_spans(spans):
    """Only the segments that map to an on-screen item, in beat order."""
    return [(i, a, b) for i, a, b in spans if i is not None]


def load_measured(lesson_dir):
    """Measured beat times from a recorded and aligned narration, if any.

    Returns {frame_number: {beat: (start, end)}}. Until a recording exists the
    syllable estimate is the best available answer; once one does, the estimate
    stops being an answer at all.
    """
    path = os.path.join(lesson_dir, "narration-timing.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    out = {}
    for b in doc.get("beats", []):
        out.setdefault(b["frame"], {})[b["beat"]] = (b["observedStart"], b["observedEnd"])
    return out


def measured_plan(segments, frame_beats, frame_start, frame_end):
    """Lay segments out on the measured clock.

    Beats sit where they were actually spoken. A gap paragraph has no marker to
    align on, so it fills the space between its neighbours; that is a gap's job
    anyway — nothing is emphasised during one.
    """
    known = {}
    for i, (idx, _t) in enumerate(segments):
        if idx is not None and idx in frame_beats:
            a, b = frame_beats[idx]
            known[i] = (round(a - frame_start, 2), round(b - frame_start, 2))
    if not known:
        return None

    span = round(frame_end - frame_start, 2)

    # A run of gap paragraphs between two measured beats has to *share* the
    # space between them. Giving each one the next beat's start and then
    # padding it to a minimum walks the next beat forward by 0.8s a paragraph,
    # so the guard then asks for motion where nobody is speaking yet. Lesson 2's
    # recap lost 2.4 seconds that way and reported a beat with no motion on it.
    n = len(segments)
    starts = [None] * n
    ends = [None] * n
    for i in known:
        starts[i], ends[i] = known[i]

    i = 0
    prev_end = 0.0
    while i < n:
        if starts[i] is not None:
            prev_end = ends[i]
            i += 1
            continue
        j = i
        while j < n and starts[j] is None:
            j += 1
        lo = prev_end
        hi = starts[j] if j < n else span
        gap = max(hi - lo, 0.0)
        step = gap / (j - i) if j > i else 0.0
        for k in range(i, j):
            starts[k] = round(lo + step * (k - i), 2)
            ends[k] = round(lo + step * (k - i + 1), 2)
        prev_end = ends[j - 1]
        i = j

    spans, prev_end = [], 0.0
    for i, (idx, _t) in enumerate(segments):
        a = max(starts[i], prev_end)
        b = max(ends[i], a + 0.05)
        spans.append((idx, round(a, 2), round(b, 2)))
        prev_end = b
    return spans


# --------------------------------------------------------------- emitting
def _sel(comp, s):
    return "#%s %s" % (comp, s)


_TINT = {
    # color drives the card's icon through currentColor, so the mark lights with
    # the words instead of needing its own tween.
    "card": ("borderColor:'%s',backgroundColor:'%s',color:'%s'" % (ACCENT, CARD_BG, ACCENT),
             "borderColor:'%s',backgroundColor:'#FFF',color:'%s'" % (LINE, INK)),
    "row": ("backgroundColor:'%s'" % ROW_BG, "backgroundColor:'#FFF'"),
    "plain": ("", ""),
}


def item(sel, kind="card", mode="present", hold=False, dx=0, dy=None, read=None):
    """One on-screen item and how it should behave.

    mode "present": on screen from the start. The viewer takes in the
    whole screen at once and the emphasis alone carries the narration. Right for
    dense reference tables, whose text stays opaque while the background carries
    emphasis. Other items retain the faint unread/read states.

    mode "reveal": arrives when the narrator reaches it. Right where the items
    are few and large, so the screen does not open cluttered.

    hold: stay lit after its beat instead of receding. Right for a construction
    sequence — a sheet border that is drawn does not become less true later.

    read: opacity once its beat has passed. The default keeps the item legible
    alongside the others. Panels stacked in one box must use 0 instead, or every
    one that has been read stays piled on top of the current one.
    """
    return {"sel": sel, "kind": kind, "mode": mode, "hold": hold,
            "dx": dx, "dy": 22 if dy is None else dy,
            "read": (1 if kind == "row" else READ) if read is None else read}


def read_along(comp, items, spans, entrance=0.95, group_stagger=0.10, overview_at=None,
               unread=UNREAD):
    """Three-state read-along: unread -> active while spoken -> read.

    Items are 1-based by beat index. A beat with no matching item is skipped
    rather than silently shifting every later item onto the wrong words.
    """
    items = [item(s) if isinstance(s, str) else s for s in items]
    out = []
    rows = [_sel(comp, it['sel']) for it in items if it['kind'] == 'row']
    if rows:
        # A transparent-black endpoint darkens the row during color interpolation.
        out.append('    gsap.set("%s",{backgroundColor:"#FFF"});' % ','.join(rows))

    present = [it for it in items if it["mode"] == "present"]
    if present:
        # Arrive just before the narrator reaches the first of them. A frame
        # whose script opens with half a minute of framing should spend that
        # time on the framing, not on a grid of faint cards nobody is discussing
        # yet.
        first = min((a for _, a, _ in beat_spans(spans)), default=LEAD_SEC)
        at = max(round(LEAD_SEC * 0.4, 2), round(first - 2.4, 2))
        if overview_at is not None:
            at = max(0, overview_at)
        # Split only consecutive runs, preserving each item's original stagger
        # index. Collecting all notes into a new group at `at` would reveal them
        # before the preceding table rows.
        runs = []
        for index, it in enumerate(present):
            opaque = it["kind"] == "row"
            if runs and runs[-1][0] == opaque:
                runs[-1][2].append(it["sel"])
            else:
                runs.append((opaque, index, [it["sel"]]))
        for opaque, index, selectors in runs:
            start = at if index == 0 else round(at + index * group_stagger, 10)
            out.append('    tl.fromTo("%s",{opacity:0,y:14},{opacity:%s,y:0,duration:%s,'
                       'stagger:%s,ease:"power2.out"},%s);'
                       % (",".join(_sel(comp, s) for s in selectors), 1 if opaque else unread,
                          entrance, group_stagger, start))

    for idx, a, b in beat_spans(spans):
        if idx < 1 or idx > len(items):
            continue
        it = items[idx - 1]
        if not it["sel"]:
            continue
        s = _sel(comp, it["sel"])
        hot, cool = _TINT[it["kind"]]
        hot = (hot + ",") if hot else ""
        cool = (cool + ",") if cool else ""
        stacked = it['mode'] == 'reveal' and it['read'] == 0
        if it["mode"] == "reveal":
            out.append('    tl.fromTo("%s",{opacity:0,x:%s,y:%s},{opacity:%s,%sx:0,y:0,'
                       'duration:%s,ease:"power3.out"},%s);'
                       % (s, it["dx"], it["dy"], ACTIVE, hot, .25 if stacked else entrance + 0.15, a))
        else:
            out.append('    tl.to("%s",{opacity:%s,%sduration:%s,ease:"%s"},%s);'
                       % (s, ACTIVE, hot, FADE, EASE, a))
        if not it["hold"]:
            out.append('    tl.to("%s",{opacity:%s,%sduration:%s,ease:"%s"},%s);'
                       % (s, it["read"], cool, .18 if stacked else FADE, EASE,
                          round(max(a, b - .2), 2) if stacked else b))
        elif hot:
            out.append('    tl.to("%s",{%sduration:%s,ease:"%s"},%s);'
                       % (s, cool, FADE, EASE, b))
    return "\n".join(out)


def attr_highlight(comp, attr, values, spans, lead=0.2, fade=0.7):
    """Light the drawing where the narrator is pointing.

    attr is "feature" for a machined surface or "dim" for a single dimension.
    values[i] is what beat i+1 points at — one id or several.

    Tweened, not class-toggled. A class added from a timeline callback survives
    a backwards scrub, so the frame ends up with every feature lit at once; a
    tween unwinds. Overlay paths already carry the accent and only their opacity
    moves, because a stroke of `none` has nothing to interpolate towards.
    """
    out = []
    for idx, a, b in beat_spans(spans):
        if idx < 1 or idx > len(values):
            continue
        v = values[idx - 1]
        if not v:
            continue
        ids = [v] if isinstance(v, str) else list(v)
        # Single quotes inside: the selector is interpolated into a
        # double-quoted JS string literal, so a double-quoted attribute value
        # closes it and the whole timeline fails to parse.
        stroke = ",".join("#%s [data-%s='%s']:not(.hl):not(.arrow):not(text)" % (comp, attr, i)
                          for i in ids)
        fill = ",".join("#%s .arrow[data-%s='%s'],#%s text[data-%s='%s']"
                        % (comp, attr, i, comp, attr, i) for i in ids)
        over = ",".join("#%s .hl[data-%s='%s']" % (comp, attr, i) for i in ids)
        for sel, prop, on, off in ((stroke, "stroke", "'%s'" % ACCENT, "'%s'" % INK),
                                   (fill, "fill", "'%s'" % ACCENT, "'%s'" % INK),
                                   (over, "opacity", 1, 0)):
            # Some features consist only of an overlay, others only of lines;
            # no geometry kind is mandatory for every feature.
            out.append('    if(document.querySelectorAll("%s").length){' % sel)
            out.append('    tl.to("%s",{%s:%s,duration:%s,ease:"%s"},%s); // narration-beat: %d on'
                       % (sel, prop, on, fade, EASE, round(a + lead, 2), idx))
            out.append('    tl.to("%s",{%s:%s,duration:%s,ease:"%s"},%s); // narration-beat: %d off'
                       % (sel, prop, off, fade, EASE, round(b, 2), idx))
            out.append('    }')
    return "\n".join(out)


def feature_highlight(comp, features, spans, lead=0.2):
    return attr_highlight(comp, "feature", features, spans, lead)


def dim_highlight(comp, dims, spans, lead=0.2):
    return attr_highlight(comp, "dim", dims, spans, lead)


# 단계 띠에 뜨는 단축키. 대본은 낭독용이라 한글로 적지만(「컨트롤 일」), 화면은
# 키보드에 적힌 대로 `Ctrl+1` 을 보여야 한다. 읽을 때만 한글을 알아본다.
_KEY_ALIAS = {'컨트롤 에스': 'Ctrl+S', '컨트롤 일': 'Ctrl+1', '컨트롤 에이': 'Ctrl+A',
              '컨트롤 지': 'Ctrl+Z', '컨트롤 오': 'Ctrl+O'}
_KEYS = re.compile(r"Ctrl\+[A-Za-z0-9]+|\bF(?:[3-9]|1[0-2])\b|"
                   + "|".join(sorted(_KEY_ALIAS, key=len, reverse=True)))

_TICK = re.compile(r"`([A-Za-z][A-Za-z0-9]{0,31})`")
_FILLET_COMMAND = re.compile(r'\bFILLET\b|모깎기|필렛\s*명령', re.I)
_FILLET_OPTION = re.compile(
    r'(?:필렛|모깎기|fillet)\s*(?:옵션|option)|첫(?:\s*번째)?\s*(?:구석|모서리)', re.I)
_COMMAND_OPTIONS = {
    'F': _FILLET_OPTION,
    # 영문판은 같은 자리를 「current layer」「first distance」라고 부른다. 국문 표현만
    # 알아보면 영문 대본에서 OFFSET 의 도면층 옵션 C 가 CIRCLE 명령으로 세어진다.
    'C': re.compile(r'(?:모따기|chamfer)\s*(?:옵션|option)|첫\s*거리|둘째\s*거리|'
                    r'(?:first|second)\s*distance|'
                    r'닫(?:기|습|으|아)|\bclose\b|현재\s*(?:레이어|도면층)|current\s*layer|'
                    r'원본으로.{0,30}현재로', re.I),
    'L': re.compile(r'(?:도면층|레이어|layer)\s*(?:옵션|option)', re.I),
}
_COMMAND_CLAUSE_END = re.compile(r'[.!?;\n]')


def _command_token_context(text, token):
    # parse_steps joins source lines. Bound each occurrence by prose clauses
    # so an option cannot suppress a later command with the same shortcut.
    start = max(text.rfind(c, 0, token.start()) for c in '.!?;\n') + 1
    stop = _COMMAND_CLAUSE_END.search(text, token.end())
    end = stop.end() if stop else len(text)
    context = text[start:end]
    following_stop = _COMMAND_CLAUSE_END.search(text, end)
    following = text[end:following_stop.end() if following_stop else len(text)]
    # A command/option explanation often follows "C, Enter." in its own sentence.
    # Never borrow another typed command's explanation.
    if not _TICK.search(following):
        context += following
    return context


def shortcuts_in(path, line_no):
    """The commands a lesson's recording actually types, in first-use order.

    Read from the script rather than listed per lesson, so the summary table
    cannot claim a command the demo never uses — or miss one it does. Option
    letters typed inside a running command are filtered out; anything left that
    the command table does not know stops the build, because a silent gap in
    that table is exactly what nobody would notice.
    """
    import lesson_kit as kit

    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    inside, seen, unknown = False, [], []
    for row_index, raw in enumerate(lines):
        m = _LINE_HEAD.match(raw)
        if m:
            inside = int(m.group(1)) == line_no
            continue
        if not inside:
            continue
        for token in _TICK.finditer(raw):
            key = token.group(1).upper()
            if key in kit.NOT_COMMANDS or key in seen:
                continue
            if key in _COMMAND_OPTIONS:
                prose = raw
                if row_index + 1 < len(lines) and lines[row_index + 1].startswith(('    ', '\t')):
                    prose += ' ' + lines[row_index + 1].strip()
                context = _command_token_context(prose, token)
                if _COMMAND_OPTIONS[key].search(context):
                    continue
            # RECTANG also accepts F while it is asking for the first corner.
            # Like D/M below, require the actual command to be introduced.
            if key == "F":
                if not _FILLET_COMMAND.search(context):
                    continue
            # Some letters are a command in one lesson and an option inside a
            # running command in another. `D` starts DIMSTYLE in lesson 7 and
            # answers CIRCLE's radius prompt in lessons 3 and 4 — counted as
            # DIMSTYLE everywhere, the summary claimed a command the recording
            # never ran. The step says which it is: a command is introduced by
            # name, an option is not.
            if key in kit.AMBIGUOUS_KEYS:
                if (kit.COMMANDS.get(key, ("",))[0] in raw
                        or (key == "M" and "이동 명령" in raw)):
                    seen.append(key)
                continue
            if key in kit.OPTION_KEYS:
                continue
            if key in kit.COMMANDS:
                seen.append(key)
            elif key not in unknown:
                unknown.append(key)
    if unknown:
        raise SystemExit(
            "%s Line %d 이 쓰는 명령이 lesson_kit.COMMANDS 에 없다: %s\n"
            "표에 넣거나, 명령이 아니면 OPTION_KEYS 에 넣어라."
            % (path, line_no, ", ".join(unknown)))
    return seen


def step_keys(path, line_no):
    """What each recording step types, one entry per step.

    Read from the step's own text rather than assigned by hand, so a checklist
    row cannot show a command that step does not use. Steps that only look at
    something return an empty string.
    """
    import lesson_kit as kit

    out = []
    for _no, text in parse_steps(path, line_no):
        found = []
        for token in _TICK.finditer(text):
            key = token.group(1).upper()
            if key in _COMMAND_OPTIONS and _COMMAND_OPTIONS[key].search(_command_token_context(text, token)):
                continue
            if key in kit.AMBIGUOUS_KEYS:
                if not (kit.COMMANDS.get(key, ("",))[0] in text
                        or (key == "M" and "이동 명령" in text)):
                    continue
            if key in kit.OPTION_KEYS:
                continue
            if key in kit.COMMANDS and key not in found:
                found.append(key)
        fk = [_KEY_ALIAS.get(k, k) for k in _KEYS.findall(text)]
        for k in fk:
            if k not in found:
                found.append(k)
        out.append(" · ".join(found[:2]))
    return out


def segment_at(spans, i):
    """Start of the i-th segment counting gaps, so an element that illustrates a
    framing paragraph can be cued to that paragraph instead of to t=0."""
    return spans[i][1] if 0 <= i < len(spans) else LEAD_SEC


def cue(comp, sel, at, dy=14, dur=0.9, ease="power3.out"):
    return ('    tl.fromTo("#%s %s",{opacity:0,y:%s},{opacity:1,y:0,duration:%s,ease:"%s"},%s);'
            % (comp, sel, dy, dur, ease, round(at, 2)))


def closing_note(comp, spans, sel=".note", dy=12):
    """Keep a supplementary note with the final measured narration paragraph."""
    index, start, _end = beat_spans(spans)[-1]
    return cue(comp, sel, start, dy=dy) + ' // narration-beat: %d on' % index


def closing_note_assertion(comp, spans, sel=".note"):
    _index, start, _end = beat_spans(spans)[-1]
    return {"kind": "appearsBy", "selector": _sel(comp, sel), "bySec": round(start + 1.0, 2)}


def outro(comp, duration, sels=(".topline", ".body"), fade=0.9):
    """Every frame ended on a hard cut with nothing leaving. Appearances with no
    departures read as the screen piling up and then snapping."""
    q = ",".join(_sel(comp, s) for s in sels)
    return ('    tl.to("%s",{opacity:0,y:-12,duration:%s,ease:"power2.in"},%s);'
            % (q, fade, round(max(duration - fade - 0.15, 0.1), 2)))


def assertions(comp, items, spans, head="h1", extra=()):
    """Assertions derived from the same plan that drives the motion.

    The old set only ever looked at the header and at containers that had no
    tween at all, so it passed whatever the content did. These pin the items the
    narrator actually walks through, which is what regresses when a script
    paragraph is rewritten and the frame is not rebuilt.
    """
    out = [{"kind": "appearsBy", "selector": "#%s %s" % (comp, head), "bySec": 3}]
    items = [item(s) if isinstance(s, str) else s for s in items]
    prev = None
    for idx, a, _b in beat_spans(spans):
        if idx < 1 or idx > len(items):
            continue
        it = items[idx - 1]
        if not it["sel"] or it["mode"] != "reveal":
            continue
        sel = _sel(comp, it["sel"])
        out.append({"kind": "appearsBy", "selector": sel, "bySec": round(a + 3.0, 1)})
        if prev:
            out.append({"kind": "before", "a": prev, "b": sel})
        prev = sel
    out.append({"kind": "staysInFrame", "selector": "#%s .body" % comp})
    return out + list(extra)


def chrome(comp, drawing=None):
    """The header and the panel frame. These may be quick — they are furniture,
    not content, and the viewer should not wait on them."""
    out = ['    tl.fromTo("#%s .topline",{opacity:0,y:-22},'
           '{opacity:1,y:0,duration:.7,ease:"power3.out"},.25);' % comp]
    if drawing:
        out.append('    tl.fromTo("#%s .panel",{opacity:0,x:%s},'
                   '{opacity:1,x:0,duration:.85,ease:"power3.out"},.75);' % (comp, drawing))
    return "\n".join(out)


def note(comp, at, sel=".note"):
    return ('    tl.fromTo("#%s %s",{opacity:0,y:12},'
            '{opacity:1,y:0,duration:.8,ease:"power2.out"},%s);' % (comp, sel, at))


def audit(items, spans, duration, max_tail=9.0, min_beat=1.5):
    """Build-time checks the runtime assertions cannot express.

    motion.json can only say "appears by", "before" and "stays in frame", so a
    beat pointing at an item that does not exist, or a frame that freezes for
    half a minute after its last cue, passes it silently. These run while the
    plan is still in hand.
    """
    items = [item(s) if isinstance(s, str) else s for s in items]
    bs = beat_spans(spans)
    seen = [i for i, _, _ in bs]
    bad = []
    for i in seen:
        if i < 1 or i > len(items):
            bad.append("비트 %d 에 대응하는 항목이 없다 (항목 %d개)" % (i, len(items)))
    orphan = [i for i in range(1, len(items) + 1) if i not in seen]
    if orphan:
        bad.append("항목 %s 를 읽는 대본 비트가 없다" % orphan)
    for i, a, b in bs:
        if b - a < min_beat:
            bad.append("비트 %d 가 %.1f초로 너무 짧다" % (i, b - a))
    if spans:
        tail = duration - spans[-1][2]
        if tail > max_tail:
            bad.append("마지막 모션 뒤 정지 %.1f초 (상한 %.1f)" % (tail, max_tail))
    return bad


def stamp_times(path, ranges, total):
    """Write the computed timecodes back into SCRIPT.md.

    The Time lines used to be hand-written, and the frame durations were then
    transcribed from them — so the script "confirmed" numbers it had supplied.
    Now the words decide the length and the timecodes are derived from that, in
    one direction only.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    def clock(t):
        return "%d:%02d" % (int(t) // 60, int(t) % 60)

    want = sum(1 for raw in lines if raw.startswith("**Time:**"))
    if want != len(ranges):
        raise SystemExit(
            "%s: Time 줄 %d개인데 프레임 구간은 %d개다. 하나가 조용히 버려진다."
            % (path, want, len(ranges)))

    out, i, no = [], 0, 0
    for raw in lines:
        if raw.startswith("**Time:**"):
            a, b = ranges[no]
            note = raw.split("(", 1)[1].rsplit(")", 1)[0] if "(" in raw else None
            out.append("**Time:** %s–%s%s" % (clock(a), clock(b),
                                              " (%s)" % note if note else ""))
            no += 1
            continue
        if raw.startswith("> 목표 길이"):
            out.append("> 목표 길이 %d분 %02d초 — `SCRIPT.md` 에서 계산된 값입니다. "
                       "실제 음성이 들어오면 단어 타임코드가 최종 기준이 됩니다."
                       % (total // 60, total % 60))
            continue
        out.append(raw)
    del i
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    return no



def split_steps(steps, cuts):
    """Slice the recording's steps at `cuts`, renumbering each slice from 1.

    `cuts` are step numbers to cut *after*, so [6, 14] gives 1–6, 7–14, 15–end.
    Each slice is renumbered because read_along, assertions and audit all index
    beats by position within their frame. The absolute number stays available
    as the returned offset, which is what the strip on screen shows — a learner
    watching part two should see 07 / 16, not 01 / 10.
    """
    bounds = list(cuts) + [len(steps)]
    out, prev = [], 0
    for c in bounds:
        piece = steps[prev:c]
        if not piece:
            raise ValueError("빈 조각이 생기는 컷: %r" % (cuts,))
        out.append((prev, [(i, t) for i, (_n, t) in enumerate(piece, 1)]))
        prev = c
    if prev != len(steps):
        raise ValueError("컷이 단계 수를 넘는다: %r" % (cuts,))
    return out


def split_lengths(total, weights):
    """Divide `total` by weight so the pieces sum to exactly `total`.

    Cumulative rounding, not per-piece: rounding each share on its own leaves a
    remainder, and verify_course recomputes this same division and compares.
    """
    s = float(sum(weights)) or 1.0
    out, acc, run = [], 0.0, 0
    for w in weights:
        acc += w
        cut = int(round(total * acc / s))
        out.append(cut - run)
        run = cut
    return out

def report(name, spans, duration):
    n = len(beat_spans(spans))
    return "  %-26s %6.1fs  비트 %2d개  마지막 %5.1fs" % (
        name, duration, n, spans[-1][2] if spans else 0.0)
