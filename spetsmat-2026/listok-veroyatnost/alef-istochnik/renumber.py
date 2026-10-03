"""Перенумерация задач в telo.tex по порядку появления; новые задачи пишутся с номером 0.
Ссылки «задачу N», «задаче N», «задачи N» исправляются по таблице старый → новый. Печатает таблицу."""
import re, sys
p = sys.argv[1] if len(sys.argv) > 1 else "telo.tex"
s = open(p, encoding="utf-8").read()
pat = re.compile(r"\\(zad|zadp|nomer)\{(\d+)\}")
mapa, k = {}, 0
def zam(m):
    global k
    k += 1
    if m.group(2) != "0":
        mapa[m.group(2)] = str(k)
    return "\\%s{%d}" % (m.group(1), k)
s = pat.sub(zam, s)
s = re.sub(r"(задач[аеиу]\s+)(\d+)", lambda m: m.group(1) + mapa.get(m.group(2), m.group(2)), s)
open(p, "w", encoding="utf-8").write(s)
print(" ".join("%s→%s" % (a, b) for a, b in mapa.items() if a != b) or "без изменений")
