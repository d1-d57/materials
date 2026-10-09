(function(){
var K=window.SimK,root=document.getElementById("sim-c3");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c3-n"),inM=root.querySelector(".c3-m"),vN=root.querySelector(".c3-nv"),vM=root.querySelector(".c3-mv"),bs=root.querySelectorAll(".c3-b");
var n=6,m=3,W=600,mode=0,G=null,run=null,Hc=0;
function star(cx,cy,R){var p=[],i;for(i=0;i<10;i++){var a=-Math.PI/2+i*Math.PI/5,r=i%2?R*0.45:R;p.push((cx+r*Math.cos(a)).toFixed(2)+","+(cy+r*Math.sin(a)).toFixed(2));}return p.join(" ");}
/* три способа разложить: ключ стопки и порядок стопок (0 — капитан, 1 — команда, 2 — рядовые) */
function stacks(cards,md){var ord=cards.map(function(c,i){return i;}),kf;
if(md===0){kf=function(c){return c.cap;};ord.sort(function(a,b){return cards[a].cap-cards[b].cap||(K.key(cards[a].team)<K.key(cards[b].team)?1:-1);});}
else if(md===1){kf=function(c){return K.key(c.team);};}
else{kf=function(c){var t=c.team.slice();t[c.cap]=0;return K.key(t);};ord.sort(function(a,b){var A=cards[a].team.slice(),B=cards[b].team.slice();A[cards[a].cap]=0;B[cards[b].cap]=0;A=K.key(A);B=K.key(B);return A<B?1:(A>B?-1:cards[a].cap-cards[b].cap);});}
var gs=K.groups(ord.map(function(i){return cards[i];}),kf);return gs.map(function(g){return g.map(function(j){return ord[j];});});}
function setH(h){Hc=h;svg.setAttribute("viewBox","0 0 "+W+" "+h.toFixed(1));}
function build(){
if(run){run.stop();run=null;}K.clear(svg);
var cards=K.cards(n,m),pc=W>=560?15:(W>=420?13:12),cw=n*pc+6,ch=pc+6,gy=3,gx=W>=560?16:12,rg=20,top=36;
var lay=[0,1,2].map(function(md){var st=stacks(cards,md),S=st.length,z=st[0].length,per=Math.max(1,Math.min(S,Math.floor((W+gx)/(cw+gx)))),rows=Math.ceil(S/per);per=Math.ceil(S/rows);
var sh=z*(ch+gy)-gy,x0=(W-(per*cw+(per-1)*gx))/2,pos=[];
var last=S-(rows-1)*per;st.forEach(function(g,s){var sh0=(Math.floor(s/per)===rows-1)?(per-last)*(cw+gx)/2:0;g.forEach(function(ci,j){pos[ci]={x:x0+sh0+(s%per)*(cw+gx),y:top+Math.floor(s/per)*(sh+rg)+j*(ch+gy),d:(s*z+j)/Math.max(1,cards.length-1)};});});
return {S:S,z:z,pos:pos,H:top+rows*sh+(rows-1)*rg+6};});
/* высота рисунка — по активной раскладке: под низкими стопками нет пустой полосы */
setH(lay[mode].H);
var lab=K.el("text",{"class":"w-lab",x:W/2,y:20,"text-anchor":"middle"},svg),gc=K.el("g",{},svg);
var items=cards.map(function(c,i){var g=K.el("g",{},gc),q,y=ch/2;K.el("rect",{"class":"c3-card",x:0.5,y:0.5,width:cw-1,height:ch-1,rx:4},g);
for(q=0;q<n;q++){var x=3+pc/2+q*pc;if(q===c.cap){K.el("polygon",{"class":"c3-cap",points:star(x,y,pc*0.5)},g);}else if(c.team[q]){K.el("circle",{"class":"c3-m",cx:x,cy:y,r:pc*0.33},g);}else{K.el("circle",{"class":"c3-o",cx:x,cy:y,r:pc*0.3},g);}}
var p=lay[mode].pos[i];g.setAttribute("transform","translate("+p.x+","+p.y+")");return {g:g,x:p.x,y:p.y};});
G={cards:cards,lay:lay,items:items,lab:lab,ch:ch};say();}
/* строка вывода: три произведения в порядке кнопок, над числами — их биномиальная запись; активное выделено */
function say(){var L=G.lay[mode],k=m-1,N=G.cards.length;
G.lab.textContent=L.S+" "+K.pl(L.S,"стопка","стопки","стопок")+" по "+L.z+" "+K.pl(L.z,"карточке","карточки","карточек");
function w(md,f,v){return '<span class="c3-w'+(md===mode?" on":"")+'" data-m="'+md+'"><span class="c3-f">'+f+'</span><span class="c3-v">'+v+"</span></span>";}
var eq='<span class="c3-eq">=</span>';
out.innerHTML=w(0,n+"·"+K.bn(n-1,k),n+" · "+K.C(n-1,k))+eq+w(2,K.bn(n,k)+"·"+(n-k),K.C(n,k)+" · "+(n-k))+eq+w(1,K.bn(n,m)+"·"+m,K.C(n,m)+" · "+m)+eq+'<span class="c3-tot">'+N+"</span>";
bs.forEach(function(b){b.classList.toggle("on",+b.getAttribute("data-m")===mode);});}
function setMode(md){if(md===mode){return;}if(run){run.stop();}mode=md;say();var P=G.lay[mode].pos,from=G.items.map(function(it){return {x:it.x,y:it.y};}),H0=Hc,H1=G.lay[mode].H,ch=G.ch;
run=K.anim(1300,function(t){var bot=0;G.items.forEach(function(it,i){var a0=0.32*P[i].d,s=K.seg(t,a0,a0+0.68);it.x=from[i].x+(P[i].x-from[i].x)*s;it.y=from[i].y+(P[i].y-from[i].y)*s;bot=Math.max(bot,it.y+ch+6);it.g.setAttribute("transform","translate("+it.x.toFixed(2)+","+it.y.toFixed(2)+")");});
/* высота плавно идёт к новой, но не срезает карточки, которые ещё не долетели */
setH(t>=1?H1:Math.max(H0+(H1-H0)*K.ease(t),bot));},function(){run=null;});}
bs.forEach(function(b){b.addEventListener("click",function(){setMode(+b.getAttribute("data-m"));});});
function upd(){n=+inN.value;inM.max=n-1;m=K.cl(+inM.value,2,n-1);inM.value=m;inM.disabled=(n-1<=2);vN.textContent=n;vM.textContent=m;build();}
inN.addEventListener("input",upd);inM.addEventListener("input",upd);
K.onWidth(root,function(w){W=w;build();});
})();
