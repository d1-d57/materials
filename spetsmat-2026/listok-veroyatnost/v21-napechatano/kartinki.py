# Генератор картинок листка 18ℵ v6: единый стиль (сетка, ось, путь) задан здесь один раз.
import math, json, random
from itertools import permutations
SETKA="gray!28,line width=0.3pt"; OS="gray!70,line width=0.6pt"; PUT="line width=1.3pt,line join=round,line cap=round"
MELKO=0.3   # масштаб «мелких» путей (серии картинок)
KRUPNO=0.38  # масштаб одиночных путей во всю строку
K={}
def pts(steps,x0=0,y0=0):
    p=[(x0,y0)]
    for s in steps: p.append((p[-1][0]+1,p[-1][1]+s))
    return p
def put(p,st=PUT): return r"\draw[%s] "%st+" -- ".join("(%g,%g)"%q for q in p)+";"
def setka(x0,y0,x1,y1): return r"\draw[step=1,%s] (%g,%g) grid (%g,%g);"%(SETKA,x0,y0,x1,y1)
def os_(x0,x1,y=0,strelka=True): return r"\draw[%s%s] (%g,%g) -- (%g,%g);"%(OS,",->" if strelka else "",x0,y,x1+(0.4 if strelka else 0),y)
def ramka(p,pad=1): lo=min(q[1] for q in p); hi=max(q[1] for q in p); return lo-pad,hi+pad
def odin_put(steps,sc=KRUPNO,extra=()):
    p=pts(steps); lo,hi=ramka(p)
    return "\n".join([r"\begin{tikzpicture}[scale=%g]"%sc,setka(0,lo,len(steps),hi),os_(0,len(steps)),put(p),*extra,r"\end{tikzpicture}"])
def ngon(n,cx,cy,r,rot=90): return [(cx+r*math.cos(math.radians(rot+360*i/n)),cy+r*math.sin(math.radians(rot+360*i/n))) for i in range(n)]
P=lambda q:"(%.3f,%.3f)"%q

# 1. Десять путей 5:3 — две строки по пять, единая высота рамки
allp=sorted(set(permutations([1]*5+[-1]*3))); random.seed(179); ten=random.sample(allp,10)
LO=min(min(q[1] for q in pts(s)) for s in ten)-1; HI=max(max(q[1] for q in pts(s)) for s in ten)+1
c=[r"\begin{tikzpicture}[scale=%g]"%MELKO]
for j,s in enumerate(ten):
    x0=(j%5)*10.6; y0=-(j//5)*(HI-LO+1.2)
    c+=[setka(x0,y0+LO,x0+8,y0+HI),os_(x0,x0+8,y0,False),put(pts(s,x0,y0))]
c.append(r"\end{tikzpicture}"); K["puti10"]="\n".join(c)

# 2. Треугольник Дика до k=12 во всю ширину: текст-определение в пустом верхнем левом углу,
#    стрелки ↗ ↘ видны, заполнено k<=8 (около половины точек), кружки под рукописные числа.
N=12; XS=1.4; YS=0.48; ZAP=5
T={(0,0):1}
for k in range(1,N+1):
    for h in range(k+1):
        if (k-h)%2==0: T[(k,h)]=T.get((k-1,h-1),0)+T.get((k-1,h+1),0)
c=[r"\begin{tikzpicture}[xscale=%g,yscale=%g,>=stealth]"%(XS,YS)]
for (k,h) in T:
    for d in (1,-1):
        if k<N and h+d>=0: c.append(r"\draw[->,black!55,line width=0.5pt,shorten >=8.6pt,shorten <=8.6pt] (%d,%d) -- (%d,%d);"%(k,h,k+1,h+d))
for (k,h),v in T.items():
    c.append(r"\node[circle,draw,line width=0.45pt,inner sep=0pt,minimum size=16pt,font=\footnotesize,fill=white] at (%d,%d) {%s};"%(k,h,v if k<=ZAP else ""))
# оси: горизонтальная — через нижний ряд узлов (точки (k,0) лежат на оси), вертикальная — по левому краю, вдоль текста
c.insert(1,r"\draw[%s,->] (0,0) -- (%g,0);"%(OS,N+0.6))
c.insert(2,r"\draw[%s,->] (0,0) -- (0,%g);"%(OS,N+0.9))
for kk in range(2,N+1,2): c.append(r"\node[font=\scriptsize,gray] at (%d,-0.95) {%d};"%(kk,kk))
for hh in range(2,N+1,2): c.append(r"\node[font=\scriptsize,gray,anchor=east] at (-0.12,%d) {%d};"%(hh,hh))
c.append(r"\node[font=\scriptsize,gray,anchor=north east] at (-0.05,-0.25) {0};")
# текст-определение трапецией вдоль диагонали: верхние строки широкие, нижние уже (владелец 03:52)
X0=0.35; STR=0.415; YTOP=(N+0.75)*YS
shir=[]
for i in range(9):
    yb=YTOP-(i+1)*STR-0.06
    w=min(15.0, yb/YS*XS-0.75-X0)
    shir.append(max(w,3.0))
ps=r"\parshape %d "%len(shir)+" ".join("0cm %.2fcm"%w for w in shir)
c.append(r"\node[anchor=north west,inner sep=0pt] at (%g,%g) {\parbox[t]{15cm}{%s\noindent \textit{Путь Дика}~— путь из $(0,0)$, который ни разу не опускается ниже оси.\\Пути Дика длины не больше 12~— это пути по стрелкам схемы ниже.\\\textit{Треугольником Каталана} называют схему, в каждой точке которой записано число путей Дика, ведущих в эту точку. Часть чисел уже~вписана.}};"%(X0/XS,N+0.75,ps))
c.append(r"\end{tikzpicture}"); K["treugolnik"]="\n".join(c)

# 2а. Все 14 путей Дика в (8,0), две строки по семь
from itertools import permutations as _perm
dik=sorted([s for s in set(_perm([1]*4+[-1]*4)) if min(q[1] for q in pts(s))>=0],reverse=True)
assert len(dik)==14
c=[r"\begin{tikzpicture}[scale=0.27]"]
for j,s in enumerate(dik):
    x0=(j%7)*10.4; y0=-(j//7)*5.8
    c+=[setka(x0,y0,x0+8,y0+4),os_(x0,x0+8,y0,False),put(pts(s,x0,y0))]
c.append(r"\end{tikzpicture}"); K["dik14"]="\n".join(c)

# 3. Все 5 триангуляций пятиугольника
c=[r"\begin{tikzpicture}[scale=1.1]"]
for j in range(5):
    Q=ngon(5,j*3.5,0,1.1)
    c.append(r"\draw[line width=1.1pt,line join=round] "+" -- ".join(P(q) for q in Q)+" -- cycle;")
    c.append(r"\draw[line width=0.8pt] %s -- %s %s -- %s;"%(P(Q[j]),P(Q[(j+2)%5]),P(Q[j]),P(Q[(j+3)%5])))
    for q in Q: c.append(r"\fill %s circle (1.7pt);"%P(q))
c.append(r"\end{tikzpicture}"); K["triang5"]="\n".join(c)

# 4. Все 5 двоичных деревьев с тремя развилками
def derevya(n):
    if n==0: return [None]
    out=[]
    for i in range(n):
        for L in derevya(i):
            for R in derevya(n-1-i): out.append((L,R))
    return out
def risuj(t,x,y,dx,out):
    out.append(("v",x,y,t is not None))
    if t is None: return
    for side,sub in ((-1,t[0]),(1,t[1])):
        nx,ny=x+side*dx,y-0.62
        out.append(("e",x,y,nx,ny)); risuj(sub,nx,ny,dx*0.55,out)
c=[r"\begin{tikzpicture}[scale=1.1]"]
for j,t in enumerate(derevya(3)):
    el=[]; risuj(t,j*3.5,0,0.8,el)
    for e in el:
        if e[0]=="e": c.append(r"\draw[line width=0.9pt] (%.3f,%.3f) -- (%.3f,%.3f);"%e[1:])
    for e in el:
        if e[0]=="v": c.append(r"\fill (%.3f,%.3f) circle (%s);"%(e[1],e[2],"2.3pt" if e[3] else "1.6pt"))
c.append(r"\end{tikzpicture}"); K["derevya5"]="\n".join(c)

# 5. Плохой путь из (0,0) в (2n,0): касается прямой y=-1, пересекает её, касается и сразу разворачивается
st=[1,-1,-1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,1,1,1,-1,-1]
assert sum(st)==0 and min(q[1] for q in pts(st))<0
K["plohoj"]=odin_put(st,sc=0.3,extra=[r"\draw[dashed,line width=0.9pt] (0,-1) -- (%d,-1) node[right,font=\small]{$y=-1$};"%len(st),r"\fill (0,0) circle (3.5pt);",r"\fill (%d,0) circle (3.5pt);"%len(st)])

# 6. Круг (владелец 11:43): старт — светлый кружок между точками на «северном полюсе»; дуга от старта
#    по часовой через первые три числа, у её конца — их сумма: +1-1+1 = 1
seq=[1,-1,1,1,-1,1,-1]
R_=1.15; N_=len(seq); ug=lambda i: 90-180/N_-360*i/N_
c=[r"\begin{tikzpicture}[>=stealth]",r"\draw[gray!60,line width=0.7pt] (0,0) circle (%g);"%R_]
for i,v in enumerate(seq):
    a=ug(i)
    c.append(r"\fill (%.3f,%.3f) circle (1.6pt);"%(R_*math.cos(math.radians(a)),R_*math.sin(math.radians(a))))
    c.append(r"\node[font=\normalsize] at (%.3f,%.3f) {$%s$};"%((R_+0.4)*math.cos(math.radians(a)),(R_+0.4)*math.sin(math.radians(a)),"+1" if v>0 else "-1"))
c.append(r"\draw[line width=0.8pt,fill=white] (90:%g) circle (2.6pt);"%R_)
k=ug(2)-8
c.append(r"\draw[->,line width=0.8pt] (84:0.82) arc (84:%.1f:0.82);"%k)
c.append(r"\node[font=\normalsize] at (0,0) {$1$};")
c.append(r"\end{tikzpicture}"); K["krug"]="\n".join(c)

# 7. Все 6 путей из (0,0) в (4,0); верхние звенья (выше оси) — жирные, как в задаче 17
ps=sorted(set(permutations([1,1,-1,-1])),reverse=True)
c=[r"\begin{tikzpicture}[scale=0.5]"]
for j,s_ in enumerate(ps):
    x0=j*5.3; p=pts(s_,x0,0); c+=[setka(x0,-2,x0+4,2),os_(x0,x0+4,0,False)]
    for i in range(4):
        up=max(p[i][1],p[i+1][1])>0
        c.append(r"\draw[%s] (%g,%g) -- (%g,%g);"%("line width=2.6pt,line cap=round" if up else "line width=0.9pt,gray",p[i][0],p[i][1],p[i+1][0],p[i+1][1]))
c.append(r"\end{tikzpicture}"); K["shest"]="\n".join(c)

# 8. Мост с самой нижней точкой
st=[1,-1,-1,1,-1,-1,-1,1,1,-1,1,1,1,1,-1,1,-1,-1]
p=pts(st); assert p[-1][1]==0; mn=min(q[1] for q in p); f=min(q[0] for q in p if q[1]==mn)
K["nizh"]=odin_put(st,sc=0.36,extra=[r"\fill (%d,%d) circle (4pt);"%(f,mn)])

# 9. Линия рекордов
st=[1,1,-1,-1,1,1,1,-1,-1,-1,-1,1,1,-1]
p=pts(st); M=[];m=0
for q in p: m=max(m,q[1]); M.append(m)
seg=[]
for k in range(len(p)):
    seg.append((k,M[k]))
    if k+1<len(p) and M[k+1]!=M[k]: seg.append((k+1,M[k]))
lo,hi=ramka(p)
K["rekordy"]="\n".join([r"\begin{tikzpicture}[scale=0.45]",setka(0,lo,len(st),hi),os_(0,len(st)),
  r"\draw[gray!45,line width=3.2pt,line join=round] "+" -- ".join("(%g,%g)"%q for q in seg)+";",put(p),r"\end{tikzpicture}"])

# 10. Петя и Вася
a=[1,1,-1,1,-1,1,1,-1]; b=[-1,1,1,1,-1,1,-1,1]
K["petya"]="\n".join([r"\begin{tikzpicture}[scale=0.38]",setka(0,-2,8,4),setka(11,-2,19,4),os_(0,8,0,False),os_(11,19,0,False),
  put(pts(a,0,0)),put(pts(b,11,0)),r"\node[font=\small] at (4,-2.9) {Петя};",r"\node[font=\small] at (15,-2.9) {Вася};",r"\end{tikzpicture}"])

# 11. Полоска
K["poloska"]="\n".join([r"\begin{tikzpicture}[scale=1.05]",r"\draw[line width=0.9pt] (0,0) grid (4,1);",r"\fill (0.5,0.5) circle (0.26);",r"\end{tikzpicture}"])

# 12. Путь на 40 бросков с ранним последним нулём
random.seed(7)
while True:
    s=[random.choice((1,-1)) for _ in range(40)]; p=pts(s); z=max(q[0] for q in p if q[1]==0)
    if 6<=z<=10 and max(abs(q[1]) for q in p)<=8: break
K["posl"]=odin_put(s,sc=0.34,extra=[r"\draw[line width=1.1pt] (%d,0) circle (0.6);"%z])

# 13. Верхние звенья
st=[1,1,-1,-1,-1,1,-1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,1,1,-1]
p=pts(st); lo,hi=ramka(p)
c=[r"\begin{tikzpicture}[scale=0.38]",setka(0,lo,len(st),hi),os_(0,len(st))]
for i in range(len(st)):
    up=max(p[i][1],p[i+1][1])>0
    c.append(r"\draw[%s] (%d,%d) -- (%d,%d);"%("line width=2.6pt,line cap=round" if up else "line width=0.9pt,gray",p[i][0],p[i][1],p[i+1][0],p[i+1][1]))
c.append(r"\end{tikzpicture}"); K["verh"]="\n".join(c)

# 14. Смены лидера
st=[1,-1,1,1,-1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,1,1,-1,-1,-1,-1,1,1,-1,1,1,1]
p=pts(st); ex=[]
for k in range(1,len(p)-1):
    if p[k][1]==0:
        if p[k-1][1]*p[k+1][1]<0: ex.append(r"\draw[line width=1.5pt] (%g,-0.45) -- (%g,0.45) (%g,0.45) -- (%g,-0.45);"%(k-0.45,k+0.45,k-0.45,k+0.45))
        else: ex.append(r"\draw[line width=1.1pt] (%d,0) circle (0.45);"%k)
K["smeny"]=odin_put(st,sc=0.38,extra=ex)
# 15. Тупик по образцу Кнута: путь справа налево, тупик-колодец вниз; состояние посреди процесса
#     (n=4: вагон 2 уже выехал налево, в тупике 1 и 3, справа ждёт 4)
def vagon(x,y,num,w=0.82,h=0.5):
    return r"\draw[line width=0.8pt,rounded corners=1.5pt,fill=white] (%.2f,%.2f) rectangle (%.2f,%.2f); \node[font=\small] at (%.2f,%.2f) {%d};"%(x-w/2,y,x+w/2,y+h,x,y+h/2,num)
c=[r"\begin{tikzpicture}[>=stealth,scale=0.95]",
   r"\draw[line width=2.4pt,gray!45,line cap=round] (0,0) -- (3.15,0) (4.25,0) -- (8.4,0);",
   r"\draw[line width=1.4pt,gray!60] (3.15,0) -- (3.15,-2.75) -- (4.25,-2.75) -- (4.25,0);",
   r"\fill[gray!12] (3.17,-0.02) rectangle (4.23,-2.73);",
   r"\draw[line width=1.4pt,gray!60] (3.15,0) -- (3.15,-2.75) -- (4.25,-2.75) -- (4.25,0);"]
c.append(vagon(1.9,0.05,2))
c.append(vagon(3.7,-2.68,1)); c.append(vagon(3.7,-2.1,3))
c.append(vagon(5.6,0.05,4))
c+=[r"\draw[->,line width=0.8pt] (6.4,0.95) .. controls (4.6,1.1) and (3.95,0.6) .. (3.95,-0.45);",
    r"\draw[->,line width=0.8pt] (3.45,-0.45) .. controls (3.45,0.6) and (2.9,1.1) .. (1.2,0.95);",
    r"\node[font=\small\itshape,gray] at (8.0,0.45) {вход};",
    r"\node[font=\small\itshape,gray] at (0.45,0.45) {выход};",
    r"\node[font=\small\itshape,gray] at (5.0,-2.4) {тупик};",
    r"\end{tikzpicture}"]
K["tupik"]="\n".join(c)

# 16. График плотности арксинуса y = 1/(π√(x(1−x))) на (0,1): оси, сетка в стиле листка, обрезка на y=4
import math as _m
XS_,YS_=6.2,0.72   # см на единицу по x и по y
xs=[0.0066+(0.5-0.0066)*(1-_m.cos(_m.pi*t/60))/2 for t in range(61)]  # гуще у краёв
xs=xs+[1-x for x in reversed(xs[:-1])]
pts_=["(%.4f,%.4f)"%(x*XS_,YS_/(_m.pi*_m.sqrt(x*(1-x)))) for x in xs]
c=[r"\begin{tikzpicture}[>=stealth]"]
for i in range(1,5): c.append(r"\draw[%s] (0,%g) -- (%g,%g);"%(SETKA,i*YS_,XS_,i*YS_))
for x in (0.25,0.5,0.75): c.append(r"\draw[%s] (%g,0) -- (%g,%g);"%(SETKA,x*XS_,x*XS_,4*YS_))
c.append(r"\draw[%s,->] (0,0) -- (%g,0) node[right,font=\small]{$x$};"%(OS,XS_+0.35))
c.append(r"\draw[%s,->] (0,0) -- (0,%g) node[above,font=\small]{$y$};"%(OS,4*YS_+0.35))
c.append(r"\draw[dashed,gray,line width=0.5pt] (%g,0) -- (%g,%g);"%(XS_,XS_,4*YS_))
c.append(r"\draw[line width=1.3pt,line join=round] "+" -- ".join(pts_)+";")
for x,l in ((0,"0"),(0.5,r"\frac12"),(1,"1")): c.append(r"\node[below,font=\small] at (%g,0) {$%s$};"%(x*XS_,l))
for y in (1,2,3,4): c.append(r"\node[left,font=\small] at (0,%g) {$%d$};"%(y*YS_,y))
c.append(r"\node[font=\small,fill=white,inner sep=1.5pt] at (%g,%g) {$y=\dfrac{1}{\pi\sqrt{x(1-x)}}$};"%(0.5*XS_,2.35*YS_))
c.append(r"\end{tikzpicture}"); K["arksinus"]="\n".join(c)

# 10. Триангуляция семиугольника (владелец 11:12): есть внутренний треугольник 1-3-6, «уши» и треугольник 3-5-6
#     с одной граничной стороной; основание 0-1 снизу жирное, отмеченная сторона 5-6 серая (граничная, не ухо)
Q=ngon(7,0,0,1.25,rot=270-360/14)   # Q[0],Q[1] — нижняя сторона
c=[r"\begin{tikzpicture}"]
c.append(r"\draw[line width=1.1pt,line join=round] "+" -- ".join(P(q) for q in Q)+" -- cycle;")
for i,j in ((1,3),(3,6),(6,1),(3,5)): c.append(r"\draw[line width=0.8pt] %s -- %s;"%(P(Q[i]),P(Q[j])))
c.append(r"\draw[line width=3pt,line cap=round] %s -- %s;"%(P(Q[0]),P(Q[1])))
c.append(r"\draw[line width=3pt,line cap=round,gray!55] %s -- %s;"%(P(Q[5]),P(Q[6])))
for q in Q: c.append(r"\fill %s circle (1.7pt);"%P(q))
c.append(r"\end{tikzpicture}"); K["shestiug"]="\n".join(c)

json.dump(K,open("kartinki.json","w"),ensure_ascii=False); print(len(K),"картинок")
