"""Derive a publishable scene-timing file from a private narration transcript.

The transcript carries the spoken text of a private recording and stays private.
This script reads it only to learn *when* things were said, aligns that against
the public SCRIPT.md, and writes a numbers-only derivative: frame identifiers,
start and end seconds, drift against the planned window, and recording-cue times.
No spoken text is ever copied into the output.

Alignment is character-level rather than word-level because the recogniser and
the script disagree about Korean word spacing, and because canonical identifiers
such as EDU-SB-01 or REFERENCE_READONLY cannot be recovered from audio at all.
The script supplies the words; the recording supplies only the clock.

Usage:
    python scripts/narration/align.py <lesson-dir> <transcript-json> <output-json>
"""

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher

FRAME_HEADING = re.compile(r"^##\s+Line\s+(\d+)\s*[—\-–]\s*(.*?)\s*\(Frame\s+(\d+)\)\s*$")
TIME_LINE = re.compile(r"^\*\*Time:\*\*\s*(\d{1,2}):(\d{2})\s*[–—\-]\s*(\d{1,2}):(\d{2})")
NARRATION_LINE = re.compile(r"^\s{4}\S")
DEMO_MENTION = re.compile(r"\bDEMO-(\d{2})\b")
# A paragraph opening with a bracketed number is a beat, and the composition
# cues that item at its start. See scripts/part/beats.py.
BEAT_MARKER = re.compile(r"^\((\d+)")
KEEP_CHARS = re.compile(r"[^0-9A-Za-z가-힣]")


def normalize(text):
    """Reduce text to comparable characters: Hangul syllables, Latin, digits."""
    return KEEP_CHARS.sub("", text).upper()


def parse_script(script_path):
    """Return the ordered narration blocks declared by SCRIPT.md."""
    with open(script_path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    frames = []
    current = None
    for raw in lines:
        heading = FRAME_HEADING.match(raw)
        if heading:
            if current:
                frames.append(current)
            current = {
                "line": int(heading.group(1)),
                "frame": int(heading.group(3)),
                "title": heading.group(2),
                "plannedStart": None,
                "plannedEnd": None,
                "paragraphs": [],
                "beats": [],
            }
            continue
        if current is None:
            continue
        timing = TIME_LINE.match(raw)
        if timing:
            current["plannedStart"] = int(timing.group(1)) * 60 + int(timing.group(2))
            current["plannedEnd"] = int(timing.group(3)) * 60 + int(timing.group(4))
            continue
        if NARRATION_LINE.match(raw):
            para = raw.strip()
            if para.startswith(">"):
                continue
            current["paragraphs"].append(para)
            beat = BEAT_MARKER.match(para)
            current["beats"].append(int(beat.group(1)) if beat else None)
    if current:
        frames.append(current)

    frames = [frame for frame in frames if frame["paragraphs"]]
    for frame in frames:
        frame["text"] = " ".join(frame["paragraphs"])
    return frames


def frame_ids(lesson_dir):
    """Map frame ordinals to composition file stems."""
    frames_dir = os.path.join(lesson_dir, "compositions", "frames")
    names = sorted(
        name for name in os.listdir(frames_dir) if name.endswith(".html")
    )
    return [os.path.splitext(name)[0] for name in names]


def flatten_words(transcript):
    words = []
    for segment in transcript["segments"]:
        for word in segment["words"]:
            words.append(word)
    return words


def build_streams(frames, words):
    """Build parallel character streams tagged with their source index."""
    script_chars = []
    script_owner = []
    for index, frame in enumerate(frames):
        normalized = normalize(frame["text"])
        script_chars.append(normalized)
        script_owner.extend([index] * len(normalized))

    asr_chars = []
    asr_owner = []
    for index, word in enumerate(words):
        normalized = normalize(word["word"])
        asr_chars.append(normalized)
        asr_owner.extend([index] * len(normalized))

    return "".join(script_chars), script_owner, "".join(asr_chars), asr_owner


def align(script_text, asr_text):
    """Return script-char index -> asr-char index for every matched position."""
    matcher = SequenceMatcher(None, script_text, asr_text, autojunk=False)
    mapping = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            mapping[block.a + offset] = block.b + offset
    return mapping


def frame_bounds(frames, script_owner, mapping, asr_owner, words):
    """Resolve each frame's first and last aligned word."""
    per_frame = {index: [] for index in range(len(frames))}
    for script_index, asr_index in mapping.items():
        per_frame[script_owner[script_index]].append(asr_index)

    bounds = []
    for index in range(len(frames)):
        matched = per_frame[index]
        if not matched:
            bounds.append(None)
            continue
        first_word = words[asr_owner[min(matched)]]
        last_word = words[asr_owner[max(matched)]]
        bounds.append(
            {
                "observedStart": first_word["start"],
                "observedEnd": last_word["end"],
                "matchedChars": len(matched),
            }
        )
    return bounds


def beat_times(frames, mapping, asr_owner, words):
    """Measured start and end for each numbered paragraph.

    Built on a second character stream tagged by paragraph rather than by
    frame, so a beat can be located inside the frame that contains it.
    """
    para_owner, offset_of = [], []
    for f_index, frame in enumerate(frames):
        for p_index, para in enumerate(frame["paragraphs"]):
            offset_of.append((f_index, p_index))
            para_owner.extend([len(offset_of) - 1] * len(normalize(para)))

    per_para = {}
    for script_index, asr_index in mapping.items():
        if script_index < len(para_owner):
            per_para.setdefault(para_owner[script_index], []).append(asr_index)

    out = []
    for slot, (f_index, p_index) in enumerate(offset_of):
        beat = frames[f_index]["beats"][p_index]
        if beat is None:
            continue
        matched = per_para.get(slot)
        if not matched:
            continue
        out.append({
            "frame": frames[f_index]["frame"],
            "beat": beat,
            "observedStart": round(words[asr_owner[min(matched)]]["start"], 3),
            "observedEnd": round(words[asr_owner[max(matched)]]["end"], 3),
            "matchedChars": len(matched),
        })
    return out


def cue_times(frames, script_owner, mapping, asr_owner, words):
    """Locate each DEMO cue mentioned in the script on the measured clock."""
    cues = []
    offset = 0
    for index, frame in enumerate(frames):
        normalized_length = len(normalize(frame["text"]))
        for mention in DEMO_MENTION.finditer(frame["text"]):
            prefix = normalize(frame["text"][: mention.start()])
            script_index = offset + len(prefix)
            candidates = [
                mapping[candidate]
                for candidate in range(script_index, min(script_index + 40, offset + normalized_length))
                if candidate in mapping
            ]
            if not candidates:
                continue
            cues.append(
                {
                    "demoId": f"DEMO-{mention.group(1)}",
                    "frame": frame["frame"],
                    "at": round(words[asr_owner[min(candidates)]]["start"], 3),
                }
            )
        offset += normalized_length
    return cues


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", help="lesson project directory")
    parser.add_argument("transcript", help="private word-level transcript JSON")
    parser.add_argument("output", help="path to write narration-timing.json")
    parser.add_argument(
        "--min-ratio",
        type=float,
        default=0.7,
        help="fail when the aligned character ratio falls below this value",
    )
    args = parser.parse_args(argv)

    with open(args.transcript, encoding="utf-8") as handle:
        transcript = json.load(handle)

    frames = parse_script(os.path.join(args.lesson, "SCRIPT.md"))
    ids = frame_ids(args.lesson)
    if len(frames) != len(ids):
        raise SystemExit(
            f"SCRIPT.md declares {len(frames)} narration blocks but the project has {len(ids)} frames"
        )

    words = flatten_words(transcript)
    if not words:
        raise SystemExit("transcript contains no word timestamps; rerun with word_timestamps enabled")

    script_text, script_owner, asr_text, asr_owner = build_streams(frames, words)
    mapping = align(script_text, asr_text)
    bounds = frame_bounds(frames, script_owner, mapping, asr_owner, words)

    unresolved = [frames[i]["frame"] for i, bound in enumerate(bounds) if bound is None]
    if unresolved:
        raise SystemExit(f"no narration could be aligned for frame(s): {unresolved}")

    audio_seconds = float(transcript["audioSeconds"])

    # Tile the measured starts so the frame durations sum to the audio length
    # exactly. The course guard compares per-frame durations across storyboard,
    # HTML, and motion, so a gap between frames must belong to one of them.
    starts = [0.0] + [bounds[i]["observedStart"] for i in range(1, len(bounds))]
    ends = starts[1:] + [audio_seconds]

    entries = []
    for index, frame in enumerate(frames):
        duration = round(ends[index] - starts[index], 3)
        planned = frame["plannedEnd"] - frame["plannedStart"]
        script_chars = len(normalize(frame["text"]))
        matched_chars = bounds[index]["matchedChars"]
        entries.append(
            {
                "frame": frame["frame"],
                "id": ids[index],
                "start": round(starts[index], 3),
                "end": round(ends[index], 3),
                "duration": duration,
                "plannedDuration": planned,
                "driftSeconds": round(duration - planned, 3),
                "matchedChars": matched_chars,
                "scriptChars": script_chars,
                # A frame dense in Latin identifiers aligns less tightly, because
                # the recogniser renders them differently every time. The boundary
                # is still anchored by the surrounding prose; the sync gate should
                # weigh a low ratio rather than treat it as a failure.
                "matchedRatio": round(matched_chars / script_chars, 4) if script_chars else 0.0,
            }
        )

    matched_total = sum(entry["matchedChars"] for entry in entries)
    script_total = sum(entry["scriptChars"] for entry in entries)
    matched_ratio = round(matched_total / script_total, 4) if script_total else 0.0

    result = {
        "schemaVersion": 1,
        "lesson": os.path.basename(os.path.normpath(args.lesson)),
        "source": transcript.get("model", "unknown"),
        "audioSeconds": round(audio_seconds, 3),
        "plannedSeconds": sum(entry["plannedDuration"] for entry in entries),
        "alignment": {
            "scriptChars": script_total,
            "matchedChars": matched_total,
            "matchedRatio": matched_ratio,
        },
        "frames": entries,
        "cues": cue_times(frames, script_owner, mapping, asr_owner, words),
        "beats": beat_times(frames, mapping, asr_owner, words),
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)

    print(f"lesson         : {result['lesson']}")
    print(f"frames         : {len(entries)}")
    print(f"audio seconds  : {result['audioSeconds']}  (planned {result['plannedSeconds']})")
    print(f"matched ratio  : {matched_ratio}")
    print(f"cues           : {len(result['cues'])}")
    print(f"written        : {args.output}")

    if matched_ratio < args.min_ratio:
        print(
            f"FAILED: aligned character ratio {matched_ratio} is below {args.min_ratio}. "
            "The recording and SCRIPT.md have diverged; re-read the script or update it.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
