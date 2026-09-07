# COURSE PLAN — AutoCAD Technician

LG이노텍 「Green Star」 테크니션 인증제 실습과정. 부품 하나를 일곱 차시에 걸쳐
처음부터 끝까지 그리고, 마지막 한 차시에서 시험 진행과 질문을 다룬다.
도면 번호 `EDU-IB-02`, 아이들러 풀리 브래킷.

전체 264:26 · A3 가로 · 제3각법 · 레이어 네 개

| 차시 | 주제 | 길이 | 프레임 | 여는 파일 | 저장하는 상태 |
| --- | --- | --- | --- | --- | --- |
| 1 | 오리엔테이션 | 7:20 | 6 | — | — |
| 2 | 부품 이해와 도면 환경 | 33:41 | 11 | — | L02_TEMPLATE |
| 3 | 기준선과 외곽 | 38:17 | 10 | L02_TEMPLATE | L03_PROFILE |
| 4 | 원·호·오프셋 | 39:11 | 11 | L03_PROFILE | L04_FEATURES |
| 5 | 제3각법 3뷰와 반복 | 44:43 | 11 | L04_FEATURES | L05_VIEWS |
| 6 | 편집과 표현 | 42:30 | 11 | L05_VIEWS | L06_REPRESENTED |
| 7 | 치수와 출도 | 49:03 | 11 | L06_REPRESENTED | L07_RELEASE |
| 8 | 시험 안내와 Q&A | 9:41 | 7 | — | — |

## 편

한 편이 영상 하나다. 20분을 넘기지 않는다. `npm run render -- -c compositions/episodes/ep1.html` 로 편 하나를 뽑는다.

| 차시 | 편 | 제목 | 길이 | 프레임 |
| --- | --- | --- | --- | --- |
| 1 | 1편 | 오리엔테이션 | 7:20 | `01-title` · `02-why-drawings` · `03-how-assessed` · `04-roadmap` · `05-recap` · `06-closing` |
| 2 | 1편 | 부품과 도면 규칙 | 16:00 | `01-title` · `02-what-is-this-part` · `03-surfaces` · `04-why-this-shape` · `05-reading-dimensions` · `06-reading-symbols` · `07-sheet-and-layers` |
| 2 | 2편 | A3 템플릿 만들기 | 17:41 | `08-build-template` · `09-recap` · `10-keys` · `11-closing` |
| 3 | 1편 | 원점과 중심선 | 17:01 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` |
| 3 | 2편 | 베이스 외곽과 목 | 12:35 | `05-demo-b` |
| 3 | 3편 | 검산과 정리 | 8:41 | `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 4 | 1편 | 축 구멍과 탭 네 개 | 18:59 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` |
| 4 | 2편 | 장공과 필렛 | 10:18 | `05-demo-b` |
| 4 | 3편 | 검산과 정리 | 9:54 | `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 5 | 1편 | 평면도 | 18:11 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` |
| 5 | 2편 | 우측면도와 축 구멍 | 10:33 | `05-demo-b` |
| 5 | 3편 | 숨은선과 정리 | 15:59 | `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 6 | 1편 | 투상선 정리 | 18:41 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` |
| 6 | 2편 | 대칭 검산과 레이어 | 11:29 | `05-demo-b` |
| 6 | 3편 | 선 종류 축척과 정리 | 12:20 | `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 7 | 1편 | 치수 스타일과 전체 크기 | 18:06 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` |
| 7 | 2편 | 치수 기입 | 18:19 | `05-demo-b` |
| 7 | 3편 | 축척 확인과 출도 | 12:38 | `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 8 | 1편 | 시험 안내와 Q&A | 9:41 | `01-title` · `02-exam` · `03-qa` · `04-technician-work` · `05-field-commands` · `06-recap` · `07-closing` |

합계 19편. 끊는 자리와 그 이유는 `scripts/part/episodes.json` 에 있다.


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

문서도 손으로 쓰지 않는다. 정본 기하와 차시 연결에서 생성된다.

    python scripts/part/edu_ib_02.py projects/autocad-technician/master-part-geometry.json --json
    python scripts/part/write_master_spec.py     # MASTER_DRAWING_SPEC.md
    python scripts/part/write_course_docs.py     # course-continuity.json · recording-map.json

스캐폴드는 한 번만 돌린다. 그 뒤 프레임은 HyperFrames Studio 에서 직접 편집하는
저작물이고, 다시 돌리면 Studio 가 심어 둔 `data-hf-id` 와 편집이 사라진다.

이전 10차시 구성은 `_archive/` 에 있다. 빌드·검사 대상이 아니다.
