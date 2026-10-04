const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const ctx=await b.newContext({viewport:{width:1440,height:810},colorScheme:'dark'});
await ctx.addInitScript(`if(!sessionStorage.x){localStorage.clear();localStorage.setItem('misha:stars','20');sessionStorage.x=1}`);
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('http://localhost:8766/zanyatie-2026-10-04.html');await p.waitForTimeout(300);
let TT=null;const jump=async(r,i)=>{await p.click('.skip');if(typeof r==='string'){if(!TT)TT=await p.$$eval('.jump .jr span',x=>x.map(e=>e.textContent));r=TT.indexOf(r)+1;}await p.click(`.jump .jr:nth-child(${r}) button:nth-of-type(${i})`);await p.waitForTimeout(150);};
const segs=async(picks)=>{const s=await p.$$('main .seg');for(let j=0;j<picks.length;j++){const bs=await s[j].$$('button');await bs[picks[j]].click();}};
// knights section all first-try -> streak and chest
await jump('Рыцари и лжецы',1);await p.fill('main input.slot','2');await p.click('.bot .chk');
await jump('Рыцари и лжецы',2);await segs([0,0,1,1]);await p.click('.bot .chk');
await jump('Рыцари и лжецы',3);await p.fill('main input.slot','2');await p.click('.bot .chk');const t1=await p.textContent('.toast');const fire=await p.textContent('.fire');
await jump('Рыцари и лжецы',4);await segs([0,0,1]);await p.click('.bot .chk');
await jump('Рыцари и лжецы',5);await segs([1,0,1]);await p.click('.bot .chk');const t2=await p.textContent('.toast');await p.waitForTimeout(1000);
const chest=!!(await p.$('.chest'));await p.screenshot({path:'/home/claude/f1.png'});
const w=await p.textContent('.stars b');
// picture: buy parizh (row 19) 
const rows=await p.$$eval('.jump .jr span',x=>x.map(e=>e.textContent));await p.click('.panel h2 button').catch(()=>{});
await p.click('.shopbtn');await p.waitForTimeout(200);await p.screenshot({path:'/home/claude/f7.png'});{const c=p.locator('.card',{hasText:'Осенний лес'});await c.click();await p.waitForTimeout(100);await p.screenshot({path:'/home/claude/f8.png'});await c.click();}await p.waitForTimeout(300);
const box=await p.$eval('.picf img',e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]});
for(const [fx,fy] of [[.2,.3],[.5,.5],[.6,.7]])await p.mouse.click(box[0]+box[2]*fx,box[1]+box[3]*fy);
const cnt=await p.textContent('.picside .cnt');const vb=await p.$('.vanya');const bb=await vb.boundingBox();
await p.mouse.move(bb.x+20,bb.y+10);await p.mouse.down();await p.waitForTimeout(1200);await p.mouse.up();
const w2=await p.textContent('.stars b');await p.screenshot({path:'/home/claude/f2.png'});
// maze
await p.click('.shopbtn');{const c=p.locator('.card',{hasText:'Лабиринт 2'});await c.click();await c.click();}await p.waitForTimeout(400);{const bx=await p.$eval('.picf img',e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]});for(const [fx,fy] of [[.5,.2],[.55,.3],[.45,.4],[.5,.55]])await p.mouse.click(bx[0]+bx[2]*fx,bx[1]+bx[3]*fy);}await p.screenshot({path:'/home/claude/f3.png'});
// final: code
await jump('Готово',1);await p.fill('.code .cin','тыква');await p.click('.code .cbtn');await p.waitForTimeout(300);
const w3=await p.textContent('.stars b');await p.screenshot({path:'/home/claude/f4.png'});
const nxt=await p.$eval('.bot .next',e=>e.disabled);console.log(JSON.stringify({nxt,t1,fire,t2,chest,w,cnt,w2,w3,errs}));await b.close();})();
