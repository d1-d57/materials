
/* === lab.js (вшито сборкой) === */
/* ============================================================
   ЛАБОРАТОРИЯ (M3): живые эксперименты в панелях дека.
   Дизайн: SIM-DESIGN.md. Стиль: ILLUSTRATION-LANGUAGE.md (токены!).
   Контракт: canvas[data-sim="…"] внутри .panel; в покое = слайд
   (seed + автопрогон до эталонного N); сцены пробрасываются в onScene.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- палитра из токенов (перекраска дека красит и лабораторию) ---------- */
  function tokens() {
    var cs = getComputedStyle(document.documentElement);
    var t = function (n, fb) { return (cs.getPropertyValue(n) || fb).trim(); };
    return {
      card: t('--card', '#fff'), ink: t('--ink', '#333'),
      rule: t('--rule', '#c3cedd'), steel: t('--steel', '#8195ad'),
      brick: t('--brick', '#bf5b4f'), mustard: t('--mustard', '#c9a23c'),
      cgreen: t('--cgreen', '#7ea474'), corange: t('--corange', '#d98e4a'),
      pastels: [t('--p1', '#b18ec0'), t('--p2', '#7b9bd1'), t('--p3', '#8fae72'),
                t('--p4', '#d9b349'), t('--p5', '#c96a55')]
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

  /* ---------- базовый эксперимент: аккумулятор + приборка + строка ---------- */
  function Lab(canvas, opts) {
    this.cv = canvas; this.o = opts || {};
    var box = canvas.parentElement.getBoundingClientRect; // размеры из вёрстки
    this.W = canvas.clientWidth  || parseFloat(canvas.getAttribute('width'))  || 800;
    this.H = canvas.clientHeight || parseFloat(canvas.getAttribute('height')) || 500;
    var dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = this.W * dpr; canvas.height = this.H * dpr;
    this.ctx = canvas.getContext('2d'); this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.off = document.createElement('canvas');
    this.off.width = canvas.width; this.off.height = canvas.height;
    this.octx = this.off.getContext('2d'); this.octx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.T = this.o.spacing || 90;
    this.seed = this.o.seed || 6143;
    this.target = this.o.autoTarget || 1000;
    this.speed = 1; this.running = false;
    this.spark = [];                 // история доли (главный график)
    this.spark2 = null;              // вторая серия (сравнение статистик)
    this.sparkEvery = this.o.sparkEvery || 5;
    this.level = this.o.level;       // риска уровня на спарклайне (напр. 2/π)
    this.C = tokens();
  }
  Lab.prototype.resetState = function () { this.n = 0; this.hit = 0; this.spark = []; };
  Lab.prototype.reset = function (seed) {
    this.rng = mulberry32(seed != null ? seed : this.seed);
    this.resetState();
    var c = this.octx;
    c.clearRect(0, 0, this.W, this.H);
    c.fillStyle = this.C.card; c.fillRect(0, 0, this.W, this.H);
    if (this.drawBase) this.drawBase(c);
    this.draw();
  };
  Lab.prototype.lines = function (c) {        // разлиновка-пол
    c.strokeStyle = this.C.rule; c.lineWidth = 1.25; c.beginPath();
    for (var y = this.T / 2; y < this.H; y += this.T) { c.moveTo(0, y + .5); c.lineTo(this.W, y + .5); }
    c.stroke();
  };
  Lab.prototype.throwN = function (n, flash) {
    for (var i = 0; i < n; i++) {
      var hit = this.throwOne(this.octx);     // эксперимент рисует объект, возвращает исход
      this.n++; if (hit) this.hit++;
      if (this.n % this.sparkEvery === 0) this.spark.push(this.hit / this.n);
    }
    this.draw();
  };
  Lab.prototype.draw = function () {
    var c = this.ctx;
    c.clearRect(0, 0, this.W, this.H);
    c.drawImage(this.off, 0, 0, this.W, this.H);
    if (this.o.dash !== false) this.dashboard(c);
    if (this.drawTop) this.drawTop(c);        // интерактивный слой поверх
  };
  /* приборная карточка: N, счётчики, столбик долей, спарклайн */
  /* док-панель (ревью автора): во всю ширину канваса; цифры слева,
     БОЛЬШОЙ график доли — главное; кнопки-иконки рисует row() поверх */
  /* док-панель: на широких — цифры слева + график; на узких (compact) —
     вертикально: строка цифр → график во всю ширину → кнопки снизу */
  Lab.prototype.dashboard = function (c) {
    var compact = this.o.compact || this.W < 560;
    var h = compact ? 122 : 112, y0 = this.H - h;
    c.fillStyle = this.C.card; c.globalAlpha = .97;
    c.fillRect(0, y0, this.W, h); c.globalAlpha = 1;
    c.strokeStyle = this.C.rule; c.lineWidth = 1;
    c.beginPath(); c.moveTo(0, y0 + .5); c.lineTo(this.W, y0 + .5); c.stroke();
    var gx, gw, gy, gh;
    if (compact) {
      /* строка цифр: N · hit · miss · доля */
      c.textAlign = 'left'; c.textBaseline = 'alphabetic';
      var bx = 12, by = y0 + 22;
      c.fillStyle = this.C.ink; c.font = '700 17px "Courier Prime",monospace';
      c.fillText(String(this.n), bx, by); bx += c.measureText(String(this.n)).width + 10;
      c.font = '15px "Courier Prime",monospace';
      c.fillStyle = this.C.brick; c.fillText(String(this.hit), bx, by);
      bx += c.measureText(String(this.hit)).width + 10;
      c.fillStyle = this.C.steel; c.fillText(String(this.n - this.hit), bx, by);
      if (this.n) {
        c.fillStyle = this.C.ink; c.textAlign = 'right';
        c.fillText((this.hit / this.n).toFixed(3), this.W - 12, by);
        c.textAlign = 'left';
      }
      gx = 12; gw = this.W - 24; gy = y0 + 32; gh = h - 32 - 44; // низ — кнопкам
    } else {
      var leftW = 140;
      c.textAlign = 'left'; c.fillStyle = this.C.ink;
      c.font = '700 24px "Courier Prime",monospace';
      c.fillText(String(this.n), 14, y0 + 30);
      c.font = '15px "Courier Prime",monospace';
      c.fillStyle = this.C.brick; c.fillText(String(this.hit), 14, y0 + 52);
      c.fillStyle = this.C.steel; c.fillText(String(this.n - this.hit), 14, y0 + 71);
      if (this.n) {
        c.fillStyle = this.C.ink; c.font = '14px "Courier Prime",monospace';
        c.fillText((this.hit / this.n).toFixed(3), 14, y0 + h - 10);
      }
      gx = leftW; gw = this.W - gx - 158; gy = y0 + 10; gh = h - 20;
    }
    var lo = this.o.sparkLo != null ? this.o.sparkLo : .4,
        hi = this.o.sparkHi != null ? this.o.sparkHi : .9;
    var yOf = function (v) {
      return gy + gh - (Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo) * gh;
    };
    c.strokeStyle = this.C.rule; c.lineWidth = 1;
    c.strokeRect(gx + .5, gy + .5, gw - 1, gh - 1);
    if (this.level) {
      c.strokeStyle = this.C.mustard; c.lineWidth = 2.5; c.beginPath();
      c.moveTo(gx, yOf(this.level)); c.lineTo(gx + gw, yOf(this.level)); c.stroke();
    }
    var draw1 = function (arr, color, width) {
      if (arr.length < 2) return;
      c.strokeStyle = color; c.lineWidth = width; c.beginPath();
      for (var i = 0; i < arr.length; i++) {
        var px = gx + 3 + (i / (arr.length - 1)) * (gw - 6);
        i ? c.lineTo(px, yOf(arr[i])) : c.moveTo(px, yOf(arr[i]));
      }
      c.stroke();
    };
    draw1(this.spark, this.C.brick, 2.2);
    if (this.spark2 && this.spark2.length) draw1(this.spark2, this.C.steel, 2.2);
    this._dock = { y0: y0, h: h, compact: compact };
  };
  /* автопрогон: живо до target, потом стоп; скорость = множитель */
  Lab.prototype.play = function () {
    if (this.running) return; this.running = true;
    var self = this, last = 0;
    (function tick(ts) {
      if (!self.running) return;
      if (self.n >= self.target && !self.o.endless) { self.running = false; self.syncRow(); return; }
      if (ts - last > 80) {
        var batch = self.n < 40 ? 1 : 4 * self.speed * self.speed; // ×1→4, ×4→64, ×16→1024… мягко
        self.throwN(Math.min(batch, Math.max(1, self.target * 4 - self.n)));
        last = ts;
      }
      requestAnimationFrame(tick);
    })(0);
    this.syncRow();
  };
  Lab.prototype.pause = function () { this.running = false; this.syncRow(); };
  /* кнопки-иконки на док-панели: ▶ пуск, ⏸ пауза, ⏩ быстро, ↺ заново */
  Lab.prototype.row = function (extra) {
    var host = this.cv.parentElement; host.style.overflow = 'visible';
    var row = document.createElement('div');
    row.className = 'lab-row';
    var self = this;
    function btn(label, title, act, cls) {
      var b = document.createElement('button');
      b.textContent = label; b.title = title; if (cls) b.className = cls;
      b.addEventListener('click', function (e) { e.stopPropagation(); act(b); });
      row.appendChild(b); return b;
    }
    this._play = btn('▸', 'вперёд', function () {
      if (self.running && self.speed === 1) { self.pause(); return; }
      self.speed = 1; self.target = Math.max(self.target, self.n + 600); self.play();
    });
    this._fast = btn('▸▸', 'в восемь раз быстрее', function () {
      if (self.running && self.speed > 1) { self.pause(); return; }
      self.speed = 8; self.target = Math.max(self.target, self.n + 5000); self.play();
    });
    btn('↺', 'заново', function () {
      self.pause(); self.speed = 1; self.target = self.o.autoTarget || 1000;
      self.reset(); REDUCED ? self.throwN(self.target) : self.play();
    });
    (extra || []).forEach(function (e) {
      var b = btn(e.label, e.title || '', function (bb) { e.act(bb); }, e.cls || '');
      e._btn = b;
    });
    host.appendChild(row);
    this._row = row; this.syncRow();
  };
  Lab.prototype.syncRow = function () {
    if (!this._row) return;
    if (this._play) this._play.textContent = (this.running && this.speed === 1) ? '❚❚' : '▸';
    if (this._fast) this._fast.textContent = (this.running && this.speed > 1) ? '❚❚' : '▸▸';
  };
  /* пере-замер размеров при ПОКАЗЕ (init-гонка: конструктор мерил до вёрстки) */
  Lab.prototype.measure = function () {
    var w = this.cv.clientWidth, h = this.cv.clientHeight;
    if (!w || !h) return;                         // вёрстка ещё не готова — не трогаем
    if (w === this.W && h === this.H) return;     // размер тот же — буферы не пересоздаём
    this.W = w; this.H = h;
    var dpr = Math.min(devicePixelRatio || 1, 2);
    this.cv.width = w * dpr; this.cv.height = h * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.off.width = this.cv.width; this.off.height = this.cv.height;
    this.octx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  Lab.prototype.settle = function () {       // состояние покоя при входе на сцену (зовётся из activate)
    this.reset();                            // всегда с нуля — сброс на каждом входе
    REDUCED ? this.throwN(this.target) : this.play();
  };

  /* ============================================================
     SIM-1: иглы (полотно sl-sim)
     ============================================================ */
  function Needles(cv) {
    Lab.call(this, cv, { spacing: 90, seed: 6143, autoTarget: 1000, level: 2 / Math.PI });
    this.L = this.T;
    this.drawBase = this.lines.bind(this);
    this.reset();
  }
  Needles.prototype = Object.create(Lab.prototype);
  Needles.prototype.throwOne = function (c) {
    var cx = this.rng() * this.W, cy = this.rng() * this.H, th = this.rng() * Math.PI;
    var dy = Math.sin(th) * this.L / 2, dx = Math.cos(th) * this.L / 2, T = this.T;
    var band = function (y) { return Math.floor((y - T / 2) / T); };
    var hit = band(cy - dy) !== band(cy + dy);
    c.strokeStyle = hit ? this.C.brick : this.C.steel;
    c.lineWidth = 1.85; c.lineCap = 'round';
    c.beginPath(); c.moveTo(cx - dx, cy - dy); c.lineTo(cx + dx, cy + dy); c.stroke();
    return hit;
  };

  /* ============================================================
     SIM-4y: жёлтая сторона (sl-yellow) — режимы по сценам
       1: треугольники целиком; 2: только жёлтые стороны;
       3-4: + популяция игл длины 1 с горчичной третью
     ============================================================ */
  function Yellow(cv) {
    Lab.call(this, cv, { spacing: 158, seed: 977, autoTarget: 320,
                         level: 2 / (3 * Math.PI), sparkEvery: 3,
                         sparkLo: 0.02, sparkHi: 0.45 });
    this.mode = 1; this.tri = []; this.ndl = [];
    this.nR = 0; this.hitR = 0; this.spark2 = [];
    this.drawBase = this.lines.bind(this);
    this.reset();
  }
  Yellow.prototype = Object.create(Lab.prototype);
  Yellow.prototype.resetState = function () {
    Lab.prototype.resetState.call(this);
    this.tri = []; this.ndl = []; this.nR = 0; this.hitR = 0; this.spark2 = [];
  };
  /* слева — треугольник (жёлтая сторона), справа — игла из трёх частей
     (жёлтая крайняя треть); статистики жёлтых пересечений идут парой */
  Yellow.prototype.throwOne = function () {
    var T = this.T, band = function (y) { return Math.floor((y - T / 2) / T); };
    var split = this.W / 2;
    var s3 = T / 3, R = s3 / Math.sqrt(3);
    var cx = 10 + this.rng() * (split - 40), cy = this.rng() * this.H, rot = this.rng() * 2 * Math.PI;
    var v = [];
    for (var k = 0; k < 3; k++) {
      var a = rot + k * 2 * Math.PI / 3;
      v.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]);
    }
    var yHit = band(v[0][1]) !== band(v[1][1]);
    this.tri.push({ v: v, yHit: yHit });
    if (this.mode >= 3) {                       // правая популяция: игла длины T
      var nx = split + 30 + this.rng() * (this.W - split - 60);
      var ny = this.rng() * this.H, th = this.rng() * Math.PI;
      var dx = Math.cos(th) * T / 2, dy = Math.sin(th) * T / 2;
      var A = [nx - dx, ny - dy], B = [nx + dx, ny + dy];
      var M = [A[0] + (B[0] - A[0]) / 3, A[1] + (B[1] - A[1]) / 3];
      var nHit = band(A[1]) !== band(M[1]);
      this.ndl.push({ v: [A, M, B], yHit: nHit });
      this.nR++; if (nHit) this.hitR++;
      if (this.nR % this.sparkEvery === 0) this.spark2.push(this.hitR / this.nR);
    }
    this.redrawAll();
    return yHit;
  };
  Yellow.prototype.redrawAll = function () {
    var c = this.octx, C = this.C, mode = this.mode, W = this.W, H = this.H;
    c.fillStyle = C.card; c.fillRect(0, 0, W, H);
    this.lines(c);
    c.lineCap = 'round';
    var i, o, v;
    for (i = 0; i < this.tri.length; i++) {
      o = this.tri[i]; v = o.v;
      c.lineWidth = 2.4;
      c.globalAlpha = (mode >= 2) ? .1 : 1;          // «сотрём все стороны, кроме жёлтой»
      c.strokeStyle = C.corange;                     // вторая сторона — оранжевая
      c.beginPath(); c.moveTo(v[1][0], v[1][1]); c.lineTo(v[2][0], v[2][1]); c.stroke();
      c.strokeStyle = C.cgreen;                      // третья сторона — зелёная
      c.beginPath(); c.moveTo(v[2][0], v[2][1]); c.lineTo(v[0][0], v[0][1]); c.stroke();
      c.globalAlpha = 1;
      c.strokeStyle = (o.yHit && mode >= 2) ? C.brick : C.mustard;   // жёлтая сторона
      c.beginPath(); c.moveTo(v[0][0], v[0][1]); c.lineTo(v[1][0], v[1][1]); c.stroke();
    }
    if (mode >= 3) {                                  // разделитель и иглы справа
      c.strokeStyle = C.steel; c.lineWidth = 2; c.globalAlpha = .55;
      c.beginPath(); c.moveTo(W / 2 + .5, 8); c.lineTo(W / 2 + .5, H - 8); c.stroke();
      c.globalAlpha = 1;
      for (i = 0; i < this.ndl.length; i++) {
        o = this.ndl[i]; v = o.v;
        c.lineWidth = 2.4;
        c.strokeStyle = C.steel; c.globalAlpha = .14;
        c.beginPath(); c.moveTo(v[1][0], v[1][1]); c.lineTo(v[2][0], v[2][1]); c.stroke();
        c.globalAlpha = 1;
        c.strokeStyle = o.yHit ? C.brick : C.mustard;
        c.beginPath(); c.moveTo(v[0][0], v[0][1]); c.lineTo(v[1][0], v[1][1]); c.stroke();
      }
    }
    this.draw();
  };
  Yellow.prototype.onScene = function (k) {
    var m = Math.max(1, Math.min(4, k));
    if (m !== this.mode) { this.mode = m; this.redrawAll(); }
  };

  /* ============================================================
     SIM-6: связка «игла ↔ точка» (sl-coords, две панели)
     ============================================================ */
  function Coords(cvNeedles, cvPhase) {
    this.A = cvNeedles; this.B = cvPhase;
    this.C = tokens();
    this.prep(this.A); this.prep(this.B);
    this.T = 150;                      // шаг линий (крупно: игла видна)
    this.pairs = [];
    this.activeIdx = -1;
    this.rng = mulberry32(4242);
    for (var i = 0; i < 5; i++) this.addPair();
    this.bind();
    this.drawAll();
  }
  Coords.prototype.prep = function (cv) {
    var dpr = Math.min(devicePixelRatio || 1, 2);
    cv._w = cv.clientWidth; cv._h = cv.clientHeight;
    cv.width = cv._w * dpr; cv.height = cv._h * dpr;
    cv.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  Coords.prototype.addPair = function () {
    this.pairs.push({ a: (this.rng() * 2 - 1) * Math.PI / 2, y: this.rng(), x: null,
                      color: this.C.pastels[this.pairs.length % 5] });
  };
  /* геометрия иглы: нижний конец на расстоянии y вниз от «своей» линии */
  Coords.prototype.needleGeo = function (p, i) {
    var W = this.A._w, H = this.A._h, T = this.T;
    var lineY = (H - T) / 2;                        // рабочая полоса по центру
    var x0 = (p.x != null) ? p.x : W * (0.14 + 0.18 * i);
    var y0 = lineY + p.y * T;
    var x1 = x0 + Math.sin(p.a) * T, y1 = y0 - Math.cos(p.a) * T;
    return { x0: x0, y0: y0, x1: x1, y1: y1, lineY: lineY };
  };
  Coords.prototype.phaseGeo = function (p) {
    var w = this.B._w, h = this.B._h, pad = 34;
    return { x: pad + (p.a + Math.PI / 2) / Math.PI * (w - pad * 2),
             y: pad + (1 - p.y) * (h - pad * 2), pad: pad };
  };
  Coords.prototype.drawAll = function () {
    var C = this.C;
    /* панель игл */
    var a = this.A.getContext('2d'), W = this.A._w, H = this.A._h;
    a.clearRect(0, 0, W, H);
    a.fillStyle = C.card; a.fillRect(0, 0, W, H);
    a.strokeStyle = C.rule; a.lineWidth = 1.4; a.beginPath();
    var laneTop = (H - this.T) / 2;
    [laneTop - this.T, laneTop, laneTop + this.T, laneTop + 2 * this.T].forEach(function (y) {
      if (y > -1 && y < H + 1) { a.moveTo(0, y + .5); a.lineTo(W, y + .5); }
    });
    a.stroke();
    for (var i = 0; i < this.pairs.length; i++) {
      var p = this.pairs[i], g = this.needleGeo(p, i), act = i === this.activeIdx;
      a.globalAlpha = (this.activeIdx >= 0 && !act) ? .35 : 1;
      a.strokeStyle = p.color; a.lineWidth = act ? 4.6 : 2.6; a.lineCap = 'round';
      a.beginPath(); a.moveTo(g.x0, g.y0); a.lineTo(g.x1, g.y1); a.stroke();
      a.fillStyle = a.strokeStyle;
      a.beginPath(); a.arc(g.x0, g.y0, act ? 5 : 3.6, 0, 7); a.fill();
    }
    a.globalAlpha = 1;
    /* фазовый прямоугольник */
    var b = this.B.getContext('2d'), w = this.B._w, h = this.B._h;
    b.clearRect(0, 0, w, h);
    b.fillStyle = C.card; b.fillRect(0, 0, w, h);
    var pad = 34;
    b.strokeStyle = C.steel; b.lineWidth = 1.6;
    b.strokeRect(pad + .5, pad + .5, w - pad * 2 - 1, h - pad * 2 - 1);
    b.fillStyle = C.ink; b.globalAlpha = .7;
    b.font = 'italic 17px Georgia,serif'; b.textAlign = 'center';
    b.fillText('−π/2', pad, h - 9); b.fillText('π/2', w - pad, h - 9);
    b.textAlign = 'left'; b.fillText('1', 8, pad + 6);
    b.fillText('0', 8, h - pad + 5);
    b.globalAlpha = 1;
    for (var j = 0; j < this.pairs.length; j++) {
      var q = this.pairs[j], g2 = this.phaseGeo(q), act2 = j === this.activeIdx;
      b.globalAlpha = (this.activeIdx >= 0 && !act2) ? .35 : 1;
      b.fillStyle = q.color;
      b.beginPath(); b.arc(g2.x, g2.y, act2 ? 10 : 6.5, 0, 7); b.fill();
      if (act2) { b.strokeStyle = q.color; b.lineWidth = 2; b.stroke(); }
    }
    b.globalAlpha = 1;
    /* шёпот-подсказка */
    b.fillStyle = C.ink; b.globalAlpha = .38;
    b.font = '14px "Courier Prime",monospace'; b.textAlign = 'right';
    b.fillText('потяни точку или иглу', w - 12, 22);
    b.globalAlpha = 1;
  };
  Coords.prototype.bind = function () {
    var self = this;
    function pos(cv, e) {
      var r = cv.getBoundingClientRect();
      var t = e.touches ? e.touches[0] : e;
      return [(t.clientX - r.left) * cv._w / r.width, (t.clientY - r.top) * cv._h / r.height];
    }
    /* drag точки в фазовом прямоугольнике */
    function downB(e) {
      var p = pos(self.B, e), best = -1, bd = 26 * 26;
      self.pairs.forEach(function (q, i) {
        var g = self.phaseGeo(q), d = (g.x - p[0]) * (g.x - p[0]) + (g.y - p[1]) * (g.y - p[1]);
        if (d < bd) { bd = d; best = i; }
      });
      if (best < 0) return;
      self.activeIdx = best; self.drawAll(); e.preventDefault();
      function move(ev) {
        var m = pos(self.B, ev), w = self.B._w, h = self.B._h, pad = 34;
        var q = self.pairs[self.activeIdx];
        q.a = Math.max(-Math.PI / 2, Math.min(Math.PI / 2,
              ((m[0] - pad) / (w - pad * 2)) * Math.PI - Math.PI / 2));
        q.y = Math.max(0, Math.min(1, 1 - (m[1] - pad) / (h - pad * 2)));
        self.drawAll(); ev.preventDefault();
      }
      function up() {
        self.activeIdx = -1; self.drawAll();
        removeEventListener('pointermove', move); removeEventListener('pointerup', up);
      }
      addEventListener('pointermove', move); addEventListener('pointerup', up);
    }
    /* drag иглы: верхняя половина — угол, нижний конец — y */
    function downA(e) {
      var p = pos(self.A, e), best = -1, bd = 22 * 22, grabTop = false;
      self.pairs.forEach(function (q, i) {
        var g = self.needleGeo(q, i);
        // дистанция до отрезка иглы + у какой половины схватили
        for (var t = 0; t <= 1; t += 0.1) {
          var px = g.x0 + (g.x1 - g.x0) * t, py = g.y0 + (g.y1 - g.y0) * t;
          var d = (px - p[0]) * (px - p[0]) + (py - p[1]) * (py - p[1]);
          if (d < bd) { bd = d; best = i; grabTop = t > 0.45; }
        }
      });
      if (best < 0) return;
      self.activeIdx = best; self.drawAll(); e.preventDefault();
      function move(ev) {
        var m = pos(self.A, ev), q = self.pairs[self.activeIdx];
        var g = self.needleGeo(q, self.activeIdx);
        if (grabTop) {                       // вращение вокруг нижнего конца
          q.a = Math.max(-Math.PI / 2, Math.min(Math.PI / 2,
                Math.atan2(m[0] - g.x0, g.y0 - m[1])));
        } else {                             // сдвиг всей иглы: y влияет на точку,
          q.y = Math.max(0, Math.min(1, (m[1] - g.lineY) / self.T));
          q.x = Math.max(20, Math.min(self.A._w - 20, m[0]));          // x — нет
        }
        self.drawAll(); ev.preventDefault();
      }
      function up() {
        self.activeIdx = -1; self.drawAll();
        removeEventListener('pointermove', move); removeEventListener('pointerup', up);
      }
      addEventListener('pointermove', move); addEventListener('pointerup', up);
    }
    this.B.style.cursor = 'grab'; this.A.style.cursor = 'grab';
    this.B.addEventListener('pointerdown', downB);
    this.A.addEventListener('pointerdown', downA);
  };

  /* ============================================================
     регистрация и активация по сценам
     ============================================================ */
  var registry = {};
  window.LAB = registry;
  window.LabCore = { Lab: Lab, tokens: tokens, mulberry32: mulberry32, REDUCED: REDUCED };
  window.LabKinds = window.LabKinds || {};
  window.LabKinds.needles = function (cv) { var l = new Needles(cv); l.row(); return l; };
  window.LabKinds.yellow  = function (cv) { var y = new Yellow(cv); y.row(); return y; };
  window.LabKinds['coords-needles'] = function (cv, slide) {
    var other = slide.querySelector('canvas[data-sim="coords-phase"]');
    return other ? new Coords(cv, other) : null;
  };
  function activate(slide, justShown) {
    var k = 1, m = slide.className.match(/scene-(\d+)/); if (m) k = +m[1];
    slide.querySelectorAll('canvas[data-sim]').forEach(function (cv) {
      var kind = cv.dataset.sim, id = slide.id + ':' + kind;
      if (!registry[id]) {
        var maker = window.LabKinds[kind];
        if (!maker) return;
        var exp0 = maker(cv, slide);
        if (exp0) registry[id] = exp0; else return;
      }
      var exp = registry[id];
      if (exp && exp.onScene) exp.onScene(k);
      if (justShown) {                                    /* ноль + авто-запуск (единый хук покоя) */
        if (exp.pause) exp.pause();
        if (exp.measure) exp.measure();                   /* init-гонка: пере-замер при показе */
        if (exp.settle) exp.settle();                     /* settle() = reset()+прогон, sim переопределяют */
        else { if (exp.reset) exp.reset(); if (exp.play) exp.play(); }
      }
    });
  }
  function watch() {
    document.querySelectorAll('.slide').forEach(function (s) {
      if (!s.querySelector('canvas[data-sim]')) return;
      var vis = function () { return s.style.display !== 'none'; };
      new MutationObserver(function () {
        var v = vis(), js = v && !s._simVis; s._simVis = v;
        if (v) activate(s, js);
      }).observe(s, { attributes: true, attributeFilter: ['style', 'class'] });
      s._simVis = vis(); if (s._simVis) activate(s, true);
    });
  }
  addEventListener('load', watch);
})();

