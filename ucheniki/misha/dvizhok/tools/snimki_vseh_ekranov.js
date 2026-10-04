const {chromium}=require('playwright');const D=process.argv[2];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1440,height:810}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8766/dz-2026-09-27.html');await p.waitForTimeout(400);
await p.screenshot({path:D+'/rv/00.png'});
await p.click('.skip');const rows=await p.$$eval('.jump .jr',rs=>rs.map(r=>r.querySelectorAll('button').length));await p.click('.panel h2 button');
let n=1;for(let r=0;r<rows.length;r++)for(let k=1;k<=rows[r];k++){await p.click('.skip');await p.click(`.jump .jr:nth-child(${r+1}) button:nth-of-type(${k})`);await p.waitForTimeout(250);
 await p.screenshot({path:`${D}/rv/${String(n++).padStart(2,'0')}.png`});}
console.log('shots',n,'errs',JSON.stringify(errs));await b.close();})();
