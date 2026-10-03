# Генератор TikZ-картинок листка 18ℵ v2. Печатает словарь имя -> код; tex собирается из него.
import math, json
K={}
def path_steps(steps, x0=0, y0=0):
    pts=[(x0,y0)]
    for s in steps: pts.append((pts[-1][0]+1, pts[-1][1]+s))
    return pts
def poly(pts, style="very thick"):
    return r"\draw[%s] "%style + " -- ".join("(%g,%g)"%p for p in pts)+";"
def grid(x0,y0,x1,y1):
    return r"\draw[step=1,gray!30,very thin] (%g,%g) grid (%g,%g);"%(x0,y0,x1,y1)
def axis(x0,x1,y=0,lab=True):
    return r"\draw[->,gray!70] (%g,%g) -- (%g,%g);"%(x0,y,x1+0.5,y)

# 1. Пример исхода для a=5,b=3: А Б Б А А Б А А
st=[1,-1,-1,1,1,-1,1,1]
pts=path_steps(st)
c=[r"\begin{tikzpicture}[scale=0.33]",grid(0,-1,8,2),axis(0,8),poly(pts)]
labs="АББААБАА"
for i,ch in enumerate(labs): c.append(r"\node[font=\tiny] at (%g,-1.6) {%s};"%(i+0.5,ch))
c.append(r"\end{tikzpicture}")
K["primer"]="\n".join(c)

# 2. Треугольник Дика до k=8, числа в первых трёх столбцах
N=8
c=[r"\begin{tikzpicture}[xscale=0.62,yscale=0.42]"]
nodes=[(k,h) for k in range(N+1) for h in range(0,k+1) if (k-h)%2==0]
for (k,h) in nodes:
    for d in (1,-1):
        if k<N and h+d>=0:
            c.append(r"\draw[->,gray!60,shorten >=4pt,shorten <=4pt] (%d,%d) -- (%d,%d);"%(k,h,k+1,h+d))
known={(0,0):1,(1,1):1,(2,0):1,(2,2):1}
for (k,h) in nodes:
    if (k,h) in known: c.append(r"\node[circle,draw,inner sep=0.5pt,minimum size=9pt,font=\scriptsize,fill=white] at (%d,%d) {%d};"%(k,h,known[(k,h)]))
    else: c.append(r"\node[circle,draw,inner sep=0.5pt,minimum size=9pt,fill=white] at (%d,%d) {};"%(k,h))
c.append(r"\draw[gray!70] (-0.4,-0.6) -- (%g,-0.6);"%(N+0.4))
c.append(r"\end{tikzpicture}")
K["treugolnik"]="\n".join(c)

# 3. Двоичные деревья с 1 и 2 развилками
def tree(root, children, sc=0.45):
    pass
c=[r"\begin{tikzpicture}[scale=0.42,every node/.style={circle,fill,inner sep=1.1pt}]"]
def T(x0,edges):
    out=[]
    for (a,b) in edges: out.append(r"\draw (%g,%g) node{} -- (%g,%g) node{};"%(a[0]+x0,a[1],b[0]+x0,b[1]))
    return out
c+=T(0,[((0,0),(-0.8,-1)),((0,0),(0.8,-1))])
c+=T(3.2,[((0,0),(-0.8,-1)),((0,0),(0.8,-1)),((-0.8,-1),(-1.5,-2)),((-0.8,-1),(-0.1,-2))])
c+=T(6.6,[((0,0),(-0.8,-1)),((0,0),(0.8,-1)),((0.8,-1),(0.1,-2)),((0.8,-1),(1.5,-2))])
c.append(r"\end{tikzpicture}")
K["derevya"]="\n".join(c)

# 4. Триангуляции: 2 квадрата + пятиугольник с двойственным деревом
def ngon(n,cx,cy,r,rot=90):
    return [(cx+r*math.cos(math.radians(rot+360*i/n)),cy+r*math.sin(math.radians(rot+360*i/n))) for i in range(n)]
c=[r"\begin{tikzpicture}[scale=0.62]"]
for cx,diag in ((0,(0,2)),(2.6,(1,3))):
    P=ngon(4,cx,0,1,45)
    c.append(r"\draw[thick] "+" -- ".join("(%.3f,%.3f)"%p for p in P)+" -- cycle;")
    c.append(r"\draw (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[diag[0]],*P[diag[1]]))
P=ngon(5,6.0,0.05,1.15,90)
c.append(r"\draw[thick] "+" -- ".join("(%.3f,%.3f)"%p for p in P)+" -- cycle;")
c.append(r"\draw (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[0],*P[2]))
c.append(r"\draw (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[0],*P[3]))
# отмеченная сторона P[2]P[3] (нижняя) жирно
c.append(r"\draw[line width=2.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[2],*P[3]))
c.append(r"\end{tikzpicture}")
K["triang"]="\n".join(c)

# 5. Плохой путь в общем виде: касается y=-1, пересекает, касается несколько раз
st=[1,-1,-1,1,-1,-1,1,1,-1,1,1,1,-1,-1,-1,1,1,1]
pts=path_steps(st)
mn=min(p[1] for p in pts); mx=max(p[1] for p in pts)
c=[r"\begin{tikzpicture}[scale=0.3]",grid(0,mn-1,len(st),mx+1),axis(0,len(st)),
   r"\draw[dashed,thick] (0,-1) -- (%d,-1) node[right,font=\scriptsize]{$y=-1$};"%len(st),poly(pts),
   r"\fill (0,0) circle (4pt) (%d,%d) circle (4pt);"%pts[-1],r"\end{tikzpicture}"]
K["plohoj"]="\n".join(c)

# 6. Круг из 7 чисел: +1 x4, -1 x3
seq=[1,1,-1,1,-1,-1,1]
c=[r"\begin{tikzpicture}[scale=0.7]",r"\draw[gray!60] (0,0) circle (1.2);"]
for i,v in enumerate(seq):
    a=90-360*i/len(seq)
    c.append(r"\node[font=\small] at (%.3f,%.3f) {$%s$};"%(1.2*math.cos(math.radians(a)),1.2*math.sin(math.radians(a)),"+1" if v>0 else "-1"))
c.append(r"\draw[->,thick] (0,0.35) arc (90:20:0.35);")
c.append(r"\end{tikzpicture}")
K["krug"]="\n".join(c)

# 7. Все 6 путей из (0,0) в (4,0)
from itertools import permutations
ps=sorted(set(permutations([1,1,-1,-1])),reverse=True)
c=[r"\begin{tikzpicture}[scale=0.3]"]
for j,p in enumerate(ps):
    x0=j*5.2
    pts=path_steps(p,x0,0)
    c+= [grid(x0,-2,x0+4,2),r"\draw[gray!70] (%g,0) -- (%g,0);"%(x0,x0+4),poly(pts)]
c.append(r"\end{tikzpicture}")
K["shest"]="\n".join(c)

# 8. Шестиугольник: триангуляция с отмеченной стороной и примыкающим треугольником
P=ngon(6,0,0,1.1,90)
c=[r"\begin{tikzpicture}[scale=0.62]"]
c.append(r"\fill[gray!25] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;"%(*P[2],*P[3],*P[0]))
c.append(r"\draw[thick] "+" -- ".join("(%.3f,%.3f)"%p for p in P)+" -- cycle;")
for a,b in ((0,2),(0,3),(3,5)): c.append(r"\draw (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[a],*P[b]))
c.append(r"\draw[line width=2.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"%(*P[2],*P[3]))
c.append(r"\end{tikzpicture}")
K["vykinut"]="\n".join(c)

# 9. Путь и линия рекордов (без отражения)
st=[1,1,-1,-1,1,1,1,-1,-1,-1,-1,1,1,-1]
pts=path_steps(st)
M=[];m=0
for p in pts: m=max(m,p[1]); M.append(m)
c=[r"\begin{tikzpicture}[scale=0.32]",grid(0,-1,len(st),4),axis(0,len(st)),poly(pts)]
seg=[]
for k in range(len(pts)):
    seg.append((k,M[k]))
    if k+1<len(pts) and M[k+1]!=M[k]: seg.append((k+1,M[k]))
c.append(r"\draw[dashed,very thick,gray] "+" -- ".join("(%g,%g)"%q for q in seg)+";")
c.append(r"\end{tikzpicture}")
K["rekordy"]="\n".join(c)

# 10. Полоска из 4 клеток с фишкой
c=[r"\begin{tikzpicture}[scale=0.55]",r"\draw (0,0) grid (4,1);",r"\fill (0.5,0.5) circle (0.25);",r"\end{tikzpicture}"]
K["poloska"]="\n".join(c)

# 11. Путь на 24 шага с последним нулём
st=[1,-1,-1,1,1,1,-1,-1,-1,1,1,1,1,-1,1,1,-1,1,1,-1,-1,1,1,1]
pts=path_steps(st)
last=max(p[0] for p in pts if p[1]==0)
mn=min(p[1] for p in pts); mx=max(p[1] for p in pts)
c=[r"\begin{tikzpicture}[scale=0.28]",grid(0,mn-1,len(st),mx+1),axis(0,len(st)),poly(pts),
   r"\draw[thick] (%d,0) circle (0.6);"%last,r"\end{tikzpicture}"]
K["posl"]="\n".join(c)

# 12. Смены лидера: крестики на пересечениях, кружки на касаниях
st=[1,-1,1,1,-1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,1,1,-1,-1,-1,-1]
pts=path_steps(st)
mn=min(p[1] for p in pts); mx=max(p[1] for p in pts)
c=[r"\begin{tikzpicture}[scale=0.28]",grid(0,mn-1,len(st),mx+1),axis(0,len(st)),poly(pts)]
ch=0;to=0
for k in range(1,len(pts)-1):
    if pts[k][1]==0:
        if pts[k-1][1]*pts[k+1][1]<0:
            c.append(r"\draw[very thick] (%g,-0.5) -- (%g,0.5) (%g,0.5) -- (%g,-0.5);"%(k-0.5,k+0.5,k-0.5,k+0.5)); ch+=1
        else:
            c.append(r"\draw[thick] (%d,0) circle (0.5);"%k); to+=1
c.append(r"\end{tikzpicture}")
K["smeny"]="\n".join(c)
print("смены:",ch,"касания:",to,"последний ноль рис.11 на шаге",last)
json.dump(K,open("kartinki.json","w"),ensure_ascii=False)
