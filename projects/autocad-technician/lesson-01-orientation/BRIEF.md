---
workflow: general-video
flow: automation
storyboard: yes
message: "이 과정이 왜 있고, 무엇으로 평가하며, 무엇을 어떤 순서로 배우는지 먼저 합의한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 7m07s
angle: orientation
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: none
checkpoint_out: none
recording_slots: 0
---

## Intent

일곱 차시 과정의 첫 시간이다. 도면을 한 줄도 그리지 않는다.
학습자가 이 과정의 목적과 평가 방식, 전체 순서를 알고 2차시로 넘어가게 하는 것이 전부다.

`LESSON_STYLE.md` 9번 원칙에 따라 과정 안내는 이 차시에만 둔다.
2차시 이후 화면에는 목차나 "오늘은 무엇을 한다" 같은 안내를 넣지 않는다.

## Must have

- 타이틀 화면 — `LG이노텍` · `for technician` · `Green Star` · 차시 주제
- 도면이 왜 필요한지와 도면이 갖춰야 할 다섯 가지 요건 **전부**
- 평가 방식 — 실습 과제의 형태. 제한시간·배점은 다루지 않는다
- 일곱 차시 로드맵과 차시별 종료 상태 파일명
- 2분할 마무리 — 이번에 한 일 / 다음
- 인사 화면 — 「고생하셨습니다」 + 다음 차시 안내 (`LESSON_STYLE.md` 8번)

## Must not

- 제한시간, 배점, 합격 기준 같은 확인되지 않은 평가 수치
- AutoCAD 조작 시연 (이 차시에는 녹화 구간이 없다)
- 부품 형상 설명 (2차시 소관)

## Frames

| # | 파일 | 길이 | 화면 | 비트 |
| --- | --- | --- | --- | --- |
| 1 | `01-title` | 12s | 검정 타이틀 · **오리엔테이션** | — |
| 2 | `02-why-drawings` | 136s | 도입 문장 + 요건 카드 5장 + 하단 문단 | 6 |
| 3 | `03-how-assessed` | 92s | 과제 카드 4장 + 하단 문단 | 5 |
| 4 | `04-roadmap` | 108s | 안내 문장 + 로드맵 표(차시·주제·하는 일) | 8 |
| 5 | `05-recap` | 63s | 2분할 마무리 | 2 |
| 6 | `06-closing` | 16s | 인사 — 검정 바탕 · 「고생하셨습니다」 · 다음 차시 | 2 |
