// Автопроверка ДЗ 27.09: каждый пункт — верный ответ (и ВСЕ разумные альтернативы) проходит, неверный — нет.
// Запуск: в папке dvizhok `python3 -m http.server 8766 &` и `node test_dz-2026-09-27.js`. Требует playwright. Итог: строка FAILS 0 of N.
const {chromium}=require('playwright');
// [section row (1-based in jump), item (1-based), actions, expect]
const T=[];
const sl=(r,i,vals,exp,tag)=>T.push({r,i,k:'slots',vals,exp,tag});
const fx=(r,i,vals,exp,tag)=>T.push({r,i,k:'fix',vals,exp,tag});
const sg=(r,i,picks,exp,tag)=>T.push({r,i,k:'seg',picks,exp,tag});
const ch=(r,i,opt,exp,tag)=>T.push({r,i,k:'choice',opt,exp,tag});
const gr=(r,i,sol,exp,tag)=>T.push({r,i,k:'grid',sol,exp,tag});
// Разбей удобно (row 2)
sl(2,1,['5','320','80','400'],true,'20+5'); sl(2,1,['5','80','320','400'],true,'20+5 swap'); sl(2,1,['5','320','80','401'],false,'20+5 wrong');
sl(2,2,['4','100','400'],true); sl(2,2,['4','100','399'],false);
sl(2,3,['20','4','300','60','360'],true,'24=20+4'); sl(2,3,['14','10','210','150','360'],true,'24=14+10'); sl(2,3,['20','4','300','60','350'],false);
sl(2,4,['450'],true); sl(2,4,[' 0450'],true,'leading zero'); sl(2,4,['451'],false);
sl(2,5,['2000'],true); sl(2,5,['2 000'],true,'space');
// Найди ошибку (row 3): fix inputs order
fx(3,1,['20','16','5','16'],true,'misha 20+5'); fx(3,1,['25','10','25','6'],true,'misha 16=10+6'); fx(3,1,['20','20','5','0'],false,'misha fake'); fx(3,1,['20','10','5','6'],false,'misha orig');
fx(3,2,['28','7','4'],true); fx(3,2,['7','28','4'],false);
fx(3,3,['100','6','6'],true); fx(3,3,['100','6','1'],false);
fx(3,4,['1','15','0','4','25','15','0'],true); fx(3,4,['1','15','0','4','25','15','25'],false);
fx(3,5,['40','25','8','25'],true,'lena 40+8'); fx(3,5,['48','20','48','5'],true,'lena 20+5'); fx(3,5,['40','20','8','5'],false,'lena orig');
// Порядок действий (row 5)
sl(5,1,['2','14'],true); sl(5,2,['3','37'],true); sl(5,3,['70','10','90'],true); sl(5,4,['17','0','4','13'],true); sl(5,5,['100','3700'],true); sl(5,6,['13000'],true); sl(5,6,['13 000'],true);
// Множества (row 6)
T.push({r:6,i:1,k:'slots',vals:['9; 4','1, 4, 6, 7, 9'],exp:true,tag:'sets any sep'}); T.push({r:6,i:1,k:'slots',vals:['{4;9}','{1;4;6;7;9}'],exp:true}); T.push({r:6,i:1,k:'slots',vals:['4;9','1;4;6;7'],exp:false});
sg(6,2,[0,1,0,1,0],true); sg(6,2,[1,1,0,1,0],false);
sg(6,3,[0,1],true); sg(6,3,[1,0],false);
ch(6,4,1,true); ch(6,4,0,false);
sg(6,5,[0,1,0,0],true); sg(6,5,[0,1,1,1],false,'his error');
sg(6,6,[0,1,1,1],true);
// Задача (row 8)
sl(8,1,['6','7','7','84'],true); sl(8,2,['2','2','84'],true); sl(8,3,['24'],true);
// головоломки
gr(4,1,[[1,3,2,4],[2,4,3,1],[3,1,4,2],[4,2,1,3]],true); gr(4,2,[[2,4,1,3],[1,3,2,4],[3,2,4,1],[4,1,3,2]],true);
gr(7,1,[[2,1,4,3],[1,2,3,4],[4,3,1,2],[3,4,2,1]],true,'futo');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const res=[];let fails=0;
for(const t of T){const ctx=await b.newContext({viewport:{width:1440,height:810}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8766/dz-2026-09-27.html');await p.waitForTimeout(150);
 await p.click('.skip');await p.click(`.jump .jr:nth-child(${t.r}) button:nth-of-type(${t.i})`);await p.waitForTimeout(120);
 if(t.k==='slots'){const ins=await p.$$('main input.slot:not(.free)');for(let j=0;j<t.vals.length;j++)await ins[j].fill(t.vals[j]);}
 if(t.k==='fix'){const ins=await p.$$('main input.num');for(let j=0;j<t.vals.length;j++)await ins[j].fill(t.vals[j]);}
 if(t.k==='seg'){const segs=await p.$$('main .seg');for(let j=0;j<t.picks.length;j++){const bs=await segs[j].$$('button');await bs[t.picks[j]].click();}}
 if(t.k==='choice'){await p.click(`main .opt >> nth=${t.opt}`);}
 if(t.k==='grid'){const cells=await p.$$('main .pc');for(let j=0;j<16;j++){if(await cells[j].evaluate(e=>e.classList.contains('fix')))continue;await cells[j].click();await p.keyboard.press(String(t.sol[j>>2][j&3]));}}
 await p.click('.bot .chk');const txt=(await p.textContent('.bot .chk')).trim();const got=txt.includes('Верно')?true:txt.includes('Ещё')?false:null;
 const ok=t.exp===null?true:got===t.exp; if(!ok)fails++;
 res.push(`${ok?'ok  ':'FAIL'} ${t.r}.${t.i} ${t.tag||''} exp=${t.exp} got=${got} ${errs.length?'ERR '+errs[0]:''}`);await ctx.close();}
console.log(res.join('\n'));console.log('FAILS',fails,'of',T.length);await b.close();})();
