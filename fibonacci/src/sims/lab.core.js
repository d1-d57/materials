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
    board: tok('--board', '#a7c2cb'), rule: tok('--rule', '#c3cedd'),
    blush: tok('--blush', '#f0e2de')
  };
  function randParts(n) { var p = [], s = 0; while (s < n) { var two = (n - s >= 2) && Math.random() < 0.5; p.push(two ? 2 : 1); s += two ? 2 : 1; } return p; }
  function code(parts) { return parts.map(function (x) { return x === 1 ? '1' : '01'; }).join(''); }
  function subset(parts) { var pos = 1, s = []; parts.forEach(function (x) { if (x === 2) s.push(pos); pos += x; }); return s; }
  function perm(parts) { var pi = [], i = 1; parts.forEach(function (x) { if (x === 1) { pi.push(i); i++; } else { pi.push(i + 1); pi.push(i); i += 2; } }); return pi; }
  /* ── карты замощение→объект для D/E/G (= биекция A_n↔X_n по рекурренте; сверено verify_models.py) ── */
  function tilingToD(parts) {       // D: квадрат-первый → часть+1 (D_{n-1}); доминошка → приписать 2 (D_{n-2})
    if (!parts.length) return [2];
    var d = tilingToD(parts.slice(1));
    return parts[0] === 1 ? [d[0] + 1].concat(d.slice(1)) : [2].concat(d);
  }
  function tilingToE(parts) {        // E: приписать квадрат справа, резать после квадратов → нечётные блоки 2j+1
    var out = [], run = 0;
    parts.forEach(function (p) { if (p === 1) { out.push(2 * run + 1); run = 0; } else { run++; } });
    out.push(2 * run + 1); return out;
  }
  function tilingToG(parts, n) {     // G: доминошка→'11'+G_{n-2}; квадрат→'0'+инверсия(G_{n-1})
    if (n <= 1) return [];
    if (parts[0] === 2) { var s = tilingToG(parts.slice(1), n - 2); return (n - 1) >= 2 ? [1, 1].concat(s) : [1]; }
    var s2 = tilingToG(parts.slice(1), n - 1); return [0].concat(s2.map(function (x) { return 1 - x; }));
  }
  var SUBS = { '0': '₀','1': '₁','2': '₂','3': '₃','4': '₄','5': '₅','6': '₆','7': '₇','8': '₈','9': '₉' };
  function sub(x) { return String(x).replace(/[0-9]/g, function (d) { return SUBS[d]; }); }
  function plural(n, one, few, many) { var t = n % 10, h = n % 100; return (t === 1 && h !== 11) ? one : (t >= 2 && t <= 4 && (h < 12 || h > 14)) ? few : many; }

  /* ── перечислители всех Xₙ для сцены «примеры» (счёт обязан = fₙ; сверено verify_models.py) ── */
  function enumTilings(n) {              // все замощения 1×n квадратами(1)/доминошками(2), квадрато-первые впереди
    if (n <= 0) return [[]];
    if (n === 1) return [[1]];
    var out = [];
    enumTilings(n - 1).forEach(function (t) { out.push([1].concat(t)); });
    enumTilings(n - 2).forEach(function (t) { out.push([2].concat(t)); });
    return out;
  }
  var H_NB = { 1: [2], 2: [1, 3], 3: [2, 4], 4: [3] };   // путь P4: соседние цифры отличаются на 1
  function enumWalksH(len) {             // строки длины len над {1..4}, старт 1 (|H_n| при len=n+1 = f_n)
    if (len <= 0) return [];
    var res = [[1]];
    for (var s = 1; s < len; s++) {
      var nx = [];
      res.forEach(function (w) { H_NB[w[w.length - 1]].forEach(function (u) { nx.push(w.concat(u)); }); });
      res = nx;
    }
    return res;
  }
  function enumD(n) {                    // D: упорядоченные разбиения n+2 на части ≥2
    function comps(total, mn) { if (total === 0) return [[]]; var r = []; for (var p = mn; p <= total; p++) comps(total - p, mn).forEach(function (t) { r.push([p].concat(t)); }); return r; }
    return comps(n + 2, 2);
  }
  function enumE(n) {                    // E: упорядоченные разбиения n+1 на нечётные
    function comps(total) { if (total === 0) return [[]]; var r = []; for (var p = 1; p <= total; p += 2) comps(total - p).forEach(function (t) { r.push([p].concat(t)); }); return r; }
    return comps(n + 1);
  }
  function enumG(n) {                    // G: (a1..a_{n-1}) 0/1 с a1≤a2≥a3≤…
    var L = n - 1; if (L <= 0) return [[]];
    var out = [];
    for (var x = 0; x < (1 << L); x++) {
      var s = []; for (var i = 0; i < L; i++) s.push((x >> i) & 1);
      var ok = true; for (var j = 0; j < L - 1; j++) { if (j % 2 === 0) { if (!(s[j] <= s[j + 1])) { ok = false; break; } } else { if (!(s[j] >= s[j + 1])) { ok = false; break; } } }
      if (ok) out.push(s);
    }
    return out;
  }
  function parseRange(str) {             // "1-4" → [1,2,3,4]; "3" → [3]
    var m = /^(\d+)(?:-(\d+))?$/.exec((str || '').trim());
    if (!m) return [1, 2, 3, 4];
    var a = +m[1], b = m[2] ? +m[2] : a, r = [];
    for (var i = a; i <= b; i++) r.push(i);
    return r;
  }
  function randC(n) { return code(randParts(n)); }   // случайная ВАЛИДНАЯ C-строка (не из одних единиц)

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
    /* ── секвенсор сцен: слайд задаёт data-stages="empty examples recur"; индекс = активная сцена.
         Активную сцену читаем из класса .scene-k, который движок (engine.js) ставит на .slide —
         engine.js НЕ трогаем. Нет data-stages ⇒ прежний интерактив (эталон subset не ломается). ── */
    var stages = (canvas.dataset.stages || '').split(/\s+/).filter(Boolean);
    var exRange = parseRange(canvas.dataset.examples || '1-4');
    var slideEl = canvas.closest('.slide');
    st.recurSeq = randC(n);              // рекуррента (строки C): случайная валидная C-строка; клик по символу редактирует
    st.recurSub = subset(randParts(n));  // рекуррента (подмножества B): случайное валидное подмножество {1..n-1} без соседних
    st.recurParts = randParts(n);        // рекуррента (замощения A / перестановки F): случайное замощение (общая база); клик по плитке
    var _hw = enumWalksH(n + 1); st.recurH = _hw[Math.floor(Math.random() * _hw.length)] || [1, 2];  // рекуррента (цифры H): случайный обход длины n+1
    var _d = enumD(n); st.recurD = _d[Math.floor(Math.random() * _d.length)] || [2];    // рекуррента D: случайное разбиение n+2 на части ≥2
    var _e = enumE(n); st.recurE = _e[Math.floor(Math.random() * _e.length)] || [1];    // рекуррента E: случайное разбиение n+1 на нечётные
    var _g = enumG(n); st.recurG = _g[Math.floor(Math.random() * _g.length)] || [];     // рекуррента G: случайный зигзаг длины n−1
    function activeScene() {
      if (!slideEl) return 1;
      for (var k = 9; k >= 1; k--) if (slideEl.classList.contains('scene-' + k)) return k;
      return 1;
    }
    function curStage() {
      if (!stages.length) return null;
      return stages[Math.max(1, Math.min(stages.length, activeScene())) - 1];
    }
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

    function drawObjRow(str) {                       // биекция D/E/G/H: объект, соответствующий полоске (низ band'а), по центру
      var by = cssH * IMG_CY, ch = Math.min(cssH * 0.13, cssW * 0.52 / Math.max(1, str.length));
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = COL.ink;
      ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      ctx.fillText(str, cssW / 2, by);
    }
    function walkForTiling(parts) {                  // A↔H: биекция по индексу (оба множества размера f_n)
      var nn = parts.reduce(function (a, x) { return a + x; }, 0), key = parts.join(','), T = enumTilings(nn), W = enumWalksH(nn + 1);
      for (var i = 0; i < T.length; i++) if (T[i].join(',') === key) return W[i] || [1];
      return W[0] || [1];
    }

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
      } else if (st.mode === 'compGE2') { drawObjRow(tilingToD(st.parts).join('+'));            // D: разбиение под полоской
      } else if (st.mode === 'compOdd') { drawObjRow(tilingToE(st.parts).join('+'));            // E: нечётное разбиение
      } else if (st.mode === 'zigzag') { var _g2 = tilingToG(st.parts, st.n); drawObjRow(_g2.length ? _g2.join('') : '∅');  // G: зигзаг
      } else if (st.mode === 'tiling') { drawStrip(st.parts, by, {});                            // A: тождество — та же полоска ниже
      } else if (st.mode === 'hwalk') { drawObjRow(walkForTiling(st.parts).join(''));            // H: обход по индекс-биекции
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
    /* ══════════ СЦЕНЫ (data-stages): пусто → примеры(в языке модели) → рекуррента(механизм) ══════════
       Правки владельца (wireframe-v1): объекты рисуем в ИХ языке (C = строки 0/1), без доминошек и
       без фиксированных разбиений; примеры — блоками по n (n=0 включён), «n=k» крупно слева, счёт НЕ
       пишем (виден); рекуррента — интерактивный механизм «по первому символу», без подписей. ── */
    function objList(nn) {                        // все объекты модели длины n в РОДНОМ представлении (строки)
      if (st.mode === 'hwalk') return enumWalksH(nn + 1).map(function (w) { return w.join(''); });
      if (st.mode === 'compGE2') return enumD(nn).map(function (c) { return c.join('+'); });     // D: разбиение 2+3
      if (st.mode === 'compOdd') return enumE(nn).map(function (c) { return c.join('+'); });      // E: разбиение 1+1+3
      if (st.mode === 'zigzag') return enumG(nn).map(function (c) { return c.length ? c.join('') : ''; });  // G: строка 010
      var T = enumTilings(nn);
      if (st.mode === 'perm') return T.map(function (t) { return perm(t).join(''); });        // F: однострочная запись π
      if (st.mode === 'subset') return T.map(function (t) { var s = subset(t); return s.length ? '{' + s.join(',') + '}' : '∅'; });  // B: множество
      return T.map(code);                         // C: строки 0/1 (= нативный C_n, сверено verify_models)
    }
    function drawSeq(str, x, cy, ch) {            // строка цифр от левого края x; возвращает ширину
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      if (str === '') { ctx.fillStyle = COL.steel; ctx.fillText('∅', x + ch * 0.35, cy); return ch * 0.7; }
      var g = ch * 0.62;
      for (var i = 0; i < str.length; i++) { ctx.fillStyle = COL.ink; ctx.fillText(str[i], x + g * (i + 0.5), cy); }
      return str.length * g;
    }
    function drawTileRow(parts, x, cy, u) {       // A: мини-полоска квадрат/доминошка от левого края x; возвращает ширину
      if (!parts.length) { ctx.fillStyle = COL.steel; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.font = Math.round(u * 1.1) + "px 'Glacial Indifference',sans-serif"; ctx.fillText('∅', x, cy); return u * 0.7; }
      var xx = x, top = cy - u / 2; ctx.lineWidth = Math.max(1, u * 0.06); ctx.strokeStyle = COL.ink;
      parts.forEach(function (p) { var w = p * u; ctx.fillStyle = p === 1 ? COL.sq : COL.dom; ctx.fillRect(xx, top, w, u); ctx.strokeRect(xx, top, w, u); xx += w; });
      return xx - x;
    }
    function drawExamples() {                      // таблица (реш. владельца): столбец n │ список объектов; минимализм, без линий, без «n=», одна гарнитура
      var ns = [0]; exRange.forEach(function (k) { if (k > 0) ns.push(k); });   // 0,1,2,3,4
      var rows = ns.length, padL = cssW * 0.06, padT = cssH * 0.08, padB = cssH * 0.08;
      var rowH = (cssH - padT - padB) / rows, numRight = padL + cssW * 0.045, objX = padL + cssW * 0.13;
      var tiling = st.mode === 'tiling', availW = cssW - objX - padL;
      var big = tiling ? enumTilings(ns[ns.length - 1]) : objList(ns[ns.length - 1]), maxItems = big.length;
      var maxLen = tiling ? ns[ns.length - 1] : big.reduce(function (a, s) { return Math.max(a, s === '' ? 1 : s.length); }, 1);
      var ch = rowH * 0.5;
      for (var t = Math.min(rowH * 0.6, 72); t >= 14; t -= 2) {   // подгон под самый длинный ряд
        var g = t * 0.62;
        if (maxItems * maxLen * g + (maxItems - 1) * t * 0.95 <= availW) { ch = t; break; }
      }
      ns.forEach(function (nn, ri) {
        var cy = padT + rowH * (ri + 0.5);
        ctx.textAlign = 'right'; ctx.textBaseline = 'middle'; ctx.fillStyle = COL.steel;   // число n — та же гарнитура, приглушённое
        ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(String(nn), numRight, cy);
        var gp = ch * 0.95, x = objX;
        if (tiling) {
          enumTilings(nn).forEach(function (t2) { x += drawTileRow(t2, x, cy, ch * 0.62) + gp; });
        } else {
          var gg = ch * 0.62;
          objList(nn).forEach(function (s) { drawSeq(s, x, cy, ch); x += (s === '' ? ch * 0.7 : s.length * gg) + gp; });
        }
      });
    }
    function braceUnder(x1, x2, y) {               // скобка ПОД отрезком: «остаток — меньшая последовательность»
      var mid = (x1 + x2) / 2; ctx.strokeStyle = COL.steel; ctx.lineWidth = 2.5; ctx.beginPath();
      ctx.moveTo(x1, y); ctx.quadraticCurveTo(x1, y + 8, mid - 8, y + 8);
      ctx.quadraticCurveTo(mid, y + 8, mid, y + 15); ctx.quadraticCurveTo(mid, y + 8, mid + 8, y + 8);
      ctx.quadraticCurveTo(x2, y + 8, x2, y); ctx.stroke();
    }
    function drawRecurMech() {                     // механизм «по первому элементу»; клик редактирует объект, сохраняя валидность
      if (st.mode === 'subset') { drawRecurSubset(); return; }
      if (st.mode === 'tiling') { drawRecurTiling(); return; }
      if (st.mode === 'perm') { drawRecurPerm(); return; }
      if (st.mode === 'hwalk') { drawRecurHwalk(); return; }
      if (st.mode === 'compGE2') { drawRecurGlyph(st.recurD.map(String), 1); return; }
      if (st.mode === 'compOdd') { drawRecurGlyph(st.recurE.map(String), 1); return; }
      if (st.mode === 'zigzag') { drawRecurGlyph(st.recurG.map(String), 1); return; }
      var seq = st.recurSeq, n = seq.length;
      var g = Math.min(cssW * 0.56 / n, cssH * 0.26), ch = g * 0.98;
      var x0 = cssW / 2 - g * (n - 1) / 2, cy = cssH * 0.44;
      var firstBlock = seq.charAt(0) === '1' ? 1 : 2;   // '1'→блок 1; '0'→обязана идти '1', блок «01»
      ctx.fillStyle = COL.blush;                        // бледный кирпич: «смотрим на первый символ»
      ctx.fillRect(x0 - g * 0.5, cy - ch * 0.62, g * firstBlock, ch * 1.24);
      st._seqHit = [];
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      for (var i = 0; i < n; i++) {
        var cx = x0 + g * i;
        ctx.fillStyle = COL.ink; ctx.fillText(seq.charAt(i), cx, cy);
        ctx.strokeStyle = COL.rule; ctx.lineWidth = 2;   // тонкое подчёркивание = символ редактируемый
        ctx.beginPath(); ctx.moveTo(cx - g * 0.27, cy + ch * 0.56); ctx.lineTo(cx + g * 0.27, cy + ch * 0.56); ctx.stroke();
        st._seqHit.push({ x: cx, i: i, g: g });
      }
      if (firstBlock < n) braceUnder(x0 + g * (firstBlock - 0.4), x0 + g * (n - 1 + 0.4), cy + ch * 0.86);
      ctx.save(); ctx.globalAlpha = 0.55; ctx.fillStyle = COL.steel; ctx.textAlign = 'center';
      ctx.font = "16px ui-monospace,monospace"; ctx.fillText('клик по любому символу — меняет 0 ⇄ 1', cssW / 2, cssH * 0.93); ctx.restore();
    }
    function editSeq(px) {                          // клик по ближайшему символу → переключить, сохраняя валидность C (нет «00», конец = 1)
      if (!st._seqHit) return false;
      var best = null, bd = 1e9;
      st._seqHit.forEach(function (h) { var d = Math.abs(px - h.x); if (d < bd) { bd = d; best = h; } });
      if (!best || bd > best.g * 0.7) return false;
      var s = st.recurSeq.split(''), n = s.length, i = best.i, bad = { x: best.x, y: cssH * 0.44, r: best.g * 0.5, a: 1 };
      if (s[i] === '0') { s[i] = '1'; st.recurSeq = s.join(''); return true; }        // убрать 0 — всегда можно
      if (i === n - 1) { st._flash = bad; flashAnim(); return 'blocked'; }             // конец обязан быть 1
      if (s[i - 1] === '0' || s[i + 1] === '0') { st._flash = bad; flashAnim(); return 'blocked'; }  // «00» нельзя
      s[i] = '0'; st.recurSeq = s.join(''); return true;
    }
    function drawRecurSubset() {                    // B: позиции 1..n-1 кружками; крайний подсвечен; клик вкл/выкл (нет соседних)
      var m = st.n - 1, inS = {}; st.recurSub.forEach(function (p) { inS[p] = 1; });
      var g = Math.min(cssW * 0.5 / Math.max(1, m), cssH * 0.24), r = g * 0.34;
      var cx0 = cssW / 2 - g * (m - 1) / 2, cy = cssH * 0.42;
      if (m >= 1) { ctx.fillStyle = COL.blush; ctx.fillRect(cx0 + g * (m - 1) - g * 0.55, cy - r * 1.7, g * 1.1, r * 3.4); }  // «смотрим на крайний элемент»
      st._subHit = [];
      for (var p = 1; p <= m; p++) {
        var x = cx0 + g * (p - 1), filled = !!inS[p], placeable = !inS[p] && !inS[p - 1] && !inS[p + 1], disabled = !filled && !placeable;
        ctx.globalAlpha = disabled ? 0.32 : 1;
        ctx.beginPath(); ctx.arc(x, cy, r, 0, 7); ctx.fillStyle = filled ? COL.brick : COL.card; ctx.fill();
        ctx.lineWidth = 2; ctx.strokeStyle = COL.ink; ctx.stroke(); ctx.globalAlpha = 1;
        ctx.fillStyle = filled ? COL.card : (disabled ? COL.steel : COL.ink);
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = Math.round(r * 1.15) + "px 'Glacial Indifference',sans-serif";
        ctx.fillText(String(p), x, cy);
        st._subHit.push({ x: x, y: cy, r: r * 1.35, p: p, active: !disabled });
      }
      var restEnd = inS[m] ? m - 2 : m - 1;          // остаток: крайний вне → 1..m-1 (B_{n-1}); в → 1..m-2 (B_{n-2})
      if (restEnd >= 1) braceUnder(cx0 - g * 0.45, cx0 + g * (restEnd - 1) + g * 0.45, cy + r * 2.3);
      ctx.save(); ctx.globalAlpha = 0.55; ctx.fillStyle = COL.steel; ctx.textAlign = 'center';
      ctx.font = "16px ui-monospace,monospace"; ctx.fillText('клик по числу — вкл/выкл в подмножество', cssW / 2, cssH * 0.93); ctx.restore();
    }
    function editSubset(px, py) {                   // клик по кружку → вкл/выкл (запрет соседних — фидбек)
      if (!st._subHit) return false;
      for (var i = 0; i < st._subHit.length; i++) {
        var h = st._subHit[i];
        if (Math.abs(px - h.x) <= h.r && Math.abs(py - h.y) <= h.r) {
          if (!h.active) { st._flash = { x: h.x, y: h.y, r: h.r, a: 1 }; flashAnim(); return 'blocked'; }
          var idx = st.recurSub.indexOf(h.p);
          if (idx >= 0) st.recurSub.splice(idx, 1); else st.recurSub.push(h.p);
          return true;
        }
      }
      return false;
    }
    function recurHint(txt) { ctx.save(); ctx.globalAlpha = 0.55; ctx.fillStyle = COL.steel; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.font = "16px ui-monospace,monospace"; ctx.fillText(txt, cssW / 2, cssH * 0.93); ctx.restore(); }
    function drawRecurTiling() {                    // A: полоска, первая плитка подсвечена, скобка над остатком; клик по плитке — квадрат ⇄ доминошка
      var parts = st.recurParts, cells = parts.reduce(function (a, x) { return a + x; }, 0);
      var u = Math.min(cssW * 0.5 / cells, cssH * 0.2), x0 = cssW / 2 - u * cells / 2, cy = cssH * 0.44, top = cy - u / 2;
      ctx.fillStyle = COL.blush; ctx.fillRect(x0 - u * 0.14, top - u * 0.16, parts[0] * u + u * 0.28, u + u * 0.32);
      var x = x0; ctx.lineWidth = Math.max(2, u * 0.05); ctx.strokeStyle = COL.ink;
      parts.forEach(function (p) { var w = p * u; ctx.fillStyle = p === 1 ? COL.sq : COL.dom; ctx.fillRect(x, top, w, u); ctx.strokeRect(x, top, w, u); x += w; });
      st._tileL = { x0: x0, u: u, cells: cells };
      var restX = x0 + parts[0] * u;
      if (restX < x0 + cells * u) braceUnder(restX, x0 + cells * u, cy + u * 0.85);
      recurHint('клик по плитке — квадрат ⇄ доминошка');
    }
    function editTiling(px) {                        // клик → перекладка плитки под курсором (валидное замощение)
      var L = st._tileL; if (!L) return false;
      var cell = Math.floor((px - L.x0) / L.u) + 1;
      if (cell < 1 || cell > L.cells) return false;
      return toggleCell(st.recurParts, cell, true);
    }
    function drawRecurPerm() {                       // F: однострочная π, первый блок подсвечен (π(1)=1 или транспозиция 21), скобка над остатком
      var pi = perm(st.recurParts), n = pi.length, fb = st.recurParts[0] === 1 ? 1 : 2;
      var g = Math.min(cssW * 0.56 / n, cssH * 0.26), ch = g * 0.95, x0 = cssW / 2 - g * (n - 1) / 2, cy = cssH * 0.44;
      ctx.fillStyle = COL.blush; ctx.fillRect(x0 - g * 0.5, cy - ch * 0.62, g * fb, ch * 1.24);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      for (var i = 0; i < n; i++) { ctx.fillStyle = COL.ink; ctx.fillText(String(pi[i]), x0 + g * i, cy); }
      st._permL = { x0: x0, g: g, n: n };
      if (fb < n) braceUnder(x0 + g * (fb - 0.4), x0 + g * (n - 1 + 0.4), cy + ch * 0.86);
      recurHint('клик по числу — переставить соседей');
    }
    function editPerm(px) {                          // клик по позиции → та же перекладка плиток (сосед. транспозиция)
      var L = st._permL; if (!L) return false;
      var pos = Math.floor((px - L.x0) / L.g + 0.5) + 1;
      if (pos < 1 || pos > L.n) return false;
      return toggleCell(st.recurParts, pos, true);
    }
    function drawRecurHwalk() {                      // H: обход цифр, первый шаг (1→2) подсвечен, скобка над остатком; клик — новый пример
      var w = st.recurH, n = w.length;
      var g = Math.min(cssW * 0.56 / n, cssH * 0.26), ch = g * 0.95, x0 = cssW / 2 - g * (n - 1) / 2, cy = cssH * 0.44;
      ctx.fillStyle = COL.blush; ctx.fillRect(x0 - g * 0.5, cy - ch * 0.62, g * 2, ch * 1.24);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      for (var i = 0; i < n; i++) { ctx.fillStyle = COL.ink; ctx.fillText(String(w[i]), x0 + g * i, cy); }
      if (n > 2) braceUnder(x0 + g * 1.6, x0 + g * (n - 1 + 0.4), cy + ch * 0.86);
      recurHint('клик — другой пример обхода');
    }
    function drawRecurGlyph(gl, firstLen) {         // D/E/G: ряд глифов объекта, первый элемент подсвечен, скобка над остатком; клик — другой пример
      var n = gl.length;
      var g = Math.min(cssW * 0.5 / Math.max(1, n), cssH * 0.24), ch = g * 0.9, x0 = cssW / 2 - g * (n - 1) / 2, cy = cssH * 0.44;
      if (!n) { ctx.fillStyle = COL.steel; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = Math.round(cssH * 0.13) + "px 'Glacial Indifference',sans-serif"; ctx.fillText('∅', cssW / 2, cy); recurHint('клик — другой пример'); return; }
      ctx.fillStyle = COL.blush; ctx.fillRect(x0 - g * 0.5, cy - ch * 0.62, g * Math.max(1, firstLen), ch * 1.24);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = "bold " + Math.round(ch) + "px 'Glacial Indifference',monospace";
      for (var i = 0; i < n; i++) { ctx.fillStyle = COL.ink; ctx.fillText(gl[i], x0 + g * i, cy); }
      if (firstLen < n) braceUnder(x0 + g * (firstLen - 0.4), x0 + g * (n - 1 + 0.4), cy + ch * 0.86);
      recurHint('клик — другой пример');
    }

    function draw() {
      if (!cssW) return;
      ctx.clearRect(0, 0, cssW, cssH);
      var stage = curStage();
      if (stage) canvas.style.cursor = (stage === 'recur' || stage === 'bijection') ? 'pointer' : 'default';
      if (stage === 'empty') { return; }                    // картинка после формулировки: низ чист
      if (stage === 'examples') { drawExamples(); return; }
      if (stage === 'recur') { drawRecurMech(); drawFlash(); return; }
      if (stage === 'bijection') {                          // биекция с A: полоска-замощение (верх) ↔ образ модели (низ), выровнены; клик по полоске
        st._L = drawStrip(st.parts, cssH * STRIP_CY, {}); drawImage(); drawFlash(); drawHint(); return;
      }
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

    if (slideEl && window.MutationObserver)   // сцена сменилась (движок повесил .scene-k) → перерисовать сразу
      new MutationObserver(function () { draw(); }).observe(slideEl, { attributes: true, attributeFilter: ['class'] });
    canvas.addEventListener('click', function (e) {
      if (stages.length) {                    // staged: клик активен на сценах «рекуррента» и «биекция»
        var stg = curStage();
        if (stg !== 'recur' && stg !== 'bijection') return;   // прочие сцены — навигация кликером/клавишами
        syncSize();
        var rr = canvas.getBoundingClientRect();
        if (!rr.width || !rr.height) return;   // слайд ещё не отмасштабирован (scale 0) → деление на 0
        var px = (e.clientX - rr.left) / rr.width * cssW, py = (e.clientY - rr.top) / rr.height * cssH;
        if (stg === 'bijection') {            // двусторонний развитый канвас: клик по образу (низ, editimg) ИЛИ по полоске (верх)
          if (editImg && py > cssH * 0.5) { if (toggleImage(px, py) === true) draw(); return; }
          if (st._L && toggleAt(st.parts, px, st._L)) { st._lastPair = -1; draw(); }
          return;
        }
        var done;                              // recur
        if (st.mode === 'subset') done = editSubset(px, py);
        else if (st.mode === 'tiling') done = editTiling(px);
        else if (st.mode === 'perm') done = editPerm(px);
        else if (st.mode === 'hwalk') { var Wk = enumWalksH(st.n + 1); st.recurH = Wk[Math.floor(Math.random() * Wk.length)]; done = true; }
        else if (st.mode === 'compGE2') { var Dk = enumD(st.n); st.recurD = Dk[Math.floor(Math.random() * Dk.length)]; done = true; }
        else if (st.mode === 'compOdd') { var Ek = enumE(st.n); st.recurE = Ek[Math.floor(Math.random() * Ek.length)]; done = true; }
        else if (st.mode === 'zigzag') { var Gk = enumG(st.n); st.recurG = Gk[Math.floor(Math.random() * Gk.length)]; done = true; }
        else done = editSeq(px);
        if (done === true) draw();
        return;
      }
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
