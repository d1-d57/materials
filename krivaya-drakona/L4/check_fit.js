/* ГЕЙТ ПОСАДКИ — запускать после каждой правки вкладок:
 *     node L4/check_fit.js L4/L4-razbory.html
 *
 * Зачем он есть. Браузера в песочнице нет, а растризатор (`render_svg.js` → convert) НЕ РИСУЕТ
 * ТЕКСТ: буквы выходят гигантскими пятнами. То есть глазами проверяется только геометрия, а
 * буквы — предмет этих вкладок — не проверяются ничем. Этот гейт закрывает дыру числом:
 * прогоняет каждую вкладку по всем шагам и меряет, что нарисовано.
 *
 * Ловит ровно те два дефекта, на которых курс уже горел (gen_l2_figs.py, 17.07):
 *   1) ПОСАДКА  — что-то уехало за сцену и молча обрезалось рамкой;
 *   2) МЕТКИ    — две подписи сели друг на друга (вершины 7 и 11 ранга 4 — одна точка).
 *
 * Чего он НЕ ловит: кегль, гарнитуру, реальный вид. Это глазами, в браузере.
 */
const fs=require('fs'), path=process.argv[2];
const html=fs.readFileSync(path,'utf8');
const js=html.split('<script>')[1].split('</script>')[0];
const VBW=1400, VBH=620, MARGIN=6, MINGAP=17;   // MINGAP — кегль буквы 21px: ближе значит слипнутся

function mk(tag){
  const e={ tagName:tag, children:[], attrs:{}, _text:'', style:{}, dataset:{}, listeners:{},
    classList:{ _s:new Set(), add(...c){c.forEach(x=>this._s.add(x));},
      remove(...c){c.forEach(x=>this._s.delete(x));},
      toggle(c,f){ f===undefined ? (this._s.has(c)?this._s.delete(c):this._s.add(c)) : (f?this._s.add(c):this._s.delete(c)); },
      contains(c){return this._s.has(c);} },
    appendChild(c){ this.children.push(c); return c; },
    setAttribute(k,v){ this.attrs[k]=v; }, getAttribute(k){ return this.attrs[k]; },
    addEventListener(t,f){ (this.listeners[t]=this.listeners[t]||[]).push(f); },
    click(){ (this.listeners.click||[]).forEach(f=>f({preventDefault(){}})); },
    querySelector(){ return mk('div'); }, querySelectorAll(){ return []; },
    get textContent(){ return this._text; }, set textContent(v){ this._text=v; this.children=[]; },
    get innerHTML(){ return this._html||''; }, set innerHTML(v){ this._html=v; this.children=[]; },
    set className(v){ this._cn=v; }, get className(){ return this._cn||''; },
    set id(v){ this._id=v; }, get id(){ return this._id; },
    set hidden(v){ this._h=v; }, get hidden(){ return this._h; } };
  return e;
}
const byId={};
global.document={ getElementById(id){ return byId[id] || (byId[id]=mk('div')); },
  createElement:mk, createElementNS:(ns,t)=>mk(t), querySelectorAll(){ return []; },
  get title(){return this._t;}, set title(v){ this._t=v; } };
global.window=global; global.performance={now:()=>Date.now()};
global.requestAnimationFrame=f=>{ f(Date.now()+1e9); };   // анимацию домотать до конца
global.addEventListener=()=>{}; global.matchMedia=()=>({matches:false});
global.setTimeout=(f)=>{ f(); return 0; };
console.log=()=>{};                                        // самопроверку страницы глушим

/* ⚠ ГЕЙТ КЛАССОВ. Класс, который используется в скрипте, но не объявлен в <style>, ничего не
   ломает: элемент просто рисуется как попало (у path это чёрная заливка вместо обводки). Оба
   прежних гейта такое пропускали — поймано на слиянии, где вместе с чужим файлом уехали
   объявления `.s-fill` и `.s-area`, и область дракона стала чёрным пятном. */
{
  const css=html.split('<style>')[1].split('</style>')[0];
  const decl=new Set([...css.matchAll(/\.(s-[a-z0-9-]+)\{/g)].map(m=>m[1]));
  const used=new Set([...js.matchAll(/'(s-[a-z0-9-]+)'/g)].map(m=>m[1]));
  const miss=[...used].filter(c=>!decl.has(c));
  if(miss.length){
    console.log('ГЕЙТ КЛАССОВ ПРОВАЛЕН: используются, но не объявлены — '+miss.join(', '));
    process.exit(1);
  }
  process.stdout.write(`  ✓ классы: объявлено ${decl.size}, использовано ${used.size}, потерянных нет\n`);
}

eval(js+'\n;global.__TABS=TABS; global.__show=show;');
const log=(...a)=>process.stdout.write(a.join(' ')+'\n');
const TABS=global.__TABS, show=global.__show;
const bad=[]; let maxT=0;

/** РАЗБОР `d` С УЧЁТОМ ОТНОСИТЕЛЬНЫХ КОМАНД.
 *  ⚠ Первая версия читала все числа подряд парами и объявляла стрелку («M x,y l-4,9 8,0 z»)
 *  уехавшей за сцену: −4 и 9 это СМЕЩЕНИЯ, а не координаты. Тот же класс ошибки, что «гейт,
 *  который ругается по неверной причине» (17.07). У дуги `A rx ry rot laf sf x y` конец — только
 *  последняя пара, остальные пять чисел координатами не являются. */
function pathPts(d){
  const tk=d.match(/[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?/g)||[];
  const out=[]; let i=0, cmd='', x=0, y=0, sx=0, sy=0;
  const num=()=>parseFloat(tk[i++]);
  while(i<tk.length){
    if(/[A-Za-z]/.test(tk[i])) cmd=tk[i++];
    const rel=(cmd===cmd.toLowerCase()), c=cmd.toUpperCase();
    if(c==='Z'){ x=sx; y=sy; continue; }
    if(c==='M'||c==='L'||c==='T'){ const a=num(), b=num();
      x = rel?x+a:a; y = rel?y+b:b; if(c==='M'){ sx=x; sy=y; } }
    else if(c==='H'){ const a=num(); x = rel?x+a:a; }
    else if(c==='V'){ const a=num(); y = rel?y+a:a; }
    else if(c==='A'){ num();num();num();num();num(); const a=num(), b=num();
      x = rel?x+a:a; y = rel?y+b:b; }
    else if(c==='C'){ num();num();num();num(); const a=num(), b=num();
      x = rel?x+a:a; y = rel?y+b:b; }
    else if(c==='Q'||c==='S'){ num();num(); const a=num(), b=num();
      x = rel?x+a:a; y = rel?y+b:b; }
    else { i++; continue; }
    out.push([x,y]);
  }
  return out;
}
/** точки, за которые отвечает элемент: для проверки посадки этого достаточно */
function pts(n){
  const a=n.attrs, N=k=>parseFloat(a[k]);
  if(n.tagName==='circle') return [[N('cx')-N('r'),N('cy')-N('r')],[N('cx')+N('r'),N('cy')+N('r')]];
  if(n.tagName==='line')   return [[N('x1'),N('y1')],[N('x2'),N('y2')]];
  if(n.tagName==='rect')   return [[N('x'),N('y')],[N('x')+N('width'),N('y')+N('height')]];
  if(n.tagName==='text')   return [[N('x'),N('y')]];
  if(n.tagName==='path') return pathPts(a.d||'');
  return [];
}
function walk(n,out){ out.push(n); n.children.forEach(c=>walk(c,out)); return out; }

/* ⚠ ШАГИ ЖДЁМ. Вкладки 17, 18, 20, 21 асинхронные: без await гейт мерил бы состояние ДО
   анимации и поздние шаги не проверялись бы вовсе — «гейт, который проходит, ничего не
   проверив». requestAnimationFrame здесь домотан до конца, так что ожидание мгновенное. */
(async()=>{
for(const t of TABS){
  const idx=TABS.indexOf(t);
  /* ранги берём из самой вкладки (`ranks`), а не из списка в гейте: иначе гейт проверял бы
     не то, что предлагает переключатель, и молча пропускал бы старший ранг — а слипаются
     буквы именно там, где их больше всего. */
  for(const n of (t.ranks || [t.n])){
  for(let step=0; step<=6; step++){
    show(idx);
    if(t.ranks){ t.n=n; t.mount(); }
    for(let s=0;s<step;s++) if(t.space) await t.space();
    const nodes=walk(byId['stage'],[]).filter(n=>n.tagName!=='div');
    // 1 — посадка
    /* ⚠ ФОН МОЖЕТ ВЫХОДИТЬ ЗА КАДР, СОДЕРЖИМОЕ — НЕТ. Рамки боксов (`s-box`) чертятся вплотную
       к краю сцены, а клетчатая бумага (`s-grid`) нарочно продолжается за неё и обрезается
       браузером — так задумано на вкладках «Линейка», «Все ранга 4», «Касания». Первая версия
       требовала поля от всего подряд и валилась на файле, который давно показан на проекторе.
       Смысл гейта — «содержимое молча не обрезалось», а не «ничего не касается края». */
    const BG = n => n.attrs.class==='s-grid' || n.attrs.class==='s-box' || n.tagName==='rect';
    for(const n of nodes){
      if(BG(n)) continue;
      const m = MARGIN;
      for(const p of pts(n)){
        if(!isFinite(p[0])||!isFinite(p[1])) { bad.push(`вкл.${t.num} шаг ${step}: <${n.tagName}> координата NaN`); continue; }
        if(p[0]<m||p[0]>VBW-m||p[1]<m||p[1]>VBH-m)
          bad.push(`вкл.${t.num} шаг ${step}: <${n.tagName}> уехал за сцену (${p[0].toFixed(0)},${p[1].toFixed(0)})`);
      }
    }
    // 2 — метки друг на друге
    const T=nodes.filter(n=>n.tagName==='text')
      .map(n=>({x:parseFloat(n.attrs.x), y:parseFloat(n.attrs.y), s:n._text}));
    for(let i=0;i<T.length;i++) for(let j=i+1;j<T.length;j++){
      const d=Math.hypot(T[i].x-T[j].x, T[i].y-T[j].y);
      if(d<MINGAP) bad.push(`вкл.${t.num} шаг ${step}: метки «${T[i].s}» и «${T[j].s}» слиплись (зазор ${d.toFixed(1)} < ${MINGAP})`);
    }
    /* 3 — ПУСТОЙ КАДР. Вкладка, открывающаяся в ничто, выглядит как сломанная, а гейт живости
       её пропускает: скрипт-то отработал. Поймано на вкладке 22 (первый кадр рисовался только
       со второго шага). Пустым не должен быть ни один шаг, до которого можно дожать пробелом. */
    if(nodes.length===0) bad.push(`вкл.${t.num} шаг ${step}: кадр ПУСТОЙ — рисовать нечего`);
    if(step===0) log(`  вкл.${t.num} «${t.title}»${t.ranks?' ранг '+n:''}: элементов ${nodes.length}, меток ${T.length}`);
    maxT=Math.max(maxT,T.length);
  }
  }
}
const uniq=[...new Set(bad)];
log(uniq.length ? '\nГЕЙТ ПОСАДКИ ПРОВАЛЕН:\n  '+uniq.slice(0,20).join('\n  ')
                : `\nГЕЙТ ПОСАДКИ ПРОЙДЕН — всё внутри сцены, метки не слиплись (максимум меток в кадре ${maxT})`);
process.exit(uniq.length?1:0);
})();
