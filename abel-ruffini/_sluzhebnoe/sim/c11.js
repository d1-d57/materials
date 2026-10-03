(function(){
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
})();
