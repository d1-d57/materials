// Проверка c6 «подмножество ↔ слово» (Playwright) на preview-c6.html.
// Для каждого n = 1..8 обходим ВСЕ 2^n слов нажатиями «+1» и сверяем кружки, цифры, веса и вывод.
// Запуск: python3 sobrat_c6.py && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node proverka_c6.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/';
const URL = 'file://' + __dirname + '/preview-c6.html';
const expect = (n, v) => {
  const bits = [], set = [], pv = [];
  for (let i = 0; i < n; i++) { const p = 2 ** (n - 1 - i); pv.push(String(p)); const b = Math.floor(v / p) % 2; bits.push(b); if (b) set.push(i + 1); }
  return {bits, pv, w: bits.join(''), set: set.length ? '{' + set.join(', ') + '}' : '∅', k: String(set.length), num: String(v), idx: String(v)};
};
const fromSet = (n, items) => items.reduce((s, i) => s + 2 ** (n - i), 0);
(async () => {
  const b = await chromium.launch(), bad = []; let ok = 0;
  const chk = (c, m) => { if (c) ok++; else if (bad.push(m) < 40) console.log('ПРОВАЛ', m); };
  for (const width of [390, 1280]) {
    const ctx = await b.newContext({viewport: {width, height: 900}, hasTouch: width < 500, isMobile: width < 500, reducedMotion: 'reduce'});
    const p = await ctx.newPage(), errs = [];
    p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    await p.goto(URL); await p.waitForTimeout(300);
    const st = () => p.evaluate(() => {
      const R = document.getElementById('sim-c6'), q = s => R.querySelector(s), t = s => (q(s) || {}).textContent;
      const cols = [...R.querySelectorAll('.c6-col')];
      return {n: +q('.c6-n').value, nv: t('.c6-nv'), cols: cols.length,
        on: cols.map(c => c.classList.contains('on') ? 1 : 0),
        dg: cols.map(c => c.querySelector('.c6-dg').textContent).join(''),
        lab: cols.map(c => c.querySelector('.c6-itl').textContent).join(','),
        pv: cols.map(c => c.querySelector('.c6-pv').textContent),
        pressed: cols.map(c => c.querySelector('[data-p=it]').getAttribute('aria-pressed') === 'true' ? 1 : 0),
        set: t('.c6-set'), k: t('.c6-k'), w: t('.c6-w'), num: t('.c6-num'), idx: t('.c6-idx'), out: t('.sim-out').replace(/\u00a0/g, ' '),
        sw: document.documentElement.scrollWidth, vw: document.documentElement.clientWidth};
    });
    const same = (s, n, v, tag) => {
      const e = expect(n, v), m = width + ' n=' + n + ' v=' + v + ' ' + tag + ': ';
      const good = s.cols === n && s.on.join('') === e.w && s.pressed.join('') === e.w && s.dg === e.w && s.w === e.w &&
        s.pv.join() === e.pv.join() && s.set === e.set && s.k === e.k && s.num === e.num && s.idx === e.idx &&
        s.lab === Array.from({length: n}, (_, i) => i + 1).join(',') && s.out.includes('0…' + (2 ** n - 1));
      chk(good, m + JSON.stringify({got: [s.on.join(''), s.dg, s.w, s.set, s.k, s.num, s.idx], want: [e.w, e.set, e.k, e.num]}));
    };
    const setN = n => p.evaluate(n => { const e = document.querySelector('#sim-c6 .c6-n'); e.value = n; e.dispatchEvent(new Event('input')); }, n);
    const press = sel => width < 500 ? p.tap(sel) : p.click(sel);
    // 0. исходное состояние: n = 6, {1, 3, 5}, 101010 = 42
    let s = await st();
    chk(s.n === 6 && s.nv === '6', width + ' по умолчанию n=6'); same(s, 6, 42, 'по умолчанию');
    chk(s.out.includes('32 + 8 + 2 = 42'), width + ' сумма 32 + 8 + 2 = 42 в выводе');
    chk(s.sw <= s.vw, width + ' гориз. прокрутка по умолчанию ' + s.sw + '>' + s.vw);
    // 1. полный обход: для каждого n — «очистить», затем 2^n раз «+1» с проверкой каждого слова
    for (let n = 1; n <= 8; n++) {
      await setN(n); await press('#sim-c6 .c6-clr');
      const N = 2 ** n;
      for (let v = 0; v < N; v++) {
        s = await st(); same(s, n, v, '+1');
        if (v === 0) { chk(s.out.includes('числа 0'), width + ' n=' + n + ' «числа 0»'); chk(s.set === '∅', width + ' n=' + n + ' пустой набор ∅'); }
        await press('#sim-c6 .c6-inc');
      }
      s = await st(); same(s, n, 0, 'обёртка 2^n−1 → 0 по +1');
      await press('#sim-c6 .c6-dec'); s = await st(); same(s, n, N - 1, 'обёртка 0 → 2^n−1 по −1');
      await press('#sim-c6 .c6-dec'); s = await st(); same(s, n, (N - 2 + N) % N, '−1 ещё раз');
      await press('#sim-c6 .c6-all'); s = await st(); same(s, n, N - 1, '«все»');
      await press('#sim-c6 .c6-clr'); s = await st(); same(s, n, 0, '«очистить»');
      // нажатие на цифру переключает кружок, нажатие на кружок — цифру; повторное — возвращает
      for (let i = 0; i < n; i++) {
        const bit = 2 ** (n - 1 - i);
        await press('#sim-c6 .c6-b[data-p=dg][data-i="' + i + '"]'); s = await st(); same(s, n, bit, 'цифра ' + (i + 1) + ' вкл');
        await press('#sim-c6 .c6-b[data-p=it][data-i="' + i + '"]'); s = await st(); same(s, n, 0, 'кружок ' + (i + 1) + ' выкл');
        await press('#sim-c6 .c6-b[data-p=it][data-i="' + i + '"]'); s = await st(); same(s, n, bit, 'кружок ' + (i + 1) + ' вкл');
        await press('#sim-c6 .c6-b[data-p=dg][data-i="' + i + '"]'); s = await st(); same(s, n, 0, 'цифра ' + (i + 1) + ' выкл');
      }
      chk(s.sw <= s.vw, width + ' n=' + n + ' гориз. прокрутка ' + s.sw + '>' + s.vw);
      // размер зон касания: не меньше 32 px по обеим осям
      const hit = await p.evaluate(() => [...document.querySelectorAll('#sim-c6 .c6-b')].map(g => { const r = g.getBoundingClientRect(); return Math.min(r.width, r.height); }));
      chk(Math.min(...hit) >= 32, width + ' n=' + n + ' зона касания ' + Math.min(...hit).toFixed(1) + ' < 32');
    }
    // 2. клавиатура: Enter и пробел на кружке и на цифре
    await setN(5); await press('#sim-c6 .c6-clr');
    await p.focus('#sim-c6 .c6-b[data-p=it][data-i="1"]'); await p.keyboard.press('Enter'); s = await st(); same(s, 5, 8, 'Enter на кружке 2');
    await p.focus('#sim-c6 .c6-b[data-p=dg][data-i="4"]'); await p.keyboard.press(' '); s = await st(); same(s, 5, 9, 'пробел на цифре 5');
    // 3. смена n сохраняет предметы, которые ещё есть
    await setN(6); await press('#sim-c6 .c6-clr');
    for (const i of [1, 3, 5]) await press('#sim-c6 .c6-b[data-p=it][data-i="' + (i - 1) + '"]');
    s = await st(); same(s, 6, 42, 'набор {1,3,5}');
    await setN(8); s = await st(); same(s, 8, fromSet(8, [1, 3, 5]), 'n 6→8 сохраняет {1,3,5}');
    await setN(4); s = await st(); same(s, 4, fromSet(4, [1, 3]), 'n 8→4 оставляет {1,3}');
    await setN(7); s = await st(); same(s, 7, fromSet(7, [1, 3]), 'n 4→7: 5 не возвращается');
    await setN(1); s = await st(); same(s, 1, 1, 'n →1 оставляет {1}');
    // 4. ошибки страницы, KaTeX, подпись
    const kx = await p.evaluate(() => ({err: document.querySelectorAll('.katex-error').length, cap: document.querySelector('#sim-c6 .sim-cap').textContent.trim(),
      aria: document.querySelector('#sim-c6 svg').getAttribute('aria-label')}));
    chk(kx.err === 0, width + ' ошибок KaTeX ' + kx.err);
    chk(kx.cap.split(/\s+/).length <= 15, width + ' подпись длиннее 15 слов');
    chk(kx.aria.startsWith('Интерактив: '), width + ' aria-label');
    chk(errs.length === 0, width + ' ошибки страницы: ' + errs.join(' | '));
    await ctx.close();
  }
  await b.close();
  console.log('c6: ' + ok + '/' + (ok + bad.length));
  process.exit(bad.length ? 1 : 0);
})();
