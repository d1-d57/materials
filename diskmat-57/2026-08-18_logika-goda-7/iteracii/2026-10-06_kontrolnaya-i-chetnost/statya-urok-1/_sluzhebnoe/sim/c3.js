(function(){
var K=window.SimK,root=document.getElementById("sim-c3");if(!root||!K){return;}
var grid=root.querySelector(".c3-grid"),bar=root.querySelector(".c3-bar"),out=root.querySelector(".sim-out"),cells={},PR=[2,3,5,7,11,13,17],sel={};
for(var d=1;d<=9;d++){for(var u=0;u<=9;u++){var n=10*d+u,c=document.createElement("div");c.className="c3-c";c.textContent=n;grid.appendChild(c);cells[n]=c;}}
function cnt(s){var k=0;for(var n=10;n<=99;n++){if(Math.floor(n/10)+n%10===s){k++;}}return k;}
PR.concat(["все"]).forEach(function(s){var b=document.createElement("button");b.type="button";b.textContent=s==="все"?"все простые":s;b.setAttribute("data-s",s);bar.appendChild(b);
b.addEventListener("click",function(){if(s==="все"){var all=PR.every(function(p){return sel[p];});PR.forEach(function(p){sel[p]=!all;});}else{sel[s]=!sel[s];}draw();});});
function draw(){var parts=[],tot=0;
for(var n=10;n<=99;n++){cells[n].classList.toggle("on",!!sel[Math.floor(n/10)+n%10]);}
PR.forEach(function(p){if(sel[p]){var k=cnt(p);parts.push(k);tot+=k;}});
var bs=bar.querySelectorAll("button");for(var i=0;i<bs.length;i++){var s=bs[i].getAttribute("data-s");bs[i].classList.toggle("on",s==="все"?PR.every(function(p){return sel[p];}):!!sel[s]);}
out.innerHTML=parts.length?("Строк: "+parts.length+". Чисел <b>"+parts.join(" + ")+(parts.length>1?" = "+tot:"")+"</b>."):"Нажмите на сумму цифр: подсветится её косая строка.";}
draw();
})();
