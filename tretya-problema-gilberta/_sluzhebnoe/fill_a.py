import sys, pathlib
F = pathlib.Path(sys.argv[1])
s = F.read_text(encoding="utf-8")

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new)

M = "/Users/ivanyakovlev/Documents/GitHub/materials/tretya-problema-gilberta"
A = "_studio/zhurnal/2026-10-03_pravila-statya"
U = A + "/UROKI-FABRIKE.md"

rep("<одна фраза почему (Sonnet — механика расписана; Opus — план рождается по ходу)>",
    "every rule and lesson text is already written in the drafts, the homes and anchors are named; the work is placement and door calls, not invention")

rep("КОНТЕКСТ. <проект в 1–2 фразы>. Прошлый этап: <состояние>. ЦЕЛЬ: <что закрыть>.\n"
    "Приёмка — по ОТЧЁТУ, без построчной сверки. <Если стоп до цели: получишь X, но НЕ Y.>",
    "КОНТЕКСТ. Сессия 02–03.10 сделала научпоп-статью «Третья проблема Гильберта» (материал `" + M + "/LENTA/`, владелец принял и опубликовал). "
    "Прошлый этап: замечания владельца разобраны в три черновика в папке материала — `OPIS-zamechanij.md` (П1–П32, A1–A11), "
    "`PRAVILA-chernovik.md` (правила по домам), `UROKI-chernovik.md` (уроки с ценой). ЦЕЛЬ: перенести уроки и ТЕКСТОВЫЕ правила "
    "в дома дисциплины ничего не потеряв; закоммитить папку материала.\n"
    "Приёмка — по ОТЧЁТУ, без построчной сверки. 🔴 СТОП ДО ЦЕЛИ: получишь уроки, правила-тексты и профиль жанра, но НЕ код "
    "(режим вида statya в `build_doc.py`, дверь публикации, фикстуры, влитие инструментов math-style-editor) — это заход "
    "`kod_statya-dvizhok.md` той же арки, он стартует после приёмки этого.")

rep("- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.",
    "- Прочитать ТОЛЬКО: три черновика `" + M + "/{UROKI-chernovik,PRAVILA-chernovik,OPIS-zamechanij}.md`; "
    "принимающие файлы зоны (каждый — перед правкой); `" + M + "/LENTA/lenta.md` — только чтобы цитировать примеры. Проект не изучай.")

TASK = f"""**Language.** Rule statements you add to English files (`SKILL.md`, `RESHENIYA.md` via the door, `FORMA.md` is Russian — follow the receiving file) follow the language of the receiving file. 🔴 Named exception: lesson titles and `ЦЕНА:` texts go into `UROKI-FABRIKE.md` VERBATIM in Russian from the draft — they are the owner's record, a translation loses it. Russian examples (❌/✅) stay Russian everywhere.

**Snapshot at build time 2026-10-03 ~16:00 — recompute each number with its command FIRST and write both values into `## ПЛАН`:**
- lessons in the draft: `grep -c '^### ' {M}/UROKI-chernovik.md` → 18
- lessons already in the arc: `grep -c '^### [0-9]' {U}` → 0
- rule entries per home: `grep -c '^\\*\\*ЗАКРЫВАЕТ:\\*\\*' skills/<s>/RESHENIYA.md` for mat-blok, math-style-editor, illustracii, lenta → 0, 0, 0, 0
- lexicon bodies Л16–Л20: `grep -c -E '^## Л(1[6-9]|20) ' skills/math-style-editor/references/leksika.md` → 0; table rows: `grep -c -E '^\\| Л[0-9]+ ' skills/math-style-editor/SKILL.md` → 15
- the false FORMA row: `grep -c 'жёсткий перенос' skills/lenta/references/FORMA.md` → 1
- profile file: `ls skills/lenta/references/ZHANR-statya.md` → absent

**Step 1 — lessons (door `urok.py`, never by hand).** For every `### N.` of `UROKI-chernovik.md`, in order 1→18:
`python3 _generator/tools/urok.py {A} --zagolovok "<title after 'N. '>" --cena "<text of its ЦЕНА: line>" --chem <ЧЕМ> --predmet "<ПРЕДМЕТ>" --dom <ДОМ>`
— ЧЕМ/ПРЕДМЕТ/ДОМ verbatim from the lesson's `> ЧЕМ: … · ПРЕДМЕТ: … · ДОМ: …` line (lesson 8 has two paths in ПРЕДМЕТ — pass both, space-separated). `ВЕРДИКТ:` stays empty — acceptance fills it. Door refuses a value → stop on that lesson, quote the refusal RAW in `## ВОПРОСЫ`, continue with the next. Write the table «draft N → arc N» into `## ОТЧЁТ`; every `--zakryvaet` below uses ARC numbers through it.

**Step 2 — mat-blok (draft §1, МБ1–МБ9, all universal).** (a) In `skills/mat-blok/SKILL.md` add a subsection after «### Machine coverage — what greps catch and what does not» and before «## §4. Fields of a block»: heading «### §3.2 How a proof and a definition are written down — nine rules (owner, 2026-10-03)», one numbered item per МБ-rule, each with its ❌/✅ example from the draft. In «### §3.1 What a definition must contain» add one line pointing to МБ7. (b) One `pravilo.py` call per rule: `python3 _generator/tools/pravilo.py --skill mat-blok --tekst "<МБk one line>" --zakryvaet {U}#<arc N> --nadezhda "<reason>"`. Lessons closed (draft numbering, translate through the table): МБ1→7; МБ3, МБ4, МБ5, МБ6→8; МБ2, МБ7, МБ8, МБ9→9. Nadezhda reason, same for all nine unless you find a real counter: «no countable signal; held by reading — mat-blok verifier».

**Step 3 — math-style-editor (draft §2).** (a) `references/leksika.md`: five bodies `## Л16 · …` … `## Л20 · …` in the format of the existing ones (what it is, owner's examples, how it differs from the nearest rule); add the three new examples to the body of Л4. Title line «тела пятнадцати правил» → «тела двадцати правил». (b) `SKILL.md`: five rows Л16–Л20 in the «## LEXICON» table (columns # | rule | Уn | carrier; level by the table's legend; carrier = the grep candidate from the draft marked as candidate, or `DOLG`-style «no counter»), heading «fifteen rules» → «twenty rules». (c) `pravilo.py --skill math-style-editor`, five calls: Л16–Л19 close draft lesson 6; Л20 closes draft lessons 4 and 6 (comma-separated). Each `--nadezhda` names the candidate lever from the draft (e.g. Л17: «grep «конечно много» — not yet wired into a gate»).

**Step 4 — illustracii (draft §3).** (a) `SKILL.md`, section «## Mandatory on every drawing»: add И1 (described construction → a figure in the neighbouring block; pre-delivery pass «construction verb without a figure»). Section «## Green build ≠ good illustration»: add И2's two live examples (label «b» on the arrow, the arrow on «−a»). (b) one `pravilo.py --skill illustracii` for И1, closes draft lesson 10, `--nadezhda` naming the grep candidate.

**Step 5 — lenta (draft §4 and ЛП1 of §5).** (a) Create `skills/lenta/references/ZHANR-statya.md`: header in the house style (КОГДА читать · ЧТО здесь · КУДА дальше), etalon path `materials/tretya-problema-gilberta/LENTA/` (accepted by the owner 03.10), then nine sections `## С1 · …` … `## С9 · …` with the draft's text and its «Закрывает П…» tags kept. С6 says plainly that its carrier (view mode + publish door) is built by `kod_statya-dvizhok.md` and does not exist yet. (b) `FORMA.md` «## §7. Чужой жанр…»: one paragraph — `zhanr: statya` has its own positive profile in `ZHANR-statya.md`. (c) `FORMA.md` «## §5. Диалект движка…»: the row whose first cell is «**`\\` в конце строки** = жёсткий перенос `<br>`» is replaced by the ЛП1 text (inside a cat `\\` at line end prints literally; line breaks inside a cat persist on their own); abort if the row is found ≠1 times. (d) `SKILL.md`: next to the row «genre flag: `zhanr:` in frontmatter…» add a row «popsci article — `zhanr: statya` → `references/ZHANR-statya.md`». (e) `pravilo.py --skill lenta`, seven calls, `--nadezhda`: С1, С4, С5, С7 → draft lesson 3; С2, С3 → lesson 4; С8 → lessons 1 and 5. С6 and ЛП1–ЛП4 are NOT recorded here (their levers are code — the next pass records them). С9 has no lesson: profile only, named in `## ОТЧЁТ` as «rule without a lesson».

**Step 6 — commits.** disciplina: the zone by `§4` as you go. materials (separate repo, do NOT switch its branch — at build time it stands on `arka/mat-kostyak`, check `git -C /Users/ivanyakovlev/Documents/GitHub/materials rev-parse --abbrev-ref HEAD` and NAME the branch in the report): `GIT_ZONA_REPO=/Users/ivanyakovlev/Documents/GitHub/materials python3 _generator/tools/git_zona.py commit --zone tretya-problema-gilberta --zone README.md -m "tretya-problema-gilberta: popsci article on Hilbert's third problem + drafts of rules and lessons"` (README.md change at build time: one added row, `git -C … diff --stat -- README.md` → 1 insertion). Hook red on materials → by §4 rules, never bare `--no-verify`.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ)** — all on the branch, every number by its command, both values (before → after) in `## ОТЧЁТ`:
1. `grep -c '^### [0-9]' {U}` = 18, and `python3 _generator/tools/check_uroki.py` on the arc green (if its call form differs — `--help`, quote it).
2. `grep -c '^\\*\\*ЗАКРЫВАЕТ:\\*\\*'` in RESHENIYA: mat-blok 9 · math-style-editor 5 · illustracii 1 · lenta 7 (sum 22). Every `ЗАКРЫВАЕТ` id resolves to a live lesson (the door checks it; quote one door output).
3. leksika: Л16–Л20 bodies = 5; SKILL.md Л-rows = 20.
4. `grep -c -E '^## С[1-9] ' skills/lenta/references/ZHANR-statya.md` = 9; `grep -c 'жёсткий перенос' skills/lenta/references/FORMA.md` = 0.
5. Nothing lost: `git diff main...HEAD -- skills | grep -c '^-[^-]'` ≤ 3, and each removed line is named (FORMA row, «fifteen» heading, «пятнадцати» title).
6. Two commit hashes (disciplina, materials) + `git_zona.py check --zone …` ✅ for both.
**Coverage line inside the verdict:** «lessons recorded X of 18; rules recorded Y of 22 (+ С9 profile-only)»."""

i = s.index("Конкретные шаги — у автора.")
assert s.count("Конкретные шаги — у автора.") == 1
j = s.index("\n", i)
s = s[:i] + TASK + s[j:]
F.write_text(s, encoding="utf-8")
print("ok")
