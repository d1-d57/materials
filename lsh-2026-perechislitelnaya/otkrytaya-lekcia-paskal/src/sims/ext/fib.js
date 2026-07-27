
/* === S8B · биекция Фибоначчи на конкретном числе =============================
   РАЗБОР §16.5, чего не хватало в проекте fibonacci/: канвас с примерами.
     слева  — выписаны ВСЕ 8 хороших слов длины 4;
     справа — 5 слов длины 3 и 3 слова длины 2 отдельными группами;
     между ними стрелки соответствия.
   🔴 Сначала выписываются ВСЕ, и только потом расставляются стрелки, причём
   слова слева ПЕРЕМЕШАНЫ — чтобы биекция не читалась сразу, а проступала.

   Порядок перемешивания зашит константой, а не случаен: слайд обязан выглядеть
   одинаково на каждом прогоне, иначе лектор не знает, что покажет проектор.
   ============================================================================ */
(function () {
  var LC = window.LabCore;

  /* все хорошие слова (без двух О подряд) длины n */
  function good(n) {
    var out = [];
    for (var m = 0; m < (1 << n); m++) {
      var s = '';
      for (var i = 0; i < n; i++) s += (m >> i) & 1 ? 'О' : 'Р';
      if (s.indexOf('ОО') < 0) out.push(s);
    }
    return out;
  }

  var L4 = good(4), L3 = good(3), L2 = good(2);
  /* перемешано ФИКСИРОВАННО: соответствие не должно читаться по порядку строк */
  var SHUF = [3, 7, 0, 5, 2, 6, 1, 4];
  var LEFT = SHUF.map(function (i) { return L4[i]; });

  function Fib(cv) { LC.Lab.call(this, cv, {}); }
  Fib.prototype = Object.create(LC.Lab.prototype);
  Fib.prototype.onScene = function (k) { this.scene = k; this.draw(); };
  Fib.prototype.settle = function () { this.draw(); };

  Fib.prototype.draw = function () {
    if (!this.measure()) return;
    var c = this.ctx, C = this.C, W = this.W, H = this.H;
    this.clear();
    var k = this.scene || 1;

    var padY = 30;
    var dy = (H - 2 * padY) / 8;
    var size = Math.max(14, Math.min(24, dy * 0.52));
    var lx = W * 0.20, rx = W * 0.74;
    var Yl = function (i) { return padY + (i + 0.5) * dy; };

    /* левая колонка — все восемь слов длины 4 */
    for (var i = 0; i < LEFT.length; i++) {
      var w = LEFT[i];
      var endsP = w.charAt(3) === 'Р';
      var lit = (k >= 2 && endsP) || (k >= 3 && !endsP);
      this.label(w, lx, Yl(i), size, lit ? C.ink : C.steel, 'center',
                 lit ? '700' : '400');
    }

    /* правые группы: 5 слов длины 3 сверху, 3 слова длины 2 снизу */
    var gap = dy * 0.55;
    var Yr3 = function (i) { return padY + (i + 0.5) * dy; };
    var Yr2 = function (i) { return padY + 5 * dy + gap + (i + 0.5) * dy; };
    for (var a = 0; a < L3.length; a++)
      this.label(L3[a], rx, Yr3(a), size, k >= 2 ? C.ink : C.steel, 'center',
                 k >= 2 ? '700' : '400');
    for (var b = 0; b < L2.length; b++)
      this.label(L2[b], rx, Yr2(b), size, k >= 3 ? C.ink : C.steel, 'center',
                 k >= 3 ? '700' : '400');

    /* рамки групп и их размеры */
    if (k >= 2) {
      c.strokeStyle = C.steel; c.lineWidth = 1.4;
      c.strokeRect(rx - size * 2.6, padY + 4, size * 5.2, 5 * dy - 8);
      this.label('5', rx + size * 3.4, padY + 5 * dy / 2, size * 1.2, C.brick, 'left');
    }
    if (k >= 3) {
      c.strokeStyle = C.steel; c.lineWidth = 1.4;
      c.strokeRect(rx - size * 2.6, padY + 5 * dy + gap + 4, size * 5.2, 3 * dy - 8);
      this.label('3', rx + size * 3.4, padY + 5 * dy + gap + 3 * dy / 2,
                 size * 1.2, C.brick, 'left');
    }

    /* стрелки соответствия: слово на Р → его начало длины 3; слово на О → длины 2 */
    if (k >= 4) {
      for (var j = 0; j < LEFT.length; j++) {
        var wd = LEFT[j], endsP2 = wd.charAt(3) === 'Р';
        var pre = endsP2 ? wd.slice(0, 3) : wd.slice(0, 2);
        var idx = (endsP2 ? L3 : L2).indexOf(pre);
        if (idx < 0) continue;
        var y1 = Yl(j), y2 = endsP2 ? Yr3(idx) : Yr2(idx);
        var x1 = lx + size * 2.4, x2 = rx - size * 2.9;
        c.strokeStyle = endsP2 ? C.steel : C.mustard;
        c.lineWidth = 1.6;
        c.beginPath();
        c.moveTo(x1, y1);
        c.bezierCurveTo((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, x2, y2);
        c.stroke();
        c.fillStyle = c.strokeStyle;               // ЗАЛИТЫЙ наконечник
        c.beginPath();
        c.moveTo(x2 + 8, y2); c.lineTo(x2 - 1, y2 - 4.5); c.lineTo(x2 - 1, y2 + 4.5);
        c.closePath(); c.fill();
      }
    }
    if (k >= 5) this.label('5 + 3 = 8', W / 2, H - 16, size * 1.3, C.brick);
  };

  window.LabKinds.fib = function (cv) { return new Fib(cv); };
})();
