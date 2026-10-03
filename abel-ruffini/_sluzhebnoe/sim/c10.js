(function(){
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
})();
