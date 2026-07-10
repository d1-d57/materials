
/* === lab-ext/title-breath.js (вшито сборкой) === */
/* «Дыхание» титульного арта: поверх гравюры изредка проступают и тают
   одиночные штрихи (ink, прозрачные). Искусство остаётся подлинным. */
(function () {
  'use strict';
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  function start() {
    var img = document.querySelector('#sl-title .art img');
    if (!img) return;
    var host = img.parentElement;
    var cv = document.createElement('canvas');
    cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;';
    host.style.position = 'relative';
    host.appendChild(cv);
    var W, H, ctx, strokes = [];
    function size() {
      W = host.clientWidth; H = host.clientHeight;
      var d = Math.min(devicePixelRatio || 1, 2);
      cv.width = W * d; cv.height = H * d;
      ctx = cv.getContext('2d'); ctx.setTransform(d, 0, 0, d, 0, 0);
    }
    size(); addEventListener('resize', size);
    function spawn() {
      // штрих внутри «листа» (центральные 78% по x, 70% по y)
      var x = W * (0.13 + 0.74 * Math.random());
      var y = H * (0.17 + 0.62 * Math.random());
      var a = Math.random() * Math.PI, L = 36 + 70 * Math.random();
      strokes.push({ x: x, y: y, dx: Math.cos(a) * L / 2, dy: Math.sin(a) * L / 2,
                     t: 0, life: 7 + 5 * Math.random() });
      if (strokes.length > 12) strokes.shift();
    }
    var last = 0, acc = 99;
    (function tick(ts) {
      var dt = Math.min(.1, (ts - last) / 1000 || 0); last = ts;
      acc += dt;
      if (acc > 2.6) { acc = 0; spawn(); }
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1.3; ctx.lineCap = 'round'; ctx.strokeStyle = '#333333';
      for (var i = 0; i < strokes.length; i++) {
        var s = strokes[i]; s.t += dt;
        var ph = s.t / s.life;                       // 0..1
        if (ph >= 1) { strokes.splice(i--, 1); continue; }
        var op = .22 * Math.sin(Math.PI * ph);       // проступил — растаял
        ctx.globalAlpha = op;
        ctx.beginPath(); ctx.moveTo(s.x - s.dx, s.y - s.dy);
        ctx.lineTo(s.x + s.dx, s.y + s.dy); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(tick);
    })(0);
  }
  addEventListener('load', start);
})();

