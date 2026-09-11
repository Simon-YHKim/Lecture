# -*- coding: utf-8 -*-
"""덱의 이름표가 두 판에서 짝을 이루는지 본다.

본문은 자습 원본의 `{ko, en}` 에서 오지만, 덱은 제 이름표도 쓴다 — 조작 종류,
카드 머리, 스냅 이름, 형상 이름. 그 표에서 한 줄이 빠지면 영문판 화면에 그
자리만 한국어로 남는다. 실제로 그렇게 나갔고, 눈으로는 263장 중 한 장에 있는
한 낱말을 못 찾는다. 그래서 표끼리 맞춰 둔다.
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_deck_selfstudy as D
import coach as C

HANGUL = re.compile(r'[가-힣]')


class DeckLabelTests(unittest.TestCase):
    def pairs(self):
        return (('덱 이름표', D._UI_KO, D._UI_EN),
                ('조작 종류', D._ACT_KO, D._ACT_EN),
                ('스냅 이름', C._SNAP_KO, C._SNAP_EN),
                ('형상 이름', C._FEATURE_KO, C._FEATURE_EN))

    def test_every_korean_label_has_an_english_twin(self):
        for name, ko, en in self.pairs():
            with self.subTest(table=name):
                self.assertEqual(sorted(ko), sorted(en))

    def test_english_labels_carry_no_hangul(self):
        for name, _ko, en in self.pairs():
            for key, value in en.items():
                with self.subTest(table=name, key=key):
                    self.assertIsNone(HANGUL.search(value), value)

    def test_format_placeholders_match(self):
        """`%s` 자리가 다르면 영문판 빌드가 그 줄에서 멎는다."""
        for name, ko, en in self.pairs():
            for key in ko:
                with self.subTest(table=name, key=key):
                    self.assertEqual(re.findall(r'%[sd]', ko[key]),
                                     re.findall(r'%[sd]', en[key]))

    def test_english_navigation_bar_is_english(self):
        """아래 막대는 슬라이드마다 늘 보인다. 여기 남은 한글이 제일 눈에 띈다."""
        path = os.path.join(HERE, 'assets', 'deck_nav.en.html')
        self.assertTrue(os.path.isfile(path), path)
        with open(path, encoding='utf-8') as fh:
            source = fh.read()
        body = re.sub(r'<script.*?</script>', ' ', source, flags=re.S)
        body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S)
        self.assertEqual(HANGUL.findall(re.sub(r'<[^>]+>', ' ', body)), [])
        self.assertEqual(re.findall(r'aria-label="[^"]*[가-힣][^"]*"', source), [])

    def test_the_lookup_key_stays_korean(self):
        """`EXTRA` 는 국문 제목으로 절을 찾는다. 열쇠까지 언어를 따르면 빌드가 멎는다."""
        node = {'ko': '점을 찍는 네 가지 방법', 'en': 'Four ways to place a point'}
        self.assertEqual(D.ident(node), '점을 찍는 네 가지 방법')


if __name__ == '__main__':
    unittest.main()
