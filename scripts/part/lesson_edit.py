"""Prepare a timing edit in a temporary copy before replacing any source file."""
from pathlib import Path
import tempfile


def staged_edit(lesson_dir, edit):
    root = Path(lesson_dir).resolve()
    paths = [root / name for name in ('index.html', 'SCRIPT.md', 'BRIEF.md',
              'STORYBOARD.md', 'narration-timing.json')]
    paths += sorted((root / 'compositions').rglob('*.html'))
    paths += sorted((root / 'compositions').rglob('*.motion.json'))
    originals = {p.relative_to(root): p.read_bytes() for p in paths if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='lecture-timing-') as tmp:
        stage = Path(tmp) / root.name
        for relative, content in originals.items():
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        result = edit(stage)
        changed = {p.relative_to(stage): p.read_bytes() for p in stage.rglob('*')
                   if p.is_file() and p.read_bytes() != originals.get(p.relative_to(stage))}
        # A concurrent editor must not lose work while this plan is prepared.
        for relative, original in originals.items():
            if not (root / relative).is_file() or (root / relative).read_bytes() != original:
                raise ValueError('Lesson changed while preparing timing: ' + str(relative))
        for relative in changed:
            if relative not in originals and (root / relative).exists():
                raise ValueError('A new file appeared while preparing timing: ' + str(relative))
        for relative, content in changed.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    return result
