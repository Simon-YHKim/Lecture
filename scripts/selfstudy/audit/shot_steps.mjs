// 자습 교재에서 코치 마크가 붙은 단계를 하나씩 찍는다.
//
//   node scripts/selfstudy/audit/shot_steps.mjs <쪽.html> <출력폴더> [n …]
//
// 좌표가 맞는지는 눈으로만 알 수 있다. 도면 위 자리를 숫자로 적어 두면 그 숫자가
// 맞는지 확인할 방법이 없고, 틀리면 학습자가 엉뚱한 곳을 클릭한다.
import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';

const [file, outdir, ...want] = process.argv.slice(2);
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1500, height: 1100 }, deviceScaleFactor: 2 });
await pg.goto(pathToFileURL(file).href);
await pg.evaluate(() => {
  const t = [...document.querySelectorAll('[role="tab"]')].find(x => /실습/.test(x.textContent));
  if (t) t.click();
});
await pg.waitForTimeout(300);
const n = await pg.evaluate(() => document.querySelectorAll('li.hasfig').length);
console.log('코치 마크 붙은 단계', n);
const take = want.length ? want.map(Number) : [...Array(n).keys()];
for (const i of take) {
  if (i >= n) continue;
  const li = pg.locator('li.hasfig').nth(i);
  await li.scrollIntoViewIfNeeded();
  await pg.waitForTimeout(120);
  await li.locator('figure.coachfig').screenshot({ path: `${outdir}/step-${i}.png` });
  console.log('찍음', i);
}
await b.close();
