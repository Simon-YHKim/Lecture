# -*- coding: utf-8 -*-
"""차시 전달 목록과 BRIEF 길이를 마스터(index.html)에 다시 맞춘다.

현재 과정은 차시당 index.html 하나를 전달한다. 기존 파일명과 호출 API는
유지하되 과거 compositions/episodes/ 파일은 갱신하지 않는다. master의
프레임 순서가 정본 선언과 일치하는지 확인하고 BRIEF 길이만 맞춘다.
저작한 프레임은 건드리지 않는다.

    python scripts/part/rebuild_episodes.py            # 여덟 차시 전부
    python scripts/part/rebuild_episodes.py <lesson-dir>
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import episodes  # noqa: E402
import lesson_kit as kit  # noqa: E402

ROOT = "projects/autocad-technician"

SLOT = re.compile(
    r'<div id="(?P<sid>[^"]+)"[^>]*?data-composition-id="(?P<cid>[^"]+)"'
    r'[^>]*?data-composition-src="compositions/frames/(?P<stem>[^"]+)\.html"'
    r'[^>]*?data-start="(?P<start>[\d.]+)"[^>]*?data-duration="(?P<dur>[\d.]+)"')


def read_slots(lesson_dir):
    """index.html 이 마스터다. (sid, cid, stem, start, dur) 를 순서대로 돌려준다."""
    p = os.path.join(lesson_dir, "index.html")
    body = io.open(p, encoding="utf-8").read()
    out = []
    for m in SLOT.finditer(body):
        out.append((m.group("sid"), m.group("cid"), m.group("stem"),
                    float(m.group("start")), float(m.group("dur"))))
    if not out:
        raise SystemExit("%s 에서 슬롯을 못 읽었다" % p)
    return out


def mmss(sec):
    return "%dm%02ds" % (int(sec) // 60, int(round(sec)) % 60)


def fix_brief(lesson_dir, total):
    p = os.path.join(lesson_dir, "BRIEF.md")
    if not os.path.exists(p):
        return None
    body = io.open(p, encoding="utf-8").read()
    want = mmss(total)
    new, n = re.subn(r"^length:\s*\S+$", "length: " + want, body, count=1, flags=re.M)
    if n and new != body:
        io.open(p, "w", encoding="utf-8", newline="\n").write(new)
        return want
    return None


def one(lesson_dir):
    slug = os.path.basename(os.path.normpath(lesson_dir))
    slots = read_slots(lesson_dir)
    total = sum(s[4] for s in slots)
    eps = kit.write_episodes(lesson_dir, slots, episodes.episodes_for(slug), os)
    brief = fix_brief(lesson_dir, total)
    caps = [t for _, _, t, _ in eps if episodes.CAP_SEC is not None and t > episodes.CAP_SEC]
    print("%-34s 통합 차시 %d개 · 전체 %6.1f초 (%s)%s%s"
          % (slug, len(eps), total, mmss(total),
             "  BRIEF length: " + brief if brief else "",
             "  ⚠ 20분 초과 %d편" % len(caps) if caps else ""))
    return total


def main(argv):
    if argv:
        targets = argv
    else:
        targets = [os.path.join(ROOT, d) for d in sorted(os.listdir(ROOT))
                   if d.startswith("lesson-") and
                   os.path.isfile(os.path.join(ROOT, d, "index.html"))]
    total = sum(one(t) for t in targets)
    print("\n합계 %.1f초 (%d:%02d)" % (total, total // 60, total % 60))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
