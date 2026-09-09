# -*- coding: utf-8 -*-
"""레이어 규격을 사내 정본 교안에 맞춘다. 한 번 돌리고 끝나는 스크립트다.

무엇을 왜 고치는가
------------------
2026-09-10 에 사용자가 사내 정본 교안(63쪽, 2026-03-16)을 재첨부했다. 26쪽
「Layer 구성을 그림과 같이 구성해보시오」 의 도면층 관리자 화면이 이 과정이
가르쳐야 할 값의 근거다.

    숨은선  노란색(2)  HIDDEN      0.15
    외형선  초록색(3)  Continuous  0.30   ← 현재 도면층
    중심선  빨간색(1)  CENTER      0.15
    치수선  흰색(7)    Continuous  0.15

그동안 저장소에는 근거 없는 값이 세 갈래로 갈라져 있었다.

    치수선 색 — MASTER_DRAWING_SPEC 「보라 6」 / 2차시 「색상 12번」 /
                lesson-02 영문 「magenta (6)」  ← 같은 항목의 한글과 영문이 서로 달랐다
    외형선 색 — 「흰색 7」 (교안은 초록 3)
    선가중치 — 0.5 / 0.25 (교안은 0.30 / 0.15)

LESSON_STYLE.md 6번이 「규격은 지어내지 않는다 — 원본 교재와 시험 지시를 근거로
한다」고 못 박는다. 교안이 없을 때 채워 넣은 값이므로 교안이 도착한 지금 되돌린다.

두 배 관계는 그대로 살아 있다 — 0.30 대 0.15 도 정확히 두 배다. 그래서 「외형선만
나머지의 두 배」라는 설명은 숫자만 바뀌고 논리는 바뀌지 않는다.

또 하나 — 2차시가 치수선에 「선 종류 축척 0.25」를 넣으라고 시키면서 같은 차시가
「Continuous 에는 조정할 간격이 없다」고 말하고 있었다. 자기모순이라 지운다.

    python scripts/patches/p01_layer_standard.py [--dry-run]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (파일, 옛 문장, 새 문장) — 옛 문장이 없으면 실패한다. 조용한 무동작을 막는다.
EDITS = [
    # ── 2차시 대본 · 레이어 표 낭독 ────────────────────────────────────────
    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "(6 외형선) 외형선은 선 종류 Continuous입니다. 굵기 0.5, 색상 흰색 7번. 눈에 보이는 모양을 그립니다. 넷 중 이것만 굵습니다.",
     "(6 외형선) 외형선은 선 종류 Continuous입니다. 선가중치 0.30, 색상 초록 3번. 눈에 보이는 모양을 그립니다. 넷 중 이것만 굵습니다."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "(7 중심선) 중심선은 Center, 굵기 0.25, 빨강 1번. 원의 중심과 대칭축을 그립니다. 점선 간격을 정하는 선 종류 축척은 0.5입니다.",
     "(7 중심선) 중심선은 CENTER, 선가중치 0.15, 빨강 1번. 원의 중심과 대칭축을 그립니다. 점선 간격을 정하는 선 종류 축척은 0.5입니다."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "(8 숨은선) 숨은선은 Hidden, 굵기 0.25, 노랑 2번. 가려져서 안 보이는 모양을 그립니다. 선 종류 축척은 중심선과 같은 0.5입니다.",
     "(8 숨은선) 숨은선은 HIDDEN, 선가중치 0.15, 노랑 2번. 가려져서 안 보이는 모양을 그립니다. 선 종류 축척은 중심선과 같은 0.5입니다."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "(9 치수선) 치수선은 Continuous, 굵기 0.25, 빨강 계열 12번, 선 종류 축척 0.25입니다. 치수를 기입할 때 씁니다. 뷰를 맞추는 보조선도 여기에 그립니다.",
     "(9 치수선) 치수선은 Continuous, 선가중치 0.15, 흰색 7번입니다. Continuous라 선 종류 축척은 넣지 않습니다. 치수를 기입할 때 씁니다. 뷰를 맞추는 보조선도 여기에 그립니다."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "(10 굵기와 축척 문단) 표에 숫자가 두 종류라 헷갈리기 쉬운 자리입니다. 굵기는 선의 두께이고 단위는 밀리미터입니다. 외형선만 0.5이고 나머지는 0.25로, 정확히 두 배입니다.",
     "(10 굵기와 축척 문단) 표에 숫자가 두 종류라 헷갈리기 쉬운 자리입니다. 선가중치는 선의 두께이고 단위는 밀리미터입니다. 외형선만 0.30이고 나머지는 0.15로, 정확히 두 배입니다."),

    # ── 2차시 대본 · 레이어 만드는 조작 ────────────────────────────────────
    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    색상 선택 대화상자에서 7번 흰색을 고르고 확인.\n"
     "    선 종류 칸은 Continuous 그대로 둡니다.\n"
     "    선가중치 칸을 클릭합니다. 목록에서 `0.50` 밀리미터를 고르고 확인.\n"
     "    넷 중 이 줄만 굵습니다.",
     "    색상 선택 대화상자에서 3번 초록을 고르고 확인.\n"
     "    선 종류 칸은 Continuous 그대로 둡니다.\n"
     "    선가중치 칸을 클릭합니다. 목록에서 `0.30` 밀리미터를 고르고 확인.\n"
     "    넷 중 이 줄만 굵습니다."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    중심선 행입니다. 색상 칸을 클릭해 1번 빨강을 고르고 확인.\n"
     "    선 종류 칸을 클릭해 `CENTER`를 고르고 확인.\n"
     "    선가중치는 `0.25` 밀리미터.",
     "    중심선 행입니다. 색상 칸을 클릭해 1번 빨강을 고르고 확인.\n"
     "    선 종류 칸을 클릭해 `CENTER`를 고르고 확인.\n"
     "    선가중치는 `0.15` 밀리미터."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    숨은선 행. 색상은 2번 노랑. 선 종류는 `HIDDEN`. 선가중치 `0.25`.",
     "    숨은선 행. 색상은 2번 노랑. 선 종류는 `HIDDEN`. 선가중치 `0.15`."),

    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    치수선 행. 색상은 12번 빨강 계열. 중심선이 쓰는 1번 빨강과 번호를 달리해 화면에서 구분됩니다. 선 종류는 Continuous 그대로. 선가중치 `0.25`. 선 종류 축척 `0.25`.",
     "    치수선 행. 색상은 7번 흰색. 외형선이 초록이라 화면에서 둘이 섞이지 않습니다. 선 종류는 Continuous 그대로. 선가중치 `0.15`.\n"
     "    Continuous에는 조정할 간격이 없으니 선 종류 축척은 비워 둡니다."),

    # ── 7차시 대본 ────────────────────────────────────────────────────────
    ("projects/autocad-technician/lesson-07-dimensioning-release/SCRIPT.md",
     "    화면 위 레이어 표시가 치수선으로 바뀌었는지 봅니다. 빨강 계열 12번입니다.",
     "    화면 위 레이어 표시가 치수선으로 바뀌었는지 봅니다. 흰색 7번입니다."),
    ("projects/autocad-technician/lesson-07-dimensioning-release/SCRIPT.md",
     "    문자 색상은 도면층별로 둡니다. 레이어에서 이미 빨강 계열 12번을 줬습니다.",
     "    문자 색상은 도면층별로 둡니다. 레이어에서 이미 흰색 7번을 줬습니다."),

    # ── 자습본 2차시 ──────────────────────────────────────────────────────
    ("scripts/selfstudy/source/lesson-02.json",
     '        "ko": "빨강 계열 12",\n        "en": "red 12"',
     '        "ko": "흰색 7",\n        "en": "white 7"'),
    ("scripts/selfstudy/source/lesson-02.json",
     "외형선만 0.5, 나머지는 0.25 로 정확히 두 배예요.",
     "외형선만 0.30, 나머지는 0.15 로 정확히 두 배예요."),
    ("scripts/selfstudy/source/lesson-02.json",
     "Only the visible line is 0.5 and the rest are 0.25, exactly double.",
     "Only the visible line is 0.30 and the rest are 0.15, exactly double."),
    ("scripts/selfstudy/source/lesson-02.json",
     '"ko": "치수선 행은 색상 12번을 고릅니다. 빨강 계열이라 눈에 띄면서, 중심선이 쓰는 1번 빨강과는 구분돼요. 선 종류는 Continuous 그대로 두고, 선 종류 축척은 0.25 로 넣습니다.",',
     '"ko": "치수선 행은 색상 7번 흰색을 고릅니다. 외형선이 초록 3번이라 화면에서 둘이 섞이지 않아요. 선 종류는 Continuous 그대로 두고, 선가중치는 0.15 입니다. Continuous 에는 조정할 간격이 없으니 선 종류 축척은 비워 둡니다.",'),
    ("scripts/selfstudy/source/lesson-02.json",
     '"en": "On the dimension line row choose magenta (6). Leave the linetype as Continuous."',
     '"en": "On the dimension line row choose white (7). The visible line is green (3), so the two never blur together on screen. Leave the linetype as Continuous and set the lineweight to 0.15. Continuous has no gaps to scale, so leave linetype scale empty."'),
    ("scripts/selfstudy/source/lesson-02.json",
     "외형선만 0.5, 나머지는 0.25 입니다.",
     "외형선만 0.30, 나머지는 0.15 입니다."),
    ("scripts/selfstudy/source/lesson-02.json",
     "0.5 for the visible line and 0.25 for the rest.",
     "0.30 for the visible line and 0.15 for the rest."),

    # ── 자습본 5차시 ──────────────────────────────────────────────────────
    ("scripts/selfstudy/source/lesson-05.json",
     "레이어 값은 `MASTER_DRAWING_SPEC.md` 가 정본입니다. 굵기는 외형선만 0.5, 나머지 셋은 0.25예요.",
     "레이어 값은 `course-standards.json` 이 정본이고, 근거는 사내 정본 교안 26쪽입니다. 선가중치는 외형선만 0.30, 나머지 셋은 0.15예요."),
    ("scripts/selfstudy/source/lesson-05.json",
     "`MASTER_DRAWING_SPEC.md` is the authority for layer settings. Lineweight is 0.5 mm on the visible layer and 0.25 on the other three.",
     "`course-standards.json` is the authority for layer settings, and it follows page 26 of the in-house course deck. Lineweight is 0.30 mm on the visible layer and 0.15 on the other three."),

    # ── 자습본 6·7차시 ────────────────────────────────────────────────────
    ("scripts/selfstudy/source/lesson-06.json",
     '        "ko": "빨강 계열 12",\n        "en": "red 12"',
     '        "ko": "흰색 7",\n        "en": "white 7"'),
    ("scripts/selfstudy/source/lesson-07.json",
     '        "ko": "빨강 계열 12번",\n        "en": "Magenta (6)"',
     '        "ko": "흰색 7번",\n        "en": "White (7)"'),
    ("scripts/selfstudy/source/lesson-07.json",
     '"ko": "화면 위 레이어 표시가 치수선으로 바뀝니다. 색은 빨강 계열 12번입니다.",',
     '"ko": "화면 위 레이어 표시가 치수선으로 바뀝니다. 색은 흰색 7번입니다.",'),
    ("scripts/selfstudy/source/lesson-07.json",
     '"en": "The layer on the ribbon changes to the dimension layer, magenta (6)."',
     '"en": "The layer on the ribbon changes to the dimension layer, white (7)."'),

    # ── 자습본 8차시 · 규격 요약 ──────────────────────────────────────────
    ("scripts/selfstudy/source/lesson-08.json",
     '"ko": "외형선 — Continuous · 굵기 0.5 · 흰색(7). 넷 중 이것만 굵습니다.",',
     '"ko": "외형선 — Continuous · 선가중치 0.30 · 초록(3). 넷 중 이것만 굵습니다.",'),
    ("scripts/selfstudy/source/lesson-08.json",
     '"en": "Visible line - Continuous, 0.5, white (7). The only thick one of the four."',
     '"en": "Visible line - Continuous, 0.30, green (3). The only thick one of the four."'),
    ("scripts/selfstudy/source/lesson-08.json",
     "중심선 — Center · 굵기 0.25 · 빨강(1) · 선 종류 축척 0.5.",
     "중심선 — CENTER · 선가중치 0.15 · 빨강(1) · 선 종류 축척 0.5."),
    ("scripts/selfstudy/source/lesson-08.json",
     "숨은선 — Hidden · 굵기 0.25 · 노랑(2) · 선 종류 축척 0.5.",
     "숨은선 — HIDDEN · 선가중치 0.15 · 노랑(2) · 선 종류 축척 0.5."),
    ("scripts/selfstudy/source/lesson-08.json",
     '"ko": "치수선 — Continuous · 굵기 0.25 · 보라(6). Continuous 라 선 종류 축척은 넣지 않습니다. 치수와 보조선을 같이 씁니다.",',
     '"ko": "치수선 — Continuous · 선가중치 0.15 · 흰색(7). Continuous 라 선 종류 축척은 넣지 않습니다. 치수와 보조선을 같이 씁니다.",'),
    ("scripts/selfstudy/source/lesson-08.json",
     '"en": "Dimension line - Continuous, 0.25, magenta (6). Dimensions and extension lines share it."',
     '"en": "Dimension line - Continuous, 0.15, white (7). Dimensions and extension lines share it."'),
    ("scripts/selfstudy/source/lesson-08.json",
     "외형선만 굵기 0.5 이고 나머지 셋은 0.25 입니다.",
     "외형선만 선가중치 0.30 이고 나머지 셋은 0.15 입니다."),
    ("scripts/selfstudy/source/lesson-08.json",
     "Only the visible line is 0.5; the other three are 0.25.",
     "Only the visible line is 0.30; the other three are 0.15."),
    ("scripts/selfstudy/source/lesson-08.json",
     "외형선만 0.5 이고 나머지 셋이 0.25 인지 봅니다.",
     "외형선만 0.30 이고 나머지 셋이 0.15 인지 봅니다."),
    ("scripts/selfstudy/source/lesson-08.json",
     "confirm only the visible line is 0.5 while the other three are 0.25.",
     "confirm only the visible line is 0.30 while the other three are 0.15."),

    # ── 생성기 ────────────────────────────────────────────────────────────
    ("scripts/part/write_master_spec.py",
     '          ("치수선", "Continuous", "0.25", "—", "보라 (6)", "치수 · 보조선")]',
     '          ("치수선", "Continuous", "0.15", "—", "흰색 (7)", "치수 · 보조선")]'),
    ("scripts/part/scaffold_lesson_02.py",
     '          ("치수선", "Continuous", "1", "보라 (6)", "치수 기입")]',
     '          ("치수선", "Continuous", "1", "흰색 (7)", "치수 기입")]'),
]


def main():
    dry = "--dry-run" in sys.argv
    done = miss = 0
    cache = {}
    for rel, old, new in EDITS:
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if path not in cache:
            with open(path, encoding="utf-8") as fh:
                cache[path] = fh.read()
        body = cache[path]
        if old not in body:
            if new in body:
                print(f"  = 이미 적용됨  {rel}  「{old[:44]}…」")
            else:
                print(f"  ✗ 못 찾음      {rel}  「{old[:44]}…」")
                miss += 1
            continue
        n = body.count(old)
        cache[path] = body.replace(old, new)
        done += n
        print(f"  ✓ {n}곳          {rel}  「{old[:44]}…」")

    if miss:
        print(f"\n앵커 {miss}건을 못 찾았다. 아무것도 쓰지 않는다.")
        return 1
    if dry:
        print(f"\n--dry-run — {done}곳을 고칠 수 있다. 쓰지 않았다.")
        return 0
    for path, body in cache.items():
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
    print(f"\n{len(cache)}개 파일 {done}곳을 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
