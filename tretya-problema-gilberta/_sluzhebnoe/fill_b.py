import sys, pathlib
F = pathlib.Path(sys.argv[1])
s = F.read_text(encoding="utf-8")

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new)

M = "/Users/ivanyakovlev/Documents/GitHub/materials/tretya-problema-gilberta"
MM = "/Users/ivanyakovlev/Documents/GitHub/matemdigest-map"
A = "_studio/zhurnal/2026-10-03_pravila-statya"
U = A + "/UROKI-FABRIKE.md"
SC = "scratchpad/statya-dvizhok"

rep("КОНТЕКСТ. <проект в 1–2 фразы>. Прошлый этап: <состояние>. ЦЕЛЬ: <что закрыть>.\n"
    "Приёмка — по ОТЧЁТУ, без построчной сверки. <Если стоп до цели: получишь X, но НЕ Y.>",
    "КОНТЕКСТ. Научпоп-статья «Третья проблема Гильберта» (`" + M + "/LENTA/`) принята владельцем 03.10; её вид для публикации "
    "собирался оверлеем руками (`" + M + "/publish_lenta.py`). Прошлый этап: заход `kod_pravila-teksty.md` этой арки перенёс уроки "
    "и текстовые правила, завёл профиль `skills/lenta/references/ZHANR-statya.md`. ЦЕЛЬ: носители-код для правил С6 и ЛП1–ЛП4 "
    "и возврат пяти инструментов math-style-editor.\n"
    "Приёмка — по ОТЧЁТУ, без построчной сверки. 🔴 СТОП ДО ЦЕЛИ: получишь режим вида, дверь, фикстуры, правила-рычаги и влитие, "
    "но НЕ опубликованную статью и НЕ проверку вида глазами — рендер на трёх ширинах делает аналитик на приёмке (браузера у тебя нет).")

rep("- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.",
    "- Прочитать ТОЛЬКО: `_generator/build_doc.py` (сборка `<head>`, разбор фронтматтера, выбор вкладок), `_generator/tools/check_termin.py`, "
    "`_generator/tools/check_view.py`; `" + M + "/publish_lenta.py` (его OVERLAY — спецификация вида, принятая владельцем); "
    "`" + M + "/PRAVILA-chernovik.md` §4 С6 и §5 ЛП1–ЛП4; `skills/lenta/references/ZHANR-statya.md`; таблица «draft N → arc N» в "
    "`## ОТЧЁТ` файла `" + A + "/kod_pravila-teksty.md`. Проект не изучай.")

TASK = f"""**Precondition — this pass starts AFTER `kod_pravila-teksty.md` is accepted.** In your worktree `{U}` must hold the 18 lessons and `skills/lenta/references/ZHANR-statya.md` must exist. Not so → STOP, write it in `## ВОПРОСЫ`, do nothing else.

**Build-time facts, recompute FIRST and write both values into `## ПЛАН` (snapshot 2026-10-03 ~16:10):**
- the engine does not read `zhanr:`: `grep -c zhanr _generator/build_doc.py` (build time: 0 hits outside the genre-of-statement dictionary — read them)
- KaTeX the view links: `grep -o 'katex@[0-9.]*' {M}/LENTA/view.html | head -1` → katex@0.16.9; vendored: `ls _generator/vendor/katex` → only LICENSE and katex.min.js (no css, no fonts)
- matemdigest-map: branch `git -C {MM} rev-parse --abbrev-ref HEAD` → rabota; behind the night branch `git -C {MM} log --oneline rabota..zahod/stil-noch | wc -l` → 24; the five tools `ls {MM}/vypuski | grep -c -E '^(stil_svod|vnesti_pravki|zamer_elusion|check_oboroty|check_dlina)\\.py$'` → 0; working tree `git -C {MM} --no-optional-locks status --porcelain | wc -l` → 0

**Never build into the materials repo** — it is outside your zone. Copy `{M}/LENTA` into `{SC}/LENTA` and build there; same for any other lenta you build.

**Step 1 — view mode `zhanr: statya` in `build_doc.py` (С6).** The engine reads `zhanr:` from the frontmatter; for `statya` it puts `data-zhanr="statya"` on `<body>` and ships CSS scoped by `[data-zhanr="statya"]` that reproduces the OVERLAY of `{M}/publish_lenta.py` (owner-accepted 03.10): no duplicate header and no tab bar for a one-tab document; margin notes (`.mn`) inline in the flow — no right column; text column scales together with the font (zoom steps, ≈ 88 characters per line at every width); figures not wider than 680px; first paragraph larger; table of contents behind a button below 900px. The values in OVERLAY are the spec — do not redesign. A document without `zhanr:` or with any other value must come out byte-identical to the old engine.

**Step 2 — service `.md` in a lenta folder (ЛП2).** A `*.md` whose name starts with `_` is not a tab: the engine skips it and prints one warning line naming the file. Fixture `_generator/tools/fixtures/build_doc/` — a two-file folder (`lenta.md` + `_chernovik.md`).

**Step 3 — publish door (ЛП4).** Move `{M}/publish_lenta.py` to `_generator/tools/publish_lenta.py` (the original stays where it is — materials is not yours). New call form: `python3 _generator/tools/publish_lenta.py <view.html> <out.html>` — KaTeX CSS and every font inlined as `data:font/woff2` from `_generator/vendor/katex/` (vendor `katex.min.css` and `fonts/*.woff2` of exactly the version the engine links — e.g. `npm pack katex@0.16.9`, take `dist/`; LICENSE is already there). The overlay leaves the door: the engine does it now (Step 1). The door keeps both asserts (link found; exactly one `</head>`) and its docstring says WHY: an artifact page accepts external stylesheets only from Google Fonts (CSP).

**Step 4 — `check_termin.py` false red (ЛП3).** Case: a two-word term whose second word is shorter than `MIN_LEN` («инвариант Дена») collapses to the one-word key «инвариант» and fires on «инвариант Хадвигера» defined earlier. Fix so the short word stays part of the key. Fixture `_generator/tools/fixtures/check_termin/`: defines «инвариант Хадвигера», uses it, later defines «инвариант Дена» and only then uses it — must be green; plus one true-red twin (term used before its definition).

**Step 5 — `check_view.py`: literal backslash (ЛП1).** In a built view, a `\\` printed at the end of a line inside a cat is a defect (FORMA §5 after the previous pass). Fixture `_generator/tools/fixtures/check_view/`: a cat with a trailing `\\` → red; the etalon article built in `{SC}` → green.

**Step 6 — rules with levers (door `pravilo.py`, `--skill lenta`, `--rychag`).** Five calls; `--zakryvaet` uses ARC numbers through the table in `kod_pravila-teksty.md` `## ОТЧЁТ`: С6 → draft lesson 11, lever `_generator/build_doc.py` (statya mode); ЛП1 → lesson 15, lever the check_view fixture; ЛП2 → lesson 16, lever the build_doc warning + fixture; ЛП3 → lesson 14, lever the check_termin fixture; ЛП4 → lessons 12, 13, 1, lever `_generator/tools/publish_lenta.py`. Then: `ZHANR-statya.md` С6 — replace «carrier does not exist yet» by the two carriers; `FORMA.md` «## §5. Диалект движка…» — one row about the publish door.

**Step 7 — matemdigest-map: merge `zahod/stil-noch` into `rabota` (lesson 18).** Premise checked at build time: the five tools were never lost — they live only on the unmerged night branch (17–20.08, also on origin); the links in `skills/math-style-editor/SKILL.md` are right. Do NOT switch the branch; not on `rabota` → STOP. Use the door: `GIT_ZONA_REPO={MM} python3 _generator/tools/git_zona.py merge --help` first, then merge with zones `vypuski`, `docs/fazy/stil.md`, `zhurnal/2026-08-17_instrument-stilya`. Build-time dry merge: exactly one conflict, in `zhurnal/2026-08-17_instrument-stilya/NOCH/OTCHET-nochi.md` (journal prose) — resolve by UNION of both sides, never by picking one; `vypuski/proverki.py` and `docs/fazy/stil.md` changed on both sides and merged cleanly. Anything else conflicts → STOP, quote RAW. Hook red → §4 rules.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ)** — before → after in `## ОТЧЁТ`, every number by its command:
1. Statya mode on the live object, not only fixtures: build `{SC}/LENTA` → `grep -c 'data-zhanr="statya"' {SC}/LENTA/view.html` rises from zero (old engine) to one; `check_view.py {SC}/LENTA` green; `check_lenta.py {SC}/LENTA/lenta.md` → «это не лента … L9 чиста».
2. No regression: copy `skills/lenta/references/lenta-etalon.md` into `{SC}/etalon/`, build with the old engine (`git show main:_generator/build_doc.py > {SC}/old_build_doc.py`) and with the new one; `diff` of the two views prints zero lines (or only a named build-timestamp line).
3. Door: `python3 _generator/tools/publish_lenta.py {SC}/LENTA/view.html {SC}/publish.html` rc=0; in the output the KaTeX CDN stylesheet link count is zero and the `data:font/woff2` count equals the `@font-face` count of the vendored css (both by `grep -c`).
4. Each new fixture is red on the old code and green on the new — both rc printed (old code via `git show main:<file>`).
5. `grep -c '^\\*\\*ЗАКРЫВАЕТ:\\*\\*' skills/lenta/RESHENIYA.md` grows by exactly five over its value after the previous pass, and `grep -c '^\\*\\*РЫЧАГ' skills/lenta/RESHENIYA.md` grows by exactly five.
6. matemdigest-map: the five tools present (count by the build-time command: zero → five); `rabota..zahod/stil-noch` count falls to zero; all eight tools answer `python3 vypuski/<tool>.py --help` with rc=0 (check_idioma, check_fraza, check_stil, stil_svod, vnesti_pravki, zamer_elusion, check_oboroty, check_dlina) — list each rc.
7. Commit hashes: disciplina zone, matemdigest-map merge; `git_zona.py check --zone …` ✅ for disciplina.
**Coverage line inside the verdict:** «levers recorded X of 5; fixtures red→green Y of 3; tools answering Z of 8»."""

i = s.index("Конкретные шаги — у автора.")
assert s.count("Конкретные шаги — у автора.") == 1
j = s.index("\n", i)
s = s[:i] + TASK + s[j:]
F.write_text(s, encoding="utf-8")
print("ok")
