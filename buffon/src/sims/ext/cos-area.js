
/* === lab-ext/cos-area.js (вшито сборкой) === */
/* ============================================================
   SIM «площадь под косинусом» (sl-area). ANIM-01-cos-area-spec.md.
   Точка P с единичной скоростью идёт по четверти единичной окружности,
   α — время. Горизонтальная проекция-путь x = sin α растёт 0→1; её скорость
   = cos α (спидометр: скорость — радиус, повёрнутый на 90°; золотая вертикаль
   = cos α). График скорости cos над осью 0…π/2; площадь под ним = путь = 1.
   Раскрытие по сценам через onScene: sc≤2 покой · sc3 дуга+путь ·
   sc4 +скорость+спидометр+график · sc5 +заливка площади. Без подписей —
   только точки-границы «1» и метка «π/2». «В покое = слайд»: автозапуск с
   нуля (G3), затем покой на финальном (полном) кадре.
   ============================================================ */
(function () {
  'use strict';
  function init() {
    if (!window.LabCore) return;
    var tokens = window.LabCore.tokens, REDUCED = window.LabCore.REDUCED;
    var PI = Math.PI, HALF = PI / 2;
    /* виртуальная система координат композиции (фит-трансформ в draw) —
       ВЫСОКАЯ доска: график скорости сверху / кинематика+спидометр снизу */
    var DW = 318, DH = 620;
    var G = { x0: 40, x1: 300, base: 212, top: 44 };   // график cos (верх)
    var SP = { x: 250, y: 290, r: 38 };                // спидометр (верх-право сцены)
    var O = { x: 58, y: 522 }, R = 182;                // дуга (низ)
    var Lv = 44;                                       // длина вектора скорости (в финале — вниз, но в панели)

    function CosArea(cv) {
      this.cv = cv; this.ctx = cv.getContext('2d');
      this.reveal = 1; this.t = 0;
      this.running = false; this.raf = 0; this.e = 0; this.last = 0;
      this.hold = 0.5; this.dur = 6.0; this.speed = 1;
      this.C = tokens();
      this.measure();
    }
    CosArea.prototype.measure = function () {
      var w = this.cv.clientWidth || parseFloat(this.cv.getAttribute('width')) || DW;
      var h = this.cv.clientHeight || parseFloat(this.cv.getAttribute('height')) || DH;
      this.W = w; this.H = h;
      var dpr = Math.min(devicePixelRatio || 1, 2);
      this.cv.width = w * dpr; this.cv.height = h * dpr;
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.draw();
    };
    /* ---- контракт покоя/сцен ---- */
    CosArea.prototype.onScene = function (k) {
      var rise = k >= 3 && this.reveal < 3;   // вход в раскрытие — играем с нуля (G3)
      this.reveal = k;
      if (rise) this.settle(); else this.draw();
    };
    CosArea.prototype.reset = function () {
      this.stop(); this.t = 0; this.e = 0; this.last = 0; this.draw();
    };
    CosArea.prototype.settle = function () {
      this.reset();
      if (REDUCED) { this.t = 1; this.draw(); }
      else this.play();
    };
    CosArea.prototype.stop = function () {
      this.running = false; if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0;
      this.syncRow();
    };
    CosArea.prototype.pause = function () { this.stop(); };
    CosArea.prototype.play = function () {
      if (this.running) return;
      if (this.t >= 1) { this.t = 0; this.e = 0; }
      this.running = true; this.last = 0; this.syncRow();
      var self = this;
      this.raf = requestAnimationFrame(function step(ts) {
        if (!self.running) return;
        if (!self.last) self.last = ts;
        var d = Math.min(0.05, (ts - self.last) / 1000); self.last = ts;
        self.e += d * self.speed;
        var m = (self.e - self.hold) / self.dur;          // ease-in у нуля через hold
        self.t = m <= 0 ? 0 : (m >= 1 ? 1 : m);
        self.draw();
        if (self.t >= 1) { self.running = false; self.raf = 0; self.syncRow(); return; }
        self.raf = requestAnimationFrame(step);
      });
    };
    /* ---- кнопки-глифы (док-строка канона) ---- */
    CosArea.prototype.row = function () {
      var host = this.cv.parentElement; host.style.overflow = 'visible';
      var row = document.createElement('div'); row.className = 'lab-row';
      var self = this;
      function btn(label, title, act) {
        var b = document.createElement('button'); b.textContent = label; b.title = title;
        b.addEventListener('click', function (e) { e.stopPropagation(); act(); });
        row.appendChild(b); return b;
      }
      this._play = btn('▸', 'играть', function () {
        if (self.running && self.speed === 1) { self.pause(); return; }
        self.speed = 1; self.play();
      });
      this._fast = btn('▸▸', 'быстрее', function () {
        if (self.running && self.speed > 1) { self.pause(); return; }
        self.speed = 2.4; self.play();
      });
      btn('↺', 'заново', function () { self.stop(); self.speed = 1; self.t = 0; self.e = 0; self.play(); });
      host.appendChild(row); this._row = row; this.syncRow();
    };
    CosArea.prototype.syncRow = function () {
      if (!this._row) return;
      if (this._play) this._play.textContent = (this.running && this.speed === 1) ? '❚❚' : '▸';
      if (this._fast) this._fast.textContent = (this.running && this.speed > 1) ? '❚❚' : '▸▸';
    };
    /* ---- примитивы ---- */
    function arrow(c, x1, y1, x2, y2, col, w) {
      var a = Math.atan2(y2 - y1, x2 - x1), h = 11;
      c.strokeStyle = col; c.fillStyle = col; c.lineWidth = w; c.lineCap = 'round';
      c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
      c.beginPath(); c.moveTo(x2, y2);
      c.lineTo(x2 - h * Math.cos(a - 0.42), y2 - h * Math.sin(a - 0.42));
      c.lineTo(x2 - h * Math.cos(a + 0.42), y2 - h * Math.sin(a + 0.42));
      c.closePath(); c.fill();
    }
    function num(c, x, y, s, col, al) {
      c.fillStyle = col; c.font = '18px "Noto Sans", sans-serif';
      c.textAlign = al || 'left'; c.textBaseline = 'alphabetic'; c.fillText(s, x, y);
    }
    function gx(a) { return G.x0 + (a / HALF) * (G.x1 - G.x0); }
    function gy(v) { return G.base + v * (G.top - G.base); }

    CosArea.prototype.draw = function () {
      var c = this.ctx, C = this.C;
      c.clearRect(0, 0, this.W, this.H);
      c.fillStyle = C.card; c.fillRect(0, 0, this.W, this.H);   // белая карточка = фон
      var s = Math.min(this.W / DW, this.H / DH);
      c.save();
      c.translate((this.W - DW * s) / 2, (this.H - DH * s) / 2); c.scale(s, s);
      if (this.reveal >= 3) { this._stage(c, C); }
      if (this.reveal >= 4) { this._graphFrame(c, C); this._speedo(c, C); this._graphCurve(c, C); }
      c.restore();
    };
    /* левая сцена: дуга, радиус, точка P, путь x, угол */
    CosArea.prototype._stage = function (c, C) {
      var a = this.t * HALF, sa = Math.sin(a), ca = Math.cos(a);
      var P = { x: O.x + R * sa, y: O.y - R * ca };
      var foot = { x: P.x, y: O.y };
      var faint = 'rgba(51,51,51,0.42)';
      /* оси */
      c.strokeStyle = C.steel; c.lineWidth = 2;
      c.beginPath(); c.moveTo(O.x, O.y + 10); c.lineTo(O.x, O.y - R - 20); c.stroke();
      c.beginPath(); c.moveTo(O.x - 10, O.y); c.lineTo(O.x + R + 20, O.y); c.stroke();
      /* дуга единичной окружности */
      c.strokeStyle = C.rule; c.lineWidth = 2;
      c.beginPath(); c.arc(O.x, O.y, R, -HALF, 0); c.stroke();
      /* точки-границы «1» */
      c.fillStyle = faint;
      c.beginPath(); c.arc(O.x, O.y - R, 3.5, 0, 7); c.fill();
      c.beginPath(); c.arc(O.x + R, O.y, 3.5, 0, 7); c.fill();
      num(c, O.x - 12, O.y - R + 6, '1', faint, 'right');
      num(c, O.x + R + 6, O.y - 7, '1', faint, 'left');
      /* угол α у O */
      c.strokeStyle = C.steel; c.lineWidth = 1.6;
      c.beginPath(); c.arc(O.x, O.y, 46, -HALF, -HALF + a); c.stroke();
      /* проекция-путь x (пунктир от P на ось + жирный путь O→foot) — со сцены 4 (A4) */
      if (this.reveal >= 4) {
        c.setLineDash([4, 5]); c.strokeStyle = C.steel; c.lineWidth = 1.6;
        c.beginPath(); c.moveTo(P.x, P.y); c.lineTo(foot.x, foot.y); c.stroke(); c.setLineDash([]);
        c.strokeStyle = C.brick; c.lineWidth = 5; c.lineCap = 'butt';
        c.beginPath(); c.moveTo(O.x, O.y); c.lineTo(foot.x, foot.y); c.stroke();
        c.fillStyle = C.brick; c.beginPath(); c.arc(foot.x, foot.y, 4.5, 0, 7); c.fill();
      }
      /* радиус O→P */
      c.strokeStyle = C.ink; c.lineWidth = 2.4;
      c.beginPath(); c.moveTo(O.x, O.y); c.lineTo(P.x, P.y); c.stroke();
      /* вектор скорости у точки (со сцены 4) */
      if (this.reveal >= 4) {
        var vdx = ca, vdy = sa;                          // dir = (cosα, sinα) экранно
        arrow(c, P.x, P.y, P.x + Lv * vdx, P.y + Lv * vdy, C.brick, 3);
      }
      /* точка P */
      c.fillStyle = C.mustard; c.strokeStyle = C.card; c.lineWidth = 2.6;
      c.beginPath(); c.arc(P.x, P.y, 7.5, 0, 7); c.fill(); c.stroke();
    };
    /* спидометр: скорость = радиус, повёрнутый на 90°; золотая вертикаль = cos */
    CosArea.prototype._speedo = function (c, C) {
      var a = this.t * HALF, sa = Math.sin(a), ca = Math.cos(a);
      var vdx = -sa, vdy = -ca;                           // дайл: вертикаль несёт cos
      c.strokeStyle = C.rule; c.lineWidth = 1.6;
      c.beginPath(); c.arc(SP.x, SP.y, SP.r, 0, 7); c.stroke();
      c.fillStyle = 'rgba(51,51,51,0.42)';
      c.beginPath(); c.arc(SP.x, SP.y, 2.6, 0, 7); c.fill();
      /* золотая вертикаль = cos α */
      c.strokeStyle = C.mustard; c.lineWidth = 5;
      c.beginPath(); c.moveTo(SP.x, SP.y); c.lineTo(SP.x, SP.y + SP.r * vdy); c.stroke();
      arrow(c, SP.x, SP.y, SP.x + SP.r * vdx, SP.y + SP.r * vdy, C.brick, 2.4);
    };
    /* рамка графика скорости (пустая координатная система — с сцены 3) */
    CosArea.prototype._graphFrame = function (c, C) {
      var faint = 'rgba(51,51,51,0.42)';
      c.strokeStyle = C.steel; c.lineWidth = 2;
      c.beginPath(); c.moveTo(G.x0, G.top - 8); c.lineTo(G.x0, G.base); c.lineTo(G.x1 + 8, G.base); c.stroke();
      c.setLineDash([3, 5]); c.strokeStyle = C.rule; c.lineWidth = 1.4;
      c.beginPath(); c.moveTo(G.x0, gy(1)); c.lineTo(G.x1, gy(1)); c.stroke(); c.setLineDash([]);
      num(c, G.x0 - 10, gy(1) + 6, '1', faint, 'right');
      num(c, G.x0 - 10, G.base + 6, '0', faint, 'right');
      num(c, G.x1, G.base + 26, 'π/2', faint, 'center');
    };
    /* кривая cos + (сцена 5) заливка площади + маркер */
    CosArea.prototype._graphCurve = function (c, C) {
      var a = this.t * HALF, ca = Math.cos(a);
      if (this.reveal >= 5) {                            // заливка ПОД кривой — первой
        c.fillStyle = 'rgba(201,162,60,0.30)';
        c.beginPath(); c.moveTo(G.x0, G.base);
        for (var i = 0; i <= 90; i++) { var aa = a * i / 90; c.lineTo(gx(aa), gy(Math.cos(aa))); }
        c.lineTo(gx(a), G.base); c.closePath(); c.fill();
      }
      c.strokeStyle = C.brick; c.lineWidth = 3; c.lineCap = 'round';
      c.beginPath();
      for (var j = 0; j <= 120; j++) { var b = HALF * j / 120, X = gx(b), Y = gy(Math.cos(b)); j ? c.lineTo(X, Y) : c.moveTo(X, Y); }
      c.stroke();
      c.fillStyle = C.brick; c.beginPath(); c.arc(gx(a), gy(ca), 5.5, 0, 7); c.fill();
    };

    window.LabKinds = window.LabKinds || {};
    window.LabKinds['cos-area'] = function (cv) { var e = new CosArea(cv); e.row(); return e; };
  }
  window.LabCore ? init() : addEventListener('load', init);
})();

