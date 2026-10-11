from itertools import combinations, permutations
L4="АБВГ"; L5="АБВГД"
def nf(s): return "".join(sorted(s, key=L5.index))
def ok(name,cond): print(("OK  " if cond else "FAIL ")+name)

# K1. Робот исполняет детские слова буквально: «сначала Аня со всеми, потом Боря со всеми, ...» на парах из 4
robot=[x+y for x in L4 for y in L4 if x!=y]
seen=set(); fd=None
for i,s in enumerate(robot):
    if nf(s) in seen and fd is None: fd=(i+1,s)
    seen.add(nf(s))
ok(f"K1 робот 'каждый со всеми' на 4: {len(robot)} записей, различных пар {len(seen)}, первый повтор {fd}",
   len(robot)==12 and len(seen)==6 and fd==(4,"БА"))
# починка «с теми, кто после него»
fixed=[x+y for i,x in enumerate(L4) for y in L4[i+1:]]
ok(f"K1 починка 'с теми, кто после': {fixed} ({len(fixed)})", fixed==["".join(c) for c in combinations(L4,2)])
# вариант «дежурный и помощник» (порядок важен) — 12, т.е. робот-список был бы верным ответом другой задачи
ok("K1' 'дежурный и помощник' из 4: 12 = список робота", len(list(permutations(L4,2)))==12 and set(robot)=={"".join(p) for p in permutations(L4,2)})

# K2. «Закрой столбик» в таблице пар из пяти = группы троек
p5=["".join(c) for c in combinations(L5,2)]
for lead in "АБВ":
    tr=[t[1:] for t in ("".join(c) for c in combinations(L5,3)) if t[0]==lead]
    rest=[p for p in p5 if L5.index(p[0])>L5.index(lead)]
    ok(f"K2 тройки с {lead} (без {lead}) = {tr} = пары из 5 после закрытия столбиков до {lead} включительно = {rest}", tr==rest)
# ошибка указателя C2: список ступени 1 (пары из АБВГ) ≠ пары из БВГД
s1=["".join(c) for c in combinations(L4,2)]
need=["".join(c) for c in combinations("БВГД",2)]
ok(f"K2' список ступени 1 {s1} содержит А в {sum('А' in p for p in s1)} записях; нужные пары {need}; совпадают буквально: {s1==need}", s1!=need)
relabel={a:b for a,b in zip("АБВГ","БВГД")}
ok("K2' совпадают только после переименования А→Б,Б→В,В→Г,Г→Д", ["".join(relabel[c] for c in p) for p in s1]==need)

# K3. «Список Пети»: 10 троек, внутренний порядок вразнобой, 1 повтор-перестановка, 1 пропуск
petya=["АБВ","ГДА","БВГ","ВАД","ДБГ","АГБ","ВГД","БАД","ГВА","БГА"]
sets=[nf(t) for t in petya]
t5=["".join(c) for c in combinations(L5,3)]
dups=sorted({s for s in sets if sets.count(s)>1})
missing=sorted(set(t5)-set(sets), key=t5.index)
pos=[i+1 for i,s in enumerate(sets) if s in dups]
ok(f"K3 список Пети: записей {len(petya)}, различных {len(set(sets))}, повтор {dups} на местах {pos} ({[petya[i-1] for i in pos]}), пропуск {missing}",
   len(petya)==10 and len(set(sets))==9 and dups==["АБГ"] and missing==["БВД"] and all(len(set(t))==3 and set(t)<=set(L5) for t in petya))
# сверка Петиного списка с упорядоченным: сколько записей уже в нормальной форме (их видно сразу)
ok(f"K3 в нормальной форме у Пети {sum(t==nf(t) for t in petya)} из 10 (остальные надо мысленно упорядочить)", True)

# K4. естественное детское правило для троек «держим первых двух, меняем третьего» даёт тот же список
odo=[]
for i,a in enumerate(L5):
    for j,b in enumerate(L5[i+1:],i+1):
        for c in L5[j+1:]: odo.append(a+b+c)
ok(f"K4 «держим двух первых — меняем третьего»: {odo} == словарный список", odo==t5)

# K5. палочки, наибольшая 6: разрез по меньшей (кто пишет по возрастанию) — тот же ответ
tri=[(a,b,6) for a in range(1,6) for b in range(a+1,6) if a+b>6]
ok(f"K5 палочки по возрастанию: {tri} ({len(tri)})", len(tri)==4)
