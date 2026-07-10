
/* === lab-ext/coin.js (вшито сборкой) === */
/* ============================================================
   SIM-3: монеты на линиях (sl-coin) — расширение лаборатории.
   Композиция = ill-sl-coin-1: две линии сталью, опасные зоны
   прозрачным кирпичом во всю ширину, монеты-контуры со
   статусным цветом и точкой-центром.
   Физика: центр равномерен по периоду T между линиями,
   пересечение ⇔ расстояние до ближайшей линии < r = d/2;
   d = T/2 ⇒ P = d/T = 1/2.
   Живость: 8-кадровый дроп (радиус 1.3r → r с лёгким
   затуханием), горчичный кадр посадки → статусный цвет.
   Накопление — пуант слайда «важно только положение центра»:
   осевшая монета остаётся точкой-центром, контур держат только
   последние KEEP монет (свежая ярче, старая тает).
   ============================================================ */
(function () {
  'use strict';
  var core = window.LabCore;
  if (!core) return;
  var Lab = core.Lab, REDUCED = core.REDUCED;

  /* радиус по кадрам дропа: 1.3r → r, лёгкое затухание у посадки */
  var DROP = [1.30, 1.24, 1.17, 1.10, 1.045, 0.992, 0.978, 1.0];

  function Coin(cv) {
    Lab.call(this, cv, { spacing: 200, seed: 9151, autoTarget: 200, endless: true,
                         level: 0.5, sparkLo: 0.2, sparkHi: 0.8,
                         sparkEvery: 2 });
    this.r = this.T / 4;                       // d = T/2 ⇒ r = T/4
    this.line1 = this.H / 2 - this.T / 2;      // две линии, центрированы
    this.line2 = this.H / 2 + this.T / 2;
    this.drops = []; this._anim = false; this._last = null;
    this.recent = []; this.KEEP = 14;          // монеты, ещё держащие контур
    this.mode = 1;                             // сцена 1: круги+2 линии; сцена 2: +центры+полосы
    var self = this;
    this._tickB = function () { self._tick(); };
    this.reset();
  }
  Coin.prototype = Object.create(Lab.prototype);

  Coin.prototype.resetState = function () {
    Lab.prototype.resetState.call(this);
    this.drops = []; this._last = null; this.recent = []; this.all = [];
  };
  /* сцена: 1 — круги без центров и без полос; 2 — центры всех монет + опасные полосы */
  Coin.prototype.onScene = function (k) {
    var m = (k >= 2) ? 2 : 1;
    if (m !== this.mode) { this.mode = m; this.rebake(); }
  };
  /* пере-запечь офскрин из накопленных монет под текущий режим */
  Coin.prototype.rebake = function () {
    var c = this.octx;
    c.clearRect(0, 0, this.W, this.H);
    c.fillStyle = this.C.card; c.fillRect(0, 0, this.W, this.H);
    this.drawBase(c);
    for (var i = 0; i < this.all.length; i++) this._dot(c, this.all[i]);
    this.draw();
  };
  /* точка-центр (только в режиме 2) */
  Coin.prototype._dot = function (c, o) {
    if (this.mode < 2) return;
    c.globalAlpha = 0.9; c.fillStyle = o.hit ? this.C.brick : this.C.steel;
    c.beginPath(); c.arc(o.x, o.y, 3, 0, 7); c.fill();
    c.globalAlpha = 1;
  };

  /* фон: зоны во всю ширину + 2 линии пола (как в статике) */
  Coin.prototype.drawBase = function (c) {
    var W = this.W, r = this.r, l1 = this.line1, l2 = this.line2, C = this.C;
    if (this.mode >= 2) {                                 // полосы — только сцена 2
      c.globalAlpha = 0.10; c.fillStyle = C.steel;        // спокойная середина
      c.fillRect(0, l1 + r, W, (l2 - r) - (l1 + r));
      c.globalAlpha = 0.16; c.fillStyle = C.brick;        // опасные зоны (< r от линии)
      c.fillRect(0, l1, W, r);
      c.fillRect(0, l2 - r, W, r);
      c.globalAlpha = 1;
    }
    c.strokeStyle = C.steel; c.lineWidth = 3; c.lineCap = 'butt';
    c.beginPath();
    c.moveTo(0, l1 + 0.5); c.lineTo(W, l1 + 0.5);
    c.moveTo(0, l2 + 0.5); c.lineTo(W, l2 + 0.5);
    c.stroke();
  };

  /* осевшая монета в аккумулятор: только точка-центр статусного цвета —
     «важно только положение центра»; контур живёт во freshest-слое */
  Coin.prototype.stamp = function (c, o) {
    this.all.push(o);
    this._dot(c, o);                          // центр — только в режиме 2
    this.recent.push(o);
    if (this.recent.length > this.KEEP) this.recent.shift();
  };

  /* контуры последних монет: свежая яркая, старая тает (под приборкой) */
  Coin.prototype.contours = function (c) {
    var n = this.recent.length;
    c.lineWidth = 2.4; c.lineCap = 'round';
    for (var i = 0; i < n; i++) {
      var o = this.recent[i], age = n - 1 - i;
      c.globalAlpha = Math.max(0.13, 0.9 * Math.pow(0.84, age));
      c.strokeStyle = o.hit ? this.C.brick : this.C.steel;
      c.beginPath(); c.arc(o.x, o.y, this.r, 0, 7); c.stroke();
    }
    c.globalAlpha = 1;
  };

  /* свой композит: аккумулятор → свежие контуры → дропы → приборка
     (приборная карточка — поверх всего, как инструмент) */
  Coin.prototype.draw = function () {
    var c = this.ctx;
    c.clearRect(0, 0, this.W, this.H);
    c.drawImage(this.off, 0, 0, this.W, this.H);
    this.contours(c);
    this.drawTop(c);
    this.dashboard(c);
  };

  /* честный бросок: x равномерно (не влияет), y равномерно по периоду T */
  Coin.prototype.throwOne = function (c) {
    var m = this.r + 12;
    var x = m + this.rng() * (this.W - 2 * m);
    var y = this.line1 + this.rng() * this.T;
    var hit = Math.min(y - this.line1, this.line2 - y) < this.r;
    var coin = { x: x, y: y, hit: hit, f: 0 };
    this._last = coin;
    if (this._noAnim || REDUCED) this.stamp(c, coin);   // пакеты — мгновенно
    else { this.drops.push(coin); this._run(); }        // одиночные — с дропом
    return hit;
  };

  /* пакеты без анимации + короткая горчичная вспышка последней монеты */
  Coin.prototype.throwN = function (n) {
    if (n > 1) {
      this._noAnim = true;
      Lab.prototype.throwN.call(this, n);
      this._noAnim = false;
      if (!REDUCED && this._last) {
        this.drops.push({ x: this._last.x, y: this._last.y, flash: true, f: 0 });
        this._run();
      }
    } else Lab.prototype.throwN.call(this, n);
  };

  Coin.prototype._run = function () {
    if (this._anim) return;
    this._anim = true;
    requestAnimationFrame(this._tickB);
  };
  Coin.prototype._tick = function () {
    var c = this.octx;
    for (var i = this.drops.length - 1; i >= 0; i--) {
      var d = this.drops[i]; d.f++;
      if (d.f >= (d.flash ? 4 : 8)) {
        if (!d.flash) this.stamp(c, d);                 // посадка → статусный цвет
        this.drops.splice(i, 1);
      }
    }
    this.draw();
    if (this.drops.length) requestAnimationFrame(this._tickB);
    else this._anim = false;
  };

  /* летящие монеты поверх композита */
  Coin.prototype.drawTop = function (c) {
    var C = this.C, r = this.r;
    for (var i = 0; i < this.drops.length; i++) {
      var d = this.drops[i];
      if (d.flash) {                                    // вспышка последней в пакете (нейтральная)
        c.globalAlpha = Math.max(0, 1 - d.f / 4);
        c.strokeStyle = C.steel; c.lineWidth = 3;
        c.beginPath(); c.arc(d.x, d.y, r, 0, 7); c.stroke();
        continue;
      }
      var land = d.f >= 6;                              // кадр посадки — статусный цвет (без горчицы)
      c.globalAlpha = land ? 1 : 0.35 + 0.07 * d.f;
      c.strokeStyle = land ? (d.hit ? C.brick : C.steel) : C.steel;
      c.lineWidth = land ? 3 : 2.2;
      c.beginPath();
      c.arc(d.x, d.y, r * DROP[Math.min(d.f, 7)], 0, 7);
      c.stroke();
      if (land && d.hit) {                              // пульс зоны при попадании
        c.globalAlpha = 0.07; c.fillStyle = C.brick;
        var zy = (d.y - this.line1 < r) ? this.line1 : this.line2 - r;
        c.fillRect(0, zy, this.W, r);
      }
    }
    c.globalAlpha = 1;
  };

  window.LabKinds = window.LabKinds || {};
  window.LabKinds['coin'] = function (cv, slide) {
    var exp = new Coin(cv);
    exp.row();
    return exp;
  };
})();

