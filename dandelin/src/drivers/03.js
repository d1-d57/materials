
(function(){
'use strict';
const DEG=Math.PI/180;
const alpha=22*DEG, sinA=Math.sin(alpha), cosA=Math.cos(alpha), tanA=Math.tan(alpha);
const Hc=4.8, Rc=Hc*tanA, tTop=Hc/cosA;
const q=new URLSearchParams(location.search);

// геометрия Данделена (как в основном файле): верхняя сфера
const c1=1.2, r1=c1*sinA;
const ny=-0.783, nx=Math.sqrt(1-ny*ny);           // нормаль секущей плоскости
const n=new THREE.Vector3(nx,ny,0);
const d=ny*c1-r1;                                   // плоскость: n·x = d
const C1=new THREE.Vector3(0,c1,0);
const F1=C1.clone().addScaledVector(n,-r1);         // фокус — касание сферы и секущей
const yc=c1*cosA*cosA, rc=c1*sinA*cosA;             // окружность касания: высота, радиус
const X0=(d-ny*yc)/nx;                              // x директрисы (y=yc, z свободно)
function u(th){ return new THREE.Vector3(sinA*Math.cos(th),cosA,sinA*Math.sin(th)); }
function P(th){ const uu=u(th); return uu.multiplyScalar(d/uu.dot(n)); }

const COL={ bg:0xffffff, cone:0xEFBE3C, plane:0x84C0DC, sec:0xB83A2B, sph:0xEC6B89,
            green:0x6FA463, dir:0x2E7D46, ink:0x3F352B, focus:0xC96A3C, planeEdge:0x3E6675 };
const RO={ shadow:0, coneBack:1, sphBack:2, plane:4, coneFront:6, sphFront:7, proxy:9, ghost:10, crisp:11, contour:12, top:14 };

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.setClearColor(COL.bg,1);
renderer.outputEncoding=THREE.sRGBEncoding; renderer.localClippingEnabled=true; THREE.ColorManagement.enabled=true;
document.getElementById('c').appendChild(renderer.domElement);
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(42,1,0.1,100);
scene.add(new THREE.DirectionalLight(0xfff7ea,0.62).translateX(6).translateY(10).translateZ(5));
const fill=new THREE.DirectionalLight(0xe4edf4,0.18); fill.position.set(-6,4,-7); scene.add(fill);
scene.add(new THREE.AmbientLight(0xffffff,0.48));
const root=new THREE.Group(); root.rotation.x=Math.PI; root.position.y=2.55; scene.add(root); root.updateMatrixWorld(true);

function bodyMat(c,o,s){ return new THREE.MeshPhongMaterial({color:c,transparent:true,opacity:o,side:s,depthWrite:false,shininess:22,specular:0x3a3328}); }
function addBody(geom,c,oF,oB,roB,roF){ const b=new THREE.Mesh(geom,bodyMat(c,oB,THREE.BackSide)); const f=new THREE.Mesh(geom,bodyMat(c,oF,THREE.FrontSide));
  b.renderOrder=roB; f.renderOrder=roF; root.add(b,f); return [b,f]; }
function addProxy(geom){ const m=new THREE.Mesh(geom,new THREE.MeshBasicMaterial({colorWrite:false,depthWrite:true,depthTest:true,side:THREE.FrontSide,polygonOffset:true,polygonOffsetFactor:1.2,polygonOffsetUnits:1.2}));
  m.renderOrder=RO.proxy; root.add(m); return m; }
function addTwoPass(geom,color,gO,cO,ro){ const g=new THREE.Mesh(geom,new THREE.MeshBasicMaterial({color,transparent:true,opacity:gO,depthTest:false,depthWrite:false})); g.renderOrder=ro?ro:RO.ghost;
  const c=new THREE.Mesh(geom,new THREE.MeshBasicMaterial({color,transparent:true,opacity:cO,depthTest:true,depthWrite:false})); c.renderOrder=(ro?ro+1:RO.crisp);
  root.add(g,c); return [g,c]; }
function contour(geom,color,op){ const m=new THREE.Mesh(geom,new THREE.MeshBasicMaterial({color,transparent:true,opacity:op,depthTest:false,depthWrite:false})); m.renderOrder=RO.contour; root.add(m); return m; }
function ring(radius,y,tube){ const g=new THREE.TorusGeometry(radius,tube,8,120); g.rotateX(Math.PI/2); g.translate(0,y,0); return g; }
function span(p1,p2,rad){ const dir=new THREE.Vector3().subVectors(p2,p1),len=dir.length();
  const g=new THREE.CylinderGeometry(rad,rad,1,12); g.translate(0,0.5,0); g.scale(1,len,1);
  g.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize())));
  g.translate(p1.x,p1.y,p1.z); return g; }

// конус
const coneGeom=new THREE.LatheGeometry([new THREE.Vector2(0.001,0),new THREE.Vector2(Rc,Hc)],128);
addBody(coneGeom,COL.cone,0.46,0.12,RO.coneBack,RO.coneFront); addProxy(coneGeom);
addTwoPass(ring(Rc,Hc,0.011),COL.ink,0.16,0.85);

// верхняя сфера Данделена + широты + окружность касания
const sGeom=new THREE.SphereGeometry(r1,48,32); sGeom.translate(0,c1,0);
addBody(sGeom,COL.sph,0.88,0.46,RO.sphBack,RO.sphFront); addProxy(sGeom);
for(const la of [-45,-15,15,45].map(x=>x*DEG))
  addTwoPass(ring(r1*Math.cos(la),c1+r1*Math.sin(la),0.009),0xB25C70,0.42,0.92);
addTwoPass(ring(rc,yc,0.010),0xB25C70,0.5,1.0);            // окружность касания
addTwoPass(ring(r1,c1,0.009),0xB25C70,0.34,0.85);   // экватор сферы
// биллбордовый силуэт (контур) сферы — всегда к камере, чтобы шар читался
const silRing=new THREE.Mesh(new THREE.RingGeometry(r1*0.955,r1*1.022,96),
  new THREE.MeshBasicMaterial({color:0x7e2f3c,side:THREE.DoubleSide,transparent:true,opacity:1.0,depthTest:false}));
silRing.renderOrder=999; scene.add(silRing);
const _scen=new THREE.Vector3();
function updateSphereSil(){ _scen.set(0,c1,0); root.localToWorld(_scen); silRing.position.copy(_scen); silRing.quaternion.copy(camera.quaternion); }

// секущая плоскость + эллипс
{
  const e1=new THREE.Vector3(0,0,1), e2=new THREE.Vector3().crossVectors(n,e1).normalize();
  const Cen=n.clone().multiplyScalar(d);
  const pm=new THREE.Mesh(new THREE.PlaneGeometry(5.2,5.2),
    new THREE.MeshPhongMaterial({color:COL.plane,transparent:true,opacity:0.52,side:THREE.DoubleSide,depthWrite:false,shininess:14,specular:0x222a30}));
  pm.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(e1,e2,n)); pm.position.copy(Cen); pm.renderOrder=RO.plane; root.add(pm);
  const cs=[[1,1],[1,-1],[-1,-1],[-1,1]].map(([a,b])=>Cen.clone().addScaledVector(e1,a*2.6).addScaledVector(e2,b*2.6));
  const bl=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(cs),new THREE.LineBasicMaterial({color:COL.planeEdge,transparent:true,opacity:0.8,depthTest:false})); bl.renderOrder=RO.contour; root.add(bl);
  const pts=[]; for(let i=0;i<240;i++) pts.push(P(i/240*2*Math.PI));
  addTwoPass(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts,true),360,0.024,12,true),COL.sec,0.28,1.0);
}

// фокус
{ const g=new THREE.SphereGeometry(0.06,20,14); g.translate(F1.x,F1.y,F1.z); const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:COL.focus,depthTest:false})); m.renderOrder=RO.top; root.add(m); }

// ЗЕЛЁНАЯ горизонтальная плоскость окружности касания (y=yc)
{
  const pg=new THREE.Mesh(new THREE.PlaneGeometry(3.0,3.6),
    new THREE.MeshPhongMaterial({color:COL.green,transparent:true,opacity:0.30,side:THREE.DoubleSide,depthWrite:false,shininess:10}));
  pg.rotation.x=-Math.PI/2; pg.position.set((X0+0.6)/1,yc,0); pg.renderOrder=RO.plane+1; root.add(pg);
  const cz=[[ -1.4,-1.8],[0.6,-1.8],[0.6,1.8],[-1.4,1.8]].map(([x,z])=>new THREE.Vector3(x+0.0,yc,z));
  const gl=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(cz.map(v=>new THREE.Vector3((X0+0.6)+ (v.x), yc, v.z))),
    new THREE.LineBasicMaterial({color:COL.dir,transparent:true,opacity:0.5,depthTest:false})); gl.renderOrder=RO.contour; root.add(gl);
}

// ДИРЕКТРИСА — пересечение зелёной и секущей плоскостей (x=X0, y=yc)
addTwoPass(span(new THREE.Vector3(X0,yc,-1.6),new THREE.Vector3(X0,yc,1.6),0.024),COL.dir,0.45,1.0,RO.top);

// силуэт конуса
function makeSil(){ const g=new THREE.CylinderGeometry(0.008,0.008,1,10); g.translate(0,0.5,0); return contour(g,COL.ink,0.82); }
const sil=[makeSil(),makeSil()]; const APEX=new THREE.Vector3();
function orientSpan(m,p1,p2){ const dir=new THREE.Vector3().subVectors(p2,p1),len=dir.length(); m.position.copy(p1); m.scale.set(1,len,1); m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize()); }
function uu2(phi){ return new THREE.Vector3(sinA*Math.cos(phi),cosA,sinA*Math.sin(phi)); }
function updateSil(camLocal){ const R=Math.hypot(camLocal.x,camLocal.z), k=tanA*camLocal.y/Math.max(R,1e-6);
  if(Math.abs(k)>=1){ sil.forEach(m=>m.visible=false); return; } const phi=Math.atan2(camLocal.z,camLocal.x), dphi=Math.acos(k);
  [phi+dphi,phi-dphi].forEach((th,i)=>{ sil[i].visible=true; orientSpan(sil[i],APEX,uu2(th).multiplyScalar(tTop)); }); }

// тень
{ const cv=document.createElement('canvas'); cv.width=cv.height=256; const g=cv.getContext('2d');
  const gr=g.createRadialGradient(128,128,8,128,128,126); gr.addColorStop(0,'rgba(74,63,51,1)'); gr.addColorStop(1,'rgba(74,63,51,0)');
  g.fillStyle=gr; g.fillRect(0,0,256,256);
  const sh=new THREE.Mesh(new THREE.PlaneGeometry(6,6),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,opacity:0.13,depthWrite:false}));
  sh.rotation.x=-Math.PI/2; sh.rotation.z=Math.atan2(5,6); sh.position.set(-0.5,-2.5,-0.4); sh.scale.set(1.1,0.8,1); sh.renderOrder=RO.shadow; scene.add(sh); }

// камера
const target=new THREE.Vector3(0,0.85,0); const SPIN=0.0052;
let az=0.35, el=0.20, dist=8.4;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches; let auto=!reduced, dragging=false, px=0, py=0;
if(q.has('az')) az=parseFloat(q.get('az'))*DEG; if(q.has('el')) el=parseFloat(q.get('el'))*DEG; if(q.has('dist')) dist=parseFloat(q.get('dist'));
if(q.has('still')){ auto=false; document.getElementById('hint').style.display='none'; }
function place(){ camera.position.set(target.x+dist*Math.cos(el)*Math.cos(az),target.y+dist*Math.sin(el),target.z+dist*Math.cos(el)*Math.sin(az)); camera.lookAt(target); }
const dom=renderer.domElement; const playbtn=document.getElementById('playbtn'); function syncPlay(){ playbtn.textContent=auto?'❚❚':'▶'; }
playbtn.onclick=()=>{ auto=!auto; syncPlay(); }; syncPlay();
dom.addEventListener('pointerdown',e=>{dragging=true;auto=false;syncPlay();px=e.clientX;py=e.clientY;dom.setPointerCapture(e.pointerId);});
dom.addEventListener('pointerup',()=>dragging=false);
dom.addEventListener('pointermove',e=>{ if(!dragging) return; az+=(e.clientX-px)*0.0055; el+=(e.clientY-py)*0.0045; el=Math.max(-1.35,Math.min(1.35,el)); px=e.clientX; py=e.clientY;});
dom.addEventListener('wheel',e=>{e.preventDefault(); dist*=(1+Math.sign(e.deltaY)*0.07); dist=Math.max(5,Math.min(20,dist));},{passive:false});
function resize(){ renderer.setSize(innerWidth,innerHeight); camera.aspect=innerWidth/innerHeight; camera.updateProjectionMatrix(); }
addEventListener('resize',resize); resize();
const camLocal=new THREE.Vector3();
function frame(){ requestAnimationFrame(frame); if(auto&&!dragging) az+=SPIN; place();
  camLocal.copy(camera.position); root.worldToLocal(camLocal); updateSil(camLocal); updateSphereSil(); renderer.render(scene,camera); }
frame();
window.__shot=function(){ place(); camLocal.copy(camera.position); root.worldToLocal(camLocal); updateSil(camLocal); updateSphereSil(); renderer.render(scene,camera); return renderer.domElement.toDataURL('image/png'); };
;window.addEventListener('message',function(ev){var d=ev.data||{};if(d.goStep!=null){try{goStep(d.goStep);}catch(e){}}});})();
