/* Движок занятий Миши. Вход: window.LESSON = {id, title, sections:[{title, items:[...]}]}.
   Типы пунктов: slots · choice · error · euler · grid (sudoku/futoshiki/takuzu) · cover.
   Состояние и журнал — localStorage, ключ "misha:<id>". Звёзды за всё время — "misha:stars". */
(function(){
"use strict";
const L=window.LESSON, KEY="misha:"+L.id, SKEY="misha:stars";
const $=(s,r=document)=>r.querySelector(s), el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;};
const norm=s=>String(s==null?"":s).trim().toLowerCase().replace(/ё/g,"е").replace(/\s+/g," ").replace(",",".");
const setNorm=s=>{const t=String(s).match(/\d+/g)||[];return [...new Set(t.map(Number))].sort((a,b)=>a-b).join(";");};
const same=(a,b)=>{const x=String(a).replace(/\s+/g,""),y=String(b).replace(/\s+/g,"");if(/^\d+$/.test(x)&&/^\d+$/.test(y))return Number(x)===Number(y);return norm(a)===norm(b);};
/* разложение a·b как (x1·y1 + x2·y2): общий множитель — одно из чисел, остальные в сумме дают другое */
const split=(v,A,B)=>{const P=[[v[0],v[1]],[v[2],v[3]]];for(const [f,g] of [[A,B],[B,A]]){for(const i of [0,1])for(const j of [0,1]){if(P[0][i]===f&&P[1][j]===f&&P[0][1-i]+P[1][1-j]===g&&P[0][1-i]>0&&P[1][1-j]>0)return true;}}return false;};
const now=()=>Date.now();

/* ---------- состояние ---------- */
let S; try{S=JSON.parse(localStorage.getItem(KEY)||"null")}catch(e){S=null}
if(!S||typeof S!=="object")S={pos:[0,0],it:{},ev:[],stars:0};
S.it=S.it||{};S.ev=S.ev||[];S.stars=S.stars||0;S.streak=S.streak||0;S.chest=S.chest||{};S.letters=S.letters||{};
let total=0;try{total=parseInt(localStorage.getItem(SKEY)||"0",10)||0}catch(e){}
/* лавка: копилка = всего заработано − потрачено; покупки общие для всех занятий */
let spent=0,bought=[];try{spent=parseInt(localStorage.getItem("misha:spent")||"0",10)||0;bought=JSON.parse(localStorage.getItem("misha:bought")||"[]")||[]}catch(e){}
const wallet=()=>Math.max(0,total-spent), has=id=>bought.includes(id);
function award(n,why){if(!n)return;S.stars+=n;total+=n;try{localStorage.setItem(SKEY,String(total))}catch(e){}log("bonus",{n,why});save();}
function buy(lk){if(has(lk.id)||wallet()<lk.price)return false;spent+=lk.price;bought.push(lk.id);try{localStorage.setItem("misha:spent",String(spent));localStorage.setItem("misha:bought",JSON.stringify(bought))}catch(e){}log("buy",{id:lk.id,price:lk.price,left:wallet()});return true;}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const log=(e,extra)=>{S.ev.push(Object.assign({t:now(),e,k:curKey()},extra||{}));save();};
const flat=[];L.sections.forEach((s,si)=>s.items.forEach((it,ii)=>flat.push({si,ii,it,k:si+"."+ii})));
const rec=k=>S.it[k]||(S.it[k]={att:0,st:"",v:null});

/* ---------- сцена ---------- */
const stage=el("div");stage.id="stage";document.body.appendChild(stage);
stage.innerHTML=`<header class="top"><div class="sec"></div><div class="prog"></div>
<div class="badge"></div><div class="fire"></div><div class="stars" title="звёзды">★ <b>0</b><small></small></div><button class="shopbtn" title="лавка">🛒</button><button class="skip" title="перейти к задаче">⏭</button></header>
<main></main>
<footer class="bot"><button class="prev" aria-label="назад">←</button><div class="dots"></div><button class="rst">↺ сбросить</button><button class="chk">✓ Проверить</button><button class="next" aria-label="дальше">→</button></footer>
<div class="toast"></div><div class="ov" hidden></div>`;
const main=$("main",stage), secEl=$(".sec",stage), prog=$(".prog",stage), dots=$(".dots",stage),
  bPrev=$(".prev",stage), bNext=$(".next",stage), bChk=$(".chk",stage), bRst=$(".rst",stage), ov=$(".ov",stage), toast=$(".toast",stage);
function scale(){const k=Math.min(innerWidth/1440,innerHeight/810);stage.style.transform=`scale(${k})`;
  stage.style.left=((innerWidth-1440*k)/2)+"px";stage.style.top=((innerHeight-810*k)/2)+"px";if(cur&&cur.fit)cur.fit();}
addEventListener("resize",scale);$(".badge",stage).textContent=L.badge||"";

/* ---------- подгонка содержимого под рабочую зону ---------- */
function fitter(work,inner,max){return ()=>{inner.style.transform="translate(-50%,-50%) scale(1)";
  const w=inner.scrollWidth,h=inner.scrollHeight,W=work.clientWidth,H=work.clientHeight;
  const k=Math.min(W/w,H/h,max||1.6);inner.style.transform=`translate(-50%,-50%) scale(${k})`;};}

/* ---------- слоты: {5}, {5|6}, {#2;8} множество, {?∈/⊂=∈} выбор, {_} свободное ---------- */
function renderLine(tpl,ctx){
  const ln=el("div","ln");const re=/\{([^}]*)\}/g;let last=0,m;
  while((m=re.exec(tpl))){ if(m.index>last)ln.appendChild(document.createTextNode(tpl.slice(last,m.index)));
    const body=m[1];
    if(body.startsWith("?")){const [opts,ok]=body.slice(1).split("=");const seg=el("span","seg");let val="";
      opts.split("/").forEach(o=>{const b=el("button","",o);b.type="button";b.onclick=()=>{val=o;[...seg.children].forEach(x=>x.classList.toggle("on",x===b));seg.classList.remove("bad","good");ctx.touch();};seg.appendChild(b);});
      ctx.slots.push({kind:"seg",node:seg,get:()=>val,set:v=>{val=v||"";[...seg.children].forEach(x=>x.classList.toggle("on",x.textContent===val));},ok:[ok]});
      ln.appendChild(seg);}
    else if(body==="_"||body==="__"){const i=el("input","slot free");i.style.width=body==="__"?"9ch":"4ch";i.oninput=ctx.touch;
      ctx.slots.push({kind:"free",node:i,get:()=>i.value,set:v=>i.value=v||""});ln.appendChild(i);}
    else {const isSet=body.startsWith("#");const oks=(isSet?body.slice(1):body).split("|");
      const i=el("input","slot");const len=Math.max(...oks.map(x=>x.length));i.style.width=(isSet?Math.max(6,len+3):Math.max(2.2,len+1.2))+"ch";
      i.inputMode=isSet?"text":"numeric";i.autocomplete="off";i.oninput=()=>{i.classList.remove("bad","good");ctx.touch();};
      ctx.slots.push({kind:isSet?"set":"val",node:i,get:()=>i.value,set:v=>i.value=v||"",ok:oks});ln.appendChild(i);}
    last=re.lastIndex;}
  if(last<tpl.length)ln.appendChild(document.createTextNode(tpl.slice(last)));
  return ln;}
function slotOk(s){const v=s.get(); if(s.kind==="free")return true; if(!String(v).trim())return false;
  if(s.kind==="set")return s.ok.some(o=>setNorm(o)===setNorm(v)); return s.ok.some(o=>same(o,v));}
function slotsFilled(sl){return sl.filter(s=>s.kind!=="free").every(s=>String(s.get()).trim());}
function markSlots(sl){let all=true;sl.forEach(s=>{if(s.kind==="free")return;const g=slotOk(s);all=all&&g;s.node.classList.toggle("bad",!g);s.node.classList.toggle("good",g);});return all;}

/* ---------- типы пунктов ---------- */
const T={};
T.slots=(it,box,ctx)=>{const lines=el("div","lines");(it.lines||[]).forEach(t=>lines.appendChild(renderLine(t,ctx)));
  const inner=el("div","fit");const hold=it.draft?el("div","drow"):inner;hold.appendChild(lines);if(it.draft)inner.appendChild(hold);
  if(it.draft){const d=el("div","draft");d.appendChild(el("div","lbl",it.draftLabel||""));
    for(let i=0;i<it.draft;i++){const x=el("input");x.oninput=ctx.touch;ctx.slots.push({kind:"free",node:x,get:()=>x.value,set:v=>x.value=v||""});d.appendChild(x);} hold.appendChild(d);}
  box.appendChild(inner);ctx.inner=inner;
  return {check(){if(!slotsFilled(ctx.slots))return null;
      if(it.rule){const v=ctx.slots.filter(s=>s.kind!=="free").map(s=>Number(String(s.get()).replace(/\s+/g,"")));const ok=!!Function("v","split","return ("+it.rule+")")(v,split);
        ctx.slots.forEach(s=>{if(s.kind!=="free"&&s.node.classList){s.node.classList.toggle("good",ok);s.node.classList.toggle("bad",!ok);}});return ok;}
      return markSlots(ctx.slots);},reset(){ctx.slots.forEach(s=>{s.set("");s.node.classList&&s.node.classList.remove("bad","good");});}};};
T.choice=(it,box,ctx)=>{const g=el("div","opts");g.style.gridTemplateColumns=`repeat(${it.cols||Math.min(it.options.length,3)},auto)`;
  const sel=new Set();const bs=it.options.map((o,i)=>{const b=el("button","opt",o);b.type="button";b.onclick=()=>{if(it.multi){sel.has(i)?sel.delete(i):sel.add(i);}else{sel.clear();sel.add(i);}
    bs.forEach((x,j)=>{x.classList.toggle("on",sel.has(j));x.classList.remove("good","bad");});ctx.touch();};g.appendChild(b);return b;});
  const inner=el("div","fit");inner.appendChild(g);
  const lines=el("div","lines");(it.lines||[]).forEach(t=>lines.appendChild(renderLine(t,ctx)));if(it.lines){lines.style.marginTop="30px";inner.appendChild(lines);}
  box.appendChild(inner);ctx.inner=inner;
  ctx.slots.push({kind:"free",node:{},get:()=>[...sel].join(","),set:v=>{sel.clear();String(v||"").split(",").filter(x=>x!=="").forEach(x=>sel.add(+x));bs.forEach((x,j)=>x.classList.toggle("on",sel.has(j)));}});
  return {check(){if(!sel.size||!slotsFilled(ctx.slots))return null;const ok=new Set(it.ok);
      let good=sel.size===ok.size&&[...sel].every(i=>ok.has(i));bs.forEach((b,j)=>{b.classList.remove("good","bad");if(sel.has(j))b.classList.add(ok.has(j)&&good?"good":"bad");});
      if(it.multi){good=good;} return markSlots(ctx.slots)&&good;},
    reset(){sel.clear();bs.forEach(b=>b.classList.remove("on","good","bad"));ctx.slots.forEach(s=>{if(s.node.classList){s.set("");s.node.classList.remove("bad","good");}});}};};
T.error=(it,box,ctx)=>{const inner=el("div","fit");const st=el("div","steps");let pick=-1;
  const bs=it.steps.map((s,i)=>{const b=el("button","step",(i===0&&it.who?`<span class="who">${it.who}:</span>`:"")+s);b.type="button";
    b.onclick=()=>{pick=i;bs.forEach((x,j)=>{x.classList.toggle("on",j===i);x.classList.remove("good");});ctx.touch();};st.appendChild(b);return b;});
  inner.appendChild(st);
  const lines=el("div","lines");(it.fix||[]).forEach(t=>lines.appendChild(renderLine(t,ctx)));inner.appendChild(lines);
  box.appendChild(inner);ctx.inner=inner;
  ctx.slots.push({kind:"free",node:{},get:()=>pick,set:v=>{pick=v==null||v===""?-1:+v;bs.forEach((x,j)=>x.classList.toggle("on",j===pick));}});
  return {check(){if(pick<0||!slotsFilled(ctx.slots))return null;const a=pick===it.wrong;bs[pick].classList.toggle("good",a);if(a)bs[pick].classList.remove("on");return markSlots(ctx.slots)&&a;},
    reset(){pick=-1;bs.forEach(b=>b.classList.remove("on","good"));ctx.slots.forEach(s=>{if(s.node.classList){s.set("");s.node.classList.remove("bad","good");}});}};};
/* fix: чужое решение, числа в строках правятся на месте, дальнейшие выкладки пересчитываются.
   Строка: [n] — правимое число (v0,v1,… по порядку), {выражение от v} — вычисляемое. Проверка: it.ok (выражение от v)
   и/или каждая строка, начинающаяся с «=», равна it.answer. */
const calc=src=>{const e=String(src).replace(/·/g,"*").replace(/:/g,"/").replace(/−/g,"-").replace(/[^0-9+\-*/(). ]/g,"");try{return Function("return ("+e+")")()}catch(_){return NaN}};
const shownum=x=>Number.isFinite(x)&&Math.abs(x-Math.round(x))<1e-9?String(Math.round(x)):"?";
T.fix=(it,box,ctx)=>{const inner=el("div","fit");const st=el("div","steps fixs");
  const init=[];it.steps.forEach(t=>{(t.match(/\[(\d+)\]/g)||[]).forEach(m=>init.push(+m.slice(1,-1)));});
  const v=init.slice();const comp=[];const rowsTxt=[];
  const rows=it.steps.map((t,ri)=>{const r=el("div","step fx");if(ri===0&&it.who)r.appendChild(el("span","who",it.who+":"));
    let k=0;const parts=t.split(/(\[\d+\]|\{[^}]+\})/);
    parts.forEach(pt=>{if(!pt)return;
      if(/^\[\d+\]$/.test(pt)){const idx=init.length?(()=>{let c=0;for(let q=0;q<ri;q++)c+=(it.steps[q].match(/\[\d+\]/g)||[]).length;return c+(k++);})():0;
        const inp=el("input","num");inp.value=v[idx];inp.inputMode="numeric";inp.style.width=Math.max(1.4,String(v[idx]).length+0.5)+"ch";
        inp.oninput=()=>{const x=inp.value.trim();v[idx]=x===""?NaN:+x;inp.style.width=Math.max(1.4,x.length+0.5)+"ch";inp.classList.toggle("ed",+x!==init[idx]);recompute();ctx.touch();};
        inp.onfocus=()=>inp.select();r.appendChild(inp);}
      else if(/^\{.+\}$/.test(pt)){const sp=el("span","cmp");sp._e=pt.slice(1,-1);comp.push(sp);r.appendChild(sp);}
      else r.appendChild(document.createTextNode(pt));});
    st.appendChild(r);return r;});
  function evalExpr(e){return calc(e.replace(/v(\d+)/g,(_,i)=>"("+v[+i]+")"));}
  function recompute(){comp.forEach(sp=>{const nv=shownum(evalExpr(sp._e));if(sp.textContent!==nv){if(sp.textContent)sp.classList.remove("flash"),void sp.offsetWidth,sp.classList.add("flash");sp.textContent=nv;}});}
  recompute();comp.forEach(sp=>sp.classList.remove("flash"));
  inner.appendChild(st);box.appendChild(inner);ctx.inner=inner;
  ctx.slots.push({kind:"free",node:{},get:()=>v.join(","),set:x=>{if(!x)return;String(x).split(",").forEach((y,i)=>{v[i]=+y;});
    st.querySelectorAll("input.num").forEach((inp,i)=>{inp.value=v[i];inp.classList.toggle("ed",v[i]!==init[i]);});recompute();}});
  const lineVal=r=>{let txt="";r.childNodes.forEach(n=>{if(n.classList&&n.classList.contains("who"))return;txt+=n.value!=null&&n.tagName==="INPUT"?n.value:n.textContent;});return txt;};
  return {check(){if(v.some(x=>!Number.isFinite(x)))return null;
      let ok=true;if(it.ok){ok=!!Function("v","split","return ("+it.ok+")")(v,split);}
      if(it.answer!=null)rows.forEach((r,ri)=>{const t=lineVal(r);const m=t.split("=");
        if(ri===0){const val=calc(m[0]);if(Number.isFinite(val)&&m.length===1)return;}
        const rhs=t.trim().startsWith("=")?m.slice(1):m.slice(1);rhs.forEach(seg=>{const val=calc(seg);if(Number.isFinite(val)&&Math.abs(val-it.answer)>1e-9)ok=false;});});
      rows.forEach(r=>r.classList.remove("good","on"));return ok;},
    reset(){init.forEach((x,i)=>v[i]=x);st.querySelectorAll("input.num").forEach((inp,i)=>{inp.value=v[i];inp.classList.remove("ed");inp.style.width=Math.max(1.4,String(v[i]).length+0.5)+"ch";});recompute();}};};
T.euler=(it,box,ctx)=>{const inner=el("div","fit");const row=el("div","row2");row.appendChild(el("div","euler",it.svg));
  const lines=el("div","lines");(it.lines||[]).forEach(t=>lines.appendChild(renderLine(t,ctx)));row.appendChild(lines);inner.appendChild(row);box.appendChild(inner);ctx.inner=inner;
  return {check(){if(!slotsFilled(ctx.slots))return null;return markSlots(ctx.slots);},reset(){ctx.slots.forEach(s=>{s.set("");s.node.classList&&s.node.classList.remove("bad","good");});}};};
/* pic: картина с прятками (mode find: метки-кружки, n предметов) или лабиринт (mode maze: путь по точкам).
   Проверяет Ваня глазами: долгое нажатие «Ваня проверил» → звёзды (find: по 1 за метку, не больше n; maze: it.stars||5). */
T.pic=(it,box,ctx)=>{const maze=it.mode==="maze";const wrap=el("div","picw");const fr=el("div","picf");const im=el("img");im.src=it.img;im.alt="";im.draggable=false;
  const sv=document.createElementNS("http://www.w3.org/2000/svg","svg");sv.setAttribute("viewBox","0 0 1000 1000");sv.setAttribute("preserveAspectRatio","none");sv.classList.add("marks");
  fr.appendChild(im);fr.appendChild(sv);wrap.appendChild(fr);
  const side=el("div","picside");const cnt=el("div","cnt");side.appendChild(cnt);
  const un=el("button","pbtn","↶ убрать");un.type="button";side.appendChild(un);
  const ok=el("button","pbtn vanya","Ваня проверил ✓");ok.type="button";side.appendChild(ok);
  const k=ctx.k;let pts=[];
  const draw=()=>{sv.style.cssText=`left:${im.offsetLeft}px;top:${im.offsetTop}px;width:${im.offsetWidth}px;height:${im.offsetHeight}px`;sv.innerHTML="";if(maze&&pts.length>1){const pl=document.createElementNS("http://www.w3.org/2000/svg","polyline");pl.setAttribute("points",pts.map(p=>p[0]*1000+","+p[1]*1000).join(" "));pl.setAttribute("class","path");sv.appendChild(pl);}
    pts.forEach((p,i)=>{const e=document.createElementNS("http://www.w3.org/2000/svg","ellipse");e.setAttribute("cx",p[0]*1000);e.setAttribute("cy",p[1]*1000);
      const r=maze?7:30;const ar=im.naturalWidth&&im.naturalHeight?im.naturalWidth/im.naturalHeight:1;e.setAttribute("rx",r/ar>r?r:r);e.setAttribute("ry",r*ar);e.setAttribute("class",maze?"pt":"ring");sv.appendChild(e);});
    cnt.innerHTML=maze?"":(it.n?`<b>${pts.length}</b> из ${it.n}`:`<b>${pts.length}</b>`);};
  fr.onclick=e=>{if(rec(k).st==="ok")return;const R=im.getBoundingClientRect();const x=(e.clientX-R.left)/R.width,y=(e.clientY-R.top)/R.height;if(x<0||x>1||y<0||y>1)return;
    pts.push([+x.toFixed(4),+y.toFixed(4)]);draw();ctx.touch();log("mark",{n:pts.length});};
  un.onclick=()=>{pts.pop();draw();ctx.touch();};
  let lp;ok.onpointerdown=()=>{ok.classList.add("hold");lp=setTimeout(()=>{ok.classList.remove("hold");const r=rec(k);if(r.st==="ok")return;
      const n=maze?(it.stars||3):(it.n?Math.floor(3*Math.min(pts.length,it.n)/it.n):Math.min(3,pts.length));r.att=1;r.st="ok";r.t1=now();award(n,maze?"лабиринт":"картина");say("+"+n+" ★",true);ok.textContent="✓ +"+n+" ★";paintNav();},1000);};
  ok.onpointerup=ok.onpointerleave=()=>{clearTimeout(lp);ok.classList.remove("hold");};
  im.onload=()=>{draw();cur&&cur.fit&&cur.fit();};
  box.appendChild(wrap);wrap.appendChild(side);
  ctx.slots.push({kind:"free",node:{},get:()=>JSON.stringify(pts),set:v=>{try{pts=JSON.parse(v)||[]}catch(e){pts=[]}draw();}});
  ctx.noCheck=true;draw();
  return {check(){return null},reset(){pts=[];draw();}};};
/* головоломки: sudoku (latin+boxes), futoshiki (latin+знаки), takuzu (●○) */
T.grid=(it,box,ctx)=>{const n=it.rows.length, tak=it.kind==="takuzu", vals=tak?[1,0]:[...Array(n)].map((_,i)=>i+1);
  const st=it.rows.map(r=>[...r].map(c=>c==="."?null:+c)), fixed=st.map(r=>r.map(v=>v!==null));
  let sel=null, brush=null; const undo=[];
  const show=v=>v===null?"":tak?`<span class="dot ${v?"b":"w"}"></span>`:String(v);
  const wrap=el("div","pz");const fut=it.kind==="futoshiki";const G=fut?2*n-1:n;
  const g=el("div","pgrid"+(fut?" fut":""));g.style.gridTemplateColumns=`repeat(${G},auto)`;
  const cells=[];const sign=(a,b)=>{for(const [x,y] of (it.ineq||[])){if(x[0]===a[0]&&x[1]===a[1]&&y[0]===b[0]&&y[1]===b[1])return "<";if(x[0]===b[0]&&x[1]===b[1]&&y[0]===a[0]&&y[1]===a[1])return ">";}return "";};
  const put=(i,j,v,noUndo)=>{if(fixed[i][j])return;if(!noUndo)undo.push([i,j,st[i][j]]);st[i][j]=v;cells[i][j].innerHTML=show(v);cells[i][j].classList.remove("bad");ctx.touch();};
  const pick=(i,j)=>{sel=[i,j];cells.flat().forEach(c=>c.classList.remove("sel"));cells[i][j].classList.add("sel");};
  for(let R=0;R<G;R++)for(let C=0;C<G;C++){
    if(!fut||(R%2===0&&C%2===0)){const i=fut?R/2:R,j=fut?C/2:C;(cells[i]=cells[i]||[]);
      const b=el("button","pc"+(fixed[i][j]?" fix":""),show(st[i][j]));b.type="button";
      if(it.kind==="sudoku"){const bs=Math.sqrt(n)|0;if((j+1)%bs===0&&j<n-1)b.classList.add("bR");if((i+1)%bs===0&&i<n-1)b.classList.add("bB");}
      b.onclick=()=>{if(fixed[i][j])return;pick(i,j);if(brush!==null)put(i,j,brush==="x"?null:brush);
        else{const cur=st[i][j];const k=cur===null?0:vals.indexOf(cur)+1;put(i,j,k>=vals.length?null:vals[k]);}};
      cells[i][j]=b;g.appendChild(b);}
    else if(R%2===0){g.appendChild(el("span","sg",sign([R/2,(C-1)/2],[R/2,(C+1)/2])));}
    else if(C%2===0){const t=sign([(R-1)/2,C/2],[(R+1)/2,C/2]);g.appendChild(el("span","sg",t==="<"?"∧":t===">"?"∨":""));}
    else g.appendChild(el("span","sg"));}
  const pal=el("div","pal");const pbs=[];
  vals.forEach(v=>{const b=el("button","",show(v));b.type="button";b.onclick=()=>{brush=brush===v?null:v;pbs.forEach(x=>x.classList.toggle("on",x._v===brush));};b._v=v;pbs.push(b);pal.appendChild(b);});
  const er=el("button","wide","стереть");er.type="button";er._v="x";er.onclick=()=>{brush=brush==="x"?null:"x";pbs.forEach(x=>x.classList.toggle("on",x._v===brush));};pbs.push(er);pal.appendChild(er);
  
  const un=el("button","wide","↶ отменить ход");un.type="button";un.onclick=()=>{const u=undo.pop();if(u)put(u[0],u[1],u[2],true);};pal.appendChild(un);
  wrap.appendChild(g);const side=el("div");side.appendChild(pal);if(it.rules)side.appendChild(el("div","rules",it.rules));wrap.appendChild(side);
  const inner=el("div","fit");inner.appendChild(wrap);box.appendChild(inner);ctx.inner=inner;ctx.maxScale=1.6;
  ctx.key=e=>{if(!sel)return false;const [i,j]=sel;
    if(/^Arrow/.test(e.key)){const d={ArrowUp:[-1,0],ArrowDown:[1,0],ArrowLeft:[0,-1],ArrowRight:[0,1]}[e.key];pick((i+d[0]+n)%n,(j+d[1]+n)%n);return true;}
    if(e.key==="Backspace"||e.key==="Delete"||e.key==="0"&&!tak){put(i,j,null);return true;}
    if(tak){if(e.key==="1"||e.key.toLowerCase()==="ч"||e.key.toLowerCase()==="b"){put(i,j,1);return true;}if(e.key==="0"||e.key.toLowerCase()==="б"||e.key.toLowerCase()==="w"){put(i,j,0);return true;}}
    else{const v=+e.key;if(v>=1&&v<=n){put(i,j,v);return true;}}return false;};
  ctx.slots.push({kind:"free",node:{},get:()=>st.map(r=>r.map(v=>v===null?".":v).join("")).join("/"),set:v=>{if(!v)return;v.split("/").forEach((r,i)=>[...r].forEach((c,j)=>{if(!fixed[i][j]){st[i][j]=c==="."?null:+c;cells[i][j].innerHTML=show(st[i][j]);}}));}});
  return {check(){if(st.some(r=>r.some(v=>v===null)))return null;
      const line=a=>tak?(a.filter(x=>x===1).length===n/2&&!/000|111/.test(a.join(""))):new Set(a).size===n;
      let ok=st.every(line);for(let j=0;j<n;j++)ok=ok&&line(st.map(r=>r[j]));
      if(tak){ok=ok&&new Set(st.map(r=>r.join(""))).size===n&&new Set(st[0].map((_,j)=>st.map(r=>r[j]).join(""))).size===n;}
      if(it.kind==="sudoku"){const bs=Math.sqrt(n)|0;for(let a=0;a<n;a+=bs)for(let b=0;b<n;b+=bs){const q=[];for(let x=0;x<bs;x++)for(let y=0;y<bs;y++)q.push(st[a+x][b+y]);ok=ok&&new Set(q).size===n;}}
      if(fut)ok=ok&&(it.ineq||[]).every(([a,b])=>st[a[0]][a[1]]<st[b[0]][b[1]]);
      return ok;},
    reset(){for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(!fixed[i][j]){st[i][j]=null;cells[i][j].innerHTML="";cells[i][j].classList.remove("bad");}undo.length=0;}};};

/* ---------- показ пункта ---------- */
let pos=S.pos&&flat.findIndex(f=>f.si===S.pos[0]&&f.ii===S.pos[1]);if(pos==null||pos<0)pos=0;
let cur=null, openedAt=0;
function curKey(){return flat[pos]?flat[pos].k:"";}
function statusOf(k){const r=S.it[k];return r?r.st:"";}
let locked=false;
function lockScreen(f,sec){const lk=sec.lock;const c=el("div","cover");c.innerHTML=`<div class="lock">🔒</div><h1>${sec.title}</h1>`;
  const lkI=c.querySelector(".lock");let lp2;lkI.onpointerdown=()=>{lp2=setTimeout(()=>{if(!has(lk.id)){bought.push(lk.id);try{localStorage.setItem("misha:bought",JSON.stringify(bought))}catch(e){}log("free",{id:lk.id});show();}},1500);};lkI.onpointerup=lkI.onpointerleave=()=>clearTimeout(lp2);
  const b=el("button","buy",`Открыть · ${lk.price} ★`);b.disabled=wallet()<lk.price;b.onclick=()=>{if(buy(lk))show();};c.appendChild(b);
  if(wallet()<lk.price)c.appendChild(el("div","need",`в копилке ${wallet()} ★`));main.appendChild(c);}
function codeScreen(c){if(!L.code)return;const W=L.code.toUpperCase();const got=Object.values(S.letters);
  const box=el("div","code");const tiles=el("div","tiles");
  const order=[...W].map((ch,i)=>({ch,i})).sort((a,b)=>((a.i*7+3)%W.length)-((b.i*7+3)%W.length));
  const pool=got.slice();order.forEach(o=>{const j=pool.indexOf(o.ch);const t=el("span",j>=0?"on":"",j>=0?o.ch:"?");if(j>=0)pool.splice(j,1);tiles.appendChild(t);});
  box.appendChild(tiles);
  if(S.codeDone){box.appendChild(el("div","cok","✓ "+W));}
  else{const inp=el("input","cin");inp.placeholder="слово";const b=el("button","cbtn","Открыть");
    b.onclick=()=>{const v=norm(inp.value).toUpperCase().replace(/Ё/g,"Е");if(v===W.replace(/Ё/g,"Е")){S.codeDone=1;award(5,"код");say("Код верный! +5 ★",true);show();}else{log("code",{v});inp.classList.add("bad");setTimeout(()=>inp.classList.remove("bad"),900);}};
    box.appendChild(inp);box.appendChild(b);}
  c.appendChild(box);}
function openShop(){const items=L.sections.map((s,si)=>({s,si})).filter(x=>x.s.shop);log("shopopen");
  const p=el("div","panel shoppanel");p.innerHTML=`<h2><span>Лавка <b class="wl">★ ${wallet()}</b></span><button>✕</button></h2>`;const g=el("div","vitr");
  items.forEach(({s,si})=>{const own=has(s.lock.id);const can=wallet()>=s.lock.price;const it=s.items[0];
    const card=el("button","card"+(own?" own":"")+(can||own?"":" poor"));
    const pic=it.img?`<div class="th${own?"":" blur"}" style="background-image:url('${it.img}')"></div>`:`<div class="th emo">${s.shop.emo||"🎁"}</div>`;
    card.innerHTML=pic+`<div class="nm">${s.shop.name||s.title}</div><div class="pr">${own?"✓ твоё":s.lock.price+" ★"}</div>`;
    card.onclick=()=>{if(own){ov.hidden=true;go(flat.findIndex(f=>f.si===si),"shop");return;}
      if(!can){card.classList.add("shake");setTimeout(()=>card.classList.remove("shake"),500);return;}
      if(card.dataset.ask){if(buy(s.lock)){ov.hidden=true;go(flat.findIndex(f=>f.si===si),"shop");}return;}
      g.querySelectorAll(".card").forEach(x=>{delete x.dataset.ask;x.classList.remove("ask")});card.dataset.ask=1;card.classList.add("ask");card.querySelector(".pr").textContent="Купить за "+s.lock.price+" ★?";};
    g.appendChild(card);});
  p.appendChild(g);ov.innerHTML="";ov.appendChild(p);ov.hidden=false;$("h2 button",p).onclick=()=>ov.hidden=true;}
function shopScreen(c){if(L.sections.some(s=>s.shop)){const b=el("button","big shopbig","🛒 Лавка");b.onclick=openShop;c.appendChild(b);return;}const locks=L.sections.map((s,si)=>({s,si})).filter(x=>x.s.lock);if(!locks.length)return;
  const sh=el("div","shop");locks.forEach(({s,si})=>{const own=has(s.lock.id);const b=el("button",own?"own":"",own?`${s.title} ✓`:`${s.title}<b>${s.lock.price} ★</b>`);
    b.disabled=!own&&wallet()<s.lock.price;b.onclick=()=>{if(own||buy(s.lock)){log("shop",{id:s.lock.id});go(flat.findIndex(f=>f.si===si),"shop");}};sh.appendChild(b);});c.appendChild(sh);}
function show(){const f=flat[pos];const it=f.it;main.innerHTML="";S.pos=[f.si,f.ii];save();
  const sec=L.sections[f.si];secEl.innerHTML=`${sec.title}<small>${sec.sub||""}</small>`;
  locked=!!(sec.lock&&!has(sec.lock.id));
  if(locked){lockScreen(f,sec);cur={check(){return null},reset(){}};bChk.style.visibility="hidden";bRst.style.visibility="hidden";openedAt=now();log("open",{lock:1});paintNav();return;}
  if(it.type==="cover"){const c=el("div","cover"+(it.bg?" hasbg":""));if(it.bg)c.style.setProperty("--bgimg",`url("${it.bg}")`);c.innerHTML=`<h1>${it.title}</h1>${it.text?`<p>${it.text}</p>`:""}`;
    if(it.final){c.innerHTML+=`<div class="sum">+${S.stars} ★</div><div class="wal">в копилке ${wallet()} ★</div>`;codeScreen(c);shopScreen(c);
      const jb=el("button","jbtn","журнал");jb.onclick=journal;c.appendChild(jb);}
    else{if(it.shop){const sb=el("button","big shopbig","🛒 Открыть лавку");sb.onclick=openShop;c.appendChild(sb);}
      const b=el("button","big",it.button||"Начать");b.onclick=()=>{rec(f.k).att=1;rec(f.k).st="ok";go(pos+1);};c.appendChild(b);}
    main.appendChild(c);cur={check(){return null},reset(){}};bChk.style.visibility="hidden";bRst.style.visibility="hidden";paintNav();return;}
  bChk.style.visibility="";bRst.style.visibility="";
  const box=el("div","item");const q=el("p","q",it.q+(it.sub?`<span class="sub">${it.sub}</span>`:""));if(it.q)box.appendChild(q);
  const work=el("div","work");box.appendChild(work);main.appendChild(box);
  const ctx={k:f.k,slots:[],touch(){const r=rec(f.k);r.v=ctx.slots.map(s=>s.get());save();const t=now();if(t-(ctx._lt||0)>4000){ctx._lt=t;log("in");}}};
  const api=T[it.type](it,work,ctx);cur=Object.assign(api,{ctx,it,k:f.k});if(ctx.noCheck){bChk.style.visibility="hidden";bRst.style.visibility="hidden";}
  const r=S.it[f.k];if(r&&r.v)ctx.slots.forEach((s,i)=>{try{s.set(r.v[i])}catch(e){}});
  if(ctx.inner){cur.fit=fitter(work,ctx.inner,ctx.maxScale||it.maxScale);requestAnimationFrame(cur.fit);}
  openedAt=now();log("open");paintNav();
  const first=work.querySelector("input.slot:not(.free)");if(first)setTimeout(()=>first.focus({preventScroll:true}),50);}
function paintNav(){const f=flat[pos];const sec=L.sections[f.si];
  dots.innerHTML="";sec.items.forEach((it,ii)=>{const k=f.si+"."+ii;const b=el("b",statusOf(k)+(ii===f.ii?" cur":""));dots.appendChild(b);});
  prog.innerHTML="";flat.forEach((x,i)=>{if(x.it.type==="cover")return;const s=el("i",statusOf(x.k)+(i===pos?" cur":""));s.style.flex="1";prog.appendChild(s);});
  const r=S.it[f.k];bPrev.disabled=pos===0;bNext.disabled=pos===flat.length-1||!(locked||r&&r.att>0||f.it.optional||f.it.type==="grid"||f.it.type==="pic");
  bChk.classList.remove("ok","no");if(r&&r.att>0){bChk.classList.add(r.st==="wrong"?"no":"ok");}
  bChk.textContent=r&&r.att>0?(r.st==="wrong"?"✗ Ещё раз":"✓ Верно"):"✓ Проверить";
  $(".stars b",stage).textContent=wallet();$(".stars small",stage).textContent="";const fe=$(".fire",stage);fe.textContent=S.streak>=2?"🔥 "+S.streak:"";}
const isShop=i=>!!(flat[i]&&L.sections[flat[i].si].shop);
function go(i,how){if(how==="shop"&&!isShop(pos))S.ret=pos;
  if(how==="next"||how==="enter"||how==="prev"){const d=how==="prev"?-1:1;
    if(isShop(pos)){if(S.ret!=null&&S.ret>=0&&S.ret<flat.length&&!isShop(S.ret)){i=S.ret;S.ret=null;}else{while(i>=0&&i<flat.length&&isShop(i))i+=d;}}
    else{while(i>=0&&i<flat.length&&isShop(i))i+=d;}}
  if(i<0||i>=flat.length)return;log("leave",{dur:now()-openedAt});pos=i;if(how)log(how);show();}
function check(){if(!cur||!cur.check)return;const res=cur.check();if(res===null){log("empty");say("Заполни всё",false);return;}
  const r=rec(cur.k);r.att++;const first=r.att===1;
  let msg="";
  if(res){r.st=first?"ok":"fixed";if(first){S.stars++;total++;try{localStorage.setItem(SKEY,String(total))}catch(e){}S.streak++;
      if(S.streak%3===0){award(1,"серия");msg="🔥 Серия! +1 ★";}}else S.streak=0;
    if(cur.it.letter&&!S.letters[cur.k]){S.letters[cur.k]=cur.it.letter;msg="Буква «"+cur.it.letter+"»!";log("letter",{l:cur.it.letter});}
    say(msg||(first?"Верно! ★":"Верно"),true);chestCheck();}
  else{r.st="wrong";S.streak=0;say("Неверно",false);}
  r.v=cur.ctx.slots.map(s=>s.get());if(!r.t0)r.t0=openedAt;if(res&&!r.t1)r.t1=now();
  log("check",{ok:res,att:r.att,v:r.v});paintNav();}
function chestCheck(){const si=flat[pos].si;if(S.chest[si])return;const its=L.sections[si].items.map((it,ii)=>({it,k:si+"."+ii})).filter(x=>!["cover","grid","pic"].includes(x.it.type));
  if(its.length<2||!its.every(x=>S.it[x.k]&&S.it[x.k].st==="ok"))return;S.chest[si]=1;award(3,"сундук");save();
  setTimeout(()=>{const ch=el("div","chest","<div>🎁</div><b>Без ошибок! +3 ★</b>");stage.appendChild(ch);setTimeout(()=>ch.remove(),2200);paintNav();},900);}
let tt;function say(t,ok){toast.textContent=t;toast.className="toast show"+(ok?"":" no");clearTimeout(tt);tt=setTimeout(()=>toast.className="toast"+(ok?"":" no"),1100);}
bPrev.onclick=()=>go(pos-1,"prev");bNext.onclick=()=>{if(!bNext.disabled)go(pos+1,"next");};bChk.onclick=check;
bRst.onclick=()=>{if(!cur)return;cur.reset();const r=rec(cur.k);r.v=null;save();log("reset");};
addEventListener("keydown",e=>{if(!ov.hidden){if(e.key==="Escape")ov.hidden=true;return;}
  if(e.ctrlKey&&e.shiftKey&&(e.code==="KeyJ")){e.preventDefault();journal();return;}
  if(cur&&cur.ctx&&cur.ctx.key&&cur.ctx.key(e)){e.preventDefault();return;}
  if(e.key==="Enter"){e.preventDefault();const r=S.it[curKey()];if((locked||(cur&&cur.ctx&&cur.ctx.noCheck)||r&&r.att>0&&r.st!=="wrong")&&!bNext.disabled)go(pos+1,"enter");else check();}});

/* ---------- скип (для репетитора) ---------- */
$(".shopbtn",stage).onclick=openShop;
$(".skip",stage).onclick=()=>{const p=el("div","panel");p.innerHTML=`<h2>Перейти к задаче <button>✕</button></h2>`;const j=el("div","jump");
  L.sections.forEach((s,si)=>{const row=el("div","jr");row.appendChild(el("span","",s.title));s.items.forEach((it,ii)=>{const b=el("button",statusOf(si+"."+ii),String(ii+1));
    b.onclick=()=>{ov.hidden=true;go(flat.findIndex(f=>f.si===si&&f.ii===ii),"skip");};row.appendChild(b);});j.appendChild(row);});
  p.appendChild(j);ov.innerHTML="";ov.appendChild(p);ov.hidden=false;$("h2 button",p).onclick=()=>ov.hidden=true;};

/* ---------- журнал (Ctrl+Shift+J или долгое нажатие на звёзды) ---------- */
function summary(){const rows=[];const ev=S.ev;
  flat.forEach(f=>{if(f.it.type==="cover")return;const E=ev.filter(x=>x.k===f.k);if(!E.length){rows.push({f,att:0});return;}
    let active=0,openT=null,firstOpen=E[0].t,lastT=E[0].t,idle=0,prev=null;
    E.forEach(x=>{if(x.e==="open")openT=x.t;if(x.e==="leave"&&openT){active+=x.t-openT;openT=null;}if(prev&&x.t-prev>90000&&x.e!=="open")idle+=x.t-prev;prev=x.t;lastT=x.t;});
    if(openT&&f.k===curKey())active+=now()-openT;
    const r=S.it[f.k]||{};const firstOk=E.find(x=>x.e==="check"&&x.ok);
    const firstChk=E.find(x=>x.e==="check");const lvAfter=firstOk&&E.find(x=>x.e==="leave"&&x.t>=firstOk.t);
    rows.push({f,start:firstOpen,end:firstOk?firstOk.t:null,active,att:r.att||0,st:r.st||"",idle,think:firstChk?firstChk.t-firstOpen:null,
      rush:lvAfter?lvAfter.t-firstOk.t:null,zoom:E.filter(x=>x.e==="zoom").length,empty:E.filter(x=>x.e==="empty").length});});return rows;}
const hm=t=>t?new Date(t).toLocaleTimeString("ru-RU",{hour:"2-digit",minute:"2-digit"}):"—";
const mm=ms=>ms?(Math.floor(ms/60000)+":"+String(Math.round(ms/1000)%60).padStart(2,"0")):"—";
function journal(){const rows=summary();const p=el("div","panel");
  const stt={ok:"✓ с первой",fixed:"✓ со второй+",wrong:"✗",'':"—"};
  let h=`<h2>Журнал: ${L.title} <button>✕</button></h2><table><tr><th>задача</th><th>открыл</th><th>решил</th><th>время</th><th>попыток</th><th>итог</th><th>до 1-й проверки</th><th>после ✓ ушёл через</th><th>простой &gt;1,5 мин</th></tr>`;
  rows.forEach(x=>{const s=L.sections[x.f.si];h+=`<tr><td>${s.title} · ${x.f.ii+1}</td><td>${hm(x.start)}</td><td>${hm(x.end)}</td><td>${mm(x.active)}</td><td>${x.att}</td><td>${stt[x.st||""]}</td><td>${mm(x.think)}</td><td>${x.rush!=null?Math.round(x.rush/1000)+" с":"—"}</td><td>${mm(x.idle)}</td></tr>`;});
  h+=`</table><div class="acts"><button data-a="all">скопировать всё (для разбора)</button><button data-a="copy">скопировать таблицу</button><button data-a="json">скачать журнал (JSON)</button><button data-a="clr">стереть прогресс этого занятия</button><button data-a="all0">сбросить ВСЁ: звёзды, лавку, занятия</button></div>`;
  p.innerHTML=h;ov.innerHTML="";ov.appendChild(p);ov.hidden=false;$("h2 button",p).onclick=()=>ov.hidden=true;
  p.querySelector(".acts").onclick=e=>{const a=e.target.dataset.a;if(!a)return;
    if(a==="all"){const txt=JSON.stringify({lesson:L.id,wallet:wallet(),total,spent,bought,today:S.stars,items:S.it,events:S.ev.map(x=>Object.assign({},x,{t:new Date(x.t).toLocaleTimeString("ru-RU")}))});
      (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>e.target.textContent="скопировано — вставь в чат",()=>e.target.textContent="не вышло — скачай JSON");}
    if(a==="copy"){const txt=rows.map(x=>[L.sections[x.f.si].title+" · "+(x.f.ii+1),hm(x.start),hm(x.end),mm(x.active),x.att,x.st,mm(x.think),x.rush!=null?Math.round(x.rush/1000):""].join("\t")).join("\n");
      (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>e.target.textContent="скопировано",()=>e.target.textContent="не вышло");}
    if(a==="json"){const blob=new Blob([JSON.stringify({lesson:L.id,title:L.title,items:S.it,events:S.ev},null,1)],{type:"application/json"});
      const u=URL.createObjectURL(blob);const x=document.createElement("a");x.href=u;x.download=`zhurnal-${L.id}.json`;document.body.appendChild(x);x.click();x.remove();}
    if(a==="all0"){if(e.target.dataset.sure){try{Object.keys(localStorage).filter(k=>k.startsWith("misha:")).forEach(k=>localStorage.removeItem(k))}catch(_){}location.reload();}else{e.target.dataset.sure=1;e.target.textContent="точно всё обнулить? нажми ещё раз";}}
    if(a==="clr"){if(e.target.dataset.sure){localStorage.removeItem(KEY);location.reload();}else{e.target.dataset.sure=1;e.target.textContent="точно стереть? нажми ещё раз";}}};}
let lp;const stEl=$(".stars",stage);stEl.onpointerdown=()=>{lp=setTimeout(journal,1200);};stEl.onpointerup=stEl.onpointerleave=()=>clearTimeout(lp);
addEventListener("visibilitychange",()=>log(document.hidden?"hide":"show"));

scale();show();
})();
