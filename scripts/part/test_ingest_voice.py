# -*- coding: utf-8 -*-
"""복제 음성을 받아 쓴 시각 파일도 같은 관문을 통과해야 한다.

`narration-timing.json` 은 화면을 음성에 맞추는 유일한 근거다. 길이를 글자 수로
추정하거나 토막 하나를 조용히 빠뜨리면 그림과 말이 밀린 채로 영상이 나간다.
여기서 보는 것은 세 가지다 — 실측한 길이로 연속된 시간선이 나오는가, 문단
사이 쉼이 규격대로인가, 토막이 없으면 멈추는가.
"""
import array
import io
import json
import math
import shutil
import sys
import tempfile
import unittest
import wave
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ingest_voice
import narrate_tts as N
import tts_jobs

CLONE = sorted(N.CLONES)[0]


def tone(path, seconds, hz=440):
    samples = array.array('h', (int(7000 * math.sin(2 * math.pi * hz * i / 24000))
                                for i in range(round(seconds * 24000))))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as out:
        out.setparams((1, 2, 24000, 0, 'NONE', 'not compressed'))
        out.writeframes(samples.tobytes())


class IngestVoiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.lesson = self.base / 'lesson-99-clone'
        self.lesson.mkdir()
        (self.lesson / 'SCRIPT.md').write_text(
            '## Line 1 — 확인 (Frame 1)\n\n    (1) 원을 읽습니다.\n\n    (2) 선을 읽습니다.\n',
            encoding='utf-8')
        self.src = self.base / 'in'

    def lay_chunks(self, seconds=1.2, skip=()):
        """대본이 부르는 이름 그대로 토막 WAV 를 깔아 둔다."""
        jobs, _u, _o = N.synthesis_plan(str(self.lesson / 'SCRIPT.md'))
        made = 0
        for key, text in jobs:
            pieces = tts_jobs.chunks_of(tts_jobs.spoken(text), 'ko')
            for n in range(1, len(pieces) + 1):
                if (key, n) in skip:
                    continue
                tone(self.src / self.lesson.name / ('%s#%02d.wav' % (key, n)),
                     seconds + .3 * made)
                made += 1
        return made

    def run_ingest(self, out='audio'):
        with redirect_stdout(io.StringIO()):
            return ingest_voice.ingest(str(self.lesson), str(self.src), str(self.base / out),
                                       CLONE, N.TEMPOS[CLONE], 'test', 'ko')

    def test_measured_timeline_passes_the_delivery_gate(self):
        self.lay_chunks()
        timing = self.run_ingest()
        self.assertEqual(N.verify_tempo_timing(timing, required=True), 1.0)
        self.assertEqual(timing['tempoMethod'], 'voice-clone-native')
        self.assertEqual(timing['voice'], CLONE)
        self.assertAlmostEqual(N.frame_hold(timing), N.BASE_FRAME_HOLD)

        frame = timing['frames'][0]
        self.assertEqual(len(frame['units']), 2)
        # 배속이 없으니 원본과 내보낸 것이 같은 소리다.
        self.assertEqual(frame['duration'], frame['sourceDuration'])
        self.assertEqual(frame['audioSha256'], frame['sourceAudioSha256'])
        # 같은 소리라도 원본은 따로 보관한다. 두 갈래의 실제 경로가 달라야 한다.
        media = json.loads((self.lesson / 'media.local.json').read_text(encoding='utf-8'))
        self.assertNotEqual(media['frames'][frame['id']], media['sourceFrames'][frame['id']])
        # 재 본 길이여야 한다. 글자 수로 추정한 값이 아니다.
        self.assertAlmostEqual(frame['duration'],
                               N.wav_seconds(media['frames'][frame['id']]), places=3)
        # 문단 사이 쉼은 규격값 그대로.
        self.assertLess(abs(frame['units'][1]['start'] - frame['units'][0]['end'] - N.GAP), .002)
        self.assertLess(abs(frame['units'][0]['start'] - N.LEAD), .002)
        self.assertNotIn(b'\r', (self.lesson / 'narration-timing.json').read_bytes())

    def test_a_missing_chunk_stops_the_run(self):
        jobs, _u, _o = N.synthesis_plan(str(self.lesson / 'SCRIPT.md'))
        self.lay_chunks(skip={(jobs[-1][0], 1)})
        with self.assertRaisesRegex(SystemExit, '토막이 없다'):
            self.run_ingest()

    def test_a_leftover_chunk_stops_the_run(self):
        """대본이 짧아졌는데 옛 토막이 남아 있으면 없는 말이 섞인다."""
        jobs, _u, _o = N.synthesis_plan(str(self.lesson / 'SCRIPT.md'))
        self.lay_chunks()
        tone(self.src / self.lesson.name / ('%s#09.wav' % jobs[0][0]), 1.0)
        with self.assertRaisesRegex(SystemExit, '남는 토막'):
            self.run_ingest()

    def test_chunks_are_joined_with_a_shorter_pause_than_paragraphs(self):
        """한 문단 안의 쉼이 문단 사이 쉼보다 짧아야 한 문단으로 들린다."""
        self.assertLess(max(ingest_voice.CHUNK_GAPS.values()), N.GAP)
        self.assertLess(ingest_voice.CHUNK_GAP, N.GAP)
        # 값을 읽는 문장 앞이 툭 던지는 말 앞보다 넉넉해야 한다.
        self.assertGreater(ingest_voice.CHUNK_GAPS['slow'], ingest_voice.CHUNK_GAPS['light'])

    def test_ffmpeg_path_still_produces_two_distinct_tracks(self):
        if not shutil.which('ffmpeg'):
            self.skipTest('배속 변환에는 ffmpeg 가 필요하다')
        self.lay_chunks()
        with redirect_stdout(io.StringIO()):
            timing = ingest_voice.ingest(str(self.lesson), str(self.src), str(self.base / 'fast'),
                                         N.VOICES['ko'], 1.38, 'ffmpeg test', 'ko')
        self.assertEqual(N.verify_tempo_timing(timing, required=True), 1.38)
        self.assertEqual(timing['tempoMethod'], 'ffmpeg-atempo-per-paragraph')
        frame = timing['frames'][0]
        self.assertLess(frame['duration'], frame['sourceDuration'])
        self.assertNotEqual(frame['audioSha256'], frame['sourceAudioSha256'])


if __name__ == '__main__':
    unittest.main()
