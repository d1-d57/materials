
/* ===== [4] ENGINE — do not edit during content/layout work ===== */
const W = 1440, H = 810;
const slides = Array.from(document.querySelectorAll('.slide:not([data-skip])'));
let groupSizes = {};

/* ---- assets hydration: zones reference <template id="ill-NAME"> ---- */
document.querySelectorAll('[data-ill]').forEach(box => {
  const t = document.getElementById('ill-' + box.dataset.ill);
  if (t) box.appendChild(t.content.cloneNode(true));
});

/* ---- auto-fit: largest font that doesn't overflow the zone ---- */
function fitText(el) {
  const zone = el.closest('.zone');
  if (!zone) return;
  const maxS = parseFloat(el.dataset.max) || 200;
  const minS = parseFloat(el.dataset.min) || 12;
  let lo = minS, hi = maxS;
  const fits = () => el.scrollWidth <= zone.clientWidth &&
                     el.scrollHeight <= zone.clientHeight;
  for (let i = 0; i < 22; i++) {
    const mid = (lo + hi) / 2;
    el.style.fontSize = mid + 'px';
    if (fits()) lo = mid; else hi = mid;
  }
  el.style.fontSize = Math.floor(lo) + 'px';
}
function measureGroups() {           // per-group minima across the deck
  groupSizes = {};
  slides.forEach(s => {
    const d = s.style.display, v = s.style.visibility;
    s.style.display = ''; s.style.visibility = 'hidden';
    s.querySelectorAll('.fit').forEach(el => {
      fitText(el);
      const g = el.dataset.fitGroup;
      if (g) groupSizes[g] = Math.min(groupSizes[g] ?? Infinity,
                                      parseFloat(el.style.fontSize));
    });
    s.style.display = d || 'none'; s.style.visibility = v;
  });
}
function fitAll(root) {
  root.querySelectorAll('.fit').forEach(el => {
    fitText(el);
    const g = el.dataset.fitGroup;
    if (g && groupSizes[g]) el.style.fontSize =
      Math.min(parseFloat(el.style.fontSize), groupSizes[g]) + 'px';
  });
}

/* ---- scenes (progressive disclosure; geometry frozen) ---- */
const scenesOf = s => parseInt(s.dataset.scenes || '1', 10) || 1;
function applyScene(slide, k) {
  for (let i = 1; i <= 9; i++) slide.classList.remove('scene-' + i);
  slide.classList.add('scene-' + k);
  slide.querySelectorAll('[data-scene-until]').forEach(el =>
    el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
}

/* ---- show / navigate ---- */
let cur = 0, scene = 1, overview = false;
function scaleSlide(slide, pad = 0.997) {  /* max screen, no frame margins */
  slide.style.transform =
    'scale(' + Math.min(innerWidth / W, innerHeight / H) * pad + ')';
}
function showSingle(i, k) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  scene = k === undefined ? 1 : k;
  slides.forEach((s, j) => {
    const active = j === cur;
    s.style.display = active ? '' : 'none';
    applyScene(s, active ? scene : scenesOf(s));   // park hidden at final
    s.querySelectorAll('video').forEach(v => {
      if (active) { v.currentTime = 0; const p = v.play(); p && p.catch(() => {}); }
      else v.pause();
    });
  });
  const s = slides[cur];
  fitAll(s);
  scaleSlide(s);
}
function next() {
  if (scene < scenesOf(slides[cur])) applyScene(slides[cur], ++scene);
  else if (cur < slides.length - 1) showSingle(cur + 1, 1);
  syncHash();
}
function prev() {
  /* Back does NOT rewind steps one-by-one: inside a scene it resets the
     slide to step 1; from step 1 it goes to the previous slide in its final
     state (presenter standard). Tested on the author — partial rollbacks
     read as breakage. */
  if (scene > 1) { scene = 1; applyScene(slides[cur], 1); }
  else if (cur > 0) showSingle(cur - 1, scenesOf(slides[cur - 1]));
  syncHash();
}
/* in-canvas step-dots (s05) drive the deck */
addEventListener('message', function(ev){
  var d=ev.data||{}; if(d.navSub==null) return;
  var sc=scenesOf(slides[cur]); var t=Math.max(1,Math.min(sc,(d.navSub|0)+1));
  scene=t; applyScene(slides[cur], scene); syncHash();
});
/* ---- swipe (touch) ---- */
let touchX = null;
addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, {passive: true});
addEventListener('touchend', e => {
  if (touchX === null || editMode || noteMode) return;
  const dx = e.changedTouches[0].clientX - touchX;
  if (Math.abs(dx) > 50) dx < 0 ? next() : prev();
  touchX = null;
}, {passive: true});
function showOverview() {
  const deck = document.getElementById('deck');
  deck.style.display = 'grid';
  deck.style.gridTemplateColumns = 'repeat(2, 1fr)';
  deck.style.gap = '24px'; deck.style.padding = '24px';
  slides.forEach(s => {
    s.style.display = ''; applyScene(s, scenesOf(s));
    fitAll(s);
    s.style.transform = 'scale(' + 420 / W + ')';
    s.style.transformOrigin = 'top left';
  });
}
function render() {
  const deck = document.getElementById('deck');
  if (!overview) {
    deck.style.display = ''; deck.style.padding = '';
    deck.style.gridTemplateColumns = '';
    slides.forEach(s => { s.style.transformOrigin = 'center center'; });
  }
  overview ? showOverview() : showSingle(cur, scene);
}

/* ---- fullscreen + blank (clicker-grade) ---- */
function toggleFullscreen() {
  const el = document.documentElement;
  if (!document.fullscreenElement)
    el.requestFullscreen && el.requestFullscreen().catch(() => {});
  else document.exitFullscreen && document.exitFullscreen().catch(() => {});
}

/* ---- export mode: ?only=N&scene=K → clean unscaled W×H frame ---- */
const Q = new URLSearchParams(location.search);
const only = Q.get('only');
function exportFrame() {
  document.getElementById('hint').style.display = 'none';
  document.getElementById('stage').style.placeItems = 'start';
  const n = +only;
  const k = Q.get('scene') !== null ? +Q.get('scene') : scenesOf(slides[n]);
  slides.forEach((s, j) => { s.style.display = j === n ? '' : 'none'; });
  applyScene(slides[n], k);
  fitAll(slides[n]);                       // no scale: exactly W×H
}

/* ---- hash routing: #s2.3 = slide 2, scene 3 (shareable position) ---- */
function syncHash() {
  if (only !== null || overview) return;
  history.replaceState(null, '', '#s' + cur + '.' + scene);
}
function readHash() {
  const m = location.hash.match(/^#s(\d+)(?:\.(\d+))?$/);
  if (m) { cur = +m[1]; scene = m[2] ? +m[2] : 1; }
}
readHash();
measureGroups();
only !== null ? exportFrame() : render();
syncHash();

/* FEEDBACK-TOOLS-START (stripped from delivery by build_single.py) */
/* ---- feedback tools: E = edit text, A = pin notes, X = report ----
   The user fixes typos/wording himself (fitter re-runs live) and pins
   visual remarks to exact spots; X produces a structured report to paste
   back into the chat — Claude applies it surgically to the source file. */
const origHTML = new Map();
document.querySelectorAll('.fit').forEach(el => origHTML.set(el, el.innerHTML));
let editMode = false, noteMode = false;
const notes = [];
function setEdit(on) {
  editMode = on;
  document.querySelectorAll('.fit').forEach(el => el.contentEditable = on);
  flash(on ? 'правка текста: кликни в текст и печатай (Esc — закончить)'
           : 'правка текста выключена');
}
function flash(msg) {
  const h = document.getElementById('hint');
  h.textContent = msg; h.style.color = '#ddd';
  clearTimeout(flash.t);
  flash.t = setTimeout(() => { h.style.color = '#888'; }, 2500);
}
function addrOf(el) {
  const slide = el.closest('.slide');
  const zones = Array.from(slide.querySelectorAll('.zone'));
  const z = el.closest('.zone');
  return slide.id + (z ? ' / зона ' + (zones.indexOf(z) + 1) +
         (z.className.replace('zone', '').trim() ? ' (' + z.className.replace('zone', '').trim() + ')' : '') : '');
}
document.addEventListener('input', e => {
  const f = e.target.closest && e.target.closest('.fit');
  if (editMode && f) fitText(f);
});
addEventListener('click', e => {
  if (!noteMode) return;
  const slide = e.target.closest('.slide');
  if (!slide || e.target.closest('.note-pin')) return;
  const r = slide.getBoundingClientRect();
  const x = Math.round((e.clientX - r.left) / r.width * 100);
  const y = Math.round((e.clientY - r.top) / r.height * 100);
  const txt = prompt('Заметка к этому месту:');
  if (!txt) return;
  notes.push({ addr: addrOf(e.target), x, y, txt });
  const pin = document.createElement('div');
  pin.className = 'note-pin'; pin.textContent = notes.length;
  pin.style.cssText = 'position:absolute;left:' + x + '%;top:' + y + '%;' +
    'transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;' +
    'background:#bf5b4f;color:#fff;display:grid;place-items:center;' +
    'font:700 18px sans-serif;z-index:99;cursor:default;';
  pin.title = txt;
  slide.appendChild(pin);
});
function buildReport() {
  let out = '';
  const edits = [];
  origHTML.forEach((orig, el) => {
    if (el.innerHTML !== orig)
      edits.push('[' + addrOf(el) + '] → «' + el.innerText.trim() + '»');
  });
  if (edits.length) out += '== ПРАВКИ ТЕКСТА ==\n' + edits.join('\n') + '\n';
  if (notes.length) out += '== ЗАМЕТКИ ==\n' + notes.map((n, i) =>
    (i + 1) + '. [' + n.addr + ' @ ' + n.x + '%,' + n.y + '%] ' + n.txt).join('\n');
  return out || 'Правок и заметок нет.';
}
function showReport() {
  const old = document.getElementById('report-overlay');
  if (old) { old.remove(); return; }
  const o = document.createElement('div');
  o.id = 'report-overlay';
  o.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.75);' +
    'display:grid;place-items:center;z-index:1000;';
  const t = document.createElement('textarea');
  t.value = buildReport();
  t.style.cssText = 'width:70%;height:60%;font:14px/1.5 monospace;padding:16px;';
  o.appendChild(t); document.body.appendChild(o);
  t.focus(); t.select();
  flash('скопируй отчёт и вставь его в чат с Claude (X — закрыть)');
  o.addEventListener('click', e => { if (e.target === o) o.remove(); });
}

/* FEEDBACK-TOOLS-END */

/* ---- keymap: works with any presentation clicker ---- */
addEventListener('keydown', e => {
  if (only !== null) return;
  if (e.target.isContentEditable) {           // typing in edit mode
    if (e.code === 'Escape') { setEdit(false); e.target.blur(); }
    return;
  }
  if (e.target.tagName === 'TEXTAREA') {      // report overlay
    if (e.code === 'Escape') document.getElementById('report-overlay')?.remove();
    return;
  }
  if (e.code === 'KeyE') { e.preventDefault(); setEdit(!editMode); return; }
  if (e.code === 'KeyA') {
    e.preventDefault(); noteMode = !noteMode;
    flash(noteMode ? 'заметки: кликай по месту на слайде (A — закончить)'
                   : 'режим заметок выключен'); return;
  }
  if (e.code === 'KeyX') { e.preventDefault(); showReport(); return; }
  if (e.code === 'KeyF' || e.code === 'F5' || e.code === 'F11') {
    e.preventDefault(); toggleFullscreen(); return;
  }
  if (e.code === 'Escape') { document.body.classList.remove('blanked'); return; }
  if (e.code === 'KeyB' || e.code === 'Period') {
    e.preventDefault(); document.body.classList.toggle('blanked'); return;
  }
  if (e.code === 'KeyO') { overview = !overview; render(); return; }
  if (overview) return;
  if (['ArrowRight','ArrowDown','PageDown','Space','Enter','KeyN'].includes(e.code)) {
    e.preventDefault(); next();
  } else if (['ArrowLeft','ArrowUp','PageUp','Backspace','KeyP'].includes(e.code)) {
    e.preventDefault(); prev();
  } else if (e.code === 'Home') { e.preventDefault(); showSingle(0, 1); }
  else if (e.code === 'End') { e.preventDefault(); showSingle(slides.length - 1, 1); }
});
addEventListener('dblclick', e => {
  if (e.target.closest('video, a, button, input, select, textarea')) return;
  toggleFullscreen();
});
addEventListener('resize', () => { if (only === null) render(); });

/* ---- re-measure after fonts load (metrics change) ---- */
if (document.fonts && document.fonts.ready)
  document.fonts.ready.then(() => {
    measureGroups();
    only !== null ? exportFrame() : render();
  });
/* ===== /ENGINE ===== */
