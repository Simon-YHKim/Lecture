# -*- coding: utf-8 -*-
"""기획 문서의 옛 방법과 옛 규격을 걷는다 — 핸드오프 큐 D.

`curriculum.json` 은 자습본을 다시 쓸 때 읽는 설계 문서다. 학습자에게 직접
나가지는 않지만, 여기 옛 값이 남아 있으면 다시 쓰는 사람이 그것을 되살린다.
이번에 갈라진 값들이 실제로 그렇게 생겼다 — 그래서 `check-standards.py` 가
이 파일도 함께 보게 하고, 걸린 열아홉 곳을 여기서 고친다.

바뀐 것 둘
  방법  절대·상대·상대극 좌표 → 객체 스냅 · 직교와 수치 · 스냅 추적과 FROM · 자유 클릭
  규격  선가중치 0.5/0.25 → 0.30/0.15 (사내 정본 교안 26쪽)

용어 사전(glossary)의 「절대좌표」·「상대좌표」 항목은 **지우지 않는다.** 학습자가
남의 도면이나 다른 교재에서 그 말을 만나기 때문이다. 대신 「이 과정은 쓰지
않는다」를 붙여, 읽을 줄은 알되 손은 스냅으로 가게 한다.

    python scripts/patches/p11_curriculum_method.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CUR = os.path.join(ROOT, "scripts", "selfstudy", "source", "curriculum.json")

EDITS = [
    ("절대좌표·상대좌표·상대극좌표를 구분해 쓰고, 눈대중 없이 값으로 형상을 그릴 수 있습니다.",
     "객체 스냅·직교와 수치 입력·스냅 추적을 구분해 쓰고, 눈대중 없이 형상 위에서 점을 잡아 그릴 수 있습니다."),
    ("절대좌표 x,y · 상대좌표 @dx,dy · 상대극좌표 @거리<각도를 구분해 쓰고 각각을 언제 쓰는지 근거를 들어 고를 수 있습니다.",
     "객체 스냅(F3) · 직교와 수치 입력(F8·F12) · 스냅 추적과 FROM(F11) · 자유 클릭 넷을 구분해 쓰고, 그 점이 도면 치수에 걸려 있는지로 넷 중 하나를 고를 수 있습니다."),
    ("좌표 오독 · 골뱅이 누락 · 레이어 미변경 · 접점 스냅 꺼짐 네 가지 실수를 화면에서 알아차리고 그 자리에서 고칠 수 있습니다.",
     "치수 오독 · 직교 꺼짐 · 레이어 미변경 · 접점 스냅 꺼짐 네 가지 실수를 화면에서 알아차리고 그 자리에서 고칠 수 있습니다."),
    ("표 하나에 세 행 — 절대좌표 x,y(원점에서 재는 자리. 시작점과 원 중심), 상대좌표 @dx,dy(앞에 찍은 점에서 얼마나 갔는지. 이어지는 변), 상대극좌표 @거리<각도(방향과 거리가 도면에 그대로 적혀 있을 때). 각 행에 이 차시에서 실제로 치는 값을 예로 답니다. 각도 기준(0도 오른쪽, 90도 위, 135도 왼쪽 위, 180도 왼쪽)을 시계 그림으로 붙입니다. 모따기를 @7.07<135로도 그릴 수 있지만 7.07은 반올림값이고 도면에 적힌 값은 5와 5라는 판단까지 씁니다.",
     "표 하나에 네 행 — 객체 스냅 F3(형상의 특징점에 붙여 찍는다. 밑변 중간점·중심선 교차점·보스 원 접점), 직교와 수치 F8·F12(방향은 마우스, 길이는 숫자. 중심선 두 개), 스냅 추적과 FROM F11(특징점에서 뻗은 안내선의 교차로 형상에 없는 점을 만든다), 자유 클릭(도면 치수에 걸리지 않은 점. 외곽의 첫 구석). 각 행에 이 차시에서 실제로 하는 손동작을 예로 답니다. 고르는 기준은 하나 — 그 점이 도면 치수에 걸려 있는가입니다. 모따기는 사각형을 먼저 세우고 CHAMFER 로 자르므로 11·115 같은 계산값이 나올 자리가 없다는 판단까지 씁니다."),
    ("실수 목록은 좌표 오독 · 골뱅이 누락 · 레이어 미변경 · 접점 스냅 꺼짐입니다.",
     "실수 목록은 치수 오독 · 직교 꺼짐 · 레이어 미변경 · 접점 스냅 꺼짐입니다."),
    ("골뱅이(@)를 빠뜨려 상대좌표가 절대좌표로 읽혔습니다. 폴리선 명령이 진행 중이면 U 엔터로 마지막 한 점만 취소하고, 명령을 이미 빠져나왔으면 Ctrl+Z입니다.",
     "직교가 꺼진 채로 길이만 쳐서 선이 반 도쯤 기울었습니다. 명령이 진행 중이면 U 엔터로 마지막 한 점만 취소하고, 명령을 이미 빠져나왔으면 Ctrl+Z입니다."),
    ("② 레이어 넷(외형선만 굵기 0.5, 나머지 0.25. 선 종류 축척은 중심선과 숨은선에만 0.5)",
     "② 레이어 넷(외형선만 선가중치 0.30, 나머지 0.15. 선 종류 축척은 중심선과 숨은선에만 0.5)"),
    ("앞에 찍은 점에서 얼마나 갔는지를 @dx,dy로 쓰는 입력입니다. 골뱅이를 빼먹으면 절대좌표로 읽혀 선이 엉뚱한 데로 튑니다.",
     "앞에 찍은 점에서 얼마나 갔는지를 @dx,dy로 쓰는 입력입니다. 남의 도면이나 다른 교재에서 만나므로 읽을 줄은 알아 둡니다. 이 과정은 쓰지 않아요 — 같은 자리를 객체 스냅과 수치 입력으로 잡습니다."),
    ("잡은 점에서 상대좌표만큼 떨어진, 도면에 점이 없는 자리를 찍을 때",
     "잡은 점에서 방향과 거리를 주어, 도면에 점이 없는 자리를 찍을 때"),
]

# 용어 사전 항목 — 지우지 않고 「이 과정은 쓰지 않는다」를 붙인다.
GLOSSARY_TAIL = {
    "절대좌표": " 이 과정은 쓰지 않아요. 용지선 두 구석만 예외입니다.",
}


def main():
    dry = "--dry-run" in sys.argv
    body = io.open(CUR, encoding="utf-8").read()
    miss = 0
    for old, new in EDITS:
        if old not in body:
            print("  %s  「%s…」" % ("= 이미 적용됨" if new in body else "✗ 못 찾음", old[:38]))
            miss += 0 if new in body else 1
            continue
        body = body.replace(old, new)
        print("  ✓ 「%s…」" % old[:38])
    if miss:
        print("\n앵커 %d건을 못 찾았다. 쓰지 않는다." % miss)
        return 1

    doc = json.loads(body)

    def walk(node):
        if isinstance(node, dict):
            term = (node.get("term") or node.get("ko")) if "def" in node or "ko" in node else None
            for k, v in node.items():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(doc)
    if dry:
        print("\n--dry-run — 쓰지 않았다.")
        return 0
    io.open(CUR, "w", encoding="utf-8", newline="\n").write(body)
    json.loads(body)
    print("\ncurriculum.json 을 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
