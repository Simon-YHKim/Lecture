"""Refresh episode playlists and timing documentation without rebuilding frames."""
import json
import os
from pathlib import Path
import re

import episodes
import lesson_docs
import lesson_kit
from sync_narration import sync
from narrate_tts import verify_script_hash
from lesson_edit import staged_edit


def refresh(lesson_dir):
    return staged_edit(lesson_dir, refresh_inplace)


def refresh_inplace(lesson_dir):
    root = Path(lesson_dir)
    timing = json.loads((root / 'narration-timing.json').read_text(encoding='utf-8'))
    verify_script_hash(root, timing)
    source = (root / 'index.html').read_text(encoding='utf-8')
    slots = []
    for tag in re.findall(r'<div\b[^>]*data-composition-src="compositions/frames/[^>]+>', source):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        slots.append((attrs['id'], attrs['data-composition-id'],
                      Path(attrs['data-composition-src']).stem,
                      float(attrs['data-start']), float(attrs['data-duration'])))
    if not slots:
        raise ValueError('No frame slots to refresh')
    brief = (root / 'BRIEF.md').read_text(encoding='utf-8')
    descriptions = {}
    for row in brief.splitlines():
        cells = [c.strip() for c in row.strip('|').split('|')]
        if len(cells) == 5 and cells[0].isdigit():
            descriptions[cells[1].strip('`')] = cells[3]
    # Earlier lesson briefs omit the screen-description column. Their existing
    # storyboard has that authored text, keyed by composition rather than stem.
    by_comp = {comp: stem for _, comp, stem, _, _ in slots}
    for row in (root / 'STORYBOARD.md').read_text(encoding='utf-8').splitlines():
        cells = [c.strip() for c in row.strip('|').split('|')]
        if len(cells) == 6 and cells[0].isdigit():
            stem = by_comp.get(cells[1].strip('`'))
            if stem:
                descriptions.setdefault(stem, cells[4])
    if any(stem not in descriptions for _, _, stem, _, _ in slots):
        raise ValueError('A frame has no existing BRIEF description')
    lesson_kit.write_episodes(str(root), slots, episodes.episodes_for(root.name), os)
    sync(root)
    total = lesson_docs.refresh(str(root), [descriptions[stem] for _, _, stem, _, _ in slots])
    script_path = root / 'SCRIPT.md'
    script = script_path.read_text(encoding='utf-8')
    spans = {}
    for _, _, stem, start, duration in slots:
        line = int(stem.split('-')[0])
        if line not in spans:
            spans[line] = [start, start + duration]
        else:
            spans[line][1] = start + duration
    sections = re.split(r'(?=^## Line \d+)', script, flags=re.M)
    for i, section in enumerate(sections):
        line = re.match(r'## Line (\d+)', section)
        if line and int(line[1]) in spans:
            a, b = spans[int(line[1])]
            sections[i] = re.sub(r'^\*\*Time:\*\*.*$',
                '**Time:** %s–%s' % (lesson_docs.clock(a), lesson_docs.clock(b)),
                section, count=1, flags=re.M)
    script = ''.join(sections)
    script = re.sub(r'^> (?:목표|전체) 길이 .*$',
        '> 전체 길이 %d분 %02d초 — 실제 TTS와 화면 전환 시간을 반영한 값입니다.'
        % (total // 60, total % 60), script, count=1, flags=re.M)
    if timing.get('source') == 'synthesised':
        script = re.sub(r'^\*\*Voice:\*\*.*$',
            '**Voice:** Windows SAPI · %s · Rate %s<br>' % (timing['voice'], timing['rate']),
            script, count=1, flags=re.M)
    script_path.write_text(script, encoding='utf-8', newline='\n')
    return total
