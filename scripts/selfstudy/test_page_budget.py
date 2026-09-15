"""Published workbook pages must fit after diagrams and navigation are added."""
import contextlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import build_selfstudy as B
import validate_content as V

SOURCE = Path(__file__).parent / 'source'


class PageBudgetTests(unittest.TestCase):
    def test_large_lesson_pages_preserve_every_step_under_the_limit(self):
        for no in (4, 5):
            lesson = json.loads((SOURCE / ('lesson-%02d.json' % no)).read_text(encoding='utf-8'))
            pages = B.build_lesson(lesson, (no - 1, no + 1))
            expected = ['L%02d-s%s' % (no, step['n']) for section in lesson['sections']
                        for block in section['blocks'] if block['type'] == 'steps'
                        for step in block['items']]
            actual = [key for page in pages for key in re.findall(r'data-step="([^"]+)"', page['html'])]
            self.assertEqual(actual, expected)
            for page in pages:
                with self.subTest(page=page['name']):
                    self.assertLessEqual(len(page['html'].encode('utf-8')), B.PAGE_CAP)

    def test_validator_rejects_an_empty_source_directory(self):
        with tempfile.TemporaryDirectory() as empty, patch.object(V, 'SCRATCH', empty):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertNotEqual(V.main([]), 0)

    def test_validator_defaults_to_the_checked_in_sources(self):
        self.assertEqual(Path(V.DEFAULT_SOURCE).resolve(), SOURCE.resolve())

    def test_oversized_unsplittable_content_is_still_rejected(self):
        lesson = json.loads((SOURCE / 'lesson-01.json').read_text(encoding='utf-8'))
        lesson['sections'][0]['blocks'] = [{'type': 'p', 'ko': '가' * 100000, 'en': 'a' * 100000}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lesson-01.json'
            path.write_text(json.dumps(lesson, ensure_ascii=False), encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                errors, _ = V.check(str(path), set())
        self.assertTrue(any('100KB' in e for e in errors), errors)

    def test_language_specific_duration_with_legacy_fallback(self):
        self.assertEqual(B.video_length({'videoLength': '1:00'}, 'en'), '1:00')
        lesson = {'videoLength': '1:00', 'videoLengthByLang': {'ko': '1:00', 'en': '1:20'}}
        self.assertEqual(B.video_length(lesson, 'en'), '1:20')


if __name__ == '__main__':
    unittest.main()
