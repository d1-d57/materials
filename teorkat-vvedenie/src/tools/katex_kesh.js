/*
 * formuly.json → src/math/katex.json (кэш {tex → готовый HTML}, Р7).
 *
 *   node teorkat-vvedenie/src/tools/katex_kesh.js
 *
 * Почему не `_generator/harvest_katex.py`: тот по своему докстрингу вынимает формулы
 * из УЖЕ отрендеренной колоды («Новые формулы — задача будущего math-арки»), а этот
 * дек greenfield — вынимать нечего. KaTeX берётся установленным ЧУЖИМ путём и только
 * НА ЧТЕНИЕ; в него ничего не пишется (зона захода — teorkat-vvedenie/src/).
 *
 * Формат значения — ровно то, что генератор подставляет вместо $tex$ и что потом
 * вынимает harvest_katex.py: <span class="katex">…</span> с annotation-исходником
 * внутри, то есть output:'htmlAndMathml'. Иначе round-trip кэша ломается.
 */
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '../../..');
const KATEX = path.join(REPO, 'lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/src/tools/node_modules/katex');
const katex = require(KATEX);

const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, 'formuly.json'), 'utf8'));
const cache = {};
const bad = [];

for (const j of jobs) {
  try {
    cache[j.tex] = katex.renderToString(j.tex, {
      displayMode: j.display,
      throwOnError: true,
      strict: 'ignore',
      output: 'htmlAndMathml',
    });
  } catch (e) {
    bad.push([j.tex, e.message.split('\n')[0]]);
  }
}

const outDir = path.resolve(__dirname, '../math');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'katex.json'),
  JSON.stringify(cache, null, 0), 'utf8');

console.log('katex', katex.version || '(версия не объявлена)');
console.log('отрендерено: ' + Object.keys(cache).length + ' из ' + jobs.length);
if (bad.length) {
  console.log('НЕ отрендерено ' + bad.length + ':');
  for (const [t, m] of bad) console.log('  $' + t + '$  → ' + m);
}
process.exit(bad.length ? 1 : 0);
