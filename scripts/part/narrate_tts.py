"""Speak the course's narration with the Windows Korean voice, and time it exactly.

The course was built to wait for a human recording: `frame.md` makes the spoken
narration the master clock, and every tracked duration stays a planning value
until one arrives. This produces that recording synthetically, which closes the
loop without a microphone.

It is not a substitute for a person reading it. A synthesised voice has no
emphasis and no judgement about where to slow down, and `LESSON_STYLE.md` 29
treats the same voice as a *reference* for exactly that reason. What it is good
for is a course that plays end to end today, and a set of timings that are
correct rather than estimated.

The timing is better than the transcription path it replaces. `build-narration-timing.ps1`
runs Whisper over a recording and aligns it to the script character by character,
which the repository README warns is not bit-reproducible — two runs can place a
boundary seconds apart. Here every paragraph is synthesised on its own, so its
start and end are known rather than recovered, `matchedRatio` is 1.0 by
construction, and a re-run produces the same numbers.

    python scripts/part/narrate_tts.py <lesson-dir> [--out DIR] [--dry-run]
    python scripts/part/narrate_tts.py --all [--out DIR]

Writes, per lesson:

    <out>/<lesson>/frame-NN.wav      the audio — never enters this repository
    <lesson>/narration-timing.json   numbers only, committed
    <lesson>/media.local.json        absolute paths, gitignored

Needs Windows with the ko-KR voice. `--voice` picks another installed one.
"""

import argparse
import io
import json
import os
import re
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402

ROOT = "projects/autocad-technician"
VOICE = "Microsoft Heami Desktop"

# Silence around a paragraph, matching what beats.plan assumes for a reading.
LEAD = getattr(beats, "LEAD_SEC", 0.4)
TAIL = getattr(beats, "TAIL_SEC", 0.6)
GAP = 0.45          # between paragraphs inside one frame

# The backtick spans are values to type, not words to read. A synthesiser says
# "backtick U C S backtick"; a person says the letters. Strip the marks and let
# the letters through.
TICK = re.compile(r"`([^`]*)`")
# Screen-direction parentheses — "(1번 카드 · 중심선)" — are stage directions for
# the frame, not narration. The reader never says them.
STAGE = re.compile(r"^\s*\([^)]*\)\s*")


def speakable(text):
    """The words a narrator actually says, from a script paragraph."""
    out = STAGE.sub("", text)
    out = TICK.sub(r"\1", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def read_wav(path):
    """{fmt, data, byte_rate, block_align} by walking the RIFF chunks.

    The synthesiser writes an 18-byte `fmt ` chunk, so the audio starts at 46
    rather than the 44 a canonical header would put it at. Assuming 44 hands the
    next two bytes of format to the mixer as if they were samples, and the file
    that comes out has no `data` tag at all.
    """
    with open(path, "rb") as fh:
        buf = fh.read()
    if buf[:4] != b"RIFF" or buf[8:12] != b"WAVE":
        raise ValueError("not a RIFF wave: %s" % path)
    fmt = data = None
    i = 12
    while i + 8 <= len(buf):
        cid = buf[i:i + 4]
        size = struct.unpack("<I", buf[i + 4:i + 8])[0]
        body = buf[i + 8:i + 8 + size]
        if cid == b"fmt ":
            fmt = body
        elif cid == b"data":
            data = body
        i += 8 + size + (size & 1)
    if fmt is None or data is None:
        raise ValueError("wave is missing fmt or data: %s" % path)
    return {"fmt": fmt, "data": data,
            "block_align": struct.unpack("<H", fmt[12:14])[0],
            "byte_rate": struct.unpack("<I", fmt[8:12])[0]}


def write_wav(path, fmt, data):
    """A canonical RIFF/WAVE file: RIFF, fmt, data. Nothing else."""
    with open(path, "wb") as fh:
        fh.write(b"RIFF")
        fh.write(struct.pack("<I", 4 + (8 + len(fmt)) + (8 + len(data))))
        fh.write(b"WAVE")
        fh.write(b"fmt ")
        fh.write(struct.pack("<I", len(fmt)))
        fh.write(fmt)
        fh.write(b"data")
        fh.write(struct.pack("<I", len(data)))
        fh.write(data)


def wav_seconds(path):
    w = read_wav(path)
    return round(len(w["data"]) / float(w["byte_rate"]), 3)


PS_SPEAK = r"""
param([string]$InFile, [string]$OutDir, [string]$Voice)
Add-Type -AssemblyName System.Speech
$syn = New-Object System.Speech.Synthesis.SpeechSynthesizer
$syn.SelectVoice($Voice)
$syn.Rate = 0
foreach ($ln in [IO.File]::ReadAllLines($InFile, [Text.Encoding]::UTF8)) {
  if ([string]::IsNullOrWhiteSpace($ln)) { continue }
  $p = $ln.Split("`t", 2)
  if ($p.Length -lt 2) { continue }
  $out = Join-Path $OutDir ($p[0] + '.wav')
  $syn.SetOutputToWaveFile($out)
  $syn.Speak($p[1])
  $syn.SetOutputToNull()
}
"""


def speak_many(items, outdir, voice):
    """items: [(key, text)] -> {key: wav path}. One process for the whole batch."""
    os.makedirs(outdir, exist_ok=True)
    fd, listfile = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    fd, script = tempfile.mkstemp(suffix=".ps1")
    os.close(fd)
    try:
        with io.open(listfile, "w", encoding="utf-8") as fh:
            for key, text in items:
                fh.write("%s\t%s\n" % (key, text.replace("\t", " ")))
        with io.open(script, "w", encoding="utf-8") as fh:
            fh.write(PS_SPEAK)
        run = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script,
             "-InFile", listfile, "-OutDir", outdir, "-Voice", voice],
            capture_output=True, text=True)
        if run.returncode != 0:
            raise SystemExit("TTS 실패:\n" + (run.stderr or run.stdout))
    finally:
        for p in (listfile, script):
            try:
                os.remove(p)
            except OSError:
                pass
    return {key: os.path.join(outdir, key + ".wav") for key, _ in items}


def concat_wavs(parts, gaps, outpath):
    """Join 16-bit PCM parts with silence between them. Returns [(start, end)].

    Every part comes from the same synthesiser, so the format is identical and
    the frames can simply be appended — no resampling, no ffmpeg.
    """
    spans, data, meta = [], bytearray(), None
    clock = 0.0

    def silence(seconds):
        n = int(round(seconds * meta["byte_rate"]))
        n -= n % max(1, meta["block_align"])
        return b"\0" * max(0, n)

    for i, p in enumerate(parts):
        w = read_wav(p)
        if meta is None:
            meta = w
        elif w["fmt"] != meta["fmt"]:
            raise ValueError("wave format changed mid-frame: %s" % p)
        data += silence(gaps[i])
        clock += gaps[i]
        start = clock
        data += w["data"]
        clock += len(w["data"]) / float(meta["byte_rate"])
        spans.append((round(start, 3), round(clock, 3)))
    data += silence(TAIL)
    clock += TAIL

    write_wav(outpath, meta["fmt"], bytes(data))
    return spans, round(clock, 3)


def lesson_frames(lesson_dir):
    """{line_no: [frame_id, ...]} keyed by the frame file's own number.

    A Line is not a frame. The recording Line of lessons 3 to 7 is cut into two
    or three frames — `05-demo-a`, `05-demo-b`, `05-demo-c` — so that no episode
    runs past twenty minutes, and all of them carry the number of the Line they
    came from. Counting files in order instead puts every frame after the demo
    one place early, which is silent: the audio still plays, under the wrong
    picture.
    """
    comp = os.path.join(lesson_dir, "compositions", "frames")
    out = {}
    for name in sorted(f[:-5] for f in os.listdir(comp) if f.endswith(".html")):
        m = re.match(r"(\d+)-", name)
        if m:
            out.setdefault(int(m.group(1)), []).append(name)
    return out


def cuts_for(lesson_dir):
    """The step numbers this lesson's recording is cut after, from the contract."""
    path = os.path.join(ROOT, "course-continuity.json")
    slug = os.path.basename(lesson_dir.rstrip("/\\"))
    try:
        with io.open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except OSError:
        return []
    for l in doc.get("lessons", []):
        if l.get("slug") == slug:
            return list(l.get("cutAfterStep") or [])
    return []


def narrate(lesson_dir, outroot, voice, dry_run=False):
    script = os.path.join(lesson_dir, "SCRIPT.md")
    sections = beats.parse_script(script)
    frames = dict(lesson_frames(lesson_dir))
    slug = os.path.basename(lesson_dir.rstrip("/\\"))
    outdir = os.path.join(outroot, slug)
    partdir = os.path.join(outdir, "_parts")

    cuts = cuts_for(lesson_dir)

    # units[(line_no, part)] = [(key, beat_index_or_None)] — one entry per frame
    jobs, units, order = [], {}, []
    for line_no in sorted(sections):
        ids = frames.get(line_no) or ["frame-%02d" % line_no]
        if len(ids) == 1:
            groups = [[(b, t) for b, t in sections[line_no]]]
        else:
            # The recording Line becomes several frames. Cut it where the
            # contract says the work finishes, not where the paragraphs fall.
            steps = beats.parse_steps(script, line_no)
            if not steps:
                groups = [[(b, t) for b, t in sections[line_no]]]
            else:
                pieces = beats.split_steps(steps, cuts)
                groups = [[(i, t) for i, t in piece] for _off, piece in pieces]
            if len(groups) != len(ids):
                raise SystemExit(
                    "%s Line %d: 프레임 %d개인데 조각이 %d개다 (cutAfterStep %r)"
                    % (slug, line_no, len(ids), len(groups), cuts))

        for part, (fid, group) in enumerate(zip(ids, groups)):
            entries = []
            for i, (beat_idx, text) in enumerate(group):
                words = speakable(text)
                if not words:
                    continue
                key = "L%02d-%d-%02d" % (line_no, part, i)
                jobs.append((key, words))
                entries.append((key, beat_idx))
            if entries:
                units[(line_no, part)] = entries
                order.append((line_no, part, fid))

    total_chars = sum(len(t) for _, t in jobs)
    if dry_run:
        print("%-34s 문단 %3d · 글자 %6d · 프레임 %d"
              % (slug, len(jobs), total_chars, len(frames)))
        return None

    made = speak_many(jobs, partdir, voice)

    frames_out, beats_out, clock = [], [], 0.0
    for seq, (line_no, part, fid) in enumerate(order, 1):
        entries = units[(line_no, part)]
        wavs = [made[k] for k, _ in entries]
        gaps = [LEAD if i == 0 else GAP for i in range(len(wavs))]
        dest = os.path.join(outdir, "%s.wav" % fid)
        spans, dur = concat_wavs(wavs, gaps, dest)

        frames_out.append({
            "frame": seq,
            "id": fid,
            "line": line_no,
            "start": round(clock, 3),
            "end": round(clock + dur, 3),
            "duration": dur,
            "audio": os.path.basename(dest),
        })
        for (key, beat_idx), (s, e) in zip(entries, spans):
            if beat_idx is not None:
                beats_out.append({
                    "frame": seq,
                    "beat": beat_idx,
                    "observedStart": round(clock + s, 3),
                    "observedEnd": round(clock + e, 3),
                })
        clock += dur

    timing = {
        "schemaVersion": 1,
        "source": "synthesised",
        "voice": voice,
        "note": ("Windows 음성으로 대본을 읽어 만든 시각이다. 문단마다 따로 합성해 "
                 "길이를 그대로 읽었으므로 정렬 오차가 없고 다시 돌려도 같은 값이 나온다. "
                 "사람이 녹음하면 그 값이 이것을 대체한다."),
        "totalSeconds": round(clock, 3),
        "frames": frames_out,
        "beats": beats_out,
    }
    with io.open(os.path.join(lesson_dir, "narration-timing.json"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(timing, ensure_ascii=False, indent=2) + "\n")

    local = {"narrationDir": os.path.abspath(outdir),
             "frames": {f["id"]: os.path.abspath(os.path.join(outdir, f["audio"]))
                        for f in frames_out}}
    with io.open(os.path.join(lesson_dir, "media.local.json"), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(local, ensure_ascii=False, indent=2) + "\n")

    print("%-34s 프레임 %2d · 비트 %3d · %6.1f초 (%d:%02d)"
          % (slug, len(frames_out), len(beats_out), clock, clock // 60, clock % 60))
    return timing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("lesson", nargs="?", help="차시 디렉터리")
    ap.add_argument("--all", action="store_true", help="여덟 차시 전부")
    ap.add_argument("--out", default=None, help="음성을 둘 곳 (저장소 밖)")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--dry-run", action="store_true", help="분량만 세고 쓰지 않는다")
    a = ap.parse_args(argv)

    outroot = a.out or os.path.join(tempfile.gettempdir(), "edu-ib-02-narration")
    if a.all:
        targets = [os.path.join(ROOT, d) for d in sorted(os.listdir(ROOT))
                   if d.startswith("lesson-") and
                   os.path.isfile(os.path.join(ROOT, d, "SCRIPT.md"))]
    elif a.lesson:
        targets = [a.lesson]
    else:
        ap.error("차시를 지정하거나 --all 을 주세요")

    total = 0.0
    for t in targets:
        r = narrate(t, outroot, a.voice, a.dry_run)
        if r:
            total += r["totalSeconds"]
    if total:
        print("\n합계 %.1f초 (%d:%02d) · 음성 위치 %s"
              % (total, total // 60, total % 60, outroot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
