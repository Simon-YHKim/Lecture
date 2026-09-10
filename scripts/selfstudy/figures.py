# -*- coding: utf-8 -*-
"""정본 도면 SVG 를 자습 교재용으로 바꾼다.

scripts/part/edu_ib_02.py 가 master-part-geometry.json 과 같은 정의에서 그린
검증된 도면을 쓴다. 손으로 다시 그리지 않는다 — 접선·필렛·탭 좌표를 눈으로
맞추면 반드시 어긋난다.

여기서 하는 일은 셋뿐이다.
  1. 색을 하드코딩된 #111 · #fff 에서 CSS 변수로 바꾼다 (라이트/다크 자동)
  2. 화면에 안 나오는 강조 겹선(.hl)과 검산선(.chk)을 지운다 — 순전한 용량
  3. 파일 크기를 줄이려고 좌표 소수점을 세 자리에서 두 자리로 줄인다

    python tools/figures.py            # tools/figures/*.svg 를 다시 만든다
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'figures')
# 저장소 뿌리는 이 파일 위치에서 찾는다. 절대 경로를 코드에 박지 않는다.
REPO = os.environ.get('LECTURE_REPO') or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
GEN = os.path.join(REPO, 'scripts', 'part', 'edu_ib_02.py')

PROFILES = [('front', ['--profile', 'front']),
            ('frontdim', ['--profile', 'frontdim']),
            ('three', [])]

# 판의 언어. 영문판은 도면의 다섯 글자(탭·장공 표기와 뷰 이름)를 영문으로 받는다.
# 학습자가 도면의 글자를 그대로 보고 타이핑하므로 본문이 인용하는 표기와 같아야 한다.
LANG = os.environ.get('SELFSTUDY_LANG', 'ko')

STYLE = ''   # .dwg 규칙은 base.css 한 곳에만 둔다 — 도해마다 복사하지 않는다

DROP = re.compile(r'<(?:path|line|circle|rect)[^>]*class="(?:hl|chk)"[^>]*/>\s*')
BG = re.compile(r'<rect[^>]*fill="#fff"[^>]*/>\s*')
OLDSTYLE = re.compile(r'<style>.*?</style>\s*', re.S)
NUM = re.compile(r'(\d+)\.(\d{3,})')
FEAT = re.compile(r'\s*data-feature="[^"]*"')


def shrink_num(m):
    whole, frac = m.group(1), m.group(2)
    v = round(float(whole + '.' + frac), 2)
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s


# 뷰 이름은 도해 안에 두 언어를 나란히 둔다. 국/영 두 벌을 만들면 용량이 두 배가 된다.
VIEW_LABELS = [('>평면도<', '>평면도 TOP<'),
               ('>정면도<', '>정면도 FRONT<'),
               ('>우측면도<', '>우측면도 RIGHT<')]


def adapt(svg, keep_features=False, keep_hl=False, lang=None):
    # 국문 도면은 뷰 이름에 영문을 나란히 붙인다. 영문 도면은 이미 영문 이름을
    # 달고 나오므로 붙이지 않는다.
    if (lang or LANG) != 'en':
        for a, b in VIEW_LABELS:
            svg = svg.replace(a, b)
    if not keep_hl:
        svg = DROP.sub('', svg)
    svg = BG.sub('', svg)
    svg = OLDSTYLE.sub(STYLE + '\n', svg)
    if not keep_features:
        svg = FEAT.sub('', svg)
    svg = NUM.sub(shrink_num, svg)
    svg = svg.replace(' xmlns="http://www.w3.org/2000/svg"', '')
    svg = re.sub(r'\n{2,}', '\n', svg)
    return svg.strip()


def build_map(keep_hl=False, lang=None):
    """정본 생성기를 돌려 {이름: svg} 로 돌려준다. 저장소에 .svg 파일을 남기지 않는다.

    `keep_hl` 은 강조 겹선(.hl)과 형상 이름(data-feature)을 남긴다. 슬라이드가
    「지금 그리는 것은 이것」을 도면 위에서 짚어 줄 때 그 겹선을 켠다. 읽는 판은
    켤 일이 없으므로 기본은 지운 판이다.

    이 저장소의 가드는 벡터·래스터 이미지 파일을 확장자로 차단한다. 그래서 도면은
    파일로 커밋하지 않고, 빌드할 때마다 scripts/part/edu_ib_02.py 에서 다시 뽑아
    HTML 안에 인라인으로 넣는다.
    """
    import tempfile, shutil
    tmpdir = tempfile.mkdtemp(prefix='selfstudy-fig-')
    try:
        out = {}
        tmp = os.path.join(tmpdir, 'raw.svg')
        want = lang or LANG
        for name, args in PROFILES:
            subprocess.run([sys.executable, GEN, tmp] + args + ['--lang', want],
                           check=True, capture_output=True)
            out[name] = adapt(io.open(tmp, encoding='utf-8').read(),
                              keep_features=keep_hl, keep_hl=keep_hl, lang=want)
        return out
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, svg in build_map().items():
        p = os.path.join(OUT, name + '.svg')
        io.open(p, 'w', encoding='utf-8', newline='\n').write(svg)
        print('%-10s %6d B' % (name, len(svg.encode('utf-8'))))


if __name__ == '__main__':
    main()
