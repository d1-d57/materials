
(function(){
'use strict';
var cx=350,cy=300,a=205,b=150,c=Math.sqrt(a*a-b*b);
var F1={x:cx-c,y:cy},F2={x:cx+c,y:cy}, twoA=2*a;
document.getElementById('F1').setAttribute('cx',F1.x);document.getElementById('F1').setAttribute('cy',F1.y);
document.getElementById('F2').setAttribute('cx',F2.x);document.getElementById('F2').setAttribute('cy',F2.y);
var r1=document.getElementById('r1'),r2=document.getElementById('r2'),P=document.getElementById('P');
var seg1=document.getElementById('seg1'),seg2=document.getElementById('seg2');
function dist(p,q){return Math.hypot(p.x-q.x,p.y-q.y);}
var step=0, theta=-0.7;
// полоска: общая высота = 2a (масштаб подобран под viewBox), низ зафиксирован
var barBot=540, scale=(440)/twoA;   // высота бара 440px = 2a
function frame(){
  if(step>=1) theta+=0.0085;        // P скользит на шаге 1; на шаге 0 — статичная картинка
  var p={x:cx+a*Math.cos(theta),y:cy+b*Math.sin(theta)};
  r1.setAttribute('x1',F1.x);r1.setAttribute('y1',F1.y);r1.setAttribute('x2',p.x);r1.setAttribute('y2',p.y);
  r2.setAttribute('x1',F2.x);r2.setAttribute('y1',F2.y);r2.setAttribute('x2',p.x);r2.setAttribute('y2',p.y);
  P.setAttribute('cx',p.x);P.setAttribute('cy',p.y);
  var d1=dist(p,F1)*scale, d2=dist(p,F2)*scale;     // |PF1|,|PF2| в пикселях бара
  // голубой снизу (PF1), красный сверху (PF2)
  seg1.setAttribute('y',barBot-d1);seg1.setAttribute('height',d1);
  seg2.setAttribute('y',barBot-d1-d2);seg2.setAttribute('height',d2);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
function goStep(k){ step=Math.max(0,Math.min(1,k|0)); }
window.addEventListener('message',function(e){ if(e&&e.data&&e.data.goStep!=null) goStep(e.data.goStep); });
window.__goStep=goStep;
})();
