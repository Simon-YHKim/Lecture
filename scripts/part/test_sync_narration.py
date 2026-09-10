import unittest

from sync_narration import attach


class NarrationPlacementTests(unittest.TestCase):
    def source(self, start=0):
        return ('<div id="root">'
                '<div data-composition-id="f1" data-composition-src="compositions/frames/01-first.html" '
                'data-start="%g" data-duration="12"></div>'
                '<div data-composition-id="f2" data-composition-src="compositions/frames/02-second.html" '
                'data-start="%g" data-duration="9"></div>'
                '</div><script>window.__timelines={}</script>') % (start, start + 12)

    def timing(self):
        return {'frames': [
            {'id': '01-first', 'audio': '01-first.wav', 'start': 0, 'duration': 10.4},
            {'id': '02-second', 'audio': '02-second.wav', 'start': 10.4, 'duration': 7.4}]}

    def test_frame_hold_is_not_lost_when_placing_second_audio(self):
        result = attach(self.source(), self.timing())
        self.assertIn('data-start="12" data-duration="7.4" data-track-index="2"', result)
        self.assertEqual(result.count('<audio '), 2)
        self.assertEqual(attach(result, self.timing()), result)

    def test_episode_uses_its_local_frame_positions(self):
        result = attach(self.source(40), self.timing())
        self.assertIn('data-start="52" data-duration="7.4" data-track-index="2"', result)

    def test_missing_or_too_long_audio_is_rejected(self):
        timing = self.timing()
        timing['frames'][0]['duration'] = 13
        with self.assertRaisesRegex(ValueError, 'fit'):
            attach(self.source(), timing)
        timing['frames'].pop()
        timing['frames'][0]['duration'] = 10
        with self.assertRaisesRegex(ValueError, 'Missing'):
            attach(self.source(), timing)

    def test_nonfinite_duration_and_duplicate_frames_are_rejected(self):
        for bad in (float('nan'), float('inf'), -1):
            timing = self.timing()
            timing['frames'][0]['duration'] = bad
            with self.assertRaises(ValueError):
                attach(self.source(), timing)
        timing = self.timing()
        timing['frames'].append(timing['frames'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            attach(self.source(), timing)


if __name__ == '__main__':
    unittest.main()
