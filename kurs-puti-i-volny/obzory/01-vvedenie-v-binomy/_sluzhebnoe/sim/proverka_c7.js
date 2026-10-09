// Проверка c7: все клетки n ≤ 8 × все направления — число стрелок, множители, точная целочисленная сверка,
// вывод под рисунком, режим «все четыре», ошибки страницы, горизонтальная прокрутка на 390 и 1280.
// Запуск: python3 sobrat_c7.py && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node proverka_c7.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/';
function B(n, k) { if (k < 0 || k > n) return 0n; let r = 1n; for (let i = 1; i <= k; i++) r = r * BigInt(n - k + i) / BigInt(i); return r; }
// ожидаемые стрелки по формулам задания
function route(n, k, d) {
  const r = [];
  if (d === 0) for (let j = 0; j < k; j++) r.push({a: [n, j], b: [n, j + 1], p: n - j, q: j + 1});
  if (d === 1) for (let j = n - 1; j >= k; j--) r.push({a: [n, j + 1], b: [n, j], p: j + 1, q: n - j});
  if (d === 2) for (let m = n - k; m < n; m++) { const j = m - (n - k); r.push({a: [m, j], b: [m + 1, j + 1], p: m + 1, q: j + 1}); }
  if (d === 3) for (let m = k; m < n; m++) r.push({a: [m, k], b: [m + 1, k], p: m + 1, q: m + 1 - k});
  return r;
}
const LEN = (n, k, d) => [k, n - k, k, n - k][d];
let pass = 0, total = 0; const fails = [];
const ok = (cond, msg) => { total++; if (cond) pass++; else fails.push(msg); };
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}});
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push('pageerror ' + e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    await p.goto('file://' + __dirname + '/preview-c7.html'); await p.waitForTimeout(400);
    // умолчание: (6,3), «влево»
    const d0 = await p.evaluate(() => { const r = document.getElementById('sim-c7'); return {sel: r.querySelector('.c7-cell.sel') && [r.querySelector('.c7-cell.sel').dataset.n, r.querySelector('.c7-cell.sel').dataset.k].join(','), on: r.querySelector('.c7-b.on').dataset.d, out: r.querySelector('.sim-out').textContent}; });
    ok(d0.sel === '6,3' && d0.on === '0', `${w}: умолчание ${JSON.stringify(d0)}`);
    for (let d = 0; d <= 4; d++) {
      await p.click(`#sim-c7 .c7-b[data-d="${d}"]`);
      for (let n = 0; n <= 8; n++) for (let k = 0; k <= n; k++) {
        const st = await p.evaluate(([n, k]) => {
          const r = document.getElementById('sim-c7');
          r.querySelector(`.c7-cell[data-n="${n}"][data-k="${k}"] .c7-hit`).dispatchEvent(new MouseEvent('click', {bubbles: true}));
          const arr = [...r.querySelectorAll('.c7-arr')].map(g => ({cls: g.getAttribute('class'), a: g.dataset.a, b: g.dataset.b, lab: g.querySelector('.c7-lab').textContent, op: g.getAttribute('opacity')}));
          const lines = [...r.querySelectorAll('.sim-out .c7-line[data-r]')].map(l => ({r: +l.dataset.r, v: l.querySelector('.c7-v') && l.querySelector('.c7-v').textContent, txt: l.textContent, fr: [...l.querySelectorAll('.c7-fr')].map(f => [f.children[0].textContent, f.children[1].textContent])}));
          const pr = r.querySelector('.sim-out .c7-pr'); const cellTxt = r.querySelector(`.c7-cell[data-n="${n}"][data-k="${k}"] .c7-num`).textContent;
          return {arr, lines, pr: pr ? pr.textContent : null, cellTxt, selOk: !!r.querySelector(`.c7-cell.sel[data-n="${n}"][data-k="${k}"]`)};
        }, [n, k]);
        const tag = `${w} d${d} (${n},${k})`;
        ok(st.selOk && st.cellTxt === String(B(n, k)), `${tag}: выделение/число в клетке`);
        const ds = d === 4 ? [0, 1, 2, 3] : [d];
        let expTot = 0;
        for (const dd of ds) {
          const exp = route(n, k, dd); expTot += exp.length;
          ok(exp.length === LEN(n, k, dd), `${tag}: длина формулы`);
          const got = st.arr.filter(a => d === 4 ? a.cls.includes('c7-r' + dd) : true);
          ok(got.length === exp.length, `${tag}/${dd}: стрелок ${got.length}, ждали ${exp.length}`);
          exp.forEach((e, i) => {
            const g = got[i]; if (!g) return;
            const m = g.lab.match(/^×(\d+)(?:\/(\d+))?$/);
            const num = m ? +m[1] : NaN, den = m ? (m[2] ? +m[2] : 1) : NaN;
            ok(m && num === e.p && den === e.q && !(m[2] && den === 1), `${tag}/${dd}#${i}: подпись ${g.lab}, ждали ×${e.p}/${e.q}`);
            ok(g.a === e.a.join(',') && g.b === e.b.join(','), `${tag}/${dd}#${i}: концы ${g.a}→${g.b}`);
            const [ta, tb] = [g.a.split(',').map(Number), g.b.split(',').map(Number)];
            ok(B(tb[0], tb[1]) * BigInt(den) === B(ta[0], ta[1]) * BigInt(num), `${tag}/${dd}#${i}: голова·q ≠ хвост·p`);
          });
          if (exp.length) {
            const a0 = exp[0].a; ok(B(a0[0], a0[1]) === 1n && (a0[1] === 0 || a0[1] === a0[0]), `${tag}/${dd}: старт не единица на краю`);
            const last = exp[exp.length - 1].b; ok(last[0] === n && last[1] === k, `${tag}/${dd}: конец не в клетке`);
          }
          // вывод
          if (n === 0 && d === 4) continue;
          const L = st.lines.find(l => l.r === dd);
          ok(!!L, `${tag}/${dd}: нет строки вывода`); if (!L) continue;
          ok(L.v === String(B(n, k)), `${tag}/${dd}: значение в выводе ${L.v}`);
          if (!exp.length) { ok(/единица/.test(L.txt), `${tag}/${dd}: нет «единица на краю»`); continue; }
          let P = 1n, Q = 1n; L.fr.forEach(([a, c]) => { P *= BigInt(a); Q *= BigInt(c); });
          ok(L.fr.length === exp.length && B(n, k) * Q === P, `${tag}/${dd}: произведение в выводе ≠ C(n,k)`);
          if (d < 4) {
            const m2 = st.pr && st.pr.match(/^(\d+) · \(([\d·]+)\) = 1 · \(([\d·]+)\)$/);
            ok(!!m2, `${tag}: вторая строка «${st.pr}»`);
            if (m2) { const pp = s => s.split('·').reduce((x, y) => x * BigInt(y), 1n); ok(BigInt(m2[1]) * pp(m2[2]) === pp(m2[3]) && m2[1] === String(B(n, k)), `${tag}: вторая строка неверна`); }
          }
        }
        ok(st.arr.length === expTot, `${tag}: всего стрелок ${st.arr.length}, ждали ${expTot}`);
        ok(st.arr.every(a => a.op === null), `${tag}: стрелки скрыты`);
      }
    }
    // «шагать»: после анимации все стрелки видны
    await p.click('#sim-c7 .c7-b[data-d="4"]');
    await p.evaluate(() => document.querySelector('#sim-c7 .c7-cell[data-n="6"][data-k="3"] .c7-hit').dispatchEvent(new MouseEvent('click', {bubbles: true})));
    await p.click('#sim-c7 .c7-go'); await p.waitForTimeout(300);
    const mid = await p.evaluate(() => [...document.querySelectorAll('#sim-c7 .c7-arr')].map(g => +g.getAttribute('opacity')));
    ok(mid.some(o => o < 0.5), `${w}: «шагать» не прячет стрелки в начале`);
    await p.waitForTimeout(2600);
    const fin = await p.evaluate(() => [...document.querySelectorAll('#sim-c7 .c7-arr')].map(g => +g.getAttribute('opacity')));
    ok(fin.length === 12 && fin.every(o => o > 0.999), `${w}: «шагать» конец ${fin}`);
    // клавиатура
    await p.focus('#sim-c7 svg'); await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowRight');
    const kb = await p.evaluate(() => { const s = document.querySelector('#sim-c7 .c7-cell.sel'); return s.dataset.n + ',' + s.dataset.k; });
    ok(kb === '7,4', `${w}: клавиатура ${kb}`);
    // прокрутка, ширина меток
    const sc = await p.evaluate(() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth}));
    ok(sc.sw <= sc.cw, `${w}: горизонтальная прокрутка ${sc.sw}>${sc.cw}`);
    const fs = await p.evaluate(() => { const t = document.querySelector('#sim-c7 .c7-lab'); const svg = t.ownerSVGElement; const k = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width; return +t.getAttribute('font-size') * k; });
    ok(fs >= 11, `${w}: шрифт подписи ${fs.toFixed(1)}px`);
    const hit = await p.evaluate(() => { const r = document.querySelector('#sim-c7 .c7-hit').getBoundingClientRect(); return Math.min(r.width, r.height); });
    ok(hit >= 28, `${w}: зона нажатия ${hit.toFixed(1)}px`);
    console.log(`  ${w}px: метка ${fs.toFixed(1)}px, зона ${hit.toFixed(1)}px`);
    ok(errs.length === 0, `${w}: ошибки ${errs.join(' | ')}`);
    const ke = await p.$$eval('.katex-error', e => e.length); ok(ke === 0, `${w}: katex-error ${ke}`);
    await ctx.close();
  }
  await b.close();
  fails.slice(0, 30).forEach(f => console.log('  ✗ ' + f));
  console.log(`c7: ${pass}/${total}`);
  process.exit(pass === total ? 0 : 1);
})();
