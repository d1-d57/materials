from functools import lru_cache
def count(cells):
    cells=frozenset(cells)
    @lru_cache(None)
    def f(s):
        if not s: return 1
        c=min(s); r=0
        for d in ((0,1),(1,0)):
            n=(c[0]+d[0],c[1]+d[1])
            if n in s: r+=f(s-{c,n})
        return r
    return f(cells)
def show(cells):
    R=max(r for r,c in cells)+1; Cc=max(c for r,c in cells)+1
    return "\n".join("".join('#' if (r,c) in cells else '.' for c in range(Cc)) for r in range(R))
# вариант: коридор-кольцо ширины 1 с четырьмя «ушами» 2x2 на углах
def shape(L):
    s=set()
    # квадраты 2x2 в углах, соединённые коридорами ширины 1 длины L
    n=L+4
    for (r0,c0) in ((0,0),(0,n-2),(n-2,0),(n-2,n-2)):
        for a in range(2):
            for b in range(2): s.add((r0+a,c0+b))
    for c in range(2,n-2): s.add((0,c)); s.add((n-1,c))
    for r in range(2,n-2): s.add((r,0)); s.add((r,n-1))
    return s
for L in range(1,6):
    s=shape(L); print(L,len(s),count(s))
s=shape(2); print(show(s))
