const {chromium}=require('playwright');
const S='Прямоугольники',M='Множества — ещё';
const T=[[S,1,['15','6','21'],[],-1],[S,2,['2','3','6'],[],-1],[S,3,['60','24','84'],[],-1],[S,4,['80','12','92','150','30','180'],[],-1],[S,5,['10','80','30','150'],[],-1],[S,6,['15','20','35'],[],-1],[S,7,[],[],1],[S,8,['20','14','20'],[],-1],[S,9,['60','8','68','120','42','162'],[],-1],
[M,1,['4'],[0,1,0],-1],[M,2,[],[0,1,0],-1],[M,3,[],[0,1,1],-1],[M,4,['10, 11, 12, 13, 14'],[],-1],[M,5,['4;3','5 4 3 2 1'],[],-1],[M,6,['3,4'],[0,0],-1],[M,7,[],[],0],[M,8,[],[],1],[M,9,['2,4,6,8'],[0,1],-1],[M,9,['0 2 4 6 8'],[0,1],-1]];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});let f=0;const errs=[];
for(const [sec,i,vals,picks,opt] of T){const c=await b.newContext({viewport:{width:1440,height:810}});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));await p.goto('http://localhost:8766/zanyatie-2026-10-04.html');await p.waitForTimeout(150);
 await p.click('.skip');const TT=await p.$$eval('.jump .jr span',x=>x.map(e=>e.textContent));await p.click(`.jump .jr:nth-child(${TT.indexOf(sec)+1}) button:nth-of-type(${i})`);await p.waitForTimeout(150);
 const ins=await p.$$('main input.slot:not(.free)');if(ins.length!==vals.length){console.log('slots mismatch',sec,i,ins.length);f++;}
 for(let j=0;j<vals.length&&j<ins.length;j++)await ins[j].fill(vals[j]);const segs=await p.$$('main .seg');if(segs.length!==picks.length){console.log('seg mismatch',sec,i,segs.length);f++;}for(let j=0;j<picks.length&&j<segs.length;j++){const bs=await segs[j].$$('button');await bs[picks[j]].click();}
 if(opt>=0)await p.click(`main .opt >> nth=${opt}`);
 await p.click('.bot .chk');const t=(await p.textContent('.bot .chk')).trim();if(!t.includes('Верно')){f++;console.log('FAIL',sec,i,t);}
 if(i===1||(sec===M&&i===6)||(sec===S&&i===7))await p.screenshot({path:`/home/claude/n-${sec===S?'s':'m'}${i}.png`});await c.close();}
console.log('FAILS',f,'of',T.length,'errs',JSON.stringify(errs));await b.close();})();
