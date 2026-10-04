const {chromium}=require('playwright');const D=process.argv[2],U=process.argv[3],CS=process.argv[4]||'dark';
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const ctx=await b.newContext({viewport:{width:1440,height:810},colorScheme:CS});
await ctx.addInitScript(`localStorage.setItem('misha:stars','12');`);const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(U);await p.waitForTimeout(400);await p.screenshot({path:D+'/00.png'});
await p.click('.skip');const rows=await p.$$eval('.jump .jr',rs=>rs.map(r=>r.querySelectorAll('button').length));await p.click('.panel h2 button');
let n=1;for(let r=0;r<rows.length;r++)for(let k=1;k<=rows[r];k++){await p.click('.skip');await p.click(`.jump .jr:nth-child(${r+1}) button:nth-of-type(${k})`);await p.waitForTimeout(200);
 await p.screenshot({path:`${D}/${String(n++).padStart(2,'0')}-r${r+1}i${k}.png`});}
console.log('shots',n,'errs',JSON.stringify(errs));await b.close();})();
