// Обход всего занятия кнопкой «→» (как ребёнок): каждый экран проходим, лавочные разделы в потоке не встречаются, ошибок страницы нет.
// + сценарий лавки: покупка из середины, метки, «Ваня проверил», возврат «→» туда, где был; перезагрузка сохраняет всё.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});let fails=0;const out=[];
const ctx=await b.newContext({viewport:{width:1440,height:810}});await ctx.addInitScript(`if(!sessionStorage.x){localStorage.clear();sessionStorage.x=1}`);
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('http://localhost:8766/zanyatie-2026-10-04.html');await p.waitForTimeout(300);
const seen=[];let steps=0;
while(steps++<200){const sec=(await p.textContent('.sec')).trim();seen.push(sec);
  const big=await p.$('.cover .big:not(.shopbig)');
  if(big){if(sec.startsWith('Готово'))break;await big.click();await p.waitForTimeout(80);continue;}
  const fin=await p.$('.cover .sum');if(fin)break;
  let dis=await p.$eval('.bot .next',e=>e.disabled);
  if(dis){for(const i of await p.$$('main input.slot:not(.free)'))await i.fill('1');
    for(const s of await p.$$('main .seg')){const bs=await s.$$('button');await bs[0].click();}
    const o=await p.$('main .opt');if(o)await o.click();
    await p.click('.bot .chk');await p.waitForTimeout(60);dis=await p.$eval('.bot .next',e=>e.disabled);}
  if(dis){fails++;out.push('FAIL stuck at '+sec);break;}
  await p.click('.bot .next');await p.waitForTimeout(80);}
const shopT=['Секретная задача','Ваня приседает','Задача для Вани','Игра на выбор','Картина','Лабиринт','Ваня говорит','Ваня рисует','Математический фокус'];
const leaked=seen.filter(s=>shopT.some(t=>s.startsWith(t)));
const reached=seen.some(s=>s.startsWith('Готово'));
if(leaked.length||!reached){fails++;}out.push(`${leaked.length||!reached?'FAIL':'ok  '} обход: шагов ${steps}, дошёл до «Готово» ${reached}, лавочных в потоке ${leaked.length}`);
const stars=+(await p.textContent('.stars b'));out.push('звёзд после обхода (ответы «1»): '+stars);
// сценарий лавки
await p.evaluate(()=>{localStorage.setItem('misha:stars','40');});await p.reload();await p.waitForTimeout(300);
await p.click('.skip');const TT=await p.$$eval('.jump .jr span',x=>x.map(e=>e.textContent));await p.click(`.jump .jr:nth-child(${TT.indexOf('Раскраски')+1}) button:nth-of-type(2)`);await p.waitForTimeout(150);
const w0=+(await p.textContent('.stars b'));
await p.click('.shopbtn');const c=p.locator('.card',{hasText:'Осенний лес'});await c.click();await c.click();await p.waitForTimeout(300);
const onPic=!!(await p.$('.picf img'));const bx=await p.$eval('.picf img',e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]});
for(const [fx,fy] of [[.4,.3],[.6,.5],[.7,.8],[.3,.6]])await p.mouse.click(bx[0]+bx[2]*fx,bx[1]+bx[3]*fy);
const nm=(await p.$$('.marks .ring')).length;const vb=await (await p.$('.vanya')).boundingBox();await p.mouse.move(bx[0]+5,bx[1]+5);
await p.mouse.move(vb.x+20,vb.y+10);await p.mouse.down();await p.waitForTimeout(1200);await p.mouse.up();const w1=+(await p.textContent('.stars b'));
// второе нажатие не даёт звёзд повторно
await p.mouse.down();await p.waitForTimeout(1200);await p.mouse.up();const w1b=+(await p.textContent('.stars b'));
await p.click('.bot .next');await p.waitForTimeout(150);const back=(await p.textContent('.sec')).trim();const dot=await p.$$eval('.dots b',x=>x.findIndex(e=>e.classList.contains('cur')));
let ok=onPic&&nm===4&&w1===w0-6+3&&w1b===w1&&back.startsWith('Раскраски')&&dot===1;if(!ok)fails++;
out.push(`${ok?'ok  ':'FAIL'} лавка: картина открылась ${onPic}, меток ${nm}, копилка ${w0}→${w1} (−6 +3), повторно ${w1b}, «→» вернул в «${back}» пункт ${dot+1}`);
// повторное открытие купленного: без оплаты, метки сохранены
await p.click('.shopbtn');await p.locator('.card',{hasText:'Осенний лес'}).click();await p.waitForTimeout(250);const nm2=(await p.$$('.marks .ring')).length;const w2=+(await p.textContent('.stars b'));
ok=nm2===4&&w2===w1;if(!ok)fails++;out.push(`${ok?'ok  ':'FAIL'} повторное открытие: меток ${nm2}, копилка ${w2}`);
// перезагрузка
await p.reload();await p.waitForTimeout(300);const w3=+(await p.textContent('.stars b'));const sec3=(await p.textContent('.sec')).trim();
ok=w3===w2;if(!ok)fails++;out.push(`${ok?'ok  ':'FAIL'} перезагрузка: копилка ${w3}, экран «${sec3}»`);
// нехватка денег: карточка не покупается
await p.evaluate(()=>{localStorage.setItem('misha:spent',localStorage.getItem('misha:stars'));});await p.reload();await p.waitForTimeout(300);
await p.click('.shopbtn');const cc=p.locator('.card',{hasText:'Лабиринт 3'});await cc.click();await cc.click();await p.waitForTimeout(200);const stillShop=!!(await p.$('.shoppanel'));
ok=stillShop;if(!ok)fails++;out.push(`${ok?'ok  ':'FAIL'} без звёзд лабиринт не покупается: лавка открыта ${stillShop}`);
out.push('ошибки страницы: '+JSON.stringify(errs));if(errs.length)fails++;
console.log(out.join('\n'));console.log('FAILS',fails);await b.close();})();
