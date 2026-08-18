---
workflow: general-video
flow: automation
storyboard: no
message: "TRIM, EXTEND, FILLET, CHAMFER, SCALE을 목적에 맞게 선택하면 복잡한 형상도 빠르고 정확하게 완성할 수 있다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
length: 14m15s
angle: guided-practice
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L06_PATTERNED_FEATURES
checkpoint_out: L07_GEOMETRY_FINAL
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 7차시는 새 예제를 시작하지 않는다. `EDU-SB-01`의 `L06_PATTERNED_FEATURES`를 열어 이미 닫힌 `OUTLINE`은 유지하고, 반복 특징 투상 뒤 남은 `CONSTRUCTION` 선과 짧은 `HIDDEN` 대응선을 TRIM·EXTEND로 정리한다. 이어 FILLET R5·CHAMFER C5로 최종 모서리를 만들고, 부품 전체가 아닌 센서 참조 윤곽만 SCALE Reference로 교정해 `L07_GEOMETRY_FINAL`을 만든다. A3 가로형 도면과 제3각법 배치를 그대로 이어 간다.

## Assets

- 비공개 원본 PPT 묶음 — 교육 범위와 시각 방향을 파악하는 참고 자료이며 Git에 올리지 않는다.
- `frame.md` — PPT에서 추출한 공개 가능한 색·서체·레이아웃 규칙.
- 공개 장면은 `LG EI` family 이름과 `Malgun Gothic` fallback만 사용한다. 폰트 바이너리와 로컬 위치는 저장소 밖에서 비공개로 관리한다.
- `assets/private/recordings/` — 사용자가 추후 전달할 무음 AutoCAD 화면 녹화 위치.
- `assets/private/audio/` — 사용자가 추후 전달할 최종 한국어 나레이션 위치.

## Customizations

- 6개 장면 안에서 `L06_PATTERNED_FEATURES → L07_GEOMETRY_FINAL` 누적 변화와 세 개의 화면 녹화 구간을 교차한다.
- 첫 장면은 결과 샘플을 미리 보여 주는 유튜브형 훅이 아니라, 과정 제목·Technician에게 CAD가 필요한 이유·강의 진행 방식·이번 차시 목차를 안내하는 정규 강의 OT로 구성한다.
- 녹화 매핑은 `F2 · DEMO-01` 뷰 밖 CONSTRUCTION 투영선 TRIM·짧은 HIDDEN 대응선 EXTEND와 정본 OUTLINE 보존, `F3 · DEMO-02` FILLET R5·CHAMFER C5, `F4 · DEMO-03` 센서 참조 윤곽만 SCALE Reference다. 모두 `L06_PATTERNED_FEATURES`에서 `L07_GEOMETRY_FINAL`을 만들며 경계·모서리·축척 혼동의 시험 감점 위험을 확인한다.
- 나레이션이 확정되면 Whisper 계열 전사로 단어 타임코드를 만들고 모션과 자막을 다시 맞춘다.
- 최종 렌더 전에는 장면 중간 시점 스냅샷, 음성 키워드 싱크, 전체 재생의 세 단계 검증을 수행한다.

## Notes

- 실습 형상은 공개 가능한 합성 부품 `EDU-SB-01 교육용 센서 장착 브래킷` 하나만 사용한다.
- 시험에서는 3D 모델·치수·지시사항을 제한시간 안에 해독하고 완성해야 한다. A3 도면틀, 제3각법, 축척, Layer 이름·색상·선종류·선가중치와 지시사항 불이행은 감점 위험이며 공식 문제지가 우선한다.
- 로고, 사내 표기, `Confidential`, 개인 정보, 라이선스 정보는 화면에 포함하지 않는다.
- AutoCAD 버전에 따라 명령 프롬프트가 달라질 수 있으므로 대본은 특정 버전 UI보다 명령 목적과 판단 기준을 우선한다.
- 사용자가 녹화할 때는 1920×1080, 30fps, 커서 표시, 앞뒤 2초 여유를 기본으로 한다.
