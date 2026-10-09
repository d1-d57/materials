(function(){
var K=window.SimK,root=document.getElementById("sim-c1");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c1-n"),inK=root.querySelector(".c1-k"),vN=root.querySelector(".c1-nv"),vK=root.querySelector(".c1-kv"),btn=root.querySelector(".c1-go");
var n=5,k=2,W=600,L=[],R=[],part=[],G=null,t=0,run=null,hl=null;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
function build(){
if(run){run.stop();run=null;}t=0;hl=null;btn.textContent="отразить";btn.disabled=false;
K.clear(svg);
var N=K.C(n,k),sym=(2*k===n),i,j;
L=K.words(n,k);R=K.words(n,n-k);
var idx={};R.forEach(function(w,i){idx[K.key(w)]=i;});
part=L.map(function(w){return idx[K.key(K.flip(w))];});
var top=70,rp=K.cl(480/N,13,30),arcS=sym?Math.min(58,12+N*2.2):6;
var cp=Math.min(rp,24,((W-2*arcS-70)/2)/n),c=Math.min(cp-Math.max(2,cp*0.17),rp-3);
var ww=n*cp-(cp-c),mid=Math.min(W-2*arcS-2*ww,300),x0=(W-(2*ww+mid))/2,xL=x0,xR=x0+ww+mid;
var H=top+N*rp+8;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
function yc(i){return top+i*rp+rp/2;}
var gA=K.el("g",{},svg),gK=K.el("g",{},svg),gR=K.el("g",{},svg),gL=K.el("g",{},svg),gF=K.el("g",{"class":"c1-flyg",style:"display:none"},svg),gH=K.el("g",{},svg);
/* заголовки: сколько закрашено и сколько слов */
txt("w-lab",xL+ww/2,20,"закрашено "+k,gH);txt("w-lab",xR+ww/2,20,"закрашено "+(n-k),gH);
txt("w-num",xL+ww/2,52,String(N),gH);txt("w-num",xR+ww/2,52,String(N),gH);txt("w-eq",W/2,52,"=",gH);
var links=[];
for(i=0;i<N;i++){links.push(K.el("line",{"class":"w-link",x1:xL+ww+6,y1:yc(i),x2:xR-6,y2:yc(part[i])},gK));}
var arcs=[];
if(sym){var bmax=arcS-8;for(i=0;i<N;i++){j=part[i];if(j<=i){continue;}var b=6+(j-i)/(N-1)*(bmax-6),xa=xL-6,xb=xR+ww+6;
arcs.push({a:i,b:j,l:K.el("path",{"class":"c1-arc",d:"M"+xa+","+yc(i)+" C"+(xa-b*1.33)+","+yc(i)+" "+(xa-b*1.33)+","+yc(j)+" "+xa+","+yc(j)},gA),r:K.el("path",{"class":"c1-arc",d:"M"+xb+","+yc(i)+" C"+(xb+b*1.33)+","+yc(i)+" "+(xb+b*1.33)+","+yc(j)+" "+xb+","+yc(j)},gA)});}}
/* side "L"/"R" — слово с рамкой и зоной касания; side "" — летящая копия левого слова */
function word(w,x,i,par,side){var g=K.el("g",{"class":side?"w-word":"c1-fly","data-side":side||"F","data-i":i},par),cells=[],q;
if(side){K.el("rect",{"class":"w-frame",x:x-3.5,y:yc(i)-c/2-3.5,width:ww+7,height:c+7,rx:4},g);}
for(q=0;q<n;q++){var cx=x+q*cp+c/2;cells.push({e:K.el("rect",{"class":"w-c"+(w[q]?" on":""),x:cx-c/2,y:yc(i)-c/2,width:c,height:c,rx:Math.min(3,c*0.18)},g),cx:cx,b:w[q]});}
if(side){K.el("rect",{"class":"w-hit",x:x-4,y:yc(i)-rp/2,width:ww+8,height:rp},g);}
return {g:g,cells:cells};}
var WL=L.map(function(w,i){return word(w,xL,i,gL,"L");}),WR=R.map(function(w,i){return word(w,xR,i,gR,"R");}),WF=L.map(function(w,i){return word(w,xL,i,gF,"");});
G={N:N,sym:sym,xL:xL,xR:xR,ww:ww,c:c,yc:yc,links:links,arcs:arcs,WL:WL,WR:WR,WF:WF,gR:gR,gF:gF};
say();}
/* левые слова остаются на месте (приглушаются), их копии отражаются в полёте и садятся на правые слова */
function frame(tt){t=tt;var N1=Math.max(1,G.N-1),dx=G.xR-G.xL,dim=(1-0.6*K.seg(tt,0,0.25)).toFixed(3);
G.gF.style.display=tt>0?"":"none";
G.WL.forEach(function(o){o.g.setAttribute("opacity",dim);});
G.WF.forEach(function(o,i){var a0=0.04+0.42*i/N1,v=K.seg(tt,a0,a0+0.54),u=K.cl((v-0.2)/0.6,0,1),sx=Math.abs(Math.cos(Math.PI*u)),fl=(u>=0.5);
o.cells.forEach(function(c){var on=fl?!c.b:c.b,w=G.c*sx;c.e.setAttribute("x",c.cx-w/2);c.e.setAttribute("width",Math.max(w,0.01));c.e.setAttribute("class","w-c"+(on?" on":""));});
o.g.setAttribute("transform","translate("+(dx*v).toFixed(2)+","+((G.yc(part[i])-G.yc(i))*v).toFixed(2)+")");});
G.gR.setAttribute("opacity",(1-0.55*K.seg(tt,0.3,1)).toFixed(3));
var lo=(1-0.85*K.cl(tt/0.4,0,1)).toFixed(3);G.links.forEach(function(e){e.setAttribute("opacity",lo);});}
function setHL(side,i){hl=(side===null)?null:{l:side==="L"?i:part.indexOf(i)};
var li=hl?hl.l:-1,ri=hl?part[li]:-1;
G.WL.forEach(function(o,q){o.g.classList.toggle("hl",q===li);});G.WR.forEach(function(o,q){o.g.classList.toggle("hl",q===ri);});
G.links.forEach(function(e,q){e.classList.toggle("hl",q===li);});
G.arcs.forEach(function(a){var on=hl&&((a.a===li||a.b===li));a.l.classList.toggle("hl",!!on);a.r.classList.toggle("hl",!!on);});
say();}
function say(){var N=G.N,s=K.bn(n,k)+" = "+N+" = "+K.bn(n,n-k);
if(G.sym){s+='<br><span class="w-dim">те же слова, но ни одно не переходит в&nbsp;себя: '+(N/2)+"&nbsp;"+K.pl(N/2,"пара","пары","пар")+"</span>";}
if(hl){var a=K.key(L[hl.l]),b=K.key(R[part[hl.l]]);s+='<br><span class="w-dim">'+a+" ↔ "+b+"</span>";}
out.innerHTML=s;}
function pick(e){var g=e.target.closest?e.target.closest(".w-word"):null;if(!g||run){return null;}return g;}
svg.addEventListener("pointerover",function(e){var g=pick(e);if(g){setHL(g.getAttribute("data-side"),+g.getAttribute("data-i"));}});
svg.addEventListener("pointerdown",function(e){var g=pick(e);if(g){setHL(g.getAttribute("data-side"),+g.getAttribute("data-i"));}else if(hl){setHL(null);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl){setHL(null);}});
btn.addEventListener("click",function(){if(run){return;}if(hl){setHL(null);}var from=t,to=(t>0.5)?0:1;btn.disabled=true;
run=K.anim(1500+40*G.N,function(s){frame(from+(to-from)*s);},function(){run=null;btn.disabled=false;btn.textContent=to?"вернуть":"отразить";});});
function upd(){n=+inN.value;inK.max=n;k=Math.min(+inK.value,n);inK.value=k;vN.textContent=n;vK.textContent=k;build();}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();
