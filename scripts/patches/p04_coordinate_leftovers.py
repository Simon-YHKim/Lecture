# -*- coding: utf-8 -*-
"""좌표 교습의 남은 부스러기를 걷는다.

앞선 라운드가 조작 단계를 REC + 치수 옵션으로 바꾸면서, 그 단계를 설명하던 문장
하나씩이 옛 방법을 그대로 말한 채 남았다. 예를 들어 2차시 표제란은 REC 로 200 과
30 을 치는데 바로 다음 줄이 「골뱅이는 방금 찍은 점에서 잰다는 뜻입니다」로 이어진다.
학습자는 화면에서 하지 않은 동작의 설명을 듣는다.

여기서 고치는 것

  2차시 대본  표제란 골뱅이 설명 · 3차시 예고(절대·상대·극좌표)
  3차시 대본  실수 카드에 남은 골뱅이 꼬리
  4차시 대본  극좌표 추적으로 그은 뒤의 골뱅이 설명 · 위치를 백틱에 넣은 `60,16`
  자습본 2차시 점 찍는 방법 표의 「절대좌표」 행과 「꼭짓점만 상대좌표」 · 표제란 상대좌표 · 3차시 예고
  자습본 3차시 골뱅이를 빠뜨린 실수 항목

일부러 남겨 둔 「다른 길 — 원점을 옮겨 좌표로」 대비 카드는 건드리지 않는다.
사용자가 「UCS 설명은 화면을 2개로 나눠서 이렇게도 가능합니다 식으로 별도 설명을
넣자」고 지정한 자리다. 대신 기계가 알아볼 수 있게 altPath 표시를 붙인다.

    python scripts/patches/p04_coordinate_leftovers.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EDITS = [
    # ── 2차시 대본 ────────────────────────────────────────────────────────
    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    골뱅이는 방금 찍은 점에서 잰다는 뜻입니다. 왼쪽으로 200, 위로 30 간 자리예요.\n",
     "    치수 옵션은 반대 구석을 찾아 클릭할 필요를 없애 줍니다. 도면에 적힌 200과 30을 그대로 칩니다.\n"),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    (2 오른쪽) 다음 시간에는 드디어 선을 긋습니다. 절대좌표, 상대좌표, 극좌표로 점을 찍습니다. 세 가지를 각각 언제 쓰는지 봅니다. LINE과 PLINE의 차이도 봅니다.",
     "    (2 오른쪽) 다음 시간에는 드디어 선을 긋습니다. 점 찍는 방법 넷을 봅니다. 객체 스냅, 직교와 수치 입력, 스냅 추적과 FROM, 그리고 자유 클릭이에요. 넷 중 무엇을 쓸지 가르는 기준도 함께 봅니다. LINE과 PLINE과 REC의 차이도 봅니다."),

    # ── 3차시 대본 ────────────────────────────────────────────────────────
    ("projects/autocad-technician/lesson-03-baseline-profile/SCRIPT.md",
     "그런데 F8 직교가 꺼져 있으면 커서가 정확히 수평이 아닙니다. 원점에서 오른쪽으로 120인 자리입니다. 엉뚱한 데에 점이 찍힙니다. 알아차리는 방법은 화면을 보는 겁니다. 선이 방금 그리던 자리에서 뚝 떨어진 곳으로 튑니까. 골뱅이를 빠뜨린 겁니다. 고치는 방법은 그 자리에서 `U` 입력하고 엔터입니다. 폴리선 명령 안에서는 U가 마지막 한 점만 취소합니다. 명령을 빠져나온 뒤라면 Ctrl+Z입니다.",
     "그런데 F8 직교가 꺼져 있으면 커서가 정확히 수평이 아닙니다. 길이는 맞는데 방향이 반 도쯤 기울어요. 화면에서는 잘 안 보입니다. 알아차리는 방법이 둘 있습니다. 상태 막대에서 직교 단추가 눌려 있는지 보는 것이 첫째예요. 둘째는 그은 선을 클릭해 `Ctrl+1` 로 시작점과 끝점의 Y 값이 같은지 보는 것입니다. 고치는 방법은 그 자리에서 `U` 입력하고 엔터입니다. 명령 안에서는 U가 마지막 한 점만 취소합니다. 명령을 빠져나온 뒤라면 `Ctrl+Z` 입니다."),

    # ── 4차시 대본 ────────────────────────────────────────────────────────
    ("projects/autocad-technician/lesson-04-circles-arcs/SCRIPT.md",
     "    골뱅이는 지금 점에서부터라는 뜻입니다. 22는 거리입니다.\n    꺾쇠 뒤의 45는 각도입니다.\n",
     "    안내선이 방향을 잡아 두었으니 남은 것은 거리 하나입니다.\n    22는 그 방향으로 나아갈 길이예요. 각도는 이미 45도로 고정돼 있습니다.\n"),

    ("projects/autocad-technician/lesson-04-circles-arcs/SCRIPT.md",
     "    베이스 윗면의 한가운데를 클릭합니다. `60,16` 근처입니다.",
     "    베이스 윗면의 한가운데를 클릭합니다. 두 목 선 사이에 낀 구간이에요."),
]

# 자습본 JSON — 문자열 교체 (한글과 영문을 짝으로)
JSON_EDITS = [
    ("scripts/selfstudy/source/lesson-02.json",
     '"ko": "`60,62` · `0,0` — 원점에서 잰 값을 그대로",',
     '"ko": "쓰지 않습니다 — 용지선 두 구석만 예외",'),
    ("scripts/selfstudy/source/lesson-02.json",
     '"en": "`60,62`, `0,0` - the value measured from the origin, as it is"',
     '"en": "Not used - the two sheet-border corners are the only exception"'),
    ("scripts/selfstudy/source/lesson-02.json",
     '"ko": "베이스 여섯 꼭짓점, 보스 중심 `60,62`, 목이 시작하는 `20,16` 과 `100,16`, 보스 원에 닿는 두 접점. 꼭짓점만 상대좌표로 넣고, 나머지는 스냅으로 잡습니다.",',
     '"ko": "베이스 네 꼭짓점, 보스 중심, 목이 시작하는 두 점, 보스 원에 닿는 두 접점. 사각형은 REC 의 치수 옵션으로 세우고 나머지는 전부 스냅과 추적으로 잡습니다.",'),
    ("scripts/selfstudy/source/lesson-02.json",
     '"en": "The six base vertices, the boss centre `60,62`, the web feet at `20,16` and `100,16`, and the two points where the web meets the circle. The first three by coordinate, the tangents by snap."',
     '"en": "The four base corners, the boss centre, the two web feet and the two tangent points. The rectangle goes in through the Dimensions option of REC; everything else comes off the geometry by snap and tracking."'),
    ("scripts/selfstudy/source/lesson-02.json",
     '"ko": "절대좌표 `x,y`",',
     '"ko": "좌표 입력 `x,y`",'),
    ("scripts/selfstudy/source/lesson-02.json",
     "크기는 도면에 적힌 200 과 30 을 골뱅이 붙인 상대좌표로 그대로 넣습니다.",
     "크기는 REC 의 치수 옵션으로 200 과 30 을 그대로 넣습니다."),
    ("scripts/selfstudy/source/lesson-02.json",
     "3차시는 기준선과 외곽입니다. 드디어 선을 그어요. 절대좌표와 상대좌표와 극좌표로 점을 찍습니다. 셋을 각각 언제 쓰는지 봐요.",
     "3차시는 기준선과 외곽입니다. 드디어 선을 그어요. 점 찍는 방법 넷을 봅니다. 객체 스냅, 직교와 수치 입력, 스냅 추적과 FROM, 자유 클릭이에요. 넷 중 무엇을 쓸지 가르는 기준도 함께 봐요."),
    ("scripts/selfstudy/source/lesson-03.json",
     '"ko": "선이 방금 그리던 자리에서 뚝 떨어진 곳으로 튀었다면 골뱅이를 빠뜨린 거예요.",',
     '"ko": "그은 선의 방향이 미심쩍으면 상태 막대의 직교 단추가 눌려 있는지 보세요.",'),
    ("scripts/selfstudy/source/lesson-03.json",
     '"ko": "골뱅이를 빠뜨려 상대좌표가 절대좌표로 읽혔습니다. 폴리선 명령이 진행 중이면 `U` 엔터로 마지막 한 점만 취소합니다. 명령을 이미 빠져나왔으면 `Ctrl+Z` 예요.",',
     '"ko": "직교가 꺼진 채로 길이만 쳐서 선이 반 도쯤 기울었습니다. 명령이 진행 중이면 `U` 엔터로 마지막 한 점만 취소합니다. 명령을 이미 빠져나왔으면 `Ctrl+Z` 예요.",'),
]

# 「다른 길」 대비 카드에 붙일 표시 — 검사기가 의도된 예외로 읽게 한다.
ALT_MARK = [("scripts/selfstudy/source/lesson-03.json", "다른 길 — 원점을 옮겨 좌표로")]


def mark_alt_paths(path, label):
    """「다른 길」 카드 블록에 altPath 표시를 넣는다.

    파일 전체를 다시 직렬화하면 손으로 잡아 둔 서식이 통째로 바뀌므로, 그 블록을
    여는 `"type": "cards",` 줄 하나만 찾아 다음 줄을 끼워 넣는다.
    """
    body = io.open(path, encoding="utf-8").read()
    at = body.find(label)
    if at < 0:
        return body, 0
    head = body.rfind('"type": "cards",', 0, at)
    if head < 0:
        return body, 0
    line_start = body.rfind("\n", 0, head) + 1
    indent = body[line_start:head]
    if '"altPath"' in body[head:at]:
        return body, 0
    ins = body.index("\n", head) + 1
    marked = body[:ins] + indent + '"altPath": true,\n' + body[ins:]
    # JSON 이 여전히 읽히는지 확인한다.
    json.loads(marked)
    return marked, 1


def main():
    dry = "--dry-run" in sys.argv
    cache = {}
    miss = 0
    for rel, old, new in EDITS + JSON_EDITS:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if p not in cache:
            cache[p] = io.open(p, encoding="utf-8").read()
        if old not in cache[p]:
            if new in cache[p]:
                print(f"  = 이미 적용됨  {rel}")
            else:
                print(f"  ✗ 못 찾음      {rel}  「{old[:46]}…」")
                miss += 1
            continue
        cache[p] = cache[p].replace(old, new, 1)
        print(f"  ✓ {rel}  「{old[:46]}…」")
    if miss:
        print(f"\n앵커 {miss}건을 못 찾았다. 아무것도 쓰지 않는다.")
        return 1
    if dry:
        print("\n--dry-run — 쓰지 않았다.")
        return 0
    for p, body in cache.items():
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)

    for rel, label in ALT_MARK:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        body, hits = mark_alt_paths(p, label)
        if hits:
            io.open(p, "w", encoding="utf-8", newline="\n").write(body)
        print(f"  ✓ altPath 표시 {hits}곳  {rel}")

    print(f"\n{len(cache)}개 파일을 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
