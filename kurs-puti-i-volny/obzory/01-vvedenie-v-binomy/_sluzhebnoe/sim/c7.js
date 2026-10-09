(function(){
var K=window.SimK,root=document.getElementById("sim-c7");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".c7-b"),go=root.querySelector(".c7-go");
var NR=8,sn=6,sk=3,dir=0,W=600,G=null,run=null;
var SYM=["←","→","↖","↗"],NM=["строка, слева","строка, справа","диагональ, слева","диагональ, справа"];
/* маршрут от единицы на краю к клетке (n,k): стрелка {a:хвост,b:голова,p/q:множитель}; значение в голове = значение в хвосте · p/q */
function route(n,k,d){var r=[],j,m;
if(d===0){for(j=0;j<k;j++){r.push({a:[n,j],b:[n,j+1],p:n-j,q:j+1});}}
else if(d===1){for(j=n-1;j>=k;j--){r.push({a:[n,j+1],b:[n,j],p:j+1,q:n-j});}}
else if(d===2){for(m=n-k;m<n;m++){j=m-(n-k);r.push({a:[m,j],b:[m+1,j+1],p:m+1,q:j+1});}}
else{for(m=k;m<n;m++){r.push({a:[m,k],b:[m+1,k],p:m+1,q:m+1-k});}}
return r;}
function start(n,k,d){return d===0?[n,0]:(d===1?[n,n]:(d===2?[n-k,0]:[k,k]));}
/* геометрия: шаг по строке dx, высота клетки ch, полоса между строками bd */
function geo(){var dx=Math.min(48,(W-6)/9.2),s=dx/38,ch=23*s,bd=29*s,dy=ch+bd,top=8*s+ch/2;
return {dx:dx,s:s,cw:dx-6*s,ch:ch,bd:bd,dy:dy,top:top,fn:Math.max(13,13*s),fl:Math.max(12,Math.min(15,12*s)),H:top+NR*dy+ch/2+bd+2*s};}
function X(n,k){return W/2+(k-n/2)*G.dx;}
function Y(n){return G.top+n*G.dy;}
function build(){if(run){run.stop();run=null;}K.clear(svg);G=geo();
svg.setAttribute("viewBox","0 0 "+W+" "+G.H.toFixed(1));
var gc=K.el("g",{},svg);G.ga=K.el("g",{},svg);G.cells={};
var n,k;for(n=0;n<=NR;n++){for(k=0;k<=n;k++){(function(n,k){var x=X(n,k),y=Y(n),g=K.el("g",{"class":"c7-cell","data-n":n,"data-k":k},gc);
K.el("rect",{"class":"c7-box",x:(x-G.cw/2).toFixed(1),y:(y-G.ch/2).toFixed(1),width:G.cw.toFixed(1),height:G.ch.toFixed(1),rx:(7*G.s).toFixed(1)},g);
var t=K.el("text",{"class":"c7-num",x:x.toFixed(1),y:(y+G.fn*0.36).toFixed(1),"font-size":G.fn.toFixed(1)},g);t.textContent=String(K.C(n,k));
var h=K.el("rect",{"class":"c7-hit",x:(x-G.dx/2).toFixed(1),y:(y-G.dy/2).toFixed(1),width:G.dx.toFixed(1),height:G.dy.toFixed(1)},g);
h.addEventListener("click",function(){pick(n,k);});G.cells[n+","+k]=g;})(n,k);}}
draw();}
/* наконечник в точке E по направлению (ux,uy) */
function head(E,ux,uy,par){var L=7*G.s,w=3.6*G.s,bx=E[0]-ux*L,by=E[1]-uy*L;
K.el("polygon",{"class":"c7-hd",points:E[0].toFixed(1)+","+E[1].toFixed(1)+" "+(bx-uy*w).toFixed(1)+","+(by+ux*w).toFixed(1)+" "+(bx+uy*w).toFixed(1)+","+(by-ux*w).toFixed(1)},par);}
function lab(a){return "×"+a.p+(a.q===1?"":"/"+a.q);}
function arrow(a,ri,par){var g=K.el("g",{"class":"c7-arr c7-r"+ri,"data-a":a.a.join(","),"data-b":a.b.join(","),"data-p":a.p,"data-q":a.q},par);
var s=G.s,A=[X(a.a[0],a.a[1]),Y(a.a[0])],B=[X(a.b[0],a.b[1]),Y(a.b[0])],t,ux,uy,L;
if(a.a[0]===a.b[0]){
/* по строке: дуга под строкой, подпись под дугой */
var sg=B[0]>A[0]?1:-1,y0=A[1]+G.ch/2+2*s,P0=[A[0]+sg*0.2*G.dx,y0],P1=[B[0]-sg*0.2*G.dx,y0],mx=(A[0]+B[0])/2,Cq=[mx,y0+10*s];
K.el("path",{"class":"c7-ln",d:"M"+P0[0].toFixed(1)+","+P0[1].toFixed(1)+" Q"+Cq[0].toFixed(1)+","+Cq[1].toFixed(1)+" "+P1[0].toFixed(1)+","+P1[1].toFixed(1)},g);
ux=P1[0]-Cq[0];uy=P1[1]-Cq[1];L=Math.sqrt(ux*ux+uy*uy);head(P1,ux/L,uy/L,g);
t=K.el("text",{"class":"c7-lab",x:mx.toFixed(1),y:(y0+7*s+G.fl*0.8).toFixed(1),"text-anchor":"middle","font-size":G.fl.toFixed(1)},g);}
else{
/* по диагонали: отрезок между клетками, подпись снаружи от маршрута */
var vx=B[0]-A[0],vy=B[1]-A[1],f=(G.ch/2+3*s)/vy,Q0=[A[0]+vx*f,A[1]+vy*f],Q1=[B[0]-vx*f,B[1]-vy*f],side=vx>0?-1:1,M=[(A[0]+B[0])/2,(A[1]+B[1])/2];
K.el("line",{"class":"c7-ln",x1:Q0[0].toFixed(1),y1:Q0[1].toFixed(1),x2:Q1[0].toFixed(1),y2:Q1[1].toFixed(1)},g);
L=Math.sqrt(vx*vx+vy*vy);head(Q1,vx/L,vy/L,g);
t=K.el("text",{"class":"c7-lab",x:(M[0]+side*7*s).toFixed(1),y:(M[1]+G.fl*0.36).toFixed(1),"text-anchor":side<0?"end":"start","font-size":G.fl.toFixed(1)},g);}
t.textContent=lab(a);return g;}
function dirs(){return dir===4?[0,1,2,3]:[dir];}
function draw(){if(run){run.stop();run=null;}K.clear(G.ga);
var key;for(key in G.cells){G.cells[key].setAttribute("class","c7-cell");}
G.arr=[];dirs().forEach(function(d){var ri=dir===4?d:0,r=route(sn,sk,d);if(!r.length){return;}
var st=start(sn,sk,d);G.cells[st.join(",")].setAttribute("class","c7-cell on st c7-r"+ri);
r.forEach(function(a,i){var hc=i<r.length-1?G.cells[a.b.join(",")]:null;if(hc){hc.setAttribute("class","c7-cell on c7-r"+ri);}G.arr.push({g:arrow(a,ri,G.ga),i:i,hc:hc,cls:"c7-cell on c7-r"+ri});});});
G.cells[sn+","+sk].setAttribute("class","c7-cell sel");
go.disabled=!G.arr.length;say();}
function fr(p,q){return '<span class="c7-fr"><span>'+p+'</span><span>'+q+'</span></span>';}
function chain(r,v){return '<span class="c7-v">'+v+'</span><span>=</span><span>1</span>'+r.map(function(a){return '<span>·</span>'+fr(a.p,a.q);}).join("");}
function say(){var v=K.C(sn,sk),h="";
if(dir<4){var r=route(sn,sk,dir);
if(!r.length){h='<div class="c7-line" data-r="'+dir+'"><span class="c7-v">'+v+'</span><span class="c7-dim">— это сама единица на краю</span></div>';}
else{h='<div class="c7-line" data-r="'+dir+'">'+chain(r,v)+'</div><div class="c7-line c7-pr">'+v+" · ("+r.map(function(a){return a.q;}).join("·")+") = 1 · ("+r.map(function(a){return a.p;}).join("·")+")</div>";}}
else{if(sn===0){h='<div class="c7-line"><span class="c7-v">1</span><span class="c7-dim">— это сама единица на краю</span></div>';}
else{[0,1,2,3].forEach(function(d){var r=route(sn,sk,d),sy='<span class="c7-s c7-s'+d+'" title="'+NM[d]+'">'+SYM[d]+'</span>';
h+='<div class="c7-line" data-r="'+d+'">'+sy+(r.length?chain(r,v):'<span class="c7-v">'+v+'</span><span class="c7-dim">— сама единица</span>')+"</div>";});}}
out.innerHTML='<div class="c7-blk'+(dir===4&&sn>0?" c7-four":"")+'">'+h+"</div>";}
function pick(n,k){sn=n;sk=k;draw();}
function setDir(d){dir=d;bs.forEach(function(b){b.classList.toggle("on",+b.getAttribute("data-d")===dir);});draw();}
bs.forEach(function(b){b.addEventListener("click",function(){setDir(+b.getAttribute("data-d"));});});
/* «шагать»: стрелки проявляются по одной от единицы; при «меньше движения» K.anim сразу даёт последний кадр */
go.addEventListener("click",function(){draw();var L=0;G.arr.forEach(function(o){L=Math.max(L,o.i+1);});if(!L){return;}
G.arr.forEach(function(o){o.g.setAttribute("opacity","0");if(o.hc){o.hc.setAttribute("class","c7-cell");}});
/* клетка маршрута загорается, когда в неё пришла стрелка */
run=K.anim(650*L+200,function(t){G.arr.forEach(function(o){var a=o.i/L*0.92,v=K.seg(t,a,a+0.6/L);o.g.setAttribute("opacity",v.toFixed(3));if(o.hc){o.hc.setAttribute("class",v>0.6?o.cls:"c7-cell");}});},function(){run=null;});});
/* клавиатура: стрелки двигают выбранную клетку */
svg.addEventListener("keydown",function(e){var n=sn,k=sk;
if(e.key==="ArrowLeft"){k--;}else if(e.key==="ArrowRight"){k++;}else if(e.key==="ArrowUp"){n--;}else if(e.key==="ArrowDown"){n++;}else{return;}
e.preventDefault();n=K.cl(n,0,NR);k=K.cl(k,0,n);pick(n,k);});
K.onWidth(root,function(w){W=w;build();});
})();
