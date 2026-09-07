# AutoCAD Technician 자습본

강사 없이 혼자 학습하는 판이다. 여덟 차시 영상 과정(19편·264분)의 대본을 근거로
국문과 영문을 한 파일에 담고, 버튼 하나로 언어를 바꾼다.

`index.html` 부터 연다.

## 영상판과 무엇이 다른가

영상은 셋에 기대고 있었다. 내레이터의 목소리, 순서대로 등장하는 화면 모션,
실시간 화면 녹화. 자습본에는 셋 다 없다. 그 자리를 이렇게 메웠다.

| 사라진 것 | 자습본이 놓은 것 |
| --- | --- |
| 내레이터의 억양·강조·되묻기 | 짧은 문장, 이유 블록, 되묻는 문장 |
| 순차 등장하는 화면 모션 | 카드 · 표 · 인라인 SVG 도해 |
| 실시간 화면 녹화 | 단계별 절차 — 입력값 · 기대 결과 · **안 되면 여기** |
| 강사가 쥐던 진도 | 단계 체크박스와 진도 막대 (브라우저에만 저장) |
| 강사가 봐 주던 검산 | 값으로 판정하는 검산 표와 자가 점검 문답 |

## 파일

| 파일 | 내용 |
| --- | --- |
| `index.html` | 과정 요약 · 차시 목록과 진도 · 아직 정해지지 않은 것 |
| `reference.html` | 국영 용어 대조 50개 · 과정에서 치는 명령 65개 |
| `lesson-01.html` … `lesson-08.html` | 차시별 본문. 1부는 요약과 개념 |
| `lesson-0N-2.html`, `-3.html` | 같은 차시의 2·3부. 실습과 점검 |
| `bilingual-review.html` | **영문 감수용.** 국영 쌍 3,906개를 기계로 훑어 볼 곳만 추린 워크리스트 |

한 파일이 100 KB 를 넘지 않게 차시를 나눴다. 나뉜 차시라도 진도 체크와 메모는
`data-progress-key` 로 묶여 **한 차시로 합산된다.**

각 파일은 자체완결이다. 외부 스크립트·스타일·이미지·폰트를 하나도 참조하지 않는다.
도면은 파일이 아니라 HTML 안의 인라인 SVG다.

## 보는 방법

내려받아 브라우저로 연다. 미리보기 창(샌드박스)에서는 `localStorage` 가 막혀
메모와 진도가 저장되지 않을 수 있다. 저장이 막히면 메모리 폴백으로 넘어가고
본문은 그대로 읽힌다.

- **국문 / EN** — 두 언어가 같은 파일에 있다. 인쇄하면 그때 선택된 언어만 나온다.
- **자동 / 밝게 / 어둡게** — 기본은 운영체제 설정을 따른다.
- **메모** — 본문을 드래그하면 「메모」 버튼이 뜬다. 인용과 위치가 고정되고,
  「메모 → 프롬프트 복사」로 전부 모아 복사한다.

## 다시 만들기

본문은 손으로 고치지 않는다. `scripts/selfstudy/source/` 의 JSON 을 고치고 다시 뽑는다.

```powershell
$env:SELFSTUDY_SRC = "$PWD\scripts\selfstudy\source"
$env:BUILD_STAMP   = (Get-Date -Format 'yyyy-MM-dd HH:mm') + ' KST'
python scripts/selfstudy/build_selfstudy.py docs/autocad-technician/self-study
```

도면은 커밋하지 않는다. 빌드할 때마다 `scripts/part/edu_ib_02.py` 가
`master-part-geometry.json` 과 같은 정의에서 다시 그린다. 그래서 도면과 본문이
서로 다른 말을 할 수 없다. 저장소 가드가 이미지 파일을 확장자로 막는 것과도 맞는다.

## 영문 감수

```powershell
python scripts/selfstudy/bilingual_review.py
```

두 가지가 나온다. `bilingual-review.html` 은 볼 곳만 추린 워크리스트이고,
`bilingual-review.csv` 는 국영 쌍 3,906개 전부다. 감수자는 CSV 를 엑셀에서 열고
마지막 「검토 의견」 칸에 고칠 영문을 적어 돌려준다. UTF-8 BOM 이라 한글 윈도우
엑셀에서 바로 열린다.

CSV 는 약 900 KB 이고 원본 JSON 에서 언제든 다시 나오므로 커밋하지 않는다
(`.gitignore`).

## 검사

```powershell
python scripts/selfstudy/validate_content.py     # 구조 · 국영 대응 · 명령 대조 · 용량
python scripts/selfstudy/tone_check.py scripts/selfstudy/source/lesson-0*.json
```

`validate_content.py` 는 **타이핑하는 값이 원본 `SCRIPT.md` 의 백틱 안에 실제로
있었는지**까지 대조한다. 명령을 지어내면 여기서 걸린다.

`tone_check.py` 는 국문 종결어미를 세어 합쇼체와 해요체의 비율을 판정한다.
요청 사양은 합쇼체 70~80% · 해요체 20~30% 이고, 문어체(`~한다`)가 하나라도
있으면 실패한다. 집필 규칙 전문은 `scripts/selfstudy/WRITER_CONTRACT.md` 에 있다.

## 무엇을 근거로 삼았나

- 본문 — `projects/autocad-technician/lesson-*/SCRIPT.md` 와 `BRIEF.md`
- 치수·레이어·용지 — `projects/autocad-technician/MASTER_DRAWING_SPEC.md`
- 도면 좌표 — `projects/autocad-technician/master-part-geometry.json`
- 차시 연결 — `projects/autocad-technician/course-continuity.json`

## 비워 둔 것

채점 기준, 배점, 제한시간, 합격선, 시험 일시·장소·제출 형식은 공유받지 못했다.
그럴듯한 값을 지어내면 학습자가 그것을 믿고 준비한다. 그래서 점선 자리에
「공유 예정」으로 두었다. 미확정 항목 전부는 `index.html` 의 **미결** 탭에 있다.

AutoCAD 버전과 언어도 확정되지 않았다. 대화상자가 실제로 띄우는 문구를 짓지 않고
「무엇을 묻고 무엇을 고르는가」로만 적었다. 버전에 따라 갈리는 대목은 두 경우를 다 적었다.

## 공개 경계

이 저장소의 규칙을 그대로 따른다. 원본 발표자료, 실제 도면, 녹화, 나레이션,
전사, 폰트 바이너리는 들어 있지 않다. 도해는 공개 가능한 합성 부품 `EDU-IB-02`
하나로만 만들었고, 검토된 HTML 안의 인라인 SVG 로만 그렸다.
