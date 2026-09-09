# -*- coding: utf-8 -*-
"""과정 전체가 `course-standards.json` 한 곳의 규격을 말하는지 확인한다.

레이어 색·굵기 같은 값은 대본·자습본·명세·생성기 네 곳에 흩어져 적힌다. 한 곳만
고치면 나머지 셋이 조용히 옛 값을 계속 가르치고, 그 사실은 학습자가 화면과 교재가
다르다고 말할 때 알게 된다. 실제로 치수선 색이 세 값(보라 6 · 색상 12 · 흰색 7)으로
갈라진 채 커밋되어 있었다.

    python scripts/check-standards.py            # 어긋난 곳을 모두 보고
    python scripts/check-standards.py --list     # 정본 값만 출력

종료 코드가 0 이 아니면 어딘가가 정본과 다르다.
"""
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "projects", "autocad-technician")
STD = os.path.join(COURSE, "course-standards.json")

SCRIPTS = "projects/autocad-technician/lesson-*/SCRIPT.md"
SELF = "scripts/selfstudy/source/lesson-0*.json"
SPEC = "projects/autocad-technician/MASTER_DRAWING_SPEC.md"


def load():
    with open(STD, encoding="utf-8") as fh:
        return json.load(fh)


def texts():
    """(라벨, 본문) — 학습자에게 실제로 나가는 한국어가 들어 있는 파일만."""
    import glob
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, SCRIPTS.replace("/", os.sep)))):
        out.append((os.path.relpath(p, ROOT), open(p, encoding="utf-8").read()))
    for p in sorted(glob.glob(os.path.join(ROOT, SELF.replace("/", os.sep)))):
        out.append((os.path.relpath(p, ROOT), open(p, encoding="utf-8").read()))
    p = os.path.join(ROOT, SPEC.replace("/", os.sep))
    if os.path.exists(p):
        out.append((SPEC, open(p, encoding="utf-8").read()))
    # 기획 문서도 함께 본다. 여기 옛 값이 남으면 다시 쓰는 사람이 되살린다 —
    # 이번에 갈라진 값들이 실제로 그렇게 생겼다.
    p = os.path.join(ROOT, "scripts", "selfstudy", "source", "curriculum.json")
    if os.path.exists(p):
        out.append(("scripts/selfstudy/source/curriculum.json",
                    open(p, encoding="utf-8").read()))
    return out


def lineno(body, idx):
    return body.count("\n", 0, idx) + 1


def check_layers(std, docs, fail):
    rows = {r["name"]: r for r in std["layers"]["rows"]}

    # 1) 폐기된 값이 남아 있는가. 하나라도 남으면 그 화면은 옛 규격을 가르친다.
    dead = [
        # 사용자 확인 (2026-09-10) — 보라색 선은 쓰지 않는다. 색 이름 자체를 막는다.
        (r"보라", "보라색은 이 과정에서 쓰지 않는다"),
        (r"색상\s*12\s*번|12\s*번\s*빨강|빨강\s*계열\s*12", "치수선 색 — 폐기된 '12번 빨강 계열'"),
        (r"굵기\s*0\.5\b|선가중치\s*[`\"]?0\.5\b", "선가중치 — 폐기된 0.5 (정본 0.30)"),
        (r"나머지는?\s*0\.25|나머지\s*셋(은|이)?\s*0\.25", "선가중치 — 폐기된 0.25 (정본 0.15)"),
        (r"외형선[^\n]{0,40}흰색\s*\(?7\)?", "외형선 색 — 폐기된 '흰색 7' (정본 초록 3)"),
        (r"치수선[^\n]{0,60}선\s*종류\s*축척[^\n]{0,10}0\.25",
         "치수선에 선 종류 축척 — Continuous 에는 조정할 간격이 없다"),
    ]
    for path, body in docs:
        for rx, why in dead:
            for m in re.finditer(rx, body):
                fail.append(f"{path}:{lineno(body, m.start())}  {why} — 「{m.group(0)}」")

    # 2) 정본 값이 실제로 실려 있는가. 2차시가 레이어를 만드는 차시다.
    two = dict(docs).get("projects/autocad-technician/lesson-02-part-and-template/SCRIPT.md", "")
    twoself = dict(docs).get("scripts/selfstudy/source/lesson-02.json", "")
    for name, r in rows.items():
        want = f"{r['colorName']}"
        for label, body in (("2차시 대본", two), ("2차시 자습본", twoself)):
            if not body:
                continue
            near = re.search(name + r"[^\n]{0,160}", body)
            if not near:
                fail.append(f"{label}: 레이어 「{name}」 을 언급하지 않는다")
            elif want not in near.group(0) and want not in body:
                fail.append(f"{label}: 레이어 「{name}」 의 색 「{want}」 이 보이지 않는다")


def check_present(std, docs, fail):
    """정본에 있는데 과정 어디에서도 가르치지 않는 것."""
    blob = "\n".join(b for _, b in docs)
    for row in std["functionKeys"]["rows"]:
        if row["key"] not in blob:
            fail.append(f"기능키 {row['key']} ({row['name']}) 를 어디에서도 설명하지 않는다")
    for row in std["specialText"]["rows"]:
        if row["code"] not in blob:
            fail.append(f"특수문자 {row['code']} ({row['glyph']} {row['name']}) 를 어디에서도 설명하지 않는다")
    for row in std["editKeys"]["rows"]:
        if row["key"] not in blob:
            fail.append(f"편집키 {row['key']} 를 어디에서도 설명하지 않는다")
    for row in std["selection"]["rows"]:
        if row["name"] not in blob:
            fail.append(f"선택 방식 「{row['name']}」 을 설명하지 않는다")


# 정책 1번의 유일한 예외 — 용지선 두 구석. 잡을 형상이 아직 없는 자리다.
ALLOWED_COORDS = {"0,0", "420,297"}
# 「쓰지 않는다」고 말하는 문장 안의 언급은 위반이 아니라 그 정책의 설명이다.
NEGATED = re.compile(
    r"쓰지\s*않|안\s*씁니다|권장하지|치지\s*않|외우지\s*않|필요\s*없|말라|금지|"
    r"does not use|do not use|never type|without typing")


def alt_spans(body):
    """`"altPath": true` 가 붙은 블록의 문자 범위.

    「이렇게도 가능합니다」 식으로 일부러 남긴 대비 카드다. 사용자가 지정한 예외라
    그 안의 좌표 언급은 위반이 아니다.
    """
    spans = []
    for m in re.finditer(r'"altPath"\s*:\s*true', body):
        # 이 키를 담은 객체의 여는 중괄호를 뒤로 찾아 올라간다.
        depth = 0
        start = None
        for i in range(m.start(), -1, -1):
            c = body[i]
            if c == "}":
                depth += 1
            elif c == "{":
                if depth == 0:
                    start = i
                    break
                depth -= 1
        if start is None:
            continue
        depth = 0
        for j in range(start, len(body)):
            c = body[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    spans.append((start, j))
                    break
    return spans


def check_coordinates(docs, fail):
    """정책 1번 — 좌표를 치라고 시키는 곳이 남아 있는가.

    백틱 안의 숫자쌍은 '이대로 타이핑하라'는 뜻이다. 백틱 없이 위치를 가리키는
    문장은 좌표 입력이 아니지만, 백틱을 씌워 두면 학습자가 그대로 친다.
    """
    typed = re.compile(r"`@?(-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?)`")
    named = re.compile(r"골뱅이|상대\s*좌표|절대\s*좌표|극\s*좌표로\s*점")
    for path, body in docs:
        skip = alt_spans(body) if path.endswith(".json") else []

        def inside_alt(pos, _skip=skip):
            return any(a <= pos <= b for a, b in _skip)

        for m in typed.finditer(body):
            if inside_alt(m.start()):
                continue
            val = re.sub(r"\s+", "", m.group(1))
            if val in ALLOWED_COORDS:
                continue
            ctx = body[max(0, m.start() - 120):m.end() + 120]
            if NEGATED.search(ctx):
                continue
            fail.append(f"{path}:{lineno(body, m.start())}  좌표를 치게 한다 — 「{m.group(0)}」")
        for m in named.finditer(body):
            if inside_alt(m.start()):
                continue
            ctx = body[max(0, m.start() - 140):m.end() + 140]
            if NEGATED.search(ctx):
                continue
            fail.append(f"{path}:{lineno(body, m.start())}  좌표 방식을 가르친다 — 「{m.group(0)}」")


def main():
    std = load()
    if "--list" in sys.argv:
        print("레이어 (정본:", std["layers"]["source"], ")")
        for r in std["layers"]["rows"]:
            lt = f"  선종류축척 {r['ltscale']}" if r["ltscale"] else ""
            print(f"  {r['name']:5} {r['colorName']:3}({r['aci']})  {r['linetype']:11}"
                  f"  선가중치 {r['lineweight']:.2f}{lt}")
        print("\n기능키")
        for r in std["functionKeys"]["rows"]:
            print(f"  {r['key']:4} {r['name']:10} {r['policy']}")
        print("\n특수문자")
        for r in std["specialText"]["rows"]:
            print(f"  {r['code']}  {r['glyph']}  {r['name']}")
        return 0

    docs = texts()
    fail = []
    check_layers(std, docs, fail)
    check_present(std, docs, fail)
    check_coordinates(docs, fail)

    if not fail:
        print(f"규격 검사 통과 — 문서 {len(docs)}개가 course-standards.json 과 일치한다.")
        return 0
    print(f"규격 불일치 {len(fail)}건\n")
    for f in fail:
        print("  ✗", f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
