
(function(){
'use strict';
const DEG=Math.PI/180;
const alpha=22*DEG, sinA=Math.sin(alpha), cosA=Math.cos(alpha), tanA=Math.tan(alpha);
const Hc=4.8, Rc=Hc*tanA, tTop=Hc/cosA;
const q=new URLSearchParams(location.search);

const COL={ bg:0xFAF6E8, cone:0xEFBE3C, plane:0x84C0DC, sec:0xB83A2B,
            ink:0x3F352B, planeEdge:0x3E6675 };
const RO={ shadow:0, coneBack:1, plane:4, coneFront:7, proxy:9, ghost:10, crisp:11, contour:12 };

const holder=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setClearColor(COL.bg,1); renderer.outputEncoding=THREE.sRGBEncoding;
renderer.localClippingEnabled=true; THREE.ColorManagement.enabled=true;
holder.appendChild(renderer.domElement);

const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(42,1,0.1,100);
const key=new THREE.DirectionalLight(0xfff7ea,0.62); key.position.set(6,10,5); scene.add(key);
const fill=new THREE.DirectionalLight(0xe4edf4,0.18); fill.position.set(-6,4,-7); scene.add(fill);
scene.add(new THREE.AmbientLight(0xffffff,0.48));

const root=new THREE.Group();
root.rotation.x=Math.PI; root.position.y=Hc*0.5; scene.add(root);
root.updateMatrixWorld(true);

// ---------- материалы / помощники ----------
function bodyMat(color,opacity,side){ return new THREE.MeshPhongMaterial({color,transparent:true,
  opacity,side,depthWrite:false,shininess:22,specular:0x3a3328}); }
function addBody(geom,color,oF,oB,roB,roF){
  const back=new THREE.Mesh(geom,bodyMat(color,oB,THREE.BackSide));
  const front=new THREE.Mesh(geom,bodyMat(color,oF,THREE.FrontSide));
  back.renderOrder=roB; front.renderOrder=roF; root.add(back,front); return [back,front];
}
function proxyMat(){ return new THREE.MeshBasicMaterial({colorWrite:false,transparent:true,
  depthWrite:true,depthTest:true,side:THREE.FrontSide,polygonOffset:true,
  polygonOffsetFactor:1.2,polygonOffsetUnits:1.2}); }
function addProxy(geom){ const m=new THREE.Mesh(geom,proxyMat()); m.renderOrder=RO.proxy; root.add(m); return m; }
function ghostMat(c,o){ return new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:o,depthTest:false,depthWrite:false}); }
function crispMat(c,o){ return new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:o,depthTest:true,depthWrite:false}); }
function addTwoPass(geom,color,gO,cO,clip){
  const g=new THREE.Mesh(geom,ghostMat(color,gO)); g.renderOrder=RO.ghost;
  const c=new THREE.Mesh(geom,crispMat(color,cO)); c.renderOrder=RO.crisp;
  if(clip){ g.material.clippingPlanes=[clip]; c.material.clippingPlanes=[clip]; }
  root.add(g,c); return [g,c];
}
function contourMesh(geom,color,op){ const m=new THREE.Mesh(geom,
  new THREE.MeshBasicMaterial({color,transparent:true,opacity:op,depthTest:false,depthWrite:false}));
  m.renderOrder=RO.contour; root.add(m); return m; }
function spanGeom(p1,p2,rad){
  const dir=new THREE.Vector3().subVectors(p2,p1),len=dir.length();
  const g=new THREE.CylinderGeometry(rad,rad,1,10); g.translate(0,0.5,0); g.scale(1,len,1);
  g.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(
    new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize())));
  g.translate(p1.x,p1.y,p1.z); return g;
}
function ringGeom(radius,y,tube){ const g=new THREE.TorusGeometry(radius,tube,8,120);
  g.rotateX(Math.PI/2); g.translate(0,y,0); return g; }

// ---------- конус: нижняя пола (всегда) + верхняя (для гиперболы) ----------
const lowGeom=new THREE.LatheGeometry([new THREE.Vector2(0.001,0),new THREE.Vector2(Rc,Hc)],128);
const upGeom =new THREE.LatheGeometry([new THREE.Vector2(0.001,0),new THREE.Vector2(Rc,-Hc)],128);
addBody(lowGeom,COL.cone,0.46,0.12,RO.coneBack,RO.coneFront);
const upBodies=addBody(upGeom,COL.cone,0.46,0.12,RO.coneBack,RO.coneFront);
addProxy(lowGeom);
const upProxy=addProxy(upGeom);
addTwoPass(ringGeom(Rc,Hc,0.011),COL.ink,0.16,0.85);            // нижнее основание
const upBase=contourMesh(ringGeom(Rc,-Hc,0.011),COL.ink,0.85);

// силуэты пол (пересчёт за кадр)
function u(phi,sig){ return new THREE.Vector3(sinA*Math.cos(phi),sig*cosA,sinA*Math.sin(phi)); }
function makeSil(){ const g=new THREE.CylinderGeometry(0.008,0.008,1,10); g.translate(0,0.5,0);
  return contourMesh(g,COL.ink,0.82); }
const silLow=[makeSil(),makeSil()], silUp=[makeSil(),makeSil()];
const APEX=new THREE.Vector3();
function orientSpan(mesh,p1,p2){ const dir=new THREE.Vector3().subVectors(p2,p1),len=dir.length();
  mesh.position.copy(p1); mesh.scale.set(1,len,1);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize()); }
function updateSil(sils,sig,camLocal){
  const R=Math.hypot(camLocal.x,camLocal.z), k=tanA*(sig*camLocal.y)/Math.max(R,1e-6);
  if(Math.abs(k)>=1||R<1e-4){ sils.forEach(m=>m.visible=false); return; }
  const phi=Math.atan2(camLocal.z,camLocal.x), dphi=Math.acos(k);
  [phi+dphi,phi-dphi].forEach((th,i)=>{ sils[i].visible=true;
    orientSpan(sils[i],APEX,u(th,sig).multiplyScalar(tTop)); });
}

// ---------- секущая плоскость + сечение (пересобирается на тип) ----------
const planeGrp=new THREE.Group(); root.add(planeGrp);
const PWp=4.9, PHp=4.9, PHvis=7.3, PWvis=6.6;
const planeMesh=new THREE.Mesh(new THREE.PlaneGeometry(2*PWvis,2*PHvis),
  new THREE.MeshPhongMaterial({color:COL.plane,transparent:true,opacity:0.52,side:THREE.DoubleSide,
    depthWrite:false,shininess:14,specular:0x222a30}));
planeMesh.renderOrder=RO.plane; planeGrp.add(planeMesh);
let planeBorder=null, secMeshes=[], clipReveal=null, e2w=new THREE.Vector3(), p0w=new THREE.Vector3();

// тип сечения: угол наклона нормали от оси и высота точки p0
const TYPES={
  ellipse:  {thn:40*DEG, h0:Hc*0.52, both:false},
  parabola: {thn:68*DEG, h0:Hc*0.42, both:false},   // ≈ 90°−α: плоскость ∥ образующей
  hyperbola:{thn:82*DEG, h0:Hc*0.22, both:true}
};
const ORDER=['ellipse','parabola','hyperbola'];
const CAPS={ellipse:'эллипс',parabola:'парабола',hyperbola:'гипербола'};

function sectionBranches(N,p0,sig,Nphi){
  const branches=[]; let cur=[];
  for(let i=0;i<=Nphi;i++){
    const phi=i/Nphi*2*Math.PI;
    const g=new THREE.Vector3(tanA*Math.cos(phi),sig,tanA*Math.sin(phi));
    const den=N.dot(g); let pt=null;
    if(Math.abs(den)>1e-4){ const t=N.dot(p0)/den; if(t>0.03&&t<=Hc) pt=g.multiplyScalar(t); }
    if(pt) cur.push(pt); else { if(cur.length>1) branches.push(cur); cur=[]; }
  }
  if(cur.length>1) branches.push(cur);
  return branches;
}
function buildSection(type){
  // очистить старое
  secMeshes.forEach(m=>{ root.remove(m); m.geometry.dispose(); m.material.dispose(); });
  secMeshes=[];
  const T=TYPES[type];
  // кадрирование под тип: гипербола — двойной конус (прицел на вершину, дальше)
  target.y = T.both ? root.position.y : 0;
  if(!q.has('dist')) dist = T.both ? 16.5 : 11.5;
  const N=new THREE.Vector3(Math.sin(T.thn),Math.cos(T.thn),0).normalize();
  const p0=new THREE.Vector3(0,T.h0,0);
  // ориентация и положение плоскости
  const e1=new THREE.Vector3(0,0,1);
  const e2=new THREE.Vector3().crossVectors(N,e1).normalize();
  planeMesh.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(e1,e2,N));
  planeMesh.position.copy(p0);
  if(planeBorder){ planeGrp.remove(planeBorder); planeBorder.geometry.dispose(); planeBorder.material.dispose(); }
  const cs=[[1,1],[1,-1],[-1,-1],[-1,1]].map(([a,b])=>p0.clone().addScaledVector(e1,a*PWvis).addScaledVector(e2,b*PHvis));
  planeBorder=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(cs),
    new THREE.LineBasicMaterial({color:COL.planeEdge,transparent:true,opacity:0.8,depthTest:false}));
  planeBorder.renderOrder=RO.contour; planeGrp.add(planeBorder);
  // вторая пола — только для гиперболы
  upBodies.forEach(m=>m.visible=T.both); upProxy.visible=T.both;
  upBase.visible=T.both; silUp.forEach(m=>m.visible=T.both);
  // clip-reveal вдоль e2 (нож)
  p0w.copy(root.localToWorld(p0.clone()));
  e2w.copy(e2).transformDirection(root.matrixWorld).normalize();
  clipReveal=new THREE.Plane(e2w.clone(),0);
  // ветви сечения
  const sigs=T.both?[1,-1]:[1];
  for(const sig of sigs){
    const branches=sectionBranches(N,p0,sig,300);
    for(const br of branches){
      const closed=(br.length>285);  // почти весь φ → замкнутая (эллипс)
      const geom=new THREE.TubeGeometry(new THREE.CatmullRomCurve3(br,closed),
        Math.max(24,br.length),0.027,12,closed);
      secMeshes.push(...addTwoPass(geom,COL.sec,0.30,1.0,clipReveal));
    }
  }
  // запомнить e2-протяжённость точки p0 для порога
  planeGrp.userData.e2off = PHp*2.2;
}

// ---------- тень ----------
{
  const cv=document.createElement('canvas'); cv.width=cv.height=256; const g=cv.getContext('2d');
  const gr=g.createRadialGradient(128,128,8,128,128,126);
  gr.addColorStop(0,'rgba(74,63,51,1)'); gr.addColorStop(1,'rgba(74,63,51,0)');
  g.fillStyle=gr; g.fillRect(0,0,256,256);
  const sh=new THREE.Mesh(new THREE.PlaneGeometry(6.2,6.2),
    new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,opacity:0.14,depthWrite:false}));
  sh.rotation.x=-Math.PI/2; sh.rotation.z=Math.atan2(5,6);
  sh.position.set(-0.5,-Hc*0.5+0.01,-0.4); sh.scale.set(1.15,0.82,1);
  sh.renderOrder=RO.shadow; scene.add(sh);
}

// ---------- камера ----------
const target=new THREE.Vector3(0,0,0); const SPIN=0.0052;
let az=-0.62, el=0.18, dist=11.5;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
let auto=!reduced, dragging=false, px=0, py=0;
if(q.has('az')) az=parseFloat(q.get('az'))*DEG;
if(q.has('el')) el=parseFloat(q.get('el'))*DEG;
if(q.has('dist')) dist=parseFloat(q.get('dist'));
if(q.has('still')){ auto=false; document.getElementById('hint').style.display='none'; }
function placeCamera(){ camera.position.set(
  target.x+dist*Math.cos(el)*Math.cos(az), target.y+dist*Math.sin(el),
  target.z+dist*Math.cos(el)*Math.sin(az)); camera.lookAt(target); }
const dom=renderer.domElement;
const playbtn=document.getElementById('playbtn');
function syncPlay(){ playbtn.textContent=auto?'❚❚':'▶'; }
playbtn.onclick=()=>{ auto=!auto; syncPlay(); };
dom.addEventListener('pointerdown',e=>{dragging=true;auto=false;syncPlay();px=e.clientX;py=e.clientY;dom.setPointerCapture(e.pointerId);});
dom.addEventListener('pointerup',()=>dragging=false);
dom.addEventListener('pointermove',e=>{ if(!dragging) return;
  az+=(e.clientX-px)*0.0055; el+=(e.clientY-py)*0.0045;
  el=Math.max(-1.35,Math.min(1.35,el)); px=e.clientX; py=e.clientY;});
dom.addEventListener('wheel',e=>{e.preventDefault(); dist*=(1+Math.sign(e.deltaY)*0.07);
  dist=Math.max(6,Math.min(24,dist));},{passive:false});
function resize(){ const w=innerWidth,h=innerHeight; renderer.setSize(w,h);
  camera.aspect=w/h; camera.updateProjectionMatrix(); }
addEventListener('resize',resize); resize();

// ---------- шаги (типы) + нож ----------
let step=q.has('step')?(parseInt(q.get('step'))||0):0;
step=Math.max(0,Math.min(ORDER.length-1,step));
let pP=1;  // прогресс въезда ножа (старт сразу с готовым сечением; нож проигрывается при переключении типа)
const bar=document.getElementById('bar'),cap=document.getElementById('cap'),dotsEl=document.getElementById('dots');
const dotBtns=ORDER.map((_,i)=>{const b=document.createElement('button');b.onclick=()=>goStep(i);dotsEl.appendChild(b);return b;});
function refreshUI(){ cap.textContent=CAPS[ORDER[step]]; dotBtns.forEach((b,i)=>b.classList.toggle('on',i===step)); }
function goStep(i){ i=Math.max(0,Math.min(ORDER.length-1,i)); if(i!==step||!clipReveal){ step=i; buildSection(ORDER[step]); pP=0; } refreshUI(); }
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown','Enter','Space'].includes(e.code)){ goStep(step+1); e.preventDefault(); }
  else if(['ArrowLeft','PageUp','Backspace'].includes(e.code)){ goStep(step-1); e.preventDefault(); }
});
buildSection(ORDER[step]); refreshUI(); syncPlay();
if(q.has('still')||reduced){ pP=1; bar.style.display='none'; playbtn.style.display='none'; }
const frozen=q.has('pp'); if(frozen) pP=parseFloat(q.get('pp'));

function applyKnife(){
  const off=planeGrp.userData.e2off*(1-pP);
  planeGrp.position.copy(e2w).multiplyScalar(0);     // плоскость строится в p0; сдвигаем вдоль e2 локально
  // сдвиг плоскости вдоль локального e2:
  const e1=new THREE.Vector3(0,0,1), N=new THREE.Vector3(Math.sin(TYPES[ORDER[step]].thn),Math.cos(TYPES[ORDER[step]].thn),0).normalize();
  const e2l=new THREE.Vector3().crossVectors(N,e1).normalize();
  planeGrp.position.copy(e2l).multiplyScalar(off);
  planeMesh.material.opacity=0.52*pP;
  if(planeBorder) planeBorder.material.opacity=0.8*pP;
  planeGrp.visible=pP>0.002;
  // нож: открываем сечение там, где лезвие прошло (порог вдоль e2)
  const D=planeGrp.userData.e2off*(1-pP);
  if(clipReveal) clipReveal.constant=-(e2w.dot(p0w)+(D-PHp));
  secMeshes.forEach(m=>{ m.visible=pP>0.002; });
}

const camLocal=new THREE.Vector3();
function frame(){ requestAnimationFrame(frame);
  if(auto&&!dragging) az+=SPIN;
  if(pP<1 && !frozen) pP=Math.min(1,pP+(reduced?1:0.045));
  applyKnife();
  placeCamera();
  camLocal.copy(camera.position); root.worldToLocal(camLocal);
  updateSil(silLow,1,camLocal); if(TYPES[ORDER[step]].both) updateSil(silUp,-1,camLocal);
  renderer.render(scene,camera);
}
frame();
window.__shot=function(){ applyKnife(); placeCamera();
  camLocal.copy(camera.position); root.worldToLocal(camLocal);
  updateSil(silLow,1,camLocal); if(TYPES[ORDER[step]].both) updateSil(silUp,-1,camLocal);
  renderer.render(scene,camera); return renderer.domElement.toDataURL('image/png'); };
;window.addEventListener('message',function(ev){var d=ev.data||{};if(d.goStep!=null){try{goStep(d.goStep);}catch(e){}}});})();
