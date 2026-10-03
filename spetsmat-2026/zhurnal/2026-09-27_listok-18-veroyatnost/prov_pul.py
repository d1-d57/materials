# Проверка перебором кандидатов в пул задач 18ℵ (01.10.2026)
from itertools import product, combinations, permutations
from math import comb, sqrt
from fractions import Fraction as F
ok=True
def chk(n,c):
    global ok
    if not c: ok=False; print("FAIL",n)
Cat=lambda n: comb(2*n,n)//(n+1)
def ps(s):
    S=[0]
    for x in s: S.append(S[-1]+x)
    return S
# A. кассир без сдачи: n с 50 р., n со 100 р., очередь случайна; никто не ждёт сдачи
for n in range(1,8):
    good=sum(1 for c in combinations(range(2*n),n) if min(ps([1 if i in c else -1 for i in range(2*n)]))>=0)
    chk("A кассир n=%d"%n, F(good,comb(2*n,n))==F(1,n+1))
# A'. кассир с k купюрами по 50 в кассе заранее? (вариант) — пропускаем
# B. правильные скобочные последовательности
def br(n):
    r=0
    for s in product("()",repeat=2*n):
        h=0;okk=True
        for c in s:
            h+=1 if c=="(" else -1
            if h<0: okk=False;break
        r+= okk and h==0
    return r
chk("B скобки", [br(n) for n in range(1,7)]==[Cat(n) for n in range(1,7)])
# C. рукопожатия: 2n человек за круглым столом, пары без пересечений
def hs(pts):
    if not pts: return 1
    a=pts[0]; t=0
    for j in range(1,len(pts),2): t+=hs(pts[1:j])*hs(pts[j+1:])
    return t
chk("C рукопожатия", [hs(list(range(2*n))) for n in range(1,9)]==[Cat(n) for n in range(1,9)])
# F. чётность C_n: зеркально-симметричных деревьев в D_n — C_{(n-1)/2} при нечётном n, 0 при чётном n>=2
def trees(n):
    if n==0: return [None]
    return [(l,r) for i in range(n) for l in trees(i) for r in trees(n-1-i)]
mir=lambda t: None if t is None else (mir(t[1]),mir(t[0]))
for n in range(0,9):
    sym=sum(1 for t in trees(n) if mir(t)==t)
    chk("F sym n=%d"%n, sym==(Cat((n-1)//2) if n%2==1 else (1 if n==0 else 0)))
odd=[n for n in range(1,70) if Cat(n)%2==1]
chk("F нечётные", odd==[1,3,7,15,31,63])
# E. Нараяна: путей Дика в (2n,0) с k пиками; симметрия k <-> n+1-k
for n in range(1,8):
    N=[0]*(n+2)
    for s in product((1,-1),repeat=2*n):
        S=ps(s)
        if S[-1]==0 and min(S)>=0:
            k=sum(1 for i in range(2*n-1) if s[i]==1 and s[i+1]==-1); N[k]+=1
    chk("E Нараяна n=%d"%n, all(N[k]==N[n+1-k] for k in range(1,n+1)) and all(N[k]==comb(n,k)*comb(n,k-1)//n for k in range(1,n+1)))
# D. отношение
chk("D", all(Cat(n+1)*(n+2)==Cat(n)*(4*n+2) for n in range(30)))
# G. производящая функция: (1-2x C(x))^2 = 1-4x как ряды
M=20; C=[Cat(n) for n in range(M)]
S=[1]+[-2*C[k-1] for k in range(1,M)]          # 1 - 2x C(x)
sq=[sum(S[i]*S[k-i] for i in range(k+1)) for k in range(M)]
chk("G", sq==[1,-4]+[0]*(M-2))
# H. сумма C(2k,k)C(2n-2k,n-k) = 4^n
chk("H", all(sum(comb(2*k,k)*comb(2*n-2*k,n-k) for k in range(n+1))==4**n for n in range(40)))
# I. оценки u_k: 1/(2√k) <= u_k <= 1/√(2k+1)
u=lambda n: F(comb(2*n,n),4**n)
chk("I низ", all(u(k)**2>=F(1,4*k) for k in range(1,300)))
chk("I верх", all(u(k)**2<=F(1,2*k+1) for k in range(300)))
# I'. 100 бросков: «последний раз поровну в момент 0» более чем в 3 раза вероятнее, чем «в момент 50»
chk("I' >3 (оценка)", F(1,4*50)*51*51>9)   # u_50 >= 1/(2√50), u_25^2 <= 1/51  =>  ratio >= 51/(2√50) > 3  <=> 51^2/(4*50) > 9
r=u(50)/(u(25)**2); print("I' точное отношение", float(r))
chk("I' >3 точно", r>3)
# J. первое возвращение: сумма 2C_{n-1}/4^n по n<=N = 1 - u_N
chk("J", all(sum(F(2*Cat(n-1),4**n) for n in range(1,N+1))==1-u(N) for N in range(1,40)))
print("ALL OK" if ok else "SOME FAIL")
