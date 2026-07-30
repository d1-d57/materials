
/* === S3-нижний ярус · вероятности заполняются по столбцу =====================
   Обязательный канвас №2, вторая половина (РАЗБОР §3, §15).
     сцена 1 — в нуле стоит единица, и всё;
     сцена 2 — столбцы 1 и 2 проступают по одному;
     сцена 3 — открывается столбец 3 (ответ на вопрос 2: 1/8, 3/8, 3/8, 1/8);
     сцена 4 — в клетку последнего столбца приходят две стрелки с коэффициентом ½;
     сцена 5 — обведены сама клетка и два её соседа слева, из которых она сложилась.

   🔴 Правило соседей показывается НА ЖИВОЙ ЗАПОЛНЕННОЙ таблице. Прежний рисунок —
   две белые точки со стрелками в пустоте — разбор забраковал прямо (§3).
   ============================================================================ */
(function () {
  var LC = window.LabCore;
  var T = 7;                    // столбцы 0…7. §3 разбора: «довести до 7–8 шага,
                                // а не до 4–5» — тогда узор виден, а не намечен

  function C2(n, k) {                          // биномиальный коэффициент
    var r = 1;
    for (var i = 0; i < k; i++) r = r * (n - i) / (i + 1);
    return Math.round(r);
  }

  function Probs(cv) { LC.Lab.call(this, cv, {}); }
  Probs.prototype = Object.create(LC.Lab.prototype);
  Probs.prototype.settle = function () { this.upto = 0; };

  Probs.prototype.onScene = function (k) {
    this.scene = k;
    this.stop();
    var target = (k <= 1) ? 0 : (k === 2 ? 3 : T);
    if (k !== 2) { this.upto = target; this.draw(); return; }
    var self = this, last = -1;
    this.upto = 0;
    this.animate(function (t) {
      var s = Math.min(target, Math.floor(t / 520));
      if (s !== last) { last = s; self.upto = s; self.draw(); }
      return s < target;
    });
  };

  /* дробь двумя этажами: числитель, черта, знаменатель */
  Probs.prototype.frac = function (num, den, x, y, size, color) {
    var c = this.ctx;
    if (den === 1) { this.label(String(num), x, y, size * 1.15, color); return; }
    this.label(String(num), x, y - size * 0.52, size, color);
    this.label(String(den), x, y + size * 0.56, size, color);
    c.save();
    c.strokeStyle = color || this.C.ink;
    c.lineWidth = 1.6;
    var w = size * 0.62;
    c.beginPath(); c.moveTo(x - w, y + 1); c.lineTo(x + w, y + 1); c.stroke();
    c.restore();
  };

  Probs.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();
    var padL = 56, padR = 40, padY = 16;
    var dx = (W - padL - padR) / T;
    var dy = Math.min(dx * 0.66, (H - 2 * padY) / (2 * T));
    var cy = H / 2;
    var X = function (t) { return padL + t * dx; };
    var Y = function (h) { return cy - h * dy; };
    var size = Math.max(15, Math.min(26, dy * 0.62));

    c.strokeStyle = C.rule; c.lineWidth = 1.3;
    c.setLineDash([5, 4]);
    c.beginPath(); c.moveTo(padL - 26, Y(0)); c.lineTo(X(T) + 26, Y(0)); c.stroke();
    c.setLineDash([]);

    for (var t = 0; t <= this.upto; t++) {
      for (var j = 0; j <= t; j++) {
        var h = 2 * j - t;
        var fresh = (t === this.upto && this.upto > 0);
        this.frac(C2(t, j), Math.pow(2, t), X(t), Y(h), size,
                  fresh ? C.brick : C.ink);
      }
    }

    if (this.scene >= 4 && this.upto >= T) {
      /* две стрелки в клетку (4, h=0) из (3, +1) и (3, −1), обе с коэффициентом ½ */
      var tx = X(T), ty = Y(0);
      [1, -1].forEach(function (s) {
        var sx = X(T - 1), sy = Y(s);
        var ux = tx - sx, uy = ty - sy, L = Math.hypot(ux, uy);
        ux /= L; uy /= L;
        var ax = sx + ux * 30, ay = sy + uy * 26;
        var bx = tx - ux * 32, by = ty - uy * 26;
        c.strokeStyle = C.brick; c.lineWidth = 1.8;
        c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
        c.fillStyle = C.brick;                       // ЗАЛИТЫЙ наконечник
        c.beginPath();
        c.moveTo(bx + ux * 9, by + uy * 9);
        c.lineTo(bx - uy * 4.5, by + ux * 4.5);
        c.lineTo(bx + uy * 4.5, by - ux * 4.5);
        c.closePath(); c.fill();
      }, this);
      this.frac(1, 2, (X(T - 1) + tx) / 2 + 4, (Y(1) + ty) / 2 - 16, size * 0.8, C.brick);
      this.frac(1, 2, (X(T - 1) + tx) / 2 + 4, (Y(-1) + ty) / 2 + 16, size * 0.8, C.brick);
    }
    if (this.scene >= 5 && this.upto >= T) {
      /* обводим клетку и ДВУХ её соседей слева — те самые, из которых она
         сложилась с коэффициентами ½ (числа считаются, не вписаны руками) */
      c.strokeStyle = C.brick; c.lineWidth = 2;
      c.beginPath(); c.arc(X(T), Y(0), size * 1.45, 0, 7); c.stroke();
      c.strokeStyle = C.mustard; c.lineWidth = 2;
      c.beginPath(); c.arc(X(T - 1), Y(1), size * 1.35, 0, 7); c.stroke();
      c.beginPath(); c.arc(X(T - 1), Y(-1), size * 1.35, 0, 7); c.stroke();
    }
  };

  window.LabKinds.probs = function (cv) { return new Probs(cv); };
})();
