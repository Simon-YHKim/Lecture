import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';
const [file, ...rest] = process.argv.slice(2);
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1600, height: 900 } });
await pg.goto(pathToFileURL(file).href, { timeout: 180000 });
await pg.waitForFunction(() => window.__deckGo && window.__timelines, null, { timeout: 180000 });
for (const spec of rest) {
  const [n, k] = spec.split(':').map(Number);
  await pg.evaluate((i) => window.__deckGo(i - 1), n);
  // k 를 안 주면 그 장의 마지막 조각까지 간다. 다음 장으로 넘어가면 되돌린다.
  const limit = k || 40;
  for (let j = 1; j < limit; j++) {
    const before = await pg.evaluate(() => document.getElementById('pos').textContent);
    await pg.keyboard.press('ArrowRight');
    await pg.waitForTimeout(60);
    const after = await pg.evaluate(() => document.getElementById('pos').textContent);
    if (after !== before) { await pg.keyboard.press('ArrowLeft'); await pg.waitForTimeout(60); break; }
  }
  await pg.waitForTimeout(250);
  console.log('  상태 ' + await pg.evaluate(() => {
    const sc = Array.from(document.querySelectorAll('[data-composition-id]'))
      .find((e) => e.getBoundingClientRect().width > 0);
    const o = Array.from(sc.querySelectorAll('.cc,.cp,.cfig,.nn'))
      .map((e) => getComputedStyle(e).opacity.slice(0, 3)).join(',');
    const p = sc.querySelector('.cp');
    return document.getElementById('pos').textContent + ' 투명도[' + o + ']'
      + (p ? ' 첫문단y=' + Math.round(p.getBoundingClientRect().top) : '');
  }));
  await pg.screenshot({ path: 'v2-' + n + (k ? '-' + k : '') + '.png' });
  console.log('찍음 ' + spec);
}
await b.close();
