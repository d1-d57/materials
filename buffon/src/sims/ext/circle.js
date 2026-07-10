
/* === lab-ext/circle.js (вшито сборкой) === */
/* ============================================================
   SIM-4c: окружности длины 1 на узкой рейке (sl-circle, .p-circles).
   Окружность периметра T (радиус T/2π) пересекает линию ⇔ расстояние
   от центра до ближайшей линии < r; доля пересечений → p/2 = 1/π.
   База: window.LabCore.Lab (lab.js). Стиль: ILLUSTRATION-LANGUAGE.md —
   пересекла → кирпич, мимо → сталь, ориентир 1/π — горчица; токены this.C.
   ============================================================ */
(function () {
  'use strict';
  var Lab = window.LabCore.Lab;

  function Circle(cv) {
    Lab.call(this, cv, { spacing: 158, seed: 158, autoTarget: 100, endless: true, level: 1 / Math.PI,
                         sparkEvery: 5 });
    this.r = this.T / (2 * Math.PI);  // T = spacing 158 — как yellow/polygons/result (A3); периметр = T («длина 1»)
    this.drawBase = this.lines.bind(this);
    this.reset();
  }
  Circle.prototype = Object.create(Lab.prototype);

  Circle.prototype.throwOne = function (c) {
    var cx = this.r + this.rng() * (this.W - 2 * this.r); // x на исход не влияет
    var cy = this.rng() * this.H;                         // y равномерен по периодам
    var u = ((cy - this.T / 2) % this.T + this.T) % this.T;
    var hit = Math.min(u, this.T - u) < this.r;           // дистанция до линии < r
    c.strokeStyle = hit ? this.C.brick : this.C.steel;
    c.lineWidth = 1.6;
    c.beginPath(); c.arc(cx, cy, this.r, 0, 7); c.stroke();
    return hit;
  };

  /* компактная приборка узкой рейки: N + счётчики + микро-спарклайн доли → 1/π */
  window.LabKinds['circle'] = function (cv) {
    var l = new Circle(cv);
    l.row();
    /* узкая рейка (276px): ужимаем лабораторную строку, чтобы не вылезала */
    if (l._row) {
      l._row.style.font = '13px/1 "Courier Prime",monospace';
      Array.prototype.forEach.call(l._row.children, function (b) {
        b.style.minWidth = '0'; b.style.padding = '4px 3px';
      });
    }
    return l;
  };
})();

