"""Prevent recording overlays drifting from the lesson's actual spoken steps."""
from pathlib import Path
import html
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'projects/autocad-technician/lesson-07-dimensioning-release'


class RecordingStepTests(unittest.TestCase):
    def test_lesson_seven_derived_steps_and_overlays_follow_script(self):
        script = (PROJECT / 'SCRIPT.md').read_text(encoding='utf-8')
        headings = re.findall(r'^### (\d+)단계 — (.+)$', script, re.M)
        self.assertEqual([int(n) for n, _ in headings], list(range(1, 18)))
        derived = json.loads((ROOT / 'scripts/part/lesson_data_3_7.json').read_text(encoding='utf-8'))
        self.assertEqual(derived['7']['data']['steps'], [title for _, title in headings])
        counts = []
        labels = []
        for suffix in 'abc':
            text = (PROJECT / f'compositions/frames/05-demo-{suffix}.html').read_text(encoding='utf-8')
            numbers = re.findall(r'<span class="no">(\d+)<i>&#8201;/&#8201;(\d+)</i>', text)
            labels += [(int(n), int(total)) for n, total in numbers]
            titles = re.findall(r'<span class="what">(.*?)</span></div>', text)
            plain = [html.unescape(re.sub(r'<[^>]*>', '', t)) for t in titles]
            start = sum(counts)
            self.assertEqual(plain, [title for _, title in headings[start:start + len(numbers)]])
            counts.append(len(numbers))
        self.assertEqual(counts, [5, 9, 3])
        self.assertEqual(labels, [(n, 17) for n in range(1, 18)])


if __name__ == '__main__':
    unittest.main()
