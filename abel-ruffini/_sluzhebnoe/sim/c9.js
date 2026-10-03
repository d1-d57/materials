(function(){
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
})();
