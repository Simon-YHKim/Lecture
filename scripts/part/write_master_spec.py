"""Regenerate MASTER_DRAWING_SPEC.md from the drawing generator's own output.

The version this replaces described a different part entirely — a sensor
bracket from the superseded ten-lesson course — and had been sitting beside the
current drawing saying otherwise. A specification that can disagree with the
thing it specifies is worse than no specification, so this one is derived from
`master-part-geometry.json`, which `edu_ib_02.py` writes.

    python scripts/part/edu_ib_02.py projects/autocad-technician/master-part-geometry.json --json
    python scripts/part/write_master_spec.py
"""

import io
import json
import os
import sys

ROOT = "projects/autocad-technician"

# 굵기는 밀리미터, 축척은 선 종류의 축척이다. 둘은 다른 것이라 열도 다르다.
LAYERS = [("외형선", "Continuous", "0.5", "—", "흰색 (7)", "보이는 모양"),
          ("중심선", "Center", "0.25", "0.5", "빨강 (1)", "중심과 대칭축"),
          ("숨은선", "Hidden", "0.25", "0.5", "노랑 (2)", "가려진 모양"),
          ("치수선", "Continuous", "0.25", "—", "보라 (6)", "치수 · 보조선")]


def main():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)
    g = json.load(io.open(os.path.join(ROOT, "master-part-geometry.json"), encoding="utf-8"))
    f = g["features"]
    env = g["envelope"]

    def row(name, val, note):
        return "| %s | %s | %s |" % (name, val, note)

    dims = [
        row("전체", "%g × %g" % (env["widthX"], env["heightY"]), "가로 · 높이. 재료를 자르는 크기"),
        row("베이스", "%g × %g" % (f["base"]["width"], f["base"]["height"]),
            "정면에서 본 높이다. 두께가 아니다"),
        row("판 두께", "%g" % (f["base"]["z"][1] - f["base"]["z"][0]), "평면도에서 읽는다"),
        row("보스 자리 두께", "%g" % env["depthZ"], "보스가 앞으로 나온 만큼 두껍다"),
        row("모따기", "2-C%g" % f["chamfer"]["size"], f["chamfer"]["purpose"]),
        row("보스", "Ø%g" % f["boss"]["diameter"],
            "중심 (%g, %g). 앞으로 %g 돌출, 뒷면은 평면"
            % (f["boss"]["centre"][0], f["boss"]["centre"][1], f["boss"]["z"][1])),
        row("축 구멍", "Ø%g %s" % (f["bore"]["diameter"], f["bore"]["fit"]),
            "앞뒤 관통. H7은 드릴로 못 내고 리머가 필요하다"),
        row("탭", "%d-%s 깊이 %g" % (f["taps"]["quantity"], f["taps"]["thread"],
                                   f["taps"]["depth"]),
            "피치원 PCD Ø%g, 첫 구멍 %g도, %g도씩"
            % (f["taps"]["pitchCircleDiameter"], f["taps"]["startAngleDeg"],
               360 / f["taps"]["quantity"])),
        row("장착 장공", "%d-R%g" % (f["slots"]["quantity"], f["slots"]["endRadius"]),
            "폭 %g, 끝원 중심거리 %g, 중심 높이 %g, 볼트 %s"
            % (f["slots"]["width"], f["slots"]["centreDistance"],
               f["slots"]["centres"][0][1], f["slots"]["bolt"])),
        row("목", "밑동 %g" % f["web"]["footSpan"],
            "필렛이 지운 이론 모서리 기준. 보스 원에 접하는 두 직선"),
        row("필렛", "2-R%g" % f["fillet"]["radius"],
            "중심 높이 %g. %s" % (f["fillet"]["centres"][0][1], f["fillet"]["purpose"])),
    ]

    v = g["verification"]
    checks = "\n".join(
        "| `%s` | %s |" % (k, ("%.2e" % val) if isinstance(val, float) else val)
        for k, val in v.items())

    # 깊이 규약은 표로 낸다. 파이썬 dict 를 그대로 찍으면 문서가 아니라 덤프가 된다.
    dc = g["depthConvention"]
    depth_rows = [("bossFront", "보스 앞면 — 보는 사람에게 가장 가깝다"),
                  ("bossPlateBoundary", "보스와 판이 만나는 면"),
                  ("plateBack", "판 뒷면 — 프레임에 밀착한다")]
    depth = ("| z | 위치 |\n| --- | --- |\n"
             + "\n".join("| %g | %s |" % (dc[k], label) for k, label in depth_rows)
             + "\n\n" + dc["note"])

    io.open(os.path.join(ROOT, "MASTER_DRAWING_SPEC.md"), "w",
            encoding="utf-8", newline="\n").write(
        "# %s 정본 도면\n\n" % g["partId"]
        + "**%s.** 일곱 차시가 이 부품 하나를 이어 그린다.\n\n" % g["name"]
        + "> 이 문서는 손으로 쓰지 않는다. `scripts/part/edu_ib_02.py` 가 만든\n"
          "> `master-part-geometry.json` 에서 생성된다. 값을 고치려면 생성기를 고치고\n"
          "> 다시 돌린다. 도면과 문서가 서로 다른 말을 할 수 없게 하기 위해서다.\n\n"
          "    python scripts/part/edu_ib_02.py projects/autocad-technician/master-part-geometry.json --json\n"
          "    python scripts/part/write_master_spec.py\n\n"
          "## 1. 치수\n\n단위 %s.\n\n| 항목 | 값 | 비고 |\n| --- | --- | --- |\n"
          % g["units"]
        + "\n".join(dims)
        + "\n\n## 2. 깊이 규약\n\n%s\n\n" % depth
        + "보스는 **앞으로** 나온다. 뒷면 전체가 프레임에 밀착해야 하기 때문이다.\n"
          "뒤로 튀어나오면 그 부분이 먼저 닿아 나머지 면이 뜬다.\n\n"
          "## 3. 용지와 도면틀\n\n"
          "- A3 가로 420 × 297\n"
          "- 도면선은 용지선에서 **사방 10** 안쪽\n"
          "- 네 변의 한가운데에 중심 마크\n"
          "- 표제란은 오른쪽 아래 **200 × 30**, 100씩 둘로 나눠 **왼쪽 이름 · 오른쪽 사번**\n"
          "- 문자 높이 10\n\n"
          "## 4. 레이어\n\n네 개뿐이다.\n\n"
          "| 레이어 | 선 종류 | 굵기 | 선 종류 축척 | 색상 | 용도 |\n"
          "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join("| %s | %s | %s | %s | %s | %s |" % r for r in LAYERS)
        + "\n\n**굵기**는 밀리미터다. 외형선만 굵은 실선 0.5, 나머지는 가는 선 0.25로\n"
          "2대 1이다. 인쇄물에서 형상이 먼저 읽히는 이유가 이것이다. 화면에서 확인하려면\n"
          "`LWDISPLAY`를 켠다.\n\n"
          "**선 종류 축척**은 굵기가 아니라 점선 간격이다. 그래서 값이 있는 줄은\n"
          "중심선과 숨은선뿐이다. Continuous에는 조정할 간격이 없다.\n\n"
          "치수선 레이어는 치수와 보조선을 함께 쓴다. 둘 다 가는 선이라 굵기가 같다.\n\n"
          "이 값들은 교재를 근거로 한 **연습용 기본값**이다. 실제 과제가 다른 이름·색상·\n"
          "굵기·축척을 지정하면 그 지시가 우선한다 (`LESSON_STYLE.md` 6번).\n\n"
          "## 5. 투상\n\n"
          "제3각법. 정면도 기준으로 위가 평면도, 오른쪽이 우측면도.\n\n"
          "## 6. 생성기가 매번 확인하는 것\n\n"
          "형상은 눈으로 맞추지 않고 풀어서 구한다. 아래 값이 커지면 도면이 틀린 것이다.\n\n"
          "| 검산 | 값 |\n| --- | --- |\n" + checks + "\n\n"
          "`scripts/part/verify_course.py` 가 과정 검사 때 이 값들을 다시 확인한다.\n")
    print("MASTER_DRAWING_SPEC.md 재생성 — %s" % g["partId"])


if __name__ == "__main__":
    sys.exit(main())
