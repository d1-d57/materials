
/* === S5A · монетка и три облика одного исхода ================================
   РАЗБОР §5A: слева нарисована монетка, на ней мигают орёл и решка — идёт
   случайная последовательность. Одновременно вдоль полосы строятся ТРИ ОБЛИКА
   СРАЗУ: ломаная, маршрут в решётке и цепочка кружков. Один и тот же исход
   в трёх видах, на глазах.
   ============================================================================ */
(function () {
  var LC = window.LabCore;
  var N = 8;

  function Views(cv) {
    LC.Lab.call(this, cv, {});
    this.reset();
  }
  Views.prototype = Object.create(LC.Lab.prototype);

  Views.prototype.reset = function () {
    this.rng = LC.mulberry32(Math.floor(Math.random() * 1e9));
    this.w = [];
    for (var i = 0; i < N; i++) this.w.push(this.rng() < 0.5 ? 1 : -1);
    this.shown = 0;
  };
  Views.prototype.settle = function () { this.reset(); this.shown = N; this.draw(); };
  Views.prototype.onScene = function (k) { this.scene = k; this.draw(); };

  Views.prototype.play = function () {
    var self = this, last = -1;
    this.animate(function (t) {
      var k = Math.floor(t / 620);
      if (k !== last) { last = k; self.shown = Math.min(k, N); self.draw(); }
      if (k > N + 3) { self.reset(); self.play(); return false; }
      return true;
    });
  };

  /* Полоса, а не столбик: доска здесь широкая и низкая (≈1150×290), и три облика,
     сложенные друг под друга, вырождались в три ниточки. Раскладка — вдоль полосы:
     монетка · ломаная · цепочка кружков · маршрут в решётке. */
  Views.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();
    var n = this.shown;
    var cur = n > 0 ? this.w[n - 1] : null;
    var cy = H / 2;

    /* монетка слева: мигает буквой последнего броска */
    var r = Math.min(58, H * 0.30);
    var cx = 20 + r;
    c.strokeStyle = C.ink; c.lineWidth = 2.6;
    c.fillStyle = C.paper;
    c.beginPath(); c.arc(cx, cy, r, 0, 7); c.fill(); c.stroke();
    if (cur !== null)
      this.label(cur > 0 ? 'О' : 'Р', cx, cy, r * 0.95, cur > 0 ? C.brick : C.steel);

    var x0 = cx + r + 34;
    var rest = W - x0 - 24;
    var w1 = rest * 0.42, w2 = rest * 0.26, w3 = rest * 0.32;

    /* облик 1 — ломаная */
    var dx = w1 / N, dy = Math.min(24, (H - 60) / 6);
    var yb = cy + dy;
    c.strokeStyle = C.rule; c.lineWidth = 1.2; c.setLineDash([5, 4]);
    c.beginPath(); c.moveTo(x0 - 8, yb); c.lineTo(x0 + w1 + 8, yb); c.stroke();
    c.setLineDash([]);
    var h = 0;
    c.strokeStyle = C.ink; c.lineWidth = 2.8; c.lineJoin = 'round'; c.lineCap = 'round';
    c.beginPath(); c.moveTo(x0, yb);
    for (var i = 0; i < n; i++) { h += this.w[i]; c.lineTo(x0 + (i + 1) * dx, yb - h * dy); }
    c.stroke();
    h = 0;
    for (var i2 = 0; i2 <= n; i2++) {
      if (i2 > 0) h += this.w[i2 - 1];
      c.fillStyle = C.card; c.strokeStyle = C.ink; c.lineWidth = 1.5;
      c.beginPath(); c.arc(x0 + i2 * dx, yb - h * dy, 4.5, 0, 7); c.fill(); c.stroke();
    }

    /* облик 2 — цепочка кружков в два ряда: залитый = орёл */
    var bx = x0 + w1 + 26;
    var rr = Math.min(15, w2 / 10);
    for (var j = 0; j < N; j++) {
      var on = j < n;
      var col = j % 4, row = Math.floor(j / 4);
      c.beginPath();
      c.arc(bx + (col + 0.5) * rr * 2.7, cy + (row - 0.5) * rr * 2.9, rr, 0, 7);
      c.fillStyle = on ? (this.w[j] > 0 ? C.ink : C.card) : C.card;
      c.fill();
      c.strokeStyle = on ? C.ink : C.rule; c.lineWidth = 1.8; c.stroke();
    }

    /* облик 3 — маршрут в решётке: орёл — вправо, решка — вверх */
    var cell = Math.min(w3 / (N + 1), (H - 44) / (N + 1));
    var gx = bx + w2 + 26, gy = cy + N * cell / 2;
    c.strokeStyle = C.rule; c.lineWidth = 1;
    for (var a = 0; a <= N; a++) {
      c.beginPath(); c.moveTo(gx + a * cell, gy); c.lineTo(gx + a * cell, gy - N * cell); c.stroke();
      c.beginPath(); c.moveTo(gx, gy - a * cell); c.lineTo(gx + N * cell, gy - a * cell); c.stroke();
    }
    c.strokeStyle = C.brick; c.lineWidth = 2.8; c.lineJoin = 'round';
    c.beginPath(); c.moveTo(gx, gy);
    var px = gx, py = gy;
    for (var s = 0; s < n; s++) {
      if (this.w[s] > 0) px += cell; else py -= cell;
      c.lineTo(px, py);
    }
    c.stroke();
    c.fillStyle = C.brick;
    c.beginPath(); c.arc(px, py, 5.5, 0, 7); c.fill();
  };

  window.LabKinds.views = function (cv) {
    var v = new Views(cv);
    v.row([{ glyph: '↺', title: 'ещё одна последовательность',
             act: function () { v.stop(); v.reset(); v.play(); } }]);
    return v;
  };
})();
