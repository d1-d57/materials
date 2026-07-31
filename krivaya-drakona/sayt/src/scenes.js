/* ═══════════════════════════════════════════════════════════════════════════
   scenes.js — восемь сцен. Вся геометрия берётся из dragon.js и только оттуда.

   Рендер двумя способами, каждый там, где он верен:
     · SVG   — сцены с наведением мыши и до 128 звеньев (1, 2, 3, 5а–5г, 6).
               Так написан весь L4, и roundPath переносится как есть.
     · canvas — тяжёлые сцены (0: ранг 14; 4: до ранга 14; 7: заливка и зум).
               Так написан референс.
   Третьего способа нет, геометрия у обоих одна.
   ═══════════════════════════════════════════════════════════════════════════ */
'use strict';

/* ─────────────────────────── общая кухня ─────────────────────────── */

const NS = 'http://www.w3.org/2000/svg';

/* ⚠ ГРАФИЧЕСКИЕ СВОЙСТВА КЛАДУТСЯ В style, А НЕ В АТРИБУТ, И ЭТО НЕ ВКУСОВЩИНА.
   Презентационный атрибут SVG проигрывает ЛЮБОМУ правилу CSS, поэтому
   `stroke-width: 2` в классе .d-acc молча съедал ВСЕ толщины, посчитанные в
   коде: ширину бумажной ленты, утолщение подсвеченного звена, хайрлайн ранга 10.
   Атрибут в разметке стоял, код «выглядел правильно» — а getComputedStyle
   возвращал 2px при атрибуте 33.18. Поймано измерением, не чтением. */
const STYLED = {'stroke-width':1, 'stroke':1, 'fill':1, 'opacity':1,
                'stroke-dasharray':1, 'stroke-linecap':1, 'stroke-linejoin':1};
function mk(name, attrs, parent){
  const e = document.createElementNS(NS, name);
  if(attrs){
    /* ⚠ `style` — ПЕРВЫМ. setAttribute('style', …) переписывает объявление
       целиком и стирает всё, что уже положено через style.setProperty. Порядок
       наоборот стоил зон наведения сцены 5а: `{fill:'transparent',
       style:'cursor:pointer'}` терял fill, круг радиусом 17 получал fill по
       умолчанию (чёрный) и накрывал вершину чёрной кляксой. */
    if(attrs.style) e.setAttribute('style', attrs.style);
    for(const k in attrs){
      if(k==='style') continue;
      if(STYLED[k]) e.style.setProperty(k, String(attrs[k]));
      else e.setAttribute(k, attrs[k]);
    }
  }
  if(parent) parent.appendChild(e);
  return e;
}
function wipe(n){ while(n && n.firstChild) n.removeChild(n.firstChild); }

function cssVar(name){
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

/** все углы сразу — для разгибания полоски одним ползунком */
function angs(v, n){ const o={}; for(let p=1;p<=n;p++) o[p]=v; return o; }

/* ⚠ СКРУГЛЕНИЕ — ЭТО НАСТРОЙКА СЦЕНЫ, А НЕ ГЛОБАЛЬНАЯ КРАСОТА.
   Первая версия ставила 0.42–0.5 везде, и это провалилось на глазах: при
   скруглении в пол-звена прямых участков не остаётся вовсе, ломаная читается
   как гладкая волна — а сцена №5а утверждает «первое звено горизонтальное,
   второе вертикальное». Утверждение стало невидимым, то есть сцена перестала
   доказывать то, ради чего она есть. Это ровно решение владельца, записанное
   в L4:176 — «по умолчанию ПРЯМЫЕ, круглые только когда нужно показать, что
   самопересечений нет». Поэтому крупное скругление осталось ровно там, где
   оно и есть предмет: сцена №4 (две дуги вместо перекрёстка). */
const ROUND = {
  strip: 0.16, halves: 0.16, vert: 0.15,
  dense: 0.50,                       // предмет сцены: в касании читаются две дуги
  /* Скругления на картинках доказательства подняты (владелец, 31.07): при 0,13–0,24
     угол на СТЫКЕ двух соседних уголков читался как перекрёсток, и кривая выглядела
     самопересекающейся — ровно то, что сцена опровергает. Ниже 0,5 держим намеренно:
     при большем скруглении перестаёт быть видно, какое звено вдоль, а какое поперёк. */
  a: 0.30, b: 0.32, v: 0.32, g: 0.32,
  four: 0.20
};

/** решётка внутри рамки: только там, где она помогает читать клетки */
function lattice(par, g, box, pad){
  const p = pad===undefined ? 1 : pad;
  for(let x=Math.floor(box.x0)-p; x<=Math.ceil(box.x1)+p; x++){
    const a=g([x,box.y0-p]), b=g([x,box.y1+p]);
    mk('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],class:'d-grid'},par);
  }
  for(let y=Math.floor(box.y0)-p; y<=Math.ceil(box.y1)+p; y++){
    const a=g([box.x0-p,y]), b=g([box.x1+p,y]);
    mk('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],class:'d-grid'},par);
  }
}

/** Полосы через одну: строка крашеная ⟺ её номер чётный.
    ⚠ Полосы кладутся ТОЛЬКО по охвату кривой (плюс полклетки), а не на всю
    ширину холста. Первая версия тянула их от края до края и на всю высоту
    рамки: получались шесть широких коричневых баров, которые перекрикивали
    саму кривую, и на скриншоте сцена читалась как полосатый фон с еле
    заметной линией. Полоса — это разметка решётки под фигурой, а не фон. */
function rowBands(par, g, box, pad){
  const p = pad===undefined ? 0 : pad;
  const x0=g([box.x0-p-0.6, 0])[0], x1=g([box.x1+p+0.6, 0])[0];
  for(let y=Math.floor(box.y0)-p; y<=Math.ceil(box.y1)+p; y++){
    if(!rowBlue(y)) continue;
    const top=g([0,y+0.5])[1], bot=g([0,y-0.5])[1];
    mk('rect',{x:Math.min(x0,x1), y:Math.min(top,bot),
               width:Math.abs(x1-x0), height:Math.abs(bot-top), class:'d-row'},par);
  }
}

/** ШАХМАТНАЯ РАСКРАСКА ВСЕЙ РЕШЁТКИ, а не только вершин кривой.
    Правка владельца: пока красились одни вершины, через которые прошла кривая,
    чередование читалось как свойство картинки. Плоскость покрыта шахматной
    раскраской независимо от кривой — и уже потом видно, что кривая ходит по ней
    определённым образом. Узлы решётки идут тише вершин кривой (opacity),
    иначе разметка перекрикивает предмет — тот же урок, что у полос .d-row. */
function latticeNodes(par, g, box, pad){
  const p = pad===undefined ? 0 : pad;
  for(let x=Math.floor(box.x0)-p; x<=Math.ceil(box.x1)+p; x++)
    for(let y=Math.floor(box.y0)-p; y<=Math.ceil(box.y1)+p; y++){
      const el=node(par, g([x,y]), isBlack([x,y]) ? 'd-node-b':'d-node', 3);
      el.style.setProperty('opacity','0.38');
    }
}

/** стрелка хода в середине звена — без неё «налево» не имеет смысла.
    ⚠ РАЗМЕР — ПАРАМЕТР, И ЭТО НЕ ВКУСОВЩИНА. Потолок 7 единиц viewBox (при
    холсте 1000×1000 это 3,5 пикселя на экране) владелец увидел как «непонятно,
    в какую сторону мы идём», и из-за этого терялось, где «направо», а где
    «налево» — то есть само правило строк. Крупная стрелка — требование
    читаемости с проектора, а не украшение. */
function arrowOn(par, p, q, cls, size){
  const mx=(p[0]+q[0])/2, my=(p[1]+q[1])/2;
  const l=Math.hypot(q[0]-p[0], q[1]-p[1]) || 1;
  const ux=(q[0]-p[0])/l, uy=(q[1]-p[1])/l, nx=-uy, ny=ux;
  /* ⚠ ПОТОЛОК ОТ ДЛИНЫ ЗВЕНА — 0,28, А НЕ 0,44. Наконечник длиной 1,6·t, и при
     0,44 он накрывал звено ЦЕЛИКОМ: на снимке подсвеченное ребро исчезало под
     своей же стрелкой, то есть шаг «по одному ребру» показывал стрелку вместо
     ребра. Поймано снимком, не чтением. */
  const t=Math.min(size===undefined?7:size, l*0.28), b=t*0.66;
  mk('polygon',{class:cls||'d-arrow', points:
    (mx+ux*t)+','+(my+uy*t)+' '+
    (mx-ux*t*0.6+nx*b)+','+(my-uy*t*0.6+ny*b)+' '+
    (mx-ux*t*0.6-nx*b)+','+(my-uy*t*0.6-ny*b)},par);
}

/** число по-русски: запятая, а не точка. В тексте сцены 7 уже стоит «1,5236»,
    и точка в строке состояния рядом читается как другое число. */
function num(x, d){ return x.toFixed(d).replace('.', ','); }

/** площадь: целое печатаем целым. «площадь 0,0 клеток» выглядит как измерение
    с точностью до десятой там, где ответ ровно ноль. */
function area(x){
  return Math.abs(x-Math.round(x))<1e-9 ? String(Math.round(x)) : num(x,1);
}

function node(par, p, cls, r){
  return mk('circle',{cx:p[0],cy:p[1],r:r||5,class:cls||'d-node'},par);
}

/** Наведение — мышью И КАСАНИЕМ. На телефоне mouseenter не приходит вообще,
    и сцены 5а–5г, у которых весь интерактив на наведении, оказывались
    мёртвыми: разметка адаптировалась, а работать было нечем. */
function onHover(el, fn){
  el.addEventListener('mouseenter', fn);
  el.addEventListener('touchstart', e=>{ fn(e); }, {passive:true});
  el.addEventListener('pointerdown', e=>{ if(e.pointerType!=='mouse') fn(e); });
}

/** canvas с ограничением devicePixelRatio двойкой */
function setupCanvas(cv){
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const r = cv.getBoundingClientRect();
  const w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
  cv.width = Math.round(w*dpr); cv.height = Math.round(h*dpr);
  const ctx = cv.getContext('2d');
  ctx.setTransform(1,0,0,1,0,0); ctx.scale(dpr,dpr);
  return { ctx, w, h };
}

/** ресайз с debounce — один обработчик на сцену */
function onResize(fn, ms){
  let t=null;
  const h=()=>{ clearTimeout(t); t=setTimeout(fn, ms||200); };
  window.addEventListener('resize', h);
  return h;
}

/** ЛИСТАЛКА — ОДНА НА ВЕСЬ САЙТ, второй не пишем: её держат и четыре шага
    доказательства, и две карточки способов рисования. Стрелки ← → и точки, плюс
    регистрация в PAGERS, чтобы клавиатура нашла листалку текущей сцены. */
function pagerOf(sec, onShow, count){
  const dots=[...sec.querySelectorAll('.pager__dot')];
  const n=count || dots.length;
  let cur=0;
  function show(i){
    cur=Math.min(n-1, Math.max(0, i));
    dots.forEach((d,k)=>d.classList.toggle('on', k===cur));
    onShow(cur);
  }
  sec.querySelectorAll('[data-page]').forEach(b=>
    b.addEventListener('click', ()=>show(cur + (+b.dataset.page))));
  dots.forEach((d,k)=>d.addEventListener('click', ()=>show(k)));
  PAGERS.set(sec, { go(d){ show(cur+d); } });
  return { show, cur:()=>cur };
}

/* ═══════════════════════ 0 · ОБЛОЖКА ═══════════════════════
   Дракон высокого ранга рождается из точки и вырастает целиком: прогрессивная
   отрисовка батчами по requestAnimationFrame, а не готовый кадр. Растворение
   в фоне — маской из референса (.cover__canvas). */

function sceneCover(sec){
  const cv = sec.querySelector('canvas');
  const N = 14;
  const P = rank(N);
  let ctx, W, H, g, raf=null, drawn=0;

  function layout(){
    const c = setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
    g = fit(P, {x:0,y:0,w:W,h:H,pad:Math.min(W,H)*0.06});
    drawn = 0;
  }
  function paint(all){
    const acc = cssVar('--acc');
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle = acc; ctx.lineWidth = 0.72; ctx.lineJoin='round'; ctx.lineCap='round';
    const upto = all ? P.length-1 : drawn;
    if(upto<1) return;
    ctx.beginPath();
    let s=g(P[0]); ctx.moveTo(s[0],s[1]);
    for(let i=1;i<=upto;i++){ const p=g(P[i]); ctx.lineTo(p[0],p[1]); }
    ctx.stroke();
  }
  function grow(){
    if(raf) cancelAnimationFrame(raf);
    if(REDUCED){ drawn=P.length-1; paint(true); return; }
    drawn = 0;
    const BATCH = Math.max(60, Math.round((P.length-1)/150));
    const step = ()=>{
      drawn = Math.min(P.length-1, drawn+BATCH);
      paint(false);
      if(drawn < P.length-1) raf = requestAnimationFrame(step); else raf=null;
    };
    raf = requestAnimationFrame(step);
  }
  onResize(()=>{ layout(); paint(true); });
  return {
    enter(){ layout(); grow(); },
    leave(){ if(raf){ cancelAnimationFrame(raf); raf=null; } }
  };
}

/* ═══════════════════════ 1 · СГИБАЕМ ПОЛОСКУ ═══════════════════════
   Основа — T17 (L4:671–714). Полоска и ломаная — ОДНА линия при угле 0° и 90°,
   а не два рисунка: этим и показано, что форму задали сгибы.

   Сцена идёт в два такта.

   ТАКТ 1, ВЪЕЗД — модель происходящего на одной полоске ранга 3 (почему именно
   третьего — у объявления IN ниже). Складывание честное, «по поколениям сгибов»,
   а не общим углом: сгиб номер p рождается на складывании birthStep(3,p) =
   3 − v2(p) (dragon.js), поэтому «сложить пополам» — это довести до упора ровно
   сгибы ОДНОГО поколения, а остальные оставить там, где стояли. Общий угол
   этого не выражает: он сгибает всё сразу, и «пополам, ещё раз, ещё» не читается.
   ⚠ УПОР — FOLD_MAX = 152°, А НЕ 180°. При 180° слои совпадают ТОЧНО, и пачка
   бумаги рисуется как один отрезок: складывания не видно вообще. При 152° видны
   кромки слоёв, то есть видно, что слоёв стало вдвое больше.
   ⚠ МАСШТАБ НА ВРЕМЯ СКЛАДЫВАНИЯ ФИКСИРОВАН масштабом прямой полоски. Кадровый
   fit() тут неверен принципиально: он подгонял бы пачку под рамку, полоска
   держала бы длину — и вышло бы, что бумага при складывании не укорачивается.
   Камера переезжает на масштаб кривой только на последнем движении, когда сгибы
   раскрываются до прямого угла.

   ТАКТ 2, ПОКОЙ — десять рангов разом, 1…10, и ОДИН ползунок на все десять.
   Каждый ранг живёт в своей клетке и подогнан по ней кадровым fit(): рамка
   зависит от углов непрерывно, поэтому кадр не прыгает, а каждая фигура
   остаётся крупной и на прямой полоске, и на готовой кривой. Сверху на fit()
   надет общий потолок масштаба — почему, у объявления CAP_AT. */

function sceneStrip(sec){
  const svg = sec.querySelector('svg');
  const W=1000, H=1000, PAD=26;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const inAngle = sec.querySelector('[data-in="angle"]');
  let a=+inAngle.value;

  /* Десять клеток: строки 4 · 3 · 3. Строка становится шире по ходу роста —
     старшим рангам, где важна частота, достаётся больше места, и квадрат
     заполняется ровно, без дыры в углу (первая раскладка 4·4·2 оставляла
     полпустой строки — видно на скриншоте). */
  const RANKS=[1,2,3,4,5,6,7,8,9,10];
  const WORDS=RANKS.map(n=>word(n));
  const ROWS=[4,3,3];
  const CELL=(function(){
    const out=[]; const ch=H/ROWS.length; let i=0;
    ROWS.forEach((cols,row)=>{
      const cw=W/cols;
      for(let c=0;c<cols;c++, i++) out.push({x:c*cw, y:row*ch, w:cw, h:ch});
    });
    return out;
  })();

  /* ⚠ ВЪЕЗДНАЯ ПОЛОСКА — РАНГ 3, И ЭТО НЕ ЛЕНЬ. На ранге 5 складывание честно
     укорачивает бумагу вдвое пять раз, то есть до 1/32 кадра, — и на скриншоте
     третий, четвёртый и пятый сгибы оказались нечитаемой закорючкой в три
     пикселя: анимация показывала не «сложили», а «исчезло». Три складывания —
     ровно то, что говорит текст сцены («пополам. Ещё раз. Ещё»), и пачка
     остаётся 1/8 кадра, то есть видимой. */
  const IN=3, IW=word(IN);
  const FOLD_MAX=152;         // упор сгиба: при 180° слои совпадают и складывания не видно
  const S_FLAT=(W-2*PAD)/Math.pow(2,IN);                // масштаб прямой полоски
  const S_CURVE=(function(){
    const b=bounds(poly(IW));
    return Math.min((W-2*PAD)/(b.x1-b.x0), (H-2*PAD)/(b.y1-b.y0));
  })();

  /** ширина бумажной ленты: полоса при малом угле, тонкая линия у кривой */
  function bandOf(s, ang){
    const k = Math.min(1, Math.max(0, ang/90));
    return Math.max(1, Math.min(s*lerp(0.34,0.15,k), lerp(9,2.6,k)));
  }

  /** одна полоска: центр bbox — в центре бокса, масштаб и ширина заданы извне */
  function paintStrip(par, o, s, box, bw){
    const P=polyAngles(IW,o), b=bounds(P);
    const cx=(b.x0+b.x1)/2, cy=(b.y0+b.y1)/2;
    const g=p=>[box.x+box.w/2+(p[0]-cx)*s, box.y+box.h/2-(p[1]-cy)*s];
    const S=P.map(g);
    mk('path',{d: roundPath(S,ROUND.strip), class:'d-acc','stroke-width':bw,
               'stroke-linecap':'butt','stroke-linejoin':'round'},par);
    node(par, S[0], 'd-node-a', Math.max(1.6, Math.min(5, s*0.05)));
  }

  /** уложить ломаную в клетку, но не крупнее заданного потолка масштаба */
  function place(P, box, pad, sMax){
    const g=fit(P,{x:box.x,y:box.y,w:box.w,h:box.h,pad:pad});
    if(!(sMax>0) || g.s<=sMax) return g;
    const b=g.box, cx=(b.x0+b.x1)/2, cy=(b.y0+b.y1)/2;
    const f=p=>[box.x+box.w/2+(p[0]-cx)*sMax, box.y+box.h/2-(p[1]-cy)*sMax];
    f.s=sMax; f.box=b; return f;
  }

  /* ⚠ ОБЩИЙ ПОТОЛОК МАСШТАБА, И ОН НЕ КОСМЕТИКА. Кадровый fit() по своей клетке
     раздувал ранг 1 — две палочки — до размеров ранга 10: десять фигур одного
     размера читались как десять случайных загогулин, а не как одна кривая,
     которая растёт (поймано скриншотом, не рассуждением). Потолок берётся с
     ранга 4 и дальше не меняется: ранги 1–3 выходят мелкими, то есть ровно
     такими, какие они и есть, а с четвёртого размер держится, и растёт одна
     только частота — это и есть то, что сцена показывает. */
  const CAP_AT=3;                                       // индекс ранга 4
  const CELL_PAD=18;

  /** потолок масштаба при текущем угле */
  function capScale(ang){
    const P=polyAngles(WORDS[CAP_AT], angs(ang, WORDS[CAP_AT].length));
    return fit(P,{x:0,y:0,w:CELL[CAP_AT].w,h:CELL[CAP_AT].h,pad:CELL_PAD}).s;
  }

  /** десять рангов разом; skip — клетка, которую рисует не сетка (перелёт) */
  function paintGrid(par, skip){
    const sMax=capScale(a);
    RANKS.forEach((n,i)=>{
      if(i===skip) return;
      const P=polyAngles(WORDS[i], angs(a, WORDS[i].length));
      const g=place(P, CELL[i], CELL_PAD, sMax);
      const S=P.map(g);
      mk('path',{d: a<45 ? sharpD(S) : roundPath(S,ROUND.strip),
                 class:'d-acc','stroke-width':bandOf(g.s,a),
                 'stroke-linecap':'butt','stroke-linejoin':'round'},par);
      node(par, S[0], 'd-node-a', Math.max(1.6, Math.min(3, g.s*0.16)));
    });
  }

  function draw(){
    wipe(svg);
    paintGrid(svg);
  }

  const FULL={x:0,y:0,w:W,h:H};
  /* Ширина бумажной ленты — 0,28 клетки, то есть примерно 1:28 к длине полоски.
     Первая версия ставила потолок в 14 единиц viewBox: на экране это 9 пикселей
     на 600, полоска читалась как ЛИНИЯ, и «сложить бумагу» не читалось вовсе. */
  const PAPER=S_FLAT*0.28;

  let tok={v:0};
  async function intro(){
    tok.v++; const my=tok;
    const o={}; for(let p=1;p<=IW.length;p++) o[p]=0;
    wipe(svg); paintStrip(svg,o,S_FLAT,FULL,PAPER);
    if(!await pause(520,my)) return;

    // СЛОЖИТЬ ПОПОЛАМ, ЕЩЁ РАЗ, ЕЩЁ: за раз доезжают до упора сгибы ОДНОГО
    // поколения (birthStep), масштаб держится — бумага честно укорачивается вдвое
    for(let k=1;k<=IN;k++){
      const born=[]; for(let p=1;p<=IW.length;p++) if(birthStep(IN,p)===k) born.push(p);
      if(!await anim(0,FOLD_MAX,520,v=>{ born.forEach(p=>o[p]=v);
        wipe(svg); paintStrip(svg,o,S_FLAT,FULL,PAPER); },my)) return;
      if(!await pause(230,my)) return;
    }
    if(!await pause(380,my)) return;

    // РАЗВЕРНУТЬ: сгибы раскрываются до прямого угла, камера едет за фигурой
    if(!await anim(0,1,1700,u=>{
      const ang=lerp(FOLD_MAX,90,u);
      for(let p=1;p<=IW.length;p++) o[p]=ang;
      wipe(svg); paintStrip(svg,o,lerp(S_FLAT,S_CURVE,u),FULL,
                            lerp(PAPER, bandOf(S_CURVE,90), u));
    },my)) return;
    if(!await pause(620,my)) return;

    /* ПЕРЕДАЧА ТАКТА. Не перекрёстное затухание, а перелёт: кривая уезжает в
       свою клетку сетки (ранг 3 — третья из десяти), и ровно на месте её
       догоняют остальные девять. Кросс-фейд из полного кадра в сетку читался
       как две картинки поверх друг друга; перелёт говорит «вот эта самая
       кривая — одна из десяти». */
    const sCell=Math.min(capScale(90), place(poly(IW),CELL[IN-1],CELL_PAD,0).s);
    if(!await anim(0,1,900,u=>{
      for(let p=1;p<=IW.length;p++) o[p]=90;
      wipe(svg);
      const gG=mk('g',{opacity:u.toFixed(3)},svg); paintGrid(gG, IN-1);
      paintStrip(svg, o, lerp(S_CURVE,sCell,u), {
        x:lerp(FULL.x,CELL[IN-1].x,u), y:lerp(FULL.y,CELL[IN-1].y,u),
        w:lerp(FULL.w,CELL[IN-1].w,u), h:lerp(FULL.h,CELL[IN-1].h,u)},
        lerp(bandOf(S_CURVE,90), bandOf(sCell,90), u));
    },my)) return;
    a=90; inAngle.value=90; draw();
  }

  inAngle.addEventListener('input', ()=>{
    tok.v++;                                            // ползунок обрывает въездной такт
    a=+inAngle.value; draw();
  });
  onResize(draw);

  return {
    enter(){ if(REDUCED){ draw(); return; } intro(); },
    leave(){ tok.v++; }
  };
}

/* ═══════════════════════ 2 · ДВЕ ОДИНАКОВЫЕ ПОЛОВИНЫ ═══════════════════════
   Основа — T4 (359–413) и T8 (511–542). Способ рисования ОДИН на все фазы:
   лента сужается (w→0), а не подменяется линией (дефект, пойман 17.07).
   Наведение на половину показывает вторую И её происхождение: копия первой,
   повёрнутая на 90° вокруг стыка (проверенное правило T8). */

function sceneHalves(sec){
  const svg = sec.querySelector('[data-card="halves"] svg');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const N=5, MID=Math.pow(2,N-1);                       // стык — середина ломаной
  const w = word(N);
  const FINAL = poly(w);
  /* ⚠ РАМКА СЧИТАЕТСЯ КАЖДЫЙ КАДР как «текущее положение + итог» — ровно так,
     как в T4 (L4:379-381). Фиксированная рамка по объединению с РАЗОГНУТОЙ
     полоской провалилась на глазах: прямая полоска ранга 5 длиной 32 клетки
     задавала масштаб на все кадры, и готовая кривая (около 6 клеток) выходила
     красным пятном в тридцать пикселей. Объединение «текущая + итоговая»
     непрерывно по углам, всегда вмещает обе, и камера едет ровно так, как
     укорачивается лента. */
  const btn = sec.querySelector('[data-act="play"]');
  let ang=90, band=0, hover=0, tok={v:0}, ring=true;

  function draw(){
    wipe(svg);
    const P = polyAngles(w, angs(ang, w.length));
    const g = fit(P.concat(FINAL), {x:0,y:0,w:W,h:H,pad:80});
    const S = P.map(g);
    const A = S.slice(0, MID+1), B = S.slice(MID);
    const bw = band>0 ? Math.max(3, g.s*0.30*band) : 0;
    const dA = ang<45 ? sharpD(A) : roundPath(A,ROUND.halves);
    const dB = ang<45 ? sharpD(B) : roundPath(B,ROUND.halves);

    if(bw>3.2){                                         // лента: бумага, вид сверху
      mk('path',{d:dB,class:'d-rib','stroke-width':bw},svg);
      mk('path',{d:dA,class:'d-rib-a','stroke-width':bw},svg);
    }
    // призрак: первая половина, повёрнутая на 90° вокруг стыка, ложится на вторую
    if(hover && ang>=88){
      const src = hover===1 ? P.slice(0,MID+1) : P.slice(MID);
      const rot = rotAbout(src, P[MID], hover===1 ? -90 : 90).map(g);
      mk('path',{d:roundPath(rot,ROUND.halves), class:'d-ghost','stroke-width':5},svg);
    }
    mk('path',{d:dB, class:hover===2?'d-hot':'d-line', 'stroke-width':hover===2?5:2.6},svg);
    mk('path',{d:dA, class:'d-acc', 'stroke-width':hover===1?5:2.6},svg);

    if(ang>=88){                                        // зоны наведения на половины
      const hitA = mk('path',{d:dA,class:'d-hit'},svg);
      const hitB = mk('path',{d:dB,class:'d-hit'},svg);
      const set=v=>{ hover=v; draw(); };
      onHover(hitA, ()=>set(1));
      onHover(hitB, ()=>set(2));
      hitA.addEventListener('mouseleave',()=>set(0));
      hitB.addEventListener('mouseleave',()=>set(0));
    }
    node(svg, S[0], 'd-node-a', 5);
    if(ring) mk('circle',{cx:S[MID][0],cy:S[MID][1],r:13,class:'d-dim','stroke-width':1.6},svg);
  }

  /* Складывание идёт по сгибам РАЗНОГО ВОЗРАСТА (birthStep), поэтому углы
     держим картой: сгиб, родившийся на шаге k, доезжает до 168° на шаге k,
     а остальные стоят там, где стояли. Один общий угол этого не выражает. */
  function drawAt(o){
    wipe(svg);
    const P = polyAngles(w, o);
    const g = fit(P.concat(FINAL), {x:0,y:0,w:W,h:H,pad:80});
    const S = P.map(g);
    const A = S.slice(0, MID+1), B = S.slice(MID);
    const bw = Math.max(2.6, g.s*0.30*band);
    mk('path',{d:sharpD(B),class:'d-rib','stroke-width':bw},svg);
    mk('path',{d:sharpD(A),class:'d-rib-a','stroke-width':bw},svg);
    node(svg, S[0], 'd-node-a', 5);
  }

  async function playSeq(){
    tok.v++; const my=tok;
    if(REDUCED){ ang=90; band=0; ring=true; hover=0; draw(); return; }
    hover=0; ring=false; band=1;
    const o={}; for(let p=1;p<=w.length;p++) o[p]=0;
    drawAt(o);
    if(!await pause(380, my)) return;
    if(!await anim(1, 0.16, 1000, v=>{ band=v; drawAt(o); }, my)) return;
    for(let k=1;k<=N;k++){
      const born=[]; for(let p=1;p<=w.length;p++) if(birthStep(N,p)===k) born.push(p);
      if(!await anim(0, 168, 430, v=>{ born.forEach(p=>o[p]=v); drawAt(o); }, my)) return;
      if(!await pause(140, my)) return;
    }
    if(!await pause(340, my)) return;
    if(!await anim(168, 90, 1800, v=>{
        for(let p=1;p<=w.length;p++) o[p]=v; drawAt(o); }, my)) return;
    ang=90; band=0; ring=true; hover=0; draw();
  }

  btn.addEventListener('click', playSeq);
  onResize(()=>{ if(ang>=88) draw(); });
  return { enter(){ playSeq(); }, leave(){ tok.v++; } };
}

/* ═══════════════════════ 2б · ВТОРОЙ СПОСОБ: ПО ВЕРШИНАМ ═══════════════════════
   ⚠ КАРТИНКА ВЗЯТА ГОТОВОЙ — ЭТО РЕШЕНИЕ ВЛАДЕЛЬЦА, А НЕ ЭКОНОМИЯ. Дословно:
   «вот этот рисунок — буквально то, что нужно показать на сцене со вторым
   способом; это красиво, а там непонятно ничего». Рисунок — прежний шаг
   доказательства «вершины двух сортов» в увеличенном виде: кривая, а поверх неё
   пунктиром диагонали через одну вершину, и пунктир — это кривая рангом ниже.
   Прежняя карточка вместо этого крутила три кривые с пересчётом рамки, и второй
   способ владелец не понимал.

   ОДНА КАРТИНКА, ЧИТАЕМАЯ В ДВЕ СТОРОНЫ, и это буквально требование правки:
     · «через одну»    — кривая ранга N гаснет, пунктир загорается: РАНГ МЛАДШЕ;
     · «треугольники»  — та же пара, прочитанная наоборот: пунктир становится
       основанием, и на каждой диагонали вырастает треугольник, вершина которого
       и есть новая вершина ранга N. При u=1 картинка совпадает с рангом N ТОЧНО.

   ⚠ ОБЕ КРИВЫЕ ДЕЛЯТ ОДНИ И ТЕ ЖЕ ВЕРШИНЫ, И ЭТО НЕ ПОДГОНКА. Вершины ранга N
   с чётными номерами — это в точности вершины ранга N−1, умноженные на (1+i)
   (mul1pi, проверено гейтом ядра до ранга 14): растяжение в √2 и поворот на 45°.
   Поэтому «через одну» ничего не пересчитывает — это ПОДМНОЖЕСТВО вершин,
   а треугольники достраиваются ровно до пропущенных.
   Рамка считается по кривой ранга N и держится на всех кадрах: LOW ⊂ BASE,
   поэтому одна рамка вмещает обе и камера не прыгает. */

function sceneVert(sec){
  const svg = sec.querySelector('[data-card="vert"] svg');
  const seg = sec.querySelector('[data-seg="vert"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);

  /* Ранг 6, а не 8: на 8 диагоналей 128, пунктир сливается в серую вату и
     «соединили вершины через одну» разглядеть нельзя. На 6 дракон узнаётся,
     а каждая диагональ ещё видна отдельно — а её видимость и есть предмет. */
  const N=6;
  const BASE = rank(N);
  const LOW  = BASE.filter((_,i)=>i%2===0);        // вершины через одну = ранг N−1
  const FRAME = bounds(BASE);
  const PAD = 62;

  let st=0, u=1, m=0, tok={v:0};

  function geom(){ return fit(BASE,{x:0,y:0,w:W,h:H,pad:PAD},FRAME); }

  /** треугольники на ДИАГОНАЛЯХ: при u=0 они лежат в диагонали, при u=1 их
      вершины — это пропущенные (новые) вершины ранга N */
  function triPath(g, u){
    let d='';
    for(let k=0;k+1<LOW.length;k++){
      const a=LOW[k], b=LOW[k+1], apex=BASE[2*k+1];
      const mid=[(a[0]+b[0])/2, (a[1]+b[1])/2];
      const t=[lerp(mid[0],apex[0],u), lerp(mid[1],apex[1],u)];
      const A=g(a), T=g(t), B=g(b);
      d += ' M '+A[0].toFixed(2)+' '+A[1].toFixed(2)
         + ' L '+T[0].toFixed(2)+' '+T[1].toFixed(2)
         + ' L '+B[0].toFixed(2)+' '+B[1].toFixed(2);
    }
    return d.trim();
  }

  /** вершины двух сортов: через одну закрашенные (они же концы диагоналей),
      между ними пустые — те, что «через одну» пропускает */
  function sorts(g, rb, rw){
    for(let i=1;i<BASE.length-1;i+=2) node(svg,g(BASE[i]),'d-node',rw);
    for(let i=0;i<BASE.length;i+=2)   node(svg,g(BASE[i]),'d-node-b',rb);
  }

  function draw(){
    wipe(svg);
    const g=geom();
    const S=BASE.map(g), L=LOW.map(g);

    if(st===0){                     // ПОКОЙ: кривая + пунктир через одну вершину
      mk('path',{d:roundPath(L,0.18),class:'d-dash','stroke-width':2.2},svg);
      mk('path',{d:roundPath(S,ROUND.vert),class:'d-acc','stroke-width':3},svg);
      sorts(g,4.6,4);
      return;
    }

    if(st<0){
      // исходная гаснет, пунктир достраивается в кривую ранга младше на глазах
      mk('path',{d:roundPath(S,ROUND.vert),class:'d-mute','stroke-width':2,
                 opacity:0.28},svg);
      for(let i=1;i<S.length-1;i+=2) node(svg,S[i],'d-node',3.4);
      const upto=Math.max(1, Math.min(L.length-1, m));
      mk('path',{d:roundPath(L.slice(0,upto+1),0.18),class:'d-acc',
                 'stroke-width':4.6},svg);
      for(let i=0;i<=upto;i++) node(svg,L[i],'d-node-a',4.6);
      return;
    }

    // та же картинка наоборот: диагонали — основание, треугольники растут
    mk('path',{d:roundPath(L,0.18),class:'d-line','stroke-width':2.6,
               opacity:0.5},svg);
    mk('path',{d:triPath(g,u),class:'d-acc','stroke-width':3.4,
               'stroke-linejoin':'round'},svg);
    for(let i=0;i<L.length;i++) node(svg,L[i],'d-node-b',4.6);
    if(u>0.15) for(let i=1;i<BASE.length-1;i+=2) node(svg,g(BASE[i]),'d-node',4);
  }

  /* Переход играется ОДИН раз и замирает на результате. Прогрессивная отрисовка
     кривой ранга младше — это и есть «соединяем вершины через одну»: рука идёт
     по вершинам на глазах, а не подменяет картинку готовой. */
  async function go(next){
    tok.v++; const my=tok;
    st=next;
    if(st===0){ u=1; m=LOW.length-1; draw(); return; }
    if(REDUCED){ u=1; m=LOW.length-1; draw(); return; }
    if(st<0){ m=0; draw();
      await anim(0, LOW.length-1, 1100, v=>{ m=Math.round(v); draw(); }, my);
      m=LOW.length-1; if(my.v===tok.v) draw();
      return;
    }
    u=0; draw();
    await anim(0, 1, 1000, v=>{ u=v; draw(); }, my);
    u=1; if(my.v===tok.v) draw();
  }

  seg.addEventListener('click', e=>{
    const b=e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(x=>x.classList.toggle('on', x===b));
    go(+b.dataset.v);
  });
  onResize(draw);
  return { enter(){ go(st); }, leave(){ tok.v++; } };
}

/* ═══════════════════════ 2 · КАК ЕЁ НАРИСОВАТЬ ═══════════════════════
   Две прежние главы слиты в одну (Ф1 + Ф6: глав ровно шесть). Слева общий текст
   на оба способа, справа листалка из двух карточек — механика та же, что у
   листалки доказательства, второй не пишем. Меняется только холст: текст один
   на обе карточки, поэтому он не мигает при листании. */

function sceneDraw(sec){
  const parts=[sceneHalves(sec), sceneVert(sec)];
  const cards=[...sec.querySelectorAll('.card')];
  const tools=[...sec.querySelectorAll('.tool')];
  const pager=pagerOf(sec, i=>{
    cards.forEach((c,k)=>c.classList.toggle('on', k===i));
    tools.forEach((t,k)=>t.classList.toggle('on', k===i));
    parts[i].enter();
  }, parts.length);
  return { enter(){ pager.show(pager.cur()); },
           leave(){ parts.forEach(p=>p.leave()); } };
}

/* ═══════════════════════ 3 · ПЕРЕСЕКАЕТ ЛИ ОНА СЕБЯ? ═══════════════════════
   Ф2. Текста на сцене нет вообще, холст занимает всю оставшуюся площадь, ранг
   фиксирован на 14, и есть зум: приблизить и увидеть, что линия НЕ сплошная.

   ⚠ ПОЧЕМУ ЗДЕСЬ НЕ CHAOS GAME, ХОТЯ Ф2 НАЗЫВАЕТ IFSRenderer. Chaos game сыплет
   точки по ЗАЛИТОЙ области дракона, а вся эта сцена — про ЛИНИЮ: спрашивается,
   не прошла ли она дважды по одному отрезку, и владелец хочет приблизить и
   увидеть, что она не сплошная. В облаке точек звеньев и зазоров между ними нет,
   на увеличении видна пыль или тело — то есть картинка опровергала бы вопрос
   сцены. Тот же дефект прошлый прогон уже поймал скриншотом на финальной сцене.
   Поэтому взята вся МЕХАНИКА, названную в Ф2, а рисуется ею наша ломаная:
     · прогрессивная отрисовка батчами по requestAnimationFrame;
     · renderToken — устаревшие кадры отменяются, а не досчитываются;
     · лог-интерполяция зума на полёте (как animateViewport в FractalSlide);
     · компенсация толщины штриха и alpha при увеличении (currentSize/currentAlpha);
     · зум-курсор рамкой и зум по клику в точку.
   Это и лечит зависание: работа в кадре ОГРАНИЧЕНА — батч, а не «вся кривая
   заново», — и на увеличении почти всё отсекается по окну, поэтому кадр на
   ранге 14 стоит тем меньше, чем глубже зум. */

function sceneCross(sec){
  const cv  = sec.querySelector('canvas');
  const fig = cv.parentNode;
  const segZ= sec.querySelector('[data-seg="zoom"]');
  const N=14, ZF=2.6, MARGIN=10;

  let P=null;                        // ломаная ранга 14 считается ОДИН раз, лениво
  let ctx, W, H;
  /* renderToken живёт объектом, а не числом, чтобы его понимал и anim(): один и
     тот же счётчик отменяет и батчи отрисовки, и кадры полёта зума. */
  const TK={v:0};
  let raf=null;
  let home=null, vp=null, zoom=1, shown=1;

  function pts(){ return P || (P=rank(N)); }

  /** окно задаётся центром и ПОЛУШИРИНОЙ; полувысота выводится из пропорций
      холста, поэтому пиксель квадратный при любом размере окна */
  function halfH(hw){ return hw*H/W; }

  function homeVp(){
    const b=bounds(pts());
    const cx=(b.x0+b.x1)/2, cy=(b.y0+b.y1)/2;
    const need=Math.max((b.x1-b.x0)/2, ((b.y1-b.y0)/2)*W/H);
    const pad=1 + (2*MARGIN)/Math.min(W,H);
    return {cx, cy, hw:need*pad*1.02};
  }

  /* Компенсация из FractalSlide: чем глубже зум, тем толще штрих и плотнее
     цвет — иначе на увеличении кривая бледнеет и «не сплошная» читается как
     «плохо нарисована». */
  function step(){ return Math.max(0, Math.log(shown)/Math.log(ZF)); }
  function lineW(){ return Math.min(0.85 + 0.34*step(), 2.6); }
  function alphaOf(){ return Math.min(0.72 + 0.07*step(), 1); }

  function mapper(){
    const s=(W/2)/vp.hw;
    return p=>[W/2+(p[0]-vp.cx)*s, H/2-(p[1]-vp.cy)*s];
  }

  /** Один проход по ломаной с шагом stride: звенья вне окна отбрасываются,
      остальные копятся в ОДИН путь и обводятся разом. Возвращает,
      сколько звеньев обработано. */
  function strokeRange(g, i0, i1, stride){
    const Q=pts(), total=Q.length-1;
    ctx.beginPath();
    let pen=false, prev=null;
    for(let i=i0;i<i1;i+=stride){
      const j=Math.min(total, i+stride);
      const a=prev || g(Q[i]), b=g(Q[j]);
      prev=b;
      if((a[0]<-8 && b[0]<-8) || (a[0]>W+8 && b[0]>W+8) ||
         (a[1]<-8 && b[1]<-8) || (a[1]>H+8 && b[1]>H+8)){ pen=false; continue; }
      if(!pen){ ctx.moveTo(a[0],a[1]); pen=true; }
      ctx.lineTo(b[0],b[1]);
    }
    ctx.stroke();
    return i1-i0;
  }

  function prep(){
    const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
    ctx.strokeStyle=cssVar('--acc');
    ctx.lineWidth=lineW(); ctx.lineJoin='round'; ctx.lineCap='round';
    ctx.globalAlpha=alphaOf();
  }

  /** ГРУБЫЙ КАДР ПОЛЁТА. Бюджет звеньев фиксирован, поэтому кадр стоит одинаково
      при любом зуме. Прореживание идёт степенями двойки — и это не небрежность:
      каждая вторая вершина кривой ранга n даёт ровно кривую ранга n−1, то есть
      силуэт остаётся тем же, только звено крупнее. */
  function paintQuick(budget){
    const total=pts().length-1;
    let stride=1;
    while(total/stride > budget) stride*=2;
    prep();
    ctx.clearRect(0,0,W,H);
    strokeRange(mapper(), 0, total, stride);
    ctx.globalAlpha=1;
  }

  /** ПОЛНЫЙ КАДР, батчами по rAF и с отменой по токену. Холст не чистится между
      батчами — плотность копится, как в renderProgressive референса. */
  function paintFull(progressive){
    const my=++TK.v;
    if(raf){ cancelAnimationFrame(raf); raf=null; }
    const total=pts().length-1;
    prep();
    ctx.clearRect(0,0,W,H);
    const g=mapper();
    if(!progressive || REDUCED){
      strokeRange(g, 0, total, 1); ctx.globalAlpha=1; return;
    }
    const B=Math.max(400, Math.ceil(total/56));
    let done=0;
    const frame=()=>{
      if(my!==TK.v) return;                        // кадр устарел — не досчитываем
      strokeRange(g, done, Math.min(total, done+B), 1);
      done+=B;
      if(done<total) raf=requestAnimationFrame(frame);
      else { raf=null; ctx.globalAlpha=1; }
    };
    raf=requestAnimationFrame(frame);
  }

  /** полёт: viewport интерполируется линейно, увеличение — по логарифму */
  async function fly(target, targetZoom){
    const my=++TK.v;
    const from={...vp}, fromZ=shown;
    if(REDUCED){ vp=target; zoom=shown=targetZoom; paintFull(false); return; }
    await anim(0,1,700,e=>{
      vp={ cx:lerp(from.cx,target.cx,e), cy:lerp(from.cy,target.cy,e),
           hw:Math.exp(lerp(Math.log(from.hw),Math.log(target.hw),e)) };
      shown=Math.exp(lerp(Math.log(fromZ),Math.log(targetZoom),e));
      paintQuick(2200);
    }, TK);
    if(my!==TK.v) return;                          // полёт перебит новым — уходим
    vp=target; zoom=shown=targetZoom;
    paintFull(true);
  }

  function zoomTo(fx, fy){
    const hh=halfH(vp.hw);
    return { cx: vp.cx + (fx-0.5)*2*vp.hw,
             cy: vp.cy - (fy-0.5)*2*hh,
             hw: vp.hw/ZF };
  }

  segZ.addEventListener('click', async e=>{
    const b=e.target.closest('button'); if(!b) return;
    const v=b.dataset.v;
    if(v==='reset'){ zoom=shown=1; vp={...home}; paintFull(true); return; }
    if(v==='out'){
      if(zoom<=1.01) return;
      const z=Math.max(1, zoom/ZF);
      if(z<=1.01){ await fly({...home},1); return; }
      await fly({cx:vp.cx, cy:vp.cy, hw:vp.hw*ZF}, z);
      return;
    }
    await fly(zoomTo(0.5,0.5), zoom*ZF);
  });

  /* зум-курсор и зум по клику — прямо из референса */
  const cur=document.createElement('div');
  cur.style.cssText='position:absolute;pointer-events:none;display:none;z-index:5;'+
    'border:1px solid color-mix(in srgb, var(--acc) 80%, white);'+
    'background:color-mix(in srgb, var(--acc) 10%, transparent);';
  fig.style.position='relative'; fig.appendChild(cur);
  cv.addEventListener('mousemove',ev=>{
    const r=cv.getBoundingClientRect();
    const w=r.width/ZF, h=r.height/ZF;
    const x=Math.max(w/2,Math.min(r.width-w/2, ev.clientX-r.left));
    const y=Math.max(h/2,Math.min(r.height-h/2, ev.clientY-r.top));
    cur.style.width=w+'px'; cur.style.height=h+'px';
    cur.style.left=(x-w/2)+'px'; cur.style.top=(y-h/2)+'px';
    cur.style.display='block'; cv.style.cursor='none';
  });
  cv.addEventListener('mouseleave',()=>{ cur.style.display='none'; cv.style.cursor=''; });
  cv.addEventListener('click',async ev=>{
    const r=cv.getBoundingClientRect();
    await fly(zoomTo((ev.clientX-r.left)/r.width, (ev.clientY-r.top)/r.height), zoom*ZF);
  });

  onResize(()=>{
    const c=setupCanvas(cv); W=c.w; H=c.h;
    if(zoom<=1.01){ home=homeVp(); vp={...home}; }
    paintFull(false);
  });

  return {
    enter(){
      const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
      if(!home){ home=homeVp(); vp={...home}; }
      paintFull(true);
    },
    leave(){ TK.v++; if(raf){ cancelAnimationFrame(raf); raf=null; } }
  };
}

/* ═══════════════════════ 5 · ДОКАЗАТЕЛЬСТВО ═══════════════════════ */

/* ═══ ВРЕЗКА: ОТКУДА БЕРЁТСЯ ПРАВИЛО СТРОК ═══
   Главное содержательное замечание владельца. Он держит разницу между двумя
   фактами доказательства, и на сайте её не было:
     · «у уголка одно звено вбок, другое вверх-вниз» — к дракону отношения не
       имеет, следует из одних прямых поворотов. Факт бесплатный.
     · ПРАВИЛО СТРОК — уже про дракона. Оно держится на том, что диагонали
       прежней кривой сами поворачивают на 90°: две соседние не могут смотреть
       одинаково. А раз соседние диагонали повёрнуты друг относительно друга,
       то и уголки, надетые на них, получаются один из другого поворотом —
       отсюда чередование.

   ⚠ ЧИСЛА ЗДЕСЬ НЕ ВЫДУМАНЫ, А ПРОВЕРЕНЫ (гейт, пункт 19, на рангах 5–7):
     · у уголка первое звено ГОРИЗОНТАЛЬНО всегда — значит уголок на диагонали
       (dx,dy) определён однозначно: старт → старт+(dx,0) → старт+(dx,dy);
     · сторона поворота = знак dx·dy, то есть свойство ОДНОЙ диагонали;
     · соседние диагонали повёрнуты на ±90°, а поворот меняет знак dx·dy —
       поэтому сторона чередуется, и излом соседней уходит в соседнюю строку.
   Схема поэтому абстрактная и маленькая: две соседние диагонали под прямым
   углом и два уголка на них. Подписей внутри нет (их на холстах нет вообще),
   объяснение — одной фразой в левой колонке. */
function insetRule(par, b){
  /* Окно врезки задано ЯВНО и шире разметки: полосы .d-row тянутся на полклетки
     за рамку содержимого, и при окне «точно по фигуре» они вылезали за рамку
     врезки — разметка обязана оставаться внутри своей врезки. */
  const g=fit([[-0.85,-0.78],[2.85,1.72]], {x:b.x,y:b.y,w:b.w,h:b.h,pad:12});
  const box={x0:0,x1:2,y0:0,y1:1};
  const G=mk('g',{},par);
  /* ⚠ ПОДЛОЖКА ГЛУХАЯ, А НЕ ОДНА РАМКА. Полосы .d-row основной картинки тянутся
     на клетку за охват кривой и проходили СКВОЗЬ врезку: у врезки своя строка 0,
     и чужая полоса поперёк неё делала схему нечитаемой. Поймано снимком. */
  mk('rect',{x:b.x,y:b.y,width:b.w,height:b.h,rx:8,class:'d-panel',
             'stroke-width':1},G);
  /* полоса крашеной строки — РОВНО по ширине решётки врезки: rowBands тянет её
     на полклетки в стороны, и на схеме из двух клеток этот запас читался как
     отдельный серый прямоугольник, а не как строка */
  const bl=g([box.x0, 0.5]), br=g([box.x1, -0.5]);
  mk('rect',{x:Math.min(bl[0],br[0]), y:Math.min(bl[1],br[1]),
             width:Math.abs(br[0]-bl[0]), height:Math.abs(br[1]-bl[1]),
             class:'d-row'},G);
  lattice(G,g,box,0);
  /* две СОСЕДНИЕ диагонали прежней кривой: (0,0)→(1,1) и (1,1)→(2,0).
     Направления (1,1) и (1,−1) — ровно поворот на 90°, иначе быть не может. */
  const D=[[[0,0],[1,1]],[[1,1],[2,0]]];
  const K=[[[0,0],[1,0],[1,1]],[[1,1],[2,1],[2,0]]];
  D.forEach(([p,q])=>mk('path',{d:sharpD([p,q].map(g)),class:'d-dash',
                                'stroke-width':1.8},G));
  K.forEach(k=>{
    const left=turnsLeft(k[0],k[1],k[2]);
    mk('path',{d:roundPath(k.map(g),ROUND.b),class:left?'d-acc2':'d-line',
               'stroke-width':3.4},G);
    for(let i=0;i<2;i++) arrowOn(G,g(k[i]),g(k[i+1]),'d-arrow',11);
  });
  /* метка прямого угла в общей вершине: квадратик между двумя диагоналями */
  const c=[1,1], r=0.18, s2=Math.SQRT1_2;   // 0,18: на 0,28 метка налезала на стрелку хода
  const u=[-s2*r,-s2*r], v=[s2*r,-s2*r];
  mk('path',{d:sharpD([[c[0]+u[0],c[1]+u[1]],
                       [c[0]+u[0]+v[0],c[1]+u[1]+v[1]],
                       [c[0]+v[0],c[1]+v[1]]].map(g)),
             class:'d-dim','stroke-width':1.4},G);
  [[0,0],[1,1],[2,0]].forEach(p=>node(G,g(p),'d-node-b',4.4));
  [[1,0],[2,1]].forEach(p=>node(G,g(p),'d-node',4.4));
  return G;
}

/* 5а. ВЕРШИНЫ ДВУХ СОРТОВ И СТРОКИ — ОДИН ШАГ.
       Прежде это были два шага. Владелец слил их: «взять картинку шага про
       строки и покрасить на ней уголки в два цвета — тогда и сорта вершин,
       и правило строк видны на одной картинке, и отдельный шаг не нужен».
       Уголок красится по СТОРОНЕ ПОВОРОТА, и цвет совпадает с цветом его
       строки — то есть правило строк читается прямо с картинки.

       Три вещи, которых на этой картинке раньше не было:
         · шахматная раскраска идёт по ВСЕЙ решётке, а не по вершинам кривой:
           так чередование выглядит свойством плоскости, а не картинки;
         · стрелки хода КРУПНЫЕ — без направления обхода «налево» бессмысленно,
           и владелец именно это и не мог прочитать;
         · внизу врезка: откуда берётся само правило строк (insetRule). */
function stepRows(sec){
  const svg = sec.querySelector('[data-step="a"] svg');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  /* Ранг 5, а не 6. На 64 звеньях стрелка хода выходит мельче самого звена, и
     требование «направление видно с расстояния» не выполняется ни при каком
     размере наконечника. На 32 звеньях дракон узнаётся, а звено крупное. */
  const N=5, P=rank(N), C=corners(P);
  let hi=null;

  /* Холст поделён: кривая сверху, врезка — узкой полосой снизу. Делить именно
     здесь, а не CSS-слоем поверх фигуры: врезка обязана не налезать на кривую,
     а положение кривой считает fit() по её собственной рамке. */
  const TOP={x:0,y:0,w:W,h:742,pad:40};
  const INSET={x:330,y:756,w:340,h:230};

  function draw(){
    wipe(svg);
    const g=fit(P,TOP);
    /* ⚠ КРУЖОЧКИ ВМЕСТО ПОЛОС ПРОБОВАЛИ И ОТКАЗАЛИСЬ — снимок в отчёте.
       Владелец предлагал обвести кружочком вершины в крашеных строках и полосы
       убрать. Обводка сама по себе чище полос, но ломается ровно там, где нужна:
       правило решает ИЗЛОМ, а излом — всегда НОВАЯ вершина, то есть уже пустой
       кружок. Обводка вокруг пустого кружка даёт ⊚, и «сорт вершины» с «строкой»
       перестают различаться глазом — то самое, от чего кружочки должны были
       избавить. Полосы остались; правило и без них видно по цвету уголка. */
    rowBands(svg,g,g.box,1);
    lattice(svg,g,g.box,1);
    latticeNodes(svg,g,g.box,1);
    C.forEach(([a,b,c],k)=>{
      const left=turnsLeft(a,b,c);
      mk('path',{d:roundPath([a,b,c].map(g),ROUND.b),
                 class: left?'d-acc2':'d-line',
                 'stroke-width': hi===k?6.5:3.2},svg);
    });
    for(let i=0;i<P.length-1;i++) arrowOn(svg,g(P[i]),g(P[i+1]),'d-arrow',17);
    C.forEach(([a,b,c],k)=>{
      node(svg,g(a),'d-node-b',5.2);
      node(svg,g(b),'d-node',5.2);
      const hit=mk('path',{d:sharpD([a,b,c].map(g)),class:'d-hit'},svg);
      onHover(hit, ()=>{ hi=k; draw(); });
      hit.addEventListener('mouseleave',()=>{ hi=null; draw(); });
    });
    node(svg,g(P[P.length-1]),'d-node-b',5.2);
    insetRule(svg, INSET);
  }
  onResize(draw);
  return { enter(){ draw(); }, leave(){} };
}

/* 5в. ГЛАВНЫЙ ИНТЕРАКТИВ. Наводишь на звено — показываются ОБА кандидата на
       продолжение, и лишний гаснет. Правило и оба кандидата берутся из
       corner() в dragon.js, проверенной на 32 764 звеньях.
       Четыре случая (звено вдоль/поперёк × строка голубая/белая) отмечаются
       по мере прохождения: читателю видно, что правило работает во всех. */
function step5v(sec){
  const svg = sec.querySelector('[data-step="v"] svg');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const N=6, P=rank(N);
  let pick=null, fade=1, tok={v:0};

  function draw(){
    wipe(svg);
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:56});
    rowBands(svg,g,g.box);
    lattice(svg,g,g.box,0);
    const S=P.map(g);
    // базовая кривая ЯРЧЕ разметки: иначе не видно, на что наводить
    mk('path',{d:roundPath(S,ROUND.v),class:'d-line','stroke-width':2.4,
               opacity:0.92},svg);

    if(pick!==null){
      const r = corner(P[pick], P[pick+1]);
      const known = [P[pick], P[pick+1]].map(g);
      // оба кандидата: сначала оба видны, потом лишний гаснет
      const goodTail = r.half===0 ? [r.corner[1], r.corner[2]] : [r.corner[0], r.corner[1]];
      const badTail  = r.half===0 ? [r.other[1],  r.other[2] ] : [r.other[0],  r.other[1] ];
      mk('path',{d:sharpD(badTail.map(g)), class:'d-acc2','stroke-width':4,
                 'stroke-dasharray':'6 6', opacity:(0.12+0.68*fade).toFixed(3)},svg);
      mk('path',{d:roundPath(r.corner.map(g),ROUND.v), class:'d-acc','stroke-width':4.4,
                 opacity:(0.35+0.65*(1-fade)).toFixed(3)},svg);
      mk('path',{d:sharpD(known), class:'d-hot','stroke-width':6},svg);
      /* Стрелка на самом подсвеченном ребре. Шаг утверждает «по ОДНОМУ ребру
         уголок восстановлен целиком», а восстановление читает направление хода:
         без стрелки на этом ребре утверждение проверить нечем. */
      arrowOn(svg, known[0], known[1], 'd-arrow-a', 22);
      node(svg, g(r.izlom), 'd-node', 6.5);
      node(svg, g(r.corner[0]), 'd-node-b', 5);
      node(svg, g(r.corner[2]), 'd-node-b', 5);
      node(svg, g(r.other[r.half===0?2:0]), 'd-node', 4.5);
    }
    for(let i=0;i<P.length-1;i++){
      const hit=mk('line',{x1:S[i][0],y1:S[i][1],x2:S[i+1][0],y2:S[i+1][1],
                           class:'d-hit'},svg);
      onHover(hit, ()=>show(i));
    }
    svg.addEventListener('mouseleave',()=>{ pick=null; fade=1; draw(); }, {once:true});
  }

  async function show(i){
    if(pick===i) return;
    pick=i; fade=1;
    draw();
    tok.v++; const my=tok;
    if(REDUCED){ fade=0; draw(); return; }
    await anim(1,0,420,v=>{ fade=v; draw(); }, my);
  }

  /* Строки «звено вдоль · строка крашеная ⇒ налево» и счётчика «пройдено N из 4»
     больше нет: Ф5 убирает все показания. Требование «все четыре случая
     достижимы» этим не отменяется — оно проверяется гейтом по самой геометрии
     (check_sayt.py, пункт 4: corner() на ранге 6 даёт h0,h1,v0,v1), а не
     надписью на экране. */

  onResize(draw);
  return { enter(){ draw(); }, leave(){ tok.v++; } };
}

/* 5г. Ранг 6 и ранг 7 рядом. Звено k ранга 6 ⟷ уголок k ранга 7: чётные
       вершины ранга 7 — это ранг 6, умноженный на (1+i) (проверено гейтом).
       Связь двусторонняя: наводишь слева — горит справа, и наоборот. */
function step5g(sec){
  const svg = sec.querySelector('[data-step="g"] svg');
  const W=1000, H=750;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const A=rank(6), B=rank(7), CB=corners(B);
  /* pick — не индекс, а {k, half}: k — номер уголка (он же номер звена ранга 6),
     half — какая из двух половин уголка под мышью. Половина нужна потому, что
     шаг обязан говорить «по ОДНОМУ РЕБРУ восстанавливается его уголок»: зона
     наведения — ребро, а не уголок целиком, иначе утверждение подменяется. */
  let pick=null;

  function draw(){
    wipe(svg);
    /* Подписей «ранг 6» / «ранг 7» внутри холста НЕТ сознательно: справа не
       бывает текста (Д2), и какая картинка какая — сказано в левой колонке. */
    const gA=fit(A,{x:0,y:0,w:W/2,h:H,pad:46});
    const gB=fit(B,{x:W/2,y:0,w:W/2,h:H,pad:46});
    const SA=A.map(gA), SB=B.map(gB);
    /* d-mute, а не d-dim: цвет границ (--rule #2A2A30) на фоне #0E0E10 почти
       не виден, и оба ранга читались как пустая панель — шаг не показывал
       ничего. Поймано скриншотом. Приглушение — прозрачностью, не цветом.
       ⚠ ПРИ НАВЕДЕНИИ ОБЕ КРИВЫЕ ГАСНУТ ДО 0,22. Иначе подсветка — короткий
       отрезок слева и мелкий уголок справа, разнесённые по разным концам
       панели, — тонула в двух полных кривых, и заявленное «звено k слева = это
       уголок k справа» глазом не подтверждалось (нашёл верификатор). Когда
       гаснет всё остальное, светятся ровно два предмета — и связь видна без
       единой подписи, которых тут и нельзя. */
    /* ⚠ КОНТРАСТ В ПОКОЕ ПОДНЯТ ДО ОСНОВНОГО ЦВЕТА ТЕКСТА (Ф8). Приглушённый
       серый на 0,8 читался на снимке как бледная плашка: верификатор назвал шаг
       «почти пустой панелью», и на проекторе это было бы хуже, чем на снимке.
       Теперь в покое обе кривые идут цветом текста и полной толщиной, а гаснут
       ТОЛЬКО при наведении — тогда светятся ровно два предмета. */
    /* 0,3 при наведении, а не 0,2: на 0,2 обе кривые на снимке уходили в фон
       почти целиком, и «вот это звено внутри вот этой кривой» проверить было
       нельзя — тот самый дефект «почти пустая панель», за который шаг уже
       правили. Гасить надо ровно настолько, чтобы подсветка выигрывала. */
    const base = pick===null ? 0.95 : 0.3;
    const cls  = pick===null ? 'd-line' : 'd-mute';
    /* ⚠ СПРАВА — ПОЛОСЫ И ДВУХЦВЕТНЫЕ УГОЛКИ, А НЕ ОДНА РОВНАЯ КРИВАЯ. Шаг
       говорит: «по одному ребру — вместе с цветом его строки и цветами его
       вершин — восстанавливается направление и поворот». Пока правая кривая шла
       одним цветом по чистому полю, ни строки, ни цвета вершин на ней не было
       видно, и цепочка доказательства опиралась на то, чего на картинке нет. */
    rowBands(svg,gB,gB.box,0);
    mk('path',{d:roundPath(SA,ROUND.g),class:cls,'stroke-width':2.6,opacity:base},svg);
    if(pick===null)
      CB.forEach(c=>mk('path',{d:roundPath(c.map(gB),ROUND.g),
        class: turnsLeft(c[0],c[1],c[2])?'d-acc2':'d-line','stroke-width':2.1},svg));
    else
      mk('path',{d:roundPath(SB,ROUND.g),class:cls,'stroke-width':2.1,opacity:base},svg);
    if(pick!==null){
      const k=pick.k, c=CB[k];
      const e0=c[pick.half], e1=c[pick.half+1];       // само ребро ранга 7
      // уголок целиком — то, во что ребро достраивается…
      /* ⚠ ПОД УГОЛКОМ — ШИРОКАЯ АКЦЕНТНАЯ ПОДЛОЖКА. Уголок ранга 7 в половине
         панели занимает десяток пикселей, и подсветка «той же толщиной, но
         ярче» на снимке терялась среди полос строк: глазом было не найти, ЧТО
         подсветилось. Подложка — единственное, что видно с расстояния; цвет
         самого уголка при этом не меняется (он несёт цвет своей строки, и
         подменять его при наведении значило бы стирать предмет шага). */
      mk('path',{d:roundPath(c.map(gB),ROUND.g),class:'d-acc',
                 'stroke-width':13,opacity:0.3},svg);
      mk('path',{d:roundPath(c.map(gB),ROUND.g),
                 class: turnsLeft(c[0],c[1],c[2])?'d-acc2':'d-line','stroke-width':6.5},svg);
      // …и ребро поверх него: направление хода стрелкой, поворот — формой уголка
      mk('path',{d:sharpD([gB(e0),gB(e1)]),class:'d-hot','stroke-width':6.5},svg);
      arrowOn(svg, gB(e0), gB(e1), 'd-arrow-a', 13);
      node(svg, gB(c[0]),'d-node-b', 5);              // концы уголка — старые вершины
      node(svg, gB(c[2]),'d-node-b', 5);
      node(svg, gB(c[1]),'d-node', 5.5);              // излом — новая вершина
      // и то, во что уголок превращается рангом ниже: одно звено ранга 6
      mk('path',{d:sharpD([SA[k],SA[k+1]]),class:'d-hot','stroke-width':7},svg);
      arrowOn(svg, SA[k], SA[k+1], 'd-arrow-a', 16);
      node(svg, gA(A[k]),   'd-node-a', 5);
      node(svg, gA(A[k+1]), 'd-node-a', 5);
    }
    for(let i=0;i<A.length-1;i++){
      const h=mk('line',{x1:SA[i][0],y1:SA[i][1],x2:SA[i+1][0],y2:SA[i+1][1],class:'d-hit'},svg);
      onHover(h, ()=>{ pick={k:i, half:0}; draw(); });
    }
    CB.forEach((c,k)=>{                               // зона на КАЖДОЕ ребро уголка
      for(let h=0;h<2;h++){
        const z=mk('path',{d:sharpD([c[h],c[h+1]].map(gB)),class:'d-hit'},svg);
        onHover(z, ()=>{ pick={k, half:h}; draw(); });
      }
    });
    svg.addEventListener('mouseleave',()=>{ pick=null; draw(); },{once:true});
  }
  onResize(draw);
  return { enter(){ draw(); }, leave(){} };
}

/* Четыре шага — слайды ОДНОЙ листалки внутри сцены: виден один, ← → листают
   шаги, ↓ уходит на следующую сцену, внизу четыре точки.
   Скрытый шаг снят из потока (display:none), но перерисовать его при показе
   всё равно можно без обмеров: все холсты сцены 5 — SVG с viewBox, и fit()
   считает по константам 1000×1000, а не по getBoundingClientRect. Если бы тут
   был canvas, он бы получил нулевой размер и остался пустым. */
function sceneProof(sec){
  /* Шагов ТРИ, а не четыре: «вершины двух сортов» и «строки» слиты в один
     (stepRows) по правке владельца. Точек листалки поэтому пять на весь сайт
     (2 карточки способов + 3 шага), и это проверяет гейт, пункт 13. */
  const parts=[stepRows(sec), step5v(sec), step5g(sec)];
  const bodies=[...sec.querySelectorAll('.steps > .scene__body')];
  const pager=pagerOf(sec, i=>{
    bodies.forEach((b,k)=>b.classList.toggle('on', k===i));
    parts[i].enter();
  }, parts.length);
  return { enter(){ pager.show(pager.cur()); },
           leave(){ parts.forEach(p=>p.leave()); } };
}

/* ═══════════════════════ 6 · ЧЕТЫРЕ ДРАКОНА ═══════════════════════
   Основа — T23 (1058–1090) и TB (1273–1289). Растут ОДНОВРЕМЕННО, все четыре,
   с ранга 4 до выбранного. Рамка считается сразу по всем четырём и по всем
   рангам — иначе камера прыгает при каждом шаге (урок T23 и TA). */

function sceneFour(sec){
  const svg = sec.querySelector('svg');
  const seg = sec.querySelector('[data-seg="rank"]');
  const segF= sec.querySelector('[data-seg="fill"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const LO=4, MAX=10;
  const cache={}, all=[];
  for(let n=LO;n<=MAX;n++){
    const P=poly(word(n),90,Math.pow(2,-n/2));
    cache[n]=P;
    for(let r=0;r<4;r++) all.push(...rotAbout(P,[0,0],r*90));
  }
  const frame=bounds(all);

  /* ═══ ПРЕДЕЛЬНОЕ ЗАПОЛНЕНИЕ ═══
     Владелец: «видно только, что они не налезают друг на друга; не видно, что
     в пределе не остаётся дырок». Заполнение и есть это «не остаётся».

     Клетка звена — квадрат на нём как на диагонали (dragCells): у него обе
     диагонали по звену, значит это ромб, и он ОДИНАКОВ для горизонтального и
     вертикального звена. Поэтому поворот всей картины на 90° — это поворот
     одного лишь ключа клетки: (p,q) → (−q,p), а форму ромба крутить не надо.

     ⚠ ЧИСЛО ПРОВЕРЕНО, А НЕ ЗАЯВЛЕНО. На рангах 4, 6, 8, 10 у четырёх драконов
     ровно 4·2ⁿ клеток и столько же РАЗНЫХ ключей — наложений нуль; и ни одной
     пустой клетки, у которой все четыре соседа по стороне заняты, — дырок нуль.
     Считается это гейтом (пункт 20), а не подписью на экране. */
  const fcache={};
  /** центры клеток всех четырёх драконов ранга n, уже в масштабе кривой */
  function cellsOf(n){
    if(fcache[n]) return fcache[n];
    const s=Math.pow(2,-n/2), K=dragCells(n), out=[];
    for(let r=0;r<4;r++){
      const C=[];
      for(const k of K){
        let cx=k[0]/2*s, cy=k[1]/2*s;
        for(let i=0;i<r;i++){ const t=cx; cx=-cy; cy=t; }
        C.push([cx,cy]);
      }
      out.push(C);
    }
    return (fcache[n]=[out, s/2]);
  }
  /** все ромбы одного дракона ОДНИМ путём: 4096 отдельных path браузер рисует
      заметно дороже, а ромбы не пересекаются, поэтому подпути независимы */
  function quadsPath(C, h, g){
    let d='';
    for(const [cx,cy] of C){
      const l=g([cx-h,cy]), t=g([cx,cy+h]), r=g([cx+h,cy]), b=g([cx,cy-h]);
      d += ' M '+l[0].toFixed(2)+' '+l[1].toFixed(2)
         + ' L '+t[0].toFixed(2)+' '+t[1].toFixed(2)
         + ' L '+r[0].toFixed(2)+' '+r[1].toFixed(2)
         + ' L '+b[0].toFixed(2)+' '+b[1].toFixed(2)+' Z';
    }
    return d.trim();
  }
  const FILL=['d-fill','d-fill-a','d-fill-a2','d-fill-m'];
  let fill=false;
  /* Четыре цвета: белый, акцент, второй акцент, серый. Второй акцент здесь
     нужен по той же причине, что и в схемах доказательства — различить
     объекты; на двух серых ранг 10 хайрлайнами уже не читается, а
     нечитаемая сцена не выполняет то, ради чего стоит. */
  const CLS=['d-line','d-acc','d-acc2','d-mute'];
  let target=6, n=LO, tok={v:0};

  function draw(){
    wipe(svg);
    const P=cache[n];
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:44},frame);
    /* ⚠ ТОЛЩИНА И ПРОЗРАЧНОСТЬ РАЗВОДЯТ БЕЛОГО И СЕРОГО ДРАКОНА. На ранге 10
       при 1,15 px белый (--text #ECECEC) и приглушённый серый (--text-muted
       #9A9AA0) сливались в одно пятно, и утверждение сцены «цвета ни разу не
       налезают» глазом проверить было нельзя (нашёл верификатор). Толщина
       поднята, а серому добавлена прозрачность: разница в светлоте на хайрлайне
       не читается, разница в плотности читается. */
    const lw = n>=10 ? 1.45 : (n>=8 ? 1.9 : (n>=6 ? 2.4 : 3.2));
    if(fill){
      const [CC,h]=cellsOf(n);
      for(let r=0;r<4;r++)
        mk('path',{d:quadsPath(CC[r],h,g), class:FILL[r], opacity:0.66},svg);
    }
    for(let r=0;r<4;r++){
      const S=rotAbout(P,[0,0],r*90).map(g);
      /* при заполнении линия становится хайрлайном и уходит вниз по плотности:
         предмет кадра — стык плиток, а не сама кривая, и толстая линия закрывала
         бы именно стык, то есть то место, где и видно «дырок нет» */
      mk('path',{d:roundPath(S,ROUND.four), class:CLS[r],
                 'stroke-width': fill ? Math.min(1.1, lw) : lw,
                 // на ранге 8 и выше линия внутри заливки превращается в
                 // клетчатую текстуру и плитку читать мешает — гасим сильнее
                 opacity: fill ? (n>=8 ? 0.22 : 0.5)
                               : (CLS[r]==='d-mute' ? 0.72 : 1)},svg);
    }
    node(svg,g([0,0]),'d-node-b',4.5);
    /* Отсчёт «отрезков, взятых дважды: 0» убран по Ф5 вместе со всеми
       остальными показаниями. Само утверждение по-прежнему проверяется — но
       гейтом ядра (sharedEdges в check_dragon.js), а не строкой на экране. */
  }
  async function grow(){
    tok.v++; const my=tok;
    if(REDUCED){ n=target; draw(); return; }
    for(n=LO;n<=target;n++){ draw(); if(!await pause(n===LO?820:560,my)) return; }
    n=target; draw();
  }
  seg.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));
    target=+b.dataset.v; grow();
  });
  segF.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    fill=!fill; b.classList.toggle('on', fill);
    if(n!==target){ tok.v++; n=target; }        // рост перебиваем, кадр не ждём
    draw();
  });
  onResize(draw);
  return { enter(){ grow(); }, leave(){ tok.v++; } };
}

/* ═══════════════════════ 7 · ЛИНИЯ, У КОТОРОЙ ЕСТЬ ПЛОЩАДЬ ═══════════════════════
   Три движения.
   1) Звено толстеет до полклетки. Клетка — квадрат на звене как на диагонали
      (dragCells), площадь ровно ½; при t=0 ромб вырожден в само звено, поэтому
      это НЕ подмена картинки, а одна фигура в двух положениях ручки.
   2) Зум в край. Механика из FractalSlide референса: зум-курсор, зум по клику,
      лог-интерполяция, компенсация плотности. Рисуется тем же аттрактором IFS,
      что в референсе (два аффинных преобразования) — и это ровно наша область:
      проверено сравнением занятости сетки 128×128, Жаккар 0,966 при
      сопряжении (без сопряжения 0,188). Поэтому переход между заливкой и
      облаком точек — смена текстуры, а не прыжок фигуры.
   3) Изрезанность края считается на глазах: dragBoundary даёт число сторон,
      отношение к прежнему рангу даёт 1,5236… */

const IFS_DRAGON = [
  {a: 0.5, b:-0.5, c: 0.5, d: 0.5, e:0, f:0},
  {a:-0.5, b:-0.5, c: 0.5, d:-0.5, e:1, f:0}
];

/** охват аттрактора — замерен chaos game на 800 тыс. точек */
const IFS_BOX = {x0:-1/3, x1:7/6, y0:-1/3, y1:2/3};

/* ⚠ ПОЧЕМУ ЗДЕСЬ НЕ CHAOS GAME, ХОТЯ В РЕФЕРЕНСЕ ОН.
   Chaos game сыплет точки по ВСЕМУ аттрактору, а в окно попадают только те,
   что в него угодили. Площадь окна падает как Z², а число точек в
   FractalSlide растёт как Z (`baseIterations * zoomLevel`) — значит заполнение
   окна падает как 1/Z. Проверено скриншотом: на увеличении ×17,6 из 1,4 млн
   точек в кадр попало около четырёх тысяч, и финальная сцена показывала
   ПЫЛЬ вместо тела с изрезанным краем. А сцена утверждает ровно обратное:
   «на каждом увеличении край выглядит так же». Утверждение опровергалось
   собственной картинкой.

   Вместо этого — точное рекурсивное измельчение с ОТСЕЧЕНИЕМ ПО ОКНУ.
   Аттрактор есть объединение своих образов под f1 и f2, поэтому: берём охват,
   применяем оба преобразования, куски вне окна выбрасываем, остальные делим
   дальше, пока кусок не станет меньше пикселя. Стоимость — порядка числа
   ВИДИМЫХ пикселей, а не всего аттрактора, поэтому картинка на любом
   увеличении одинаково плотная. Это тот же дракон: множество задаётся теми
   же двумя преобразованиями (совпадение с нашей ломаной проверено, Жаккар
   0,966). Зум-курсор, зум по клику и лог-интерполяция взяты из FractalSlide
   как есть — заменена только заливка. */
/* ⚠ ОБХОД ИДЁТ СТЕКОМ И ПОРЦИЯМИ, И ЭТО ЛЕЧЕНИЕ ЗАВИСАНИЯ (Ф2).
   Прежняя версия шла УРОВНЯМИ: держала массив кусков (страховка стояла на
   900 000 элементов) и досчитывала весь кадр СИНХРОННО — а вызывалась она из
   каждого кадра полёта зума. То есть браузер получал десятки полных отрисовок
   подряд, каждая на сотни тысяч кусков, и на живом железе это встаёт колом:
   владелец поймал зависание дважды, верификатор на своей машине не поймал —
   ровно та разница в нагрузке, о которой говорит оговорка захода.

   Теперь: обход в глубину стеком (память O(глубины), а не O(числа кусков)) и
   метод step(budget), который обрабатывает не больше budget кусков за вызов.
   Кто вызывает — решает, сколько платить за кадр: на полёте зума бюджет мелкий
   и куски крупные, на финальном кадре обход добивается батчами по rAF с
   отменой по renderToken. Работа в кадре стала ОГРАНИЧЕННОЙ — это и есть
   механика прогрессивной отрисовки из референса, приложенная к нашей заливке. */
const IFS_CORNERS = [[IFS_BOX.x0,IFS_BOX.y0],[IFS_BOX.x1,IFS_BOX.y0],
                     [IFS_BOX.x1,IFS_BOX.y1],[IFS_BOX.x0,IFS_BOX.y1]];

function deepWalk(ctx, vp, W, H, o){
  const m=o.margin, iw=W-2*m, ih=H-2*m;
  const sx=iw/(vp.xMax-vp.xMin), sy=ih/(vp.yMax-vp.yMin);
  const PX = o.px || 1.15;
  const MAXD = o.maxDepth || 44;
  const alpha = o.alpha===undefined ? 1 : o.alpha;
  // кусок = аффинное преобразование (a,b,c,d,e,f) плюс глубина
  const st=[[1,0,0,1,0,0,0]];
  return {
    /** обработать не больше budget кусков; true — обход закончен */
    step(budget){
      ctx.globalAlpha=alpha; ctx.fillStyle=o.color;
      let used=0;
      while(st.length && used<budget){
        const T=st.pop(); used++;
        const a=T[0],b=T[1],c=T[2],d=T[3],e=T[4],f=T[5],dep=T[6];
        // экранная рамка куска: образы четырёх углов охвата
        let X0=Infinity,X1=-Infinity,Y0=Infinity,Y1=-Infinity;
        for(let q=0;q<4;q++){
          const ux=IFS_CORNERS[q][0], uy=IFS_CORNERS[q][1];
          const wx=a*ux+b*uy+e, wy=c*ux+d*uy+f;
          const px=(wx-vp.xMin)*sx+m, py=H-m-(wy-vp.yMin)*sy;
          if(px<X0)X0=px; if(px>X1)X1=px; if(py<Y0)Y0=py; if(py>Y1)Y1=py;
        }
        if(X1<0||X0>W||Y1<0||Y0>H) continue;                 // вне окна — выбросить
        if((X1-X0<=PX && Y1-Y0<=PX) || dep>=MAXD){           // мельче пикселя — залить
          ctx.fillRect(X0, Y0, Math.max(PX,X1-X0), Math.max(PX,Y1-Y0));
          continue;
        }
        for(const t of IFS_DRAGON){                          // иначе — делить дальше
          st.push([ a*t.a+b*t.c, a*t.b+b*t.d,
                    c*t.a+d*t.c, c*t.b+d*t.d,
                    a*t.e+b*t.f+e, c*t.e+d*t.f+f, dep+1 ]);
        }
      }
      ctx.globalAlpha=1;
      return st.length===0;
    }
  };
}

function sceneArea(sec){
  const cv  = sec.querySelector('canvas');
  const fig = cv.parentNode;
  const inT = sec.querySelector('[data-in="thick"]');
  const segR= sec.querySelector('[data-seg="rank"]');
  const segZ= sec.querySelector('[data-seg="zoom"]');

  /* HOME — КВАДРАТНАЯ рамка вокруг фактического охвата аттрактора
     (x −0,333…1,167, y −0,333…0,667; замерено chaos game на 800 тыс. точек).
     Квадратная обязательно: toScreen масштабирует x и y независимо, и на
     неквадратной рамке квадратный холст растянул бы дракона. */
  const HOME={xMin:-0.35, xMax:1.18, yMin:-0.60, yMax:0.93};
  const MARGIN=14, ZF=2.6;
  let n=12, t=0, ctx, W, H, raf=null, tok={v:0};
  /* ⚠ У ЗАЛИВКИ СВОЙ ТОКЕН, ОТДЕЛЬНО ОТ ТОКЕНА АНИМАЦИЙ. Сначала батчи заливки
     считали тем же tok, что и anim() — и получилось так: анимация толщины на
     каждом кадре зовёт paint(), paint() бьёт tok, а anim() видит, что её метка
     устарела, и глохнет после ПЕРВОГО кадра. Ползунок оставался на нуле, сцена
     показывала линию вместо заливки — то самое, что сцена и опровергает.
     Поймано скриншотом (ползунок стоял в нуле), а не чтением кода. */
  const rtok={v:0};
  let vp={...HOME}, zoom=1, shown=1, blend=0;      // blend: 0 — клетки, 1 — облако точек
  const cache={};

  /* НОРМИРОВКА в координаты аттрактора: M(z) = conj(z / E), где E — конец
     ломаной. M линейна (M(0)=0), поэтому её достаточно задать образами базиса:
       M(1,0) = ( ex/den,  ey/den )
       M(0,1) = ( ey/den, −ex/den )
     Сопряжение обязательно: наша ломаная (первый сгиб L) — это аттрактор
     референса, отражённый по y. Проверено занятостью сетки 128×128 на ранге 16:
     с сопряжением Жаккар 0,966, без него 0,188. Поэтому переход «заливка →
     облако точек» — смена текстуры, а не прыжок фигуры.

     ⚠ ОДНА КАРТА, А НЕ ДВЕ. Первая версия держала отдельно базис (ux, uy) и
     отдельно «полдиагональ в нормированных единицах» (0.5/|E|) и перемножала
     их — а базис уже содержит 1/|E|. Полудиагональ выходила 0.5/|E|², то есть
     на ранге 12 в четыре тысячи раз меньше нужной: сцена рисовалась ПУСТОЙ.
     Поймано скриншотом, не кодом. Теперь смещение считается только через M,
     и полдиагональ — честные 0.5 клетки ДО отображения. */
  function normMap(k){
    if(cache[k]) return cache[k];
    const P=rank(k), E=P[P.length-1], den=E[0]*E[0]+E[1]*E[1];
    const M=(x,y)=>[ (x*E[0]+y*E[1])/den, -((y*E[0]-x*E[1])/den) ];
    const ux=M(1,0), uy=M(0,1);                    // образы базиса: уже с 1/|E|
    const C=dragCells(k);
    const q=C.map(([px,py])=>M(px/2, py/2));       // центры клеток
    const line=P.map(([x,y])=>M(x,y));             // сама ломаная
    /* Точка, в которую целится «Зум в край»: НЕ угаданная координата, а
       настоящая точка границы области — ближайшая к верхней середине фигуры.
       Считается из dragBoundary, поэтому попадает в край при любом ранге. */
    const B=dragBoundary(k).map(([s,e])=>M((s[0]+e[0])/2,(s[1]+e[1])/2));
    const aim=[0.4165, 0.667];
    let edge=B[0], best=Infinity;
    for(const p of B){
      const d=(p[0]-aim[0])*(p[0]-aim[0])+(p[1]-aim[1])*(p[1]-aim[1]);
      if(d<best){ best=d; edge=p; }
    }
    return (cache[k]={q, line, ux, uy, edge});
  }

  function toScreen(p){
    const iw=W-2*MARGIN, ih=H-2*MARGIN;
    return [ ((p[0]-vp.xMin)/(vp.xMax-vp.xMin))*iw+MARGIN,
             H-MARGIN-((p[1]-vp.yMin)/(vp.yMax-vp.yMin))*ih ];
  }

  function paintCells(alpha){
    const {q,line,ux,uy}=normMap(n);
    const HALF=0.5;                                 // полдиагональ клетки, в клетках
    ctx.globalAlpha=alpha;
    const acc=cssVar('--acc');
    if(t<0.02){                                     // t=0 — сама линия, без заливки
      ctx.strokeStyle=acc; ctx.lineWidth=n>=13?1:(n>=12?1.4:2.2);
      ctx.lineCap='round'; ctx.lineJoin='round';
      ctx.beginPath();
      for(let i=0;i<line.length;i++){
        const s=toScreen(line[i]);
        i? ctx.lineTo(s[0],s[1]) : ctx.moveTo(s[0],s[1]);
      }
      ctx.stroke(); ctx.globalAlpha=1; return;
    }
    ctx.fillStyle=acc;
    ctx.beginPath();
    for(let i=0;i<q.length;i++){
      const c=q[i];
      // ромб: ±полдиагональ вдоль звена и ±t·полдиагональ поперёк
      const a=toScreen([c[0]-ux[0]*HALF,   c[1]-ux[1]*HALF]);
      const b=toScreen([c[0]+uy[0]*HALF*t, c[1]+uy[1]*HALF*t]);
      const d=toScreen([c[0]+ux[0]*HALF,   c[1]+ux[1]*HALF]);
      const e=toScreen([c[0]-uy[0]*HALF*t, c[1]-uy[1]*HALF*t]);
      ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]);
      ctx.lineTo(d[0],d[1]); ctx.lineTo(e[0],e[1]); ctx.closePath();
    }
    ctx.fill();
    ctx.globalAlpha=1;
  }

  /* ЗАЛИВКА ДОБИВАЕТСЯ БАТЧАМИ, А НЕ ЗА ОДИН КАДР. Бюджет кусков на кадр
     ограничен, устаревшие кадры отменяются токеном — та же дисциплина, что в
     renderProgressive/renderToken референса, и именно она снимает зависание:
     раньше один вызов досчитывал сотни тысяч кусков синхронно. */
  function paint(progressive){
    const my=++rtok.v;
    if(raf){ cancelAnimationFrame(raf); raf=null; }
    const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
    ctx.clearRect(0,0,W,H);
    if(blend<1) paintCells(1-blend);
    if(blend<=0) return;
    const w=deepWalk(ctx,vp,W,H,
      {alpha:blend, color:cssVar('--acc'), margin:MARGIN, px:1.5});
    if(!progressive || REDUCED){
      // без анимации: бюджет всё равно ограничен, но крупнее — кадр один
      for(let k=0;k<24 && !w.step(20000);k++);
      return;
    }
    const frame=()=>{
      if(my!==rtok.v) return;                    // кадр устарел — не досчитываем
      if(w.step(28000)){ raf=null; return; }
      raf=requestAnimationFrame(frame);
    };
    raf=requestAnimationFrame(frame);
  }

  /* ── зум: лог-интерполяция viewport, как в FractalSlide ── */
  async function goto(target, targetZoom){
    tok.v++; const my=tok;
    const from={...vp}, fromZ=shown;
    if(REDUCED){ vp=target; zoom=targetZoom; shown=targetZoom; paint(false); return; }
    /* ⚠ КАДР ПОЛЁТА СТОИТ ФИКСИРОВАННО. Куски крупные (px 6) И бюджет жёсткий
       (9 000 кусков на кадр): раньше здесь стоял полный синхронный обход на
       каждом кадре полёта, и это — вторая половина зависания. */
    await anim(0,1,760,e=>{
      vp={ xMin:lerp(from.xMin,target.xMin,e), xMax:lerp(from.xMax,target.xMax,e),
           yMin:lerp(from.yMin,target.yMin,e), yMax:lerp(from.yMax,target.yMax,e) };
      shown=Math.exp(lerp(Math.log(fromZ),Math.log(targetZoom),e));
      const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
      ctx.clearRect(0,0,W,H);
      if(blend<1) paintCells(1-blend);
      if(blend>0) deepWalk(ctx,vp,W,H,
        {alpha:blend, color:cssVar('--acc'), margin:MARGIN, px:6}).step(9000);
    }, my);
    if(my.v!==tok.v) return;
    vp=target; zoom=targetZoom; shown=targetZoom; paint(true);
  }

  async function toCloud(){
    if(blend>=1) return;
    t=1; inT.value=100;
    tok.v++; const my=tok;
    if(REDUCED){ blend=1; paint(false); return; }
    await anim(0,1,520,v=>{ blend=v; paint(false); }, my);
    blend=1; paint(true);
  }

  function zoomAt(fx, fy){                  // fx,fy — доля холста, куда целимся
    const xs=vp.xMax-vp.xMin, ys=vp.yMax-vp.yMin;
    const cx=vp.xMin+xs*fx, cy=vp.yMax-ys*fy;
    const nx=xs/ZF, ny=ys/ZF;
    return {xMin:cx-nx/2, xMax:cx+nx/2, yMin:cy-ny/2, yMax:cy+ny/2};
  }

  inT.addEventListener('input',()=>{
    t=+inT.value/100;
    if(blend>0){ blend=0; zoom=1; shown=1; vp={...HOME}; }
    paint(false);
  });
  segR.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    segR.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));
    n=+b.dataset.v; paint(false);
  });
  segZ.addEventListener('click',async e=>{
    const b=e.target.closest('button'); if(!b) return;
    if(b.dataset.v==='reset'){ blend=0; t=+inT.value/100; vp={...HOME}; zoom=1; shown=1;
      paint(false); return; }
    if(b.dataset.v==='out'){
      if(zoom<=1.01) return;
      const xs=vp.xMax-vp.xMin, ys=vp.yMax-vp.yMin;
      const cx=(vp.xMin+vp.xMax)/2, cy=(vp.yMin+vp.yMax)/2;
      const z=Math.max(1, zoom/ZF);
      if(z<=1.01){ await goto({...HOME},1); return; }
      await goto({xMin:cx-xs*ZF/2,xMax:cx+xs*ZF/2,yMin:cy-ys*ZF/2,yMax:cy+ys*ZF/2}, z);
      return;
    }
    await toCloud();
    // «в край»: центрируемся на настоящей точке границы (см. normMap.edge)
    const E=normMap(n).edge;
    const xs=(vp.xMax-vp.xMin)/ZF, ys=(vp.yMax-vp.yMin)/ZF;
    await goto({xMin:E[0]-xs/2, xMax:E[0]+xs/2,
                yMin:E[1]-ys/2, yMax:E[1]+ys/2}, zoom*ZF);
  });

  /* зум-курсор и зум по клику — прямо из референса */
  const cur=document.createElement('div');
  cur.style.cssText='position:absolute;pointer-events:none;display:none;z-index:5;'+
    'border:1px solid color-mix(in srgb, var(--acc) 80%, white);'+
    'background:color-mix(in srgb, var(--acc) 10%, transparent);';
  fig.style.position='relative'; fig.appendChild(cur);
  cv.addEventListener('mousemove',ev=>{
    const r=cv.getBoundingClientRect();
    const w=r.width/ZF, h=r.height/ZF;
    const x=Math.max(w/2,Math.min(r.width-w/2, ev.clientX-r.left));
    const y=Math.max(h/2,Math.min(r.height-h/2, ev.clientY-r.top));
    cur.style.width=w+'px'; cur.style.height=h+'px';
    cur.style.left=(x-w/2)+'px'; cur.style.top=(y-h/2)+'px';
    cur.style.display='block'; cv.style.cursor='none';
  });
  cv.addEventListener('mouseleave',()=>{ cur.style.display='none'; cv.style.cursor=''; });
  cv.addEventListener('click',async ev=>{
    const r=cv.getBoundingClientRect();
    await toCloud();
    await goto(zoomAt((ev.clientX-r.left)/r.width, (ev.clientY-r.top)/r.height), zoom*ZF);
  });

  onResize(()=>paint(false));
  return {
    enter(){
      /* ⚠ ПРИ REDUCED НАДО ДОВЕСТИ ДО КОНЕЧНОГО КАДРА, А НЕ ПРОСТО НЕ АНИМИРОВАТЬ.
         Раньше здесь был выход до отрисовки, и сцена оставалась на t=0 — то есть
         линией, тогда как весь её смысл в том, что линия становится заливкой.
         Читатель с выключенной анимацией видел ровно противоположное тому, что
         утверждает заголовок «У линии есть площадь». §2.5 захода требует именно
         «мгновенно доводит анимации до конечного кадра». Поймано прогоном под
         reduced_motion, которого верификатор не делал. */
      if(REDUCED){ if(t<0.02){ t=1; inT.value=100; } paint(false); return; }
      paint(true);
      if(t>0.02) return;
      tok.v++; const my=tok;
      pause(500,my).then(ok=>{ if(!ok) return;
        anim(0,1,2000,v=>{ t=v; inT.value=Math.round(v*100); paint(false); }, my); });
    },
    leave(){ tok.v++; rtok.v++; if(raf){ cancelAnimationFrame(raf); raf=null; } }
  };
}

/* ═══════════════════════ каркас страницы ═══════════════════════ */

const FACTORY = { cover:sceneCover, strip:sceneStrip, draw:sceneDraw,
  cross:sceneCross, proof:sceneProof, four:sceneFour, area:sceneArea };

/** сцена → её листалка шагов; заполняет sceneProof, читает клавиатура */
const PAGERS = new Map();

/* ПЕРЕХОД МЕЖДУ СЦЕНАМИ — МГНОВЕННЫЙ. Плавного снап-скролла из референса тут
   больше нет сознательно (Д2): прокат в секунду на каждый шаг читался как
   задержка, а сам снап ловил читателя посреди сцены и утаскивал.
   Осталось три входа, и все три дают один и тот же мгновенный прыжок:
   стрелка-кнопка внизу сцены, клавиши ↓/↑, точки навигации справа. */
function setupJump(sections){
  function jumpTo(id){
    const el=document.getElementById(id); if(!el) return;
    window.scrollTo(0, el.offsetTop);            // behavior по умолчанию 'auto' — без анимации
  }
  /** текущая сцена: та, чей верх последним прошёл треть экрана */
  function current(){
    const y=window.pageYOffset + window.innerHeight*0.35;
    let cur=sections[0];
    for(const s of sections) if(s.offsetTop<=y) cur=s;
    return cur;
  }
  function step(d){
    const i=sections.indexOf(current());
    jumpTo(sections[Math.min(sections.length-1, Math.max(0, i+d))].id);
  }
  document.querySelectorAll('[data-goto]').forEach(b=>
    b.addEventListener('click', ()=>jumpTo(b.dataset.goto)));
  return { jumpTo, step, current };
}

/* Клавиатура: ↓/↑ — сцена вперёд/назад, ←/→ — шаг внутри сцены, если у неё
   есть листалка. Ползунки не отбираем: пока фокус на range, стрелки его. */
function setupKeys(api){
  document.addEventListener('keydown', e=>{
    if(e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
    const t=e.target, tag=(t && t.tagName || '').toLowerCase();
    if(tag==='input' || tag==='textarea' || tag==='select') return;
    if(document.querySelector('.deeper[data-open="true"]')) return;
    if(e.key==='ArrowDown' || e.key==='PageDown'){ e.preventDefault(); api.step(1); }
    else if(e.key==='ArrowUp' || e.key==='PageUp'){ e.preventDefault(); api.step(-1); }
    else if(e.key==='ArrowRight' || e.key==='ArrowLeft'){
      const p=PAGERS.get(api.current()); if(!p) return;
      e.preventDefault(); p.go(e.key==='ArrowRight' ? 1 : -1);
    }
  });
}

function setupPanels(){
  const back=document.getElementById('backdrop');
  const panels=[...document.querySelectorAll('.deeper')];
  function sync(p){
    if(window.innerWidth<=720){
      p.style.left=''; p.style.width='';
      p.style.removeProperty('--panel-x'); p.style.removeProperty('--panel-pad');
      return;
    }
    const host=document.querySelector('[data-open="'+p.id+'"]');
    const col=host && host.closest('.col');
    if(!col) return;
    const r=col.getBoundingClientRect();
    p.style.left=r.left+'px';
    p.style.width=(r.width+44)+'px';
    p.style.setProperty('--panel-x', r.left+'px');
    p.style.setProperty('--panel-pad','44px');
  }
  function close(){
    panels.forEach(p=>{ p.dataset.open='false'; p.setAttribute('aria-hidden','true'); });
    back.dataset.open='false';
  }
  document.querySelectorAll('[data-open]').forEach(b=>{
    b.addEventListener('click',()=>{
      const p=document.getElementById(b.dataset.open); if(!p) return;
      close(); sync(p);
      p.dataset.open='true'; p.setAttribute('aria-hidden','false');
      back.dataset.open='true';
      const c=p.querySelector('.deeper__close'); if(c) c.focus();
    });
  });
  panels.forEach(p=>p.querySelector('.deeper__close')
    .addEventListener('click',close));
  back.addEventListener('click',close);
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') close(); });
  window.addEventListener('resize',()=>panels.forEach(p=>{
    if(p.dataset.open==='true') sync(p); }));
}

function setupNav(sections, api){
  const nav=document.getElementById('nav');
  const items=sections.filter(s=>s.dataset.nav || s.id==='s0');
  items.forEach(s=>{
    const b=document.createElement('button');
    b.dataset.target=s.id;
    const sp=document.createElement('span');
    sp.textContent=s.dataset.nav || 'Начало';
    b.appendChild(sp);
    b.addEventListener('click',()=>api.jumpTo(s.id));
    nav.appendChild(b);
  });
  function mark(){
    const y=window.pageYOffset+window.innerHeight*0.4;
    let cur=items[0];
    for(const s of items) if(s.offsetTop<=y) cur=s;
    nav.querySelectorAll('button').forEach(b=>
      b.classList.toggle('on', b.dataset.target===cur.id));
  }
  window.addEventListener('scroll',mark,{passive:true});
  mark();
}

function boot(){
  const sections=[...document.querySelectorAll('[data-scene]')];
  const api=setupJump(sections);
  setupPanels();
  setupNav(sections, api);
  setupKeys(api);

  /* Анимация стартует по въезду и ГЛОХНЕТ при уходе: иначе восемь холстов
     молотят одновременно. Это же и требование §2.5. */
  const live=new Map();
  const io=new IntersectionObserver(es=>{
    for(const e of es){
      const sec=e.target, inst=live.get(sec);
      if(!inst) continue;
      if(e.isIntersecting){ sec.classList.add('is-in'); inst.enter(); }
      else { inst.leave(); }
    }
  }, {threshold:0.15});

  for(const sec of sections){
    const f=FACTORY[sec.dataset.scene];
    if(!f) continue;
    let inst;
    try { inst=f(sec); }
    catch(err){ console.error('сцена '+sec.dataset.scene+': '+err.message); continue; }
    live.set(sec, inst);
    io.observe(sec);
  }
  document.documentElement.dataset.ready='1';
}

if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
