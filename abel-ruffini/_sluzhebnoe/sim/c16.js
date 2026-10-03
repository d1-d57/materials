(function(){
var K=window.SimK,root=document.getElementById("sim-c16"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll("button");
var S=new K.Panel(25,10,600,280,[0.5-0.4*600/280,0.5+0.4*600/280],[-0.4,0.4]);
var R0=0.06,M=0.035,X0=[[0.55,0],[0.2,0.25],[0.84,-0.24],[1.22,0.14]],X=X0.map(function(p){return [p[0],p[1]];}),sel=-1,st=K.el("g",{},svg),dyn=K.el("g",{},svg);
K.el("line",{"class":"k-thin",x1:S.x0,y1:S.Y(0),x2:S.x0+S.w,y2:S.Y(0)},st);
K.el("line",{"class":"k-thin c16-seg",x1:S.X(0),y1:S.Y(0),x2:S.X(1),y2:S.Y(0)},st);
function lab(x,y,s,an){var e=K.el("text",{"class":"k-lab",x:x,y:y,"text-anchor":an||"start"},st);e.textContent=s;}
lab(S.X(0),S.Y(0)+22,"0","middle");lab(S.X(1),S.Y(0)+22,"1","middle");lab(S.x0+4,S.y0+16,"s");
function near(p){return Math.abs(p[1])<R0&&p[0]>0&&p[0]<1;}
function dArc(p,c,r,sd){if(sd*p[1]>=0){return Math.abs(Math.hypot(p[0]-c,p[1])-r);}return Math.min(Math.hypot(p[0]-c+r,p[1]),Math.hypot(p[0]-c-r,p[1]));}
function plan(){var cl=X.filter(near).map(function(p){return {L:p[0]-R0,R:p[0]+R0};}),it,mg,ch,res;
for(it=0;it<40;it++){cl.sort(function(u,v){return u.L-v.L;});mg=[];cl.forEach(function(q){var l=mg[mg.length-1];if(l&&q.L<=l.R){l.R=Math.max(l.R,q.R);}else{mg.push({L:q.L,R:q.R});}});cl=mg;ch=false;
cl.forEach(function(q){var c=(q.L+q.R)/2,r=(q.R-q.L)/2,nu=0,nd=0;X.forEach(function(p){if(Math.hypot(p[0]-c,p[1])<r+M){if(p[1]>1e-9){nu++;}if(p[1]<-1e-9){nd++;}}});q.sd=nu>nd?-1:1;
X.forEach(function(p){var d;if(dArc(p,c,r,q.sd)<M){d=Math.hypot(p[0]-c,p[1])+M;if(d>r){r=d;ch=true;}}});q.L=c-r;q.R=c+r;});
if(!ch){break;}}
cl.forEach(function(q){if(q.L<0.004){q.L=0.004;}if(q.R>0.996){q.R=0.996;}});
res=[[0,0]];cl.forEach(function(q){var c=(q.L+q.R)/2,r=(q.R-q.L)/2,j,th;res.push([q.L,0]);for(j=1;j<=60;j++){th=Math.PI*(1-j/60);res.push([c+r*Math.cos(th),q.sd*r*Math.sin(th)]);}});res.push([1,0]);return res;}
function arrow(pts){var L=0,i,acc=0,tot,p,q,sl=0,u,dx,dy,n,x,y;for(i=1;i<pts.length;i++){L+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);}tot=0.93*L;
for(i=1;i<pts.length;i++){p=pts[i-1];q=pts[i];sl=Math.hypot(q[0]-p[0],q[1]-p[1]);if(acc+sl>=tot){break;}acc+=sl;}
u=sl>0?(tot-acc)/sl:0;x=S.X(p[0]+(q[0]-p[0])*u);y=S.Y(p[1]+(q[1]-p[1])*u);dx=S.X(q[0])-S.X(p[0]);dy=S.Y(q[1])-S.Y(p[1]);n=Math.hypot(dx,dy)||1;dx/=n;dy/=n;
K.el("path",{"class":"c16-arr",d:"M"+(x+dx*8).toFixed(1)+","+(y+dy*8).toFixed(1)+" L"+(x-dx*6-dy*6).toFixed(1)+","+(y-dy*6+dx*6).toFixed(1)+" L"+(x-dx*6+dy*6).toFixed(1)+","+(y-dy*6-dx*6).toFixed(1)+" z"},dyn);}
function draw(){K.clear(dyn);var pts=plan(),n=X.filter(near).length;
K.el("path",{"class":"k-l1 c16-path",d:S.d(pts)},dyn);arrow(pts);
[0,1].forEach(function(v){K.el("circle",{"class":"k-base",cx:S.X(v),cy:S.Y(0),r:5},dyn);});
X.forEach(function(p,k){var x=S.X(p[0]),y=S.Y(p[1]);if(k===sel){K.el("circle",{"class":"k-halo",cx:x,cy:y,r:16},dyn);}K.el("circle",{"class":"c16-hit",cx:x,cy:y,r:14},dyn);K.el("path",{"class":"k-x c16-x",d:"M"+(x-6)+","+(y-6)+" l12,12 M"+(x-6)+","+(y+6)+" l12,-12"},dyn);});
if(n===0){out.textContent="на отрезке нет плохих точек — путь идёт прямо";}else if(n===1){out.textContent="на отрезке 1 плохая точка — путь её обходит";}else{out.textContent="на отрезке "+n+" плохие точки — путь их обходит";}}
function clamp(p){var x=Math.max(S.xr[0]+0.03,Math.min(S.xr[1]-0.03,p[0])),y=Math.max(-0.37,Math.min(0.37,p[1]));[0,1].forEach(function(b){var d=Math.hypot(x-b,y);if(d<0.1){if(d<1e-9){y=0.1;}else{x=b+(x-b)*0.1/d;y=y*0.1/d;}}});return [x,y];}
svg.addEventListener("pointerdown",function(e){var s=K.pt(svg,e),bd=24;sel=-1;X.forEach(function(p,k){var d=Math.hypot(S.X(p[0])-s.x,S.Y(p[1])-s.y);if(d<bd){bd=d;sel=k;}});if(sel>=0){svg.setPointerCapture(e.pointerId);draw();}});
svg.addEventListener("pointermove",function(e){if(sel<0){return;}var s=K.pt(svg,e);X[sel]=clamp([S.ix(s.x),S.iy(s.y)]);draw();});
svg.addEventListener("pointerup",function(){sel=-1;draw();});
bs[0].addEventListener("click",function(){var v=[],x,k,ok,tries=0;while(v.length<X.length&&tries<1000){tries++;x=0.15+0.7*Math.random();ok=true;for(k=0;k<v.length;k++){if(Math.abs(v[k]-x)<0.05){ok=false;}}if(ok){v.push(x);}}X=v.map(function(x){return [x,0];});draw();});
bs[1].addEventListener("click",function(){X=X0.map(function(p){return [p[0],p[1]];});draw();});
draw();
})();
