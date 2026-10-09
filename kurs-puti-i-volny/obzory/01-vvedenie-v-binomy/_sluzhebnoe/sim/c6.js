(function(){
var K=window.SimK,root=document.getElementById("sim-c6");if(!root||!K){return;}
var svg=root.querySelector("svg"),out=root.querySelector(".sim-out"),inN=root.querySelector(".c6-n"),vN=root.querySelector(".c6-nv");
var SUP="⁰¹²³⁴⁵⁶⁷⁸";
var n=+inN.value,W=600,bits=[],cols=[],run=null,flash=[];
/* по умолчанию выбраны 1, 3, 5 */
(function(){var i;for(i=0;i<8;i++){bits.push(i%2===0&&i<5?1:0);}})();
function txt(cls,x,y,s,par,anchor){var e=K.el("text",{"class":cls,x:x,y:y,"text-anchor":anchor||"middle"},par);e.textContent=s;return e;}
function pw(i){return Math.pow(2,n-1-i);}
function value(){var v=0,i;for(i=0;i<n;i++){if(bits[i]){v+=pw(i);}}return v;}
function setValue(v){var i;for(i=0;i<n;i++){bits[i]=Math.floor(v/pw(i))%2;}}
function build(){
K.clear(svg);cols=[];flash=[];
var p=Math.min(64,(W-8)/n),bw=n*p,x0=(W-bw)/2,r=Math.min(19,p*0.36),b=Math.min(40,p-8);
var cy=8+19,bt=cy+19+28,py=bt+b+20,H=py+8,lab=x0>=100,i;
svg.setAttribute("viewBox","0 0 "+W+" "+H);
if(lab){var lx=x0-16;txt("c6-rl",lx,cy+4.5,"предметы",svg,"end");txt("c6-rl",lx,bt+b/2+4.5,"слово",svg,"end");txt("c6-rl",lx,py,"вес разряда",svg,"end");}
for(i=0;i<n;i++){
var cx=x0+p*(i+0.5),g=K.el("g",{"class":"c6-col"},svg);
var fl=K.el("rect",{"class":"c6-fl",x:cx-p/2+1,y:2,width:p-2,height:H-4,rx:6,opacity:0},g);
K.el("line",{"class":"c6-ln",x1:cx,y1:cy+r+2,x2:cx,y2:bt-2},g);
var gi=K.el("g",{"class":"c6-b","data-i":i,"data-p":"it",role:"button",tabindex:"0"},g);
K.el("circle",{"class":"c6-ring",cx:cx,cy:cy,r:r+4},gi);
K.el("circle",{"class":"c6-it",cx:cx,cy:cy,r:r},gi);
txt("c6-itl",cx,cy+5.5,String(i+1),gi);
K.el("rect",{"class":"w-hit",x:cx-p/2,y:cy-Math.max(r+6,18),width:p,height:2*Math.max(r+6,18)},gi);
var gd=K.el("g",{"class":"c6-b","data-i":i,"data-p":"dg",role:"button",tabindex:"0"},g);
K.el("rect",{"class":"c6-ring",x:cx-b/2-4,y:bt-4,width:b+8,height:b+8,rx:7},gd);
K.el("rect",{"class":"c6-bx",x:cx-b/2,y:bt,width:b,height:b,rx:5},gd);
var dg=txt("c6-dg",cx,bt+b/2+7.5,"0",gd);
K.el("rect",{"class":"w-hit",x:cx-p/2,y:bt-6,width:p,height:Math.max(b+12,36)},gd);
txt("c6-pv",cx,py,String(pw(i)),g);
cols.push({g:g,gi:gi,gd:gd,dg:dg});flash.push(fl);}
render();}
function setStr(a){return a.length?"{"+a.join(", ")+"}":"∅";}
function render(){var i,a=[],terms=[],v=value(),w="";
for(i=0;i<n;i++){var on=!!bits[i],c=cols[i];w+=on?"1":"0";
if(on){a.push(i+1);terms.push(String(pw(i)));}
if(c){c.g.classList.toggle("on",on);c.dg.textContent=on?"1":"0";
c.gi.setAttribute("aria-pressed",on?"true":"false");c.gi.setAttribute("aria-label","предмет "+(i+1)+(on?", выбран":", не выбран"));
c.gd.setAttribute("aria-label","цифра на месте "+(i+1)+": "+(on?"1":"0"));}}
var sum=terms.length>1?terms.join("&nbsp;+ ")+"&nbsp;= ":"";
var N=Math.pow(2,n);
out.innerHTML='<span class="c6-l"><span class="c6-nw">набор <span class="c6-set">'+setStr(a)+'</span></span> · <span class="c6-nw">выбрано <i>k</i> = <span class="c6-k">'+a.length+"</span></span></span>"+
'<span class="c6-l"><span class="c6-nw">слово <span class="c6-w">'+w+'</span></span> — <span class="c6-nw">двоичная запись</span> числа '+sum+'<b class="c6-num">'+v+"</b></span>"+
'<span class="c6-l w-dim"><span class="c6-nw">его номер среди 2'+SUP.charAt(n)+' слов,</span> <span class="c6-nw">считая с нуля: <span class="c6-idx">'+v+"</span> из 0…"+(N-1)+"</span></span>";}
/* вспышка столбцов, где цифра поменялась; при «меньше движения» — без вспышки */
function blink(ch){if(run){run.stop();run=null;}flash.forEach(function(f){f.setAttribute("opacity",0);});
if(!ch.length||K.reduced()){return;}
run=K.anim(520,function(t){var o=(0.9*(1-t)).toFixed(3);ch.forEach(function(i){if(flash[i]){flash[i].setAttribute("opacity",o);}});},function(){run=null;});}
function change(fn){var old=bits.slice(0,n),ch=[],i;fn();for(i=0;i<n;i++){if(old[i]!==bits[i]){ch.push(i);}}render();blink(ch);}
function toggle(i){change(function(){bits[i]=bits[i]?0:1;});}
svg.addEventListener("click",function(e){var g=e.target.closest?e.target.closest(".c6-b"):null;if(g){toggle(+g.getAttribute("data-i"));}});
svg.addEventListener("keydown",function(e){var g=e.target.closest?e.target.closest(".c6-b"):null;if(g&&(e.key==="Enter"||e.key===" "||e.key==="Spacebar")){e.preventDefault();toggle(+g.getAttribute("data-i"));}});
function step(d){var N=Math.pow(2,n);change(function(){setValue((value()+d+N)%N);});}
root.querySelector(".c6-dec").addEventListener("click",function(){step(-1);});
root.querySelector(".c6-inc").addEventListener("click",function(){step(1);});
root.querySelector(".c6-clr").addEventListener("click",function(){change(function(){var i;for(i=0;i<n;i++){bits[i]=0;}});});
root.querySelector(".c6-all").addEventListener("click",function(){change(function(){var i;for(i=0;i<n;i++){bits[i]=1;}});});
/* при смене n предметы с номерами больше n снимаются */
inN.addEventListener("input",function(){var m=+inN.value,i;for(i=m;i<8;i++){bits[i]=0;}n=m;vN.textContent=n;if(run){run.stop();run=null;}build();});
K.onWidth(root,function(w){W=w;build();});
})();
