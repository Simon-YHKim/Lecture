# -*- coding: utf-8 -*-
"""코치 마크가 빠져 있던 작도 단계에 도면과 자리 표시를 붙인다.

사용자 정책 2번 — 「작도를 실습하는 슬라이드라면 모두 적용해야 함」.
실습 단계 103개 중 29개에만 붙어 있었다. 남은 74개 중 대화상자·저장·레이어
전환처럼 도면 위에 짚을 것이 없는 단계를 빼면, **도면 위에서 자리를 잡는
단계 열둘**이 남는다. 그 열둘을 여기서 채운다.

2차시 넷은 앞선 핸드오프가 「A3 용지 도해가 없어서 막혔다」고 적었던 자리다.
사실이 아니었다 — 도해는 `sheet_figures.SVG_A3` 에 있었고, 막힌 것은 코치 마크가
정면도 좌표만 알고 용지 좌표를 몰랐던 것이다. `coach.py` 의 `sheet` 바탕이 그것을
푼다. 검수 메모 8~11 이 여기서 닫힌다.

좌표는 지어내지 않았다. 부품 쪽은 `master-part-geometry.json`, 용지 쪽은
`MASTER_DRAWING_SPEC.md` 의 A3 규격(420 × 297 · 사방 10 · 표제란 200 × 30)이다.

    python scripts/patches/p08_coach_marks.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "scripts", "selfstudy", "source")


def sp(x, y, snap, ko, en, **kw):
    d = {"x": x, "y": y, "hover": {"ko": ko, "en": en}}
    if snap:
        d["snap"] = snap
    d.update(kw)
    return d


# 차시 → {단계 번호: (바탕, 강조 형상 또는 None, [자리…])}
PLAN = {
    2: {
        11: ("sheet", "sh-frame", [
            sp(0, 0, None, "용지선의 첫 구석입니다. 여기만 좌표로 `0,0` 을 칩니다 — 아직 잡을 형상이 없거든요.",
               "The first corner of the sheet line. This is one of only two places you type a coordinate, because there is no geometry to snap to yet."),
            sp(420, 297, None, "반대 구석 `420,297`. A3 가로의 크기 그대로입니다.",
               "The opposite corner, `420,297` - the size of a landscape A3 exactly."),
            sp(210, 150, None, "간격띄우기 방향을 묻습니다. 용지선 **안쪽** 아무 데나 클릭하면 도면선이 안으로 생깁니다.",
               "Offset asks which way. Click anywhere **inside** the sheet line and the border lands inward."),
        ]),
        12: ("sheet", "sh-mark", [
            sp(210, 0, "mid", "아래 변에 커서를 올리면 세모 표식이 뜹니다. 중간점이에요. 표식을 보고 나서 클릭합니다.",
               "Rest the cursor on the bottom edge until the triangle appears - that is the midpoint. Click only after you see it."),
            sp(210, 297, "mid", "위 변의 중간점. 여기서 아래로 `30` 입니다.",
               "Midpoint of the top edge. From here you go `30` down."),
            sp(0, 148.5, "mid", "왼쪽 변의 중간점. 오른쪽으로 `30`.",
               "Midpoint of the left edge, then `30` to the right."),
            sp(420, 148.5, "mid", "오른쪽 변의 중간점. 왼쪽으로 `30`.",
               "Midpoint of the right edge, then `30` to the left."),
        ]),
        13: ("sheet", "sh-title", [
            sp(410, 10, "end", "도면선의 오른쪽 아래 모서리입니다. 네모 표식이 뜨면 클릭합니다. 여기서 시작해야 표제란이 도면선에 딱 붙습니다.",
               "The lower-right corner of the border. Click when the square marker appears; starting here is what makes the title block sit flush."),
            sp(310, 40, "mid", "가로 200 세로 30 이 붙은 뒤, 그 위 변의 중간점입니다. 여기서 아래로 `30` 을 그으면 칸이 둘로 나뉩니다.",
               "Once the 200 by 30 box is there, this is the midpoint of its top edge. A line `30` down from here splits it in two."),
        ]),
        15: ("sheet", "sh-title", [
            sp(260, 25, "int", "왼쪽 칸에 그은 X 자가 만나는 자리입니다. 가위표 표식, 교차점이 뜨면 클릭합니다. 이름이 여기 가운데로 들어갑니다.",
               "Where the X you drew across the left cell crosses. Click on the cross marker - the intersection. The name lands centered here."),
            sp(360, 25, "int", "오른쪽 칸도 같은 방법이에요. 사번이 들어갑니다.",
               "Same again in the right cell, for the employee number."),
        ]),
    },
    3: {
        3: ("sheet", None, [
            sp(20, 20, None, "줌 윈도우의 첫 구석입니다. 도면틀 왼쪽 아래 사분면에서 그냥 클릭해요. 치수에 걸린 점이 아니라 아무 데나 됩니다.",
               "The first corner of the zoom window. Just click in the lower-left quadrant of the border - this point is not on any dimension."),
            sp(230, 180, None, "반대 구석. 이 안이 화면을 채웁니다. 작게 놓고 그리면 스냅이 어디에 붙었는지 안 보여요.",
               "The opposite corner. This fills the screen. Draw it small and you cannot see where the snap landed."),
        ]),
        5: ("front", "basehl", [
            sp(60, 0, None, "방금 그린 외곽 위 아무 데나 클릭합니다. 여섯 변이 한꺼번에 파랗게 잡히면 폴리선 하나로 잘 그린 겁니다.",
               "Click anywhere on the outline you just drew. If all six edges highlight at once, it went in as a single polyline."),
        ]),
    },
    4: {
        3: ("front", "boss", [
            sp(60, 90, "qua", "간격띄우기할 객체를 물어봅니다. 보스 Ø56 원의 선을 클릭해요. 위쪽 사분점 근처가 잡기 쉽습니다.",
               "It asks which object to offset. Click the Ø56 boss circle; near the top quadrant is the easiest place to catch it."),
            sp(60, 62, None, "어느 쪽으로 띄울지 물어봅니다. 원 **안쪽** 아무 곳이나 클릭하면 지름 44 피치원이 안쪽에 생깁니다.",
               "It asks which way. Click anywhere **inside** the circle and the Ø44 pitch circle lands inside."),
        ]),
        5: ("front", "tap", [
            sp(75.556, 77.556, "end", "45도 보조선의 바깥쪽 끝입니다. 네모 표식, 끝점이 뜨면 클릭해요. 이 점이 첫 탭 구멍의 중심입니다.",
               "The far end of the 45-degree guide line. Click on the square marker - the endpoint. This is the centre of the first tapped hole."),
        ]),
        10: ("front", "slot", [
            sp(34, 8, None, "왼쪽 장공에서 왼쪽 끝원의 **오른쪽 반**입니다. 장공 안쪽으로 들어간 부분이라 지웁니다.",
               "The **right half** of the left end circle of the left slot - the part that reaches into the slot. That is what goes."),
            sp(36, 8, None, "오른쪽 끝원의 **왼쪽 반**. 같은 이유로 지웁니다. 남는 것은 바깥쪽 반원 둘과 위아래 직선 둘이에요.",
               "The **left half** of the right end circle, for the same reason. What is left is two outer half-circles and two straight sides."),
        ]),
        12: ("front", "basehl", [
            sp(60, 16, None, "베이스 윗면의 한가운데입니다. 두 목 선 사이에 낀 구간이에요. 여기를 클릭하면 그 구간만 사라집니다.",
               "The middle of the base top face - the stretch caught between the two web lines. Click here and only that stretch goes."),
        ]),
        13: ("front", "fillet", [
            sp(110, 16, None, "첫 번째 객체는 윗면의 오른쪽 토막입니다. **남기고 싶은 쪽**을 클릭하세요. 모서리 바깥쪽입니다.",
               "The first object is the right stub of the top face. Click the **side you want to keep** - outward from the corner."),
            sp(100, 30, None, "두 번째 객체는 오른쪽 목 선입니다. 역시 남기고 싶은 쪽, 모서리보다 위쪽을 클릭합니다.",
               "The second object is the right web line. Again click the side you keep - above the corner."),
        ]),
    },
    6: {
        10: ("front", "bossc", [
            sp(60, 62, None, "먼저 원본을 클릭합니다. 제대로 된 중심선, 곧 빨간 파선으로 보이는 선이에요. 커서가 붓 모양으로 바뀝니다.",
               "Click the source first - a centerline that is already right, the one showing as a red dashed line. The cursor turns into a brush."),
            sp(60, 62, None, "그다음 고칠 선을 클릭합니다. 클릭한 선이 원본과 같은 레이어로 옮겨지고 색과 선 종류도 따라 바뀝니다.",
               "Then click the line to fix. It moves to the source's layer and takes its color and linetype."),
        ]),
    },
}


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for no, steps in sorted(PLAN.items()):
        path = os.path.join(SRC, "lesson-%02d.json" % no)
        doc = json.load(io.open(path, encoding="utf-8"))
        hit = 0
        for sec in doc.get("sections", []):
            for blk in sec.get("blocks", []):
                if blk.get("type") != "steps":
                    continue
                for st in blk.get("items", []):
                    plan = steps.get(st.get("n"))
                    if not plan:
                        continue
                    surface, feature, spots = plan
                    if st.get("spots"):
                        print("  = 이미 있음  %d차시 %d단계" % (no, st["n"]))
                        continue
                    if surface != "front":
                        st["on"] = surface
                    if feature:
                        st["feature"] = feature
                    st["spots"] = spots
                    hit += 1
        missing = set(steps) - {st.get("n")
                                for sec in doc.get("sections", [])
                                for blk in sec.get("blocks", [])
                                if blk.get("type") == "steps"
                                for st in blk.get("items", [])}
        if missing:
            print("  ✗ %d차시에 없는 단계 번호: %s" % (no, sorted(missing)))
            return 1
        print("  ✓ %d차시 — 단계 %d개에 코치 마크" % (no, hit))
        total += hit
        if not dry and hit:
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
    print("\n%s%d단계" % ("--dry-run — 쓰지 않았다. " if dry else "붙였다: ", total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
