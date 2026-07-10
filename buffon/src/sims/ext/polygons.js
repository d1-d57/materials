
/* === lab-ext/polygons.js (вшито сборкой) === */
/* ============================================================
   SIM-4k: правильные k-угольники в узкой рейке (sl-polygons).
   Игла длины T погнута на k частей → правильный k-угольник
   периметра T. Пуант: доля пересечений → p/2 = 1/π при ЛЮБОМ k.
   База: window.LabCore.Lab (lab.js). Стиль: ILLUSTRATION-LANGUAGE.md.
   ============================================================ */
(function () {
  'use strict';

  function Polygons(cv) {
    var Lab = window.LabCore.Lab;
    Lab.call(this, cv, {
      spacing: 158, seed: 208, autoTarget: 110, endless: true,
      level: 2 / Math.PI / 2,            /* p/2 = 1/π ≈ .318 — риска на спарклайне */
      sparkEvery: 3, sparkLo: 0.10, sparkHi: 0.55
    });
    this.k = 8;                          /* по умолчанию — восьмиугольники (эталон p-26) */
    /* честная статистика: смещение по y равномерно на ЦЕЛОМ числе периодов
       (H = 6.75·T дало бы перекос); хвост ниже панели просто не виден */
    this.HP = Math.ceil(this.H / this.T) * this.T;
    this.drawBase = this.lines.bind(this);
    this.reset();
  }
  Polygons.prototype = Object.create(window.LabCore.Lab.prototype);

  /* честный бросок: центр равномерно по панели, поворот равномерно [0, 2π);
     выпуклый контур пересекает линию ⇔ линия проходит между minY и maxY */
  Polygons.prototype.throwOne = function (c) {
    var k = this.k, T = this.T;
    var side = T / k;                                  /* периметр = T = длина иглы */
    var R = side / (2 * Math.sin(Math.PI / k));        /* радиус описанной окружности */
    var cx = this.rng() * this.W, cy = this.rng() * this.H;
    var rot = this.rng() * 2 * Math.PI;
    var pts = [], minY = Infinity, maxY = -Infinity, j, a, x, y;
    for (j = 0; j < k; j++) {
      a = rot + j * 2 * Math.PI / k;
      x = cx + R * Math.cos(a); y = cy + R * Math.sin(a);
      pts.push([x, y]);
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }
    var band = function (yy) { return Math.floor((yy - T / 2) / T); };
    var hit = band(minY) !== band(maxY);
    c.strokeStyle = hit ? this.C.brick : this.C.steel; /* статусная окраска */
    c.lineWidth = 1.8; c.lineJoin = 'round';
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (j = 1; j < k; j++) c.lineTo(pts[j][0], pts[j][1]);
    c.closePath(); c.stroke();
    return hit;
  };

  Polygons.prototype.redraw = function () { this.draw(); };

  /* переключение k: подсветка кнопки, сброс к эталонному seed и автопрогон */
  Polygons.prototype.setK = function (k) {
    if (this.k === k) return;
    this.k = k;
    var self = this;
    (this._kBtns || []).forEach(function (b) {
      b.className = (+b.textContent === self.k) ? 'on' : '';
    });
    this.pause(); this.reset();
    window.LabCore.REDUCED ? this.throwN(this.target) : this.play();
  };

  /* приборка узкой рейки: счётчики + спарклайн доли с риской p/2 = 1/π */
  window.LabKinds = window.LabKinds || {};
  window.LabKinds['polygons'] = function (cv, slide) {
    var exp = new Polygons(cv);
    exp.row([
      { label: '4', act: function () { exp.setK(4); } },
      { label: '5', act: function () { exp.setK(5); } },
      { label: '8', act: function () { exp.setK(8); }, cls: 'on' }
    ]);
    /* узкая рейка (~265px): строка переносится в две, остаётся в панели */
    exp._kBtns = ['4', '5', '8'].map(function (t) {
      return Array.prototype.find.call(exp._row.children,
        function (b) { return b.textContent === t; });
    });
    exp._row.style.right = '8px';
    exp._row.style.whiteSpace = 'normal';
    exp._row.style.lineHeight = '1.7';
    return exp;
  };
})();

