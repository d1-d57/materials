from itertools import combinations, permutations
L4="АБВГ"; L5="АБВГД"
def nf(t): return "".join(sorted(t, key=lambda c:"АБВГД".index(c)))
def succ(s, alph):
    # ball rule: raise last letter if possible; else raise previous and put the rest right after it
    k=len(s); n=len(alph); idx=[alph.index(c) for c in s]
    for i in range(k-1,-1,-1):
        if idx[i] < n-(k-i):
            idx[i]+=1
            for j in range(i+1,k): idx[j]=idx[j-1]+1
            return "".join(alph[x] for x in idx)
    return None
def chain(first, alph):
    out=[first]
    while True:
        s=succ(out[-1],alph)
        if s is None: return out
        out.append(s)
def ok(name,cond): print(("OK " if cond else "FAIL ")+name)

# S1 pairs from 4
p4=["".join(c) for c in combinations(L4,2)]
ok(f"S1 pairs4 = {p4} ({len(p4)})", len(p4)==6 and chain("АБ",L4)==p4)
ordered4=["".join(c) for c in permutations(L4,2)]
ok(f"S1 ordered/каждый-с-каждым = {len(ordered4)}", len(ordered4)==12)
alpha_noNF=sorted(ordered4,key=lambda s:[L4.index(c) for c in s])
seen=set(); firstdup=None
for i,s in enumerate(alpha_noNF):
    if nf(s) in seen: firstdup=(i+1,s); break
    seen.add(nf(s))
ok(f"S1 'по алфавиту без НФ': {alpha_noNF}; первый повтор на месте {firstdup}", firstdup==(4,"БА"))
cyc4={nf(L4[i]+L4[(i+1)%4]) for i in range(4)}
ok(f"S1 'по кругу' = {sorted(cyc4)} ({len(cyc4)}), пропущены {sorted(set(p4)-cyc4)}", len(cyc4)==4 and set(p4)-cyc4=={"АВ","БГ"})
disj=[("АБ","ВГ")]; ok("S1 прогноз '2' (разбить на пары) — 2 из 6", True)

# S2 pairs from 5
p5=["".join(c) for c in combinations(L5,2)]
groups=[sum(1 for s in p5 if s[0]==c) for c in L5]
ok(f"S2 pairs5 = {p5} ({len(p5)}), группы {groups}", len(p5)==10 and groups==[4,3,2,1,0] and chain("АБ",L5)==p5)
ok(f"S2 ordered = {len(list(permutations(L5,2)))}", len(list(permutations(L5,2)))==20)
cyc5={nf(L5[i]+L5[(i+1)%5]) for i in range(5)}
ok(f"S2 'по кругу' = {sorted(cyc5)} ({len(cyc5)}), пропущены {sorted(set(p5)-cyc5)}", len(cyc5)==5)

# S3 triples from 5
t5=["".join(c) for c in combinations(L5,3)]
tg=[sum(1 for s in t5 if s[0]==c) for c in L5]
ok(f"S3 triples5 = {t5} ({len(t5)}), группы по первой {tg}", len(t5)==10 and tg==[6,3,1,0,0] and chain("АБВ",L5)==t5)
Agroup=[s[1:] for s in t5 if s[0]=="А"]
ok(f"S3 тройки с А без А = {Agroup} == пары из БВГД", Agroup==["".join(c) for c in combinations("БВГД",2)])
ok(f"S3 ordered = {len(list(permutations(L5,3)))}", len(list(permutations(L5,3)))==60)
ordered_t=sorted(["".join(p) for p in permutations(L5,3)],key=lambda s:[L5.index(c) for c in s])
seen=set(); fd=None
for i,s in enumerate(ordered_t):
    if nf(s) in seen: fd=(i+1,s); break
    seen.add(nf(s))
ok(f"S3 'по алфавиту без НФ' первые 4: {ordered_t[:4]}; первый повтор {fd}", fd==(4,"АВБ"))
cyct={nf(L5[i]+L5[(i+1)%5]+L5[(i+2)%5]) for i in range(5)}
ok(f"S3 'по кругу' = {sorted(cyct,key=t5.index)} ({len(cyct)}), пропущены {sorted(set(t5)-cyct,key=t5.index)}", len(cyct)==5)
comp={s:nf(set(L5)-set(s)) for s in t5}
ok(f"S3 дополнение тройка->пара биекция: {len(set(comp.values()))} разных пар", set(comp.values())==set(p5))
ok(f"ставка: C(5,2)={len(p5)} == C(5,3)={len(t5)}", len(p5)==len(t5))
# ball traps
ok(f"мяч S2: после АД -> {succ('АД',L5)}, после ГД -> {succ('ГД',L5)}", succ('АД',L5)=="БВ" and succ('ГД',L5) is None)
ok(f"мяч S3: после АБД -> {succ('АБД',L5)}, после АГД -> {succ('АГД',L5)}, после БГД -> {succ('БГД',L5)}, после ВГД -> {succ('ВГД',L5)}",
   succ('АГД',L5)=="БВГ" and succ('ВГД',L5) is None)

# S5 sticks, largest 6
tri=[(6,b,c) for b in range(5,0,-1) for c in range(b-1,0,-1) if b+c>6]
deg=[(6,b,c) for b in range(5,0,-1) for c in range(b-1,0,-1) if b+c==6]
all6=[(6,b,c) for b in range(5,0,-1) for c in range(b-1,0,-1)]
# brute check from definition
brute=[t for t in combinations(range(1,7),3) if max(t)==6 and sorted(t)[0]+sorted(t)[1]>6]
ok(f"S5 палочки, наибольшая 6: {tri} ({len(tri)}); вырожденные {deg}; всех троек с 6: {len(all6)}", len(tri)==4==len(brute) and len(all6)==10)
ok(f"S5 лесенка по средней: 5->{[c for (_,b,c) in tri if b==5]}, 4->{[c for (_,b,c) in tri if b==4]}", True)
# 'pairs from 1..5 with sum>6' == S5
pairs_sum=[p for p in combinations(range(1,6),2) if sum(p)>6]
ok(f"S5 = пары из 1..5 с суммой >6: {pairs_sum}", len(pairs_sum)==4)
# backup: sticks largest 5 -> answer
t5s=[t for t in combinations(range(1,6),3) if max(t)==5 and sorted(t)[0]+sorted(t)[1]>5]
ok(f"запас: палочки 1..5, наибольшая 5: {t5s} ({len(t5s)})", len(t5s)==2)
