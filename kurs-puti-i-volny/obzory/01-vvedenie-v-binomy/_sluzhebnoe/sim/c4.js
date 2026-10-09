(function(){
var K=window.SimK,root=document.getElementById("sim-c4");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c4-n"),vN=root.querySelector(".c4-nv"),btn=root.querySelector(".c4-go");
var n=5,W=600,G=null,s=1,run=null,sel=-1;
/* квадратичная дуга P0→P2 с контрольной точкой Q; точка и касательная при параметре u */
function qp(a,q,b,u){var v=1-u;return [v*v*a[0]+2*v*u*q[0]+u*u*b[0],v*v*a[1]+2*v*u*q[1]+u*u*b[1]];}
function qd(a,q,b,u){return [2*(1-u)*(q[0]-a[0])+2*u*(b[0]-q[0]),2*(1-u)*(q[1]-a[1])+2*u*(b[1]-q[1])];}
function dist(p,c){return Math.hypot(p[0]-c[0],p[1]-c[1]);}
/* параметр, где дуга выходит из круга радиуса rho вокруг c (бисекция; inside — сторона u0) */
function cut(a,q,b,c,rho,u0,u1){var lo=u0,hi=u1,i;for(i=0;i<30;i++){var mid=(lo+hi)/2;if(dist(qp(a,q,b,mid),c)<rho){lo=mid;}else{hi=mid;}}return (lo+hi)/2;}
function build(){
if(run){run.stop();run=null;}K.clear(svg);
var H=Math.round(Math.min(W,460)),cx=W/2,cy=H/2,R=H/2-22,rv=n>7?5:6,i;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
var P=[];for(i=0;i<n;i++){var a=-Math.PI/2+2*Math.PI*i/n;P.push([cx+R*Math.cos(a),cy+R*Math.sin(a)]);}
var gS=K.el("g",{},svg),gA=K.el("g",{},svg),gV=K.el("g",{},svg),ars=K.arrows(n).map(function(p){return {i:p[0],j:p[1],path:K.el("path",{"class":"c4-ar"},gA),hd:K.el("path",{"class":"c4-hd"},gA)};});
var segs=[];for(i=0;i<n;i++){for(var j=i+1;j<n;j++){segs.push({i:i,j:j,e:K.el("line",{"class":"c4-seg",x1:P[i][0],y1:P[i][1],x2:P[j][0],y2:P[j][1],opacity:0},gS)});}}
var vs=P.map(function(p,i){var c=K.el("circle",{"class":"c4-v",cx:p[0],cy:p[1],r:rv},gV);K.el("circle",{"class":"c4-hit",cx:p[0],cy:p[1],r:20,"data-v":i},gV);return c;});
G={P:P,ars:ars,segs:segs,vs:vs,gA:gA,gS:gS,rho:rv+4+n*1.1};frame(s);mark();}
function frame(ss){s=ss;var P=G.P,rho=G.rho,op=K.cl(ss*1.6-0.3,0,1);
G.ars.forEach(function(A){var a=P[A.i],b=P[A.j],dx=b[0]-a[0],dy=b[1]-a[1],L=Math.hypot(dx,dy),nx=-dy/L,ny=dx/L,d=Math.min(16,0.13*L)*ss;
var q=[(a[0]+b[0])/2+nx*d*2,(a[1]+b[1])/2+ny*d*2];
var u0=cut(a,q,b,a,rho,0,0.5),u1=1-cut(b,q,a,b,rho,0,0.5);
/* остриё — по касательной в конце (СК1): высота 9, основание 8 */
var T=qp(a,q,b,u1),tg=qd(a,q,b,u1),tl=Math.hypot(tg[0],tg[1]),ux=tg[0]/tl,uy=tg[1]/tl,Bx=T[0]-9*ux,By=T[1]-9*uy,u2=1-cut(b,q,a,b,rho+7,0,0.5),pts=[],k;
for(k=0;k<=16;k++){var p=qp(a,q,b,u0+(u2-u0)*k/16);pts.push(p[0].toFixed(1)+","+p[1].toFixed(1));}
A.path.setAttribute("d","M"+pts.join(" L"));A.hd.setAttribute("d","M"+(Bx-4*uy).toFixed(1)+","+(By+4*ux).toFixed(1)+" L"+T[0].toFixed(1)+","+T[1].toFixed(1)+" L"+(Bx+4*uy).toFixed(1)+","+(By-4*ux).toFixed(1)+"Z");
A.hd.setAttribute("opacity",op.toFixed(3));});G.gA.style.display=ss>0.02?"":"none";
var so=K.cl((0.25-ss)/0.25,0,1);G.segs.forEach(function(S){S.e.setAttribute("opacity",so.toFixed(3));});G.gS.style.display=so>0?"":"none";}
function mark(){var arrows=s>0.5;G.vs.forEach(function(v,i){v.classList.toggle("hl",i===sel);});
G.ars.forEach(function(A){var on=arrows&&(A.i===sel);A.path.classList.toggle("hl",on);A.hd.classList.toggle("hl",on);A.path.classList.toggle("dim",arrows&&sel>=0&&!on);A.hd.classList.toggle("dim",arrows&&sel>=0&&!on);});
G.segs.forEach(function(S){var on=!arrows&&(S.i===sel||S.j===sel);S.e.classList.toggle("hl",on);S.e.classList.toggle("dim",!arrows&&sel>=0&&!on);});
var N=n*(n-1),t;
if(arrows){t="стрелок: "+n+" · "+(n-1)+" = <b>"+N+"</b>";if(sel>=0){t+='<br><span class="w-dim">из вершины выходит '+(n-1)+" "+K.pl(n-1,"стрелка","стрелки","стрелок")+"</span>";}}
else{t="отрезков: "+K.bn(n,2)+" = <b>"+N/2+"</b>, стрелок "+N+" = 2 · "+N/2;if(sel>=0){t+='<br><span class="w-dim">из вершины выходит '+(n-1)+" "+K.pl(n-1,"отрезок","отрезка","отрезков")+"</span>";}}
out.innerHTML=t;}
svg.addEventListener("pointerdown",function(e){var v=e.target.getAttribute&&e.target.getAttribute("data-v");var i=(v===null||v===undefined)?-1:+v;sel=(i===sel)?-1:i;mark();});
btn.addEventListener("click",function(){if(run){return;}var from=s,to=s>0.5?0:1;btn.disabled=true;sel=-1;mark();
run=K.anim(1600,function(u){frame(from+(to-from)*K.ease(u));},function(){run=null;btn.disabled=false;btn.textContent=to?"склеить пары":"развести";mark();});});
inN.addEventListener("input",function(){n=+inN.value;vN.textContent=n;sel=-1;build();});
K.onWidth(root,function(w){W=w;build();});
})();
