"""강의 프레임의 상자 크기를 실제 브라우저로 재기 위한 측정 쪽을 만든다.

프레임 본문은 `<template>` 안에 들어 있고 HyperFrames 런타임이 재생할 때 꺼내
붙인다. 그래서 파일을 그냥 열면 아무것도 안 보이고 크기도 못 잰다. 이 쪽은
`fetch` 로 프레임을 읽어 `<template>` 을 직접 복제해 붙이므로, 국문 원본과 영문
사본을 같은 조건에서 나란히 잴 수 있다.

넘침을 눈이 아니라 숫자로 봐야 하는 이유가 있다. `.clip` 은 `overflow:hidden`
이라 넘친 부분이 그냥 잘려 나가고, 잘린 화면은 "원래 그런 그림" 처럼 보인다.
1080 캔버스에서 아래 여백 64 를 뺀 **1016** 이 한계선이다.

    python scripts/part/frame_sheet.py <잴 폴더> --en <영문 사본 루트>
    cd <잴 폴더> && python -m http.server 8731 --bind 127.0.0.1
    # 브라우저에서 http://127.0.0.1:8731/measure.html 를 열고
    # window.measure('/ko/<차시>/<프레임>.html') 를 부른다. 반환값의 boxes 를 본다.

`--en` 을 주면 `build_english_lesson.py` 가 만든 사본들의 프레임도 함께 복사해
`/en/<차시>/<프레임>.html` 로 놓는다. 국문은 늘 `/ko/...` 다.
"""
import argparse
import json
import shutil
from pathlib import Path

COURSE = Path('projects/autocad-technician')
LIMIT = 1016  # 1080 캔버스에서 .clip 의 아래 여백 64 를 뺀 값

PAGE = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>frame box measure</title>
<style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden}</style>
</head><body>
<script>
// 프레임은 <template> 안에 있다. 런타임 대신 여기서 복제해 붙인다. GSAP 은
// opacity 와 transform 만 움직이므로 상자 크기에는 영향을 주지 않는다.
window.measure = async function (src) {
  const html = await (await fetch(src)).text();
  const doc = new DOMParser().parseFromString(html, 'text/html');
  document.body.innerHTML = '';
  document.body.appendChild(document.importNode(doc.querySelector('template').content, true));
  await document.fonts.ready;
  const boxes = [];
  for (const sel of ['.clip', '.body', '.body > section', '.panel', '.card', 'table', 'tr']) {
    for (const el of document.querySelectorAll(sel)) {
      const r = el.getBoundingClientRect();
      boxes.push({ sel: sel, cls: String(el.className).slice(0, 40),
                   top: Math.round(r.top * 100) / 100,
                   bottom: Math.round(r.bottom * 100) / 100,
                   height: Math.round(r.height * 100) / 100 });
    }
  }
  const deepest = Math.max(0, ...boxes.filter(b => b.sel !== '.clip').map(b => b.bottom));
  return { src: src, limit: LIMIT_PLACEHOLDER, bottom: Math.round(deepest * 100) / 100,
           over: deepest > LIMIT_PLACEHOLDER, boxes: boxes };
};
// frames.json 의 모든 프레임을 한 번에 재고 넘친 것만 돌려준다.
window.measureAll = async function () {
  const list = await (await fetch('/frames.json')).json();
  const rows = [];
  for (const row of list) {
    const one = async (root) => {
      try { return (await window.measure('/' + root + '/' + row.lesson + '/' + row.frame)).bottom; }
      catch (e) { return null; }
    };
    rows.push({ lesson: row.lesson, frame: row.frame, ko: await one('ko'), en: await one('en') });
  }
  return { frames: rows.length, over: rows.filter(r => Math.max(r.ko || 0, r.en || 0) > LIMIT_PLACEHOLDER), rows: rows };
};
</script>
</body></html>
'''


def collect(out, english=None):
    out = Path(out).resolve()
    if out.exists():
        shutil.rmtree(out)
    rows = []
    for lesson in sorted(COURSE.glob('lesson-*/compositions/frames')):
        name = lesson.parents[1].name
        for frame in sorted(lesson.glob('*.html')):
            dest = out / 'ko' / name / frame.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(frame, dest)
            rows.append({'lesson': name, 'frame': frame.name})
    if english:
        for lesson in sorted(Path(english).glob('*/compositions/frames')):
            name = lesson.parents[1].name
            for frame in sorted(lesson.glob('*.html')):
                dest = out / 'en' / name / frame.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(frame, dest)
    (out / 'frames.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n',
                                     encoding='utf-8', newline='\n')
    (out / 'measure.html').write_text(PAGE.replace('LIMIT_PLACEHOLDER', str(LIMIT)),
                                      encoding='utf-8', newline='\n')
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('out')
    ap.add_argument('--en', help='build_english_lesson.py 사본들이 모인 폴더')
    a = ap.parse_args(argv)
    rows = collect(a.out, a.en)
    print('프레임 %d장 · 한계선 %dpx · %s' % (len(rows), LIMIT, a.out))
    print('cd %s && python -m http.server 8731 --bind 127.0.0.1' % a.out)
    print('브라우저에서 measure.html 을 열고 await measureAll() 를 부른다')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
