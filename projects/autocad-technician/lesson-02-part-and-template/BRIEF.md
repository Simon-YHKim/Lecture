---
workflow: general-video
flow: automation
storyboard: yes
message: "면마다 왜 다르게 깎는지 알면 도면의 표기가 지시로 읽히고, 그리기 전에 종이와 선의 규칙을 먼저 세운다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 25m46s
angle: part-reading-and-drawing-environment
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: none
checkpoint_out: L02_TEMPLATE
paper: A3-landscape
projection: third-angle
recording_slots: 1
---

## Intent

일곱 차시에 걸쳐 `EDU-IB-02 아이들러 풀리 브래킷` 하나를 완성하는 과정의 첫 실습 차시다.
학습자는 부품의 기능에서 형상의 이유를 읽고, 면마다 가공과 표면 거칠기가 다른 이유를 이해하고,
도면 위 모든 표기를 읽은 뒤, A3 도면틀과 레이어 네 개가 준비된 템플릿 파일을 직접 만든다.
종료 상태는 `L02_TEMPLATE`.

## Must have

- 타이틀 화면 (`LESSON_STYLE.md` 8번)
- 부품의 **용도 · 실제 역할 · 적용 예시 · 그 효과** — 네 가지를 모두
- 면마다의 **가공 방법 · 표면 거칠기 · 왜 그렇게 정했는가**, 설명하는 동안 도면에서 그 부위를 강조
- 도면 위 **모든** 치수와 기호 (13개 이상). 한 화면에 안 들어가면 나눈다
- A3 규격 — 사방 10 도면틀, 중심 마크, 200×30 표제란(이름 | 사번), 문자 높이 10
- 레이어 네 개 — 외형선 / 중심선 / 숨은선 / 치수선
- 조작 대본은 명령어·입력값·엔터·대화상자 항목까지 (`LESSON_STYLE.md` 7번)
- 2분할 마무리
- 인사 화면 — 「고생하셨습니다」 + 다음 차시 안내 (`LESSON_STYLE.md` 8번)

## Must not

- 목차나 "오늘은 무엇을 한다" 안내 (1차시 소관, `LESSON_STYLE.md` 5번)
- 교재에 근거가 없는 규격값 (`LESSON_STYLE.md` 6번)
- 표면 거칠기·기하공차·열처리의 **실습** (개념만 언급하고 넘어간다)

## Frames

| # | 파일 | 길이 | 화면 | 비트 |
| --- | --- | --- | --- | --- |
| 1 | `01-title` | 12s | 검정 타이틀 · **부품 이해와 도면 환경** | — |
| 2 | `02-what-is-this-part` | 134s | 왼쪽 카드 4장 / 오른쪽 정면도 | 4 |
| 3 | `03-surfaces` | 218s | 왼쪽 정면도 / 오른쪽 가공 표 6행 + 이유 문단 | 6 |
| 4 | `04-why-this-shape` | 100s | 왼쪽 정면도 / 오른쪽 근거 카드 5장 | 5 |
| 5 | `05-reading-dimensions` | 125s | 왼쪽 3뷰 / 오른쪽 치수 8행 | 8 |
| 6 | `06-reading-symbols` | 115s | 왼쪽 3뷰 / 오른쪽 기호 8행 | 8 |
| 7 | `07-sheet-and-layers` | 145s | 왼쪽 A3 규격도 / 오른쪽 레이어 표 + 두 문단 | 11 |
| 8 | `08-build-template` | 480s | 전체화면 **녹화 삽입 영역** — 하단 띠에 진행 중인 단계와 단축키 | 15 |
| 9 | `09-recap` | 105s | 2분할 마무리 | 2 |
| 10 | `10-keys` | 99s | 오늘 친 단축키 표 + 기능키 | 13 |
| 11 | `11-closing` | 13s | 인사 — 검정 바탕 · 「고생하셨습니다」 · 다음 차시 | 2 |
