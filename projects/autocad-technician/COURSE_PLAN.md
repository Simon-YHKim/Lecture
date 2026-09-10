# COURSE PLAN — AutoCAD Technician

LG이노텍 「Green Star」 테크니션 인증제 실습과정. 부품 하나를 2~7차시의 여섯 실습 차시에 걸쳐
처음부터 끝까지 그리고, 마지막 한 차시에서 시험 진행과 질문을 다룬다.
도면 번호 `EDU-IB-02`, 아이들러 풀리 브래킷.

전체 181:49 · A3 가로 · 제3각법 · 레이어 네 개

| 차시 | 주제 | 길이 | 프레임 | 여는 파일 | 저장하는 상태 |
| --- | --- | --- | --- | --- | --- |
| 1 | 오리엔테이션 | 5:36 | 6 | — | — |
| 2 | 부품 이해와 도면 환경 | 26:55 | 11 | — | L02_TEMPLATE |
| 3 | 기준선과 외곽 | 26:47 | 10 | L02_TEMPLATE | L03_PROFILE |
| 4 | 원·호·오프셋 | 27:26 | 11 | L03_PROFILE | L04_FEATURES |
| 5 | 제3각법 3뷰와 반복 | 28:39 | 11 | L04_FEATURES | L05_VIEWS |
| 6 | 편집과 표현 | 28:14 | 11 | L05_VIEWS | L06_REPRESENTED |
| 7 | 치수와 출도 | 31:37 | 11 | L06_REPRESENTED | L07_RELEASE |
| 8 | 시험 안내와 Q&A | 6:35 | 7 | — | — |

## 통합 전달

차시당 영상 하나, 전체 8개를 전달한다. 에피소드 분할과 20분 상한은 적용하지 않는다. Heami Rate 0 원본에 음높이 보존 1.38배속을 적용하고 결과 음성의 실제 길이에 맞춘다. 학생 전달의 기준은 각 차시 `index.html`이다. 과거 `compositions/episodes/` 파일은 역사 자료이며 전달·갱신 대상이 아니다.

| 차시 | 제목 | 길이 | 프레임 |
| --- | --- | --- | --- |
| 1 | 오리엔테이션 | 5:36 | `01-title` · `02-why-drawings` · `03-how-assessed` · `04-roadmap` · `05-recap` · `06-closing` |
| 2 | 부품 이해와 도면 환경 | 26:54 | `01-title` · `02-what-is-this-part` · `03-surfaces` · `04-why-this-shape` · `05-reading-dimensions` · `06-reading-symbols` · `07-sheet-and-layers` · `08-build-template` · `09-recap` · `10-keys` · `11-closing` |
| 3 | 기준선과 외곽 | 26:46 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` · `05-demo-b` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 4 | 원·호·오프셋 | 27:26 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` · `05-demo-b` · `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 5 | 제3각법 3뷰와 반복 | 28:39 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` · `05-demo-b` · `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 6 | 편집과 표현 | 28:14 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` · `05-demo-b` · `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 7 | 치수와 출도 | 31:36 | `01-title` · `02-today` · `03-concept` · `04-on-the-drawing` · `05-demo-a` · `05-demo-b` · `05-demo-c` · `06-check` · `07-recap` · `08-keys` · `09-closing` |
| 8 | 시험 안내와 Q&A | 6:35 | `01-title` · `02-exam` · `03-qa` · `04-technician-work` · `05-field-commands` · `06-recap` · `07-closing` |

합계 8개 통합 차시. 실습 녹화 내부의 단계 경계만 `scripts/part/episodes.json`에 보존한다.


## 이 과정이 스스로 지키는 것

- **길이는 대본이 정한다.** 프레임 길이도 항목 등장 시각도 `SCRIPT.md` 에서 계산된다.
  손으로 적은 숫자는 대본이 바뀌는 순간 조용히 어긋난다 (`LESSON_STYLE.md` 13·14번).
- **화면 글자는 낭독의 요약이다.** 내레이터가 읽지 않는 문장을 화면에 올리지 않는다.
- **차시는 이어진다.** 매 차시 앞 차시의 저장 상태를 열어서 그 위에 그린다.
- **규격은 지어내지 않는다.** 용지·표제란·레이어는 교재를 근거로 한다.
  실제 과제 지시가 언제나 우선한다 (`LESSON_STYLE.md` 6번).

## 검사

    pwsh -File scripts/check-course-projects.ps1

대본·실측 음성·master의 프레임 시각과 정본 정책을 함께 확인한다.
HyperFrames 검사는 `prepare_lecture.py`로 만든 새 통합 프로젝트와 장면별 검사 사본에서 실행한다.
원본 폴더에는 과거 episode가 남아 있으므로 현재 전달의 검증 범위로 사용하지 않는다.

## 다시 만들기

    python scripts/part/scaffold_lesson_01.py projects/autocad-technician/lesson-01-orientation
    python scripts/part/scaffold_lesson_02.py projects/autocad-technician/lesson-02-part-and-template
    python scripts/part/scaffold_lessons_3_7.py
    python scripts/part/lesson_eight.py

스캐폴드는 한 번만 돌린다. 그 뒤 프레임은 HyperFrames Studio 에서 직접 편집하는
저작물이고, 다시 돌리면 Studio 가 심어 둔 `data-hf-id` 와 편집이 사라진다.

이전 10차시 구성은 `_archive/` 에 있다. 빌드·검사 대상이 아니다.
