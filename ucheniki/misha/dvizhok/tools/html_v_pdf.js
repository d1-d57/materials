const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
const p=await b.newPage();
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(600);
await p.emulateMedia({media:'print'});await p.pdf({path:process.argv[3],format:'A4',preferCSSPageSize:true});await b.close();})();
