
/* ===== [4] ENGINE — канонический из deck-skeleton.html ===== */
const W = 1440, H = 810;
const slides = Array.from(document.querySelectorAll('.slide'));
let groupSizes = {};

document.querySelectorAll('[data-ill]').forEach(box => {
  const t = document.getElementById('ill-' + box.dataset.ill);
  if (t) box.appendChild(t.content.cloneNode(true));
});

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
function measureGroups() {
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

const scenesOf = s => parseInt(s.dataset.scenes || '1', 10) || 1;
function applyScene(slide, k) {
  for (let i = 1; i <= 9; i++) slide.classList.remove('scene-' + i);
  slide.classList.add('scene-' + k);
  slide.querySelectorAll('[data-scene-until]').forEach(el =>
    el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
}

let cur = 0, scene = 1, overview = false;
function scaleSlide(slide, pad = 0.997) {  /* ПАТЧ (автор): максимум экрана, поля убраны */
  slide.style.transform =
    'scale(' + Math.min(innerWidth / W, innerHeight / H) * pad + ')';
}
function showSingle(i, k) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  scene = k === undefined ? 1 : k;
  slides.forEach((s, j) => {
    const active = j === cur;
    s.style.display = active ? '' : 'none';
    applyScene(s, active ? scene : scenesOf(s));
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
/* ПАТЧ (решение автора, 2026-06-10; отличие от скелета):
   «назад» не отматывает шаги по одному — внутри сцены сбрасывает слайд
   к шагу 1 целиком; с шага 1 уходит на предыдущий слайд в финальном
   состоянии (стандарт презентеров). Кандидат на upstream в скилл. */
function prev() {
  if (scene > 1) { scene = 1; applyScene(slides[cur], 1); }
  else if (cur > 0) showSingle(cur - 1, scenesOf(slides[cur - 1]));
  syncHash();
}
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
  const stage = document.getElementById('stage');
  stage.style.placeItems = 'start'; stage.style.overflowY = 'auto';
  deck.style.display = 'grid';
  const cols = innerWidth < 1100 ? 3 : 4;
  const sc = Math.min(0.30, (innerWidth - 44 - (cols - 1) * 16) / cols / W);
  deck.style.gridTemplateColumns = 'repeat(' + cols + ', ' + Math.round(W * sc) + 'px)';
  deck.style.gap = '16px'; deck.style.padding = '22px';
  deck.style.justifyContent = 'center'; deck.style.alignContent = 'start';
  slides.forEach((s, i) => {
    s.style.display = ''; applyScene(s, scenesOf(s));
    fitAll(s);
    s.style.transform = ''; s.style.zoom = sc;
    s.style.cursor = 'pointer';
    s.style.boxShadow = (i === cur) ? '0 0 0 3px var(--accent,#785a18)' : '0 1px 5px rgba(0,0,0,.22)';
    if (!s._ovBound) { s._ovBound = true; s.addEventListener('click', function () {
      if (!overview) return; cur = i; scene = scenesOf(slides[i]); overview = false; render();
    }); }
  });
}
function render() {
  const deck = document.getElementById('deck');
  if (!overview) {
    deck.style.display = ''; deck.style.padding = '';
    deck.style.gridTemplateColumns = ''; deck.style.gap = '';
    deck.style.justifyContent = ''; deck.style.alignContent = '';
    const stage = document.getElementById('stage');
    stage.style.placeItems = ''; stage.style.overflowY = '';
    slides.forEach(s => { s.style.transformOrigin = 'center center'; s.style.zoom = ''; s.style.cursor = ''; s.style.boxShadow = ''; });
  }
  overview ? showOverview() : showSingle(cur, scene);
}

function toggleFullscreen() {
  const el = document.documentElement;
  if (!document.fullscreenElement)
    el.requestFullscreen && el.requestFullscreen().catch(() => {});
  else document.exitFullscreen && document.exitFullscreen().catch(() => {});
}

const Q = new URLSearchParams(location.search);
const only = Q.get('only');
function exportFrame() {
  document.getElementById('hint').style.display = 'none';
  document.getElementById('stage').style.placeItems = 'start';
  const n = +only;
  const k = Q.get('scene') !== null ? +Q.get('scene') : scenesOf(slides[n]);
  slides.forEach((s, j) => { s.style.display = j === n ? '' : 'none'; });
  applyScene(slides[n], k);
  fitAll(slides[n]);
}

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
  flash.t = setTimeout(() => { h.style.color = '#8a96a3'; }, 2500);
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

addEventListener('keydown', e => {
  if (only !== null) return;
  if (e.target.isContentEditable) {
    if (e.code === 'Escape') { setEdit(false); e.target.blur(); }
    return;
  }
  if (e.target.tagName === 'TEXTAREA') {
    if (e.code === 'Escape') document.getElementById('report-overlay')?.remove();
    return;
  }
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

if (document.fonts && document.fonts.ready)
  document.fonts.ready.then(() => {
    measureGroups();
    only !== null ? exportFrame() : render();
  });
/* ===== /ENGINE ===== */
