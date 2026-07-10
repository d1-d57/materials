
/* === lab-ext/result.js (вшито сборкой) === */
/* ============================================================
   SIM-4r: выпуклые контуры (sl-result, панель .p-contours)
   Бросаем случайные выпуклые контуры РАЗНЫХ периметров L ∈ [0.6T, T]
   (эллипсы / капсулы / скруглённые треугольники) на разлиновку с шагом T.
   Честная физика: выпуклый контур пересекает горизонталь 0 или 2 раза,
   значит число пересечений = 2 × (линий внутри [ymin, ymax]).
   Среднее число пересечений на бросок → 2·L̄/(πT) (формула Коши:
   средняя ширина выпуклого контура = L/π). Карточка: среднее/прогноз,
   спарклайн среднего без уровня — уровень у каждого периметра свой.
   Стиль: ILLUSTRATION-LANGUAGE.md (только токены this.C).
   ============================================================ */
(function () {
  'use strict';
  window.LabKinds = window.LabKinds || {};
  window.LabKinds['result'] = function (cv) {
    var Lab = window.LabCore.Lab;
    var exp = Object.create(Lab.prototype);
    Lab.call(exp, cv, { spacing: 158, seed: 30141, autoTarget: 120, endless: true, level: 2 / Math.PI,
                        sparkEvery: 5 });
    exp.drawBase = exp.lines.bind(exp);

    exp.resetState = function () {
      Lab.prototype.resetState.call(this);
      this.sumL = 0;                       // сумма брошенных периметров
    };

    /* hit = ЧИСЛО пересечений (0/2), не индикатор — поэтому свой throwN */
    exp.throwN = function (n) {
      for (var i = 0; i < n; i++) {
        var k = this.throwOne(this.octx);
        this.n++; this.hit += k;
        if (this.n % this.sparkEvery === 0) this.spark.push(this.hit / this.n);
      }
      this.draw();
    };

    /* ---------- три семейства выпуклых контуров периметра L ---------- */
    /* каждое возвращает {y0,y1,path}: точный вертикальный габарит + путь */
    exp.ellipse = function (L, cx, cy, th) {
      var q = 0.55 + 0.4 * (this._shape ? this._shape.a : this.rng()); // b/a фиксирован: ОДИН овал
      var P1 = Math.PI * (3 * (1 + q) - Math.sqrt((3 + q) * (1 + 3 * q))); // Рамануджан, a=1
      var a = L / P1, b = q * a;
      var hy = Math.sqrt(a * a * Math.sin(th) * Math.sin(th) +
                         b * b * Math.cos(th) * Math.cos(th));
      return { y0: cy - hy, y1: cy + hy, path: function (c) {
        c.ellipse(cx, cy, a, b, th, 0, 7);
      } };
    };
    exp.capsule = function (L, cx, cy, th) {
      var rho = 0.35 + 0.3 * (this._shape ? this._shape.b : this.rng()); // фиксирован
      var s = L / (2 + 2 * Math.PI * rho), r = rho * s;
      var ux = Math.cos(th), uy = Math.sin(th);
      var hy = Math.abs(uy) * s / 2 + r;
      return { y0: cy - hy, y1: cy + hy, path: function (c) {
        c.arc(cx - ux * s / 2, cy - uy * s / 2, r, th + Math.PI / 2, th + 3 * Math.PI / 2);
        c.arc(cx + ux * s / 2, cy + uy * s / 2, r, th - Math.PI / 2, th + Math.PI / 2);
        c.closePath();
      } };
    };
    exp.roundTri = function (L, cx, cy, th) {
      var rho = 0.22 + 0.18 * this.rng();  // r/s — мягкость углов
      var s = L / (3 + 2 * Math.PI * rho), r = rho * s;  // сумма Минковского: P = 3s + 2πr
      var R = s / Math.sqrt(3), v = [], k;
      for (k = 0; k < 3; k++) {
        var a = th + k * 2 * Math.PI / 3;
        v.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]);
      }
      var ang = [];                        // углы внешних нормалей рёбер k→k+1
      for (k = 0; k < 3; k++) {
        var p = v[k], w = v[(k + 1) % 3];
        ang.push(Math.atan2(-(w[0] - p[0]), w[1] - p[1]));
      }
      return {
        y0: Math.min(v[0][1], v[1][1], v[2][1]) - r,
        y1: Math.max(v[0][1], v[1][1], v[2][1]) + r,
        path: function (c) {
          for (var k = 0; k < 3; k++) c.arc(v[k][0], v[k][1], r, ang[(k + 2) % 3], ang[k]);
          c.closePath();
        }
      };
    };

    exp.throwOne = function (c) {
      var L = this.T;                                     // периметр = шагу линий (как всюду)
      if (!this._shape) this._shape = { kind: this.rng(), a: this.rng(), b: this.rng() }; // ОДИН контур
      // подмешиваем кэш формы вместо новых случайных параметров
      var SH = this._shape;
      var cx = this.rng() * this.W, cy = this.rng() * this.H;
      var th = this.rng() * 2 * Math.PI;
      var t = this.rng();
      var t1 = this._shape ? this._shape.kind : t;   // ОДНО семейство на весь опыт
      var g = t1 < 1 / 3 ? this.ellipse(L, cx, cy, th)
            : t1 < 2 / 3 ? this.capsule(L, cx, cy, th)
            :              this.roundTri(L, cx, cy, th);
      var T = this.T, band = function (y) { return Math.floor((y - T / 2) / T); };
      var cross = 2 * (band(g.y1) - band(g.y0));          // выпуклость: 2 на линию
      this.sumL += L;
      c.strokeStyle = cross ? this.C.brick : this.C.steel;
      c.lineWidth = 1.8; c.lineJoin = 'round';
      c.beginPath(); g.path(c); c.stroke();
      return cross;
    };

    /* ---------- приборка: N, среднее, прогноз 2L̄/(πT), спарклайн ---------- */
    exp.reset();
    exp.row();
    /* узкая панель (263px): строка в две строки, мельче */
    var st = exp._row.style;
    st.whiteSpace = 'normal'; st.right = '8px'; st.fontSize = '13px'; st.lineHeight = '1.5';
    return exp;
  };
})();

