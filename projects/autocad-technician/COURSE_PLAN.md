# COURSE PLAN — AutoCAD Technician

LG이노텍 「Green Star」 테크니션 인증제 실습과정. 부품 하나를 일곱 차시에 걸쳐
처음부터 끝까지 그리고, 마지막 한 차시에서 시험 진행과 질문을 다룬다.
도면 번호 `EDU-IB-02`, 아이들러 풀리 브래킷.

전체 221:12 · A3 가로 · 제3각법 · 레이어 네 개

| 차시 | 주제 | 길이 | 프레임 | 여는 파일 | 저장하는 상태 |
| --- | --- | --- | --- | --- | --- |
| 1 | 오리엔테이션 | 7:07 | 6 | — | — |
| 2 | 부품 이해와 도면 환경 | 25:55 | 11 | — | L02_TEMPLATE |
| 3 | 기준선과 외곽 | 32:51 | 9 | L02_TEMPLATE | L03_PROFILE |
| 4 | 원·호·오프셋 | 31:06 | 9 | L03_PROFILE | L04_FEATURES |
| 5 | 제3각법 3뷰와 반복 | 36:51 | 9 | L04_FEATURES | L05_VIEWS |
| 6 | 편집과 표현 | 35:48 | 9 | L05_VIEWS | L06_REPRESENTED |
| 7 | 치수와 출도 | 42:51 | 9 | L06_REPRESENTED | L07_RELEASE |
| 8 | 시험 안내와 Q&A | 8:43 | 7 | — | — |

## 이 과정이 스스로 지키는 것

- **길이는 대본이 정한다.** 프레임 길이도 항목 등장 시각도 `SCRIPT.md` 에서 계산된다.
  손으로 적은 숫자는 대본이 바뀌는 순간 조용히 어긋난다 (`LESSON_STYLE.md` 13·14번).
- **화면 글자는 낭독의 요약이다.** 내레이터가 읽지 않는 문장을 화면에 올리지 않는다.
- **차시는 이어진다.** 매 차시 앞 차시의 저장 상태를 열어서 그 위에 그린다.
- **규격은 지어내지 않는다.** 용지·표제란·레이어는 교재를 근거로 한다.
  실제 과제 지시가 언제나 우선한다 (`LESSON_STYLE.md` 6번).

## 검사

    pwsh -File scripts/check-course-projects.ps1
    pwsh -File scripts/check-course-projects.ps1 -RunHyperFramesChecks

첫 번째는 빌드 결과가 대본과 맞는지 본다 — 대본을 고치고 스캐폴드를 다시
돌리지 않으면 여기서 걸린다. 두 번째는 각 차시에 `npm run check` 를 더한다.

## 다시 만들기

    python scripts/part/scaffold_lesson_01.py projects/autocad-technician/lesson-01-orientation
    python scripts/part/scaffold_lesson_02.py projects/autocad-technician/lesson-02-part-and-template
    python scripts/part/scaffold_lessons_3_7.py
    python scripts/part/lesson_eight.py

스캐폴드는 한 번만 돌린다. 그 뒤 프레임은 HyperFrames Studio 에서 직접 편집하는
저작물이고, 다시 돌리면 Studio 가 심어 둔 `data-hf-id` 와 편집이 사라진다.

이전 10차시 구성은 `_archive/` 에 있다. 빌드·검사 대상이 아니다.
