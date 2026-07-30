
/* === S3 · верхний ярус: где частица МОЖЕТ оказаться ==========================
   Обязательный канвас №2, первая половина (РАЗБОР §3, §15).
   Слева вертикальная ось с отметками 0, 1, −1, 2, −2, …; вправо — время.
   Точки (без чисел!) проступают шаг за шагом, и видно, что они идут через одну.
   Сцены: 1 — только оси · 2 — точки набегают по столбцу · 3 — всё, десятый
   столбец подсвечен: ровно одиннадцать чётных точек (ответ на вопрос 1).
   ============================================================================ */
(function () {
  var LC = window.LabCore;
  var T = 10;                       // до десятого шага включительно

  function Reach(cv) {
    LC.Lab.call(this, cv, {});
    this.upto = 0;
  }
  Reach.prototype = Object.create(LC.Lab.prototype);

  Reach.prototype.settle = function () { this.upto = 0; };

  Reach.prototype.onScene = function (k) {
    this.scene = k;
    this.stop();
    if (k === 1) { this.upto = 0; this.draw(); return; }
    if (k >= 3) { this.upto = T; this.draw(); return; }
    var self = this, last = -1;                 // сцена 2 — набегают по столбцу
    this.upto = 0;
    this.animate(function (t) {
      var s = Math.min(T, Math.floor(t / 300));
      if (s !== last) { last = s; self.upto = s; self.draw(); }
      return s < T;
    });
  };

  Reach.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();
    var padL = 66, padR = 34, padY = 30;
    var dx = (W - padL - padR) / T;
    var dy = Math.min(dx, (H - 2 * padY) / (2 * T));
    var cy = H / 2;
    var X = function (t) { return padL + t * dx; };
    var Y = function (h) { return cy - h * dy; };

    /* ось положений слева: метки только у ближних уровней, дальше — засечки */
    c.strokeStyle = C.steel; c.lineWidth = 1.4;
    c.beginPath(); c.moveTo(padL - 26, Y(T)); c.lineTo(padL - 26, Y(-T)); c.stroke();
    for (var h = -T; h <= T; h++) {
      c.beginPath();
      c.moveTo(padL - 30, Y(h)); c.lineTo(padL - 22, Y(h));
      c.stroke();
      if (Math.abs(h) <= 2 || Math.abs(h) === T)
        this.label(String(h).replace('-', '−'), padL - 38, Y(h), 14, C.steel, 'right', '400');
    }
    /* ось времени снизу */
    c.strokeStyle = C.rule;
    c.setLineDash([5, 4]);
    c.beginPath(); c.moveTo(padL - 26, Y(0)); c.lineTo(X(T) + 16, Y(0)); c.stroke();
    c.setLineDash([]);

    /* точки достижимости: (t, h) достижимо, если |h| ≤ t и чётности совпадают */
    for (var t = 0; t <= this.upto; t++) {
      for (var k = -t; k <= t; k += 2) {
        var last = (t === this.upto && this.upto > 0);
        var hot = (this.scene >= 3 && t === T);
        c.fillStyle = hot ? C.brick : (last ? C.ink : C.steel);
        c.beginPath();
        c.arc(X(t), Y(k), hot ? 6 : (last ? 6 : 4.6), 0, 7);
        c.fill();
      }
    }
    if (this.scene >= 3) {
      c.strokeStyle = C.brick; c.lineWidth = 1.6;
      c.setLineDash([4, 4]);
      c.beginPath(); c.moveTo(X(T), Y(T) - 14); c.lineTo(X(T), Y(-T) + 14); c.stroke();
      c.setLineDash([]);
      this.label('11', X(T) + 22, Y(0), 22, C.brick, 'left');
    }
  };

  window.LabKinds.reach = function (cv) { return new Reach(cv); };
})();
