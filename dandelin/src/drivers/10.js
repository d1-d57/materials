
(function(){
'use strict';
const DEG = Math.PI/180;

// ---------- геометрия (проверена, дословно) ----------
const alpha = 22*DEG;
const sinA = Math.sin(alpha), cosA = Math.cos(alpha), tanA = Math.tan(alpha);
const c1 = 1.2, c2 = 3.4;
const r1 = c1*sinA, r2 = c2*sinA;
const ny = (c1+c2)*sinA/(c1-c2), nx = Math.sqrt(1-ny*ny);
const n  = new THREE.Vector3(nx, ny, 0);
const d  = ny*c1 - r1;
const C1 = new THREE.Vector3(0,c1,0), C2 = new THREE.Vector3(0,c2,0);
const F1 = C1.clone().addScaledVector(n,-r1);
const F2 = C2.clone().addScaledVector(n, r2);
const Hc = 4.8, Rc = Hc*tanA;
function u(th){ return new THREE.Vector3(sinA*Math.cos(th), cosA, sinA*Math.sin(th)); }
function P(th){ const uu=u(th); return uu.multiplyScalar(d/uu.dot(n)); }
const Cen = P(0).add(P(Math.PI)).multiplyScalar(0.5);

// ---------- палитра ----------
const COL = {
  bg:0xFAF6E8, cone:0xE6A92A, s1:0x46A75F, s2:0x9A60E4, plane:0x5BA9D4,
  ellipse:0xA4159B,            // версия 1: маджента-герой
  ellipsePlum:0xA1473A,        // версия 2 (выбрана): тёплый глиняно-красный
  focus:0xC96A3C, ink:0x3F352B, gen:0xA8661C,
  latS1:0x4E8F63, latS2:0x7E58A8, planeEdge:0x3E6675,
  proofRed:0xE11D48, proofBlue:0x2563EB
};
const q = new URLSearchParams(location.search);
let ellipseIsPlum = (q.get('ellipse')!=='magenta');  // по умолчанию глиняный
let ellipseColor = ellipseIsPlum ? COL.ellipsePlum : COL.ellipse;
let ellipseMeshes = null, ellipseGeom = null;

// слои рендера (всё прозрачно → один проход, порядок задаётся renderOrder)
const RO = { shadow:0, coneBack:1, sphFarBack:2, sphFarFront:3, plane:4,
             sphNearBack:5, sphNearFront:6, coneFront:7,
             proxy:9, ghost:10, crisp:11, contour:12 };

// ---------- рендерер / сцена ----------
const holder = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setClearColor(COL.bg,1);
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.localClippingEnabled = true;
THREE.ColorManagement.enabled = true;
holder.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42,1,0.1,100);

// свет фиксирован в мире — при облёте градиент/блик ползут по телам (сигнал вращения)
const key  = new THREE.DirectionalLight(0xfff7ea,0.82); key.position.set(6,10,5); scene.add(key);
const fill = new THREE.DirectionalLight(0xe4edf4,0.22); fill.position.set(-6,4,-7); scene.add(fill);
scene.add(new THREE.AmbientLight(0xffffff,0.34));

// корневая группа: математика «вершиной вниз», переворачиваем как в этюдах
const root = new THREE.Group();
root.rotation.x = Math.PI;        // y -> -y : вершина вверх
root.position.y = Hc + 0.55;      // основание парит над землёй
scene.add(root);
root.updateMatrixWorld(true);
const G = { sph:[], foc:[], pln:[], ell:[] };  // стадии (каркас фазы 1)

// ---------- тела: alpha-полупрозрачность двумя проходами (back/front) ----------
function bodyMat(color, opacity, side){
  return new THREE.MeshPhongMaterial({color, transparent:true, opacity, side,
    depthWrite:false, shininess:34, specular:0x4a4038});
}
function addBody(geom, color, oFront, oBack, roBack, roFront, clip){
  const mb = bodyMat(color,oBack ,THREE.BackSide);
  const mf = bodyMat(color,oFront,THREE.FrontSide);
  if(clip){ mb.clippingPlanes=[clip]; mf.clippingPlanes=[clip]; }
  const back  = new THREE.Mesh(geom, mb);
  const front = new THREE.Mesh(geom, mf);
  back.renderOrder = roBack; front.renderOrder = roFront;
  root.add(back, front);
  return [back, front];
}

// конус — открытая поверхность (lathe профиля)
const coneGeom = new THREE.LatheGeometry(
  [new THREE.Vector2(0.001,0), new THREE.Vector2(Rc,Hc)], 128);
addBody(coneGeom, COL.cone, 0.42, 0.16, RO.coneBack, RO.coneFront);

// мировые клип-плоскости по обе стороны секущей (мир статичен)
const clipPos = new THREE.Plane(n.clone(), -d).applyMatrix4(root.matrixWorld);
const clipNeg = clipPos.clone().negate();

// сферы — половинками относительно секущей плоскости
const s1g = new THREE.SphereGeometry(r1,64,48); s1g.translate(0,c1,0);
const s2g = new THREE.SphereGeometry(r2,96,64); s2g.translate(0,c2,0);
const halvesPos = [], halvesNeg = [];
halvesPos.push(...addBody(s1g, COL.s1, 0.60, 0.16, 0,0, clipPos));
halvesPos.push(...addBody(s2g, COL.s2, 0.60, 0.16, 0,0, clipPos));
halvesNeg.push(...addBody(s1g, COL.s1, 0.60, 0.16, 0,0, clipNeg));
halvesNeg.push(...addBody(s2g, COL.s2, 0.60, 0.16, 0,0, clipNeg));
G.sph.push(...halvesPos, ...halvesNeg);
[halvesPos[0],halvesPos[1],halvesNeg[0],halvesNeg[1]].forEach(m=>m.userData.cc=c1);
[halvesPos[2],halvesPos[3],halvesNeg[2],halvesNeg[3]].forEach(m=>m.userData.cc=c2);
function sortHalves(camWorld){
  const camOnPos = clipPos.distanceToPoint(camWorld) > 0;
  const near = camOnPos ? halvesPos : halvesNeg;
  const far  = camOnPos ? halvesNeg : halvesPos;
  far .forEach((m,i)=> m.renderOrder = (i%2===0) ? RO.sphFarBack  : RO.sphFarFront);
  near.forEach((m,i)=> m.renderOrder = (i%2===0) ? RO.sphNearBack : RO.sphNearFront);
}

// секущая плоскость
const e1 = new THREE.Vector3(0,0,1);
const e2 = new THREE.Vector3().crossVectors(n,e1).normalize();
const PW = 1.62, PH = 1.86;
const planeMesh = new THREE.Mesh(new THREE.PlaneGeometry(2*PW, 2*PH),
  new THREE.MeshPhongMaterial({color:COL.plane, transparent:true, opacity:0.46,
    side:THREE.DoubleSide, depthWrite:false, shininess:14, specular:0x222a30}));
planeMesh.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(e1, e2, n));
planeMesh.position.copy(Cen);
planeMesh.renderOrder = RO.plane;
const planeGrp = new THREE.Group(); root.add(planeGrp);
planeGrp.add(planeMesh); planeMesh.userData.op0 = 0.62; G.pln.push(planeMesh);
let planeBorder = null;

// ---------- depth-proxy: тела пишут ТОЛЬКО глубину (для линий) ----------
// прозрачный материал с depthWrite:true пишет глубину; colorWrite:false — невидим;
// polygonOffset отодвигает глубину прокси, чтобы линии НА поверхности не конфликтовали
function proxyMat(){
  return new THREE.MeshBasicMaterial({colorWrite:false, transparent:true,
    depthWrite:true, depthTest:true, side:THREE.FrontSide,
    polygonOffset:true, polygonOffsetFactor:1.2, polygonOffsetUnits:1.2});
}
function addProxy(geom){
  const m = new THREE.Mesh(geom, proxyMat());
  m.renderOrder = RO.proxy; root.add(m); return m;
}
addProxy(coneGeom);
{ const p1=addProxy(s1g); p1.userData.cc=c1; const p2=addProxy(s2g); p2.userData.cc=c2; G.sph.push(p1,p2); }

// ---------- ДВУХПРОХОДНЫЕ линии: призрак (за стеклом) + чёткая (ближняя) ----------
// ближняя проявляется только там, где перед ней нет тела (depthTest по прокси);
// призрак виден всюду слабо (depthTest:false) → дальняя дуга не исчезает, а тускнеет.
function ghostMat(color, op){ return new THREE.MeshBasicMaterial({color,
  transparent:true, opacity:op, depthTest:false, depthWrite:false}); }
function crispMat(color, op){ return new THREE.MeshBasicMaterial({color,
  transparent:true, opacity:op, depthTest:true,  depthWrite:false}); }
function addTwoPass(geom, color, ghostOp, crispOp){
  const g = new THREE.Mesh(geom, ghostMat(color,ghostOp)); g.renderOrder = RO.ghost;
  const c = new THREE.Mesh(geom, crispMat(color,crispOp)); c.renderOrder = RO.crisp;
  root.add(g, c); return [g, c];
}
// контур (всегда чёткий, поверх всего) — для силуэтов и рёбер
function contourMat(color, op){ return new THREE.MeshBasicMaterial({color,
  transparent:true, opacity:op, depthTest:false, depthWrite:false}); }
function addContourMesh(geom, color, op){
  const m = new THREE.Mesh(geom, contourMat(color,op)); m.renderOrder = RO.contour;
  root.add(m); return m;
}

// тор-кольцо в горизонтальной плоскости (широты, окружности касания)
function torusRing(radius, y, tube){
  const g = new THREE.TorusGeometry(radius, tube, 8, 96);
  g.rotateX(Math.PI/2); g.translate(0,y,0); return g;
}

// широты сфер — двухпроходные (ближняя дуга ярче дальней → читается объём)
function latitudes(c, r, color, lats, tube, gOp, cOp){
  for(const latDeg of lats){
    const la = latDeg*DEG;
    const ms=addTwoPass(torusRing(r*Math.cos(la), c + r*Math.sin(la), tube), color, gOp, cOp); ms.forEach(m=>m.userData.cc=c); G.sph.push(...ms);
  }
}
latitudes(c1, r1, COL.latS1, [-52,-24,24,52], 0.0072, 0.18, 0.64);  // верхняя — чуть жирнее/ярче
latitudes(c2, r2, COL.latS2, [-55,-28,0,28,55], 0.006, 0.16, 0.55);

// окружности касания сферы с конусом — двухпроходные, тёмные
{ const cr1=addTwoPass(torusRing(c1*sinA*cosA, c1*cosA*cosA, 0.007), COL.ink, 0.22, 0.9);
  cr1.forEach(m=>{m.userData.cc=c1; m.userData.op0=m.material.opacity; m.userData.grp='contact';}); G.sph.push(...cr1);
  const cr2=addTwoPass(torusRing(c2*sinA*cosA, c2*cosA*cosA, 0.010), COL.ink, 0.22, 0.9);
  cr2.forEach(m=>{m.userData.cc=c2; m.userData.op0=m.material.opacity; m.userData.grp='contact';}); G.sph.push(...cr2); }

// мировые e2 и центр — для «реза вслед за лезвием» (clip-reveal эллипса)
const Cenw = root.localToWorld(Cen.clone());
const e2w = e2.clone().transformDirection(root.matrixWorld).normalize();
const clipReveal = new THREE.Plane(e2w.clone(), 0);

// эллипс-сечение — герой, двухпроходный (приклеивается к конусу, тускнеет за телами)
{
  const pts=[]; for(let i=0;i<240;i++) pts.push(P(i/240*2*Math.PI));
  const geom = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts,true),360,0.027,12,true);
  ellipseMeshes = addTwoPass(geom, ellipseColor, 0.28, 1.0);
  ellipseMeshes.forEach(m=>{ m.userData.op0=m.material.opacity; m.material.clippingPlanes=[clipReveal]; });
  ellipseGeom = geom;
  G.ell.push(...ellipseMeshes);
}

// фокусы — двухпроходные (ярко спереди, слабо за телом)
for(const F of [F1,F2]){
  const geom = new THREE.SphereGeometry(0.06,24,16); geom.translate(F.x,F.y,F.z);
  G.foc.push(...addTwoPass(geom, COL.focus, 0.32, 1.0));
}
G.foc.forEach(m=>m.userData.op0=m.material.opacity);

// ОДНА образующая на фиксированном угле — «едет» при облёте = сигнал вращения
function spanGeom(geomLen, p1, p2){
  const dir = new THREE.Vector3().subVectors(p2,p1), len = dir.length();
  const g = new THREE.CylinderGeometry(0.0105,0.0105,1,12);
  g.translate(0,0.5,0); g.scale(1,len,1);
  const m = new THREE.Matrix4().makeRotationFromQuaternion(
    new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0), dir.normalize()));
  g.applyMatrix4(m); g.translate(p1.x,p1.y,p1.z); return g;
}
let genMeshes;
{
  const th0 = 0.95;
  const A0 = new THREE.Vector3(0,0,0);
  const B0 = new THREE.Vector3(Rc*Math.cos(th0), Hc, Rc*Math.sin(th0));
  const B1 = new THREE.Vector3(Rc*Math.cos(th0+Math.PI), Hc, Rc*Math.sin(th0+Math.PI));
  genMeshes = addTwoPass(spanGeom(null, A0, B0), COL.gen, 0.18, 0.72)
        .concat(addTwoPass(spanGeom(null, A0, B1), COL.gen, 0.18, 0.72));
  genMeshes.forEach(m=>m.userData.op0=m.material.opacity);
}

// ---------- фаза 2: доказательство (точку можно двигать) ----------
// отрезки/точки — ПОВЕРХ контуров (ro 13-15), толще и ярче, обновляются за кадр
const RO_PG=13, RO_PC=14, RO_PT=15;
function makeCyl(rad, ro, dTest, color, op){
  const g=new THREE.CylinderGeometry(rad,rad,1,12); g.translate(0,0.5,0);
  const m=new THREE.Mesh(g, new THREE.MeshBasicMaterial({color,transparent:true,opacity:op,depthTest:dTest,depthWrite:false}));
  m.renderOrder=ro; root.add(m); return m;
}
function makeSegment(color, rad, Garr){              // призрак(сквозь тела) + чёткий(поверх)
  const ghost=makeCyl(rad,RO_PG,false,color,0.22); ghost.userData.op0=0.22;
  const crisp=makeCyl(rad,RO_PC,true ,color,1.0 ); crisp.userData.op0=1.0;
  Garr.push(ghost,crisp); return {ghost,crisp};
}
function setSpan(seg,p1,p2){ orientSpan(seg.ghost,p1,p2); orientSpan(seg.crisp,p1,p2); }
function makeDot(color, rad, Garr){                  // точки — всегда поверх (важные)
  const m=new THREE.Mesh(new THREE.SphereGeometry(rad,20,14),
    new THREE.MeshBasicMaterial({color,transparent:true,opacity:1,depthTest:false,depthWrite:false}));
  m.renderOrder=RO_PT; root.add(m); m.userData.op0=1.0; Garr.push(m); return m;
}
function makeTicks(nn,color,Garr){ const a=[]; for(let i=0;i<nn;i++) a.push(makeSegment(color,0.018,Garr)); return a; }
G.pt=[]; G.r1=[]; G.r2=[];
const dotP=makeDot(0x2A2620,0.075,G.pt), dotA=makeDot(COL.proofRed,0.060,G.pt), dotB=makeDot(COL.proofBlue,0.060,G.pt);
const segPA =makeSegment(COL.proofRed ,0.019,G.r1), segPF1=makeSegment(COL.proofRed ,0.019,G.r1);
const segPB =makeSegment(COL.proofBlue,0.019,G.r2), segPF2=makeSegment(COL.proofBlue,0.019,G.r2);
const tkPA=makeTicks(1,COL.proofRed,G.r1), tkPF1=makeTicks(1,COL.proofRed,G.r1);
const tkPB=makeTicks(2,COL.proofBlue,G.r2), tkPF2=makeTicks(2,COL.proofBlue,G.r2);
function setTicks(tks,p1,p2){
  const mid=p1.clone().add(p2).multiplyScalar(0.5), dir=p2.clone().sub(p1).normalize();
  let perp=dir.clone().cross(camLocal.clone().sub(mid));   // перпендикуляр к отрезку и к взгляду
  if(perp.lengthSq()<1e-5) perp=dir.clone().cross(new THREE.Vector3(0,1,0));
  perp.normalize().multiplyScalar(0.065);
  const nn=tks.length;
  tks.forEach((t,i)=>{ const c=mid.clone().addScaledVector(dir,(i-(nn-1)/2)*0.085);
    setSpan(t, c.clone().sub(perp), c.clone().add(perp)); });
}
let thetaP = q.has('thp') ? parseFloat(q.get('thp')) : 5.3, pRun=false;
function proofPointLocal(){ const uu=u(thetaP); return uu.clone().multiplyScalar(d/uu.dot(n)); }
function updateProof(){
  const uu=u(thetaP);
  const Pp=uu.clone().multiplyScalar(d/uu.dot(n));
  const Ap=uu.clone().multiplyScalar(c1*cosA);
  const Bp=uu.clone().multiplyScalar(c2*cosA);
  dotP.position.copy(Pp); dotA.position.copy(Ap); dotB.position.copy(Bp);
  setSpan(segPA,Ap,Pp); setSpan(segPF1,Pp,F1);
  setSpan(segPB,Pp,Bp); setSpan(segPF2,Pp,F2);
  setTicks(tkPA,Ap,Pp); setTicks(tkPF1,Pp,F1);
  setTicks(tkPB,Pp,Bp); setTicks(tkPF2,Pp,F2);
}

// ---------- контуры: аналитические силуэты (пересчёт за кадр) ----------
// сфера: окружность-горизонт (единичный тор, масштабируем/ориентируем)
function makeHorizon(){
  const g = new THREE.TorusGeometry(1, 0.008, 8, 128);
  return addContourMesh(g, COL.ink, 0.82);
}
const silS1 = makeHorizon(), silS2 = makeHorizon();
G.sph.push(silS1, silS2); silS1.userData.sphere=1; silS2.userData.sphere=2;
function updateHorizon(m, S, r, camLocal, k){
  if(k<0.02){ m.visible=false; return; }
  r = r*k;
  const dir = new THREE.Vector3().subVectors(camLocal,S);
  const dist = dir.length();
  if(dist<=r*1.001){ m.visible=false; return; }
  m.visible=true; dir.divideScalar(dist);
  m.position.copy(S).addScaledVector(dir, r*r/dist);
  m.scale.setScalar(r*Math.sqrt(1-(r/dist)*(r/dist)));
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1), dir);
}
// конус: две силуэтные образующие  cos(th-phi)=tanA*Cy/R
const tTop = Hc/cosA, APEX = new THREE.Vector3();
const silGen = [0,1].map(()=>{
  const g = new THREE.CylinderGeometry(0.008,0.008,1,10); g.translate(0,0.5,0);
  return addContourMesh(g, COL.ink, 0.82);
});
function orientSpan(mesh, p1, p2){
  const dir = new THREE.Vector3().subVectors(p2,p1), len = dir.length();
  mesh.position.copy(p1); mesh.scale.set(1,len,1);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), dir.normalize());
}
function updateConeSil(camLocal){
  const R = Math.hypot(camLocal.x, camLocal.z);
  const k = tanA*camLocal.y/Math.max(R,1e-6);
  if(Math.abs(k)>=1 || R<1e-4){ silGen.forEach(m=>m.visible=false); return; }
  const phi = Math.atan2(camLocal.z, camLocal.x), dth = Math.acos(k);
  [phi+dth, phi-dth].forEach((th,i)=>{
    silGen[i].visible=true;
    orientSpan(silGen[i], APEX, u(th).multiplyScalar(tTop));
  });
}
// основание конуса — двухпроходное: передняя дуга чёткая, задняя тускнеет за конусом и нижними сферами
addTwoPass(torusRing(Rc, Hc, 0.011), COL.ink, 0.16, 0.85);
{
  const cs=[[1,1],[1,-1],[-1,-1],[-1,1]].map(([a,b])=>
    Cen.clone().addScaledVector(e1,a*PW).addScaledVector(e2,b*PH));
  const l = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(cs),
    new THREE.LineBasicMaterial({color:COL.planeEdge, transparent:true, opacity:0.85, depthTest:false}));
  l.renderOrder = RO.contour; planeGrp.add(l); l.userData.op0=0.85; planeBorder=l; G.pln.push(l);
}

// ---------- направленная тень: смещена от света, вытянута ----------
{
  const cv = document.createElement('canvas'); cv.width=cv.height=256;
  const g = cv.getContext('2d');
  const gr = g.createRadialGradient(128,128,8,128,128,126);
  gr.addColorStop(0,'rgba(74,63,51,1)'); gr.addColorStop(1,'rgba(74,63,51,0)');
  g.fillStyle=gr; g.fillRect(0,0,256,256);
  const tex = new THREE.CanvasTexture(cv);
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(6.0,6.0),
    new THREE.MeshBasicMaterial({map:tex, transparent:true, opacity:0.15, depthWrite:false}));
  sh.rotation.x = -Math.PI/2;
  // свет по горизонтали ~(6,5) в мире → тень падает в противоположную сторону, вытянута вдоль оси света
  sh.rotation.z = Math.atan2(5,6);
  sh.position.set(-0.55,0.0,-0.45); sh.scale.set(1.15,0.82,1);
  sh.renderOrder = RO.shadow; scene.add(sh);
}

// ---------- камера: орбита + деликатный автоповорот ----------
const target = new THREE.Vector3(0,2.7,0);
const SPIN = 0.0052;   // быстрее
let az = -0.62, el = 0.20, dist = 8.0;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let auto = !reduced, dragging=false, px=0, py=0;

if(q.has('az')) az = parseFloat(q.get('az'))*DEG;
if(q.has('el')) el = parseFloat(q.get('el'))*DEG;
if(q.has('dist')) dist = parseFloat(q.get('dist'));
if(q.has('still')){ auto=false; document.getElementById('hint').style.display='none'; }

function placeCamera(){
  camera.position.set(
    target.x + dist*Math.cos(el)*Math.cos(az),
    target.y + dist*Math.sin(el),
    target.z + dist*Math.cos(el)*Math.sin(az));
  camera.lookAt(target);
}
const dom = renderer.domElement;
const playbtn = document.getElementById('playbtn');
function syncPlay(){ playbtn.textContent = auto ? '❚❚' : '▶'; }
playbtn.onclick = ()=>{ auto=!auto; syncPlay(); };
const playP = document.getElementById('playP');
function syncPlayP(){ playP.textContent = pRun ? '❚❚ точка' : '▶ точка'; }
playP.onclick = ()=>{ pRun=!pRun; if(pRun){ goStep(6); auto=false; syncPlay(); } syncPlayP(); };
let draggingP=false;
function toScreen(v){ const p=v.clone().project(camera);
  return {x:(p.x*0.5+0.5)*innerWidth, y:(-p.y*0.5+0.5)*innerHeight}; }
function rayFromPointer(e){ const ndc=new THREE.Vector2((e.clientX/innerWidth)*2-1, -(e.clientY/innerHeight)*2+1);
  const rc=new THREE.Raycaster(); rc.setFromCamera(ndc,camera); return rc.ray; }
function nearestTheta(ray){ let best=thetaP, bd=Infinity;
  for(let i=0;i<120;i++){ const th=i/120*2*Math.PI; const uu=u(th);
    const Pw=root.localToWorld(uu.multiplyScalar(d/uu.dot(n)));
    const dd=ray.distanceSqToPoint(Pw); if(dd<bd){bd=dd;best=th;} }
  return best; }
dom.addEventListener('pointerdown',e=>{
  if(step>=4 && cur.pt>0.5){
    const sp=toScreen(root.localToWorld(proofPointLocal()));
    if(Math.hypot(e.clientX-sp.x, e.clientY-sp.y) < 38){ draggingP=true; pRun=false; syncPlayP(); dom.setPointerCapture(e.pointerId); return; }
  }
  dragging=true; auto=false; syncPlay(); px=e.clientX; py=e.clientY; dom.setPointerCapture(e.pointerId);
});
dom.addEventListener('pointerup',()=>{dragging=false; draggingP=false;});
dom.addEventListener('pointermove',e=>{
  if(draggingP){ thetaP = nearestTheta(rayFromPointer(e)); return; }
  if(!dragging) return;
  az += (e.clientX-px)*0.0055; el += (e.clientY-py)*0.0045;
  el = Math.max(-1.35, Math.min(1.35, el)); px=e.clientX; py=e.clientY;});
dom.addEventListener('wheel',e=>{e.preventDefault();
  dist *= (1+Math.sign(e.deltaY)*0.07); dist=Math.max(4,Math.min(18,dist));},{passive:false});

function resize(){
  const w=innerWidth,h=innerHeight;
  renderer.setSize(w,h); camera.aspect=w/h; camera.updateProjectionMatrix();
}
addEventListener('resize',resize); resize();

addEventListener('keydown',e=>{
  if(e.code==='KeyE' && ellipseMeshes){
    ellipseIsPlum = !ellipseIsPlum;
    const col = ellipseIsPlum ? COL.ellipsePlum : COL.ellipse;
    ellipseMeshes.forEach(m=> m.material.color.setHex(col));
  }
});

// ---------- цикл ----------
const camLocal = new THREE.Vector3();
function updateContours(){
  camLocal.copy(camera.position); root.worldToLocal(camLocal);
  updateHorizon(silS1, C1, r1, camLocal, cur.sK);
  updateHorizon(silS2, C2, r2, camLocal, cur.sK);
  updateConeSil(camLocal);
}
function frame(){
  requestAnimationFrame(frame);
  if(pRun){ thetaP += 0.010; auto=false; }
  if(auto && !dragging) az += SPIN;
  if(!frozen) ease(); applyAnim();
  placeCamera();
  sortHalves(camera.position);
  updateContours();
  updateProof();
  renderer.render(scene,camera);
}
// ---- анимация фазы 1: проявление по бетам ----
const BEAT = [
  {pP:0,sK:0,cO:0,fO:0,pt:0,r1:0,r2:0},  // 0 конус
  {pP:1,sK:0,cO:0,fO:0,pt:0,r1:0,r2:0},  // 1 рассекаем плоскостью
  {pP:1,sK:1,cO:1,fO:0,pt:0,r1:0,r2:0},  // 2 вписываем сферы
  {pP:1,sK:1,cO:1,fO:1,pt:0,r1:0,r2:0},  // 3 два фокуса
  {pP:1,sK:1,cO:1,fO:1,pt:1,r1:0,r2:0},  // 4 точка P + A,B
  {pP:1,sK:1,cO:1,fO:1,pt:1,r1:1,r2:0},  // 5 первая пара (красные равны)
  {pP:1,sK:1,cO:1,fO:1,pt:1,r1:1,r2:1},  // 6 вторая пара (синие равны)
];
const CAPS = ['конус','рассекаем плоскостью','вписываем две сферы','два фокуса','точка на эллипсе','первая пара равных','вторая пара равных'];
let step = q.has('step') ? (parseInt(q.get('step'))||0) : 0;
step = Math.max(0, Math.min(BEAT.length-1, step));
const cur = {pP:0,sK:0,cO:0,fO:0,pt:0,r1:0,r2:0};
const frozen = q.has('frz');
const PSLIDE = PH*2.4;
function smooth01(x){ x=Math.max(0,Math.min(1,x)); return x*x*(3-2*x); }
function ease(){
  const t = BEAT[step], lam = reduced ? 1 : 0.10;
  for(const k of ['pP','sK','cO','fO','pt','r1','r2']){
    let tgt = t[k];
    if(k==='cO' && cur.sK<0.9) tgt = Math.min(tgt, cur.cO);   // контакты — после раздувания
    cur[k] += (tgt-cur[k])*lam;
    if(Math.abs(tgt-cur[k])<0.0008) cur[k]=tgt;
  }
}
function applyAnim(){
  for(const m of G.sph){
    if(m.userData.sphere) continue;                 // силуэты — в updateHorizon
    const cc = m.userData.cc; if(cc===undefined) continue;
    m.scale.setScalar(cur.sK); m.position.y=(1-cur.sK)*cc;
    if(m.userData.grp==='contact'){ m.material.opacity=m.userData.op0*cur.cO; m.visible=cur.cO>0.002; }
    else m.visible = cur.sK>0.002;
  }
  planeGrp.position.copy(e2).multiplyScalar(PSLIDE*(1-cur.pP));
  planeMesh.material.opacity = planeMesh.userData.op0*cur.pP;
  if(planeBorder) planeBorder.material.opacity = planeBorder.userData.op0*cur.pP;
  planeGrp.visible = cur.pP>0.002;
  const D = PSLIDE*(1-cur.pP);
  clipReveal.constant = -(e2w.dot(Cenw) + (D - PH));   // рез открывается вслед за лезвием
  ellipseMeshes.forEach(m=>{ m.material.opacity=m.userData.op0; m.visible=cur.pP>0.002; });
  G.foc.forEach(m=>{ m.material.opacity=m.userData.op0*cur.fO; m.visible=cur.fO>0.002; });
  const setOp=(m,f)=>{ m.material.opacity=m.userData.op0*f; m.visible=f>0.002; };
  G.pt.forEach(m=>setOp(m,cur.pt));
  G.r1.forEach(m=>setOp(m,cur.r1));
  G.r2.forEach(m=>setOp(m,cur.r2));
  genMeshes.forEach(m=>{ m.material.opacity=m.userData.op0*(1-0.8*cur.pt); });   // янтарная гаснет под доказательство
}
// полоса шагов
const bar=document.getElementById('bar'), cap=document.getElementById('cap'), dotsEl=document.getElementById('dots');
let winLo=0, winHi=BEAT.length-1, winClk=false;
const dotBtns = BEAT.map((_,i)=>{ const b=document.createElement('button'); b.onclick=()=>{ if(winClk){ try{ window.parent.postMessage({navSub:i-winLo},'*'); }catch(e){} } }; dotsEl.appendChild(b); return b; });
function refreshUI(){ cap.textContent=CAPS[step]; dotBtns.forEach((b,i)=>{ b.classList.toggle('on',i===step); b.style.display=(i>=winLo&&i<=winHi)?'':'none'; }); }
function setWindow(lo,hi,clk){ winLo=lo; winHi=hi; winClk=clk; dotsEl.style.pointerEvents=clk?'auto':'none'; dotBtns.forEach(b=>{ b.style.cursor=clk?'pointer':'default'; }); refreshUI(); }
function goStep(i){ step=Math.max(0,Math.min(BEAT.length-1,i)); refreshUI(); }
function clickerNext(){
  if(step < BEAT.length-1){ goStep(step+1); }
  else if(!pRun){ pRun=true; auto=false; syncPlay(); syncPlayP(); }   // кульминация: точка бежит
  else { pRun=false; syncPlayP(); }                                    // уже бежит → стоп
}
function clickerPrev(){ if(pRun){ pRun=false; syncPlayP(); } else goStep(step-1); }
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown','Enter','Space'].includes(e.code)){ clickerNext(); e.preventDefault(); }
  else if(['ArrowLeft','PageUp','Backspace'].includes(e.code)){ clickerPrev(); e.preventDefault(); }
});
refreshUI();
if(q.has('still')||reduced){ Object.assign(cur, BEAT[step]); }
if(q.has('frz')){ const v=q.get('frz').split(',').map(Number); ['pP','sK','cO','fO','pt','r1','r2'].forEach((k,i)=>{ if(!isNaN(v[i])) cur[k]=v[i]; }); }
syncPlay(); syncPlayP();
if(q.has('still')){ bar.style.display='none'; playbtn.style.display='none'; playP.style.display='none'; }
applyAnim();

frame();

// хук для рендер-проверки (headless)
window.__shot = function(){
  applyAnim(); placeCamera(); sortHalves(camera.position); updateContours(); updateProof();
  renderer.render(scene,camera);
  return renderer.domElement.toDataURL('image/png');
};
;window.addEventListener('message',function(ev){var d=ev.data||{};if(d.goStep!=null){try{goStep(d.goStep);}catch(e){}}if(d.win){try{setWindow(d.win[0],d.win[1],!!d.clickable);}catch(e){}}});})();
