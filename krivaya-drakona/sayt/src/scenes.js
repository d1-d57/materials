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
  strip: 0.16, halves: 0.16, pairs: 0.20,
  dense: 0.50,                       // предмет сцены: в касании читаются две дуги
  a: 0.13,                           // должно быть видно, что звенья вдоль и поперёк
  b: 0.26, v: 0.20, g: 0.24,
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
function rowBands(par, g, box){
  const x0=g([box.x0-0.6, 0])[0], x1=g([box.x1+0.6, 0])[0];
  for(let y=Math.floor(box.y0); y<=Math.ceil(box.y1); y++){
    if(!rowBlue(y)) continue;
    const top=g([0,y+0.5])[1], bot=g([0,y-0.5])[1];
    mk('rect',{x:Math.min(x0,x1), y:Math.min(top,bot),
               width:Math.abs(x1-x0), height:Math.abs(bot-top), class:'d-row'},par);
  }
}

/** стрелка хода в середине звена — без неё «налево» не имеет смысла */
function arrowOn(par, p, q, cls){
  const mx=(p[0]+q[0])/2, my=(p[1]+q[1])/2;
  const l=Math.hypot(q[0]-p[0], q[1]-p[1]) || 1;
  const ux=(q[0]-p[0])/l, uy=(q[1]-p[1])/l, nx=-uy, ny=ux;
  const t=Math.min(7, l*0.3), b=t*0.62;
  mk('polygon',{class:cls||'d-arrow', points:
    (mx+ux*t)+','+(my+uy*t)+' '+
    (mx-ux*t*0.6+nx*b)+','+(my-uy*t*0.6+ny*b)+' '+
    (mx-ux*t*0.6-nx*b)+','+(my-uy*t*0.6-ny*b)},par);
}

/** число по-русски: запятая, а не точка. В тексте сцены 7 уже стоит «1,5236»,
    и точка в строке состояния рядом читается как другое число. */
function num(x, d){ return x.toFixed(d).replace('.', ','); }

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
  const outAngle = sec.querySelector('[data-out="angle"]');
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
    outAngle.textContent = a + '°';
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
  const svg = sec.querySelector('svg');
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

/* ═══════════════════════ 3 · ЗВЕНЬЯ ПАРАМИ ═══════════════════════
   Основа — T20 (845–900). Красим через одно на ранге 4; при складывании из
   одного звена выходят два звена ЕГО цвета, поэтому цвет звена k ранга n —
   это цвет его прапрародителя: floor(k / 2^(n−4)) mod 2. Отсюда «цвета идут
   парами» — не факт, который надо принять, а след построения.
   Размер держим постоянным (seg = 2^(−n/2)): тогда видно, что звено СГИБАЕТСЯ
   ПОПОЛАМ, а не что фигура растёт. */

function scenePairs(sec){
  const svg = sec.querySelector('svg');
  const out = sec.querySelector('[data-out="pairs"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const LO=4, HI=10;
  const cache={}, frames=[];
  for(let n=LO;n<=HI;n++){
    cache[n]=poly(word(n), 90, Math.pow(2,-n/2));
    frames.push(...cache[n]);
  }
  const frame = bounds(frames);
  let n=LO, tok={v:0};

  function draw(){
    wipe(svg);
    const P=cache[n];
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:64},frame);
    const S=P.map(g);
    const blk = Math.pow(2, n-LO);                    // длина одноцветного куска
    const lw = n>=9 ? 2 : (n>=7 ? 2.8 : 4);
    let i=0;
    while(i < S.length-1){
      const c = Math.floor(i/blk) % 2;
      let j=i;
      while(j < S.length-1 && Math.floor(j/blk)%2 === c) j++;
      const run = S.slice(i, j+1);
      mk('path',{d:roundPath(run,ROUND.pairs), class: c? 'd-acc':'d-line',
                 'stroke-width':lw},svg);
      i=j;
    }
    node(svg, S[0], 'd-node-a', 4.5);
    if(out) out.innerHTML='ранг <b>'+n+'</b> · звеньев <b>'+Math.pow(2,n)
      +'</b> · подряд одного цвета <b>'+blk+'</b>';
  }
  async function loop(){
    tok.v++; const my=tok;
    if(REDUCED){ n=HI; draw(); return; }
    for(;;){
      for(n=LO;n<=HI;n++){ draw(); if(!await pause(n===LO?900:620, my)) return; }
      if(!await pause(500, my)) return;
      for(n=HI;n>=LO;n--){ draw(); if(!await pause(n===HI?900:620, my)) return; }
      if(!await pause(500, my)) return;
    }
  }
  onResize(draw);
  return { enter(){ loop(); }, leave(){ tok.v++; } };
}

/* ═══════════════════════ 4 · ПЛОТНОСТЬ ═══════════════════════
   Ранг 12 крупно, углы скруглены ЗАМЕТНО: в местах касания должны читаться две
   отдельные дуги, а не перекрёсток. Число касаний считается по ЛОМАНОЙ (целые
   вершины) — по скруглённому виду считать нельзя (урок touches в L4). */

function sceneDense(sec){
  const cv = sec.querySelector('canvas');
  const out = sec.querySelector('[data-out="dense"]');
  const seg = sec.querySelector('[data-seg="rank"]');
  let n=12, ctx, W, H, raf=null;
  const cache={};
  function pts(k){ return cache[k] || (cache[k]=rank(k)); }

  function paint(progressive){
    if(raf){ cancelAnimationFrame(raf); raf=null; }
    const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
    const P=pts(n);
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:Math.min(W,H)*0.05});
    const S=P.map(g);
    const lw = n>=13 ? 1.05 : (n>=12 ? 1.5 : (n>=10 ? 2.2 : 3.2));
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle=cssVar('--acc'); ctx.lineWidth=lw; ctx.lineCap='round';
    const total=S.length-1;
    const run=(upto)=>{
      ctx.clearRect(0,0,W,H);
      strokeRounded(ctx, S.slice(0, upto+1), 0.5);      // скругление = половина звена
    };
    if(!progressive || REDUCED){ run(total); }
    else {
      let done=0; const B=Math.max(120, Math.round(total/120));
      const step=()=>{ done=Math.min(total, done+B); run(done);
        if(done<total) raf=requestAnimationFrame(step); else raf=null; };
      raf=requestAnimationFrame(step);
    }
    const t=touches(word(n)).length;
    out.innerHTML='ранг <b>'+n+'</b> · звеньев <b>'+Math.pow(2,n)
      +'</b> · вершин, где линия подходит к себе: <b>'+t+'</b>';
  }
  seg.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(x=>x.classList.toggle('on', x===b));
    n=+b.dataset.v; paint(true);
  });
  onResize(()=>paint(false));
  return { enter(){ paint(true); }, leave(){ if(raf){cancelAnimationFrame(raf); raf=null;} } };
}

/* ═══════════════════════ 5 · ДОКАЗАТЕЛЬСТВО ═══════════════════════ */

/* 5а. Вершины двух сортов. Наведение на вершину зажигает ВСЕ вершины её сорта.
       Пунктиром — прежняя кривая, и скруглён он тоже (правка по f5). */
function step5a(sec){
  const svg = sec.querySelector('[data-step="a"] svg');
  const out = sec.querySelector('[data-out="a"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const N=4;
  const P=rank(N), Q=mul1pi(rank(N-1));
  let sort=null;

  function draw(){
    wipe(svg);
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:64});
    lattice(svg,g,g.box,1);
    const S=P.map(g), T=Q.map(g);
    mk('path',{d:roundPath(T,ROUND.a),class:'d-dash'},svg);   // прежняя кривая, скруглена так же
    mk('path',{d:roundPath(S,ROUND.a),class:'d-line','stroke-width':2.6},svg);
    for(let i=0;i<S.length-1;i++) arrowOn(svg,S[i],S[i+1],'d-arrow');
    const seen=new Set();
    P.forEach((p,i)=>{
      const k=p[0]+','+p[1]; if(seen.has(k)) return; seen.add(k);
      const black=isBlack(p);
      const on = sort!==null && sort===black;
      const el=node(svg, S[i], black ? 'd-node-b':'d-node', on?8:5.4);
      if(on) el.setAttribute('class', black?'d-node-a':'d-node');
      if(on && !black) el.style.setProperty('stroke', cssVar('--acc'));
      const hit=mk('circle',{cx:S[i][0],cy:S[i][1],r:17,class:'d-hit-dot'},svg);
      onHover(hit, ()=>{ sort=black; draw(); });
      hit.addEventListener('mouseleave',()=>{ sort=null; draw(); });
    });
    /* Праздная строка состояния — ЧИСЛА, а не приглашение навести мышь: подписи-инструкции
       с сайта убраны, но строка обязана оставаться живой и меняться, иначе
       читатель не поймёт, что вершины вообще откликаются. */
    if(sort===null){
      const seen2=new Set(); let nb=0, nn=0;
      for(const p of P){ const k=p[0]+','+p[1]; if(seen2.has(k)) continue;
        seen2.add(k); if(isBlack(p)) nb++; else nn++; }
      out.innerHTML='старых вершин <b>'+nb+'</b> · новых <b>'+nn+'</b>';
    } else out.innerHTML = sort
      ? '<span class="hi">старые вершины</span> — были на кривой раньше, лежат на пунктире'
      : '<span class="hi">новые вершины</span> — появились при последнем складывании';
  }
  onResize(draw);
  return { enter(){ draw(); }, leave(){} };
}

/* 5б. Строки двух цветов. Уголок красится по направлению поворота, и цвет
       уголка совпадает с цветом его строки. Стрелки хода обязательны:
       без них «налево» не имеет смысла (правка по f6). */
function step5b(sec){
  const svg = sec.querySelector('[data-step="b"] svg');
  const out = sec.querySelector('[data-out="b"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const N=6, P=rank(N), C=corners(P);
  let hi=null;

  function draw(){
    wipe(svg);
    const g=fit(P,{x:0,y:0,w:W,h:H,pad:56});
    rowBands(svg,g,g.box);
    lattice(svg,g,g.box,0);
    C.forEach(([a,b,c],k)=>{
      const tri=[a,b,c].map(g);
      const left=turnsLeft(a,b,c);
      const on = hi===k;
      mk('path',{d:roundPath(tri,ROUND.b), class: left?'d-acc2':'d-line',
                 'stroke-width': on?5:2.6},svg);
    });
    for(let i=0;i<P.length-1;i++){
      const a=g(P[i]), b=g(P[i+1]);
      if(g.s>18) arrowOn(svg,a,b,'d-arrow');
    }
    C.forEach(([a,b,c],k)=>{
      node(svg,g(a),'d-node-b',3.4);
      node(svg,g(b),'d-node',3.4);
      const hit=mk('path',{d:sharpD([a,b,c].map(g)),class:'d-hit'},svg);
      onHover(hit, ()=>{ hi=k; draw(); });
      hit.addEventListener('mouseleave',()=>{ hi=null; draw(); });
    });
    node(svg,g(P[P.length-1]),'d-node-b',3.4);
    if(hi===null) out.innerHTML='уголков <b>'+C.length+'</b>';
    else {
      const [a,b,c]=C[hi];
      out.innerHTML='излом в <b>'+(rowBlue(b[1])?'крашеной':'чистой')+'</b> строке · поворот '
        +'<span class="hi">'+(turnsLeft(a,b,c)?'налево':'направо')+'</span>';
    }
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
  const out = sec.querySelector('[data-out="v"]');
  const out4 = sec.querySelector('[data-out="v4"]');
  const W=1000, H=1000;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const N=6, P=rank(N);
  const CASES=[['гориз',true],['гориз',false],['вертик',true],['вертик',false]];
  const seen=new Set();
  let pick=null, fade=1, tok={v:0};

  function caseKey(r){ return (r.horiz?'гориз':'вертик')+(r.blue?'1':'0'); }

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
    report();
  }

  async function show(i){
    if(pick===i) return;
    pick=i; fade=1;
    const r=corner(P[i],P[i+1]);
    seen.add(caseKey(r));
    draw();
    tok.v++; const my=tok;
    if(REDUCED){ fade=0; draw(); return; }
    await anim(1,0,420,v=>{ fade=v; draw(); }, my);
  }

  function report(){
    if(pick===null){ out.innerHTML='звеньев <b>'+(P.length-1)+'</b>'; }
    else {
      const r=corner(P[pick],P[pick+1]);
      /* ⚠ СНАЧАЛА ПОВОРОТ, ПОТОМ НАПРАВЛЕНИЕ. Строка задаёт поворот НАЛЕВО или
         НАПРАВО — величину, не зависящую от того, куда едем. «Вверх» или
         «вниз» получается из поворота ВМЕСТЕ с направлением хода, поэтому в
         одном и том же случае (скажем, звено вдоль в крашеной строке) уголок
         честно идёт то вверх, то вниз. Проверено проходом по всем 64 звеньям.
         Первая версия печатала только «пошёл вверх / пошёл вниз», и читатель
         видел у одного случая два разных ответа — правило выглядело
         неработающим ровно там, где оно работает. */
      out.innerHTML='звено <b>'+(r.horiz?'вдоль':'поперёк')+'</b> — '
        +(r.half===0?'первая':'вторая')+' половина · строка <b>'
        +(r.blue?'крашеная':'чистая')+'</b> ⇒ поворот '
        +'<span class="hi">'+(r.blue?'налево':'направо')+'</span> · '
        +corDir(r);
    }
    /* Счётчик прогресса остался (все четыре случая должны быть достижимы и
       читатель должен видеть, что прошёл их), а перечисление случаев словами
       и слово-инструкция — убраны. */
    out4.innerHTML = 'пройдено <b'+(seen.size===4?' class="hi"':'')+'>'
      + seen.size + ' из ' + CASES.length + '</b>';
  }
  function corDir(r){
    const c=r.corner;
    if(r.half===0) return c[2][1] > c[1][1] ? 'пошёл вверх' : 'пошёл вниз';
    return c[0][0] < c[1][0] ? 'начался слева' : 'начался справа';
  }
  onResize(draw);
  return { enter(){ draw(); }, leave(){ tok.v++; } };
}

/* 5г. Ранг 6 и ранг 7 рядом. Звено k ранга 6 ⟷ уголок k ранга 7: чётные
       вершины ранга 7 — это ранг 6, умноженный на (1+i) (проверено гейтом).
       Связь двусторонняя: наводишь слева — горит справа, и наоборот. */
function step5g(sec){
  const svg = sec.querySelector('[data-step="g"] svg');
  const out = sec.querySelector('[data-out="g"]');
  const W=1000, H=750;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const A=rank(6), B=rank(7), CB=corners(B);
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
       ничего. Поймано скриншотом. Приглушение — прозрачностью, не цветом. */
    mk('path',{d:roundPath(SA,ROUND.g),class:'d-mute','stroke-width':2.2,opacity:0.62},svg);
    mk('path',{d:roundPath(SB,ROUND.g),class:'d-mute','stroke-width':1.8,opacity:0.62},svg);
    if(pick!==null){
      mk('path',{d:sharpD([SA[pick],SA[pick+1]]),class:'d-hot','stroke-width':6},svg);
      mk('path',{d:roundPath(CB[pick].map(gB),ROUND.g),class:'d-acc','stroke-width':5},svg);
      node(svg, gB(CB[pick][1]), 'd-node', 5.5);
    }
    for(let i=0;i<A.length-1;i++){
      const h=mk('line',{x1:SA[i][0],y1:SA[i][1],x2:SA[i+1][0],y2:SA[i+1][1],class:'d-hit'},svg);
      onHover(h, ()=>{ pick=i; draw(); });
    }
    CB.forEach((c,k)=>{
      const h=mk('path',{d:sharpD(c.map(gB)),class:'d-hit'},svg);
      onHover(h, ()=>{ pick=k; draw(); });
    });
    svg.addEventListener('mouseleave',()=>{ pick=null; draw(); },{once:true});
    out.innerHTML = pick===null
      ? 'звеньев слева '+(A.length-1)+' · уголков справа '+CB.length+' — их ровно столько же'
      : 'звено <b>'+(pick+1)+'</b> ранга 6 — это уголок <b>'+(pick+1)+'</b> ранга 7';
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
  const parts=[step5a(sec), step5b(sec), step5v(sec), step5g(sec)];
  const bodies=[...sec.querySelectorAll('.steps > .scene__body')];
  const dots=[...sec.querySelectorAll('.pager__dot')];
  let cur=0;

  function show(i){
    cur = Math.min(bodies.length-1, Math.max(0, i));
    bodies.forEach((b,k)=>b.classList.toggle('on', k===cur));
    dots.forEach((d,k)=>d.classList.toggle('on', k===cur));
    parts[cur].enter();
  }
  sec.querySelectorAll('[data-page]').forEach(b=>
    b.addEventListener('click', ()=>show(cur + (+b.dataset.page))));
  dots.forEach((d,k)=>d.addEventListener('click', ()=>show(k)));
  PAGERS.set(sec, { go(d){ show(cur+d); } });

  return { enter(){ show(cur); }, leave(){ parts.forEach(p=>p.leave()); } };
}

/* ═══════════════════════ 6 · ЧЕТЫРЕ ДРАКОНА ═══════════════════════
   Основа — T23 (1058–1090) и TB (1273–1289). Растут ОДНОВРЕМЕННО, все четыре,
   с ранга 4 до выбранного. Рамка считается сразу по всем четырём и по всем
   рангам — иначе камера прыгает при каждом шаге (урок T23 и TA). */

function sceneFour(sec){
  const svg = sec.querySelector('svg');
  const out = sec.querySelector('[data-out="four"]');
  const seg = sec.querySelector('[data-seg="rank"]');
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
    const lw = n>=10 ? 1.15 : (n>=8 ? 1.7 : (n>=6 ? 2.4 : 3.2));
    for(let r=0;r<4;r++){
      const S=rotAbout(P,[0,0],r*90).map(g);
      mk('path',{d:roundPath(S,ROUND.four), class:CLS[r], 'stroke-width':lw},svg);
    }
    node(svg,g([0,0]),'d-node-b',4.5);
    // общих отрезков — СЧИТАЕМ, а не утверждаем: это и есть предмет сцены
    const dup=sharedEdges(n);
    out.innerHTML='ранг <b>'+n+'</b> · звеньев у каждого <b>'+Math.pow(2,n)
      +'</b> · отрезков, взятых дважды: <b'+(dup?' class="hi"':'')+'>'+dup+'</b>';
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
function drawDeep(ctx, vp, W, H, o){
  const m=o.margin, iw=W-2*m, ih=H-2*m;
  const sx=iw/(vp.xMax-vp.xMin), sy=ih/(vp.yMax-vp.yMin);
  const PX = o.px || 1.15;
  ctx.globalAlpha = o.alpha===undefined ? 1 : o.alpha;
  ctx.fillStyle = o.color;
  // кусок = аффинное преобразование (a,b,c,d,e,f), приложенное к охвату
  let cur=[[1,0,0,1,0,0]], next=[], depth=0;
  const MAXD = o.maxDepth || 44;
  let drawn=0;
  while(cur.length && depth<MAXD){
    next.length=0;
    for(const T of cur){
      const [a,b,c,d,e,f]=T;
      // экранная рамка куска: образы четырёх углов охвата
      let X0=Infinity,X1=-Infinity,Y0=Infinity,Y1=-Infinity;
      for(const [ux,uy] of [[IFS_BOX.x0,IFS_BOX.y0],[IFS_BOX.x1,IFS_BOX.y0],
                            [IFS_BOX.x1,IFS_BOX.y1],[IFS_BOX.x0,IFS_BOX.y1]]){
        const wx=a*ux+b*uy+e, wy=c*ux+d*uy+f;
        const px=(wx-vp.xMin)*sx+m, py=H-m-(wy-vp.yMin)*sy;
        if(px<X0)X0=px; if(px>X1)X1=px; if(py<Y0)Y0=py; if(py>Y1)Y1=py;
      }
      if(X1<0||X0>W||Y1<0||Y0>H) continue;                 // вне окна — выбросить
      if(X1-X0<=PX && Y1-Y0<=PX){                          // мельче пикселя — залить
        ctx.fillRect(X0, Y0, Math.max(PX,X1-X0), Math.max(PX,Y1-Y0));
        drawn++;
        continue;
      }
      for(const t of IFS_DRAGON){                          // иначе — делить дальше
        next.push([ a*t.a+b*t.c, a*t.b+b*t.d,
                    c*t.a+d*t.c, c*t.b+d*t.d,
                    a*t.e+b*t.f+e, c*t.e+d*t.f+f ]);
      }
    }
    const tmp=cur; cur=next.slice(); next=tmp; depth++;
    if(cur.length > 900000) break;                         // страховка от разрастания
  }
  ctx.globalAlpha=1;
  return drawn;
}

function sceneArea(sec){
  const cv  = sec.querySelector('canvas');
  const fig = cv.parentNode;
  const out = sec.querySelector('[data-out="area"]');
  const outD= sec.querySelector('[data-out="dim"]');
  const outT= sec.querySelector('[data-out="thick"]');
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

  function paint(){
    if(raf){ cancelAnimationFrame(raf); raf=null; }
    const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
    ctx.clearRect(0,0,W,H);
    if(blend<1) paintCells(1-blend);
    if(blend>0) drawDeep(ctx,vp,W,H,
      {alpha:blend, color:cssVar('--acc'), margin:MARGIN});
    readout();
  }

  function readout(){
    outT.textContent = t<0.02 ? 'линия' : (t>=0.995 ? 'полклетки' : Math.round(t*100)+'%');
    const cells=Math.pow(2,n);
    /* В облаке ранг уже не тот, что на ползунке: измельчение идёт до пикселя,
       то есть «складываем дальше». Врать про ранг 12 здесь нельзя. */
    out.innerHTML = blend>0.5
      ? 'складываем дальше · ранг <b>→ ∞</b> · увеличение <span class="hi">×'
        + num(shown,1) + '</span>'
      : 'ранг <b>'+n+'</b> · клеток <b>'+cells+'</b> · площадь <b>'
        + (cells/2) + '</b> клеток';
    const b=dragBoundary(n).length, pb=dragBoundary(n-1).length;
    const r=b/pb, d=Math.log(r)/Math.log(Math.SQRT2);
    outD.innerHTML='сторон края <b>'+b+'</b> · длиннее прежнего в <b>'+num(r,3)
      +'</b> раза ⇒ изрезанность <span class="hi">'+num(d,4)+'</span>';
  }

  /* ── зум: лог-интерполяция viewport, как в FractalSlide ── */
  async function goto(target, targetZoom){
    tok.v++; const my=tok;
    const from={...vp}, fromZ=shown;
    if(REDUCED){ vp=target; zoom=targetZoom; shown=targetZoom; paint(); return; }
    /* На кадрах полёта измельчаем грубее (px 3), на финальном — до пикселя:
       иначе каждый кадр стоит как готовая картинка и полёт дёргается. */
    await anim(0,1,760,e=>{
      vp={ xMin:lerp(from.xMin,target.xMin,e), xMax:lerp(from.xMax,target.xMax,e),
           yMin:lerp(from.yMin,target.yMin,e), yMax:lerp(from.yMax,target.yMax,e) };
      shown=Math.exp(lerp(Math.log(fromZ),Math.log(targetZoom),e));
      const c=setupCanvas(cv); ctx=c.ctx; W=c.w; H=c.h;
      ctx.clearRect(0,0,W,H);
      if(blend<1) paintCells(1-blend);
      if(blend>0) drawDeep(ctx,vp,W,H,
        {alpha:blend, color:cssVar('--acc'), margin:MARGIN, px:3});
      readout();
    }, my);
    if(my.v!==tok.v) return;
    vp=target; zoom=targetZoom; shown=targetZoom; paint();
  }

  async function toCloud(){
    if(blend>=1) return;
    t=1; inT.value=100;
    tok.v++; const my=tok;
    if(REDUCED){ blend=1; paint(); return; }
    await anim(0,1,520,v=>{ blend=v; paint(); }, my);
    blend=1; paint();
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
    paint();
  });
  segR.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    segR.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));
    n=+b.dataset.v; paint();
  });
  segZ.addEventListener('click',async e=>{
    const b=e.target.closest('button'); if(!b) return;
    if(b.dataset.v==='reset'){ blend=0; t=+inT.value/100; vp={...HOME}; zoom=1; shown=1;
      paint(); return; }
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

  onResize(()=>paint());
  return {
    enter(){
      paint();
      if(REDUCED || t>0.02) return;
      tok.v++; const my=tok;
      pause(500,my).then(ok=>{ if(!ok) return;
        anim(0,1,2000,v=>{ t=v; inT.value=Math.round(v*100); paint(); }, my); });
    },
    leave(){ tok.v++; if(raf){ cancelAnimationFrame(raf); raf=null; } }
  };
}

/* ═══════════════════════ каркас страницы ═══════════════════════ */

const FACTORY = { cover:sceneCover, strip:sceneStrip, halves:sceneHalves,
  pairs:scenePairs, dense:sceneDense, proof:sceneProof, four:sceneFour, area:sceneArea };

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
