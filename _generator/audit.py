#!/usr/bin/env python3
"""Канон-аудит собранного дека фабрики (арка 10 · гейт слой 3, 10-sborka-qa/DOK.md).

Использование: python3 audit.py <src>/dist/index.html [--free] [--scene-diff]
  --free        пропустить канон-only проверки (палитра, цвет текста, figcaption)
  --scene-diff  инвариант замороженной геометрии: соседние сцены отличаются ТОЛЬКО
                добавленными пикселями И ни один клик не пуст (каждый шаг что-то раскрывает)

Паттерн 1:1 с html-slides-studio/scripts/audit.py (JS-пробинг через page.evaluate,
PASS/FAIL/WARN построчно, exit 1 при FAIL, WARN билд не валит), НО адаптировано под НАШ
канон-выход build_deck.py:
  · точка входа — <src>/dist/index.html (самодостаточный дек, всё вшито);
  · ALLOWED_BG НЕ хардкод — ПАРСИТСЯ из :root СОБРАННОГО дека (tokens.css вшит в <style>),
    т.к. Р8-tiers разрешает пер-дек оверрайд палитры (10-DOK §гейт слой 3).

ТРЕБУЕТ Playwright (браузер) — гонится на машине владельца; в песочнице генератора
браузера нет (см. _generator/README.md). Написан по контракту, прогон — за владельцем.
"""
import sys, os, re
from playwright.sync_api import sync_playwright

DECK = os.path.abspath(sys.argv[1])
FREE = '--free' in sys.argv
FLOOR_PX = 35   # 4.3% от 810 — тело никогда ниже (канон: не ужимать, а делить слайд)


def _norm_hex(h):
    """'#abc' → '#aabbcc'; '#AABBCC' → '#aabbcc' (сверять с выходом px2hex в JS)."""
    h = h.lower()
    if len(h) == 4:   # #rgb
        h = '#' + ''.join(c * 2 for c in h[1:])
    return h


def parse_allowed_bg(deck_path):
    """ALLOWED_BG = все hex-цвета из ПЕРВОГО :root{...} собранного дека (вшитый tokens.css) +
    'transparent'. Не хардкод-сет — палитра берётся из самого дека (пер-дек оверрайд, Р8)."""
    text = open(deck_path, encoding='utf-8').read()
    m = re.search(r':root\s*\{(.*?)\}', text, re.S)
    root = m.group(1) if m else ''
    allowed = {_norm_hex(h) for h in re.findall(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b', root)}
    allowed.add('transparent')
    return allowed


# ── JS-проба (дословно паттерн скилла: измеряем каждый слайд в ФИНАЛЬНОЙ сцене) ──
JS = r"""
() => {
  const px2hex = c => {
    const m = c.match(/\d+(\.\d+)?/g);
    if (!m) return c;
    if (m.length >= 4 && parseFloat(m[3]) === 0) return 'transparent';
    return '#' + m.slice(0,3).map(n => (+n).toString(16).padStart(2,'0')).join('');
  };
  const out = { slides: [] };
  document.querySelectorAll('.slide').forEach((s, i) => {
    const r = { id: s.id || ('#'+i), overflow: [], forbidden: [],
                bg: new Set(), textColors: new Set(), fits: [], svgOverflow: [],
                svgProse: [], smallCanvas: [],
                figcaption: s.querySelector('figcaption') !== null };
    // припарковать в финальной сцене — чтобы всё измеримо/видимо
    const n = parseInt(s.dataset.scenes || '1', 10) || 1;
    for (let k = 1; k <= 9; k++) s.classList.remove('scene-' + k);
    s.classList.add('scene-' + n);
    const disp = s.style.display; s.style.display = '';
    s.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none') return;
      const b = el.getBoundingClientRect();
      // запрещённая декорация (канон: ноль где угодно)
      if (cs.boxShadow !== 'none') r.forbidden.push(['box-shadow', el.tagName + '.' + el.className]);
      if (parseFloat(cs.borderRadius) > 0) r.forbidden.push(['border-radius', el.tagName + '.' + el.className]);
      if (/gradient/.test(cs.backgroundImage)) r.forbidden.push(['gradient', el.tagName + '.' + el.className]);
      // проба палитры: только крупные плоские заливки
      if (b.width * b.height > 8000) {
        const bg = px2hex(cs.backgroundColor);
        if (bg !== 'transparent') r.bg.add(bg);
      }
      if (el.matches('.zone') &&
          (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1))
        r.overflow.push(el.className);
      if (el.matches('.fit')) {
        r.fits.push({ group: el.dataset.fitGroup || null,
                      size: parseFloat(cs.fontSize) });
      }
      if (el.matches('.t-body'))
        r.bodySizes = (r.bodySizes || []).concat(parseFloat(cs.fontSize));
      if ((el.matches('.fit') || el.matches('.t-body')) && (el.textContent || '').trim())
        r.textColors.add(px2hex(cs.color));
    });
    // инлайн-SVG, вылезающий за панель = баг несайзнутого SVG (нужен width/height:100% + preserveAspectRatio)
    const MATHOP = /[=+*−×·÷≤≥⇒→√∑]/;
    s.querySelectorAll('svg').forEach(svg => {
      const p = svg.parentElement;
      if (p) {
        const sb = svg.getBoundingClientRect(), pb = p.getBoundingClientRect();
        if (sb.width > pb.width + 1 || sb.height > pb.height + 1)
          r.svgOverflow.push(svg.getAttribute('class') || p.className || 'svg');
      }
      // адвайзори: <text> как фраза (пробел + слово 3+ букв), НЕ формула (нет матоператоров) = проза-подпись
      svg.querySelectorAll('text').forEach(t => {
        const tx = (t.textContent || '').trim();
        if (tx && /\s/.test(tx) && /[a-zа-яё]{3,}/i.test(tx) && !MATHOP.test(tx))
          r.svgProse.push(tx.slice(0, 40));
      });
    });
    // адвайзори: ключевой canvas — крошечная врезка (< 12% слайда); иллюстрации должны быть крупными
    const _sb = s.getBoundingClientRect(), _area = (_sb.width * _sb.height) || (1440 * 810);
    s.querySelectorAll('canvas').forEach(c => {
      const cb = c.getBoundingClientRect(), a = cb.width * cb.height;
      if (a > 0 && a < 0.12 * _area) r.smallCanvas.push(Math.round(100 * a / _area) + '%');
    });
    s.style.display = disp;
    r.bg = [...r.bg]; r.textColors = [...r.textColors];
    out.slides.push(r);
  });
  return out;
}
"""

fails, report = [], []
def check(name, ok, detail=''):
    report.append(("PASS" if ok else "FAIL") + "  " + name + ((' — ' + detail) if detail and not ok else ''))
    if not ok:
        fails.append(name)

warns = []
def warn(name, ok, detail=''):
    """Адвайзори: печатает WARN, но билд не валит (exit-код остаётся 0)."""
    report.append(("PASS" if ok else "WARN") + "  " + name + ((' — ' + detail) if detail and not ok else ''))
    if not ok:
        warns.append(name)


ALLOWED_BG = parse_allowed_bg(DECK)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 810})
    pg.goto('file://' + DECK)
    pg.wait_for_load_state('networkidle')
    pg.evaluate('document.fonts && document.fonts.ready')
    pg.wait_for_timeout(200)
    data = pg.evaluate(JS)
    b.close()

groups = {}
for s in data['slides']:
    sid = s['id']
    check(sid + ': no overflow', not s['overflow'], str(s['overflow']))
    check(sid + ': inline SVG fits its box (else width/height:100% + preserveAspectRatio)',
          not s.get('svgOverflow'), str(s.get('svgOverflow')))
    warn(sid + ': no prose caption on illustration (SVG <text>; canvas-drawn text NOT checked)',
         not s.get('svgProse'), str(s.get('svgProse')))
    warn(sid + ': canvas not a tiny inset (>=12% of slide)',
         not s.get('smallCanvas'), str(s.get('smallCanvas')))
    check(sid + ': no shadows/radius/gradients', not s['forbidden'],
          str(s['forbidden'][:3]))
    if not FREE:
        bad_bg = [c for c in s['bg'] if c not in ALLOWED_BG]
        check(sid + ': planes within canon palette (:root)', not bad_bg, str(bad_bg))
        bad_tc = [c for c in s['textColors'] if c != '#333333']
        check(sid + ': all text #333', not bad_tc, str(bad_tc))
        check(sid + ': no figcaption', not s['figcaption'])
    for f in s['fits']:
        if f['group']:
            groups.setdefault(f['group'], set()).add(round(f['size']))
    if not FREE:
        for sz in s.get('bodySizes') or []:
            check(sid + ': body (.t-body) >= ' + str(FLOOR_PX) + 'px floor', sz >= FLOOR_PX,
                  str(sz) + "px — split the slide, don't shrink")

for g, sizes in groups.items():
    check('fit-group "' + g + '" consistent across deck', len(sizes) == 1, str(sorted(sizes)))

if '--scene-diff' in sys.argv:
    from PIL import Image
    import tempfile
    BG = [(0xe6,0xe5,0xe1), (0xa7,0xc2,0xcb), (0xff,0xff,0xff), (0x11,0x11,0x11)]
    TOL, MAX_BAD = 14, 0.0005   # допуск на канал; доля «плохих» пикселей
    EMPTY_SHARE = 0.0001        # ниже этой доли ИЗМЕНЁННЫХ пикселей сцена ничего не раскрыла (пустой клик)
    def is_bg(px):
        return any(all(abs(px[i]-bb[i]) <= TOL for i in range(3)) for bb in BG)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 810})
        pg.goto('file://' + DECK)
        # `.slide:not([data-skip])` — тот же счёт, что у движка (render.py:36):
        # `?only=i` индексирует массив slides движка, а он data-skip не включает.
        # Со старым `.slide` каждый индекс после пропущенного слайда указывал на
        # СОСЕДА (найдено 30.07 на dandelin: 19 узлов против 18 в slides).
        n_scenes = pg.evaluate(
            "Array.from(document.querySelectorAll('.slide:not([data-skip])'))"
            ".map(s=>+(s.dataset.scenes||1))")
        tmp = tempfile.mkdtemp()
        for i, n in enumerate(n_scenes):
            if n < 2:
                continue
            frames = []
            for k in range(1, n + 1):
                pg.goto('file://' + DECK + '?only=' + str(i) + '&scene=' + str(k))
                pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(250)
                f = tmp + '/s' + str(i) + '-' + str(k) + '.png'; pg.screenshot(path=f)
                frames.append(Image.open(f).convert('RGB'))
            for k in range(1, n):
                a, c = frames[k-1], frames[k]
                pa, pc = a.load(), c.load()
                bad = changed = 0
                for y in range(0, a.height, 2):          # шаг 2: достаточно быстро
                    for x in range(0, a.width, 2):
                        if pa[x, y] != pc[x, y]:
                            changed += 1
                            if not is_bg(pa[x, y]):
                                bad += 1
                tot = a.width * a.height / 4
                share, ch_share = bad / tot, changed / tot
                check('slide ' + str(i) + ': scene ' + str(k) + '->' + str(k+1) + ' adds pixels only',
                      share <= MAX_BAD, '%.2f%% non-additive pixels' % (share * 100))
                check('slide ' + str(i) + ': scene ' + str(k+1) + ' not empty (a click must reveal something)',
                      ch_share >= EMPTY_SHARE,
                      'only %.3f%% changed — empty click; fix the script or delete the scene' % (ch_share * 100))
        b.close()

print('\n'.join(report))
print('\n' + ('ALL PASS' if not fails else (str(len(fails)) + ' FAILURES')) +
      (('  (' + str(len(warns)) + ' warnings)') if warns else ''))
sys.exit(1 if fails else 0)
