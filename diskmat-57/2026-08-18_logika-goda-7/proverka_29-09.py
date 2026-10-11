from itertools import combinations, product
# К1 книга: первая стр (чётная) f, последняя (нечётная) l -> листы (l+1 - (f-1) + 1)/2
def kniga(f,l): assert f%2==0 and l%2==1; return (f-1, l+1, (l+1-(f-1)+1)//2)
print('К1 А 88..213', kniga(88,213)); print('К1 Б 96..231', kniga(96,231))
def nediv(N,a,b):
    A=sum(1 for x in range(1,N+1) if x%a==0); B=sum(1 for x in range(1,N+1) if x%b==0)
    AB=sum(1 for x in range(1,N+1) if x%a==0 and x%b==0); none=sum(1 for x in range(1,N+1) if x%a and x%b)
    assert none==N-A-B+AB; return A,B,AB,none
print('К2 А 500,7,11',nediv(500,7,11)); print('К2 Б 600,7,13',nediv(600,7,13))
def kv(m,n):  # квадраты любого размера
    return [ (m-k+1)*(n-k+1) for k in range(1,min(m,n)+1)]
def dom(m,n): return m*(n-1), (m-1)*n
for m,n in ((3,5),(3,6),(4,5)): print('К3',m,n,'квадраты',kv(m,n),sum(kv(m,n)),'доминошки гор/верт',dom(m,n),sum(dom(m,n)))
def tri(L):
    res=[(a,b,c) for a,b,c in combinations(L,3) if a+b>c]
    by={}
    for a,b,c in res: by[c]=by.get(c,0)+1
    return len(res),by
print('К4 1..7',tri(range(1,8))); print('К4 2..8',tri(range(2,9))); print('К4 1..8',tri(range(1,9)))
# листок
print('отрезки 5,10:',len(list(combinations(range(5),2))),len(list(combinations(range(10),2))),'28->',[n for n in range(2,20) if n*(n-1)//2==28])
print('цветы 16м14д: девочкам',16*14,'учительнице',16*14+16)
pr=[2,3,5,7]; print('1.3:',sorted({a*b for a in pr for b in pr}))
print('10x10 выше диагонали',sum(1 for i in range(10) for j in range(10) if j>i),'с диагональю',sum(1 for i in range(10) for j in range(10) if j>=i))
def spichki(m,n): return m*(n+1)+n*(m+1)
print('спички 8x8',spichki(8,8),'3x5',spichki(3,5))
print('Буратино 1.4а',sum(1 for a in '13579' for b in '13579' if a!=b))
print('дороги 12 городов',len(list(combinations(range(12),2))))
print('Д5 рейсы',11+7*13)
print('1.10',sum(1 for x in range(100,1000) if (x//100)%2!=(x//10%10)%2 and sum(map(int,str(x)))%10==0))
print('Д1 глобус',(17+1)*24)
print('Д9/Д14 пары 1..31 нечёт/чёт',sum(1 for a,b in combinations(range(1,32),2) if (a+b)%2),sum(1 for a,b in combinations(range(1,32),2) if (a+b)%2==0))
def coins(S,c=(1,2,5,10)):
    cnt=0
    for d in range(S//10+1):
        for f in range((S-10*d)//5+1):
            r=S-10*d-5*f; cnt+=r//2+1
    return cnt
print('монеты 10,20',coins(10),coins(20))
print('семёрки 1..200,1..2000, чисел с 7 до 2000',sum(str(x).count('7') for x in range(1,201)),sum(str(x).count('7') for x in range(1,2001)),sum(1 for x in range(1,2001) if '7' in str(x)))
def eq(S): return sum(1 for z in range(S//5+1) for y in range((S-5*z)//2+1))
print('x+2y+5z 17,37',eq(17),eq(37))
print('Д3 Кругляндия',20*17)
print('Д6 каюты',13*16+16*17+17*24+24*13)
print('2.7 10-значные из 1,2 сумма 12',sum(1 for t in product((1,2),repeat=10) if sum(t)==12))
print('Д12 матчи 12 команд',12*11//2,'очки',12*11)
print('Д2 сумма цифр простое',sum(1 for x in range(10,100) if (lambda s: s>1 and all(s%d for d in range(2,s)))(x//10+x%10)))
print('Д18 подряд из 1..20 (>=2)',sum(1 for a in range(1,21) for b in range(a+1,21)))
print('==== Б')
print('отрезки 6,11:',15,55,'36->',[n for n in range(2,20) if n*(n-1)//2==36])
print('цветы 15м13д',15*13,15*13+15)
print('цифры >3 с повт / без',sum(1 for a in range(4,10) for b in range(4,10)),sum(1 for a in range(4,10) for b in range(4,10) if a!=b))
print('нечёт с повт',25)
print('спички 7x7',spichki(7,7),'4x5',spichki(4,5))
print('дороги 13',13*12//2); print('Д5 Б',9+6*14)
print('1.10 Б одна чётность',sum(1 for x in range(100,1000) if (x//100)%2==(x//10%10)%2 and sum(map(int,str(x)))%10==0))
print('глобус Б 14/30',15*30)
print('Кругляндия 18',18*15)
print('9-значные из 1,2 сумма 11',sum(1 for t in product((1,2),repeat=9) if sum(t)==11))
print('хоккей 14',14*13//2,14*13)
print('каюты Б 11,14,19,22', 11*14+14*19+19*22+22*11)
print('монеты 15,25',coins(15),coins(25)); print('пары 1..41',sum(1 for a,b in combinations(range(1,42),2) if (a+b)%2),sum(1 for a,b in combinations(range(1,42),2) if (a+b)%2==0))
print('четвёрки 1..300/3000/чисел',sum(str(x).count('4') for x in range(1,301)),sum(str(x).count('4') for x in range(1,3001)),sum(1 for x in range(1,3001) if '4' in str(x)))
print('ур 23 43',eq(23),eq(43))
print('трёхзн сумма 4, 5',sum(1 for x in range(100,1000) if sum(map(int,str(x)))==4),sum(1 for x in range(100,1000) if sum(map(int,str(x)))==5),'четырёхзн >33, >32',sum(1 for x in range(1000,10000) if sum(map(int,str(x)))>33),sum(1 for x in range(1000,10000) if sum(map(int,str(x)))>32))
print('К4 Б самая длинная 6 в 1..7:',tri(range(1,8))[1][6])
