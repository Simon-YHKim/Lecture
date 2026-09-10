"""영문 대응이 실제로 영문인지, 용어가 정본과 맞는지 센다.

`curriculum.json` 의 `terminologyRules` 는 산문이라 사람만 읽는다. 이 검사기는
그 규칙 가운데 기계가 판정할 수 있는 것만 규칙으로 옮겨, 학습자에게 나가는
`en` 문자열을 전수로 본다.

    한글 잔존   `en` 안에 한글이 남아 있다 — 번역이 안 된 자리다.
    용어 흔들림 외형선을 outline layer 로, 장공을 oblong hole 로 부르는 자리다.
    짝 없음     한글이 든 `ko` 인데 `en` 이 비어 있다.

    python scripts/selfstudy/check_english.py                 전체
    python scripts/selfstudy/check_english.py lesson-05.json  한 파일

종료코드 1 이면 위반이다. 명령 이름·치수·파일명처럼 두 언어가 같아야 하는
문자열은 위반이 아니다 — 한글이 없으면 통과한다. 규칙은 이름을 겨냥한다.
`the base outline` 처럼 모양을 가리키는 보통명사는 잡지 않는다.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.environ.get('SELFSTUDY_SRC') or os.path.join(HERE, 'source')
HANGUL = re.compile(r'[가-힣]')

# (정규식, 무엇이 맞는가) — terminologyRules 에서 기계 판정이 가능한 것만 옮겼다.
BANNED = [
    (re.compile(r'\boutline\s+(?:layer|linetype|lines?\b)', re.I),
     '외형선은 visible line 이다 (최초 1회 object line 병기만 허용)'),
    (re.compile(r'\b(?:layer|linetype)\s+outline\b', re.I), '외형선은 visible line 이다'),
    (re.compile(r'\bsolid\s+line\s+layer\b', re.I), '외형선은 visible line 이다'),
    (re.compile(r'\bcenter line\b', re.I), 'centerline 은 한 단어다'),
    (re.compile(r'\bline\s+weight\b', re.I), 'lineweight 는 한 단어다'),
    (re.compile(r'\bline\s+type\b', re.I), 'linetype 은 한 단어다'),
    (re.compile(r'\boblong hole\b|\belongated hole\b', re.I), '장공은 slot 이다'),
    (re.compile(r'\belevation\b|\bplan view\b', re.I), '뷰 이름은 front / top / right side view 다'),
    (re.compile(r'\bdia\.?\s*\d', re.I), '지름은 Ø 기호를 그대로 쓴다'),
    (re.compile(r'\d[\d.]*\s*(?:in\.|inch\b|inches\b)'), '인치 환산을 병기하지 않는다'),
    (re.compile(r'\b(?:third|first) angle\b', re.I), 'third-angle · first-angle 은 하이픈이 필요하다'),
    (re.compile(r'R10[^.]{0,40}\bround\b|\bround\b[^.]{0,40}R10', re.I),
     'R10 은 안쪽 모서리라 round 로 쓰지 않는다'),
]


# 도면에 새겨진 표기를 그대로 인용하는 자리다. 도면 생성기가 한국어로 그리므로
# 영문 도면(`edu_ib_02.py --lang en`)이 나오기 전에는 여기를 고칠 수 없다.
# 도면이 영문이 되면 이 목록을 지우고 문장을 그 표기에 맞춘다.
PENDING = {
    ('lesson-05.json', '/sections/9/blocks/1/items/2/spots/3/hover'),
    ('lesson-07.json', '/sections/3/blocks/0/rows/3/3'),
    ('lesson-07.json', '/sections/5/blocks/0/alt'),
    ('lesson-07.json', '/sections/5/blocks/1/rows/13/1'),
    ('lesson-07.json', '/sections/6/blocks/1/items/1/label'),
    ('lesson-07.json', '/sections/6/blocks/3/rows/1/0'),
    ('lesson-07.json', '/sections/6/blocks/3/rows/3/0'),
    ('lesson-07.json', '/sections/8/blocks/1/items/3/title'),
    ('lesson-07.json', '/sections/8/blocks/1/items/3/actions/5/do'),
    ('lesson-07.json', '/sections/8/blocks/1/items/3/expect'),
    ('lesson-07.json', '/sections/9/blocks/1/items/1/title'),
    ('lesson-07.json', '/sections/9/blocks/1/items/1/expect'),
    ('lesson-07.json', '/recap/did/7'),
    ('lesson-07.json', '/recap/did/10'),
}


def pairs(node, path, found):
    """ko/en 짝을 전부 모은다. 경로는 사람이 파일에서 찾아갈 수 있게 남긴다."""
    if isinstance(node, dict):
        if isinstance(node.get('ko'), str):
            found.append((path, node['ko'], node.get('en')))
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                pairs(value, path + '/' + str(key), found)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            pairs(value, path + '/' + str(index), found)


def violations(name, where, ko, en):
    if not isinstance(en, str) or not en.strip():
        return [(name, where, '짝 없음', ko)] if HANGUL.search(ko) else []
    found = []
    if HANGUL.search(en):
        found.append((name, where, '한글 잔존', en))
    for pattern, correct in BANNED:
        if pattern.search(en):
            found.append((name, where, correct, en))
    return found


def check(files):
    found = []
    for name in files:
        with open(os.path.join(SOURCE, name), encoding='utf-8') as handle:
            data = json.load(handle)
        rows = []
        pairs(data, '', rows)
        for where, ko, en in rows:
            found.extend(violations(name, where, ko, en))
    return found


def main(argv):
    files = argv[1:] or sorted(f for f in os.listdir(SOURCE) if f.endswith('.json'))
    found = check(files)
    pending = [row for row in found if (row[0], row[1]) in PENDING]
    open_rows = [row for row in found if (row[0], row[1]) not in PENDING]
    for name, where, why, text in open_rows:
        print('%-16s %-52s %s' % (name, where[-52:], why))
        print('%-16s %s' % ('', text.strip()[:110]))
    if open_rows:
        print()
        print('영문 검사 실패 — %d 건.' % len(open_rows))
        return 1
    print('영문 검사 통과 — 파일 %d 개에 한글 잔존 0 · 용어 흔들림 0.' % len(files))
    if pending:
        print('보류 %d 건 — 영문 도면이 나오면 함께 고친다 (PENDING).' % len(pending))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
