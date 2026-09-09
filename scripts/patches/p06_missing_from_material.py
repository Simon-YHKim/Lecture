# -*- coding: utf-8 -*-
"""사내 정본 교안에 있는데 이 과정이 한 번도 다루지 않던 것을 채운다.

교안 부록(단축키 v2) 2쪽을 이 과정의 내용과 대조해 보면 세 덩어리가 통째로 비어
있었다. 셋 다 이 과정이 이미 채택한 방식을 **실제로 실행하려면** 필요한 것들이다.

1. 기능키 — F3 과 F8 만 나오고 F7 · F9 · F10 · F11 · F12 가 없었다.
   「좌표를 치지 않고 마우스와 스냅으로 그린다」는 정책은 F11 객체 스냅 추적과
   F12 동적 입력 위에서 돈다. 학습자가 그 둘이 꺼진 화면을 켜면 대본과 화면이
   다르게 보이고, 왜 다른지 알 방법이 없다. F7 그리드와 F9 스냅은 반대로 **꺼야**
   하는데, 켜져 있으면 특징점 대신 모눈에 붙어 스냅이 안 되는 것처럼 보인다.

2. 특수문자 %%c · %%d · %%p — 7차시가 Ø 를 「명령이 자동으로 붙여 준다」까지만
   말하고 끝난다. 도면에 직접 Ø 나 ° 나 ± 를 써야 하는 순간(주기, 공차 문자,
   지시선 문자)에 칠 것이 없다.

3. 편집 단축키 Ctrl+C · Ctrl+V · Ctrl+X · Ctrl+Shift+C — 교안이 표로 주는데
   과정에는 Ctrl+1 · Ctrl+A · Ctrl+Z 만 있었다. 특히 Ctrl+Shift+C(기준점 복사)는
   다른 도면으로 같은 자리에 옮길 때 쓰는, 현장에서 실제로 필요한 하나다.

강의용에는 그 자리에서 필요한 만큼만 넣고, 전체 대응표는 자습용 부록에 둔다.
영상은 흐름이 끊기면 안 되고, 자습본은 찾아보는 물건이기 때문이다.

    python scripts/patches/p06_missing_from_material.py [--dry-run]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEXT_EDITS = [
    # ── 2차시 대본 · 상태 막대 ────────────────────────────────────────────
    ("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md",
     "    화면 아래 상태 막대를 봅니다. 객체 스냅이 켜져 있는지 확인합니다.\n"
     "    단축키는 F3입니다.\n"
     "    직교 모드도 켭니다. 단축키 F8입니다.\n"
     "    방향을 수평 수직으로 고정해 주는 기능입니다.\n"
     "    앞으로 자리는 이렇게 잡습니다.\n"
     "    클릭이나 스냅으로 시작점을 잡고, 직교로 방향을 고정하고, 거리만 칩니다.\n",
     "    화면 아래 상태 막대를 봅니다. 여기서 다섯 개를 정해 두고 시작합니다.\n"
     "    객체 스냅이 켜져 있는지 확인합니다. 단축키는 F3입니다.\n"
     "    직교 모드도 켭니다. 단축키 F8입니다. 방향을 수평 수직으로 고정해 줍니다.\n"
     "    객체 스냅 추적을 켭니다. F11입니다.\n"
     "    특징점에 커서를 얹으면 안내선이 뻗고, 두 안내선이 만나는 자리를 잡을 수 있어요.\n"
     "    형상에 아직 없는 점을 만드는 방법입니다.\n"
     "    동적 입력도 켭니다. F12입니다.\n"
     "    커서 옆에 입력칸이 따라다니면서 길이와 각도를 거기서 받습니다.\n"
     "    꺼져 있으면 같은 숫자가 화면 아래 명령행으로 들어가요. 값은 같지만 눈이 두 군데를 봐야 합니다.\n"
     "    반대로 꺼 두는 것이 둘입니다.\n"
     "    F7 그리드와 F9 스냅입니다. 모눈은 화면만 어지럽히고, 스냅은 커서를 일정 간격에 붙잡아\n"
     "    끝점이나 중간점 대신 엉뚱한 자리에 걸리게 만듭니다.\n"
     "    스냅이 안 잡히는 것 같으면 F9부터 확인하세요.\n"
     "    기울어진 방향이 필요할 때만 F10 극좌표 추적을 켭니다. 4차시에 씁니다.\n"
     "    앞으로 자리는 이렇게 잡습니다.\n"
     "    클릭이나 스냅으로 시작점을 잡고, 직교로 방향을 고정하고, 거리만 칩니다.\n"),

    # ── 7차시 대본 · 특수문자 ─────────────────────────────────────────────
    ("projects/autocad-technician/lesson-07-dimensioning-release/SCRIPT.md",
     "    앞에 붙은 Ø 기호는 우리가 친 게 아닙니다. 지름 치수 명령이 자동으로 붙입니다.",
     "    앞에 붙은 Ø 기호는 우리가 친 게 아닙니다. 지름 치수 명령이 자동으로 붙입니다.\n"
     "    직접 쳐야 할 때도 있어요. 주기나 지시선 문자에 Ø를 넣을 때입니다.\n"
     "    그때는 `%%c` 를 칩니다. 퍼센트 두 개에 c 예요. 화면에 Ø로 바뀝니다.\n"
     "    각도 기호는 `%%d`, 플러스마이너스는 `%%p` 입니다.\n"
     "    셋 다 문자 명령에서도 치수 문자 재정의에서도 똑같이 씁니다."),
]


def append_appendix(path):
    """자습본 8차시 끝에 「원본 교안 대응표」 절을 붙인다."""
    doc = json.load(io.open(path, encoding="utf-8"))
    if any(s.get("id") == "material-map" for s in doc["sections"]):
        return None, 0

    std = json.load(io.open(
        os.path.join(ROOT, "projects", "autocad-technician", "course-standards.json"),
        encoding="utf-8"))

    def rows(items, cols):
        return [[c(it) for c in cols] for it in items]

    fk = std["functionKeys"]["rows"]
    ek = std["editKeys"]["rows"]
    sp = std["specialText"]["rows"]
    sel = std["selection"]["rows"]

    section = {
        "id": "material-map",
        "kind": "concept",
        "label": {"ko": "부록 · 원본 교안 대응표",
                  "en": "Appendix - map to the in-house course deck"},
        "lede": {
            "ko": "사내 정본 교안이 표로 주는 것 중, 작도 차시에서 그때그때 쓰느라 한자리에 모이지 않았던 것들입니다. 시험 전에 여기만 훑어도 됩니다.",
            "en": "The tables the in-house deck gives you, gathered in one place because the drawing lessons use them a few at a time. Skimming this before the exam is enough."},
        "blocks": [
            {"type": "p",
             "ko": "기능키 일곱 개가 상태 막대의 일곱 단추와 하나씩 짝입니다. 이 과정은 다섯을 켜고 둘을 끕니다. 켜고 끄는 이유가 방법과 붙어 있어요. 스냅으로 형상에서 점을 뽑는 방식이라, 커서를 다른 데로 끌고 가는 기능은 방해가 됩니다.",
             "en": "Seven function keys, one for each button on the status bar. This course turns five on and two off, and the reason is tied to the method: when you pull points off the geometry with snaps, anything that drags the cursor elsewhere is in the way."},
            {"type": "table",
             "head": [{"ko": "키", "en": "Key"}, {"ko": "이름", "en": "Name"},
                      {"ko": "무엇을 하나", "en": "What it does"},
                      {"ko": "이 과정에서", "en": "In this course"}],
             "rows": rows(fk, [lambda r: {"ko": r["key"], "en": r["key"]},
                               lambda r: {"ko": r["name"], "en": r["name"]},
                               lambda r: {"ko": r["what"], "en": r["what"]},
                               lambda r: {"ko": r["policy"], "en": r["policy"]}])},
            {"type": "note", "tone": "why",
             "label": {"ko": "스냅이 안 잡히는 것 같으면", "en": "When snapping seems broken"},
             "ko": "F9 스냅이 켜져 있는지부터 보세요. 켜져 있으면 커서가 일정 간격 격자에 먼저 걸려서, 끝점 표식이 떠도 그 자리에 못 갑니다. 객체 스냅(F3)이 고장 난 것처럼 보이는 원인의 대부분이 이것입니다.",
             "en": "Check F9 first. With grid snap on, the cursor lands on the spacing grid before it can reach the endpoint, so object snap (F3) looks broken when it is not."},
            {"type": "p",
             "ko": "특수문자 셋은 문자 명령과 치수 문자에서 똑같이 씁니다. 치수 명령이 자동으로 붙여 주는 Ø 와 달리, 주기나 지시선에 직접 쓸 때 필요해요.",
             "en": "Three special codes, the same in text commands and in dimension text. The dimension commands add Ø for you; these are for when you type it yourself in a note or a leader."},
            {"type": "table",
             "head": [{"ko": "입력", "en": "Type"}, {"ko": "나오는 기호", "en": "You get"},
                      {"ko": "이름", "en": "Name"}],
             "rows": rows(sp, [lambda r: {"ko": r["code"], "en": r["code"]},
                               lambda r: {"ko": r["glyph"], "en": r["glyph"]},
                               lambda r: {"ko": r["name"], "en": r["name"]}])},
            {"type": "p",
             "ko": "편집 단축키는 윈도우에서 쓰던 것과 대부분 같습니다. 하나만 다릅니다. Ctrl+Shift+C 는 기준점을 먼저 묻습니다. 다른 도면에 붙였을 때 같은 자리에 놓이게 하는 것이 이 한 걸음이에요.",
             "en": "The editing shortcuts are the Windows ones you already know, with one exception: Ctrl+Shift+C asks for a base point first. That single step is what lands the paste in the same place in another drawing."},
            {"type": "table",
             "head": [{"ko": "키", "en": "Key"}, {"ko": "무엇을 하나", "en": "What it does"}],
             "rows": rows(ek, [lambda r: {"ko": r["key"], "en": r["key"]},
                               lambda r: {"ko": r["what"], "en": r["what"]}])},
            {"type": "p",
             "ko": "마지막으로 선택입니다. 마우스를 어느 쪽으로 끄느냐에 따라 고르는 것이 달라집니다. 자르기와 지우기에서 이것을 모르면 왜 어떤 것은 골라지고 어떤 것은 안 골라지는지 알 수 없어요.",
             "en": "Last, selection. Which way you drag decides what gets picked. Without this, trimming and erasing look arbitrary."},
            {"type": "table",
             "head": [{"ko": "끄는 방향", "en": "Drag"}, {"ko": "이름", "en": "Name"},
                      {"ko": "상자 테두리", "en": "Box border"},
                      {"ko": "골라지는 것", "en": "What it picks"}],
             "rows": rows(sel, [lambda r: {"ko": r["drag"], "en": r["drag"]},
                                lambda r: {"ko": r["name"], "en": r["name"]},
                                lambda r: {"ko": r["border"], "en": r["border"]},
                                lambda r: {"ko": r["picks"], "en": r["picks"]}])},
        ],
    }
    doc["sections"].append(section)
    return doc, 1


def main():
    dry = "--dry-run" in sys.argv
    cache, miss = {}, 0
    for rel, old, new in TEXT_EDITS:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        cache.setdefault(p, io.open(p, encoding="utf-8").read())
        if old not in cache[p]:
            if new.split("\n")[0] in cache[p]:
                print(f"  = 이미 적용됨  {rel}")
            else:
                print(f"  ✗ 못 찾음      {rel}  「{old[:46]}…」")
                miss += 1
            continue
        cache[p] = cache[p].replace(old, new, 1)
        print(f"  ✓ {rel}")
    if miss:
        print(f"\n앵커 {miss}건을 못 찾았다. 아무것도 쓰지 않는다.")
        return 1

    p8 = os.path.join(ROOT, "scripts", "selfstudy", "source", "lesson-08.json")
    doc, added = append_appendix(p8)
    print(f"  ✓ 자습본 8차시 부록 절 {added}개")

    if dry:
        print("\n--dry-run — 쓰지 않았다.")
        return 0
    for p, body in cache.items():
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)
    if doc:
        with io.open(p8, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    print(f"\n{len(cache) + (1 if doc else 0)}개 파일을 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
