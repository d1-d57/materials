import sys
P='_sluzhebnoe/proverki.py'; s=open(P,encoding='utf-8').read()
a='\nimport re, os\n_t = open('
if s.count(a)!=1: sys.exit('якорь')
add='''
# v7d (10.10, В40, В42): порядок «способ → результат»
check("v7d: из троих капитан и заместитель — 6 пар ВП,ВО,ПВ,ПО,ОВ,ОП; без ролей 3",
      sorted(a+b for a,b in permutations("ВПО",2))==sorted(["ВП","ВО","ПВ","ПО","ОВ","ОП"]) and C(3,2)==3)
check("v7d: задача 13 вдоль строки 8: 1·8=8, 8·7=56, 56·6=336", 1*8==8==Ar(8,1) and 8*7==56==Ar(8,2) and 56*6==336==Ar(8,3))
check("v7d: треугольник размещений заполняется правилом утв. 11 из строки 0",
      all(Ar(n,k)==(Ar(n-1,k)+k*Ar(n-1,k-1)) for n in range(1,6) for k in range(1,n+1)) and Ar(5,5)==120)
check("v7d: слова длины n+1 = слова длины n с приписанной 0 или 1 спереди",
      all(sum(1 for _ in product((0,1),repeat=n+1))==2*sum(1 for _ in product((0,1),repeat=n)) for n in range(8)))
'''
s=s.replace(a,add+a); open(P,'w',encoding='utf-8').write(s); print('ok')
