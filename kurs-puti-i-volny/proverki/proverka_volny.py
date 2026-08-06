from math import comb, cos, sin, pi
print("=== 1. числа Каталана как ИНТЕГРАЛ ===")
def integral_catalan(n, K=200000):
    s=0.0
    for i in range(K):
        th=pi*(i+0.5)/K
        s+=(2*cos(th))**(2*n)*sin(th)**2
    return 2/pi*s*pi/K
for n in range(0,8):
    C=comb(2*n,n)//(n+1)
    print(f"   n={n}: (2/pi)∫(2cosθ)^{2*n} sin²θ dθ = {integral_catalan(n):12.5f}   C_{n} = {C}")

print()
print("=== 2. вес sin²θ — это и есть принцип отражения ===")
print("   sin²θ = (2 - e^{2iθ} - e^{-2iθ})/4, а ∫e^{2ijθ}dθ = 0 при j≠0")
print("   => выживают три слагаемых бинома и остаётся:")
for n in range(1,8):
    print(f"   n={n}: C({2*n},{n}) - C({2*n},{n+1}) = {comb(2*n,n)-comb(2*n,n+1)},   C_{n} = {comb(2*n,n)//(n+1)}")

print()
print("=== 3. коридор высоты m=3: спектральная формула = формула Бине ===")
def d(m,n):
    f=[0]*(m+3); f[1]=1
    for _ in range(2*n):
        g=[0]*(m+3)
        for x in range(1,m+2):
            if f[x]:
                if x-1>=1: g[x-1]+=f[x]
                if x+1<=m+1: g[x+1]+=f[x]
        f=g
    return f[1]
F=[0,1]
for _ in range(30): F.append(F[-1]+F[-2])
for n in range(1,9):
    print(f"   n={n}: путей Дика высоты <=3 длины {2*n} = {d(3,n)},  F_{2*n-1} = {F[2*n-1]}  -> {d(3,n)==F[2*n-1]}")

print()
print("=== 4. точная спектральная формула (теорема 20) ===")
def spec(m,n):
    M=m+2
    return 2/M*sum((2*cos(k*pi/M))**(2*n)*sin(k*pi/M)**2 for k in range(1,M))
for m in (2,4,6):
    for n in (3,6,9):
        print(f"   m={m} n={n}: перебор = {d(m,n):8d}   спектр = {spec(m,n):14.5f}")

print()
print("=== 5. у каждой специализации своё уравнение ===")
print("   биномы      C(n,k)=C(n-1,k-1)+C(n-1,k)          двумерная рекуррента (Паскаль)")
print("   Фибоначчи   F=F+F                                x²=x+1, корни (1±√5)/2")
print("   коридор m   P_(m+1)=P_m - z P_(m-1)              t²-λt+1=0, корни e^{±iθ}, λ=2cosθ")
print("   Каталан     C=1+zC²                              квадратное уравнение на РЯД, не на числа")
print("   разбиения   p(n)=Σ(-1)^{k+1}(p(n-g_k)+p(n-h_k))  рекурсия из БЕСКОНЕЧНОГО произведения")
print("   -> одно и то же характеристическое уравнение t²-λt+1=0 даёт и золотое сечение, и косинусы:")
for m in (1,2,3,4,5,9):
    print(f"      m={m}: наибольший корень 2cos(pi/{m+2}) = {2*cos(pi/(m+2)):.6f}")
