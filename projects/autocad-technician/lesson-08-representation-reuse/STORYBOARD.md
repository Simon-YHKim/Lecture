---
format: 1920x1080
duration: 11m00s
message: "EDU-SB-01의 완성 형상에 단면 표현·재사용 심볼·주석 관리를 더한다."
arc: "누적 상태 확인 → A–A HATCH → 센서 BLOCK → 주석 GROUP → 도면틀 점검 → 시험 고지"
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L07_GEOMETRY_FINAL
checkpoint_out: L08_REPRESENTED
paper: A3-landscape
projection: third-angle
---

## Frame 1 — L07 형상에 표현 정보를 더한다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 12s
- transition_in: cut
- scene: EDU-SB-01의 L07_GEOMETRY_FINAL과 BORDER·TITLE·HATCH·OUTLINE·CENTER·HIDDEN Layer를 확인한다.
- voiceover: "같은 A3 제3각법 도면에 표현과 관리 정보만 더해 L08_REPRESENTED를 만듭니다."
- media: motion-only

3D 모델·치수·지시사항을 제한시간 안에 처리하는 시험 흐름에서 현재 위치를 표시한다.

## Frame 2 — A–A 단면을 HATCH로 구분한다

- status: animated
- src: compositions/frames/02-hatch.html
- duration: 150s
- poster: 22s
- transition_in: magenta-rule-wipe
- scene: A–A 단면의 열린 경계와 닫힌 OUTLINE을 비교하고, X=40이 통과하는 Ø4 sensorPattern·AF30 포켓·Ø20 구멍·22×8 장공의 네 빈 영역을 확인한 뒤 DEMO-01 HATCH로 전환한다.
- voiceover: "HATCH Layer에는 절단된 재료 영역만 남기고 Ø4 패턴 구멍, AF30 포켓, Ø20 구멍, 상부 장공의 네 빈 영역은 비웁니다."
- media: DEMO-01 HATCH USER RECORDING

해칭 패턴보다 경계의 폐합과 네 빈 영역의 단면 의미를 먼저 검수한다.

## Frame 3 — 센서 심볼을 BLOCK·INSERT한다

- status: animated
- src: compositions/frames/03-block-insert.html
- duration: 180s
- poster: 26s
- transition_in: technical-cut
- scene: L07에서 SCALE Reference로 교정한 센서 참조 윤곽을 CENTER 기준점의 BLOCK 정의로 바꾸고 인스턴스를 INSERT한 뒤 DEMO-02로 이어진다.
- voiceover: "센서 심볼은 하나의 BLOCK 정의로 관리하고 필요한 위치에 INSERT합니다."
- media: DEMO-02 BLOCK / INSERT USER RECORDING

OUTLINE과 CENTER 관계를 유지하며 복사본과 정의 인스턴스의 차이를 보여 준다.

## Frame 4 — TITLE 주석은 GROUP으로 묶는다

- status: animated
- src: compositions/frames/04-group-compare.html
- duration: 120s
- poster: 20s
- transition_in: split-wipe
- scene: TITLE Layer의 A–A 라벨·리더를 선택 묶음으로 관리하고 DEMO-03으로 전환한다.
- voiceover: "재사용 정의가 아니라 선택 편의만 필요하므로 주석은 GROUP으로 관리합니다."
- media: DEMO-03 GROUP USER RECORDING

BLOCK과 GROUP을 누적 도면의 실제 역할로 구분한다.

## Frame 5 — BORDER·TITLE과 여섯 Layer를 점검한다

- status: animated
- src: compositions/frames/05-guided-practice.html
- duration: 105s
- poster: 18s
- transition_in: cut
- scene: 420×297 A3 외관선, 우측 하단 표제란과 BORDER·TITLE·HATCH·OUTLINE·CENTER·HIDDEN을 검수한다.
- voiceover: "형상만 보지 말고 A3 외관선과 표제란까지 확인해 L08_REPRESENTED로 저장합니다."
- media: motion-only

각 Layer가 담당 객체를 가리키면 체크포인트가 승급된다.

## Frame 6 — 표현 누락의 감점 위험을 남긴다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 45s
- poster: 16s
- transition_in: magenta-rule-wipe
- scene: L08_REPRESENTED에서 다음 DIM 단계로 연결하며 시험 감점 항목을 표시한다.
- voiceover: "도면틀·표제란·Layer·제3각법·축척 누락은 감점 위험이며 공식 문제지가 우선합니다."
- media: motion-only

`L08_REPRESENTED → L09_RELEASE_CANDIDATE` 상태선을 표시한다.
