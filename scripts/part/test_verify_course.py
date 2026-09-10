"""Keep archived preview caches out of the active-lesson inventory."""
from pathlib import Path
import tempfile
import unittest

from verify_course import is_lesson_source_dir


class LessonInventoryTests(unittest.TestCase):
    def test_cache_does_not_hide_an_actual_old_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.hyperframes').mkdir()
            (root / 'assets').mkdir()
            self.assertFalse(is_lesson_source_dir(root))
            (root / 'SCRIPT.md').write_text('Old lesson', encoding='utf-8')
            self.assertTrue(is_lesson_source_dir(root))

    def test_frame_entry_without_script_is_still_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html></html>', encoding='utf-8')
            self.assertTrue(is_lesson_source_dir(root))


if __name__ == '__main__':
    unittest.main()
