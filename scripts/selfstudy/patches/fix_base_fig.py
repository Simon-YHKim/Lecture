# -*- coding: utf-8 -*-
"""베이스 외곽 그림에서 좌표 딱지를 뗀다.

꼭짓점마다 `@120,0` 같은 입력값을 붙여 두었는데, 이제 그렇게 그리지 않는다.
새 방법에서 사람이 주는 숫자는 넷뿐이다 — 120, 16, 그리고 모따기 5, 5.
그림에도 그 넷만 남긴다. 꼭짓점 번호는 「여섯 개다」를 보여 주는 것이라 둔다.
"""
import io
import json
import os
# 저장소 뿌리에서 상대로 잡는다 — 남의 컴퓨터에서도 돌아가야 한다.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


P = os.path.join(os.path.join(REPO, 'scripts', 'selfstudy', 'source'), 'lesson-03.json')

SVG = (
 '<svg viewBox="0 0 600 200" width="600" height="200">'
 '<polygon class="si" points="45,140 525,140 525,96 505,76 65,76 45,96" fill="none"/>'
 # 모따기 전 사각형 — 먼저 그리는 것이 이것이라는 뜻으로 옅게 둔다.
 '<path class="sn" d="M45 96 L45 76 L65 76 M505 76 L525 76 L525 96" fill="none"/>'
 '<circle class="sh" cx="45" cy="140" r="4" fill="none"/>'
 '<circle class="sh" cx="525" cy="140" r="4" fill="none"/>'
 '<circle class="sh" cx="525" cy="96" r="4" fill="none"/>'
 '<circle class="sh" cx="505" cy="76" r="4" fill="none"/>'
 '<circle class="sh" cx="65" cy="76" r="4" fill="none"/>'
 '<circle class="sh" cx="45" cy="96" r="4" fill="none"/>'
 '<text class="slh" x="36" y="156">1</text>'
 '<text class="slh" x="530" y="156">2</text>'
 '<text class="slh" x="536" y="100">3</text>'
 '<text class="slh" x="503" y="66">4</text>'
 '<text class="slh" x="62" y="66">5</text>'
 '<text class="slh" x="30" y="100">6</text>'
 '<text class="sl" x="285" y="158" text-anchor="middle">120</text>'
 '<text class="sl" x="285" y="182" text-anchor="middle">REC 의 가로</text>'
 '<path class="sd" d="M33 76 L33 140" fill="none"/>'
 '<text class="sl" x="6" y="106">16</text>'
 '<text class="sl" x="6" y="122">세로</text>'
 '<text class="sl" x="540" y="86">5</text>'
 '<text class="sl" x="540" y="70">×5</text>'
 '<text class="sl" x="40" y="66">5×5</text>'
 '<text class="sl" x="285" y="40" text-anchor="middle">2-C5 — CHAMFER 로 나중에</text>'
 '</svg>')


def main():
    d = json.load(io.open(P, encoding='utf-8'))
    b = d['sections'][4]['blocks'][3]
    assert '@120,0' in b['svg'], '이미 바꾼 것 같다'
    b['svg'] = SVG
    b['caption'] = {'ko': '사람이 주는 숫자는 넷뿐입니다 — 120, 16, 그리고 모따기 5와 5.',
                    'en': 'You give four numbers: 120, 16, and the chamfer 5 and 5.'}
    io.open(P, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(d, ensure_ascii=False, indent=1))
    print('베이스 외곽 그림을 다시 그렸다')


main()
