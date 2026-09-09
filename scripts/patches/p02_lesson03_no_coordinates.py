# -*- coding: utf-8 -*-
"""3차시 강의 자료에서 좌표 교습을 걷어낸다 — 대본과 화면을 함께.

무엇이 어긋나 있었나
--------------------
자습본은 2026-09-09 라운드에서 골뱅이 상대좌표를 84곳 전부 걷어내고 마우스 커서 +
객체 스냅 + 수치 입력으로 다시 썼다. 그런데 **녹화용 대본과 프레임은 그대로였다.**
그 결과 3차시 한 차시 안에서 앞뒤가 서로를 부정하고 있었다.

    03-concept 프레임 : 「시작점은 절대좌표, 이어지는 변은 상대좌표」
    05-demo 대본      : 「좌표는 치지 않습니다」

게다가 대본 Line 3 은 카드가 다섯인데 프레임은 넷이라 다섯째 문단이 걸릴 항목이
화면에 없었다.

무엇으로 바꾸나
---------------
카드 넷을 이 과정이 실제로 쓰는 점 찍는 방법 넷으로 바꾼다. 개수를 넷으로 두면
타임라인의 tk1~tk4 구조와 잰 시각이 그대로 살아 있고, 바뀌는 것은 글과 마크뿐이다.

    1 객체 스냅            F3 — 형상의 특징점에 붙여 찍는다
    2 직교와 직접 거리 입력  F8 · F12 — 방향은 마우스, 길이는 숫자
    3 객체 스냅 추적과 FROM  F11 — 형상에 없는 점을 두 안내선의 교차로 잡는다
    4 LINE · PLINE · REC    낱개인가 하나인가

Line 4 「도면 위에서」의 앞 세 행도 REC + CHAMFER 순서로 바꾼다. 11 과 115 라는
계산값은 이 방법에서 아예 나오지 않는다 — 그 사실 자체가 이 방법을 쓰는 이유다.

    python scripts/patches/p02_lesson03_no_coordinates.py [--dry-run]
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L3 = os.path.join(ROOT, "projects", "autocad-technician", "lesson-03-baseline-profile")
FRAMES = os.path.join(L3, "compositions", "frames")


def kw(text):
    return " ".join(f'<span class="kw">{w}</span>' for w in text.split())


# ── 프레임 03-concept · 카드 넷 ────────────────────────────────────────────
ICONS = {
    # 선 위의 끝점(네모)과 중간점(세모) — AutoCAD 가 실제로 띄우는 표식이다.
    1: ('<path d="M4 24h24"/><rect x="2" y="22" width="4" height="4"/>'
        '<path d="M16 21.2l2.4 3.6h-4.8z"/><path d="M16 10v6"/><circle cx="16" cy="7" r="2.2"/>'),
    # 십자 커서가 축에 갇힌 모습 + 커서 옆 수치 입력칸.
    2: ('<path d="M3 20h16M11 12v16"/><rect x="19" y="5" width="11" height="7"/>'
        '<path d="M21.5 8.5h6"/><path d="M11 20l7.5-7.5" stroke-dasharray="2.5 2"/>'),
    # 두 특징점에서 뻗은 추적 안내선이 만나 없는 점을 만든다.
    3: ('<circle cx="6" cy="26" r="2"/><circle cx="26" cy="6" r="2"/>'
        '<path d="M6 24V8h12" stroke-dasharray="3 2.4" stroke-linecap="butt"/>'
        '<path d="M24 6H10v16" stroke-dasharray="3 2.4" stroke-linecap="butt"/>'
        '<path d="M7 5l6 6M13 5l-6 6" transform="translate(-3 -1)"/>'),
    # 낱개 선분들과 한 덩어리 윤곽 — 원래 카드의 뜻을 그대로 둔다.
    4: ('<path d="M3 10h9M15 10h9"/><rect x="1.6" y="8.4" width="3.2" height="3.2"/>'
        '<rect x="22.4" y="8.4" width="3.2" height="3.2"/>'
        '<path d="M4 30v-8l6-4h16v12z"/>'),
}

CARDS = {
    1: ("객체 스냅 F3", "형상이 답을 갖고 있다",
        "커서를 올리면 끝점·중간점·중심·사분점·교차점·접점 표식이 뜬다. "
        "표식을 보고 누르면 그 점은 계산 없이 정확하다. 오늘 가장 많이 쓴다."),
    2: ("직교와 수치 F8 · F12", "방향은 마우스, 길이는 숫자",
        "직교를 켜고 가려는 쪽에 커서를 둔 뒤 길이만 친다. 동적 입력이 켜져 있으면 "
        "커서 옆 칸에 그대로 들어간다. 도면에 길이만 적힌 자리에 쓴다."),
    3: ("스냅 추적과 FROM F11", "형상에 없는 점을 만든다",
        "특징점에 커서를 잠깐 얹으면 안내선이 뻗는다. 두 안내선이 만나는 자리가 점이다. "
        "FROM 은 기준점을 하나 잡고 거기서 떨어진 자리를 찍는다."),
    4: ("LINE · PLINE · REC", "낱개인가 하나인가",
        "윤곽은 REC 이나 PLINE 으로 한 덩어리로 그린다. 간격띄우기와 면적이 한 번에 걸린다. "
        "뒤에서 자르고 둥글릴 조각은 LINE 으로 낱개로 둔다."),
}

NOTE_NEW = (
    "<b>" + kw("고르는 기준") + "</b> "
    + kw("그 점이 도면 치수에 걸려 있는가 하나다. 걸려 있으면 스냅과 추적으로 형상에서 뽑고, "
         "길이만 적혀 있으면 방향을 마우스로 잡고 숫자를 친다. 걸려 있지 않으면 그냥 클릭한다. "
         "좌표를 치는 자리는 이 과정에서 용지선 두 구석뿐이다.")
)


def rebuild_concept(text):
    for n, (title, sub, body) in CARDS.items():
        rx = re.compile(
            r'(<div class="card tk tk%d"[^>]*>)<svg class="ico".*?</svg>(.*?)</div>' % n, re.S)
        m = rx.search(text)
        if not m:
            raise SystemExit(f"03-concept: tk{n} 카드를 못 찾았다")
        svg = ('<svg class="ico" viewBox="0 0 32 32" width="58" height="58" aria-hidden="true">'
               + ICONS[n] + "</svg>")
        inner = (svg
                 + '<b style="margin-top:16px">' + kw(title) + "</b>"
                 + "<strong>" + kw(sub) + "</strong>"
                 + "<span>" + kw(body) + "</span>")
        text = text[:m.start()] + m.group(1) + inner + "</div>" + text[m.end():]
    rx = re.compile(r'(<div class="note"[^>]*>).*?(</div>)', re.S)
    if not rx.search(text):
        raise SystemExit("03-concept: note 를 못 찾았다")
    text = rx.sub(lambda m: m.group(1) + NOTE_NEW + m.group(2), text, count=1)
    return text


# ── 프레임 04-on-the-drawing · 앞 세 행 ────────────────────────────────────
ROW_EDITS = [
    ("0,0", "좌표 원점",
     "베이스 왼쪽 아래 구석. 도면이 재는 기준과 맞추면 적힌 숫자가 그대로 입력값이 된다.",
     "기준 구석", "도면이 재는 자리",
     "베이스 왼쪽 아래 구석. 도면의 치수가 대부분 여기서 나온다. 원점을 옮기지는 않고 화면에서 클릭해 잡는다."),
    ("120 × 16", "베이스 꼭짓점",
     "왼쪽 아래 0,0에서 오른쪽 아래 120,0. 모따기가 모서리를 잘라 꼭짓점이 여섯이다.",
     "120 × 16", "REC 의 치수 옵션",
     "구석 하나를 클릭하고 D 로 가로 120, 세로 16 을 친다. 네 꼭짓점이 한 번에 정확히 선다."),
    ("2-C5", "45도로 5 잘라내기",
     "가로 간 만큼 세로도 간다. 세로변은 11까지만 올라가고 윗면은 110이 된다.",
     "2-C5", "CHAMFER 로 나중에",
     "사각형을 세운 뒤 위 두 구석만 5와 5로 자른다. 11 이나 115 같은 계산값이 나올 자리가 없다."),
]


def rebuild_on_drawing(text):
    for old_a, old_b, old_c, new_a, new_b, new_c in ROW_EDITS:
        for old, new in ((old_b, new_b), (old_c, new_c)):
            plain = re.sub(r"<[^>]+>", "", text)
            if old not in plain:
                raise SystemExit(f"04-on-the-drawing: 「{old[:34]}…」 를 못 찾았다")
        # kw 로 쪼개진 상태라 어절 단위로 찾아 바꾼다.
        text = replace_kw_run(text, old_b, new_b, "04-on-the-drawing")
        text = replace_kw_run(text, old_c, new_c, "04-on-the-drawing")
    text = replace_kw_run(text, "0,0", "기준 구석", "04-on-the-drawing", once=True)
    return text


def replace_kw_run(text, old, new, where, once=True):
    """kw span 으로 쪼개진 문장을 통째로 갈아 끼운다."""
    words = old.split()
    pat = r"\s*".join(
        r"(?:<span class=\"kw\">)?" + re.escape(w) + r"(?:</span>)?" for w in words)
    rx = re.compile(pat)
    m = rx.search(text)
    if not m:
        raise SystemExit(f"{where}: 「{old[:40]}…」 를 못 찾았다")
    return text[:m.start()] + kw(new) + text[m.end():]


def main():
    dry = "--dry-run" in sys.argv
    jobs = [
        ("03-concept.html", rebuild_concept),
        ("04-on-the-drawing.html", rebuild_on_drawing),
    ]
    out = {}
    for name, fn in jobs:
        p = os.path.join(FRAMES, name)
        s = io.open(p, encoding="utf-8").read()
        out[p] = fn(s)
        print(f"  ✓ {name}")
    if dry:
        print("\n--dry-run — 쓰지 않았다.")
        return 0
    for p, s in out.items():
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print(f"\n프레임 {len(out)}개를 고쳤다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
