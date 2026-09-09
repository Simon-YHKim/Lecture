# -*- coding: utf-8 -*-
"""조작 한 줄이 어떤 종류인지 표시한다.

3차시는 손으로 달아 두었고 나머지는 비어 있다. 종류가 없으면 슬라이드에서
「입력」·「마우스」·「스냅」 라벨이 안 붙어, 자습자가 지금 칠 차례인지 올릴
차례인지를 문장에서 찾아내야 한다. 문장은 이미 그 답을 갖고 있으므로 읽어서
붙인다. 짐작이 아니라 어휘로 가른다.
"""
import io, json, re, glob, os, sys

KEYS = re.compile(r'^(Enter|Esc|Tab|Delete|Space|Backspace|F\d{1,2}|'
                  r'(Ctrl|Shift|Alt)\+\S+)$')
TYPING = re.compile(r'(입력하고|입력한|입력합니다|입력하면|를 입력|을 입력)')
ENTER = re.compile(r'엔터')
# 「끝점 스냅으로 클릭」처럼 어느 스냅인지 문장이 이미 말하고 있다.
SNAPWORD = re.compile(r'(표식|끝점|중간점|사분점|교차점|접점|근처점|직교 스냅|'
                      r'스냅으로|중심을 클릭|중심점을 클릭)')
MOUSE_OVER = re.compile(r'커서를.*(올립니다|가져갑니다|올려|끕니다|끌|움직)')
CLICK = re.compile(r'(클릭|고릅니다|엽니다|펼칩니다|체크|드래그|끌어|선택합니다|'
                   r'바꿉니다|되돌립니다|누릅니다|둡니다|비워 둡니다)')
ASK = re.compile(r'(묻습니다|물어봅니다|물어요)')
SEE = re.compile(r'(봅니다|보입니다|확인합니다|확인만|확인해|나와야|보이면|뜹니다|셉니다|'
                 r'읽습니다|훑어|적어 둡니다|메모합니다|나옵니다|사라집니다|됩니다)')


def kind_of(a):
    t = (a.get('type') or '').strip()
    txt = (a.get('do') or {}).get('ko', '')
    if t and KEYS.match(t):
        return 'key'
    if t:
        return 'type'
    if SNAPWORD.search(txt):
        return 'snap'
    if MOUSE_OVER.search(txt):
        return 'move'
    if TYPING.search(txt):
        return 'type'
    if ENTER.search(txt):
        return 'key'
    if ASK.search(txt) and not CLICK.search(txt):
        return 'ask'
    if CLICK.search(txt):
        return 'click'
    if SEE.search(txt):
        return 'see'
    return None


def main(paths, write=True):
    for p in paths:
        d = json.load(io.open(p, encoding='utf-8'))
        tally, total, blank = {}, 0, 0
        for s in d['sections']:
            for b in s.get('blocks', []):
                if b.get('type') != 'steps':
                    continue
                for st in b['items']:
                    for a in st.get('actions', []):
                        total += 1
                        if a.get('kind'):
                            tally[a['kind']] = tally.get(a['kind'], 0) + 1
                            continue
                        k = kind_of(a)
                        if k:
                            a['kind'] = k
                            tally[k] = tally.get(k, 0) + 1
                        else:
                            blank += 1
        if write:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(
                json.dumps(d, ensure_ascii=False, indent=1))
        print('%-18s 조작 %3d · 미분류 %2d · %s' % (
            os.path.basename(p), total, blank,
            ' '.join('%s=%d' % kv for kv in sorted(tally.items()))))


if __name__ == '__main__':
    main(sorted(glob.glob('scripts/selfstudy/source/lesson-0*.json')),
         write='--dry' not in sys.argv)
