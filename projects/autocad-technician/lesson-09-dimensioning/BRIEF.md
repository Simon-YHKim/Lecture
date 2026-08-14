---
workflow: general-video
flow: automation
storyboard: no
message: "치수는 값을 장식하는 표기가 아니라 제작과 검사를 가능하게 하는 설계 의도다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
length: 14m
angle: guided-practice
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L08_REPRESENTED
checkpoint_out: L09_RELEASE_CANDIDATE
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 9차시는 `EDU-SB-01`의 `L08_REPRESENTED`에서 이어진다. 같은 브래킷의 `DIM`, `OUTLINE`, `CENTER` Layer를 기준으로 제작 가능한 최소 치수 세트인 80×50×8, Ø20 중심 (40,22), 같은 중심의 AF30·깊이 4, 22×8 장공 중심 (40,42), 2×Ø6 위치, 3×Ø4·PCD Ø36·시작각 30°, R15·R5·C5, 14×14 국부 포켓 위치·깊이 2를 배치한다. Model 1:1과 A3 가로형 제3각법 뷰 축척·표기까지 검수해 `L09_RELEASE_CANDIDATE`를 만든다.

## Assets

- `frame.md` — 공개 가능한 디자인 규칙.
- 공개 장면은 `LG EI` family 이름과 `Malgun Gothic` fallback만 사용한다. 폰트 바이너리와 로컬 위치는 저장소 밖에서 비공개로 관리한다.
- `assets/private/recordings/` — 사용자 무음 화면 녹화 경로.
- `assets/private/audio/` — 사용자 한국어 나레이션 경로.

## Customizations

- 6개 장면, 840초 고정 타임라인이다.
- 녹화 매핑은 `F2 · DEMO-01` DIMSTYLE·DIM Layer·Model 1:1, `F3 · DEMO-02` DIMLINEAR·DIMALIGNED·DIMANGULAR, `F4 · DEMO-03` DIMRADIUS·DIMDIAMETER·수량 표기 검수다. 모두 `L08_REPRESENTED`에서 `L09_RELEASE_CANDIDATE`를 만들며 치수 누락·중복·Layer 오용의 시험 감점 위험을 확인한다.
- Frame 5의 번호형 callout은 `① 외피·Datum`, `② 중앙 특징`, `③ 구멍 패턴`, `④ 장공·윤곽`, `⑤ 국부 포켓`으로 묶어 치수 누락을 감사한다. 같은 정보를 여러 뷰에 반복하지 않고 필요한 기준 위치치수만 남긴다.
- 치수는 새로운 일회성 예제가 아니라 누적 부품 `EDU-SB-01`에만 적용하며 회사 도면을 복제하지 않는다.
- 최종 렌더는 실제 녹화·나레이션 삽입과 Whisper 동기화, Studio 승인 뒤 수행한다.

## Notes

- 특정 AutoCAD 버전 UI보다 치수 기준, 형상 방향, 중복 방지 원칙을 우선한다.
- 시험 입력은 3D 모델·치수·지시사항이며 제한시간이 있다. 제3각법, 축척, A3 외관선·표제란, Layer 이름·색상·선종류·선가중치, 치수 누락·중복·수동 덮어쓰기는 감점 위험이다.
- 녹화 기준은 1920×1080, 30fps, 커서 표시, 무음, 앞뒤 2초 핸들이다.
