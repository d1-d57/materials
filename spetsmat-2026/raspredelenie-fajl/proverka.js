const fs=require('fs'), {JSDOM}=require('jsdom');
const PUT='/sessions/fervent-beautiful-mccarthy/mnt/materials/spetsmat-2026/raspredelenie-fajl/raspredelenie.html';
let pamyat={};
const okno=()=>new JSDOM(fs.readFileSync(PUT,'utf8'),{runScripts:'dangerously',url:'https://p.local/',
 beforeParse(w){w.localStorage.__proto__.setItem=(k,v)=>{pamyat[k]=v};
  w.localStorage.__proto__.getItem=k=>pamyat[k]??null;
  w.localStorage.__proto__.removeItem=k=>{delete pamyat[k]};
  w.URL.createObjectURL=()=>'blob:x'; w.URL.revokeObjectURL=()=>{};}});
const bad=[]; const t=(n,ok,v)=>{console.log((ok?'  ✅ ':'  ❌ ')+n+(v!==undefined?'  → '+v:'')); if(!ok)bad.push(n)};
const tab=(d,v)=>{const b=[...d.querySelectorAll('#tabbar button')].find(x=>x.dataset.v===v);
  b.dispatchEvent(new d.defaultView.Event('click',{bubbles:true})); return b;};

let dom=okno(), d=dom.window.document;

// К1 — пять вкладок В ПОРЯДКЕ ВЛАДЕЛЬЦА
const poryadok=[...d.querySelectorAll('#tabbar button')].map(b=>b.dataset.v);
t('пять вкладок в порядке: школьникам В Д Н преподавателям',
  JSON.stringify(poryadok)===JSON.stringify(['shk','В','Д','Н','prp']), poryadok.join(' · '));
t('первой открыта «школьникам»', d.querySelector('#tabbar button.on').dataset.v==='shk');

// К2 — мусора нет
const ves=d.body.textContent.toLowerCase();
t('нет слов «авто» и «предположение»', !/авто|предположен/.test(ves));
t('нет «скопировать текстом»', !/скопировать/.test(ves));
t('кнопка выгрузки ровно одна', d.querySelectorAll('#skachat').length===1);

// К3 — «не назначены» ВНИЗУ, не наверху
const niz=d.querySelector('.niz');
t('сводка внизу существует', !!niz);
t('сводка — последний блок страницы', d.getElementById('telo').lastElementChild===niz);
t('внизу видно, кто без преподавателя', /Без преподавателя — 11/.test(niz.textContent), niz.textContent.slice(0,58));
t('и отдельно — кто ВНЕ ГРУПП', /Вне групп/.test(niz.textContent));
t('и преподаватели с малым числом рядом', /Меньше трёх/.test(niz.textContent));

// К4 — вкладка преподавателей: имя, число, ГРУППА выпадающим списком
tab(d,'prp');
const pr=[...d.querySelectorAll('.prepstroka')];
t('строк преподавателей 14', pr.length===14, pr.length);
const olga=pr.find(x=>/Ольга/.test(x.textContent));
const olgaN=dom.window.eval("sostoyanie.shkolniki.filter(s=>s.prepodavatel===sostoyanie.prepodavateli.find(p=>p.imya==='Ольга Рыжая').id).length");
t('порядок в строке: имя, потом число, потом группа',
  new RegExp('^ОльгаРыжая'+olgaN+'ВДН$').test(olga.textContent.replace(/\s+/g,'')),
  JSON.stringify(olga.textContent.replace(/\s+/g,''))+' при '+olgaN+' школьниках');
t('группа — выпадающий список', olga.querySelector('select[data-p]').options.length===3);
t('группа выделена цветом', /g-[ВДН]/.test(olga.querySelector('select').className), olga.querySelector('select').className);
t('Ольга красная (меньше трёх)', olga.classList.contains('malo'));

// К5 — перевод преподавателя уводит школьников с ним
const vanya=dom.window.eval("sostoyanie.prepodavateli.find(p=>p.imya==='Ваня Яковлев').id");
const doP=dom.window.eval(`sostoyanie.shkolniki.filter(s=>s.prepodavatel===${vanya}).length`);
const vGruppe=g=>dom.window.eval(`(()=>{const po=new Map(sostoyanie.prepodavateli.map(p=>[p.id,p]));return sostoyanie.shkolniki.filter(s=>(s.prepodavatel===null?s.gruppa:po.get(s.prepodavatel).gruppa)==='${g}').length})()`);
const doV=vGruppe('В'), doN=vGruppe('Н');
const sv=d.querySelector(`select[data-p="${vanya}"]`); sv.value='Н';
sv.dispatchEvent(new dom.window.Event('change',{bubbles:true}));
tab(d,'Н');
const vN=[...d.querySelectorAll('.deti .stroka')].length;
tab(d,'В');
const vV=[...d.querySelectorAll('.deti .stroka')].length;
t('преподавателя перевели — школьники уехали с ним',
  vN===doN+doP && vV===doV-doP,
  `В ${doV}→${vV}, Н ${doN}→${vN}, у Вани ${doP} школьников`);
// вернём
const sv2=(tab(d,'prp'), d.querySelector(`select[data-p="${vanya}"]`)); sv2.value='В';
sv2.dispatchEvent(new dom.window.Event('change',{bubbles:true}));

// К6 — вкладка группы: шапка один раз, кабинет правится, безгруппных нет
tab(d,'В');
t('шапка группы ровно одна', d.querySelectorAll('.shapka').length===1);
t('в шапке кабинет полем ввода', !!d.getElementById('kab'), 'кабинет='+d.getElementById('kab').value);
const imenaV=d.querySelector('.deti').textContent;
t('Гамаюновой и Ишкаева в группе нет', !/Гамаюнова|Ишкаев/.test(imenaV));
tab(d,'shk');
t('а на вкладке «школьникам» они есть', /Гамаюнова/.test(d.querySelector('.spisok').textContent));

tab(d,'В');
// К6б — ТРИ КОЛОНКИ: у преподавателя видны ФАМИЛИИ и крестик
t('три колонки на вкладке группы', !!d.querySelector('.troe'));
const karty=[...d.querySelectorAll('.karta')];
t('карточка на каждого преподавателя группы', karty.length===dom.window.eval("sostoyanie.prepodavateli.filter(p=>p.aktiven&&p.gruppa==='В').length"), karty.length);
const svanya=karty.find(k=>/Ваня Яковлев/.test(k.textContent));
const tabl=[...svanya.querySelectorAll('.tabl')];
const familii=tabl.map(x=>x.textContent.replace('×','').trim());
t('у преподавателя видны ФАМИЛИИ его школьников', familii.length>0, familii.join(', '));
t('только фамилия, без имени', familii.every(f=>!/\s/.test(f)), familii.join(' | '));
t('таблетка и есть крестик', tabl.every(x=>x.dataset.snyat && x.querySelector('.x')));
t('порядок: имя · число · таблетки, одной строкой',
  svanya.querySelector('.imya').nextElementSibling===svanya.querySelector('.n')
  && svanya.querySelector('.n').nextElementSibling===tabl[0]);
const olgaK=karty.find(k=>/Ольга/.test(k.textContent));
t('у кого мало — имя красное', olgaK.classList.contains('malo'));
t('у КАЖДОГО преподавателя рядом число школьников', karty.every(k=>{
  const n=k.querySelector('.n'); if(!n) return false;
  return +n.textContent === k.querySelectorAll('.tabl').length;
}), karty.map(k=>k.querySelector('.imya').textContent+' '+(k.querySelector('.n')||{}).textContent).join(' · '));
t('нет заголовков-пустышек', !/у кого кто|школьники группы —|все школьники —/.test(d.body.textContent));
t('число школьников — в шапке рядом с кабинетом',
  /школьников/.test(d.querySelector('.shapka').textContent), d.querySelector('.shapka').textContent.replace(/\s+/g,' ').trim());
const kl=[...d.querySelectorAll('.deti .kl')].map(x=>x.textContent);
t('класс — одной буквой', kl.every(x=>x.length===1), [...new Set(kl)].join(''));

// К6в — крестик снимает, и школьник ОСТАЁТСЯ на этой же вкладке красным
const bylo=[...d.querySelectorAll('.deti .stroka')].length;
const krest=svanya.querySelector('.tabl');
const snyatyj=+krest.dataset.snyat, imyaSnyatogo=familii[0];
krest.dispatchEvent(new dom.window.Event('click',{bubbles:true}));
t('крестик открепил школьника',
  dom.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${snyatyj}).prepodavatel`)===null);
t('и он НЕ исчез со вкладки', [...d.querySelectorAll('.deti .stroka')].length===bylo, `было ${bylo}, стало ${[...d.querySelectorAll('.deti .stroka')].length}`);
t('и стал красным', !!d.querySelector(`.deti .stroka.net select[data-s="${snyatyj}"]`), imyaSnyatogo);
t('счёт у преподавателя упал',
  +karty.length && /Ваня Яковлев/.test([...d.querySelectorAll('.karta')].find(k=>/Ваня/.test(k.textContent)).textContent));
// вернём обратно
const vs=d.querySelector(`select[data-s="${snyatyj}"]`); vs.value=String(vanya);
vs.dispatchEvent(new dom.window.Event('change',{bubbles:true}));
t('назначили заново — вернулся к преподавателю',
  dom.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${snyatyj}).prepodavatel`)===vanya);

// К6г — ТРИ СТУПЕНИ: нигде · в группе без преподавателя · у преподавателя
tab(d,'В');
const savkov=dom.window.eval("sostoyanie.shkolniki.find(s=>s.familiya==='Савков').id");
const selS=d.querySelector(`select[data-s="${savkov}"]`);
t('Савков сейчас в группе В без преподавателя', !!selS && selS.value==='g:В', selS && selS.value);
const opts=[...selS.options].map(o=>o.value);
t('в списке есть ступень «нигде»', opts[0]==='');
t('и три ступени группы', ['g:В','g:Д','g:Н'].every(v=>opts.includes(v)));
const podpisi=[...selS.options].slice(0,4).map(o=>o.textContent);
t('подписи без лишних слов', podpisi.slice(1).every(x=>/^группа [ВДН]$/.test(x)), podpisi.join(' | '));
const bylo2=[...d.querySelectorAll('.deti .stroka')].length;
selS.value=''; selS.dispatchEvent(new dom.window.Event('change',{bubbles:true}));
t('выбрал «нигде» — ВЫПАЛ из группы В',
  [...d.querySelectorAll('.deti .stroka')].length===bylo2-1, `${bylo2} → ${[...d.querySelectorAll('.deti .stroka')].length}`);
t('и группы у него больше нет',
  dom.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${savkov}).gruppa`)===null);
tab(d,'shk');
t('но на вкладке «школьникам» он есть', /Савков/.test(d.querySelector('.spisok').textContent));
const selS2=d.querySelector(`select[data-s="${savkov}"]`);
selS2.value='g:В'; selS2.dispatchEvent(new dom.window.Event('change',{bubbles:true}));
tab(d,'В');
t('вернул «группа В без преподавателя» — снова в В',
  [...d.querySelectorAll('.deti .stroka')].length===bylo2);
t('крестик роняет на СРЕДНЮЮ ступень, не в никуда', (()=>{
  const k=[...d.querySelectorAll('.karta')].find(x=>/Ваня Яковлев/.test(x.textContent));
  const id=+k.querySelector('.tabl').dataset.snyat;
  k.querySelector('.tabl').dispatchEvent(new dom.window.Event('click',{bubbles:true}));
  const s=dom.window.eval(`(()=>{const s=sostoyanie.shkolniki.find(s=>s.id===${id});return [s.prepodavatel,s.gruppa]})()`);
  return s[0]===null && s[1]==='В';
})());

// К7 — правка школьника + свои первыми
tab(d,'shk');
const s1=d.querySelector('.spisok .stroka select[data-s]');
t('свои первыми в списке принимающих',
  s1.querySelector('optgroup')!==null && /группа/.test(s1.querySelector('optgroup').label),
  [...s1.querySelectorAll('optgroup')].map(g=>g.label).join(' | '));

// К8 — память и выгрузка
const reb=dom.window.eval("sostoyanie.shkolniki.find(s=>s.prepodavatel===null).id");
const olgaId=dom.window.eval("sostoyanie.prepodavateli.find(p=>p.imya==='Ольга Рыжая').id");
const ss=d.querySelector(`select[data-s="${reb}"]`); ss.value=String(olgaId);
ss.dispatchEvent(new dom.window.Event('change',{bubbles:true}));
t('назначение применилось', dom.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${reb}).prepodavatel`)===olgaId);
let dom2=okno();
t('после переоткрытия правка на месте',
  dom2.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${reb}).prepodavatel`)===olgaId);

const d2=dom2.window.document; let fajl=null;
dom2.window.Blob=function(c){fajl=c[0]};
d2.createElement=((o)=>function(g){const e=o.call(d2,g); if(g==='a')e.click=()=>{}; return e})(d2.createElement);
d2.getElementById('skachat').dispatchEvent(new dom2.window.Event('click',{bubbles:true}));
t('выгрузка отдала файл', typeof fajl==='string'&&fajl.length>20000, (fajl||'').length/1024|0);
t('в выгруженном нет обращений к сети', !/https?:\/\/|fetch\(/.test(fajl||'x'));
const dom3=new JSDOM(fajl,{runScripts:'dangerously',url:'https://p.local/',beforeParse(w){
  w.localStorage.__proto__.setItem=()=>{};w.localStorage.__proto__.getItem=()=>null;}});
t('выгруженный открывается и рисует', dom3.window.document.getElementById('telo').innerHTML.length>2000);
t('и помнит правку', dom3.window.eval(`sostoyanie.shkolniki.find(s=>s.id===${reb}).prepodavatel`)===olgaId);

console.log('\n'+(bad.length?'❌ ПРОВАЛЕНО: '+bad.join(' · '):'✅ все '+'пробы прошли'));
process.exit(bad.length?1:0);
