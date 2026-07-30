
/* === lab.core.js (вшито сборкой) ===============================================
   ЛАБОРАТОРИЯ дека «Внутри треугольника Паскаля».

   Устройство скопировано с buffon/src/sims/lab.core.js (реестр + активация по
   показу слайда + проброс сцен через onScene + «в покое = слайд»), но БЕЗ его
   экспериментов: там в ядре зашиты иглы, треугольники и фазовый прямоугольник —
   к Паскалю они отношения не имеют, и тащить их значило бы возить чужой дек.
   Здесь ядро тонкое, а все опыты — отдельными файлами в sims/ext/.

   Контракт (тот же, что у эталона):
     · <canvas data-sim="<kind>"> внутри .panel;
     · опыт регистрируется как window.LabKinds[kind] = function (cv, slide) {…};
     · у опыта есть draw(); необязательные reset(seed), onScene(k), settle();
     · при КАЖДОМ входе на слайд опыт пересоздаётся заново: свежая случайность
       (правило автора), затем settle() — и слайд в покое выглядит законченным.

   Ловушки, уже оплаченные эталоном и здесь соблюдённые:
     · в файле опыта НЕТ локального core — только window.LabCore;
     · буфер канваса меряется ПОСЛЕ вёрстки (measure), иначе круги станут овалами;
     · кнопки — текстовые глифы ▸ ▸▸ ❚❚ ↺, не эмодзи.
   ============================================================================ */
(function () {
  'use strict';

  function tokens() {
    var cs = getComputedStyle(document.documentElement);
    var t = function (n, fb) { return (cs.getPropertyValue(n) || fb).trim(); };
    return {
      paper: t('--paper', '#e6e5e1'), board: t('--board', '#a7c2cb'),
      card: t('--card', '#fff'), ink: t('--ink', '#333'),
      brick: t('--brick', '#bf5b4f'), steel: t('--steel', '#8195ad'),
      mustard: t('--mustard', '#c9a23c'), rule: t('--rule', '#c3cedd'),
      blush: t('--blush', '#f0e2de')
    };
  }

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- базовый опыт: буфер, размер, палитра, кнопки ---------- */
  function Lab(canvas, opts) {
    this.cv = canvas;
    this.o = opts || {};
    this.C = tokens();
    this.scene = 1;
    this.rng = mulberry32((this.o.seed || 1) + 1);
    this.ctx = canvas.getContext('2d');
    this.measure();
  }
  Lab.prototype.measure = function () {
    var w = this.cv.clientWidth, h = this.cv.clientHeight;
    if (!w || !h) return false;                    // вёрстка ещё не готова
    var dpr = Math.min(devicePixelRatio || 1, 2);
    if (w === this.W && h === this.H && this.cv.width) return true;
    this.W = w; this.H = h;
    this.cv.width = Math.round(w * dpr);
    this.cv.height = Math.round(h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return true;
  };
  Lab.prototype.clear = function () {
    var c = this.ctx;
    c.setTransform(Math.min(devicePixelRatio || 1, 2), 0, 0,
                   Math.min(devicePixelRatio || 1, 2), 0, 0);
    c.clearRect(0, 0, this.W, this.H);
    c.fillStyle = this.C.card;
    c.fillRect(0, 0, this.W, this.H);
  };
  /* подпись-МЕТКА внутри канваса: число или одна буква, шрифт дека */
  Lab.prototype.label = function (s, x, y, size, color, align, weight) {
    var c = this.ctx;
    c.save();
    c.fillStyle = color || this.C.ink;
    c.font = (weight || '700') + ' ' + (size || 17) +
             'px "Glacial Indifference","Noto Sans",sans-serif';
    c.textAlign = align || 'center';
    c.textBaseline = 'middle';
    c.fillText(s, x, y);
    c.restore();
  };
  Lab.prototype.onScene = function (k) { this.scene = k; this.draw(); };
  Lab.prototype.settle = function () { this.draw(); };
  Lab.prototype.stop = function () {
    if (this._raf) { cancelAnimationFrame(this._raf); this._raf = null; }
  };
  /* анимация: step(t) вызывается каждый кадр, пока не вернёт false */
  Lab.prototype.animate = function (step) {
    this.stop();
    if (REDUCED) { while (step(1e9) !== false) {} return; }
    var self = this, t0 = null;
    this._raf = requestAnimationFrame(function tick(ts) {
      if (t0 === null) t0 = ts;
      if (step(ts - t0) === false) { self._raf = null; return; }
      self._raf = requestAnimationFrame(tick);
    });
  };
  /* строка кнопок-глифов в углу панели */
  Lab.prototype.row = function (buttons) {
    var host = this.cv.parentElement;
    if (!host || host.querySelector('.lab-row')) return;
    host.style.overflow = 'visible';
    var row = document.createElement('div');
    row.className = 'lab-row';
    buttons.forEach(function (b) {
      var el = document.createElement('button');
      el.textContent = b.glyph;
      el.title = b.title || '';
      el.addEventListener('click', function (e) { e.stopPropagation(); b.act(); });
      row.appendChild(el);
    });
    host.appendChild(row);
    this._row = row;
  };

  /* ---------- реестр и активация по показу слайда ---------- */
  var live = {};
  window.LabCore = { Lab: Lab, tokens: tokens, mulberry32: mulberry32, REDUCED: REDUCED };
  window.LabKinds = window.LabKinds || {};
  window.LAB = live;

  function activate(slide, justShown) {
    var k = 1, m = slide.className.match(/scene-(\d+)/);
    if (m) k = +m[1];
    slide.querySelectorAll('canvas[data-sim]').forEach(function (cv) {
      var kind = cv.dataset.sim, id = slide.id + ':' + kind;
      if (justShown && live[id]) {                 /* уходим со слайда — состояние не храним */
        if (live[id].stop) live[id].stop();
        var row = cv.parentElement && cv.parentElement.querySelector('.lab-row');
        if (row) row.remove();
        delete live[id];
      }
      if (!live[id]) {
        var maker = window.LabKinds[kind];
        if (!maker) return;                        /* опыт ещё не написан — панель просто пуста */
        var exp = maker(cv, slide);
        if (!exp) return;
        live[id] = exp;
      }
      var e = live[id];
      if (e.measure) e.measure();                  /* гонка инициализации: мерим по вёрстке */
      if (justShown && e.settle) e.settle();
      if (e.onScene) e.onScene(k);
    });
  }

  function watch() {
    document.querySelectorAll('.slide').forEach(function (s) {
      if (!s.querySelector('canvas[data-sim]')) return;
      var vis = function () { return s.style.display !== 'none'; };
      new MutationObserver(function () {
        var v = vis(), js = v && !s._simVis;
        s._simVis = v;
        if (v) activate(s, js);
      }).observe(s, { attributes: true, attributeFilter: ['style', 'class'] });
      s._simVis = vis();
      if (s._simVis) activate(s, true);
    });
    addEventListener('resize', function () {
      Object.keys(live).forEach(function (id) {
        var e = live[id];
        if (e.measure && e.measure() && e.draw) e.draw();
      });
    });
  }
  addEventListener('load', watch);
})();
