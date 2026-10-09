(function(){
var K=window.SimK,root=document.getElementById("sim-c5");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c5-n"),vN=root.querySelector(".c5-nv"),bGo=root.querySelector(".c5-go"),bSh=root.querySelector(".c5-sh"),bRs=root.querySelector(".c5-rs");
var n=5,W=600,G=null,T=0,run=null,hl=null;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
/* T: 0 — одна лесенка; 0→1 — отражение (j,i); 1→2 — сдвиг нижней лесенки на ряд вверх */
function build(){
if(run){run.stop();run=null;}T=0;hl=null;K.clear(svg);
var lw=30,s=Math.floor(Math.min(50,(W-lw-14)/n)),x0=Math.round((W-lw-n*s)/2+lw),y0=38,gp=Math.max(2,Math.round(s*0.07)),H=y0+n*s+10,r,c;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
svg.setAttribute("data-x0",x0);svg.setAttribute("data-y0",y0);svg.setAttribute("data-s",s);svg.setAttribute("data-gp",gp);
var gG=K.el("g",{},svg),gT=K.el("g",{},svg),gU=K.el("g",{},svg),gD=K.el("g",{},svg),gM=K.el("g",{opacity:0},svg);
for(r=1;r<=n;r++){for(c=1;c<=n;c++){K.el("rect",{"class":"c5-g"+(r===c?" c5-diag":""),x:x0+(c-1)*s+gp,y:y0+(r-1)*s+gp,width:s-2*gp,height:s-2*gp,rx:3},gG);}}
var rows=[],cols=[];
for(r=1;r<=n;r++){rows.push(txt("c5-l",x0-10,y0+(r-0.5)*s+5,String(r),gT,"end"));cols.push(txt("c5-l",x0+(r-0.5)*s,y0-10,String(r),gT));}
/* размеры прямоугольника: n по горизонтали, n−1 по вертикали */
var cx=x0+n*s/2,yt=y0-15,xl=x0-15,ym=y0+(n-1)*s/2,yb=y0+(n-1)*s;
K.el("path",{"class":"c5-dim",d:"M"+(x0+gp)+","+(yt-4)+" v8 M"+(x0+gp)+","+yt+" H"+(cx-12)+" M"+(cx+12)+","+yt+" H"+(x0+n*s-gp)+" M"+(x0+n*s-gp)+","+(yt-4)+" v8"},gM);
txt("c5-dl",cx,yt+5,String(n),gM);
K.el("path",{"class":"c5-dim",d:"M"+(xl-4)+","+(y0+gp)+" h8 M"+xl+","+(y0+gp)+" V"+(ym-13)+" M"+xl+","+(ym+13)+" V"+(yb-gp)+" M"+(xl-4)+","+(yb-gp)+" h8"},gM);
txt("c5-dl",xl,ym+6,String(n-1),gM);
var P=K.ladder(n),cw=s-2*gp;
var U=P.map(function(p,q){return K.el("rect",{"class":"c5-up","data-q":q,"data-s":"u",width:cw,height:cw,rx:3},gU);});
var D=P.map(function(p,q){return K.el("rect",{"class":"c5-dn","data-q":q,"data-s":"d",width:cw,height:cw,rx:3},gD);});
G={P:P,U:U,D:D,x0:x0,y0:y0,s:s,gp:gp,gG:gG,gM:gM,rows:rows,cols:cols};
U.forEach(function(e,q){var A=XY(P[q].u);e.setAttribute("x",A[0]);e.setAttribute("y",A[1]);});
frame(0);ui();say();}
function XY(rc){return [G.x0+(rc[1]-1)*G.s+G.gp,G.y0+(rc[0]-1)*G.s+G.gp];}
function frame(tt){T=tt;var u=K.seg(tt,1,2),span=Math.max(1,n-2);
G.D.forEach(function(e,q){var p=G.P[q],A=XY(p.u),B=XY(p.d1),C=XY(p.d2),x,y,o;
if(tt<=1){var a0=0.4*(p.j-p.i-1)/span,v=K.seg(tt,a0,a0+0.6);x=A[0]+(B[0]-A[0])*v;y=A[1]+(B[1]-A[1])*v;o=K.cl(v*5,0,1);}
else{x=B[0]+(C[0]-B[0])*u;y=B[1]+(C[1]-B[1])*u;o=1;}
e.setAttribute("x",x.toFixed(2));e.setAttribute("y",y.toFixed(2));e.setAttribute("opacity",o.toFixed(3));e.style.pointerEvents=(tt>=1)?"":"none";});
G.gG.setAttribute("opacity",(1-u).toFixed(3));
var lo=(1-K.seg(tt,1,1.5)).toFixed(3);G.rows.forEach(function(e){e.setAttribute("opacity",lo);});G.cols.forEach(function(e){e.setAttribute("opacity",lo);});
G.gM.setAttribute("opacity",K.seg(tt,1.5,2).toFixed(3));}
function ui(){var busy=!!run;bGo.disabled=busy||T!==0;bSh.disabled=busy||T!==1;bRs.disabled=busy||T===0;}
function ladderSum(){var a=[],i;for(i=n-1;i>=1;i--){a.push(i);}return a.join(" + ");}
function say(){var N=n*(n-1),s;
if(T===0){s="лесенка: "+(n>2?ladderSum()+" = ":"")+"<b>"+N/2+"</b>";}
else if(T===1){s="две лесенки: упорядоченные пары (<i>i</i>, <i>j</i>), <i>i</i>&nbsp;≠&nbsp;<i>j</i>&nbsp;— <span class=\"c5-nw\">"+n+" · "+(n-1)+" = <b>"+N+"</b></span>";}
else{s="прямоугольник "+(n-1)+" × "+n+" из двух лесенок:<br><span class=\"c5-nw\">2 · "+K.bn(n,2)+" = 2 · <b>"+N/2+"</b> = "+(n-1)+" · "+n+" = "+N+" "+K.pl(N,"клетка","клетки","клеток")+"</span>";}
if(hl){var p=G.P[hl.q];s+='<br><span class="w-dim">'+(hl.s==="u"?(T>=1?"("+p.i+", "+p.j+") — ":"")+"пара {"+p.i+", "+p.j+"}":"("+p.j+", "+p.i+") — та же пара, другой порядок")+"</span>";}
out.innerHTML=s;}
function setHL(h){hl=h;var q=h?h.q:-1,both=T>=1,lab=h&&T<1.5,r=-1,c=-1;
if(h){var p=G.P[q];r=h.s==="u"?p.i:p.j;c=h.s==="u"?p.j:p.i;}
G.U.forEach(function(e,z){e.classList.toggle("hl",z===q&&(h.s==="u"||both));});
G.D.forEach(function(e,z){e.classList.toggle("hl",z===q&&both);});
G.rows.forEach(function(e,z){e.classList.toggle("hl",!!lab&&z===r-1);});G.cols.forEach(function(e,z){e.classList.toggle("hl",!!lab&&z===c-1);});
say();}
function pick(e){var t=e.target,q=t.getAttribute?t.getAttribute("data-q"):null;if(q===null||run){return null;}return {q:+q,s:t.getAttribute("data-s")};}
svg.addEventListener("pointerover",function(e){var h=pick(e);if(h){setHL(h);}});
svg.addEventListener("pointerdown",function(e){var h=pick(e);if(h){setHL(h);}else if(hl){setHL(null);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl){setHL(null);}});
function go(to,ms){if(run){return;}if(hl){setHL(null);}var from=T;
run=K.anim(ms,function(x){frame(from+(to-from)*x);},function(){run=null;frame(to);ui();say();});ui();}
bGo.addEventListener("click",function(){go(1,1700);});
bSh.addEventListener("click",function(){go(2,1300);});
bRs.addEventListener("click",function(){go(0,T>1?1500:1000);});
inN.addEventListener("input",function(){n=+inN.value;vN.textContent=n;build();});
K.onWidth(root,function(w){W=w;build();});
})();
