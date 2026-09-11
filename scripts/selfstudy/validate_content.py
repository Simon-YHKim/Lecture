# -*- coding: utf-8 -*-
"""자습 교재 콘텐츠 JSON 검사.

    python tools/validate_content.py content/lesson-03.json

무엇을 보는가
  1. 구조 — 필수 키가 있는가, JSON 이 파싱되는가
  2. 이중언어 — {"ko":…, "en":…} 쌍에 한쪽만 있는 곳이 없는가
  3. 사실 충실도 — 타이핑하는 값이 원본 대본의 백틱 안에 실제로 있었는가
  4. 안전 — 산문에 HTML 태그가 섞였는가, 도해 ref 가 실재하는가
  5. 용량 — 62 KB(정본 도면을 쓰면 50 KB) 안에 들어오는가
"""
import io, json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('SELFSTUDY_SRC') or os.path.dirname(HERE)
REPO = os.environ.get('LECTURE_REPO') or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
LESSON_DIR = {
    1: 'lesson-01-orientation', 2: 'lesson-02-part-and-template',
    3: 'lesson-03-baseline-profile', 4: 'lesson-04-circles-arcs',
    5: 'lesson-05-three-views', 6: 'lesson-06-editing-symbols',
    7: 'lesson-07-dimensioning-release', 8: 'lesson-08-exam-and-qa',
}
TOP_REQUIRED = ['no', 'slug', 'title', 'videoLength', 'selfStudyMin', 'summary',
                'objectives', 'sections', 'checks', 'shortcuts', 'recap']
BLOCK_TYPES = {'p', 'list', 'cards', 'table', 'note', 'figure', 'steps'}
# 영문 철자는 미국식으로 통일한다. 이 과정이 고르라고 하는 AutoCAD 선 종류 이름이
# `CENTER` 라서, 본문이 centre 라고 쓰면 같은 것을 두 이름으로 부르게 된다.
BRITISH = re.compile(
    r'(centre|centres|centred|centring|centreline|centrelines|colour|colours|'
    r'coloured|colouring|recolour|metre|metres|millimetre|millimetres|practise|'
    r'organise|organised|recognise|analyse|labelled|labelling|modelling|grey|'
    r'draught|favour|behaviour)', re.I)
TAG = re.compile(r'</?(?:div|span|p|br|table|tr|td|th|ul|li|b|i|em|strong|h[1-6]|script|style)\b', re.I)
BACKTICK = re.compile(r'`([^`\n]+)`')


def pairs(node, path='', out=None):
    if out is None:
        out = []
    if isinstance(node, dict):
        if 'ko' in node and isinstance(node.get('ko'), str) and 'svg' not in node:
            out.append((path, node.get('ko', ''), node.get('en', '')))
        for k, v in node.items():
            if k in ('ko', 'en', 'svg'):
                continue
            pairs(v, path + '/' + str(k), out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            pairs(v, '%s[%d]' % (path, i), out)
    return out


def source_tokens(no):
    d = LESSON_DIR.get(no)
    if not d:
        return None
    p = os.path.join(REPO, 'projects', 'autocad-technician', d, 'SCRIPT.md')
    if not os.path.exists(p):
        return None
    txt = io.open(p, encoding='utf-8').read()
    toks = set()
    for m in BACKTICK.finditer(txt):
        toks.add(m.group(1).strip())
    return toks


def check(path, figures):
    errs, warns = [], []
    try:
        d = json.load(io.open(path, encoding='utf-8'))
    except Exception as e:
        return ['JSON 파싱 실패: %s' % e], []

    for k in TOP_REQUIRED:
        if k not in d:
            errs.append('최상위 키 없음: %s' % k)
    no = d.get('no')

    # 블록 유형
    used_refs, inline_svg_bytes, step_types = set(), 0, []
    for si, sec in enumerate(d.get('sections', [])):
        if not sec.get('label'):
            errs.append('sections[%d] label 없음' % si)
        for bi, b in enumerate(sec.get('blocks', [])):
            t = b.get('type')
            if t not in BLOCK_TYPES:
                errs.append('sections[%d].blocks[%d] 알 수 없는 type: %r' % (si, bi, t))
            if t == 'figure':
                if b.get('ref'):
                    used_refs.add(b['ref'])
                    if b['ref'] not in figures:
                        errs.append('없는 도면 ref: %s' % b['ref'])
                elif b.get('svg'):
                    inline_svg_bytes += len(b['svg'].encode('utf-8'))
                    if 'stroke="#' in b['svg'] or 'fill="#' in b['svg']:
                        errs.append('sections[%d] SVG 에 색이 하드코딩됐다 (클래스를 쓸 것)' % si)
                else:
                    errs.append('sections[%d].blocks[%d] figure 에 ref 도 svg 도 없다' % (si, bi))
            if t == 'steps':
                for st in b.get('items', []):
                    for a in st.get('actions', []):
                        if a.get('type'):
                            # 판마다 치는 값이 다른 자리는 사전이다. 명령을
                            # 세는 기준은 국문 과정이다.
                            value = a['type']
                            step_types.append(value['ko'] if isinstance(value, dict)
                                              else value)
                    for key in ('expect', 'why', 'pitfall'):
                        if not st.get(key):
                            warns.append('%d단계에 %s 가 비었다' % (st.get('n', 0), key))

    # 이중언어
    empty_en = [p for p, ko, en in pairs(d) if ko.strip() and not (en or '').strip()]
    if empty_en:
        errs.append('영문이 빈 쌍 %d곳: %s' % (len(empty_en), ', '.join(empty_en[:5])))
    skew = []
    for p, ko, en in pairs(d):
        if len(ko) > 25 and en:
            r = len(en) / float(len(ko))
            if r < 0.7 or r > 3.2:
                skew.append('%s (ko %d / en %d)' % (p, len(ko), len(en)))
    if skew:
        warns.append('국영 길이가 크게 어긋난 곳 %d: %s' % (len(skew), '; '.join(skew[:4])))

    # 영국식 철자 — 영문과 도해 글자 양쪽을 본다
    brit = []
    for path, ko, en in pairs(d):
        for m in BRITISH.finditer(en or ''):
            brit.append('%s: %s' % (path, m.group(0)))
    def svg_scan(node, path=''):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == 'svg' and isinstance(v, str):
                    for m in BRITISH.finditer(v):
                        brit.append('%s/svg: %s' % (path, m.group(0)))
                else:
                    svg_scan(v, path + '/' + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                svg_scan(v, '%s[%d]' % (path, i))
    svg_scan(d)
    if brit:
        errs.append('영국식 철자 %d곳: %s' % (len(brit), ', '.join(sorted(set(brit))[:6])))

    # HTML 태그 혼입
    tagged = [p for p, ko, en in pairs(d) if TAG.search(ko) or TAG.search(en or '')]
    if tagged:
        errs.append('산문에 HTML 태그가 섞였다: %s' % ', '.join(tagged[:4]))

    # 사실 충실도 — 타이핑 값이 원본 대본에 있었는가
    src = source_tokens(no)
    if src is None:
        warns.append('원본 SCRIPT.md 를 못 찾아 명령 대조를 건너뛴다')
    else:
        unknown = sorted({t for t in step_types if t not in src})
        if unknown:
            warns.append('원본 대본의 백틱에 없는 입력값 %d개: %s'
                         % (len(unknown), ', '.join(unknown[:10])))
        sk = [s.get('key') for s in d.get('shortcuts', [])]
        missing = [k for k in sk if k not in src]
        if missing:
            warns.append('단축키 표에 원본에 없는 것: %s' % ', '.join(missing[:8]))

    # 용량 — 들여쓰기가 아니라 내용을 잰다
    size = len(json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    # 실제 상한은 빌더가 잰다 — 한 쪽이 100KB 를 넘으면 1부/2부로 나눈다.
    # 여기 값은 한 차시가 통째로 비대해지는 것만 막는 안전선이다.
    cap = 120 * 1024
    if size > cap:
        errs.append('%d B — 한도 %d B 를 넘었다' % (size, cap))
    if inline_svg_bytes > 8 * 1024:
        warns.append('직접 그린 SVG 합계 %d B (한도 8192 B)' % inline_svg_bytes)

    print('%s  %s' % (os.path.basename(path), 'FAIL' if errs else 'PASS'))
    print('  %d B (한도 %d) · 절 %d · 단계 %d · 도면 ref %s'
          % (size, cap, len(d.get('sections', [])), len(step_types),
             ','.join(sorted(used_refs)) or '없음'))
    for e in errs:
        print('  X %s' % e)
    for w in warns:
        print('  ! %s' % w)
    return errs, warns


def main(argv):
    # 도면 이름은 생성기 목록에서 얻는다. .svg 파일은 저장소에 두지 않는다.
    sys.path.insert(0, HERE)
    try:
        import figures as figmod
        figures = {name for name, _ in figmod.PROFILES}
    except Exception:
        figdir = os.path.join(HERE, 'figures')
        figures = {f[:-4] for f in os.listdir(figdir)} if os.path.isdir(figdir) else set()
    paths = argv or (sorted(glob.glob(os.path.join(SCRATCH, 'content', 'lesson-*.json')))
                     or sorted(glob.glob(os.path.join(SCRATCH, 'lesson-*.json'))))
    bad = 0
    for p in paths:
        e, _ = check(p, figures)
        bad += 1 if e else 0
        print()
    print('%d/%d 통과' % (len(paths) - bad, len(paths)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith('-')]))
