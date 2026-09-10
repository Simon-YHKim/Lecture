"""Regenerate the course-level documents from the lessons that exist.

`course-continuity.json` and `recording-map.json` used to be maintained by hand
beside the lessons they described, which is the same two-copies problem the
frame durations had. They are derived here instead, so a renamed lesson or a
changed script cannot leave them behind.

    python scripts/part/write_course_docs.py
"""

import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import episodes  # noqa: E402
import verify_course as vc  # noqa: E402
from narrate_tts import verify_script_hash, verify_tempo_timing, frame_hold  # noqa: E402

ROOT = "projects/autocad-technician"

TOPIC = {
    "lesson-01-orientation": "오리엔테이션",
    "lesson-02-part-and-template": "부품 이해와 도면 환경",
    "lesson-03-baseline-profile": "기준선과 외곽",
    "lesson-04-circles-arcs": "원·호·오프셋",
    "lesson-05-three-views": "제3각법 3뷰와 반복",
    "lesson-06-editing-symbols": "편집과 표현",
    "lesson-07-dimensioning-release": "치수와 출도",
    "lesson-08-exam-and-qa": "시험 안내와 Q&A",
}


def clock(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def scan():
    out = []
    for i, (slug, cp_in, cp_out) in enumerate(vc.LESSONS, 1):
        d = os.path.join(ROOT, slug)
        with open(os.path.join(d, 'narration-timing.json'), encoding='utf-8') as fh:
            timing = json.load(fh)
        verify_script_hash(d, timing)
        verify_tempo_timing(timing, required=True)
        with io.open(os.path.join(d, "index.html"), encoding="utf-8") as fh:
            index = fh.read()
        slots = vc._SLOT.findall(index)
        if [s[0] for s in slots] != [f['id'] for f in timing['frames']]:
            raise ValueError(slug + ': master frames differ from narration timing; retime first')
        clock_sec, hold = 0.0, frame_hold(timing)
        for (_stem, start, duration), frame in zip(slots, timing['frames']):
            expected = round(frame['duration'] + hold, 3)
            if abs(float(start) - clock_sec) > .002 or abs(float(duration) - expected) > .002:
                raise ValueError(slug + ': master has not adopted current narration timing; retime first')
            clock_sec = round(clock_sec + expected, 3)
        total = sum(float(s[2]) for s in slots)
        sp = os.path.join(d, "SCRIPT.md")
        steps = beats.parse_steps(sp, 5) or beats.parse_steps(sp, 8)
        demo = [s for s in slots if "demo" in s[0] or "build-template" in s[0]]
        out.append({
            "no": i, "slug": slug, "topic": TOPIC[slug],
            "durationSec": int(round(total)), "frames": len(slots),
            "checkpointIn": cp_in, "checkpointOut": cp_out,
            "demoId": "DEMO-01" if demo else None,
            "demoSec": round(sum(float(x[2]) for x in demo), 3) if demo else 0,
            "demoParts": [{"id": "DEMO-01" + "ABCDEFGH"[k],
                           "lengthSec": round(float(x[2]), 3)}
                          for k, x in enumerate(demo)] if len(demo) > 1 else [],
            "cutAfterStep": episodes.cuts_for(slug),
            "steps": len(steps),
            "delivery": {"entry": "index.html", "title": TOPIC[slug],
                         "lengthSec": round(total, 3), "frames": [s[0] for s in slots]},
            "narrationTempo": timing['tempo'],
        })
    return out


def main():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)
    L = scan()
    total = sum(x["durationSec"] for x in L)

    io.open(os.path.join(ROOT, "course-continuity.json"), "w",
            encoding="utf-8", newline="\n").write(json.dumps({
                "part": "EDU-IB-02",
                "partName": "아이들러 풀리 브래킷",
                "paper": "A3-landscape",
                "projection": "third-angle",
                "layers": ["외형선", "중심선", "숨은선", "치수선"],
                "lessonCount": len(L),
                "deliveryMode": "lesson",
                "videoCount": len(L),
                "totalSec": total,
                "note": ("차시마다 새 파일을 열지 않는다. 앞 차시의 checkpointOut 파일을 열어 "
                         "이어 그린다. 이 파일은 scripts/part/write_course_docs.py 가 만든다."),
                "lessons": [{k: v for k, v in x.items() if k != "steps"} for x in L],
            }, ensure_ascii=False, indent=2) + "\n")

    io.open(os.path.join(ROOT, "recording-map.json"), "w",
            encoding="utf-8", newline="\n").write(json.dumps({
                "note": ("차시마다 통합 영상 하나를 전달한다. cutAfterStep은 실습 녹화의 내부 조각 경계다. "
                         "lengthSec은 현재 master의 실측 음성 기반 슬롯 길이이며 실제 AutoCAD 조작 검수는 별도다. "
                         "입력 녹화는 목표 슬롯과 원본 1프레임+3ms 이내로 같아야 하며 자동으로 자르거나 늘이지 않는다."),
                "recordings": [{
                    "lesson": x["no"], "slug": x["slug"], "demoId": x["demoId"],
                    "lengthSec": x["demoSec"], "steps": x["steps"],
                    "cutAfterStep": x["cutAfterStep"], "parts": x["demoParts"],
                    "opens": x["checkpointIn"], "saves": x["checkpointOut"],
                } for x in L if x["demoId"]],
                "deliveries": [{"lesson": x["no"], "slug": x["slug"],
                                **x["delivery"]} for x in L],
            }, ensure_ascii=False, indent=2) + "\n")

    io.open(os.path.join(ROOT, "COURSE_PLAN.md"), "w",
            encoding="utf-8", newline="\n").write(
        "# COURSE PLAN — AutoCAD Technician\n\n"
        "LG이노텍 「Green Star」 테크니션 인증제 실습과정. 부품 하나를 2~7차시의 여섯 실습 차시에 걸쳐\n"
        "처음부터 끝까지 그리고, 마지막 한 차시에서 시험 진행과 질문을 다룬다.\n"
        "도면 번호 `EDU-IB-02`, 아이들러 풀리 브래킷.\n\n"
        "전체 %s · A3 가로 · 제3각법 · 레이어 네 개\n\n" % clock(total)
        + "| 차시 | 주제 | 길이 | 프레임 | 여는 파일 | 저장하는 상태 |\n"
          "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join("| %d | %s | %s | %d | %s | %s |"
                   % (x["no"], x["topic"], clock(x["durationSec"]), x["frames"],
                      x["checkpointIn"] or "—", x["checkpointOut"] or "—") for x in L)
        + "\n\n## 통합 전달\n\n차시당 영상 하나, 전체 8개를 전달한다. 에피소드 분할과 20분 상한은 적용하지 않는다. "
          "Heami Rate 0 원본에 음높이 보존 1.38배속을 적용하고 결과 음성의 실제 길이에 맞춘다. "
          "학생 전달의 기준은 각 차시 `index.html`이다. 과거 `compositions/episodes/` 파일은 역사 자료이며 전달·갱신 대상이 아니다.\n\n"
        + "| 차시 | 제목 | 길이 | 프레임 |\n| --- | --- | --- | --- |\n"
        + "\n".join(
            "| %d | %s | %s | %s |"
            % (x["no"], e["title"], clock(e["lengthSec"]),
               " · ".join("`%s`" % f for f in e["frames"]))
            for x in L for e in [x["delivery"]])
        + "\n\n합계 %d개 통합 차시. 실습 녹화 내부의 단계 경계만 "
          "`scripts/part/episodes.json`에 보존한다.\n" % len(L)
        + "\n\n## 이 과정이 스스로 지키는 것\n\n"
          "- **길이는 대본이 정한다.** 프레임 길이도 항목 등장 시각도 `SCRIPT.md` 에서 계산된다.\n"
          "  손으로 적은 숫자는 대본이 바뀌는 순간 조용히 어긋난다 (`LESSON_STYLE.md` 13·14번).\n"
          "- **화면 글자는 낭독의 요약이다.** 내레이터가 읽지 않는 문장을 화면에 올리지 않는다.\n"
          "- **차시는 이어진다.** 매 차시 앞 차시의 저장 상태를 열어서 그 위에 그린다.\n"
          "- **규격은 지어내지 않는다.** 용지·표제란·레이어는 교재를 근거로 한다.\n"
          "  실제 과제 지시가 언제나 우선한다 (`LESSON_STYLE.md` 6번).\n\n"
          "## 검사\n\n"
          "    pwsh -File scripts/check-course-projects.ps1\n"
          "\n대본·실측 음성·master의 프레임 시각과 정본 정책을 함께 확인한다.\n"
          "HyperFrames 검사는 `prepare_lecture.py`로 만든 새 통합 프로젝트와 장면별 검사 사본에서 실행한다.\n"
          "원본 폴더에는 과거 episode가 남아 있으므로 현재 전달의 검증 범위로 사용하지 않는다.\n\n"
          "## 다시 만들기\n\n"
          "    python scripts/part/scaffold_lesson_01.py projects/autocad-technician/lesson-01-orientation\n"
          "    python scripts/part/scaffold_lesson_02.py projects/autocad-technician/lesson-02-part-and-template\n"
          "    python scripts/part/scaffold_lessons_3_7.py\n"
          "    python scripts/part/lesson_eight.py\n\n"
          "스캐폴드는 한 번만 돌린다. 그 뒤 프레임은 HyperFrames Studio 에서 직접 편집하는\n"
          "저작물이고, 다시 돌리면 Studio 가 심어 둔 `data-hf-id` 와 편집이 사라진다.\n\n"
          "이전 10차시 구성은 `_archive/` 에 있다. 빌드·검사 대상이 아니다.\n")

    # RECORDING_GUIDE.md is reviewed operational guidance, not a generated table.

    print("과정 문서 3개 재생성 — 전체 %s, %d차시" % (clock(total), len(L)))
    for x in L:
        print("  %d %-32s %6s  DEMO %5s  %d단계"
              % (x["no"], x["slug"], clock(x["durationSec"]),
                 clock(x["demoSec"]) if x["demoSec"] else "—", x["steps"]))


if __name__ == "__main__":
    main()
