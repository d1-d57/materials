
(function(){
var svg=document.getElementById('svg');
// штриховка зеркала
var h=document.getElementById('hatch'),s='';
for(var x=80;x<=600;x+=40) s+='<line x1="'+x+'" y1="250" x2="'+(x-14)+'" y2="266"/>';
h.innerHTML=s;
function arcBetween(vx,vy,ax,ay,bx,by,r){
  var a1=Math.atan2(ay-vy,ax-vx),a2=Math.atan2(by-vy,bx-vx);
  var d=a2-a1; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI;
  var x0=vx+r*Math.cos(a1),y0=vy+r*Math.sin(a1),x1=vx+r*Math.cos(a1+d),y1=vy+r*Math.sin(a1+d);
  return 'M'+x0.toFixed(2)+' '+y0.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x1.toFixed(2)+' '+y1.toFixed(2);
}
var S={x:190,y:80}, R={x:470,y:110}, P={x:300,y:250}; // P сдвинут от оптимума → углы неравные
document.getElementById('ray').setAttribute('points',S.x+','+S.y+' '+P.x+','+P.y+' '+R.x+','+R.y);
document.getElementById('P').setAttribute('cx',P.x); document.getElementById('P').setAttribute('cy',P.y);
// дуги С ЗЕРКАЛОМ (горизонталью): слева между лучом к источнику и зеркалом, справа между зеркалом и лучом к приёмнику
document.getElementById('arcA').setAttribute('d',arcBetween(P.x,P.y, S.x,S.y, P.x-40,P.y, 30));
document.getElementById('arcB').setAttribute('d',arcBetween(P.x,P.y, P.x+40,P.y, R.x,R.y, 30));
})();
