"""A timing header edit may reuse speech; a spoken edit may not."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from narrate_tts import narrate, private_output, spoken_hash, synthesis_plan, verify_script_hash


class SpeechIdentityTests(unittest.TestCase):
    def test_single_recording_frame_keeps_measured_step_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frames = root / 'compositions/frames'
            frames.mkdir(parents=True)
            (frames / '05-demo.html').write_text('recording')
            script = root / 'SCRIPT.md'
            script.write_text('## Line 5 — 실습 (Frame 5)\n\n### 1단계\n\n'
                              '    원을 그립니다.\n\n### 2단계\n\n    선을 그립니다.\n', encoding='utf-8')
            jobs, units, order = synthesis_plan(script)
            self.assertEqual(len(jobs), 2)
            self.assertEqual([beat for _, beat in units[(5, 0)]], [1, 2])
            self.assertEqual(order, [(5, 0, '05-demo')])

    def test_spoken_change_requires_regeneration_but_time_header_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / 'SCRIPT.md'
            content = '## Line 1 — 소개 (Frame 1)\n\n**Time:** 0:00–0:10\n\n    (1) 도면을 읽습니다.\n'
            script.write_text(content, encoding='utf-8')
            timing = {'spokenTextSha256': spoken_hash(script)}
            script.write_text(content.replace('0:10', '0:12'), encoding='utf-8')
            verify_script_hash(tmp, timing)
            script.write_text(content.replace('읽습니다', '그립니다'), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'TTS'):
                verify_script_hash(tmp, timing)

    def test_audio_inside_repository_is_rejected(self):
        repo = Path(__file__).resolve().parents[2]
        with self.assertRaises(ValueError):
            private_output(repo / 'audio-output')
        self.assertEqual(private_output(Path(tempfile.gettempdir())),
                         Path(tempfile.gettempdir()).resolve())

    def test_script_changed_during_synthesis_does_not_publish_timing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'lesson'
            root.mkdir()
            script = root / 'SCRIPT.md'
            content = '## Line 1 — 소개 (Frame 1)\n\n    (1) 도면을 읽습니다.\n'
            script.write_text(content, encoding='utf-8')
            def change_script(*args):
                script.write_text(content.replace('읽습니다', '그립니다'), encoding='utf-8')
                return {}
            # A runner without FFmpeg stops at the tempo pre-flight, so stub that
            # probe and leave the spoken-text identity as the only way to fail.
            probe = subprocess.CompletedProcess([], 0, stdout='ffmpeg version 0 (stub)')
            with patch('narrate_tts.lesson_frames', return_value=[(1, ['01-title'])]), \
                 patch('narrate_tts.cuts_for', return_value=[]), \
                 patch('narrate_tts.shutil.which', return_value='ffmpeg'), \
                 patch('narrate_tts.subprocess.run', return_value=probe), \
                 patch('narrate_tts.speak_many', side_effect=change_script):
                with self.assertRaisesRegex(ValueError, 'TTS'):
                    narrate(str(root), str(Path(tmp) / 'audio'), 'Microsoft Heami Desktop')
            self.assertFalse((root / 'narration-timing.json').exists())


if __name__ == '__main__':
    unittest.main()
