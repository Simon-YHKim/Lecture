# -*- coding: utf-8 -*-
"""기획 문서에 남은 「보라」를 걷는다.

사용자 확인 (2026-09-10) — **보라색 선은 사용하지 않는다.** 학습자에게 나가는
글에서는 이미 사라졌지만 `curriculum.json` 에 일곱 군데가 남아 있었다. 이 파일은
자습본을 다시 쓸 때 읽는 기획 문서라, 여기 남아 있으면 다음에 다시 쓰는 사람이
옛 색을 되살린다. 실제로 이번에 갈라진 값들이 그렇게 생겼다.

치수선은 **흰색 7번**이다(사내 정본 교안 26쪽). 그래서 「보라색 투상선」이라는
설명도 사실이 아니다 — 투상선은 치수선 레이어에 긋고, 그 레이어는 흰색이다.
화면에서 그것을 형상과 구별하는 근거는 색이 아니라 **외형선이 초록**이라는 것이다.

    python scripts/patches/p10_no_purple.py [--dry-run]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CUR = os.path.join(ROOT, "scripts", "selfstudy", "source", "curriculum.json")

EDITS = [
    ("외형선 Continuous 흰색7 0.5, 중심선 CENTER 빨강1 0.25 축척 0.5, 숨은선 HIDDEN 노랑2 0.25 축척 0.5, 치수선 Continuous 보라6 0.25.",
     "외형선 Continuous 초록3 0.30, 중심선 CENTER 빨강1 0.15 축척 0.5, 숨은선 HIDDEN 노랑2 0.15 축척 0.5, 치수선 Continuous 흰색7 0.15."),
    ("영상 프레임 7 화면 표와 정본 값이 어긋나므로 정본을 확정하기 전에는 이 표를 확정 인쇄하지 않습니다(openQuestions).",
     "정본은 course-standards.json 이고 근거는 사내 정본 교안 26쪽입니다. 값을 여기 다시 적지 않습니다."),
    ("세 뷰 위에 수직 투상선 일곱과 수평 투상선 일곱을 보라색으로 겹쳐 그리고,",
     "세 뷰 위에 수직 투상선 일곱과 수평 투상선 일곱을 가는 선으로 겹쳐 그리고,"),
    ("② 뷰 밖으로 튀어나온 보라색 투상선이 보임(안 보이면 5차시에서 이미 지웠거나 치수선 레이어가 꺼진 채로 저장된 것)",
     "② 뷰 밖으로 튀어나온 투상선이 보임 — 형상은 초록이고 투상선은 흰색이라 색으로 갈립니다(안 보이면 5차시에서 이미 지웠거나 치수선 레이어가 꺼진 채로 저장된 것)"),
    ("F3 → 치수선 레이어를 현재로(색은 보라 6번) →",
     "F3 → 치수선 레이어를 현재로(색은 흰색 7번) →"),
    ("치수 하나를 클릭해 레이어 표시가 치수선(보라 6번)인가,",
     "치수 하나를 클릭해 레이어 표시가 치수선(흰색 7번)인가,"),
    ("치수와 보조선을 그리는 가는 실선입니다. 보라 6번, 굵기 0.25.",
     "치수와 보조선을 그리는 가는 실선입니다. 흰색 7번, 선가중치 0.15."),
    # 같은 문단의 외형선 설명도 옛 값이다.
    ("눈에 보이는 모양을 그리는 굵은 실선입니다. 이 과정에서는 흰색 7번, 굵기 0.5로 넷 중 이것만 굵습니다.",
     "눈에 보이는 모양을 그리는 굵은 실선입니다. 이 과정에서는 초록 3번, 선가중치 0.30 으로 넷 중 이것만 굵습니다."),
]


def main():
    dry = "--dry-run" in sys.argv
    body = io.open(CUR, encoding="utf-8").read()
    miss = 0
    for old, new in EDITS:
        if old not in body:
            if new in body:
                print("  = 이미 적용됨  「%s…」" % old[:40])
            else:
                print("  ✗ 못 찾음      「%s…」" % old[:40])
                miss += 1
            continue
        body = body.replace(old, new)
        print("  ✓ 「%s…」" % old[:40])
    if miss:
        print("\n앵커 %d건을 못 찾았다. 쓰지 않는다." % miss)
        return 1
    left = body.count("보라")
    print("\n남은 「보라」 %d건" % left)
    if dry:
        print("--dry-run — 쓰지 않았다.")
        return 0
    io.open(CUR, "w", encoding="utf-8", newline="\n").write(body)
    return 0 if left == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
