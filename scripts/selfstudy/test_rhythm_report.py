import unittest

from rhythm_report import measure


class RhythmMeasureTests(unittest.TestCase):
    def test_global_ratio_changes_with_length_while_fixed_windows_do_not(self):
        paragraph = '도면을 읽습니다. 위치가 맞나요? 길이를 입력합니다. 화면이 바뀌었죠.'
        short, long = measure([paragraph] * 5), measure([paragraph] * 10)
        self.assertAlmostEqual(short['globalEndingRatio'], long['globalEndingRatio'] * 2)
        self.assertEqual(short['windowEndingRatioMean'], long['windowEndingRatioMean'])

    def test_labels_are_excluded_and_actual_repeated_words_are_counted(self):
        got = measure(['도면\n레이어\n선을 그립니다. 원을 그립니다. 호를 그립니다. 결과가 맞나요?'])
        self.assertEqual(got['sentences'], 4)
        self.assertEqual(got['longestRepeatedFinalWord'], 3)
        self.assertEqual(got['formalPercent'], 75)

    def test_short_text_has_no_invented_window_score(self):
        self.assertIsNone(measure(['한 문장입니다.'])['windowEndingRatioMean'])


if __name__ == '__main__':
    unittest.main()
