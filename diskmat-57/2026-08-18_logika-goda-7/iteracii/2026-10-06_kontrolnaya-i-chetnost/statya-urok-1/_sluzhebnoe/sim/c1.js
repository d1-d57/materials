(function(){
var K=window.SimK,root=document.getElementById("sim-c1");if(!root||!K){return;}
var grid=root.querySelector(".c1-grid"),out=root.querySelector(".sim-out"),bs=root.querySelectorAll(".c1-b"),cells={},m="";
for(var n=1;n<=90;n++){var c=document.createElement("div");c.className="c1-c";c.textContent=n;grid.appendChild(c);cells[n]=c;}
function show(mm){m=(m===mm)?"":mm;
for(var n=1;n<=90;n++){var c=cells[n],a=n%9===0,b=n%15===0;c.className="c1-c";
if(m==="a"&&a){c.classList.add("a");}if(m==="b"&&b){c.classList.add("b");}
if(m==="ab"&&(a||b)){c.classList.add(a&&b?"ab":(a?"a":"b"));}}
for(var i=0;i<bs.length;i++){bs[i].classList.toggle("on",bs[i].getAttribute("data-m")===m);}
out.innerHTML={"":"Нажмите на список.","a":"Кратные 9: 9, 18, …, 90 — <b>10</b> чисел.","b":"Кратные 15: 15, 30, …, 90 — <b>6</b> чисел.","ab":"10 + 6 = 16? Числа 45 и 90 стоят в обоих списках — повторы. Всего <b>10 + 6 − 2 = 14</b>."}[m];}
for(var i=0;i<bs.length;i++){bs[i].addEventListener("click",function(){show(this.getAttribute("data-m"));});}
show("");
})();
