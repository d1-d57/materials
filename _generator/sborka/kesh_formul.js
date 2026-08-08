#!/usr/bin/env node
// <лекция>/slajdy/<sid>/slaid.md → <лекция>/math/katex.json (кэш {tex: готовый HTML}).
// Вход — КАРТОЧКИ, не formuly.json (заказчик: `teorkat-vvedenie/src/tools/katex_kesh.js`
// читает рукописный список формул — гарантированное расхождение с текстом на следующей
// же правке). Здесь список формул ВЫЧИСЛЯЕТСЯ из тех же карточек, что идут в дек.
//
//   node _generator/sborka/kesh_formul.js <лекция>
//   node _generator/sborka/kesh_formul.js teorkat-vvedenie/L2
//
// Формулы ищутся ТОЧНО там же и ТЕМ ЖЕ регекспом, что их найдёт рендерер
// (render_inline_md, _generator/build_deck.py — /\$(.+?)\$/, без DOTALL,
// не отличает $$ от $), и ТОЛЬКО внутри раздела "## Текст слайда — сжато"
// каждой карточки — граница раздела та же, что _generator/sborka/bloki.py:
// _split_sections (^##\s+(.+?)\s*$ до следующего такого заголовка). Раздел
// «Математика — развёрнуто» НЕ сканируется: он не попадает на экран
// (bloki.render_section_markdown берёт только раздел «Текст слайда — сжато»).
//
// Рендерер — вендоренный _generator/vendor/katex/katex.min.js (в git, не
// node_modules чужой лекции: тот не отслеживается, и git clean стирает
// рендер для ВСЕЙ фабрики молча — 153 формулы «пропадают» без единой ошибки).
// Формат значения — output:'htmlAndMathml', тот же, что уже пишет
// teorkat-vvedenie/src/tools/katex_kesh.js — иначе round-trip
// _generator/harvest_katex.py ломается.
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '../..');
const katex = require(path.join(REPO, '_generator/vendor/katex/katex.min.js'));

const lekcijaArg = process.argv[2];
if (!lekcijaArg) {
  console.error('использование: node kesh_formul.js <лекция>');
  process.exit(2);
}
const lekcija = path.resolve(REPO, lekcijaArg);
const slajdyDir = path.join(lekcija, 'slajdy');

const TEKST_HEADING = 'Текст слайда — сжато';
const SECTION_RE = /^##\s+(.+?)\s*$/gm;
const FORMULA_RE = /\$(.+?)\$/g;

function extractTekstSection(raw) {
  const matches = [...raw.matchAll(SECTION_RE)];
  for (let i = 0; i < matches.length; i++) {
    if (matches[i][1].trim() === TEKST_HEADING) {
      const start = matches[i].index + matches[i][0].length;
      const end = i + 1 < matches.length ? matches[i + 1].index : raw.length;
      return raw.slice(start, end);
    }
  }
  return '';
}

const sids = fs.readdirSync(slajdyDir).filter(
  (n) => fs.existsSync(path.join(slajdyDir, n, 'slaid.md')));

const formulas = new Map();  // tex → [sid, ...] (для сообщения об ошибке — где искать)
for (const sid of sids) {
  const raw = fs.readFileSync(path.join(slajdyDir, sid, 'slaid.md'), 'utf8');
  const tekst = extractTekstSection(raw);
  for (const m of tekst.matchAll(FORMULA_RE)) {
    const tex = m[1];
    if (!formulas.has(tex)) formulas.set(tex, []);
    formulas.get(tex).push(sid);
  }
}

const cache = {};
const bad = [];
for (const tex of formulas.keys()) {
  try {
    cache[tex] = katex.renderToString(tex, {
      displayMode: false,
      throwOnError: true,
      strict: 'ignore',
      output: 'htmlAndMathml',
    });
  } catch (e) {
    bad.push([tex, e.message.split('\n')[0]]);
  }
}

const outDir = path.join(lekcija, 'math');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'katex.json'), JSON.stringify(cache, null, 0), 'utf8');

console.log('katex ' + (katex.version || '(версия не объявлена)'));
console.log('карточек: ' + sids.length + ', уникальных формул в разделе «' + TEKST_HEADING + '»: ' + formulas.size);
console.log('отрендерено: ' + Object.keys(cache).length + ' из ' + formulas.size);
if (bad.length) {
  console.log('НЕ отрендерено ' + bad.length + ':');
  for (const [t, m] of bad) {
    console.log('  $' + t + '$  → ' + m + '  (' + formulas.get(t).join(', ') + ')');
  }
}
process.exit(bad.length ? 1 : 0);
