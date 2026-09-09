// 실제로 보이는 장면이 아니라 이름으로 집는다. 데크는 장면을 겹쳐 두고
// 투명도로만 가리므로, 「폭이 0이 아닌 첫 장면」은 엉뚱한 장을 집을 수 있다.
import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1600, height: 900 } });
await pg.goto(pathToFileURL(process.argv[2]).href);
await pg.waitForFunction(() => window.__deckGo && window.__timelines);
const n = Number(process.argv[3]);
await pg.evaluate((i) => window.__deckGo(i - 1), n);
for (let j = 1; j < Number(process.argv[4] || 1); j++) { await pg.keyboard.press('ArrowRight'); await pg.waitForTimeout(40); }
await pg.waitForTimeout(250);
console.log(await pg.evaluate(() => {
  const lab = document.getElementById('lab').textContent;
  const sc = Array.from(document.querySelectorAll('[data-composition-id]'))
    .filter((e) => e.getBoundingClientRect().width > 0);
  const out = ['보이는 장면 후보 ' + sc.length + '개 · 제목 ' + lab];
  const walk = (e, d) => {
    const c = getComputedStyle(e), r = e.getBoundingClientRect();
    out.push('  '.repeat(d) + e.tagName.toLowerCase() + '.' + String(e.className || '').slice(0, 24)
      + ' [' + c.display + ' op=' + c.opacity + ']'
      + ' y=' + Math.round(r.top) + '..' + Math.round(r.bottom));
    if (d < 2) Array.from(e.children).forEach((k) => walk(k, d + 1));
  };
  sc.forEach((s) => {
    out.push('— ' + s.getAttribute('data-composition-id') + ' op=' + getComputedStyle(s).opacity
      + ' vis=' + getComputedStyle(s).visibility);
  });
  const want = sc.find((s) => (s.getAttribute('data-label') || '') === lab) || sc[0];
  out.push('== ' + want.getAttribute('data-composition-id'));
  walk(want.querySelector('.clip') || want, 0);
  return out.join('\n');
}));
await b.close();
