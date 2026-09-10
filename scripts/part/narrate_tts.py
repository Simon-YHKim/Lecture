"""Create measured Heami Rate 0 narration with pitch-preserving 1.38x tempo.

Each paragraph is synthesised separately and converted with local FFmpeg
atempo. Boundaries are measured from the resulting PCM, not estimated by
dividing the source length. Inter-paragraph silence and frame holds also use
the approved tempo. Pronunciation and instructional meaning need human review.

    python scripts/part/narrate_tts.py <lesson-dir> --tempo 1.38 --out DIR
    python scripts/part/narrate_tts.py --all --tempo 1.38 --out DIR

DIR must be outside Git and each lesson's destination must be fresh. It keeps
the Rate 0 source frames in `_source/` and converted frames in the lesson root.
Tracked narration-timing.json contains numbers, relative names and hashes;
gitignored media.local.json holds paths and preserves recording bindings.
Requires Windows Microsoft Heami Desktop and local FFmpeg. --dry-run only
counts the current script and frame mapping without writing or synthesising.
"""

import argparse
import hashlib
import io
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import episodes  # noqa: E402

ROOT = "projects/autocad-technician"
VOICE = "Microsoft Heami Desktop"
TEMPO = 1.38
BASE_FRAME_HOLD = 1.6

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


def spoken_hash(script):
    """Hash exactly the frame/part/beat jobs sent to the speech engine."""
    jobs, units, order = synthesis_plan(script)
    content = {'jobs': jobs, 'units': sorted((line, part, value)
               for (line, part), value in units.items()), 'order': order}
    return hashlib.sha256(json.dumps(content, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def verify_script_hash(lesson_dir, timing):
    expected = timing.get('spokenTextSha256')
    if not expected:
        raise ValueError('대본 식별정보가 없습니다. TTS를 다시 생성하세요.')
    if expected != spoken_hash(os.path.join(lesson_dir, 'SCRIPT.md')):
        raise ValueError('대본이 음성 생성 뒤 바뀌었습니다. TTS를 다시 생성하세요.')


def timing_identity(timing):
    payload = {k: v for k, v in timing.items() if k != 'timingSha256'}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def verify_tempo_timing(timing, required=False):
    """Keep old reference audio distinct from the current 1.38x delivery voice."""
    if 'tempo' not in timing:
        if required:
            raise ValueError('Current delivery requires regenerated 1.38x tempo timing')
        return 1.0
    if (timing.get('schemaVersion') != 2 or timing.get('rate') != 0
            or timing.get('tempo') != TEMPO or timing.get('tempoMethod') != 'ffmpeg-atempo-per-paragraph'
            or not timing.get('tempoToolVersion') or timing.get('voice') != VOICE):
        raise ValueError('Expected Heami Rate 0 followed by pitch-preserving 1.38x tempo conversion')
    if timing.get('timingSha256') != timing_identity(timing):
        raise ValueError('Narration timing identity changed; regenerate speech')
    if timing.get('sourceFrameHoldSeconds') != BASE_FRAME_HOLD or abs(timing.get('frameHoldSeconds', -1) - BASE_FRAME_HOLD / TEMPO) > 1e-9:
        raise ValueError('Frame hold must use the same approved tempo')
    expected_beats, clock, source_clock = [], 0.0, 0.0
    for seq, frame in enumerate(timing['frames'], 1):
        for key in ('duration', 'sourceDuration', 'start', 'end', 'sourceStart', 'sourceEnd'):
            if not isinstance(frame.get(key), (int, float)) or not math.isfinite(frame[key]) or frame[key] < 0:
                raise ValueError('Narration times must be finite and nonnegative')
        if (frame['frame'] != seq or frame['duration'] <= 0 or frame['sourceDuration'] <= 0
                or abs(frame['start'] - clock) > .002 or abs(frame['sourceStart'] - source_clock) > .002
                or abs(frame['end'] - clock - frame['duration']) > .002
                or abs(frame['sourceEnd'] - source_clock - frame['sourceDuration']) > .002):
            raise ValueError('Narration frames do not form continuous measured timelines')
        for key in ('audioSha256', 'sourceAudioSha256'):
            if not re.fullmatch(r'[0-9a-f]{64}', frame.get(key, '')):
                raise ValueError('Narration is missing a source or output identity')
        previous, source_previous = 0.0, 0.0
        if not frame.get('units'):
            raise ValueError('Measured paragraph boundaries are required')
        for unit in frame['units']:
            values = [unit.get(k) for k in ('start', 'end', 'sourceStart', 'sourceEnd')]
            if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
                raise ValueError('Paragraph times must be finite')
            a, b, sa, sb = values
            if not (previous <= a < b <= frame['duration'] and source_previous <= sa < sb <= frame['sourceDuration']):
                raise ValueError('Paragraphs overlap or leave their measured frame')
            previous, source_previous = b, sb
            if unit['beat'] is not None:
                expected_beats.append({'frame': seq, 'beat': unit['beat'],
                    'observedStart': round(clock + a, 3), 'observedEnd': round(clock + b, 3),
                    'sourceObservedStart': round(source_clock + sa, 3),
                    'sourceObservedEnd': round(source_clock + sb, 3)})
        clock += frame['duration']
        source_clock += frame['sourceDuration']
    if (timing['beats'] != expected_beats or abs(timing['totalSeconds'] - clock) > .002
            or abs(timing['sourceTotalSeconds'] - source_clock) > .002):
        raise ValueError('Measured beats or totals differ from their paragraph timelines')
    return TEMPO


def frame_hold(timing):
    return BASE_FRAME_HOLD / verify_tempo_timing(timing)


def change_tempo(source, target, tempo=TEMPO):
    """Create new PCM with atempo; source audio and its pitch are preserved."""
    if tempo != TEMPO:
        raise ValueError('The approved narration tempo is 1.38')
    source, target = private_output(source), private_output(target)
    if source == target or target.exists():
        raise ValueError('Tempo output must be a fresh file')
    exe = shutil.which('ffmpeg')
    if not exe:
        raise ValueError('Local FFmpeg is required for pitch-preserving 1.38x speech')
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, '-nostdin', '-v', 'error', '-xerror', '-i', str(source),
                    '-map', '0:a:0', '-af', 'atempo=1.38', '-c:a', 'pcm_s16le', '-n', str(target)],
                   capture_output=True, check=True, timeout=max(60, wav_seconds(source) * 2 + 30))
    original, result = read_wav(source), read_wav(target)
    if original['fmt'][:16] != result['fmt'][:16] or not result['data']:
        raise ValueError('Tempo conversion changed the PCM format or produced empty audio')
    return str(target)


def private_output(path):
    root = Path(__file__).resolve().parents[2]
    target = Path(path).expanduser().resolve()
    if target == root or root in target.parents or any((p / '.git').exists() for p in (target, *target.parents)):
        raise ValueError('음성은 Git 저장소 밖의 폴더에 저장해야 합니다.')
    return target


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
$ErrorActionPreference = 'Stop'
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


def concat_wavs(parts, gaps, outpath, tail=TAIL):
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
        start = len(data) / float(meta['byte_rate'])
        data += w["data"]
        clock = len(data) / float(meta['byte_rate'])
        spans.append((round(start, 3), round(clock, 3)))
    data += silence(tail)
    clock = len(data) / float(meta['byte_rate'])

    write_wav(outpath, meta["fmt"], bytes(data))
    return spans, round(clock, 3)


def lesson_frames(lesson_dir):
    """{line_no: [frame_id, ...]} keyed by the frame file's own number.

    A Line is not a frame. The recording Line of lessons 3 to 7 uses two or
    three internal recording fragments — `05-demo-a`, `05-demo-b`, `05-demo-c` —
    and all of them carry the number of the Line they came from. These are
    assembled into one lesson delivery. Counting files in order instead puts every frame after the demo
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
    slug = os.path.basename(lesson_dir.rstrip("/\\"))
    return episodes.cuts_for(slug) if slug in episodes.slugs() else []


def synthesis_plan(script):
    lesson_dir = str(Path(script).parent)
    sections = beats.parse_script(script)
    frames = dict(lesson_frames(lesson_dir)) if (Path(lesson_dir) / 'compositions/frames').is_dir() else {}
    slug = Path(lesson_dir).name
    cuts = cuts_for(lesson_dir)
    # units[(line_no, part)] = [(key, beat_index_or_None)] — one entry per frame
    jobs, units, order = [], {}, []
    for line_no in sorted(sections):
        ids = frames.get(line_no) or ["frame-%02d" % line_no]
        steps = beats.parse_steps(script, line_no)
        if steps:
            if len(ids) == 1:
                groups = [steps]
            else:
                pieces = beats.split_steps(steps, cuts)
                groups = [[(i, t) for i, t in piece] for _off, piece in pieces]
        else:
            groups = [[(b, t) for b, t in sections[line_no]]]
        if len(groups) != len(ids):
            raise ValueError('%s Line %d: frame and narration group counts differ' % (slug, line_no))

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

    return jobs, units, order


def narrate(lesson_dir, outroot, voice, dry_run=False, tempo=TEMPO):
    if tempo != TEMPO or voice != VOICE:
        raise ValueError('Use Microsoft Heami Desktop Rate 0 with tempo 1.38')
    outroot = str(private_output(outroot))
    script = os.path.join(lesson_dir, 'SCRIPT.md')
    input_hash = spoken_hash(script)
    jobs, units, order = synthesis_plan(script)
    slug = os.path.basename(lesson_dir.rstrip('/\\'))
    outdir = os.path.join(outroot, slug)
    partdir = os.path.join(outdir, '_parts-rate0')

    total_chars = sum(len(t) for _, t in jobs)
    if dry_run:
        print("%-34s 문단 %3d · 글자 %6d · 프레임 %d · Rate 0 → atempo 1.38"
              % (slug, len(jobs), total_chars, len(order)))
        return None

    if os.path.exists(outdir):
        raise ValueError('Choose a fresh narration output directory: ' + outdir)
    if not jobs:
        raise ValueError('No narration paragraphs were found')
    lesson = Path(lesson_dir)
    originals = {name: (lesson / name).read_bytes() if (lesson / name).exists() else None
                 for name in ('narration-timing.json', 'media.local.json')}
    local = json.loads(originals['media.local.json']) if originals['media.local.json'] is not None else {}
    if not isinstance(local, dict):
        raise ValueError('Existing media.local.json must be an object')
    exe = shutil.which('ffmpeg')
    if not exe:
        raise ValueError('Local FFmpeg is required for pitch-preserving 1.38x speech')
    tool_version = subprocess.run([exe, '-version'], capture_output=True, text=True,
                                  check=True, timeout=30).stdout.splitlines()[0]
    verify_script_hash(lesson_dir, {'spokenTextSha256': input_hash})
    made = speak_many(jobs, partdir, voice)
    verify_script_hash(lesson_dir, {'spokenTextSha256': input_hash})
    fast = {key: change_tempo(path, Path(outdir) / '_parts-tempo' / (key + '.wav'), tempo)
            for key, path in made.items()}
    verify_script_hash(lesson_dir, {'spokenTextSha256': input_hash})

    frames_out, beats_out, clock, source_clock = [], [], 0.0, 0.0
    source_dir = Path(outdir) / '_source'
    source_dir.mkdir(parents=True, exist_ok=True)
    for seq, (line_no, part, fid) in enumerate(order, 1):
        entries = units[(line_no, part)]
        wavs = [fast[k] for k, _ in entries]
        gaps = [LEAD if i == 0 else GAP for i in range(len(wavs))]
        dest = os.path.join(outdir, "%s.wav" % fid)
        source_dest = source_dir / ('%s.wav' % fid)
        source_spans, source_dur = concat_wavs([made[k] for k, _ in entries], gaps, source_dest)
        spans, dur = concat_wavs(wavs, [gap / tempo for gap in gaps], dest, tail=TAIL / tempo)
        unit_times = [{'beat': beat_idx, 'start': s, 'end': e, 'sourceStart': sa, 'sourceEnd': se}
                      for (_, beat_idx), (s, e), (sa, se) in zip(entries, spans, source_spans)]

        frames_out.append({
            "frame": seq,
            "id": fid,
            "line": line_no,
            "start": round(clock, 3),
            "end": round(clock + dur, 3),
            "duration": dur,
            "audio": os.path.basename(dest),
            "audioSha256": hashlib.sha256(Path(dest).read_bytes()).hexdigest(),
            "sourceAudio": source_dest.name,
            "sourceAudioSha256": hashlib.sha256(source_dest.read_bytes()).hexdigest(),
            "sourceStart": round(source_clock, 3),
            "sourceEnd": round(source_clock + source_dur, 3),
            "sourceDuration": source_dur,
            "units": unit_times,
        })
        for (key, beat_idx), (s, e), (sa, se) in zip(entries, spans, source_spans):
            if beat_idx is not None:
                beats_out.append({
                    "frame": seq,
                    "beat": beat_idx,
                    "observedStart": round(clock + s, 3),
                    "observedEnd": round(clock + e, 3),
                    "sourceObservedStart": round(source_clock + sa, 3),
                    "sourceObservedEnd": round(source_clock + se, 3),
                })
        clock += dur
        source_clock += source_dur

    timing = {
        "schemaVersion": 2,
        "source": "synthesised",
        "voice": voice,
        "rate": 0,
        "tempo": tempo,
        "tempoMethod": "ffmpeg-atempo-per-paragraph",
        "tempoToolVersion": tool_version,
        "sourceFrameHoldSeconds": BASE_FRAME_HOLD,
        "frameHoldSeconds": BASE_FRAME_HOLD / tempo,
        "spokenTextSha256": input_hash,
        "note": ("Heami Rate 0 원본 문단을 atempo=1.38로 변환하고 결과 PCM 길이를 다시 쟀다. "
                 "문단 경계는 실제 합친 음성의 시각이며 문장 내부의 발음·의미는 별도 검수한다. "
                 "원본 음성과 변환 음성, 도구 버전과 해시를 비공개 출력에 함께 보존한다."),
        "totalSeconds": round(clock, 3),
        "sourceTotalSeconds": round(source_clock, 3),
        "frames": frames_out,
        "beats": beats_out,
    }
    timing['timingSha256'] = timing_identity(timing)
    verify_script_hash(lesson_dir, timing)
    verify_tempo_timing(timing, required=True)
    local.update({"narrationDir": os.path.abspath(outdir),
                  "frames": {f["id"]: os.path.abspath(os.path.join(outdir, f["audio"]))
                              for f in frames_out},
                  "sourceFrames": {f['id']: str((source_dir / f['sourceAudio']).resolve()) for f in frames_out}})
    # Reuse the two-file transaction; a concurrent metadata editor must survive.
    from ingest_recording import write_metadata
    write_metadata(lesson.resolve(), {'narration-timing.json': timing, 'media.local.json': local}, originals)

    print("%-34s 프레임 %2d · 비트 %3d · %6.1f초 (%d:%02d)"
          % (slug, len(frames_out), len(beats_out), clock, clock // 60, clock % 60))
    return timing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("lesson", nargs="?", help="차시 디렉터리")
    ap.add_argument("--all", action="store_true", help="여덟 차시 전부")
    ap.add_argument("--out", default=None, help="음성을 둘 곳 (저장소 밖)")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--tempo", type=float, choices=[TEMPO], default=TEMPO,
                    help="Rate 0 원본의 음높이를 보존한 1.38배속")
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
        r = narrate(t, outroot, a.voice, a.dry_run, a.tempo)
        if r:
            total += r["totalSeconds"]
    if total:
        print("\n합계 %.1f초 (%d:%02d) · 음성 위치 %s"
              % (total, total // 60, total % 60, outroot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
