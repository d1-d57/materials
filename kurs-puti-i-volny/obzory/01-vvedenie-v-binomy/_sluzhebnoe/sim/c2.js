(function(){
var K=window.SimK,root=document.getElementById("sim-c2");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c2-n"),inK=root.querySelector(".c2-k"),vN=root.querySelector(".c2-nv"),vK=root.querySelector(".c2-kv"),go=root.querySelector(".c2-go"),back=root.querySelector(".c2-back");
var n=5,k=2,W=600,G=null,t=0,run=null;
function txt(cls,x,y,s,par){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":"middle"},par);e.textContent=s;return e;}
function build(){
if(run){run.stop();run=null;}t=0;K.clear(svg);
var ws=K.words(n,k),N=ws.length,a=K.C(n-1,k-1),b=K.C(n-1,k);
/* вперемешку: по убыванию перевёрнутого слова, чтобы первая цифра чередовалась */
var mix=ws.map(function(w,i){return i;}).sort(function(p,q){var A=ws[p].slice().reverse().join(""),B=ws[q].slice().reverse().join("");return A<B?1:(A>B?-1:0);});
var rp=W<480?24:27,c=Math.min(19,rp-6,((W*0.44)-3*(n-1))/n),cp=c+3,ww=n*cp-3,top=88;
var cols=N>Math.max(a,b)?2:1,rowsA=Math.ceil(N/cols),gapA=22,bw=cols*ww+(cols-1)*gapA,xA=(W-bw)/2;
var off=Math.min(W*0.24,175),cx1=W/2-off,cx0=W/2+off;
var rows=Math.max(rowsA,a,b),H=top+rows*rp+4;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
var hA=K.el("g",{},svg),hB=K.el("g",{opacity:0},svg),gw=K.el("g",{},svg);
txt("w-lab",W/2,40,"длина "+n+", закрашено "+k,hA);txt("w-num",W/2,74,String(N),hA);
/* подписи кучек держатся до сброса; после стирания первой клетки под ними проявляется «длина n−1, закрашено …» */
txt("w-lab",cx1,18,"первая закрашена",hB);txt("w-lab",cx0,18,"первая пустая",hB);
var lc1=txt("w-lab",cx1,40,"длина "+(n-1)+", закрашено "+(k-1),hB),lc0=txt("w-lab",cx0,40,"длина "+(n-1)+", закрашено "+k,hB);
txt("w-num",cx1,74,String(a),hB);txt("w-num",cx0,74,String(b),hB);txt("w-eq",W/2,74,"+",hB);
var items=[];
mix.forEach(function(wi,q){var w=ws[wi],g=K.el("g",{},gw),cells=[],j;
for(j=0;j<n;j++){cells.push(K.el("rect",{"class":"w-c"+(w[j]?" on":"")+(j===0?" c2-first":""),x:j*cp,y:-c/2,width:c,height:c,rx:Math.min(3,c*0.18)},g));}
var A={x:xA+(q%cols)*(ww+gapA),y:top+Math.floor(q/cols)*rp+rp/2},B;
var r=0;ws.forEach(function(v,z){if(z<wi&&v[0]===w[0]){r++;}});B={x:(w[0]?cx1:cx0)-ww/2,y:top+r*rp+rp/2};
items.push({g:g,first:cells[0],A:A,B:B,d:q/Math.max(1,N-1)});});
G={N:N,a:a,b:b,cp:cp,items:items,hA:hA,hB:hB,lc:[lc1,lc0]};
frame(0);go.disabled=false;back.disabled=true;say(false);}
function frame(tt){t=tt;var sh=K.seg(tt,0.72,1)*(-G.cp/2),fo=1-K.seg(tt,0.64,0.84),sw=K.seg(tt,0.7,0.86);
G.items.forEach(function(it){var a0=0.04+0.3*it.d,m=K.seg(tt,a0,a0+0.28),x=it.A.x+(it.B.x-it.A.x)*m+sh*m,y=it.A.y+(it.B.y-it.A.y)*m;
it.g.setAttribute("transform","translate("+x.toFixed(2)+","+y.toFixed(2)+")");it.first.setAttribute("opacity",fo.toFixed(3));});
G.hA.setAttribute("opacity",(1-K.seg(tt,0,0.15)).toFixed(3));G.hB.setAttribute("opacity",K.seg(tt,0.5,0.64).toFixed(3));
G.lc.forEach(function(e){e.setAttribute("opacity",sw.toFixed(3));});}
function say(done){var s=K.bn(n,k)+" = "+G.N;
if(done){s=K.bn(n,k)+" = "+K.bn(n-1,k-1)+" + "+K.bn(n-1,k)+'<br><span class="w-dim">'+G.N+" = "+G.a+" + "+G.b+"</span>";}
out.innerHTML=s;}
function play(to){if(run){return;}var from=t;go.disabled=true;back.disabled=true;if(!to){say(false);}
run=K.anim(2600,function(s){frame(from+(to-from)*s);},function(){run=null;go.disabled=!!to;back.disabled=!to;say(!!to);});}
go.addEventListener("click",function(){play(1);});back.addEventListener("click",function(){play(0);});
function upd(){n=+inN.value;inK.max=n-1;k=Math.min(+inK.value,n-1);inK.value=k;vN.textContent=n;vK.textContent=k;build();}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();
