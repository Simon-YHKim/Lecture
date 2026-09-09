// 전 슬라이드를 마지막 조각까지 열어 두 가지를 잰다.
//
//   · 넘침 — 글이 제 상자를 넘어 아래 것 위로 겹쳐 앉는 곳.
//   · 아래 빈 띠 — 내용이 끝난 자리부터 슬라이드 바닥까지의 높이.
//
// 둘 다 눈으로 191장을 넘겨서는 못 찾는다. 마지막 조각에서 재야 한다.
// 중간 조각은 아직 안 나온 것이 있어 원래 비어 있기 때문이다.
import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';

const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1600, height: 900 } });
await pg.goto(pathToFileURL(process.argv[2]).href);
await pg.waitForFunction(() => window.__deckGo && window.__timelines);

const meta = await pg.evaluate(() => {
  const out = [];
  document.querySelectorAll('script[type="application/hyperframes-slideshow+json"]')
    .forEach((s) => JSON.parse(s.textContent).slides
      .forEach((sl) => out.push({ id: sl.sceneId, nf: (sl.fragments || []).length })));
  return out;
});

const rows = [];
for (let n = 0; n < meta.length; n++) {
  await pg.evaluate((k) => window.__deckGo(k), n);
  for (let k = 1; k < meta[n].nf; k++) { await pg.keyboard.press('ArrowRight'); }
  await pg.waitForTimeout(45);
  rows.push(await pg.evaluate((id) => {
    const root = document.getElementById(id + '-root');
    if (!root) return { id, err: '장면 없음' };
    const box = root.getBoundingClientRect();
    const body = root.querySelector('.body') || root;
    const bb = body.getBoundingClientRect();
    let over = 0, worst = '';
    let lowest = bb.top;
    root.querySelectorAll('*').forEach((e) => {
      const c = getComputedStyle(e);
      if (c.display === 'none' || parseFloat(c.opacity) < 0.05) return;
      const r = e.getBoundingClientRect();
      if (r.height > 0 && r.bottom > lowest) lowest = r.bottom;
      // 스크롤이 없는 상자에서 내용이 상자보다 크면 밖으로 삐져나온다.
      if (c.overflow === 'visible' && e.scrollHeight > e.clientHeight + 2
          && e.clientHeight > 0 && /card|cc|cp|op|note|sc/.test(e.className || '')) {
        const d = e.scrollHeight - e.clientHeight;
        if (d > over) { over = d; worst = String(e.className).slice(0, 18); }
      }
    });
    return { id, over, worst,
             gap: Math.round(bb.bottom - lowest),
             h: Math.round(bb.height) };
  }, meta[n].id));
}
await b.close();

const bad = rows.filter((r) => r.over > 4).sort((a, b2) => b2.over - a.over);
console.log('=== 글이 상자를 넘는 곳 ===');
bad.slice(0, 20).forEach((r, i) => console.log('  ' + (rows.indexOf(r) + 1) + ' ' + r.id
  + '  +' + r.over + 'px  ' + r.worst));
console.log('  합계 ' + bad.length + '장');

const gapy = rows.filter((r) => r.gap > r.h * 0.12).sort((a, b2) => b2.gap - a.gap);
console.log('\n=== 아래가 12% 넘게 비는 곳 ===');
gapy.slice(0, 24).forEach((r) => console.log('  ' + (rows.indexOf(r) + 1) + ' ' + r.id
  + '  빈 띠 ' + r.gap + 'px / 본문 ' + r.h + 'px'));
console.log('  합계 ' + gapy.length + '장 / ' + rows.length + '장');
