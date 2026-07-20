/* СНИМОК ВКЛАДКИ В SVG — чтобы посмотреть глазами без браузера.
 *     node L4/render_svg.js L4/L4-razbory.html <num> <шагов> > /tmp/t.svg
 *
 * Зачем он есть. В песочнице нет браузера (playwright/wkhtmltoimage не встают), а `check_page.js`
 * проверяет, что скрипт жив, но НЕ что видно. Здесь тот же мок DOM, только узлы копят атрибуты
 * и текст, а в конце дерево <svg> печатается как файл — дальше `convert` даёт PNG.
 *
 * Чего он НЕ ловит: реальные шрифты страницы (в SVG уезжают классы, стили подставляются здесь
 * вручную), CSS-раскладку вне <svg>, анимацию. Ловит главное: посадку, налезание, обрезку рамкой.
 */
const fs=require('fs'), path=process.argv[2];
const NUM=parseInt(process.argv[3]||'17',10), STEPS=parseInt(process.argv[4]||'0',10);
const html=fs.readFileSync(path,'utf8');
const js=html.split('<script>')[1].split('</script>')[0];

/* ⚠ РАСТРИЗАТОР НЕ ЗНАЕТ CSS-ПЕРЕМЕННЫХ. Со `stroke:var(--ink)` он молча роняет ВЕСЬ блок стилей,
   и снимок выходит с чёрной заливкой вместо обводки — «гейт, который врёт красивее, чем молчит».
   Поэтому переменные подставляем значениями здесь, а в самой странице оставляем канон (цвет
   только классом). Берём лишь правила `.s-*`: разметка вне <svg> в снимке не нужна. */
const cssRaw=html.split('<style>')[1].split('</style>')[0];
const vars={};
for(const m of cssRaw.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;}]+)/g)) vars[m[1]]=m[2].trim();
const css=[...cssRaw.matchAll(/(\.s-[a-z0-9-]+)\s*\{([^}]*)\}/g)]
  .map(m=>m[1]+'{'+m[2].replace(/var\((--[a-z0-9-]+)\)/g,(_,v)=>vars[v]||'#000')+'}')
  .join('\n');

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
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
    querySelector(){ return mk('div'); }, querySelectorAll(){ return []; },
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
function ser(n){
  if(n.tagName==='#text') return esc(n._text);
  const a=Object.entries(n.attrs).map(([k,v])=>` ${k}="${esc(v)}"`).join('');
  const inner=n.children.map(ser).join('') + (n._text?esc(n._text):'');
  return `<${n.tagName}${a}>${inner}</${n.tagName}>`;
}
const byId={};
global.document={
  getElementById(id){ return byId[id] || (byId[id]=mk('div')); },
  createElement:mk, createElementNS:(ns,t)=>mk(t),
  querySelectorAll(){ return []; },
  get title(){return this._t;}, set title(v){ this._t=v; },
};
global.window=global; global.performance={now:()=>Date.now()};
/* анимация проматывается МГНОВЕННО в конечное состояние: снимок — это кадр после шага */
global.requestAnimationFrame=f=>{ f(Date.now()+1e9); };
global.addEventListener=()=>{};
global.matchMedia=()=>({matches:false});
global.setTimeout=(f)=>{ f(); return 0; };
/* самопроверка страницы печатает в stdout — уводим в stderr, иначе она попадёт внутрь SVG */
console.log=(...a)=>process.stderr.write(a.join(' ')+'\n');

eval(js+'\n;global.__TABS=TABS; global.__show=show;');
const TABS=global.__TABS, show=global.__show;
const idx=TABS.findIndex(t=>t.num===NUM);
if(idx<0){ console.error('нет вкладки '+NUM); process.exit(1); }
/* ⚠ ШАГИ ЖДЁМ — иначе снимок врёт молча. Асинхронные вкладки ставят busy на время анимации и
   отбивают следующий пробел; без await получался кадр раннего шага, а выглядело как пустая
   вкладка. Ровно та же дыра, что чинилась в check_fit.js. */
(async()=>{
show(idx);
for(let i=0;i<STEPS;i++) if(TABS[idx].space) await TABS[idx].space();

const st=byId['stage'];
const capTxt=(byId['cap']._html||byId['cap']._text||'').replace(/<[^>]+>/g,'');
process.stdout.write(
 `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 700" width="1400" height="700">`
 +`<style>${css}</style><rect x="0" y="0" width="1400" height="700" fill="#fff"/>`
 + st.children.map(ser).join('')
 +`<text x="20" y="672" font-family="Helvetica" font-size="19" fill="#333">${esc(capTxt)}</text>`
 +`<text x="1380" y="672" text-anchor="end" font-family="Helvetica" font-size="15" fill="#8195ad">`
 +`вкладка ${NUM} · шагов ${STEPS}</text></svg>`);
})();
