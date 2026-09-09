// 191장을 전부 넘겨 보며 두 가지를 센다.
//
//   · 다음을 눌렀는데 화면이 그대로인 구간 — 조각은 있는데 움직임이 없는 곳.
//   · 발표자 노트가 비어 있는 장.
//
// 사람이 191장을 눌러 보는 대신 브라우저에게 시킨다. 판정은 눈이 아니라
// 계산된 스타일이다: 투명도·변형·색·글자를 모아 지문을 만들고, 앞 조각과
// 같으면 「안 변함」으로 센다.
import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';

const FILE = process.argv[2];
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = [];
pg.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)); });
pg.on('pageerror', (e) => errs.push('PAGEERROR ' + String(e).slice(0, 160)));
await pg.goto(pathToFileURL(FILE).href);
await pg.waitForFunction(() => window.__deckGo && window.__timelines);

const meta = await pg.evaluate(() => {
  const out = [];
  document.querySelectorAll('script[type="application/hyperframes-slideshow+json"]')
    .forEach((s) => JSON.parse(s.textContent).slides.forEach((sl) => out.push({
      id: sl.sceneId, nf: (sl.fragments || []).length, notes: (sl.notes || '').trim(),
    })));
  return out;
});

async function sign() {
  return pg.evaluate(() => {
    const sc = Array.from(document.querySelectorAll('[data-composition-id]'))
      .find((e) => e.getBoundingClientRect().width > 0);
    if (!sc) return 'none';
    let s = '';
    sc.querySelectorAll('*').forEach((e) => {
      const c = getComputedStyle(e);
      if (c.display === 'none') return;
      s += c.opacity + '|' + c.transform + '|' + c.color + '|' + c.stroke + '|' + c.fill + ';';
    });
    let h = 0;
    for (let i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) | 0; }
    return h + ':' + s.length;
  });
}

const dead = [], nonote = [], noanim = [];
for (let n = 0; n < meta.length; n++) {
  const m = meta[n];
  if (!m.notes || m.notes === '—') nonote.push([n + 1, m.id]);
  await pg.evaluate((k) => window.__deckGo(k), n);
  await pg.waitForTimeout(30);
  let prev = await sign(), same = 0;
  for (let k = 1; k < Math.max(1, m.nf); k++) {
    await pg.keyboard.press('ArrowRight');
    await pg.waitForTimeout(30);
    const cur = await sign();
    if (cur === prev) same++;
    prev = cur;
  }
  if (m.nf > 1 && same) dead.push([n + 1, m.id, m.nf, same]);
  if (m.nf <= 1) noanim.push([n + 1, m.id]);
}

const pad = (x, w) => String(x).padStart(w);
console.log('=== 다음을 눌러도 안 변하는 구간 ===');
dead.forEach(([n, id, nf, s]) => console.log('  ' + pad(n, 3) + '  ' + id.padEnd(11) + ' 조각 ' + pad(nf, 2) + ' 중 ' + pad(s, 2) + ' 구간 정지'));
console.log('  합계 ' + dead.length + '장 / 조각 있는 ' + meta.filter((m) => m.nf > 1).length + '장');
console.log('\n=== 조각이 하나뿐(넘길 것이 없음) ===');
console.log('  ' + noanim.map(([n, id]) => n + ' ' + id).join(' · '));
console.log('\n=== 노트 빈 장 ===');
console.log('  ' + (nonote.length ? nonote.map(([n, id]) => n + ' ' + id).join(' · ') : '없음'));
console.log('\n=== 콘솔 오류 ' + errs.length + '건 ===');
Array.from(new Set(errs)).slice(0, 12).forEach((e) => console.log('  ' + e));
await b.close();
