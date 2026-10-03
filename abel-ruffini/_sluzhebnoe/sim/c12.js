(function(){
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
})();
