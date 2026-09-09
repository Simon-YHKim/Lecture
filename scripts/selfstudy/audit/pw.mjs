// Playwright 를 어디에 깔았든 찾아 준다.
//
// 검사 스크립트가 브라우저를 띄우려면 playwright 가 필요한데, 이 저장소에는
// node_modules 가 없다. 경로를 적어 두면 그 컴퓨터의 사용자 폴더가 공개
// 저장소에 남는다 — private-materials-guard 가 막는 것이 바로 그것이다.
// 그래서 실행할 때 찾는다.
//
//   1. PLAYWRIGHT_PKG 로 지정한 곳
//   2. 이 저장소 안 node_modules
//   3. npm 전역 설치 위치 (npm root -g)
import { createRequire } from 'module';
import { execSync } from 'child_process';

const require = createRequire(import.meta.url);

function load() {
  const tried = [];
  for (const where of [process.env.PLAYWRIGHT_PKG, 'playwright']) {
    if (!where) continue;
    try {
      return require(where);
    } catch (e) {
      tried.push(where);
    }
  }
  try {
    const root = execSync('npm root -g', { encoding: 'utf8' }).trim();
    return require(root.replace(/\\/g, '/') + '/playwright');
  } catch (e) {
    tried.push('npm root -g');
  }
  throw new Error(
    'playwright 를 못 찾았습니다. 찾아본 곳: ' + tried.join(', ') + '\n'
    + '  npm i -g playwright  하거나  PLAYWRIGHT_PKG=<경로> 로 알려 주세요.');
}

export const { chromium } = load();
