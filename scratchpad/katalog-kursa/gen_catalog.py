import pathlib, re, sys
P = "kurs-puti-i-volny/"
ARH, ZAM, RT = P + "ARHITEKTURA.md", P + "ZAMYSEL.md", P + "SBORKA/REESTR-tekstov.md"
GEN_QUOTE = "СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ"
ZH, US, OT, PO, AR = "живой", "устарел", "отменён", "порождаемый", "архив"
# (path relative to kurs-puti-i-volny/, phrase, status, evidence file (repo-relative, or None = the row's own file), quote)
DATA = [
 ("ARHITEKTURA.md", "map of homes: where each kind of information lives and what feeds what", ZH, ZAM, "Сразу вторым — ARHITEKTURA.md: где какая информация лежит"),
 ("CHITAT.md", "checked reading list and links for the course", ZH, ARH, "что почитать | CHITAT.md"),
 ("HREBET-kursa.md", "2026-08 research digest: the year by quarters, materials per board, ending in the duality of two formulas; the quarter framing is cancelled, the rest stands", ZH, ZAM, "сама последовательность методов верна и полезна как оптика"),
 ("INDEKS.md", "generated index of the corpus built from the file headers", PO, None, "СОБРАН ГЕНЕРАТОРОМ tools/indeks.py. РУКАМИ НЕ ПРАВИТЬ"),
 ("KOSTYAK.md", "mathematical skeleton «one problem counted twice» of the pre-rebuild course", US, None, "математический скелет с излагаемыми теоремами (УСТАРЕЛ)"),
 ("OBEKT.md", "the whole course on two pages: the object, its degenerations, four views, two directions of the story", ZH, ARH, "что такое объект и во что он вырождается | OBEKT.md"),
 ("OBOZNACHENIYA.md", "single home of notation: one letter, one meaning", ZH, ARH, "буква | OBOZNACHENIYA.md"),
 ("OBRAZEC-summy-kvadratov.md", "pointer stub to the sum-of-four-squares sample kept in obrazec/src/obrazec.md", ZH, None, "Указатель — см. obrazec/src/obrazec.md"),
 ("PAZL.md", "grid «specialization × view»: what is known, where the holes are, in which order to dig", ZH, ARH, "PAZL.md, сетка «специализация × взгляд»"),
 ("PERESTROYKA.md", "record of the restructuring: goal, fork, plan (2026-09-03)", ZH, ZAM, "Разбор и предложение из семи глав — PERESTROYKA.md §5б–5в"),
 ("PLAN-goda-krupno.md", "year at a glance: one object, two generalization axes, seven blocks (draft of 2026-09-19)", ZH, None, "Собран 2026-09-19 по решениям владельца"),
 ("RASSKAZ-god.md", "year story in eight chapters about one path function, in a single readable file", ZH, None, "годовая история курса «Пути и волны» одним читаемым файлом"),
 ("RAZVEDKA-metody-i-obrazcy.md", "map of about 17 sources of the figure «count → generating function → equation → asymptotics»", ZH, RT, "В первый текст не вошла никак"),
 ("README.md", "course entry page as of 2026-08-05: goal, state, debts", US, ARH, "заморожен на 05.08, описывает курс до перестройки"),
 ("REESTR-reserchey.md", "numbered register of research moves with verdicts", ZH, ARH, "что уже делалось и зачем | REESTR-reserchey.md"),
 ("SBORKA/KALENDAR-i-sostav.md", "real class calendar against the 32-topic composition, counted by command", ZH, ARH, "счётные своды от 18.09 (расхождения, реестр текстов, календарь)"),
 ("SBORKA/KARTA-rashozhdeniy.md", "map of the places where course documents contradict each other", ZH, ARH, "Расхождения — SBORKA/KARTA-rashozhdeniy.md"),
 ("SBORKA/REESTR-tekstov.md", "this registry: what is written, in what state, whose verdict; debts; the catalogue of all files", ZH, ARH, "счётные своды от 18.09 (расхождения, реестр текстов, календарь)"),
 ("SBORKA/RESHENIE-instrumenty.md", "decision not to install IWE and what is built instead (2026-09-18)", ZH, ARH, "счётные своды от 18.09 (расхождения, реестр текстов, календарь)"),
 ("SBORKA/SLEDUYUSHCHIY-ZAHOD.md", "program and calendar for the next executor's work on the corpus", ZH, None, "Course Shape (Owner Decision 2026-09-19)"),
 ("SBORKA/ZAMER-grafa.md", "measurement of the corpus link graph, written by tools/graf.py", PO, P + "tools/graf.py", "Writes ZAMER-grafa.md and graf-rebra.tsv to the SBORKA folder"),
 ("SLOVAR.md", "single home of words: which word names which concept", ZH, ZAM, "OBOZNACHENIYA.md · SLOVAR.md"),
 ("ZAMYSEL.md", "decision home: what the course tells and why; cancelled decisions with their traces", ZH, None, "Единственный дом решений о том, ЧТО мы рассказываем и ЗАЧЕМ"),
 ("anons.md", "ready announcement text for a poster or an external audience", ZH, ARH, "формулировка замысла для внешнего читателя | anons.md"),
 ("obrazec/src/obrazec.md", "source of the sum-of-four-squares sample text, embedded into the output HTML", ZH, RT, "образец арки для финала"),
 ("otchety/GRANICA-chto-vidno-na-okruzhnosti.md", "report: what modular-form theory shows on the one-dimensional circle", ZH, RT, "восемь файлов (кроме забракованного"),
 ("otchety/KARTA-mosta.md", "report: what modular forms really give the walk problem, and where it is a stretch", ZH, RT, "восемь файлов (кроме забракованного"),
 ("otchety/OPTIKA-odna-funkciya.md", "report: the whole course as a study of one continued fraction (2026-08-06)", ZH, RT, "Самый поздний и сжатый ответ на «про что курс»"),
 ("otchety/OTCHET-okruzhnost.md", "report answering the brief «is it simpler on the circle», with checked / from memory / unchecked marks", ZH, RT, "восемь файлов (кроме забракованного"),
 ("otchety/RASSKAZ-dva-sposoba.md", "story «two ways to count the same thing» ending at the zeta functional equation", US, None, "рассказ двумя способами (УСТАРЕЛ)"),
 ("otchety/RAZBOR-i-perestroyka.md", "analysis of the rejected circle survey and where the entrance to modularity was found", ZH, RT, "восемь файлов (кроме забракованного"),
 ("otchety/ZAMETKI.md", "provenance notes, open places and plans for the accepted survey", ZH, RT, "восемь файлов (кроме забракованного"),
 ("otchety/ZAPISKA-iz-simmetrii.md", "note on counting on the circle from symmetry, with a verdict on sources", ZH, RT, "восемь файлов (кроме забракованного"),
 ("plan/src/chast-1-do-analiza.md", "generated view: the «before analysis» part of the year", PO, None, GEN_QUOTE),
 ("plan/src/chetvert-1.md", "generated view: quarter 1", PO, None, GEN_QUOTE),
 ("plan/src/chetvert-2.md", "generated view: quarter 2 (still «not yet written»)", PO, None, GEN_QUOTE),
 ("plan/src/chetvert-3.md", "generated view: quarter 3 (still «not yet written»)", PO, None, GEN_QUOTE),
 ("plan/src/chetvert-4.md", "generated view: quarter 4 (still «not yet written»)", PO, None, GEN_QUOTE),
 ("plan/src/god.md", "generated view: the year, one line per point", PO, None, GEN_QUOTE),
 ("plan/src/karkas.md", "32-topic skeleton, third edition; now the raw source that punkty.md cites", ZH, None, "Этот файл остаётся источником ПЕРЕВОДА"),
 ("plan/src/lekciya-1.md", "generated view: lecture 1 expanded from its storyboard", PO, None, GEN_QUOTE),
 ("plan/src/plan.md", "rejected schedule of 32 sessions, kept as a historical draft", OT, None, "ЗАБРАКОВАН владельцем 06.08"),
 ("plan/src/punkty.md", "single home of the list of course points; source of the generated plan views", ZH, None, "Пункты курса «Пути и волны» — единый дом"),
 ("plan/src/voprosy.md", "list of the questions the year is assembled from, in groups", ZH, ARH, "открытый вопрос года | plan/src/voprosy.md"),
 ("zahody/ZAHOD-formy-yakobi.md", "executor brief: is F(z,q) a Jacobi form; stands on the cancelled circle frame", US, ZAM, "задания исполнителям, стоящие на отменённой рамке"),
 ("zahody/ZAHOD-okruzhnost-i-nepreryvnyj-predel.md", "first version of the circle brief, cancelled the same day", OT, None, "ОТМЕНЁН — см. ZAHOD-okruzhnost.md"),
 ("zahody/ZAHOD-okruzhnost.md", "brief that started the circle line: is it simpler on the circle", ZH, RT, "Живые заходы ZAHOD-okruzhnost.md"),
 ("zahody/ZAHOD-sverka-koncepcii.md", "executor brief: reconcile the concept, then modularity; stands on the cancelled circle frame", US, ZAM, "задания исполнителям, стоящие на отменённой рамке"),
]
def norm(s): return re.sub(r"\s+", " ", re.sub(r"[*`_]", "", s)).strip()
rows, weak = [], []
for path, phrase, status, ev, quote in DATA:
    full = P + path
    evf = ev or full
    lines = pathlib.Path(evf).read_text(encoding="utf-8").split("\n")
    hits = [i for i, l in enumerate(lines, 1) if norm(quote) in norm(l)]
    assert hits, ("quote not found", path, evf, quote)
    assert len(quote.split()) <= 12, ("quote longer than 12 words", quote)
    assert "|" not in phrase
    ln = hits[0]
    rows.append((full, phrase, status, evf, ln, quote, len(hits)))
    if ev is None and status == ZH and path in ("RASSKAZ-god.md", "PLAN-goda-krupno.md", "SBORKA/SLEDUYUSHCHIY-ZAHOD.md", "ZAMYSEL.md", "plan/src/karkas.md", "plan/src/punkty.md", "OBRAZEC-summy-kvadratov.md"):
        weak.append(full)
allp = sorted(str(p) for p in pathlib.Path("kurs-puti-i-volny").rglob("*.md"))
assert sorted(r[0] for r in rows) == allp, (set(allp) ^ {r[0] for r in rows})
out = ["| path | what it is | status | confirming address |", "|---|---|---|---|"]
for full, phrase, status, evf, ln, quote, nh in sorted(rows):
    out.append("| `%s` | %s | %s | `%s:%d` «%s» |" % (full, phrase, status, evf, ln, quote))
pathlib.Path("scratchpad/katalog-kursa/catalog-table.md").write_text("\n".join(out) + "\n", encoding="utf-8")
from collections import Counter
print("rows", len(rows), dict(Counter(r[2] for r in rows)))
print("self-attested (evidence is the row's own file):", weak)
print("multi-hit quotes (first hit used):", [(r[0], r[6]) for r in rows if r[6] > 1])
