---
workflow: general-video
flow: automation
storyboard: no
message: "Hatch로 의미를 구분하고 Block과 Group으로 반복 요소를 관리하면 도면이 읽기 쉽고 수정하기 쉬워진다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
length: 11m
angle: guided-practice
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L07_GEOMETRY_FINAL
checkpoint_out: L08_REPRESENTED
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 8차시는 `EDU-SB-01`의 `L07_GEOMETRY_FINAL`에서 이어진다. 같은 A3 가로형·제3각법 도면에 A–A 단면 HATCH, 센서 심볼 BLOCK·INSERT, 주석 GROUP을 적용하고 `BORDER`, `TITLE`, `HATCH`, `OUTLINE`, `CENTER`, `HIDDEN` Layer를 점검해 `L08_REPRESENTED`를 만든다.

## Assets

- `frame.md` — 공개 가능한 디자인 규칙.
- 공개 장면은 `LG EI` family 이름과 `Malgun Gothic` fallback만 사용한다. 폰트 바이너리와 로컬 위치는 저장소 밖에서 비공개로 관리한다.
- `assets/private/recordings/` — 사용자가 추후 제공할 무음 녹화 경로.
- `assets/private/audio/` — 사용자가 추후 제공할 한국어 나레이션 경로.

## Customizations

- 6개 장면, 660초 고정 타임라인으로 구성한다.
- 녹화 매핑은 `F2 · DEMO-01` A–A 닫힌 경계 HATCH, `F3 · DEMO-02` L07에서 SCALE Reference로 교정한 센서 윤곽의 BLOCK·INSERT, `F4 · DEMO-03` TITLE 주석 GROUP 선택 관계다. 모두 `L07_GEOMETRY_FINAL`에서 `L08_REPRESENTED`를 만들며 표현·Layer·주석 누락의 시험 감점 위험을 확인한다.
- A–A 정본은 X=40 절단면이 통과하는 하단 Ø4 sensorPattern, AF30 포켓, 중앙 Ø20 구멍, 22×8 상부 장공의 네 빈 영역을 모두 비운 Y50×Z8 단면으로 표현한다.
- 실제 사내 도면이나 PPT 이미지는 사용하지 않고 `EDU-SB-01`과 추상 센서 심볼을 인라인 SVG로 작성한다.
- 최종 렌더 전 장면 중간 스냅샷, Whisper 단어 타임코드 동기화, 전체 재생 검증을 수행한다.

## Notes

- AutoCAD 버전별 UI 차이보다 경계, 기준점, 정의와 인스턴스의 관계를 우선 설명한다.
- 시험에서는 3D 모델·치수·지시사항을 제한시간 안에 처리한다. A3 외관선·표제란, 제3각법, 축척, Layer 설정과 지시사항 누락은 감점 위험이며 공식 문제지가 우선한다.
- 녹화 기준은 1920×1080, 30fps, 커서 표시, 무음, 앞뒤 2초 핸들이다.
