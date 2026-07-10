
'use strict';
var NS='http://www.w3.org/2000/svg', svg=document.getElementById('svg');
function E(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e;}
function arcPath(vx,vy,ax,ay,bx,by,r){
  var a1=Math.atan2(ay-vy,ax-vx),a2=Math.atan2(by-vy,bx-vx),d=a2-a1;
  while(d<=-Math.PI)d+=2*Math.PI; while(d>Math.PI)d-=2*Math.PI;
  var x1=vx+r*Math.cos(a1),y1=vy+r*Math.sin(a1),x2=vx+r*Math.cos(a2),y2=vy+r*Math.sin(a2);
  return 'M'+x1.toFixed(2)+' '+y1.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x2.toFixed(2)+' '+y2.toFixed(2);
}
var S={x:198,y:88}, R={x:482,y:122}, P={x:300,y:255}, my=255;
E('line',{x1:60,y1:my,x2:620,y2:my,stroke:'#283845','stroke-width':2.4});
for(var x=80;x<=600;x+=40) E('line',{x1:x,y1:my,x2:x-14,y2:my+16,stroke:'#8195ad','stroke-width':1,opacity:0.5});
E('polyline',{points:S.x+','+S.y+' '+P.x+','+P.y+' '+R.x+','+R.y,fill:'none',stroke:'#c0aa5a','stroke-width':2.6,'stroke-linejoin':'round','stroke-linecap':'round'});
// дуги = углы с зеркалом (горизонталью), неравные
E('path',{d:arcPath(P.x,P.y, P.x-60,P.y, S.x,S.y, 34),fill:'none',stroke:'#bf5b4f','stroke-width':2});
E('path',{d:arcPath(P.x,P.y, P.x+60,P.y, R.x,R.y, 34),fill:'none',stroke:'#bf5b4f','stroke-width':2});
E('circle',{cx:S.x,cy:S.y,r:5,fill:'#785a18',stroke:'#fff','stroke-width':2});
var t1=E('text',{x:S.x,y:S.y-15,'text-anchor':'middle','font-size':16,'font-weight':700,fill:'#785a18'});t1.textContent='источник';
E('circle',{cx:R.x,cy:R.y,r:5,fill:'#785a18',stroke:'#fff','stroke-width':2});
var t2=E('text',{x:R.x,y:R.y-15,'text-anchor':'middle','font-size':16,'font-weight':700,fill:'#785a18'});t2.textContent='приёмник';
E('circle',{cx:P.x,cy:P.y,r:4,fill:'#333'});
