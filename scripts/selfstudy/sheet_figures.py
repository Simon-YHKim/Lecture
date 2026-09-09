# -*- coding: utf-8 -*-
"""자습본 도해 둘 — A3 도면틀과 제3각법 비교.

핸드오프에 「2차시는 A3 용지 도해가, 5차시는 3뷰 도해가 없어서 막혀 있다」고
적었는데 사실이 아니었다. 둘 다 이미 그려져 있었고 휘발성 작업 폴더에만
있었을 뿐이다. 여기로 옮긴다.

막힌 진짜 이유는 **슬라이드로 옮기는 경로**다. 자습본 도해는 선 종류를 짧은
이름(`si` `sh` `sd` `sc` `sn` `sl`)으로 구분하는데, 슬라이드에서 `sc` 는 점검
카드다. 그래서 도해를 슬라이드에 실을 때는 반드시 `.cfw` 안으로 가둬야 한다 —
`build_deck_selfstudy.py` 의 `.ss .cfw .si{...}` 계열이 그 처리다.

좌표는 A3 실치수(420×297)를 그린 것이 아니라 도해용으로 줄인 값이다.
라벨은 좌표가 아니라 **그 자리를 어떻게 잡는지**를 적는다 — 정책 1번대로
용지선 두 구석만 좌표이고 나머지는 스냅이다.
용지선 rect(30,30,462,327) · 도면선 rect(41,41,440,305) · 표제란(261,313,220,33).
"""

SVG_A3 = (
 '<svg viewBox="0 0 560 400" width="560" height="400">'
 '<rect class="si" x="30" y="30" width="462" height="327"/>'
 '<rect class="si" x="41" y="41" width="440" height="305"/>'
 '<path class="si" d="M261 357 L261 346 M261 41 L261 30 M30 194 L41 194 M481 194 L492 194"/>'
 '<rect class="sh" x="261" y="313" width="220" height="33"/>'
 '<path class="sh" d="M371 313 L371 346"/>'
 '<path class="sd" d="M30 62 L41 62"/>'
 '<text class="sl" x="47" y="66">10</text>'
 '<text class="sl" x="30" y="372" text-anchor="middle">0,0</text>'
 '<text class="sl" x="486" y="24" text-anchor="middle">420,297</text>'
 '<text class="slh" x="48" y="336">끝점 스냅</text>'
 '<text class="slh" x="474" y="58" text-anchor="end">OFFSET 10</text>'
 '<text class="slh" x="256" y="370" text-anchor="end">중간점 스냅</text>'
 '<text class="slh" x="476" y="308" text-anchor="end">끝점에서 시작</text>'
 '<text class="slh" x="371" y="308" text-anchor="middle">310</text>'
 '<text class="sl" x="316" y="308" text-anchor="middle">200 × 30</text>'
 '<text class="sl" x="46" y="190">148.5</text>'
 '<text class="sl" x="46" y="208">중심 마크</text>'
 '<text class="slh" x="277" y="329">중간-센터</text>'
 '<text class="sl" x="277" y="343">이름</text>'
 '<text class="slh" x="387" y="329">중간-센터</text>'
 '<text class="sl" x="387" y="343">사번</text>'
 '<text class="sl" x="261" y="390" text-anchor="middle">A3 420 × 297 · 문자 높이 10</text>'
 # 강조 겹선 — 코치 마크가 「지금 그리는 것」을 켤 때 쓴다. 평소에는 stroke:none 이라 보이지 않는다.
 '<rect class="hl" data-feature="sh-paper" x="30" y="30" width="462" height="327"/>'
 '<rect class="hl" data-feature="sh-frame" x="41" y="41" width="440" height="305"/>'
 '<path class="hl" data-feature="sh-mark" d="M261 357 L261 346 M261 41 L261 30 M30 194 L41 194 M481 194 L492 194"/>'
 '<rect class="hl" data-feature="sh-title" x="261" y="313" width="220" height="33"/>'
 '</svg>')

SVG_THIRD = (
 '<svg viewBox="0 0 600 196" width="600" height="196">'
 '<text class="slh" x="8" y="15">제3각법</text>'
 '<text class="sl" x="308" y="15">제1각법</text>'
 '<line class="sd" x1="298" y1="4" x2="298" y2="192"/>'
 '<circle class="si" cx="72" cy="92" r="34"/>'
 '<circle class="si" cx="72" cy="92" r="18"/>'
 '<line class="sc" x1="26" y1="92" x2="118" y2="92"/>'
 '<line class="sc" x1="72" y1="46" x2="72" y2="138"/>'
 '<polygon class="sh" points="152,74 234,58 234,126 152,110"/>'
 '<line class="sc" x1="142" y1="92" x2="244" y2="92"/>'
 '<text class="sl" x="132" y="150" text-anchor="middle">작은 끝</text>'
 '<text class="sl" x="252" y="150" text-anchor="middle">큰 끝</text>'
 '<text class="slh" x="8" y="172">작은 끝이 원을 향합니다</text>'
 '<text class="sl" x="8" y="188">평면도는 위 · 우측면도는 오른쪽</text>'
 '<circle class="si" cx="372" cy="92" r="34"/>'
 '<circle class="si" cx="372" cy="92" r="18"/>'
 '<line class="sc" x1="326" y1="92" x2="418" y2="92"/>'
 '<line class="sc" x1="372" y1="46" x2="372" y2="138"/>'
 '<polygon class="si" points="452,58 534,74 534,110 452,126"/>'
 '<line class="sc" x1="442" y1="92" x2="544" y2="92"/>'
 '<text class="sl" x="432" y="150" text-anchor="middle">큰 끝</text>'
 '<text class="sl" x="552" y="150" text-anchor="middle">작은 끝</text>'
 '<text class="sl" x="308" y="172">큰 끝이 원을 향합니다</text>'
 '<text class="sl" x="308" y="188">평면도는 아래 · 우측면도는 왼쪽</text>'
 '</svg>')
