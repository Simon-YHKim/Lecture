---
name: "LG technical training — AutoCAD technician"
version: "0.3"
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
  display_weight: 600
  body_weight: 400
  emphasis_weight: 600
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
---

# Frame design specification

## Overview

이 과정은 승인된 AutoCAD 교육자료의 시각 언어를 영상 매체에 맞게 재구성한다. 밝은 흰색 교육 화면, LG 마젠타 포인트, 검정과 회색의 명확한 정보 계층, 얇은 구분선이 핵심이다. 원본 슬라이드의 높은 정보 밀도를 복제하지 않고, 한 화면에 한 가지 학습 판단만 남긴다.

## Typography

- 제목과 명령어 표시는 시스템 family `LG EI Headline TTF Semibold`를 사용한다.
- 설명, 단계, 자막은 한글 지원 범위가 넓은 시스템 family `LG EI Text TTF Regular`를 사용한다.
- 보조 강조는 `LG EI Text TTF Regular`에 600 weight를 적용하고 필요 시 로컬 `LG EI Text TTF SemiBold`로 대체한다.
- 공개 HTML에는 파일 URL 없이 `@font-face { src: local("Exact Font Name") }` 선언을 두어 설치된 `LG EI` family를 연결하고, `Malgun Gothic` fallback을 유지한다. private URL이나 폰트 파일 경로는 기록하지 않는다.
- 폰트 바이너리와 절대·상대 private 경로는 공개 저장소에 포함하지 않는다. 로컬 폰트가 없을 때는 `Malgun Gothic`으로 대체한다.
- 1920×1080 기준 제목 88–112px, 장면 제목 56–72px, 본문 34–44px, 캡션 30–36px를 기준으로 한다.

## The frame

- 기본 바탕은 순백색이며 전체 프레임에 무거운 카드나 그림자를 깔지 않는다.
- 상단에는 2px 회색 규칙선과 현재 절을 나타내는 마젠타 인덱스를 둔다.
- 학습 포인트는 화면 왼쪽 40%, 시연 또는 형상은 오른쪽 60%를 우선 사용한다.
- AutoCAD 녹화 화면은 전체 화면을 무조건 축소하지 않는다. 필요한 조작 영역을 읽을 수 있는 크기로 자르고, 명령줄이 필요한 구간은 하단을 가리지 않는다.
- 화면 녹화 위 강조는 마젠타 2px 윤곽선, 짧은 라벨, 포인터 링만 허용한다.

## Composition rules

- 한 장면에는 핵심 문장 하나와 보조 근거 최대 세 개만 동시에 노출한다.
- 명령어는 영문 대문자와 한글 의미를 한 쌍으로 표시한다. 예: `TRIM · 잘라내기`.
- 명령 선택과 결과를 비교할 때는 같은 크기의 좌우 분할을 사용한다.
- 실제 회사 도면, 로고, `Confidential` 표기, 사내 시스템 정보는 사용하지 않는다.
- 연습 형상은 공개 가능한 단일 합성 부품 `EDU-IB-02`로 제작하며, `master-part-geometry.json`의 좌표·크기·개수를 정본으로 사용한다.
- 원본 자료의 주석용 빨강·노랑·파랑은 기본 팔레트로 승격하지 않는다.

## Cumulative drawing language

- 모든 차시는 같은 `EDU-IB-02` 부품과 같은 A3 가로 도면 좌표계를 사용한다.
- 장면 상단 메타에는 현재 `checkpoint_in → checkpoint_out`을 표시한다.
- 이전 차시에서 확정된 형상은 검정, 이번 차시에서 추가·수정하는 형상은 마젠타, 아직 배우지 않은 형상은 회색 점선으로 표현한다.
- 한 차시의 마지막 부품 상태와 다음 차시의 첫 부품 상태는 시각적으로 동일해야 한다.
- 아직 배우지 않은 특징은 숨길 수 있지만 이미 완성한 특징의 위치·크기·개수는 바꾸지 않는다. 탭은 PCD Ø44의 4×M5, 시작각 45°, 깊이 10을 유지하고, 장착 장공은 중심 (35, 8)·(85, 8)에 폭 10·끝원 R5·끝원 중심거리 12를 유지한다. 이 값들은 `master-part-geometry.json`의 `features.taps`·`features.slots`에서 온다.
- A3 도면틀을 보여 줄 때는 420×297 비율, 사방 10mm 교육용 외관선, 우측 하단 200×30 표제란을 유지한다.
- `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`은 단순 라벨이 아니라 각 선의 실제 기능과 함께 보여 준다.
- 시험 관련 장면에는 교육용 템플릿·Layer 값보다 해당 회차 문제지와 감독 지시가 우선한다는 고지를 둔다.
- 감점 위험은 공포 문구가 아니라 `지시 확인 → 오류 발견 → 수정 → 재검수`의 작업 게이트로 표현한다.

## Motion language

- 움직임은 설명을 대신해야 한다. 선은 그려지고, 불필요한 선은 잘려 나가며, 경계는 목표점에 정확히 맞물린다.
- 명령어 카드는 아래에서 짧게 들어와 `SNAP`되고, 0.6초 이상 읽을 수 있게 정지한다.
- 장면 전환은 마젠타 규칙선 와이프 또는 직접 컷을 사용한다. 장식적 3D 회전과 글리치는 사용하지 않는다.
- 화면 녹화 중에는 카메라 이동을 최소화하고, 필요한 경우 한 번의 좌표 기반 줌으로 명령줄 또는 형상만 확대한다.
- `USER RECORDING` 대체 레이어는 상단 수업 제목·상태 cue 아래에서 시작한다(1920×1080 기준 top 216px 이상). 가림 허용 속성으로 제목 충돌을 우회하지 않는다.
- 강조 애니메이션은 나레이션 키워드 뒤에 오지 않도록 2–4프레임 먼저 시작한다.

## Audio and captions

- 사용자가 녹음한 한국어 나레이션을 마스터 타임라인으로 사용한다.
- AutoCAD 화면 녹화는 원칙적으로 무음으로 받고, 클릭 효과음은 필요한 위치에만 별도 추가한다.
- 자막은 2줄 이하, 화면 하단 안전 영역 안에 배치하되 AutoCAD 명령줄과 겹칠 때는 상단으로 이동한다.
- 배경음악은 선택 사항이며, 사용한다면 기술교육 집중을 방해하지 않는 낮은 음량의 미니멀 리듬만 허용한다.

## Private asset boundary

`assets/private/` 아래의 폰트·녹화·음성·전사·렌더 중간물은 로컬 전용이다. 공개 가능한 HTML과 코드에는 폰트 패밀리명만 두며 private 경로·URL과 바이너리는 추적하지 않는다.
