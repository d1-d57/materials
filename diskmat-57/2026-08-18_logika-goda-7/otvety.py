# -*- coding: utf-8 -*-
"""Ответы обоих вариантов листка 22.09, посчитанные перебором.
Вариант B — изоморфизм A: та же абстрактная форма, другие числа."""
from itertools import combinations
import calendar, datetime

def v(*a): return a
R={}
# 1а,1б: чисел от m до n = n-m+1
R['1а']=(123-17+1, 131-23+1)
R['1б']=(123+17+1, 131+23+1)
# 1в: первая страница листа нечётна, последняя чётна → чёт/нечёт невозможно
R['1в']=('нельзя: 144 чётная, 327 нечётная','нельзя: 208 чётная, 451 нечётная')
# 2: N - N//d
R['2']=(100-100//3, 150-150//4)
# 3: |масть ∪ картинки|
R['3']=(9+12-3, 13+12-3)
# 4а: пары цифр a<b / a>b
R['4а']=(sum(1 for a in range(1,10) for b in range(0,10) if a<b),
         sum(1 for a in range(1,10) for b in range(0,10) if a>b))
# 4б: сумма цифр >=10 / <=5
R['4б']=(sum(1 for a in range(1,10) for b in range(0,10) if a+b>=10),
         sum(1 for a in range(1,10) for b in range(0,10) if a+b<=5))
# 5: тройки различных натуральных в сумме S
trip=lambda S: sorted(c for c in combinations(range(1,S),3) if sum(c)==S)
R['5']=(len(trip(10)), len(trip(12)))
R['5спис']=(trip(10), trip(12))
# 7: от 1 до N есть две различные цифры = N - (из одинаковых цифр)
odno=lambda N: sum(1 for x in range(1,N+1) if len(set(str(x)))==1)
R['7']=(2019-odno(2019), 3000-odno(3000))
# 8: общий делитель с K больше 1 среди 1..N
def sdel(N,K):
    from math import gcd
    return sum(1 for x in range(1,N+1) if gcd(x,K)>1)
R['8']=(sdel(300,99), sdel(400,65))
# 9: четвёрки различных в сумме S
quad=lambda S: sorted(c for c in combinations(range(1,S),4) if sum(c)==S)
R['9']=(len(quad(15)), len(quad(16)))
R['9спис']=(quad(15), quad(16))
# 10: наборы монет
def monety(S,nom):
    if S==0: return 1
    if not nom: return 0
    return sum(monety(S-k*nom[0],nom[1:]) for k in range(S//nom[0]+1))
R['10а']=(monety(10,[10,5,2,1]), monety(15,[10,5,2,1]))
R['10б']=(monety(20,[10,5,2,1]), monety(25,[10,5,2,1]))
# 11: не потеряли -> оценка снизу
R['11а']=((30-26,30-23,30-21),(28-25,28-22,28-19))
R['11б']=(30-((30-26)+(30-23)+(30-21)), 28-((28-25)+(28-22)+(28-19)))
# 12: вхождения цифры d
vhozh=lambda N,d: sum(str(x).count(str(d)) for x in range(1,N+1))
soderzh=lambda N,d: sum(1 for x in range(1,N+1) if str(d) in str(x))
R['12а']=(vhozh(100,7), vhozh(100,3))
R['12б']=(vhozh(1000,7), vhozh(1000,3))
R['12в']=(soderzh(1000,7), soderzh(1000,3))
# 13: все, кто принёс A, принёс и B. |A|=N-zabylA, |B|=N-zabylB
R['13']=((12-9,12-2,(12-2)-(12-9)), (15-11,15-3,(15-3)-(15-11)))
# 14: x+2y+5z=S
resh=lambda S: sum(1 for z in range(S//5+1) for y in range((S-5*z)//2+1))
R['14']=(resh(37), resh(43))
# 15: у третьего вычеркнуто W слов, вычеркнуть могли только (K-o1)+(K-o2)
R['15']=((10-2, (10-8)+(10-7)), (12-3, (12-9)+(12-8)))
# 16: сумма n целых = S; сколько нечётных k (k = S mod 2, шаг 2, k<=n)
R['16']=([k for k in range(0,6) if k%2==2026%2], [k for k in range(0,8) if k%2==2027%2])
# 17: пары с нечётной суммой из 1..N
par=lambda N: (N//2)*((N+1)//2)
R['17']=(par(31), par(41))
# 18: перемен на 1 меньше уроков в КАЖДЫЙ учебный день
def uchdni(year,month,vyh):
    return sum(1 for d in range(1,calendar.monthrange(year,month)[1]+1)
               if datetime.date(year,month,d).weekday()!=vyh)
# A: апрель, 1 апреля среда, кроме воскресений. Подберём год.
def god_s_dnem(month, target_wd):
    for y in range(2001,2100):
        if datetime.date(y,month,1).weekday()==target_wd: return y
yA=god_s_dnem(4,2); yB=god_s_dnem(3,0)
dA=uchdni(yA,4,6); dB=uchdni(yB,3,6)
R['18а']=(dA,dB)
R['18б']=(100-dA, 120-dB)
# 19а: трёхзначные с суммой цифр = S
R['19а']=(sum(1 for x in range(100,1000) if sum(map(int,str(x)))==4),
          sum(1 for x in range(100,1000) if sum(map(int,str(x)))==5))
# 19б: четырёхзначные с суммой цифр > S
R['19б']=(sum(1 for x in range(1000,10000) if sum(map(int,str(x)))>33),
          sum(1 for x in range(1000,10000) if sum(map(int,str(x)))>32))
for k in sorted(R, key=lambda s:(int(''.join(c for c in s if c.isdigit())), s)):
    a,b = R[k]
    print('%-7s A: %-28s B: %s' % (k, str(a)[:28], str(b)[:60]))
