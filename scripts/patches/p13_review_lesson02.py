# -*- coding: utf-8 -*-
"""2차시 검수 메모를 반영한다 — 슬라이드별 1~9번.

무엇을 고치나

  1·2  「정확해야 하는 점 — 오늘」의 「— 오늘」을 뗀다. 이 절은 이 부품만이 아니라
        점을 찍는 방법 전체를 말한다. 「오늘」이 붙으면 오늘만 쓰는 규칙으로 읽힌다.
  5     3/4 장(절대좌표·마우스 문단 둘)을 지운다. 같은 말이 바로 위 표 두 개에
        이미 있다 — 표의 「좌표 입력 · 쓰지 않습니다」 행과 「직접 거리 입력」 행이다.
  6     4/4 장의 각도 표(0·90·135·180도)를 지운다. 각도를 외우는 화면인데 이 과정은
        각도를 치지 않는다. 다만 검수 의견대로 **각도를 눈대중으로 찍으면 안 된다**는
        경고는 남긴다 — 극좌표 추적 행으로 옮겨 실제로 쓰는 자리에 붙인다.
  7     선가중치 값이 절대적이지 않다는 것을 참고로 붙인다.
  8     중심 마크의 `30` 이 절대값이 아님을 밝힌다. 도면선만 넘으면 된다.
  9     표제란이 엉뚱한 데 붙었을 때 `M`(MOVE) 으로 옮기는 길을 준다.

3·4번(대본 누락)은 자료가 아니라 렌더러 결함이었다. 나뉜 개념 절의 모든 장에 절의
lede 를 그대로 붙이고 있어 2/4·3/4·4/4 가 1/4 과 같은 한 줄을 갖고 있었다.
`build_deck_selfstudy.part_notes` 가 장마다 그 장의 글로 노트를 만든다.

    python scripts/patches/p13_review_lesson02.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "scripts", "selfstudy", "source", "lesson-02.json")


def main():
    dry = "--dry-run" in sys.argv
    doc = json.load(io.open(SRC, encoding="utf-8"))
    log = []

    # ── 개념 절 「점을 찍는 네 가지 방법」 ────────────────────────────────
    sec = next(s for s in doc["sections"]
               if "점을 찍는" in (s.get("label") or {}).get("ko", ""))
    blocks = sec["blocks"]

    # 1·2 — 「— 오늘」 떼기
    for b in blocks:
        if b.get("type") != "cards":
            continue
        for it in b.get("items", []):
            for lang, tail in (("ko", " — 오늘"), ("en", " - today")):
                lab = (it.get("label") or {}).get(lang, "")
                if lab.endswith(tail):
                    it["label"][lang] = lab[: -len(tail)]
                    log.append("카드 이름에서 「%s」 뗌 — %s" % (tail.strip(), it["label"][lang]))

    # 6 — 각도 경고를 실제로 쓰는 자리로 옮긴다
    tbl = next(b for b in blocks
               if b.get("type") == "table"
               and any("직접 거리 입력" in ((r[0] or {}).get("ko", "") if isinstance(r[0], dict) else "")
                       for r in b.get("rows", [])))
    if not any("극좌표 추적" in ((r[0] or {}).get("ko", "") if isinstance(r[0], dict) else "")
               for r in tbl["rows"]):
        tbl["rows"].append([
            {"ko": "극좌표 추적 `F10`", "en": "Polar tracking `F10`"},
            {"ko": "각도는 안내선이 고정, 거리만 숫자",
             "en": "The guide holds the angle; you type only the distance"},
            {"ko": "45도 보조선처럼 기운 방향이 필요할 때. **각도를 눈대중으로 찍으면 안 됩니다** — 화면에서는 45도처럼 보여도 값이 다릅니다",
             "en": "When you need a slanted direction, like the 45-degree guide. **Never eyeball an angle** - it can look like 45 on screen and not be."},
        ])
        log.append("표에 극좌표 추적 행 추가 — 각도 눈대중 경고를 여기로")

    # 5·6 — 표와 겹치는 문단 둘, 그리고 각도 표를 뺀다
    drop = []
    for i, b in enumerate(blocks):
        ko = (b.get("ko") or "")
        if b.get("type") == "p" and ko.startswith("절대좌표는 도면에 원점 기준으로"):
            drop.append(i)
        elif b.get("type") == "p" and ko.startswith("나머지는 전부 마우스와 숫자입니다"):
            drop.append(i)
        elif b.get("type") == "table" and len(b.get("rows", [])) == 4 and all(
                ((r[0] or {}).get("ko", "") if isinstance(r[0], dict) else "").endswith("도")
                for r in b["rows"]):
            drop.append(i)
    for i in reversed(drop):
        log.append("겹치는 블록 제거 — %s" % (blocks[i].get("ko") or "각도 표")[:34])
        blocks.pop(i)

    # ── 따라 하기 단계 ────────────────────────────────────────────────────
    for s in doc["sections"]:
        for blk in s.get("blocks", []):
            if blk.get("type") != "steps":
                continue
            for st in blk.get("items", []):
                n = st.get("n")

                # 7 — 선가중치는 절대적인 값이 아니다
                if n == 9 and "절대적인" not in (st.get("why") or {}).get("ko", ""):
                    st["why"]["ko"] += (" 이 굵기 값은 절대적인 것이 아니에요. "
                                        "회사 표준이나 과제 지시가 다른 값을 주면 그 지시가 우선합니다. "
                                        "정해진 것은 **외형선만 굵고 나머지는 그 절반**이라는 관계이고, "
                                        "이 과정은 그 관계를 0.30 과 0.15 로 씁니다.")
                    st["why"]["en"] += (" These numbers are not absolute. A company standard or an "
                                        "assignment may name others, and that instruction wins. What is "
                                        "fixed is the relation - the visible line is thick and the rest "
                                        "are half of it - which this course writes as 0.30 and 0.15.")
                    log.append("9단계 — 선가중치가 절대값이 아님을 밝힘")

                # 8 — 중심 마크의 30 은 예시다
                if n == 12:
                    for a in st.get("actions", []):
                        do = (a.get("do") or {}).get("ko", "")
                        if a.get("type") == "30" and "넘기만" not in do:
                            a["do"]["ko"] = ("거리만 입력하고 엔터를 누릅니다. 엔터를 한 번 더 눌러 "
                                             "명령을 끝냅니다. 이 `30` 은 정해진 값이 아니에요. "
                                             "**도면선을 넘어가기만 하면 됩니다** — 넘친 만큼은 곧 "
                                             "TRIM 으로 잘라 내거든요.")
                            a["do"]["en"] = ("Type just the distance and press Enter, then Enter once "
                                             "more to finish. The `30` is not a fixed value: **it only "
                                             "has to reach past the border**, because you trim the "
                                             "overshoot in a moment.")
                            log.append("12단계 — 30 이 정해진 값이 아님을 밝힘")
                    why = (st.get("why") or {}).get("ko", "")
                    if "넉넉히" in why and "정해진" not in why:
                        st["why"]["ko"] = why.replace(
                            "넉넉히 긋고 넘친 만큼을 TRIM 으로 잘라 내면 자리가 저절로 맞습니다.",
                            "넉넉히 긋고 넘친 만큼을 TRIM 으로 잘라 내면 자리가 저절로 맞아요. "
                            "그래서 길이는 정해진 값이 아니라 도면선만 넘으면 되는 값입니다.")
                        log.append("12단계 — 왜 이 순서인가에 같은 취지를 맞춤")

                # 9 — 자리가 어긋났으면 MOVE 로 옮긴다
                if n == 13:
                    acts = st.get("actions", [])
                    if not any((a.get("type") or "") == "M" for a in acts):
                        acts.append({
                            "kind": "alt",
                            "type": "M",
                            "do": {
                                "ko": "자리가 어긋났으면 지우고 다시 그리지 않아요. 입력하고 엔터, "
                                      "표제란을 클릭하고 엔터. 기준점으로 표제란의 오른쪽 아래 "
                                      "모서리를 끝점 스냅으로 잡고, 두 번째 점으로 도면선의 오른쪽 "
                                      "아래 모서리를 잡으면 딱 붙습니다. 두 점을 스냅으로 잡았으니 "
                                      "눈대중이 끼어들 자리가 없어요.",
                                "en": "If it landed wrong, do not erase and redraw. Type it, Enter, "
                                      "click the title block, Enter. Snap the base point to the block's "
                                      "lower-right corner and the second point to the border's "
                                      "lower-right corner, and it lands flush. Both points came from "
                                      "snaps, so there is no eyeballing in it."},
                        })
                        log.append("13단계 — MOVE 로 자리를 고치는 길 추가")

    if not log:
        print("  = 고칠 것이 없다")
        return 0
    for line in log:
        print("  ✓", line)
    if dry:
        print("\n--dry-run — 쓰지 않았다.")
        return 0
    with io.open(SRC, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("\nlesson-02.json — %d곳" % len(log))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
