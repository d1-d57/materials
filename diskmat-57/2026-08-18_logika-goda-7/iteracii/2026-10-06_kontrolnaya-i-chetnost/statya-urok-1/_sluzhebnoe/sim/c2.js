(function(){
var K=window.SimK,root=document.getElementById("sim-c2");if(!root||!K){return;}
var box=root.querySelector(".c2-cards"),out=root.querySelector(".sim-out"),bN=root.querySelector(".c2-norm"),bT=root.querySelector(".c2-tab"),bH=root.querySelector(".c2-hole"),bB=root.querySelector(".c2-back");
var CH=["2+4","1+1+1+1+1+1","1+2+1+2","3+3","1+5","1+1+2+1+1","2+3+1","6","1+1+3+1","2+1+1+2","2+2+2"];
function nrm(s){return s.split("+").map(Number).sort(function(a,b){return b-a;}).join("+");}
function parts(n,m){if(n===0){return [[]];}var r=[];for(var k=Math.min(n,m);k>=1;k--){parts(n-k,k).forEach(function(p){r.push([k].concat(p));});}return r;}
var P=parts(6,6).map(function(p){return p.join("+");});
function card(t,cls){var e=document.createElement("span");e.className="c2-k"+(cls?" "+cls:"");e.textContent=t;return e;}
function chaos(){K.clear(box);CH.forEach(function(s){box.appendChild(card(s));});bN.disabled=false;bT.disabled=true;bH.disabled=true;out.innerHTML="Записей <b>11</b>, и правильный ответ 11. Верен ли список?";}
function norm(){K.clear(box);var cnt={};CH.forEach(function(s){var t=nrm(s);cnt[t]=(cnt[t]||0)+1;});
CH.forEach(function(s){var t=nrm(s);box.appendChild(card(t,cnt[t]>1?"dup":""));});
bN.disabled=true;bT.disabled=false;out.innerHTML="Повтор: <b>2+2+1+1</b> записано дважды. Разных разложений 10, а ответ 11 — где пропуск?";}
function table(reveal){K.clear(box);var have={};CH.forEach(function(s){have[nrm(s)]=1;});
var tb=document.createElement("table"),num=0;
for(var f=6;f>=1;f--){var tr=document.createElement("tr"),th=document.createElement("th"),td=document.createElement("td");th.textContent=f;
P.filter(function(p){return +p.split("+")[0]===f;}).forEach(function(p){num++;var ok=have[p],e=card("",ok?"":(reveal?"found":"hole"));
var nn=document.createElement("span");nn.className="c2-n";nn.textContent=num;e.appendChild(nn);e.appendChild(document.createTextNode(ok||reveal?p:"?"));td.appendChild(e);});
tr.appendChild(th);tr.appendChild(td);tb.appendChild(tr);}
box.appendChild(tb);bT.disabled=true;bH.disabled=!!reveal;
out.innerHTML=reveal?"Пропуск — <b>4+1+1</b>. Всего <b>1 + 1 + 2 + 3 + 3 + 1 = 11</b>.":"Строка четвёрки неполна: после 4 бывает 2 или 1+1. Пустое место видно сразу.";}
bN.addEventListener("click",norm);bT.addEventListener("click",function(){table(false);});bH.addEventListener("click",function(){table(true);});bB.addEventListener("click",chaos);
chaos();
})();
