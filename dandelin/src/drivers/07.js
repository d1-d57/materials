
'use strict';
var NS='http://www.w3.org/2000/svg', svg=document.getElementById('svg');
function E(t,a,p){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e;}
function arcPath(vx,vy,ax,ay,bx,by,r){
  var a1=Math.atan2(ay-vy,ax-vx),a2=Math.atan2(by-vy,bx-vx),d=a2-a1;
  while(d<=-Math.PI)d+=2*Math.PI; while(d>Math.PI)d-=2*Math.PI;
  var x1=vx+r*Math.cos(a1),y1=vy+r*Math.sin(a1),x2=vx+r*Math.cos(a2),y2=vy+r*Math.sin(a2);
  return 'M'+x1.toFixed(2)+' '+y1.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x2.toFixed(2)+' '+y2.toFixed(2);
}
var cx=340,cy=212,rx=250,ry=150,c=Math.sqrt(rx*rx-ry*ry);
var F1={x:cx-c,y:cy},F2={x:cx+c,y:cy};
// статичные элементы
E('ellipse',{cx:cx,cy:cy,rx:rx,ry:ry,fill:'#a7c2cb','fill-opacity':0.09,stroke:'#333','stroke-width':1.7});
E('circle',{cx:F1.x,cy:F1.y,r:4.5,fill:'#bf5b4f',stroke:'#fff','stroke-width':2});
var lf1=E('text',{x:F1.x,y:F1.y+24,'text-anchor':'middle','font-size':15,'font-weight':700,fill:'#bf5b4f'});lf1.textContent='F₁';
E('circle',{cx:F2.x,cy:F2.y,r:4.5,fill:'#bf5b4f',stroke:'#fff','stroke-width':2});
var lf2=E('text',{x:F2.x,y:F2.y+24,'text-anchor':'middle','font-size':15,'font-weight':700,fill:'#bf5b4f'});lf2.textContent='F₂';
// динамичные
var tline=E('line',{stroke:'#283845','stroke-width':2});
var ray=E('polyline',{fill:'none',stroke:'#c0aa5a','stroke-width':2.6,'stroke-linejoin':'round','stroke-linecap':'round'});
var arc1=E('path',{fill:'none',stroke:'#c0aa5a','stroke-width':2});
var arc2=E('path',{fill:'none',stroke:'#c0aa5a','stroke-width':2});
var Tc=E('circle',{id:'T',r:6,fill:'#785a18',stroke:'#fff','stroke-width':2.5});
var Tl=E('text',{'text-anchor':'middle','font-size':15,'font-weight':700,fill:'#785a18'});Tl.textContent='T';
var theta=-Math.PI/2;
function redraw(){
  var T={x:cx+rx*Math.cos(theta),y:cy+ry*Math.sin(theta)};
  var tdx=-rx*Math.sin(theta),tdy=ry*Math.cos(theta),tl=Math.hypot(tdx,tdy),ux=tdx/tl,uy=tdy/tl;
  var L=235; var tA={x:T.x+ux*L,y:T.y+uy*L},tB={x:T.x-ux*L,y:T.y-uy*L};
  tline.setAttribute('x1',tA.x);tline.setAttribute('y1',tA.y);tline.setAttribute('x2',tB.x);tline.setAttribute('y2',tB.y);
  ray.setAttribute('points',F1.x+','+F1.y+' '+T.x+','+T.y+' '+F2.x+','+F2.y);
  var s1=((F1.x-T.x)*ux+(F1.y-T.y)*uy)>0?1:-1, s2=((F2.x-T.x)*ux+(F2.y-T.y)*uy)>0?1:-1;
  arc1.setAttribute('d',arcPath(T.x,T.y, F1.x,F1.y, T.x+ux*40*s1,T.y+uy*40*s1, 30));
  arc2.setAttribute('d',arcPath(T.x,T.y, F2.x,F2.y, T.x+ux*40*s2,T.y+uy*40*s2, 30));
  Tc.setAttribute('cx',T.x);Tc.setAttribute('cy',T.y);
  Tl.setAttribute('x',T.x);Tl.setAttribute('y',T.y-16);
}
redraw();
function toSvg(evt){var pt=svg.createSVGPoint();pt.x=evt.clientX;pt.y=evt.clientY;return pt.matrixTransform(svg.getScreenCTM().inverse());}
var drag=false;
Tc.addEventListener('pointerdown',function(e){drag=true;Tc.style.cursor='grabbing';Tc.setPointerCapture(e.pointerId);e.preventDefault();});
svg.addEventListener('pointermove',function(e){if(drag){var p=toSvg(e);theta=Math.atan2((p.y-cy)/ry,(p.x-cx)/rx);redraw();}});
svg.addEventListener('pointerup',function(){drag=false;Tc.style.cursor='grab';});
svg.addEventListener('pointercancel',function(){drag=false;});
window.addEventListener('message',function(e){});
