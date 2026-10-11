---
tab: Умный перебор
status: chernovik
poryadok: 1
registr: читаемый
nomera: da
zhanr: statya
---

# Умный перебор

Урок — разбор домашнего задания. К каждому подсчёту у скептика два вопроса: нет ли **пропуска** (какой-то объект потеряли) и нет ли **повтора** (какой-то объект посчитали дважды).

## Правило разности

**Задача 1 (далматинцы · ДЗ, №3). Статус: выверено, dz_29-09_dannye.py.**
Из 101 далматинца у 29 пятно только на левом ухе, у 17 — только на правом ухе, а у 22 далматинцев нет пятен на ушах. Сколько далматинцев имеют пятно на правом ухе?

- Первый ответ — 17. Пропуск: пятно на правом ухе есть и у тех, у кого пятна на обоих ушах.
- Нужных далматинцев напрямую не сосчитать. Зато ненужные известны: без пятен (22) и только с левым (29).
- Ответ: $101-22-29=50$.

<figure>
<!-- static: раскладка одного подсчёта, двигать нечего -->
<svg viewBox="0 0 640 126" role="img" aria-label="Полоса из 101 далматинца разрезана на четыре куска: без пятен 22, только левое ухо 29, только правое 17, оба уха неизвестно; пятно на правом ухе у 101 минус 22 минус 29"><style>.up-t{font-family:var(--sans,system-ui,sans-serif);fill:var(--text,#222)}.up-m{font-family:var(--sans,system-ui,sans-serif);fill:var(--muted,#666)}.up-c{fill:var(--panel,#fff);stroke:var(--rule,#c9c9c9);stroke-width:1}.up-a{fill:var(--accent,#2f6f8f);fill-opacity:.2;stroke:var(--accent,#2f6f8f);stroke-width:1}.up-w{fill:var(--warm,#b5651d);fill-opacity:.2;stroke:var(--warm,#b5651d);stroke-width:1}.up-s{fill:var(--muted,#888);fill-opacity:.16;stroke:var(--rule,#c9c9c9);stroke-width:1}.up-x{fill:none;stroke:var(--text,#222);stroke-width:2.2}.up-l{fill:none;stroke:var(--muted,#666);stroke-width:1.2}.up-al{fill:none;stroke:var(--accent,#2f6f8f);stroke-width:1.4}</style><rect class="up-s" x="20.0" y="46" width="130.7" height="34"/><text class="up-m" x="85.3" y="24.0" font-size="12" text-anchor="middle" font-weight="400">без пятен на ушах</text><text class="up-t" x="85.3" y="39.0" font-size="13" text-anchor="middle" font-weight="600">22</text><rect class="up-s" x="150.7" y="46" width="172.3" height="34"/><text class="up-m" x="236.8" y="24.0" font-size="12" text-anchor="middle" font-weight="400">только левое</text><text class="up-t" x="236.8" y="39.0" font-size="13" text-anchor="middle" font-weight="600">29</text><rect class="up-a" x="323.0" y="46" width="101.0" height="34"/><text class="up-m" x="373.5" y="24.0" font-size="12" text-anchor="middle" font-weight="400">только правое</text><text class="up-t" x="373.5" y="39.0" font-size="13" text-anchor="middle" font-weight="600">17</text><rect class="up-a" x="424.0" y="46" width="196.0" height="34"/><text class="up-m" x="522.0" y="24.0" font-size="12" text-anchor="middle" font-weight="400">оба уха</text><text class="up-t" x="522.0" y="39.0" font-size="13" text-anchor="middle" font-weight="600">?</text><path class="up-al" d="M323.0,90 v8 H620.0 v-8"/><text class="up-t" x="471.5" y="116.0" font-size="13" text-anchor="middle" font-weight="600">пятно на правом ухе: 101 − 22 − 29 = 50</text><path class="up-l" d="M20.0,90 v8 H323.0 v-8"/><text class="up-m" x="171.5" y="116.0" font-size="12" text-anchor="middle" font-weight="400">ненужные: 22 + 29</text></svg>
<figcaption>Все 101 далматинец одной полосой: нужный кусок — всё минус ненужные</figcaption>
</figure>

**Утверждение 2 (правило суммы). Статус: пишем с нуля.**
Если каждый объект попал ровно в один кусок, то всего объектов столько, сколько во всех кусках вместе.

- Ровно в один — значит хотя бы в один (нет пропусков) и не больше чем в один (нет повторов).

**Утверждение 3 (правило разности). Статус: пишем с нуля.**
Если все объекты делятся на нужные и остальные, то нужных столько, сколько всего, минус число остальных.

*Доказательство — утверждение 2 для двух кусков:* всего = нужные + остальные.

**Задача 4 (лестница · ДЗ, №1). Статус: выверено, dz_29-09_dannye.py.**
Человек поднимается с первого этажа на пятый за минуту. Сколько ему понадобится времени, чтобы с той же скоростью подняться с первого на десятый этаж?

- Если бы человек шёл из подвала, на $k$-й этаж ему нужно было бы $k$ пролётов: на первый — один, на десятый — десять.
- Он идёт с первого этажа, и пролёт «из подвала на первый» вычёркиваем. С 1-го на 5-й — $5-1=4$ пролёта, по 15 секунд.
- С 1-го на 10-й — $10-1=9$ пролётов, 135 секунд, то есть 2 минуты 15 секунд.

<figure>
<!-- static: раскладка одного подсчёта, двигать нечего -->
<svg viewBox="0 0 364 110" role="img" aria-label="Десять клеток — подъёмы из подвала на этажи с первого по десятый; первая клетка зачёркнута, остаётся девять"><style>.up-t{font-family:var(--sans,system-ui,sans-serif);fill:var(--text,#222)}.up-m{font-family:var(--sans,system-ui,sans-serif);fill:var(--muted,#666)}.up-c{fill:var(--panel,#fff);stroke:var(--rule,#c9c9c9);stroke-width:1}.up-a{fill:var(--accent,#2f6f8f);fill-opacity:.2;stroke:var(--accent,#2f6f8f);stroke-width:1}.up-w{fill:var(--warm,#b5651d);fill-opacity:.2;stroke:var(--warm,#b5651d);stroke-width:1}.up-s{fill:var(--muted,#888);fill-opacity:.16;stroke:var(--rule,#c9c9c9);stroke-width:1}.up-x{fill:none;stroke:var(--text,#222);stroke-width:2.2}.up-l{fill:none;stroke:var(--muted,#666);stroke-width:1.2}.up-al{fill:none;stroke:var(--accent,#2f6f8f);stroke-width:1.4}</style><rect class="up-s" x="12" y="40" width="34" height="30"/><text class="up-t" x="29.0" y="60.0" font-size="12" text-anchor="middle" font-weight="400">1</text><path class="up-x" d="M16,66 L42,44"/><rect class="up-a" x="46" y="40" width="34" height="30"/><text class="up-t" x="63.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">2</text><rect class="up-a" x="80" y="40" width="34" height="30"/><text class="up-t" x="97.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">3</text><rect class="up-a" x="114" y="40" width="34" height="30"/><text class="up-t" x="131.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">4</text><rect class="up-a" x="148" y="40" width="34" height="30"/><text class="up-t" x="165.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">5</text><rect class="up-a" x="182" y="40" width="34" height="30"/><text class="up-t" x="199.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">6</text><rect class="up-a" x="216" y="40" width="34" height="30"/><text class="up-t" x="233.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">7</text><rect class="up-a" x="250" y="40" width="34" height="30"/><text class="up-t" x="267.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">8</text><rect class="up-a" x="284" y="40" width="34" height="30"/><text class="up-t" x="301.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">9</text><rect class="up-a" x="318" y="40" width="34" height="30"/><text class="up-t" x="335.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">10</text><path class="up-al" d="M46,34 v-8 H352 v8"/><text class="up-t" x="199.0" y="20.0" font-size="13" text-anchor="middle" font-weight="600">с 1-го на 10-й: 10 − 1 = 9 пролётов</text><path class="up-l" d="M12,76 v8 H46 v-8"/><text class="up-m" x="69.0" y="100.0" font-size="12" text-anchor="middle" font-weight="400">из подвала на 1-й</text></svg>
<figcaption>Подъёмы из подвала на этажи 1…10; первый зачёркнут</figcaption>
</figure>

## Два списка

**Задача 5 (9 или 15 · ДЗ, №5). Статус: выверено, dz_29-09_dannye.py.**
Сколько существует трёхзначных чисел, делящихся хотя бы на одно из чисел 9 и 15?

Сначала маленькая модель: числа от 1 до 90.

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

<div class="sim" id="sim-c1"><style>#sim-c1 .c1-grid{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:3px;max-width:560px;margin:0 auto;font-family:var(--sans);font-variant-numeric:tabular-nums}
#sim-c1 .c1-c{position:relative;text-align:center;font-size:15px;padding:5px 0;border:1px solid var(--rule);border-radius:4px;background:var(--panel);color:var(--text);transition:background .3s,border-color .3s}
#sim-c1 .c1-c.a{background:var(--warm-soft);border-color:var(--warm)}
#sim-c1 .c1-c.b{background:var(--accent-soft);border-color:var(--accent)}
#sim-c1 .c1-c.ab{background:linear-gradient(135deg,var(--warm-soft) 50%,var(--accent-soft) 50%);border:2px solid var(--text);font-weight:600}
@media (max-width:480px){#sim-c1 .c1-c{font-size:12px;padding:3px 0}}</style><div class="sim-bar w-top"><button type="button" class="c1-b" data-m="a">кратные 9</button><button type="button" class="c1-b" data-m="b">кратные 15</button><button type="button" class="c1-b" data-m="ab">оба списка</button></div>
<div class="c1-grid" role="img" aria-label="Интерактив: числа от 1 до 90 таблицей по десять; кнопки отмечают кратные 9, кратные 15 и оба списка сразу, общие числа 45 и 90 попадают в оба"></div>
<div class="sim-out"></div>
<div class="sim-cap">Числа от 1 до 90 — маленькая модель задачи: те же два списка, общие объекты — кратные 45.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c1");if(!root||!K){return;}
var grid=root.querySelector(".c1-grid"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".c1-b"),cells={},m="";
for(var n=1;n<=90;n++){var c=document.createElement("div");c.className="c1-c";c.textContent=n;grid.appendChild(c);cells[n]=c;}
function show(mm){m=(m===mm)?"":mm;
for(var n=1;n<=90;n++){var c=cells[n],a=n%9===0,b=n%15===0;c.className="c1-c";
if(m==="a"&&a){c.classList.add("a");}if(m==="b"&&b){c.classList.add("b");}
if(m==="ab"&&(a||b)){c.classList.add(a&&b?"ab":(a?"a":"b"));}}
for(var i=0;i<bs.length;i++){bs[i].classList.toggle("on",bs[i].getAttribute("data-m")===m);}
out.innerHTML={"":"Нажмите на список.","a":"Кратные 9: 9, 18, …, 90 — <b>10</b> чисел.","b":"Кратные 15: 15, 30, …, 90 — <b>6</b> чисел.","ab":"10 + 6 = 16? Числа 45 и 90 стоят в обоих списках — повторы. Всего <b>10 + 6 − 2 = 14</b>."}[m];}
for(var i=0;i<bs.length;i++){bs[i].addEventListener("click",function(){show(this.getAttribute("data-m"));});}
show("");
})();</script></div>

- В модели кратных 9 — десять, кратных 15 — шесть, а числа 45 и 90 стоят в обоих списках. Это повторы: $10+6-2=14$.
- Теперь трёхзначные. Кратные 9 — это $9\cdot k$ при $k$ от 12 до 111. Сколько номеров от 12 до 111? Вычёркиваем 11 номеров перед первым: $111-11=100$.

<figure>
<!-- static: раскладка одного подсчёта, двигать нечего -->
<svg viewBox="0 0 364 110" role="img" aria-label="Номера k от 1 до 111 для чисел 9·k; номера с 1 по 11 зачёркнуты, остаётся 111 минус 11, то есть 100"><style>.up-t{font-family:var(--sans,system-ui,sans-serif);fill:var(--text,#222)}.up-m{font-family:var(--sans,system-ui,sans-serif);fill:var(--muted,#666)}.up-c{fill:var(--panel,#fff);stroke:var(--rule,#c9c9c9);stroke-width:1}.up-a{fill:var(--accent,#2f6f8f);fill-opacity:.2;stroke:var(--accent,#2f6f8f);stroke-width:1}.up-w{fill:var(--warm,#b5651d);fill-opacity:.2;stroke:var(--warm,#b5651d);stroke-width:1}.up-s{fill:var(--muted,#888);fill-opacity:.16;stroke:var(--rule,#c9c9c9);stroke-width:1}.up-x{fill:none;stroke:var(--text,#222);stroke-width:2.2}.up-l{fill:none;stroke:var(--muted,#666);stroke-width:1.2}.up-al{fill:none;stroke:var(--accent,#2f6f8f);stroke-width:1.4}</style><rect class="up-s" x="12" y="40" width="34" height="30"/><text class="up-t" x="29.0" y="60.0" font-size="12" text-anchor="middle" font-weight="400">1</text><path class="up-x" d="M16,66 L42,44"/><rect class="up-s" x="46" y="40" width="34" height="30"/><text class="up-t" x="63.0" y="60.0" font-size="12" text-anchor="middle" font-weight="400">2</text><path class="up-x" d="M50,66 L76,44"/><text class="up-m" x="97.0" y="60.0" font-size="14" text-anchor="middle" font-weight="400">…</text><rect class="up-s" x="114" y="40" width="34" height="30"/><text class="up-t" x="131.0" y="60.0" font-size="12" text-anchor="middle" font-weight="400">10</text><path class="up-x" d="M118,66 L144,44"/><rect class="up-s" x="148" y="40" width="34" height="30"/><text class="up-t" x="165.0" y="60.0" font-size="12" text-anchor="middle" font-weight="400">11</text><path class="up-x" d="M152,66 L178,44"/><rect class="up-a" x="182" y="40" width="34" height="30"/><text class="up-t" x="199.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">12</text><rect class="up-a" x="216" y="40" width="34" height="30"/><text class="up-t" x="233.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">13</text><text class="up-m" x="267.0" y="60.0" font-size="14" text-anchor="middle" font-weight="400">…</text><rect class="up-a" x="284" y="40" width="34" height="30"/><text class="up-t" x="301.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">110</text><rect class="up-a" x="318" y="40" width="34" height="30"/><text class="up-t" x="335.0" y="60.0" font-size="12" text-anchor="middle" font-weight="600">111</text><path class="up-al" d="M182,34 v-8 H352 v8"/><text class="up-t" x="267.0" y="20.0" font-size="13" text-anchor="middle" font-weight="600">номера 12…111: 111 − 11 = 100</text><path class="up-l" d="M12,76 v8 H182 v-8"/><text class="up-m" x="137.0" y="100.0" font-size="12" text-anchor="middle" font-weight="400">номера 1…11 — двузначные 9·k</text></svg>
<figcaption>Номера кратных 9: первые одиннадцать дают двузначные числа и вычёркиваются</figcaption>
</figure>

- Кратные 15 — это $15\cdot k$ при $k$ от 7 до 66: $66-6=60$.
- Повторы — числа, которые делятся и на 9, и на 15. Частая ошибка — «это кратные 135». Но 180 делится и на 9, и на 15, а на 135 нет.
- Выпишем кратные 15: 15, 30, 45, 60, 75, 90, …; на 9 делится каждое третье из них: 45, 90, 135, 180, … Это кратные 45: $45\cdot k$ при $k$ от 3 до 22, их $22-2=20$.
- Ответ: $100+60-20=140$.

**Утверждение 6 (два списка). Статус: пишем с нуля.**
Если каждый объект попал хотя бы в один из двух списков, то всего объектов столько, сколько в первом списке, плюс сколько во втором, минус число объектов, попавших в оба.

*Доказательство — утверждение 2 для трёх кусков:* «только в первом», «только во втором», «в обоих». В сумме двух списков кусок «в обоих» посчитан дважды, поэтому его вычитаем один раз.

## Перебор: разложения шестёрки

**Задача 7 (разложения шестёрки). Статус: пишем с нуля.**
Сколькими способами можно представить число 6 в виде суммы натуральных слагаемых? Порядок слагаемых не важен: $2+4$ и $4+2$ — одно разложение. Само 6 тоже считается.

### Список учителя

Учитель выписывает разложения вразброс:

$$2+4,\quad 1+1+1+1+1+1,\quad 1+2+1+2,\quad 3+3,\quad 1+5,\quad 1+1+2+1+1,$$
$$2+3+1,\quad 6,\quad 1+1+3+1,\quad 2+1+1+2,\quad 2+2+2.$$

- Записей 11, правильный ответ тоже 11, но список неверен.
- Повтор: $1+2+1+2$ и $2+1+1+2$ — одно разложение.
- Приманка: $1+1+3+1$ похожа на повтор — тоже четыре слагаемых, — но это другое разложение.
- Тогда разных разложений на доске 10, а ответ 11. Где пропуск? Глазами его не найти: потерянного разложения на доске нет, сравнивать не с чем.
- Повтор ловится вниманием, пропуск — только порядком.

**Определение 8 (одна запись на объект). Статус: пишем с нуля.**
Если порядок внутри объекта не важен, каждый объект записываем одним способом. Для разложений — слагаемые по убыванию: $2+2+1+1$, а не $1+2+1+2$.

### Правила класса

Спрашиваем класс, в каком порядке выписывать, и каждое правило исполняем буквально. Вот что предлагают двенадцатилетние и что из этого выходит (всё проверено перебором).

| правило | что получится | вопрос классу |
|---|---|---|
| по возрастанию первого слагаемого, остальные как придут | 32 записи на 11 разложений: $1+4+1$ и $1+1+4$ — одно и то же | «Это одно разложение? Договоримся писать каждое одним способом» |
| по числу слагаемых | ничья: из трёх слагаемых $4+1+1$, $3+2+1$, $2+2+2$ | «Кто из них первый? Нужен второй признак» |
| сначала самое большое слагаемое | ничья: $4+2$ и $4+1+1$ | «Какое из двух с четвёркой раньше?» — смотрим на второе |
| отщипываем единичку от самого большого | 6, $5+1$, $4+1+1$, …, $1+1+1+1+1+1$ — шесть из одиннадцати | «Правило кончилось, а ответ 11. Цепочка не ветвится» |
| перекладываем по одному: $5+1\to 4+2\to 3+3\to 2+4$ | 16 записей: шесть повторов и пропуск $2+2+2$ | «Оба греха сразу, как в моём списке» |
| разбиваем одно слагаемое на два | 18 записей, семь повторов | «Хорошо для проверки, но кто следующий?» |
| как придёт, но каждое новое сверяем со старыми | повторов нет, пропуск не ловится | «Как ты узнаешь, что всё?» |
| по убыванию первого, при равных — по второму, и так далее | 11, без пропусков и повторов | работает: это словарный порядок от больших к меньшим |

Любое другое правило проверяют два вопроса: у каждого объекта одна запись? Я называю разложение — какое следующее, и оно одно?

### Таблица строим мячом

Правило выбрано. Учитель называет 6 и бросает мяч; поймавший называет следующее разложение по правилу и возвращает мяч, учитель вписывает разложение в строку его первого слагаемого. Так таблица появляется на доске по одному разложению.

<div class="sim" id="sim-c2"><style>#sim-c2 .c2-cards{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;min-height:120px}
#sim-c2 .c2-k{font-family:var(--sans);font-variant-numeric:tabular-nums;font-size:16px;padding:6px 12px;border:1px solid var(--rule);border-radius:6px;background:var(--panel);color:var(--text);transition:border-color .3s,background .3s}
#sim-c2 .c2-k.dup{border:2px solid var(--warm);background:var(--warm-soft)}
#sim-c2 .c2-k.hole{border:2px dashed var(--warm);color:var(--warm);background:transparent}
#sim-c2 .c2-k.found{border:2px solid var(--accent);background:var(--accent-soft)}
#sim-c2 table{border-collapse:separate;border-spacing:0 6px;margin:0 auto}
#sim-c2 th{font-family:var(--sans);font-weight:400;color:var(--muted);text-align:right;padding-right:12px;font-size:15px;white-space:nowrap}
#sim-c2 td{display:flex;flex-wrap:wrap;gap:6px}
#sim-c2 .c2-n{font-size:11px;color:var(--muted);margin-right:4px}</style><div class="c2-cards" role="img" aria-label="Интерактив: одиннадцать записей учителя; кнопки приводят их к одной записи, находят повтор и раскладывают по строкам таблицы"></div>
<div class="sim-bar"><button type="button" class="c2-norm">одна запись на разложение</button><button type="button" class="c2-tab" disabled>в таблицу по первому слагаемому</button><button type="button" class="c2-hole" disabled>показать пропуск</button><button type="button" class="c2-back">сначала</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Одиннадцать записей учителя превращаются в таблицу.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c2");if(!root||!K){return;}
var box=root.querySelector(".c2-cards"),out=root.querySelector(".sim-out"),bN=root.querySelector(".c2-norm"),bT=root.querySelector(".c2-tab"),bH=root.querySelector(".c2-hole"),bB=root.querySelector(".c2-back");
var CH=["2+4","1+1+1+1+1+1","1+2+1+2","3+3","1+5","1+1+2+1+1","2+3+1","6","1+1+3+1","2+1+1+2","2+2+2"];
function nrm(s){return s.split("+").map(Number).sort(function(a,b){return b-a;}).join("+");}
function parts(n,m){if(n===0){return [[]];}var r=[];for(var k=Math.min(n,m);k>=1;k--){parts(n-k,k).forEach(function(p){r.push([k].concat(p));});}return r;}
var P=parts(6,6).map(function(p){return p.join("+");});
function card(t,cls){var e=document.createElement("span");e.className="c2-k"+(cls?" "+cls:"");e.textContent=t;return e;}
function chaos(){K.clear(box);CH.forEach(function(s){box.appendChild(card(s));});bN.disabled=false;bT.disabled=true;bH.disabled=true;out.innerHTML="Записей <b>11</b>, и правильный ответ 11. Верен ли список?";}
function norm(){K.clear(box);var cnt={};CH.forEach(function(s){var t=nrm(s);cnt[t]=(cnt[t]||0)+1;});
CH.forEach(function(s){var t=nrm(s);box.appendChild(card(t,cnt[t]>1?"dup":""));});
bN.disabled=true;bT.disabled=false;out.innerHTML="Повтор: <b>2+2+1+1</b> записано дважды. Разных разложений 10, а ответ 11 — где пропуск?";}
function table(reveal){K.clear(box);var have={};CH.forEach(function(s){have[nrm(s)]=1;});
var tb=document.createElement("table"),num=0;
for(var f=6;f>=1;f--){var tr=document.createElement("tr"),th=document.createElement("th"),td=document.createElement("td");th.textContent=f;
P.filter(function(p){return +p.split("+")[0]===f;}).forEach(function(p){num++;var ok=have[p],e=card("",ok?"":(reveal?"found":"hole"));
var nn=document.createElement("span");nn.className="c2-n";nn.textContent=num;e.appendChild(nn);e.appendChild(document.createTextNode(ok||reveal?p:"?"));td.appendChild(e);});
tr.appendChild(th);tr.appendChild(td);tb.appendChild(tr);}
box.appendChild(tb);bT.disabled=true;bH.disabled=!!reveal;
out.innerHTML=reveal?"Пропуск — <b>4+1+1</b>. Всего <b>1 + 1 + 2 + 3 + 3 + 1 = 11</b>.":"Строка четвёрки неполна: после 4 бывает 2 или 1+1. Пустое место видно сразу.";}
bN.addEventListener("click",norm);bT.addEventListener("click",function(){table(false);});bH.addEventListener("click",function(){table(true);});bB.addEventListener("click",chaos);
chaos();
})();</script></div>

| первое слагаемое | разложения (с номерами) | сколько |
|---|---|---|
| 6 | 1: 6 | 1 |
| 5 | 2: 5+1 | 1 |
| 4 | 3: 4+2, 4: 4+1+1 | 2 |
| 3 | 5: 3+3, 6: 3+2+1, 7: 3+1+1+1 | 3 |
| 2 | 8: 2+2+2, 9: 2+2+1+1, 10: 2+1+1+1+1 | 3 |
| 1 | 11: 1+1+1+1+1+1 | 1 |

- Главное — стыки строк: после $4+1+1$ идёт $3+3$ (частая ошибка — $3+2+1$); после $1+1+1+1+1+1$ — «всё», и надо объяснить почему.
- Всего $1+1+2+3+3+1=11$. Повторов нет: у каждого разложения одна запись и одно первое слагаемое.
- Пропуск из списка учителя виден сразу: строка четвёрки — это 4 и после неё 2 или $1+1$. Без $4+1+1$ строка неполна.
- Когда таблица готова, мяч идёт обратно: что стоит перед $2+2+2$? Ответ — $3+1+1+1$, последнее разложение предыдущей строки.

### Номер в таблице

Таблица даёт каждому разложению номер. Вопрос классу: какой номер у $3+2+1$? И какое разложение стоит девятым?

- Перед строкой тройки стоят строки 6, 5 и 4: в них $1+1+2=4$ разложения. В строке тройки $3+2+1$ второе. Номер $4+2=6$.
- Девятое: строки 6, 5, 4 и 3 занимают $1+1+2+3=7$ номеров. Значит, девятое — второе в строке двойки: $2+2+1+1$.

**Утверждение 9 (номер в таблице). Статус: пишем с нуля.**
Если объекты выписаны строками по порядку, то номер объекта равен числу объектов в строках выше плюс его месту в своей строке. Номер последнего объекта равен числу всех объектов.

*Доказательство — строки выше занимают первые номера:* объектов в них столько, сколько в этих строках вместе, по утверждению 2.

**Утверждение 10 (хороший разрез). Статус: пишем с нуля.**
Если признак у каждого объекта принимает ровно одно значение, то куски «объекты с данным значением» не пересекаются и вместе дают все объекты.

*Доказательство — утверждение 2:* одно значение у каждого объекта — это «ровно в один кусок».

## Флаги

**Задача 11 (флаги). Статус: пишем с нуля.**
Флаг состоит из трёх горизонтальных полос, каждая белая (Б), красная (К) или синяя (С); соседние полосы разного цвета. Сколько всего флагов?

- БКС и КБС — разные флаги: у флага есть верх и низ.
- КББ — не флаг: две соседние белые полосы.
- Порядок — словарный: цвета в порядке Б, К, С; сначала смотрим на верхнюю полосу, при одинаковой верхней — на среднюю, затем на нижнюю. Строки таблицы — по цвету верхней полосы.
- Строка «верх белый»: при красной средней нижняя белая или синяя — БКБ, БКС; при синей средней нижняя белая или красная — БСБ, БСК. Флагов $2+2=4$.
- Строка «верх красный»: КБК, КБС, КСБ, КСК. Строка «верх синий»: СБК, СБС, СКБ, СКС. Всего $4+4+4=12$.

<div class="sim" id="sim-c4"><style>#sim-c4 .c4-rows{display:flex;flex-direction:column;gap:10px;align-items:center}
#sim-c4 .c4-r{display:flex;gap:10px;align-items:center}
#sim-c4 .c4-l{font-family:var(--sans);color:var(--muted);font-size:14px;width:7.5em;text-align:right}
#sim-c4 .c4-f{display:flex;flex-direction:column;align-items:center;gap:3px;font-family:var(--sans);font-size:13px;color:var(--muted);padding:4px;border-radius:6px;border:2px solid transparent;transition:border-color .25s,background .25s;cursor:pointer}
#sim-c4 .c4-f.on{border-color:var(--accent);background:var(--accent-soft);color:var(--text)}
#sim-c4 .c4-flag{display:flex;flex-direction:column;width:46px;height:30px;border:1.5px solid var(--text);border-radius:2px;overflow:hidden}
#sim-c4 .c4-flag i{flex:1}
@media (max-width:480px){#sim-c4 .c4-l{width:5.5em;font-size:12px}#sim-c4 .c4-flag{width:34px;height:22px}}</style><div class="c4-rows" role="img" aria-label="Интерактив: двенадцать флагов из трёх полос в словарном порядке; кнопки ведут подсветку по порядку от флага к флагу"></div>
<div class="sim-bar"><button type="button" class="c4-prev">← перед</button><button type="button" class="c4-next">после →</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Строка — цвет верхней полосы, внутри строки словарный порядок Б, К, С.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c4");if(!root||!K){return;}
var box=root.querySelector(".c4-rows"),out=root.querySelector(".sim-out"),bp=root.querySelector(".c4-prev"),bn=root.querySelector(".c4-next");
var C=["Б","К","С"],COL={"Б":"#ffffff","К":"#c8322c","С":"#2a55b5"},NM={"Б":"белый","К":"красный","С":"синий"},FL=[],el=[],cur=0;
C.forEach(function(a){C.forEach(function(b){C.forEach(function(c){if(a!==b&&b!==c){FL.push(a+b+c);}});});});
C.forEach(function(top){var r=document.createElement("div");r.className="c4-r";var l=document.createElement("span");l.className="c4-l";l.textContent="верх "+NM[top];r.appendChild(l);
FL.forEach(function(f,i){if(f[0]!==top){return;}var w=document.createElement("span");w.className="c4-f";var fl=document.createElement("span");fl.className="c4-flag";
for(var j=0;j<3;j++){var s=document.createElement("i");s.style.background=COL[f[j]];fl.appendChild(s);}
w.appendChild(fl);w.appendChild(document.createTextNode(f));w.addEventListener("click",function(){go(i);});r.appendChild(w);el[i]=w;});
box.appendChild(r);});
function go(i){cur=Math.max(0,Math.min(FL.length-1,i));el.forEach(function(e,k){e.classList.toggle("on",k===cur);});
var f=FL[cur],nx=FL[cur+1],pv=FL[cur-1],s="Флаг <b>"+(cur+1)+"</b> из 12: "+f+".";
if(nx&&nx[0]!==f[0]){s+=" Следующий, "+nx+", — уже в строке «верх "+NM[nx[0]]+"»: стык строк.";}
if(!nx){s+=" Дальше флагов нет.";}
if(pv&&pv[0]!==f[0]){s+=" Перед ним — "+pv+", последний флаг строки «верх "+NM[pv[0]]+"».";}
out.innerHTML=s;bp.disabled=cur===0;bn.disabled=cur===FL.length-1;}
bp.addEventListener("click",function(){go(cur-1);});bn.addEventListener("click",function(){go(cur+1);});
go(0);
})();</script></div>

Флаги мячом, по таблице:

- после БСК идёт КБК — начало следующей строки;
- частые ошибки — КББ (не флаг) и КБС (пропуск: перескочили КБК);
- обратный вопрос, труднее: перед СБК стоит КСК, последний флаг предыдущей строки;
- номер флага КСБ: выше строка «верх белый», четыре флага; в своей строке КСБ третий. Номер $4+3=7$.

## Простая сумма цифр

**Задача 12 (простая сумма цифр · ДЗ, №4). Статус: выверено, dz_29-09_dannye.py.**
У скольких двузначных чисел сумма цифр — простое число?

- Сначала маленький случай: двузначные с суммой цифр 7. Подбирая пары цифр, многие пишут 16, 25, 34, 43, 52, 61 и останавливаются: вторая цифра дошла до 1. Но она может быть нулём, и 70 потеряно. Если резать по первой цифре (от 1 до 7), вторая определена однозначно: семь чисел.
- В таблице двузначных чисел числа с одной суммой цифр лежат на одной косой линии. Резать удобно по самой сумме — она и есть условие.

<div class="sim" id="sim-c3"><style>#sim-c3 .c3-grid{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:3px;max-width:560px;margin:0 auto;font-family:var(--sans);font-variant-numeric:tabular-nums}
#sim-c3 .c3-c{text-align:center;font-size:15px;padding:5px 0;border:1px solid var(--rule);border-radius:4px;background:var(--panel);color:var(--text);transition:background .3s,border-color .3s}
#sim-c3 .c3-c.on{background:var(--accent-soft);border-color:var(--accent);font-weight:600}
#sim-c3 .c3-bar button{min-width:2.6em}
@media (max-width:480px){#sim-c3 .c3-c{font-size:12px;padding:3px 0}}</style><div class="sim-bar w-top c3-bar"></div>
<div class="c3-grid" role="img" aria-label="Интерактив: двузначные числа таблицей; числа с одинаковой суммой цифр лежат на одной косой линии; кнопки подсвечивают строки простых сумм"></div>
<div class="sim-out"></div>
<div class="sim-cap">Числа с одной суммой цифр лежат на одной косой линии таблицы.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c3");if(!root||!K){return;}
var grid=root.querySelector(".c3-grid"),bar=root.querySelector(".c3-bar"),out=root.querySelector(".sim-out"),cells={},PR=[2,3,5,7,11,13,17],sel={};
for(var d=1;d<=9;d++){for(var u=0;u<=9;u++){var n=10*d+u,c=document.createElement("div");c.className="c3-c";c.textContent=n;grid.appendChild(c);cells[n]=c;}}
function cnt(s){var k=0;for(var n=10;n<=99;n++){if(Math.floor(n/10)+n%10===s){k++;}}return k;}
PR.concat(["все"]).forEach(function(s){var b=document.createElement("button");b.type="button";b.textContent=s==="все"?"все простые":s;b.setAttribute("data-s",s);bar.appendChild(b);
b.addEventListener("click",function(){if(s==="все"){var all=PR.every(function(p){return sel[p];});PR.forEach(function(p){sel[p]=!all;});}else{sel[s]=!sel[s];}draw();});});
function draw(){var parts=[],tot=0;
for(var n=10;n<=99;n++){cells[n].classList.toggle("on",!!sel[Math.floor(n/10)+n%10]);}
PR.forEach(function(p){if(sel[p]){var k=cnt(p);parts.push(k);tot+=k;}});
var bs=bar.querySelectorAll("button");for(var i=0;i<bs.length;i++){var s=bs[i].getAttribute("data-s");bs[i].classList.toggle("on",s==="все"?PR.every(function(p){return sel[p];}):!!sel[s]);}
out.innerHTML=parts.length?("Строк: "+parts.length+". Чисел <b>"+parts.join(" + ")+(parts.length>1?" = "+tot:"")+"</b>."):"Нажмите на сумму цифр: подсветится её косая строка.";}
draw();
})();</script></div>

- Простые суммы: 2, 3, 5, 7, 11, 13, 17.
- Сумма $s\le 9$: первая цифра от 1 до $s$, это $s$ чисел.
- Сумма $s\ge 10$: первая цифра от $s-9$ до 9. Из цифр 1…9 не годятся первые $s-10$, остаётся $9-(s-10)=19-s$ чисел.
- Всего $2+3+5+7+8+6+2=33$.

## Фокус

**Пример 13 (номер разложения). Статус: пишем с нуля.**
Разложений девятки тридцать, на доске их нет. «Назовите любое — скажу его номер, если выписать все по нашему правилу. Назовите номер от 1 до 30 — скажу разложение». Учитель отвечает, не глядя в таблицу.

- «$4+3+2$?» — «Четырнадцатое». «Двадцатое?» — «$3+3+2+1$».
- Как это сделано? Так же, как номера шестёрки, по утверждению 9. Учитель знает, сколько разложений в каждой строке; это и есть весь секрет. Выписываем длины строк на доску, и дальше номера считает класс.
- Строки девятки по первому слагаемому 9, 8, …, 1 содержат 1, 1, 2, 3, 5, 6, 7, 4, 1 разложений.
- $4+3+2$: выше $1+1+2+3+5=12$, в строке четвёрки оно второе (после $4+4+1$). Номер 14.
- Номер 20: строки 9…4 занимают $12+6=18$ номеров, значит, это второе в строке тройки (после $3+3+3$) — $3+3+2+1$.

Таблица девятки целиком:

| первое слагаемое | разложения (с номерами) |
|---|---|
| 9 | 1: 9 |
| 8 | 2: 8+1 |
| 7 | 3: 7+2, 4: 7+1+1 |
| 6 | 5: 6+3, 6: 6+2+1, 7: 6+1+1+1 |
| 5 | 8: 5+4, 9: 5+3+1, 10: 5+2+2, 11: 5+2+1+1, 12: 5+1+1+1+1 |
| 4 | 13: 4+4+1, 14: 4+3+2, 15: 4+3+1+1, 16: 4+2+2+1, 17: 4+2+1+1+1, 18: 4+1+1+1+1+1 |
| 3 | 19: 3+3+3, 20: 3+3+2+1, 21: 3+3+1+1+1, 22: 3+2+2+2, 23: 3+2+2+1+1, 24: 3+2+1+1+1+1, 25: 3+1+1+1+1+1+1 |
| 2 | 26: 2+2+2+2+1, 27: 2+2+2+1+1+1, 28: 2+2+1+1+1+1+1, 29: 2+1+1+1+1+1+1+1 |
| 1 | 30: 1+1+1+1+1+1+1+1+1 |

## Ответ

Фокус работает потому, что таблица — это и есть счёт: у каждого объекта свой номер, без пропусков и повторов, и последний номер равен числу объектов. Каждый ответ урока получен одинаково: выбрали, на какие куски резать, проверили, что нет пропусков и повторов, сложили или вычли.

| задача | режем по | ответ |
|---|---|---|
| 1, далматинцы | пятнам на ушах | $101-22-29=50$ |
| 4, лестница | пролётам; первый, из подвала, вычеркнут | $10-1=9$ пролётов |
| 5, 9 или 15 | делимости; повторы — кратные 45 | $100+60-20=140$ |
| 7, разложения 6 | первому слагаемому | $1+1+2+3+3+1=11$ |
| 11, флаги | цвету верхней полосы | $4+4+4=12$ |
| 12, простая сумма цифр | самой сумме цифр | $2+3+5+7+8+6+2=33$ |
| 13, разложения 9 | первому слагаемому | $1+1+2+3+5+6+7+4+1=30$ |

Если резать все двузначные числа по сумме цифр, строки сумм от 1 до 9 содержат $1+2+\ldots+9=45$ чисел. Как быстро складывать такие суммы — следующий разговор.
