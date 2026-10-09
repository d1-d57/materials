(function(){
var K=window.SimK,root=document.getElementById("sim-c0");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),cnt=root.querySelector(".c0-cnt"),inN=root.querySelector(".c0-n"),inK=root.querySelector(".c0-k"),vN=root.querySelector(".c0-nv"),vK=root.querySelector(".c0-kv");
var n=+inN.value,k=+inK.value,W=600,G=null,run=null,hl=-1;
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
/* {1, 3}; пустой набор — { } */
function setStr(a){return a.length?"{"+a.join(", ")+"}":"{ }";}
function listStr(a){return a.length<2?String(a[0]):a.slice(0,-1).join(", ")+" и "+a[a.length-1];}
/* ширина подписи набора: меряем прямо в рисунке, при неудаче — оценка */
function measure(s){var e=txt("c0-set",0,-40,s,svg,"start"),w=0;try{w=e.getComputedTextLength();}catch(x){w=0;}svg.removeChild(e);return w>0?w:s.length*8.6;}
/* fade — мягкое появление строк (только при смене ползунков) */
function build(fade){
if(run){run.stop();run=null;}hl=-1;K.clear(svg);
var ws=K.words(n,k),N=ws.length,sets=ws.map(K.nabor),i,q,big=[];
for(i=1;i<=k;i++){big.push(i);}
var rp=W<480?28:30,c=rp-10,cp=c+4,cw=n*cp-4,lw=Math.max(24,Math.ceil(measure(setStr(big)))),gap=24,pad=10,bw=pad+lw+gap+cw+pad,cg=32;
var cols=(N>6&&2*bw+cg<=W)?2:1,rpc=Math.ceil(N/cols),top=24,H=top+rpc*rp+2;
var x0=Math.round((W-(cols*bw+(cols-1)*cg))/2);
svg.setAttribute("viewBox","0 0 "+W+" "+H);svg.setAttribute("data-cols",cols);
var gT=K.el("g",{},svg),gR=K.el("g",{},svg),heads=[],rows=[];
/* над кодами — номера мест 1..n */
for(q=0;q<cols;q++){var hs=[],hx=x0+q*(bw+cg)+pad+lw+gap;for(i=0;i<n;i++){hs.push(txt("c0-pos",hx+i*cp+c/2,top-8,String(i+1),gT));}heads.push(hs);}
ws.forEach(function(w,i){var col=Math.floor(i/rpc),r=i%rpc,bx=x0+col*(bw+cg),y=top+r*rp,cy=y+rp/2,j;
var g=K.el("g",{"class":"w-word c0-row","data-i":i},gR);
K.el("rect",{"class":"c0-zebra"+(r%2?" odd":""),x:bx,y:y+1,width:bw,height:rp-2,rx:5},g);
K.el("rect",{"class":"w-frame",x:bx+1,y:y+2,width:bw-2,height:rp-4,rx:5},g);
txt("c0-set",bx+pad,cy+5.5,setStr(sets[i]),g,"start");
for(j=0;j<n;j++){K.el("rect",{"class":"w-c"+(w[j]?" on":""),x:bx+pad+lw+gap+j*cp,y:cy-c/2,width:c,height:c,rx:3},g);}
K.el("rect",{"class":"w-hit",x:bx,y:y,width:bw,height:rp},g);
rows.push(g);});
G={ws:ws,sets:sets,rows:rows,heads:heads,rpc:rpc};
cnt.innerHTML="вариантов: <b>"+N+"</b>";
say();
if(fade&&!K.reduced()){var N1=Math.max(1,N-1);
rows.forEach(function(g){g.setAttribute("opacity","0");});
run=K.anim(320+18*N,function(t){rows.forEach(function(g,i){var a=0.55*i/N1,v=K.seg(t,a,a+0.45);g.setAttribute("opacity",v.toFixed(3));g.setAttribute("transform","translate(0,"+((1-v)*6).toFixed(2)+")");});},function(){run=null;rows.forEach(function(g){g.removeAttribute("opacity");g.removeAttribute("transform");});});}}
function say(){var s;
if(hl<0){s='<span class="w-dim">'+(k===0?"вариант один: не выбрать ничего":"наведите на строку или коснитесь её")+"</span>";}
else{var a=G.sets[hl];
s='<span class="c0-pair">'+setStr(a)+" ↔ "+K.key(G.ws[hl])+":</span> "+'<span class="c0-pair">'+(a.length===0?"единиц нет — ничего не выбрано":(a.length===1?"на месте "+a[0]+" — единица":"на местах "+listStr(a)+" — единицы"))+"</span>";}
out.innerHTML=s;}
function setHL(i){hl=i;var col=i<0?-1:Math.floor(i/G.rpc),w=i<0?null:G.ws[i];
G.rows.forEach(function(g,q){g.classList.toggle("hl",q===i);});
G.heads.forEach(function(hs,c){hs.forEach(function(e,p){e.classList.toggle("hl",c===col&&!!w[p]);});});
say();}
function pick(e){var g=e.target.closest?e.target.closest(".c0-row"):null;return g?+g.getAttribute("data-i"):-1;}
svg.addEventListener("pointerover",function(e){var i=pick(e);if(i>=0&&i!==hl){setHL(i);}});
svg.addEventListener("pointerdown",function(e){var i=pick(e);if(i>=0){setHL(i);}else if(hl>=0){setHL(-1);}});
svg.addEventListener("pointerleave",function(e){if(e.pointerType==="mouse"&&hl>=0){setHL(-1);}});
function upd(){n=+inN.value;inK.max=n;k=Math.min(+inK.value,n);inK.value=k;vN.textContent=n;vK.textContent=k;build(true);}
inN.addEventListener("input",upd);inK.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build(false);});
})();
