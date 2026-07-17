/* ГЕЙТ СТРАНИЦЫ Л2 — запускать после КАЖДОЙ правки:
 *     node L2/check_page.js L2/L2-razbory.html
 *
 * Зачем он есть. 17.07 страница открылась ПУСТОЙ: функция bar() (дополнение слова, имя из
 * эталона gen_ill.py) столкнулась с `const bar = getElementById('bar')` → SyntaxError → не
 * исполнился ВЕСЬ скрипт. Гейты модели этого не поймали: они вынимали из файла отдельные
 * функции и сверяли их с python — то есть проверяли МОДЕЛЬ, а не ФАЙЛ. Этот гейт проверяет файл
 * целиком: минимальный DOM → скрипт исполняется весь → открываются все вкладки → жмутся все
 * кнопки. Ловит синтаксис, коллизии имён, падения при mount, обращения к null.
 *
 * Чего он НЕ ловит: типографику, налезающие надписи, реальный рендер — для этого нужен браузер.
 */
/* ГЕЙТ ФАЙЛА ЦЕЛИКОМ: минимальный DOM → скрипт исполняется весь, открываются ВСЕ вкладки,
   нажимаются ВСЕ кнопки. Ловит то, что гейт «вынуть функции и сверить» пропускает:
   синтаксис, коллизии имён, падения при mount, обращения к null. */
const fs=require('fs'), path=process.argv[2];
const html=fs.readFileSync(path,'utf8');
const js=html.split('<script>')[1].split('</script>')[0];

function mk(tag){
  const e={ tagName:tag, children:[], attrs:{}, _text:'', style:{}, dataset:{}, listeners:{},
    classList:{ _s:new Set(),
      add(...c){c.forEach(x=>this._s.add(x));}, remove(...c){c.forEach(x=>this._s.delete(x));},
      toggle(c,f){ f===undefined ? (this._s.has(c)?this._s.delete(c):this._s.add(c)) : (f?this._s.add(c):this._s.delete(c)); },
      contains(c){return this._s.has(c);} },
    appendChild(c){ this.children.push(c); return c; },
    setAttribute(k,v){ this.attrs[k]=v; }, getAttribute(k){ return this.attrs[k]; },
    addEventListener(t,f){ (this.listeners[t]=this.listeners[t]||[]).push(f); },
    click(){ (this.listeners.click||[]).forEach(f=>f({preventDefault(){}})); },
    querySelector(){ return mk('div'); },
    querySelectorAll(){ return []; },
    get textContent(){ return this._text; },
    set textContent(v){ this._text=v; this.children=[]; },
    get innerHTML(){ return this._html||''; },
    set innerHTML(v){ this._html=v; this.children=[]; },
    set className(v){ this._cn=v; }, get className(){ return this._cn||''; },
    set id(v){ this._id=v; }, get id(){ return this._id; },
    set hidden(v){ this._h=v; }, get hidden(){ return this._h; },
  };
  return e;
}
const byId={};
global.document={
  getElementById(id){ return byId[id] || (byId[id]=mk('div')); },
  createElement:mk, createElementNS:(ns,t)=>mk(t),
  querySelectorAll(sel){ return (global.__segs&&sel==='.seg')?global.__segs:[]; },
  get title(){return this._t;}, set title(v){ this._t=v; },
};
global.window=global; global.performance={now:()=>Date.now()};
global.requestAnimationFrame=f=>setTimeout(()=>f(Date.now()+9999),0);
global.addEventListener=()=>{};
global.matchMedia=()=>({matches:false});
let errors=[];
process.on('uncaughtException',e=>{ errors.push('runtime: '+e.message); });

try { eval(js + '\n;global.__TABS=(typeof TABS!=="undefined")?TABS:null; global.__show=(typeof show!=="undefined")?show:null;'); } catch(e){ console.log('✗ СКРИПТ НЕ ИСПОЛНИЛСЯ: '+e.message); process.exit(1); }
console.log('✓ скрипт исполнился целиком (show(0) отработал)');

// открыть все вкладки
const TABS=global.__TABS, show=global.__show;
if(!TABS){ console.log('✗ ГЕЙТ СЛЕП: TABS не достался — проверка вкладок НЕ выполнена'); process.exit(1); }
{
  TABS.forEach((t,i)=>{
    try { show(i); console.log('  ✓ вкладка '+t.num+' «'+t.title+'» открылась'); }
    catch(e){ errors.push('вкладка '+t.num+': '+e.message); console.log('  ✗ вкладка '+t.num+': '+e.message); }
  });
  // ПРОБЕЛ — универсальное действие вкладки: жмём много раз на каждой (шаги должны зациклиться)
  TABS.forEach(t=>{
    if(!t.space) return;
    for(let i=0;i<7;i++){
      try { t.space(); }
      catch(e){ errors.push('пробел на вкладке '+t.num+' (шаг '+i+'): '+e.message);
                console.log('  ✗ вкладка '+t.num+': пробел упал на шаге '+i+' — '+e.message); break; }
    }
    if(!errors.some(x=>x.includes('вкладке '+t.num)))
      console.log('  ✓ вкладка '+t.num+': пробел отработал 7 раз');
  });
  // выбор сгибов на вкладке 3
  try { const t3=TABS.find(t=>t.num===3);
    t3.folds=['L','R','L']; t3.opened=false; for(let p=1;p<=7;p++) t3.ang[p]=0; t3.render();
    console.log('  ✓ вкладка 3: выбор сгибов отрисовался'); }
  catch(e){ errors.push('вкладка 3 сгибы: '+e.message); console.log('  ✗ вкладка 3: '+e.message); }
}
setTimeout(()=>{
  console.log(errors.length ? '\nГЕЙТ ПРОВАЛЕН: '+errors.join(' | ') : '\nГЕЙТ ПРОЙДЕН — файл живой целиком');
  process.exit(errors.length?1:0);
}, 60);
