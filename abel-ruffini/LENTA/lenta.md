---
tab: Геометрия дискриминанта
status: chistovik
poryadok: 1
registr: читаемый
nomera: da
zhanr: statya
---

# Геометрия дискриминанта

<div class="podzag">почему у уравнения пятой степени нет формулы</div>

Корни квадратного уравнения выражаются через коэффициенты по известной со школы формуле. Для уравнений третьей и четвёртой степени такие формулы тоже есть, только длиннее. Есть ли формула для уравнения пятой степени?

Формулы для третьей и четвёртой степени нашли итальянские алгебраисты XVI века. Тарталья открыл способ решать кубические уравнения и сообщил его Кардано, взяв с него клятву никому этот способ не раскрывать. В 1540 году ученик Кардано Феррари свёл уравнение четвёртой степени к кубическому, и в 1545 году Кардано, несмотря на клятву, опубликовал оба решения в книге «Великое искусство». С пятой степенью ничего не выходило ещё два с половиной столетия. Чтобы понять почему, не будем искать формулу, а посмотрим на сами многочлены как на точки пространства и проследим, как от точки зависят корни.

<div class="chast">Часть I · вещественный мир</div>

## Сколько корней: степени 2, 3 и 4

Приведённый квадратный трёхчлен $x^2+px+q$ задаётся парой чисел $(p,q)$, то есть точкой плоскости. Число его корней определяется знаком дискриминанта $D=p^2-4q$: при $D\gt 0$ корней два, при $D=0$ один, при $D\lt 0$ корней нет. Значит, парабола $q=p^2/4$ делит плоскость на две области. Под параболой лежат трёхчлены с двумя корнями, над ней — без корней, а на самой параболе — трёхчлены с одним корнем.

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
.sim .k-d0{background:var(--text)}.sim .k-d1{background:var(--accent)}.sim .k-d2{background:var(--warm)}.sim .k-d3{background:var(--defn)}.sim .k-d4{background:var(--sim-v)}</style><script>(function(){
var NS="http://www.w3.org/2000/svg";
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
})();</script></div>

<div class="sim" id="sim-c12"><style>#sim-c12 .c12-pt{stroke:var(--panel);stroke-width:1.5}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева плоскость коэффициентов трёхчлена x в квадрате плюс p x плюс q с параболой q равно p в квадрате на 4, справа графики трёхчленов; чёрную точку можно перетаскивать"></svg>
<div class="sim-bar"><button type="button">два корня</button><button type="button">один корень</button><button type="button">нет корней</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Слева плоскость коэффициентов $(p,q)$ трёхчлена $x^2+px+q$, справа графики. Цветные точки — три трёхчлена-образца, их графики тех же цветов; чёрную точку можно перетаскивать, её график жирный: под параболой корней два, на ней один, над ней (закрашено) ни одного.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c12"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var A=new K.Panel(20,18,290,264,[-3,3],[-1.7,2.7]),B=new K.Panel(360,18,270,264,[-3,3],[-3,4]);
var st=K.el("g",{},svg),gs=K.el("g",{},svg),dyn=K.el("g",{},svg),tp=K.el("g",{},svg),hl=K.el("g",{},svg),i,cv=[];
for(i=0;i<=240;i++){var p0=-3+6*i/240;cv.push([p0,p0*p0/4]);}
K.el("polygon",{"class":"k-shade",points:cv.map(function(v){return A.X(v[0]).toFixed(1)+","+A.Y(v[1]).toFixed(1);}).join(" ")+" "+A.X(3)+","+A.Y(2.7)+" "+A.X(-3)+","+A.Y(2.7)},st);
A.axes(st,"p","q");B.axes(st,"x","y");
K.el("path",{"class":"k-curve",d:A.d(cv)},st);
var S=[[0.9,-0.9,1,false],[1.6,0.64,3,true],[-0.6,1.6,2,false]];
function roots(p,q,on){var D=p*p-4*q,s;if(on){return [-p/2];}if(D<0){return [];}s=Math.sqrt(D);return [(-p-s)/2,(-p+s)/2];}
function gr(p,q){var pts=[],k,x;for(k=0;k<=300;k++){x=-3+6*k/300;pts.push([x,x*x+p*x+q]);}return pts;}
S.forEach(function(s){K.el("path",{"class":"k-t"+s[2],d:B.d(gr(s[0],s[1]))},gs);roots(s[0],s[1],s[3]).forEach(function(r){K.el("circle",{"class":"k-k"+s[2]+" c12-pt",cx:B.X(r),cy:B.Y(0),r:4.5},tp);});K.el("circle",{"class":"k-k"+s[2]+" c12-pt",cx:A.X(s[0]),cy:A.Y(s[1]),r:5.5},st);});
var P=[-1.4,-0.6],on=false,drag=false;
function poly(p,q){var s="x²";if(Math.abs(p)>=0.005){s+=(p<0?" − ":" + ")+K.num(Math.abs(p))+"x";}if(Math.abs(q)>=0.005){s+=(q<0?" − ":" + ")+K.num(Math.abs(q));}return s;}
function draw(){K.clear(dyn);K.clear(hl);var p=P[0],q=P[1],r=roots(p,q,on),D=p*p-4*q,h;
K.el("path",{"class":"k-curve",d:B.d(gr(p,q))},dyn);
r.forEach(function(x){K.el("circle",{"class":"k-k0 c12-pt",cx:B.X(x),cy:B.Y(0),r:6.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(p),cy:A.Y(q),r:16},hl);K.el("circle",{"class":"k-handle",cx:A.X(p),cy:A.Y(q),r:6.5},hl);
if(on){h="D = 0, один корень: "+K.num(r[0]);}else if(D>0){h="D = "+K.num(D)+" > 0, два корня: "+K.num(r[0])+" и "+K.num(r[1]);}else{h="D = "+K.num(D)+" < 0, корней нет";}
out.textContent=poly(p,q)+": "+h;}
function cl(v,a,b){return Math.max(a,Math.min(b,v));}
function set(e){var s=K.pt(svg,e),p=cl(A.ix(s.x),-2.95,2.95),q=cl(A.iy(s.y),-1.65,2.65),f=q-p*p/4;on=Math.abs(f)/Math.sqrt(1+p*p/4)<0.04;if(on){q=p*p/4;}P=[p,q];draw();}
function go(k){P=[S[k][0],S[k][1]];on=S[k][3];draw();}
bs.forEach(function(b,k){b.addEventListener("click",function(){go(k);});});
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
svg.addEventListener("pointercancel",function(){drag=false;});
draw();
})();</script></div>

**Определение 1 (кратный корень). Статус: выверено, SKELET опр. 2.**
Корень $x_0$ многочлена $f$ называется кратным, если $f$ делится на $(x-x_0)^2$, и простым в противном случае.

Для кубических многочленов ответ тоже читается по коэффициентам. Член с $x^2$ убирается сдвигом $x\mapsto x+c$, поэтому достаточно рассмотреть $x^3+px+q$.

**Утверждение 2 (корни кубического многочлена). Статус: объявляем.**
Пусть $D_3=-4p^3-27q^2$. Если $D_3\gt 0$, у многочлена $x^3+px+q$ три различных вещественных корня; если $D_3\lt 0$ — один вещественный корень, простой; если $D_3=0$ и $(p,q)\ne(0,0)$ — двойной корень и простой; если $p=q=0$ — тройной корень $0$.

> поле:mn Это утверждение мы принимаем без доказательства; его можно доказать школьными средствами, сравнив значения многочлена в точках локального минимума и максимума. См. статью «[Кубическое уравнение](https://ru.wikipedia.org/wiki/Кубическое_уравнение)».

Многочлен с двойным корнем $t$ имеет вид
$$(x-t)^2(x+2t)=x^3-3t^2x+2t^3$$
(сумма корней равна нулю, поэтому третий корень $-2t$), то есть
$$p=-3t^2,\qquad q=2t^3.$$
Такие точки образуют полукубическую параболу $4p^3+27q^2=0$ с остриём в начале координат. Внутри её «клюва» лежат многочлены с тремя корнями, снаружи — с одним.

<div class="sim" id="sim-c13"><style>#sim-c13 .c13-pt{stroke:var(--panel);stroke-width:1.5}
#sim-c13 .c13-mult{fill:none;stroke:var(--text);stroke-width:1.2;opacity:.6}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева плоскость коэффициентов многочлена x в кубе плюс p x плюс q с полукубической параболой 4p в кубе плюс 27q в квадрате равно нулю, справа графики многочленов; чёрную точку можно перетаскивать"></svg>
<div class="sim-bar"><button type="button">три корня</button><button type="button">двойной и простой</button><button type="button">тройной</button><button type="button">один корень</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Слева плоскость $(p,q)$ многочленов $x^3+px+q$ с полукубической параболой $4p^3+27q^2=0$, справа графики; цветные точки — четыре образца, их графики тех же цветов. Чёрную точку можно перетаскивать: в закрашенном «клюве» корней три, снаружи один, на кривой два из них сливаются в двойной, а в острие все три — в тройной.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c13"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var A=new K.Panel(20,18,290,264,[-4,1.5],[-3,3]),B=new K.Panel(360,18,270,264,[-2.6,2.6],[-4,4]);
var st=K.el("g",{},svg),gs=K.el("g",{},svg),dyn=K.el("g",{},svg),tp=K.el("g",{},svg),hl=K.el("g",{},svg),i,cv=[],TM=Math.sqrt(4/3);
for(i=0;i<=300;i++){var t0=-TM+2*TM*i/300;cv.push([-3*t0*t0,2*t0*t0*t0]);}
K.el("polygon",{"class":"k-shade",points:cv.map(function(v){return A.X(v[0]).toFixed(1)+","+A.Y(Math.max(-3,Math.min(3,v[1]))).toFixed(1);}).join(" ")},st);
A.axes(st,"p","q");B.axes(st,"x","y");
K.el("path",{"class":"k-curve",d:A.d(cv)},st);
var S=[[-3.2,-0.5,1,0,0],[-1.47,0.686,3,1,0.7],[0,0,4,2,0],[0.8,1.02,2,0,0]];
function cub(p,q,x){return x*x*x+p*x+q;}
function roots(p,q,m,t){var D=-4*p*p*p-27*q*q,a,b,x,k,r=[],c,th,d;
if(m===2){return [[0,3]];}
if(m===1){return t>0?[[-2*t,1],[t,2]]:[[t,2],[-2*t,1]];}
if(D>0){c=2*Math.sqrt(-p/3);th=Math.acos(Math.max(-1,Math.min(1,3*q/(2*p)*Math.sqrt(-3/p))))/3;for(k=0;k<3;k++){r.push([c*Math.cos(th-2*Math.PI*k/3),1]);}r.sort(function(u,v){return u[0]-v[0];});return r;}
a=-q/2;b=Math.sqrt(Math.max(0,q*q/4+p*p*p/27));x=Math.cbrt(a+b)+Math.cbrt(a-b);
for(k=0;k<3;k++){d=3*x*x+p;if(Math.abs(d)>1e-9){x-=cub(p,q,x)/d;}}
return [[x,1]];}
function gr(p,q){var pts=[],k,x;for(k=0;k<=300;k++){x=-2.6+5.2*k/300;pts.push([x,cub(p,q,x)]);}return pts;}
S.forEach(function(s){K.el("path",{"class":"k-t"+s[2],d:B.d(gr(s[0],s[1]))},gs);roots(s[0],s[1],s[3],s[4]).forEach(function(r){K.el("circle",{"class":"k-k"+s[2]+" c13-pt",cx:B.X(r[0]),cy:B.Y(0),r:4.5},tp);});K.el("circle",{"class":"k-k"+s[2]+" c13-pt",cx:A.X(s[0]),cy:A.Y(s[1]),r:5.5},st);});
var P=[-1.6,-0.5],M=0,T=0,drag=false;
function poly(p,q){var s="x³";if(Math.abs(p)>=0.005){s+=(p<0?" − ":" + ")+K.num(Math.abs(p))+"x";}if(Math.abs(q)>=0.005){s+=(q<0?" − ":" + ")+K.num(Math.abs(q));}return s;}
function fd(v){if(Math.abs(v)>=0.005){return K.num(v);}return (v<0?"−":"")+Math.abs(v).toPrecision(2).replace(".",",");}
function lst(r){var s=r.map(function(e){return K.num(e[0]);});return s.length>1?s.slice(0,-1).join("; ")+" и "+s[s.length-1]:s[0];}
function draw(){K.clear(dyn);K.clear(hl);var p=P[0],q=P[1],r=roots(p,q,M,T),D=-4*p*p*p-27*q*q,h;
K.el("path",{"class":"k-curve",d:B.d(gr(p,q))},dyn);
r.forEach(function(e){var j;for(j=1;j<e[1];j++){K.el("circle",{"class":"c13-mult",cx:B.X(e[0]),cy:B.Y(0),r:7+4*j},dyn);}K.el("circle",{"class":"k-k0 c13-pt",cx:B.X(e[0]),cy:B.Y(0),r:6.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(p),cy:A.Y(q),r:16},hl);K.el("circle",{"class":"k-handle",cx:A.X(p),cy:A.Y(q),r:6.5},hl);
if(M===2){h="p = q = 0 — тройной корень 0";}else if(M===1){h="D₃ = 0 — двойной корень "+K.num(T)+" и простой "+K.num(-2*T);}else if(D>0){h="D₃ = "+fd(D)+" > 0 — три различных корня: "+lst(r);}else{h="D₃ = "+fd(D)+" < 0 — один вещественный корень "+K.num(r[0][0]);}
out.textContent=poly(p,q)+": "+h;}
function cl(v,a,b){return Math.max(a,Math.min(b,v));}
function set(e){var s=K.pt(svg,e),p=cl(A.ix(s.x),-3.95,1.45),q=cl(A.iy(s.y),-2.95,2.95),k,t,d,bd=1e9,bt=0;
M=0;if(Math.hypot(p,q)<0.1){M=2;p=0;q=0;}else{for(k=-570;k<=570;k++){t=k/500;d=Math.hypot(p+3*t*t,q-2*t*t*t);if(d<bd){bd=d;bt=t;}}if(bd<0.04){M=1;T=bt;p=-3*bt*bt;q=2*bt*bt*bt;}}
P=[p,q];draw();}
function go(k){var s=S[k];P=[s[0],s[1]];M=s[3];T=s[4];draw();}
bs.forEach(function(b,k){b.addEventListener("click",function(){go(k);});});
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
svg.addEventListener("pointercancel",function(){drag=false;});
draw();
})();</script></div>

Многочлены $x^4+ax^2+bx+c$ — точки трёхмерного пространства, и здесь то же исследование можно провести полностью. Многочлен с двойным корнем $t$ делится на $(x-t)^2$, а так как сумма корней равна нулю, частное имеет вид $x^2+2tx+e$:
$$(x-t)^2(x^2+2tx+e)=x^4+(e-3t^2)x^2+2t(t^2-e)\,x+t^2e.$$
Отсюда $a=e-3t^2$, и
$$b=-4t^3-2at,\qquad c=3t^4+at^2.$$
Эти точки образуют поверхность, которую по форме называют ласточкиным хвостом. Она делит пространство на три области, в которых у многочлена 0, 2 и 4 вещественных корня.

<div class="sim" id="sim-c6"><style>#sim-c6 .c6-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:14px;align-items:center}
#sim-c6 .c6-3d{position:relative;height:320px;min-width:0;overflow:hidden;border-radius:12px;border:1px solid var(--rule);cursor:grab;touch-action:none;user-select:none;-webkit-user-select:none}
#sim-c6 .c6-3d.c6-drag{cursor:grabbing}
#sim-c6 .c6-3d canvas{display:block;width:100%;height:100%;touch-action:none}
#sim-c6 .c6-msg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:0 1.5em;text-align:center;font-family:var(--sans);font-size:15px;color:var(--muted)}
#sim-c6 .c6-lab{position:absolute;left:0;top:0;transform:translate(-50%,-50%);font-family:var(--sans);font-size:15px;font-style:italic;color:var(--muted);pointer-events:none;line-height:1}
#sim-c6 .c6-hint{position:absolute;right:10px;bottom:7px;font-family:var(--sans);font-size:12px;color:var(--faint);pointer-events:none}
#sim-c6 .c6-sl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px 18px;margin:.9em 0 .2em;font-family:var(--sans)}
#sim-c6 .c6-sl label{display:flex;align-items:center;gap:.55em;min-width:0;color:var(--text);font-size:15px}
#sim-c6 .c6-sl i{font-family:var(--serif,Georgia,serif);font-size:17px;width:.7em;text-align:center}
#sim-c6 .c6-sl input{flex:1;min-width:0;margin:0;accent-color:var(--accent);height:26px;cursor:pointer}
#sim-c6 .c6-sl output{font-variant-numeric:tabular-nums;color:var(--muted);min-width:3.4em;text-align:right}
#sim-c6 .k-c6r{fill:var(--panel);stroke:var(--text);stroke-width:1.8}
@media (max-width:640px){#sim-c6 .c6-grid{grid-template-columns:minmax(0,1fr)}#sim-c6 .c6-3d{height:300px}#sim-c6 .c6-sl{grid-template-columns:minmax(0,1fr)}}</style><div class="c6-grid"><div class="c6-3d" role="img" aria-label="Интерактив: поверхность ласточкина хвоста в пространстве коэффициентов a, b, c многочлена x в четвёртой плюс a x квадрат плюс b x плюс c; картинку можно вращать, точка P двигается ползунками"><div class="c6-msg">загружаю трёхмерную картинку…</div></div><svg viewBox="0 0 360 300" role="img" aria-label="График многочлена x в четвёртой плюс a x квадрат плюс b x плюс c с отмеченными вещественными корнями"></svg></div>
<div class="c6-sl"><label><i>a</i><input type="range" min="-2.5" max="1.2" step="0.01" value="-2" aria-label="коэффициент a"><output>−2,00</output></label><label><i>b</i><input type="range" min="-2.6" max="2.6" step="0.01" value="0" aria-label="коэффициент b"><output>0,00</output></label><label><i>c</i><input type="range" min="-1.2" max="3.2" step="0.01" value="0.5" aria-label="коэффициент c"><output>0,50</output></label></div>
<div class="sim-bar"><button type="button">в пирамидку</button><button type="button">наружу</button><button type="button">над хвостом</button><button type="button">исходный вид</button></div>
<div class="sim-out"></div><div class="sim-cap">Ласточкин хвост — это многочлены $x^4+ax^2+bx+c$ с кратным корнем; жирные линии на нём — рёбра возврата (тройной корень) и линия самопересечения (два двойных корня). Ползунки двигают точку $P=(a,b,c)$, хвост можно вращать мышью или пальцем, а график показывает корни: внутри «пирамидки» их четыре, снаружи два, над хвостом ни одного.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c6");
if(!root||!K){return;}
var wrap=root.querySelector(".c6-3d"),msg=root.querySelector(".c6-msg"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".sim-bar button"),ins=root.querySelectorAll(".c6-sl input"),ovs=root.querySelectorAll(".c6-sl output");
var RG=[[-2.5,1.2],[-2.6,2.6],[-1.2,3.2]],P0=[-2,0,0.5],P=P0.slice(),V0=[0.55,0.4],view=V0.slice(),G=null,kind="--warm";
var Pn=new K.Panel(34,14,312,262,[-2.3,2.3],[-3,5]),st=K.el("g",{},svg),dyn=K.el("g",{},svg);
Pn.axes(st,"x","y");
function f(x){return x*(x*(x*x+P[0])+P[1])+P[2];}
function cub(p,q){var D=q*q/4+p*p*p/27,r=[],i,k;
if(D>1e-13){var s=Math.sqrt(D);r=[Math.cbrt(-q/2+s)+Math.cbrt(-q/2-s)];}else if(p<-1e-9){var m=2*Math.sqrt(-p/3),th=Math.acos(Math.max(-1,Math.min(1,1.5*q/p*Math.sqrt(-3/p))))/3;for(k=0;k<3;k++){r.push(m*Math.cos(th-2*Math.PI*k/3));}}else{r=[0];}
for(i=0;i<r.length;i++){for(k=0;k<4;k++){var d=3*r[i]*r[i]+p;if(Math.abs(d)>1e-9){r[i]-=(r[i]*r[i]*r[i]+p*r[i]+q)/d;}}}
r.sort(function(u,v){return u-v;});return r;}
function roots(){var cr=cub(P[0]/2,P[1]/4),cs=[],i,j,R=1+Math.max(Math.abs(P[0]),Math.abs(P[1]),Math.abs(P[2])),tol=1e-5,res=[];
if(cr.length===1&&Math.abs(P[0])<1e-9&&Math.abs(P[1])<1e-9){cs=[{x:0,n:3}];}else{for(i=0;i<cr.length;i++){if(cs.length&&Math.abs(cr[i]-cs[cs.length-1].x)<2e-3){cs[cs.length-1].n++;}else{cs.push({x:cr[i],n:1});}}}
var nd=[{x:-R,v:f(-R)}];cs.forEach(function(c){var v=f(c.x);nd.push({x:c.x,v:v,z:Math.abs(v)<tol});if(Math.abs(v)<tol){res.push({x:c.x,m:c.n+1});}});nd.push({x:R,v:f(R)});
for(i=0;i+1<nd.length;i++){var u=nd[i],w=nd[i+1];if(!u.z&&!w.z&&u.v*w.v<0){var lo=u.x,hi=w.x,fl=u.v;for(j=0;j<70;j++){var mi=(lo+hi)/2,fm=f(mi);if(fm*fl>0){lo=mi;fl=fm;}else{hi=mi;}}res.push({x:(lo+hi)/2,m:1});}}
res.sort(function(u,v){return u.x-v.x;});return res;}
function poly(){var a=P[0],b=P[1],c=P[2];return "x⁴ "+(a<-0.004?"− ":"+ ")+K.num(Math.abs(a))+"x² "+(b<-0.004?"− ":"+ ")+K.num(Math.abs(b))+"x "+(c<-0.004?"− ":"+ ")+K.num(Math.abs(c));}
function words(rs){var mu=rs.filter(function(r){return r.m>1;}),s=rs.length-mu.length;
if(!mu.length){return s===4?"четыре вещественных корня":(s===2?"два вещественных корня":"вещественных корней нет");}
if(mu.length===2){return "кратные корни: два двойных, точка P на линии самопересечения";}
var m=mu[0].m,nm=m===2?"двойной":(m===3?"тройной":"четвёртой кратности");
return "кратный корень ("+nm+")"+(s===2?" и ещё два простых":(s===1?" и ещё простой":", других вещественных нет"))+", точка P на поверхности";}
function draw2d(rs){K.clear(dyn);var g=[],x;for(x=-2.3;x<=2.3001;x+=0.01){g.push([x,f(x)]);}
K.el("path",{"class":"k-curve",d:Pn.d(g)},dyn);
rs.forEach(function(r){if(r.m>1){K.el("circle",{"class":"k-ring",cx:Pn.X(r.x),cy:Pn.Y(0),r:11},dyn);K.el("circle",{"class":"k-c6r",cx:Pn.X(r.x),cy:Pn.Y(0),r:5.5},dyn);}else{K.el("circle",{"class":rs.length===4?"k-f2":"k-f1",cx:Pn.X(r.x),cy:Pn.Y(0),r:5.5},dyn);}});}
function update(){var rs=roots(),mu=rs.some(function(r){return r.m>1;});
kind=mu?"--text":(rs.length===4?"--warm":(rs.length===2?"--accent":"--muted"));
draw2d(rs);out.textContent=poly()+": "+words(rs);
P.forEach(function(v,i){ins[i].value=v;ovs[i].textContent=K.num(v);});
if(G){G.place();}}
function setP(q){P=q.slice();update();}
ins.forEach(function(inp,i){inp.addEventListener("input",function(){P[i]=Math.round(parseFloat(inp.value)*100)/100;update();});});
bs[0].addEventListener("click",function(){setP([-2,0,0.5]);});
bs[1].addEventListener("click",function(){setP([-2,0,-1]);});
bs[2].addEventListener("click",function(){setP([-2,0,3]);});
bs[3].addEventListener("click",function(){view=V0.slice();setP(P0);if(G){G.req();}});
update();
function col(n,fb){var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||fb;}
function fail(){msg.textContent="трёхмерная картинка не загрузилась, а график и ползунки работают";}
function init3d(){var T=window.THREE;
var KA=0.6,KB=0.42,KC=0.42,A0=(RG[0][0]+RG[0][1])/2,C0=(RG[2][0]+RG[2][1])/2,SZ=1;
function V(a,b,c){return new T.Vector3(b*KB,(c-C0)*KC,SZ*(a-A0)*KA);}
var rd;
try{rd=new T.WebGLRenderer({antialias:true,alpha:true});}catch(e){fail();return;}
rd.setPixelRatio(Math.min(2,window.devicePixelRatio||1));rd.setClearColor(0x000000,0);rd.localClippingEnabled=true;
msg.parentNode.removeChild(msg);wrap.appendChild(rd.domElement);
var sc=new T.Scene(),cam=new T.PerspectiveCamera(26,1,0.1,60);sc.add(cam);
sc.add(new T.AmbientLight(0xffffff,0.55));var dl=new T.DirectionalLight(0xffffff,0.6);dl.position.set(1.2,2.2,3);cam.add(dl);
var xm=RG[1][1]*KB,y0=(RG[2][0]-C0)*KC,y1=(RG[2][1]-C0)*KC,e=1e-3;
var planes=[new T.Plane(new T.Vector3(-1,0,0),xm+e),new T.Plane(new T.Vector3(1,0,0),xm+e),new T.Plane(new T.Vector3(0,-1,0),y1+e),new T.Plane(new T.Vector3(0,1,0),-y0+e)];
function tmax(a){var t=0;while(t<1.6){t+=0.004;var b=-4*t*t*t-2*a*t,c=3*t*t*t*t+a*t*t;if(Math.abs(b)>RG[1][1]||c>RG[2][1]){break;}}return Math.min(1.6,t+0.012);}
var NA=110,NT=200,pos=[],nor=[],idx=[],i,j;
for(i=0;i<=NA;i++){var a=RG[0][0]+(RG[0][1]-RG[0][0])*i/NA,tm=tmax(a);for(j=0;j<=NT;j++){var t=tm*(2*j/NT-1),p=V(a,-4*t*t*t-2*a*t,3*t*t*t*t+a*t*t);pos.push(p.x,p.y,p.z);
var ux=-2*t*KB,uy=t*t*KC,uz=SZ*KA,vx=KB,vy=-t*KC,nx=-uz*vy,ny=uz*vx,nz=ux*vy-uy*vx,nl=Math.sqrt(nx*nx+ny*ny+nz*nz)||1;nor.push(nx/nl,ny/nl,nz/nl);}}
for(i=0;i<NA;i++){for(j=0;j<NT;j++){var k=i*(NT+1)+j;idx.push(k,k+1,k+NT+1,k+1,k+NT+2,k+NT+1);}}
var geo=new T.BufferGeometry();geo.setAttribute("position",new T.Float32BufferAttribute(pos,3));geo.setAttribute("normal",new T.Float32BufferAttribute(nor,3));geo.setIndex(idx);
var mS=new T.MeshPhongMaterial({transparent:true,opacity:0.45,side:T.DoubleSide,depthWrite:false,shininess:20,specular:0x0c0c0c,clippingPlanes:planes});
sc.add(new T.Mesh(geo,mS));
var mE=new T.MeshBasicMaterial({}),mA=new T.LineBasicMaterial({}),mH=new T.MeshBasicMaterial({}),mB=new T.LineBasicMaterial({transparent:true,opacity:0.7}),mP=new T.MeshPhongMaterial({shininess:30,specular:0x1a1a1a});
function tube(F,n,t0,t1){var ps=[],q;for(q=0;q<=n;q++){ps.push(F(t0+(t1-t0)*q/n));}sc.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(ps),n*2,0.011,8,false),mE));}
var tc=Math.sqrt(2.5/6);
tube(function(t){return V(-6*t*t,8*t*t*t,-3*t*t*t*t);},80,0,tc);
tube(function(t){return V(-6*t*t,8*t*t*t,-3*t*t*t*t);},80,0,-tc);
tube(function(s){return V(s,0,s*s/4);},80,0,-2.5);
var ax=[[V(RG[0][0],0,0),V(RG[0][1],0,0)],[V(0,RG[1][0],0),V(0,RG[1][1],0)],[V(0,0,RG[2][0]),V(0,0,RG[2][1])]],nm=["a","b","c"],labs=[];
ax.forEach(function(s,q){var g=new T.BufferGeometry().setFromPoints(s);sc.add(new T.Line(g,mA));var dir=s[1].clone().sub(s[0]).normalize(),cone=new T.Mesh(new T.ConeGeometry(0.028,0.1,14),mH);cone.position.copy(s[1]).add(dir.clone().multiplyScalar(0.05));cone.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);sc.add(cone);
var l=document.createElement("span");l.className="c6-lab";l.textContent=nm[q];wrap.appendChild(l);labs.push({el:l,v:s[1].clone().add(dir.clone().multiplyScalar(0.2))});});
var bx=new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(2*xm,y1-y0,(RG[0][1]-RG[0][0])*KA)),mB);bx.position.set(0,(y0+y1)/2,0);sc.add(bx);
var sg=new T.SphereGeometry(0.06,28,18),ball=new T.Mesh(sg,mP),mG=new T.MeshPhongMaterial({transparent:true,opacity:0.92,depthTest:false,depthWrite:false,shininess:30,specular:0x1a1a1a}),ghost=new T.Mesh(sg,mG),mO=new T.MeshBasicMaterial({side:T.BackSide,transparent:true,opacity:0.75,depthTest:false,depthWrite:false}),rim=new T.Mesh(new T.SphereGeometry(0.078,28,18),mO);ghost.renderOrder=5;rim.renderOrder=4;sc.add(ball);sc.add(rim);sc.add(ghost);
var hint=document.createElement("span");hint.className="c6-hint";hint.textContent="тяните, чтобы повернуть";wrap.appendChild(hint);
var W=1,H=1,pend=false;
function size(){W=Math.max(1,wrap.clientWidth);H=Math.max(1,wrap.clientHeight);rd.setSize(W,H,false);cam.aspect=W/H;var vf=cam.fov*Math.PI/180,hf=2*Math.atan(Math.tan(vf/2)*cam.aspect);cam.userData.d=1.62/Math.sin(Math.min(vf,hf)/2);cam.updateProjectionMatrix();}
function render(){var d=cam.userData.d,th=view[0],ph=view[1];cam.position.set(d*Math.cos(ph)*Math.sin(th),d*Math.sin(ph),d*Math.cos(ph)*Math.cos(th));cam.lookAt(0,0.02,0);cam.updateMatrixWorld();rd.render(sc,cam);
labs.forEach(function(L){var q=L.v.clone().project(cam);L.el.style.left=((q.x+1)/2*W).toFixed(1)+"px";L.el.style.top=((1-q.y)/2*H).toFixed(1)+"px";});}
function req(){if(!pend){pend=true;requestAnimationFrame(function(){pend=false;render();});}}
function recolor(){mS.color.set(col("--accent","#2f6e8e"));mE.color.set(col("--text","#211f1b"));mA.color.set(col("--muted","#726c60"));mH.color.set(col("--muted","#726c60"));mB.color.set(col("--rule","#e7e2d6"));mO.color.set(col("--panel","#fffdf8"));mP.color.set(col(kind,"#c9743a"));mG.color.set(col(kind,"#c9743a"));req();}
function place(){var p=V(P[0],P[1],P[2]);ball.position.copy(p);ghost.position.copy(p);rim.position.copy(p);mP.color.set(col(kind,"#c9743a"));mG.color.set(col(kind,"#c9743a"));req();}
G={place:place,req:req};
var dr=null;
wrap.addEventListener("pointerdown",function(ev){dr={x:ev.clientX,y:ev.clientY};wrap.setPointerCapture(ev.pointerId);wrap.classList.add("c6-drag");ev.preventDefault();});
wrap.addEventListener("pointermove",function(ev){if(!dr){return;}view[0]-=(ev.clientX-dr.x)*0.009;view[1]=Math.max(-1.35,Math.min(1.35,view[1]+(ev.clientY-dr.y)*0.009));dr={x:ev.clientX,y:ev.clientY};req();});
function up(){dr=null;wrap.classList.remove("c6-drag");}
wrap.addEventListener("pointerup",up);wrap.addEventListener("pointercancel",up);
if(window.ResizeObserver){new ResizeObserver(function(){size();req();}).observe(wrap);}else{window.addEventListener("resize",function(){size();req();});}
new MutationObserver(recolor).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme","class","style"]});
var mq=window.matchMedia?window.matchMedia("(prefers-color-scheme: dark)"):null;
if(mq){if(mq.addEventListener){mq.addEventListener("change",recolor);}else if(mq.addListener){mq.addListener(recolor);}}
size();recolor();place();}
if(window.THREE&&window.THREE.WebGLRenderer){init3d();}else{var src="https:"+"/"+"/cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",sc0=document.querySelector("script[data-three-r128]");
var ok=function(){if(window.THREE&&window.THREE.WebGLRenderer){init3d();}else{fail();}};
if(sc0){if(window.THREE){ok();}else{sc0.addEventListener("load",ok);sc0.addEventListener("error",fail);}}else{sc0=document.createElement("script");sc0.src=src;sc0.async=true;sc0.setAttribute("data-three-r128","1");sc0.addEventListener("load",ok);sc0.addEventListener("error",fail);document.head.appendChild(sc0);}}
})();</script></div>

Её удобно изучать и по сечениям $a=\mathrm{const}$. При $a\gt 0$ сечение — гладкая кривая, при $a=0$ у неё появляется особая точка (многочлен $x^4$), при $a\lt 0$ — два острия и самопересечение.

<div class="sim" id="sim-c15"><style>#sim-c15 .c15-ctl{display:inline-flex;align-items:center;gap:.45em;font-size:15px;color:var(--muted);white-space:nowrap}
#sim-c15 .c15-ctl i{font-family:Georgia,serif;font-size:17px;color:var(--text)}
#sim-c15 input[type=range]{accent-color:var(--accent);width:min(9em,40vw);margin:0;cursor:pointer}
#sim-c15 .c15-v{display:inline-block;min-width:3.2em;color:var(--text);font-variant-numeric:tabular-nums}
#sim-c15 .c15-dot{stroke:var(--panel);stroke-width:1.5}
@media (max-width:520px){#sim-c15 .c15-ctl{flex-basis:100%;justify-content:center}}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева сечение ласточкина хвоста — дискриминантная кривая многочленов x в четвёртой плюс a x квадрат плюс b x плюс c при фиксированном a, точку (b, c) можно перетаскивать; справа график многочлена и его вещественные корни"></svg><div class="sim-bar"><label class="c15-ctl"><i>a</i> <input type="range" min="-2.5" max="1.5" step="0.01" value="-2" aria-label="параметр a"><span class="c15-v">−2,00</span></label><button type="button">a &gt; 0</button><button type="button">a = 0</button><button type="button">a &lt; 0</button></div><div class="sim-out"></div><div class="sim-cap">Слева плоскость $(b,c)$ при фиксированном $a$ и кривая, где у $x^4+ax^2+bx+c$ кратный корень: при $a&gt;0$ она гладкая, при $a=0$ у неё особая точка, при $a&lt;0$ — два острия и самопересечение, а в закрашенном треугольнике корней четыре. Ползунок меняет $a$, точку $(b,c)$ можно перетаскивать; справа график многочлена.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c15"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),rng=root.querySelector("input"),vA=root.querySelector(".c15-v"),bs=root.querySelectorAll("button");
var A=new K.Panel(22,15,300,270,[-3,3],[-1.5,3.5]),B=new K.Panel(372,15,258,270,[-2.2,2.2],[-3,4]);
var gS=K.el("g",{},svg),gA=K.el("g",{},svg),dyn=K.el("g",{},svg),a=-2,P=[0,0.5],drag=false;
A.axes(gA,"b","c");B.axes(gA,"x","y");
function cu(t){return [-4*t*t*t-2*a*t,3*t*t*t*t+a*t*t];}
function f(x){return x*x*x*x+a*x*x+P[0]*x+P[1];}
function cub(p,q){var D=4*p*p*p+27*q*q,m,th,r=[],k,u,w;
if(Math.abs(p)<1e-9&&Math.abs(q)<1e-9){return [[0,3]];}
if(Math.abs(D)<1e-10&&p<0){u=-3*q/(2*p);r=[[u,2],[-2*u,1]];r.sort(function(x,y){return x[0]-y[0];});return r;}
if(D<0){m=2*Math.sqrt(-p/3);th=Math.acos(Math.max(-1,Math.min(1,3*q/(2*p)*Math.sqrt(-3/p))))/3;for(k=0;k<3;k++){r.push([m*Math.cos(th-2*Math.PI*k/3),1]);}r.sort(function(x,y){return x[0]-y[0];});return r;}
w=Math.sqrt(q*q/4+p*p*p/27);return [[Math.cbrt(-q/2+w)+Math.cbrt(-q/2-w),1]];}
function roots(){var cr=cub(a/2,P[0]/4),xs=[-30],res=[],i,j,lo,hi,fl,fm,md;
cr.forEach(function(e){xs.push(e[0]);if(Math.abs(f(e[0]))<1e-9){res.push([e[0],e[1]+1]);}});xs.push(30);
for(i=0;i<xs.length-1;i++){lo=xs[i];hi=xs[i+1];fl=f(lo);if(Math.abs(fl)>=1e-9&&Math.abs(f(hi))>=1e-9&&fl*f(hi)<0){for(j=0;j<90;j++){md=(lo+hi)/2;fm=f(md);if(fl*fm<=0){hi=md;}else{lo=md;fl=fm;}}res.push([(lo+hi)/2,1]);}}
res.sort(function(x,y){return x[0]-y[0];});return res;}
function sg(v){return v<-0.005?" − ":" + ";}
function say(r){var n=0,ml=r.filter(function(e){return e[1]>1;}),sm=r.length-ml.length,W=["","","двойной","тройной","четырёхкратный"],h;
r.forEach(function(e){n+=e[1];});
if(ml.length===0){return ["нет вещественных корней","","два вещественных корня","","четыре вещественных корня"][n];}
if(ml.length===2){return "два двойных корня "+K.num(ml[0][0])+" и "+K.num(ml[1][0]);}
h=W[ml[0][1]]+" корень "+K.num(ml[0][0]);
if(sm===1){return h+" и простой";}if(sm===2){return h+" и два простых";}
if(ml[0][1]===2){return h+", два других — комплексные";}return h;}
function snap(bx,cy){var best=1e9,bt=0,i,t,v,d,cand=[],s;
if(a<=0){s=Math.sqrt(-a/6);cand.push([8*s*s*s,-3*s*s*s*s],[-8*s*s*s,-3*s*s*s*s]);if(a<0){cand.push([0,a*a/4]);}}
for(i=0;i<cand.length;i++){d=Math.hypot(A.X(cand[i][0])-A.X(bx),A.Y(cand[i][1])-A.Y(cy));if(d<8){return cand[i];}}
for(i=0;i<=2400;i++){t=-2+4*i/2400;v=cu(t);d=Math.hypot(A.X(v[0])-A.X(bx),A.Y(v[1])-A.Y(cy));if(d<best){best=d;bt=t;}}
if(best<5){return cu(bt);}return [bx,cy];}
function draw(){K.clear(gS);K.clear(dyn);var cv=[],i,t,T,poly=[],gp=[],x,r=roots();
if(a<0){T=Math.sqrt(-a/2);for(i=0;i<=300;i++){t=-T+2*T*i/300;poly.push(cu(t));}K.el("polygon",{"class":"k-shade",points:poly.map(function(v){return A.X(v[0]).toFixed(1)+","+A.Y(v[1]).toFixed(1);}).join(" ")},gS);}
for(i=0;i<=1600;i++){t=-2+4*i/1600;cv.push(cu(t));}
K.el("path",{"class":"k-curve",d:A.d(cv)},dyn);
for(i=0;i<=440;i++){x=-2.2+4.4*i/440;gp.push([x,f(x)]);}
K.el("path",{"class":"k-curve",d:B.d(gp)},dyn);
r.forEach(function(e){if(e[1]>1){K.el("circle",{"class":"k-f2 c15-dot",cx:B.X(e[0]),cy:B.Y(0),r:7},dyn);}else{K.el("circle",{"class":"k-f1 c15-dot",cx:B.X(e[0]),cy:B.Y(0),r:5.5},dyn);}});
K.el("circle",{"class":"k-halo",cx:A.X(P[0]),cy:A.Y(P[1]),r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(P[0]),cy:A.Y(P[1]),r:6.5},dyn);
vA.textContent=K.num(a);
out.textContent="a = "+K.num(a)+": x⁴"+sg(a)+K.num(Math.abs(a))+"x²"+sg(P[0])+K.num(Math.abs(P[0]))+"x"+sg(P[1])+K.num(Math.abs(P[1]))+" — "+say(r);}
function setA(v){a=Math.round(v*100)/100;if(Math.abs(a)<1e-9){a=0;}rng.value=String(a);}
rng.addEventListener("input",function(){setA(parseFloat(rng.value));draw();});
[[1,[0.4,-0.5]],[0,[0.3,-0.35]],[-2,[0,0.5]]].forEach(function(e,k){bs[k].addEventListener("click",function(){setA(e[0]);P=[e[1][0],e[1][1]];draw();});});
function set(e){var s=K.pt(svg,e);P=snap(Math.max(-2.95,Math.min(2.95,A.ix(s.x))),Math.max(-1.45,Math.min(3.45,A.iy(s.y))));draw();}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+12){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

Итак, для степеней до четвёртой структуру корней — сколько их и есть ли среди них кратные — можно полностью прочитать по коэффициентам. Что можно сказать для любой степени $n$? Приведённый многочлен $x^n+a_{n-1}x^{n-1}+\dots+a_1x+a_0$ — точка пространства $\mathbb R^n$ с координатами $a_0,\dots,a_{n-1}$. Как в этом пространстве устроены множества многочленов с данным числом вещественных корней и что лежит между ними? Начнём с того, что происходит внутри такого множества.

## Корень не пропадает

Чтобы следить за простым корнем, нам понадобится производная.

**Утверждение 3 (кратный корень и производная). Статус: выверено, SKELET утв. 3.**
Корень $x_0$ многочлена $f$ кратный тогда и только тогда, когда $f'(x_0)=0$.

*Доказательство — теорема Безу.* По теореме Безу $f=(x-x_0)h$ для некоторого многочлена $h$. Тогда $f'=h+(x-x_0)h'$ и $f'(x_0)=h(x_0)$, а $f$ делится на $(x-x_0)^2$ ровно тогда, когда $h(x_0)=0$.

Геометрически в кратном корне график касается оси абсцисс, а в простом пересекает её под ненулевым углом. Возле простого корня график почти совпадает с касательной. При малом изменении коэффициентов график и касательная сдвинутся мало, поэтому пересечение с осью сохранится и останется единственным: касательная не станет горизонтальной.

<div class="sim" id="sim-c7"><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева пульт возмущения коэффициентов многочлена x в кубе минус 2x плюс 0,3, справа графики исходного и возмущённого многочлена; на отмеченном отрезке у возмущённого многочлена остаётся ровно один корень"></svg>
<div class="sim-bar"><button type="button">покачать</button><button type="button">в центр</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Слева точка $(\delta_1,\delta_0)$ задаёт возмущённый многочлен $g(x)=f(x)+\delta_1x+\delta_0$ для $f(x)=x^3-2x+0{,}3$; её можно перетаскивать; центр квадрата отвечает самому $f$. Справа тонкий график $f$, жирный — $g$; пока точка в закрашенном квадрате, на отрезке в скобках у $g$ ровно один корень, и он лишь слегка сдвигается от корня $f$ (пунктирный кружок).</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c7"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var A=new K.Panel(25,20,260,260,[-0.6,0.6],[-0.6,0.6]),B=new K.Panel(345,20,285,260,[-0.95,1.25],[-1.6,2.2]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),E=0.35,Q=0.25,X0=0.15,i,t,fp=[];
function f(x){return x*x*x-2*x+0.3;}
for(i=0;i<8;i++){X0=X0-f(X0)/(3*X0*X0-2);}
var LO=X0-E,HI=X0+E,P=[0.14,-0.12],trail=[],busy=false,drag=false;
K.el("rect",{"class":"k-shade",x:A.X(-Q),y:A.Y(Q),width:A.X(Q)-A.X(-Q),height:A.Y(-Q)-A.Y(Q)},st);
A.axes(st,"δ₁","δ₀");
t=K.el("text",{"class":"k-lab",x:A.X(Q)+6,y:A.Y(Q)+13},st);t.textContent="|δᵢ| < 0,25";
K.el("circle",{"class":"k-base",cx:A.X(0),cy:A.Y(0),r:4},st);
t=K.el("text",{"class":"k-lab",x:A.X(0)-15,y:A.Y(0)+16},st);t.textContent="f";
B.axes(st,"x","y");
for(i=0;i<=440;i++){var x=-0.95+2.2*i/440;fp.push([x,f(x)]);}
K.el("path",{"class":"k-thin",d:B.d(fp)},st);
var bx=[B.X(LO),B.X(HI)],by=B.Y(0);
K.el("line",{"class":"k-l1",x1:bx[0],y1:by,x2:bx[1],y2:by,style:"stroke-width:4;stroke-linecap:butt"},st);
K.el("path",{"class":"k-l1",d:"M"+(bx[0]+6)+","+(by-9)+" h-6 v18 h6 M"+(bx[1]-6)+","+(by-9)+" h6 v18 h-6",style:"stroke-width:2"},st);
t=K.el("text",{"class":"k-lab",x:bx[0],y:by+26,"text-anchor":"middle"},st);t.textContent="x₀−ε";
t=K.el("text",{"class":"k-lab",x:bx[1],y:by-16,"text-anchor":"middle"},st);t.textContent="x₀+ε";
function g(x){return x*x*x+(P[0]-2)*x+0.3+P[1];}
function roots(){var r=[],n=350,k,a,b,ga,gb,m,j;for(k=0;k<n;k++){a=LO+(HI-LO)*k/n;b=LO+(HI-LO)*(k+1)/n;ga=g(a);gb=g(b);if(ga===0){r.push(a);}else if(ga*gb<0){for(j=0;j<50;j++){m=(a+b)/2;if(ga*g(m)<=0){b=m;}else{a=m;ga=g(m);}}r.push((a+b)/2);}}return r;}
function draw(){K.clear(dyn);var gp=[],k,rs=roots(),sx=B.w/2.2,sy=B.h/3.8;
if(trail.length>1){K.el("path",{"class":"k-path",d:A.d(trail)},dyn);}
for(k=0;k<=440;k++){var x=-0.95+2.2*k/440;gp.push([x,g(x)]);}
K.el("path",{"class":"k-curve",d:B.d(gp)},dyn);
var xl=-0.8,up=g(xl)>=f(xl),cl=function(y){return Math.max(B.y0+12,Math.min(B.y0+B.h-4,y));};
var tf=K.el("text",{"class":"k-lab",x:B.X(xl)-4,y:cl(B.Y(f(xl))+(up?19:-9))},dyn);tf.textContent="f";
var tl=K.el("text",{"class":"k-lab",x:B.X(xl)-4,y:cl(B.Y(g(xl))+(up?-10:20)),style:"fill:var(--text)"},dyn);tl.textContent="g";
rs.forEach(function(r){var s=3*r*r-2+P[0],vx=sx,vy=-s*sy,L=Math.hypot(vx,vy),c=95/L;K.el("line",{"class":"k-l2",x1:B.X(r)-vx*c,y1:B.Y(0)-vy*c,x2:B.X(r)+vx*c,y2:B.Y(0)+vy*c,style:"stroke-width:1.6;stroke-dasharray:6 4"},dyn);});
K.el("circle",{"class":"k-ring",cx:B.X(X0),cy:B.Y(0),r:9},dyn);
rs.forEach(function(r){K.el("circle",{"class":"k-f1",cx:B.X(r),cy:B.Y(0),r:5.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(P[0]),cy:A.Y(P[1]),r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(P[0]),cy:A.Y(P[1]),r:6.5},dyn);
var hl=K.el("text",{"class":"k-lab",x:A.X(P[0])+11,y:A.Y(P[1])-10,style:"fill:var(--text)"},dyn);hl.textContent="g";
var h="на отмеченном отрезке у g ";
if(rs.length===0){h+="корней нет";}else if(rs.length===1){h+="один корень: x\u00a0≈\u00a0"+K.num(rs[0]);}else{h+=(rs.length===2?"два корня":rs.length+" корня")+": x\u00a0≈\u00a0"+rs.map(K.num).join("; ");}
out.textContent=h;}
function dis(b){busy=b;bs.forEach(function(x){x.disabled=b;});}
function sm(q){return q-Math.sin(2*Math.PI*q)/(2*Math.PI);}
bs[0].addEventListener("click",function(){if(busy){return;}dis(true);var r=Math.hypot(P[0],P[1]),a0=r>0.01?Math.atan2(P[1],P[0]):0,S=[P[0],P[1]],G=[0.2*Math.cos(a0),0.2*Math.sin(a0)],T0=null;trail=[];
function step(ts){if(T0===null){T0=ts;}var u=(ts-T0)/1000,q;if(u<0.5){q=sm(u/0.5);P=[S[0]+(G[0]-S[0])*q,S[1]+(G[1]-S[1])*q];}else{q=Math.min(1,(u-0.5)/3.2);var a=a0+2*Math.PI*sm(q);P=[0.2*Math.cos(a),0.2*Math.sin(a)];trail.push([P[0],P[1]]);}draw();if(u<3.7){requestAnimationFrame(step);}else{dis(false);}}
requestAnimationFrame(step);});
bs[1].addEventListener("click",function(){if(busy){return;}P=[0,0];trail=[];draw();});
function set(e){var s=K.pt(svg,e);P=[Math.max(-0.59,Math.min(0.59,A.ix(s.x))),Math.max(-0.59,Math.min(0.59,A.iy(s.y)))];draw();}
svg.addEventListener("pointerdown",function(e){if(busy){return;}var s=K.pt(svg,e);if(s.x<A.x0+A.w+15){drag=true;trail=[];svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

Превратим эту картинку в доказательство. Нам понадобятся три простые оценки.

**Лемма 4 (близкие коэффициенты — близкие значения). Статус: выверено, SKELET т. 9.**
Пусть $|x|\le M$ при всех $x\in I$ и каждый коэффициент многочлена $g$ степени $n$ отличается от соответствующего коэффициента $f$ меньше чем на $\delta$. Тогда при всех $x\in I$
$$|g(x)-f(x)|\le\delta K,\qquad |g'(x)-f'(x)|\le\delta K',$$
где $K=1+M+\dots+M^{n}$ и $K'=1+2M+\dots+nM^{n-1}$ зависят только от $M$ и $n$.

*Доказательство — неравенство треугольника.* Пусть $a_i$ и $b_i$ — коэффициенты $f$ и $g$ при $x^i$. Разность $g-f$ — сумма слагаемых $(b_i-a_i)x^{i}$, каждое по модулю меньше $\delta M^{i}$. Для производных так же, с множителями $i$.

**Лемма 5 (производная сохраняет знак). Статус: выверено, SKELET т. 9.**
Если $f'(x_0)\gt 0$, то найдутся числа $\varepsilon\gt 0$ и $m\gt 0$ такие, что $f'(x)\ge m$ на отрезке $[x_0-\varepsilon,\,x_0+\varepsilon]$; то же верно и для всех меньших $\varepsilon$.

*Доказательство — непрерывность.* Производная многочлена непрерывна. Возьмём $m=f'(x_0)/2$; рядом с $x_0$ производная больше $m$.

**Лемма 6 (знаки на концах отрезка). Статус: выверено, SKELET т. 9.**
Если $f(x_0)=0$ и $f'\ge m$ на $[x_0-\varepsilon,\,x_0+\varepsilon]$, то $f(x_0-\varepsilon)\le-m\varepsilon$ и $f(x_0+\varepsilon)\ge m\varepsilon$.

*Доказательство — теорема Лагранжа.* По [формуле конечных приращений](https://ru.wikipedia.org/wiki/Формула_конечных_приращений) $f(x_0+\varepsilon)-f(x_0)=f'(\xi)\,\varepsilon\ge m\varepsilon$ для некоторой точки $\xi$ между $x_0$ и $x_0+\varepsilon$. Для левого конца рассуждение такое же.

**Теорема 7 (корень не пропадает). Статус: выверено, SKELET т. 9.**
Пусть $x_0$ — простой корень вещественного многочлена $f$. Тогда для любого достаточно малого $\varepsilon\gt 0$ найдётся $\delta\gt 0$ такое, что у любого вещественного многочлена $g$ той же степени, каждый коэффициент которого отличается от соответствующего коэффициента $f$ меньше чем на $\delta$, на отрезке $[x_0-\varepsilon,\,x_0+\varepsilon]$ ровно один корень.

*Доказательство — три леммы и две теоремы анализа.* Пусть для определённости $f'(x_0)\gt 0$ (по утверждению 3 $f'(x_0)\ne0$; случай $f'(x_0)\lt 0$ такой же).
**Шаг 1.** По лемме 5 выберем $\varepsilon$ и $m$ так, что $f'\ge m$ на $I=[x_0-\varepsilon,\,x_0+\varepsilon]$. По лемме 6 $f(x_0-\varepsilon)\le-m\varepsilon$ и $f(x_0+\varepsilon)\ge m\varepsilon$.
**Шаг 2.** Для отрезка $I$ возьмём $K$ и $K'$ из леммы 4 и выберем $\delta$ так, что $\delta K\lt m\varepsilon$ и $\delta K'\lt m$.
**Шаг 3.** По лемме 4 $g(x_0-\varepsilon)\lt -m\varepsilon+m\varepsilon=0$ и $g(x_0+\varepsilon)\gt 0$, а на всём $I$ производная $g'\gt m-m=0$.
**Шаг 4 (существование).** На концах $I$ у $g$ разные знаки, поэтому по [теореме о промежуточном значении](https://ru.wikipedia.org/wiki/Теорема_о_промежуточном_значении) у $g$ есть корень на $I$.
**Шаг 5 (единственность).** На $I$ производная $g'\gt 0$, поэтому $g$ строго возрастает и второго корня на $I$ нет.

Шаг 5 и есть «касательная не становится горизонтальной». В теореме 7 мы следили за одним корнем. Чтобы следить за всеми сразу, нужно ещё убедиться, что новые корни не появятся где-то далеко.

**Лемма 8 (корни не уходят далеко). Статус: выверено, SKELET л. 10.**
Каждый корень приведённого многочлена $x^n+a_{n-1}x^{n-1}+\dots+a_1x+a_0$ удовлетворяет неравенству $|x|\le1+\max|a_i|$.

*Доказательство — сравнить старший член с остальными.* Пусть $A=\max|a_i|$ и $|x|\gt 1+A$. Тогда $|a_{n-1}x^{n-1}+\dots+a_1x+a_0|\le A\,\dfrac{|x|^n-1}{|x|-1}\lt |x|^n$, и многочлен в точке $x$ не равен нулю.

**Теорема 9 (простые корни — открытое условие). Статус: выверено, SKELET т. 11.**
Пусть у приведённого многочлена $f$ ровно $k$ вещественных корней и все они простые. Тогда найдётся $\delta\gt 0$ такое, что у любого приведённого $g$ той же степени с коэффициентами, отличающимися от коэффициентов $f$ меньше чем на $\delta$, тоже ровно $k$ вещественных корней, все простые, и каждый лежит рядом со своим корнем $f$.

*Доказательство — корни не пропадают и не появляются.* **Шаг 1.** Вокруг каждого корня $f$ возьмём отрезок из теоремы 7, причём настолько короткий, что отрезки не пересекаются. **Шаг 2.** Все корни всех близких $g$ лежат на отрезке $[-R,R]$ с $R=2+\max|a_i|$ (лемма 8; считаем $\delta\le1$). **Шаг 3.** Множество $L$ — отрезок $[-R,R]$ без внутренностей маленьких отрезков — замкнуто и ограничено, а $f$ на нём не обращается в ноль. По [теореме Вейерштрасса](https://ru.wikipedia.org/wiki/Теорема_Вейерштрасса_о_функции_на_компакте) $|f|\ge\mu\gt 0$ на $L$. По лемме 4 при малом $\delta$ на $L$ выполнено $|g-f|\lt\mu$, и $g$ там не обращается в ноль. **Шаг 4.** Значит, корни $g$ есть только на маленьких отрезках, и по теореме 7 на каждом ровно один, причём простой (там $g'\ne0$).

Иначе говоря, многочлены, у которых ровно $k$ вещественных корней и все они простые, образуют открытое множество: вместе с каждой своей точкой оно содержит маленький шар вокруг неё.

## Пока не задеваем кратных корней

Пусть теперь точка $f_s$ движется по непрерывному пути, $s\in[0,1]$, и ни у одного $f_s$ нет кратных вещественных корней.

**Теорема 10 (корни вдоль пути). Статус: выверено, SKELET т. 11.**
Если непрерывный путь $f_s$, $s\in[0,1]$, в пространстве приведённых многочленов степени $n$ не проходит через многочлены с кратным вещественным корнем, то число вещественных корней $f_s$ одно и то же при всех $s$, а сами корни непрерывно зависят от $s$.

*Доказательство — покрыть путь интервалами.* **Шаг 1.** По теореме 9 каждая точка $s_0$ лежит в интервале, где число корней $f_s$ постоянно, а каждый корень остаётся рядом со «своим»; так как отрезки в теореме 7 можно брать сколь угодно короткими, корни непрерывно зависят от $s$. **Шаг 2.** Эти интервалы покрывают отрезок $[0,1]$. По [лемме Гейне — Бореля](https://ru.wikipedia.org/wiki/Лемма_Гейне_—_Бореля) из покрытия можно выбрать конечное подпокрытие. Соседние интервалы перекрываются, поэтому число корней одно и то же на всём пути.

<div class="sim" id="sim-c8"><svg viewBox="0 0 650 295" role="img" aria-label="Интерактив: коэффициенты многочлена пятой степени меняются вдоль пути, справа его график и три вещественных корня, которые ни разу не сталкиваются; внизу следы корней"></svg>
<div class="sim-bar"><label style="display:inline-flex;align-items:center;gap:.5em">s <input type="range" min="0" max="1" step="0.001" value="0" aria-label="параметр пути s" style="width:min(240px,52vw);accent-color:var(--accent)"></label><button type="button">пройти путь</button></div>
<div class="sim-out"></div>
<div class="sim-cap">Слева коэффициенты $f_s(x)=x^5+a_4x^4+a_3x^3+a_2x^2+a_1x+a_0$ вдоль пути $f_s=(1-s)f_0+sf_1+\sin(\pi s)\,(x^3-x)$; $s$ меняется ползунком или кнопкой. Справа график $f_s$ и его три вещественных корня, внизу их следы ($s$ растёт сверху вниз): следы не пересекаются, корни ни разу не сливаются.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c8"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),btn=root.querySelector("button"),rng=root.querySelector("input");
var A=new K.Panel(45,20,245,240,[0,5],[-3,3]),B=new K.Panel(350,15,280,180,[-1.8,1.8],[-2.5,2.5]),T=new K.Panel(350,222,280,62,[-1.8,1.8],[0,1]);
var F0=[-0.8,-2.2,2.5,0.6,-0.5],F1=[0.8,-2.2,-2.5,0.6,0.5],H=[0,1,0,-1,0],N=1000,R=[],C=[],i,t,k;
function co(s){var w=Math.sin(Math.PI*s);return F0.map(function(v,j){return (1-s)*v+s*F1[j]+w*H[j];});}
function cz(a){return [[1,0]].concat(a.map(function(v){return [v,0];}));}
var z=K.dk(cz(co(0)),[[-1.5,0],[-0.49,0],[0.41,0],[1.19,0.48],[1.19,-0.48]],40);
for(i=0;i<=N;i++){z=K.dk(cz(co(i/N)),z,8);var w=z.slice().sort(function(p,q){return Math.abs(p[1])-Math.abs(q[1]);});C.push(w.filter(function(p){return Math.abs(p[1])<1e-6;}).length);R.push(w.slice(0,3).map(function(p){return p[0];}).sort(function(p,q){return p-q;}));}
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),j=0,busy=false,NM=["нет вещественных корней","один вещественный корень","два вещественных корня","три вещественных корня","четыре вещественных корня","пять вещественных корней"],SB=["₄","₃","₂","₁","₀"];
[-2,-1,1,2].forEach(function(v){K.el("line",{"class":"k-thin",x1:A.x0,y1:A.Y(v),x2:A.x0+A.w,y2:A.Y(v),style:"stroke-dasharray:2 4"},st);});
[-2,-1,0,1,2].forEach(function(v){var u=K.el("text",{"class":"k-lab",x:A.x0-8,y:A.Y(v)+4,"text-anchor":"end"},st);u.textContent=v<0?"−"+(-v):String(v);});
K.el("line",{"class":"k-ax",x1:A.x0,y1:A.Y(0),x2:A.x0+A.w,y2:A.Y(0)},st);
for(k=0;k<5;k++){t=K.el("text",{"class":"k-lab",x:A.X(k+0.5),y:A.y0+A.h+20,"text-anchor":"middle",style:"font-size:15px;fill:var(--text)"},st);t.textContent="a"+SB[k];}
B.axes(st,"x","y");
K.el("rect",{"class":"k-shade",x:T.x0,y:T.y0,width:T.w,height:T.h,rx:4,style:"opacity:.55"},st);
K.el("line",{"class":"k-thin",x1:T.X(0),y1:T.y0,x2:T.X(0),y2:T.y0+T.h,style:"stroke-dasharray:2 4"},st);
t=K.el("text",{"class":"k-lab",x:T.x0-6,y:T.y0+10,"text-anchor":"end"},st);t.textContent="s = 0";
t=K.el("text",{"class":"k-lab",x:T.x0-6,y:T.y0+T.h,"text-anchor":"end"},st);t.textContent="1";
function ev(a,x){var r=1;a.forEach(function(v){r=r*x+v;});return r;}
function draw(){K.clear(dyn);var s=j/N,a=co(s),gp=[],m,x,cur=R[j];
a.forEach(function(v,n){var y0=A.Y(0),y1=A.Y(v),cx=A.X(n+0.5);K.el("rect",{"class":"k-f1",x:cx-14,y:Math.min(y0,y1),width:28,height:Math.max(1,Math.abs(y1-y0)),rx:2,style:"opacity:.85"},dyn);var u=K.el("text",{"class":"k-lab",x:cx,y:v>=0?y1-6:y1+15,"text-anchor":"middle",style:"paint-order:stroke;stroke:var(--panel);stroke-width:4px;stroke-linejoin:round"},dyn);u.textContent=K.num(v);});
for(m=0;m<=360;m++){x=-1.8+3.6*m/360;gp.push([x,ev(a,x)]);}
K.el("path",{"class":"k-curve",d:B.d(gp)},dyn);
K.el("line",{"class":"k-thin",x1:T.x0,y1:T.Y(1-s),x2:T.x0+T.w,y2:T.Y(1-s)},dyn);
[0,1,2].forEach(function(n){var tr=[];for(m=0;m<=j;m++){tr.push([R[m][n],1-m/N]);}if(tr.length>1){K.el("path",{"class":"k-t"+(n+1),d:T.d(tr),style:"stroke-width:2;opacity:.8"},dyn);}K.el("circle",{"class":"k-k"+(n+1),cx:T.X(cur[n]),cy:T.Y(1-s),r:3.5},dyn);K.el("line",{"class":"k-thin",x1:B.X(cur[n]),y1:B.Y(0)+7,x2:T.X(cur[n]),y2:T.Y(1-s)-4,style:"stroke-dasharray:2 3"},dyn);});
[0,1,2].forEach(function(n){K.el("circle",{"class":"k-k"+(n+1),cx:B.X(cur[n]),cy:B.Y(0),r:6},dyn);});
out.textContent="s = "+K.num(s)+": "+NM[C[j]]+", "+cur.map(K.num).join("; ");}
rng.addEventListener("input",function(){busy=false;btn.disabled=false;j=Math.round(Number(rng.value)*N);draw();});
btn.addEventListener("click",function(){if(busy){return;}busy=true;btn.disabled=true;var T0=null;
function step(ts){if(!busy){return;}if(T0===null){T0=ts;}var u=Math.min(1,(ts-T0)/4000);j=Math.round(u*N);rng.value=String(j/N);draw();if(u<1){requestAnimationFrame(step);}else{busy=false;btn.disabled=false;}}
requestAnimationFrame(step);});
draw();
})();</script></div>

## Дискриминант и касательные

Теперь посмотрим на то, что лежит между областями: на многочлены с кратным вещественным корнем. Их множество называют дискриминантным множеством или просто дискриминантом: у квадратных трёхчленов это парабола, у кубических — полукубическая парабола, у многочленов четвёртой степени — ласточкин хвост. Каждой его точке отвечает свой кратный корень; начнём с параболы.

Какие трёхчлены имеют корень $t$? Подставим $x=t$: $t^2+pt+q=0$. Это линейное уравнение на $p$ и $q$, поэтому такие трёхчлены образуют прямую. Обозначим её $L_t$.

**Утверждение 11 (прямые $L_t$ касаются дискриминанта). Статус: выверено, SKELET утв. 5.**
При любом $t$ прямая $L_t\colon q=-tp-t^2$ касается параболы $q=p^2/4$ в точке $(-2t,\,t^2)$, то есть в трёхчлене $(x-t)^2$.

*Доказательство — выделить полный квадрат.* На прямой $L_t$
$$p^2-4q=p^2+4tp+4t^2=(p+2t)^2.$$
Это выражение неотрицательно и обращается в ноль только при $p=-2t$. Значит, прямая имеет с параболой одну общую точку и нигде не заходит выше неё, то есть касается её.

По определению точка $(p,q)$ лежит на $L_t$ ровно тогда, когда $t$ — корень трёхчлена $x^2+px+q$. Поэтому корней у трёхчлена столько, сколько касательных к параболе проходит через его точку: из точки под параболой — две, из точки над ней — ни одной. Сам корень читается по наклону касательной: наклон $L_t$ равен $-t$.

<div class="sim" id="sim-c1"><svg viewBox="0 0 650 275" role="img" aria-label="Интерактив: плоскость коэффициентов квадратного трёхчлена с параболой-дискриминантом и график трёхчлена; точку можно перетаскивать"></svg><div class="sim-out"></div><div class="sim-cap">Точку на плоскости $(p,q)$ можно перетаскивать. Из точки под параболой проходят две касательные; их наклоны со знаком минус — корни трёхчлена, отмеченные на графике справа тем же цветом. Над параболой касательных нет, и корней нет.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c1"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out");
var A=new K.Panel(20,15,300,240,[-3,3],[-1.7,2.7]),B=new K.Panel(370,15,260,240,[-2.6,2.6],[-1.7,2.7]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),i,ps=[],up=[];
for(i=0;i<=200;i++){var p=-3+6*i/200;ps.push([p,p*p/4]);}
up=ps.map(function(v){return A.X(v[0]).toFixed(1)+","+A.Y(Math.min(v[1],2.7)).toFixed(1);});
K.el("polygon",{"class":"k-shade",points:up.join(" ")+" "+A.X(3)+","+A.Y(2.7)+" "+A.X(-3)+","+A.Y(2.7)},st);
A.axes(st,"p","q");B.axes(st,"x","y");
K.el("path",{"class":"k-curve",d:A.d(ps)},st);
var P=[0.5,-0.75],drag=false;
function draw(){K.clear(dyn);var p=P[0],q=P[1],D=p*p-4*q,r=[];
if(D>1e-4){r=[(-p+Math.sqrt(D))/2,(-p-Math.sqrt(D))/2];}else if(D>-1e-4){r=[-p/2];}
var gr=[],x;for(x=-2.6;x<=2.6;x+=0.02){gr.push([x,x*x+p*x+q]);}
K.el("path",{"class":"k-curve",d:B.d(gr)},dyn);
r.forEach(function(t,k){var cl=k?"2":"1",ln=[[-3,3*t-t*t],[3,-3*t-t*t]],j,pts=[];for(j=0;j<=60;j++){var pp=-3+6*j/60;pts.push([pp,-t*pp-t*t]);}
K.el("path",{"class":"k-l"+cl,d:A.d(pts)},dyn);K.el("circle",{"class":"k-f"+cl,cx:A.X(-2*t),cy:A.Y(t*t),r:4},dyn);K.el("circle",{"class":"k-f"+cl,cx:B.X(t),cy:B.Y(0),r:5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(p),cy:A.Y(q),r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(p),cy:A.Y(q),r:6.5},dyn);
var f="x² "+(p<0?"− ":"+ ")+K.num(Math.abs(p))+"x "+(q<0?"− ":"+ ")+K.num(Math.abs(q));
out.textContent=f+(r.length===2?": два корня, "+K.num(r[1])+" и "+K.num(r[0]):(r.length===1?": кратный корень "+K.num(r[0]):": вещественных корней нет"));}
function set(e){var s=K.pt(svg,e);P=[Math.max(-2.9,Math.min(2.9,A.ix(s.x))),Math.max(-1.6,Math.min(2.6,A.iy(s.y)))];draw();}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

У кубических многочленов $x^3+px+q$ прямые $L_t\colon t^3+pt+q=0$ снова касаются дискриминантной кривой — полукубической параболы, и снова корней столько, сколько касательных проходит через точку.

<div class="sim" id="sim-c11"><style>#sim-c11 .k-l3{fill:none;stroke:var(--defn);stroke-width:2.2}
#sim-c11 .k-f3{fill:var(--defn)}
#sim-c11 .c11-tp{stroke:var(--panel);stroke-width:1.5}
#sim-c11 .c11-zone{font-family:var(--sans);font-size:13px;fill:var(--muted);font-style:italic}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: плоскость коэффициентов кубического многочлена x в кубе плюс p x плюс q с полукубической параболой-дискриминантом и график многочлена; точку можно перетаскивать"></svg><div class="sim-out"></div><div class="sim-cap">Точку можно перетаскивать. Корней столько, сколько касательных к кривой проходит через точку; наклон касательной равен корню со знаком минус.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c11"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out");
var A=new K.Panel(20,15,300,270,[-5.6,1.6],[-5,5]),B=new K.Panel(370,15,260,270,[-2.8,2.8],[-4,4]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),i,cv=[];
for(i=0;i<=240;i++){var t=-1.3572+2.7144*i/240;cv.push([-3*t*t,2*t*t*t]);}
K.el("polygon",{"class":"k-shade",points:cv.map(function(v){return A.X(v[0]).toFixed(1)+","+A.Y(v[1]).toFixed(1);}).join(" ")+" "+A.X(-5.6)+","+A.Y(5)+" "+A.X(-5.6)+","+A.Y(-5)},st);
A.axes(st,"p","q");B.axes(st,"x","y");
K.el("path",{"class":"k-curve",d:A.d(cv)},st);
var z1=K.el("text",{"class":"c11-zone",x:A.X(-5.45),y:A.Y(-0.42)},st);z1.textContent="три корня";
var z2=K.el("text",{"class":"c11-zone",x:A.X(0.12),y:A.Y(-4.55)},st);z2.textContent="один корень";
var P=[-1.5,0.3],drag=false;
function roots(p,q){var D=4*p*p*p+27*q*q,m,th,r=[],k,s;
if(D<-1e-3){m=2*Math.sqrt(-p/3);th=Math.acos(Math.max(-1,Math.min(1,3*q/(2*p)*Math.sqrt(-3/p))))/3;for(k=0;k<3;k++){r.push(m*Math.cos(th-2*Math.PI*k/3));}r.sort(function(a,b){return a-b;});return [[r[0],1],[r[1],2],[r[2],3]];}
if(D>1e-3){var a=-q/2,b=Math.sqrt(q*q/4+p*p*p/27);return [[Math.cbrt(a+b)+Math.cbrt(a-b),q>0?1:3]];}
if(Math.abs(p)<1e-3){return [[0,2]];}
s=-3*q/(2*p);return [[-2*s,q>0?1:3],[s,2]];}
function chip(v,c){return '<span class="sim-chip"><span class="sim-dot k-d'+c+'"></span>'+K.num(v)+'</span>';}
function draw(){K.clear(dyn);var p=P[0],q=P[1],r=roots(p,q),gr=[],x;
for(x=-2.8;x<=2.801;x+=0.01){gr.push([x,x*x*x+p*x+q]);}
K.el("path",{"class":"k-curve",d:B.d(gr)},dyn);
r.forEach(function(e){var t=e[0],c=e[1],j,pts=[];for(j=0;j<=300;j++){var pp=-5.6+7.2*j/300;pts.push([pp,-t*pp-t*t*t]);}K.el("path",{"class":"k-l"+c,d:A.d(pts)},dyn);});
r.forEach(function(e){var t=e[0],c=e[1];if(A.inside(-3*t*t,2*t*t*t)){K.el("circle",{"class":"k-f"+c+" c11-tp",cx:A.X(-3*t*t),cy:A.Y(2*t*t*t),r:5},dyn);}K.el("circle",{"class":"k-f"+c,cx:B.X(t),cy:B.Y(0),r:5.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(p),cy:A.Y(q),r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(p),cy:A.Y(q),r:6.5},dyn);
var f="x³ "+(p<0?"− ":"+ ")+K.num(Math.abs(p))+"x "+(q<0?"− ":"+ ")+K.num(Math.abs(q)),h;
if(r.length===3){h=": три корня "+chip(r[0][0],1)+chip(r[1][0],2)+chip(r[2][0],3);}else if(r.length===2){h=": кратный корень "+chip(r[1][0],2)+" и простой "+chip(r[0][0],r[0][1]);}else if(r[0][1]===2){h=": тройной корень "+chip(0,2);}else{h=": один корень "+chip(r[0][0],r[0][1]);}
out.innerHTML=f+h;}
function set(e){var s=K.pt(svg,e);P=[Math.max(-5.4,Math.min(1.5,A.ix(s.x))),Math.max(-4.8,Math.min(4.8,A.iy(s.y)))];draw();}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

Через дискриминант не пройти так, как в теореме 10: в типичной его точке два вещественных корня сливаются и исчезают или, наоборот, рождаются. В вещественном мире дискриминант — стена: внутри каждой области число корней постоянно, а при переходе через стену оно меняется на два.

Что из этого обобщается? Утверждение теоремы 7 и рассуждение теорем 9 и 10 переносятся на многочлены с комплексными коэффициентами и комплексные корни. Не переносится доказательство теоремы 7: у комплексного числа знака нет. И пропадает стена.

<div class="chast">Часть II · комплексный мир</div>

## Дискриминант можно обойти

Приведённый многочлен $x^n+a_{n-1}x^{n-1}+\dots+a_1x+a_0$ с комплексными коэффициентами — точка пространства $\mathbb C^n$. Каждая комплексная координата — это две вещественные, поэтому $\mathbb C^n$ можно считать вещественным пространством $\mathbb R^{2n}$.

Дискриминантное множество в этом мире задаётся уравнением на коэффициенты. Нам нужно описание, которое не опирается на корни: мы ещё не знаем, что они у каждого многочлена есть, и иначе доказательство основной теоремы алгебры ниже пошло бы по кругу.

**Определение 12 (результант и дискриминант). Статус: выверено, SKELET опр. 14, 15.**
Для многочленов $f$ и $g$ заданных степеней существует многочлен $R(f,g)$ от их коэффициентов, который обращается в ноль тогда и только тогда, когда у $f$ и $g$ есть общий делитель положительной степени. Он называется [результантом](https://ru.wikipedia.org/wiki/Результант). Дискриминант многочлена $f$ — это $D(f)=R(f,f')$, многочлен от коэффициентов $f$.

> поле:mn Существование результанта мы принимаем без доказательства. Это определитель матрицы Сильвестра, составленной из коэффициентов $f$ и $g$; что он обращается в ноль ровно тогда, когда есть общий делитель, доказывается линейной алгеброй и не использует существования корней. Например, для $x^2+px+q$ и его производной $R=4q-p^2$, то есть дискриминант $p^2-4q$ с точностью до знака.

Если $D(f)\ne0$, то у $f$ нет кратных корней: кратный корень был бы общим корнем $f$ и $f'$. Многочлены с $D(f)=0$ образуют дискриминантное множество $\Delta$. Одно комплексное уравнение — это два вещественных, поэтому $\Delta$ «на две размерности меньше» всего пространства, как точка на плоскости или прямая в $\mathbb R^3$. А точку на плоскости можно обойти.

**Теорема 13 (обход дискриминанта). Статус: выверено, SKELET т. 16.**
Любые два приведённых многочлена $f,g\notin\Delta$ степени $n$ можно соединить непрерывным путём в $\mathbb C^n$, который не задевает $\Delta$.

*Доказательство — комплексная прямая через две точки.* Рассмотрим многочлены $h_s=(1-s)f+sg$, где $s$ — любое комплексное число; все они приведены, так как $(1-s)+s=1$. Функция
$$s\mapsto D\big((1-s)f+sg\big)$$
— многочлен от одной переменной $s$, и он не равен нулю тождественно, потому что при $s=0$ равен $D(f)\ne0$. Значит, у него конечное число корней: каждый корень $s_i$ отщепляет множитель $s-s_i$, и корней не больше степени. На плоскости $s$ пройдём от $0$ к $1$ по отрезку, обходя лежащие на нём корни $s_i$ по маленьким полуокружностям. Соответствующий путь $h_s$ не задевает $\Delta$.

<div class="sim" id="sim-c16"><style>#sim-c16 .c16-seg{stroke:var(--muted);stroke-dasharray:3 4}
#sim-c16 .c16-path{stroke-width:3;stroke-linejoin:round;stroke-linecap:round}
#sim-c16 .c16-arr{fill:var(--accent)}
#sim-c16 .c16-x{stroke:var(--warm);stroke-width:2.6}
#sim-c16 .c16-hit{fill:transparent;cursor:grab}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: плоскость параметра s с точками 0 и 1, крестиками — плохими значениями s — и путём из 0 в 1, который обходит крестики маленькими полуокружностями; крестики можно перетаскивать"></svg><div class="sim-bar"><button type="button">бросить на отрезок</button><button type="button">заново</button></div><div class="sim-out"></div><div class="sim-cap">Крестики — значения $s$, при которых многочлен $(1-s)f+sg$ попадает в дискриминант; их конечное число, и путь из $0$ в $1$ всегда можно провести в обход. Крестики можно перетаскивать.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c16"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var S=new K.Panel(25,10,600,280,[0.5-0.4*600/280,0.5+0.4*600/280],[-0.4,0.4]);
var R0=0.06,M=0.035,X0=[[0.55,0],[0.2,0.25],[0.84,-0.24],[1.22,0.14]],X=X0.map(function(p){return [p[0],p[1]];}),sel=-1,st=K.el("g",{},svg),dyn=K.el("g",{},svg);
K.el("line",{"class":"k-thin",x1:S.x0,y1:S.Y(0),x2:S.x0+S.w,y2:S.Y(0)},st);
K.el("line",{"class":"k-thin c16-seg",x1:S.X(0),y1:S.Y(0),x2:S.X(1),y2:S.Y(0)},st);
function lab(x,y,s,an){var e=K.el("text",{"class":"k-lab",x:x,y:y,"text-anchor":an||"start"},st);e.textContent=s;}
lab(S.X(0),S.Y(0)+22,"0","middle");lab(S.X(1),S.Y(0)+22,"1","middle");lab(S.x0+4,S.y0+16,"s");
function near(p){return Math.abs(p[1])<R0&&p[0]>0&&p[0]<1;}
function dArc(p,c,r,sd){if(sd*p[1]>=0){return Math.abs(Math.hypot(p[0]-c,p[1])-r);}return Math.min(Math.hypot(p[0]-c+r,p[1]),Math.hypot(p[0]-c-r,p[1]));}
function plan(){var cl=X.filter(near).map(function(p){return {L:p[0]-R0,R:p[0]+R0};}),it,mg,ch,res;
for(it=0;it<40;it++){cl.sort(function(u,v){return u.L-v.L;});mg=[];cl.forEach(function(q){var l=mg[mg.length-1];if(l&&q.L<=l.R){l.R=Math.max(l.R,q.R);}else{mg.push({L:q.L,R:q.R});}});cl=mg;ch=false;
cl.forEach(function(q){var c=(q.L+q.R)/2,r=(q.R-q.L)/2,nu=0,nd=0;X.forEach(function(p){if(Math.hypot(p[0]-c,p[1])<r+M){if(p[1]>1e-9){nu++;}if(p[1]<-1e-9){nd++;}}});q.sd=nu>nd?-1:1;
X.forEach(function(p){var d;if(dArc(p,c,r,q.sd)<M){d=Math.hypot(p[0]-c,p[1])+M;if(d>r){r=d;ch=true;}}});q.L=c-r;q.R=c+r;});
if(!ch){break;}}
cl.forEach(function(q){if(q.L<0.004){q.L=0.004;}if(q.R>0.996){q.R=0.996;}});
res=[[0,0]];cl.forEach(function(q){var c=(q.L+q.R)/2,r=(q.R-q.L)/2,j,th;res.push([q.L,0]);for(j=1;j<=60;j++){th=Math.PI*(1-j/60);res.push([c+r*Math.cos(th),q.sd*r*Math.sin(th)]);}});res.push([1,0]);return res;}
function arrow(pts){var L=0,i,acc=0,tot,p,q,sl=0,u,dx,dy,n,x,y;for(i=1;i<pts.length;i++){L+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);}tot=0.93*L;
for(i=1;i<pts.length;i++){p=pts[i-1];q=pts[i];sl=Math.hypot(q[0]-p[0],q[1]-p[1]);if(acc+sl>=tot){break;}acc+=sl;}
u=sl>0?(tot-acc)/sl:0;x=S.X(p[0]+(q[0]-p[0])*u);y=S.Y(p[1]+(q[1]-p[1])*u);dx=S.X(q[0])-S.X(p[0]);dy=S.Y(q[1])-S.Y(p[1]);n=Math.hypot(dx,dy)||1;dx/=n;dy/=n;
K.el("path",{"class":"c16-arr",d:"M"+(x+dx*8).toFixed(1)+","+(y+dy*8).toFixed(1)+" L"+(x-dx*6-dy*6).toFixed(1)+","+(y-dy*6+dx*6).toFixed(1)+" L"+(x-dx*6+dy*6).toFixed(1)+","+(y-dy*6-dx*6).toFixed(1)+" z"},dyn);}
function draw(){K.clear(dyn);var pts=plan(),n=X.filter(near).length;
K.el("path",{"class":"k-l1 c16-path",d:S.d(pts)},dyn);arrow(pts);
[0,1].forEach(function(v){K.el("circle",{"class":"k-base",cx:S.X(v),cy:S.Y(0),r:5},dyn);});
X.forEach(function(p,k){var x=S.X(p[0]),y=S.Y(p[1]);if(k===sel){K.el("circle",{"class":"k-halo",cx:x,cy:y,r:16},dyn);}K.el("circle",{"class":"c16-hit",cx:x,cy:y,r:14},dyn);K.el("path",{"class":"k-x c16-x",d:"M"+(x-6)+","+(y-6)+" l12,12 M"+(x-6)+","+(y+6)+" l12,-12"},dyn);});
if(n===0){out.textContent="на отрезке нет плохих точек — путь идёт прямо";}else if(n===1){out.textContent="на отрезке 1 плохая точка — путь её обходит";}else{out.textContent="на отрезке "+n+" плохие точки — путь их обходит";}}
function clamp(p){var x=Math.max(S.xr[0]+0.03,Math.min(S.xr[1]-0.03,p[0])),y=Math.max(-0.37,Math.min(0.37,p[1]));[0,1].forEach(function(b){var d=Math.hypot(x-b,y);if(d<0.1){if(d<1e-9){y=0.1;}else{x=b+(x-b)*0.1/d;y=y*0.1/d;}}});return [x,y];}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e),bd=24;sel=-1;X.forEach(function(p,k){var d=Math.hypot(S.X(p[0])-s.x,S.Y(p[1])-s.y);if(d<bd){bd=d;sel=k;}});if(sel>=0){svg.setPointerCapture(e.pointerId);draw();}});
svg.addEventListener("pointermove",function(e){if(sel<0){return;}var s=K.pt(svg,e);X[sel]=clamp([S.ix(s.x),S.iy(s.y)]);draw();});
svg.addEventListener("pointerup",function(){sel=-1;draw();});
bs[0].addEventListener("click",function(){var v=[],x,k,ok,tries=0;while(v.length<X.length&&tries<1000){tries++;x=0.15+0.7*Math.random();ok=true;for(k=0;k<v.length;k++){if(Math.abs(v[k]-x)<0.05){ok=false;}}if(ok){v.push(x);}}X=v.map(function(x){return [x,0];});draw();});
bs[1].addEventListener("click",function(){X=X0.map(function(p){return [p[0],p[1]];});draw();});
draw();
})();</script></div>

## Сколько корней у многочлена

Прежде чем переставлять корни, нужно знать, что они есть и что их всегда $n$. Для этого повторим вещественное рассуждение. Сначала нужен комплексный вариант теоремы 7.

**Теорема 14 (комплексный корень не пропадает). Статус: выверено, SKELET т. 17.**
Пусть $z_0$ — простой корень многочлена $f$ с комплексными коэффициентами. Тогда для любого достаточно малого $r\gt 0$ найдётся $\delta\gt 0$ такое, что у любого многочлена $g$ той же степени, каждый коэффициент которого отличается от соответствующего коэффициента $f$ меньше чем на $\delta$, в круге $|z-z_0|\lt r$ ровно один корень.

<details class="d-proof"><summary>доказательство — число оборотов</summary><div class="proof"><p>Знаков у комплексных чисел нет, поэтому вместо смены знака следим, сколько раз точка $g(z)$ обходит ноль, когда $z$ обходит окружность.</p><p><b>Шаг 1 (число оборотов).</b> Если замкнутая кривая на плоскости не проходит через ноль, у неё есть <a href="https://en.wikipedia.org/wiki/Winding_number">число оборотов</a> вокруг нуля: сколько раз она его обходит против часовой стрелки, за вычетом обходов по часовой. Если кривую непрерывно деформировать, не проводя её через ноль, число оборотов не меняется: это целое число, а меняться может только непрерывно.</p><p><b>Шаг 2 (собака на поводке).</b> Если две кривые $w_1(t)$ и $w_2(t)$ таковы, что всегда $|w_2(t)-w_1(t)|\lt |w_1(t)|$, то они обходят ноль одинаковое число раз: отрезок между $w_1(t)$ и $w_2(t)$ не проходит через ноль, и одну кривую можно продеформировать в другую по этим отрезкам. Хозяин обходит столб, собака на коротком поводке обходит его столько же раз.</p><p><b>Шаг 3 (вокруг простого корня — один оборот).</b> Возле $z_0$ имеем $f(z)=f'(z_0)(z-z_0)+(z-z_0)^2u(z)$. На маленькой окружности $|z-z_0|=r$ второе слагаемое по модулю меньше первого, поэтому по шагу 2 образ окружности обходит ноль столько же раз, сколько $f'(z_0)(z-z_0)$, то есть один раз.</p><p><b>Шаг 4 (меняем коэффициенты).</b> На этой окружности $|f|\ge\mu\gt 0$. По лемме 4 при малом $\delta$ выполнено $|g-f|\lt\mu\le|f|$, и по шагу 2 образ окружности под действием $g$ тоже обходит ноль один раз.</p><p><b>Шаг 5 (есть корень).</b> Если бы у $g$ не было корня в круге, окружность можно было бы стянуть в точку, не проходя через корни; число оборотов не изменилось бы (шаг 1), а образ крошечной окружности вокруг точки, где $g\ne0$, ноль не обходит. Противоречие.</p><p><b>Шаг 6 (корень один).</b> Для многочлена $g(z)-g(w)=(z-w)\,Q(z,w)$, где $Q$ — многочлен от $z,w$ и $Q(z,z)=g'(z)$. В маленьком круге и при малом $\delta$ число $Q$ близко к $f'(z_0)\ne0$, поэтому из $g(z)=g(w)=0$ следует $z=w$.</p><div class="sim" id="sim-c9"><style>#sim-c9 .c9-ctl{display:inline-flex;align-items:center;gap:.45em;font-size:15px;color:var(--muted);white-space:nowrap}
#sim-c9 input[type=range]{accent-color:var(--accent);width:8.5em;margin:0;cursor:pointer}
#sim-c9 .c9-v{display:inline-block;min-width:3.2em;color:var(--text);font-variant-numeric:tabular-nums}
#sim-c9 .c9-arr{fill:var(--text)}
#sim-c9 .c9-arg{fill:var(--accent)}
#sim-c9 .c9-cnt{font-family:var(--sans);font-size:17px;fill:var(--text)}
#sim-c9 .c9-in{stroke:var(--panel);stroke-width:1.5}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева плоскость z с корнями многочлена и окружностью, справа образ окружности под действием многочлена и число его оборотов вокруг нуля"></svg><div class="sim-bar"><label class="c9-ctl">радиус <input class="c9-r" type="range" min="0.1" max="2" step="0.01" value="0.6"><span class="c9-v c9-rv">0,60</span></label><label class="c9-ctl">шевелить коэффициент <input class="c9-d" type="range" min="-0.5" max="0.5" step="0.01" value="0"><span class="c9-v c9-dv">0,00</span></label></div><div class="sim-out"></div><div class="sim-cap">Слева корни многочлена $f(z)=z^3-z+0{,}4+\delta$ и окружность, её центр можно перетаскивать; справа кривая, которую пробегает $f(z)$, когда $z$ обходит окружность. Число её оборотов вокруг нуля равно числу корней внутри окружности и не меняется, пока окружность не проходит через корень.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c9"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inR=root.querySelector(".c9-r"),inD=root.querySelector(".c9-d"),vR=root.querySelector(".c9-rv"),vD=root.querySelector(".c9-dv");
var A=new K.Panel(15,15,297,270,[-2.2,2.2],[-2,2]),B=new K.Panel(360,15,270,270,[-1.12,1.12],[-1.12,1.12]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),N=400;
A.axes(st,"","");B.axes(st,"","");
var l1=K.el("text",{"class":"k-lab",x:A.x0+4,y:A.y0+12},st);l1.textContent="z";
var l2=K.el("text",{"class":"k-lab",x:B.x0+B.w-56,y:B.y0+12},st);l2.textContent="w = f(z)";
var l3=K.el("text",{"class":"k-lab",x:B.X(0)+7,y:B.Y(0)+17},st);l3.textContent="0";
var C=[0.5,0.1],rad=0.6,dl=0,Z=[[0.4,0.9],[-0.65,0.72],[0.2,-0.9]],drag=false;
function co(){return [[1,0],[0,0],[-1,0],[0.4+dl,0]];}
function plural(n,a,b,c){var m=n%10,h=n%100;if(m===1&&h!==11){return a;}if(m>=2&&m<=4&&(h<10||h>=20)){return b;}return c;}
function arrow(g,x,y,dx,dy,cl){var L=Math.hypot(dx,dy)||1,ux=dx/L,uy=dy/L,s=7;K.el("path",{"class":cl,d:"M"+(x+ux*s).toFixed(1)+","+(y+uy*s).toFixed(1)+" L"+(x-ux*s-uy*s*0.6).toFixed(1)+","+(y-uy*s+ux*s*0.6).toFixed(1)+" L"+(x-ux*s+uy*s*0.6).toFixed(1)+","+(y-uy*s-ux*s*0.6).toFixed(1)+" z"},g);}
function draw(){K.clear(dyn);var c=co(),j,zs=[],ws=[],ls=0,ang=0,mn=1e9;
Z=K.dk(c,Z.map(function(r,k){return [r[0],r[1]+0.002*(k-1)];}),80);if(Z.some(function(r){var v=K.ev(c,r);return !(Math.hypot(v[0],v[1])<1e-6);})){Z=K.dk(c,[[0.4,0.9],[-0.65,0.72],[0.2,-0.9]],300);}
for(j=0;j<=N;j++){var th=2*Math.PI*j/N,z=[C[0]+rad*Math.cos(th),C[1]+rad*Math.sin(th)],w=K.ev(c,z),rh=Math.hypot(w[0],w[1]);zs.push(z);ws.push(w);if(j<N){ls+=Math.log(Math.max(rh,1e-9));}mn=Math.min(mn,rh);}
for(j=0;j<N;j++){var a=ws[j],b=ws[j+1];ang+=Math.atan2(a[0]*b[1]-a[1]*b[0],a[0]*b[0]+a[1]*b[1]);}
var S=1.5*Math.exp(ls/N),wd=Math.round(ang/(2*Math.PI)),mx=1e-12;ws.forEach(function(w){var rh=Math.hypot(w[0],w[1]);mx=Math.max(mx,rh/(rh+S));});var ds=ws.map(function(w){var rh=Math.hypot(w[0],w[1]),u=0.97/(mx*(rh+S));return [w[0]*u,w[1]*u];});
var inside=0,touch=false;Z.forEach(function(r){var d=Math.hypot(r[0]-C[0],r[1]-C[1]);if(d<rad){inside++;}if(Math.abs(d-rad)<0.012){touch=true;}});
K.el("path",{"class":"k-l1",d:A.d(zs)},dyn);
K.el("path",{"class":"k-curve",d:B.d(ds)+" Z"},dyn);
K.el("path",{"class":"k-x",d:"M"+(B.X(0)-5)+","+(B.Y(0)-5)+" l10,10 M"+(B.X(0)-5)+","+(B.Y(0)+5)+" l10,-10"},dyn);
[0,100,200,300].forEach(function(k){var p0=ds[k],p1=ds[k+3],q0=zs[k],q1=zs[k+3];if(A.inside(q0[0],q0[1])){arrow(dyn,A.X(q0[0]),A.Y(q0[1]),A.X(q1[0])-A.X(q0[0]),A.Y(q1[1])-A.Y(q0[1]),"c9-arg");}arrow(dyn,B.X(p0[0]),B.Y(p0[1]),B.X(p1[0])-B.X(p0[0]),B.Y(p1[1])-B.Y(p0[1]),"c9-arr");});
Z.forEach(function(r,k){if(A.inside(r[0],r[1])){K.el("circle",{"class":"k-k"+(k+1)+" c9-in",cx:A.X(r[0]),cy:A.Y(r[1]),r:6},dyn);}});
K.el("circle",{"class":"k-halo",cx:A.X(C[0]),cy:A.Y(C[1]),r:15},dyn);K.el("circle",{"class":"k-handle",cx:A.X(C[0]),cy:A.Y(C[1]),r:6},dyn);
var ct=K.el("text",{"class":"c9-cnt",x:B.x0+4,y:B.y0+14},dyn);
var ft=K.el("text",{"class":"k-lab",x:A.x0+A.w-4,y:A.y0+A.h-6,"text-anchor":"end"},dyn);ft.textContent="f(z) = z³ − z "+(0.4+dl<0?"− ":"+ ")+K.num(Math.abs(0.4+dl));
vR.textContent=K.num(rad);vD.textContent=(dl>0.005?"+":"")+K.num(dl);
if(touch||mn<1e-4){ct.textContent="оборотов: ?";out.textContent="окружность проходит через корень — образ проходит через ноль";return;}
ct.textContent="оборотов: "+wd;
if(inside===0){out.textContent="внутри окружности корней нет — образ обходит ноль 0 раз";}else{out.textContent="внутри окружности "+inside+" "+plural(inside,"корень","корня","корней")+" — образ обходит ноль "+wd+" "+plural(wd,"раз","раза","раз");}}
inR.addEventListener("input",function(){rad=parseFloat(inR.value);draw();});
inD.addEventListener("input",function(){dl=parseFloat(inD.value);draw();});
function set(e){var s=K.pt(svg,e);C=[Math.max(-2.1,Math.min(2.1,A.ix(s.x))),Math.max(-1.9,Math.min(1.9,A.iy(s.y)))];draw();}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div></div></details>

Теоремы 9 и 10 переносятся дословно: отрезки заменяются кругами, отрезок $[-R,R]$ — кругом $|z|\le R$. Вдоль пути, не задевающего $\Delta$, корни непрерывно зависят от параметра, и их число не меняется.

**Теорема 15 (основная теорема алгебры). Статус: выверено, SKELET т. 19.**
У всякого многочлена степени $n\ge1$ с комплексными коэффициентами есть комплексный корень.

*Доказательство — соединить с $x^n-1$ и перейти к пределу.* Можно считать многочлен $f$ приведённым.
**Шаг 1 ($f\notin\Delta$).** По теореме 13 соединим $f$ путём вне $\Delta$ с многочленом $x^n-1$. У $x^n-1$ ровно $n$ корней — вершины правильного $n$-угольника на единичной окружности. Вдоль пути число корней не меняется, поэтому у $f$ тоже $n$ корней.
**Шаг 2 ($f\in\Delta$).** На комплексной прямой $h_s=(1-s)f+s(x^n-1)$ лишь конечное число точек лежит в $\Delta$, поэтому найдутся $s_k\to0$ с $h_{s_k}\notin\Delta$. По шагу 1 у каждого $h_{s_k}$ есть корень $z_k$, и по лемме 8 все $z_k$ лежат в одном круге. По [теореме Больцано — Вейерштрасса](https://ru.wikipedia.org/wiki/Теорема_Больцано_—_Вейерштрасса) у последовательности $z_k$ есть предельная точка $z$, и $f(z)=\lim h_{s_k}(z_k)=0$.

Отщепляя найденный корень множителем $x-z$ и повторяя рассуждение для частного, получаем: у многочлена степени $n$ ровно $n$ корней с учётом кратности.

## После обхода корни меняются местами

Возьмём $x^2+\lambda$ и пустим $\lambda=e^{i\varphi}$ по единичной окружности вокруг нуля; ноль здесь — единственная точка дискриминанта. Корни $\pm ie^{i\varphi/2}$ поворачиваются вдвое медленнее. Когда $\lambda$ сделает полный оборот, каждый корень повернётся на пол-оборота: корни $i$ и $-i$ поменяются местами.

<div class="sim" id="sim-c3"><svg viewBox="0 0 580 250" role="img" aria-label="Интерактив: параметр лямбда обходит ноль, корни трёхчлена x квадрат плюс лямбда меняются местами"></svg><div class="sim-bar"><button type="button">обойти ноль</button></div><div class="sim-cap">Слева $\lambda$ обходит точку дискриминанта $0$, справа корни $x^2+\lambda$. Каждый корень проходит пол-оборота, и после обхода корни меняются местами; второй обход возвращает их обратно.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c3"),svg=root.querySelector("svg"),btn=root.querySelector("button");
var A=new K.Panel(30,15,220,220,[-1.5,1.5],[-1.5,1.5]),B=new K.Panel(330,15,220,220,[-1.5,1.5],[-1.5,1.5]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),c=[],i;
for(i=0;i<=120;i++){c.push([Math.cos(2*Math.PI*i/120),Math.sin(2*Math.PI*i/120)]);}
A.axes(st,"","");B.axes(st,"","");K.el("path",{"class":"k-ring",d:A.d(c)},st);K.el("path",{"class":"k-ring",d:B.d(c)},st);
K.el("path",{"class":"k-x",d:"M"+(A.X(0)-5)+","+(A.Y(0)-5)+" l10,10 M"+(A.X(0)-5)+","+(A.Y(0)+5)+" l10,-10"},st);
var phi=0,phi0=0,run=false,tr=[[],[],[]];
function rt(k){var a=phi/2+Math.PI/2+(k?Math.PI:0);return [Math.cos(a),Math.sin(a)];}
function draw(){K.clear(dyn);K.el("path",{"class":"k-path",d:A.d(tr[0])},dyn);K.el("path",{"class":"k-t1",d:B.d(tr[1])},dyn);K.el("path",{"class":"k-t2",d:B.d(tr[2])},dyn);
K.el("circle",{"class":"k-handle",cx:A.X(Math.cos(phi)),cy:A.Y(Math.sin(phi)),r:6},dyn);
[0,1].forEach(function(k){var z=rt(k);K.el("circle",{"class":"k-f"+(k+1),cx:B.X(z[0]),cy:B.Y(z[1]),r:6.5},dyn);});}
function step(){if(!run){return;}phi=Math.min(phi+0.035,phi0+2*Math.PI);tr[0].push([Math.cos(phi),Math.sin(phi)]);tr[1].push(rt(0));tr[2].push(rt(1));draw();if(phi>=phi0+2*Math.PI-1e-9){run=false;btn.disabled=false;return;}requestAnimationFrame(step);}
btn.addEventListener("click",function(){if(run){return;}phi0=phi;tr=[[[Math.cos(phi),Math.sin(phi)]],[rt(0)],[rt(1)]];run=true;btn.disabled=true;requestAnimationFrame(step);});
draw();
})();</script></div>

**Определение 16 (монодромия). Статус: выверено, SKELET опр. 20.**
Пусть $\gamma$ — замкнутый путь в пространстве приведённых многочленов степени $n$, не задевающий $\Delta$, с началом и концом в $f_0$. Проследим корни $f_0$ вдоль $\gamma$: каждый корень непрерывно движется и в конце пути попадает в один из корней $f_0$, причём разные корни не сталкиваются, так как путь не задевает $\Delta$. Получившаяся перестановка корней $f_0$ называется монодромией пути $\gamma$.

**Утверждение 17 (свойства монодромии). Статус: выверено, SKELET утв. 21.**
(а) если путь непрерывно деформировать, не сдвигая его концов и не задевая $\Delta$, перестановка не изменится; (б) обратный путь даёт обратную перестановку; (в) если пройти два пути подряд, перестановки перемножатся.

Свойство (а) верно потому, что перестановка — дискретная величина, а концы путей корней при деформации меняются непрерывно и не могут перескочить с одного корня на другой. Для (б) достаточно пройти путь назад: корни вернутся на свои места.

Для $x^n+\lambda$ картина та же, что для $x^2+\lambda$: корни — вершины правильного $n$-угольника, и при обходе $\lambda$ вокруг нуля каждый корень поворачивается на $1/n$ оборота, то есть корни переставляются по циклу.

<div class="sim" id="sim-c10"><style>#sim-c10 .c10-slot{stroke-dasharray:3 3;stroke-width:1.5;opacity:.75}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: параметр лямбда обходит ноль по окружности, пять корней многочлена x в пятой плюс лямбда поворачиваются на пятую часть оборота и переходят друг в друга по циклу"></svg><div class="sim-bar"><button type="button">обойти ноль</button><button type="button">заново</button></div><div class="sim-out"></div><div class="sim-cap">Слева $\lambda$ обходит ноль по окружности, справа пять корней $x^5+\lambda$; пунктирные кружки отмечают, где каждый корень стоял вначале. За один обход каждый корень проходит пятую часть оборота и встаёт на место соседа — корни сдвигаются по циклу.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c10"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var A=new K.Panel(30,15,270,270,[-1.5,1.5],[-1.5,1.5]),B=new K.Panel(350,15,270,270,[-1.5,1.5],[-1.5,1.5]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),c=[],i;
for(i=0;i<=160;i++){c.push([Math.cos(2*Math.PI*i/160),Math.sin(2*Math.PI*i/160)]);}
A.axes(st,"","");B.axes(st,"","");K.el("path",{"class":"k-ring",d:A.d(c)},st);K.el("path",{"class":"k-thin",d:B.d(c)},st);
K.el("path",{"class":"k-x",d:"M"+(A.X(0)-5)+","+(A.Y(0)-5)+" l10,10 M"+(A.X(0)-5)+","+(A.Y(0)+5)+" l10,-10"},st);
var l1=K.el("text",{"class":"k-lab",x:A.x0+4,y:A.y0+12},st);l1.textContent="λ";
var l2=K.el("text",{"class":"k-lab",x:B.x0+4,y:B.y0+12},st);l2.textContent="x";
var l3=K.el("text",{"class":"k-lab",x:A.X(1)+8,y:A.Y(0)+18},st);l3.textContent="1";
function rt(k,ph){var a=(Math.PI*(2*k+1)+ph)/5;return [Math.cos(a),Math.sin(a)];}
for(i=0;i<5;i++){var s0=rt(i,0);K.el("circle",{"class":"k-t"+i+" c10-slot",cx:B.X(s0[0]),cy:B.Y(s0[1]),r:12},st);}
var phi=0,phi0=0,run=false,n=0,tr=[[],[],[],[],[],[]],W=["","на одно место","на два места","на три места","на четыре места"];
function draw(){K.clear(dyn);var k;K.el("path",{"class":"k-path",d:A.d(tr[5])},dyn);for(k=0;k<5;k++){K.el("path",{"class":"k-t"+k,d:B.d(tr[k])},dyn);}
K.el("circle",{"class":"k-halo",cx:A.X(Math.cos(phi)),cy:A.Y(Math.sin(phi)),r:15},dyn);K.el("circle",{"class":"k-handle",cx:A.X(Math.cos(phi)),cy:A.Y(Math.sin(phi)),r:6},dyn);
for(k=0;k<5;k++){var z=rt(k,phi);K.el("circle",{"class":"k-k"+k,cx:B.X(z[0]),cy:B.Y(z[1]),r:6.5},dyn);}
if(run){out.textContent="обход "+(n+1)+"…";}else if(n===0){out.textContent="обходов: 0 — корни на своих местах";}else if(n%5===0){out.textContent="обходов: "+n+" — каждый корень вернулся на своё место";}else{out.textContent="обходов: "+n+" — корни сдвинулись по циклу "+W[n%5];}}
function lock(v){run=v;bs.forEach(function(x){x.disabled=v;});}
function step(){phi=Math.min(phi+0.035,phi0+2*Math.PI);tr[5].push([Math.cos(phi),Math.sin(phi)]);for(var k=0;k<5;k++){tr[k].push(rt(k,phi));}if(phi>=phi0+2*Math.PI-1e-9){n++;lock(false);draw();return;}draw();requestAnimationFrame(step);}
bs[0].addEventListener("click",function(){if(run){return;}phi0=phi;tr=[[rt(0,phi)],[rt(1,phi)],[rt(2,phi)],[rt(3,phi)],[rt(4,phi)],[[Math.cos(phi),Math.sin(phi)]]];lock(true);requestAnimationFrame(step);});
bs[1].addEventListener("click",function(){if(run){return;}phi=0;n=0;tr=[[],[],[],[],[],[]];draw();});
draw();
})();</script></div>

<div class="istoriya"><p>Перестановками корней первым занялся Лагранж. В «Размышлениях об алгебраическом решении уравнений» (1770–1771) он объяснил через них, почему существуют формулы для степеней 3 и 4, и увидел, что для степени 5 его способ не работает.</p></div>

## Пятая степень: все перестановки

Посмотрим на семейство уравнений
$$x^5-x+a=0,\qquad a\in\mathbb C.$$
Разберём его по шагам.

**Где сливаются корни.** Кратный корень — общий корень многочлена и его производной (утверждение 3), поэтому
$$\begin{cases}x^5-x+a=0,\\ 5x^4-1=0.\end{cases}$$
Из второго уравнения $x^4=\frac15$, то есть $x$ — одно из четырёх чисел
$$x_k=5^{-1/4}\,i^k,\qquad k=0,1,2,3.$$
Из первого уравнения находим $a$:
$$a=x-x^5=x\,(1-x^4)=\tfrac45\,x.$$
Значит, точек дискриминанта на прямой $a$ четыре:
$$a=\pm a_*,\ \pm ia_*,\qquad a_*=\tfrac45\cdot5^{-1/4}\approx0{,}535.$$

**Сколько корней сливается.** В точке $a=\frac45x_k$ кратный корень один — это $x_k$: остальные числа $x_j$ дают другие значения $a$. Он двойной, а не тройной: вторая производная $20x^3$ в точке $x_k$ не равна нулю. Остальные три корня простые.

**Корни в базовой точке.** При $a=0$ уравнение $x^5-x=x(x^4-1)=0$ даёт корни $0$, $\pm1$, $\pm i$.

**Какие корни сливаются.** Две из четырёх точек вещественные, и их видно на графике $a=x-x^5$. Когда $a$ растёт от нуля до $a_*$, корни $0$ и $1$ сближаются и при $a=a_*$ сливаются в вершине графика. Функция $x-x^5$ нечётна, поэтому при $a=-a_*$ сливаются $0$ и $-1$. При $x=iy$ имеем $x-x^5=i(y-y^5)$: на мнимой оси параметра то же самое происходит с корнями $0$ и $\pm i$.

<div class="sim" id="sim-c14"><style>#sim-c14 .c14-dash{stroke-dasharray:5 4}
#sim-c14 .c14-drop{stroke-dasharray:2 3}
#sim-c14 .c14-loc{stroke-width:1.4;opacity:.75}
#sim-c14 .c14-lev{fill:none;stroke:var(--accent);stroke-width:1.6}
#sim-c14 .c14-v{fill:var(--panel);stroke:var(--text);stroke-width:1.6}
#sim-c14 .c14-dot{stroke:var(--panel);stroke-width:1.5}
#sim-c14 .c14-dbl{fill:none;stroke:var(--accent);stroke-width:1.4}
#sim-c14 svg{cursor:ns-resize}</style><svg viewBox="0 0 650 300" role="img" aria-label="Интерактив: слева график a равно x минус x в пятой и горизонтальная прямая на высоте a, которую можно перетаскивать; точки пересечения — вещественные корни уравнения x в пятой минус x плюс a равно нулю; справа все пять корней на комплексной плоскости"></svg><div class="sim-out"></div><div class="sim-cap">Слева график $a=x-x^5$ и уровень $a$ — прямую можно перетаскивать; её пересечения с графиком — вещественные корни $x^5-x+a=0$, справа все пять корней на комплексной плоскости. Когда $a$ растёт от $0$ до $a_*\approx0{,}535$, корни $0$ и $1$ сближаются и сливаются, а дальше уходят в комплексную плоскость парой.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c14"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out");
var A=new K.Panel(28,15,322,270,[-1.55,1.55],[-1.25,1.25]),B=new K.Panel(392,25,250,250,[-1.45,1.45],[-1.45,1.45]);
var V=Math.pow(5,-0.25),AS=0.8*V,a=0.3,drag=false,st=K.el("g",{},svg),dyn=K.el("g",{},svg),i,k,t,gp=[],tr=[[],[],[],[],[]];
function g(x){return x-x*x*x*x*x;}
function co(v){return [[1,0],[0,0],[0,0],[0,0],[-1,0],[v,0]];}
function lab(x,y,s,an,p){var e=K.el("text",{"class":"k-lab",x:x,y:y,"text-anchor":an||"start"},p||st);e.textContent=s;return e;}
[AS,-AS].forEach(function(v){K.el("line",{"class":"k-thin c14-dash",x1:A.x0,y1:A.Y(v),x2:A.x0+A.w,y2:A.Y(v)},st);});
[[-V,-AS],[V,AS]].forEach(function(v){K.el("line",{"class":"k-thin c14-dash",x1:A.X(v[0]),y1:A.Y(v[1]),x2:A.X(v[0]),y2:A.Y(0)},st);});
A.axes(st,"x","a");
lab(A.x0+A.w,A.Y(AS)-6,"a*","end");lab(A.x0+A.w,A.Y(-AS)+16,"−a*","end");
lab(A.X(1)-6,A.Y(0)+16,"1","end");lab(A.X(-1)-6,A.Y(0)+16,"−1","end");
for(i=0;i<=540;i++){t=-1.35+2.7*i/540;gp.push([t,g(t)]);}
K.el("path",{"class":"k-curve",d:A.d(gp)},st);
[[-V,-AS],[V,AS]].forEach(function(v){K.el("circle",{"class":"c14-v",cx:A.X(v[0]),cy:A.Y(v[1]),r:4},st);});
function track(dir){var z=[[0,0],[1,0],[-1,0],[0,1],[0,-1]],res=[[],[],[],[],[]],j,m;for(j=1;j<=380;j++){z=K.dk(co(dir*0.95*j/380),z.map(function(r,n){return [r[0],r[1]+1e-5*(n-2)];}),30);for(m=0;m<5;m++){res[m].push([z[m][0],z[m][1]]);}}return res;}
var tn=track(-1),tp=track(1);
for(k=0;k<5;k++){tr[k]=tn[k].slice().reverse().concat([[[0,0],[1,0],[-1,0],[0,1],[0,-1]][k]]).concat(tp[k]);K.el("path",{"class":"k-thin c14-loc",d:B.d(tr[k])},st);}
B.axes(st,"","");
[[0,0],[1,0],[-1,0],[0,1],[0,-1]].forEach(function(v){K.el("circle",{"class":"k-ring",cx:B.X(v[0]),cy:B.Y(v[1]),r:10},st);});
lab(B.X(0)-7,B.Y(0)+19,"0","end");lab(B.X(1),B.Y(0)+24,"1","middle");lab(B.X(-1),B.Y(0)+24,"−1","middle");lab(B.X(0)-16,B.Y(1)+4,"i","end");lab(B.X(0)-16,B.Y(-1)+4,"−i","end");
lab(B.x0+2,B.y0+12,"x");
function h(x){return x*x*x*x*x-x+a;}
function real(){var xs=[-3,-V,V,3],res=[],j,n,lo,hi,fl,fm,md;
[-V,V].forEach(function(c){if(Math.abs(h(c))<1e-9){res.push([c,2]);}});
for(j=0;j<3;j++){lo=xs[j];hi=xs[j+1];fl=h(lo);if(Math.abs(fl)>=1e-9&&Math.abs(h(hi))>=1e-9&&fl*h(hi)<0){for(n=0;n<90;n++){md=(lo+hi)/2;fm=h(md);if(fl*fm<=0){hi=md;}else{lo=md;fl=fm;}}res.push([(lo+hi)/2,1]);}}
res.sort(function(p,q){return p[0]-q[0];});return res;}
function draw(){K.clear(dyn);var r=real(),nm=0,z,cx,ly=A.Y(a),s,d;
r.forEach(function(e){nm+=e[1];});
z=K.dk(co(a),[0,1,2,3,4].map(function(n){return [0.4+0.9*Math.cos(1.3*n),0.9*Math.sin(1.3*n)+0.1];}),160);
z.sort(function(p,q){return Math.abs(p[1])-Math.abs(q[1]);});cx=z.slice(nm);
K.el("line",{"class":"c14-lev",x1:A.x0,y1:ly,x2:A.x0+A.w,y2:ly},dyn);
r.forEach(function(e){K.el("line",{"class":"k-thin c14-drop",x1:A.X(e[0]),y1:ly,x2:A.X(e[0]),y2:A.Y(0)},dyn);});
r.forEach(function(e){K.el("circle",{"class":"k-f1 c14-dot",cx:A.X(e[0]),cy:ly,r:e[1]>1?7:5.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(-1.45),cy:ly,r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(-1.45),cy:ly,r:6.5},dyn);
cx.forEach(function(e){K.el("circle",{"class":"k-f2 c14-dot",cx:B.X(e[0]),cy:B.Y(e[1]),r:5.5},dyn);});
r.forEach(function(e){if(e[1]>1){K.el("circle",{"class":"c14-dbl",cx:B.X(e[0]),cy:B.Y(0),r:11},dyn);}K.el("circle",{"class":"k-f1 c14-dot",cx:B.X(e[0]),cy:B.Y(0),r:e[1]>1?7:5.5},dyn);});
s=Math.abs(Math.abs(a)-AS)<1e-12?(a>0?"a = a* ≈ 0,535: ":"a = −a* ≈ −0,535: "):"a = "+K.num(a)+": ";
if(r.length===3){d=s+"три вещественных корня, "+r.map(function(e){return K.num(e[0]);}).join("; ")+"; и пара комплексных";}
else if(r.length===2){r.sort(function(p,q){return q[1]-p[1];});d=s+"двойной корень "+K.num(r[0][0])+", простой "+K.num(r[1][0])+" и пара комплексных";}
else{d=s+"один вещественный корень "+K.num(r[0][0])+" и две пары комплексных";}
out.textContent=d;}
function set(e){var p=K.pt(svg,e),v=Math.max(-0.95,Math.min(0.95,A.iy(p.y)));if(Math.abs(Math.abs(v)-AS)<0.02){v=v>0?AS:-AS;}a=v;draw();}
svg.addEventListener("pointerdown",function(e){var p=K.pt(svg,e);if(p.x<A.x0+A.w+12){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

**Утверждение 18 (монодромия семейства $x^5-x+a$). Статус: выверено, SKELET утв. 25.**
Пусть петля идёт из $a=0$ по отрезку почти до одной из точек дискриминанта, обходит её по маленькой окружности и возвращается по тому же отрезку. Монодромия такой петли меняет местами корень $0$ и корень $1$, $-1$, $i$ или $-i$ (для точек $a_*$, $-a_*$, $ia_*$, $-ia_*$ соответственно), а остальные три корня оставляет на месте.

*Доказательство — возле точки слияния всё как у $x^2+\lambda$.* Три простых корня по теореме 14 всё время остаются в своих маленьких кругах и возвращаются на место. Возле двойного корня $x_k$ имеем $a-a_k=(x-x_k)^2u(x)$, где $u(x_k)\ne0$, поэтому рядом с $x_k$ число $u(x)$ почти не меняется и вокруг нуля не оборачивается. Когда $a$ обходит $a_k$, аргумент числа $a-a_k$ растёт на $2\pi$; значит, аргумент $(x-x_k)^2$ тоже растёт на $2\pi$, а аргумент $x-x_k$ — на $\pi$. Корень делает пол-оборота вокруг $x_k$ и приходит на место второго корня, как в примере $x^2+\lambda$.

<div class="sim" id="sim-c4"><svg viewBox="0 0 650 310" role="img" aria-label="Интерактив: плоскость параметра a с четырьмя точками дискриминанта и пять корней многочлена x в пятой минус x плюс a; петли вокруг точек переставляют корни"></svg><div class="sim-bar"><button type="button">вокруг +a*</button><button type="button">вокруг −a*</button><button type="button">вокруг +ia*</button><button type="button">вокруг −ia*</button><button type="button">заново</button></div><div class="sim-out"></div><div class="sim-cap">Слева плоскость параметра $a$: крестики — точки дискриминанта, точку $a$ можно перетаскивать или пустить по петле кнопкой. Справа пять корней $x^5-x+a$; пунктирные кружки — места корней при $a=0$. Под рисунком видно, какой корень оказался на каком месте после обходов.</div><script>(function(){
var K=window.SimK,root=document.getElementById("sim-c4"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var A=new K.Panel(20,15,280,280,[-0.85,0.85],[-0.85,0.85]),B=new K.Panel(350,15,280,280,[-1.55,1.55],[-1.55,1.55]);
var st=K.el("g",{},svg),dyn=K.el("g",{},svg);
var as=Math.pow(256/3125,0.25),BR=[[as,0],[-as,0],[0,as],[0,-as]],SL=[[0,0],[1,0],[-1,0],[0,1],[0,-1]],NM=["0","1","−1","i","−i"];
A.axes(st,"","");B.axes(st,"","");
BR.forEach(function(b){K.el("path",{"class":"k-x",d:"M"+(A.X(b[0])-5)+","+(A.Y(b[1])-5)+" l10,10 M"+(A.X(b[0])-5)+","+(A.Y(b[1])+5)+" l10,-10"},st);});
SL.forEach(function(s,k){K.el("circle",{"class":"k-ring",cx:B.X(s[0]),cy:B.Y(s[1]),r:11},st);var t=K.el("text",{"class":"k-lab",x:B.X(s[0])+13,y:B.Y(s[1])+(k===4?20:-9)},st);t.textContent=NM[k];});
K.el("circle",{"class":"k-base",cx:A.X(0),cy:A.Y(0),r:4},st);
var a=[0,0],z=SL.map(function(s){return [s[0],s[1]];}),ta=[],tz=[[],[],[],[],[]],busy=false,drag=false;
function co(a){return [[1,0],[0,0],[0,0],[0,0],[-1,0],[a[0],a[1]]];}
function moveTo(b){var dx=b[0]-a[0],dy=b[1]-a[1],n=Math.max(1,Math.ceil(Math.hypot(dx,dy)/0.003)),i;for(i=1;i<=n;i++){var c=[a[0]+dx*i/n,a[1]+dy*i/n];z=K.dk(co(c),z,6);}a=[b[0],b[1]];ta.push([a[0],a[1]]);z.forEach(function(w,k){tz[k].push([w[0],w[1]]);});}
function slots(){var res=[];SL.forEach(function(s){var best=0,bd=9;z.forEach(function(w,k){var d=Math.hypot(w[0]-s[0],w[1]-s[1]);if(d<bd){bd=d;best=k;}});res.push(best);});return res;}
function draw(){K.clear(dyn);K.el("path",{"class":"k-path",d:A.d(ta)},dyn);tz.forEach(function(t,k){K.el("path",{"class":"k-t"+k,d:B.d(t)},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(a[0]),cy:A.Y(a[1]),r:15},dyn);K.el("circle",{"class":"k-handle",cx:A.X(a[0]),cy:A.Y(a[1]),r:6},dyn);
z.forEach(function(w,k){K.el("circle",{"class":"k-k"+k,cx:B.X(w[0]),cy:B.Y(w[1]),r:6.5},dyn);});
if(Math.hypot(a[0],a[1])<0.02){var s=slots(),h="на местах ";s.forEach(function(k,j){h+='<span class="sim-chip">'+NM[j]+' <span class="sim-dot k-d'+k+'"></span></span>';});out.innerHTML=h;}else{out.textContent="a = "+K.num(a[0])+(a[1]<0?" − ":" + ")+K.num(Math.abs(a[1]))+"i";}}
function loopPts(b){var u=[b[0]/as,b[1]/as],r=0.07,P=[],i,n=Math.ceil((as-r)/0.01);for(i=1;i<=n;i++){P.push([u[0]*(as-r)*i/n,u[1]*(as-r)*i/n]);}for(i=1;i<=90;i++){var t=2*Math.PI*i/90,c=Math.cos(t),s=Math.sin(t);P.push([b[0]-r*(u[0]*c-u[1]*s),b[1]-r*(u[1]*c+u[0]*s)]);}for(i=n-1;i>=0;i--){P.push([u[0]*(as-r)*i/n,u[1]*(as-r)*i/n]);}return P;}
function play(P){busy=true;bs.forEach(function(x){x.disabled=true;});var j=0;function f(){var k;for(k=0;k<2&&j<P.length;k++,j++){moveTo(P[j]);}draw();if(j<P.length){requestAnimationFrame(f);}else{moveTo([0,0]);draw();busy=false;bs.forEach(function(x){x.disabled=false;});}}requestAnimationFrame(f);}
function start(){ta=[[a[0],a[1]]];tz=z.map(function(w){return [[w[0],w[1]]];});}
[0,1,2,3].forEach(function(k){bs[k].addEventListener("click",function(){if(busy){return;}var P=[],d=Math.hypot(a[0],a[1]),i,n=Math.ceil(d/0.01);for(i=1;i<=n;i++){P.push([a[0]*(1-i/n),a[1]*(1-i/n)]);}start();play(P.concat(loopPts(BR[k])));});});
bs[4].addEventListener("click",function(){if(busy){return;}a=[0,0];z=SL.map(function(s){return [s[0],s[1]];});ta=[];tz=[[],[],[],[],[]];draw();});
function set(e){var s=K.pt(svg,e),b=[Math.max(-0.84,Math.min(0.84,A.ix(s.x))),Math.max(-0.84,Math.min(0.84,A.iy(s.y)))];moveTo(b);draw();}
svg.addEventListener("pointerdown",function(e){if(busy){return;}var s=K.pt(svg,e);if(s.x<A.x0+A.w+10){drag=true;svg.setPointerCapture(e.pointerId);start();set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();</script></div>

**Все перестановки.** Обмены (транспозиции) корня $0$ с каждым из остальных корней порождают все перестановки. Обмен любых двух корней $u$ и $v$ получается так:
$$(u\,v)=(0\,u)(0\,v)(0\,u),$$
а любая перестановка — произведение обменов. По свойству (в) произведению перестановок соответствует проход петель подряд. Значит, обходами точек дискриминанта получаются все $5!=120$ перестановок корней.

<figure>
<svg viewBox="0 0 540 250" role="img" aria-label="Слева: плоскость параметра a, четыре точки дискриминанта и четыре петли из нуля. Справа: корни 0, 1, минус 1, i, минус i; каждая петля меняет местами корень 0 с одним из четырёх — звезда обменов"><path class="s-thin-a" d="M130.0,125.0 L193.9,125.0"/><path class="s-thin-a" d="M193.9,125.0 L194.0,125.8 L194.1,126.5 L194.2,127.3 L194.4,128.0 L194.7,128.7 L195.0,129.4 L195.4,130.1 L195.8,130.7 L196.3,131.3 L196.8,131.9 L197.4,132.4 L198.0,132.9 L198.6,133.3 L199.3,133.6 L200.0,133.9 L200.7,134.2 L201.5,134.4 L202.2,134.5 L203.0,134.6 L203.8,134.6 L204.5,134.6 L205.3,134.5 L206.0,134.3 L206.8,134.1 L207.5,133.8 L208.2,133.5 L208.8,133.1 L209.4,132.6 L210.0,132.1 L210.6,131.6 L211.1,131.0 L211.5,130.4 L211.9,129.8 L212.3,129.1 L212.6,128.4 L212.8,127.6 L213.0,126.9 L213.1,126.1 L213.2,125.4 L213.2,124.6 L213.1,123.9 L213.0,123.1 L212.8,122.4 L212.6,121.6 L212.3,120.9 L211.9,120.2 L211.5,119.6 L211.1,119.0 L210.6,118.4 L210.0,117.9 L209.4,117.4 L208.8,116.9 L208.2,116.5 L207.5,116.2 L206.8,115.9 L206.0,115.7 L205.3,115.5 L204.5,115.4 L203.8,115.4 L203.0,115.4 L202.2,115.5 L201.5,115.6 L200.7,115.8 L200.0,116.1 L199.3,116.4 L198.6,116.7 L198.0,117.1 L197.4,117.6 L196.8,118.1 L196.3,118.7 L195.8,119.3 L195.4,119.9 L195.0,120.6 L194.7,121.3 L194.4,122.0 L194.2,122.7 L194.1,123.5 L194.0,124.2 L193.9,125.0"/><path class="s-accent" d="M199.6,121.0 L207.6,129.0 M199.6,129.0 L207.6,121.0"/><path class="s-thin-a" d="M130.0,125.0 L130.0,61.1"/><path class="s-thin-a" d="M130.0,61.1 L130.8,61.0 L131.5,60.9 L132.3,60.8 L133.0,60.6 L133.7,60.3 L134.4,60.0 L135.1,59.6 L135.7,59.2 L136.3,58.7 L136.9,58.2 L137.4,57.6 L137.9,57.0 L138.3,56.4 L138.6,55.7 L138.9,55.0 L139.2,54.3 L139.4,53.5 L139.5,52.8 L139.6,52.0 L139.6,51.2 L139.6,50.5 L139.5,49.7 L139.3,49.0 L139.1,48.2 L138.8,47.5 L138.5,46.8 L138.1,46.2 L137.6,45.6 L137.1,45.0 L136.6,44.4 L136.0,43.9 L135.4,43.5 L134.8,43.1 L134.1,42.7 L133.4,42.4 L132.6,42.2 L131.9,42.0 L131.1,41.9 L130.4,41.8 L129.6,41.8 L128.9,41.9 L128.1,42.0 L127.4,42.2 L126.6,42.4 L125.9,42.7 L125.2,43.1 L124.6,43.5 L124.0,43.9 L123.4,44.4 L122.9,45.0 L122.4,45.6 L121.9,46.2 L121.5,46.8 L121.2,47.5 L120.9,48.2 L120.7,49.0 L120.5,49.7 L120.4,50.5 L120.4,51.2 L120.4,52.0 L120.5,52.8 L120.6,53.5 L120.8,54.3 L121.1,55.0 L121.4,55.7 L121.7,56.4 L122.1,57.0 L122.6,57.6 L123.1,58.2 L123.7,58.7 L124.3,59.2 L124.9,59.6 L125.6,60.0 L126.3,60.3 L127.0,60.6 L127.7,60.8 L128.5,60.9 L129.2,61.0 L130.0,61.1"/><path class="s-accent" d="M126.0,47.4 L134.0,55.4 M126.0,55.4 L134.0,47.4"/><path class="s-thin-a" d="M130.0,125.0 L66.1,125.0"/><path class="s-thin-a" d="M66.1,125.0 L66.0,124.2 L65.9,123.5 L65.8,122.7 L65.6,122.0 L65.3,121.3 L65.0,120.6 L64.6,119.9 L64.2,119.3 L63.7,118.7 L63.2,118.1 L62.6,117.6 L62.0,117.1 L61.4,116.7 L60.7,116.4 L60.0,116.1 L59.3,115.8 L58.5,115.6 L57.8,115.5 L57.0,115.4 L56.2,115.4 L55.5,115.4 L54.7,115.5 L54.0,115.7 L53.2,115.9 L52.5,116.2 L51.8,116.5 L51.2,116.9 L50.6,117.4 L50.0,117.9 L49.4,118.4 L48.9,119.0 L48.5,119.6 L48.1,120.2 L47.7,120.9 L47.4,121.6 L47.2,122.4 L47.0,123.1 L46.9,123.9 L46.8,124.6 L46.8,125.4 L46.9,126.1 L47.0,126.9 L47.2,127.6 L47.4,128.4 L47.7,129.1 L48.1,129.8 L48.5,130.4 L48.9,131.0 L49.4,131.6 L50.0,132.1 L50.6,132.6 L51.2,133.1 L51.8,133.5 L52.5,133.8 L53.2,134.1 L54.0,134.3 L54.7,134.5 L55.5,134.6 L56.2,134.6 L57.0,134.6 L57.8,134.5 L58.5,134.4 L59.3,134.2 L60.0,133.9 L60.7,133.6 L61.4,133.3 L62.0,132.9 L62.6,132.4 L63.2,131.9 L63.7,131.3 L64.2,130.7 L64.6,130.1 L65.0,129.4 L65.3,128.7 L65.6,128.0 L65.8,127.3 L65.9,126.5 L66.0,125.8 L66.1,125.0"/><path class="s-accent" d="M52.4,121.0 L60.4,129.0 M52.4,129.0 L60.4,121.0"/><path class="s-thin-a" d="M130.0,125.0 L130.0,188.9"/><path class="s-thin-a" d="M130.0,188.9 L129.2,189.0 L128.5,189.1 L127.7,189.2 L127.0,189.4 L126.3,189.7 L125.6,190.0 L124.9,190.4 L124.3,190.8 L123.7,191.3 L123.1,191.8 L122.6,192.4 L122.1,193.0 L121.7,193.6 L121.4,194.3 L121.1,195.0 L120.8,195.7 L120.6,196.5 L120.5,197.2 L120.4,198.0 L120.4,198.8 L120.4,199.5 L120.5,200.3 L120.7,201.0 L120.9,201.8 L121.2,202.5 L121.5,203.2 L121.9,203.8 L122.4,204.4 L122.9,205.0 L123.4,205.6 L124.0,206.1 L124.6,206.5 L125.2,206.9 L125.9,207.3 L126.6,207.6 L127.4,207.8 L128.1,208.0 L128.9,208.1 L129.6,208.2 L130.4,208.2 L131.1,208.1 L131.9,208.0 L132.6,207.8 L133.4,207.6 L134.1,207.3 L134.8,206.9 L135.4,206.5 L136.0,206.1 L136.6,205.6 L137.1,205.0 L137.6,204.4 L138.1,203.8 L138.5,203.2 L138.8,202.5 L139.1,201.8 L139.3,201.0 L139.5,200.3 L139.6,199.5 L139.6,198.8 L139.6,198.0 L139.5,197.2 L139.4,196.5 L139.2,195.7 L138.9,195.0 L138.6,194.3 L138.3,193.6 L137.9,193.0 L137.4,192.4 L136.9,191.8 L136.3,191.3 L135.7,190.8 L135.1,190.4 L134.4,190.0 L133.7,189.7 L133.0,189.4 L132.3,189.2 L131.5,189.1 L130.8,189.0 L130.0,188.9"/><path class="s-accent" d="M126.0,194.6 L134.0,202.6 M126.0,202.6 L134.0,194.6"/><circle class="s-node s-node-r" cx="130.0" cy="125.0" r="3.6"/><line class="s-accent" x1="410.0" y1="125.0" x2="483.3" y2="125.0"/><line class="s-accent" x1="410.0" y1="125.0" x2="336.7" y2="125.0"/><line class="s-accent" x1="410.0" y1="125.0" x2="410.0" y2="51.7"/><line class="s-accent" x1="410.0" y1="125.0" x2="410.0" y2="198.3"/><circle class="s-node" cx="483.3" cy="125.0" r="3.6"/><circle class="s-node" cx="336.7" cy="125.0" r="3.6"/><circle class="s-node" cx="410.0" cy="51.7" r="3.6"/><circle class="s-node" cx="410.0" cy="198.3" r="3.6"/><circle class="s-node s-node-r" cx="410.0" cy="125.0" r="3.6"/><text class="s-txt-m" x="481.3" y="143.0">1</text><text class="s-txt-m" x="328.7" y="143.0">−1</text><text class="s-txt-m" x="418.0" y="51.7">i</text><text class="s-txt-m" x="418.0" y="202.3">−i</text><text class="s-txt-m" x="416.0" y="141.0">0</text></svg>
<figcaption>Слева — четыре петли из $a=0$ вокруг точек дискриминанта. Справа — обмены, которые они дают: корень $0$ меняется местами с каждым из четырёх остальных</figcaption>
</figure>

## Почему нет формулы

Перестановки, которые дают замкнутые пути с началом в одной точке, образуют группу — группу монодромии: произведение и обратная перестановка снова получаются из путей (свойства (б) и (в)). Чтобы сказать, чем группа монодромии уравнения, решаемого в радикалах, отличается от группы всех перестановок, нужны два понятия.

**Определение 19 (коммутатор и разрешимая группа). Статус: объявляем.**
Коммутатор перестановок $\sigma$ и $\tau$ — это перестановка $[\sigma,\tau]=\sigma\tau\sigma^{-1}\tau^{-1}$. Для группы перестановок $G$ её коммутант $G'$ — множество всех произведений коммутаторов элементов $G$; это снова группа. Группа $G$ называется разрешимой, если цепочка $G\supseteq G'\supseteq G''\supseteq\dots$ через несколько шагов доходит до группы из одной тождественной перестановки.

> поле:mn Подробнее — в статьях «[Коммутант](https://ru.wikipedia.org/wiki/Коммутант)» и «[Разрешимая группа](https://ru.wikipedia.org/wiki/Разрешимая_группа)» и в первой главе книги В. Б. Алексеева.

Например, группа циклических сдвигов $n$ корней $x^n+\lambda$ разрешима: циклические сдвиги перестановочны, поэтому все коммутаторы тождественны и уже $G'$ состоит из одной тождественной перестановки.

**Теорема 20 (Арнольд; топологическая форма теоремы Абеля). Статус: объявляем.**
Если корни уравнения $x^5-x+a=0$ выражаются через $a$ с помощью сложения, вычитания, умножения, деления и извлечения корней натуральной степени, то группа монодромии этого уравнения разрешима.

Эту теорему мы принимаем без доказательства: на лекции его не было. Идея Арнольда такая. Пройдём первую петлю, вторую, затем первую и вторую в обратную сторону — это коммутатор петель. Радикалы первого этажа формулы при обходе петли поворачиваются на долю оборота, как корни $x^n+\lambda$, а повороты перестановочны, поэтому после коммутатора петель они возвращаются на место. Радикалы второго этажа возвращаются после коммутатора коммутаторов, и так далее: если в формуле $k$ этажей, то $k$-кратные коммутаторы петель не двигают корни. Подробно это доказано у Алексеева (гл. 2, §§ 11–14) и у Фукса — Табачникова (лекция 5).

**Утверждение 21 (все перестановки пяти корней — неразрешимая группа). Статус: выверено, proverki.py п. 10.**
Группа всех $120$ перестановок пяти элементов неразрешима.

*Доказательство — каждый цикл длины 3 есть коммутатор двух циклов длины 3.* Коммутатор циклов $(1\,2\,4)$ и $(1\,3\,5)$ — снова цикл длины 3, а переименовывая элементы, любой цикл длины 3 можно получить как коммутатор двух циклов длины 3. Значит, если группа содержит все циклы длины 3, то и её коммутант их содержит. Группа всех перестановок их содержит, поэтому их содержит каждый член цепочки $G\supseteq G'\supseteq G''\supseteq\dots$, и до тождественной группы цепочка не доходит.

По утверждению 18 группа монодромии уравнения $x^5-x+a=0$ — все 120 перестановок, а по утверждению 21 она неразрешима. Значит, по теореме 20 **формулы в радикалах для корней уравнения $x^5-x+a=0$ через $a$ нет.** Тем более нет формулы для общего уравнения пятой степени через его коэффициенты: пути на прямой $a$ лежат и в пространстве всех приведённых многочленов пятой степени, поэтому монодромия общего уравнения тоже даёт все 120 перестановок.

> поле:mn Формула в радикалах многозначна, и среди её значений могут быть лишние. Доказательство от этого не ломается: ветвь формулы, совпавшая с корнем, остаётся корнем при любом продолжении, поэтому группа перестановок корней — образ группы перестановок значений формулы, а образ разрешимой группы разрешим.

Итак, нет формулы, пригодной сразу при всех $a$. Отдельные уравнения семейства решаются в радикалах, например, $x^5-x-30=(x-2)(x^4+2x^3+4x^2+8x+15)$. А чтобы доказать, что в радикалах не решается конкретное уравнение с числовыми коэффициентами, например $x^5-x-1=0$, нужна уже теория Галуа.

<div class="istoriya"><p>У самой теоремы непростая история. В 1799 году Паоло Руффини опубликовал доказательство в двухтомном трактате; в доказательстве был пробел, и современники отнеслись к работе холодно, хотя в 1821 году Коши написал Руффини, что тот доказал теорему полностью. В 1824 году Нильс Хенрик Абель издал доказательство за свой счёт и ради экономии уложил его в шесть страниц; одну брошюру он отправил Гауссу. Подробный вариант вышел в 1826 году в первом томе журнала Крелле. Абель умер от туберкулёза в апреле 1829 года в 26 лет; через два дня после его смерти пришло письмо с приглашением в Берлинский университет. Эварист Галуа, погибший на дуэли в 1832 году в двадцать лет, нашёл, когда уравнение решается в радикалах; Пуассон счёл его мемуар недостаточно ясным, и работы Галуа опубликовал Лиувилль только в 1846 году.</p></div>

<div class="istoriya"><p>Топологическое доказательство, по следам которого мы шли, придумал В. И. Арнольд. В 1963–1964 годах он рассказал его школьникам только что открытой физико-математической школы-интерната при МГУ. В 1976 году один из слушателей, В. Б. Алексеев, издал по этим лекциям книгу «Теорема Абеля в задачах и решениях».</p></div>

## Ответ и что читать дальше

Формулы в радикалах для уравнения пятой степени нет. Препятствие — не сложность выкладок, а геометрия: в комплексном мире дискриминант можно обойти, число корней всегда одно и то же, но при обходе точки дискриминанта корни меняются местами. Обходы дают все 120 перестановок, а формула в радикалах дала бы разрешимую группу.

В этих записках изложена лекция, и заканчиваются они там же, где она. Доказательство теоремы 20 подробно разобрано у В. Б. Алексеева («Теорема Абеля в задачах и решениях», гл. 2, §§ 11–14) и у Д. Б. Фукса и С. Л. Табачникова («Математический дивертисмент», лекция 5; там то же семейство $x^5-x+a$). Вещественную геометрию дискриминантов, включая ласточкин хвост, подробно описывает брошюра В. А. Васильева «Геометрия дискриминанта». Идея работает и за пределами радикалов. А. Г. Хованский построил топологическую теорию Галуа: тем же способом доказывается, что многие функции не выражаются ни в радикалах, ни даже в квадратурах. В 2020 году А. Я. Канель-Белов с соавторами доказали этим методом, что уравнение $\tan x-x=a$ не решается в элементарных функциях.

> поле:mn В топологии множество пар «многочлен вне дискриминанта, его корень» называется накрытием над дополнением к дискриминанту, а группа перестановок корней при обходах — группой монодромии этого накрытия. Подробности — в книге Алексеева и в книге Хованского «Топологическая теория Галуа».
