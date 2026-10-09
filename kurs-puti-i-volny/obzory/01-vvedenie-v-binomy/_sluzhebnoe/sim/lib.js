(function(){
var NS="http:"+"/"+"/www.w3.org/2000/svg";
function el(tag,attrs,parent){var e=document.createElementNS(NS,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(parent){parent.appendChild(e);}return e;}
function Panel(x0,y0,w,h,xr,yr){this.x0=x0;this.y0=y0;this.w=w;this.h=h;this.xr=xr;this.yr=yr;}
Panel.prototype.X=function(x){return this.x0+(x-this.xr[0])/(this.xr[1]-this.xr[0])*this.w;};
Panel.prototype.Y=function(y){return this.y0+this.h-(y-this.yr[0])/(this.yr[1]-this.yr[0])*this.h;};
Panel.prototype.ix=function(X){return this.xr[0]+(X-this.x0)/this.w*(this.xr[1]-this.xr[0]);};
Panel.prototype.iy=function(Y){return this.yr[0]+(this.y0+this.h-Y)/this.h*(this.yr[1]-this.yr[0]);};
Panel.prototype.inside=function(x,y){return x>=this.xr[0]&&x<=this.xr[1]&&y>=this.yr[0]&&y<=this.yr[1];};
Panel.prototype.d=function(pts){var s="",pen=false;for(var i=0;i<pts.length;i++){var x=pts[i][0],y=pts[i][1];if(this.inside(x,y)){s+=(pen?" L":" M")+this.X(x).toFixed(1)+","+this.Y(y).toFixed(1);pen=true;}else{pen=false;}}return s||"M0,0";};
Panel.prototype.axes=function(g,lx,ly){var X0=this.X(0),Y0=this.Y(0);el("line",{"class":"k-ax",x1:this.x0,y1:Y0,x2:this.x0+this.w,y2:Y0},g);el("line",{"class":"k-ax",x1:X0,y1:this.y0+this.h,x2:X0,y2:this.y0},g);el("path",{"class":"k-axh",d:"M"+(this.x0+this.w)+","+Y0+" l-8,-3.5 0,7 z"},g);el("path",{"class":"k-axh",d:"M"+X0+","+this.y0+" l-3.5,8 7,0 z"},g);if(lx){var t=el("text",{"class":"k-lab",x:this.x0+this.w-10,y:Y0+17},g);t.textContent=lx;}if(ly){var u=el("text",{"class":"k-lab",x:X0+8,y:this.y0+10},g);u.textContent=ly;}};
function mul(a,b){return [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
function sub(a,b){return [a[0]-b[0],a[1]-b[1]];}
function div(a,b){var q=b[0]*b[0]+b[1]*b[1];return [(a[0]*b[0]+a[1]*b[1])/q,(a[1]*b[0]-a[0]*b[1])/q];}
function ev(c,z){var r=[1,0];for(var i=1;i<c.length;i++){r=mul(r,z);r=[r[0]+c[i][0],r[1]+c[i][1]];}return r;}
function dk(c,z0,it){var n=z0.length,z=z0.map(function(v){return [v[0],v[1]];});for(var k=0;k<it;k++){for(var i=0;i<n;i++){var den=[1,0];for(var j=0;j<n;j++){if(j!==i){den=mul(den,sub(z[i],z[j]));}}z[i]=sub(z[i],div(ev(c,z[i]),den));}}return z;}
function pt(svg,e){var p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
function num(v){var s=Math.abs(v).toFixed(2).replace(".",",");return (v<-0.005?"−":"")+s;}
function clear(g){while(g.firstChild){g.removeChild(g.firstChild);}}
window.SimK={el:el,Panel:Panel,mul:mul,sub:sub,div:div,ev:ev,dk:dk,pt:pt,num:num,clear:clear};
})();
/* ── дописки obzor01 (биномиальные коэффициенты): счёт, слова из 0/1, анимация, ширина ── */
(function(G){
var K=G.SimK||(G.SimK={});
function C(n,k){if(k<0||k>n){return 0;}var r=1,i;for(i=1;i<=k;i++){r=r*(n-k+i)/i;}return Math.round(r);}
/* все слова длины n из 0 и 1 с k единицами; порядок: 1 раньше 0 (убывание двоичного числа) */
function words(n,k){var out=[],w=[];function rec(ones){var left=n-w.length;if(ones>left||ones<0){return;}if(left===0){out.push(w.slice());return;}if(ones>0){w.push(1);rec(ones-1);w.pop();}w.push(0);rec(ones);w.pop();}rec(k);return out;}
function flip(w){return w.map(function(b){return 1-b;});}
function key(w){return w.join("");}
/* карточки «команда из m человек среди n, в ней капитан» */
function cards(n,m){var res=[];words(n,m).forEach(function(t){t.forEach(function(b,i){if(b){res.push({team:t,cap:i});}});});return res;}
/* разбить список на стопки по ключу; порядок стопок — по первому появлению */
function groups(list,keyf){var map={},order=[];list.forEach(function(c,i){var g=keyf(c);if(!map.hasOwnProperty(g)){map[g]=[];order.push(g);}map[g].push(i);});return order.map(function(g){return map[g];});}
/* упорядоченные пары различных вершин 0..n-1 */
function arrows(n){var a=[],i,j;for(i=0;i<n;i++){for(j=0;j<n;j++){if(i!==j){a.push([i,j]);}}}return a;}
var mq=(G.matchMedia?G.matchMedia("(prefers-reduced-motion: reduce)"):null);
function reduced(){return !!(mq&&mq.matches);}
function ease(t){t=t<0?0:(t>1?1:t);return t<0.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
function seg(t,a,b){return ease((t-a)/(b-a));}
/* t бежит 0→1 за ms; при «меньше движения» — сразу последний кадр (асинхронно: ручка остановки возвращается раньше done) */
function anim(ms,step,done){var alive=true;if(reduced()||!(ms>0)||!G.requestAnimationFrame){G.setTimeout(function(){if(alive){step(1);if(done){done();}}},0);return {stop:function(){alive=false;}};}var t0=null;function fr(ts){if(!alive){return;}if(t0===null){t0=ts;}var t=Math.min(1,(ts-t0)/ms);step(t);if(t<1){G.requestAnimationFrame(fr);}else if(done){done();}}G.requestAnimationFrame(fr);return {stop:function(){alive=false;}};}
/* бином (n над k) для HTML-строк под рисунком */
function bn(n,k){return '<span class="bn"><span>'+n+'</span><span>'+k+'</span></span>';}
/* вызвать fn(ширина) сейчас и при каждом изменении ширины элемента */
function onWidth(el,fn){var w=-1;function chk(){var x=Math.round(el.getBoundingClientRect().width);if(x>0&&x!==w){w=x;fn(x);}}if(G.ResizeObserver){new G.ResizeObserver(chk).observe(el);}G.addEventListener("resize",chk);chk();}
function cl(v,a,b){return Math.max(a,Math.min(b,v));}
/* русское число: pl(5,"пара","пары","пар") */
function pl(x,a,b,c){var m=x%10,h=x%100;return (m===1&&h!==11)?a:((m>=2&&m<=4&&(h<10||h>=20))?b:c);}
/* лесенка n×n (строки и столбцы 1..n): пара {i,j}, i<j; u — клетка верхней лесенки (строка i, столбец j), d1 — отражение (j,i), d2 — оно же на ряд выше (j-1,i) */
function ladder(n){var a=[],i,j;for(i=1;i<=n;i++){for(j=i+1;j<=n;j++){a.push({i:i,j:j,u:[i,j],d1:[j,i],d2:[j-1,i]});}}return a;}
K.ladder=ladder;
/* набор по коду: номера (с 1) мест, где стоят единицы; 1010 → [1,3] */
function nabor(w){var a=[],i;for(i=0;i<w.length;i++){if(w[i]){a.push(i+1);}}return a;}
K.nabor=nabor;
K.C=C;K.words=words;K.flip=flip;K.key=key;K.cards=cards;K.groups=groups;K.arrows=arrows;K.reduced=reduced;K.ease=ease;K.seg=seg;K.anim=anim;K.bn=bn;K.onWidth=onWidth;K.cl=cl;K.pl=pl;
})(typeof window!=="undefined"?window:globalThis);
