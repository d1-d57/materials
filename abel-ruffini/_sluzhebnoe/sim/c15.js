(function(){
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
})();
