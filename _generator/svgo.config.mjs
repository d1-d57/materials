// SVGO-конфиг фабрики презентаций (арка 9 · Р10 · 09-illustracii/DOK.md).
//
// ЗАЧЕМ. Все иллюстрации инлайнятся живыми <svg> в ОДИН финальный dist/index.html
// одновременно (реестр <template id="ill-*">). Два независимых id="waffle" в разных
// SVG тихо ломают друг друга через общий namespace документа (clipPath/gradient/mask
// цепляются к первому попавшемуся). Лечится ТОЛЬКО пер-файловым префиксом id на этапе
// нормализации — руками не углядеть. Прецедент: cone-title.svg → clipPath id="waffle".
//
// PINNED ВЕРСИЯ (не «latest» — детерминизм нормализации): svgo@3.3.2.
// Запуск (стем файла → префикс id):
//   npx svgo@3.3.2 --config _generator/svgo.config.mjs -i illustrations/foo.svg -o illustrations/foo.svg
//   npx svgo@3.3.2 --config _generator/svgo.config.mjs -f illustrations/ -o illustrations/   (пакетно)
// Префикс берётся из имени входного файла (info.path), поэтому каждый файл получает
// СВОЙ префикс автоматически; конфиг общий, префикс — пер-файловый.

export default {
  // многопроходность до неподвижной точки — стабильнее для сложной вёрстки
  multipass: true,
  // НЕ трогаем geometric precision агрессивно: канон-рисунки промерены пиксельно
  floatPrecision: 3,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          // viewBox обязателен (Р10: без него фолбэк на intrinsic size → обрезание при масштабе деки)
          removeViewBox: false,
          // не схлопывать id ВНУТРИ файла до prefixIds — иначе нечего префиксовать связно
          cleanupIds: false,
        },
      },
    },
    {
      // пер-файловый префикс id по stem входного файла (foo.svg → id "a" станет "foo__a")
      name: 'prefixIds',
      params: {
        delim: '__',
        prefix: (_node, info) => {
          const p = (info && info.path) || '';
          const base = p.split(/[\\/]/).pop() || 'svg';
          return base.replace(/\.svg$/i, '') || 'svg';
        },
      },
    },
  ],
};
