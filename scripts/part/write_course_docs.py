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
import verify_course as vc  # noqa: E402

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
        index = io.open(os.path.join(d, "index.html"), encoding="utf-8").read()
        slots = vc._SLOT.findall(index)
        total = sum(float(s[2]) for s in slots)
        sp = os.path.join(d, "SCRIPT.md")
        steps = beats.parse_steps(sp, 5) or beats.parse_steps(sp, 8)
        demo = [s for s in slots if "demo" in s[0] or "build-template" in s[0]]
        out.append({
            "no": i, "slug": slug, "topic": TOPIC[slug],
            "durationSec": int(round(total)), "frames": len(slots),
            "checkpointIn": cp_in, "checkpointOut": cp_out,
            "demoId": "DEMO-01" if demo else None,
            "demoSec": int(round(float(demo[0][2]))) if demo else 0,
            "steps": len(steps),
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
                "totalSec": total,
                "note": ("차시마다 새 파일을 열지 않는다. 앞 차시의 checkpointOut 파일을 열어 "
                         "이어 그린다. 이 파일은 scripts/part/write_course_docs.py 가 만든다."),
                "lessons": [{k: v for k, v in x.items() if k != "steps"} for x in L],
            }, ensure_ascii=False, indent=2) + "\n")

    io.open(os.path.join(ROOT, "recording-map.json"), "w",
            encoding="utf-8", newline="\n").write(json.dumps({
                "note": ("녹화 구간은 차시마다 하나이고 언제나 DEMO-01 이다. lengthSec 은 "
                         "낭독 시간 × 1.3 으로 계산한 예상치이며, 실제 녹화가 다르면 "
                         "SCRIPT.md Line 5 를 고치고 스캐폴드를 다시 돌린다."),
                "recordings": [{
                    "lesson": x["no"], "slug": x["slug"], "demoId": x["demoId"],
                    "lengthSec": x["demoSec"], "steps": x["steps"],
                    "opens": x["checkpointIn"], "saves": x["checkpointOut"],
                } for x in L if x["demoId"]],
            }, ensure_ascii=False, indent=2) + "\n")

    io.open(os.path.join(ROOT, "COURSE_PLAN.md"), "w",
            encoding="utf-8", newline="\n").write(
        "# COURSE PLAN — AutoCAD Technician\n\n"
        "LG이노텍 「Green Star」 테크니션 인증제 실습과정. 부품 하나를 일곱 차시에 걸쳐\n"
        "처음부터 끝까지 그리고, 마지막 한 차시에서 시험 진행과 질문을 다룬다.\n"
        "도면 번호 `EDU-IB-02`, 아이들러 풀리 브래킷.\n\n"
        "전체 %s · A3 가로 · 제3각법 · 레이어 네 개\n\n" % clock(total)
        + "| 차시 | 주제 | 길이 | 프레임 | 여는 파일 | 저장하는 상태 |\n"
          "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join("| %d | %s | %s | %d | %s | %s |"
                   % (x["no"], x["topic"], clock(x["durationSec"]), x["frames"],
                      x["checkpointIn"] or "—", x["checkpointOut"] or "—") for x in L)
        + "\n\n## 이 과정이 스스로 지키는 것\n\n"
          "- **길이는 대본이 정한다.** 프레임 길이도 항목 등장 시각도 `SCRIPT.md` 에서 계산된다.\n"
          "  손으로 적은 숫자는 대본이 바뀌는 순간 조용히 어긋난다 (`LESSON_STYLE.md` 13·14번).\n"
          "- **화면 글자는 낭독의 요약이다.** 내레이터가 읽지 않는 문장을 화면에 올리지 않는다.\n"
          "- **차시는 이어진다.** 매 차시 앞 차시의 저장 상태를 열어서 그 위에 그린다.\n"
          "- **규격은 지어내지 않는다.** 용지·표제란·레이어는 교재를 근거로 한다.\n"
          "  실제 과제 지시가 언제나 우선한다 (`LESSON_STYLE.md` 6번).\n\n"
          "## 검사\n\n"
          "    pwsh -File scripts/check-course-projects.ps1\n"
          "    pwsh -File scripts/check-course-projects.ps1 -RunHyperFramesChecks\n\n"
          "첫 번째는 빌드 결과가 대본과 맞는지 본다 — 대본을 고치고 스캐폴드를 다시\n"
          "돌리지 않으면 여기서 걸린다. 두 번째는 각 차시에 `npm run check` 를 더한다.\n\n"
          "## 다시 만들기\n\n"
          "    python scripts/part/scaffold_lesson_01.py projects/autocad-technician/lesson-01-orientation\n"
          "    python scripts/part/scaffold_lesson_02.py projects/autocad-technician/lesson-02-part-and-template\n"
          "    python scripts/part/scaffold_lessons_3_7.py\n"
          "    python scripts/part/lesson_eight.py\n\n"
          "스캐폴드는 한 번만 돌린다. 그 뒤 프레임은 HyperFrames Studio 에서 직접 편집하는\n"
          "저작물이고, 다시 돌리면 Studio 가 심어 둔 `data-hf-id` 와 편집이 사라진다.\n\n"
          "이전 10차시 구성은 `_archive/` 에 있다. 빌드·검사 대상이 아니다.\n")

    io.open(os.path.join(ROOT, "RECORDING_GUIDE.md"), "w",
            encoding="utf-8", newline="\n").write(
        "# RECORDING GUIDE\n\n"
        "차시마다 화면 녹화 구간이 하나씩 있다. 슬롯 이름은 언제나 `DEMO-01` 이다.\n\n"
        + "| 차시 | 주제 | 여는 파일 | 저장하는 상태 | 단계 | 예상 길이 |\n"
          "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join("| %d | %s | %s | %s | %d | %s |"
                   % (x["no"], x["topic"], x["checkpointIn"] or "—",
                      x["checkpointOut"] or "—", x["steps"], clock(x["demoSec"]))
                   for x in L if x["demoId"])
        + "\n\n예상 길이는 그 차시 `SCRIPT.md` Line 5 의 낭독 시간 × 1.3 이다.\n"
          "타이핑과 대화상자와 기다리는 시간은 말하지 않기 때문이다.\n\n"
          "## 녹화하기 전에\n\n"
          "1. 그 차시 `SCRIPT.md` 의 Line 5 를 처음부터 끝까지 읽는다. 단계 순서가 곧 녹화 순서다.\n"
          "2. **여는 파일**을 연다. 새로 만들지 않는다. 앞 차시가 저장한 상태에서 이어 그린다.\n"
          "3. 화면 배율을 100%로 두고 1920×1080 으로 녹화한다. 프레임 안 삽입 영역이 그 비율이다.\n"
          "4. 명령행이 보이게 둔다. 학습자가 따라 칠 값이 거기 뜬다.\n"
          "5. 마지막 단계는 언제나 새 이름으로 저장이다. 저장까지 녹화한다.\n\n"
          "## 녹화한 뒤\n\n"
          "녹화 파일은 **저장소 밖 비공개 위치**에 둔다. 옮겨 오지 않는다.\n\n"
          "    python scripts/part/ingest_recording.py <차시> <녹화파일>\n\n"
          "이 명령이 두 파일을 쓴다.\n\n"
          "- `recording.json` — 길이·해상도·프레임레이트만. 공개되고 커밋된다.\n"
          "- `media.local.json` — 파일의 절대경로. gitignore 되며 미리보기만 읽는다.\n\n"
          "그다음 그 차시를 다시 만들면 DEMO 프레임이 **예상치가 아니라 실제 길이**가 된다.\n\n"
          "    python scripts/part/scaffold_lessons_3_7.py <차시번호>\n\n"
          "현재 상태는 언제든 확인할 수 있다.\n\n"
          "    python scripts/part/ingest_recording.py --list\n\n"
          "## 목소리를 녹음했다면\n\n"
          "화면 녹화와 별개로 나레이션을 녹음했다면, 항목이 등장하는 시각을\n"
          "**추정이 아니라 실제 음성**에 맞출 수 있다.\n\n"
          "    pwsh -File scripts/transcribe-narration.ps1 -AudioPath <음성파일>\n"
          "    pwsh -File scripts/build-narration-timing.ps1 -LessonPath <차시> -TranscriptPath <위 결과>\n\n"
          "받아쓴 글은 비공개 위치에 남고, 저장소에는 숫자만 담긴 `narration-timing.json` 만\n"
          "들어온다. 그 파일이 있으면 스캐폴드가 음절 추정 대신 실측 시각을 쓴다.\n"
          "지금 타이밍은 초당 5.0음절 가정이라, 실제 낭독이 그보다 빠르거나 느리면\n"
          "화면이 말보다 앞서거나 뒤처진다.\n\n"
          "## 길이가 다르면\n\n"
          "손으로 프레임을 맞추지 않는다. 대본을 고치고 다시 만들거나, 위 방법으로\n"
          "실측값을 넣는다. 길이의 원본은 대본이다 (`LESSON_STYLE.md` 14번).\n")

    print("과정 문서 4개 재생성 — 전체 %s, %d차시" % (clock(total), len(L)))
    for x in L:
        print("  %d %-32s %6s  DEMO %5s  %d단계"
              % (x["no"], x["slug"], clock(x["durationSec"]),
                 clock(x["demoSec"]) if x["demoSec"] else "—", x["steps"]))


if __name__ == "__main__":
    main()
