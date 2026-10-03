# Сборка листка 18ℵ из telo.tex (метки @имя@) и kartinki.json (генерирует kartinki.py).
#   python3 kartinki.py && python3 sobrat.py [ПРЕАМБУЛА.tex] [ВЫХОД.tex]
# Преамбула и шапка берутся из уже собранного листка (по умолчанию ../18alef-veroyatnost.tex), тело заменяется.
import json,re,sys
K=json.load(open('kartinki.json'))
t=open('telo.tex').read()
for k,v in K.items(): t=t.replace('@%s@'%k, v.replace('\n',' '))
left=re.findall(r'@\w+@',t); assert not left,left
ish=sys.argv[1] if len(sys.argv)>1 else '../18alef-veroyatnost.tex'
vyh=sys.argv[2] if len(sys.argv)>2 else ish
doc=open(ish).read()
pre,rest=doc.split('\\begin{document}')
lines=pre.split('\n')
i=next(j for j,l in enumerate(lines) if l.startswith('%% ВЕРСИЯ'))
lines[i]='%% ВЕРСИЯ: номер и история — в SESSIYA.md арки zhurnal/2026-09-27_listok-18-veroyatnost; собрано sobrat.py из alef-istochnik/telo.tex + kartinki.py'
pre='\n'.join(lines)
if r'\newcommand{\zadp}' not in pre:
    mak=(r'%% \zadp{номер}{маркер} — задача без общего условия: номер, и на той же строке сразу первый \punkt. perevod.py понимает.'+'\n'
         r'\newif\ifvstroku'+'\n'
         r'\newcommand{\zadp}[2]{\par\noindent\nomer{#1}{#2}\hspace{\zazor}\global\vstrokutrue}'+'\n')
    old_punkt=r'\newcommand{\punkt}[3]{\par\nopagebreak\blok{\okno\hspace{\zazor}\textbf{#1)}$^{#2}$\ #3}}'
    assert old_punkt in pre
    pre=pre.replace(old_punkt, mak+r'\newcommand{\punkt}[3]{\ifvstroku\global\vstrokufalse\else\par\nopagebreak\noindent\fi\okno\hspace{\zazor}\textbf{#1)}$^{#2}$\ #3\par}')
zv_old='  \\par\\medskip}\n\\newcommand{\\zad}'
zv_new='  \\par\\nopagebreak\\medskip}\n\\newcommand{\\zad}'
if zv_old in pre: pre=pre.replace(zv_old,zv_new)   # разделитель частей не остаётся последним на странице
assert zv_new in pre
# Поле «Фамилия, имя» вверху третьей страницы (владелец, 01.10 02:13: листок из 4 страниц печатают на двух листах)
FAM=r'\AddToHook{shipout/foreground}{\ifnum\value{page}=3 \put(305,-22){\small Фамилия, имя:\ \rule{6.2cm}{0.4pt}}\fi}'
if 'Фамилия, имя' not in pre: pre=pre.rstrip('\n')+'\n%% Поле для подписи на третьей странице\n'+FAM+'\n'
shapka=rest.split('\n\n',1)[0]
shapka=shapka.replace('уч.год','уч.~год')
# Шапка по стандарту коллег (владелец, 04:03): буква уровня — в правом верхнем углу, в заголовке только номер.
STARAYA=r'\centerline{\textit{Школа № 179. Ключики 2026/2027 уч.~год}}'
if STARAYA in shapka:
    shapka=('\n'+r'\noindent\rlap{\makebox[\linewidth]{\textit{Школа № 179. Ключики 2026/2027 уч.~год}}}\hfill{\LARGE$\aleph$}\par\medskip'+'\n'
            +r'\centerline{\rule{0.62\linewidth}{0.4pt}}\par\smallskip'+'\n'
            +r'\centerline{\large\textbf{18. \textsc{Вероятность}}}\par\smallskip')
# Номер страницы внизу по центру: листок из 4 страниц печатают с двух сторон (владелец, 04:03)
NOM=r'\AddToHook{shipout/foreground}{\put(298.8,-818){\makebox[0pt]{\small\thepage}}}'
if NOM not in pre: pre=pre.rstrip('\n')+'\n%% Номер страницы внизу по центру\n'+NOM+'\n'
open(vyh,'w').write(pre+'\\begin{document}'+shapka+'\n\n'+t+'\n\\end{document}\n')
print("собрано →",vyh,"; картинок:", t.count(r'\begin{tikzpicture}'))
