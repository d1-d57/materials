// Проверка счёта, часть 2 (Playwright): для всех допустимых положений ползунков считаем,
// что виджет НАРИСОВАЛ (элементы DOM и числа в подписях), и сверяем с биномами.
// Запуск: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node proverka_dom.js
const {chromium} = require('/opt/npm-tools/node_modules/playwright');
const C = (n, k) => { let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return Math.round(r); };
(async () => {
  const b = await chromium.launch(), bad = []; let ok = 0;
  for (const width of [390, 1280]) {
    const p = await b.newPage({viewport: {width, height: 900}});
    await p.emulateMedia({reducedMotion: 'reduce'});            // анимации — сразу последний кадр
    const errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.route(/cdn\.jsdelivr\.net/, r => r.abort());
    await p.goto('file://' + __dirname + '/preview.html'); await p.waitForTimeout(200);
    const chk = (c, m) => { if (c) ok++; else bad.push(width + ': ' + m); };
    const set = (id, c, v) => p.evaluate(([id, c, v]) => { const e = document.querySelector('#sim-' + id + ' .' + c); e.value = v; e.dispatchEvent(new Event('input')); }, [id, c, v]);
    const sw = () => p.evaluate(() => document.documentElement.scrollWidth);
    // значения по умолчанию (до любых действий)
    const d = await p.evaluate(() => {
      const q = s => document.querySelector(s), v = s => +q(s).value;
      return {c1: [v('#sim-c1 .c1-n'), v('#sim-c1 .c1-k'), +q('#sim-c1 .c1-n').max], c2: [v('#sim-c2 .c2-n'), v('#sim-c2 .c2-k')], c2nums: [...document.querySelectorAll('#sim-c2 .w-num')].map(e => +e.textContent),
        c3: [v('#sim-c3 .c3-n'), v('#sim-c3 .c3-m')], c3lab: q('#sim-c3 .w-lab').textContent, c3ctl: q('#sim-c3 .sim-ctl:nth-child(2)').textContent.replace(/\d+$/, '').trim(),
        c3btn: [...document.querySelectorAll('#sim-c3 .c3-b')].map(e => e.textContent), c3cards: document.querySelectorAll('#sim-c3 svg g g').length,
        c3val: [...document.querySelectorAll('#sim-c3 .c3-v')].map(e => e.textContent), c5: v('#sim-c5 .c5-n')};
    });
    chk(d.c1.join() === '5,2,6', `default c1 ${d.c1}`);
    chk(d.c2.join() === '5,2' && d.c2nums.join() === '10,4,6', `default c2 ${d.c2} ${d.c2nums}`);
    chk(d.c3.join() === '6,3' && d.c3cards === 60 && d.c3lab === '6 стопок по 10 карточек', `default c3 ${d.c3} ${d.c3cards} "${d.c3lab}"`);
    chk(d.c3ctl === 'команда (k+1)', `c3 slider label "${d.c3ctl}"`);
    chk(d.c3btn.join('|') === 'сначала капитан|сначала рядовые|сначала команда', `c3 button order ${d.c3btn}`);
    chk(d.c3val.join('|') === '6 · 10|15 · 4|20 · 3', `c3 default products ${d.c3val}`);
    chk(d.c5 === 5, `default c5 ${d.c5}`);
    // c0: значения по умолчанию, затем все 27 положений ползунков — строки читаем из DOM (текст набора, классы клеток, геометрия)
    const c0d = await p.evaluate(() => { const R = document.getElementById('sim-c0'), q = s => R.querySelector(s); return [+q('.c0-n').value, +q('.c0-k').value, +q('.c0-n').min, +q('.c0-n').max, +q('.c0-k').max, R.querySelectorAll('.c0-row').length, q('.c0-cnt').textContent]; });
    chk(c0d.join() === '4,2,1,6,4,6,вариантов: 6', `default c0 ${c0d}`);
    const setStr = a => a.length ? '{' + a.join(', ') + '}' : '{ }';
    const tail = a => a.length === 0 ? 'единиц нет — ничего не выбрано' : a.length === 1 ? `на месте ${a[0]} — единица` : `на местах ${a.slice(0, -1).join(', ')} и ${a[a.length - 1]} — единицы`;
    let c0rows = 0;
    for (let n = 1; n <= 6; n++) for (let k = 0; k <= n; k++) {
      await set('c0', 'c0-n', n); await set('c0', 'c0-k', k);
      const r = await p.evaluate(() => { const R = document.getElementById('sim-c0'), sv = R.querySelector('svg'), sb = sv.getBoundingClientRect();
        const rows = [...R.querySelectorAll('.c0-row')].map(g => { const cells = [...g.querySelectorAll('.w-c')], hb = g.querySelector('.w-hit').getBoundingClientRect();
          return {set: g.querySelector('.c0-set').textContent, code: cells.map(e => e.classList.contains('on') ? 1 : 0).join(''), xs: cells.map(e => e.getBoundingClientRect().x), hit: [hb.x, hb.y, hb.width, hb.height], op: g.getAttribute('opacity')}; });
        return {rows, cnt: R.querySelector('.c0-cnt').textContent, cols: +sv.getAttribute('data-cols'), svg: [sb.x, sb.y, sb.width, sb.height], k: +R.querySelector('.c0-k').value, kmax: +R.querySelector('.c0-k').max}; });
      const N = C(n, k), codes = r.rows.map(x => x.code); c0rows += r.rows.length;
      chk(r.rows.length === N && r.cnt === 'вариантов: ' + N, `c0 count n=${n} k=${k}: ${r.rows.length} "${r.cnt}"`);
      chk(r.k === k && r.kmax === n, `c0 slider k n=${n} k=${k}: ${r.k}/${r.kmax}`);
      chk(new Set(codes).size === N, `c0 distinct n=${n} k=${k}`);
      chk(codes.every(c => c.length === n && c.split('').filter(x => x === '1').length === k), `c0 k ones n=${n} k=${k}`);
      chk(r.rows.every(x => x.xs.every((v, i, a) => i === 0 || a[i - 1] < v)), `c0 cells left-to-right n=${n} k=${k}`);
      chk(r.rows.every(x => x.set === setStr(x.code.split('').map((b, i) => b === '1' ? i + 1 : 0).filter(Boolean))), `c0 set<->code n=${n} k=${k}`);
      chk(codes.every((c, i) => i === 0 || codes[i - 1] > c), `c0 order n=${n} k=${k}: ${codes.join(' ')}`);
      const hs = r.rows.map(x => x.hit), [sx, sy, swd, sht] = r.svg, eps = 0.5;
      chk(hs.every(([x, y, w, h]) => x >= sx - eps && y >= sy - eps && x + w <= sx + swd + eps && y + h <= sy + sht + eps), `c0 rows inside svg n=${n} k=${k}`);
      chk(hs.every((a, i) => hs.every((b, j) => i === j || a[0] + a[2] <= b[0] + eps || b[0] + b[2] <= a[0] + eps || a[1] + a[3] <= b[1] + eps || b[1] + b[3] <= a[1] + eps)), `c0 rows overlap n=${n} k=${k}`);
      chk(Math.min(...hs.map(h => h[3])) >= 24, `c0 tap height n=${n} k=${k}`);
      chk(r.cols === (N > 6 && width >= 1000 ? 2 : 1), `c0 columns n=${n} k=${k}: ${r.cols}`);
      chk(r.rows.every(x => x.op === null), `c0 no fade under reduced motion n=${n} k=${k}`);
      const i = Math.floor(N / 2);
      await p.dispatchEvent(`#sim-c0 .c0-row[data-i="${i}"]`, 'pointerdown');
      const h = await p.evaluate(i => { const R = document.getElementById('sim-c0'); return {out: R.querySelector('.sim-out').textContent, hl: [...R.querySelectorAll('.c0-row.hl')].map(g => +g.dataset.i), pos: [...R.querySelectorAll('.c0-pos.hl')].map(e => +e.textContent)}; }, i);
      const a = codes[i].split('').map((b, j) => b === '1' ? j + 1 : 0).filter(Boolean);
      chk(h.out === `${setStr(a)} ↔ ${codes[i]}: ${tail(a)}`, `c0 hover n=${n} k=${k}: "${h.out}"`);
      chk(h.hl.join() === String(i) && h.pos.join() === a.join(), `c0 hover marks n=${n} k=${k}: ${h.hl} / ${h.pos}`);
    }
    chk(c0rows === 126, `c0 total rows ${c0rows}`);
    await set('c0', 'c0-n', 6); await set('c0', 'c0-k', 5); await set('c0', 'c0-n', 3);
    const sh = await p.evaluate(() => { const R = document.getElementById('sim-c0'); return [+R.querySelector('.c0-k').value, R.querySelector('.c0-kv').textContent, R.querySelectorAll('.c0-row').length]; });
    chk(sh.join() === '3,3,1', `c0 k shrinks with n: ${sh}`);
    await set('c0', 'c0-n', 6); await set('c0', 'c0-k', 3);
    const c0w = await p.evaluate(() => { const R = document.getElementById('sim-c0'), s = R.querySelector('svg').getBoundingClientRect(); return [R.scrollWidth <= R.clientWidth, Math.round(s.height)]; });
    chk(c0w[0], `c0 no horizontal overflow`); console.log(`  ${width}px: c0 n=6 k=3 — высота рисунка ${c0w[1]}px`);
    // c1
    for (let n = 2; n <= 6; n++) for (let k = 0; k <= n; k++) {
      await set('c1', 'c1-n', n); await set('c1', 'c1-k', k);
      const r = await p.evaluate(() => { const R = document.getElementById('sim-c1'); return {L: R.querySelectorAll('.w-word[data-side=L]').length, R: R.querySelectorAll('.w-word[data-side=R]').length, links: R.querySelectorAll('.w-link').length, nums: [...R.querySelectorAll('.w-num')].map(e => +e.textContent), arcs: R.querySelectorAll('.c1-arc').length,
        onL: [...R.querySelectorAll('.w-word[data-side=L]')].map(g => g.querySelectorAll('.w-c.on').length), hit: Math.min(...[...R.querySelectorAll('.w-hit')].map(e => e.getBoundingClientRect().height))}; });
      const N = C(n, k);
      chk(r.L === N && r.R === C(n, n - k) && r.links === N && r.nums.every(x => x === N), `c1 n=${n} k=${k} ${JSON.stringify(r).slice(0, 80)}`);
      chk(r.onL.every(x => x === k), `c1 ones n=${n} k=${k}`);
      chk(2 * k === n ? r.arcs === N : r.arcs === 0, `c1 arcs n=${n} k=${k}`);
      chk(r.hit >= 20, `c1 tap row height n=${n} k=${k}: ${r.hit.toFixed(1)}px`);
      await p.click('#sim-c1 .c1-go'); await p.waitForTimeout(30);
      // после «отразить»: левые слова на месте (видны, k закрашенных), копии с n-k закрашенными легли ровно на правые слова
      const f = await p.evaluate(() => { const R = document.getElementById('sim-c1'), box = g => [...g.querySelectorAll('.w-c')].map(e => { const b = e.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), e.classList.contains('on') ? 1 : 0].join(':'); }).join('|');
        const Ls = [...R.querySelectorAll('.w-word[data-side=L]')], Rs = new Set([...R.querySelectorAll('.w-word[data-side=R]')].map(box)), Fs = [...R.querySelectorAll('.c1-fly')];
        return {lOn: Ls.map(g => g.querySelectorAll('.w-c.on').length), lOp: Math.min(...Ls.map(g => +getComputedStyle(g).opacity)), lVis: Ls.every(g => g.getBoundingClientRect().width > 0),
          fOn: Fs.map(g => g.querySelectorAll('.w-c.on').length), land: new Set(Fs.map(box)).size === Fs.length && Fs.every(g => Rs.has(box(g)))}; });
      chk(f.lOn.every(x => x === k) && f.lVis && f.lOp >= 0.3, `c1 left stays n=${n} k=${k} op=${f.lOp}`);
      chk(f.fOn.length === N && f.fOn.every(x => x === n - k) && f.land, `c1 copies land n=${n} k=${k} ${f.land}`);
    }
    // c2
    for (let n = 2; n <= 6; n++) for (let k = 1; k < n; k++) {
      await set('c2', 'c2-n', n); await set('c2', 'c2-k', k);
      const r = await p.evaluate(() => { const R = document.getElementById('sim-c2'); return {words: R.querySelectorAll('.c2-first').length, first1: R.querySelectorAll('.c2-first.on').length, nums: [...R.querySelectorAll('.w-num')].map(e => +e.textContent)}; });
      chk(r.words === C(n, k) && r.first1 === C(n - 1, k - 1) && r.words - r.first1 === C(n - 1, k), `c2 n=${n} k=${k} ${JSON.stringify(r)}`);
      chk(r.nums.join() === [C(n, k), C(n - 1, k - 1), C(n - 1, k)].join(), `c2 nums n=${n} k=${k} ${r.nums}`);
      await p.click('#sim-c2 .c2-go'); await p.waitForTimeout(30);
      const o = await p.evaluate(() => { const R = document.getElementById('sim-c2'), vis = e => { let x = e, op = 1; while (x && x.tagName !== 'svg') { op *= +(x.getAttribute('opacity') ?? 1); x = x.parentNode; } return op; };
        return {out: R.querySelector('.sim-out').textContent, labs: [...R.querySelectorAll('.w-lab')].filter(e => vis(e) > 0.99).map(e => e.textContent)}; });
      chk(o.out.includes(C(n, k) + ' = ' + C(n - 1, k - 1) + ' + ' + C(n - 1, k)), `c2 out n=${n} k=${k} "${o.out}"`);
      const want = ['первая закрашена', 'первая пустая', `длина ${n - 1}, закрашено ${k - 1}`, `длина ${n - 1}, закрашено ${k}`];
      chk(want.every(w => o.labs.includes(w)) && !o.labs.includes(`длина ${n}, закрашено ${k}`), `c2 labels n=${n} k=${k}: ${o.labs}`);
      await p.click('#sim-c2 .c2-back'); await p.waitForTimeout(30);
    }
    // c3: читаем карточки из DOM, собираем стопки по положению, проверяем однородность; высота рисунка — по активной раскладке
    for (let n = 3; n <= 6; n++) for (let m = 2; m < n; m++) {
      await set('c3', 'c3-n', n); await set('c3', 'c3-m', m);
      for (const md of [0, 2, 1]) {
        await p.click(`#sim-c3 .c3-b[data-m="${md}"]`); await p.waitForTimeout(30);
        const r = await p.evaluate(() => { const R = document.getElementById('sim-c3');
          const cs = [...R.querySelectorAll('svg g g')].map(g => { const t = g.getAttribute('transform').match(/[-\d.]+/g).map(Number), team = [], ch = [...g.children].slice(1); let cap = -1;
            ch.forEach((e, i) => { if (e.tagName === 'polygon') { cap = i; team.push(1); } else team.push(e.classList.contains('c3-m') ? 1 : 0); });
            return {x: t[0], y: t[1], team: team.join(''), cap, h: +g.firstChild.getAttribute('height')}; });
          const vbH = +R.querySelector('svg').getAttribute('viewBox').split(' ')[3], bottom = Math.max(...cs.map(c => c.y + c.h));
          cs.sort((a, b) => a.x - b.x || a.y - b.y); const st = []; let cur = null;
          cs.forEach(c => { if (cur && Math.abs(cur.x - c.x) < .5 && c.y - cur.ly < 30) { cur.c.push(c); cur.ly = c.y; } else { cur = {x: c.x, ly: c.y, c: [c]}; st.push(cur); } });
          return {N: cs.length, stacks: st.map(s => s.c), lab: R.querySelector('.w-lab').textContent, vals: [...R.querySelectorAll('.c3-w')].map(e => e.dataset.m + ':' + e.querySelector('.c3-v').textContent + (e.classList.contains('on') ? '*' : '')),
            tot: R.querySelector('.c3-tot').textContent, gap: vbH - bottom}; });
        const k = m - 1, S = [n, C(n, m), C(n, k)][md], z = [C(n - 1, k), m, n - k][md];
        const key = c => md === 0 ? c.cap : md === 1 ? c.team : c.team.split('').map((v, i) => i === c.cap ? 0 : v).join('');
        chk(r.N === m * C(n, m), `c3 total n=${n} m=${m}`);
        chk(r.stacks.length === S && r.stacks.every(s => s.length === z), `c3 stacks n=${n} m=${m} md=${md}: ${r.stacks.length}x${r.stacks.map(s => s.length)}`);
        chk(r.stacks.every(s => s.every(c => key(c) === key(s[0]))) && new Set(r.stacks.map(s => key(s[0]))).size === S, `c3 homogeneous n=${n} m=${m} md=${md}`);
        chk(r.lab.startsWith(S + ' ') && r.lab.includes(' по ' + z + ' '), `c3 label n=${n} m=${m} md=${md} "${r.lab}"`);
        const wantV = [`0:${n} · ${C(n - 1, k)}`, `2:${C(n, k)} · ${n - k}`, `1:${C(n, m)} · ${m}`].map(s => s + (+s[0] === md ? '*' : ''));
        chk(r.vals.join('|') === wantV.join('|') && +r.tot === m * C(n, m), `c3 out n=${n} m=${m} md=${md}: ${r.vals} = ${r.tot}`);
        chk(r.gap >= 0 && r.gap <= 8, `c3 no empty band n=${n} m=${m} md=${md}: ${r.gap.toFixed(1)}`);
      }
      await p.click('#sim-c3 .c3-b[data-m="0"]'); await p.waitForTimeout(30);
    }
    // c4
    for (let n = 3; n <= 10; n++) {
      await set('c4', 'c4-n', n);
      const a = await p.evaluate(() => ({ar: document.querySelectorAll('#sim-c4 .c4-ar').length, hd: document.querySelectorAll('#sim-c4 .c4-hd').length, sg: document.querySelectorAll('#sim-c4 .c4-seg').length, v: document.querySelectorAll('#sim-c4 .c4-v').length, out: document.querySelector('#sim-c4 .sim-out').textContent}));
      chk(a.ar === n * (n - 1) && a.hd === n * (n - 1) && a.sg === n * (n - 1) / 2 && a.v === n && a.out.endsWith('= ' + n * (n - 1)), `c4 n=${n} ${JSON.stringify(a)}`);
      await p.click('#sim-c4 .c4-hit[data-v="0"]', {force: true});
      const h = await p.evaluate(() => document.querySelectorAll('#sim-c4 .c4-ar.hl').length); chk(h === n - 1, `c4 out-arrows n=${n}: ${h}`);
      await p.click('#sim-c4 .c4-go'); await p.waitForTimeout(30);
      const o = await p.evaluate(() => document.querySelector('#sim-c4 .sim-out').textContent);
      chk(o.includes('= ' + n * (n - 1) / 2) && o.includes('стрелок ' + n * (n - 1) + ' = 2 · ' + n * (n - 1) / 2) && !o.includes(': 2'), `c4 glued n=${n} "${o}"`);
      await p.click('#sim-c4 .c4-go'); await p.waitForTimeout(30);
    }
    // c5: клетки читаем из DOM (x, y → строка, столбец), проверяем лесенку, отражение, прямоугольник и счётчики
    for (let n = 2; n <= 8; n++) {
      await set('c5', 'c5-n', n);
      const st = () => p.evaluate(() => { const R = document.getElementById('sim-c5'), sv = R.querySelector('svg'), g = a => +sv.getAttribute('data-' + a), x0 = g('x0'), y0 = g('y0'), s = g('s'), gp = g('gp');
        const rc = e => { const x = (+e.getAttribute('x') - gp - x0) / s, y = (+e.getAttribute('y') - gp - y0) / s; return {r: y + 1, c: x + 1, op: +(e.getAttribute('opacity') ?? 1)}; };
        return {up: [...R.querySelectorAll('.c5-up')].map(rc), dn: [...R.querySelectorAll('.c5-dn')].map(rc), out: R.querySelector('.sim-out').textContent, size: s,
          btn: [...R.querySelectorAll('button')].map(b => b.disabled ? 0 : 1).join('')}; });
      const M = n * (n - 1) / 2, sum = Array.from({length: n - 1}, (_, i) => n - 1 - i).join(' + ');
      const exact = cs => cs.every(c => Math.abs(c.r - Math.round(c.r)) < 1e-6 && Math.abs(c.c - Math.round(c.c)) < 1e-6), key = c => Math.round(c.r) + ',' + Math.round(c.c);
      let r = await st();
      chk(r.up.length === M && r.dn.length === M && exact(r.up) && r.up.every(c => c.r < c.c) && new Set(r.up.map(key)).size === M, `c5 ladder n=${n}`);
      chk(r.dn.every(c => c.op === 0), `c5 lower hidden n=${n}`);
      chk(r.out.startsWith('лесенка: ' + (n > 2 ? sum + ' = ' : '') + M), `c5 out0 n=${n} "${r.out}"`);
      chk(r.btn === '100', `c5 buttons0 n=${n} ${r.btn}`);
      chk(r.size >= 36, `c5 cell size n=${n}: ${r.size}`);
      await p.dispatchEvent(`#sim-c5 .c5-up[data-q="0"]`, 'pointerdown');
      r = await st(); chk(r.out.includes('пара {1, 2}'), `c5 hover up n=${n} "${r.out}"`);
      await p.click('#sim-c5 .c5-go'); await p.waitForTimeout(30); r = await st();
      chk(exact(r.dn) && r.dn.every((c, q) => Math.round(c.r) === Math.round(r.up[q].c) && Math.round(c.c) === Math.round(r.up[q].r) && c.op === 1), `c5 mirror n=${n}`);
      const two = r.up.concat(r.dn).map(key); chk(new Set(two).size === n * (n - 1) && two.every(k => k.split(',')[0] !== k.split(',')[1]), `c5 off-diagonal n=${n}`);
      chk(r.out.includes(n + ' · ' + (n - 1) + ' = ' + n * (n - 1)) && r.out.includes('упорядоченные пары'), `c5 out1 n=${n} "${r.out}"`);
      chk(r.btn === '011', `c5 buttons1 n=${n} ${r.btn}`);
      if (n >= 2) { const q = (n >= 5) ? 3 : 0; await p.dispatchEvent(`#sim-c5 .c5-dn[data-q="${q}"]`, 'pointerdown'); const pr = r.up[q]; r = await st();
        chk(r.out.includes(`(${Math.round(pr.c)}, ${Math.round(pr.r)}) — та же пара, другой порядок`), `c5 hover dn n=${n} "${r.out}"`); }
      await p.click('#sim-c5 .c5-sh'); await p.waitForTimeout(30); r = await st();
      const bar = r.up.concat(r.dn), bk = bar.map(key), want = []; for (let i = 1; i < n; i++) for (let j = 1; j <= n; j++) want.push(i + ',' + j);
      chk(exact(bar) && new Set(bk).size === bk.length, `c5 bar no overlap n=${n}`);
      chk(bk.length === (n - 1) * n && bk.slice().sort().join() === want.sort().join(), `c5 bar no holes n=${n}`);
      chk(r.out.includes(`прямоугольник ${n - 1} × ${n}`) && r.out.includes(`= 2 · ${M} = ${n - 1} · ${n} = ${n * (n - 1)} клет`) && !/шоколад|: 2/.test(r.out), `c5 out2 n=${n} "${r.out}"`);
      chk(r.btn === '001', `c5 buttons2 n=${n} ${r.btn}`);
      await p.click('#sim-c5 .c5-rs'); await p.waitForTimeout(30); r = await st();
      chk(r.out.startsWith('лесенка:') && r.dn.every(c => c.op === 0) && r.btn === '100', `c5 reset n=${n}`);
    }
    chk((await sw()) <= width, `scrollWidth ${await sw()} > ${width}`);
    chk(errs.length === 0, 'page errors ' + errs.join(';'));
    await p.close();
  }
  // c0 без «меньше движения»: строки появляются плавно и в конце видны все
  { const p = await b.newPage({viewport: {width: 1280, height: 900}}), errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.route(/cdn\.jsdelivr\.net/, r => r.abort()); await p.goto('file://' + __dirname + '/preview.html'); await p.waitForTimeout(200);
    await p.evaluate(() => { const R = document.getElementById('sim-c0'), n = R.querySelector('.c0-n'), k = R.querySelector('.c0-k'); n.value = 6; n.dispatchEvent(new Event('input')); k.value = 3; k.dispatchEvent(new Event('input')); });
    await p.waitForTimeout(120);
    const mid = await p.evaluate(() => [...document.querySelectorAll('#sim-c0 .c0-row')].filter(g => g.getAttribute('opacity') !== null && +g.getAttribute('opacity') < 1).length);
    await p.waitForTimeout(1200);
    const end = await p.evaluate(() => [document.querySelectorAll('#sim-c0 .c0-row').length, document.querySelectorAll('#sim-c0 .c0-row[opacity], #sim-c0 .c0-row[transform]').length]);
    if (mid > 0) ok++; else bad.push(`c0 fade: no rows mid-animation`);
    if (end[0] === 20 && end[1] === 0) ok++; else bad.push(`c0 fade end: ${end}`);
    if (errs.length === 0) ok++; else bad.push('c0 fade page errors ' + errs.join(';'));
    console.log(`  анимация c0: в середине полупрозрачных строк ${mid} из 20, в конце ${end[0]} строк, с остаточной прозрачностью ${end[1]}`);
    await p.close(); }
  console.log(`DOM-проверок: ${ok + bad.length}, прошло: ${ok}, упало: ${bad.length}`); if (bad.length) console.log(bad.join('\n'));
  await b.close(); process.exit(bad.length ? 1 : 0);
})();
