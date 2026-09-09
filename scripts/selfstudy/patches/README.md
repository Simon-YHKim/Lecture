# patches — 한 번 돌리고 끝난 스크립트

여기 있는 것은 다시 돌리라고 둔 도구가 아니다. **한 번 돌려서 원본을 고친 기록**이고,
그 안에 이 저장소 어디에도 없는 판단이 들어 있어서 남긴다. 스크립트를 지우면 판단도
같이 사라진다.

전부 원본(`scripts/selfstudy/source/lesson-0N.json`, `projects/.../SCRIPT.md`,
`projects/.../compositions/frames/*.html`)에 이미 반영되어 있다. **다시 돌리지 말 것** —
대부분 「원문이 정확히 한 번 있을 때만 손댄다」로 막혀 있어 두 번째 실행은 그냥 건너뛰지만,
`fix_note_order.py` 처럼 시각을 옮기는 것은 두 번 돌리면 두 번 밀린다.

| 파일 | 여기에만 있는 것 |
|---|---|
| `coach_l67.py` | **좌표계 정본.** 원점은 베이스 왼쪽 아래, x 오른쪽, y 위. `BOSS=(60,62)` · 필렛 중심 `(12.14,26)`·`(107.86,26)`(사이가 참고 치수 95.7) · 탭 오프셋 `15.556`(= 피치원 반지름 22 를 45도로 나눈 값). 7차시 9단계·6차시 4단계의 코치 마크 `(x, y, snap)` 26개 전부 |
| `fix_dim_targets.py` | **어느 치수가 어디를 재는가.** `DIM2HL` 22행 — `w120·h90→profile` `c60·c62·a45→bossc` `h16·c5→basehl` `w80→neck` `f26·f95→filletc` `s8→slotc` `t12·t20→thick` `d25→bore` `d56→boss` `pcd·m5→tap` `r10→fillet` `s29·s50·s12·sr5→slot`. 겹선을 새로 그리지 않고 **이미 그려진 요소를 복제**한다는 설계 판단(좌표를 다시 계산하지 않으므로 형상과 어긋날 수가 없다) |
| `drop_relcoord.py` | **정책 3(좌표 금지)의 실행 규칙.** 자리마다 대체 방법이 다르다 — 한 축이면 직교+거리, 두 축이면 OFFSET 교차점이나 「길이 먼저 만들고 중간점으로 MOVE」, 사각형이면 `REC` 의 `D` 옵션 + `CHAMFER`. 값의 근거도 여기 있다(33 = 반지름 28 + 내미는 5, 40 = 밑동 80 의 절반, 장공 = 밑변 OFFSET 8 ∩ 왼쪽 변 OFFSET 29) |
| `drop_relcoord2.py` | 설명하는 대목의 치환. 3차시 「베이스 여섯 꼭짓점과 모따기 산술」 절이 통째로 옛말이 된 이유 — 새 방법에는 11·115·110 같은 계산값이 아예 없다 |
| `script_relcoord.py` | 녹화 대본 13문단의 before/after 전문 |
| `fix_base_fig.py` | 베이스 외곽 도해 SVG 전문. 사람이 주는 숫자가 넷(120·16·5·5)뿐임을 보이도록 다시 그린 것 |
| `fix_note_order.py` | 「계열에 안 속한 꼬리 요소」를 찾아내는 규칙. 손으로 넣은 시각은 113.00 처럼 딱 떨어지는 숫자로 남는다는 관찰 |
| `tag_kinds.py` | 자습본 조작 한 줄의 `kind` 자동 판별 규칙(우선순위 9단계). 값 8종 — `type` `see` `key` `move` `snap` `click` `alt` `ask`. 렌더러는 `build_selfstudy.py:ACT_KIND`, 스타일은 `assets/base.css` 의 `.act .kind` 계열 |

## 다시 쓸 수 있는 도구는 여기 없다

- 전수 검사 → `scripts/selfstudy/audit/`
- 도면 생성 → `scripts/part/edu_ib_02.py`
- 프레임 시각 재조정 → `scripts/part/retime_frames.py`
- A3·제3각법 도해 → `scripts/selfstudy/sheet_figures.py`
