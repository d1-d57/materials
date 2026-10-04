// Автопроверка занятия 4.10: ДЗ 27.09 (строки переразмечены) + рыцари, раскраски, камни, секретная, лавка.
// Запуск: в папке dvizhok `python3 -m http.server 8766 &` и `node test_zanyatie-2026-10-04.js`. Итог: FAILS 0 of N.
const {chromium}=require('playwright');
// [section row (1-based in jump), item (1-based), actions, expect]
const T=[];
const sl=(r,i,vals,exp,tag)=>T.push({r,i,k:'slots',vals,exp,tag});
const fx=(r,i,vals,exp,tag)=>T.push({r,i,k:'fix',vals,exp,tag});
const sg=(r,i,picks,exp,tag)=>T.push({r,i,k:'seg',picks,exp,tag});
const ch=(r,i,opt,exp,tag)=>T.push({r,i,k:'choice',opt,exp,tag});
const gr=(r,i,sol,exp,tag)=>T.push({r,i,k:'grid',sol,exp,tag});
// Разбей удобно (row 2)
sl(4,1,['5','320','80','400'],true,'20+5'); sl(4,1,['5','80','320','400'],true,'20+5 swap'); sl(4,1,['5','320','80','401'],false,'20+5 wrong');
sl(4,2,['4','100','400'],true); sl(4,2,['4','100','399'],false);
sl(4,3,['20','4','300','60','360'],true,'24=20+4'); sl(4,3,['14','10','210','150','360'],true,'24=14+10'); sl(4,3,['20','4','300','60','350'],false);
sl(4,4,['450'],true); sl(4,4,[' 0450'],true,'leading zero'); sl(4,4,['451'],false);
sl(4,5,['2000'],true); sl(4,5,['2 000'],true,'space');
// Найди ошибку (row 3): fix inputs order
fx(5,1,['20','16','5','16'],true,'misha 20+5'); fx(5,1,['25','10','25','6'],true,'misha 16=10+6'); fx(5,1,['20','20','5','0'],false,'misha fake'); fx(5,1,['20','10','5','6'],false,'misha orig');
fx(5,2,['28','7','4'],true); fx(5,2,['7','28','4'],false);
fx(5,3,['100','6','6'],true); fx(5,3,['100','6','1'],false);
fx(5,4,['1','15','0','4','25','15','0'],true); fx(5,4,['1','15','0','4','25','15','25'],false);
fx(5,5,['40','25','8','25'],true,'lena 40+8'); fx(5,5,['48','20','48','5'],true,'lena 20+5'); fx(5,5,['40','20','8','5'],false,'lena orig');
// Порядок действий (row 5)
sl(6,1,['2','14'],true); sl(6,2,['3','37'],true); sl(6,3,['70','10','90'],true); sl(6,4,['17','0','4','13'],true); sl(6,5,['100','3700'],true); sl(6,6,['13000'],true); sl(6,6,['13 000'],true);
// Множества (row 6)
T.push({r:7,i:1,k:'slots',vals:['9; 4','1, 4, 6, 7, 9'],exp:true,tag:'sets any sep'}); T.push({r:7,i:1,k:'slots',vals:['{4;9}','{1;4;6;7;9}'],exp:true}); T.push({r:7,i:1,k:'slots',vals:['4;9','1;4;6;7'],exp:false});
sg(7,2,[0,1,0,1,0],true); sg(7,2,[1,1,0,1,0],false);
sg(7,3,[0,1],true); sg(7,3,[1,0],false);
ch(7,4,1,true); ch(7,4,0,false);
sg(7,5,[0,1,0,0],true); sg(7,5,[0,1,1,1],false,'his error');
sg(7,6,[0,1,1,1],true);
// Задача (row 8)
sl(12,1,['6','7','7','84'],true); sl(12,2,['2','2','84'],true); sl(12,3,['24'],true);
// головоломки
gr(11,1,[[1,3,2,4],[2,4,3,1],[3,1,4,2],[4,2,1,3]],true); gr(11,2,[[2,4,1,3],[1,3,2,4],[3,2,4,1],[4,1,3,2]],true);
gr(14,1,[[2,1,4,3],[1,2,3,4],[4,3,1,2],[3,4,2,1]],true,'futo');

// ---- новое 4.10 ----
const mx=(r,i,vals,picks,exp,tag)=>T.push({r,i,k:'mix',vals,picks,exp,tag});
const cm=(r,i,opts,exp,tag)=>T.push({r,i,k:'multi',opts,exp,tag});
// Рыцари (row 4)
sl(2,1,['2'],true); sl(2,1,['3'],false);
sg(2,2,[0,0,1,1],true); sg(2,2,[0,1,1,1],false);
sl(2,3,['2'],true); sl(2,3,['1'],false);
sg(2,4,[0,0,1],true); sg(2,4,[1,0,1],false);
sg(2,5,[1,0,1],true); sg(2,5,[0,1,0],false);
// Раскраски (row 7)
sl(8,1,['13','12'],true); sl(8,1,['12','13'],false);
mx(8,2,['24','12','1'],[0],true); mx(8,2,['24','12','1'],[1],false);
cm(8,3,[0,2],true); cm(8,3,[0],false,'only one'); cm(8,3,[0,1],false);
sg(8,4,[1,0,1],true); sg(8,4,[1,0,0],false);
sg(8,5,[1,0,1],true); sg(8,5,[1,1,1],false);
// Камни (row 10)
sg(13,1,[1,0,1],true); sg(13,1,[0,0,1],false);
sl(13,2,['2, 5, 7, 10, 12'],true,'set commas'); sl(13,2,['12 10 7 5 2'],true,'set spaces'); sl(13,2,['2;5;7;10'],false);
mx(13,3,['1'],[1,0],true); mx(13,3,['4'],[1,0],false);
// Секретная (row 12, куплена в init)
sg(15,1,[0,0,1,1],true); sg(15,1,[0,0,0,1],false);
const OLD=['Занятие 4 октября','Рыцари и лжецы','Минутка','Разбей удобно','Найди ошибку','Порядок действий','Множества','Раскраски','Минутка','Перерыв','Судоку','Задача','Камни','Футошики','Секретная задача','Ваня приседает 10 раз','Задача для Вани','Игра на выбор','Готово'];
let TT=null;const R=async(p,r)=>{if(!TT)TT=await p.$$eval('.jump .jr span',x=>x.map(e=>e.textContent));return TT.indexOf(OLD[r-1])+1;};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const res=[];let fails=0;
const URL='http://localhost:8766/zanyatie-2026-10-04.html';
async function page(init){const ctx=await b.newContext({viewport:{width:1440,height:810}});await ctx.addInitScript(init);const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto(URL);await p.waitForTimeout(150);return {ctx,p,errs};}
const ALL=`localStorage.setItem('misha:bought',JSON.stringify(['sekret-1','igra-1','vanya-sit-1','vanya-task-1','labirint-1']));`;
for(const t of T){const {ctx,p,errs}=await page(ALL);
 await p.click('.skip');{const rr=await R(p,t.r);await p.click(`.jump .jr:nth-child(${rr}) button:nth-of-type(${t.i})`);}await p.waitForTimeout(120);
 if(t.k==='slots'||t.k==='mix'){const ins=await p.$$('main input.slot:not(.free)');for(let j=0;j<t.vals.length;j++)await ins[j].fill(t.vals[j]);}
 if(t.k==='fix'){const ins=await p.$$('main input.num');for(let j=0;j<t.vals.length;j++)await ins[j].fill(t.vals[j]);}
 if(t.k==='seg'||t.k==='mix'){const segs=await p.$$('main .seg');for(let j=0;j<t.picks.length;j++){const bs=await segs[j].$$('button');await bs[t.picks[j]].click();}}
 if(t.k==='choice'){await p.click(`main .opt >> nth=${t.opt}`);}
 if(t.k==='multi'){for(const o of t.opts)await p.click(`main .opt >> nth=${o}`);}
 if(t.k==='grid'){const cells=await p.$$('main .pc');for(let j=0;j<16;j++){if(await cells[j].evaluate(e=>e.classList.contains('fix')))continue;await cells[j].click();await p.keyboard.press(String(t.sol[j>>2][j&3]));}}
 await p.click('.bot .chk');const txt=(await p.textContent('.bot .chk')).trim();const got=txt.includes('Верно')?true:txt.includes('Ещё')?false:null;
 const ok=t.exp===null?true:got===t.exp; if(!ok)fails++;
 res.push(`${ok?'ok  ':'FAIL'} ${t.r}.${t.i} ${t.tag||''} exp=${t.exp} got=${got} ${errs.length?'ERR '+errs[0]:''}`);await ctx.close();}
// лавка: 10 звёзд, ничего не куплено → замок, покупка за 5, остаток 5, задача открылась
{const {ctx,p,errs}=await page(`localStorage.setItem('misha:stars','10');localStorage.removeItem('misha:spent');localStorage.removeItem('misha:bought');`);
 await p.click('.skip');{const rr=await R(p,15);await p.click(`.jump .jr:nth-child(${rr}) button:nth-of-type(1)`);}await p.waitForTimeout(120);
 const lockOk=!!(await p.$('.cover .buy'))&&!(await p.$eval('.cover .buy',e=>e.disabled));await p.click('.cover .buy');await p.waitForTimeout(120);
 const opened=!!(await p.$('main .seg'));const w=(await p.textContent('.stars b')).trim();
 const _x=!(await p.$eval('.bot .next',e=>e.disabled));
 const ok=lockOk&&opened&&w==='6';if(!ok)fails++;res.push(`${ok?'ok  ':'FAIL'} shop buy lock=${lockOk} opened=${opened} wallet=${w} ${errs.join(';')}`);
 // нехватка: igra-1 стоит 8, осталось 5 → кнопка неактивна, «дальше» открыта
 await p.click('.skip');{const rr=await R(p,18);await p.click(`.jump .jr:nth-child(${rr}) button:nth-of-type(1)`);}await p.waitForTimeout(120);
 const dis=await p.$eval('.cover .buy',e=>e.disabled);const nx=!(await p.$eval('.bot .next',e=>e.disabled));
 const ok2=dis&&nx;if(!ok2)fails++;res.push(`${ok2?'ok  ':'FAIL'} shop not enough disabled=${dis} next=${nx}`);
 // звезда за верный ответ пополняет копилку
 await p.click('.skip');{const rr=await R(p,2);await p.click(`.jump .jr:nth-child(${rr}) button:nth-of-type(1)`);}await p.waitForTimeout(120);
 await p.fill('main input.slot','2');await p.click('.bot .chk');const w2=(await p.textContent('.stars b')).trim();
 const ok3=w2==='7';if(!ok3)fails++;res.push(`${ok3?'ok  ':'FAIL'} star adds to wallet ${w2}`);await ctx.close();}
console.log(res.join('\n'));console.log('FAILS',fails,'of',T.length+3);await b.close();})();
