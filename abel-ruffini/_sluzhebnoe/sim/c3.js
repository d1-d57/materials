(function(){
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
})();
