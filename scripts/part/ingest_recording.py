"""Register a screen recording with the lesson that shows it.

The recording itself never enters this repository. It stays wherever you keep
private course material; this reads its dimensions and duration and writes two
small files:

  <lesson>/recording.json        numbers only — publishable, committed
  <lesson>/media.local.json      the absolute path — gitignored, yours alone

The split matters. `recording.json` is what the build reads to size the DEMO
frame, so the length of that frame stops being an estimate. `media.local.json`
is what preview reads to actually play the file, and it is the only place an
absolute path to your private storage appears.

    python scripts/part/ingest_recording.py <lesson-dir> <video-path>
    python scripts/part/ingest_recording.py --list
"""

import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_course as vc  # noqa: E402

ROOT = "projects/autocad-technician"


def probe(path):
    """Duration, size and frame rate. ffprobe ships with ffmpeg."""
    exe = shutil.which("ffprobe")
    if not exe:
        raise SystemExit(
            "ffprobe 를 찾을 수 없습니다. ffmpeg 를 설치하고 PATH 에 넣어 주세요.\n"
            "  winget install Gyan.FFmpeg")
    out = subprocess.run(
        [exe, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate:format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    st = (d.get("streams") or [{}])[0]
    num, _, den = (st.get("r_frame_rate") or "0/1").partition("/")
    fps = round(float(num) / float(den or 1), 3) if float(den or 1) else 0.0
    return {
        "durationSec": round(float(d["format"]["duration"]), 3),
        "width": st.get("width"),
        "height": st.get("height"),
        "fps": fps,
    }


def ingest(lesson_dir, video):
    repo = os.path.abspath(".")
    full = os.path.abspath(video)
    if full.lower().startswith(repo.lower() + os.sep):
        raise SystemExit(
            "녹화 파일이 저장소 안에 있습니다: %s\n"
            "원본은 저장소 밖 비공개 위치에 두세요. 이 스크립트는 읽기만 합니다." % full)
    if not os.path.isfile(full):
        raise SystemExit("파일이 없습니다: %s" % full)

    info = probe(full)
    if info["width"] != 1920 or info["height"] != 1080:
        print("  주의: %sx%s 입니다. 삽입 영역은 1920x1080 기준입니다."
              % (info["width"], info["height"]))

    slug = os.path.basename(os.path.normpath(lesson_dir))
    rec = dict(info)
    rec.update({"schemaVersion": 1, "lesson": slug, "demoId": "DEMO-01"})
    with open(os.path.join(lesson_dir, "recording.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    with open(os.path.join(lesson_dir, "media.local.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump({"note": "비공개 경로. 커밋되지 않습니다.",
                   "DEMO-01": full.replace("\\", "/")}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("  %s" % slug)
    print("    길이 %d:%02d · %sx%s · %g fps"
          % (int(info["durationSec"]) // 60, int(info["durationSec"]) % 60,
             info["width"], info["height"], info["fps"]))
    print("    recording.json  기록 (공개)")
    print("    media.local.json 기록 (비공개, gitignore)")
    print("\n  이제 그 차시를 다시 만들면 DEMO 프레임이 실제 길이가 됩니다.")
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
    if len(argv) != 2:
        raise SystemExit(__doc__)
    lesson = argv[0]
    if not os.path.isdir(lesson):
        cand = [s for s, _a, _b in vc.LESSONS if re.search(argv[0], s)]
        if len(cand) != 1:
            raise SystemExit("차시를 특정할 수 없습니다: %s" % argv[0])
        lesson = os.path.join(ROOT, cand[0])
    ingest(lesson, argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
