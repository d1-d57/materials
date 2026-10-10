// Проверка c8: для каждой выбираемой строки n = 0..6 — число и концы стрелок, правило Паскаля по стрелкам,
// суммы всех 8 строк = 2^n, равенства в выводе, переключатель «степени двойки», «шагать», клавиатура,
// перекрытие сумм с треугольником, ошибки страницы, горизонтальная прокрутка на 390 и 1280.
// Запуск: python3 sobrat_c8.py && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node proverka_c8.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const KD = '/opt/npm-tools/node_modules/katex/dist/';
const C = (n, k) => { if (k < 0 || k > n) return 0; let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return Math.round(r); };
const SUP = {'⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4, '⁵': 5, '⁶': 6, '⁷': 7};
const nums = s => s.replace(/ /g, ' ').split('+').map(x => +x.trim());
let pass = 0, total = 0; const fails = [];
const ok = (cond, msg) => { total++; if (cond) pass++; else fails.push(msg); };
// состояние виджета одним снимком DOM
const STATE = () => {
  const r = document.getElementById('sim-c8'), svg = r.querySelector('svg');
  const k = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
  const cells = [...r.querySelectorAll('.c8-cell')].map(c => { const b = c.querySelector('.c8-box'); return {n: +c.dataset.n, k: +c.dataset.k, v: c.querySelector('.c8-num').textContent, x: +b.getAttribute('x'), y: +b.getAttribute('y'), w: +b.getAttribute('width'), h: +b.getAttribute('height')}; });
  const arr = [...r.querySelectorAll('.c8-arr')].map(g => { const l = g.querySelector('.c8-ln'), hd = g.querySelector('.c8-hd').getAttribute('points').split(' ')[0].split(',').map(Number); return {cls: g.getAttribute('class'), a: g.dataset.a, b: g.dataset.b, x1: +l.getAttribute('x1'), y1: +l.getAttribute('y1'), tip: hd, op: g.getAttribute('opacity')}; });
  const sums = [...r.querySelectorAll('.c8-sum')].map(t => { const bb = t.getBBox(); return {n: +t.dataset.n, txt: t.textContent, x: bb.x, r: bb.x + bb.width}; });
  const on = [...r.querySelectorAll('.c8-row.on')].map(g => +g.dataset.n);
  return {cells, arr, sums, on, W: svg.viewBox.baseVal.width, k, l1: r.querySelector('.c8-l1').textContent, l2: r.querySelector('.c8-l2').textContent, pw: r.querySelector('.c8-pw').classList.contains('on')};
};
function checkSums(st, pow, tag) {
  ok(st.sums.length === 8, `${tag}: сумм ${st.sums.length}`);
  for (let n = 0; n <= 7; n++) {
    const s = st.sums.find(x => x.n === n); if (!s) { ok(false, `${tag}: нет суммы ${n}`); continue; }
    const rowSum = st.cells.filter(c => c.n === n).reduce((a, c) => a + +c.v, 0);
    const m = s.txt.match(/^= (\d+)(?: = 2([⁰¹²³⁴⁵⁶⁷]))?$/);
    ok(!!m && +m[1] === 2 ** n && +m[1] === rowSum, `${tag}: сумма строки ${n} «${s.txt}», по клеткам ${rowSum}`);
    if (m) ok(pow ? (m[2] !== undefined && SUP[m[2]] === n && 2 ** SUP[m[2]] === +m[1]) : m[2] === undefined, `${tag}: степень у суммы ${n} «${s.txt}»`);
    // сумма не налезает на треугольник и не вылезает за рисунок
    const right = Math.max(...st.cells.filter(c => c.n === n).map(c => c.x + c.w));
    ok(s.x > right + 2 && s.r <= st.W, `${tag}: сумма ${n} перекрывает/вылезает (${s.x.toFixed(1)}..${s.r.toFixed(1)}, клетки до ${right.toFixed(1)}, W ${st.W})`);
  }
}
function checkRow(st, n, tag) {
  ok(st.on.join() === [n, n + 1].join(), `${tag}: подсвечены строки ${st.on}`);
  for (const c of st.cells) ok(c.v === String(C(c.n, c.k)), `${tag}: клетка (${c.n},${c.k}) = ${c.v}`);
  ok(st.arr.length === 2 * (n + 1), `${tag}: стрелок ${st.arr.length}, ждали ${2 * (n + 1)}`);
  const cell = (a, b) => st.cells.find(c => c.n === a && c.k === b);
  const inc = {};
  for (let k = 0; k <= n; k++) {
    const mine = st.arr.filter(a => a.a === n + ',' + k);
    ok(mine.length === 2, `${tag}: из (${n},${k}) стрелок ${mine.length}`);
    const tg = mine.map(a => a.b).sort();
    ok(tg.join('|') === [(n + 1) + ',' + k, (n + 1) + ',' + (k + 1)].sort().join('|'), `${tag}: из (${n},${k}) цели ${tg}`);
    const tl = cell(n, k);
    for (const a of mine) {
      const [bn, bk] = a.b.split(',').map(Number), tc = cell(bn, bk);
      ok(!!tc, `${tag}: цель ${a.b} вне треугольника`); if (!tc) continue;
      // геометрия: хвост под своей клеткой, остриё над клеткой-целью
      ok(a.x1 > tl.x && a.x1 < tl.x + tl.w && a.y1 > tl.y + tl.h && a.y1 < tl.y + tl.h + 8, `${tag}: хвост ${a.a}→${a.b}`);
      ok(a.tip[0] > tc.x && a.tip[0] < tc.x + tc.w && a.tip[1] < tc.y && a.tip[1] > tc.y - 8, `${tag}: остриё ${a.a}→${a.b}`);
      ok(a.cls.includes(bk === k ? 'c8-L' : 'c8-R'), `${tag}: цвет ${a.a}→${a.b}`);
      ok(a.op === null, `${tag}: стрелка скрыта`);
      inc[a.b] = (inc[a.b] || 0) + +tl.v;
    }
  }
  // правило Паскаля по стрелкам: число строки n+1 = сумма хвостов пришедших в него стрелок
  for (let k = 0; k <= n + 1; k++) ok(inc[(n + 1) + ',' + k] === C(n + 1, k), `${tag}: в (${n + 1},${k}) пришло ${inc[(n + 1) + ',' + k]}`);
  // вывод
  const S = 2 ** n, l1 = st.l1.replace(/ /g, ' '), l2 = st.l2.replace(/ /g, ' ');
  const m1 = l1.match(/^строка (\d+): (.*)$/);
  ok(!!m1 && +m1[1] === n, `${tag}: строка 1 «${l1}»`);
  if (m1) {
    const parts = m1[2].split('=').map(x => x.trim()), terms = nums(parts[0]), tot = +parts[parts.length - 1];
    ok(terms.join() === Array.from({length: n + 1}, (_, k) => C(n, k)).join() && terms.reduce((a, b) => a + b, 0) === tot && tot === S && parts.length === (n ? 2 : 1), `${tag}: строка 1 неверна «${l1}»`);
  }
  const m2 = l2.match(/^каждое число строки (\d+) вошло в строку (\d+) дважды: 2 · (\d+) = (\d+) = (.*)$/);
  ok(!!m2, `${tag}: строка 2 «${l2}»`);
  if (m2) {
    const terms = nums(m2[5]);
    ok(+m2[1] === n && +m2[2] === n + 1 && +m2[3] === S && 2 * +m2[3] === +m2[4] && terms.reduce((a, b) => a + b, 0) === +m2[4] && terms.join() === Array.from({length: n + 2}, (_, k) => C(n + 1, k)).join(), `${tag}: строка 2 неверна «${l2}»`);
  }
  ok(!/[\/÷]|раздел|делим|половин/.test(l1 + l2), `${tag}: в выводе деление`);
}
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 1280]) {
    const ctx = await b.newContext({viewport: {width: w, height: 900}});
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push('pageerror ' + e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    await p.goto('file://' + __dirname + '/preview-c8.html'); await p.waitForTimeout(400);
    // умолчание: строка 4, степени выключены
    let st = await p.evaluate(STATE);
    ok(!st.pw, `${w}: степени включены по умолчанию`);
    checkRow(st, 4, `${w} умолчание`); checkSums(st, false, `${w} умолчание`);
    await p.locator('#sim-c8').scrollIntoViewIfNeeded();
    // каждая строка: настоящим нажатием мыши — по клетке (по очереди разной) и по сумме
    for (let n = 0; n <= 6; n++) {
      for (const target of ['cell', 'sum']) {
        await p.evaluate(() => document.querySelector('#sim-c8 .c8-row[data-n="0"] .c8-hit').dispatchEvent(new MouseEvent('click', {bubbles: true})));
        const sel = target === 'cell' ? `#sim-c8 .c8-cell[data-n="${n}"][data-k="${Math.floor(n / 2)}"] .c8-box` : `#sim-c8 .c8-sum[data-n="${n}"]`;
        const bb = await p.locator(sel).boundingBox();
        await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
        st = await p.evaluate(STATE);
        checkRow(st, n, `${w} n${n} ${target}`);
      }
    }
    // нижняя строка 7 выбирает 6 (её «предыдущую»)
    { const bb = await p.locator('#sim-c8 .c8-cell[data-n="7"][data-k="3"] .c8-box').boundingBox(); await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2); st = await p.evaluate(STATE); checkRow(st, 6, `${w} клик по строке 7`); }
    // степени двойки
    await p.click('#sim-c8 .c8-pw'); st = await p.evaluate(STATE);
    ok(st.pw, `${w}: кнопка степеней не нажата`); checkSums(st, true, `${w} степени`); checkRow(st, 6, `${w} степени`);
    await p.click('#sim-c8 .c8-pw'); st = await p.evaluate(STATE); checkSums(st, false, `${w} степени выкл`);
    // «шагать»: 4 → 5 с анимацией, 6 → 0
    await p.evaluate(() => document.querySelector('#sim-c8 .c8-row[data-n="4"] .c8-hit').dispatchEvent(new MouseEvent('click', {bubbles: true})));
    await p.click('#sim-c8 .c8-go'); await p.waitForTimeout(250);
    const mid = await p.evaluate(() => [...document.querySelectorAll('#sim-c8 .c8-arr')].map(g => g.getAttribute('opacity')));
    ok(mid.length === 12 && mid.some(o => o !== null && +o < 0.5), `${w}: «шагать» не прячет стрелки в начале ${mid}`);
    await p.waitForTimeout(1500); st = await p.evaluate(STATE); checkRow(st, 5, `${w} шагать 4→5`);
    await p.click('#sim-c8 .c8-go'); await p.waitForTimeout(1600); st = await p.evaluate(STATE); checkRow(st, 6, `${w} шагать 5→6`);
    await p.click('#sim-c8 .c8-go'); await p.waitForTimeout(1600); st = await p.evaluate(STATE); checkRow(st, 0, `${w} шагать 6→0`);
    // клавиатура
    await p.focus('#sim-c8 svg'); await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowUp');
    st = await p.evaluate(STATE); checkRow(st, 1, `${w} клавиатура`);
    // размеры: шрифт чисел, зона нажатия
    const fs = st.k * +(await p.getAttribute('#sim-c8 .c8-num', 'font-size'));
    const fsum = st.k * +(await p.getAttribute('#sim-c8 .c8-sum', 'font-size'));
    const hit = await p.evaluate(() => { const r = document.querySelector('#sim-c8 .c8-hit').getBoundingClientRect(); return Math.min(r.width, r.height); });
    ok(fs >= 12.5 && fsum >= 13, `${w}: шрифт чисел ${fs.toFixed(1)}px, сумм ${fsum.toFixed(1)}px`);
    ok(hit >= 28, `${w}: зона нажатия ${hit.toFixed(1)}px`);
    console.log(`  ${w}px: числа ${fs.toFixed(1)}px, суммы ${fsum.toFixed(1)}px, зона ${hit.toFixed(1)}px`);
    const sc = await p.evaluate(() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth}));
    ok(sc.sw <= sc.cw, `${w}: горизонтальная прокрутка ${sc.sw}>${sc.cw}`);
    const al = await p.getAttribute('#sim-c8 svg', 'aria-label'); ok(/^Интерактив: /.test(al), `${w}: aria-label`);
    ok(errs.length === 0, `${w}: ошибки ${errs.join(' | ')}`);
    const ke = await p.$$eval('.katex-error', e => e.length); ok(ke === 0, `${w}: katex-error ${ke}`);
    await ctx.close();
  }
  // «меньше движения»: «шагать» сразу даёт последний кадр
  { const ctx = await b.newContext({viewport: {width: 390, height: 900}, reducedMotion: 'reduce'}); const p = await ctx.newPage();
    await p.route(/cdn\.jsdelivr\.net\/npm\/katex@[^/]+\/dist\/(.*)/, r => r.fulfill({path: KD + r.request().url().replace(/.*\/dist\//, '')}));
    await p.goto('file://' + __dirname + '/preview-c8.html'); await p.waitForTimeout(300);
    await p.click('#sim-c8 .c8-go'); await p.waitForTimeout(60); const st = await p.evaluate(STATE); checkRow(st, 5, 'reduced шагать'); await ctx.close(); }
  await b.close();
  fails.slice(0, 30).forEach(f => console.log('  ✗ ' + f));
  console.log(`c8: ${pass}/${total}`);
  process.exit(pass === total ? 0 : 1);
})();
