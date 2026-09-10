"""국문 차시에서 영문 차시 사본을 만든다 — 저장소 밖에.

영문판은 국문 프레임을 건드리지 않는다. 검수 중인 화면이 흔들리면 안 되기
때문이다. 대신 국문 차시를 통째로 복사한 **비공개 사본** 위에 영문 대본과
영문 글자를 얹고, 기존 파이프라인(narrate_tts · retime_frames · prepare_lecture)
을 그 사본에서 그대로 돌린다.

    python scripts/part/build_english_lesson.py <차시 디렉터리> <나갈 곳>

나갈 곳은 저장소 밖이어야 하고 비어 있어야 한다. 만들고 나면 그 안에서
`SCRIPT.md` 는 영문 대본이고 프레임의 글자는 영문이다. 국문 음성·시각 파일은
가져오지 않는다 — 영문은 자기 음성을 처음부터 잰다.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frame_text  # noqa: E402

HANGUL = re.compile(r'[가-힣]')
# 국문 음성에 매인 것들. 영문 사본은 자기 것을 새로 만든다.
DROP = ('narration-timing.json', 'media.local.json', 'SCRIPT.en.md')
MAPS = Path(__file__).resolve().parent / 'frames_en'

# 표의 설명 칸은 국문에서 「선을 긋는다」처럼 짧아서 줄바꿈을 막아 두었다.
# 영문은 같은 자리가 한 문장이라, 줄바꿈을 막으면 그 칸이 한 줄 전체 너비를
# 차지하고 옆 칸이 100px 남짓으로 찌그러진다. 그러면 옆 칸이 네댓 줄로 접히면서
# 표가 캔버스 밖으로 내려간다 — 3차시 명령표가 724px 자리에서 1470px 이 됐다.
# 그래서 **먹색 설명 칸에서만** 줄바꿈 금지를 푼다. 명령 이름과 치수 값이 들어가는
# 강조색 칸은 짧고 끊기면 안 되므로 그대로 둔다.
WRAP = re.compile(r'(style="color:#111;(?:font-size:\d+px;)?)white-space:nowrap"')

# 명령표는 국문에서 한 줄로 앉는 칸이 영문에서 두 줄이 된다. 17개짜리 표는
# 그것만으로 칸(573px)을 넘긴다. 칸을 줄이려고 문장을 더 깎으면 표가 자동
# 배치라 열 너비가 다시 나뉘면서 다른 행이 대신 두 줄이 된다 — 6차시에서 세 줄
# 짜리 두 행을 없앴는데 전체 높이가 585px 그대로였다. 그래서 글자 크기는
# 건드리지 않고 **행 사이만** 좁힌다. 6px → 3px 로 한 줄에 6px, 열 줄에 60px.
ROW_PADDING = ('table.spec.tight th,table.spec.tight td{padding:6px 8px}',
               'table.spec.tight th,table.spec.tight td{padding:3px 8px}')


def private(path):
    out = Path(path).resolve()
    repo = Path(__file__).resolve().parents[2]
    if repo == out or repo in out.parents:
        raise ValueError('영문 사본은 저장소 밖에 두어야 한다: %s' % out)
    return out


def build(lesson_dir, out_dir):
    lesson = Path(lesson_dir).resolve()
    out = private(out_dir)
    if out.exists():
        raise ValueError('나갈 곳이 이미 있다. 새 폴더를 주어라: %s' % out)
    english_script = lesson / 'SCRIPT.en.md'
    if not english_script.is_file():
        raise ValueError('영문 대본이 없다: %s' % english_script)
    mapping = MAPS / (lesson.name + '.json')
    if not mapping.is_file():
        raise ValueError('프레임 영문 지도가 없다: %s' % mapping)
    english = json.loads(mapping.read_text(encoding='utf-8'))

    shutil.copytree(lesson, out, ignore=shutil.ignore_patterns('_*', '.hyperframes', 'node_modules'))
    for name in DROP:
        target = out / name
        if target.exists():
            target.unlink()
    shutil.copyfile(english_script, out / 'SCRIPT.md')

    missing, left, unwrapped = {}, {}, 0
    for path in frame_text.frames(str(out)):
        source = Path(path).read_text(encoding='utf-8')
        localised, gaps = frame_text.localise(source, english)
        localised = localised.replace('<html lang="ko">', '<html lang="en">')
        localised, hits = WRAP.subn(lambda m: m.group(1).rstrip(';') + '"', localised)
        unwrapped += hits
        localised = localised.replace(*ROW_PADDING)
        Path(path).write_text(localised, encoding='utf-8', newline='\n')
        if gaps:
            missing[os.path.basename(path)] = gaps
        body = frame_text.SCRIPTS.sub('', localised)
        rest = HANGUL.findall(re.sub(r'<svg.*?</svg>', '', body, flags=re.S))
        if rest:
            left[os.path.basename(path)] = len(rest)

    print('영문 사본 %s' % out)
    print('프레임 %d장 · 번역 지도 %d줄 · 설명 칸 줄바꿈 허용 %d곳'
          % (len(frame_text.frames(str(out))), len(english), unwrapped))
    if missing:
        print('바꾸지 못한 글자가 있다:')
        for name, gaps in missing.items():
            for text in gaps[:5]:
                print('   %-24s %s' % (name, text[:70]))
    if left:
        print('한글이 남은 프레임 (도면 SVG 는 제외):')
        for name, count in left.items():
            print('   %-24s %d자' % (name, count))
    return 1 if missing or left else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('lesson')
    ap.add_argument('out')
    a = ap.parse_args(argv)
    return build(a.lesson, a.out)


if __name__ == '__main__':
    sys.exit(main())
