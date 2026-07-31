/* ═══════════════════════════════════════════════════════════════════════════
   dragon.js — ЕДИНСТВЕННАЯ геометрия дракона на сайте.

   Ядро перенесено из krivaya-drakona/L4/L4-razbory.html:121–281 (эталон
   razbor/gen_ill.py). В репозитории геометрия написана девять раз; десятой
   быть не должно, поэтому весь сайт считает только через этот файл, а
   остальные восемь копий обслуживают листки курса и не трогаются.

   Что добавлено сверх порта:
     · dragCells / dragBoundary — из L4:1214–1235 (сцена 7);
     · corner() — восстановление уголка по одному звену (сцена 5в).
       Правило выведено из parent_edge() в gen_ill.py и проверено численно
       ДО написания сцены: ранги 2..14, 32 764 звена, 0 расхождений.
       Ключ вывода: в gen_ill.py sum(div(w)) тождественно равно ординате w,
       поэтому «чётность узла» из питона — это ровно «чётность строки».
   ═══════════════════════════════════════════════════════════════════════════ */
'use strict';

/* ─────────────────────────── слово дракона ─────────────────────────── */

function flip(s){ let r=''; for(let i=s.length-1;i>=0;i--) r+=(s[i]==='L'?'R':'L'); return r; }

function word(n, choices){ const ch=choices||Array(n).fill('L'); let s='';
  for(let i=0;i<n;i++) s = s + ch[i] + flip(s); return s; }

function wordByFolds(f){ return word(f.length, f.slice().reverse()); }   // порядок word() обратный

function v2(k){ let r=0; while(k%2===0){ k/=2; r++; } return r; }

/** на каком складывании родился сгиб номер p у дракона ранга n */
function birthStep(n,p){ return n - v2(p); }

/* ─────────────────────────── ломаная ─────────────────────────── */

/** ломаная при ПРОИЗВОЛЬНЫХ углах сгибов: ang[k] — угол k-го сгиба в градусах.
    При всех углах 0 это прямая полоска, при 90 — сама кривая дракона. Одна и
    та же функция, а не два разных рисунка: этим и показано разгибание. */
function polyAngles(w, ang, seg){
  const L=seg||1; let x=L,y=0,dx=L,dy=0; const out=[[0,0],[L,0]];
  for(let i=0;i<w.length;i++){
    const s=(w[i]==='L')?1:-1, a=(ang[i+1]||0)*Math.PI/180*s;
    const co=Math.cos(a), si=Math.sin(a);
    const nx=dx*co-dy*si, ny=dx*si+dy*co;
    dx=nx; dy=ny; x+=dx; y+=dy; out.push([x,y]);
  }
  return out;
}

function poly(w, a, seg){ const o={}; for(let p=1;p<=w.length;p++) o[p]=(a===undefined?90:a);
  return polyAngles(w,o,seg); }

/** ломаная ранга n ЦЕЛЫМИ координатами — самый частый вызов на сайте.
    ⚠ ОКРУГЛЕНИЕ ЗДЕСЬ ОБЯЗАТЕЛЬНО, А НЕ ДЛЯ КРАСОТЫ. polyAngles крутит cos/sin,
    и при 90° вершина выходит не (0,1), а (6.1e-17, 1). Любое рассуждение о
    сорте вершины, о чётности строки и о том, горизонтально ли звено, на таких
    числах ЛОЖНО: `a[1]===b[1]` не срабатывает, `%2` даёт мусор. Это поймал
    гейт ядра — до округления он показал 21 811 расхождений в правиле уголка из
    32 764 звеньев и перекос 37/6/18/3 вместо 16/16/16/16 в четырёх случаях
    сцены 5в. Тот же урок, что в L4 про touches: скругление и углы — это ВИД,
    считать по нему нельзя, счёт идёт по целой ломаной. */
function rank(n){ return poly(word(n)).map(p=>[Math.round(p[0]), Math.round(p[1])]); }

/** привести вершину к целой решётке: страховка на входе всех правил ниже */
function lat(p){ return [Math.round(p[0]), Math.round(p[1])]; }

function rot90(P,k){ let R=P; for(let i=0;i<(k%4);i++) R=R.map(p=>[-p[1],p[0]]); return R; }

/** поворот набора точек вокруг центра на deg */
function rotAbout(P, c, deg){
  const a=deg*Math.PI/180, co=Math.cos(a), si=Math.sin(a);
  return P.map(([x,y])=>{ const dx=x-c[0], dy=y-c[1];
    return [c[0]+dx*co-dy*si, c[1]+dx*si+dy*co]; });
}

function keyShape(w){
  const P=poly(w).map(p=>[Math.round(p[0]),Math.round(p[1])]); let best=null;
  for(const rf of [false,true]){ const Q=rf?P.map(p=>[p[0],-p[1]]):P;
    for(let k=0;k<4;k++){ const R=rot90(Q,k);
      for(const rv of [false,true]){ const S=rv?R.slice().reverse():R; const [x0,y0]=S[0];
        const t=S.map(p=>(p[0]-x0)+','+(p[1]-y0)).join(' '); if(best===null||t<best) best=t; } } }
  return best;
}

/** касания — по ЛОМАНОЙ (целые вершины). Скругление это ВИД: считать по нему нельзя. */
function touches(w){
  const m=new Map();
  for(const p of poly(w)){ const k=Math.round(p[0])+','+Math.round(p[1]); m.set(k,(m.get(k)||0)+1); }
  return [...m.entries()].filter(e=>e[1]>1).map(e=>e[0].split(',').map(Number));
}

/** умножение на (1+i): растяжение в √2 и поворот на 45°.
    Переводит ломаную ранга n−1 ровно в ЧЁТНЫЕ вершины ломаной ранга n
    (проверено до ранга 14) — это и есть «прежняя кривая» пунктиром. */
function mul1pi(P){ return P.map(([x,y])=>[x-y, x+y]); }

/* ───────────────── два сорта вершин и уголок (сцена 5) ─────────────────
   Определения — те же слова, что в лекции, и больше их значение не меняется:
     чёрная вершина — была на кривой до последнего складывания;
     новая вершина  — появилась при нём;
     уголок         — кусок кривой между двумя соседними чёрными вершинами.  */

/** чёрная (старая) вершина ⟺ чётная сумма координат ⟺ чётный индекс на ломаной */
function isBlack(p){ const q=lat(p); return ((q[0]+q[1]) % 2 + 2) % 2 === 0; }

/** строка «голубая» ⟺ её номер чётный. Красим через одну, начиная с нулевой. */
function rowBlue(y){ const r=Math.round(y); return ((r % 2) + 2) % 2 === 0; }

/** ПРАВИЛО ВОССТАНОВЛЕНИЯ. По ОДНОМУ звену a→b уголок определён однозначно.
      · звено горизонтальное — это первая половина, излом = b, уголок пойдёт вверх/вниз;
      · звено вертикальное  — это вторая половина, излом = a, уголок начался слева/справа.
    Куда именно — говорит цвет строки излома: голубая → поворот НАЛЕВО, белая → НАПРАВО.
    Возвращает {half, izlom, corner, other, horiz, blue}, где corner — выбранный уголок
    [p0, излом, p2], а other — тот кандидат, который гаснет. */
function corner(a0, b0){
  const a = lat(a0), b = lat(b0);                      // считаем ТОЛЬКО по целым
  const horiz = a[1] === b[1];
  const izlom = horiz ? b : a;
  const blue  = rowBlue(izlom[1]);
  if(horiz){
    const dx = b[0]-a[0];
    const dy = blue ? dx : -dx;                        // налево ⟺ dx·dy > 0
    return { half:0, horiz:true, blue, izlom,
             corner:[a, b, [b[0], b[1]+dy]],
             other: [a, b, [b[0], b[1]-dy]] };
  }
  const dy = b[1]-a[1];
  const dx = blue ? dy : -dy;
  return { half:1, horiz:false, blue, izlom,
           corner:[[a[0]-dx, a[1]], a, b],
           other: [[a[0]+dx, a[1]], a, b] };
}

/** уголки ломаной: уголок номер k — это звенья 2k и 2k+1 */
function corners(P){ const out=[];
  for(let k=0;k+2<P.length;k+=2) out.push([lat(P[k]),lat(P[k+1]),lat(P[k+2])]);
  return out; }

/** поворачивает ли уголок налево (по знаку векторного произведения) */
function turnsLeft(a,b,c){ return (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0]) > 0; }

/* ───────────────── область дракона и её граница (сцена 7) ─────────────────
   Порт L4:1214–1235. Клетка — квадрат на звене как на диагонали, площадь ½.
   Ключ клетки — удвоенная середина звена, поэтому ключи целые. */

/** ПРОВЕРЕНО до ранга 14: плитки не налезают, то есть это ровно область дракона. */
function dragCells(n){
  const w=word(n); let x=0,y=0,dx=1,dy=0; const C=[];
  for(let i=0;i<Math.pow(2,n);i++){
    C.push([2*x+dx, 2*y+dy]);
    x+=dx; y+=dy;
    if(i<w.length){ const t=dx; if(w[i]==='L'){ dx=-dy; dy=t; } else { dx=dy; dy=-t; } }
  }
  return C;
}

/** ПРОВЕРЕНО ГЕОМЕТРИЕЙ: две клетки делят сторону ⟺ ключи отличаются на (±1,±1).
    Считать соседей через (±2,0) неверно — там квадраты касаются лишь УГЛОМ. */
const NB=[[1,1],[1,-1],[-1,1],[-1,-1]];
function dragBoundary(n){
  const C=dragCells(n), S=new Set(C.map(c=>c[0]+','+c[1])), out=[];
  for(const [p,q] of C){
    const cx=p/2, cy=q/2;
    for(const [a,b] of NB) if(!S.has((p+a)+','+(q+b)))
      out.push([[cx+a*0.5, cy], [cx, cy+b*0.5]]);
  }
  return out;
}

/** Сколько отрезков решётки берут на себя ДВА разных дракона из четырёх.
    Сцена 6 утверждает «ни повтора, ни дырки» — и это число не вписывается
    руками, а считается на месте: ключ отрезка — упорядоченная пара вершин,
    поэтому общий отрезок даёт ровно одно совпадение. Ноль на экране означает
    «проверено сейчас», а не «так было написано». */
function sharedEdges(n){
  const P=rank(n), seen=new Set(); let dup=0;
  for(let r=0;r<4;r++){
    const Q=rotAbout(P,[0,0],r*90).map(lat);
    for(let i=0;i+1<Q.length;i++){
      const a=Q[i], b=Q[i+1];
      const k = (a[0]<b[0] || (a[0]===b[0] && a[1]<b[1]))
        ? a[0]+','+a[1]+'|'+b[0]+','+b[1]
        : b[0]+','+b[1]+'|'+a[0]+','+a[1];
      if(seen.has(k)) dup++; else seen.add(k);
    }
  }
  return dup;
}

/** клетка как ромб: полдиагонали в каждую сторону от центра.
    t — насколько звено «растолстело»: 0 — сама линия, 1 — полная клетка. */
function cellQuad(key, t){
  const cx=key[0]/2, cy=key[1]/2, h=(t===undefined?1:t)*0.5;
  return [[cx-0.5,cy],[cx,cy+h],[cx+0.5,cy],[cx,cy-h]];
}

/* ─────────────────────────── экранная кухня ─────────────────────────── */

/** целые вершины → экранные, с сохранением пропорций и центровкой в боксе.
    Возвращает функцию g; g.s — сколько пикселей в одной клетке.
    common задаёт общую рамку на несколько кадров: тогда камера не прыгает. */
function fit(P, b, common){
  const pad=b.pad===undefined?26:b.pad;
  let x0,x1,y0,y1;
  if(common){ ({x0,x1,y0,y1}=common); }
  else { const xs=P.map(p=>p[0]), ys=P.map(p=>p[1]);
    x0=Math.min(...xs); x1=Math.max(...xs); y0=Math.min(...ys); y1=Math.max(...ys); }
  const s=Math.min((b.w-2*pad)/Math.max(x1-x0,1e-6),(b.h-2*pad)/Math.max(y1-y0,1e-6));
  const ox=b.x+pad+((b.w-2*pad)-s*(x1-x0))/2, oy=b.y+pad+((b.h-2*pad)-s*(y1-y0))/2;
  const g=p=>[ox+(p[0]-x0)*s, b.y+b.h-(oy-b.y)-(p[1]-y0)*s];
  g.s=s; g.box={x0,x1,y0,y1}; return g;
}

/** рамка по набору точек — чтобы посчитать её один раз и держать */
function bounds(P){
  const xs=P.map(p=>p[0]), ys=P.map(p=>p[1]);
  return {x0:Math.min(...xs), x1:Math.max(...xs), y0:Math.min(...ys), y1:Math.max(...ys)};
}

function sharpD(P){ return 'M '+P.map(p=>p[0].toFixed(2)+' '+p[1].toFixed(2)).join(' L '); }

/** ПРИМИТИВ: угол → дуга. f — доля звена, уходящая в скругление (0..0.5).
    Скругление это ВИД: ни одно утверждение по нему не считается. */
function roundPath(P, f){
  const k=(f===undefined?0.5:f); let d='';
  if(P.length<3) return sharpD(P);
  d+='M '+P[0][0].toFixed(2)+' '+P[0][1].toFixed(2);
  for(let i=1;i<P.length-1;i++){
    const u=P[i-1], v=P[i], w=P[i+1];
    const a=[v[0]-u[0], v[1]-u[1]], b=[w[0]-v[0], w[1]-v[1]];
    const la=Math.hypot(a[0],a[1]), lb=Math.hypot(b[0],b[1]);
    const cross=a[0]*b[1]-a[1]*b[0];
    if(Math.abs(cross)<1e-9||la<1e-9||lb<1e-9) continue;
    const c=Math.min(la*k, lb*k), sw=cross>0?1:0;
    const p1=[v[0]-a[0]/la*c, v[1]-a[1]/la*c], p2=[v[0]+b[0]/lb*c, v[1]+b[1]/lb*c];
    d+=' L '+p1[0].toFixed(2)+' '+p1[1].toFixed(2);
    d+=' A '+c.toFixed(2)+' '+c.toFixed(2)+' 0 0 '+sw+' '+p2[0].toFixed(2)+' '+p2[1].toFixed(2);
  }
  const L=P[P.length-1];
  d+=' L '+L[0].toFixed(2)+' '+L[1].toFixed(2);
  return d;
}

/** то же скругление, но на canvas: arcTo делает ровно дугу между двумя звеньями */
function strokeRounded(ctx, P, f){
  const k=(f===undefined?0.5:f);
  ctx.beginPath();
  if(P.length<2) return;
  ctx.moveTo(P[0][0], P[0][1]);
  for(let i=1;i<P.length-1;i++){
    const u=P[i-1], v=P[i], w=P[i+1];
    const la=Math.hypot(v[0]-u[0], v[1]-u[1]), lb=Math.hypot(w[0]-v[0], w[1]-v[1]);
    const r=Math.min(la*k, lb*k);
    if(r<0.2){ ctx.lineTo(v[0], v[1]); continue; }
    ctx.arcTo(v[0], v[1], w[0], w[1], r);
  }
  const L=P[P.length-1];
  ctx.lineTo(L[0], L[1]);
  ctx.stroke();
}

/* ─────────────────────────── время ─────────────────────────── */

const ease=t=> t<.5 ? 2*t*t : 1-Math.pow(-2*t+2,2)/2;
const easeOutQuart=t=> 1-Math.pow(1-t,4);
function lerp(a,b,t){ return a+(b-a)*t; }

/** анимация from→to за ms. Возвращает промис; отмена — через token-объект:
    если tok.v изменился, кадры перестают идти и промис разрешается сразу.
    Без этого уехавшая со экрана сцена продолжает молотить (восемь холстов). */
function anim(from,to,ms,step,tok){
  const mark = tok ? tok.v : null;
  return new Promise(res=>{ const t0=performance.now();
    (function fr(now){
      if(tok && tok.v!==mark){ res(false); return; }
      const t=Math.min(1,(now-t0)/ms); step(from+(to-from)*ease(t));
      if(t<1) requestAnimationFrame(fr); else res(true);
    })(t0); });
}

function pause(ms,tok){
  const mark = tok ? tok.v : null;
  return new Promise(r=>setTimeout(()=>r(!tok || tok.v===mark), ms));
}

const REDUCED = typeof matchMedia==='function'
  && matchMedia('(prefers-reduced-motion: reduce)').matches;
