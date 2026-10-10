(function(){
var K=window.SimK,root=document.getElementById("sim-c8");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),pw=root.querySelector(".c8-pw"),go=root.querySelector(".c8-go");
var NR=7,sn=4,pow=false,W=600,G=null,run=null,NB=" ";
var SUP=["⁰","¹","²","³","⁴","⁵","⁶","⁷"];
/* геометрия как в c7: шаг по строке dx, высота клетки ch, полоса между строками bd; справа колонка сумм шириной sw */
function geo(){var fs=W<480?14:15,sw=fs*5.6,gap=W<480?10:18,dx=Math.min(48,(W-10-gap-sw)/8),s=dx/38,ch=23*s,bd=31*s,dy=ch+bd,top=6*s+ch/2,tw=8*dx+gap+sw,x0=(W-tw)/2;
return {dx:dx,s:s,cw:dx-6*s,ch:ch,bd:bd,dy:dy,top:top,fs:fs,fn:Math.max(13,13*s),tc:x0+4*dx,sx:x0+8*dx+gap,H:top+NR*dy+ch/2+6*s};}
function X(n,k){return G.tc+(k-n/2)*G.dx;}
function Y(n){return G.top+n*G.dy;}
function row(n){var r=[],k;for(k=0;k<=n;k++){r.push(K.C(n,k));}return r;}
function build(){if(run){run.stop();run=null;}K.clear(svg);G=geo();
svg.setAttribute("viewBox","0 0 "+W+" "+G.H.toFixed(1));
var gr=K.el("g",{},svg);G.ga=K.el("g",{},svg);G.rows=[];G.sums=[];
var n,k;for(n=0;n<=NR;n++){(function(n){var y=Y(n),g=K.el("g",{"class":"c8-row c8-r"+n,"data-n":n},gr);
for(k=0;k<=n;k++){var x=X(n,k),c=K.el("g",{"class":"c8-cell","data-n":n,"data-k":k},g);
K.el("rect",{"class":"c8-box",x:(x-G.cw/2).toFixed(1),y:(y-G.ch/2).toFixed(1),width:G.cw.toFixed(1),height:G.ch.toFixed(1),rx:(7*G.s).toFixed(1)},c);
var t=K.el("text",{"class":"c8-num",x:x.toFixed(1),y:(y+G.fn*0.36).toFixed(1),"font-size":G.fn.toFixed(1)},c);t.textContent=String(K.C(n,k));}
/* пунктир от строки к её сумме */
var xe=X(n,n)+G.cw/2+5*G.s,xs=G.sx-5;if(xs-xe>6){K.el("line",{"class":"c8-lead",x1:xe.toFixed(1),y1:y.toFixed(1),x2:xs.toFixed(1),y2:y.toFixed(1)},g);}
var sm=K.el("text",{"class":"c8-sum","data-n":n,x:G.sx.toFixed(1),y:(y+G.fs*0.36).toFixed(1),"font-size":G.fs},g);G.sums.push(sm);
/* зона нажатия — вся полоса строки, вместе с суммой */
var h=K.el("rect",{"class":"c8-hit",x:0,y:(y-G.dy/2).toFixed(1),width:W,height:G.dy.toFixed(1)},g);
h.addEventListener("click",function(){pick(Math.min(n,NR-1));});G.rows.push(g);})(n);}
sums();draw();}
function sums(){G.sums.forEach(function(t,n){K.clear(t);var v=Math.pow(2,n);t.textContent="= "+v+(pow?" = 2"+SUP[n]:"");t.setAttribute("data-p",pow?n:"");});}
/* наконечник в точке E по направлению (ux,uy) */
function head(E,ux,uy,par){var L=6.5*G.s,w=3.4*G.s,bx=E[0]-ux*L,by=E[1]-uy*L;
K.el("polygon",{"class":"c8-hd",points:E[0].toFixed(1)+","+E[1].toFixed(1)+" "+(bx-uy*w).toFixed(1)+","+(by+ux*w).toFixed(1)+" "+(bx+uy*w).toFixed(1)+","+(by-ux*w).toFixed(1)},par);}
/* стрелка из клетки (n,k) вниз: d=-1 — в (n+1,k) левее, d=1 — в (n+1,k+1) правее; выходит из своей половины клетки, входит в ближнюю половину цели */
function arrow(n,k,d){var kb=d<0?k:k+1,g=K.el("g",{"class":"c8-arr "+(d<0?"c8-L":"c8-R"),"data-a":n+","+k,"data-b":(n+1)+","+kb},G.ga);
var s=G.s,P=[X(n,k)+d*0.1*G.cw,Y(n)+G.ch/2+2.5*s],Q=[X(n+1,kb)-d*0.24*G.cw,Y(n+1)-G.ch/2-2.5*s],vx=Q[0]-P[0],vy=Q[1]-P[1],L=Math.sqrt(vx*vx+vy*vy);
K.el("line",{"class":"c8-ln",x1:P[0].toFixed(1),y1:P[1].toFixed(1),x2:(Q[0]-vx/L*4*s).toFixed(1),y2:(Q[1]-vy/L*4*s).toFixed(1)},g);
head(Q,vx/L,vy/L,g);return g;}
function draw(){if(run){run.stop();run=null;}K.clear(G.ga);
G.rows.forEach(function(g,n){g.setAttribute("class","c8-row c8-r"+n+(n===sn||n===sn+1?" on":" dim"));});
G.arr=[];var k;for(k=0;k<=sn;k++){G.arr.push({g:arrow(sn,k,-1),k:k,d:-1});G.arr.push({g:arrow(sn,k,1),k:k,d:1});}
say();}
function plus(a){var n=a.length;return n<2?String(a[0]):a.slice(0,n-1).join(NB+"+ ")+NB+"+"+NB+a[n-1];}
function say(){var a=row(sn),b=row(sn+1),S=Math.pow(2,sn);
var h='<div class="c8-line c8-l1"><span class="c8-pr">строка '+sn+':</span> <span class="c8-f">'+(a.length>1?plus(a)+NB+"= ":"")+"<b>"+S+"</b></span></div>";
h+='<div class="c8-line c8-l2"><span class="c8-pr">каждое число строки'+NB+sn+" вошло в"+NB+"строку"+NB+(sn+1)+NB+'дважды:</span> <span class="c8-f">2'+NB+"·"+NB+S+NB+"= <b>"+2*S+"</b>"+NB+"= "+plus(b)+"</span></div>";
out.innerHTML=h;}
function pick(n){sn=n;draw();}
pw.addEventListener("click",function(){pow=!pow;pw.classList.toggle("on",pow);pw.setAttribute("aria-pressed",pow?"true":"false");sums();});
/* «шагать»: выделение спускается на строку; сначала проявляются синие стрелки (первая копия строки), потом рыжие (вторая) */
go.addEventListener("click",function(){pick(sn<NR-1?sn+1:0);var m=sn+1;
G.arr.forEach(function(o){o.g.setAttribute("opacity","0");});
run=K.anim(1300,function(t){G.arr.forEach(function(o){var a=(o.d<0?0:0.5)+0.4*o.k/m;o.g.setAttribute("opacity",K.seg(t,a,a+0.45/m+0.08).toFixed(3));});},function(){G.arr.forEach(function(o){o.g.removeAttribute("opacity");});run=null;});});
/* клавиатура: стрелки вверх-вниз двигают выбранную строку */
svg.addEventListener("keydown",function(e){var n=sn;if(e.key==="ArrowUp"){n--;}else if(e.key==="ArrowDown"){n++;}else{return;}e.preventDefault();pick(K.cl(n,0,NR-1));});
K.onWidth(root,function(w){W=w;build();});
})();
