# -*- coding: utf-8 -*-
"""몰려 있는 대구를 푼다 — humanize-korean 룰북 C-8.

검수 요청 (전 차시 공통 2) 로 설치한 `humanize-korean` v2.3.2 의 정량 지표를
전 문서에 돌렸다. 결과는 열여섯 파일 전부 `risk_band: low` (점수 0~3) 였지만,
두 축이 실제로 나빴다.

    종결 다양성  0.031 ~ 0.108   (문장이 같은 꼴로 끝난다)
    대구 반복    파일당 최대 18   (「A가 아니라 B」)

C-8 규칙은 「2회+ 반복이면 한 번만 살리고 나머지는 비대칭 평서문으로. **전멸
금지** — 사람 필자도 다용하는 수사이므로 연쇄로 몰려 있지 않으면 보존 우선」이다.
그래서 전체 110개를 다 걷지 않고, **1500자 안에 셋 이상 몰린 일곱 구간**만 골라
묶음마다 가장 뜻이 살아 있는 하나를 남기고 나머지를 평서문으로 편다.

남기는 쪽을 고른 기준은 「그 대비가 정보를 나르는가」다.
「남길 쪽이 아니라 없앨 쪽을 클릭합니다」는 대비 자체가 지시라서 남긴다.
「선 전체가 아니라 일부만 없앤다」는 대비 없이도 같은 말이라 편다.

    python scripts/patches/p14_humanize_antithesis.py [--dry-run]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

L6 = "projects/autocad-technician/lesson-06-editing-symbols/SCRIPT.md"
L7 = "projects/autocad-technician/lesson-07-dimensioning-release/SCRIPT.md"
S4 = "scripts/selfstudy/source/lesson-04.json"
S7 = "scripts/selfstudy/source/lesson-07.json"

EDITS = [
    # ── 6차시 대본 ────────────────────────────────────────────────────────
    (L6, "선 전체가 아니라 일부만 없애야 하기 때문이에요.",
     "선의 일부만 없애야 하기 때문이에요."),
    (L6, "스냅으로 잡은 점은 눈대중이 아니라 정확한 점이에요.",
     "스냅으로 잡은 점은 값이 정확합니다."),
    (L6, "객체 유형이 구성선이 아니라 그대로 남아요.",
     "객체 유형이 구성선으로 안 잡혀서 그대로 남아요."),
    (L6, "선 전체가 아니라 경계와 경계 사이의 한 구간만 없어집니다.",
     "경계와 경계 사이의 한 구간만 없어집니다."),

    # ── 7차시 대본 ────────────────────────────────────────────────────────
    (L7, "그래서 90의 두 번째 점은 모서리가 아니라 원의 위쪽 사분점입니다.",
     "그래서 90의 두 번째 점은 원의 위쪽 사분점입니다. 모서리를 찍으면 값이 달라져요."),
    (L7, "지름 앞에 PCD를 붙여 이게 구멍이 아니라고 표시합니다.",
     "지름 앞에 PCD를 붙여 이게 구멍이 아님을 표시합니다."),
    (L7, "각도 치수는 점이 아니라 선 두 개를 골라 그 사이를 잽니다.",
     "각도 치수는 점을 찍지 않습니다. 선 두 개를 골라 그 사이를 재요."),
    (L7, "화면이 아니라 종이 기준으로 확인하는 습관이 남아야 합니다.",
     "종이 기준으로 확인하는 습관이 남아야 합니다."),
    (L7, "선 종류·색상을 개체가 아니라 레이어로 정할 때 씁니다.",
     "선 종류·색상을 레이어로 정할 때 씁니다."),

    # ── 자습본 ────────────────────────────────────────────────────────────
    (S4, "오프셋은 지름이 아니라 반지름을 밉니다.",
     "오프셋이 미는 것은 반지름입니다."),
    (S7, "최종 판정은 화면이 아니라 종이입니다.",
     "최종 판정은 종이에서 납니다."),
    (S7, "선형 치수가 직선거리가 아니라 치수선 방향의 성분만 재기 때문입니다.",
     "선형 치수는 치수선 방향의 성분만 재기 때문입니다."),
]

# 남기기로 한 것 — 대비 자체가 정보를 나르는 문장이다. 다음에 누가 또 지우지
# 않도록 여기 적어 둔다.
KEEP = [
    "도면이 지시가 아니라 그림이 돼요.",
    "남길 쪽이 아니라 **없앨 쪽**을 클릭합니다.",
    "위쪽 변이 아니라 바닥 변에서 잽니다.",
    "도면은 그림이 아니라 지시 문서입니다.",
    "경사면의 실제 길이 7 이 아니라 5 로",
]


def main():
    dry = "--dry-run" in sys.argv
    cache, miss = {}, 0
    for rel, old, new in EDITS:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        cache.setdefault(p, io.open(p, encoding="utf-8").read())
        if old not in cache[p]:
            if new in cache[p]:
                print("  = 이미 적용됨  「%s…」" % old[:34])
            else:
                print("  ✗ 못 찾음      %s 「%s…」" % (os.path.basename(rel), old[:34]))
                miss += 1
            continue
        cache[p] = cache[p].replace(old, new, 1)
        print("  ✓ 「%s…」" % old[:38])
    if miss:
        print("\n앵커 %d건을 못 찾았다. 쓰지 않는다." % miss)
        return 1
    print("\n남긴 대구 %d개 — 대비가 정보를 나르는 문장" % len(KEEP))
    if dry:
        print("--dry-run — 쓰지 않았다.")
        return 0
    for p, body in cache.items():
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)
    print("%d개 파일을 고쳤다. 6·7차시 대본이 바뀌었으므로 TTS 재합성이 뒤따른다." % len(cache))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
