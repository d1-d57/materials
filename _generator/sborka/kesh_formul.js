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
// не отличает $$ от $), внутри ДВУХ разделов карточки — "## Текст слайда — сжато"
// и "## Математика — развёрнуто"; граница раздела та же, что
// _generator/sborka/bloki.py: _split_sections (^##\s+(.+?)\s*$ до следующего
// такого заголовка).
//
// Раздел «Математика» добавлен 2026-08-12: прежде он не сканировался с
// обоснованием «не попадает на экран», и для деки это верно — но `lenta.py`
// показывает его двумя вкладками из трёх, и на первой же ленте Л2 вышло 362
// ⟦MISSING-MATH⟧. Причина двойная, обе лечатся здесь: формул этого раздела в
// кэше не было ВОВСЕ, а сами они написаны в display-виде $$…$$, на котором
// inline-регексп рендерера ловит `$x` и сбивает парность — после чего между
// формулами захватывается обычный текст (17 обломков → 133 ложных «формулы»).
// Поэтому $$…$$ приводится к $…$ ТЕМ ЖЕ ходом и здесь, и в `lenta.py`
// (_normalize_display): кэш и рендерер обязаны видеть один и тот же tex.
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
const MATEM_HEADING = 'Математика — развёрнуто';
const HEADINGS = [TEKST_HEADING, MATEM_HEADING];
const SECTION_RE = /^##\s+(.+?)\s*$/gm;
const FORMULA_RE = /\$(.+?)\$/g;

// $$tex$$ → $tex$: inline-регексп рендерера display-обёртку не знает.
function normalizeDisplay(s) {
  return s.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => '$' + tex.trim() + '$');
}

function extractSection(raw, heading) {
  const matches = [...raw.matchAll(SECTION_RE)];
  for (let i = 0; i < matches.length; i++) {
    if (matches[i][1].trim() === heading) {
      const start = matches[i].index + matches[i][0].length;
      const end = i + 1 < matches.length ? matches[i + 1].index : raw.length;
      return normalizeDisplay(raw.slice(start, end));
    }
  }
  return '';
}

const sids = fs.readdirSync(slajdyDir).filter(
  (n) => fs.existsSync(path.join(slajdyDir, n, 'slaid.md')));

const formulas = new Map();  // tex → [sid, ...] (для сообщения об ошибке — где искать)
for (const sid of sids) {
  const raw = fs.readFileSync(path.join(slajdyDir, sid, 'slaid.md'), 'utf8');
  for (const heading of HEADINGS) {
    for (const m of extractSection(raw, heading).matchAll(FORMULA_RE)) {
      const tex = m[1];
      if (!formulas.has(tex)) formulas.set(tex, []);
      formulas.get(tex).push(sid);
    }
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
console.log('карточек: ' + sids.length + ', уникальных формул в разделах «'
            + HEADINGS.join('» + «') + '»: ' + formulas.size);
console.log('отрендерено: ' + Object.keys(cache).length + ' из ' + formulas.size);
if (bad.length) {
  console.log('НЕ отрендерено ' + bad.length + ':');
  for (const [t, m] of bad) {
    console.log('  $' + t + '$  → ' + m + '  (' + formulas.get(t).join(', ') + ')');
  }
}
process.exit(bad.length ? 1 : 0);
