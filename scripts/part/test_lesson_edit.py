from pathlib import Path
import tempfile
import unittest

from lesson_edit import staged_edit
from narrate_tts import spoken_hash, verify_script_hash
from prepare_lecture import motion_spec


class TimingSafetyTests(unittest.TestCase):
    def test_failed_preparation_keeps_source_and_episode_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'lesson'
            ep = root / 'compositions/episodes/ep1.html'
            ep.parent.mkdir(parents=True)
            ep.write_text('original narration', encoding='utf-8')
            def fail(stage):
                (stage / 'compositions/episodes/ep1.html').write_text('changed')
                raise ValueError('invalid storyboard')
            with self.assertRaises(ValueError):
                staged_edit(root, fail)
            self.assertEqual(ep.read_text(encoding='utf-8'), 'original narration')

    def test_step_boundaries_are_part_of_speech_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / 'SCRIPT.md'
            before = ('## Line 5 — 실습 (Frame 5)\n\n### 1단계\n\n'
                      '    원을 그립니다.\n\n### 2단계\n\n    선을 그립니다.\n')
            script.write_text(before, encoding='utf-8')
            identity = spoken_hash(script)
            script.write_text(before.replace('### 2단계\n\n', '') + '\n### 2단계\n', encoding='utf-8')
            self.assertNotEqual(identity, spoken_hash(script))

    def test_legacy_timing_without_identity_cannot_be_reused(self):
        with self.assertRaisesRegex(ValueError, 'TTS'):
            verify_script_hash('.', {'source': 'synthesised'})

    def test_nested_motion_deadlines_use_the_master_clock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sidecar = root / 'compositions/frames/02-next.motion.json'
            sidecar.parent.mkdir(parents=True)
            sidecar.write_text('{"duration":12,"assertions":[{"kind":"appearsBy",'
                               '"selector":"#next h1","bySec":3}]}', encoding='utf-8')
            html = ('<div data-composition-id="next" '
                    'data-composition-src="compositions/frames/02-next.html" '
                    'data-start="40" data-duration="12"></div>')
            spec = motion_spec(root, html)
            self.assertEqual(spec['duration'], 52)
            self.assertEqual(spec['assertions'][0]['bySec'], 43)


if __name__ == '__main__':
    unittest.main()
