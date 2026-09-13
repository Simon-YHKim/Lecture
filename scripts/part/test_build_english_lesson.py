"""Drawing localization must see numeric entities as the learner sees them."""
import re
import unittest

import build_english_lesson as english


class DrawingEntitiesTests(unittest.TestCase):
    def test_encoded_callouts_use_the_existing_english_drawing_terms(self):
        source = '<svg><text x="12" y="20">4-M5 &#44618;&#51060; 10</text><text x="4">2-&#51109;&#44277; R5</text></svg>'
        result, hits = english.localise_drawing(source)
        self.assertEqual(hits, 2)
        self.assertIn('4-M5 DEPTH 10', result)
        self.assertIn('2-SLOT R5', result)
        remove_text = lambda s: re.sub(r'(?<=>)[^<>]+(?=<)', '', s)
        self.assertEqual(remove_text(source), remove_text(result))

    def test_literal_labels_and_whitespace_remain_supported(self):
        source = '<tspan x="1">  4-M5 깊이 10 </tspan><text>정면도</text>'
        result, hits = english.localise_drawing(source)
        self.assertEqual(hits, 2)
        self.assertEqual(result, '<tspan x="1">  4-M5 DEPTH 10 </tspan><text>FRONT VIEW</text>')

    def test_other_drawing_values_are_unchanged_and_translation_is_idempotent(self):
        source = '<text x="2">PCD Ø44</text><text>45°</text><text>4-M5 DEPTH 10</text>'
        self.assertEqual(english.localise_drawing(source), (source, 0))


if __name__ == '__main__':
    unittest.main()
