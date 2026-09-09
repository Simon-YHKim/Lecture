# -*- coding: utf-8 -*-
"""편과 BRIEF 의 길이를 마스터(index.html)에 다시 맞춘다.

편은 복사본이 아니라 같은 프레임을 가리키는 재생 목록이다(LESSON_STYLE 30번).
그런데 `narrate_tts` 가 나레이션을 다시 재고 `retime_frames` 가 프레임을 다시
맞추면 index.html 의 슬롯 길이만 바뀌고, `compositions/episodes/ep*.html` 과
`BRIEF.md` 의 `length:` 는 옛 값을 든 채 남는다. 검사기가 「편 길이가 마스터와
다르다」로 잡는 것이 이 상태다.

스캐폴드를 다시 돌리면 이것도 고쳐지지만 Studio 가 심어 둔 편집이 사라진다
(COURSE_PLAN 「다시 만들기」). 그래서 편만 다시 굽는다 — 프레임은 건드리지 않고
index.html 을 읽어 슬롯을 그대로 옮긴다.

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
    caps = [t for _, _, t, _ in eps if t > episodes.CAP_SEC]
    print("%-34s 편 %d · 전체 %6.1f초 (%s)%s%s"
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
