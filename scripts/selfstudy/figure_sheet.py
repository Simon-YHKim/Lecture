"""도해만 모은 측정용 한 쪽을 만든다.

교재 안에서는 탭에 가려진 도해가 있어 브라우저가 크기를 재지 못한다. 도해만
뽑아 한 쪽에 늘어놓으면 전부 보이므로, 영문 글자가 도해 밖으로 나가는지
서로 겹치는지를 실제 렌더로 잴 수 있다.

    python figure_sheet.py <out.html> [ko|en]
"""
import json
import re
import sys
from pathlib import Path

SOURCE = Path('scripts/selfstudy/source')
CSS = Path('scripts/selfstudy/assets/base.css')
TEXT = re.compile(r'<text[^>]*>(.*?)</text>', re.S)


def main(argv):
    out = Path(argv[1])
    lang = argv[2] if len(argv) > 2 else 'en'
    blocks = []
    for path in sorted(SOURCE.glob('lesson-*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))

        def walk(node, where=''):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == 'svg' and isinstance(value, str):
                        blocks.append((path.name, where + '/svg', value))
                    elif isinstance(value, (dict, list)):
                        walk(value, where + '/' + str(key))
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, where + '/' + str(index))

        walk(data)

    parts = ['<!doctype html><meta charset="utf-8"><title>figure sheet</title>',
             '<style>%s</style>' % CSS.read_text(encoding='utf-8'),
             '<style>figure{margin:0 0 28px;padding:8px;border:1px solid #8884}'
             'figcaption{font:12px monospace;opacity:.7}svg{max-width:100%%}</style>',
             '<body data-lang="%s">' % lang]
    for name, where, svg in blocks:
        parts.append('<figure data-source="%s%s"><figcaption>%s %s</figcaption>%s</figure>'
                     % (name, where, name, where, svg))
    parts.append('</body>')
    out.write_text('\n'.join(parts), encoding='utf-8', newline='\n')
    print('%s · 도해 %d · %d B' % (out.name, len(blocks), out.stat().st_size))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
