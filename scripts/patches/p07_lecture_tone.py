# -*- coding: utf-8 -*-
"""녹화 대본의 어투를 정책 범위 안으로 되돌린다.

정책은 합쇼체 70~80% · 해요체 20~30% 다. 자습본은 72~78% 로 그 안에 있는데,
녹화 대본만 **90% 대 9%** 였다. 사람 앞에서 말하는 쪽이 읽는 쪽보다 더 딱딱한
상태다 — LESSON_STYLE 24번 「읽는 사람이 앞에 있다고 생각하고 쓴다」의 반대다.

기계적으로 「니다」를 「요」로 바꾸면 문장이 뭉개진다. 그래서 **설명·부연으로 문장이
끝나는 자리**만 골랐다. 지시("입력하고 엔터")와 규격("A3 가로 420 × 297입니다")은
건드리지 않는다. 한 문단 안에서 해요체가 연달아 나오지 않게 하나 걸러 바꾼다 —
전부 바꾸면 이번에는 반대로 수다스러워진다.

문어체 세 곳과 번역투 한 곳도 함께 고친다. 40자를 넘는 문장은 귀로 못 따라가므로
(LESSON_STYLE 24번) 긴 것부터 끊는다.

    python scripts/patches/p07_lecture_tone.py [--dry-run] [--report]
"""
import io
import os
import re
import sys
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 설명·부연으로 끝나는 종결만. 앞뒤 문맥 없이 바꿔도 뜻이 흔들리지 않는 것들이다.
SOFTEN = [
    ("기 때문입니다.", "기 때문이에요."),
    ("하면 됩니다.", "하면 돼요."),
    ("것입니다.", "것이에요."),
    ("아닙니다.", "아니에요."),
    ("같습니다.", "같아요."),
    ("쉽습니다.", "쉬워요."),
    ("좋습니다.", "좋아요."),
    ("그렇습니다.", "그래요."),
    ("뜻입니다.", "뜻이에요."),
    ("값입니다.", "값이에요."),
    ("자리입니다.", "자리예요."),
    ("까닭입니다.", "까닭이에요."),
    ("셈입니다.", "셈이에요."),
    ("어렵습니다.", "어려워요."),
    ("없습니다.", "없어요."),
    ("많습니다.", "많아요."),
    ("생깁니다.", "생겨요."),
    ("나옵니다.", "나와요."),
    ("달라집니다.", "달라져요."),
    ("맞습니다.", "맞아요."),
    ("됩니다.", "돼요."),
    ("있습니다.", "있어요."),
    ("겁니다.", "거예요."),
    ("들어갑니다.", "들어가요."),
    ("사라집니다.", "사라져요."),
    ("붙습니다.", "붙어요."),
    ("걸립니다.", "걸려요."),
    ("일입니다.", "일이에요."),
    ("방법입니다.", "방법이에요."),
    ("뿐입니다.", "뿐이에요."),
    ("보입니다.", "보여요."),
]
SOFTEN_RX = re.compile("|".join(re.escape(a) for a, _ in SOFTEN))
SOFTEN_MAP = dict(SOFTEN)

# 문어체 · 번역투 — 세는 것이 아니라 고치는 것이다.
FIXES = [
    ("작업을 편하게 할 지그를 하나 제안한다고 해 봅시다.",
     "작업을 편하게 할 지그를 하나 제안한다고 해 보겠습니다."),
    ("Ø가 붙어 있으면 `D`를 먼저 누른다.",
     "Ø가 붙어 있으면 `D`를 먼저 누릅니다."),
    ("R이 붙어 있으면 그냥 넣는다.",
     "R이 붙어 있으면 그냥 넣습니다."),
    ("(2행 · 기하 공차) 네모 칸을 좌우로 나눈 표기입니다.",
     "(2행 · 기하 공차) 네모 칸을 좌우로 나눈 표기예요."),
]

# 40자를 넘어 귀로 따라가기 어려운 문장 — 뜻을 그대로 두고 끊는다.
SPLITS = [
    ("조립도를 열어 그 부품을 찾고, 부품 도면을 확인하여, 도면을 기준으로 가공집과 이야기할 수 있습니다.",
     "조립도를 열어 그 부품을 찾습니다. 부품 도면을 확인합니다. 그 도면을 기준으로 가공집과 이야기합니다."),
    ("앞서 말씀드린 일을 할 수 있는 능력을 갖추려고 우리는 실습 과제를 함께하며, LG Innotek 의 내부 시험에 대비합니다.",
     "그 일을 할 수 있는 능력을 갖추는 것이 목표입니다. 그래서 실습 과제를 함께하고, LG Innotek 의 내부 시험에 대비합니다."),
    ("이 과정에서 정하는 값은 연습용 기본값이고, 실제 과제에 지시가 적혀 있으면 그 지시를 따릅니다.",
     "이 과정에서 정하는 값은 연습용 기본값이에요. 실제 과제에 지시가 적혀 있으면 그 지시를 따릅니다."),
    ("아이들러 풀리 브래킷은 V-벨트로 동력을 전달할 때 벨트의 텐션을 확보하려고 벨트를 눌러 주는, 풀리 형태의 부품입니다.",
     "아이들러 풀리 브래킷은 벨트를 눌러 주는 부품입니다. V-벨트로 동력을 전달할 때 벨트의 텐션을 확보하려고 씁니다. 생김새는 풀리와 같아요."),
    ("장력이 맞으면 미끄러짐이 없어 동력이 그대로 전달되고, 벨트와 풀리가 덜 닳아 교체 주기가 길어집니다.",
     "장력이 맞으면 미끄러짐이 없습니다. 동력이 그대로 전달돼요. 벨트와 풀리도 덜 닳아 교체 주기가 길어집니다."),
    ("현장에서는 설비가 들어갈 영역을 폴리선으로 두르면 넓이가 한 번에 나오고, 자리를 옮겨 볼 때도 통째로 잡아 끕니다.",
     "현장에서는 설비가 들어갈 영역을 폴리선으로 두릅니다. 그러면 넓이가 한 번에 나와요. 자리를 옮겨 볼 때도 통째로 잡아 끕니다."),
    ("그러니 목이 시작하는 자리는 세로 중심선에서 좌우로 40씩 떨어진 베이스 윗면 위의 두 점입니다.",
     "그러니 목이 시작하는 자리는 두 점이에요. 세로 중심선에서 좌우로 40씩 떨어진 베이스 윗면 위입니다."),
    ("PM(예방보전) 과정에서 조립도를 열어 부품을 찾고, 그 부품 도면을 들고 가공집과 이야기합니다.",
     "PM, 그러니까 예방보전 과정에서 조립도를 열어 부품을 찾습니다. 그 부품 도면을 들고 가공집과 이야기해요."),
]

HAP = re.compile(r"(니다|니까|십시오|합시다|십시다)$")
HAE = re.compile(r"[가-힣](요|죠)$")


def narration_lines(body):
    """낭독 문단의 (인덱스, 줄) — 네 칸 들여쓴 줄이 낭독이다."""
    for i, line in enumerate(body.split("\n")):
        if line.startswith("    ") and not line.startswith("    >"):
            yield i, line


def soften(body):
    """한 문단 안에서 하나 걸러 부드럽게 한다."""
    lines = body.split("\n")
    changed = 0
    for i, line in list(narration_lines(body)):
        out = []
        pos = 0
        last = -999           # 직전에 바꾼 자리. 너무 가까우면 건너뛴다.
        for m in SOFTEN_RX.finditer(line):
            # 백틱 안(타이핑할 값)은 건드리지 않는다.
            if line.count("`", 0, m.start()) % 2 == 1:
                continue
            # 해요체가 바로 옆 문장에 또 오면 수다스러워진다. 한 문장은 띄운다.
            if m.start() - last < 30:
                continue
            last = m.end()
            out.append(line[pos:m.start()])
            out.append(SOFTEN_MAP[m.group(0)])
            pos = m.end()
            changed += 1
        if out:
            out.append(line[pos:])
            lines[i] = "".join(out)
    return "\n".join(lines), changed


def ratio(body):
    hap = hae = 0
    for _, line in narration_lines(body):
        t = re.sub(r"`[^`]*`", "값", line[4:])
        t = re.sub(r"^\([^)]*\)\s*", "", t)
        for s in re.split(r"(?<=[.!?])\s+", t):
            s = s.strip()
            if not s or not re.search(r"[가-힣]", s):
                continue
            core = re.sub(r"[\"'\)\]\}»”’\s.!?…]+$", "", s)
            if HAP.search(core):
                hap += 1
            elif HAE.search(core):
                hae += 1
    return hap, hae


def main():
    dry = "--dry-run" in sys.argv
    paths = sorted(glob.glob(os.path.join(
        ROOT, "projects", "autocad-technician", "lesson-0*", "SCRIPT.md")))
    before_h = before_e = after_h = after_e = 0
    out = {}
    fixed = split_n = soft_n = 0
    for p in paths:
        body = io.open(p, encoding="utf-8").read()
        h, e = ratio(body)
        before_h += h
        before_e += e
        for a, b in FIXES:
            if a in body:
                body = body.replace(a, b)
                fixed += 1
        for a, b in SPLITS:
            if a in body:
                body = body.replace(a, b)
                split_n += 1
        body, n = soften(body)
        soft_n += n
        h, e = ratio(body)
        after_h += h
        after_e += e
        out[p] = body

    tot_b = before_h + before_e
    tot_a = after_h + after_e
    print(f"  문어체·번역투 {fixed}곳 · 긴 문장 {split_n}곳 · 어투 완화 {soft_n}곳")
    print(f"  해요체 비율  {before_e * 100 / max(1, tot_b):.1f}%  →  {after_e * 100 / max(1, tot_a):.1f}%"
          f"   (목표 20~30%)")
    if "--report" in sys.argv or dry:
        print("\n--dry-run — 쓰지 않았다." if dry else "")
        return 0
    for p, body in out.items():
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)
    print(f"\n대본 {len(out)}개를 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
