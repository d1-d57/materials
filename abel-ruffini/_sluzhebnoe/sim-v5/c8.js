(function(){
var K=window.SimK,root=document.getElementById("sim-c8"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),btn=root.querySelector("button"),rng=root.querySelector("input");
var A=new K.Panel(45,20,245,240,[0,5],[-3,3]),B=new K.Panel(350,15,280,180,[-1.8,1.8],[-2.5,2.5]),T=new K.Panel(350,222,280,62,[-1.8,1.8],[0,1]);
var F0=[-0.8,-2.2,2.5,0.6,-0.5],F1=[0.8,-2.2,-2.5,0.6,0.5],H=[0,1,0,-1,0],N=1000,R=[],C=[],i,t,k;
function co(s){var w=Math.sin(Math.PI*s);return F0.map(function(v,j){return (1-s)*v+s*F1[j]+w*H[j];});}
function cz(a){return [[1,0]].concat(a.map(function(v){return [v,0];}));}
var z=K.dk(cz(co(0)),[[-1.5,0],[-0.49,0],[0.41,0],[1.19,0.48],[1.19,-0.48]],40);
for(i=0;i<=N;i++){z=K.dk(cz(co(i/N)),z,8);var w=z.slice().sort(function(p,q){return Math.abs(p[1])-Math.abs(q[1]);});C.push(w.filter(function(p){return Math.abs(p[1])<1e-6;}).length);R.push(w.slice(0,3).map(function(p){return p[0];}).sort(function(p,q){return p-q;}));}
var st=K.el("g",{},svg),dyn=K.el("g",{},svg),j=0,busy=false,NM=["нет вещественных корней","один вещественный корень","два вещественных корня","три вещественных корня","четыре вещественных корня","пять вещественных корней"],SB=["₁","₂","₃","₄","₅"];
[-2,-1,1,2].forEach(function(v){K.el("line",{"class":"k-thin",x1:A.x0,y1:A.Y(v),x2:A.x0+A.w,y2:A.Y(v),style:"stroke-dasharray:2 4"},st);});
[-2,-1,0,1,2].forEach(function(v){var u=K.el("text",{"class":"k-lab",x:A.x0-8,y:A.Y(v)+4,"text-anchor":"end"},st);u.textContent=v<0?"−"+(-v):String(v);});
K.el("line",{"class":"k-ax",x1:A.x0,y1:A.Y(0),x2:A.x0+A.w,y2:A.Y(0)},st);
for(k=0;k<5;k++){t=K.el("text",{"class":"k-lab",x:A.X(k+0.5),y:A.y0+A.h+20,"text-anchor":"middle",style:"font-size:15px;fill:var(--text)"},st);t.textContent="a"+SB[k];}
B.axes(st,"x","y");
K.el("rect",{"class":"k-shade",x:T.x0,y:T.y0,width:T.w,height:T.h,rx:4,style:"opacity:.55"},st);
K.el("line",{"class":"k-thin",x1:T.X(0),y1:T.y0,x2:T.X(0),y2:T.y0+T.h,style:"stroke-dasharray:2 4"},st);
t=K.el("text",{"class":"k-lab",x:T.x0-6,y:T.y0+10,"text-anchor":"end"},st);t.textContent="s = 0";
t=K.el("text",{"class":"k-lab",x:T.x0-6,y:T.y0+T.h,"text-anchor":"end"},st);t.textContent="1";
function ev(a,x){var r=1;a.forEach(function(v){r=r*x+v;});return r;}
function draw(){K.clear(dyn);var s=j/N,a=co(s),gp=[],m,x,cur=R[j];
a.forEach(function(v,n){var y0=A.Y(0),y1=A.Y(v),cx=A.X(n+0.5);K.el("rect",{"class":"k-f1",x:cx-14,y:Math.min(y0,y1),width:28,height:Math.max(1,Math.abs(y1-y0)),rx:2,style:"opacity:.85"},dyn);var u=K.el("text",{"class":"k-lab",x:cx,y:v>=0?y1-6:y1+15,"text-anchor":"middle",style:"paint-order:stroke;stroke:var(--panel);stroke-width:4px;stroke-linejoin:round"},dyn);u.textContent=K.num(v);});
for(m=0;m<=360;m++){x=-1.8+3.6*m/360;gp.push([x,ev(a,x)]);}
K.el("path",{"class":"k-curve",d:B.d(gp)},dyn);
K.el("line",{"class":"k-thin",x1:T.x0,y1:T.Y(1-s),x2:T.x0+T.w,y2:T.Y(1-s)},dyn);
[0,1,2].forEach(function(n){var tr=[];for(m=0;m<=j;m++){tr.push([R[m][n],1-m/N]);}if(tr.length>1){K.el("path",{"class":"k-t"+(n+1),d:T.d(tr),style:"stroke-width:2;opacity:.8"},dyn);}K.el("circle",{"class":"k-k"+(n+1),cx:T.X(cur[n]),cy:T.Y(1-s),r:3.5},dyn);K.el("line",{"class":"k-thin",x1:B.X(cur[n]),y1:B.Y(0)+7,x2:T.X(cur[n]),y2:T.Y(1-s)-4,style:"stroke-dasharray:2 3"},dyn);});
[0,1,2].forEach(function(n){K.el("circle",{"class":"k-k"+(n+1),cx:B.X(cur[n]),cy:B.Y(0),r:6},dyn);});
out.textContent="s = "+K.num(s)+": "+NM[C[j]]+", "+cur.map(K.num).join("; ");}
rng.addEventListener("input",function(){busy=false;btn.disabled=false;j=Math.round(Number(rng.value)*N);draw();});
btn.addEventListener("click",function(){if(busy){return;}busy=true;btn.disabled=true;var T0=null;
function step(ts){if(!busy){return;}if(T0===null){T0=ts;}var u=Math.min(1,(ts-T0)/4000);j=Math.round(u*N);rng.value=String(j/N);draw();if(u<1){requestAnimationFrame(step);}else{busy=false;btn.disabled=false;}}
requestAnimationFrame(step);});
draw();
})();
