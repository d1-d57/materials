
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg', svg=document.getElementById('svg');
var A={x:170,y:95}, B={x:480,y:75}, riverY=190, Bp={x:B.x,y:2*riverY-B.y};
var Wopt=A.x+((riverY-A.y)/(Bp.y-A.y))*(Bp.x-A.x);
var path=document.getElementById('path'),W=document.getElementById('W'),Wlab=document.getElementById('Wlab');
var refl=document.getElementById('refl'),bb=document.getElementById('bb'),Bpc=document.getElementById('Bp'),straight=document.getElementById('straight'),wbp=document.getElementById('wbp');
var arcA=document.getElementById('arcA'),arcB=document.getElementById('arcB');
Bpc.setAttribute('cx',Bp.x);Bpc.setAttribute('cy',Bp.y);
bb.setAttribute('x1',B.x);bb.setAttribute('y1',B.y);bb.setAttribute('x2',Bp.x);bb.setAttribute('y2',Bp.y);
straight.setAttribute('x1',A.x);straight.setAttribute('y1',A.y);straight.setAttribute('x2',Bp.x);straight.setAttribute('y2',Bp.y);

// === УНИВЕРСАЛЬНАЯ ДУГА УГЛА: меньшая дуга строго между лучами V→A и V→B, радиус r ===
function arcBetween(vx,vy, ax,ay, bx,by, r){
  var a1=Math.atan2(ay-vy,ax-vx), a2=Math.atan2(by-vy,bx-vx);
  var d=a2-a1; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI;
  var x0=vx+r*Math.cos(a1), y0=vy+r*Math.sin(a1);
  var x1=vx+r*Math.cos(a1+d), y1=vy+r*Math.sin(a1+d);
  return 'M'+x0.toFixed(2)+' '+y0.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x1.toFixed(2)+' '+y1.toFixed(2);
}

var step=0, wx=240, dragging=false;
function redraw(){
  path.setAttribute('points',A.x+','+A.y+' '+wx.toFixed(1)+','+riverY+' '+B.x+','+B.y);
  W.setAttribute('cx',wx);Wlab.setAttribute('x',wx);
  wbp.setAttribute('x1',wx);wbp.setAttribute('y1',riverY);wbp.setAttribute('x2',Bp.x);wbp.setAttribute('y2',Bp.y);
  // дуги углов с рекой (горизонталью) в точке W — равны в оптимуме
  arcA.setAttribute('d',arcBetween(wx,riverY, A.x,A.y, wx-40,riverY, 26));
  arcB.setAttribute('d',arcBetween(wx,riverY, wx+40,riverY, B.x,B.y, 26));
  refl.setAttribute('opacity', step>=1?'1':'0');
}
redraw();

function toSvgX(evt){var pt=svg.createSVGPoint();pt.x=evt.clientX;pt.y=evt.clientY;
  return pt.matrixTransform(svg.getScreenCTM().inverse()).x;}
function clamp(x){return Math.max(70,Math.min(610,x));}
W.addEventListener('pointerdown',function(e){dragging=true;W.style.cursor='grabbing';W.setPointerCapture(e.pointerId);e.preventDefault();});
svg.addEventListener('pointermove',function(e){if(dragging){wx=clamp(toSvgX(e));redraw();}});
svg.addEventListener('pointerup',function(){dragging=false;W.style.cursor='grab';});
svg.addEventListener('pointercancel',function(){dragging=false;});

function goStep(k){ step=Math.max(0,Math.min(1,k|0)); redraw(); }
window.addEventListener('message',function(e){ if(e&&e.data&&e.data.goStep!=null) goStep(e.data.goStep); });
window.__goStep=goStep; window.__setW=function(x){wx=clamp(x);redraw();};
})();
