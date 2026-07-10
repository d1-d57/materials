
/* === lab-ext/convergence.js (вшито сборкой) === */
/* ============================================================
   SIM-2: живой график сходимости (sl-convergence, панель 950×533).
   В покое = статичный SVG ill-sl-convergence-1: 5 кирпичных серий
   с убывающей прозрачностью, горчичный уровень 2/π, сетка rule,
   подписи осей. Живость: ⏵ докидывает броски всем 5 сериям
   синхронно, ось X — окно 1..max(5000, N). Приборки нет (dash:false),
   вместо неё текущие доли серий mono справа от концов кривых.
   Физика честная: d ~ U[0, T/2], θ ~ U[0, π), L = T → P = 2/π.
   ============================================================ */
(function () {
  'use strict';

  function init() {
    if (!window.LabCore) return;
    var Lab = window.LabCore.Lab;

    /* геометрия канона (SVG ill-sl-convergence-1, 950×533) */
    var PADL = 70, PADR = 66, TOP = 36, PADB = 43;   // ось на H-43 (= 490)
    var V_LO = 0.45, V_HI = 0.85;                    // видимый диапазон долей
    var GRID = [0.50, 0.60, 0.70, 0.80];
    var ALPHAS = [0.45, 0.55, 0.70, 0.85, 1.0];
    var LEVEL = 2 / Math.PI;

    function Conv(cv) {
      Lab.call(this, cv, {
        seed: 9203, autoTarget: 5000, dash: false,
        sparkEvery: 1e9, level: LEVEL
      });
      this.speed = 4;                  // автопрогон покоя живой, но не вечный
      this.reset();
    }
    Conv.prototype = Object.create(Lab.prototype);

    Conv.prototype.resetState = function () {
      Lab.prototype.resetState.call(this);
      this.target = this.o.autoTarget; // ⏵-добавки не переживают сброс
      this.S = [[], [], [], [], []];   // кумулятивные счётчики пересечений
    };

    /* один «бросок» = по игле каждой из 5 серий; честная физика */
    Conv.prototype.throwOne = function () {
      var hit = false;
      for (var s = 0; s < 5; s++) {
        var d = this.rng() * 0.5;                    // центр → ближайшая линия
        var th = this.rng() * Math.PI;               // наклон иглы
        var h = d <= 0.5 * Math.sin(th);             // L = T: P = 2/π
        var arr = this.S[s];
        arr.push((arr.length ? arr[arr.length - 1] : 0) + (h ? 1 : 0));
        if (s === 4) hit = h;                        // основная серия — в ядро
      }
      return hit;
    };

    /* ⏵ после покоя докидывает следующее окно — кривые растут вправо */
    Conv.prototype.settle = function () {
      this.reset();                           // всегда с нуля на входе
      this.throwN(50);                        // 0..50 уже отрисовано (шумный старт вне области — скрыт)
      if (!window.LabCore.REDUCED) this.play(); else this.throwN(this.target - this.n);
    };
    Conv.prototype.play = function () {
      if (!this.running && this.n >= this.target)
        this.target = this.n + this.o.autoTarget;
      Lab.prototype.play.call(this);
    };

    Conv.prototype.draw = function () {
      this.redraw();
      Lab.prototype.draw.call(this);
    };

    /* ---------- отрисовка целиком (оси и кривые — сами, по канону SVG) ---------- */
    Conv.prototype.maxN = function () { return Math.max(this.o.autoTarget, this.n); };
    Conv.prototype.tickStep = function (maxN) {
      var steps = [1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000, 100000];
      for (var i = 0; i < steps.length; i++) if (maxN / steps[i] <= 5.2) return steps[i];
      return 200000;
    };

    Conv.prototype.redraw = function () {
      var c = this.octx, C = this.C, W = this.W, H = this.H;
      var x0 = PADL, x1 = W - PADR, axisY = H - PADB, plotW = x1 - x0;
      var maxN = this.maxN();
      function yOf(v) { return axisY - (v - V_LO) / (V_HI - V_LO) * (axisY - TOP); }
      function xOf(N) { return x0 + (N / maxN) * plotW; }

      c.fillStyle = C.card; c.fillRect(0, 0, W, H);

      /* сетка rule */
      c.strokeStyle = C.rule; c.lineWidth = 1.25; c.beginPath();
      for (var g = 0; g < GRID.length; g++) {
        var gy = yOf(GRID[g]);
        c.moveTo(x0, gy); c.lineTo(x1, gy);
      }
      c.stroke();

      /* уровень 2/π — горчица */
      var ly = yOf(LEVEL);
      c.strokeStyle = C.mustard; c.lineWidth = 2; c.beginPath();
      c.moveTo(x0, ly); c.lineTo(x1, ly); c.stroke();

      /* ось X — сталь, риски, подписи */
      c.strokeStyle = C.steel; c.lineWidth = 2.5; c.lineCap = 'butt'; c.beginPath();
      c.moveTo(x0, axisY); c.lineTo(x1, axisY); c.stroke();
      var step = this.tickStep(maxN), N;
      c.lineWidth = 1.5; c.beginPath();
      for (N = step; N <= maxN; N += step) { c.moveTo(xOf(N), axisY); c.lineTo(xOf(N), axisY + 7); }
      c.stroke();
      c.fillStyle = C.ink; c.globalAlpha = .7;
      c.font = '16px "Noto Sans",sans-serif'; c.textAlign = 'center'; c.textBaseline = 'alphabetic';
      for (N = step; N <= maxN; N += step) c.fillText(String(N), xOf(N), axisY + 28);

      /* подписи оси Y */
      c.textAlign = 'right'; c.textBaseline = 'middle';
      for (g = 0; g < GRID.length; g++) c.fillText(GRID[g].toFixed(2), x0 - 12, yOf(GRID[g]));
      c.globalAlpha = 1;

      /* 5 кривых — кирпич с убывающей прозрачностью, клип по полю графика */
      var n = this.n;
      if (n > 1) {
        c.save();
        c.beginPath(); c.rect(x0, TOP, plotW, axisY - TOP); c.clip();
        c.strokeStyle = C.brick; c.lineWidth = 2.2;
        c.lineJoin = 'round'; c.lineCap = 'round';
        for (var s = 0; s < 5; s++) {
          var cum = this.S[s];
          c.globalAlpha = ALPHAS[s];
          c.beginPath();
          var endX = xOf(n), first = true;
          for (var px = 0; ; px += 2) {
            var x = x0 + px, last = false;
            if (x >= endX) { x = endX; last = true; }
            var i = Math.max(1, Math.min(n, Math.round((x - x0) / plotW * maxN))); // кривые от нуля
            var y = yOf(cum[i - 1] / i);
            first ? c.moveTo(x, y) : c.lineTo(x, y);
            first = false;
            if (last) break;
          }
          c.stroke();
        }
        c.globalAlpha = 1;
        c.restore();
      }

      /* подписи справа: 2/π + текущие доли серий мелким mono, без наложений */
      var items = [{ kind: 'level', ty: ly }];
      if (n) for (s = 0; s < 5; s++)
        items.push({ kind: 'frac', s: s, v: this.S[s][n - 1] / n,
                     ty: yOf(this.S[s][n - 1] / n) });
      layout(items, 17, TOP + 10, axisY - 10);
      c.textAlign = 'left'; c.textBaseline = 'middle';
      for (var k = 0; k < items.length; k++) {
        var it = items[k];
        if (it.kind === 'level') {
          c.fillStyle = C.mustard; c.globalAlpha = 1;
          c.font = 'italic 18px "Noto Sans",sans-serif';
          c.fillText('≈ 0,63', x1 + 12, it.y);
        } else {
          c.fillStyle = C.brick; c.globalAlpha = Math.max(.55, ALPHAS[it.s]);
          c.font = '14px "Courier Prime",monospace';
          c.fillText(it.v.toFixed(3), x1 + 12, it.y);
        }
      }
      c.globalAlpha = 1; c.textBaseline = 'alphabetic';
    };

    /* раскладка подписей: кластеры наезжающих разводятся вокруг среднего */
    function layout(items, gap, minY, maxY) {
      items.sort(function (a, b) { return a.ty - b.ty; });
      var cl = [];
      function fit(c) {
        var span = (c.items.length - 1) * gap;
        var sum = 0;
        c.items.forEach(function (x) { sum += x.ty; });
        c.y = sum / c.items.length - span / 2;
        if (c.y < minY) c.y = minY;
        if (c.y + span > maxY) c.y = maxY - span;
      }
      items.forEach(function (it) {
        cl.push({ items: [it] }); fit(cl[cl.length - 1]); // (кластеризация уже раздвигает)
        while (cl.length > 1) {
          var a = cl[cl.length - 2], b = cl[cl.length - 1];
          if (a.y + (a.items.length - 1) * gap + gap > b.y) {
            a.items = a.items.concat(b.items); cl.pop(); fit(a);
          } else break;
        }
      });
      cl.forEach(function (c) {
        c.items.forEach(function (it, i) { it.y = c.y + i * gap; });
      });
    }

    window.LabKinds = window.LabKinds || {};
    window.LabKinds['convergence'] = function (cv, slide) {
      var exp = new Conv(cv);
      exp.row();
      return exp;
    };
  }

  window.LabCore ? init() : addEventListener('load', init);
})();

