# -*- coding: utf-8 -*-
"""5차시 제3각법 단계에 코치 마크를 붙인다 — `three` 바탕을 처음 쓴다.

5차시는 전부 「어느 뷰의 어느 점」을 잡는 일이다. 「평면도 맨 아래 선과 왼쪽
투상선의 교차점」 같은 문장은 정확하지만, 화면에서 그 자리를 찾는 일은 여전히
학습자 몫이다. 사용자 정책 2번이 없애라고 한 것이 바로 그 탐색이다.

좌표는 `coach.py` 가 세 뷰의 자리를 각각 안다. 값은 `master-part-geometry.json`
과 도면 생성기가 실제로 그린 경로에서 확인했다.

    정면도  (58 + x, 208 - y)          부품 좌표 그대로
    평면도  (58 + x, 84 - z)           z=0 앞면이 아래 — 정면도에 가까운 변이 앞면
    우측면도 (224 + z, 208 - y)         z=0 앞면이 왼쪽

    확인한 경로 — 평면도 판 `M58 76 L178 76 L178 64 L58 64 Z` (x 0~120 · z 8~20)
                  평면도 보스 `M90 84 L146 84 L146 76 L90 76 Z` (x 32~88 · z 0~8)
                  우측면도 `M232 208 L244 208 L244 118 L224 118 L224 174 L232 174 Z`

투상선끼리 만나는 자리처럼 부품 위에 없는 점은 `view: raw` 로 SVG 좌표를 쓴다.
45도 선의 원점(224, 84)이 그렇다 — 부품 좌표로 환산하면 아무도 못 읽는 숫자가 된다.

    python scripts/patches/p09_coach_three_view.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "scripts", "selfstudy", "source")


def f(x, y, snap, ko, en):
    """정면도 위의 자리 — 부품 좌표."""
    d = {"x": x, "y": y, "hover": {"ko": ko, "en": en}}
    if snap:
        d["snap"] = snap
    return d


def t(x, z, snap, ko, en):
    """평면도 위의 자리 — 부품 x 와 깊이 z."""
    d = {"view": "top", "x": x, "z": z, "hover": {"ko": ko, "en": en}}
    if snap:
        d["snap"] = snap
    return d


def s(z, y, snap, ko, en):
    """우측면도 위의 자리 — 깊이 z 와 부품 y."""
    d = {"view": "side", "z": z, "y": y, "hover": {"ko": ko, "en": en}}
    if snap:
        d["snap"] = snap
    return d


def r(sx, sy, snap, ko, en):
    """부품 위에 없는 자리 — 도해 좌표를 그대로."""
    d = {"view": "raw", "x": sx, "y": sy, "hover": {"ko": ko, "en": en}}
    if snap:
        d["snap"] = snap
    return d


PLAN = {
    5: ("boss", [
        f(60, 90, "qua", "보스 원의 위쪽 사분점입니다. 마름모 표식이 뜨면 클릭해요. 여기서 높이 90 을 지나는 수평선이 생깁니다.",
          "The top quadrant of the boss circle. Click on the diamond marker. The horizontal construction line through height 90 starts here."),
        t(42, 0, None, "그 선을 30 띄운 자리입니다. 평면도의 맨 아래 선이고 **보스 앞면**이에요. 정면도에 가까운 변이 앞면입니다.",
          "Offset that line by 30 and you get the bottom edge of the top view - the **boss front face**. In third angle the edge nearest the front view is the front."),
        t(60, 8, None, "거기서 다시 8 을 띄우면 **판 앞면**입니다. 보스가 앞으로 8 나와 있으니 판은 그만큼 뒤예요.",
          "Offset 8 more and that is the **plate front face**. The boss stands 8 proud, so the plate sits that far back."),
        t(78, 20, None, "다시 12 를 띄우면 **뒷면**입니다. 판 두께 12 예요. 이 세 줄이 평면도의 깊이를 다 정합니다.",
          "Another 12 gives the **back face** - the 12 plate thickness. Those three lines fix every depth in the top view."),
    ]),
    6: (None, [
        t(0, 0, "int", "보스 앞면 선과 왼쪽 투상선이 만나는 자리입니다. 가위표 표식, 교차점이 뜨면 클릭해요. 가로선의 시작점입니다.",
          "Where the boss-front line crosses the leftmost projector. Click on the cross marker - the intersection. This is where the horizontal starts."),
        t(120, 0, "int", "같은 선과 오른쪽 투상선의 교차점입니다. 폭 전체를 가로지르는 선 하나가 생깁니다.",
          "The same line against the rightmost projector. One line now spans the whole width."),
        t(0, 8, "int", "판 앞면 선 위에도 하나. 가로는 세 줄입니다.",
          "One more along the plate-front line. Three horizontals in all."),
        t(32, 20, "int", "세로줄은 여섯입니다. 5 · 32 · 88 · 115 · 120 과 왼쪽 끝 0 이에요. 정면도에서 올린 투상선이 그 자리를 이미 잡아 두었습니다.",
          "Six verticals: 0, 5, 32, 88, 115 and 120. The projectors raised from the front view already mark them."),
    ]),
    7: (None, [
        t(16, 0, None, "보스 앞면 선에서 32 **왼쪽** 구간입니다. 클릭하면 사라져요. 보스는 32 에서 88 사이에만 있거든요.",
          "The stretch of the boss-front line **left of 32**. Click and it goes - the boss only exists between 32 and 88."),
        t(104, 0, None, "같은 선의 88 **오른쪽** 구간. 같은 이유예요.",
          "The stretch **right of 88** on the same line, for the same reason."),
        t(60, 8, None, "판 앞면 선의 32 와 88 **사이** 구간입니다. 그 구간은 보스가 앞을 덮고 있어요.",
          "The stretch of the plate-front line **between 32 and 88**. The boss covers it from the front."),
        t(0, 4, None, "왼쪽 세로선의 맨 아래 8 구간. 판의 양 끝에는 보스가 없습니다.",
          "The lowest 8 of the left vertical. There is no boss at the ends of the plate."),
        t(32, 14, None, "32 세로선에서 판 앞면보다 **위쪽** 구간. 보스 단차는 앞으로 나온 8 안에만 있어요.",
          "On the 32 vertical, the stretch **above** the plate front. The boss step lives only in the 8 that stands proud."),
    ]),
    8: (None, [
        f(120, 90, None, "정면도 오른쪽 끝에서 올린 수직 투상선입니다. 이 선을 30 오른쪽으로 띄우면 우측면도의 맨 왼쪽 선이 돼요.",
          "The projector raised from the right end of the front view. Offset it 30 to the right and it becomes the leftmost line of the side view."),
        r(224, 84, "int", "그 세로선과 평면도 맨 아래 선이 만나는 자리입니다. 두 뷰의 **앞면끼리** 만나는 점이에요. 45도 선이 여기서 출발합니다.",
          "Where that vertical meets the bottom line of the top view - the point where the two views' **front faces** meet. The 45-degree line starts here."),
        r(232, 76, "int", "45도 선과 평면도 판 앞면 선의 교차점. 우측면도 왼쪽 선에서 8 떨어진 자리가 됩니다.",
          "Where the 45-degree line crosses the plate-front line of the top view. That lands 8 from the left edge of the side view."),
        r(244, 64, "int", "45도 선과 뒷면 선의 교차점. 20 떨어진 자리예요. 깊이가 이렇게 평면도에서 우측면도로 건너갑니다.",
          "Where it crosses the back line - 20 across. This is how depth travels from the top view to the side view."),
    ]),
    10: (None, [
        s(8, 0, "int", "판 앞면 세로선과 바닥선의 교차점입니다. 첫 점이에요.",
          "Where the plate-front vertical meets the base line. That is your first point."),
        s(20, 0, "int", "뒷면 세로선과 바닥선의 교차점.",
          "Where the back vertical meets the base line."),
        s(20, 90, "int", "뒷면 세로선과 90 선의 교차점. 부품의 맨 위입니다.",
          "Where the back vertical meets the 90 line - the top of the part."),
        s(0, 90, "int", "보스 앞면 세로선과 90 선의 교차점.",
          "Where the boss-front vertical meets the 90 line."),
        s(0, 34, "int", "보스 앞면 세로선과 34 선의 교차점. 보스 원의 아래쪽 사분점에서 온 높이예요.",
          "Where the boss-front vertical meets the 34 line - the height that came from the bottom quadrant of the boss circle."),
        s(8, 34, "int", "판 앞면 세로선과 34 선의 교차점. 여기서 `C` 를 치면 시작점까지 닫히면서 끝납니다.",
          "Where the plate-front vertical meets the 34 line. Type `C` here and it closes back to the start."),
    ]),
    11: ("bossc", [
        t(60, 0, "int", "60 수직 투상선과 평면도 보스 앞면 선의 교차점입니다. `FROM` 의 기준점이에요.",
          "Where the 60 projector crosses the boss-front line of the top view. This is the base point for `FROM`."),
        t(60, -5, None, "커서를 그 점의 **아래**에 두고 5 를 칩니다. 중심선이 형상 밖으로 나오는 몫이에요.",
          "Put the cursor **below** it and type 5 - the overhang the centerline needs outside the shape."),
        s(0, 62, "int", "62 수평 투상선과 우측면도 보스 앞면 세로선의 교차점. 우측면도 축 중심선의 기준점입니다.",
          "Where the 62 projector crosses the boss-front vertical of the side view. Base point for the side view's axis centerline."),
        s(0, 8, "int", "8 수평 투상선과 우측면도 판 앞면 세로선의 교차점. 장공 중심선의 기준점이에요.",
          "Where the 8 projector crosses the plate-front vertical. Base point for the slot centerline."),
    ]),
    12: ("bore", [
        f(47.5, 62, "qua", "축 구멍 원의 **왼쪽 사분점**입니다. 47.5 예요. 중심 60 에서 12.5 왼쪽입니다.",
          "The **left quadrant** of the shaft hole - 47.5, which is 12.5 left of the 60 centre."),
        f(72.5, 62, "qua", "**오른쪽 사분점**. 72.5 입니다.",
          "The **right quadrant** - 72.5."),
        t(47.5, 0, "int", "그 투상선과 평면도 보스 앞면 선의 교차점. 숨은선의 시작점이에요.",
          "Where that projector meets the boss-front line of the top view. The hidden line starts here."),
        t(47.5, 20, "int", "같은 투상선과 뒷면 선의 교차점. 구멍이 뚫려 있으니 앞에서 뒤까지 이어집니다.",
          "The same projector against the back line. The hole goes through, so the line runs front to back."),
    ]),
    13: ("bore", [
        f(60, 74.5, "qua", "축 구멍 원의 **위쪽 사분점**입니다. 74.5 예요.",
          "The **top quadrant** of the shaft hole - 74.5."),
        f(60, 49.5, "qua", "**아래쪽 사분점**. 49.5 이고 중심 62 에서 12.5 씩입니다.",
          "The **bottom quadrant** - 49.5. Both are 12.5 from the 62 centre."),
        s(0, 74.5, "int", "보스 앞면 세로선과 위쪽 투상선의 교차점.",
          "Where the boss-front vertical meets the upper projector."),
        s(20, 74.5, "int", "뒷면 세로선과 같은 투상선의 교차점. 두 줄 다 가로로 20 입니다.",
          "The back vertical against the same projector. Both lines run 20 across."),
    ]),
    14: ("tap", [
        f(75.556, 77.556, "cen", "오른쪽 위 탭 원입니다. 사분점 둘을 투상선으로 올려요.",
          "The upper-right tapped hole. Two quadrants go up as projectors."),
        f(44.444, 77.556, "cen", "왼쪽 위 탭 원. 아래쪽 탭 둘은 가로 자리가 같아 같은 선에 겹칩니다.",
          "The upper-left one. The two lower holes share the same across-positions, so they land on the same projectors."),
        t(44.444, 0, "int", "투상선과 평면도 보스 앞면 선의 교차점입니다. 여기서 시작해 **위로 10**.",
          "Where a projector meets the boss-front line. Start here and go **10 up**."),
        t(44.444, 10, None, "탭 깊이 10 만큼만 들어갑니다. 관통이 아니에요 — 도면 표기가 `4-M5 깊이 10` 입니다.",
          "It reaches only the 10 of thread depth. Not a through hole - the drawing says `4-M5 깊이 10`."),
    ]),
    15: ("tap", [
        f(75.556, 88.556, "qua", "위쪽 탭 원의 **위쪽 사분점**입니다. 여기서 수평 투상선을 우측면도로 보냅니다.",
          "The **top quadrant** of an upper tapped hole. A horizontal projector goes from here to the side view."),
        s(0, 88.556, "int", "보스 앞면 세로선과 그 투상선의 교차점. **오른쪽으로 10** 입니다 — 우측면도는 왼쪽이 앞면이라 재료가 오른쪽에 있어요.",
          "Where the boss-front vertical meets it. Go **10 to the right**: in the side view the front is on the left, so material lies to the right."),
        s(0, 62, "end", "우측면도 축 중심선의 **왼쪽 끝점**입니다. 대칭선의 첫 점이에요.",
          "The **left endpoint** of the side view's axis centerline - the first point of the mirror line."),
        s(20, 62, "end", "같은 중심선의 **오른쪽 끝점**. 아래쪽 탭은 다시 그리지 않고 이 축으로 넘깁니다.",
          "The **right endpoint** of the same centerline. The lower holes get mirrored across it instead of redrawn."),
    ]),
    16: ("slot", [
        f(24, 8, "qua", "왼쪽 장공에서 **왼쪽 끝원의 왼쪽 사분점**입니다. 24 예요. 끝원 중심 29 에서 반지름 5 를 뺀 값이에요.",
          "The **left quadrant of the left end circle** of the left slot - 24, which is the 29 end-circle centre less the 5 radius."),
        f(46, 8, "qua", "**오른쪽 끝원의 오른쪽 사분점**. 46 입니다. 41 에 5 를 더한 값이에요.",
          "The **right quadrant of the right end circle** - 46, which is 41 plus 5."),
        t(24, 8, "int", "그 투상선과 평면도 **판 앞면** 선의 교차점입니다. 장공은 판에만 있어 보스 앞면까지 가지 않아요.",
          "Where that projector meets the **plate-front** line. The slot is only in the plate, so it does not reach the boss front."),
        t(24, 20, "int", "같은 투상선과 뒷면 선의 교차점. 두 줄 모두 길이 12 — 판 두께 그대로입니다.",
          "The same projector against the back line. Both lines are 12 long - the plate thickness."),
        t(60, 20, "end", "평면도 축 중심선의 끝점입니다. 오른쪽 장공은 이 축으로 대칭 복사해요. 중심 35 와 85 가 둘 다 60 에서 25 씩이라 정확히 맞습니다.",
          "An endpoint of the top view's axis centerline. The right slot mirrors across it - 35 and 85 are both 25 from 60, so it lands exactly."),
    ]),
}


def main():
    dry = "--dry-run" in sys.argv
    path = os.path.join(SRC, "lesson-05.json")
    doc = json.load(io.open(path, encoding="utf-8"))
    hit, seen = 0, set()
    for sec in doc.get("sections", []):
        for blk in sec.get("blocks", []):
            if blk.get("type") != "steps":
                continue
            for st in blk.get("items", []):
                seen.add(st.get("n"))
                plan = PLAN.get(st.get("n"))
                if not plan:
                    continue
                feature, spots = plan
                if st.get("spots"):
                    print("  = 이미 있음  5차시 %d단계" % st["n"])
                    continue
                st["on"] = "three"
                if feature:
                    st["feature"] = feature
                st["spots"] = spots
                hit += 1
                print("  ✓ 5차시 %2d단계 — 자리 %d" % (st["n"], len(spots)))
    missing = set(PLAN) - seen
    if missing:
        print("  ✗ 없는 단계 번호: %s" % sorted(missing))
        return 1
    if dry:
        print("\n--dry-run — %d단계를 붙일 수 있다. 쓰지 않았다." % hit)
        return 0
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("\n5차시에 코치 마크 %d단계를 붙였다." % hit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
