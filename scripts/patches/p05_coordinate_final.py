# -*- coding: utf-8 -*-
"""좌표 정리의 마지막 네 곳.

  자습본 3차시 앞머리 요약 두 줄이 아직 「절대좌표는 하나도 없습니다」 · 「나머지는
  도면에 적힌 숫자를 상대좌표로 넣습니다」로 되어 있었다. 앞줄은 옳지만 좌표라는
  말로 설명하고 있고, 뒷줄은 이제 사실이 아니다.

  「점을 찍는 네 가지 방법이 한 도형 안에서 다 나왔습니다 … 좌표는 전부
  상대좌표였어요」도 같은 이유로 사실이 아니다.

  4차시 조작 한 줄이 위치를 백틱에 넣어 `60,16` 이라 적어, 학습자가 그대로 치게
  만들고 있었다. 대본에서는 p04 가 고쳤고 자습본에도 같은 줄이 있다.

  UCS 대비 카드에 딸린 「언제 옮길 만한가」 주석은 그 카드와 한 덩어리인데 블록이
  달라 altPath 밖에 있었다. 표시를 붙인다.
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EDITS = [
    ("scripts/selfstudy/source/lesson-03.json",
     '"ko": "스냅으로 잡을 것이 있으려면 형상이 먼저 있어야 합니다. 외곽이 서면 중심선도 보스 중심도 목 접점도 전부 형상에서 나와요. 오늘 치는 절대좌표는 하나도 없습니다.",',
     '"ko": "스냅으로 잡을 것이 있으려면 형상이 먼저 있어야 합니다. 외곽이 서면 중심선도 보스 중심도 목 접점도 전부 형상에서 나와요. 오늘 치는 숫자는 도면에 적힌 치수뿐입니다.",'),
    ("scripts/selfstudy/source/lesson-03.json",
     '"en": "A snap needs something to catch, so the shape has to come first. Once the outline stands, the centerlines, the boss centre and the tangents all come out of it. Not one absolute coordinate is typed today."',
     '"en": "A snap needs something to catch, so the shape has to come first. Once the outline stands, the centerlines, the boss centre and the tangents all come out of it. The only numbers you type today are the dimensions printed on the drawing."'),
    ("scripts/selfstudy/source/lesson-03.json",
     '"ko": "베이스 외곽을 폴리선 하나로 그립니다. 첫 점은 자유 클릭이고, 나머지는 도면에 적힌 숫자를 상대좌표로 넣습니다.",',
     '"ko": "베이스 외곽을 사각형 하나로 세웁니다. 첫 구석은 자유 클릭이고, 가로 120 과 세로 16 은 REC 의 치수 옵션으로 넣습니다. 모따기는 그다음에 CHAMFER 로 자릅니다.",'),
    ("scripts/selfstudy/source/lesson-03.json",
     '"ko": "점을 찍는 네 가지 방법이 한 도형 안에서 다 나왔습니다. 자유 클릭 한 번, 방향과 거리 두 번, 스냅 일곱 번, 좌표는 전부 상대좌표였어요.",',
     '"ko": "점을 찍는 네 가지 방법이 한 도형 안에서 다 나왔습니다. 자유 클릭 한 번, 방향과 거리 두 번, 스냅과 추적 일곱 번, 그리고 치수 옵션으로 준 숫자 둘이에요. 좌표는 한 번도 치지 않았습니다.",'),
    ("scripts/selfstudy/source/lesson-04.json",
     '"ko": "베이스 윗면의 한가운데를 클릭합니다. `60,16` 근처입니다.",',
     '"ko": "베이스 윗면의 한가운데를 클릭합니다. 두 목 선 사이에 낀 구간이에요.",'),
    ("scripts/selfstudy/source/lesson-04.json",
     '"en": "Click the middle of the base top face, near 60,16."',
     '"en": "Click the middle of the base top face - the stretch caught between the two web lines."'),
]

# 「언제 옮길 만한가」 주석도 UCS 대비 카드의 일부다.
ALT_NOTES = [("scripts/selfstudy/source/lesson-03.json", "언제 옮길 만한가")]


def mark_alt(path, label):
    body = io.open(path, encoding="utf-8").read()
    at = body.find(label)
    if at < 0:
        return body, 0
    head = body.rfind('"type": "note",', 0, at)
    if head < 0:
        return body, 0
    line_start = body.rfind("\n", 0, head) + 1
    indent = body[line_start:head]
    if '"altPath"' in body[head:at]:
        return body, 0
    ins = body.index("\n", head) + 1
    marked = body[:ins] + indent + '"altPath": true,\n' + body[ins:]
    json.loads(marked)
    return marked, 1


def main():
    dry = "--dry-run" in sys.argv
    cache, miss = {}, 0
    for rel, old, new in EDITS:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        cache.setdefault(p, io.open(p, encoding="utf-8").read())
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
    for rel, label in ALT_NOTES:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        body, hits = mark_alt(p, label)
        if hits:
            io.open(p, "w", encoding="utf-8", newline="\n").write(body)
        print(f"  ✓ altPath 표시 {hits}곳  {rel} — 「{label}」")
    print(f"\n{len(cache)}개 파일을 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
