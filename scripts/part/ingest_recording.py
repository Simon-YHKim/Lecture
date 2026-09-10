"""Register a screen recording with the lesson that shows it.

The recording itself never enters this repository. It stays wherever you keep
private course material; this reads its dimensions and duration and writes two
small files:

  <lesson>/recording.json        stream measurements and hashes — publishable
  <lesson>/media.local.json      the absolute path — gitignored, yours alone

The existing narration/other bindings in `media.local.json` are retained.
`prepare_lecture.py` validates registered recordings against the measured slots,
then connects copies inside a fresh private delivery. It never rebuilds authored
frames, changes video speed, or automatically trims a take.

    python scripts/part/ingest_recording.py <lesson-dir> <video> [<video> ...]
        끊어 찍은 차시는 부분 수만큼 순서대로 넘긴다.
    python scripts/part/ingest_recording.py --list
"""

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import episodes  # noqa: E402
import verify_course as vc  # noqa: E402
from narrate_tts import private_output  # noqa: E402

ROOT = "projects/autocad-technician"


def recording_ids(slug):
    """The checked-in map and episode cuts must name the same complete take set."""
    path = Path(__file__).resolve().parents[2] / ROOT / 'recording-map.json'
    rows = [r for r in json.loads(path.read_text(encoding='utf-8'))['recordings'] if r['slug'] == slug]
    if len(rows) != 1 or rows[0]['cutAfterStep'] != episodes.cuts_for(slug):
        raise ValueError('No matching canonical recording plan: ' + slug)
    row = rows[0]
    ids = [p['id'] for p in row['parts']] if row['parts'] else [row['demoId']]
    count = len(row['cutAfterStep']) + 1
    expected = ['DEMO-01' + ('ABCDEFGH'[i] if count > 1 else '') for i in range(count)]
    if ids != expected:
        raise ValueError('Recording parts differ from the episode cuts')
    return ids


def recording_frames(slug):
    if slug not in episodes.slugs():
        return {}
    frames = [stem for stem in episodes.frames_for(slug)
              if stem == '08-build-template' or re.fullmatch(r'05-demo(?:-[a-h])?', stem)]
    if not frames:
        return {}
    ids = recording_ids(slug)
    if len(frames) != len(ids):
        raise ValueError('Recording frames differ from the canonical parts')
    return dict(zip(frames, ids))


def file_sha256(path):
    with open(path, 'rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def recording_file(path):
    target = private_output(path)
    if target.suffix.lower() != '.mp4' or not target.is_file():
        raise ValueError('A private, existing MP4 recording is required')
    return target


def probe(path):
    """Validate the actual video stream, then decode it completely without edits."""
    exe = shutil.which("ffprobe")
    if not exe:
        raise SystemExit(
            "ffprobe 를 찾을 수 없습니다. ffmpeg 를 설치하고 PATH 에 넣어 주세요.\n"
            "  winget install Gyan.FFmpeg")
    out = subprocess.run(
        [exe, "-v", "error", "-show_streams", "-show_format",
         "-of", "json", path],
        capture_output=True, text=True, check=True, timeout=60).stdout
    d = json.loads(out)
    streams = [s for s in d.get('streams', []) if s.get('codec_type') == 'video']
    if len(streams) != 1:
        raise ValueError('Recording must contain exactly one video stream')
    st = streams[0]
    try:
        num, den = st['avg_frame_rate'].split('/')
        fps, duration = float(num) / float(den), float(st['duration'])
        start = float(st.get('start_time', 0))
        rotation = float(st.get('tags', {}).get('rotate', 0))
        rotations = [float(s['rotation']) for s in st.get('side_data_list', []) if 'rotation' in s]
    except (KeyError, ValueError, ZeroDivisionError, TypeError) as error:
        raise ValueError('Recording has no valid video duration or frame rate') from error
    if not all(math.isfinite(n) for n in (duration, fps, start, rotation, *rotations)) or duration <= 0 or not 1 <= fps <= 120:
        raise ValueError('Recording duration and frame rate must be finite and positive')
    if (st.get('codec_name') != 'h264' or st.get('pix_fmt') != 'yuv420p'
            or (st.get('width'), st.get('height')) != (1920, 1080)
            or st.get('sample_aspect_ratio') != '1:1'
            or abs(start) > .002 or rotation != 0 or any(rotations)
            or st.get('disposition', {}).get('attached_pic', 0)
            or 'mp4' not in d.get('format', {}).get('format_name', '').split(',')):
        raise ValueError('Recording requires an unrotated 1920x1080 square-pixel H.264/yuv420p MP4 starting at zero')
    decoder = shutil.which('ffmpeg')
    if not decoder:
        raise ValueError('ffmpeg is required to verify the complete recording')
    decoded = subprocess.run([decoder, '-nostdin', '-v', 'error', '-xerror', '-err_detect', 'explode',
                    '-noautorotate', '-i', str(path), '-map', '0:v:0', '-an', '-fps_mode', 'passthrough',
                    '-progress', 'pipe:1', '-f', 'null', '-'], capture_output=True, text=True,
                    check=True, timeout=max(60, math.ceil(duration * 2 + 30)))
    progress = dict(line.split('=', 1) for line in decoded.stdout.splitlines() if '=' in line)
    try:
        count, decoded_seconds = int(progress['frame']), int(progress['out_time_us']) / 1e6
        expected_count = int(st['nb_frames'])
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError('Complete decoded recording length cannot be verified') from error
    if (progress.get('progress') != 'end' or count <= 0 or count != expected_count
            or abs(decoded_seconds - duration) > 1 / fps + .003):
        raise ValueError('Decoded recording is incomplete or differs from its declared length')
    return {'durationSec': round(duration, 3), 'width': 1920, 'height': 1080,
            'fps': fps, 'codec': 'h264', 'pixelFormat': 'yuv420p'}


def write_metadata(lesson, updates, originals):
    """Stage both documents; restore the first if replacing the second fails."""
    with tempfile.TemporaryDirectory(prefix='.recording-', dir=lesson) as temp:
        stage = Path(temp)
        for name, value in updates.items():
            (stage / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            if originals[name] is not None:
                (stage / (name + '.before')).write_bytes(originals[name])
        for name, original in originals.items():
            path = lesson / name
            if (path.read_bytes() if path.exists() else None) != original:
                raise ValueError('Recording metadata changed during validation: ' + name)
        replaced = []
        try:
            for name in updates:
                os.replace(stage / name, lesson / name)
                replaced.append(name)
        except OSError:
            for name in reversed(replaced):
                if originals[name] is None:
                    (lesson / name).unlink()
                else:
                    os.replace(stage / (name + '.before'), lesson / name)
            raise


def ingest(lesson_dir, videos):
    slug = os.path.basename(os.path.normpath(lesson_dir))
    ids = recording_ids(slug)
    want = len(ids)
    if len(videos) != want:
        raise SystemExit(
            "%s 는 녹화가 %d개입니다 (%s). %d개를 받았습니다.\n"
            "끊는 자리는 RECORDING_GUIDE.md 와 episodes.json 에 있습니다."
            % (slug, want,
               " · ".join("%d단계 뒤" % c for c in episodes.cuts_for(slug)) or "안 끊음",
               len(videos)))

    lesson = Path(lesson_dir).resolve()
    originals = {name: (lesson / name).read_bytes() if (lesson / name).exists() else None
                 for name in ('recording.json', 'media.local.json')}
    local = json.loads(originals['media.local.json']) if originals['media.local.json'] is not None else {}
    if not isinstance(local, dict):
        raise ValueError('Existing media.local.json must be an object')
    parts, paths, identities = [], {}, {}
    for k, video in enumerate(videos):
        full = recording_file(video)
        if full in identities:
            raise ValueError('Each recording part requires a distinct file')
        identity = file_sha256(full)
        info = probe(full)
        if file_sha256(full) != identity:
            raise ValueError('Recording changed during validation')
        identities[full] = identity
        demo_id = ids[k]
        info["demoId"] = demo_id
        info['sha256'] = identity
        parts.append(info)
        paths[demo_id] = full.as_posix()

    total = round(sum(p["durationSec"] for p in parts), 3)
    first = parts[0]
    rec = {"schemaVersion": 2, "lesson": slug, "demoId": "DEMO-01",
           "durationSec": total,
           "width": first["width"], "height": first["height"],
           "fps": first["fps"],
            "parts": parts}
    local.update(paths)
    for path, identity in identities.items():
        if file_sha256(path) != identity:
            raise ValueError('Recording changed before registration')
    write_metadata(lesson, {'recording.json': rec, 'media.local.json': local}, originals)

    print("  %s" % slug)
    for p in parts:
        print("    %s  %d:%02d" % (p["demoId"], int(p["durationSec"]) // 60,
                                   int(p["durationSec"]) % 60))
    print("    합계 %d:%02d · %sx%s · %g fps"
          % (int(total) // 60, int(total) % 60,
             first["width"], first["height"], first["fps"]))
    print("    recording.json  기록 (공개)")
    print("    media.local.json 기록 (비공개, gitignore)")
    print("\n  원본 프레임을 보존하고 prepare_lecture.py로 연결·길이를 검증하세요.")
    return rec


def status():
    print("  차시                              녹화        나레이션 타이밍")
    for slug, _a, _b in vc.LESSONS:
        d = os.path.join(ROOT, slug)
        r = os.path.join(d, "recording.json")
        t = os.path.join(d, "narration-timing.json")
        if os.path.isfile(r):
            with open(r, encoding="utf-8") as fh:
                sec = json.load(fh)["durationSec"]
            got = "%d:%02d" % (int(sec) // 60, int(sec) % 60)
        else:
            got = "—"
        print("  %-32s %-10s %s"
              % (slug, got, "있음" if os.path.isfile(t) else "—"))


def main(argv):
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)
    if not argv or argv[0] in ("--list", "-l"):
        return status()
    if len(argv) < 2:
        raise SystemExit(__doc__)
    lesson = argv[0]
    if not os.path.isdir(lesson):
        cand = [s for s, _a, _b in vc.LESSONS if re.search(argv[0], s)]
        if len(cand) != 1:
            raise SystemExit("차시를 특정할 수 없습니다: %s" % argv[0])
        lesson = os.path.join(ROOT, cand[0])
    ingest(lesson, argv[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
