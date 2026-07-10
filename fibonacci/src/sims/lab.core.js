/* ============================================================
   fib-strip — единый интерактив курса «Числа Фибоначчи».
   ОДИН механизм (§4 захода), переиспользованный на всех биекциях.
   Полоска квадратов(=1)/доминошек(=2) редактируется кликом; образ
   под соответствием обновляется живьём. Режим — data-mode:
     recur | code | subset | perm | sum | cassini
   Холст делится на две зоны: сверху — полоска (редактируется),
   снизу — её образ. Оркестрация — идемпотентный pump по интервалу
   (canvas живёт в скрытом слайде display:none → инициализируем/рисуем
   при появлении, не завися от таймингов DOMContentLoaded).
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
    brick: tok('--brick', '#bf5b4f'), steel: tok('--steel', '#8195ad'), board: tok('--board', '#a7c2cb')
  };
  function randParts(n) { var p = [], s = 0; while (s < n) { var two = (n - s >= 2) && Math.random() < 0.5; p.push(two ? 2 : 1); s += two ? 2 : 1; } return p; }
  function code(parts) { return parts.map(function (x) { return x === 1 ? '1' : '01'; }).join(''); }
  function subset(parts) { var pos = 1, s = []; parts.forEach(function (x) { if (x === 2) s.push(pos); pos += x; }); return s; }
  function perm(parts) { var pi = [], i = 1; parts.forEach(function (x) { if (x === 1) { pi.push(i); i++; } else { pi.push(i + 1); pi.push(i); i += 2; } }); return pi; }
  var SUBS = { '0': '₀','1': '₁','2': '₂','3': '₃','4': '₄','5': '₅','6': '₆','7': '₇','8': '₈','9': '₉' };
  function sub(x) { return String(x).replace(/[0-9]/g, function (d) { return SUBS[d]; }); }

  function makeStrip(canvas) {
    var mode = canvas.dataset.mode || 'code';
    var n = parseInt(canvas.dataset.n || '8', 10);
    var st = { parts: randParts(n), n: n, mode: mode, pairB: randParts(n), _L: null };
    var ctx = canvas.getContext('2d');
    var cssW = 0, cssH = 0;

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
    function drawStrip(parts, cy, opts) {
      opts = opts || {};
      var L = layout(parts, cy), x = L.x0;
      ctx.lineWidth = Math.max(2, L.u * 0.05); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.font = Math.round(L.u * 0.34) + "px 'Glacial Indifference','Noto Sans',sans-serif";
      parts.forEach(function (p, idx) {
        var w = p * L.u, hi = opts.hi != null && opts.hi === idx;
        ctx.fillStyle = hi ? COL.brick : (p === 1 ? COL.sq : COL.dom);
        ctx.strokeStyle = COL.ink; ctx.fillRect(x, L.y, w, L.side); ctx.strokeRect(x, L.y, w, L.side);
        if (opts.labels) { ctx.fillStyle = COL.ink; ctx.fillText(p === 1 ? '1' : '0 1', x + w / 2, L.y + L.side + L.u * 0.44); }
        x += w;
      });
      return L;
    }
    function toggleAt(parts, cellX, L) {
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
      return null;
    }
    function arc(x1, x2, y, u) { ctx.beginPath(); ctx.moveTo(x1, y); ctx.quadraticCurveTo((x1 + x2) / 2, y - u * 0.9, x2, y); ctx.stroke(); }
    function drawImage() {
      var by = cssH * 0.68;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = COL.ink;
      if (st.mode === 'code') {
        ctx.font = "bold " + Math.round(cssH * 0.12) + "px 'Glacial Indifference',monospace";
        ctx.fillText(code(st.parts).split('').join(' '), cssW / 2, by);
      } else if (st.mode === 'subset') {
        var s = subset(st.parts), u = Math.min((cssW * 0.8) / st.n, cssH * 0.17), x0 = (cssW - u * (st.n - 1)) / 2;
        ctx.font = Math.round(u * 0.5) + "px 'Glacial Indifference',sans-serif";
        for (var k = 1; k <= st.n - 1; k++) {
          var cx = x0 + u * (k - 1), inS = s.indexOf(k) >= 0;
          ctx.beginPath(); ctx.arc(cx, by, u * 0.36, 0, 7); ctx.fillStyle = inS ? COL.brick : COL.card; ctx.fill();
          ctx.lineWidth = 2; ctx.strokeStyle = COL.ink; ctx.stroke();
          ctx.fillStyle = inS ? COL.card : COL.ink; ctx.fillText(String(k), cx, by);
        }
      } else if (st.mode === 'perm') {
        var pi = perm(st.parts), u = Math.min((cssW * 0.78) / (st.n - 1 || 1), cssH * 0.2), x0 = (cssW - u * (st.n - 1)) / 2;
        var X = function (k) { return x0 + u * (k - 1); };
        ctx.lineWidth = Math.max(2, u * 0.06); ctx.strokeStyle = COL.steel;
        for (var i = 0; i < pi.length; i++) if (pi[i] === i + 2) arc(X(i + 1), X(i + 2), by, u);
        for (var k2 = 1; k2 <= st.n; k2++) { ctx.beginPath(); ctx.arc(X(k2), by, u * 0.14, 0, 7); ctx.fillStyle = pi[k2 - 1] === k2 ? COL.sq : COL.dom; ctx.fill(); }
      } else if (st.mode === 'recur') {
        ctx.font = Math.round(cssH * 0.1) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText('первая ' + (st.parts[0] === 1 ? 'клетка' : 'доминошка') + '  →  A' + sub(st.n - st.parts[0]), cssW / 2, by);
      } else if (st.mode === 'sum') {
        var kk = firstHi(), pre = 0, lim = kk == null ? st.parts.length : kk;
        for (var j = 0; j < lim; j++) pre += st.parts[j];
        ctx.font = Math.round(cssH * 0.088) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(kk == null ? 'сплошь квадраты — особый, это «−1»' : (pre + ' квадрат(ов), затем доминошка  →  A' + sub(st.n - pre - 2)), cssW / 2, by);
      }
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
      ctx.fillText('клик по клетке ⟳', cssW - 14, cssH - 10); ctx.restore();
    }
    function draw() {
      if (!cssW) return;
      ctx.clearRect(0, 0, cssW, cssH);
      if (st.mode === 'cassini') { drawCassini(); return; }
      st._L = drawStrip(st.parts, cssH * 0.30, { labels: st.mode === 'code', hi: (st.mode === 'recur' || st.mode === 'sum') ? firstHi() : null });
      drawImage();
      drawHint();
    }
    canvas.addEventListener('click', function (e) {
      syncSize();
      var r = canvas.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width * cssW;
      if (st.mode === 'cassini') { st.parts = randParts(st.n); st.pairB = randParts(st.n); draw(); return; }
      if (st._L && toggleAt(st.parts, x, st._L)) draw();
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
