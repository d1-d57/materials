(function(){
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
})();
