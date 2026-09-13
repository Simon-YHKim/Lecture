# -*- coding: utf-8 -*-
"""무음은 조용한 게 아니라 **틀린 시각**이다.

문단 경계 시각은 합친 음성의 실측 길이에서 나온다. 토막 앞에 10초 무음이
붙으면 그 10초가 그대로 `narration-timing.json` 에 실려, 화면이 멈춰 선 채
말이 늦게 시작한다. 실제로 국문 279토막 중 143개(51%)에 그런 무음이 있었고
가장 심한 것은 18.1초 중 11초가 죽은 공기였다.

여기서 보는 것은 셋이다 — 앞뒤 무음을 걷는가, 안쪽 구멍을 줄이는가, 말을
자르지 않는가.
"""
import sys
import tempfile
from types import SimpleNamespace
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import speak_clone as S

SR = 24000


def tone(seconds, level=0.3, hz=220):
    import numpy as np
    t = np.arange(int(seconds * SR), dtype=np.float32) / SR
    return (level * np.sin(2 * np.pi * hz * t)).astype('float32')


def hush(seconds, level=0.0):
    import numpy as np
    n = int(seconds * SR)
    if not level:
        return np.zeros(n, dtype='float32')
    # 잡음 바닥. 최대 진폭 기준 문턱은 이것을 소리로 셌다.
    rng = np.random.default_rng(7)
    return (level * rng.standard_normal(n)).astype('float32')


def seconds(x):
    return len(x) / float(SR)


class TrimTests(unittest.TestCase):
    def test_leading_silence_goes_even_with_a_noise_floor(self):
        import numpy as np
        for level in (0.0, 0.004, 0.01):
            x = np.concatenate([hush(10.5, level), tone(6.5)])
            out = S.trim(x, SR)
            with self.subTest(noise=level):
                self.assertLess(seconds(out), 7.0, '앞 무음이 남았다')
                self.assertGreater(seconds(out), 6.3, '말을 잘랐다')

    def test_trailing_silence_goes(self):
        import numpy as np
        x = np.concatenate([tone(6.4), hush(4.5, 0.006)])
        out = S.trim(x, SR)
        self.assertLess(seconds(out), 6.9)
        self.assertGreater(seconds(out), 6.2)

    def test_a_long_inside_gap_becomes_one_breath(self):
        import numpy as np
        x = np.concatenate([tone(3), hush(5, 0.005), tone(3)])
        out = S.trim(x, SR)
        # 6초 말 + 한 호흡. 5초 구멍이 그대로 남으면 11초가 된다.
        self.assertLess(seconds(out), 6 + S.KEEP_GAP + .4)
        self.assertGreater(seconds(out), 6 - .4)

    def test_a_natural_pause_survives(self):
        """문장 사이 한 호흡은 낭독의 일부다. 그것까지 지우면 말이 붙어 버린다."""
        import numpy as np
        gap = S.MAX_GAP - .2
        x = np.concatenate([tone(2), hush(gap), tone(2)])
        out = S.trim(x, SR)
        self.assertGreater(seconds(out), 4 + gap - .3)

    def test_speech_without_silence_is_left_alone(self):
        x = tone(5)
        self.assertLess(abs(seconds(S.trim(x, SR)) - 5), .25)

    def test_all_silence_survives_rather_than_vanishing(self):
        """전부 무음이면 손대지 않는다. 빈 파일을 쓰면 그 문단이 통째로 사라진다."""
        x = hush(2, 0.002)
        self.assertGreater(len(S.trim(x, SR)), 0)


class BandTests(unittest.TestCase):
    def test_a_different_codec_does_not_reuse_the_12hz_budget(self):
        for sample_rate, samples_per_frame, expected in ((24000, 1920, 12.5), (24000, 960, 25)):
            codec = SimpleNamespace(get_output_sample_rate=lambda: sample_rate,
                                    get_decode_upsample_rate=lambda: samples_per_frame)
            model = SimpleNamespace(model=SimpleNamespace(speech_tokenizer=codec))
            hz = S.codec_frame_rate(model)
            self.assertEqual(hz, expected)
            allowed = S.BAND[1] * 100 / 7.35
            self.assertGreaterEqual(S.token_cap(100, 7.35, hz) / hz, allowed)
            self.assertLess(S.token_cap(100, 7.35, hz) / hz, allowed + 8)

    def test_token_budget_bounds_audio_at_the_codec_frame_rate(self):
        # The cached 12Hz codec emits 1,920 samples per generation step at 24kHz.
        # A 120-token/second assumption permits minutes for a ten-second sentence.
        codec_hz = 24000 / 1920
        for chars, rate in ((30, 7.35), (100, 7.35), (260, 13.18), (380, 13.18)):
            with self.subTest(chars=chars, rate=rate):
                allowed_seconds = S.BAND[1] * chars / rate
                cap_seconds = S.token_cap(chars, rate) / codec_hz
                self.assertGreaterEqual(cap_seconds, allowed_seconds)
                self.assertLess(cap_seconds, allowed_seconds + 8)

    def test_rate_falls_back_to_the_seed_until_there_are_samples(self):
        rate, n = S.measured_rate({}, 5.5)
        self.assertEqual((rate, n), (5.5, 0))

    def test_rate_uses_the_measured_median_once_calibrated(self):
        done = {('s', 'k', i): {'ok': True, 'sec': 10.0, 'chars': 72}
                for i in range(S.CALIBRATE)}
        rate, n = S.measured_rate(done, 5.5)
        self.assertEqual(n, S.CALIBRATE)
        self.assertAlmostEqual(rate, 7.2, places=3)

    def test_the_band_is_tight_enough_to_catch_a_third_of_a_sentence(self):
        """본문의 3분의 1만 읽힌 토막은 반드시 걸려야 한다."""
        low, high = S.BAND
        want = 10.0
        self.assertFalse(low * want <= want / 3 <= high * want)
        self.assertTrue(low * want <= want <= high * want)


class PronunciationCacheTests(unittest.TestCase):
    def test_only_the_changed_pronunciation_is_regenerated(self):
        doc = {'lessons': [{'slug': 'lesson', 'jobs': [{'key': 'line', 'chunks': [
            {'n': 1, 'text': 'Ø25 H7.'}, {'n': 2, 'text': 'Keep the drawing.'}]}]}]}
        done = {('lesson', 'line', c['n']): {'sha': S.sha(c['text'])}
                for c in doc['lessons'][0]['jobs'][0]['chunks']}
        readings = {'lesson/line#01': 'diameter twenty-five H seven.'}
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'lesson'
            folder.mkdir()
            for n in (1, 2):
                (folder / ('line#%02d.wav' % n)).touch()
            self.assertEqual(S.plan(doc, done, tmp, ''), [])
            todo = S.plan(doc, done, tmp, '', pronunciations=readings)
            self.assertEqual(len(todo), 1)
            self.assertEqual(todo[0]['text'], 'Ø25 H7.')
            self.assertEqual(S.speech_text(todo[0]), readings['lesson/line#01'])
            done[('lesson', 'line', 1)]['spokenSha'] = S.sha(readings['lesson/line#01'])
            self.assertEqual(S.plan(doc, done, tmp, '', pronunciations=readings), [])
            removed = S.plan(doc, done, tmp, '')
            self.assertEqual(len(removed), 1, 'removing a pronunciation override must replace its cached audio')
            self.assertEqual(S.speech_text(removed[0]), 'Ø25 H7.')
            readings['lesson/line#01'] = 'diameter twenty-five, H seven.'
            self.assertEqual(len(S.plan(doc, done, tmp, '', pronunciations=readings)), 1)

    def test_unknown_or_empty_reading_cannot_silently_skip(self):
        doc = {'lessons': [{'slug': 'lesson', 'jobs': [{'key': 'line', 'chunks': [
            {'n': 1, 'text': 'Read this.'}]}]}]}
        for readings in ({'missing': 'Read this.'}, {'lesson/line#01': ' '}):
            with self.subTest(readings=readings), self.assertRaises(ValueError):
                S.plan(doc, {}, '.', '', pronunciations=readings)


if __name__ == '__main__':
    unittest.main()
