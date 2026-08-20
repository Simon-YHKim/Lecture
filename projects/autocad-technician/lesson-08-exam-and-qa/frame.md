---
name: "LG technical training — AutoCAD technician"
version: "1.0"
format: "1920x1080"
colors:
  canvas: "#FFFFFF"
  surface: "#F5F5F3"
  ink: "#111111"
  muted: "#666666"
  rule: "#A4A3A4"
  accent: "#C7004C"
typography:
  display_family: "LG EI Headline TTF Semibold"
  body_family: "LG EI Text TTF Regular"
  fallback: "Malgun Gothic, Arial, sans-serif"
spacing:
  frame_safe_x: 96
  frame_safe_y: 72
  grid_unit: 8
components:
  corner_radius: 0
  border_width: 2
  shadow: "none"
motion:
  character: "precise, instructional, restrained"
  default_ease: "power3.out"
  transition_duration: "0.35s"
line_weights:
  outline: 0.50
  center: 0.25
  hidden: 0.25
  dim: 0.25
  tangent: 0.25
  hatch: 0.18
---

# Frame design specification

## Overview

밝은 흰색 교육 화면, LG 마젠타 포인트, 검정과 회색의 명확한 정보 계층, 얇은 구분선이 핵심이다. 한 화면에 한 가지 학습 판단만 남긴다.

## Typography

- 제목과 명령어 표시는 `LG EI Headline TTF Semibold`, 설명과 자막은 `LG EI Text TTF Regular`를 사용한다.
- 공개 HTML에는 파일 URL 없이 `@font-face { src: local("Exact Font Name") }` 선언만 두고 `Malgun Gothic`으로 대체한다. 폰트 바이너리와 private 경로는 추적하지 않는다.
- 1920×1080 기준 제목 56–72px, 본문 22–30px, 캡션 19–24px.

## The frame

- 바탕은 순백색이며 무거운 카드나 그림자를 쓰지 않는다.
- 상단에 2px 회색 규칙선과 현재 절을 나타내는 마젠타 인덱스를 둔다.
- 설명은 화면 왼쪽, 형상과 시연은 오른쪽을 우선 사용한다.
- AutoCAD 녹화 화면은 무조건 축소하지 않는다. 명령줄이 필요한 구간은 하단을 가리지 않는다.

## Drawing rules

- **부품 형상은 손으로 그리지 않는다.** `scripts/part/edu_ib_02.py`가 생성한 인라인 SVG만 사용한다. 프레임 HTML에 좌표를 직접 써 넣으면 `master-part-geometry.json`과 어긋날 수 있다.
- 원호는 SVG `A` 명령의 large-arc·sweep 플래그로 그리지 않는다. 플래그는 중심을 암묵적으로 고르므로 형상이 바뀌면 다른 원을 선택한다. 실제 원에서 각도를 계산한 점열로 그린다. 예외는 정확한 반원뿐이며 그때는 중심이 하나로 정해진다.
- 선 굵기는 위 `line_weights`를 따른다. 외형선 0.50mm, 나머지 0.25mm, 해칭 0.18mm.
- 강조는 `data-feature` 속성 선택으로 한다. 프레임마다 다른 선택자를 만들지 않는다.
- 실제 회사 도면, 로고, `Confidential` 표기, 사내 시스템 정보는 사용하지 않는다.

## Cumulative drawing language

- 모든 차시는 같은 `EDU-IB-02` 부품과 같은 A3 가로 도면 좌표계를 사용한다.
- 장면 상단 메타에는 현재 `checkpoint_in → checkpoint_out`을 표시한다.
- 이전 차시에서 확정된 형상은 검정, 이번 차시에서 추가·수정하는 형상은 마젠타, 아직 배우지 않은 형상은 회색 점선으로 표현한다.
- 한 차시의 마지막 부품 상태와 다음 차시의 첫 부품 상태는 시각적으로 동일해야 한다.
- 시험 관련 장면에는 교육용 기본값보다 해당 회차 문제지와 감독 지시가 우선한다는 고지를 둔다.

## Motion language

- 움직임은 설명을 대신해야 한다. 선은 그려지고, 강조는 특징 단위로 켜진다.
- 장면 전환은 마젠타 규칙선 와이프 또는 직접 컷을 쓴다. 장식적 3D 회전과 글리치는 쓰지 않는다.
- `USER RECORDING` 대체 레이어는 상단 제목·상태 cue 아래에서 시작한다(1920×1080 기준 top 216px 이상).
- 강조 애니메이션은 나레이션 키워드 뒤에 오지 않도록 2–4프레임 먼저 시작한다.

## Audio and captions

- 사용자가 녹음한 한국어 나레이션을 마스터 타임라인으로 사용한다. 프레임의 `duration`은 녹음 전까지 기획값이며, `narration-timing.json`이 생기면 그 값으로 재생성한다.
- AutoCAD 화면 녹화는 원칙적으로 무음으로 받는다.
- 자막은 2줄 이하, 하단 안전 영역 안에 두되 AutoCAD 명령줄과 겹치면 상단으로 옮긴다.

## Private asset boundary

`assets/private/` 아래의 폰트·녹화·음성·전사·렌더 중간물은 로컬 전용이다. 공개 HTML과 코드에는 폰트 패밀리명만 두며 private 경로·URL과 바이너리는 추적하지 않는다.
