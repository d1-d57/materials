
(function(){
var svg=document.getElementById('svg');
var cx=340,cy=215,rx=250,ry=135, F1={x:130,y:215},F2={x:550,y:215};
var tang=document.getElementById('tang'),tlab=document.getElementById('tlab'),rays=document.getElementById('rays');
var arcA=document.getElementById('arcA'),arcB=document.getElementById('arcB'),Tc=document.getElementById('T'),Tlab=document.getElementById('Tlab');
var Pc=document.getElementById('P'),Plab=document.getElementById('Plab'),pf1=document.getElementById('pf1'),pf2=document.getElementById('pf2');
function arcBetween(vx,vy,ax,ay,bx,by,r){
  var a1=Math.atan2(ay-vy,ax-vx),a2=Math.atan2(by-vy,bx-vx);
  var d=a2-a1; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI;
  var x0=vx+r*Math.cos(a1),y0=vy+r*Math.sin(a1),x1=vx+r*Math.cos(a1+d),y1=vy+r*Math.sin(a1+d);
  return 'M'+x0.toFixed(2)+' '+y0.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x1.toFixed(2)+' '+y1.toFixed(2);
}
var theta=-Math.PI/2, dragging=false;
function redraw(){
  var T={x:cx+rx*Math.cos(theta), y:cy+ry*Math.sin(theta)};
  var tx=-rx*Math.sin(theta), ty=ry*Math.cos(theta), L=Math.hypot(tx,ty); tx/=L; ty/=L;
  var EL={x:T.x-tx*220,y:T.y-ty*220}, ER={x:T.x+tx*220,y:T.y+ty*220};
  tang.setAttribute('x1',EL.x);tang.setAttribute('y1',EL.y);tang.setAttribute('x2',ER.x);tang.setAttribute('y2',ER.y);
  tlab.setAttribute('x',ER.x-6); tlab.setAttribute('y',ER.y-8);
  rays.setAttribute('points',F1.x+','+F1.y+' '+T.x.toFixed(1)+','+T.y.toFixed(1)+' '+F2.x+','+F2.y);
  Tc.setAttribute('cx',T.x);Tc.setAttribute('cy',T.y); Tlab.setAttribute('x',T.x); Tlab.setAttribute('y',T.y-14);
  arcA.setAttribute('d',arcBetween(T.x,T.y, F1.x,F1.y, T.x-tx*40,T.y-ty*40, 28));
  arcB.setAttribute('d',arcBetween(T.x,T.y, T.x+tx*40,T.y+ty*40, F2.x,F2.y, 28));
  // другая точка P на касательной (вне эллипса) — путь длиннее
  var sgn = (tx>=0)?1:-1; // P справа по касательной
  var P={x:T.x+tx*128*sgn, y:T.y+ty*128*sgn};
  Pc.setAttribute('cx',P.x);Pc.setAttribute('cy',P.y); Plab.setAttribute('x',P.x); Plab.setAttribute('y',P.y+22);
  pf1.setAttribute('x1',F1.x);pf1.setAttribute('y1',F1.y);pf1.setAttribute('x2',P.x);pf1.setAttribute('y2',P.y);
  pf2.setAttribute('x1',F2.x);pf2.setAttribute('y1',F2.y);pf2.setAttribute('x2',P.x);pf2.setAttribute('y2',P.y);
}
redraw();
function toSvg(evt){var pt=svg.createSVGPoint();pt.x=evt.clientX;pt.y=evt.clientY;return pt.matrixTransform(svg.getScreenCTM().inverse());}
Tc.addEventListener('pointerdown',function(e){dragging=true;Tc.style.cursor='grabbing';Tc.setPointerCapture(e.pointerId);e.preventDefault();});
svg.addEventListener('pointermove',function(e){if(dragging){var p=toSvg(e);theta=Math.atan2((p.y-cy)/ry,(p.x-cx)/rx);redraw();}});
svg.addEventListener('pointerup',function(){dragging=false;Tc.style.cursor='grab';});
svg.addEventListener('pointercancel',function(){dragging=false;});
window.__setTheta=function(t){theta=t;redraw();};
})();
