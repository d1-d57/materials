
/* === S7 · сумма квадратов строки — КАНВАС ВМЕСТО СЛАЙДА =====================
   РАЗБОР §7 и §16.6: «самое классное» решение. Текста на слайде нет вообще —
   голубой фон и большой треугольник во всю ширину.

   Щёлкаешь по строке верхней половины (она отчерчена лёгким пунктиром) — под
   треугольником выписываются квадраты её чисел, показывается сумма, и в строке
   с удвоенным номером высвечивается клетка, где стоит ровно это число.
   Щёлкать можно по любой строке верхней половины: 1+6²+15²+20²+15²+6²+1 = 924,
   и 924 стоит в середине двенадцатой строки — это же вопрос 6 бота.

   Треугольник до 12-й строки: вопрос бота про ШЕСТУЮ строку, а её ответ живёт
   в двенадцатой. На десяти строках (как в §16.6) ответ было бы негде показать.
   ============================================================================ */
(function () {
  var LC = window.LabCore;
  var ROWS = 12;                     // строки 0…12
  var HALF = 6;                      // щёлкается верхняя половина: строки 0…6

  var TRI = [];
  for (var n = 0; n <= ROWS; n++) {
    TRI[n] = [];
    for (var k = 0; k <= n; k++)
      TRI[n][k] = (k === 0 || k === n) ? 1 : TRI[n - 1][k - 1] + TRI[n - 1][k];
  }

  function Squares(cv, slide) {
    LC.Lab.call(this, cv, {});
    this.pick = null;
    this.hover = null;
    var self = this;
    cv.style.cursor = 'pointer';
    function rowAt(e) {
      var r = cv.getBoundingClientRect();
      var y = (e.clientY - r.top) * self.H / r.height;
      var n = Math.round((y - self.oy) / self.dy);
      return (n >= 0 && n <= HALF) ? n : null;
    }
    cv.addEventListener('pointermove', function (e) {
      var n = rowAt(e);
      if (n !== self.hover) { self.hover = n; self.draw(); }
    });
    cv.addEventListener('pointerleave', function () {
      if (self.hover !== null) { self.hover = null; self.draw(); }
    });
    cv.addEventListener('click', function (e) {
      var n = rowAt(e);
      if (n !== null) { self.pick = (self.pick === n ? null : n); self.showAnswer = true; self.draw(); }
    });
  }
  Squares.prototype = Object.create(LC.Lab.prototype);

  /* сцены ведут лектора без мыши: 1 — чистый треугольник, 2 — строка 6,
     3 — она же с подсветкой середины двенадцатой (ответ вопроса 6) */
  Squares.prototype.onScene = function (k) {
    /* Три РАЗНЫХ кадра, а не два одинаковых: сцена 2 выписывает квадраты строки,
       и только сцена 3 высвечивает клетку-ответ в строке 2n. Раньше 2 и 3 рисовали
       одно и то же — щелчок кликера ничего не менял (поймано audit.py --scene-diff:
       «scene 3 not empty — empty click»). Пустой щелчок на лекции читается как
       сломанный кликер. */
    this.scene = k;
    this.pick = (k <= 1) ? null : 6;
    this.showAnswer = (k >= 3);
    this.draw();
  };
  Squares.prototype.settle = function () { this.pick = null; this.showAnswer = false; this.draw(); };

  Squares.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();

    var bottom = 108;                                   // полоса под выкладку
    var dy = Math.min(46, (H - bottom - 56) / (ROWS + 1));
    var dxCell = Math.min(74, (W - 90) / (ROWS + 1));
    this.dy = dy;
    this.oy = 40;
    var X = function (n, k) { return W / 2 + (k - n / 2) * dxCell; };
    var Y = function (n) { return 40 + n * dy; };
    var size = Math.max(11, Math.min(19, dxCell * 0.30));

    /* пунктир под верхней половиной — «вот докуда щёлкается» */
    c.strokeStyle = C.steel; c.lineWidth = 1.2;
    c.setLineDash([4, 5]);
    c.beginPath();
    c.moveTo(48, Y(HALF) + dy * 0.55); c.lineTo(W - 48, Y(HALF) + dy * 0.55);
    c.stroke();
    c.setLineDash([]);

    var pick = this.pick;
    var band = (this.hover !== null && this.hover !== pick) ? this.hover : null;

    for (var n = 0; n <= ROWS; n++) {
      for (var k = 0; k <= n; k++) {
        var isPicked = (pick !== null && n === pick);
        var isAnswer = (this.showAnswer && pick !== null && n === 2 * pick && k === pick);
        var col = C.ink, weight = '400';
        if (isPicked) { col = C.brick; weight = '700'; }
        if (band !== null && n === band) col = C.steel;
        if (isAnswer) {
          c.fillStyle = C.brick;
          c.beginPath(); c.arc(X(n, k), Y(n), size * 1.45, 0, 7); c.fill();
          col = C.card; weight = '700';
        }
        this.label(String(TRI[n][k]), X(n, k), Y(n), size, col, 'center', weight);
      }
    }

    if (pick !== null) {
      /* выкладка: квадраты чисел строки, их сумма, и куда она встала */
      var parts = TRI[pick].map(function (v) { return v * v; });
      var sum = parts.reduce(function (a, b) { return a + b; }, 0);
      var line = parts.join(' + ') + ' = ' + sum;
      c.save();
      c.fillStyle = C.blush;
      c.fillRect(0, H - bottom, W, bottom);
      c.restore();
      /* сумма печатается ОДИН раз — в конце выкладки; отдельная крупная подпись
         снизу дублировала то же число и читалась как второй, другой результат */
      this.label(line, W / 2, H - bottom / 2,
                 Math.min(34, W / (line.length * 0.60)), C.ink);
    }
  };

  window.LabKinds.squares = function (cv, slide) { return new Squares(cv, slide); };
})();
