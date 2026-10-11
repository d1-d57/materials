# Проверка «ложных правил Васи»: правило исполняется буквально, правильный ответ — перебором.
from itertools import product, permutations, combinations
def ds(n): return sum(map(int,str(n)))
def coin_parts(total, coins):
    res=[]
    def rec(rest, maxi, cur):
        if rest==0: res.append(tuple(cur)); return
        for c in coins:
            if c<=maxi and c<=rest: rec(rest-c, c, cur+[c])
    rec(total, max(coins), []); return res
OK=0
def report(name, vasya, truth, extra=""):
    global OK; OK+=1
    print(f"[{name}] Вася: {vasya} | верно: {truth} {extra}")

# R1 монеты: «разменяй одну самую крупную не-рублёвую монету: 5->2+2+1, 2->1+1»
for variant in ("крупную","мелкую"):
    cur=(5,5); seen=[cur]
    while any(c>1 for c in cur):
        big=[c for c in cur if c>1]; c=max(big) if variant=="крупную" else min(big)
        l=list(cur); l.remove(c); l+= [2,2,1] if c==5 else [1,1]
        cur=tuple(sorted(l,reverse=True)); seen.append(cur)
    allp=coin_parts(10,[5,2,1])
    miss=[p for p in allp if p not in seen]
    report(f"R1 размен ({variant})", len(seen), len(allp), f"пропущены {miss}")
# R1' разбиения: «уменьши наибольшее на 1, допиши 1»
cur=(7,); seen=[cur]
while cur[0]>1:
    l=list(cur); l[0]-=1; l.append(1); cur=tuple(sorted(l,reverse=True)); seen.append(cur)
allp=coin_parts(7,list(range(7,0,-1)))
report("R1' разбиения 7", len(seen), len(allp), f"первые пропуски {[p for p in allp if p not in seen][:4]}")

# R2 сумма цифр s>=10: «первая цифра от s-9 до 9, значит 9-(s-9)=18-s»
for s in (10,11,13,15,17,18):
    truth=[n for n in range(10,100) if ds(n)==s]
    report(f"R2 s={s}", 18-s, len(truth), str(truth))

# R3 монеты по числу пятёрок, «двоек от 0 до m — это m способов»
for T in (10,15,20):
    v=sum((T-5*k)//2 for k in range(T//5+1))
    report(f"R3 T={T}", v, len(coin_parts(T,[5,2,1])))

# R4 палочки 1..L, самая длинная L: «a от L-b до b-1» (Вася) vs a+b>L
for L in (7,9):
    vas=[(a,b,L) for b in range(1,L) for a in range(L-b,b) if a>=1]
    tru=[(a,b,L) for a,b in combinations(range(1,L),2) if a+b>L]
    report(f"R4 L={L}", len(vas), len(tru), f"лишние(вырожд.) {[t for t in vas if t[0]+t[1]==L]}")

# R5 «есть хотя бы одна цифра 5/7»: сумма по разрядам
v2=10+9; t2=sum(1 for n in range(10,100) if '7' in str(n))
report("R5 двузначные с 7", v2, t2)
v3=100+90+90; t3=sum(1 for n in range(100,1000) if '5' in str(n))
report("R5 трёхзначные с 5", v3, t3)

# R6 «прибавляй 9, пока сумма цифр не испортится»
def plus9(start,s):
    out=[start]; n=start
    while ds(n+9)==s and n+9<1000: n+=9; out.append(n)
    return out
v=plus9(29,11); t=[n for n in range(10,100) if ds(n)==11]
report("R6 двузначн. сумма 11 (работает!)", len(v), len(t), str(v))
v=plus9(103,4); t=[n for n in range(100,1000) if ds(n)==4]
report("R6 трёхзн. сумма 4", len(v), len(t), f"Вася {v}; пропущено {[x for x in t if x not in v]}")
v=plus9(104,5); t=[n for n in range(100,1000) if ds(n)==5]
report("R6 трёхзн. сумма 5", len(v), len(t), f"Вася {v}")

# R7 перестановки: сдвиг по кругу; вернулись к началу круга — меняем две последние буквы; повтор — стоп
def shiftswap(word):
    seen=[word]; start=word; cur=word
    while True:
        nxt=cur[1:]+cur[0]
        if nxt==start:
            nxt=cur[:-2]+cur[-1]+cur[-2]; start=nxt
        if nxt in seen: break
        seen.append(nxt); cur=nxt
    return seen
for w in ("АБВ","АБВГ"):
    s=shiftswap(w); allw=[''.join(p) for p in permutations(w)]
    report(f"R7 {w}", len(s), len(allw), f"Вася: {s}; без него на А: {[x for x in allw if x not in s and x[0]=='А']}")

# R8 карандаш из 4 колец К/С, переворачивать можно. Вася: «поворачиваю красным влево: 2^3=8»
words=[''.join(p) for p in product('КС',repeat=4)]
classes={min(w,w[::-1]) for w in words}
vas=[w for w in words if w[0]=='К']
dbl=[(w,w[::-1]) for w in vas if w[::-1] in vas and w<w[::-1]]
missed=sorted({min(w,w[::-1]) for w in words if w[0]=='С' and w[-1]=='С'})
report("R8 карандаш 4 кольца", len(vas), len(classes), f"дважды: {dbl}; не посчитаны: {missed}")
for n in (3,5):
    ws=[''.join(p) for p in product('КС',repeat=n)]
    report(f"R8 карандаш {n} колец", 2**(n-1), len({min(w,w[::-1]) for w in ws}))

# R9 торт из n кусков по кругу, вишня/нет, повороты одинаковы. Вася: 2^n / n
for n in (3,4,6):
    ws=[''.join(p) for p in product('01',repeat=n)]
    cl={min(w[i:]+w[:i] for i in range(n)) for w in ws}
    small=[c for c in cl if len({c[i:]+c[:i] for i in range(n)})<n]
    report(f"R9 торт {n}", f"{2**n}/{n}={2**n/n:.2f}", len(cl), f"меньше {n} поворотов: {sorted(small)}")

# R10 «по первому орлу»: О, РО, РРО...
for n in (2,3,4):
    t=sum(1 for p in product('ОР',repeat=n) if 'О' in p)
    report(f"R10 {n} бросков", n, t)

# R11 Галилей: разложения vs броски
for k,ss in ((2,(9,10)),(3,(9,10))):
    for s in ss:
        part=len({tuple(sorted(p)) for p in product(range(1,7),repeat=k) if sum(p)==s})
        ordd=sum(1 for p in product(range(1,7),repeat=k) if sum(p)==s)
        report(f"R11 {k} кубика сумма {s}", f"разложений {part}", f"бросков {ordd}")

# R12 монеты 1,2,3,5 по одной: наборы vs суммы
c=[1,2,3,5]; subs=[s for r in range(1,5) for s in combinations(c,r)]
sums={sum(s) for s in subs}
report("R12 монеты 1,2,3,5", len(subs), len(sums), f"суммы {sorted(sums)}; повторы: {[ (x,[s for s in subs if sum(s)==x]) for x in sorted(sums) if sum(1 for s in subs if sum(s)==x)>1]}")
c=[1,2,5,10]; subs=[s for r in range(1,5) for s in combinations(c,r)]
report("R12 монеты 1,2,5,10 (контроль: биекция верна)", len(subs), len({sum(s) for s in subs}))

# R13 кратные 7 трёхзначные: (последнее-первое)/7
f=min(n for n in range(100,1000) if n%7==0); l=max(n for n in range(100,1000) if n%7==0)
report("R13 трёхзн. кратные 7", (l-f)//7, sum(1 for n in range(100,1000) if n%7==0), f"первое {f}, последнее {l}")
report("R13 чётные от 20 до 50", (50-20)//2, len(range(20,51,2)))

# R14 ладьи n на nxn: Вася n^2*(n-1)^2*...
import math
for n in (3,4):
    v=math.prod(k*k for k in range(1,n+1))
    t=sum(1 for p in permutations(range(n)))
    report(f"R14 ладьи {n}x{n}", v, t, f"отношение {v//t}")
print("проверено блоков:", OK)
