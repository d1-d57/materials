
/* === S2 · пожарная лестница и растущий из неё график =========================
   Обязательный канвас №1 (РАЗБОР §15, §17.1, §17.7). Один рисунок в ДВЕ ФАЗЫ,
   а не два рядом:
     сцены 1–2 — вертикальная лестница, по ней ходит точка; внизу лестница
                 кончается, шаг с нижней ступеньки — падение; каждый прогон
                 случайный, кнопка ↺ запускает новый;
     сцена 3   — лестница уезжает влево, из неё вырастает ось времени, и вправо
                 разворачивается график того же движения: та самая ломаная,
                 с буквами О и Р под звеньями.
   Смысл кадра (§16.1): по точке считать невозможно, а по графику — можно.
   ============================================================================ */
(function () {
  var LC = window.LabCore;

  var STEPS = 16;          // сколько шагов показываем в одном прогоне
  var START = 3;           // пьяница ЗАБРАЛСЯ на лестницу — стартует не с нижней
                           // ступеньки: из нуля симметричное блуждание срывается
                           // в среднем за пару шагов, и смотреть было не на что
  var TOP = 5;             // ступенек выше нуля: на короткой доске 7 давали
                         // ступеньку в 21px — лестница читалась как штрих

  function Ladder(cv) {
    LC.Lab.call(this, cv, {});
    this.reset();
  }
  Ladder.prototype = Object.create(LC.Lab.prototype);

  Ladder.prototype.reset = function (seed) {
    this.rng = LC.mulberry32(seed != null ? seed : Math.floor(Math.random() * 1e9));
    this.w = [];             // шаги ±1
    this.h = [START];        // высоты, начиная со стартовой ступеньки
    this.shown = 0;          // сколько шагов уже показано
    var h = START;
    for (var i = 0; i < STEPS; i++) {
      var up = this.rng() < 0.5;
      if (h >= TOP) up = false;                 // выше лестницы не лезем
      this.w.push(up ? 1 : -1);
      h += up ? 1 : -1;
      this.h.push(h);
      if (h < 0) break;                          // сорвался — прогон кончен
    }
    this.fell = h < 0;
  };

  Ladder.prototype.settle = function () {
    /* «в покое = статичный слайд» (канон симуляций): на входе прогон уже пройден,
       пустого кадра зал не видит. Кнопка ↺ проигрывает заново — и вот там прогон
       уже любой, в том числе с падением: разбор просит, чтобы срывались не все.
       В ПОКОЕ показываем прогон, который дожил до конца, иначе первый же взгляд
       на слайд — это лежащая под лестницей точка и ломаная в два звена. */
    for (var t = 0; t < 300 && this.fell; t++) this.reset();
    this.shown = this.w.length;
    this.draw();
  };

  Ladder.prototype.play = function () {
    var self = this, last = -1;
    this.animate(function (t) {
      var k = Math.floor(t / 380);
      if (k === last) return true;
      last = k;
      self.shown = Math.min(k, self.w.length);
      self.draw();
      if (self.shown >= self.w.length) {
        if (t > 380 * self.w.length + 1400) {   // подержали финал и пошли заново
          self.reset(); self.shown = 0; self.play(); return false;
        }
      }
      return true;
    });
  };

  Ladder.prototype.onScene = function (k) {
    this.scene = k;
    this.stop();
    /* На третьей сцене график должен быть УЖЕ ПОСТРОЕН: лектор приходит сюда, чтобы
       сказать «вот она, ломаная», а не смотреть, как она набирается. Движение зал
       уже видел на первых двух сценах; кнопка ↺ проигрывает заново по желанию. */
    for (var t = 0; t < 300 && this.fell; t++) this.reset();
    this.shown = this.w.length;
    this.draw();
  };

  Ladder.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();
    var graph = this.scene >= 3;

    var railW = 78;
    var lx = graph ? 54 : (W - railW) / 2;        // фаза 1 — лестница по центру
    var pad = 20, letterRoom = 30;                // строка букв О/Р живёт ПОД обрывом
    var rung = Math.min(52, (H - 2 * pad - letterRoom) / (TOP + 2));
    var y0 = H - pad - letterRoom - rung;         // y нулевой ступеньки
    var Y = function (h) { return y0 - h * rung; };

    /* лестница: две тетивы и ступеньки, снизу обрыв */
    c.strokeStyle = C.ink; c.lineWidth = 2.4; c.lineCap = 'round';
    c.beginPath();
    c.moveTo(lx, Y(TOP) - rung * 0.6); c.lineTo(lx, Y(0));
    c.moveTo(lx + railW, Y(TOP) - rung * 0.6); c.lineTo(lx + railW, Y(0));
    c.stroke();
    c.lineWidth = 1.6; c.strokeStyle = C.steel;
    for (var i = 0; i <= TOP; i++) {
      c.beginPath(); c.moveTo(lx, Y(i)); c.lineTo(lx + railW, Y(i)); c.stroke();
      this.label(String(i), lx - 12, Y(i), 15, C.steel, 'right', '400');
    }
    c.strokeStyle = C.ink; c.lineWidth = 3;       // обрыв под нижней ступенькой
    c.beginPath();
    c.moveTo(lx - 22, Y(-1) + 4); c.lineTo(lx + railW + 22, Y(-1) + 4);
    c.stroke();

    /* точка на лестнице */
    var hNow = this.h[Math.min(this.shown, this.h.length - 1)];
    var fell = hNow < 0;
    c.fillStyle = fell ? C.brick : C.ink;
    c.beginPath();
    c.arc(lx + railW / 2, Y(Math.max(hNow, -1)), 9, 0, 7);
    c.fill();

    if (!graph) {
      this.label(fell ? 'сорвался' : '', lx + railW / 2, Y(-1) + 34, 17, C.brick);
      return;
    }

    /* фаза 2: ось времени вправо и график того же движения */
    var gx = lx + railW + 46;
    /* шаг по x — по фактической длине прогона, а не по максимальной: прогон
       обрывается падением, и раскладка на STEPS оставляла две трети доски пустыми */
    var dx = (W - gx - 40) / Math.max(8, this.w.length);
    c.strokeStyle = C.rule; c.lineWidth = 1.4;
    c.setLineDash([5, 4]);
    c.beginPath(); c.moveTo(gx, Y(0)); c.lineTo(gx + STEPS * dx, Y(0)); c.stroke();
    c.setLineDash([]);
    c.strokeStyle = C.ink; c.lineWidth = 3;
    c.beginPath();
    c.moveTo(gx, Y(-1) + 4); c.lineTo(gx + STEPS * dx, Y(-1) + 4);
    c.stroke();

    var n = Math.min(this.shown, this.w.length);
    c.strokeStyle = C.brick; c.lineWidth = 2.8;
    c.lineJoin = 'round'; c.lineCap = 'round';
    c.beginPath();
    c.moveTo(gx, Y(START));
    for (var j = 1; j <= n; j++) c.lineTo(gx + j * dx, Y(this.h[j]));
    c.stroke();
    for (var j2 = 0; j2 <= n; j2++) {
      c.fillStyle = C.card; c.strokeStyle = C.ink; c.lineWidth = 1.5;
      c.beginPath(); c.arc(gx + j2 * dx, Y(this.h[j2]), 4, 0, 7); c.fill(); c.stroke();
    }
    /* буквы О и Р ПОД звеньями (РАЗБОР §16.9: читать удобнее снизу) */
    for (var j3 = 0; j3 < n; j3++) {
      this.label(this.w[j3] > 0 ? 'О' : 'Р',
                 gx + (j3 + 0.5) * dx, Y(-1) + 22, 16, C.steel);
    }
  };

  window.LabKinds.ladder = function (cv) {
    var l = new Ladder(cv);
    l.row([{ glyph: '↺', title: 'ещё один прогон',
             act: function () { l.stop(); l.reset(); l.shown = 0; l.play(); } }]);
    return l;
  };
})();
