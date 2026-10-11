(function(){
var K=window.SimK,root=document.getElementById("sim-c4");if(!root||!K){return;}
var box=root.querySelector(".c4-rows"),out=root.querySelector(".sim-out"),bp=root.querySelector(".c4-prev"),bn=root.querySelector(".c4-next");
var C=["Б","К","С"],COL={"Б":"#ffffff","К":"#c8322c","С":"#2a55b5"},NM={"Б":"белый","К":"красный","С":"синий"},FL=[],el=[],cur=0;
C.forEach(function(a){C.forEach(function(b){C.forEach(function(c){if(a!==b&&b!==c){FL.push(a+b+c);}});});});
C.forEach(function(top){var r=document.createElement("div");r.className="c4-r";var l=document.createElement("span");l.className="c4-l";l.textContent="верх "+NM[top];r.appendChild(l);
FL.forEach(function(f,i){if(f[0]!==top){return;}var w=document.createElement("span");w.className="c4-f";var fl=document.createElement("span");fl.className="c4-flag";
for(var j=0;j<3;j++){var s=document.createElement("i");s.style.background=COL[f[j]];fl.appendChild(s);}
w.appendChild(fl);w.appendChild(document.createTextNode(f));w.addEventListener("click",function(){go(i);});r.appendChild(w);el[i]=w;});
box.appendChild(r);});
function go(i){cur=Math.max(0,Math.min(FL.length-1,i));el.forEach(function(e,k){e.classList.toggle("on",k===cur);});
var f=FL[cur],nx=FL[cur+1],pv=FL[cur-1],s="Флаг <b>"+(cur+1)+"</b> из 12: "+f+".";
if(nx&&nx[0]!==f[0]){s+=" Следующий, "+nx+", — уже в строке «верх "+NM[nx[0]]+"»: стык строк.";}
if(!nx){s+=" Дальше флагов нет.";}
if(pv&&pv[0]!==f[0]){s+=" Перед ним — "+pv+", последний флаг строки «верх "+NM[pv[0]]+"».";}
out.innerHTML=s;bp.disabled=cur===0;bn.disabled=cur===FL.length-1;}
bp.addEventListener("click",function(){go(cur-1);});bn.addEventListener("click",function(){go(cur+1);});
go(0);
})();
