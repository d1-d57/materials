/* ГЕЙТ ЯДРА — запускать после каждой правки src/dragon.js:
 *     node krivaya-drakona/sayt/check_dragon.js
 *
 * Проверяет ТОТ ЖЕ ФАЙЛ, который уедет в сайт, а не свою копию правил: урок
 * L4/check_page.js — гейты, вынимавшие функции и сверявшие их с эталоном,
 * проверяли МОДЕЛЬ, а не ФАЙЛ, и пропустили пустую страницу.
 *
 * Каждый пункт может провалиться: exit 1 и явное «что именно».
 */
'use strict';
const fs = require('fs'), path = require('path');
const SRC = path.join(__dirname, 'src', 'dragon.js');
const code = fs.readFileSync(SRC, 'utf8');

// исполняем файл целиком в своём скоупе и вытаскиваем то, чем пользуется сайт
const NAMES = ['word','wordByFolds','poly','polyAngles','rank','rotAbout','rot90','keyShape',
  'touches','mul1pi','isBlack','rowBlue','corner','corners','turnsLeft','birthStep',
  'dragCells','dragBoundary','cellQuad','sharedEdges','fit','bounds','roundPath','sharpD','lerp','lat'];
let API;
try {
  API = new Function(code + '\nreturn {' + NAMES.join(',') + '};')();
} catch (e) {
  console.error('❌ dragon.js не исполняется целиком: ' + e.message);
  process.exit(1);
}

let bad = 0;
function check(name, ok, detail) {
  console.log((ok ? '  ✅ ' : '  ❌ ') + name + (ok || !detail ? '' : ' — ' + detail));
  if (!ok) bad++;
}

const { word, poly, rank, mul1pi, isBlack, rowBlue, corner, corners, turnsLeft,
        dragCells, dragBoundary, cellQuad } = API;

console.log('ГЕЙТ src/dragon.js');

/* 1. геометрия дракона определена в файле ровно один раз */
const polyDefs = (code.match(/^function poly\(/gm) || []).length;
check('определение ломаной ровно одно (^function poly\\()', polyDefs === 1, 'нашлось ' + polyDefs);

/* 2. длина слова и ломаной */
let ok2 = true, why2 = '';
for (let n = 1; n <= 14; n++) {
  if (word(n).length !== Math.pow(2, n) - 1) { ok2 = false; why2 = 'слово ранга ' + n; break; }
  if (rank(n).length !== Math.pow(2, n) + 1) { ok2 = false; why2 = 'ломаная ранга ' + n; break; }
}
check('слово 2ⁿ−1 букв, ломаная 2ⁿ+1 вершин (ранги 1..14)', ok2, why2);

/* 3. вершины целые */
let ok3 = true;
for (let n = 1; n <= 12; n++)
  for (const p of rank(n))
    if (Math.abs(p[0] - Math.round(p[0])) > 1e-9 || Math.abs(p[1] - Math.round(p[1])) > 1e-9) ok3 = false;
check('вершины целые при угле 90° (ранги 1..12)', ok3);

/* 4. чётные вершины ранга n = ранг n−1, умноженный на (1+i) */
let ok4 = true, why4 = '';
for (let n = 2; n <= 14; n++) {
  const P = rank(n).map(p => [Math.round(p[0]), Math.round(p[1])]);
  const Q = mul1pi(rank(n - 1).map(p => [Math.round(p[0]), Math.round(p[1])]));
  const ev = P.filter((_, i) => i % 2 === 0);
  if (JSON.stringify(ev) !== JSON.stringify(Q)) { ok4 = false; why4 = 'ранг ' + n; break; }
}
check('чётные вершины ранга n = (1+i)·ранг n−1 (ранги 2..14)', ok4, why4);

/* 5. чёрная вершина ⟺ чётный индекс; чётное звено горизонтально */
let ok5a = true, ok5b = true;
for (let n = 2; n <= 14; n++) {
  const P = rank(n);
  for (let i = 0; i < P.length; i++) if (isBlack(P[i]) !== (i % 2 === 0)) ok5a = false;
  for (let i = 0; i + 1 < P.length; i++)
    if ((Math.abs(P[i][1] - P[i + 1][1]) < 1e-9) !== (i % 2 === 0)) ok5b = false;
}
check('чёрная вершина ⟺ чётная сумма координат ⟺ чётный индекс', ok5a);
check('чётное звено горизонтально, нечётное вертикально', ok5b);

/* 6. ПРАВИЛО СТРОК: уголок поворачивает налево ⟺ строка излома голубая */
let ok6 = true, why6 = '';
for (let n = 2; n <= 14; n++) {
  for (const [a, b, c] of corners(rank(n)))
    if (turnsLeft(a, b, c) !== rowBlue(b[1])) { ok6 = false; why6 = 'ранг ' + n; break; }
  if (!ok6) break;
}
check('уголок налево ⟺ строка излома голубая (ранги 2..14)', ok6, why6);

/* 7. ВОССТАНОВЛЕНИЕ УГОЛКА по одному звену — на всех звеньях всех рангов */
let seen = 0, wrong = 0, firstWrong = '';
for (let n = 2; n <= 14; n++) {
  const P = rank(n), C = corners(P);
  for (let i = 0; i + 1 < P.length; i++) {
    seen++;
    const r = corner(P[i], P[i + 1]);
    const want = C[Math.floor(i / 2)];
    if (JSON.stringify(r.corner) !== JSON.stringify(want)) {
      wrong++; if (!firstWrong) firstWrong = 'ранг ' + n + ', звено ' + i;
    }
    if (JSON.stringify(r.izlom) !== JSON.stringify(P[Math.floor(i / 2) * 2 + 1])) wrong++;
    if (JSON.stringify(r.other) === JSON.stringify(r.corner)) wrong++;   // кандидаты обязаны различаться
  }
}
check('уголок восстанавливается по ОДНОМУ звену: ' + seen + ' звеньев, расхождений ' + wrong,
      wrong === 0, firstWrong);

/* 8. все ЧЕТЫРЕ случая сцены 5в достижимы на ранге 6 и различимы */
const cases = new Map();
{ const P = rank(6);
  for (let i = 0; i + 1 < P.length; i++) {
    const r = corner(P[i], P[i + 1]);
    const k = (r.horiz ? 'гориз' : 'вертик') + '×' + (r.blue ? 'голубая' : 'белая');
    cases.set(k, (cases.get(k) || 0) + 1);
  } }
check('на ранге 6 все 4 случая: ' + [...cases.entries()].sort().map(e => e[0] + '=' + e[1]).join(', '),
      cases.size === 4);

/* 9. ОБЛАСТЬ: клеток ровно 2ⁿ и все различны (плитки не налезают) */
let ok9 = true, why9 = '';
for (let n = 1; n <= 13; n++) {
  const C = dragCells(n);
  if (C.length !== Math.pow(2, n)) { ok9 = false; why9 = 'ранг ' + n + ': клеток ' + C.length; break; }
  if (new Set(C.map(c => c.join(','))).size !== C.length) { ok9 = false; why9 = 'ранг ' + n + ': повтор клетки'; break; }
}
check('клеток области ровно 2ⁿ и ни одна не повторяется (ранги 1..13)', ok9, why9);

/* 10. центр клетки = середина звена: область лежит ровно на ломаной */
let ok10 = true;
for (let n = 1; n <= 12; n++) {
  const P = rank(n), C = dragCells(n);
  for (let i = 0; i + 1 < P.length; i++) {
    const mx = P[i][0] + P[i + 1][0], my = P[i][1] + P[i + 1][1];
    if (C[i][0] !== mx || C[i][1] !== my) ok10 = false;
  }
}
check('ключ клетки = удвоенная середина своего звена (ранги 1..12)', ok10);

/* 10-бис. ЧЕТЫРЕ ДРАКОНА не делят ни одного отрезка (утверждение сцены 6) */
{ const rows = [];
  let okShared = true;
  for (let n = 3; n <= 11; n++) {
    const d = API.sharedEdges(n);
    rows.push(n + ':' + d);
    if (d !== 0) okShared = false;
  }
  console.log('     общих отрезков у четырёх копий, ранги 3..11: ' + rows.join(' '));
  check('четыре дракона не делят ни одного отрезка (ранги 3..11)', okShared);
}

/* 11. ГРАНИЦА: считаем отношение и размерность — число обязано выйти 1,52 */
const bs = [];
for (let n = 4; n <= 12; n++) bs.push(dragBoundary(n).length);
const ratios = bs.slice(1).map((b, i) => b / bs[i]);
const dims = ratios.map(r => Math.log(r) / Math.log(Math.SQRT2));
const dLast = dims[dims.length - 1];
console.log('     сторон границы, ранги 4..12: ' + bs.join(', '));
console.log('     размерность по последнему шагу: ' + dLast.toFixed(4));
check('размерность границы сходится к 1,5236 (|d−1,5236| < 0,02 на ранге 12)',
      Math.abs(dLast - 1.5236) < 0.02, 'вышло ' + dLast.toFixed(4));

/* 12. ромб клетки: при t=1 площадь ровно ½, при t=0 — вырожден в звено */
{ const q = cellQuad([1, 0], 1);
  const area = Math.abs(q.reduce((s, p, i) => {
    const r = q[(i + 1) % 4]; return s + p[0] * r[1] - r[0] * p[1]; }, 0)) / 2;
  const q0 = cellQuad([1, 0], 0);
  check('клетка при t=1 имеет площадь ½, при t=0 вырождена',
        Math.abs(area - 0.5) < 1e-9 && Math.abs(q0[1][1] - q0[3][1]) < 1e-9, 'площадь ' + area);
}

console.log(bad === 0 ? '\n✅ ядро в порядке' : '\n❌ провалов: ' + bad);
process.exit(bad === 0 ? 0 : 1);
