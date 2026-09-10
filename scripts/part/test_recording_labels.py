import unittest

from refresh_recording_labels import replace_labels


class RecordingLabelTests(unittest.TestCase):
    def test_global_step_number_and_text_preserve_scene_and_timing(self):
        cue = ('<div class="sp sp1" data-layout-allow-overlap>'
               '<span class="no">01<i>/16</i></span><span class="key"><span class="kw">OLD</span></span>'
               '<span class="what"><span class="kw">이전 제목</span></span></div>')
        original = '<div class="film">' + cue + '</div><script>tl.to(".sp1",{},12.8);</script>'
        updated = replace_labels(original, [('새 제목 <검산>', 'XL · TRIM')], 7, 17)
        self.assertIn('07<i>&#8201;/&#8201;17</i>', updated)
        self.assertIn('&lt;검산&gt;', updated)
        self.assertNotIn('OLD', updated)
        self.assertTrue(updated.endswith('</div><script>tl.to(".sp1",{},12.8);</script>'))

    def test_missing_or_duplicated_cues_are_rejected(self):
        with self.assertRaises(ValueError):
            replace_labels('<div class="film"></div>', [('저장', 'SAVEAS')], 1, 1)
        with self.assertRaises(ValueError):
            replace_labels('<div class="sp sp2"></div>', [('저장', 'SAVEAS')], 1, 1)


if __name__ == '__main__':
    unittest.main()
