"""Emit BRIEF.md and STORYBOARD.md for lessons 3-7 from what was actually built.

Both files used to be written by hand and then drifted from the frames the
moment a script paragraph changed. Here they are generated from the same plan
that drives the motion, so a stale duration in a document is not possible.
"""

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import lesson_build as lb  # noqa: E402

ROOT = "projects/autocad-technician"


def clock(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def write(lesson_dir, L, meta):
    name = os.path.basename(os.path.normpath(lesson_dir))
    script = beats.parse_script(os.path.join(lesson_dir, "SCRIPT.md"))
    steps = beats.parse_steps(os.path.join(lesson_dir, "SCRIPT.md"), 5)
    script[5] = list(steps)

    rows, start = [], 0
    demo = int(round(sum(beats.read_seconds(t) for _, t in steps)
                     * lb.DEMO_FACTOR / 10.0)) * 10
    for i, (stem, _fn, line_no, _key) in enumerate(lb.PLAN, 1):
        fixed = 12 if line_no == 1 else (demo if line_no == 5 else None)
        spans, dur = beats.plan(script[line_no], duration=fixed)
        rows.append((i, stem, start, dur, len(beats.beat_spans(spans))))
        start += dur
    total = start

    io.open(os.path.join(lesson_dir, "BRIEF.md"), "w", encoding="utf-8", newline="\n").write(
        "---\nworkflow: general-video\nflow: automation\nstoryboard: yes\n"
        'message: "%s"\n' % meta["message"]
        + "destination: desktop-course\naspect: 1920x1080\nlanguage: ko\n"
        'audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"\n'
        "length: %dm%02ds\n" % (total // 60, total % 60)
        + "angle: %s\nnarration: user-recorded\nstyle_preset: lg-training\n" % name
        + "part_id: EDU-IB-02\ncheckpoint_in: %s\ncheckpoint_out: %s\n"
          % (L["cp"].split(" → ")[0], L["cp_out"])
        + "paper: A3-landscape\nprojection: third-angle\nrecording_slots: 1\n---\n\n"
        + "## Intent\n\n" + meta["intent"] + "\n\n"
        + "## Must have\n\n"
        + "\n".join("- " + m for m in meta["mustHave"]) + "\n\n"
        + "## Must not\n\n"
        + "\n".join("- " + m for m in meta["mustNot"]) + "\n\n"
        + "## Frames\n\n| # | 파일 | 길이 | 비트 |\n| --- | --- | --- | --- |\n"
        + "\n".join("| %d | `%s` | %ds | %s |"
                    % (i, stem, dur, n if n else "—") for i, stem, _s, dur, n in rows)
        + "\n\n프레임 길이와 비트 시각은 `SCRIPT.md` 에서 계산된다 "
          "(`LESSON_STYLE.md` 13·14번). 이 표는 손으로 고치지 않는다.\n")

    io.open(os.path.join(lesson_dir, "STORYBOARD.md"), "w", encoding="utf-8", newline="\n").write(
        "# STORYBOARD — %d차시 · %s\n\n" % (L["no"], L["title"])
        + "전체 %s · 1920×1080 · 녹화 구간 1개 (`DEMO-01`, %s)\n\n" % (clock(total), clock(demo))
        + "**모든 시각은 `SCRIPT.md` 에서 계산된다.** 문단 앞 `(N …)` 이 N번째 항목의 비트다.\n"
          "아래 값은 `python scripts/part/scaffold_lessons_3_7.py %d` 의 출력이지 "
          "사람이 정한 값이 아니다.\n\n" % L["no"]
        + "| # | 컴포지션 | 시작 | 길이 | 화면 | 비트 |\n| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| %d | `l%df%d` | %s | %ds | %s | %s |"
            % (i, L["no"], i, clock(s), dur, desc, n if n else "—")
            for (i, _stem, s, dur, n), desc in zip(rows, [
                "검정 타이틀 · **%s**" % L["title"],
                "왼쪽 카드 4장(마크 포함) / 오른쪽 정면도",
                "개념 카드 4장 + 하단 문단",
                "왼쪽 도면 / 오른쪽 표 6행 — 행마다 도면의 해당 위치가 붉어진다",
                "왼쪽 **녹화 삽입 영역** + 진행 바 / 오른쪽 %d단계" % len(steps),
                "확인 카드 4장 + 하단 문단",
                "2분할 마무리",
                "인사 — 검정 바탕 · 「고생하셨습니다」",
            ]))
        + "\n\n## 이 차시의 도면 강조\n\n"
        + "\n".join("- %s → `%s`" % (r[1], " ".join(r[0]) if r[0] else "없음")
                    for r in L["ondrawing"])
        + "\n\n강조는 클래스 토글이 아니라 색·불투명도 트윈이다 (`LESSON_STYLE.md` 17번).\n\n"
          "## 녹화 구간\n\n"
          "`DEMO-01` %s = %d단계 낭독 %s × 1.3. 타이핑·대화상자·대기는 말하지 않는다.\n"
          "실제 녹화 길이가 다르면 `SCRIPT.md` Line 5 를 고치고 스캐폴드를 다시 돌린다.\n\n"
          "## 검증\n\n    cd %s/%s\n    npm run check\n"
          % (clock(demo), len(steps),
             clock(sum(beats.read_seconds(t) for _, t in steps)), ROOT, name))
    return total
