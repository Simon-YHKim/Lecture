"""Refresh recording cue text from SCRIPT.md without rebuilding its scene."""
import argparse
from html import escape
from pathlib import Path
import re

import beats
import episodes
from lesson_edit import staged_edit
from lesson_kit import keep_words

STRIP = re.compile(r'<div class="sp sp(?P<index>\d+)"[^>]*>.*?</div>', re.S)


def replace_labels(source, rows, first, total):
    """Replace only cue labels; keep the authored scene and timing byte-for-byte."""
    strips = list(STRIP.finditer(source))
    if [int(m['index']) for m in strips] != list(range(1, len(rows) + 1)):
        raise ValueError('Recording cues do not match the complete ordered step range')

    def replace(match):
        local = int(match['index']) - 1
        title, keys = rows[local]
        body = match[0]
        replacements = [
            (r'(<span class="no">).*?(</span><span class="key">)',
             f'{first + local:02d}<i>&#8201;/&#8201;{total:02d}</i>'),
            (r'(<span class="key">).*?(</span><span class="what">)',
             keep_words(escape(keys)) if keys else '&#183;'),
            (r'(<span class="what">).*?(</span></div>)',
             keep_words(escape(title.replace('`', '')))),
        ]
        for pattern, value in replacements:
            body, count = re.subn(pattern, lambda m: m[1] + value + m[2], body, flags=re.S)
            if count != 1:
                raise ValueError('Unsupported recording cue markup')
        return body

    return STRIP.sub(replace, source)


def refresh_inplace(root):
    root = Path(root)
    number = int(root.name.split('-')[1])
    line = 8 if number == 2 else 5
    script = root / 'SCRIPT.md'
    steps = beats.parse_steps(str(script), line)
    if not steps:
        return 0
    text = script.read_text(encoding='utf-8')
    section = next(s for s in re.split(r'(?=^## Line \d+)', text, flags=re.M)
                   if s.startswith(f'## Line {line} '))
    heads = re.findall(r'^### (\d+)단계\s*[—–-]\s*(.+)$', section, re.M)
    if [int(n) for n, _ in heads] != list(range(1, len(steps) + 1)):
        raise ValueError('Practice headings must enumerate every step exactly once')
    rows = list(zip([title for _, title in heads], beats.step_keys(str(script), line)))
    frames = [f for f in episodes.frames_for(root.name)
              if f == '08-build-template' or re.fullmatch(r'05-demo(?:-[a-h])?', f)]
    cuts = [0, *episodes.cuts_for(root.name), len(rows)]
    if len(frames) != len(cuts) - 1 or cuts != sorted(set(cuts)):
        raise ValueError('Internal recording cuts do not partition the practice')
    pending = []
    for frame, lo, hi in zip(frames, cuts, cuts[1:]):
        path = root / 'compositions' / 'frames' / (frame + '.html')
        source = path.read_text(encoding='utf-8')
        pending.append((path, replace_labels(source, rows[lo:hi], lo + 1, len(rows))))
    for path, updated in pending:
        path.write_text(updated, encoding='utf-8', newline='\n')
    return len(pending)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', nargs='?', type=Path)
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    if bool(args.lesson) == args.all:
        parser.error('Provide one lesson directory or --all')
    roots = [Path('projects/autocad-technician') / slug for slug in episodes.slugs()
             if 2 <= int(slug.split('-')[1]) <= 7] if args.all else [args.lesson]
    for root in roots:
        print(root.name, staged_edit(root, refresh_inplace), 'recording cues refreshed')
