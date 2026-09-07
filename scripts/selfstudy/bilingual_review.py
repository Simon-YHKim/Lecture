# -*- coding: utf-8 -*-
"""영문 감수용 국영 대조표.

두 가지를 낸다.

1. `bilingual-review.csv` — 국문·영문 쌍 전부. 감수자가 엑셀에서 열고 마지막
   「검토 의견」 칸에 적어 돌려주는 파일이다. UTF-8 BOM 이라 한글 윈도우 엑셀에서
   바로 열린다. 저장소에는 커밋하지 않는다 — 원본 JSON 에서 언제든 다시 나온다.

2. `bilingual-review.html` — 볼 곳만 추린 워크리스트. 3,900 쌍을 전부 화면에
   깔면 아무도 안 본다. 기계로 의심할 수 있는 것만 올린다 — 용어집을 벗어난 역어,
   길이가 크게 어긋난 쌍, 영문에 남은 한글, 영문이 비었거나 국문과 같은 곳.

    python scripts/selfstudy/bilingual_review.py [출력 디렉터리]
"""
import csv, io, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_selfstudy as B          # shell·bi·render_block 을 그대로 쓴다

SRC = os.environ.get('SELFSTUDY_SRC') or os.path.join(HERE, 'source')
HANGUL = re.compile(r'[가-힣]')
CAP = 60                              # 표 하나에 올리는 최대 행. 넘으면 그 사실을 적는다


def pairs(node, out, path='', lesson=''):
    if isinstance(node, dict):
        if isinstance(node.get('ko'), str) and 'svg' not in node:
            out.append({'lesson': lesson, 'path': path,
                        'ko': node['ko'], 'en': node.get('en', '') or ''})
        for k, v in node.items():
            if k in ('ko', 'en', 'svg'):
                continue
            pairs(v, out, path + '/' + str(k), lesson)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            pairs(v, out, '%s[%d]' % (path, i), lesson)


def load():
    rows = []
    for n in range(1, 9):
        p = os.path.join(SRC, 'lesson-%02d.json' % n)
        if os.path.exists(p):
            pairs(json.load(io.open(p, encoding='utf-8')), rows, '', '%d차시' % n)
    p = os.path.join(SRC, 'curriculum.json')
    C = json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else {}
    pairs(C, rows, '', '공통')
    return rows, C


def section_of(path):
    """/sections[3]/blocks[1]/... 를 사람이 읽는 자리로 바꾼다."""
    m = re.match(r'/sections\[(\d+)\]', path)
    if m:
        rest = path[m.end():]
        kind = 'steps' if '/items[' in rest else ('table' if '/rows[' in rest else 'text')
        return '절 %d · %s' % (int(m.group(1)) + 1, kind)
    seg = path.strip('/').split('/')[0] if path.strip('/') else '머리'
    return re.sub(r'\[\d+\]', '', seg) or '머리'


# ── 점검 ────────────────────────────────────────────────────────
def check(rows, C):
    """의심되는 것만 골라 돌려준다. 판정이 아니라 확인 요청이다."""
    empty, same, hangul, skew, term = [], [], [], [], []

    ratios = [len(r['en']) / float(len(r['ko']))
              for r in rows if len(r['ko']) >= 20 and r['en']]
    ratios.sort()
    med = ratios[len(ratios) // 2] if ratios else 1.9
    lo, hi = med / 2.0, med * 2.0

    # 영문에 남아도 되는 한글 — 학습자가 그대로 타이핑하거나 도면에 적힌 문자열
    literal = set()
    for g in C.get('glossary', []):
        literal.add(g['ko'])
    for name in ('외형선', '중심선', '숨은선', '치수선', '구성선',
                 '장공', '깊이', '사번', '이름', '굴림'):
        literal.add(name)

    for r in rows:
        ko, en = r['ko'].strip(), r['en'].strip()
        if not ko:
            continue
        if not en:
            empty.append(r); continue
        if en == ko:
            same.append(r); continue
        if HANGUL.search(en):
            left = en
            for t in sorted(literal, key=len, reverse=True):
                left = left.replace(t, '')
            if HANGUL.search(left):
                hangul.append(dict(r, note=''.join(sorted(set(HANGUL.findall(left))))[:20]))
        if len(ko) >= 20:
            ratio = len(en) / float(len(ko))
            if ratio < lo or ratio > hi:
                skew.append(dict(r, ratio=ratio))

    # 용어집 준수 — 두 가지를 따로 센다.
    #   exact  정한 어구 그대로 ("quadrant point")
    #   part   그 어구의 낱말 하나라도 ("quadrant" 만 나와도 인정)
    # 세는 대상에서 빼는 것이 둘 있다.
    #   · 국문의 그 말이 백틱 안에만 있는 쌍 — 타이핑하는 값이지 설명이 아니다
    #   · 영문이 한글을 그대로 남긴 쌍 — 레이어 이름처럼 그래야 맞는 자리다
    tick = re.compile(r'`[^`]*`')
    for g in C.get('glossary', []):
        k, e = g['ko'], (g.get('en') or '').split('(')[0].strip().lower()
        if not k or not e or len(k) < 2:
            continue
        # 낱말은 앞 6글자만 본다. centerline 과 center, projection 과 project 를
        # 다른 말로 세면 「줄여 썼다」가 「용어를 안 썼다」로 잡힌다.
        words = [w for w in re.split(r'[\s/]+', e) if len(w) >= 4]
        partre = (re.compile('|'.join(r'\b%s' % re.escape(w[:6]) for w in words))
                  if words else None)

        seen = []
        for r in rows:
            if not r['en']:
                continue
            prose = tick.sub(' ', r['ko'])       # 타이핑 값은 설명이 아니다
            if k not in prose:
                continue
            if k in r['en']:                     # 영문이 일부러 한글을 남긴 자리
                continue
            seen.append(r)
        if not seen:
            continue
        ex = [r for r in seen if e in r['en'].lower()]
        pt = [r for r in seen if partre and partre.search(r['en'].lower())]
        if len(ex) == len(seen):
            continue
        neither = [r for r in seen if not (partre and partre.search(r['en'].lower()))]
        term.append({'ko': k, 'en': g.get('en', ''), 'words': words,
                     'hit': len(seen),
                     'exact': len(ex) / float(len(seen)),
                     'headrate': len(pt) / float(len(seen)),
                     'rate': len(pt) / float(len(seen)),
                     'samples': (neither or [r for r in seen if e not in r['en'].lower()])[:3]})
    term.sort(key=lambda x: (x['headrate'], x['exact']))
    skew.sort(key=lambda x: abs(x['ratio'] - med), reverse=True)
    return {'empty': empty, 'same': same, 'hangul': hangul, 'skew': skew,
            'term': term, 'median': med, 'lo': lo, 'hi': hi}


# ── 산출 ────────────────────────────────────────────────────────
def write_csv(rows, path):
    with io.open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['차시', '자리', '경로', '국문', '영문',
                    '국문 글자수', '영문 글자수', '영문/국문', '검토 의견'])
        for r in rows:
            ko, en = r['ko'], r['en']
            ratio = ('%.2f' % (len(en) / float(len(ko)))) if ko and en else ''
            w.writerow([r['lesson'], section_of(r['path']), r['path'],
                        ko, en, len(ko), len(en), ratio, ''])


def tbl(head, rows_html, ctx):
    return B.render_block({'type': 'table', 'head': head, 'rows': rows_html}, ctx)


def cell(s):
    return {'ko': s, 'en': s}


def clip(s, n=150):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n] + '…'


def build_html(rows, C, res, csv_name):
    ctx = {'lesson': 'REV', 'label': ''}
    per = {}
    for r in rows:
        d = per.setdefault(r['lesson'], [0, 0, 0])
        d[0] += 1; d[1] += len(r['ko']); d[2] += len(r['en'])

    ov = ['<h2 class="first"><span class="num">01</span><span class="k">무엇을 보는 자리인가</span>'
          '<span class="e">What this page is</span></h2>']
    ov.append(B.render_block({'type': 'cards', 'items': [
        {'label': {'ko': '무엇을', 'en': 'What'},
         'body': {'ko': '자습 교재의 국문·영문 쌍 %d개를 기계로 훑어 **확인이 필요한 것만** 모았습니다.'
                        % len(rows),
                  'en': 'All %d Korean/English pairs in the self-study material, machine-checked, '
                        'with only the ones worth a second look listed here.' % len(rows)}},
        {'label': {'ko': '왜', 'en': 'Why'},
         'body': {'ko': '3,900쌍을 화면에 다 깔면 아무도 끝까지 안 봅니다. 볼 곳을 줄이는 것이 이 장의 일이에요.',
                  'en': 'Nobody reads 3,900 rows on screen. The job of this page is to shorten the list.'}},
        {'label': {'ko': '어떻게', 'en': 'How'},
         'body': {'ko': '전체 대조는 `%s` 로 나갑니다. 엑셀에서 열고 마지막 칸에 의견을 적어 돌려주세요.'
                        % csv_name,
                  'en': 'The full comparison ships as `%s`. Open it in Excel and write in the last column.'
                        % csv_name}}]}, ctx))
    ov.append(B.render_block({'type': 'note', 'tone': 'warn',
                              'label': {'ko': '아래 목록은 판정이 아닙니다', 'en': 'These are not verdicts'},
                              'ko': '기계는 뜻을 못 읽습니다. 「용어가 안 보인다」는 대명사로 받았거나 문장을 다시 쓴 경우일 수도 있어요. '
                                    '틀렸다는 뜻이 아니라 **사람이 한 번 볼 자리**라는 뜻입니다.',
                              'en': 'A machine cannot read meaning. “The term is missing” may simply be a pronoun or a '
                                    'sentence rewritten in English. It marks a place for a human to look, not an error.'}, ctx))
    ov.append('<h3><span class="k">분량</span><span class="e">Volume</span></h3>')
    ov.append(tbl([cell('차시'), cell('쌍'), cell('국문 글자'), cell('영문 글자'), cell('영문/국문')],
                  [[cell(k), cell('%d' % v[0]), cell('%d' % v[1]), cell('%d' % v[2]),
                    cell('%.2f' % (v[2] / float(v[1])) if v[1] else '—')]
                   for k, v in sorted(per.items())], ctx))

    def block(title_ko, title_en, lede_ko, lede_en, items, render, n):
        h = ['<h2%s id="s%d"><span class="num">%02d</span><span class="k">%s</span><span class="e">%s</span></h2>'
             % (' class="first"' if n == 1 else '', n, n, title_ko, title_en)]
        h.append('<p class="lede"><span class="k">%s</span><span class="e">%s</span></p>' % (lede_ko, lede_en))
        if not items:
            h.append(B.render_block({'type': 'note', 'tone': 'tip',
                                     'label': {'ko': '없음', 'en': 'None'},
                                     'ko': '이 검사에서 걸린 것이 없습니다.',
                                     'en': 'Nothing tripped this check.'}, ctx))
            return ''.join(h)
        h.append(render(items[:CAP]))
        if len(items) > CAP:
            h.append(B.render_block({'type': 'note', 'tone': 'warn',
                                     'label': {'ko': '잘린 목록', 'en': 'List truncated'},
                                     'ko': '%d건 중 %d건만 올렸습니다. 나머지는 `%s` 에 전부 있습니다.'
                                           % (len(items), CAP, csv_name),
                                     'en': '%d of %d shown. The rest are all in `%s`.'
                                           % (CAP, len(items), csv_name)}, ctx))
        return ''.join(h)

    def rows_pair(items):
        return tbl([cell('자리'), cell('국문'), cell('영문')],
                   [[cell('%s · %s' % (r['lesson'], section_of(r['path']))),
                     cell(clip(r['ko'])), cell(clip(r['en']) or '—')] for r in items], ctx)

    fl = []
    n = 0
    n += 1; fl.append(block('영문이 비었습니다', 'English is empty',
        '국문만 있고 영문이 없는 쌍입니다. 이건 판정이 아니라 결함이에요.',
        'Korean with no English. This one really is a defect, not a question.',
        res['empty'], rows_pair, n))
    n += 1; fl.append(block('영문이 국문과 똑같습니다', 'English identical to Korean',
        '옮기지 않고 그대로 둔 자리일 수 있습니다. 고유명사·명령·좌표라면 정상이에요.',
        'Possibly left untranslated. Normal if it is a proper noun, a command or a coordinate.',
        res['same'], rows_pair, n))
    n += 1; fl.append(block('영문에 한글이 남았습니다', 'Hangul left inside the English',
        '레이어 이름처럼 <b>그대로 타이핑해야 하는 값</b>은 남는 것이 맞습니다. 그 밖이라면 옮겨야 해요.',
        'Values the learner must type verbatim — layer names and the like — belong there. Anything else should be translated.',
        res['hangul'],
        lambda it: tbl([cell('자리'), cell('남은 한글'), cell('영문')],
                       [[cell('%s · %s' % (r['lesson'], section_of(r['path']))),
                         cell(r.get('note', '')), cell(clip(r['en']))] for r in it], ctx), n))
    n += 1; fl.append(block('길이가 크게 어긋납니다', 'Length is far off',
        '이 교재의 영문/국문 글자수 중앙값은 %.2f 입니다. %.2f 아래이거나 %.2f 위인 쌍만 올렸어요. '
        '한쪽에 사실이 빠졌거나 늘어난 자리일 수 있습니다.'
        % (res['median'], res['lo'], res['hi']),
        'The median English-to-Korean character ratio here is %.2f. Only pairs below %.2f or above %.2f are listed. '
        'One side may be missing a fact, or padded.' % (res['median'], res['lo'], res['hi']),
        res['skew'],
        lambda it: tbl([cell('자리'), cell('비율'), cell('국문'), cell('영문')],
                       [[cell('%s · %s' % (r['lesson'], section_of(r['path']))),
                         cell('%.2f' % r['ratio']), cell(clip(r['ko'], 110)), cell(clip(r['en'], 110))]
                        for r in it], ctx), n))

    gl = ['<h2 id="term"><span class="num">05</span><span class="k">용어집을 벗어난 자리</span>'
          '<span class="e">Where the glossary term does not appear</span></h2>',
          '<p class="lede"><span class="k">두 열을 따로 셌습니다. <b>어구 그대로</b>는 「drawing border」처럼 정한 말이 통째로 나온 비율이고, '
          '<b>낱말 하나라도</b>는 「quadrant」처럼 그 어구의 낱말 하나만 나와도 인정한 비율이에요. 앞이 낮고 뒤가 높으면 영문이 짧게 줄여 쓴 것이라 대개 문제가 아닙니다. '
          '<b>둘 다 낮은 줄</b>이 실제로 볼 자리입니다.</span>'
          '<span class="e">Two separate counts. <b>Exact</b> is how often the agreed phrase appears whole, '
          '<b>any word</b> how often at least one word of it does. A low exact with a high head noun usually just means '
          'the English shortened it. <b>Rows low in both</b> are the ones worth reading.</span></p>']
    if res['term']:
        gl.append(tbl([cell('국문'), cell('정한 역어'), cell('나온 쌍'),
                       {'ko': '어구 그대로', 'en': 'Exact'},
                       {'ko': '낱말 하나라도', 'en': 'Any word'}],
                      [[cell(t['ko']), cell(t['en']), cell('%d' % t['hit']),
                        cell('%.0f%%' % (100 * t['exact'])),
                        cell('%.0f%%' % (100 * t['headrate']))]
                       for t in res['term'][:40]], ctx))
        worst = res['term'][0] if res['term'] else None
        if worst and worst['samples']:
            gl.append('<h3><span class="k">가장 낮은 항목 「%s」의 실제 문장</span>'
                      '<span class="e">Actual sentences for the lowest one, “%s”</span></h3>'
                      % (worst['ko'], worst['ko']))
            gl.append(tbl([cell('국문'), cell('영문')],
                          [[cell(clip(s['ko'], 120)), cell(clip(s['en'], 120))]
                           for s in worst['samples']], ctx))
    else:
        gl.append(B.render_block({'type': 'note', 'tone': 'tip',
                                  'label': {'ko': '없음', 'en': 'None'},
                                  'ko': '모든 용어가 짝이 되는 영문에 나타납니다.',
                                  'en': 'Every term appears in its paired English.'}, ctx))

    how = ['<h2 class="first"><span class="num">01</span><span class="k">전체 대조표 쓰는 법</span>'
           '<span class="e">Using the full comparison</span></h2>',
           B.render_block({'type': 'table',
                           'caption': {'ko': '`%s` 의 열' % csv_name, 'en': 'Columns in `%s`' % csv_name},
                           'head': [cell('열'), {'ko': '무엇', 'en': 'What'}],
                           'rows': [[cell('차시 · 자리 · 경로'),
                                     {'ko': '어느 차시의 어느 절인지. 경로는 원본 JSON 안의 정확한 위치입니다.',
                                      'en': 'Which lesson and section. The path is the exact spot in the source JSON.'}],
                                    [cell('국문 · 영문'),
                                     {'ko': '대조할 두 문장입니다.', 'en': 'The two strings to compare.'}],
                                    [cell('글자수 · 영문/국문'),
                                     {'ko': '한쪽이 빠졌는지 훑을 때 씁니다.',
                                      'en': 'Use it to scan for a side that lost something.'}],
                                    [cell('검토 의견'),
                                     {'ko': '**여기에 적어 주세요.** 고칠 영문을 그대로 적으면 그대로 반영합니다.',
                                      'en': '**Write here.** Put the replacement English in and it goes in verbatim.'}]]}, ctx),
           B.render_block({'type': 'note', 'tone': 'tip',
                           'label': {'ko': '다시 만들려면', 'en': 'To regenerate'},
                           'ko': '`python scripts/selfstudy/bilingual_review.py` 를 돌리면 이 장과 CSV 가 다시 나옵니다. '
                                 'CSV 는 저장소에 커밋하지 않습니다 — 원본 JSON 에서 언제든 나오니까요.',
                           'en': 'Run `python scripts/selfstudy/bilingual_review.py` to rebuild this page and the CSV. '
                                 'The CSV is not committed — it falls out of the source JSON whenever you need it.'}, ctx)]

    meta = ('<span class="k">작성 %s · 발행 Claude Code · 쌍 %d개 · </span>'
            '<span class="e">Written %s · Claude Code · %d pairs · </span>'
            % (B.STAMP, len(rows), B.STAMP, len(rows)))
    eyeb = ('<span class="k">LG이노텍 Green Star · for technician · 영문 감수</span>'
            '<span class="e">LG Innotek Green Star · for technician · English review</span>')
    pager = ('<nav class="pager" aria-label="이동 / Navigation">'
             '<a href="index.html"><span class="k">&#8592; 과정 전체</span>'
             '<span class="e">&#8592; All lessons</span></a><span class="sp"></span></nav>')
    return B.shell('국영 대조 — 영문 감수', eyeb,
                   B.bi({'ko': '국영 대조 — 영문 감수', 'en': 'Korean / English review'}),
                   meta,
                   [('p-ov', {'ko': '요약', 'en': 'Overview'}),
                    ('p-fl', {'ko': '볼 곳', 'en': 'Worklist'}),
                    ('p-tm', {'ko': '용어', 'en': 'Terms'}),
                    ('p-hw', {'ko': '쓰는 법', 'en': 'How to use'})],
                   [('p-ov', ''.join(ov)), ('p-fl', ''.join(fl)),
                    ('p-tm', ''.join(gl)), ('p-hw', ''.join(how))],
                   pager, grade='S')


def main(outdir):
    rows, C = load()
    res = check(rows, C)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    csv_name = 'bilingual-review.csv'
    cp = os.path.join(outdir, csv_name)
    write_csv(rows, cp)
    hp = os.path.join(outdir, 'bilingual-review.html')
    io.open(hp, 'w', encoding='utf-8', newline='\n').write(build_html(rows, C, res, csv_name))
    print('%8d B  %s   (커밋하지 않음)' % (os.path.getsize(cp), csv_name))
    print('%8d B  %s' % (os.path.getsize(hp), os.path.basename(hp)))
    print('쌍 %d · 영문 빔 %d · 국영 동일 %d · 한글 잔류 %d · 길이 이상 %d · 용어 확인 %d'
          % (len(rows), len(res['empty']), len(res['same']), len(res['hangul']),
             len(res['skew']), len(res['term'])))
    return 0 if os.path.getsize(hp) <= B.PAGE_CAP else 1


if __name__ == '__main__':
    default = os.path.join(os.path.abspath(os.path.join(HERE, os.pardir, os.pardir)),
                           'docs', 'autocad-technician', 'self-study')
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default))
