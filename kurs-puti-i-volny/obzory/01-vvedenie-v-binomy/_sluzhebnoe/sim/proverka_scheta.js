// Проверка счёта, часть 1 (node): генераторы lib.js против независимой формулы n!/(k!(n-k)!).
// Запуск: node proverka_scheta.js
global.window = global; require('./lib.js'); const K = window.SimK;
const fact = n => n <= 1 ? 1 : n * fact(n - 1), Cf = (n, k) => fact(n) / (fact(k) * fact(n - k));
let ok = 0, bad = [];
const chk = (c, msg) => { if (c) ok++; else bad.push(msg); };
const keys = ws => ws.map(K.key);
const isSet = (ws, n, k) => { const s = new Set(keys(ws)); return s.size === ws.length && ws.every(w => w.length === n && w.reduce((a, b) => a + b, 0) === k); };
// c1: n 2..6, k 0..n — слова и отражение-биекция
for (let n = 2; n <= 6; n++) for (let k = 0; k <= n; k++) {
  const L = K.words(n, k), R = K.words(n, n - k);
  chk(L.length === Cf(n, k) && K.C(n, k) === Cf(n, k), `c1 count n=${n} k=${k}`);
  chk(isSet(L, n, k) && isSet(R, n, n - k), `c1 set n=${n} k=${k}`);
  const Rk = new Set(keys(R)), img = new Set(L.map(w => K.key(K.flip(w))));
  chk(img.size === L.length && [...img].every(x => Rk.has(x)), `c1 bijection n=${n} k=${k}`);
  if (2 * k === n) chk(L.every(w => K.key(K.flip(w)) !== K.key(w)), `c1 no fixed word n=${n}`);
}
// c2: n 2..6, k 1..n-1 — разъезд по первой цифре, хвосты = все слова длины n-1
for (let n = 2; n <= 6; n++) for (let k = 1; k < n; k++) {
  const W = K.words(n, k), one = W.filter(w => w[0] === 1).map(w => w.slice(1)), zero = W.filter(w => w[0] === 0).map(w => w.slice(1));
  chk(one.length === Cf(n - 1, k - 1) && zero.length === Cf(n - 1, k) && W.length === one.length + zero.length, `c2 counts n=${n} k=${k}`);
  chk(keys(one).sort().join() === keys(K.words(n - 1, k - 1)).sort().join(), `c2 tails-1 n=${n} k=${k}`);
  chk(keys(zero).sort().join() === keys(K.words(n - 1, k)).sort().join(), `c2 tails-0 n=${n} k=${k}`);
}
// c3: n 3..6, m 2..n-1 — карточки и три раскладки
let maxCards = 0;
for (let n = 3; n <= 6; n++) for (let m = 2; m < n; m++) {
  const k = m - 1, cs = K.cards(n, m), N = cs.length; maxCards = Math.max(maxCards, N);
  chk(N === m * Cf(n, m) && N === n * Cf(n - 1, k) && N === (n - k) * Cf(n, k), `c3 total n=${n} m=${m}`);
  chk(new Set(cs.map(c => K.key(c.team) + '/' + c.cap)).size === N && cs.every(c => c.team[c.cap] === 1), `c3 distinct n=${n} m=${m}`);
  const ord = c => { const t = c.team.slice(); t[c.cap] = 0; return K.key(t); };
  [[c => c.cap, n, Cf(n - 1, k)], [c => K.key(c.team), Cf(n, m), m], [ord, Cf(n, k), n - k]].forEach(([f, S, z], md) => {
    const g = K.groups(cs, f); chk(g.length === S && g.every(x => x.length === z), `c3 mode${md} n=${n} m=${m}`);
  });
}
// c4: n 3..10 — упорядоченные пары и склейка
for (let n = 3; n <= 10; n++) {
  const a = K.arrows(n), un = new Set(a.map(([i, j]) => Math.min(i, j) + '-' + Math.max(i, j)));
  chk(a.length === n * (n - 1) && new Set(a.map(p => p.join())).size === a.length, `c4 arrows n=${n}`);
  chk(un.size === Cf(n, 2) && un.size * 2 === a.length, `c4 segments n=${n}`);
  chk(a.every(([i, j]) => a.some(([p, q]) => p === j && q === i)), `c4 reverse n=${n}`);
}
// c5: n 2..8 — лесенка, отражение, сдвиг: прямоугольник (n-1)×n без наложений и дыр
for (let n = 2; n <= 8; n++) {
  const P = K.ladder(n), M = n * (n - 1) / 2, rc = a => a[0] + ',' + a[1];
  let sum = 0; for (let i = n - 1; i >= 1; i--) sum += i;
  chk(P.length === M && P.length === Cf(n, 2) && sum === M, `c5 count n=${n}`);
  chk(new Set(P.map(p => p.i + '-' + p.j)).size === M && P.every(p => 1 <= p.i && p.i < p.j && p.j <= n), `c5 pairs n=${n}`);
  chk(P.every(p => p.u[0] === p.i && p.u[1] === p.j && p.d1[0] === p.j && p.d1[1] === p.i && p.d2[0] === p.j - 1 && p.d2[1] === p.i), `c5 positions n=${n}`);
  // верхняя лесенка — ровно клетки r<c, по n-r в строке r
  const up = P.map(p => rc(p.u)), want0 = []; for (let r = 1; r <= n; r++) for (let c = r + 1; c <= n; c++) want0.push(r + ',' + c);
  chk(up.slice().sort().join() === want0.sort().join(), `c5 ladder n=${n}`);
  // две лесенки — все клетки вне диагонали, n(n-1), без повторов
  const two = up.concat(P.map(p => rc(p.d1))), want1 = []; for (let r = 1; r <= n; r++) for (let c = 1; c <= n; c++) if (r !== c) want1.push(r + ',' + c);
  chk(new Set(two).size === two.length && two.length === n * (n - 1) && two.slice().sort().join() === want1.sort().join(), `c5 two ladders n=${n}`);
  // после сдвига — прямоугольник строк 1..n-1 × столбцов 1..n: без наложений, без дыр, ряд n и диагональ ничем не заняты сверх прямоугольника
  const bar = up.concat(P.map(p => rc(p.d2))), want2 = []; for (let r = 1; r <= n - 1; r++) for (let c = 1; c <= n; c++) want2.push(r + ',' + c);
  chk(new Set(bar).size === bar.length, `c5 no overlap n=${n}`);
  chk(bar.length === (n - 1) * n && bar.slice().sort().join() === want2.sort().join(), `c5 no holes n=${n}`);
  for (let r = 1; r <= n - 1; r++) { const lo = P.filter(p => p.d2[0] === r).length, hi = P.filter(p => p.u[0] === r).length; chk(lo === r && hi === n - r, `c5 row ${r} n=${n}: ${lo}+${hi}`); }
}
// c0: n 1..6, k 0..n — все варианты выбора: число строк, различие кодов, k единиц, набор ↔ код, словарный порядок
// независимо: k-подмножества {1..n} в лексикографическом порядке наборов; их коды должны идти по убыванию двоичного числа
const combos = (n, k, from = 1) => k === 0 ? [[]] : from > n ? [] : combos(n, k - 1, from + 1).map(c => [from, ...c]).concat(combos(n, k, from + 1));
const codeOf = (set, n) => Array.from({length: n}, (_, i) => set.includes(i + 1) ? 1 : 0);
let c0rows = 0;
for (let n = 1; n <= 6; n++) for (let k = 0; k <= n; k++) {
  const W = K.words(n, k), S = W.map(K.nabor), ref = combos(n, k); c0rows += W.length;
  chk(W.length === Cf(n, k) && ref.length === Cf(n, k), `c0 count n=${n} k=${k}: ${W.length}`);
  chk(new Set(keys(W)).size === W.length, `c0 distinct n=${n} k=${k}`);
  chk(W.every(w => w.length === n && w.every(b => b === 0 || b === 1) && w.reduce((a, b) => a + b, 0) === k), `c0 k ones n=${n} k=${k}`);
  chk(S.every((s, i) => s.length === k && s.every((x, j) => (j === 0 || s[j - 1] < x) && x >= 1 && x <= n) && K.key(codeOf(s, n)) === K.key(W[i]) && s.every(x => W[i][x - 1] === 1)), `c0 set<->code n=${n} k=${k}`);
  chk(keys(W).every((x, i, a) => i === 0 || a[i - 1] > x), `c0 code order n=${n} k=${k}`);
  chk(S.map(s => s.join()).join('|') === ref.map(s => s.join()).join('|'), `c0 set order n=${n} k=${k}`);
}
chk(K.key(K.words(4, 2).map(K.key)) === '110010101001011001010011', 'c0 order n=4 k=2: 1100,1010,1001,0110,0101,0011');
console.log(`c0: строк во всех 27 положениях ползунков ${c0rows} (= сумма 2^n по n=1..6 = 126)`);
chk(c0rows === 126, 'c0 total rows');
console.log(`проверок: ${ok + bad.length}, прошло: ${ok}, упало: ${bad.length}; максимум карточек в c3: ${maxCards}`);
if (bad.length) { console.log(bad.join('\n')); process.exit(1); }
