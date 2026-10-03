(function(){
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
})();
