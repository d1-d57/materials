(function(){
var K=window.SimK,root=document.getElementById("sim-c6");
if(!root||!K){return;}
var wrap=root.querySelector(".c6-3d"),msg=root.querySelector(".c6-msg"),svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".sim-bar button"),ins=root.querySelectorAll(".c6-sl input"),ovs=root.querySelectorAll(".c6-sl output");
var RG=[[-2.5,1.2],[-2.6,2.6],[-1.2,3.2]],P0=[-2,0,0.5],P=P0.slice(),V0=[0.55,0.4],view=V0.slice(),G=null,kind="--warm";
var Pn=new K.Panel(34,14,312,262,[-2.3,2.3],[-3,5]),st=K.el("g",{},svg),dyn=K.el("g",{},svg);
Pn.axes(st,"x","y");
function f(x){return x*(x*(x*x+P[0])+P[1])+P[2];}
function cub(p,q){var D=q*q/4+p*p*p/27,r=[],i,k;
if(D>1e-13){var s=Math.sqrt(D);r=[Math.cbrt(-q/2+s)+Math.cbrt(-q/2-s)];}else if(p<-1e-9){var m=2*Math.sqrt(-p/3),th=Math.acos(Math.max(-1,Math.min(1,1.5*q/p*Math.sqrt(-3/p))))/3;for(k=0;k<3;k++){r.push(m*Math.cos(th-2*Math.PI*k/3));}}else{r=[0];}
for(i=0;i<r.length;i++){for(k=0;k<4;k++){var d=3*r[i]*r[i]+p;if(Math.abs(d)>1e-9){r[i]-=(r[i]*r[i]*r[i]+p*r[i]+q)/d;}}}
r.sort(function(u,v){return u-v;});return r;}
function roots(){var cr=cub(P[0]/2,P[1]/4),cs=[],i,j,R=1+Math.max(Math.abs(P[0]),Math.abs(P[1]),Math.abs(P[2])),tol=1e-5,res=[];
if(cr.length===1&&Math.abs(P[0])<1e-9&&Math.abs(P[1])<1e-9){cs=[{x:0,n:3}];}else{for(i=0;i<cr.length;i++){if(cs.length&&Math.abs(cr[i]-cs[cs.length-1].x)<2e-3){cs[cs.length-1].n++;}else{cs.push({x:cr[i],n:1});}}}
var nd=[{x:-R,v:f(-R)}];cs.forEach(function(c){var v=f(c.x);nd.push({x:c.x,v:v,z:Math.abs(v)<tol});if(Math.abs(v)<tol){res.push({x:c.x,m:c.n+1});}});nd.push({x:R,v:f(R)});
for(i=0;i+1<nd.length;i++){var u=nd[i],w=nd[i+1];if(!u.z&&!w.z&&u.v*w.v<0){var lo=u.x,hi=w.x,fl=u.v;for(j=0;j<70;j++){var mi=(lo+hi)/2,fm=f(mi);if(fm*fl>0){lo=mi;fl=fm;}else{hi=mi;}}res.push({x:(lo+hi)/2,m:1});}}
res.sort(function(u,v){return u.x-v.x;});return res;}
function poly(){var a=P[0],b=P[1],c=P[2];return "x⁴ "+(a<-0.004?"− ":"+ ")+K.num(Math.abs(a))+"x² "+(b<-0.004?"− ":"+ ")+K.num(Math.abs(b))+"x "+(c<-0.004?"− ":"+ ")+K.num(Math.abs(c));}
function words(rs){var mu=rs.filter(function(r){return r.m>1;}),s=rs.length-mu.length;
if(!mu.length){return s===4?"четыре вещественных корня":(s===2?"два вещественных корня":"вещественных корней нет");}
if(mu.length===2){return "кратные корни: два двойных, точка P на линии самопересечения";}
var m=mu[0].m,nm=m===2?"двойной":(m===3?"тройной":"четвёртой кратности");
return "кратный корень ("+nm+")"+(s===2?" и ещё два простых":(s===1?" и ещё простой":", других вещественных нет"))+", точка P на поверхности";}
function draw2d(rs){K.clear(dyn);var g=[],x;for(x=-2.3;x<=2.3001;x+=0.01){g.push([x,f(x)]);}
K.el("path",{"class":"k-curve",d:Pn.d(g)},dyn);
rs.forEach(function(r){if(r.m>1){K.el("circle",{"class":"k-ring",cx:Pn.X(r.x),cy:Pn.Y(0),r:11},dyn);K.el("circle",{"class":"k-c6r",cx:Pn.X(r.x),cy:Pn.Y(0),r:5.5},dyn);}else{K.el("circle",{"class":rs.length===4?"k-f2":"k-f1",cx:Pn.X(r.x),cy:Pn.Y(0),r:5.5},dyn);}});}
function update(){var rs=roots(),mu=rs.some(function(r){return r.m>1;});
kind=mu?"--text":(rs.length===4?"--warm":(rs.length===2?"--accent":"--muted"));
draw2d(rs);out.textContent=poly()+": "+words(rs);
P.forEach(function(v,i){ins[i].value=v;ovs[i].textContent=K.num(v);});
if(G){G.place();}}
function setP(q){P=q.slice();update();}
ins.forEach(function(inp,i){inp.addEventListener("input",function(){P[i]=Math.round(parseFloat(inp.value)*100)/100;update();});});
bs[0].addEventListener("click",function(){setP([-2,0,0.5]);});
bs[1].addEventListener("click",function(){setP([-2,0,-1]);});
bs[2].addEventListener("click",function(){setP([-2,0,3]);});
bs[3].addEventListener("click",function(){view=V0.slice();setP(P0);if(G){G.req();}});
update();
function col(n,fb){var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||fb;}
function fail(){msg.textContent="трёхмерная картинка не загрузилась, а график и ползунки работают";}
function init3d(){var T=window.THREE;
var KA=0.6,KB=0.42,KC=0.42,A0=(RG[0][0]+RG[0][1])/2,C0=(RG[2][0]+RG[2][1])/2,SZ=1;
function V(a,b,c){return new T.Vector3(b*KB,(c-C0)*KC,SZ*(a-A0)*KA);}
var rd;
try{rd=new T.WebGLRenderer({antialias:true,alpha:true});}catch(e){fail();return;}
rd.setPixelRatio(Math.min(2,window.devicePixelRatio||1));rd.setClearColor(0x000000,0);rd.localClippingEnabled=true;
msg.parentNode.removeChild(msg);wrap.appendChild(rd.domElement);
var sc=new T.Scene(),cam=new T.PerspectiveCamera(26,1,0.1,60);sc.add(cam);
sc.add(new T.AmbientLight(0xffffff,0.55));var dl=new T.DirectionalLight(0xffffff,0.6);dl.position.set(1.2,2.2,3);cam.add(dl);
var xm=RG[1][1]*KB,y0=(RG[2][0]-C0)*KC,y1=(RG[2][1]-C0)*KC,e=1e-3;
var planes=[new T.Plane(new T.Vector3(-1,0,0),xm+e),new T.Plane(new T.Vector3(1,0,0),xm+e),new T.Plane(new T.Vector3(0,-1,0),y1+e),new T.Plane(new T.Vector3(0,1,0),-y0+e)];
function tmax(a){var t=0;while(t<1.6){t+=0.004;var b=-4*t*t*t-2*a*t,c=3*t*t*t*t+a*t*t;if(Math.abs(b)>RG[1][1]||c>RG[2][1]){break;}}return Math.min(1.6,t+0.012);}
var NA=110,NT=200,pos=[],nor=[],idx=[],i,j;
for(i=0;i<=NA;i++){var a=RG[0][0]+(RG[0][1]-RG[0][0])*i/NA,tm=tmax(a);for(j=0;j<=NT;j++){var t=tm*(2*j/NT-1),p=V(a,-4*t*t*t-2*a*t,3*t*t*t*t+a*t*t);pos.push(p.x,p.y,p.z);
var ux=-2*t*KB,uy=t*t*KC,uz=SZ*KA,vx=KB,vy=-t*KC,nx=-uz*vy,ny=uz*vx,nz=ux*vy-uy*vx,nl=Math.sqrt(nx*nx+ny*ny+nz*nz)||1;nor.push(nx/nl,ny/nl,nz/nl);}}
for(i=0;i<NA;i++){for(j=0;j<NT;j++){var k=i*(NT+1)+j;idx.push(k,k+1,k+NT+1,k+1,k+NT+2,k+NT+1);}}
var geo=new T.BufferGeometry();geo.setAttribute("position",new T.Float32BufferAttribute(pos,3));geo.setAttribute("normal",new T.Float32BufferAttribute(nor,3));geo.setIndex(idx);
var mS=new T.MeshPhongMaterial({transparent:true,opacity:0.45,side:T.DoubleSide,depthWrite:false,shininess:20,specular:0x0c0c0c,clippingPlanes:planes});
sc.add(new T.Mesh(geo,mS));
var mE=new T.MeshBasicMaterial({}),mA=new T.LineBasicMaterial({}),mH=new T.MeshBasicMaterial({}),mB=new T.LineBasicMaterial({transparent:true,opacity:0.7}),mP=new T.MeshPhongMaterial({shininess:30,specular:0x1a1a1a});
function tube(F,n,t0,t1){var ps=[],q;for(q=0;q<=n;q++){ps.push(F(t0+(t1-t0)*q/n));}sc.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(ps),n*2,0.011,8,false),mE));}
var tc=Math.sqrt(2.5/6);
tube(function(t){return V(-6*t*t,8*t*t*t,-3*t*t*t*t);},80,0,tc);
tube(function(t){return V(-6*t*t,8*t*t*t,-3*t*t*t*t);},80,0,-tc);
tube(function(s){return V(s,0,s*s/4);},80,0,-2.5);
var ax=[[V(RG[0][0],0,0),V(RG[0][1],0,0)],[V(0,RG[1][0],0),V(0,RG[1][1],0)],[V(0,0,RG[2][0]),V(0,0,RG[2][1])]],nm=["a","b","c"],labs=[];
ax.forEach(function(s,q){var g=new T.BufferGeometry().setFromPoints(s);sc.add(new T.Line(g,mA));var dir=s[1].clone().sub(s[0]).normalize(),cone=new T.Mesh(new T.ConeGeometry(0.028,0.1,14),mH);cone.position.copy(s[1]).add(dir.clone().multiplyScalar(0.05));cone.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);sc.add(cone);
var l=document.createElement("span");l.className="c6-lab";l.textContent=nm[q];wrap.appendChild(l);labs.push({el:l,v:s[1].clone().add(dir.clone().multiplyScalar(0.2))});});
var bx=new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(2*xm,y1-y0,(RG[0][1]-RG[0][0])*KA)),mB);bx.position.set(0,(y0+y1)/2,0);sc.add(bx);
var sg=new T.SphereGeometry(0.06,28,18),ball=new T.Mesh(sg,mP),mG=new T.MeshPhongMaterial({transparent:true,opacity:0.92,depthTest:false,depthWrite:false,shininess:30,specular:0x1a1a1a}),ghost=new T.Mesh(sg,mG),mO=new T.MeshBasicMaterial({side:T.BackSide,transparent:true,opacity:0.75,depthTest:false,depthWrite:false}),rim=new T.Mesh(new T.SphereGeometry(0.078,28,18),mO);ghost.renderOrder=5;rim.renderOrder=4;sc.add(ball);sc.add(rim);sc.add(ghost);
var hint=document.createElement("span");hint.className="c6-hint";hint.textContent="тяните, чтобы повернуть";wrap.appendChild(hint);
var W=1,H=1,pend=false;
function size(){W=Math.max(1,wrap.clientWidth);H=Math.max(1,wrap.clientHeight);rd.setSize(W,H,false);cam.aspect=W/H;var vf=cam.fov*Math.PI/180,hf=2*Math.atan(Math.tan(vf/2)*cam.aspect);cam.userData.d=1.62/Math.sin(Math.min(vf,hf)/2);cam.updateProjectionMatrix();}
function render(){var d=cam.userData.d,th=view[0],ph=view[1];cam.position.set(d*Math.cos(ph)*Math.sin(th),d*Math.sin(ph),d*Math.cos(ph)*Math.cos(th));cam.lookAt(0,0.02,0);cam.updateMatrixWorld();rd.render(sc,cam);
labs.forEach(function(L){var q=L.v.clone().project(cam);L.el.style.left=((q.x+1)/2*W).toFixed(1)+"px";L.el.style.top=((1-q.y)/2*H).toFixed(1)+"px";});}
function req(){if(!pend){pend=true;requestAnimationFrame(function(){pend=false;render();});}}
function recolor(){mS.color.set(col("--accent","#2f6e8e"));mE.color.set(col("--text","#211f1b"));mA.color.set(col("--muted","#726c60"));mH.color.set(col("--muted","#726c60"));mB.color.set(col("--rule","#e7e2d6"));mO.color.set(col("--panel","#fffdf8"));mP.color.set(col(kind,"#c9743a"));mG.color.set(col(kind,"#c9743a"));req();}
function place(){var p=V(P[0],P[1],P[2]);ball.position.copy(p);ghost.position.copy(p);rim.position.copy(p);mP.color.set(col(kind,"#c9743a"));mG.color.set(col(kind,"#c9743a"));req();}
G={place:place,req:req};
var dr=null;
wrap.addEventListener("pointerdown",function(ev){dr={x:ev.clientX,y:ev.clientY};wrap.setPointerCapture(ev.pointerId);wrap.classList.add("c6-drag");ev.preventDefault();});
wrap.addEventListener("pointermove",function(ev){if(!dr){return;}view[0]-=(ev.clientX-dr.x)*0.009;view[1]=Math.max(-1.35,Math.min(1.35,view[1]+(ev.clientY-dr.y)*0.009));dr={x:ev.clientX,y:ev.clientY};req();});
function up(){dr=null;wrap.classList.remove("c6-drag");}
wrap.addEventListener("pointerup",up);wrap.addEventListener("pointercancel",up);
if(window.ResizeObserver){new ResizeObserver(function(){size();req();}).observe(wrap);}else{window.addEventListener("resize",function(){size();req();});}
new MutationObserver(recolor).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme","class","style"]});
var mq=window.matchMedia?window.matchMedia("(prefers-color-scheme: dark)"):null;
if(mq){if(mq.addEventListener){mq.addEventListener("change",recolor);}else if(mq.addListener){mq.addListener(recolor);}}
size();recolor();place();}
if(window.THREE&&window.THREE.WebGLRenderer){init3d();}else{var src="https:"+"/"+"/cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",sc0=document.querySelector("script[data-three-r128]");
var ok=function(){if(window.THREE&&window.THREE.WebGLRenderer){init3d();}else{fail();}};
if(sc0){if(window.THREE){ok();}else{sc0.addEventListener("load",ok);sc0.addEventListener("error",fail);}}else{sc0=document.createElement("script");sc0.src=src;sc0.async=true;sc0.setAttribute("data-three-r128","1");sc0.addEventListener("load",ok);sc0.addEventListener("error",fail);document.head.appendChild(sc0);}}
})();
