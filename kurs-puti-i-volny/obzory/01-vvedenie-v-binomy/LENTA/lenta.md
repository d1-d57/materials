---
tab: Биномиальные коэффициенты
status: chistovik
poryadok: 1
registr: читаемый
nomera: da
zhanr: statya
---

# Биномиальные коэффициенты

Индийские медики различали шесть вкусов: сладкий, кислый, солёный, острый, горький и вяжущий. Сколько разных смесей можно составить ровно из трёх вкусов? А сколько всего смесей, если брать любое число вкусов, но хотя бы один?

Ответ знали ещё на рубеже эр: в медицинском трактате Чараки сочетания шести вкусов пересчитаны по группам. Около 550 года астроном Варахамихира считал смеси благовоний и нашёл, что четыре вещества из шестнадцати можно выбрать 1820 способами. Выписывать 1820 смесей он не стал. Как сосчитать их, не перебирая? Такие числа называются биномиальными коэффициентами; дальше в курсе с их помощью мы будем считать и вероятности, например в задаче о случайном блуждании. Сначала выясним, что это за числа, и попробуем сложить из них таблицу.

## Число способов выбрать

Вопрос из вступления звучит так: сколькими способами можно выбрать три предмета из шести? Такие вопросы задают по-разному. Говорят о числе способов выбрать $k$ предметов из $n$, о числе сочетаний из $n$ по $k$, о количестве вариантов. Во всех случаях речь об одном и том же числе. Посчитаем его, когда предметов немного, честно выписывая все варианты.

Возьмём четыре предмета и обозначим их числами 1, 2, 3, 4. Два предмета из них можно выбрать шестью способами:
$$\{1,2\},\ \{1,3\},\ \{1,4\},\ \{2,3\},\ \{2,4\},\ \{3,4\}.$$
Порядок внутри набора не важен: $\{1,2\}$ и $\{2,1\}$ — один и тот же выбор. Так же выпишем и другие случаи.

| из | берём | все варианты | всего |
|---|---|---|---|
| 3 | 2 | $\{1,2\}$, $\{1,3\}$, $\{2,3\}$ | 3 |
| 4 | 1 | $\{1\}$, $\{2\}$, $\{3\}$, $\{4\}$ | 4 |
| 4 | 2 | $\{1,2\}$, $\{1,3\}$, $\{1,4\}$, $\{2,3\}$, $\{2,4\}$, $\{3,4\}$ | 6 |
| 4 | 3 | $\{1,2,3\}$, $\{1,2,4\}$, $\{1,3,4\}$, $\{2,3,4\}$ | 4 |
| 4 | 4 | $\{1,2,3,4\}$ | 1 |

Другие случаи можно посмотреть в виджете: задайте, сколько всего предметов и сколько из них нужно выбрать, и он выпишет все варианты.

<div class="sim-lib" hidden><style>:root{--sim-v:#7b4fa6}
:root[data-theme="dark"]{--sim-v:#b994dc}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--sim-v:#b994dc}}
.sim{margin:2.4em auto 2.2em;max-width:740px}
.sim svg{width:100%;height:auto;display:block;touch-action:none;user-select:none;-webkit-user-select:none}
.sim .sim-bar{display:flex;flex-wrap:wrap;gap:.5em;justify-content:center;margin:.7em 0 .3em;font-family:var(--sans)}
.sim button{font:inherit;font-size:15px;line-height:1.2;padding:.4em 1em;border-radius:999px;border:1px solid var(--rule);background:var(--panel);color:var(--text);cursor:pointer;transition:border-color .15s,color .15s}
.sim button:hover,.sim button:focus-visible{border-color:var(--accent);color:var(--accent);outline:none}
.sim button[disabled]{opacity:.45;cursor:default}
.sim .sim-out{font-family:var(--sans);font-size:16px;color:var(--text);text-align:center;min-height:1.6em;margin-top:.2em}
.sim .sim-cap{font-family:var(--sans);font-size:16px;color:var(--muted);margin-top:.5rem}
.sim .sim-chip{display:inline-flex;align-items:center;gap:.3em;margin:0 .45em;white-space:nowrap}
.sim .sim-dot{display:inline-block;width:.8em;height:.8em;border-radius:50%}
.k-ax{fill:none;stroke:var(--muted);stroke-width:1.2}
.k-axh{fill:var(--muted)}
.k-lab{font-family:var(--sans);font-size:13px;fill:var(--muted)}
.k-curve{fill:none;stroke:var(--text);stroke-width:2;stroke-linejoin:round}
.k-thin{fill:none;stroke:var(--faint);stroke-width:1.2}
.k-shade{fill:var(--shade)}
.k-x{fill:none;stroke:var(--accent);stroke-width:2.2;stroke-linecap:round}
.k-ring{fill:none;stroke:var(--faint);stroke-width:1.4;stroke-dasharray:3 3}
.k-handle{fill:var(--text);stroke:var(--panel);stroke-width:2;cursor:grab}
.k-halo{fill:var(--accent);opacity:.14}
.k-base{fill:var(--panel);stroke:var(--text);stroke-width:1.8}
.k-l1{fill:none;stroke:var(--accent);stroke-width:2.2}
.k-l2{fill:none;stroke:var(--warm);stroke-width:2.2}
.k-f1{fill:var(--accent)}.k-f2{fill:var(--warm)}
.k-k0{fill:var(--text)}.k-k1{fill:var(--accent)}.k-k2{fill:var(--warm)}.k-k3{fill:var(--defn)}.k-k4{fill:var(--sim-v)}
.k-t0{fill:none;stroke:var(--text);stroke-width:1.6;opacity:.55}.k-t1{fill:none;stroke:var(--accent);stroke-width:1.6;opacity:.6}.k-t2{fill:none;stroke:var(--warm);stroke-width:1.6;opacity:.6}.k-t3{fill:none;stroke:var(--defn);stroke-width:1.6;opacity:.6}.k-t4{fill:none;stroke:var(--sim-v);stroke-width:1.6;opacity:.6}
.k-path{fill:none;stroke:var(--accent);stroke-width:1.6;opacity:.7}
.sim .k-d0{background:var(--text)}.sim .k-d1{background:var(--accent)}.sim .k-d2{background:var(--warm)}.sim .k-d3{background:var(--defn)}.sim .k-d4{background:var(--sim-v)}
/* ── дописки obzor01: ползунки, бином в строке, слова-клеточки, карточки, стрелки ── */
.sim svg.w-svg{touch-action:manipulation}
.sim .sim-bar.w-top{margin:0 0 .6em}
.sim .sim-ctl{display:inline-flex;align-items:center;gap:.45em;font-size:15px;color:var(--muted);white-space:nowrap}
.sim .sim-ctl i{font-family:var(--serif);font-size:19px;color:var(--text)}
.sim input[type=range]{accent-color:var(--accent);width:min(9em,30vw);margin:0;cursor:pointer}
.sim .sim-v{display:inline-block;min-width:1.2em;color:var(--text);font-variant-numeric:tabular-nums}
.sim button.on{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.sim .sim-out{line-height:1.9}
.sim .sim-out b{font-weight:600;color:var(--accent)}
.sim .sim-out .w-dim{color:var(--muted)}
.sim .bn{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;position:relative;font-size:.78em;line-height:1.08;padding:0 .42em;margin:0 .08em;font-variant-numeric:tabular-nums}
.sim .bn::before,.sim .bn::after{content:"";position:absolute;top:.04em;bottom:.04em;width:.5em;border:1.4px solid currentColor;border-radius:50%}
.sim .bn::before{left:0;border-color:transparent transparent transparent currentColor}
.sim .bn::after{right:0;border-color:transparent currentColor transparent transparent}
.w-c{fill:none;stroke:var(--quiet);stroke-width:1.2}
.w-c.on{fill:var(--accent);stroke:var(--accent)}
.w-frame{fill:none;stroke:var(--warm);stroke-width:2;opacity:0}
.w-word.hl .w-frame{opacity:1}
.w-hit{fill:transparent;cursor:pointer}
.w-link{fill:none;stroke:var(--faint);stroke-width:1.2}
.w-link.hl{stroke:var(--warm);stroke-width:2.4}
.w-lab{font-family:var(--sans);font-size:14px;fill:var(--muted)}
.w-num{font-family:var(--sans);font-size:26px;font-weight:600;fill:var(--text);font-variant-numeric:tabular-nums}
.w-eq{font-family:var(--sans);font-size:26px;fill:var(--muted)}</style><script>(function(){
var NS="http:"+"/"+"/www.w3.org/2000/svg";
function el(tag,attrs,parent){var e=document.createElementNS(NS,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(parent){parent.appendChild(e);}return e;}
function Panel(x0,y0,w,h,xr,yr){this.x0=x0;this.y0=y0;this.w=w;this.h=h;this.xr=xr;this.yr=yr;}
Panel.prototype.X=function(x){return this.x0+(x-this.xr[0])/(this.xr[1]-this.xr[0])*this.w;};
Panel.prototype.Y=function(y){return this.y0+this.h-(y-this.yr[0])/(this.yr[1]-this.yr[0])*this.h;};
Panel.prototype.ix=function(X){return this.xr[0]+(X-this.x0)/this.w*(this.xr[1]-this.xr[0]);};
Panel.prototype.iy=function(Y){return this.yr[0]+(this.y0+this.h-Y)/this.h*(this.yr[1]-this.yr[0]);};
Panel.prototype.inside=function(x,y){return x>=this.xr[0]&&x<=this.xr[1]&&y>=this.yr[0]&&y<=this.yr[1];};
Panel.prototype.d=function(pts){var s="",pen=false;for(var i=0;i<pts.length;i++){var x=pts[i][0],y=pts[i][1];if(this.inside(x,y)){s+=(pen?" L":" M")+this.X(x).toFixed(1)+","+this.Y(y).toFixed(1);pen=true;}else{pen=false;}}return s||"M0,0";};
Panel.prototype.axes=function(g,lx,ly){var X0=this.X(0),Y0=this.Y(0);el("line",{"class":"k-ax",x1:this.x0,y1:Y0,x2:this.x0+this.w,y2:Y0},g);el("line",{"class":"k-ax",x1:X0,y1:this.y0+this.h,x2:X0,y2:this.y0},g);el("path",{"class":"k-axh",d:"M"+(this.x0+this.w)+","+Y0+" l-8,-3.5 0,7 z"},g);el("path",{"class":"k-axh",d:"M"+X0+","+this.y0+" l-3.5,8 7,0 z"},g);if(lx){var t=el("text",{"class":"k-lab",x:this.x0+this.w-10,y:Y0+17},g);t.textContent=lx;}if(ly){var u=el("text",{"class":"k-lab",x:X0+8,y:this.y0+10},g);u.textContent=ly;}};
function mul(a,b){return [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
function sub(a,b){return [a[0]-b[0],a[1]-b[1]];}
function div(a,b){var q=b[0]*b[0]+b[1]*b[1];return [(a[0]*b[0]+a[1]*b[1])/q,(a[1]*b[0]-a[0]*b[1])/q];}
function ev(c,z){var r=[1,0];for(var i=1;i<c.length;i++){r=mul(r,z);r=[r[0]+c[i][0],r[1]+c[i][1]];}return r;}
function dk(c,z0,it){var n=z0.length,z=z0.map(function(v){return [v[0],v[1]];});for(var k=0;k<it;k++){for(var i=0;i<n;i++){var den=[1,0];for(var j=0;j<n;j++){if(j!==i){den=mul(den,sub(z[i],z[j]));}}z[i]=sub(z[i],div(ev(c,z[i]),den));}}return z;}
function pt(svg,e){var p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
function num(v){var s=Math.abs(v).toFixed(2).replace(".",",");return (v<-0.005?"−":"")+s;}
function clear(g){while(g.firstChild){g.removeChild(g.firstChild);}}
window.SimK={el:el,Panel:Panel,mul:mul,sub:sub,div:div,ev:ev,dk:dk,pt:pt,num:num,clear:clear};
})();
/* ── дописки obzor01 (биномиальные коэффициенты): счёт, слова из 0/1, анимация, ширина ── */
(function(G){
var K=G.SimK||(G.SimK={});
function C(n,k){if(k<0||k>n){return 0;}var r=1,i;for(i=1;i<=k;i++){r=r*(n-k+i)/i;}return Math.round(r);}
/* все слова длины n из 0 и 1 с k единицами; порядок: 1 раньше 0 (убывание двоичного числа) */
function words(n,k){var out=[],w=[];function rec(ones){var left=n-w.length;if(ones>left||ones<0){return;}if(left===0){out.push(w.slice());return;}if(ones>0){w.push(1);rec(ones-1);w.pop();}w.push(0);rec(ones);w.pop();}rec(k);return out;}
function flip(w){return w.map(function(b){return 1-b;});}
function key(w){return w.join("");}
/* карточки «команда из m человек среди n, в ней капитан» */
function cards(n,m){var res=[];words(n,m).forEach(function(t){t.forEach(function(b,i){if(b){res.push({team:t,cap:i});}});});return res;}
/* разбить список на стопки по ключу; порядок стопок — по первому появлению */
function groups(list,keyf){var map={},order=[];list.forEach(function(c,i){var g=keyf(c);if(!map.hasOwnProperty(g)){map[g]=[];order.push(g);}map[g].push(i);});return order.map(function(g){return map[g];});}
/* упорядоченные пары различных вершин 0..n-1 */
function arrows(n){var a=[],i,j;for(i=0;i<n;i++){for(j=0;j<n;j++){if(i!==j){a.push([i,j]);}}}return a;}
var mq=(G.matchMedia?G.matchMedia("(prefers-reduced-motion: reduce)"):null);
function reduced(){return !!(mq&&mq.matches);}
function ease(t){t=t<0?0:(t>1?1:t);return t<0.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
function seg(t,a,b){return ease((t-a)/(b-a));}
/* t бежит 0→1 за ms; при «меньше движения» — сразу последний кадр (асинхронно: ручка остановки возвращается раньше done) */
function anim(ms,step,done){var alive=true;if(reduced()||!(ms>0)||!G.requestAnimationFrame){G.setTimeout(function(){if(alive){step(1);if(done){done();}}},0);return {stop:function(){alive=false;}};}var t0=null;function fr(ts){if(!alive){return;}if(t0===null){t0=ts;}var t=Math.min(1,(ts-t0)/ms);step(t);if(t<1){G.requestAnimationFrame(fr);}else if(done){done();}}G.requestAnimationFrame(fr);return {stop:function(){alive=false;}};}
/* бином (n над k) для HTML-строк под рисунком */
function bn(n,k){return '<span class="bn"><span>'+n+'</span><span>'+k+'</span></span>';}
/* вызвать fn(ширина) сейчас и при каждом изменении ширины элемента */
function onWidth(el,fn){var w=-1;function chk(){var x=Math.round(el.getBoundingClientRect().width);if(x>0&&x!==w){w=x;fn(x);}}if(G.ResizeObserver){new G.ResizeObserver(chk).observe(el);}G.addEventListener("resize",chk);chk();}
function cl(v,a,b){return Math.max(a,Math.min(b,v));}
/* русское число: pl(5,"пара","пары","пар") */
function pl(x,a,b,c){var m=x%10,h=x%100;return (m===1&&h!==11)?a:((m>=2&&m<=4&&(h<10||h>=20))?b:c);}
/* лесенка n×n (строки и столбцы 1..n): пара {i,j}, i<j; u — клетка верхней лесенки (строка i, столбец j), d1 — отражение (j,i), d2 — оно же на ряд выше (j-1,i) */
function ladder(n){var a=[],i,j;for(i=1;i<=n;i++){for(j=i+1;j<=n;j++){a.push({i:i,j:j,u:[i,j],d1:[j,i],d2:[j-1,i]});}}return a;}
K.ladder=ladder;
/* набор по коду: номера (с 1) мест, где стоят единицы; 1010 → [1,3] */
function nabor(w){var a=[],i;for(i=0;i<w.length;i++){if(w[i]){a.push(i+1);}}return a;}
K.nabor=nabor;
K.C=C;K.words=words;K.flip=flip;K.key=key;K.cards=cards;K.groups=groups;K.arrows=arrows;K.reduced=reduced;K.ease=ease;K.seg=seg;K.anim=anim;K.bn=bn;K.onWidth=onWidth;K.cl=cl;K.pl=pl;
})(typeof window!=="undefined"?window:globalThis);</script></div>

<div class="sim" id="sim-c0"><style>#sim-c0 .c0-cnt{font-family:var(--sans);font-size:16px;color:var(--muted);text-align:center;margin:0 0 .25em}
#sim-c0 .c0-cnt b{font-size:19px;font-weight:600;color:var(--accent);font-variant-numeric:tabular-nums}
#sim-c0 .c0-set{font-family:var(--sans);font-size:16px;fill:var(--text);font-variant-numeric:tabular-nums}
#sim-c0 .c0-row.hl .c0-set{fill:var(--warm);font-weight:600}
#sim-c0 .c0-pos{font-family:var(--sans);font-size:13px;fill:var(--quiet);font-variant-numeric:tabular-nums}
#sim-c0 .c0-pos.hl{fill:var(--warm);font-weight:600}
#sim-c0 .c0-zebra{fill:none}
#sim-c0 .c0-zebra.odd{fill:var(--shade);fill-opacity:.5}
#sim-c0 .sim-out{min-height:1.9em;line-height:1.5;padding:.2em 0}
@media (max-width:520px){#sim-c0 .sim-out{min-height:3.2em}}
#sim-c0 .c0-pair{white-space:nowrap;font-variant-numeric:tabular-nums}</style><div class="sim-bar w-top"><label class="sim-ctl"><span>предметов <i>n</i></span><input class="c0-n" type="range" min="1" max="6" step="1" value="4"><span class="sim-v c0-nv">4</span></label><label class="sim-ctl"><span>выбираем <i>k</i></span><input class="c0-k" type="range" min="0" max="4" step="1" value="2"><span class="sim-v c0-kv">2</span></label></div>
<div class="c0-cnt">вариантов: <b>6</b></div>
<svg class="w-svg" viewBox="0 0 600 220" role="img" aria-label="Интерактив: список всех способов выбрать k предметов из n; в каждой строке слева набор номеров выбранных предметов в фигурных скобках, справа его код — ряд из n клеток, где закрашены клетки на местах выбранных предметов; строки идут в словарном порядке кодов"></svg>
<div class="sim-out"></div>
<div class="sim-cap">Все способы выбрать $k$ предметов из $n$.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c0");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),cnt=root.querySelector(".c0-cnt"),inN=root.querySelector(".c0-n"),inK=root.querySelector(".c0-k"),vN=root.querySelector(".c0-nv"),vK=root.querySelector(".c0-kv");
var n=+inN.value,k=+inK.value,W=600,G=null,run=null,hl=-1;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
/* {1, 3}; пустой набор — { } */
function setStr(a){return a.length?"{"+a.join(", ")+"}":"{ }";}
function listStr(a){return a.length<2?String(a[0]):a.slice(0,-1).join(", ")+" и "+a[a.length-1];}
/* ширина подписи набора: меряем прямо в рисунке, при неудаче — оценка */
function measure(s){var e=txt("c0-set",0,-40,s,svg,"start"),w=0;try{w=e.getComputedTextLength();}catch(x){w=0;}svg.removeChild(e);return w>0?w:s.length*8.6;}
/* fade — мягкое появление строк (только при смене ползунков) */
function build(fade){
if(run){run.stop();run=null;}hl=-1;K.clear(svg);
var ws=K.words(n,k),N=ws.length,sets=ws.map(K.nabor),i,q,big=[];
for(i=1;i<=k;i++){big.push(i);}
var rp=W<480?28:30,c=rp-10,cp=c+4,cw=n*cp-4,lw=Math.max(24,Math.ceil(measure(setStr(big)))),gap=24,pad=10,bw=pad+lw+gap+cw+pad,cg=32;
var cols=(N>6&&2*bw+cg<=W)?2:1,rpc=Math.ceil(N/cols),top=24,H=top+rpc*rp+2;
var x0=Math.round((W-(cols*bw+(cols-1)*cg))/2);
svg.setAttribute("viewBox","0 0 "+W+" "+H);svg.setAttribute("data-cols",cols);
var gT=K.el("g",{},svg),gR=K.el("g",{},svg),heads=[],rows=[];
/* над кодами — номера мест 1..n */
for(q=0;q<cols;q++){var hs=[],hx=x0+q*(bw+cg)+pad+lw+gap;for(i=0;i<n;i++){hs.push(txt("c0-pos",hx+i*cp+c/2,top-8,String(i+1),gT));}heads.push(hs);}
ws.forEach(function(w,i){var col=Math.floor(i/rpc),r=i%rpc,bx=x0+col*(bw+cg),y=top+r*rp,cy=y+rp/2,j;
var g=K.el("g",{"class":"w-word c0-row","data-i":i},gR);
K.el("rect",{"class":"c0-zebra"+(r%2?" odd":""),x:bx,y:y+1,width:bw,height:rp-2,rx:5},g);
K.el("rect",{"class":"w-frame",x:bx+1,y:y+2,width:bw-2,height:rp-4,rx:5},g);
txt("c0-set",bx+pad,cy+5.5,setStr(sets[i]),g,"start");
for(j=0;j<n;j++){K.el("rect",{"class":"w-c"+(w[j]?" on":""),x:bx+pad+lw+gap+j*cp,y:cy-c/2,width:c,height:c,rx:3},g);}
K.el("rect",{"class":"w-hit",x:bx,y:y,width:bw,height:rp},g);
rows.push(g);});
G={ws:ws,sets:sets,rows:rows,heads:heads,rpc:rpc};
cnt.innerHTML="вариантов: <b>"+N+"</b>";
say();
if(fade&&!K.reduced()){var N1=Math.max(1,N-1);
rows.forEach(function(g){g.setAttribute("opacity","0");});
run=K.anim(320+18*N,function(t){rows.forEach(function(g,i){var a=0.55*i/N1,v=K.seg(t,a,a+0.45);g.setAttribute("opacity",v.toFixed(3));g.setAttribute("transform","translate(0,"+((1-v)*6).toFixed(2)+")");});},function(){run=null;rows.forEach(function(g){g.removeAttribute("opacity");g.removeAttribute("transform");});});}}
function say(){var s;
if(hl<0){s='<span class="w-dim">'+(k===0?"вариант один: не выбрать ничего":"наведите на строку или коснитесь её")+"</span>";}
else{var a=G.sets[hl];
s='<span class="c0-pair">'+setStr(a)+" ↔ "+K.key(G.ws[hl])+":</span> "+'<span class="c0-pair">'+(a.length===0?"единиц нет — ничего не выбрано":(a.length===1?"на месте "+a[0]+" — единица":"на местах "+listStr(a)+" — единицы"))+"</span>";}
out.innerHTML=s;}
function setHL(i){hl=i;var col=i<0?-1:Math.floor(i/G.rpc),w=i<0?null:G.ws[i];
G.rows.forEach(function(g,q){g.classList.toggle("hl",q===i);});
G.heads.forEach(function(hs,c){hs.forEach(function(e,p){e.classList.toggle("hl",c===col&&!!w[p]);});});
say();}
function pick(e){var g=e.target.closest?e.target.closest(".c0-row"):null;return g?+g.getAttribute("data-i"):-1;}
svg.addEventListener("pointerover",function(e){var i=pick(e);if(i>=0&&i!==hl){setHL(i);}});
svg.addEventListener("pointerdown",function(e){var i=pick(e);if(i>=0){setHL(i);}else if(hl>=0){setHL(-1);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl>=0){setHL(-1);}});
function upd(){n=+inN.value;inK.max=n;k=Math.min(+inK.value,n);inK.value=k;vN.textContent=n;vK.textContent=k;build(true);}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build(false);});
})();</script></div>

Теперь попробуем так же выписать тройки из шести вкусов. Занумеруем вкусы по порядку, от сладкого (1) до вяжущего (6), и начнём: $\{1,2,3\}$, $\{1,2,4\}$, $\{1,3,5\}$, $\{2,4,6\}$… Сразу видны три трудности. Записей много. Непонятно, в каком порядке их перебирать. И когда список кончится, трудно проверить, что ни одна тройка не пропущена.

Все три трудности снимает простой код. Пройдём по номерам от 1 до 6 и напишем 1, если вкус выбран, и 0, если нет. Получится последовательность из шести нулей и единиц; для краткости будем называть такие последовательности словами. Тройка «сладкий, солёный, горький», то есть $\{1,3,5\}$, станет словом 101010, тройка «кислый, солёный, острый», то есть $\{2,3,4\}$, — словом 011100. Каждой тройке отвечает слово длины 6 ровно с тремя единицами.

Слово из нулей и единиц — это ещё и число, записанное в двоичной системе. В привычной записи места цифр справа налево означают единицы, десятки, сотни. В двоичной записи цифр только две, 0 и 1, а места справа налево означают 1, 2, 4, 8, 16, 32: каждое следующее вдвое больше. Слово 011100 — это число $16+8+4=28$.

Выпишем все слова длины 3 по возрастанию: 000, 001, 010, 011, 100, 101, 110, 111. Каждое слово оказалось двоичной записью своего номера в списке, если считать с нуля: 000 записывает 0, 101 записывает 5, а 111 записывает 7.

В виджете можно нажимать и на предметы, и на цифры слова: меняется одно — меняется и другое. Под каждой цифрой подписано, что означает её место в двоичной записи. Кнопка «+1» прибавляет к числу единицу, и, нажимая её, можно пройти по очереди все наборы.

<div class="sim" id="sim-c6"><style>#sim-c6 .c6-it{fill:var(--panel);stroke:var(--muted);stroke-width:1.6;transition:fill .15s,stroke .15s}
#sim-c6 .c6-col.on .c6-it{fill:var(--accent);stroke:var(--accent)}
#sim-c6 .c6-itl{font-family:var(--sans);font-size:16px;fill:var(--text);font-variant-numeric:tabular-nums;pointer-events:none}
#sim-c6 .c6-col.on .c6-itl{fill:var(--panel);font-weight:600}
#sim-c6 .c6-bx{fill:var(--panel);stroke:var(--faint);stroke-width:1.4;transition:fill .15s,stroke .15s}
#sim-c6 .c6-col.on .c6-bx{fill:var(--accent-soft);stroke:var(--accent)}
#sim-c6 .c6-dg{font-family:var(--sans);font-size:22px;fill:var(--quiet);font-variant-numeric:tabular-nums;pointer-events:none}
#sim-c6 .c6-col.on .c6-dg{fill:var(--accent);font-weight:600}
#sim-c6 .c6-ln{stroke:var(--faint);stroke-width:1.2}
#sim-c6 .c6-col.on .c6-ln{stroke:var(--accent);stroke-width:2}
#sim-c6 .c6-pv{font-family:var(--sans);font-size:13px;fill:var(--quiet);font-variant-numeric:tabular-nums}
#sim-c6 .c6-col.on .c6-pv{fill:var(--accent);font-weight:600}
#sim-c6 .c6-rl{font-family:var(--sans);font-size:13px;fill:var(--quiet)}
#sim-c6 .c6-fl{fill:var(--warm-soft)}
#sim-c6 .c6-b{cursor:pointer;outline:none}
#sim-c6 .c6-b:hover .c6-it,#sim-c6 .c6-b:hover .c6-bx{stroke:var(--accent)}
#sim-c6 .c6-ring{fill:none;stroke:var(--warm);stroke-width:2;opacity:0}
#sim-c6 .c6-b:focus-visible .c6-ring{opacity:1}
#sim-c6 .sim-out{line-height:1.55;min-height:4.8em}
@media (max-width:520px){#sim-c6 .sim-out{min-height:6.3em}}
#sim-c6 .sim-out i{font-family:var(--serif)}
#sim-c6 .c6-l{display:block}
#sim-c6 .c6-nw{white-space:nowrap}
#sim-c6 .c6-w{font-variant-numeric:tabular-nums;letter-spacing:.06em;font-weight:600}</style><div class="sim-bar w-top"><label class="sim-ctl"><span>предметов <i>n</i></span><input class="c6-n" type="range" min="1" max="8" step="1" value="6"><span class="sim-v c6-nv">6</span></label></div>
<svg class="w-svg" viewBox="0 0 600 170" role="group" aria-label="Интерактив: сверху n кружков-предметов с номерами от 1 до n, под каждым на линии — его цифра в слове из нулей и единиц и вес этого разряда; нажатие на кружок или на цифру выбирает предмет или снимает выбор, а слово и набор меняются вместе."></svg>
<div class="sim-bar"><button type="button" class="c6-dec" aria-label="минус один">−1</button><button type="button" class="c6-inc" aria-label="плюс один">+1</button><button type="button" class="c6-clr">очистить</button><button type="button" class="c6-all">все</button></div>
<div class="sim-out" aria-live="polite"></div>
<div class="sim-cap">Нажимайте на кружки или на цифры: подмножество и слово меняются вместе.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c6");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c6-n"),vN=root.querySelector(".c6-nv");
var SUP="⁰¹²³⁴⁵⁶⁷⁸";
var n=+inN.value,W=600,bits=[],cols=[],run=null,flash=[];
/* по умолчанию выбраны 1, 3, 5 */
(function(){var i;for(i=0;i<8;i++){bits.push(i%2===0&&i<5?1:0);}})();
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
function pw(i){return Math.pow(2,n-1-i);}
function value(){var v=0,i;for(i=0;i<n;i++){if(bits[i]){v+=pw(i);}}return v;}
function setValue(v){var i;for(i=0;i<n;i++){bits[i]=Math.floor(v/pw(i))%2;}}
function build(){
K.clear(svg);cols=[];flash=[];
var p=Math.min(64,(W-8)/n),bw=n*p,x0=(W-bw)/2,r=Math.min(19,p*0.36),b=Math.min(40,p-8);
var cy=8+19,bt=cy+19+28,py=bt+b+20,H=py+8,lab=x0>=100,i;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
if(lab){var lx=x0-16;txt("c6-rl",lx,cy+4.5,"предметы",svg,"end");txt("c6-rl",lx,bt+b/2+4.5,"слово",svg,"end");txt("c6-rl",lx,py,"вес разряда",svg,"end");}
for(i=0;i<n;i++){
var cx=x0+p*(i+0.5),g=K.el("g",{"class":"c6-col"},svg);
var fl=K.el("rect",{"class":"c6-fl",x:cx-p/2+1,y:2,width:p-2,height:H-4,rx:6,opacity:0},g);
K.el("line",{"class":"c6-ln",x1:cx,y1:cy+r+2,x2:cx,y2:bt-2},g);
var gi=K.el("g",{"class":"c6-b","data-i":i,"data-p":"it",role:"button",tabindex:"0"},g);
K.el("circle",{"class":"c6-ring",cx:cx,cy:cy,r:r+4},gi);
K.el("circle",{"class":"c6-it",cx:cx,cy:cy,r:r},gi);
txt("c6-itl",cx,cy+5.5,String(i+1),gi);
K.el("rect",{"class":"w-hit",x:cx-p/2,y:cy-Math.max(r+6,18),width:p,height:2*Math.max(r+6,18)},gi);
var gd=K.el("g",{"class":"c6-b","data-i":i,"data-p":"dg",role:"button",tabindex:"0"},g);
K.el("rect",{"class":"c6-ring",x:cx-b/2-4,y:bt-4,width:b+8,height:b+8,rx:7},gd);
K.el("rect",{"class":"c6-bx",x:cx-b/2,y:bt,width:b,height:b,rx:5},gd);
var dg=txt("c6-dg",cx,bt+b/2+7.5,"0",gd);
K.el("rect",{"class":"w-hit",x:cx-p/2,y:bt-6,width:p,height:Math.max(b+12,36)},gd);
txt("c6-pv",cx,py,String(pw(i)),g);
cols.push({g:g,gi:gi,gd:gd,dg:dg});flash.push(fl);}
render();}
function setStr(a){return a.length?"{"+a.join(", ")+"}":"∅";}
function render(){var i,a=[],terms=[],v=value(),w="";
for(i=0;i<n;i++){var on=!!bits[i],c=cols[i];w+=on?"1":"0";
if(on){a.push(i+1);terms.push(String(pw(i)));}
if(c){c.g.classList.toggle("on",on);c.dg.textContent=on?"1":"0";
c.gi.setAttribute("aria-pressed",on?"true":"false");c.gi.setAttribute("aria-label","предмет "+(i+1)+(on?", выбран":", не выбран"));
c.gd.setAttribute("aria-label","цифра на месте "+(i+1)+": "+(on?"1":"0"));}}
var sum=terms.length>1?terms.join("&nbsp;+ ")+"&nbsp;= ":"";
var N=Math.pow(2,n);
out.innerHTML='<span class="c6-l"><span class="c6-nw">набор <span class="c6-set">'+setStr(a)+'</span></span> · <span class="c6-nw">выбрано <i>k</i> = <span class="c6-k">'+a.length+"</span></span></span>"+
'<span class="c6-l"><span class="c6-nw">слово <span class="c6-w">'+w+'</span></span> — <span class="c6-nw">двоичная запись</span> числа '+sum+'<b class="c6-num">'+v+"</b></span>"+
'<span class="c6-l w-dim"><span class="c6-nw">его номер среди 2'+SUP.charAt(n)+' слов,</span> <span class="c6-nw">считая с нуля: <span class="c6-idx">'+v+"</span> из 0…"+(N-1)+"</span></span>";}
/* вспышка столбцов, где цифра поменялась; при «меньше движения» — без вспышки */
function blink(ch){if(run){run.stop();run=null;}flash.forEach(function(f){f.setAttribute("opacity",0);});
if(!ch.length||K.reduced()){return;}
run=K.anim(520,function(t){var o=(0.9*(1-t)).toFixed(3);ch.forEach(function(i){if(flash[i]){flash[i].setAttribute("opacity",o);}});},function(){run=null;});}
function change(fn){var old=bits.slice(0,n),ch=[],i;fn();for(i=0;i<n;i++){if(old[i]!==bits[i]){ch.push(i);}}render();blink(ch);}
function toggle(i){change(function(){bits[i]=bits[i]?0:1;});}
svg.addEventListener("click",function(e){var g=e.target.closest?e.target.closest(".c6-b"):null;if(g){toggle(+g.getAttribute("data-i"));}});
svg.addEventListener("keydown",function(e){var g=e.target.closest?e.target.closest(".c6-b"):null;if(g&&(e.key==="Enter"||e.key===" "||e.key==="Spacebar")){e.preventDefault();toggle(+g.getAttribute("data-i"));}});
function step(d){var N=Math.pow(2,n);change(function(){setValue((value()+d+N)%N);});}
root.querySelector(".c6-dec").addEventListener("click",function(){step(-1);});
root.querySelector(".c6-inc").addEventListener("click",function(){step(1);});
root.querySelector(".c6-clr").addEventListener("click",function(){change(function(){var i;for(i=0;i<n;i++){bits[i]=0;}});});
root.querySelector(".c6-all").addEventListener("click",function(){change(function(){var i;for(i=0;i<n;i++){bits[i]=1;}});});
/* при смене n предметы с номерами больше n снимаются */
inN.addEventListener("input",function(){var m=+inN.value,i;for(i=m;i<8;i++){bits[i]=0;}n=m;vN.textContent=n;if(run){run.stop();run=null;}build();});
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

Нули впереди числа не меняют, но в слове они нужны: первый ноль в 011100 означает, что первый вкус не выбран. Поэтому длина слова всегда равна числу предметов. А главное, тройки теперь можно перебирать по порядку чисел, например по убыванию: 111000, 110100, 110010, 110001, 101100 и так далее. Ничего не пропустишь и ничего не повторишь. В первом виджете при шести предметах и трёх выбранных видны все такие слова.

Вот тот же код для выбора двух предметов из четырёх:

| набор | слово |
|---|---|
| $\{1,2\}$ | 1100 |
| $\{1,3\}$ | 1010 |
| $\{1,4\}$ | 1001 |
| $\{2,3\}$ | 0110 |
| $\{2,4\}$ | 0101 |
| $\{3,4\}$ | 0011 |

Эта таблица работает как словарь в обе стороны: каждому набору отвечает ровно одно слово, и каждое слово с двумя единицами — перевод ровно одного набора. Набор восстанавливается по слову: это номера мест, где стоят единицы.

Соответствие, которое работает в обе стороны, называют взаимно однозначным (по-учёному — биекцией). Если между двумя совокупностями есть взаимно однозначное соответствие, предметов в них поровну. Так учитель, не пересчитывая детей, видит, что их столько же, сколько стульев: каждый сидит на своём стуле, ни один стул не занят дважды, и свободных стульев нет. Поэтому тройки вкусов можно не выписывать, а считать слова: их столько же. Этим приёмом мы будем пользоваться постоянно.

## Определение

Теперь можно сказать то же самое точно. Набор, выбранный из имеющихся предметов, математики называют подмножеством, а сами предметы — элементами.

**Определение 1 (биномиальный коэффициент). Статус: выверено, SKELET опр. 1.**
Пусть $n\ge0$ и $k\ge0$ — целые числа и $[n]=\{1,2,\dots,n\}$; при $n=0$ это пустое множество. Число $\binom nk$ («из $n$ по $k$») — это количество подмножеств множества $[n]$, состоящих ровно из $k$ элементов.

Это и есть число способов выбрать $k$ предметов из $n$: по таблице $\binom32=3$, $\binom42=6$, $\binom43=4$. Вместо чисел можно брать любые предметы — людей, вершины, вкусы: важно только, сколько их. В вопросе о вкусах нужно найти $\binom63$. В русской школе пишут $C_n^k$, а запись в скобках ввёл в 1826 году австрийский математик Андреас фон Эттингсгаузен.

В определении $k$ может быть и больше $n$. Чему равно $\binom3{10}$? У множества из трёх элементов нет подмножеств из десяти элементов, поэтому $\binom3{10}=0$. Так же при любом $k\gt n$ получается $\binom nk=0$. Отдельно договариваться об этом не нужно: это следует из определения.

**Утверждение 2 (два языка). Статус: выверено, SKELET утв. 2.**
Для любых $n\ge0$ и $k\ge0$ число $\binom nk$ равно числу слов длины $n$ из нулей и единиц, в которых ровно $k$ единиц.

*Доказательство — тот же словарь.* Сопоставим подмножеству слово: на месте $i$ стоит 1, если $i$ входит в подмножество, и 0, если нет. По слову подмножество восстанавливается — это номера мест с единицами, — и любое слово так получается из какого-то подмножества. Значит, это взаимно однозначное соответствие, а число единиц в слове равно числу элементов подмножества.

В виджетах ниже слово изображено рядом клеток: единица — закрашенная клетка, ноль — пустая. Этот язык старше, чем кажется. Больше двух тысяч лет назад индийский учёный Пингала разбирал стихотворные размеры санскрита. Каждый размер задаётся последовательностью лёгких и тяжёлых слогов, то есть снова словом из двух знаков: «тяжёлый, лёгкий, лёгкий, тяжёлый» записывается как 1001. Пингала считал, сколько размеров данной длины содержат данное число тяжёлых слогов.

## Число пар

**Задача 3 (число пар). Статус: пишем с нуля.**
Сколькими способами можно выбрать два предмета из $n$?

По таблице из трёх предметов получаются три пары, из четырёх — шесть. Найдём ответ для любого $n$. Разберём три способа; в каждом сначала посчитаем пары из пяти предметов (должно получиться 10), а потом то же самое в общем виде. Нам понадобится правило произведения: если первый выбор можно сделать $a$ способами, а второй при любом первом — $b$ способами, то оба выбора вместе можно сделать $a\cdot b$ способами.

*Способ 1 — по наименьшему элементу.* Пара $\{i,j\}$ с $i\lt j$ задаётся меньшим числом $i$ и бо́льшим $j$. Если меньшее число равно $i$, бо́льшее можно выбрать $n-i$ способами: это любое из чисел $i+1,\dots,n$. Для пяти предметов при $i=1$ получаются четыре пары, при $i=2$ три, при $i=3$ две, при $i=4$ одна, всего $4+3+2+1=10$. В общем случае
$$\binom n2=(n-1)+(n-2)+\dots+2+1.$$
Чтобы сосчитать такую сумму, запишем её в обратном порядке под исходной и сложим столбиками. Для пяти предметов:
$$\begin{array}{ccccccc}4&+&3&+&2&+&1\\1&+&2&+&3&+&4\end{array}$$
Каждый столбик даёт 5, столбиков 4, поэтому удвоенная сумма равна $5\cdot4=20$, то есть $2\cdot10=20$. В общем случае каждый столбик даёт $n$, столбиков $n-1$, поэтому $2\binom n2=n(n-1)$.

*Способ 2 — клетки таблицы.* Нарисуем таблицу $n\times n$. Клетка в строке $i$ и столбце $j$ — это упорядоченная пара $(i,j)$: пары $(2,5)$ и $(5,2)$ разные, хотя множество $\{2,5\}$ одно. Клеток вне диагонали, где $i\ne j$, по правилу произведения $n(n-1)$: строку можно выбрать $n$ способами, а столбец — $n-1$ способом. С другой стороны, каждое множество $\{i,j\}$ занимает ровно две такие клетки, $(i,j)$ и $(j,i)$, одну выше диагонали и одну ниже. Значит, $n(n-1)=2\binom n2$. Для пяти предметов получается $5\cdot4=20$ клеток и 10 пар.

Клетки выше диагонали образуют лесенку; в виджете она отражается под диагональ, а после сдвига на клетку вверх две лесенки складываются в прямоугольник из $n-1$ ряда по $n$ клеток.

<div class="sim" id="sim-c5"><style>#sim-c5 .c5-g{fill:none;stroke:var(--quiet);stroke-width:1}
#sim-c5 .c5-diag{fill:var(--shade);stroke-dasharray:3 3}
#sim-c5 .c5-up{fill:var(--accent);cursor:pointer}
#sim-c5 .c5-dn{fill:var(--accent);fill-opacity:.4;stroke:var(--accent);stroke-width:1.4;cursor:pointer}
#sim-c5 .c5-up.hl{fill:var(--warm)}
#sim-c5 .c5-dn.hl{fill:var(--warm);stroke:var(--warm)}
#sim-c5 .c5-l{font-family:var(--sans);font-size:15px;fill:var(--muted);font-variant-numeric:tabular-nums}
#sim-c5 .c5-l.hl{fill:var(--warm);font-weight:600}
#sim-c5 .c5-dim{fill:none;stroke:var(--muted);stroke-width:1.2}
#sim-c5 .c5-dl{font-family:var(--sans);font-size:16px;font-weight:600;fill:var(--text);font-variant-numeric:tabular-nums}
#sim-c5 .sim-out{min-height:3.8em}
#sim-c5 .c5-nw{white-space:nowrap}</style><div class="sim-bar w-top"><label class="sim-ctl"><i>n</i><input class="c5-n" type="range" min="2" max="8" step="1" value="5"><span class="sim-v c5-nv">5</span></label></div>
<svg class="w-svg" viewBox="0 0 600 300" role="img" aria-label="Интерактив: таблица n на n, строки и столбцы занумерованы от 1 до n; клетки выше диагонали закрашены и образуют лесенку; лесенка отражается относительно диагонали, затем отражённая лесенка сдвигается на ряд вверх, и две лесенки складываются в прямоугольник из n минус 1 ряда по n клеток"></svg>
<div class="sim-bar"><button type="button" class="c5-go">отразить</button><button type="button" class="c5-sh" disabled>сдвинуть</button><button type="button" class="c5-rs" disabled>сначала</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Две лесенки складываются в прямоугольник $(n-1)\times n$.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c5");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c5-n"),vN=root.querySelector(".c5-nv"),bGo=root.querySelector(".c5-go"),bSh=root.querySelector(".c5-sh"),bRs=root.querySelector(".c5-rs");
var n=5,W=600,G=null,T=0,run=null,hl=null;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
/* T: 0 — одна лесенка; 0→1 — отражение (j,i); 1→2 — сдвиг нижней лесенки на ряд вверх */
function build(){
if(run){run.stop();run=null;}T=0;hl=null;K.clear(svg);
var lw=30,s=Math.floor(Math.min(50,(W-lw-14)/n)),x0=Math.round((W-lw-n*s)/2+lw),y0=38,gp=Math.max(2,Math.round(s*0.07)),H=y0+n*s+10,r,c;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
svg.setAttribute("data-x0",x0);svg.setAttribute("data-y0",y0);svg.setAttribute("data-s",s);svg.setAttribute("data-gp",gp);
var gG=K.el("g",{},svg),gT=K.el("g",{},svg),gU=K.el("g",{},svg),gD=K.el("g",{},svg),gM=K.el("g",{opacity:0},svg);
for(r=1;r<=n;r++){for(c=1;c<=n;c++){K.el("rect",{"class":"c5-g"+(r===c?" c5-diag":""),x:x0+(c-1)*s+gp,y:y0+(r-1)*s+gp,width:s-2*gp,height:s-2*gp,rx:3},gG);}}
var rows=[],cols=[];
for(r=1;r<=n;r++){rows.push(txt("c5-l",x0-10,y0+(r-0.5)*s+5,String(r),gT,"end"));cols.push(txt("c5-l",x0+(r-0.5)*s,y0-10,String(r),gT));}
/* размеры прямоугольника: n по горизонтали, n−1 по вертикали */
var cx=x0+n*s/2,yt=y0-15,xl=x0-15,ym=y0+(n-1)*s/2,yb=y0+(n-1)*s;
K.el("path",{"class":"c5-dim",d:"M"+(x0+gp)+","+(yt-4)+" v8 M"+(x0+gp)+","+yt+" H"+(cx-12)+" M"+(cx+12)+","+yt+" H"+(x0+n*s-gp)+" M"+(x0+n*s-gp)+","+(yt-4)+" v8"},gM);
txt("c5-dl",cx,yt+5,String(n),gM);
K.el("path",{"class":"c5-dim",d:"M"+(xl-4)+","+(y0+gp)+" h8 M"+xl+","+(y0+gp)+" V"+(ym-13)+" M"+xl+","+(ym+13)+" V"+(yb-gp)+" M"+(xl-4)+","+(yb-gp)+" h8"},gM);
txt("c5-dl",xl,ym+6,String(n-1),gM);
var P=K.ladder(n),cw=s-2*gp;
var U=P.map(function(p,q){return K.el("rect",{"class":"c5-up","data-q":q,"data-s":"u",width:cw,height:cw,rx:3},gU);});
var D=P.map(function(p,q){return K.el("rect",{"class":"c5-dn","data-q":q,"data-s":"d",width:cw,height:cw,rx:3},gD);});
G={P:P,U:U,D:D,x0:x0,y0:y0,s:s,gp:gp,gG:gG,gM:gM,rows:rows,cols:cols};
U.forEach(function(e,q){var A=XY(P[q].u);e.setAttribute("x",A[0]);e.setAttribute("y",A[1]);});
frame(0);ui();say();}
function XY(rc){return [G.x0+(rc[1]-1)*G.s+G.gp,G.y0+(rc[0]-1)*G.s+G.gp];}
function frame(tt){T=tt;var u=K.seg(tt,1,2),span=Math.max(1,n-2);
G.D.forEach(function(e,q){var p=G.P[q],A=XY(p.u),B=XY(p.d1),C=XY(p.d2),x,y,o;
if(tt<=1){var a0=0.4*(p.j-p.i-1)/span,v=K.seg(tt,a0,a0+0.6);x=A[0]+(B[0]-A[0])*v;y=A[1]+(B[1]-A[1])*v;o=K.cl(v*5,0,1);}
else{x=B[0]+(C[0]-B[0])*u;y=B[1]+(C[1]-B[1])*u;o=1;}
e.setAttribute("x",x.toFixed(2));e.setAttribute("y",y.toFixed(2));e.setAttribute("opacity",o.toFixed(3));e.style.pointerEvents=(tt>=1)?"":"none";});
G.gG.setAttribute("opacity",(1-u).toFixed(3));
var lo=(1-K.seg(tt,1,1.5)).toFixed(3);G.rows.forEach(function(e){e.setAttribute("opacity",lo);});G.cols.forEach(function(e){e.setAttribute("opacity",lo);});
G.gM.setAttribute("opacity",K.seg(tt,1.5,2).toFixed(3));}
function ui(){var busy=!!run;bGo.disabled=busy||T!==0;bSh.disabled=busy||T!==1;bRs.disabled=busy||T===0;}
function ladderSum(){var a=[],i;for(i=n-1;i>=1;i--){a.push(i);}return a.join(" + ");}
function say(){var N=n*(n-1),s;
if(T===0){s="лесенка: "+(n>2?ladderSum()+" = ":"")+"<b>"+N/2+"</b>";}
else if(T===1){s="две лесенки: упорядоченные пары (<i>i</i>, <i>j</i>), <i>i</i>&nbsp;≠&nbsp;<i>j</i>&nbsp;— <span class=\"c5-nw\">"+n+" · "+(n-1)+" = <b>"+N+"</b></span>";}
else{s="прямоугольник "+(n-1)+" × "+n+" из двух лесенок:<br><span class=\"c5-nw\">2 · "+K.bn(n,2)+" = 2 · <b>"+N/2+"</b> = "+(n-1)+" · "+n+" = "+N+" "+K.pl(N,"клетка","клетки","клеток")+"</span>";}
if(hl){var p=G.P[hl.q];s+='<br><span class="w-dim">'+(hl.s==="u"?(T>=1?"("+p.i+", "+p.j+") — ":"")+"пара {"+p.i+", "+p.j+"}":"("+p.j+", "+p.i+") — та же пара, другой порядок")+"</span>";}
out.innerHTML=s;}
function setHL(h){hl=h;var q=h?h.q:-1,both=T>=1,lab=h&&T<1.5,r=-1,c=-1;
if(h){var p=G.P[q];r=h.s==="u"?p.i:p.j;c=h.s==="u"?p.j:p.i;}
G.U.forEach(function(e,z){e.classList.toggle("hl",z===q&&(h.s==="u"||both));});
G.D.forEach(function(e,z){e.classList.toggle("hl",z===q&&both);});
G.rows.forEach(function(e,z){e.classList.toggle("hl",!!lab&&z===r-1);});G.cols.forEach(function(e,z){e.classList.toggle("hl",!!lab&&z===c-1);});
say();}
function pick(e){var t=e.target,q=t.getAttribute?t.getAttribute("data-q"):null;if(q===null||run){return null;}return {q:+q,s:t.getAttribute("data-s")};}
svg.addEventListener("pointerover",function(e){var h=pick(e);if(h){setHL(h);}});
svg.addEventListener("pointerdown",function(e){var h=pick(e);if(h){setHL(h);}else if(hl){setHL(null);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl){setHL(null);}});
function go(to,ms){if(run){return;}if(hl){setHL(null);}var from=T;
run=K.anim(ms,function(x){frame(from+(to-from)*x);},function(){run=null;frame(to);ui();say();});ui();}
bGo.addEventListener("click",function(){go(1,1700);});
bSh.addEventListener("click",function(){go(2,1300);});
bRs.addEventListener("click",function(){go(0,T>1?1500:1000);});
inN.addEventListener("input",function(){n=+inN.value;vN.textContent=n;build();});
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

*Способ 3 — стрелки и отрезки.* Отметим $n$ точек и соединим каждые две отрезком; отрезков столько же, сколько пар. Проведём стрелки от каждой точки к каждой другой и посчитаем их. Начало стрелки можно выбрать $n$ способами, конец — $n-1$ способом, всего $n(n-1)$ стрелок. С другой стороны, каждый отрезок несёт ровно две стрелки, по одной в каждую сторону. Значит, снова $n(n-1)=2\binom n2$. У пяти точек $5\cdot4=20$ стрелок и 10 отрезков. Если точки — вершины пятиугольника, это пять сторон и пять диагоналей. Так же решается задача о рукопожатиях: если каждый из $n$ человек пожал руку каждому, рукопожатий столько же, сколько пар, $\binom n2$.

<div class="sim" id="sim-c4"><style>#sim-c4 .c4-ar{fill:none;stroke:var(--accent);stroke-width:1.3}
#sim-c4 .c4-hd{fill:var(--accent)}
#sim-c4 .c4-seg{fill:none;stroke:var(--text);stroke-width:1.7}
#sim-c4 .c4-v{fill:var(--bg);stroke:var(--text);stroke-width:2}
#sim-c4 .c4-hit{fill:transparent;cursor:pointer}
#sim-c4 .c4-ar.dim,#sim-c4 .c4-hd.dim{opacity:.16}
#sim-c4 .c4-seg.dim{opacity:.22}
#sim-c4 .c4-ar.hl{stroke:var(--warm);stroke-width:2.2}
#sim-c4 .c4-hd.hl{fill:var(--warm)}
#sim-c4 .c4-seg.hl{stroke:var(--warm);stroke-width:2.6}
#sim-c4 .c4-v.hl{fill:var(--warm);stroke:var(--warm)}</style><div class="sim-bar w-top"><label class="sim-ctl"><i>n</i><input class="c4-n" type="range" min="3" max="10" step="1" value="5"><span class="sim-v c4-nv">5</span></label></div>
<svg class="w-svg" viewBox="0 0 600 420" role="img" aria-label="Интерактив: вершины правильного n-угольника, между каждыми двумя вершинами две встречные стрелки; кнопка склеивает каждую пару встречных стрелок в один отрезок"></svg>
<div class="sim-bar"><button type="button" class="c4-go">склеить пары</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Каждый отрезок склеен из двух встречных стрелок, поэтому стрелок вдвое больше.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c4");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c4-n"),vN=root.querySelector(".c4-nv"),btn=root.querySelector(".c4-go");
var n=5,W=600,G=null,s=1,run=null,sel=-1;
/* квадратичная дуга P0→P2 с контрольной точкой Q; точка и касательная при параметре u */
function qp(a,q,b,u){var v=1-u;return [v*v*a[0]+2*v*u*q[0]+u*u*b[0],v*v*a[1]+2*v*u*q[1]+u*u*b[1]];}
function qd(a,q,b,u){return [2*(1-u)*(q[0]-a[0])+2*u*(b[0]-q[0]),2*(1-u)*(q[1]-a[1])+2*u*(b[1]-q[1])];}
function dist(p,c){return Math.hypot(p[0]-c[0],p[1]-c[1]);}
/* параметр, где дуга выходит из круга радиуса rho вокруг c (бисекция; inside — сторона u0) */
function cut(a,q,b,c,rho,u0,u1){var lo=u0,hi=u1,i;for(i=0;i<30;i++){var mid=(lo+hi)/2;if(dist(qp(a,q,b,mid),c)<rho){lo=mid;}else{hi=mid;}}return (lo+hi)/2;}
function build(){
if(run){run.stop();run=null;}K.clear(svg);
var H=Math.round(Math.min(W,460)),cx=W/2,cy=H/2,R=H/2-22,rv=n>7?5:6,i;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
var P=[];for(i=0;i<n;i++){var a=-Math.PI/2+2*Math.PI*i/n;P.push([cx+R*Math.cos(a),cy+R*Math.sin(a)]);}
var gS=K.el("g",{},svg),gA=K.el("g",{},svg),gV=K.el("g",{},svg),ars=K.arrows(n).map(function(p){return {i:p[0],j:p[1],path:K.el("path",{"class":"c4-ar"},gA),hd:K.el("path",{"class":"c4-hd"},gA)};});
var segs=[];for(i=0;i<n;i++){for(var j=i+1;j<n;j++){segs.push({i:i,j:j,e:K.el("line",{"class":"c4-seg",x1:P[i][0],y1:P[i][1],x2:P[j][0],y2:P[j][1],opacity:0},gS)});}}
var vs=P.map(function(p,i){var c=K.el("circle",{"class":"c4-v",cx:p[0],cy:p[1],r:rv},gV);K.el("circle",{"class":"c4-hit",cx:p[0],cy:p[1],r:20,"data-v":i},gV);return c;});
G={P:P,ars:ars,segs:segs,vs:vs,gA:gA,gS:gS,rho:rv+4+n*1.1};frame(s);mark();}
function frame(ss){s=ss;var P=G.P,rho=G.rho,op=K.cl(ss*1.6-0.3,0,1);
G.ars.forEach(function(A){var a=P[A.i],b=P[A.j],dx=b[0]-a[0],dy=b[1]-a[1],L=Math.hypot(dx,dy),nx=-dy/L,ny=dx/L,d=Math.min(16,0.13*L)*ss;
var q=[(a[0]+b[0])/2+nx*d*2,(a[1]+b[1])/2+ny*d*2];
var u0=cut(a,q,b,a,rho,0,0.5),u1=1-cut(b,q,a,b,rho,0,0.5);
/* остриё — по касательной в конце (СК1): высота 9, основание 8 */
var T=qp(a,q,b,u1),tg=qd(a,q,b,u1),tl=Math.hypot(tg[0],tg[1]),ux=tg[0]/tl,uy=tg[1]/tl,Bx=T[0]-9*ux,By=T[1]-9*uy,u2=1-cut(b,q,a,b,rho+7,0,0.5),pts=[],k;
for(k=0;k<=16;k++){var p=qp(a,q,b,u0+(u2-u0)*k/16);pts.push(p[0].toFixed(1)+","+p[1].toFixed(1));}
A.path.setAttribute("d","M"+pts.join(" L"));A.hd.setAttribute("d","M"+(Bx-4*uy).toFixed(1)+","+(By+4*ux).toFixed(1)+" L"+T[0].toFixed(1)+","+T[1].toFixed(1)+" L"+(Bx+4*uy).toFixed(1)+","+(By-4*ux).toFixed(1)+"Z");
A.hd.setAttribute("opacity",op.toFixed(3));});G.gA.style.display=ss>0.02?"":"none";
var so=K.cl((0.25-ss)/0.25,0,1);G.segs.forEach(function(S){S.e.setAttribute("opacity",so.toFixed(3));});G.gS.style.display=so>0?"":"none";}
function mark(){var arrows=s>0.5;G.vs.forEach(function(v,i){v.classList.toggle("hl",i===sel);});
G.ars.forEach(function(A){var on=arrows&&(A.i===sel);A.path.classList.toggle("hl",on);A.hd.classList.toggle("hl",on);A.path.classList.toggle("dim",arrows&&sel>=0&&!on);A.hd.classList.toggle("dim",arrows&&sel>=0&&!on);});
G.segs.forEach(function(S){var on=!arrows&&(S.i===sel||S.j===sel);S.e.classList.toggle("hl",on);S.e.classList.toggle("dim",!arrows&&sel>=0&&!on);});
var N=n*(n-1),t;
if(arrows){t="стрелок: "+n+" · "+(n-1)+" = <b>"+N+"</b>";if(sel>=0){t+='<br><span class="w-dim">из вершины выходит '+(n-1)+" "+K.pl(n-1,"стрелка","стрелки","стрелок")+"</span>";}}
else{t="отрезков: "+K.bn(n,2)+" = <b>"+N/2+"</b>, стрелок "+N+" = 2 · "+N/2;if(sel>=0){t+='<br><span class="w-dim">из вершины выходит '+(n-1)+" "+K.pl(n-1,"отрезок","отрезка","отрезков")+"</span>";}}
out.innerHTML=t;}
svg.addEventListener("pointerdown",function(e){var v=e.target.getAttribute&&e.target.getAttribute("data-v");var i=(v===null||v===undefined)?-1:+v;sel=(i===sel)?-1:i;mark();});
btn.addEventListener("click",function(){if(run){return;}var from=s,to=s>0.5?0:1;btn.disabled=true;sel=-1;mark();
run=K.anim(1600,function(u){frame(from+(to-from)*K.ease(u));},function(){run=null;btn.disabled=false;btn.textContent=to?"склеить пары":"развести";mark();});});
inN.addEventListener("input",function(){n=+inN.value;vN.textContent=n;sel=-1;build();});
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

Все три способа привели к одному ответу.

**Утверждение 4 (число пар). Статус: выверено, SKELET утв. 4.**
Для любого целого $n\ge0$ выполняется равенство
$$\binom n2=\frac{n(n-1)}2.$$

*Доказательство — способ 2 или 3.* В каждом из них получилось $2\binom n2=n(n-1)$, и оба рассуждения годятся при любом $n$.

Во всех трёх способах работает одна мысль: двойной подсчёт. Одно и то же количество (две суммы столбиками, клетки, стрелки) считаем двумя способами. Один раз получаем произведение, которое легко найти, а другой раз — неизвестное число пар, умноженное на 2. Приравниваем два ответа: $n(n-1)=2\binom n2$. Деления здесь нет: мы только умножаем, а каждое умножение опирается на правило произведения. К этой мысли мы ещё будем возвращаться.

Со сложением задом наперёд связан анекдот: учитель задал классу сложить числа от 1 до 100, а маленький Гаусс сразу написал ответ, 5050. Это именно анекдот. В первой биографии Гаусса, вышедшей в 1856 году, история о школьной задаче есть, но чисел от 1 до 100 в ней нет; по данным Брайана Хейса, собравшего больше сотни пересказов, эти числа появляются только в книге 1938 года.

## Пустой выбор и края

**Задача 5 (пустой выбор). Статус: пишем с нуля.**
Сколькими способами можно выбрать из четырёх предметов ни одного?

Ответ: одним. Ничего не выбрать — тоже вариант выбора; в вопросе из вступления его специально исключили словами «хотя бы один вкус». На языке слов это видно сразу: слово 0000 можно написать, как и любое другое, и такое слово одно.

На языке множеств ничего не выбрать — значит взять пустое подмножество, в котором нет ни одного элемента. Множества считаются равными, если у них одни и те же элементы, поэтому пустое подмножество одно: у двух пустых множеств элементы одни и те же — никаких. Итак, $\binom40=1$.

Соберём теперь все случаи для четырёх предметов вместе. Ниже выписаны все слова длины 4 — их 16 — и разложены по числу единиц.

<figure>
<!-- static: перечень всех шестнадцати слов, двигать нечего: это итог выписывания, а не процесс -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 206" width="440" role="img" aria-label="Все шестнадцать слов длины 4 из нулей и единиц, разложенные в пять столбцов по числу единиц: в столбцах 1, 4, 6, 4 и 1 слово" style="color:var(--text,#222)">
<text x="44.0" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">0</text>
<rect x="9.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="27.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="45.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="63.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="198" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">1</text>
<text x="132.0" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">1</text>
<rect x="97.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="115.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="133.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="97.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="115.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="133.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="97.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="115.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="133.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="151.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="97.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="115.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="133.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<text x="132.0" y="198" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">4</text>
<text x="220.0" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">2</text>
<rect x="185.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="185.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="185.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="185.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="185.5" y="126" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="126" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="126" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="126" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="185.5" y="149" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="203.5" y="149" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="221.5" y="149" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="239.5" y="149" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<text x="220.0" y="198" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">6</text>
<text x="308.0" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">3</text>
<rect x="273.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="291.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="309.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="327.5" y="34" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="273.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="291.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="309.5" y="57" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="327.5" y="57" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="273.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="291.5" y="80" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="309.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="327.5" y="80" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="273.5" y="103" width="15" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="291.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="309.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="327.5" y="103" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<text x="308.0" y="198" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">4</text>
<text x="396.0" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">4</text>
<rect x="361.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="379.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="397.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<rect x="415.5" y="34" width="15" height="15" rx="2" fill="currentColor" stroke="currentColor" stroke-width="1.2"/>
<text x="396.0" y="198" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">1</text>
</svg>
<figcaption>Все слова длины 4: сверху число единиц, снизу число слов.</figcaption>
</figure>

В столбцах соответственно 1, 4, 6, 4 и 1 слово:
$$\begin{gathered}\binom40=1,\quad\binom41=4,\quad\binom42=6,\\\binom43=4,\quad\binom44=1.\end{gathered}$$
Числа ряда — высоты столбцов: мы выписали все слова длины 4 и разложили их по числу единиц, каждое слово попало ровно в один столбец. Крайние столбцы устроены просто при любом числе предметов.

**Утверждение 6 (края). Статус: выверено, SKELET утв. 3.**
Для любого целого $n\ge0$ выполняются равенства $\binom n0=1$, $\binom nn=1$ и $\binom n1=n$.

*Доказательство — посмотреть на слова.* Слово длины $n$ без единиц одно, и слово из одних единиц одно. Слово с одной единицей задаётся местом этой единицы, а мест $n$.

## Симметрия

Ряд 1, 4, 6, 4, 1 одинаково читается с обоих концов. Так же и для шести предметов $\binom62=\binom64=15$: выбрать два предмета из шести — то же самое, что выбрать четыре, которые останутся. На языке слов это ещё нагляднее. Поменяем в слове нули на единицы и наоборот: 1000 станет 0111, а 1100 станет 0011.

**Утверждение 7 (симметрия). Статус: выверено, SKELET утв. 5.**
Для любых целых $n\ge0$ и $0\le k\le n$ выполняется равенство
$$\binom nk=\binom n{n-k}.$$

*Доказательство — поменять цифры.* Заменим в слове (утверждение 2) каждый ноль единицей, а каждую единицу — нулём. Слово с $k$ единицами станет словом с $n-k$ единицами, а повторная замена вернёт исходное слово. Значит, замена — взаимно однозначное соответствие, и таких слов поровну.

<div class="sim" id="sim-c1"><style>#sim-c1 .c1-arc{fill:none;stroke:var(--muted);stroke-width:1.2;opacity:.7}
#sim-c1 .c1-arc.hl{stroke:var(--warm);stroke-width:2.2;opacity:1}
#sim-c1 .c1-flyg{pointer-events:none}
#sim-c1 .w-word.hl,#sim-c1 .w-link.hl{opacity:1}</style><div class="sim-bar w-top"><label class="sim-ctl"><i>n</i><input class="c1-n" type="range" min="2" max="6" step="1" value="5"><span class="sim-v c1-nv">5</span></label><label class="sim-ctl"><i>k</i><input class="c1-k" type="range" min="0" max="5" step="1" value="2"><span class="sim-v c1-kv">2</span></label></div>
<svg class="w-svg" viewBox="0 0 600 400" role="img" aria-label="Интерактив: слева все слова длины n из нулей и единиц с k единицами, справа все слова с n минус k единицами; линия соединяет каждое слово с его отражением, где нули и единицы поменяны местами"></svg>
<div class="sim-bar"><button type="button" class="c1-go">отразить</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Замена пустых клеток на закрашенные и обратно переводит слова с $k$ закрашенными в слова с $n-k$.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c1");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c1-n"),inK=root.querySelector(".c1-k"),vN=root.querySelector(".c1-nv"),vK=root.querySelector(".c1-kv"),btn=root.querySelector(".c1-go");
var n=5,k=2,W=600,L=[],R=[],part=[],G=null,t=0,run=null,hl=null;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
function build(){
if(run){run.stop();run=null;}t=0;hl=null;btn.textContent="отразить";btn.disabled=false;
K.clear(svg);
var N=K.C(n,k),sym=(2*k===n),i,j;
L=K.words(n,k);R=K.words(n,n-k);
var idx={};R.forEach(function(w,i){idx[K.key(w)]=i;});
part=L.map(function(w){return idx[K.key(K.flip(w))];});
var top=70,rp=K.cl(480/N,13,30),arcS=sym?Math.min(58,12+N*2.2):6;
var cp=Math.min(rp,24,((W-2*arcS-70)/2)/n),c=Math.min(cp-Math.max(2,cp*0.17),rp-3);
var ww=n*cp-(cp-c),mid=Math.min(W-2*arcS-2*ww,300),x0=(W-(2*ww+mid))/2,xL=x0,xR=x0+ww+mid;
var H=top+N*rp+8;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
function yc(i){return top+i*rp+rp/2;}
var gA=K.el("g",{},svg),gK=K.el("g",{},svg),gR=K.el("g",{},svg),gL=K.el("g",{},svg),gF=K.el("g",{"class":"c1-flyg",style:"display:none"},svg),gH=K.el("g",{},svg);
/* заголовки: сколько закрашено и сколько слов */
txt("w-lab",xL+ww/2,20,"закрашено "+k,gH);txt("w-lab",xR+ww/2,20,"закрашено "+(n-k),gH);
txt("w-num",xL+ww/2,52,String(N),gH);txt("w-num",xR+ww/2,52,String(N),gH);txt("w-eq",W/2,52,"=",gH);
var links=[];
for(i=0;i<N;i++){links.push(K.el("line",{"class":"w-link",x1:xL+ww+6,y1:yc(i),x2:xR-6,y2:yc(part[i])},gK));}
var arcs=[];
if(sym){var bmax=arcS-8;for(i=0;i<N;i++){j=part[i];if(j<=i){continue;}var b=6+(j-i)/(N-1)*(bmax-6),xa=xL-6,xb=xR+ww+6;
arcs.push({a:i,b:j,l:K.el("path",{"class":"c1-arc",d:"M"+xa+","+yc(i)+" C"+(xa-b*1.33)+","+yc(i)+" "+(xa-b*1.33)+","+yc(j)+" "+xa+","+yc(j)},gA),r:K.el("path",{"class":"c1-arc",d:"M"+xb+","+yc(i)+" C"+(xb+b*1.33)+","+yc(i)+" "+(xb+b*1.33)+","+yc(j)+" "+xb+","+yc(j)},gA)});}}
/* side "L"/"R" — слово с рамкой и зоной касания; side "" — летящая копия левого слова */
function word(w,x,i,par,side){var g=K.el("g",{"class":side?"w-word":"c1-fly","data-side":side||"F","data-i":i},par),cells=[],q;
if(side){K.el("rect",{"class":"w-frame",x:x-3.5,y:yc(i)-c/2-3.5,width:ww+7,height:c+7,rx:4},g);}
for(q=0;q<n;q++){var cx=x+q*cp+c/2;cells.push({e:K.el("rect",{"class":"w-c"+(w[q]?" on":""),x:cx-c/2,y:yc(i)-c/2,width:c,height:c,rx:Math.min(3,c*0.18)},g),cx:cx,b:w[q]});}
if(side){K.el("rect",{"class":"w-hit",x:x-4,y:yc(i)-rp/2,width:ww+8,height:rp},g);}
return {g:g,cells:cells};}
var WL=L.map(function(w,i){return word(w,xL,i,gL,"L");}),WR=R.map(function(w,i){return word(w,xR,i,gR,"R");}),WF=L.map(function(w,i){return word(w,xL,i,gF,"");});
G={N:N,sym:sym,xL:xL,xR:xR,ww:ww,c:c,yc:yc,links:links,arcs:arcs,WL:WL,WR:WR,WF:WF,gR:gR,gF:gF};
say();}
/* левые слова остаются на месте (приглушаются), их копии отражаются в полёте и садятся на правые слова */
function frame(tt){t=tt;var N1=Math.max(1,G.N-1),dx=G.xR-G.xL,dim=(1-0.6*K.seg(tt,0,0.25)).toFixed(3);
G.gF.style.display=tt>0?"":"none";
G.WL.forEach(function(o){o.g.setAttribute("opacity",dim);});
G.WF.forEach(function(o,i){var a0=0.04+0.42*i/N1,v=K.seg(tt,a0,a0+0.54),u=K.cl((v-0.2)/0.6,0,1),sx=Math.abs(Math.cos(Math.PI*u)),fl=(u>=0.5);
o.cells.forEach(function(c){var on=fl?!c.b:c.b,w=G.c*sx;c.e.setAttribute("x",c.cx-w/2);c.e.setAttribute("width",Math.max(w,0.01));c.e.setAttribute("class","w-c"+(on?" on":""));});
o.g.setAttribute("transform","translate("+(dx*v).toFixed(2)+","+((G.yc(part[i])-G.yc(i))*v).toFixed(2)+")");});
G.gR.setAttribute("opacity",(1-0.55*K.seg(tt,0.3,1)).toFixed(3));
var lo=(1-0.85*K.cl(tt/0.4,0,1)).toFixed(3);G.links.forEach(function(e){e.setAttribute("opacity",lo);});}
function setHL(side,i){hl=(side===null)?null:{l:side==="L"?i:part.indexOf(i)};
var li=hl?hl.l:-1,ri=hl?part[li]:-1;
G.WL.forEach(function(o,q){o.g.classList.toggle("hl",q===li);});G.WR.forEach(function(o,q){o.g.classList.toggle("hl",q===ri);});
G.links.forEach(function(e,q){e.classList.toggle("hl",q===li);});
G.arcs.forEach(function(a){var on=hl&&((a.a===li||a.b===li));a.l.classList.toggle("hl",!!on);a.r.classList.toggle("hl",!!on);});
say();}
function say(){var N=G.N,s=K.bn(n,k)+" = "+N+" = "+K.bn(n,n-k);
if(G.sym){s+='<br><span class="w-dim">те же слова, но ни одно не переходит в&nbsp;себя: '+(N/2)+"&nbsp;"+K.pl(N/2,"пара","пары","пар")+"</span>";}
if(hl){var a=K.key(L[hl.l]),b=K.key(R[part[hl.l]]);s+='<br><span class="w-dim">'+a+" ↔ "+b+"</span>";}
out.innerHTML=s;}
function pick(e){var g=e.target.closest?e.target.closest(".w-word"):null;if(!g||run){return null;}return g;}
svg.addEventListener("pointerover",function(e){var g=pick(e);if(g){setHL(g.getAttribute("data-side"),+g.getAttribute("data-i"));}});
svg.addEventListener("pointerdown",function(e){var g=pick(e);if(g){setHL(g.getAttribute("data-side"),+g.getAttribute("data-i"));}else if(hl){setHL(null);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl){setHL(null);}});
btn.addEventListener("click",function(){if(run){return;}if(hl){setHL(null);}var from=t,to=(t>0.5)?0:1;btn.disabled=true;
run=K.anim(1500+40*G.N,function(s){frame(from+(to-from)*s);},function(){run=null;btn.disabled=false;btn.textContent=to?"вернуть":"отразить";});});
function upd(){n=+inN.value;inK.max=n;k=Math.min(+inK.value,n);inK.value=k;vN.textContent=n;vK.textContent=k;build();}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

В частности, при $n\ge1$ выполняется $\binom n{n-1}=\binom n1=n$: слово с одним нулём задаётся местом этого нуля. В трактате Чараки сочетания из пяти вкусов описаны именно так: их шесть, потому что из смеси каждый раз исключается ровно один вкус. Набор из пяти вкусов задаётся тем единственным, которого в нём нет.

## Треугольник Паскаля

**Определение 8 (треугольник Паскаля). Статус: выверено, SKELET опр. 5.1.**
Треугольник Паскаля — таблица из строк с номерами $n=0,1,2,\dots$; в строке номер $n$ стоят числа $\binom n0,\binom n1,\dots,\binom nn$.

Строки нумеруются с нуля, и ряд для четырёх предметов оказывается строкой номер 4. Заполним строки с номерами от 0 до 6 тем, что уже доказано: края по утверждению 6, числа $\binom n2$ по утверждению 4, остальное отражением по утверждению 7. Наверху стоит $\binom00=1$: из пустого множества можно выбрать ровно одно подмножество — его самого.
$$\begin{array}{c}1\\1\quad1\\1\quad2\quad1\\1\quad3\quad3\quad1\\1\quad4\quad6\quad4\quad1\\1\quad5\quad10\quad10\quad5\quad1\\1\quad6\quad15\quad\boxed{\,?\,}\quad15\quad6\quad1\end{array}$$

Заполнились все клетки, кроме одной. Утверждения 4, 6 и 7 дают $\binom nk$, когда $k$ или $n-k$ не больше двух, а в строках с номерами от 0 до 6 только у одной клетки и $k$, и $n-k$ не меньше трёх — у $\binom63$. Это и есть вопрос о трёх вкусах из шести. Чтобы ответить на него, нужен новый инструмент.

## Правило Паскаля

Присмотримся к треугольнику: каждое число в нём, кроме крайних, равно сумме двух чисел над ним, например $6=3+3$ и $10=4+6$. Это не совпадение.

Разберём сначала один случай: почему $\binom52=\binom41+\binom42$? Выпишем все слова длины 5 с двумя единицами и разложим их на две кучки по первой цифре. С 1 начинаются слова 11000, 10100, 10010, 10001. Если стереть первую единицу, останутся все слова длины 4 с одной единицей, их $\binom41=4$. Остальные шесть слов начинаются с 0: 01100, 01010, 01001, 00110, 00101, 00011. Если стереть первый ноль, останутся все слова длины 4 с двумя единицами, их $\binom42=6$. Вместе $4+6=10=\binom52$.

Так же устроен край строки. Почему $\binom44=\binom33+\binom34$? Слово длины 4 с четырьмя единицами одно, 1111, и оно начинается с 1; без первой цифры остаётся 111, то есть $\binom33=1$. Слов, которые начинаются с 0, нет вовсе: тогда на остальных трёх местах пришлось бы поставить четыре единицы. И правая часть с этим согласна: $\binom34=0$.

**Утверждение 9 (правило Паскаля). Статус: выверено, SKELET утв. 7.**
Для любых целых $n\ge1$ и $1\le k\le n$ выполняется равенство
$$\binom nk=\binom{n-1}{k-1}+\binom{n-1}{k}.$$

*Доказательство — разделить слова по первой цифре.* Разложим слова длины $n$ с $k$ единицами (утверждение 2) на две кучки.
**Случай 1: слово начинается с 1.** Сотрём первую цифру — останется слово длины $n-1$ с $k-1$ единицами; приписав 1 спереди, вернём исходное слово. Значит, в кучке $\binom{n-1}{k-1}$ слов.
**Случай 2: слово начинается с 0.** Сотрём первую цифру — останется слово длины $n-1$ с $k$ единицами; приписав 0, вернём исходное. В кучке $\binom{n-1}{k}$ слов; при $k=n$ кучка пуста, и $\binom{n-1}n=0$.
**Итог.** В двух кучках вместе лежат все слова, а их $\binom nk$.

<div class="sim" id="sim-c2"><style>#sim-c2 .c2-first{stroke:var(--warm);stroke-width:2}
#sim-c2 .c2-first.on{stroke:var(--warm)}</style><div class="sim-bar w-top"><label class="sim-ctl"><i>n</i><input class="c2-n" type="range" min="2" max="6" step="1" value="5"><span class="sim-v c2-nv">6</span></label><label class="sim-ctl"><i>k</i><input class="c2-k" type="range" min="1" max="5" step="1" value="2"><span class="sim-v c2-kv">3</span></label></div>
<svg class="w-svg" viewBox="0 0 600 340" role="img" aria-label="Интерактив: все слова длины n из нулей и единиц с k единицами разъезжаются в две кучки по первой цифре, после чего первая цифра стирается и остаются слова длины n минус 1"></svg>
<div class="sim-bar"><button type="button" class="c2-go">разделить по первой цифре</button><button type="button" class="c2-back" disabled>собрать обратно</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Слова разложены на две кучки по первой клетке.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c2");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c2-n"),inK=root.querySelector(".c2-k"),vN=root.querySelector(".c2-nv"),vK=root.querySelector(".c2-kv"),go=root.querySelector(".c2-go"),back=root.querySelector(".c2-back");
var n=5,k=2,W=600,G=null,t=0,run=null;
function txt(cls,x,y,s,par){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":"middle"},par);e.textContent=s;return e;}
function build(){
if(run){run.stop();run=null;}t=0;K.clear(svg);
var ws=K.words(n,k),N=ws.length,a=K.C(n-1,k-1),b=K.C(n-1,k);
/* вперемешку: по убыванию перевёрнутого слова, чтобы первая цифра чередовалась */
var mix=ws.map(function(w,i){return i;}).sort(function(p,q){var A=ws[p].slice().reverse().join(""),B=ws[q].slice().reverse().join("");return A<B?1:(A>B?-1:0);});
var rp=W<480?24:27,c=Math.min(19,rp-6,((W*0.44)-3*(n-1))/n),cp=c+3,ww=n*cp-3,top=88;
var cols=N>Math.max(a,b)?2:1,rowsA=Math.ceil(N/cols),gapA=22,bw=cols*ww+(cols-1)*gapA,xA=(W-bw)/2;
var off=Math.min(W*0.24,175),cx1=W/2-off,cx0=W/2+off;
var rows=Math.max(rowsA,a,b),H=top+rows*rp+4;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
var hA=K.el("g",{},svg),hB=K.el("g",{opacity:0},svg),gw=K.el("g",{},svg);
txt("w-lab",W/2,40,"длина "+n+", закрашено "+k,hA);txt("w-num",W/2,74,String(N),hA);
/* подписи кучек держатся до сброса; после стирания первой клетки под ними проявляется «длина n−1, закрашено …» */
txt("w-lab",cx1,18,"первая закрашена",hB);txt("w-lab",cx0,18,"первая пустая",hB);
var lc1=txt("w-lab",cx1,40,"длина "+(n-1)+", закрашено "+(k-1),hB),lc0=txt("w-lab",cx0,40,"длина "+(n-1)+", закрашено "+k,hB);
txt("w-num",cx1,74,String(a),hB);txt("w-num",cx0,74,String(b),hB);txt("w-eq",W/2,74,"+",hB);
var items=[];
mix.forEach(function(wi,q){var w=ws[wi],g=K.el("g",{},gw),cells=[],j;
for(j=0;j<n;j++){cells.push(K.el("rect",{"class":"w-c"+(w[j]?" on":"")+(j===0?" c2-first":""),x:j*cp,y:-c/2,width:c,height:c,rx:Math.min(3,c*0.18)},g));}
var A={x:xA+(q%cols)*(ww+gapA),y:top+Math.floor(q/cols)*rp+rp/2},B;
var r=0;ws.forEach(function(v,z){if(z<wi&&v[0]===w[0]){r++;}});B={x:(w[0]?cx1:cx0)-ww/2,y:top+r*rp+rp/2};
items.push({g:g,first:cells[0],A:A,B:B,d:q/Math.max(1,N-1)});});
G={N:N,a:a,b:b,cp:cp,items:items,hA:hA,hB:hB,lc:[lc1,lc0]};
frame(0);go.disabled=false;back.disabled=true;say(false);}
function frame(tt){t=tt;var sh=K.seg(tt,0.72,1)*(-G.cp/2),fo=1-K.seg(tt,0.64,0.84),sw=K.seg(tt,0.7,0.86);
G.items.forEach(function(it){var a0=0.04+0.3*it.d,m=K.seg(tt,a0,a0+0.28),x=it.A.x+(it.B.x-it.A.x)*m+sh*m,y=it.A.y+(it.B.y-it.A.y)*m;
it.g.setAttribute("transform","translate("+x.toFixed(2)+","+y.toFixed(2)+")");it.first.setAttribute("opacity",fo.toFixed(3));});
G.hA.setAttribute("opacity",(1-K.seg(tt,0,0.15)).toFixed(3));G.hB.setAttribute("opacity",K.seg(tt,0.5,0.64).toFixed(3));
G.lc.forEach(function(e){e.setAttribute("opacity",sw.toFixed(3));});}
function say(done){var s=K.bn(n,k)+" = "+G.N;
if(done){s=K.bn(n,k)+" = "+K.bn(n-1,k-1)+" + "+K.bn(n-1,k)+'<br><span class="w-dim">'+G.N+" = "+G.a+" + "+G.b+"</span>";}
out.innerHTML=s;}
function play(to){if(run){return;}var from=t;go.disabled=true;back.disabled=true;if(!to){say(false);}
run=K.anim(2600,function(s){frame(from+(to-from)*s);},function(){run=null;go.disabled=!!to;back.disabled=!to;say(!!to);});}
go.addEventListener("click",function(){play(1);});back.addEventListener("click",function(){play(0);});
function upd(){n=+inN.value;inK.max=n-1;k=Math.min(+inK.value,n-1);inK.value=k;vN.textContent=n;vK.textContent=k;build();}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

Единица $\binom00=1$ наверху треугольника с правилом согласована: строка 1 получается из строки 0, $\binom11=\binom00+\binom01=1+0$.

Теперь можно заполнить последнюю клетку:
$$\binom63=\binom52+\binom53=10+10=20.$$
Из шести вкусов можно составить 20 смесей ровно по три.

То же правило годится и для людей. Выберем из восьми человек троих дежурных и отметим одного из восьми, скажем Веру. Групп с Верой $\binom72$ — к ней нужно добавить двоих из оставшихся семи; групп без Веры $\binom73$. Строка номер 7 складывается из строки номер 6: $\binom72=6+15=21$, $\binom73=15+20=35$. Итого $\binom83=21+35=56$.

## Размещения

Правило Паскаля заполняет треугольник строку за строкой, но чтобы дойти до $\binom{16}4$ Варахамихиры, понадобилось бы шестнадцать строк. Нужна формула, которая даёт число сразу.

Формулу можно было бы искать, сравнивая соседние числа одной строки. Но у биномиальных коэффициентов закономерность там не видна: в строке номер 6 стоят 1, 6, 15, 20, и от 6 к 15 целым множителем не перейти. Чтобы понять, как сравнивать соседей, отвлечёмся на похожую задачу, в которой важен порядок.

Выберем из трёх человек, Веры, Пети и Оли, капитана и заместителя. Запишем выбор парой: сначала капитан, потом заместитель. Получится шесть вариантов: ВП, ВО, ПВ, ПО, ОВ, ОП. Пар без ролей было бы три, а здесь каждая пара встречается дважды: капитан Вера и заместитель Петя — не тот же выбор, что капитан Петя и заместитель Вера.

**Определение 10 (размещение). Статус: пишем с нуля.**
Размещение из $n$ по $k$ — это $k$ разных предметов из данных $n$, выписанных по порядку: первый, второй, …, $k$-й. Число размещений из $n$ по $k$ обозначается $n^{\underline k}$.

Обозначение взято из книги Грэхема, Кнута и Паташника «Конкретная математика», а само число называют ещё убывающим факториалом. Мы только что нашли $3^{\underline 2}=6$. Ничего не выбрать можно одним способом, поэтому $n^{\underline 0}=1$. Если $k\gt n$, разных предметов не хватит, и $n^{\underline k}=0$.

Есть ли у размещений своё правило Паскаля? Возьмём $4^{\underline 2}$ — число способов выбрать капитана и заместителя из четырёх человек: к Вере, Пете и Оле добавим Гошу. Отметим Веру. Если Вера не выбрана, капитана и заместителя выбирают из трёх остальных: $3^{\underline 2}=6$ способов. Если выбрана, она капитан или заместитель — 2 способа, а на оставшееся место годится любой из трёх остальных: $2\cdot3^{\underline 1}=6$ способов. Всего $4^{\underline 2}=6+6=12$.

**Утверждение 11 (правило Паскаля для размещений). Статус: пишем с нуля.**
Для любых целых $n\ge1$ и $1\le k\le n$ выполняется равенство
$$n^{\underline k}=(n-1)^{\underline k}+k\cdot(n-1)^{\underline{k-1}}.$$

*Доказательство — по Вере.* Размещений без Веры столько же, сколько размещений из остальных $n-1$ человек по $k$. В размещении с Верой её место можно выбрать $k$ способами, а остальные $k-1$ мест по порядку заполнить из $n-1$ человек — $(n-1)^{\underline{k-1}}$ способами. По правилу произведения размещений с Верой $k\cdot(n-1)^{\underline{k-1}}$.

Заполним этим правилом первые строки треугольника: в строке $n$ стоят числа $n^{\underline 0},n^{\underline 1},\dots,n^{\underline n}$.
$$\begin{array}{c}1\\1\quad1\\1\quad2\quad2\\1\quad3\quad6\quad6\\1\quad4\quad12\quad24\quad24\\1\quad5\quad20\quad60\quad120\quad120\end{array}$$

Правило понятное, но считать по нему тяжело. Число складывается из двух чисел над ним, причём левое из них ещё умножается на $k$, номер места нового числа (места считаем с нуля). Числа растут быстро: в строке 5 уже стоит 120. А чтобы дойти до строки 8, пришлось бы заполнить все строки до неё.

Посмотрим вместо этого на соседей в одной строке. В строке 4 стоят 1, 4, 12, 24, 24: каждое следующее число получается из предыдущего умножением на 4, 3, 2 и 1.

**Утверждение 12 (соседи у размещений). Статус: пишем с нуля.**
Для любых целых $n\ge1$ и $1\le k\le n$ выполняются равенства
$$\begin{gathered}n^{\underline k}=n^{\underline{k-1}}\cdot(n-k+1),\\n^{\underline k}=n\cdot(n-1)^{\underline{k-1}}.\end{gathered}$$

*Доказательство — два порядка выбора.* Первое равенство: сначала заполним первые $k-1$ мест, $n^{\underline{k-1}}$ способами; на последнее место остаётся $n-(k-1)=n-k+1$ человек. Второе: сначала выберем первого, $n$ способами, потом расставим за ним $k-1$ человек из $n-1$ оставшихся.

Первое равенство связывает соседей в строке, второе — соседей по диагонали. Теперь до любого числа можно дойти от единицы на краю, не заполняя строк выше.

**Задача 13 (капитан, заместитель и третий). Статус: пишем с нуля.**
Сколькими способами можно выбрать из восьми человек капитана, заместителя и третьего игрока?

Пройдём по строке 8 от края по первому равенству утверждения 12: $8^{\underline 1}=1\cdot8=8$, $8^{\underline 2}=8\cdot7=56$, $8^{\underline 3}=56\cdot6=336$. Тот же ответ даёт и прямой подсчёт: капитана можно выбрать 8 способами, заместителя из оставшихся — 7, третьего — 6.

Каждый шаг вдоль строки добавляет один множитель, и после $k$ шагов получается произведение.

**Утверждение 14 (число размещений). Статус: пишем с нуля.**
Для любых целых $n\ge0$ и $0\le k\le n$ выполняется равенство
$$n^{\underline k}=n(n-1)\cdots(n-k+1).$$
При $k=0$ произведение пусто и считается равным 1.

*Доказательство — ходьба вдоль строки от края.* Начнём с $n^{\underline 0}=1$ и применим первое равенство утверждения 12 $k$ раз: множители $n$, $n-1$, …, $n-k+1$ дают нужное произведение.

Последнее число строки, $n^{\underline n}$, — это число способов расставить по порядку все $n$ предметов. Для него есть своё обозначение.

**Определение 15 (факториал). Статус: выверено, SKELET опр. 10.**
Для целого $n\ge1$ число $n!$ («эн факториал») равно $1\cdot2\cdot\ldots\cdot n$; кроме того, $0!=1$.

По утверждению 14 $n!=n^{\underline n}$. Например, $3!=6$ и $10!=3\,628\,800$. Договорённость $0!=1$ согласуется с тем, что $n^{\underline 0}=1$: расставить ноль предметов можно одним способом. Второе равенство утверждения 12 при $k=n$ даёт $n!=n\cdot(n-1)!$, например $6!=6\cdot5!$: чтобы расставить шестерых, выберем первого, а остальных пятерых расставим за ним.

С размещениями всё обстоит наоборот, чем с биномиальными коэффициентами: правило Паскаля сложное, а соседей сравнивать просто, каждое число получается из соседа одним умножением.

## Формула

Вернёмся к треугольнику Паскаля и сравним соседей тем же приёмом, что в утверждении 12: одно и то же количество будем выбирать в разном порядке.

**Задача 16 (команда с капитаном). Статус: пишем с нуля.**
В классе 25 человек. Нужно выбрать футбольную команду из 11 игроков, а в ней — капитана. Сколькими способами это можно сделать?

Посчитаем тремя способами.

*Сначала капитан.* Капитана можно выбрать 25 способами, потом остальных 10 игроков из 24 человек — $\binom{24}{10}$ способами. Всего $25\cdot\binom{24}{10}$.

*Сначала рядовые.* Десять игроков без капитана можно выбрать $\binom{25}{10}$ способами, потом капитана из 15 оставшихся — 15 способами. Всего $\binom{25}{10}\cdot15$.

*Сначала вся команда.* Команду из 11 человек можно выбрать $\binom{25}{11}$ способами, потом капитана из её 11 игроков. Всего $\binom{25}{11}\cdot11$.

Во всех трёх случаях посчитано одно и то же, поэтому
$$25\binom{24}{10}=15\binom{25}{10}=11\binom{25}{11}.$$
Самих чисел мы пока не знаем, но связь между ними уже есть. Теперь заменим 25 человек на $n$, а 11 игроков — на $k+1$: тогда рядовых будет $k$, и в равенстве встретятся соседние числа строки, $\binom nk$ и $\binom n{k+1}$.

**Утверждение 17 (капитан). Статус: выверено, SKELET утв. 8.**
Для любых целых $n\ge1$ и $k\ge0$ выполняются равенства
$$n\binom{n-1}k=(n-k)\binom nk=(k+1)\binom n{k+1}.$$

*Доказательство — три порядка выбора.* Все три числа равны количеству способов выбрать из $n$ человек команду из $k+1$ человека и в ней капитана.
**Порядок 1.** Сначала капитан — $n$ способов, затем $k$ рядовых из $n-1$ человека — $\binom{n-1}k$ способов.
**Порядок 2.** Сначала $k$ рядовых — $\binom nk$ способов, затем капитан из $n-k$ оставшихся.
**Порядок 3.** Сначала вся команда — $\binom n{k+1}$ способов, затем капитан из $k+1$ её членов.
В каждом порядке два выбора задают команду с капитаном однозначно, и каждая команда с капитаном получается ровно один раз. Если $k+1\gt n$, команды не собрать, и все три числа равны нулю.

<div class="sim" id="sim-c3"><style>#sim-c3 .c3-card{fill:none;stroke:var(--faint);stroke-width:1}
#sim-c3 .c3-m{fill:var(--accent)}
#sim-c3 .c3-o{fill:none;stroke:var(--quiet);stroke-width:1.1}
#sim-c3 .c3-cap{fill:var(--warm);stroke:var(--warm);stroke-width:1;stroke-linejoin:round}
#sim-c3 .sim-out{line-height:1.45;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:.1em .15em}
#sim-c3 .c3-w{display:inline-flex;flex-direction:column;align-items:center;padding:.15em .45em .2em;border-radius:8px;border:1px solid transparent;transition:background-color .2s,border-color .2s,color .2s}
#sim-c3 .c3-w.on{color:var(--accent);background:var(--accent-soft);border-color:var(--accent)}
#sim-c3 .c3-v{color:var(--muted);font-variant-numeric:tabular-nums}
#sim-c3 .c3-w.on .c3-v{color:var(--accent);font-weight:600}
#sim-c3 .c3-eq{color:var(--muted);padding:0 .1em}
#sim-c3 .c3-tot{font-weight:600;font-variant-numeric:tabular-nums}</style><div class="sim-bar w-top"><label class="sim-ctl"><i>n</i><input class="c3-n" type="range" min="3" max="6" step="1" value="6"><span class="sim-v c3-nv">6</span></label><label class="sim-ctl"><span>команда (<i>k</i>+1)</span><input class="c3-m" type="range" min="2" max="5" step="1" value="3"><span class="sim-v c3-mv">3</span></label></div>
<div class="sim-bar w-top c3-modes"><button type="button" class="c3-b on" data-m="0">сначала капитан</button><button type="button" class="c3-b" data-m="2">сначала рядовые</button><button type="button" class="c3-b" data-m="1">сначала команда</button></div>
<svg class="w-svg" viewBox="0 0 600 400" role="img" aria-label="Интерактив: карточки, на каждой ряд из n человек, закрашены члены команды, звездой отмечен капитан; одни и те же карточки раскладываются в стопки тремя способами"></svg>
<div class="sim-out"></div>
<div class="sim-cap">Одни и те же команды с капитаном, разложенные в стопки тремя способами.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c3");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c3-n"),inM=root.querySelector(".c3-m"),vN=root.querySelector(".c3-nv"),vM=root.querySelector(".c3-mv"),bs=root.querySelectorAll(".c3-b");
var n=6,m=3,W=600,mode=0,G=null,run=null,Hc=0;
function star(cx,cy,R){var p=[],i;for(i=0;i<10;i++){var a=-Math.PI/2+i*Math.PI/5,r=i%2?R*0.45:R;p.push((cx+r*Math.cos(a)).toFixed(2)+","+(cy+r*Math.sin(a)).toFixed(2));}return p.join(" ");}
/* три способа разложить: ключ стопки и порядок стопок (0 — капитан, 1 — команда, 2 — рядовые) */
function stacks(cards,md){var ord=cards.map(function(c,i){return i;}),kf;
if(md===0){kf=function(c){return c.cap;};ord.sort(function(a,b){return cards[a].cap-cards[b].cap||(K.key(cards[a].team)<K.key(cards[b].team)?1:-1);});}
else if(md===1){kf=function(c){return K.key(c.team);};}
else{kf=function(c){var t=c.team.slice();t[c.cap]=0;return K.key(t);};ord.sort(function(a,b){var A=cards[a].team.slice(),B=cards[b].team.slice();A[cards[a].cap]=0;B[cards[b].cap]=0;A=K.key(A);B=K.key(B);return A<B?1:(A>B?-1:cards[a].cap-cards[b].cap);});}
var gs=K.groups(ord.map(function(i){return cards[i];}),kf);return gs.map(function(g){return g.map(function(j){return ord[j];});});}
function setH(h){Hc=h;svg.setAttribute("viewBox","0 0 "+W+" "+h.toFixed(1));}
function build(){
if(run){run.stop();run=null;}K.clear(svg);
var cards=K.cards(n,m),pc=W>=560?15:(W>=420?13:12),cw=n*pc+6,ch=pc+6,gy=3,gx=W>=560?16:12,rg=20,top=36;
var lay=[0,1,2].map(function(md){var st=stacks(cards,md),S=st.length,z=st[0].length,per=Math.max(1,Math.min(S,Math.floor((W+gx)/(cw+gx)))),rows=Math.ceil(S/per);per=Math.ceil(S/rows);
var sh=z*(ch+gy)-gy,x0=(W-(per*cw+(per-1)*gx))/2,pos=[];
var last=S-(rows-1)*per;st.forEach(function(g,s){var sh0=(Math.floor(s/per)===rows-1)?(per-last)*(cw+gx)/2:0;g.forEach(function(ci,j){pos[ci]={x:x0+sh0+(s%per)*(cw+gx),y:top+Math.floor(s/per)*(sh+rg)+j*(ch+gy),d:(s*z+j)/Math.max(1,cards.length-1)};});});
return {S:S,z:z,pos:pos,H:top+rows*sh+(rows-1)*rg+6};});
/* высота рисунка — по активной раскладке: под низкими стопками нет пустой полосы */
setH(lay[mode].H);
var lab=K.el("text",{"class":"w-lab",x:W/2,y:20,"text-anchor":"middle"},svg),gc=K.el("g",{},svg);
var items=cards.map(function(c,i){var g=K.el("g",{},gc),q,y=ch/2;K.el("rect",{"class":"c3-card",x:0.5,y:0.5,width:cw-1,height:ch-1,rx:4},g);
for(q=0;q<n;q++){var x=3+pc/2+q*pc;if(q===c.cap){K.el("polygon",{"class":"c3-cap",points:star(x,y,pc*0.5)},g);}else if(c.team[q]){K.el("circle",{"class":"c3-m",cx:x,cy:y,r:pc*0.33},g);}else{K.el("circle",{"class":"c3-o",cx:x,cy:y,r:pc*0.3},g);}}
var p=lay[mode].pos[i];g.setAttribute("transform","translate("+p.x+","+p.y+")");return {g:g,x:p.x,y:p.y};});
G={cards:cards,lay:lay,items:items,lab:lab,ch:ch};say();}
/* строка вывода: три произведения в порядке кнопок, над числами — их биномиальная запись; активное выделено */
function say(){var L=G.lay[mode],k=m-1,N=G.cards.length;
G.lab.textContent=L.S+" "+K.pl(L.S,"стопка","стопки","стопок")+" по "+L.z+" "+K.pl(L.z,"карточке","карточки","карточек");
function w(md,f,v){return '<span class="c3-w'+(md===mode?" on":"")+'" data-m="'+md+'"><span class="c3-f">'+f+'</span><span class="c3-v">'+v+"</span></span>";}
var eq='<span class="c3-eq">=</span>';
out.innerHTML=w(0,n+"·"+K.bn(n-1,k),n+" · "+K.C(n-1,k))+eq+w(2,K.bn(n,k)+"·"+(n-k),K.C(n,k)+" · "+(n-k))+eq+w(1,K.bn(n,m)+"·"+m,K.C(n,m)+" · "+m)+eq+'<span class="c3-tot">'+N+"</span>";
bs.forEach(function(b){b.classList.toggle("on",+b.getAttribute("data-m")===mode);});}
function setMode(md){if(md===mode){return;}if(run){run.stop();}mode=md;say();var P=G.lay[mode].pos,from=G.items.map(function(it){return {x:it.x,y:it.y};}),H0=Hc,H1=G.lay[mode].H,ch=G.ch;
run=K.anim(1300,function(t){var bot=0;G.items.forEach(function(it,i){var a0=0.32*P[i].d,s=K.seg(t,a0,a0+0.68);it.x=from[i].x+(P[i].x-from[i].x)*s;it.y=from[i].y+(P[i].y-from[i].y)*s;bot=Math.max(bot,it.y+ch+6);it.g.setAttribute("transform","translate("+it.x.toFixed(2)+","+it.y.toFixed(2)+")");});
/* высота плавно идёт к новой, но не срезает карточки, которые ещё не долетели */
setH(t>=1?H1:Math.max(H0+(H1-H0)*K.ease(t),bot));},function(){run=null;});}
bs.forEach(function(b){b.addEventListener("click",function(){setMode(+b.getAttribute("data-m"));});});
function upd(){n=+inN.value;inM.max=n-1;m=K.cl(+inM.value,2,n-1);inM.value=m;inM.disabled=(n-1<=2);vN.textContent=n;vM.textContent=m;build();}
inN.addEventListener("input",upd);inM.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

В равенстве $(n-k)\binom nk=(k+1)\binom n{k+1}$ перенесём множитель $k+1$ в другую часть и получим связь между соседними числами строки.

**Утверждение 18 (шаг вдоль строки). Статус: выверено, SKELET сл. 9.**
Для любых целых $n\ge1$ и $0\le k\le n-1$ соседние числа строки $n$ связаны равенством
$$\binom n{k+1}=\frac{n-k}{k+1}\binom nk.$$

Пройдём так по шестой строке от левого края. При $n=6$ множитель $\frac{n-k}{k+1}$ равен $\frac61$ при $k=0$, $\frac52$ при $k=1$ и $\frac43$ при $k=2$: $\binom61=\frac61\cdot1=6$, $\binom62=\frac52\cdot6=15$, $\binom63=\frac43\cdot15=20$. Двадцать смесей мы нашли без таблицы. На рисунке каждая стрелка несёт свой множитель. Дойти до клетки от единицы на краю можно четырьмя путями: по строке слева или справа и по одной из двух диагоналей.

<div class="sim" id="sim-c7"><style>#sim-c7 svg:focus{outline:none}
#sim-c7 svg:focus-visible{outline:2px solid var(--accent);outline-offset:4px;border-radius:10px}
#sim-c7 .c7-box{fill:var(--panel);stroke:var(--rule);stroke-width:1.2;transition:fill .15s,stroke .15s}
#sim-c7 .c7-num{font-family:var(--sans);fill:var(--text);text-anchor:middle;font-variant-numeric:tabular-nums;pointer-events:none}
#sim-c7 .c7-hit{fill:transparent;cursor:pointer}
#sim-c7 .c7-cell:hover .c7-box{stroke:var(--accent)}
#sim-c7 .c7-cell.on .c7-box{stroke-width:1.8}
#sim-c7 .c7-cell.st .c7-box{stroke-width:2.6}
#sim-c7 .c7-cell.st .c7-num{font-weight:600}
#sim-c7 .c7-cell.c7-r0 .c7-box{stroke:var(--accent)}
#sim-c7 .c7-cell.c7-r1 .c7-box{stroke:var(--warm)}
#sim-c7 .c7-cell.c7-r2 .c7-box{stroke:var(--defn)}
#sim-c7 .c7-cell.c7-r3 .c7-box{stroke:var(--sim-v)}
#sim-c7 .c7-cell.sel .c7-box{fill:var(--accent);stroke:var(--accent)}
#sim-c7 .c7-cell.sel .c7-num{fill:var(--bg);font-weight:600}
#sim-c7 .c7-arr{pointer-events:none}
#sim-c7 .c7-ln{fill:none;stroke-width:1.7;stroke-linecap:round}
#sim-c7 .c7-lab{font-family:var(--sans);font-variant-numeric:tabular-nums;paint-order:stroke;stroke:var(--bg);stroke-width:3.5px;stroke-linejoin:round}
#sim-c7 .c7-r0 .c7-ln{stroke:var(--accent)}#sim-c7 .c7-r0 .c7-hd,#sim-c7 .c7-r0 .c7-lab{fill:var(--accent)}
#sim-c7 .c7-r1 .c7-ln{stroke:var(--warm)}#sim-c7 .c7-r1 .c7-hd,#sim-c7 .c7-r1 .c7-lab{fill:var(--warm)}
#sim-c7 .c7-r2 .c7-ln{stroke:var(--defn)}#sim-c7 .c7-r2 .c7-hd,#sim-c7 .c7-r2 .c7-lab{fill:var(--defn)}
#sim-c7 .c7-r3 .c7-ln{stroke:var(--sim-v)}#sim-c7 .c7-r3 .c7-hd,#sim-c7 .c7-r3 .c7-lab{fill:var(--sim-v)}
#sim-c7 .sim-out{line-height:1.5}
#sim-c7 .c7-blk{display:inline-flex;flex-direction:column;align-items:center;max-width:100%}
#sim-c7 .c7-four{align-items:flex-start}
#sim-c7 .c7-four .c7-line{justify-content:flex-start}
#sim-c7 .c7-line{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:.05em .3em;margin:.15em 0;font-variant-numeric:tabular-nums}
#sim-c7 .c7-pr{color:var(--muted);font-size:15px}
#sim-c7 .c7-v{font-weight:600}
#sim-c7 .c7-fr{display:inline-flex;flex-direction:column;align-items:center;font-size:.8em;line-height:1.1;vertical-align:middle}
#sim-c7 .c7-fr>span+span{border-top:1.3px solid currentColor;padding:0 .15em}
#sim-c7 .c7-s{display:inline-block;min-width:1.2em;font-weight:600}
#sim-c7 .c7-s0{color:var(--accent)}#sim-c7 .c7-s1{color:var(--warm)}#sim-c7 .c7-s2{color:var(--defn)}#sim-c7 .c7-s3{color:var(--sim-v)}
#sim-c7 .c7-dim{color:var(--muted)}</style><div class="sim-bar w-top c7-modes"><button type="button" class="c7-b on" data-d="0">строка, слева</button><button type="button" class="c7-b" data-d="1">строка, справа</button><button type="button" class="c7-b" data-d="2">диагональ, слева</button><button type="button" class="c7-b" data-d="3">диагональ, справа</button><button type="button" class="c7-b" data-d="4">все четыре</button></div>
<svg class="w-svg" viewBox="0 0 600 560" role="img" tabindex="0" aria-label="Интерактив: треугольник Паскаля из девяти строк, где выбранная клетка соединена с единицей на краю цепочкой стрелок с множителями."></svg>
<div class="sim-bar"><button type="button" class="c7-go">шагать от единицы</button></div>
<div class="sim-out" aria-live="polite"></div>
<div class="sim-cap">Нажмите на клетку: стрелки ведут к ней от единицы на краю.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c7");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".c7-b"),go=root.querySelector(".c7-go");
var NR=8,sn=6,sk=3,dir=0,W=600,G=null,run=null;
var SYM=["←","→","↖","↗"],NM=["строка, слева","строка, справа","диагональ, слева","диагональ, справа"];
/* маршрут от единицы на краю к клетке (n,k): стрелка {a:хвост,b:голова,p/q:множитель}; значение в голове = значение в хвосте · p/q */
function route(n,k,d){var r=[],j,m;
if(d===0){for(j=0;j<k;j++){r.push({a:[n,j],b:[n,j+1],p:n-j,q:j+1});}}
else if(d===1){for(j=n-1;j>=k;j--){r.push({a:[n,j+1],b:[n,j],p:j+1,q:n-j});}}
else if(d===2){for(m=n-k;m<n;m++){j=m-(n-k);r.push({a:[m,j],b:[m+1,j+1],p:m+1,q:j+1});}}
else{for(m=k;m<n;m++){r.push({a:[m,k],b:[m+1,k],p:m+1,q:m+1-k});}}
return r;}
function start(n,k,d){return d===0?[n,0]:(d===1?[n,n]:(d===2?[n-k,0]:[k,k]));}
/* геометрия: шаг по строке dx, высота клетки ch, полоса между строками bd */
function geo(){var dx=Math.min(48,(W-6)/9.2),s=dx/38,ch=23*s,bd=29*s,dy=ch+bd,top=8*s+ch/2;
return {dx:dx,s:s,cw:dx-6*s,ch:ch,bd:bd,dy:dy,top:top,fn:Math.max(13,13*s),fl:Math.max(12,Math.min(15,12*s)),H:top+NR*dy+ch/2+bd+2*s};}
function X(n,k){return W/2+(k-n/2)*G.dx;}
function Y(n){return G.top+n*G.dy;}
function build(){if(run){run.stop();run=null;}K.clear(svg);G=geo();
svg.setAttribute("viewBox","0 0 "+W+" "+G.H.toFixed(1));
var gc=K.el("g",{},svg);G.ga=K.el("g",{},svg);G.cells={};
var n,k;for(n=0;n<=NR;n++){for(k=0;k<=n;k++){(function(n,k){var x=X(n,k),y=Y(n),g=K.el("g",{"class":"c7-cell","data-n":n,"data-k":k},gc);
K.el("rect",{"class":"c7-box",x:(x-G.cw/2).toFixed(1),y:(y-G.ch/2).toFixed(1),width:G.cw.toFixed(1),height:G.ch.toFixed(1),rx:(7*G.s).toFixed(1)},g);
var t=K.el("text",{"class":"c7-num",x:x.toFixed(1),y:(y+G.fn*0.36).toFixed(1),"font-size":G.fn.toFixed(1)},g);t.textContent=String(K.C(n,k));
var h=K.el("rect",{"class":"c7-hit",x:(x-G.dx/2).toFixed(1),y:(y-G.dy/2).toFixed(1),width:G.dx.toFixed(1),height:G.dy.toFixed(1)},g);
h.addEventListener("click",function(){pick(n,k);});G.cells[n+","+k]=g;})(n,k);}}
draw();}
/* наконечник в точке E по направлению (ux,uy) */
function head(E,ux,uy,par){var L=7*G.s,w=3.6*G.s,bx=E[0]-ux*L,by=E[1]-uy*L;
K.el("polygon",{"class":"c7-hd",points:E[0].toFixed(1)+","+E[1].toFixed(1)+" "+(bx-uy*w).toFixed(1)+","+(by+ux*w).toFixed(1)+" "+(bx+uy*w).toFixed(1)+","+(by-ux*w).toFixed(1)},par);}
function lab(a){return "×"+a.p+(a.q===1?"":"/"+a.q);}
function arrow(a,ri,par){var g=K.el("g",{"class":"c7-arr c7-r"+ri,"data-a":a.a.join(","),"data-b":a.b.join(","),"data-p":a.p,"data-q":a.q},par);
var s=G.s,A=[X(a.a[0],a.a[1]),Y(a.a[0])],B=[X(a.b[0],a.b[1]),Y(a.b[0])],t,ux,uy,L;
if(a.a[0]===a.b[0]){
/* по строке: дуга под строкой, подпись под дугой */
var sg=B[0]>A[0]?1:-1,y0=A[1]+G.ch/2+2*s,P0=[A[0]+sg*0.2*G.dx,y0],P1=[B[0]-sg*0.2*G.dx,y0],mx=(A[0]+B[0])/2,Cq=[mx,y0+10*s];
K.el("path",{"class":"c7-ln",d:"M"+P0[0].toFixed(1)+","+P0[1].toFixed(1)+" Q"+Cq[0].toFixed(1)+","+Cq[1].toFixed(1)+" "+P1[0].toFixed(1)+","+P1[1].toFixed(1)},g);
ux=P1[0]-Cq[0];uy=P1[1]-Cq[1];L=Math.sqrt(ux*ux+uy*uy);head(P1,ux/L,uy/L,g);
t=K.el("text",{"class":"c7-lab",x:mx.toFixed(1),y:(y0+7*s+G.fl*0.8).toFixed(1),"text-anchor":"middle","font-size":G.fl.toFixed(1)},g);}
else{
/* по диагонали: отрезок между клетками, подпись снаружи от маршрута */
var vx=B[0]-A[0],vy=B[1]-A[1],f=(G.ch/2+3*s)/vy,Q0=[A[0]+vx*f,A[1]+vy*f],Q1=[B[0]-vx*f,B[1]-vy*f],side=vx>0?-1:1,M=[(A[0]+B[0])/2,(A[1]+B[1])/2];
K.el("line",{"class":"c7-ln",x1:Q0[0].toFixed(1),y1:Q0[1].toFixed(1),x2:Q1[0].toFixed(1),y2:Q1[1].toFixed(1)},g);
L=Math.sqrt(vx*vx+vy*vy);head(Q1,vx/L,vy/L,g);
t=K.el("text",{"class":"c7-lab",x:(M[0]+side*7*s).toFixed(1),y:(M[1]+G.fl*0.36).toFixed(1),"text-anchor":side<0?"end":"start","font-size":G.fl.toFixed(1)},g);}
t.textContent=lab(a);return g;}
function dirs(){return dir===4?[0,1,2,3]:[dir];}
function draw(){if(run){run.stop();run=null;}K.clear(G.ga);
var key;for(key in G.cells){G.cells[key].setAttribute("class","c7-cell");}
G.arr=[];dirs().forEach(function(d){var ri=dir===4?d:0,r=route(sn,sk,d);if(!r.length){return;}
var st=start(sn,sk,d);G.cells[st.join(",")].setAttribute("class","c7-cell on st c7-r"+ri);
r.forEach(function(a,i){var hc=i<r.length-1?G.cells[a.b.join(",")]:null;if(hc){hc.setAttribute("class","c7-cell on c7-r"+ri);}G.arr.push({g:arrow(a,ri,G.ga),i:i,hc:hc,cls:"c7-cell on c7-r"+ri});});});
G.cells[sn+","+sk].setAttribute("class","c7-cell sel");
go.disabled=!G.arr.length;say();}
function fr(p,q){return '<span class="c7-fr"><span>'+p+'</span><span>'+q+'</span></span>';}
function chain(r,v){return '<span class="c7-v">'+v+'</span><span>=</span><span>1</span>'+r.map(function(a){return '<span>·</span>'+fr(a.p,a.q);}).join("");}
function say(){var v=K.C(sn,sk),h="";
if(dir<4){var r=route(sn,sk,dir);
if(!r.length){h='<div class="c7-line" data-r="'+dir+'"><span class="c7-v">'+v+'</span><span class="c7-dim">— это сама единица на краю</span></div>';}
else{h='<div class="c7-line" data-r="'+dir+'">'+chain(r,v)+'</div><div class="c7-line c7-pr">'+v+" · ("+r.map(function(a){return a.q;}).join("·")+") = 1 · ("+r.map(function(a){return a.p;}).join("·")+")</div>";}}
else{if(sn===0){h='<div class="c7-line"><span class="c7-v">1</span><span class="c7-dim">— это сама единица на краю</span></div>';}
else{[0,1,2,3].forEach(function(d){var r=route(sn,sk,d),sy='<span class="c7-s c7-s'+d+'" title="'+NM[d]+'">'+SYM[d]+'</span>';
h+='<div class="c7-line" data-r="'+d+'">'+sy+(r.length?chain(r,v):'<span class="c7-v">'+v+'</span><span class="c7-dim">— сама единица</span>')+"</div>";});}}
out.innerHTML='<div class="c7-blk'+(dir===4&&sn>0?" c7-four":"")+'">'+h+"</div>";}
function pick(n,k){sn=n;sk=k;draw();}
function setDir(d){dir=d;bs.forEach(function(b){b.classList.toggle("on",+b.getAttribute("data-d")===dir);});draw();}
bs.forEach(function(b){b.addEventListener("click",function(){setDir(+b.getAttribute("data-d"));});});
/* «шагать»: стрелки проявляются по одной от единицы; при «меньше движения» K.anim сразу даёт последний кадр */
go.addEventListener("click",function(){draw();var L=0;G.arr.forEach(function(o){L=Math.max(L,o.i+1);});if(!L){return;}
G.arr.forEach(function(o){o.g.setAttribute("opacity","0");if(o.hc){o.hc.setAttribute("class","c7-cell");}});
/* клетка маршрута загорается, когда в неё пришла стрелка */
run=K.anim(650*L+200,function(t){G.arr.forEach(function(o){var a=o.i/L*0.92,v=K.seg(t,a,a+0.6/L);o.g.setAttribute("opacity",v.toFixed(3));if(o.hc){o.hc.setAttribute("class",v>0.6?o.cls:"c7-cell");}});},function(){run=null;});});
/* клавиатура: стрелки двигают выбранную клетку */
svg.addEventListener("keydown",function(e){var n=sn,k=sk;
if(e.key==="ArrowLeft"){k--;}else if(e.key==="ArrowRight"){k++;}else if(e.key==="ArrowUp"){n--;}else if(e.key==="ArrowDown"){n++;}else{return;}
e.preventDefault();n=K.cl(n,0,NR);k=K.cl(k,0,n);pick(n,k);});
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

Каждый шаг даёт новый множитель в числителе и новый в знаменателе: $\binom63=\frac{6\cdot5\cdot4}{1\cdot2\cdot3}$. В числителе стоит $6^{\underline 3}$, в знаменателе $3!$.

**Теорема 19 (формула). Статус: выверено, SKELET т. 11.**
Для любых целых $n\ge0$ и $0\le k\le n$ выполняются равенства
$$\begin{gathered}\binom nk=\frac{n^{\underline k}}{k!}=\frac{n(n-1)\cdots(n-k+1)}{k!},\\\binom nk=\frac{n!}{k!\,(n-k)!}.\end{gathered}$$
При $k=0$ произведение в числителе пусто и считается равным 1, и формула даёт $\binom n0=1$.

*Доказательство — ходьба вдоль строки от края.* Начнём с $\binom n0=1$ и применим утверждение 18 $k$ раз, как в примере выше:
$$\binom nk=\frac n1\cdot\frac{n-1}2\cdot\ldots\cdot\frac{n-k+1}k.$$
В числителе получилось $n(n-1)\cdots(n-k+1)$, в знаменателе $k!$. Чтобы получить вторую запись, домножим числитель и знаменатель на $(n-k)!$: в числителе получится $n(n-1)\cdots(n-k+1)\cdot(n-k)!=n!$.

Шагать можно и по диагонали, как во втором равенстве утверждения 12. Первая и третья части равенства утверждения 17, записанные для команды из $k$ человек, дают $k\binom nk=n\binom{n-1}{k-1}$ при $1\le k\le n$. За $k$ шагов вверх по диагонали, до края $\binom{n-k}0=1$, получается та же формула; в виджете выше это путь «диагональ, слева».

Теперь можно найти число Варахамихиры: $\binom{16}4=\frac{16\cdot15\cdot14\cdot13}{1\cdot2\cdot3\cdot4}=1820$. А футбольную команду с капитаном из задачи 16 можно выбрать $11\binom{25}{11}=11\cdot4\,457\,400=49\,031\,400$ способами; проверьте по формуле, что два других ответа задачи дают то же число.

## Формула двойным подсчётом

Формулу можно получить и сразу, без ходьбы по треугольнику, — тем же двойным подсчётом, что и число пар. Ходьба при этом не была лишней: она показала, как связаны соседние числа строки, и именно так рассуждал сам Паскаль.

**Задача 20 (тройки из восьми). Статус: пишем с нуля.**
Сколькими способами можно выбрать троих из восьми человек?

Ответ мы знаем, это 56; получим его ещё раз. Капитана, заместителя и третьего игрока мы выбирали в задаче 13: это $8^{\underline 3}=8\cdot7\cdot6$ способов. Посчитаем их иначе: сначала выберем тройку ($\binom83$ способами), потом в ней капитана (3 способами), потом заместителя из двух оставшихся (2 способами); третий определится сам. Это одно и то же количество, поэтому
$$\binom83\cdot3\cdot2=8\cdot7\cdot6,$$
то есть $6\binom83=336$ и $\binom83=56$, как и в примере с дежурными.

В общем случае размещение из $n$ по $k$ можно получить так: сначала выбрать множество из $k$ человек — $\binom nk$ способами, а потом расставить его по порядку — $k!$ способами. Каждое размещение получается ровно один раз: множество — это те, кто в нём выписан. Приравниваем:
$$\binom nk\cdot k!=n^{\underline k}.$$
Остаётся перенести $k!$ в другую часть, и получится теорема 19. До этого последнего шага мы только умножали. Число пар получается при $k=2$: $\binom n2\cdot2=n(n-1)$.

Тот же ответ даёт задача, в условии которой числа 3 нет вовсе.

**Задача 21 (восемь по порядку). Статус: пишем с нуля.**
Сколькими способами можно расставить восемь человек по порядку?

Ответ — $8!=40\,320$. Посчитаем иначе. Сначала выберем, кто займёт первые три места, — $\binom83$ способами; потом расставим этих троих на первых трёх местах — $3!$ способами; потом остальных пятерых на оставшихся пяти местах — $5!$ способами. Каждая расстановка получается ровно один раз: тройка — это те, кто стоит на первых трёх местах. Поэтому
$$8!=\binom83\cdot3!\cdot5!,$$
то есть $40\,320=720\binom83$ и $\binom83=56$.

Тем же рассуждением для любых $0\le k\le n$ получается $n!=\binom nk\cdot k!\cdot(n-k)!$, вторая запись теоремы 19. Это рассуждение трудно придумать, не зная ответа: в задаче о расстановке восьми человек числа 3 нет, мы ввели его сами. Зато в равенстве $k$ и $n-k$ стоят на равных, и симметрия $\binom nk=\binom n{n-k}$ (утверждение 7) видна сразу.

Места можно разбивать не на две группы, а на несколько. Расставим девятерых по порядку и разобьём девять мест на группы из двух, трёх и четырёх мест подряд. Сначала решим, кто в какую группу попадёт, потом расставим людей внутри групп, $2!\cdot3!\cdot4!$ способами. Значит, число способов разбить людей на группы, умноженное на $2!\cdot3!\cdot4!$, равно $9!$. Само число способов разбить людей на группы равно 1260. Такие числа называют мультиномиальными коэффициентами, и мы, возможно, к ним ещё вернёмся.

## Правило Паскаля и формула с факториалами

У нас есть две формулы для одних и тех же чисел: правило Паскаля, которое вместе с единицами по краям вычисляет строку по предыдущей, и формула теоремы 19 с факториалами. Сначала проверим на примере, что они согласованы. По формуле $\binom52=\frac{5!}{2!\,3!}=10$, $\binom53=\frac{5!}{3!\,2!}=10$ и $\binom63=\frac{6!}{3!\,3!}=20$, и правило Паскаля выполняется: $20=10+10$.

**Утверждение 22 (формула и правило Паскаля). Статус: пишем с нуля.**
Формула теоремы 19 подчиняется правилу Паскаля (утверждение 9): для любых целых $n\ge2$ и $1\le k\le n-1$ выполняется равенство
$$\frac{(n-1)!}{(k-1)!\,(n-k)!}+\frac{(n-1)!}{k!\,(n-k-1)!}=\frac{n!}{k!\,(n-k)!}.$$

*Доказательство — общий знаменатель.* Так как $k!=k\cdot(k-1)!$ и $(n-k)!=(n-k)\cdot(n-k-1)!$, домножим числитель и знаменатель первой дроби на $k$, а второй — на $n-k$. У обеих дробей станет знаменатель $k!\,(n-k)!$, а в числителях — $(n-1)!\cdot k$ и $(n-1)!\cdot(n-k)$. Вместе в числителе получается $(n-1)!\cdot(k+n-k)=(n-1)!\cdot n=n!$.

Значит, теорему 19 можно доказать и по-другому. Треугольник однозначно задаётся единицами по краям и правилом Паскаля: каждая строка вычисляется по предыдущей. Формула даёт единицы по краям, $\frac{n!}{0!\,n!}=1$, и по утверждению 22 подчиняется тому же правилу. В строке 0 формула верна; если она верна в какой-то строке, то по правилу Паскаля верна и в следующей; значит, она верна во всех строках. Такое рассуждение называется доказательством по индукции.

И наоборот: зная формулу, правило Паскаля можно проверить вычислением, не раскладывая слова по кучкам. Подсчёт и вычисление — два взгляда на один и тот же факт.

## Сумма строки

**Задача 23 (все смеси). Статус: пишем с нуля.**
Сколько всего смесей можно составить из шести вкусов, если брать любое число вкусов, но хотя бы один?

Числа смесей из одного, двух, …, шести вкусов составляют всю шестую строку, кроме первого числа: единица в начале строки отвечает пустой смеси. Сложим:
$$6+15+20+15+6+1=63.$$
Столько их и насчитано у Чараки. Вместе с пустой смесью получается 64.

Сложим так же числа в первых строках треугольника. Получится 1, 2, 4, 8, 16, 32, 64: каждая сумма вдвое больше предыдущей.

<div class="sim" id="sim-c8"><style>#sim-c8 svg:focus{outline:none}
#sim-c8 svg:focus-visible{outline:2px solid var(--accent);outline-offset:4px;border-radius:10px}
#sim-c8 .c8-box{fill:var(--panel);stroke:var(--rule);stroke-width:1.2;transition:stroke .15s,opacity .15s}
#sim-c8 .c8-num{font-family:var(--sans);fill:var(--text);text-anchor:middle;font-variant-numeric:tabular-nums;pointer-events:none;transition:opacity .15s}
#sim-c8 .c8-sum{font-family:var(--sans);fill:var(--muted);font-variant-numeric:tabular-nums;pointer-events:none;transition:opacity .15s}
#sim-c8 .c8-lead{stroke:var(--rule);stroke-width:1.2;stroke-dasharray:1.5 4;stroke-linecap:round;pointer-events:none}
#sim-c8 .c8-hit{fill:transparent;cursor:pointer}
#sim-c8 .c8-row:hover .c8-box{stroke:var(--accent)}
#sim-c8 .c8-row.dim .c8-box,#sim-c8 .c8-row.dim .c8-num{opacity:.55}
#sim-c8 .c8-row.on .c8-box{stroke:var(--text);stroke-width:1.6}
#sim-c8 .c8-row.on .c8-num{font-weight:600}
#sim-c8 .c8-row.on .c8-sum{fill:var(--text);font-weight:600}
#sim-c8 .c8-arr{pointer-events:none}
#sim-c8 .c8-ln{fill:none;stroke-width:1.7;stroke-linecap:round}
#sim-c8 .c8-L .c8-ln{stroke:var(--accent)}#sim-c8 .c8-L .c8-hd{fill:var(--accent)}
#sim-c8 .c8-R .c8-ln{stroke:var(--warm)}#sim-c8 .c8-R .c8-hd{fill:var(--warm)}
#sim-c8 .sim-out{line-height:1.5}
#sim-c8 .c8-line{margin:.15em 0;font-variant-numeric:tabular-nums}
#sim-c8 .c8-line>span{display:inline-block;max-width:100%;text-wrap:balance}
#sim-c8 .c8-pr{color:var(--muted)}
#sim-c8 .c8-f{color:var(--text);display:inline-block;max-width:100%}
@media (max-width:480px){#sim-c8 .sim-out{font-size:15px}}</style><svg class="w-svg" viewBox="0 0 600 420" role="img" tabindex="0" aria-label="Интерактив: треугольник Паскаля из восьми строк с суммами справа, где каждое число выбранной строки двумя стрелками уходит в два числа следующей строки."></svg>
<div class="sim-bar"><button type="button" class="c8-pw" aria-pressed="false">степени двойки</button><button type="button" class="c8-go">шагать</button></div>
<div class="sim-out" aria-live="polite"></div>
<div class="sim-cap">Справа — суммы строк; нажмите на строку, и стрелки покажут, почему следующая сумма вдвое больше.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c8");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),pw=root.querySelector(".c8-pw"),go=root.querySelector(".c8-go");
var NR=7,sn=4,pow=false,W=600,G=null,run=null,NB=" ";
var SUP=["⁰","¹","²","³","⁴","⁵","⁶","⁷"];
/* геометрия как в c7: шаг по строке dx, высота клетки ch, полоса между строками bd; справа колонка сумм шириной sw */
function geo(){var fs=W<480?14:15,sw=fs*5.6,gap=W<480?10:18,dx=Math.min(48,(W-10-gap-sw)/8),s=dx/38,ch=23*s,bd=31*s,dy=ch+bd,top=6*s+ch/2,tw=8*dx+gap+sw,x0=(W-tw)/2;
return {dx:dx,s:s,cw:dx-6*s,ch:ch,bd:bd,dy:dy,top:top,fs:fs,fn:Math.max(13,13*s),tc:x0+4*dx,sx:x0+8*dx+gap,H:top+NR*dy+ch/2+6*s};}
function X(n,k){return G.tc+(k-n/2)*G.dx;}
function Y(n){return G.top+n*G.dy;}
function row(n){var r=[],k;for(k=0;k<=n;k++){r.push(K.C(n,k));}return r;}
function build(){if(run){run.stop();run=null;}K.clear(svg);G=geo();
svg.setAttribute("viewBox","0 0 "+W+" "+G.H.toFixed(1));
var gr=K.el("g",{},svg);G.ga=K.el("g",{},svg);G.rows=[];G.sums=[];
var n,k;for(n=0;n<=NR;n++){(function(n){var y=Y(n),g=K.el("g",{"class":"c8-row c8-r"+n,"data-n":n},gr);
for(k=0;k<=n;k++){var x=X(n,k),c=K.el("g",{"class":"c8-cell","data-n":n,"data-k":k},g);
K.el("rect",{"class":"c8-box",x:(x-G.cw/2).toFixed(1),y:(y-G.ch/2).toFixed(1),width:G.cw.toFixed(1),height:G.ch.toFixed(1),rx:(7*G.s).toFixed(1)},c);
var t=K.el("text",{"class":"c8-num",x:x.toFixed(1),y:(y+G.fn*0.36).toFixed(1),"font-size":G.fn.toFixed(1)},c);t.textContent=String(K.C(n,k));}
/* пунктир от строки к её сумме */
var xe=X(n,n)+G.cw/2+5*G.s,xs=G.sx-5;if(xs-xe>6){K.el("line",{"class":"c8-lead",x1:xe.toFixed(1),y1:y.toFixed(1),x2:xs.toFixed(1),y2:y.toFixed(1)},g);}
var sm=K.el("text",{"class":"c8-sum","data-n":n,x:G.sx.toFixed(1),y:(y+G.fs*0.36).toFixed(1),"font-size":G.fs},g);G.sums.push(sm);
/* зона нажатия — вся полоса строки, вместе с суммой */
var h=K.el("rect",{"class":"c8-hit",x:0,y:(y-G.dy/2).toFixed(1),width:W,height:G.dy.toFixed(1)},g);
h.addEventListener("click",function(){pick(Math.min(n,NR-1));});G.rows.push(g);})(n);}
sums();draw();}
function sums(){G.sums.forEach(function(t,n){K.clear(t);var v=Math.pow(2,n);t.textContent="= "+v+(pow?" = 2"+SUP[n]:"");t.setAttribute("data-p",pow?n:"");});}
/* наконечник в точке E по направлению (ux,uy) */
function head(E,ux,uy,par){var L=6.5*G.s,w=3.4*G.s,bx=E[0]-ux*L,by=E[1]-uy*L;
K.el("polygon",{"class":"c8-hd",points:E[0].toFixed(1)+","+E[1].toFixed(1)+" "+(bx-uy*w).toFixed(1)+","+(by+ux*w).toFixed(1)+" "+(bx+uy*w).toFixed(1)+","+(by-ux*w).toFixed(1)},par);}
/* стрелка из клетки (n,k) вниз: d=-1 — в (n+1,k) левее, d=1 — в (n+1,k+1) правее; выходит из своей половины клетки, входит в ближнюю половину цели */
function arrow(n,k,d){var kb=d<0?k:k+1,g=K.el("g",{"class":"c8-arr "+(d<0?"c8-L":"c8-R"),"data-a":n+","+k,"data-b":(n+1)+","+kb},G.ga);
var s=G.s,P=[X(n,k)+d*0.1*G.cw,Y(n)+G.ch/2+2.5*s],Q=[X(n+1,kb)-d*0.24*G.cw,Y(n+1)-G.ch/2-2.5*s],vx=Q[0]-P[0],vy=Q[1]-P[1],L=Math.sqrt(vx*vx+vy*vy);
K.el("line",{"class":"c8-ln",x1:P[0].toFixed(1),y1:P[1].toFixed(1),x2:(Q[0]-vx/L*4*s).toFixed(1),y2:(Q[1]-vy/L*4*s).toFixed(1)},g);
head(Q,vx/L,vy/L,g);return g;}
function draw(){if(run){run.stop();run=null;}K.clear(G.ga);
G.rows.forEach(function(g,n){g.setAttribute("class","c8-row c8-r"+n+(n===sn||n===sn+1?" on":" dim"));});
G.arr=[];var k;for(k=0;k<=sn;k++){G.arr.push({g:arrow(sn,k,-1),k:k,d:-1});G.arr.push({g:arrow(sn,k,1),k:k,d:1});}
say();}
function plus(a){var n=a.length;return n<2?String(a[0]):a.slice(0,n-1).join(NB+"+ ")+NB+"+"+NB+a[n-1];}
function say(){var a=row(sn),b=row(sn+1),S=Math.pow(2,sn);
var h='<div class="c8-line c8-l1"><span class="c8-pr">строка '+sn+':</span> <span class="c8-f">'+(a.length>1?plus(a)+NB+"= ":"")+"<b>"+S+"</b></span></div>";
h+='<div class="c8-line c8-l2"><span class="c8-pr">каждое число строки'+NB+sn+" вошло в"+NB+"строку"+NB+(sn+1)+NB+'дважды:</span> <span class="c8-f">2'+NB+"·"+NB+S+NB+"= <b>"+2*S+"</b>"+NB+"= "+plus(b)+"</span></div>";
out.innerHTML=h;}
function pick(n){sn=n;draw();}
pw.addEventListener("click",function(){pow=!pow;pw.classList.toggle("on",pow);pw.setAttribute("aria-pressed",pow?"true":"false");sums();});
/* «шагать»: выделение спускается на строку; сначала проявляются синие стрелки (первая копия строки), потом рыжие (вторая) */
go.addEventListener("click",function(){pick(sn<NR-1?sn+1:0);var m=sn+1;
G.arr.forEach(function(o){o.g.setAttribute("opacity","0");});
run=K.anim(1300,function(t){G.arr.forEach(function(o){var a=(o.d<0?0:0.5)+0.4*o.k/m;o.g.setAttribute("opacity",K.seg(t,a,a+0.45/m+0.08).toFixed(3));});},function(){G.arr.forEach(function(o){o.g.removeAttribute("opacity");});run=null;});});
/* клавиатура: стрелки вверх-вниз двигают выбранную строку */
svg.addEventListener("keydown",function(e){var n=sn;if(e.key==="ArrowUp"){n--;}else if(e.key==="ArrowDown"){n++;}else{return;}e.preventDefault();pick(K.cl(n,0,NR-1));});
K.onWidth(root,function(w){W=w;build();});
})();</script></div>

Похоже, что сумма строки $n$ равна $2^n$. Объясним это подсчётом.

**Утверждение 24 (сумма строки). Статус: выверено, SKELET утв. 12.**
Для любого целого $n\ge0$ выполняется равенство
$$\binom n0+\binom n1+\dots+\binom nn=2^n.$$

*Доказательство — посчитать все слова.* Слагаемое $\binom nk$ — число слов длины $n$ с $k$ единицами (утверждение 2), поэтому сумма — число всех слов длины $n$. Слово похоже на ряд из $n$ лампочек: 1 — горит, 0 — не горит. Каждую лампочку можно зажечь или не зажечь, и по правилу произведения слов $2\cdot2\cdot\ldots\cdot2=2^n$.

То же видно и по двоичной записи. Слова длины 6, от 000000 до 111111, — это двоичные записи чисел от 0 до $32+16+8+4+2+1=63$, каждого ровно один раз. Чисел от 0 до 63 ровно 64. Пустой смеси отвечает 0, поэтому настоящих смесей 63 — по одной на каждое число от 1 до 63.

Удвоение, которое мы заметили в начале, видно и из правила Паскаля. Каждое число строки входит слагаемым ровно в два числа следующей строки — в то, что под ним слева, и в то, что под ним справа; крайние единицы следующей строки получают по одному такому вкладу. Поэтому в следующей строке каждое число предыдущей посчитано дважды: для строки 4 это $2\cdot16=32=1+5+10+10+5+1$. На языке слов это то же разложение по первой цифре, что в доказательстве правила Паскаля: слово длины $n+1$ — это слово длины $n$, перед которым приписан 0 или 1. Первая лампочка либо горит, либо нет.

## Ответ

Вот и ответы на вопросы из начала: из шести вкусов можно составить 20 смесей по три и 63 смеси всего, а 1820 смесей Варахамихиры получаются одной строчкой вычислений.

Ходьба вдоль строки, которая привела нас к формуле, — не наше изобретение. В 1654 году Блез Паскаль написал и отпечатал «Трактат об арифметическом треугольнике»; в свет он вышел посмертно, в 1665 году. Таблица у Паскаля повёрнута: его «основания» — это диагонали таблицы, и основание номер $m$ совпадает с нашей строкой $m-1$.

Двенадцатое следствие трактата утверждает: две соседние клетки одного основания относятся как число клеток от верхней до верха основания к числу клеток от нижней до низа, включительно. В наших обозначениях это утверждение 18; например, в строке 6 соседние числа 15 и 20 относятся как $3:4$. Доказывает его Паскаль по-другому: соотношение верно во втором основании, то есть в нашей строке из двух единиц, а если верно в каком-то основании, то верно и в следующем. Так устроено доказательство по индукции: проверить первый случай и показать, что из каждого случая следует следующий. Это одно из первых явных доказательств такого рода.

Седьмое следствие трактата совпадает с нашим наблюдением о суммах: сумма клеток каждого основания вдвое больше суммы предыдущего. В конце, после следствий, Паскаль ставит задачу — найти число в клетке, не строя треугольника, — и решает её так же, как мы: перемножает $3\cdot4\cdot5\cdot6$, делит на $1\cdot2\cdot3\cdot4$ и получает 15. У нас это $\binom64$ — соседка вопросительного знака в шестой строке.

В следующий раз биномиальные коэффициенты помогут понять, куда может уйти точка, которая шагает наугад влево и вправо.
