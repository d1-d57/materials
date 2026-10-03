(function(){
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
})();
