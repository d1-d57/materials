/* ============================================================
   fib-strip — единый интерактив курса «Числа Фибоначчи».
   ОДИН механизм (§4 захода), переиспользованный на всех биекциях.
   Полоска квадратов(=1)/доминошек(=2) редактируется кликом; образ
   под соответствием обновляется живьём. Режим — data-mode:
     recur | code | subset | perm | sum | firstsq | cassini

   ── Двузонный canvas (стандарт §3 захода; ДНК — референс стр. 8–9) ──
   ВЕРХ-band: полоска-объект A_n (редактируется кликом).
   НИЗ-band : её образ X_n, ВЫРОВНЕННЫЙ по тем же колонкам (код-цифра
              строго под своей плиткой, лунка — под левым краем доминошки).
   Обе стороны редактируемы (data-editimg="1") — клик по образу правит
   ту же полоску. Ограничение — во ВВОДЕ: соседние лунки к занятой гаснут
   (нельзя два подряд); «0» всегда тянет «1» (нет «00»).
   Слайд = КОНФИГ над примитивами (mode/n/editimg), не новый код.

   Оркестрация — идемпотентный pump по интервалу (canvas живёт в скрытом
   слайде display:none → инициализируем/рисуем при появлении).
   ============================================================ */
(function () {
  "use strict";
  function tok(name, fb) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fb;
  }
  var COL = {
    sq: tok('--cgreen', '#7ea474'), dom: tok('--mustard', '#c9a23c'),
    ink: tok('--ink', '#333333'), card: tok('--card', '#ffffff'),
    brick: tok('--brick', '#bf5b4f'), steel: tok('--steel', '#8195ad'),
    board: tok('--board', '#a7c2cb'), rule: tok('--rule', '#c3cedd')
  };
  function randParts(n) { var p = [], s = 0; while (s < n) { var two = (n - s >= 2) && Math.random() < 0.5; p.push(two ? 2 : 1); s += two ? 2 : 1; } return p; }
  function code(parts) { return parts.map(function (x) { return x === 1 ? '1' : '01'; }).join(''); }
  function subset(parts) { var pos = 1, s = []; parts.forEach(function (x) { if (x === 2) s.push(pos); pos += x; }); return s; }
  function perm(parts) { var pi = [], i = 1; parts.forEach(function (x) { if (x === 1) { pi.push(i); i++; } else { pi.push(i + 1); pi.push(i); i += 2; } }); return pi; }
  var SUBS = { '0': '₀','1': '₁','2': '₂','3': '₃','4': '₄','5': '₅','6': '₆','7': '₇','8': '₈','9': '₉' };
  function sub(x) { return String(x).replace(/[0-9]/g, function (d) { return SUBS[d]; }); }
  function plural(n, one, few, many) { var t = n % 10, h = n % 100; return (t === 1 && h !== 11) ? one : (t >= 2 && t <= 4 && (h < 12 || h > 14)) ? few : many; }

  /* ── примитив: модель-уровневая правка полоски по НОМЕРУ клетки (1-based) ──
     клетка в доминошке → расщепить на два квадрата; клетка-квадрат →
     слить с правым соседом-квадратом (левый край здесь = доминошка (p,p+1)),
     иначе с левым. Возвращает true, если полоска изменилась. */
  function partAtCell(parts, cellPos) {
    var pos = 1;
    for (var idx = 0; idx < parts.length; idx++) {
      var w = parts[idx];
      if (cellPos >= pos && cellPos < pos + w) return { idx: idx, left: pos };
      pos += w;
    }
    return null;
  }
  function toggleCell(parts, cellPos, preferRight) {
    var info = partAtCell(parts, cellPos); if (!info) return false;
    var idx = info.idx;
    if (parts[idx] === 2) { parts.splice(idx, 1, 1, 1); return true; }   // доминошка → 2 квадрата
    if (preferRight) { if (parts[idx + 1] === 1) { parts.splice(idx, 2, 2); return true; }
                       if (parts[idx - 1] === 1) { parts.splice(idx - 1, 2, 2); return true; } }
    else            { if (parts[idx - 1] === 1) { parts.splice(idx - 1, 2, 2); return true; }
                       if (parts[idx + 1] === 1) { parts.splice(idx, 2, 2); return true; } }
    return false;
  }

  function makeStrip(canvas) {
    var mode = canvas.dataset.mode || 'code';
    var n = parseInt(canvas.dataset.n || '8', 10);
    var editImg = canvas.dataset.editimg === '1';
    var st = { parts: randParts(n), n: n, mode: mode, pairB: randParts(n), sel: [], _L: null, _hit: [], _flash: 0, _lastPair: -1 };
    var ctx = canvas.getContext('2d');
    var cssW = 0, cssH = 0;
    var STRIP_CY = 0.30, IMG_CY = 0.70;   // центры двух band'ов (доля высоты)

    function syncSize() {
      var w = canvas.clientWidth, h = canvas.clientHeight;
      if (!w || !h) return false;
      var dpr = Math.max(1, window.devicePixelRatio || 1);
      var nw = Math.round(w * dpr), nh = Math.round(h * dpr);
      if (canvas.width === nw && canvas.height === nh && cssW === w) return false;
      canvas.width = nw; canvas.height = nh;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cssW = w; cssH = h;
      return true;
    }
    function layout(parts, cy) {
      var cells = parts.reduce(function (a, x) { return a + x; }, 0);
      var u = Math.min((cssW * 0.86) / cells, cssH * 0.26);
      return { u: u, x0: (cssW - u * cells) / 2, y: cy - u / 2, side: u };
    }
    function cellCenterX(L, p) { return L.x0 + L.u * (p - 0.5); }   // центр клетки p (1-based)
    function boundaryX(L, i) { return L.x0 + L.u * i; }             // граница между клетками i и i+1

    function drawStrip(parts, cy, opts) {
      opts = opts || {};
      var L = layout(parts, cy), x = L.x0;
      ctx.lineWidth = Math.max(2, L.u * 0.05); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      parts.forEach(function (p, idx) {
        var w = p * L.u, hi = opts.hi != null && opts.hi === idx;
        ctx.fillStyle = hi ? COL.brick : (p === 1 ? COL.sq : COL.dom);
        ctx.strokeStyle = COL.ink; ctx.fillRect(x, L.y, w, L.side); ctx.strokeRect(x, L.y, w, L.side);
        x += w;
      });
      return L;
    }
    function toggleAt(parts, cellX, L) {   // клик по ВЕРХ-полоске: клетка из пикселя
      var acc = L.x0;
      for (var i = 0; i < parts.length; i++) {
        var w = parts[i] * L.u;
        if (cellX >= acc && cellX < acc + w) {
          if (parts[i] === 2) { parts.splice(i, 1, 1, 1); return true; }
          if (parts[i + 1] === 1) { parts.splice(i, 2, 2); return true; }
          if (parts[i - 1] === 1) { parts.splice(i - 1, 2, 2); return true; }
          return false;
        }
        acc += w;
      }
      return false;
    }
    function firstHi() {
      if (st.mode === 'recur') return 0;
      if (st.mode === 'sum') { for (var i = 0; i < st.parts.length; i++) if (st.parts[i] === 2) return i; }
      if (st.mode === 'firstsq') { for (var j = 0; j < st.parts.length; j++) if (st.parts[j] === 1) return j; }
      return null;
    }
    function arc(x1, x2, y, u) { ctx.beginPath(); ctx.moveTo(x1, y); ctx.quadraticCurveTo((x1 + x2) / 2, y - u * 0.9, x2, y); ctx.stroke(); }

    /* ── ОБРАЗ (низ), выровненный по колонкам полоски st._L. Собирает st._hit
         для редактируемых режимов (subset/code). ── */
    function drawImage() {
      var L = st._L, by = cssH * IMG_CY; st._hit = [];
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';

      if (st.mode === 'code') {
        var pos = 1, r = Math.min(L.u * 0.5, cssH * 0.14);
        ctx.font = "bold " + Math.round(r) + "px 'Glacial Indifference',monospace";
        st.parts.forEach(function (p) {
          if (p === 1) { ctx.fillStyle = COL.ink; ctx.fillText('1', cellCenterX(L, pos), by);
                         st._hit.push({ x: cellCenterX(L, pos), y: by, r: L.u * 0.5, cell: pos, active: true }); pos += 1; }
          else { ctx.fillStyle = COL.dom; ctx.fillText('0', cellCenterX(L, pos), by);
                 ctx.fillStyle = COL.ink; ctx.fillText('1', cellCenterX(L, pos + 1), by);
                 st._hit.push({ x: cellCenterX(L, pos + 0.5), y: by, r: L.u, cell: pos, active: true }); pos += 2; }
        });
      } else if (st.mode === 'subset') {
        var s = subset(st.parts), inS = {}; s.forEach(function (i) { inS[i] = 1; });
        var rr = Math.min(L.u * 0.34, cssH * 0.12);
        ctx.font = Math.round(rr * 1.15) + "px 'Glacial Indifference',sans-serif";
        for (var k = 1; k <= st.n - 1; k++) {
          var cx = boundaryX(L, k), filled = !!inS[k];
          var placeable = !inS[k] && !inS[k - 1] && !inS[k + 1];
          var disabled = !filled && !placeable;
          if (filled) {   // связка пары: доминошка (верх) ↔ её лунка (низ)
            ctx.strokeStyle = COL.rule; ctx.lineWidth = k === st._lastPair ? 3 : 1.5;
            ctx.beginPath(); ctx.moveTo(cx, cssH * STRIP_CY + L.side * 0.5); ctx.lineTo(cx, by - rr); ctx.stroke();
          }
          ctx.beginPath(); ctx.arc(cx, by, rr, 0, 7);
          ctx.fillStyle = filled ? COL.brick : COL.card; ctx.globalAlpha = disabled ? 0.28 : 1; ctx.fill();
          ctx.lineWidth = 2; ctx.strokeStyle = COL.ink; ctx.stroke(); ctx.globalAlpha = 1;
          ctx.fillStyle = filled ? COL.card : (disabled ? COL.steel : COL.ink); ctx.fillText(String(k), cx, by);
          st._hit.push({ x: cx, y: by, r: rr * 1.25, cell: k, active: !disabled, filled: filled });
        }
      } else if (st.mode === 'perm') {
        var pi = perm(st.parts);
        ctx.lineWidth = Math.max(2, L.u * 0.06); ctx.strokeStyle = COL.steel;
        for (var i2 = 0; i2 < pi.length; i2++) if (pi[i2] === i2 + 2) arc(cellCenterX(L, i2 + 1), cellCenterX(L, i2 + 2), by, L.u);
        for (var k2 = 1; k2 <= st.n; k2++) { ctx.beginPath(); ctx.arc(cellCenterX(L, k2), by, Math.max(3, L.u * 0.12), 0, 7);
          ctx.fillStyle = pi[k2 - 1] === k2 ? COL.sq : COL.dom; ctx.fill(); }
      } else if (st.mode === 'recur') {
        var f0 = st.parts[0];   // «первая плитка → остаток A_{n−first}»
        var restStart = cellCenterX(L, f0 === 1 ? 1.5 : 2), restEnd = L.x0 + L.u * st.n;
        ctx.strokeStyle = COL.brick; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(cellCenterX(L, f0 === 1 ? 1 : 1.5), cssH * STRIP_CY + L.side * 0.6);
        ctx.lineTo((restStart + restEnd) / 2, by - L.u * 0.5); ctx.stroke();
        ctx.fillStyle = COL.ink; ctx.font = Math.round(cssH * 0.085) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText((f0 === 1 ? 'квадрат' : 'доминошка') + ' + A' + sub(st.n - f0), (L.x0 + restEnd) / 2, by);
      } else if (st.mode === 'sum') {
        var kk = firstHi(), pre = 0, lim = kk == null ? st.parts.length : kk, j;
        for (j = 0; j < lim; j++) pre += st.parts[j];
        ctx.fillStyle = COL.ink; ctx.font = Math.round(cssH * 0.082) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(kk == null ? 'сплошь квадраты — особое, это «−1»'
          : pre + ' ' + plural(pre, 'квадрат', 'квадрата', 'квадратов') + ' · доминошка · A' + sub(st.n - pre - 2), cssW / 2, by);
      } else if (st.mode === 'firstsq') {
        var qk = firstHi(), pd = 0, lim2 = qk == null ? st.parts.length : qk, jj;
        for (jj = 0; jj < lim2; jj++) pd += st.parts[jj];   // клеток до первого квадрата (все доминошки → pd = 2·#дом)
        ctx.fillStyle = COL.ink; ctx.font = Math.round(cssH * 0.082) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(qk == null ? 'сплошь доминошки — особое (только при чётном n)'
          : (pd / 2) + ' ' + plural(pd / 2, 'доминошка', 'доминошки', 'доминошек') + ' · квадрат · A' + sub(st.n - pd - 1), cssW / 2, by);
      }
    }

    /* ── Цекендорф (задача 5): кирпичи-числа Фибоначчи, выбор НЕСОСЕДНИХ (тот же
         запрет-во-вводе, что у эталона B_n) → сумма = число. ── */
    function drawZeck() {
      var fibs = [1, 2, 3, 5, 8, 13, 21], m = fibs.length;
      var bw = Math.min(cssW * 0.108, cssH * 0.30), gap = bw * 0.30;
      var x0 = (cssW - (m * bw + (m - 1) * gap)) / 2, by = cssH * 0.52, bh = bw;
      var isSel = {}; st.sel.forEach(function (i) { isSel[i] = 1; });
      st._hit = [];
      var sum = st.sel.reduce(function (a, i) { return a + fibs[i]; }, 0);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillStyle = COL.brick; ctx.font = "bold " + Math.round(cssH * 0.16) + "px 'Glacial Indifference',sans-serif";
      ctx.fillText(sum > 0 ? String(sum) : '?', cssW / 2, cssH * 0.19);
      for (var i = 0; i < m; i++) {
        var x = x0 + i * (bw + gap), selected = !!isSel[i];
        var disabled = !selected && (isSel[i - 1] || isSel[i + 1]);
        ctx.globalAlpha = disabled ? 0.3 : 1;
        ctx.fillStyle = selected ? COL.sq : COL.card; ctx.strokeStyle = COL.ink; ctx.lineWidth = 2.5;
        ctx.fillRect(x, by, bw, bh); ctx.strokeRect(x, by, bw, bh);
        ctx.fillStyle = selected ? COL.card : (disabled ? COL.steel : COL.ink);
        ctx.font = Math.round(bw * 0.4) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(String(fibs[i]), x + bw / 2, by + bh / 2);
        ctx.globalAlpha = 1;
        st._hit.push({ x: x + bw / 2, y: by + bh / 2, r: bw / 2, idx: i, active: !disabled });
      }
    }
    function toggleZeck(px, py) {
      for (var i = 0; i < st._hit.length; i++) {
        var h = st._hit[i];
        if (Math.abs(px - h.x) <= h.r && Math.abs(py - h.y) <= h.r) {
          if (h.active === false) { st._flash = { x: h.x, y: h.y, r: h.r, a: 1 }; flashAnim(); return 'blocked'; }
          var p = st.sel.indexOf(h.idx);
          if (p >= 0) st.sel.splice(p, 1); else st.sel.push(h.idx);
          return true;
        }
      }
      return false;
    }

    function drawCassini() {
      drawStrip(st.parts, cssH * 0.3, {});
      drawStrip(st.pairB, cssH * 0.62, {});
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = COL.brick;
      ctx.font = Math.round(cssH * 0.07) + "px 'Glacial Indifference',sans-serif";
      ctx.fillText('пара лент · клик — переклеить хвосты', cssW / 2, cssH * 0.9);
    }
    function drawHint() {
      ctx.save(); ctx.globalAlpha = 0.32; ctx.fillStyle = COL.ink;
      ctx.textAlign = 'right'; ctx.textBaseline = 'bottom'; ctx.font = "15px ui-monospace,monospace";
      ctx.fillText(editImg ? 'клик по ленте или образу ⟳' : 'клик по клетке ⟳', cssW - 14, cssH - 10); ctx.restore();
    }
    function drawFlash() {   // фидбек «нельзя»: красное кольцо на запрещённой лунке, гаснет
      if (!st._flash) return;
      var a = st._flash.a; if (a <= 0) { st._flash = 0; return; }
      ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = COL.brick; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(st._flash.x, st._flash.y, st._flash.r, 0, 7); ctx.stroke(); ctx.restore();
    }
    function draw() {
      if (!cssW) return;
      ctx.clearRect(0, 0, cssW, cssH);
      if (st.mode === 'cassini') { drawCassini(); return; }
      if (st.mode === 'zeck') { drawZeck(); drawFlash(); drawHint(); return; }
      st._L = drawStrip(st.parts, cssH * STRIP_CY, { hi: (st.mode === 'recur' || st.mode === 'sum' || st.mode === 'firstsq') ? firstHi() : null });
      drawImage();
      drawFlash();
      drawHint();
    }

    function toggleImage(px, py) {   // клик по НИЗ-образу (редактируемые режимы)
      for (var i = 0; i < st._hit.length; i++) {
        var h = st._hit[i];
        if (Math.abs(px - h.x) <= h.r && Math.abs(py - h.y) <= (st._L.side * 0.9)) {
          if (h.active === false) {                    // запрещено (ограничение-во-вводе) → фидбек
            st._flash = { x: h.x, y: h.y, r: (h.r || 20), a: 1 }; flashAnim(); return 'blocked';
          }
          st._lastPair = h.cell;
          toggleCell(st.parts, h.cell, true);           // правый приоритет = семантика левого края
          return true;
        }
      }
      return false;
    }
    function flashAnim() {   // короткая микроанимация кольца (~320мс), self-contained rAF
      var t0 = performance.now();
      (function step(t) {
        var k = 1 - (t - t0) / 320;
        if (k <= 0 || !st._flash) { st._flash = 0; draw(); return; }
        st._flash.a = k; draw(); requestAnimationFrame(step);
      })(t0);
    }

    canvas.addEventListener('click', function (e) {
      syncSize();
      var r = canvas.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width * cssW;
      var y = (e.clientY - r.top) / r.height * cssH;
      if (st.mode === 'cassini') { st.parts = randParts(st.n); st.pairB = randParts(st.n); draw(); return; }
      if (st.mode === 'zeck') { if (toggleZeck(x, y) === true) draw(); return; }
      if (editImg && y > cssH * 0.5) { var res = toggleImage(x, y); if (res === true) draw(); return; }
      if (st._L && toggleAt(st.parts, x, st._L)) { st._lastPair = -1; draw(); }
    });
    return { syncAndDraw: function () { if (syncSize()) draw(); else if (cssW && !st._drawn) { st._drawn = 1; draw(); } } };
  }

  function pump() {
    document.querySelectorAll('canvas[data-sim="fib-strip"]').forEach(function (c) {
      try { if (!c.__fib) c.__fib = makeStrip(c); c.__fib.syncAndDraw(); }
      catch (e) { if (window.console) console.error('fib-strip:', e && e.message, e); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pump); else pump();
  window.addEventListener('load', pump);
  window.addEventListener('resize', pump);
  setInterval(pump, 250);
})();
