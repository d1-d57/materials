(function(){
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
})();
