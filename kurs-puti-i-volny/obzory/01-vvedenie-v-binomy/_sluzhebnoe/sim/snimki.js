// Скриншоты preview.html: 390 и 1280 px, светлая и тёмная тема, до и после ключевых кнопок.
// Запуск: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node snimki.js [фильтр-имени]  → shots/*.png
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/', OUT = __dirname + '/shots/', ONLY = process.argv[2] || '';
const set = (id, c, v) => `(()=>{const e=document.querySelector('#sim-${id} .${c}');e.value=${v};e.dispatchEvent(new Event('input'));})();`;
const click = sel => `document.querySelector('${sel}').click();`;
const tap = sel => `document.querySelector('${sel}').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));`;
// [имя, sim, шаги [[js, ждать мс], ...]]
const SC = [
  ['c0-do', 'c0', []], ['c0-n6k3', 'c0', [[set('c0', 'c0-n', 6) + set('c0', 'c0-k', 3), 900]]],
  ['c0-n3k0', 'c0', [[set('c0', 'c0-n', 3) + set('c0', 'c0-k', 0), 600]]],
  ['c0-navedenie', 'c0', [[tap('#sim-c0 .c0-row[data-i="1"]'), 0]]],
  ['c0-n6k3-navedenie', 'c0', [[set('c0', 'c0-n', 6) + set('c0', 'c0-k', 3), 900], [tap('#sim-c0 .c0-row[data-i="13"]'), 0]]],
  ['c0-n3k0-navedenie', 'c0', [[set('c0', 'c0-n', 3) + set('c0', 'c0-k', 0), 600], [tap('#sim-c0 .c0-row[data-i="0"]'), 0]]],
  ['c0-poyavlenie', 'c0', [[set('c0', 'c0-n', 5) + set('c0', 'c0-k', 2), 180]]],
  ['c1-do', 'c1', []], ['c1-navedenie', 'c1', [[tap('#sim-c1 .w-word[data-side=L][data-i="2"]'), 0]]],
  ['c1-polet', 'c1', [[click('#sim-c1 .c1-go'), 1000]]], ['c1-otrazheno', 'c1', [[click('#sim-c1 .c1-go'), 2300]]],
  ['c1-otrazheno-navedenie', 'c1', [[click('#sim-c1 .c1-go'), 2300], [tap('#sim-c1 .w-word[data-side=L][data-i="3"]'), 0]]],
  ['c1-n6k3', 'c1', [[set('c1', 'c1-n', 6) + set('c1', 'c1-k', 3) + tap('#sim-c1 .w-word[data-side=L][data-i="4"]'), 0]]],
  ['c1-n6k3-otrazheno', 'c1', [[set('c1', 'c1-n', 6) + set('c1', 'c1-k', 3) + click('#sim-c1 .c1-go'), 2600]]],
  ['c2-do', 'c2', []], ['c2-razezd', 'c2', [[click('#sim-c2 .c2-go'), 1300]]], ['c2-hvosty', 'c2', [[click('#sim-c2 .c2-go'), 3000]]],
  ['c2-n4k2-hvosty', 'c2', [[set('c2', 'c2-n', 4) + set('c2', 'c2-k', 2) + click('#sim-c2 .c2-go'), 3000]]],
  ['c3-kapitan', 'c3', []], ['c3-ryadovye', 'c3', [[click('#sim-c3 .c3-b[data-m="2"]'), 1800]]], ['c3-komanda', 'c3', [[click('#sim-c3 .c3-b[data-m="1"]'), 1800]]],
  ['c3-perehod', 'c3', [[click('#sim-c3 .c3-b[data-m="1"]'), 300]]],
  ['c3-perehod-vverh', 'c3', [[click('#sim-c3 .c3-b[data-m="1"]'), 1800], [click('#sim-c3 .c3-b[data-m="0"]'), 250]]],
  ['c3-n5m3-ryadovye', 'c3', [[set('c3', 'c3-n', 5) + set('c3', 'c3-m', 3) + click('#sim-c3 .c3-b[data-m="2"]'), 1800]]],
  ['c4-strelki', 'c4', []], ['c4-vershina', 'c4', [[set('c4', 'c4-n', 7) + tap('#sim-c4 .c4-hit[data-v="1"]'), 0]]],
  ['c4-skleika', 'c4', [[set('c4', 'c4-n', 7) + click('#sim-c4 .c4-go'), 800]]], ['c4-otrezki', 'c4', [[set('c4', 'c4-n', 7) + click('#sim-c4 .c4-go'), 2000]]],
  ['c4-n10', 'c4', [[set('c4', 'c4-n', 10), 0]]],
  ['c5-do', 'c5', []], ['c5-navedenie', 'c5', [[tap('#sim-c5 .c5-up[data-q="5"]'), 0]]],
  ['c5-polet', 'c5', [[click('#sim-c5 .c5-go'), 800]]], ['c5-otrazheno', 'c5', [[click('#sim-c5 .c5-go'), 1900]]],
  ['c5-otrazheno-navedenie', 'c5', [[click('#sim-c5 .c5-go'), 1900], [tap('#sim-c5 .c5-dn[data-q="5"]'), 0]]],
  ['c5-sdvig', 'c5', [[click('#sim-c5 .c5-go'), 1900], [click('#sim-c5 .c5-sh'), 600]]],
  ['c5-pryamougolnik', 'c5', [[click('#sim-c5 .c5-go'), 1900], [click('#sim-c5 .c5-sh'), 1500]]],
  ['c5-n8-pryamougolnik', 'c5', [[set('c5', 'c5-n', 8) + click('#sim-c5 .c5-go'), 1900], [click('#sim-c5 .c5-sh'), 1500]]],
  ['c5-n2-otrazheno', 'c5', [[set('c5', 'c5-n', 2) + click('#sim-c5 .c5-go'), 1900]]],
];
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) for (const th of ['light', 'dark']) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}, deviceScaleFactor: w < 500 ? 2 : 1, colorScheme: th});
    const p = await ctx.newPage();
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    const load = async () => { await p.goto('file://' + __dirname + '/preview.html'); await p.waitForTimeout(300); };
    if (!ONLY) { await load(); await p.screenshot({path: `${OUT}stranica-${w}-${th}.png`, fullPage: true}); }
    for (const [name, sim, steps] of SC) {
      if (ONLY && !name.startsWith(ONLY)) continue;
      await load(); const el = await p.$('#sim-' + sim); await el.scrollIntoViewIfNeeded();
      for (const [js, wait] of steps) { await p.evaluate(js); await p.waitForTimeout(wait + 150); }
      if (!steps.length) await p.waitForTimeout(150);
      await el.screenshot({path: `${OUT}${name}-${w}-${th}.png`});
    }
    await ctx.close();
  }
  await b.close(); console.log('готово');
})();
