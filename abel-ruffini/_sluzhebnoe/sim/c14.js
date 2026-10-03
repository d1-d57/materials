(function(){
var K=window.SimK,root=document.getElementById("sim-c14"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out");
var A=new K.Panel(28,15,322,270,[-1.55,1.55],[-1.25,1.25]),B=new K.Panel(392,25,250,250,[-1.45,1.45],[-1.45,1.45]);
var V=Math.pow(5,-0.25),AS=0.8*V,a=0.3,drag=false,st=K.el("g",{},svg),dyn=K.el("g",{},svg),i,k,t,gp=[],tr=[[],[],[],[],[]];
function g(x){return x-x*x*x*x*x;}
function co(v){return [[1,0],[0,0],[0,0],[0,0],[-1,0],[v,0]];}
function lab(x,y,s,an,p){var e=K.el("text",{"class":"k-lab",x:x,y:y,"text-anchor":an||"start"},p||st);e.textContent=s;return e;}
[AS,-AS].forEach(function(v){K.el("line",{"class":"k-thin c14-dash",x1:A.x0,y1:A.Y(v),x2:A.x0+A.w,y2:A.Y(v)},st);});
[[-V,-AS],[V,AS]].forEach(function(v){K.el("line",{"class":"k-thin c14-dash",x1:A.X(v[0]),y1:A.Y(v[1]),x2:A.X(v[0]),y2:A.Y(0)},st);});
A.axes(st,"x","a");
lab(A.x0+A.w,A.Y(AS)-6,"a*","end");lab(A.x0+A.w,A.Y(-AS)+16,"−a*","end");
lab(A.X(1)-6,A.Y(0)+16,"1","end");lab(A.X(-1)-6,A.Y(0)+16,"−1","end");
for(i=0;i<=540;i++){t=-1.35+2.7*i/540;gp.push([t,g(t)]);}
K.el("path",{"class":"k-curve",d:A.d(gp)},st);
[[-V,-AS],[V,AS]].forEach(function(v){K.el("circle",{"class":"c14-v",cx:A.X(v[0]),cy:A.Y(v[1]),r:4},st);});
function track(dir){var z=[[0,0],[1,0],[-1,0],[0,1],[0,-1]],res=[[],[],[],[],[]],j,m;for(j=1;j<=380;j++){z=K.dk(co(dir*0.95*j/380),z.map(function(r,n){return [r[0],r[1]+1e-5*(n-2)];}),30);for(m=0;m<5;m++){res[m].push([z[m][0],z[m][1]]);}}return res;}
var tn=track(-1),tp=track(1);
for(k=0;k<5;k++){tr[k]=tn[k].slice().reverse().concat([[[0,0],[1,0],[-1,0],[0,1],[0,-1]][k]]).concat(tp[k]);K.el("path",{"class":"k-thin c14-loc",d:B.d(tr[k])},st);}
B.axes(st,"","");
[[0,0],[1,0],[-1,0],[0,1],[0,-1]].forEach(function(v){K.el("circle",{"class":"k-ring",cx:B.X(v[0]),cy:B.Y(v[1]),r:10},st);});
lab(B.X(0)-7,B.Y(0)+19,"0","end");lab(B.X(1),B.Y(0)+24,"1","middle");lab(B.X(-1),B.Y(0)+24,"−1","middle");lab(B.X(0)-16,B.Y(1)+4,"i","end");lab(B.X(0)-16,B.Y(-1)+4,"−i","end");
lab(B.x0+2,B.y0+12,"x");
function h(x){return x*x*x*x*x-x+a;}
function real(){var xs=[-3,-V,V,3],res=[],j,n,lo,hi,fl,fm,md;
[-V,V].forEach(function(c){if(Math.abs(h(c))<1e-9){res.push([c,2]);}});
for(j=0;j<3;j++){lo=xs[j];hi=xs[j+1];fl=h(lo);if(Math.abs(fl)>=1e-9&&Math.abs(h(hi))>=1e-9&&fl*h(hi)<0){for(n=0;n<90;n++){md=(lo+hi)/2;fm=h(md);if(fl*fm<=0){hi=md;}else{lo=md;fl=fm;}}res.push([(lo+hi)/2,1]);}}
res.sort(function(p,q){return p[0]-q[0];});return res;}
function draw(){K.clear(dyn);var r=real(),nm=0,z,cx,ly=A.Y(a),s,d;
r.forEach(function(e){nm+=e[1];});
z=K.dk(co(a),[0,1,2,3,4].map(function(n){return [0.4+0.9*Math.cos(1.3*n),0.9*Math.sin(1.3*n)+0.1];}),160);
z.sort(function(p,q){return Math.abs(p[1])-Math.abs(q[1]);});cx=z.slice(nm);
K.el("line",{"class":"c14-lev",x1:A.x0,y1:ly,x2:A.x0+A.w,y2:ly},dyn);
r.forEach(function(e){K.el("line",{"class":"k-thin c14-drop",x1:A.X(e[0]),y1:ly,x2:A.X(e[0]),y2:A.Y(0)},dyn);});
r.forEach(function(e){K.el("circle",{"class":"k-f1 c14-dot",cx:A.X(e[0]),cy:ly,r:e[1]>1?7:5.5},dyn);});
K.el("circle",{"class":"k-halo",cx:A.X(-1.45),cy:ly,r:16},dyn);K.el("circle",{"class":"k-handle",cx:A.X(-1.45),cy:ly,r:6.5},dyn);
cx.forEach(function(e){K.el("circle",{"class":"k-f2 c14-dot",cx:B.X(e[0]),cy:B.Y(e[1]),r:5.5},dyn);});
r.forEach(function(e){if(e[1]>1){K.el("circle",{"class":"c14-dbl",cx:B.X(e[0]),cy:B.Y(0),r:11},dyn);}K.el("circle",{"class":"k-f1 c14-dot",cx:B.X(e[0]),cy:B.Y(0),r:e[1]>1?7:5.5},dyn);});
s=Math.abs(Math.abs(a)-AS)<1e-12?(a>0?"a = a* ≈ 0,535: ":"a = −a* ≈ −0,535: "):"a = "+K.num(a)+": ";
if(r.length===3){d=s+"три вещественных корня, "+r.map(function(e){return K.num(e[0]);}).join("; ")+"; и пара комплексных";}
else if(r.length===2){r.sort(function(p,q){return q[1]-p[1];});d=s+"двойной корень "+K.num(r[0][0])+", простой "+K.num(r[1][0])+" и пара комплексных";}
else{d=s+"один вещественный корень "+K.num(r[0][0])+" и две пары комплексных";}
out.textContent=d;}
function set(e){var p=K.pt(svg,e),v=Math.max(-0.95,Math.min(0.95,A.iy(p.y)));if(Math.abs(Math.abs(v)-AS)<0.02){v=v>0?AS:-AS;}a=v;draw();}
svg.addEventListener("pointerdown",function(e){var p=K.pt(svg,e);if(p.x<A.x0+A.w+12){drag=true;svg.setPointerCapture(e.pointerId);set(e);}});
svg.addEventListener("pointermove",function(e){if(drag){set(e);}});
svg.addEventListener("pointerup",function(){drag=false;});
draw();
})();
