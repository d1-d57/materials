import os, sys
sys.path.insert(0, "/Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools")
import korni
print("ИМЯ_РЕПО", korni.ИМЯ_РЕПО)
print("КОРНИ_ПО_УМОЛЧАНИЮ", korni.КОРНИ_ПО_УМОЛЧАНИЮ)
print("roots", [к.имя for к in korni.КОРНИ])
print("ПРИЧИНА", repr(korni.ПРИЧИНА_ПО_УМОЛЧАНИЮ)[:60])
for p in ("_studio/docs/x.md", "kurs-puti-i-volny/ZAMYSEL.md", "obzory/a/b.md", "_illustracii/x.md", "teorkat-vvedenie/a.md", "diskmat-57/x.md", "README.md"):
    try:
        k = korni.корень_пути(p)
    except Exception as e:
        k = "ERR %s" % e
    print("корень_пути", p, "->", k)
