# -*- coding: utf-8 -*-
"""Colab 이 만든 복제 음성을 받아 차시별 시각 파일을 쓴다.

`qwen_colab.py` 는 토막 단위로 WAV 를 낸다. 여기서 토막을 문단으로, 문단을
프레임으로 이어 붙이고 **실제 PCM 길이를 다시 재서** `narration-timing.json` 을
쓴다. 길이를 글자 수로 추정하지 않는다 — 그러면 화면과 음성이 조금씩 밀린다.

    python scripts/part/ingest_voice.py --in <풀어놓은 zip> --out <저장소 밖 폴더>
    python scripts/part/ingest_voice.py --in ... --out ... --lesson lesson-02

받는 모양:  <풀어놓은 zip>/<차시>/<열쇠>#<번호>.wav

복제 음성은 사람 말투 그대로 나오므로 기본 배속이 1.0 이다. Heami 의 1.38 은
규칙 기반 음성이 느려서 올린 값이고, 복제본에 올릴 이유가 없다. 그래도 같은
속도로 맞추고 싶으면 `--tempo 1.38` 을 주면 ffmpeg 로 변환해 두 갈래(원본·변환)를
그대로 남긴다.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import narrate_tts as N
import tts_jobs

# 한 문단 안에서 토막을 잇는 쉼. **말투마다 다르다.** 참조 음성이 하나면
# 억양은 한 가지로 나오므로, 문장 사이 호흡이 강의에 굴곡을 주는 유일한 수단이
# 된다. 값을 읽는 문장 앞은 벌리고, 툭 던지는 말 앞은 붙인다. 전부 문단 사이
# 쉼(0.45초)보다 짧아야 한 문단으로 들린다.
CHUNK_GAPS = {'slow': 0.30, 'warn': 0.28, 'stress': 0.24, 'ask': 0.22,
              'warm': 0.22, 'calm': 0.20, 'point': 0.20, 'light': 0.14}
CHUNK_GAP = 0.20                # 이름 없는 말투
CHUNK = re.compile(r'^(?P<key>L\d+-\d+-\d+)#(?P<n>\d+)\.wav$')


def chunk_paths(folder, key, count):
    """문단의 토막들을 번호 순서로. 하나라도 없으면 멈춘다 — 조용히 건너뛰면 말이 빠진다."""
    out = []
    for n in range(1, count + 1):
        path = folder / ('%s#%02d.wav' % (key, n))
        if not path.is_file():
            raise SystemExit('토막이 없다: %s' % path)
        out.append(str(path))
    stray = sorted(p.name for p in folder.glob('%s#*.wav' % key)
                   if int(CHUNK.match(p.name).group('n')) > count)
    if stray:
        raise SystemExit('%s 에 남는 토막이 있다(대본이 바뀌었나?): %s' % (key, ', '.join(stray)))
    return out


def sha_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ingest(lesson_dir, source, outroot, voice, tempo, tool_version, lang='ko'):
    lesson = Path(lesson_dir)
    slug = lesson.name
    script = lesson / 'SCRIPT.md'
    jobs, units, order = N.synthesis_plan(str(script))
    input_hash = N.spoken_hash(str(script))

    outdir = Path(N.private_output(outroot)) / slug
    if outdir.exists():
        raise SystemExit('비어 있는 출력 폴더를 써라: %s' % outdir)
    source_dir = outdir / '_source'
    partdir = outdir / '_parts'
    source_dir.mkdir(parents=True)
    partdir.mkdir(parents=True)

    # 토막 → 문단. 쪼개는 함수는 작업 목록을 만들 때와 같은 것이다.
    joined = {}
    for row in tts_jobs.lesson_rows(script, lang):
        key = row['key']
        parts = chunk_paths(Path(source) / slug, key, len(row['chunks']))
        # 쉼은 **뒤에 오는 토막의 말투**로 정한다. 호흡이 그 문장을 끌고 온다.
        gaps = [0.0] + [CHUNK_GAPS.get(c['tone'], CHUNK_GAP) for c in row['chunks'][1:]]
        dest = partdir / ('%s.wav' % key)
        N.concat_wavs(parts, gaps, str(dest), tail=0.0)
        joined[key] = str(dest)
    if sorted(joined) != sorted(k for k, _ in jobs):
        raise SystemExit('문단 목록이 대본과 어긋난다')

    fast = joined if tempo == 1.0 else {
        key: N.change_tempo(path, outdir / '_parts-tempo' / (key + '.wav'), tempo)
        for key, path in joined.items()}

    frames_out, beats_out, clock, source_clock = [], [], 0.0, 0.0
    for seq, (line_no, part, fid) in enumerate(order, 1):
        entries = units[(line_no, part)]
        gaps = [N.LEAD if i == 0 else N.GAP for i in range(len(entries))]
        dest = outdir / ('%s.wav' % fid)
        source_dest = source_dir / ('%s.wav' % fid)
        source_spans, source_dur = N.concat_wavs([joined[k] for k, _ in entries], gaps,
                                                 str(source_dest))
        if tempo == 1.0:
            shutil.copyfile(source_dest, dest)      # 변환이 없으니 같은 소리다
            spans, dur = source_spans, source_dur
        else:
            spans, dur = N.concat_wavs([fast[k] for k, _ in entries],
                                       [g / tempo for g in gaps], str(dest),
                                       tail=N.TAIL / tempo)
        frames_out.append({
            'frame': seq, 'id': fid, 'line': line_no,
            'start': round(clock, 3), 'end': round(clock + dur, 3), 'duration': dur,
            'audio': dest.name, 'audioSha256': sha_of(dest),
            'sourceAudio': source_dest.name, 'sourceAudioSha256': sha_of(source_dest),
            'sourceStart': round(source_clock, 3),
            'sourceEnd': round(source_clock + source_dur, 3), 'sourceDuration': source_dur,
            'units': [{'beat': b, 'start': s, 'end': e, 'sourceStart': sa, 'sourceEnd': se}
                      for (_, b), (s, e), (sa, se) in zip(entries, spans, source_spans)],
        })
        for (_key, beat_idx), (s, e), (sa, se) in zip(entries, spans, source_spans):
            if beat_idx is not None:
                beats_out.append({'frame': seq, 'beat': beat_idx,
                                  'observedStart': round(clock + s, 3),
                                  'observedEnd': round(clock + e, 3),
                                  'sourceObservedStart': round(source_clock + sa, 3),
                                  'sourceObservedEnd': round(source_clock + se, 3)})
        clock += dur
        source_clock += source_dur

    timing = {
        'schemaVersion': 2, 'source': 'synthesised', 'voice': voice, 'rate': 0,
        'tempo': tempo,
        'tempoMethod': ('voice-clone-native' if tempo == 1.0
                        else 'ffmpeg-atempo-per-paragraph'),
        'tempoToolVersion': tool_version,
        'sourceFrameHoldSeconds': N.BASE_FRAME_HOLD,
        'frameHoldSeconds': N.BASE_FRAME_HOLD / tempo,
        'spokenTextSha256': input_hash,
        'note': ('%s 복제 음성으로 문장 토막을 따로 만들고 %.2f초 쉼으로 한 문단으로 이었다. '
                 % (voice, CHUNK_GAP) +
                 '문단 경계는 합친 PCM 을 다시 재서 얻은 실측값이다. 발음과 의미는 별도 검수한다. '
                 '원본 음성과 도구 버전, 해시를 비공개 출력에 함께 보존한다.'),
        'totalSeconds': round(clock, 3), 'sourceTotalSeconds': round(source_clock, 3),
        'frames': frames_out, 'beats': beats_out,
    }
    timing['timingSha256'] = N.timing_identity(timing)
    N.verify_script_hash(str(lesson), timing)
    N.verify_tempo_timing(timing, required=True)

    originals = {name: (lesson / name).read_bytes() if (lesson / name).exists() else None
                 for name in ('narration-timing.json', 'media.local.json')}
    local = json.loads(originals['media.local.json']) if originals['media.local.json'] else {}
    local.update({'narrationDir': str(outdir.resolve()),
                  'frames': {f['id']: str((outdir / f['audio']).resolve()) for f in frames_out},
                  'sourceFrames': {f['id']: str((source_dir / f['sourceAudio']).resolve())
                                   for f in frames_out}})
    from ingest_recording import write_metadata
    write_metadata(lesson.resolve(), {'narration-timing.json': timing,
                                      'media.local.json': local}, originals)
    print('%-34s 프레임 %2d · 비트 %3d · %6.1f초 (%d:%02d)'
          % (slug, len(frames_out), len(beats_out), clock, clock // 60, clock % 60))
    return timing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--in', dest='source', required=True, help='토막 WAV 가 든 폴더')
    ap.add_argument('--out', required=True, help='음성을 둘 곳 (저장소 밖)')
    ap.add_argument('--lesson', default='', help='한 차시만 (예: lesson-02)')
    ap.add_argument('--voice', default=sorted(N.CLONES)[0], choices=sorted(N.CLONES))
    ap.add_argument('--tempo', type=float, default=None, help='기본은 목소리에 정해진 값')
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'),
                    help='토막을 나눈 기준. 영문 사본이면 en')
    a = ap.parse_args(argv)

    tempo = N.TEMPOS[a.voice] if a.tempo is None else a.tempo
    tool_version = None
    if tempo != 1.0:
        ffmpeg = shutil.which('ffmpeg')
        if not ffmpeg:
            raise SystemExit('1.0 이 아닌 배속은 ffmpeg 가 필요하다')
        tool_version = subprocess.run([ffmpeg, '-version'], capture_output=True, text=True,
                                      check=True, timeout=30).stdout.splitlines()[0]
    else:
        tool_version = 'qwen-tts voice clone (no tempo conversion)'

    lessons = [p for p in sorted(tts_jobs.COURSE.glob('lesson-*'))
               if p.is_dir() and (p / 'SCRIPT.md').is_file()
               and (not a.lesson or a.lesson in p.name)]
    if not lessons:
        raise SystemExit('해당하는 차시가 없다')
    total = 0.0
    for lesson in lessons:
        if not (Path(a.source) / lesson.name).is_dir():
            print('%-34s 토막 폴더 없음 — 건너뜀' % lesson.name)
            continue
        total += ingest(str(lesson), a.source, a.out, a.voice, tempo,
                        tool_version, a.lang)['totalSeconds']
    print('합계 %.1f초 (%d:%02d)' % (total, total // 60, total % 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
