
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var cx=340, cy=190, a=272, b=150, c=Math.sqrt(a*a-b*b);
var F1={x:cx-c,y:cy}, F2={x:cx+c,y:cy};
function E(t){ return {x:cx+a*Math.cos(t), y:cy+b*Math.sin(t)}; }

// 6 лучей: точки на стенке веером (верх и низ, не у самой оси)
var rays=document.getElementById('rays'), rayLines=[];
[55,90,125,235,270,305].forEach(function(deg){
  var Q=E(deg*Math.PI/180);
  function mk(x1,y1,x2,y2){var l=document.createElementNS(NS,'line');
    l.setAttribute('x1',x1);l.setAttribute('y1',y1);l.setAttribute('x2',x2);l.setAttribute('y2',y2);
    l.setAttribute('stroke','#c0aa5a');l.setAttribute('stroke-width','1.5');l.setAttribute('stroke-linecap','round');
    l.setAttribute('opacity','0');rays.appendChild(l);return l;}
  rayLines.push({inc:mk(F1.x,F1.y,Q.x,Q.y), ref:mk(Q.x,Q.y,F2.x,F2.y), Q:Q});
});

var front=document.getElementById('front'), frontEls=[];
for(var i=0;i<3;i++){var p=document.createElementNS(NS,'circle');
  p.setAttribute('fill','none');p.setAttribute('stroke-width','2.2');p.setAttribute('opacity','0');
  front.appendChild(p);frontEls.push(p);}

function stonePath(jit){var n=7,base=6.5,s='';
  for(var i=0;i<n;i++){var ang=i/n*2*Math.PI,rr=base+(jit?Math.sin(i*3+performance.now()/55)*1.6:0);
    s+=(i?'L':'M')+(F2.x+rr*Math.cos(ang)).toFixed(1)+' '+(F2.y+rr*Math.sin(ang)).toFixed(1);}return s+'Z';}
document.getElementById('stone').setAttribute('d',stonePath(false));
var sr=document.getElementById('sparkRays');
for(var i=0;i<8;i++){var ang=i/8*2*Math.PI,l=document.createElementNS(NS,'line');
  l.setAttribute('x1',F1.x+7*Math.cos(ang));l.setAttribute('y1',F1.y+7*Math.sin(ang));
  l.setAttribute('x2',F1.x+12*Math.cos(ang));l.setAttribute('y2',F1.y+12*Math.sin(ang));sr.appendChild(l);}
var shards=document.getElementById('shards');
for(var i=0;i<8;i++){var l=document.createElementNS(NS,'line');l._a=i/8*2*Math.PI;shards.appendChild(l);}

var maxR=a+c+10;            // хватит, чтобы фронт дошёл до дальней стенки; clip обрежет
var step=0, phase=0;
function frame(){
  if(step>=1){ phase+=0.011; if(phase>1){ phase=0; } }
  // лучи
  rayLines.forEach(function(o){
    o.inc.setAttribute('opacity', step===1? '0.7' : (step>=2?'0.12':'0'));
    o.ref.setAttribute('opacity', step>=2? '0.7' : '0');
  });
  // фронт: шаг1 — расходится от F1; шаг2 — сходится к F2
  var ctr, r0, col;
  if(step===1){ ctr=F1; r0=phase*maxR; col='#6f86b8'; }
  else if(step>=2){ ctr=F2; r0=(1-phase)*maxR; col='#785a18'; }
  frontEls.forEach(function(el,idx){
    var r=r0 - idx*24;
    if(step>=1 && r>3){
      el.setAttribute('cx',ctr.x);el.setAttribute('cy',ctr.y);el.setAttribute('r',r.toFixed(1));
      el.setAttribute('stroke',col);el.setAttribute('opacity', step===1?'0.5':'0.75');
    } else el.setAttribute('opacity','0');
  });
  // удар: конец схождения (r0 мал) на шаге 2
  var hit=(step>=2 && r0<40 && r0>2);
  document.getElementById('stone').setAttribute('d',stonePath(hit));
  shards.setAttribute('opacity',hit?'0.95':'0');
  if(hit){var g=(40-r0)/38; Array.prototype.forEach.call(shards.children,function(l){
    var ang=l._a,ra=9,rb=9+13*g;
    l.setAttribute('x1',F2.x+ra*Math.cos(ang));l.setAttribute('y1',F2.y+ra*Math.sin(ang));
    l.setAttribute('x2',F2.x+rb*Math.cos(ang));l.setAttribute('y2',F2.y+rb*Math.sin(ang));});}
  document.getElementById('concl').setAttribute('opacity', step>=2?'1':'0');
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
function goStep(k){ step=Math.max(0,Math.min(2,k|0)); if(step>=1&&phase===0)phase=0.001; }
window.addEventListener('message',function(e){ if(e&&e.data&&e.data.goStep!=null) goStep(e.data.goStep); });
window.__goStep=goStep;
})();
