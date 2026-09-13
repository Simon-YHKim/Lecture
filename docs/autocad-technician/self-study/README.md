# AutoCAD Technician 자습본

강사 없이 혼자 학습하는 국문·영문 검수판이다. 언어별 여덟 차시의 최신 대본을
근거로 두 언어를 한 파일에 담고, 버튼 하나로 언어를 바꾼다.
현재 검수 영상은 국문 약 212분, 영문 약 253분이며 2~7차시에는 실습 녹화 전
PREVIEW가 포함된다. 언어별 실측 길이는 원본 JSON의 `videoLengthByLang`에 둔다.

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

분권 HTML 한 파일이 100 KB를 넘지 않게 실제 도해·문서 틀을 포함해 나눈다.
120 KB보다 큰 원본 JSON은 생성된 각 페이지의 100 KB 제한을 검사한다.
내용을 자르거나 제한을 올리지 않는다. 나뉜 차시라도 진도 체크와 메모는
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

## 한 장으로 묶어 건네려면

```powershell
python scripts/selfstudy/build_single.py
```

여덟 차시를 파일 하나로 다시 엮는다. 차시 사이 이동이 링크가 아니라 탭이고,
진도 막대가 과정 전체로 하나이며, 용어·명령·미결이 같은 파일에 들어온다.
본문은 쪽 판과 같은 원본에서 나오므로 둘이 어긋날 수 없다.

약 1.1 MB 라 커밋하지 않는다(`.gitignore`). 사람에게 주소 하나로 건네야 할 때만 뽑는다.
`SELFSTUDY_ARTIFACT=1` 을 주면 문서 껍데기를 뺀 형태로 나온다.

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

`validate_content.py`는 기본으로 저장소의 `source/` 8개를 검사하며 대상이 없으면
실패한다. **타이핑 값과 단축키가 원본 `SCRIPT.md`의 백틱 안에 있는지**도 대조한다.
백틱 밖의 설명이나 공통 단축키는 경고로 남으므로, 이 검사만으로 실제 AutoCAD
조작이 검증됐다고 해석하지 않는다.

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

대상은 AutoCAD 2024다. 실제 응용프로그램에서의 절차 검수와 실습 녹화는 남아 있다.
국문·영문 설명과 별개로 설치된 UI 언어에 따라 대화상자 문구를 확인해야 한다.

## 공개 경계

이 저장소의 규칙을 그대로 따른다. 원본 발표자료, 실제 도면, 녹화, 나레이션,
전사, 폰트 바이너리는 들어 있지 않다. 도해는 공개 가능한 합성 부품 `EDU-IB-02`
하나로만 만들었고, 검토된 HTML 안의 인라인 SVG 로만 그렸다.
