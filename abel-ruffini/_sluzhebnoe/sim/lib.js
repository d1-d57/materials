(function(){
var NS="http://www.w3.org/2000/svg";
function el(tag,attrs,parent){var e=document.createElementNS(NS,tag);for(var k in attrs){e.setAttribute(k,attrs[k]);}if(parent){parent.appendChild(e);}return e;}
function Panel(x0,y0,w,h,xr,yr){this.x0=x0;this.y0=y0;this.w=w;this.h=h;this.xr=xr;this.yr=yr;}
Panel.prototype.X=function(x){return this.x0+(x-this.xr[0])/(this.xr[1]-this.xr[0])*this.w;};
Panel.prototype.Y=function(y){return this.y0+this.h-(y-this.yr[0])/(this.yr[1]-this.yr[0])*this.h;};
Panel.prototype.ix=function(X){return this.xr[0]+(X-this.x0)/this.w*(this.xr[1]-this.xr[0]);};
Panel.prototype.iy=function(Y){return this.yr[0]+(this.y0+this.h-Y)/this.h*(this.yr[1]-this.yr[0]);};
Panel.prototype.inside=function(x,y){return x>=this.xr[0]&&x<=this.xr[1]&&y>=this.yr[0]&&y<=this.yr[1];};
Panel.prototype.d=function(pts){var s="",pen=false;for(var i=0;i<pts.length;i++){var x=pts[i][0],y=pts[i][1];if(this.inside(x,y)){s+=(pen?" L":" M")+this.X(x).toFixed(1)+","+this.Y(y).toFixed(1);pen=true;}else{pen=false;}}return s||"M0,0";};
Panel.prototype.axes=function(g,lx,ly){var X0=this.X(0),Y0=this.Y(0);el("line",{"class":"k-ax",x1:this.x0,y1:Y0,x2:this.x0+this.w,y2:Y0},g);el("line",{"class":"k-ax",x1:X0,y1:this.y0+this.h,x2:X0,y2:this.y0},g);el("path",{"class":"k-axh",d:"M"+(this.x0+this.w)+","+Y0+" l-8,-3.5 0,7 z"},g);el("path",{"class":"k-axh",d:"M"+X0+","+this.y0+" l-3.5,8 7,0 z"},g);if(lx){var t=el("text",{"class":"k-lab",x:this.x0+this.w-10,y:Y0+17},g);t.textContent=lx;}if(ly){var u=el("text",{"class":"k-lab",x:X0+8,y:this.y0+10},g);u.textContent=ly;}};
function mul(a,b){return [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
function sub(a,b){return [a[0]-b[0],a[1]-b[1]];}
function div(a,b){var q=b[0]*b[0]+b[1]*b[1];return [(a[0]*b[0]+a[1]*b[1])/q,(a[1]*b[0]-a[0]*b[1])/q];}
function ev(c,z){var r=[1,0];for(var i=1;i<c.length;i++){r=mul(r,z);r=[r[0]+c[i][0],r[1]+c[i][1]];}return r;}
function dk(c,z0,it){var n=z0.length,z=z0.map(function(v){return [v[0],v[1]];});for(var k=0;k<it;k++){for(var i=0;i<n;i++){var den=[1,0];for(var j=0;j<n;j++){if(j!==i){den=mul(den,sub(z[i],z[j]));}}z[i]=sub(z[i],div(ev(c,z[i]),den));}}return z;}
function pt(svg,e){var p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
function num(v){var s=Math.abs(v).toFixed(2).replace(".",",");return (v<-0.005?"−":"")+s;}
function clear(g){while(g.firstChild){g.removeChild(g.firstChild);}}
window.SimK={el:el,Panel:Panel,mul:mul,sub:sub,div:div,ev:ev,dk:dk,pt:pt,num:num,clear:clear};
})();
