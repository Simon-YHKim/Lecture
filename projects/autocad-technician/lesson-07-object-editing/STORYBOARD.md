---
format: 1920x1080
duration: 14m15s
message: "EDU-SB-01의 반복 형상을 수정·검수해 L07_GEOMETRY_FINAL로 넘긴다."
arc: "누적 상태 확인 → 경계 마감 → R5·C5 → 센서 참조 교정 → 형상 게이트 → 시험 고지"
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
mode: collaborative
part_id: EDU-SB-01
checkpoint_in: L06_PATTERNED_FEATURES
checkpoint_out: L07_GEOMETRY_FINAL
paper: A3-landscape
projection: third-angle
---

## Frame 1 — L06 반복 결과에서 계속한다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 10s
- transition_in: cut
- scene: EDU-SB-01의 L06_PATTERNED_FEATURES를 열고 OUTLINE·CENTER·HIDDEN을 유지해 L07_GEOMETRY_FINAL로 넘길 증분을 제시한다.
- voiceover: "새 예제가 아니라 지난 차시의 같은 브래킷을 이어서 형상 마감합니다."
- media: motion-only

A3 가로형·제3각법 상태선을 중심으로 `TRIM/EXTEND → R5/C5 → 센서 참조 SCALE → 검수`를 표시한다. 시험 입력은 3D 모델·치수·지시사항이며 제한시간이 있다는 고지를 함께 둔다.

## Frame 2 — OUTLINE 경계를 정리한다

- status: animated
- src: compositions/frames/02-trim-extend.html
- duration: 195s
- poster: 24s
- transition_in: magenta-rule-wipe
- scene: 닫힌 EDU-SB-01 OUTLINE은 유지하고, 반복 특징 투상 뒤 뷰 외피를 넘은 CONSTRUCTION 선과 짧은 HIDDEN 대응선을 비교한 뒤 DEMO-01로 전환한다.
- voiceover: "OUTLINE은 남길 경계를 먼저 정하고, CENTER와 HIDDEN은 보존합니다."
- media: DEMO-01 trim-extend screen recording

누적 형상 위에 투영 보조선·숨은선 수정 지점만 마젠타로 표시한다. 녹화에서는 TRIM과 EXTEND 뒤 정본 OUTLINE 불변, HIDDEN 범위와 CONSTRUCTION 정리를 검수한다.

## Frame 3 — 어깨 R5와 하단 C5를 완성한다

- status: animated
- src: compositions/frames/03-fillet-chamfer.html
- duration: 195s
- poster: 28s
- transition_in: technical-cut
- scene: 같은 EDU-SB-01의 어깨 FILLET R5와 하단 CHAMFER C5를 비교하고 DEMO-02로 이어진다.
- voiceover: "R5는 둥근 연결, C5는 평평한 절삭면이라는 제작 의도를 남깁니다."
- media: DEMO-02 fillet-chamfer screen recording

OUTLINE 결과를 좌우로 비교하되 CENTER와 HIDDEN이 변하지 않았다는 확인 칩을 함께 보여 준다.

## Frame 4 — 센서 참조 윤곽만 Reference로 교정한다

- status: animated
- src: compositions/frames/04-scale.html
- duration: 180s
- poster: 22s
- transition_in: split-wipe
- scene: 부품 전체 SCALE 금지 경고 뒤 외부 센서 참조 윤곽만 기준점을 고정해 DEMO-03으로 교정한다.
- voiceover: "80×50 부품은 유지하고 센서 참조 윤곽만 SCALE Reference로 맞춥니다."
- media: DEMO-03 scale screen recording

부품 치수는 잠금 표시로 고정하고 선택된 참조 윤곽만 변화시킨다. 적용 후 목표 길이와 고정 기준점을 검증한다.

## Frame 5 — L07 형상 마감 게이트를 통과한다

- status: animated
- src: compositions/frames/05-guided-challenge.html
- duration: 180s
- poster: 18s
- transition_in: cut
- scene: EDU-SB-01의 다섯 수정 지점과 OUTLINE·CENTER·HIDDEN Layer 체크를 20초 실습 후 공개한다.
- voiceover: "경계, R5, C5, 참조 윤곽과 세 Layer를 확인해 L07_GEOMETRY_FINAL로 저장하세요."
- media: motion with optional short answer screen clips

새 형상을 만들지 않고 L06 전후를 겹쳐 비교한다. 형상 게이트가 모두 잠기면 체크포인트가 승급된다.

## Frame 6 — 감점 위험을 기록하고 표현 단계로 넘긴다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 45s
- poster: 16s
- transition_in: magenta-rule-wipe
- scene: L07_GEOMETRY_FINAL을 고정하고 다음 L08_REPRESENTED와 시험 감점 위험을 연결한다.
- voiceover: "제3각법, 축척, 도면틀, Layer와 지시사항 오류는 감점 위험입니다."
- media: motion-only

실제 감점 기준은 공식 문제지를 우선한다는 고지 뒤 `형상 완성 → 표현과 재사용` 상태선을 그린다.
