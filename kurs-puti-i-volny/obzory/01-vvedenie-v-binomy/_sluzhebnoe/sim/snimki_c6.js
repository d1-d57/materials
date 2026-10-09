// Скриншоты c6 (preview-c6.html): 390 и 1280 px, светлая и тёмная тема → shots/c6-*.png
// Запуск: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node snimki_c6.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/', OUT = __dirname + '/shots/';
const setN = v => `(()=>{const e=document.querySelector('#sim-c6 .c6-n');e.value=${v};e.dispatchEvent(new Event('input'));})();`;
const click = sel => `document.querySelector('${sel}').click();`;
const SC = [
  ['c6-do', []],
  ['c6-n8-vse', [[setN(8) + click('#sim-c6 .c6-all'), 0]]],
  ['c6-n8-pusto', [[setN(8) + click('#sim-c6 .c6-clr'), 0]]],
  ['c6-n1', [[setN(1), 0]]],
  ['c6-plus1-vspyshka', [[click('#sim-c6 .c6-inc') + click('#sim-c6 .c6-inc'), 120]]],
  ['c6-fokus', [[`document.querySelector('#sim-c6 .c6-b[data-p=dg][data-i="3"]').focus();`, 0]]],
];
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) for (const th of ['light', 'dark']) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}, deviceScaleFactor: w < 500 ? 2 : 1, colorScheme: th});
    const p = await ctx.newPage();
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    for (const [name, steps] of SC) {
      await p.goto('file://' + __dirname + '/preview-c6.html'); await p.waitForTimeout(300);
      const el = await p.$('#sim-c6'); await el.scrollIntoViewIfNeeded();
      for (const [js, wait] of steps) { await p.evaluate(js); await p.waitForTimeout(wait); }
      if (name === 'c6-fokus') await p.keyboard.press('Shift+Tab'), await p.keyboard.press('Tab');
      await p.waitForTimeout(name.includes('vspyshka') ? 0 : 150);
      await el.screenshot({path: `${OUT}${name}-${w}-${th}.png`});
    }
    await ctx.close();
  }
  await b.close(); console.log('готово');
})();
