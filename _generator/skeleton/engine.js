
/* ===== [4] ENGINE — do not edit during content/layout work ===== */
const W = 1440, H = 810;
const slides = Array.from(document.querySelectorAll('.slide:not([data-skip])'));
let groupSizes = {};

/* ---- lecture progress bar (Д27 захода gruppa-D-kompilyator) ----
   `sborka/deck.py` и `slaid.py` не читают `_generator/skeleton/shablon.html`
   (у них свой инлайн-шаблон `doc = """…"""`) — тот прогресс-бар (#lect-progress/
   #lect-zone), что уже есть в shablon.html у пайплайна build_deck.py, до них не
   долетает вовсе. Прототип там опрашивал `location.hash` по таймеру (отдельный
   скрипт, без доступа к внутренностям движка); здесь `cur`/`slides.length` уже
   точно известны движку — хук в showSingle() ниже, без опроса. */
const lectZone = document.createElement('div');
lectZone.id = 'lect-zone';
document.body.appendChild(lectZone);
const lectProgress = document.createElement('div');
lectProgress.id = 'lect-progress';
document.body.appendChild(lectProgress);
/* П13 (POMARKI-2026-08-09 §4): номер слайда в правом нижнем углу — механизм
   был закрыт ошибочно на #lect-progress (та полоса прогресса, не номер);
   долг Д27 в части номера возвращён в ЖИВ. */
const lectNumber = document.createElement('div');
lectNumber.id = 'lect-number';
document.body.appendChild(lectNumber);
function updateProgress() {
  lectProgress.style.width = (slides.length ? 100 * (cur + 1) / slides.length : 0) + '%';
  lectNumber.textContent = slides.length ? (cur + 1) + ' / ' + slides.length : '';
}
lectZone.addEventListener('mouseenter', () => {
  lectProgress.style.height = '6px'; lectProgress.style.opacity = '.85';
});
lectZone.addEventListener('mouseleave', () => {
  lectProgress.style.height = '2.5px'; lectProgress.style.opacity = '.55';
});
lectZone.addEventListener('click', e => {
  const i = Math.min(slides.length - 1, Math.floor(e.clientX / innerWidth * slides.length));
  showSingle(i, 1); syncHash();
});

/* ---- assets hydration: zones reference <template id="ill-NAME"> ---- */
document.querySelectorAll('[data-ill]').forEach(box => {
  const t = document.getElementById('ill-' + box.dataset.ill);
  if (!t) return;
  box.appendChild(t.content.cloneNode(true));
  /* Д52#2 захода gruppa-D-kompilyator: `.panel > svg{width:100%;height:100%}`
     (base.css) сажает БОКС svg на панель, но не спасает от собственных
     width/height-атрибутов авторской иллюстрации (специфичность инлайн-
     атрибута может забить внешний стиль) и не удерживает пропорцию — снимаем
     конфликтующие атрибуты и явно ставим preserveAspectRatio ЗДЕСЬ, в
     единственном месте, где иллюстрация становится живым DOM (не в каждой
     иллюстрации по отдельности). Вписывает и маленький svg в большую панель,
     и большой в маленькую — оба вида проверял audit.py (`svgOverflow`). */
  box.querySelectorAll('svg').forEach(svg => {
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    if (!svg.hasAttribute('preserveAspectRatio'))
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  });
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
/* Math.max(1, …) — не украшение: parseInt('-3') даёт −3, а это ЧИСЛО, значит
   `|| 1` его не отсекает. Отрицательное `data-scenes` уходило дальше во все
   потребители сразу (next/prev/парковка скрытых/обзор), а с зажатием в
   applyScene давало класс `scene--3`, которого нет ни в одном каскаде и который
   не снимается фильтром `/^scene-\d+$/`. Порог стоит ЗДЕСЬ, в единственном
   месте, где число сцен вообще читается, — иначе его пришлось бы повторять у
   шести вызывающих. Найдено верификатором. */
const scenesOf = s => Math.max(1, parseInt(s.dataset.scenes || '1', 10) || 1);
function applyScene(slide, k) {
  /* Сцена не может выйти за фактическое число сцен слайда. Ставится ЗДЕСЬ, а не
     у вызывающих: так лечатся все входы разом — hash-роутинг #sN.K (readHash
     ничего не проверяет), ручной ?scene=, ?scene=0, ?scene=-1, экспорт, будущие
     инструменты. Один вход это уже умел (postMessage ниже зажимает сам) —
     остальные приводятся к нему. NaN из мусора («?scene=abc») тоже сюда: он не
     пройдёт ни одно сравнение и даст 1. */
  const n = scenesOf(slide);
  k = (k >= 1 && k <= n) ? Math.floor(k) : (k > n ? n : 1);
  /* Снимаем ФАКТИЧЕСКИЕ scene-классы, а не диапазон 1..9. Цикл до девятки не
     снимал ни scene-10 и выше, ни залипший scene-99 из старой ссылки — то есть
     давал слайд с двумя классами сцен разом. Фильтр по classList верхней границы
     не знает вовсе и потому не может от неё отстать снова. */
  Array.from(slide.classList)
    .filter(c => /^scene-\d+$/.test(c))
    .forEach(c => slide.classList.remove(c));
  slide.classList.add('scene-' + k);
  slide.querySelectorAll('[data-scene-until]').forEach(el =>
    el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
  /* Возвращаем ФАКТИЧЕСКУЮ сцену. Нужна она ровно одному вызывающему —
     showSingle: он держит `scene`, из которой syncHash пишет адрес. Остальные
     (exportFrame, next, prev, обзор, postMessage) значение отбрасывают законно:
     они и так передают k из диапазона, и своего состояния сцены не держат. */
  return k;
}

/* ---- show / navigate ---- */
let cur = 0, scene = 1, overview = false;
function scaleSlide(slide, pad = 0.997) {  /* max screen, no frame margins */
  slide.style.transform =
    'scale(' + Math.min(innerWidth / W, innerHeight / H) * pad + ')';
}

/* ---- ВЫЛЕТ ФОНА ЗА КАДР (доводка Л2, Ф1а) ----
   Летербокс сделали цветом холста (base.css, Ш3) — и осталась вторая половина
   того же дефекта: на слайде с полосой зелёная панель обрывалась ровно на кромке
   кадра, номер слайда внизу лежал на бежевом ПОД зелёной полосой, и кадр всё
   равно читался границей. Здесь поля дописываются: каждая точка поля берёт цвет
   той точки слайда, что стоит над ней (или сбоку от неё).
   Раскраска снимается с ЖИВОГО DOM, а не повторяет типы вёрстки из tipy.py:
   девять типов (polosa_gorizontalnaya, polosa_vertikalnaya, kompozit, vizitka…)
   пришлось бы описать вторым, независимым списком — и он молча отстал бы от
   первого на следующем новом типе. Правило простое и типов не знает: элемент с
   непрозрачным фоном, дотянувшийся до кромки кадра, продолжает свой цвет наружу
   по этой кромке; коснулся двух кромок — заполняет и угол.
   ::before читается отдельно, потому что линейка между текстом и картинкой
   (_linija_ill) — именно псевдоэлемент, и на слайде с ВЕРТИКАЛЬНОЙ полосой без
   неё поле сверху получалось двухцветным, но без разделителя.
   Порядок обхода = порядок DOM = порядок отрисовки: вложенный фон ложится
   поверх фона родителя, как и в самом слайде. */
const bleed = document.createElement('div');
bleed.id = 'bleed';
const bleedBands = document.createElement('div');
bleedBands.style.cssText = 'position:absolute;inset:0';
const bleedUzor = document.createElement('div');
bleedUzor.id = 'bleed-uzor';
bleed.appendChild(bleedBands);
bleed.appendChild(bleedUzor);
/* ПЕРВЫМ ребёнком body, а не последним: слой обязан лежать выше фона body и ниже
   #stage, а у позиционированных соседей с z-index:auto порядок отрисовки = порядок
   DOM. Приписанный в конец (как #lect-zone ниже) он закрыл бы собою слайд. */
document.body.insertBefore(bleed, document.body.firstChild);
/* «rgba(…, 0)» — это ПРОЗРАЧНО, и именно такую строку отдаёт getComputedStyle
   для фона по умолчанию: без этой проверки поля залились бы чёрным. */
const isOpaque = c => !!c && c !== 'transparent' && !/,\s*0\s*\)\s*$/.test(c);
function bleedOff() {
  bleed.style.display = 'none';
  slides.forEach(s => {
    s.style.removeProperty('--uzor-sz');
    s.style.removeProperty('--uzor-x');
    s.style.removeProperty('--uzor-y');
  });
}
function paintBleed(slide) {
  const r = slide.getBoundingClientRect();
  const k = r.width / W || 1;                    // масштаб кадра → локальные px
  const padT = r.top, padB = innerHeight - r.bottom,
        padL = r.left, padR = innerWidth - r.right;
  bleed.style.display = '';
  bleedBands.textContent = '';
  const eps = 1.5;                               // pad 0.997 в scaleSlide даёт дробную щель
  const put = (x, y, w, h, bg, op) => {
    if (w <= .5 || h <= .5) return;
    const d = document.createElement('div');
    d.style.cssText = 'position:absolute;left:' + x + 'px;top:' + y + 'px;width:' +
      w + 'px;height:' + h + 'px;background:' + bg + ';opacity:' + op;
    bleedBands.appendChild(d);
  };
  const spill = (q, bg, op) => {
    const onT = q.top <= r.top + eps, onB = q.bottom >= r.bottom - eps;
    const onL = q.left <= r.left + eps, onR = q.right >= r.right - eps;
    const x0 = onL ? 0 : q.left, x1 = onR ? innerWidth : q.right;
    const y0 = onT ? 0 : q.top,  y1 = onB ? innerHeight : q.bottom;
    if (onT) put(x0, 0, x1 - x0, padT, bg, op);
    if (onB) put(x0, r.bottom, x1 - x0, padB, bg, op);
    if (onL) put(0, y0, padL, y1 - y0, bg, op);
    if (onR) put(r.right, y0, padR, y1 - y0, bg, op);
  };
  [slide].concat(Array.from(slide.querySelectorAll('*'))).forEach((el, i) => {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    const op = parseFloat(cs.opacity);
    /* Прозрачное наружу не лезет — но у САМОГО слайда (i === 0) opacity в этот
       момент 0 всегда: идёт анимация deck-in, и paintBleed зовётся на её первом
       кадре. Без исключения фон слайда не дописывался НИКОГДА, и на слайде со
       сплошным зелёным холстом (обложка, разделитель, финал) поле оставалось
       бежевым. Опасности нет: анимация кончается на opacity 1. */
    if (i > 0 && !(op > .02)) return;
    const q = el.getBoundingClientRect();
    if (q.width < .5 || q.height < .5) return;
    if (isOpaque(cs.backgroundColor)) spill(q, cs.backgroundColor, 1);
    const ps = getComputedStyle(el, '::before');
    if (ps.content === 'none' || !isOpaque(ps.backgroundColor)) return;
    const pw = parseFloat(ps.width), ph = parseFloat(ps.height);
    if (!(pw > .5) || !(ph > .5)) return;
    const pl = parseFloat(ps.left) || 0, pt = parseFloat(ps.top) || 0;
    spill({ left:  q.left + pl * k, right:  q.left + (pl + pw) * k,
            top:   q.top  + pt * k, bottom: q.top  + (pt + ph) * k },
          ps.backgroundColor, parseFloat(ps.opacity) || 1);
  });
  /* 🔴 ПОЛНОКАДРОВЫЙ РАСТР — ВТОРОЙ ВИД ФОНА, КОТОРОГО ЦИКЛ ВЫШЕ НЕ ВИДИТ ВОВСЕ
     (Д4 захода vlitie-i-deka, 2026-08-15). Цикл продлевает наружу только
     непрозрачный background-COLOR. Обложка и финальный нарисованы иначе: их фон —
     картинка дизайнеров (`sluzhebnye/cover-bg.html`, `<div class="bg"><img>`),
     у которой background-color нет ни на одном узле. Наружу поэтому уезжал
     единственный непрозрачный цвет в слайде — беж самого `.slide`
     (`background:var(--paper)`), и зелёная панель с вертикальной линией
     обрывались ровно на кромке кадра.
     ЦЕНА: владелец открыл деку и сказал «структура обложки неправильная… линия
     доходит не доверху, и зелёная линия тоже не доходит доверху». Замер, которым
     это найдено: в окне 1440×900 слайд стоит y=46..854, а `#bleed` рисует ЧЕТЫРЕ
     полосы, и все беж.
     ⇒ Картинка дописывается наружу ТЕМ ЖЕ приёмом, что узор ниже, но с одним
     отличием, и оно существенно: растягивается ТОЛЬКО та ось, по которой есть
     поле. По второй оси отображение совпадает со слайдом пиксель в пиксель —
     иначе вертикальная линия и край панели уехали бы относительно кадра, и на
     границе поля появился бы шов. Дизайн обложки — вертикальные полосы, вдоль
     поля они постоянны, поэтому растяжение по этой оси невидимо и точно. */
  const polnokadrovyj = Array.from(slide.querySelectorAll('img')).find(im => {
    const q = im.getBoundingClientRect();
    return q.left <= r.left + eps && q.top <= r.top + eps &&
           q.right >= r.right - eps && q.bottom >= r.bottom - eps &&
           parseFloat(getComputedStyle(im).opacity) > .98;
  });
  if (polnokadrovyj) {
    const rastyagX = padL > .5 || padR > .5, rastyagY = padT > .5 || padB > .5;
    const d = document.createElement('div');
    d.style.cssText = 'position:absolute;inset:0;background-repeat:no-repeat' +
      ';background-image:url("' + polnokadrovyj.src + '")' +
      ';background-size:' + (rastyagX ? innerWidth : r.width) + 'px ' +
                            (rastyagY ? innerHeight : r.height) + 'px' +
      ';background-position:' + (rastyagX ? 0 : r.left) + 'px ' +
                                (rastyagY ? 0 : r.top) + 'px';
    bleedBands.appendChild(d);   /* ПОСЛЕ цветных полос — ложится поверх бежа */
  }

  /* Узор — растр: за собственным краем картинки ничего нет, продлить его нельзя.
     Поэтому он растягивается на всё ОКНО, а кадр показывает середину (переменные
     читает uzor.css). */
  slide.style.setProperty('--uzor-sz', (innerWidth / k) + 'px ' + (innerHeight / k) + 'px');
  slide.style.setProperty('--uzor-x', (-padL / k) + 'px');
  slide.style.setProperty('--uzor-y', (-padT / k) + 'px');
  /* УГОЛ, А НЕ ОБЩИЙ ФОН (заход polya-i-uzor, Э4). Старая проверка смотрела на
     computed background-image ВСЕГО .slide — верно только для служебных слайдов
     со сплошным фоном на корневом узле. Там, где угол закрывает изнутри
     непрозрачная ДОЧЕРНЯЯ зона (полоса иллюстрации, доска), .slide сам по себе
     остаётся с узором, и bleedUzor рисовал полосу СНАРУЖИ кадра поверх заведомо
     перекрытого изнутри угла — шов на границе кадра, а не на линии слайда.
     Проверяем сам угол: элемент в пикселе угла и цепочка предков до .slide
     включительно; непрозрачен кто-то из них — этому углу (и только ему) узор
     снаружи не рисуем. Два угла — две независимые переменные (uzor.css), не
     один общий display: у элемента #bleed-uzor один DOM-узел на оба слоя. */
  const cornerBlocked = (x, y) => {
    let el = document.elementFromPoint(x, y);
    // `.slide` несёт `background:var(--paper)` БЕЗУСЛОВНО — цвет непрозрачен
    // ВСЕГДА, у обычного слайда так же, как у служебного. Опаковость ЦВЕТА
    // на самом `.slide` ничего не различает; признак служебного слайда —
    // backgroundIMAGE==='none' (шорткод `background:var(--board)` в `tipy.py`
    // сбрасывает и его). 🔴 Проверка `el===slide` обязана идти ПЕРВОЙ, до
    // блокировки по картинке — та же логика порядка, что уже была здесь.
    const slideBlocked = () => getComputedStyle(slide).backgroundImage === 'none';
    // ПОДЛОЖКА vs ИЛЛЮСТРАЦИЯ (заход kadr-uzor-i-vmeshchenie, Э1). Было:
    // `isOpaque(getComputedStyle(el).backgroundColor)` на ЛЮБОМ предке — но
    // `.zone.board` (зелёная подложка, `tipy.py:91`) непрозрачна ПО ПОСТРОЕНИЮ,
    // и `_ill_zone` навешивает тот же класс `board` на полосу С картинкой
    // (`cls="board"`, `tipy.py:_ill_zone`) — то есть цвет одинаково опаковый и
    // там, где угла ничто не закрывает, и там, где под ним лежит иллюстрация.
    // Узор гас на КАЖДОМ слайде с зелёной зоной, с картинкой или без —
    // владелец увидел ровно это: «поверх зелёного он наносится, поверх
    // иллюстраций — нет» означает, что признак «непрозрачен» здесь неверный
    // сигнал вовсе, сама подложка ДОЛЖНА быть проходимой.
    // Настоящая иллюстрация физически рисуется НЕ через CSS-фон: `.panel`
    // (единственный контейнер картинки, `_ill_zone`) несёт `background:none`
    // (base.css:140), а `<img>/<svg>/<canvas>` внутри нет своего
    // background-color — значит `isOpaque(backgroundColor)` не увидел бы
    // иллюстрацию, даже если бы искал её специально. Верный признак —
    // принадлежность `.panel`: он один на все типы вёрстки (`_ill_zone` —
    // единственный источник панелей), не завязан на конкретный `tip_verstki`.
    const isIllustration = e => e.classList && e.classList.contains('panel');
    if (!el) return slideBlocked();
    while (el && el !== document.documentElement) {
      if (el === slide) return slideBlocked();
      if (isIllustration(el)) return true;
      el = el.parentElement;
    }
    return false;
  };
  const setCorner = (name, blocked) => {
    if (blocked) bleedUzor.style.setProperty(name, 'none');
    else bleedUzor.style.removeProperty(name);
  };
  /* 🔴 ВТОРАЯ ПОЛОВИНА ТОГО ЖЕ ДЕФЕКТА — И ОНА ОТ ТОЙ ЖЕ СЛЕПОТЫ К КАРТИНКЕ.
     `cornerBlocked` доходит до `.slide` и решает по `slideBlocked()` —
     «backgroundImage у слайда === none». У слайда с полнокадровым растром это
     ЛОЖЬ: узор из `uzor.css` висит на `.slide` у ВСЕХ слайдов, значит угол не
     считался закрытым никогда. Внутри кадра узор всё равно не виден — его
     закрывает непрозрачная картинка, — а СНАРУЖИ, в поле, он рисовался. Ровно
     «полурисуемый узор», который владелец назвал худшим из трёх исходов:
     «если наносить сюда паттерн, он должен не перекрываться ничем, полностью
     рисоваться; его можно вообще убрать, но если оставлять — то целиком».
     ⇒ Полнокадровый растр закрывает ОБА угла по построению: узор снаружи не
     рисуется вовсе. Из трёх исходов это второй законный — «не рисуется». */
  setCorner('--uzor-tr-corner', !!polnokadrovyj || cornerBlocked(r.right - eps, r.top + eps));
  setCorner('--uzor-bl-corner', !!polnokadrovyj || cornerBlocked(r.left + eps, r.bottom - eps));
}
function showSingle(i, k) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  scene = k === undefined ? 1 : k;
  slides.forEach((s, j) => {
    const active = j === cur;
    s.style.display = active ? '' : 'none';
    /* активному слайду возвращённая сцена ПРИСВАИВАЕТСЯ: иначе `scene` держит
       непроверенное число из хэша (#s2.99), DOM показывает зажатую сцену, а
       syncHash пишет в адрес ту, которой на экране нет. */
    const eff = applyScene(s, active ? scene : scenesOf(s));   // park hidden at final
    if (active) scene = eff;
    s.querySelectorAll('video').forEach(v => {
      if (active) { v.currentTime = 0; const p = v.play(); p && p.catch(() => {}); }
      else v.pause();
    });
  });
  const s = slides[cur];
  fitAll(s);
  scaleSlide(s);
  paintBleed(s);
  updateProgress();
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
  bleedOff();                       /* в обзоре кадра нет — дописывать нечего */
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
  bleedOff();                       /* экспорт — ровно кадр W×H, без полей */
  document.getElementById('hint').style.display = 'none';
  lectZone.style.display = 'none'; lectProgress.style.display = 'none';
  lectNumber.style.display = 'none';
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
