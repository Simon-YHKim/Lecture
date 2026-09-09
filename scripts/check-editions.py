# -*- coding: utf-8 -*-
"""강의용 판과 자습용 판이 같은 것을 가르치는지 확인한다.

이 과정은 판이 둘이다.

    강의용  projects/autocad-technician/lesson-0N/     대본 · 프레임 · 편 · 나레이션
    자습용  scripts/selfstudy/source/lesson-0N.json    읽고 따라 하는 교재 · 검수 데크

둘은 **같은 작업을 가르치되 다른 매체**다. 분량과 등장 순서와 단계를 쪼개는
방식은 달라도 된다 — 영상은 말이 끌고 가고 교재는 눈이 끌고 가기 때문이다.
같아야 하는 것은 셋뿐이다.

    1. 학습자가 치는 명령의 집합
    2. 차시를 잇는 체크포인트 파일 이름
    3. 규격 (레이어·용지·기능키 — `check-standards.py` 가 따로 본다)

실제로 갈라졌었다. 자습본은 골뱅이 상대좌표를 84곳 걷어냈는데 녹화 대본은 그대로
였고, 2차시 「다음 시간에는 절대좌표·상대좌표·극좌표로 점을 찍습니다」라는 예고가
3차시가 더 이상 하지 않는 일을 가리키고 있었다. 사람이 세어서 찾은 것이라 세는
일을 여기 옮긴다.

    python scripts/check-editions.py            # 어긋난 곳을 보고
    python scripts/check-editions.py --verbose  # 차시별 대조표까지

종료 코드가 0 이 아니면 한쪽 판만 가르치는 것이 있다.
"""
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "projects", "autocad-technician")
SELF = os.path.join(ROOT, "scripts", "selfstudy", "source")

SLUG = {
    1: "lesson-01-orientation", 2: "lesson-02-part-and-template",
    3: "lesson-03-baseline-profile", 4: "lesson-04-circles-arcs",
    5: "lesson-05-three-views", 6: "lesson-06-editing-symbols",
    7: "lesson-07-dimensioning-release", 8: "lesson-08-exam-and-qa",
}

# 백틱 안에는 명령만 있는 것이 아니다. 키·파일 이름·값·한국어는 뺀다.
NOT_A_COMMAND = re.compile(
    r"^(F\d{1,2}|Ctrl\+\S+|Esc|Enter|Tab|Shift|Delete|Space|"
    r"(EDU-IB-02_)?L0\d_[A-Z_]+|EDU-IB-02\S*|acadiso\.dwt|\S+\.(dwg|dwt|shx)|"
    r"\d[\d.,\-]*|[가-힣].*|.{25,})$", re.I)
TICK = re.compile(r"`([^`\n]+)`")
STEP_HEAD = re.compile(r"^### (\d+)단계", re.M)


def commands_in(text):
    out = set()
    for t in TICK.findall(text):
        t = t.strip()
        if t and not NOT_A_COMMAND.match(t):
            out.add(t.upper())
    return out


def demo_span(body):
    """실습 구간 — `### N단계` 가 들어 있는 Line 하나."""
    spans = [m.start() for m in re.finditer(r"^## Line \d+ —", body, re.M)]
    spans.append(len(body))
    for a, b in zip(spans, spans[1:]):
        if STEP_HEAD.search(body[a:b]):
            return body[a:b]
    return ""


def lecture(no):
    body = io.open(os.path.join(COURSE, SLUG[no], "SCRIPT.md"), encoding="utf-8").read()
    demo = demo_span(body)
    return {"body": body, "demo": demo,
            "steps": len(STEP_HEAD.findall(demo)),
            "cmds": commands_in(demo)}


def selfstudy(no):
    doc = json.load(io.open(os.path.join(SELF, "lesson-%02d.json" % no), encoding="utf-8"))
    steps, cmds = 0, set()
    for sec in doc.get("sections", []):
        for blk in sec.get("blocks", []):
            if blk.get("type") != "steps":
                continue
            for st in blk.get("items", []):
                steps += 1
                for a in st.get("actions", []):
                    t = (a.get("type") or "").strip()
                    if t and not NOT_A_COMMAND.match(t):
                        cmds.add(t.upper())
                    cmds |= commands_in((a.get("do") or {}).get("ko", ""))
    return {"doc": doc, "steps": steps, "cmds": cmds,
            "text": json.dumps(doc, ensure_ascii=False)}


def main():
    verbose = "--verbose" in sys.argv
    fail, note = [], []
    L = {n: lecture(n) for n in SLUG}
    S = {n: selfstudy(n) for n in SLUG}

    # 1) 과정 전체에서 한쪽만 치는 명령. 차시별로 보면 판마다 배치가 달라
    #    거짓 경보가 난다 — 어느 차시에서 가르치든 과정 안에 있으면 된다.
    all_l = set().union(*(L[n]["cmds"] for n in SLUG))
    all_s = set().union(*(S[n]["cmds"] for n in SLUG))
    only_l = sorted(all_l - all_s)
    only_s = sorted(all_s - all_l)
    if only_l:
        fail.append("강의용에서만 치는 명령: %s" % ", ".join(only_l))
    if only_s:
        fail.append("자습용에서만 치는 명령: %s" % ", ".join(only_s))

    # 2) 차시를 잇는 사슬. 여는 파일과 저장하는 파일의 이름이 두 판에서 같아야
    #    학습자가 영상에서 본 이름을 교재에서 찾을 수 있다.
    for no in sorted(SLUG):
        for key, label in (("opens", "여는 파일"), ("saves", "저장하는 파일")):
            want = S[no]["doc"].get(key)
            if not want:
                continue
            tail = want.split("_", 1)[-1] if "_" in want else want
            if want not in L[no]["body"] and tail not in L[no]["body"]:
                fail.append("%d차시 %s 「%s」 를 대본이 말하지 않는다" % (no, label, want))

    # 3) 코치 마크 — 사용자 정책 2번. 「도면 위에서 자리를 잡는 단계」에는 도면과
    #    코치 마크가 있어야 한다. 그 단계를 무엇으로 아는가: 조작에 `snap` 이 있는
    #    단계다. 스냅은 형상 위의 점을 잡는다는 뜻이고, 그 점을 글로만 부르면
    #    학습자가 화면에서 찾아내야 한다 — 정책이 없애라고 한 그 탐색이다.
    for no in sorted(SLUG):
        holes = []
        for sec in S[no]["doc"].get("sections", []):
            for blk in sec.get("blocks", []):
                if blk.get("type") != "steps":
                    continue
                for st in blk.get("items", []):
                    kinds = {a.get("kind") for a in st.get("actions", [])}
                    if "snap" in kinds and not st.get("spots"):
                        holes.append(st.get("n"))
        if holes:
            fail.append("%d차시 — 스냅으로 점을 잡는데 코치 마크가 없는 단계: %s"
                        % (no, ", ".join(str(h) for h in holes)))

    # 4) 단계 쪼개기 — 다르다고 틀린 것은 아니다. 크게 벌어지면 알려만 준다.
    for no in sorted(SLUG):
        a, b = L[no]["steps"], S[no]["steps"]
        if a and b and abs(a - b) > 3:
            note.append("%d차시 실습 단계 — 강의 %d · 자습 %d (쪼개는 방식이 다르다)"
                        % (no, a, b))

    if verbose:
        print("%-6s %8s %8s %10s" % ("차시", "강의단계", "자습단계", "공통명령"))
        for no in sorted(SLUG):
            print("%-6d %8d %8d %10d"
                  % (no, L[no]["steps"], S[no]["steps"],
                     len(L[no]["cmds"] & S[no]["cmds"])))
        print()

    for n in note:
        print("  · ", n)
    if not fail:
        print("판 대조 통과 — 두 판이 같은 명령과 같은 체크포인트를 가르친다.")
        return 0
    print("\n두 판이 어긋난 곳 %d건\n" % len(fail))
    for f in fail:
        print("  ✗", f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
