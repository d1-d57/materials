// Скриншоты c8: 390 и 1280 px, светлая и тёмная тема. Запуск: python3 sobrat_c8.py && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node snimki_c8.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/', OUT = __dirname + '/shots/';
const row = n => `document.querySelector('#sim-c8 .c8-row[data-n="${n}"] .c8-hit').dispatchEvent(new MouseEvent('click',{bubbles:true}));`;
const pw = "document.querySelector('#sim-c8 .c8-pw').click();", go = "document.querySelector('#sim-c8 .c8-go').click();";
const SC = [
  ['c8-do', []], ['c8-n6', [[row(6), 0]]], ['c8-stepeni', [[pw, 0]]], ['c8-n6-stepeni', [[row(6) + pw, 0]]],
  ['c8-n0', [[row(0), 0]]], ['c8-shag', [[go, 650]]],
];
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) for (const th of ['light', 'dark']) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}, deviceScaleFactor: w < 500 ? 2 : 1, colorScheme: th});
    const p = await ctx.newPage();
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    for (const [name, steps] of SC) {
      await p.goto('file://' + __dirname + '/preview-c8.html'); await p.waitForTimeout(300);
      const el = await p.$('#sim-c8'); await el.scrollIntoViewIfNeeded();
      for (const [js, wait] of steps) { await p.evaluate(js); await p.waitForTimeout(wait + 150); }
      await el.screenshot({path: `${OUT}${name}-${w}-${th}.png`});
    }
    await ctx.close();
  }
  await b.close(); console.log('готово');
})();
