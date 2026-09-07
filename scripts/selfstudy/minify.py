# -*- coding: utf-8 -*-
"""인라인용 최소 축약. 이름을 바꾸지 않고 주석과 줄바꿈만 걷어낸다."""
import re

_COMMENT = re.compile(r'/\*.*?\*/', re.S)
_NL = re.compile(r'\s*\n\s*')
_RUN = re.compile(r'[ \t]{2,}')
_TIGHT = re.compile(r'\s*([{};,>])\s*')
_SEMI = re.compile(r';\}')


def min_css(t):
    t = _COMMENT.sub('', t)
    t = _NL.sub('', t)
    t = _RUN.sub(' ', t)
    t = _TIGHT.sub(r'\1', t)
    return _SEMI.sub('}', t).strip()


def min_js(t):
    out = []
    for line in t.split('\n'):
        s = line.strip()
        if s.startswith('//') or s.startswith('/*') or s.startswith('*'):
            continue
        i = s.find('  // ')
        if i > 0 and s.count('"') % 2 == 0 and s.count("'") % 2 == 0:
            s = s[:i].rstrip()
        if s:
            out.append(s)
    return '\n'.join(out)
