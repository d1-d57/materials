
/* === lab-ext/phase-mass.js (вшито сборкой) === */
/* ============================================================
   SIM-6m: phase-mass — масса точек в фазовом прямоугольнике.
   Один модуль, две раскладки по slide.id:
   • sl-condition — фазовый прямоугольник α∈[−π/2,π/2], y∈[0,1]:
     точки сыплются нейтральными (ink op .5, кривой нет);
     сцена 2 — кривая y = cos α (чернильная 2.6) проявляется и
     точки перекрашиваются ВОЛНОЙ слева направо (~1.2 c, rAF по
     α-порогу): под кривой → кирпич, над → сталь.
     prefers-reduced-motion: мгновенно.
   • sl-phase — полотно: слева полоса с линиями и иглами (~22%
     ширины), справа фазовый прямоугольник; каждый бросок = игла
     слева + точка справа, цвет сразу статусный; автоброс
     батчами до 4000; приборка с риской 2/π и спарклайном;
     клик по карточке — живая строка «π ≈ 2N/X».
   Физика честная: α ~ U[−π/2, π/2], y ~ U[0, 1];
   пересечение ⇔ y ⩽ cos α ⇒ P = (1/π)∫cos α dα = 2/π.
   Цвета — только токены this.C (+ микрообводка darker 12%,
   ILLUSTRATION-LANGUAGE «Чёткость и микроконтраст»).
   ============================================================ */
(function () {
  'use strict';
  var core = window.LabCore;
  if (!core) return;
  var Lab = core.Lab, REDUCED = core.REDUCED;
  var PI = Math.PI, HPI = Math.PI / 2;

  /* гравюрная кромка: тот же цвет, темнее на 12% */
  function darker(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec(String(hex).trim());
    if (!m) return hex;
    var v = parseInt(m[1], 16), k = 0.88;
    return 'rgb(' + Math.round(((v >> 16) & 255) * k) + ',' +
                    Math.round(((v >> 8) & 255) * k) + ',' +
                    Math.round((v & 255) * k) + ')';
  }

  function PhaseMass(cv, layout) {
    this.layout = layout;                       // 'condition' | 'canvas'
    Lab.call(this, cv, layout === 'canvas'
      ? { seed: 7351, autoTarget: 4000, level: 2 / PI, sparkEvery: 8 }
      : { seed: 5077, autoTarget: 800, dash: false, endless: true });
    this.pts = [];                              // все точки (для волны)
    this.recent = []; this.KEEP = 24;           // свежие иглы полосы
    this.mode = 2;                              // 2 = статус-цвета; 3 = + кривая
    this.waving = false; this.waveT = -HPI;
    this.showPi = false;

    if (layout === 'canvas') {
      this.speed = 4;                           // батчи бодрее: ~800 бросков/с
      var sw = Math.round(this.W * 0.22);       // полоса с иглами
      this.stripW = sw;
      this.T = 92;                              // шаг линий = длина иглы
      var top = (this.H - 3 * this.T) / 2;      // веер игл по центру полосы
      this.lineYs = [top, top + this.T, top + 2 * this.T, top + 3 * this.T];
      this.baseLines = [this.lineYs[1], this.lineYs[2]];  // низ и верх игл в кадре
      this.rect = { x: sw + 46, y: 22, w: this.W - sw - 46 - 32, h: this.H - 22 - 56 };
    } else {
      this.rect = { x: 32, y: 16, w: this.W - 32 - 16, h: this.H - 16 - 52 };
    }
    this.drawBase = this.base.bind(this);
    this.bind();
    this.reset();
  }
  PhaseMass.prototype = Object.create(Lab.prototype);

  PhaseMass.prototype.resetState = function () {
    Lab.prototype.resetState.call(this);
    this.pts = []; this.recent = [];
  };

  /* ---------- геометрия фазового прямоугольника ---------- */
  PhaseMass.prototype.ptXY = function (a, y) {
    var R = this.rect;
    return [R.x + (a + HPI) / PI * R.w, R.y + (1 - y) * R.h];
  };

  /* ---------- фон: рамка, подписи осей, полоса с линиями ---------- */
  PhaseMass.prototype.base = function (c) {
    var C = this.C, R = this.rect, small = this.layout !== 'canvas';
    if (!small) {                                /* полоса игл слева */
      c.strokeStyle = C.rule; c.lineWidth = 1.4; c.beginPath();
      for (var i = 0; i < this.lineYs.length; i++) {
        var y = this.lineYs[i];
        c.moveTo(0, y + .5); c.lineTo(this.stripW - 18, y + .5);
      }
      c.stroke();
      c.strokeStyle = C.rule; c.lineWidth = 1.25; c.beginPath();
      c.moveTo(this.stripW + .5, 12); c.lineTo(this.stripW + .5, this.H - 12);
      c.stroke();
    }
    c.strokeStyle = C.steel; c.lineWidth = 2;    /* рамка прямоугольника */
    c.strokeRect(R.x + .5, R.y + .5, R.w - 1, R.h - 1);
    c.fillStyle = C.ink; c.globalAlpha = .7;     /* подписи осей */
    c.font = 'italic ' + (small ? 16 : 18) + 'px Georgia,serif';
    c.textAlign = 'center';
    c.fillText('−π/2', R.x + (small ? 2 : 0), R.y + R.h + (small ? 20 : 22));
    c.fillText('π/2', R.x + R.w, R.y + R.h + (small ? 20 : 22));
    c.textAlign = 'right';
    c.fillText('1', R.x - 9, R.y + 7);
    c.fillText('0', R.x - 9, R.y + R.h + 4);
    c.globalAlpha = 1; c.textAlign = 'left';
  };

  /* ---------- точка в фазовом прямоугольнике ---------- */
  PhaseMass.prototype.stampDot = function (c, a, y, col, alpha) {
    var p = this.ptXY(a, y);
    c.globalAlpha = alpha; c.fillStyle = col;
    c.beginPath(); c.arc(p[0], p[1], 3.5, 0, 7); c.fill();
    c.globalAlpha = Math.min(1, alpha + .08);
    c.strokeStyle = darker(col); c.lineWidth = .9; c.stroke();
    c.globalAlpha = 1;
  };
  PhaseMass.prototype.dotStyle = function (pt, thr) {
    if (this.layout === 'canvas' || pt.a <= thr)
      return [pt.hit ? this.C.brick : this.C.steel, .85];
    return [this.C.ink, .5];                    // нейтральная масса до развязки
  };

  /* ---------- бросок: игла слева (canvas) + точка справа ---------- */
  PhaseMass.prototype.throwOne = function (c) {
    var a = (this.rng() * 2 - 1) * HPI, y = this.rng();
    var hit = y <= Math.cos(a);
    var pt = { a: a, y: y, hit: hit };
    this.pts.push(pt);
    if (this.layout === 'canvas') {
      var x0 = 60 + this.rng() * (this.stripW - 120);
      var line = this.baseLines[(this.rng() * this.baseLines.length) | 0];
      var y0 = line + y * this.T;
      this.recent.push({ x0: x0, y0: y0,
                         x1: x0 + Math.sin(a) * this.T,
                         y1: y0 - Math.cos(a) * this.T, hit: hit });
      if (this.recent.length > this.KEEP) this.recent.shift();
      this.stampDot(c, a, y, hit ? this.C.brick : this.C.steel, .85);
    } else {
      if (this.pts.length > this.o.autoTarget) this.pts.shift();  // катящееся окно — не заливает
      this.redrawAll(this.waving ? this.waveT : Infinity);         // статусные цвета всегда
    }
    return hit;
  };

  /* полная перерисовка аккумулятора с α-порогом (волна / смена сцены) */
  PhaseMass.prototype.redrawAll = function (thr) {
    var c = this.octx;
    c.fillStyle = this.C.card; c.fillRect(0, 0, this.W, this.H);
    this.base(c);
    for (var i = 0; i < this.pts.length; i++) {
      var st = this.dotStyle(this.pts[i], thr);
      this.stampDot(c, this.pts[i].a, this.pts[i].y, st[0], st[1]);
    }
    this.draw();
  };

  /* ---------- свой композит: точки → кривая/иглы → приборка ---------- */
  PhaseMass.prototype.draw = function () {
    var c = this.ctx;
    c.clearRect(0, 0, this.W, this.H);
    c.drawImage(this.off, 0, 0, this.W, this.H);
    if (this.layout === 'canvas') {
      this.drawCurve(c, HPI);
      this.drawNeedles(c);
      this.dashboard(c);
    } else if (this.waving || this.mode >= 3) {     // кривая — со сцены 2
      this.drawCurve(c, this.waving ? this.waveT : HPI);
    }
  };

  /* кривая y = cos α — чернильная, поверх точек; limA — фронт волны */
  PhaseMass.prototype.drawCurve = function (c, limA) {
    var R = this.rect, a1 = Math.min(limA, HPI);
    if (a1 <= -HPI) return;
    var n = Math.max(2, Math.ceil((a1 + HPI) / PI * 72));
    c.strokeStyle = this.C.ink; c.lineWidth = 2.6;
    c.lineCap = 'butt'; c.lineJoin = 'round';
    c.beginPath();
    for (var i = 0; i <= n; i++) {
      var a = -HPI + (a1 + HPI) * i / n;
      var x = R.x + (a + HPI) / PI * R.w, y = R.y + (1 - Math.cos(a)) * R.h;
      i ? c.lineTo(x, y) : c.moveTo(x, y);
    }
    c.stroke();
  };

  /* свежие иглы полосы: новая ярче, старая тает (паттерн coin) */
  PhaseMass.prototype.drawNeedles = function (c) {
    var n = this.recent.length;
    if (!n) return;
    c.save();
    c.beginPath(); c.rect(0, 0, this.stripW, this.H); c.clip();
    c.lineCap = 'round';
    for (var i = 0; i < n; i++) {
      var o = this.recent[i], age = n - 1 - i;
      var col = o.hit ? this.C.brick : this.C.steel;
      c.globalAlpha = Math.max(.26, .95 * Math.pow(.9, age));
      c.strokeStyle = col; c.lineWidth = 2.3;
      c.beginPath(); c.moveTo(o.x0, o.y0); c.lineTo(o.x1, o.y1); c.stroke();
      c.fillStyle = col;
      c.beginPath(); c.arc(o.x0, o.y0, 2.7, 0, 7); c.fill();
    }
    c.globalAlpha = 1;
    c.restore();
  };

  /* приборка: стандартная карточка + (по клику) строка «π ≈ 2N/X».
     Сдвиг вверх на 32 — нижняя кромка карточки сидит на нижней
     грани прямоугольника, подписи −π/2 / π/2 остаются видны. */
  PhaseMass.prototype.dashDY = -32;
  PhaseMass.prototype.cardBox = function () {
    var w = 232, h = 148;
    return { x: this.W - w - 22, y: this.H - h - 20 + this.dashDY, w: w, h: h };
  };
  PhaseMass.prototype.dashboard = function (c) {
    if (this.showPi) {
      var b = this.cardBox(), y = b.y - 36;
      c.fillStyle = this.C.card; c.fillRect(b.x, y, b.w, 30);
      c.strokeStyle = this.C.rule; c.lineWidth = 1;
      c.strokeRect(b.x + .5, y + .5, b.w - 1, 29);
      c.fillStyle = this.C.ink; c.textAlign = 'left';
      c.font = '700 17px "Courier Prime",monospace';
      var est = this.hit ? (2 * this.n / this.hit).toFixed(3).replace('.', ',') : '—';
      c.fillText('π ≈ ' + est, b.x + 12, y + 21);
    }
    c.save(); c.translate(0, this.dashDY);
    Lab.prototype.dashboard.call(this, c);
    c.restore();
  };

  /* клик по карточке — показать/спрятать живую оценку π */
  PhaseMass.prototype.bind = function () {
    if (this.layout !== 'canvas') return;
    var self = this, cv = this.cv;
    function pos(e) {
      var r = cv.getBoundingClientRect();
      return [(e.clientX - r.left) * self.W / r.width,
              (e.clientY - r.top) * self.H / r.height];
    }
    function inCard(p) {
      var b = self.cardBox(), top = self.showPi ? b.y - 36 : b.y;
      return p[0] >= b.x && p[0] <= b.x + b.w && p[1] >= top && p[1] <= b.y + b.h;
    }
    cv.addEventListener('click', function (e) {
      if (!inCard(pos(e))) return;
      self.showPi = !self.showPi; self.draw();
    });
    cv.addEventListener('pointermove', function (e) {
      cv.style.cursor = inCard(pos(e)) ? 'pointer' : '';
    });
  };

  /* ---------- сцены (sl-condition): кривая + волна перекраски ---------- */
  PhaseMass.prototype.onScene = function (k) {
    if (this.layout !== 'condition') return;
    /* статусные цвета — всегда (ревью автора); сцена ≥2 добавляет кривую волной */
    var withCurve = k >= 2 ? 3 : 2;
    if (withCurve === this.mode) return;
    var was = this.mode;
    this.mode = withCurve;
    if (withCurve === 3 && was < 3 && !window.LabCore.REDUCED && this.pts.length) this.startWave();
    else { this.waving = false; this.redrawAll(Infinity); }
  };

  /* волна перекраски-проявления кривой слева направо (~1.2 c) */
  PhaseMass.prototype.startWave = function () {
    var self = this, t0 = performance.now(), DUR = 1200, HPI = Math.PI / 2;
    this.waving = true;
    (function step(ts) {
      if (!self.waving || self.mode !== 3) return;
      var ph = Math.min(1, (ts - t0) / DUR);
      self.waveT = -HPI + ph * Math.PI;
      self.redrawAll(self.waveT);
      if (ph < 1) requestAnimationFrame(step);
      else { self.waving = false; self.redrawAll(Infinity); }
    })(t0);
  };

  window.LabKinds = window.LabKinds || {};
  window.LabKinds['phase-mass'] = function (cv, slide) {
    var exp = new PhaseMass(cv, slide.id === 'sl-phase' ? 'canvas' : 'condition');
    exp.row();
    return exp;
  };
})();

