
/* === lab-ext/prob.js (вшито сборкой) === */
/* ============================================================
   SIM-4p: счёт треугольников (sl-prob) — расширение лаборатории.
   Равносторонние треугольники периметра T (сторона T/3, T=96);
   пересёк линию → кирпичный контур, мимо → сталь.
   Спарклайн доли сходится к p/2 = 1/π ≈ 0.318 (горчичная риска).
   Сцены слайда визуально не различаются: статусная окраска всегда.
   Физика честная: центр и поворот равномерны; пересечение ⇔
   вертикальный размах вершин накрывает линию y = T/2 + kT
   (сторона T/3 < T ⇒ максимум одна линия). Seed фиксирован.
   ============================================================ */
(function () {
  'use strict';
  var Lab = window.LabCore.Lab;

  function Prob(cv) {
    Lab.call(this, cv, {
      spacing: 96, seed: 19, autoTarget: 500, endless: true,
      level: 2 / Math.PI / 2,            /* p/2 = 1/π */
      sparkLo: .1, sparkHi: .6
    });
    this.side = this.T / 3;              /* периметр = T = длина иглы */
    this.drawBase = this.lines.bind(this);
    this.reset();
  }
  Prob.prototype = Object.create(Lab.prototype);

  /* один бросок: рисует треугольник в аккумулятор, возвращает исход */
  Prob.prototype.throwOne = function (c) {
    var s = this.side, R = s / Math.sqrt(3);
    var cx = this.rng() * this.W, cy = this.rng() * this.H,
        rot = this.rng() * 2 * Math.PI;
    var v = [], lo = Infinity, hi = -Infinity, k;
    for (k = 0; k < 3; k++) {
      var a = rot + k * 2 * Math.PI / 3;
      var x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
      v.push([x, y]);
      if (y < lo) lo = y; if (y > hi) hi = y;
    }
    var T = this.T, band = function (y) { return Math.floor((y - T / 2) / T); };
    var hit = band(lo) !== band(hi);
    c.strokeStyle = hit ? this.C.brick : this.C.steel;
    c.lineWidth = 2; c.lineJoin = 'round';   /* как у треугольников sl-yellow */
    c.beginPath();
    c.moveTo(v[0][0], v[0][1]); c.lineTo(v[1][0], v[1][1]);
    c.lineTo(v[2][0], v[2][1]); c.closePath(); c.stroke();
    return hit;
  };

  /* полная перерисовка не нужна (аккумулятор), но сброс уже честный:
     reset() ядра очищает офскрин и зовёт drawBase */

  window.LabKinds['prob'] = function (cv, slide) {
    var exp = new Prob(cv);
    exp.row();
    return exp;
  };
})();

