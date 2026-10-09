// Скриншоты c7: 390 и 1280 px, светлая и тёмная тема. Запуск: python3 sobrat_c7.py && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node snimki_c7.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/', OUT = __dirname + '/shots/';
const cell = (n, k) => `document.querySelector('#sim-c7 .c7-cell[data-n="${n}"][data-k="${k}"] .c7-hit').dispatchEvent(new MouseEvent('click',{bubbles:true}));`;
const dir = d => `document.querySelector('#sim-c7 .c7-b[data-d="${d}"]').click();`;
const SC = [
  ['c7-do', []], ['c7-vpravo', [[dir(1), 0]]], ['c7-vverh-vlevo', [[dir(2), 0]]], ['c7-vverh-vpravo', [[dir(3), 0]]],
  ['c7-vse', [[dir(4), 0]]], ['c7-n8k1', [[cell(8, 1), 0]]], ['c7-n8k1-vse', [[cell(8, 1) + dir(4), 0]]],
  ['c7-n8k4-vse', [[cell(8, 4) + dir(4), 0]]], ['c7-n8k0-vpravo', [[cell(8, 0) + dir(1), 0]]],
  ['c7-kray', [[cell(5, 0), 0]]], ['c7-shag', [[dir(4) + "document.querySelector('#sim-c7 .c7-go').click();", 900]]],
];
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) for (const th of ['light', 'dark']) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}, deviceScaleFactor: w < 500 ? 2 : 1, colorScheme: th});
    const p = await ctx.newPage();
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    for (const [name, steps] of SC) {
      await p.goto('file://' + __dirname + '/preview-c7.html'); await p.waitForTimeout(300);
      const el = await p.$('#sim-c7'); await el.scrollIntoViewIfNeeded();
      for (const [js, wait] of steps) { await p.evaluate(js); await p.waitForTimeout(wait + 150); }
      await el.screenshot({path: `${OUT}${name}-${w}-${th}.png`});
    }
    await ctx.close();
  }
  await b.close(); console.log('готово');
})();
