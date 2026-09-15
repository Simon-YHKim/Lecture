# -*- coding: utf-8 -*-
"""이미 만든 토막의 무음을 다시 걷어낸다. 모델은 부르지 않는다.

앞뒤 무음을 걷던 문턱이 최대 진폭 기준이라 잡음 바닥을 소리로 셌다. 그래서
앞에 10.5초 무음이 붙은 토막이 그대로 통과했다. **말은 정상이고 무음만
문제이므로 다시 만들 필요가 없다** — 파일을 다시 다듬고 `done.jsonl` 의 길이를
고치면 된다. 1,184토막을 다시 생성하면 네 시간, 다시 다듬으면 1분이다.

    python scripts/part/retrim_clone.py --work local-materials/qwen-narration --lang ko
    python scripts/part/retrim_clone.py --work ... --lang ko --dry

`done.jsonl` 은 덧붙이기 파일이라 고쳐 쓰지 않고 **새 줄을 덧붙인다** —
`load_done` 이 같은 열쇠의 나중 줄로 덮으므로 마지막 값이 이긴다. 옛 값이
남아 있어야 무엇이 어떻게 바뀌었는지 나중에 볼 수 있다.
"""
import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import speak_clone as S


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--work', required=True)
    ap.add_argument('--lang', default='ko', choices=('ko', 'en'))
    ap.add_argument('--dry', action='store_true', help='고치지 않고 무엇이 바뀔지만 본다')
    a = ap.parse_args(argv)

    import numpy as np
    import soundfile as sf

    outdir = Path(a.work) / 'out' / a.lang
    donefile = outdir / 'done.jsonl'
    done = S.load_done(str(donefile))
    if not done:
        raise SystemExit('만든 토막이 없다: %s' % donefile)

    changed, gone, rows = [], 0.0, []
    for (slug, key, n), row in sorted(done.items()):
        path = outdir / slug / ('%s#%02d.wav' % (key, n))
        if not path.is_file():
            continue
        audio, sr = sf.read(str(path), dtype='float32', always_2d=False)
        fixed = S.trim(audio, sr)
        before, after = len(audio) / float(sr), len(fixed) / float(sr)
        if before - after < 0.05:               # 0.05초 미만은 잡음이다
            continue
        changed.append((slug, key, n, before, after, row['chars']))
        gone += before - after
        if not a.dry:
            sf.write(str(path), np.asarray(fixed, dtype=np.float32), sr, subtype='PCM_16')
            rows.append(dict(row, sec=round(after, 3), retrimmed=round(before, 3),
                             ok=None, at=time.strftime('%Y-%m-%d %H:%M:%S')))

    if rows:
        # 대역은 새 길이로 다시 본다. 실측 속도도 새 길이에서 나와야 한다.
        merged = dict(done)
        for r in rows:
            merged[(r['slug'], r['key'], r['n'])] = r
        rate, samples = S.measured_rate({k: v for k, v in merged.items() if v.get('ok')},
                                        S.RATE[a.lang])
        low, high = S.BAND
        for r in rows:
            want = r['chars'] / rate
            r['ok'] = low * want <= r['sec'] <= high * want
        with io.open(donefile, 'a', encoding='utf-8') as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + '\n')
        print('속도 %.2f자/초 (표본 %d) · done.jsonl 에 %d줄 덧붙였다'
              % (rate, samples, len(rows)))

    print('%s다듬은 토막 %d / %d · 걷어낸 무음 %.1f초 (%.1f분)'
          % ('[미적용] ' if a.dry else '', len(changed), len(done), gone, gone / 60))
    for slug, key, n, before, after, chars in sorted(changed, key=lambda x: x[3] - x[4],
                                                     reverse=True)[:12]:
        print('   %-30s %-12s#%02d  %5.1f → %5.1f초 · %3d자 → %.2f자/초'
              % (slug[:28], key, n, before, after, chars, chars / after if after else 0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
