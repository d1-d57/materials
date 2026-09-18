# MANDATE — noch-puti-i-volny

<!-- assembled by bootstrap_mandate.py; two halves, two authors; do not merge them -->

**STATUS:** `OPEN`
**TOP_HALF_STATUS:** `COMPLETE`
**BOTTOM_HALF_STATUS:** `PENDING`
**ARC:** `_studio/zhurnal/2026-08-24_obzor-funkciya-putey`
**JOURNAL:** `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/ZHURNAL-volny-noch-puti-i-volny.md`
**ASSEMBLED:** `2026-09-19`

> Status is one of `OPEN` · `CLOSED` · `REFUSED` · `CLOSED-S-DOLGOM`. `REFUSED` is a LAWFUL outcome and
> needs a written reason in the bottom half — refusing is not the same as stopping.
> The one outcome forbidden to the orchestrator is to stop and leave the wave
> untouched: a tool's refusal is a task, not an outcome
> (`skills/disciplina-orkestrator/SKILL.md`).

> Phase markers — `TOP_HALF_STATUS: COMPLETE` (this tool always writes the top
> half) and `BOTTOM_HALF_STATUS: PENDING` / `COMPLETE` (the orchestrator flips it
> on return). The linter REFUSES mismatch with STATUS: OPEN ↔ PENDING, CLOSED ↔
> COMPLETE. A reader without context can tell which half is done.

> 🔴 `JOURNAL` — the wave's journal, written ALONG THE WAY, circle by circle, never
> reconstructed at the end of the shift (owner, 03.09, repeated 06.09). Every record
> carries a PRICE AS A NUMBER and a line ABOUT THE LEADING HEAD ITSELF, not only
> about the subject of the wave. At `STATUS: CLOSED` the linter REFUSES a mandate
> whose journal is absent, empty, missing those two halves in a record, or reached
> git in a single sitting; where the journal is outside git the signal cannot be
> computed and the linter answers `НЕПРОВЕРЯЕМО` (rc 3) rather than passing in
> silence. A wave whose journal is empty or back-dated does not count as closed.

## START MESSAGE — WHAT THE OWNER PASTES INTO CLAUDE CODE

```
Ты голова ночной волны. Модель: Opus — ты собираешь позиции и судишь их, а
рассуждение рождается по ходу.

Репозиторий работы: /Users/ivanyakovlev/Documents/GitHub/materials
Инструменты фабрики:  /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools

Твой мандат — единственный вход:
/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-08-24_obzor-funkciya-putey/mandate_noch-puti-i-volny.md

Прочитай его ЦЕЛИКОМ, затем дисциплину головы:
  disciplina/skills/disciplina-orkestrator/SKILL.md
  disciplina/skills/disciplina-orkestrator/CIKL-ORKESTRATORA.md

Тексты позиций пишешь ТЫ, не владелец: bootstrap_zahod.py по одному на ступень,
гейт check_zahod.py зелёный до пуска. Ступень не стартует, пока её зависимость
не ЗАКОММИЧЕНА — проверяешь коммит, а не слово исполнителя.

Позиция S1 написана, её гейт check_zahod.py зелёный (rc=0), начни с неё:
_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_pasporta-korpusa.md
Заходы для ступеней S2-S7 пишешь сам, по одному, перед запуском каждой.

🔴 ТРИ ВЕЩИ, КОТОРЫЕ УЖЕ ЕСТЬ НА ДИСКЕ — не смей писать их заново:
  1. Рассказ про ВЕСЬ ГОД — obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/,
     восемь глав, 119 581 знак, вся годовая программа собрана в рассказ про одну
     функцию. Единственный дефект — написано занудно, владелец не смог прочесть.
     S4 это ПРАВКА СТИЛЯ, а не первый черновик.
  2. Как из одного объекта получаются частные — kurs-puti-i-volny/OBEKT.md §2,
     утверждения 4, 5, 8 скелета, раздел каркаса «Как одно вкладывается в другое».
     Исследовано, проверено счётом, записано.
  3. Программа года полекционно — kurs-puti-i-volny/plan/src/karkas.md, 32 темы.
🔴 Прежде чем сказать «этого нет», назови команду, которой ты это проверил, и
прочитай kurs-puti-i-volny/ARHITEKTURA.md §0. Аналитик, писавший этот мандат,
дважды за одну сессию объявил пустым то, что лежит на диске. Не повтори.

🔴 ГЛАВНОЕ ОГРАНИЧЕНИЕ — ТОКЕНЫ. Механику отдавай бесплатным и малым моделям,
платные только под суждение (четыре плана и закон закрытия). Бюджеты ролей
и порог остановки — в мандате, блок В. Дошёл до порога — доводишь начатое,
пишешь журнал и закрываешься, не спрашивая.

Владелец спит. Вопросы пиши в раздел QUESTIONS TO THE OWNER мандата и продолжай
работу, не блокируясь на них. Дополнения владельца, если появятся утром, — в
раздел DOPOLNENIYA.
```

## HALF ONE — WRITTEN BY COWORK, BEFORE THE WAVE

### GOAL

Fold everything already learned about the course Puti i volny into one graph that cannot lose anything, and derive from it four linked plans - year, first part, first quarter, first lecture - where each finer plan specialises the coarser one and the linkage is machine-checked

### INTERVIEW — RENDERED IN ENGLISH FROM A RUSSIAN CONVERSATION — 2026-09-18

> **ИНТЕРВЬЮ ПРОВЕДЕНО** (flag `--intervyu da` at assembly). ⚠ The flag proves the
> assembler was asked, not that the conversation happened — same honest limit
> `bootstrap_zahod.py --intervyu` already prints. ⚠ The interview was held in
> Russian and what is recorded here is the ENGLISH RENDERING of the settled
> meaning, not a quotation. A rendering can be wrong, and only the owner can
> say so.

- **Q1** — Q: Q1
  — M: Nothing may be lost: a concept once found, written down and named must never fall out of reach again. The real product is a structure where loss is impossible by construction, not by diligence
- **Q2** — Q: Q2
  — M: No duplication. Each thing is laid down once, in one home, referenced by id from everywhere else. Two articles about one subject is the failure mode to design against
- **Q3** — Q: Q3
  — M: Year story, first part, quarter plan and first-lecture plan are one structure at four magnifications; each finer plan specialises a named item of the coarser one, and that linkage is a machine-checked gate, not a hope
- **Q4** — Q: Q4
  — M: Token spend is the binding constraint. Work cheap: free or small models wherever the task is mechanical, paid only where judgement is produced during execution
- **Q5** — Q: Q5
  — M: The orchestrator writes its own position briefs, launches them, watches them, restarts dead channels, makes each position commit as it goes, and reads those commits to judge quality. The analyst supplies the mandate, not the briefs

### FINALIZED AT INTERVIEW — 2026-09-18

- [F1] One home for findings - catalan/kartoteka/; creating a second card index is forbidden
- [F2] The knowledge index is the OUTPUT of tools/indeks.py built from file headers; never hand-edited
- [F3] IWE and any markdown normaliser are not installed: they delete anchors and break KaTeX
- [F4] The link year -> quarter -> lecture must be a machine-checkable id reference, not prose
- [F5] Every position prepares its successor: its last move writes the successor context
- [F6] Tokens are the binding constraint; mechanical work goes to cheap models, paid models only for judgement

### BOUNDARIES AND WHAT IS ALREADY CLOSED

- Course mathematics is untouched: no new theorems, no filling of PAZL holes - those are separate research waves
- No IWE, no markdown normalisers - reason in kurs-puti-i-volny/SBORKA/RESHENIE-instrumenty.md
- No second card index
- Closed on 18.09, do not reopen: KARTA-rashozhdeniy, REESTR-tekstov, KALENDAR-i-sostav, OBEKT.md, PAZL.md, ARHITEKTURA.md, tools/indeks.py

### CLOSING PHASE — KNOWLEDGE

**The orchestrator runs this phase AFTER the last pass is ACCEPTED and BEFORE the
bottom half is written.** It is not optional and not a report: `--lint` refuses a
bottom half that does not answer it with numbers.

**a. HARVEST.** Collect every lesson, debt and incident born in THIS wave — from the
`kod_*` files of the wave and from the wave journal. Count them.

**b. JUDGE.** Every harvested lesson gets a verdict, from a FRESH free-model pass, in
batches of about ten, and NEVER from the model that wrote it — the author is the
wrong judge, and that is the structural reason this phase exists at all. Three
lawful verdicts: it becomes a **RULE** in a named skill · it becomes a **DEBT** at a
named address · it is **dismissed** with a reason. A lesson with no `ЦЕНА:` is not
judged at all: it goes back to its author as `доработка`, because a lesson without a
price is an observation.

**c. RULES TO CARRIERS.** For every lesson promoted to a rule, name what goes RED when
it is violated. If nothing can, the rule is declared a **hope**, in writing, by our own
law (`skills/disciplina-kachestvo/SKILL.md`). Each new carrier — a gate, a phase, an
artifact field — becomes a NAMED follow-up pass, written now: run in this wave if the
clock allows, carried into the next mandate if not.

**d. BALANCE.** Print the four numbers below. That single delta is what tells us
whether we are winning.

**COST.** All of it on free models, judging batched, and each judging pass reads only
the lesson text, its price and its named home — never the repository. The phase is
bounded by the CLOCK, not by a number of tries: when time runs out, unjudged lessons
are listed BY NAME in the bottom half and carried into the next mandate as an explicit
debt. They may never be dropped silently.

### RESPONSIBILITIES — fixed here so they stop being re-decided every wave

| what | whose |
|---|---|
| MERGING a branch | the pass itself, as its last move |
| ACCEPTANCE of a returned pass | the orchestrator, per pass, in parallel |
| COMMITS ALONG THE WAY | the pass, by path, as it goes |
| THE FINAL COMMITS AND THE PUSH | the orchestrator |
| THE CLOSING PHASE | the orchestrator, before the mandate is closed |

**ЗАКРЫВАЮЩАЯ ПОЗИЦИЯ:** `ZK1` — zakon-zakrytiya-noch-puti-i-volny

> **This is the LAST NAMED POSITION of the wave, and it is what runs the law
> of closure over this mandate.** It does not live in a Stop hook: a hook is
> killed at its 600 s ceiling and its verdict then vanishes without a word, so
> «found no violation» and «stopped existing» look identical from outside.
> A position of the wave has no ceiling.
>
> Its outcome is one of these, and all are lawful: `CLOSED`, or `CLOSED-S-DOLGOM`
> with one `**ДОЛГ УСЛОВИЯ (<letter>):**` line per condition that stayed red.
> The wave ends either way — a red condition MOVES, with a name, and is never
> dropped. `--lint` refuses a closing status that did not name this position.
>
> 🔴 **ORDER OF MOVES, AND IT IS NOT DECORATION.** This position appends its own
> line to the СОСТАВ file, which means the law it runs JUDGES IT TOO. Run the law
> only AFTER this position's own report has been accepted and its branch merged
> and retired — otherwise the branch condition and the verdict condition go red
> on the position itself, and the wave reads that as its own failure. Measured
> live, not reasoned: running the law straight after appending the line failed
> the verdict condition (this position's own kod_ file is not on disk yet) and
> left the branch condition unjudgeable; completing the cycle first gave five
> green out of five.

_Its line for the wave's `СОСТАВ` file — append it as it stands, no hand editing:_

```
ZK1|zakon-zakrytiya-noch-puti-i-volny|opus|_studio/zhurnal/2026-08-24_obzor-funkciya-putey/mandate_noch-puti-i-volny.md|pryamoj
```

### SCALE

7 stages with dependencies, 9-12 positions; one night, 6 hours target; at most 2 positions in parallel and never two on the same model. S7 (the first-lecture plan) has a deadline outside the wave and is finished even if the stop threshold is hit; S5 is the first stage to drop if something must be dropped

### WHAT COUNTS AS FAILURE

🔴 **REWRITTEN AFTER VERIFICATION.** The first version had six clauses and a verifier proved that
**not one of them could fail**: (a) was measured by a gate that forgives inherited debt, (c) by a gate
that catches the opposite error, and (b), (d), (e), (f) by nothing at all. A criterion that cannot go
red is a wish. Each clause below now names the command that judges it.

| # | failed if | judged by |
|---|---|---|
| **a** | files without a description remain | `python3 kurs-puti-i-volny/tools/indeks.py` prints **`без описания: 0`**. ⚠ Do **not** read `✅ гейт зелёный` for this — the gate forgives the 78 inherited files by design and is green right now with all 78 unwritten |
| **b** | an entity acquired a second home | `python3 kurs-puti-i-volny/tools/dubli.py` shows no NEW pair above 0.45 beyond the six known today. The known six are listed in the journal as the baseline before S1 starts |
| **c** | a plan does not reference the plan above it | the tool does not exist yet, **so S2 builds it**: `graf.py` prints, for every anchor matching `god-|chast-|chetvert-|lekciya-`, whether it has an outgoing `[[…]]` upward. Zero orphans required. ⚠ The linkage syntax is `[[id]]` and nothing else — `indeks.py` reads only that form; prose such as «обобщает god-03» passes no gate |
| **d** | spend exceeded the stop threshold | the head records its own token counter in the round line each round; no factory tool measures wave spend, so this clause is held by the head's own arithmetic and that is said out loud rather than pretended |
| **e** | the year story reads as a syllabus | judged by a **fresh verifier who has not seen the corpus and knows nothing of these discussions**. It reads the text alone and answers: did it enjoy a finished story · what is the author leading to · and — the real question — **did it see how these unfamiliar tools help investigate a probability model**. An answer that does not match the concept fails the clause. The owner is asleep; a naive reader is the closest available instrument, and the substitution is named, not hidden |
| **f** | S7 was not delivered | `ls -la kurs-puti-i-volny/plan/src/lekciya-1.md` and it is non-empty |

---

## BLOCKS B–E OF THE CANON — WRITTEN BY HAND

> `bootstrap_mandate.py` has flags only for block A. Blocks B–E are named in
> `skills/disciplina-orkestrator/KANON-MANDATA.md` and **have no refusal yet** — the canon
> says so itself and calls it a debt (position Ц9). Written here by hand, deliberately,
> because a field without a refusal is still better than a field that is absent.

### OSNASTKA — taken and proved before launch

Each mechanism carries a VERB and a PROBE. `TAKE` refuses on failure; `MEASURE` records
the result and red is lawful.

| mechanism | verb | probe — command with the expected answer |
|---|---|---|
| sleep lock | TAKE | `caffeinate -dimsu &` then `pgrep caffeinate` returns a pid. A sleeping Mac stops every window at once; this was the price paid on wave 2 |
| index generator | TAKE | `cd kurs-puti-i-volny && python3 tools/indeks.py --proverit; echo $?` → `0` |
| duplicate detector | TAKE | `python3 kurs-puti-i-volny/tools/dubli.py --porog 0.45` prints `пар выше порога: 6` |
| calendar | TAKE | `python3 kurs-puti-i-volny/proverki/kalendar_goda.py` prints `слотов 33, тем 32` |
| graph primitives | MEASURE | `python3 ../disciplina/_generator/tools/reserch/topsort_karty.py --help; echo $?` → `0` |
| model pool | MEASURE | 🔴 corrected after verification — the old probe returned `rc=2`, it is an argument parser, not a report. Read the registry without touching the network: `python3 -c "import json;d=json.load(open('../disciplina/doma/zahody/MODELI-ZHIVOST.json'));print(d['data_dannyh'], sum(1 for v in d['modeli'].values() if v['sostoyanie']=='живa'))"` — expected: a date not older than a day and at least 5 alive. **Snapshot on 17.09 was 8 alive of 25, two days stale.** Refresh with `modeli.py zhivost` only if the count is below 5: the call is networked and costly, and debt 10 of CIKL-ORKESTRATORA forbids probing the pool 'just in case' |
| conductor | MEASURE | `python3 ../disciplina/_generator/tools/dirizher.py --help; echo $?` |

🔴 **Two-stage probe.** The synthetic probe above proves the script. The **observed** probe
proves the harness and is taken **after the first position's first move**. The wave is not
launched until stage two has passed.

### BYUDZHET-ROLI — token budget per role

Wave 2 spent 10M tokens, of which 5M went to twelve writers at ~420k each for six lines of
task. That is the whole reason this field exists.

| role | budget | what it does |
|---|---|---|
| `mehanik` | **220k** | headers, links, registration, running generators. No judgement. 🔴 Raised from 80k after verification: S1 must read and describe **78 files**, about 1k tokens each with the read, so 80k was unreachable by arithmetic and the position would have died mid-way looking like a lazy executor |
| `pisatel-plana` | **150k** | writes one plan (year / quarter / lecture) from material already on disk |
| `instrumentalshchik` | **120k** | writes one tool on top of existing primitives |
| `verifikator` | **60k** | reads the result without seeing the work; verdict plus coverage |
| `golova` (orchestrator itself) | **400k** | assembling briefs, launching, reading commits, judging |

🔴 **A number given as a CEILING works as a TARGET.** These are ceilings. The target is
*finish the task*, and a position that finishes at 30k is a good position, not an
under-performing one.

### PLATNO-PO-POSTROENIYU — paid by nature, not an escalation

Three kinds of work are paid by construction and do not count against the escalation clause:
writing all four plans - year story, first part, quarter, lecture (judgement is produced during execution, not before); the closing
law of the wave; any verifier whose job is to disprove the analyst. Everything else — headers,
links, scripts, greps, registration — is mechanical and goes to free or small models.

### ESKALACIYA — when a paid model becomes lawful

A position may move to a paid model when **both** hold: the free channel failed twice with a
machine-visible cause (rate limit, empty log, provider withdrawal), and the position is on the
critical path of a stage that blocks the next. Otherwise the position waits in quarantine.
Escalation is written into the journal with the cause class, never silently.

### PARALLEL — read by the conductor, not prose in SCALE

**At most 2 positions at once, and never two on the same model.** On wave 2 this rule stood as
prose inside `scale`, the conductor never saw it, and four positions went in parallel.

### POLITIKA-KANALOV — the outcome class decides the channel's fate

| outcome | what it means | what to do |
|---|---|---|
| rate limit | channel alive, temporarily busy | quarantine with a named term, retry after it |
| timeout | channel alive, task too big | quarantine, split the position |
| empty log | the command is wrong, not the channel | fix the command, do not touch the pool |
| withdrawn by provider | the only irreversible outcome | remove from the pool, record the provider text |

**Never conclude "the models gave up" while the pool is alive.** Five of twelve positions on
wave 2 were written off that way against a live pool.

### POROG-OSTANOVKI — number on the binding resource

**Stop at 70% of the head's context window, or at 2.5M total wave tokens, whichever comes
first.** On reaching it the wave finishes what is started, writes the journal and closes —
without asking. Half-done work that is committed is worth more than a full plan that died with
the window.

### CHTO-OGRANICHIVAET — the binding constraint

**TOKENS.** The owner named this directly. Time is not binding (the night is long), money is
not binding separately from tokens, external resources are not involved. Everything else is
declared unconstrained explicitly, so nobody spends the night guessing what to economise.

### POROG-PEREDACHI — managed handover threshold

**At 60% of the head's context** the wave goes to a managed handover and does not wait for
auto-compaction at ~97%. 🔴 Corrected after verification: this stood at 70% — the same number as the
stop threshold — so at one moment the head was ordered both to close the wave and to hand it over.
Handover comes first and comes earlier; stopping is the later, harder event. Compaction mid-work is quiet degradation that nobody notices.

### POROGI-SREDY — environment thresholds

Free disk not below 10 GB (`df -h .`); working copies not above 20 (`git worktree list | wc -l`
— **today it is 16**, so this threshold is nearly reached and new worktrees are not to be
created casually). The factory produced 237 working copies and 23 GB once already.

### MARSHRUT-NAHODOK — where a finding goes so it survives the wave

| kind of finding | address |
|---|---|
| mathematical finding about the course | a card in `catalan/kartoteka/` plus its line in `KARTA-OBLASTI.md`, same move |
| two documents disagreeing | a row in `kurs-puti-i-volny/SBORKA/KARTA-rashozhdeniy.md` |
| lesson about the factory | `UROKI-FABRIKE.md` of this arc, with a PRICE |
| knowledge about a channel or model | `disciplina/_generator/tools/modeli.py`, as a comment with the provider text |
| defect of this mandate | a `dopolnenie` record below, typed |

🔴 A position's verdict is **not closed** until its findings have been routed to the addresses
above. On wave 2 the 72 KB find-box existed only because the owner demanded it by hand.

### GEJT-POZICII — checked before a position is launched

1. Not a single absolute path of the main tree in the brief text. On wave 2 all twelve texts
   carried 17–23 such paths and two executors rewrote tools in the main tree.
2. The readiness criterion names an artefact that can go red, and carries its own coverage
   (`checked X of Y`, with Y counted from the source **before** the work).
3. The brief names what to read by name, and says "do not study the project".

### DOPOLNENIE — the flow of owner additions

Record `Д<N>`: time from `date` · text · GROUNDS (a measurement) · TYPE · STATUS.
Four types: `ПРАВКА-ЗАКОНА` (names `F<N>`) · `НОВАЯ-РАБОТА` · `ЗАПРЕТ` · `ОТМЕНА-РЕШЕНИЯ`.
At closing every `ПРАВКА-ЗАКОНА` is either promoted into `RESHENIYA.md` or dropped with a named
reason. **The count of law-amendments is printed in the closing balance** — it is the direct
measure of how good this mandate was.

---

## STAGES — ORDER WITH DEPENDENCIES, NOT A LIST OF IMPORTANCE

> Each stage names what it consumes and what it produces. A stage does not start until its
> dependency has been **committed** — the conductor checks the commit, not the executor's word.

**S1 · PASSPORTS — the corpus becomes visible.** *Depends on: nothing.* The brief is already
written and its gate is green: `kod_pasporta-korpusa.md`. Produces: `INDEKS.md` with zero
undescribed files, `[[kart-…]]` links from the corpus into the card index, and the successor
context file. Role `mehanik`.

**S2 · GRAPH STATISTICS — the corpus becomes measurable.** *Depends on: S1.* One tool over the
corpus graph, standing on the primitives of `disciplina/_generator/tools/reserch/topsort_karty.py`
(`postroit_graf`, `komponenty`, `najti_cikl`, `kan_poryadok` — do not write these again). It must
answer the six questions nobody answers today: degree distribution · transitive closure and
cascade ("if I rewrite X, what falls downstream") · chain length and graph depth · reachability
from the entry point · one graph over the whole corpus · export of edges to a machine format.
Role `instrumentalshchik`.

**S3 · CONSOLIDATION — the corpus stops arguing with itself.** *Depends on: S1.* Runs
`tools/dubli.py`, routes the findings, closes the rows of `KARTA-rashozhdeniy.md` that a document
edit can close, and moves into the card index whatever findings are living as prose in reports.
🔴 Does not decide the four owner questions (Р1–Р4, Р16) — those are the owner's and stay open.
Role `mehanik`. May run in parallel with S2.

### 🔴 THE SHAPE OF THE COURSE — SETTLED BY THE OWNER 19.09, USE THIS AND NOT THE OLD KARKAS

The writing stages S4–S7 all specialise **one** structure, and the owner stated it directly. Do not
re-derive it, do not take it from `plan/src/karkas.md` where block 3 and block 4 still separate the
plain and the `q` version — that separation is exactly the oscillation diagnosed as Р3.

**The board advances; the weight is switched on and stays on.**

| floor | board | weight | what falls out |
|---|---|---|---|
| **lecture 1** | line | `q` off | binomial coefficients — the baby example of the whole course |
| **quarter 1** | line | **`q` on** | `q`-binomials (Gaussian), partitions. The quarter GENERALISES lecture 1 — same story, one handle turned |
| **next** | ray | **both at once** | Catalan and `q`-Catalan **together, in one pass** — not the plain version first and the weighted one a block later |
| **then** | segment | both | the global generalisation: everything above is a substitution in one function |
| **last** | — | — | analysis: asymptotics, Laplacian, the limit |

🔴 **The relation between the magnifications is GENERALISATION, not summary.** Lecture 1 is quarter 1
with the weight switched off. Quarter 1 is the first part with the board still the line. The first part
is the year without analysis. Every plan must make its own generalisation visible, in one sentence,
in its opening.

### THE WRITING STAGES

**S4 · YEAR — THE READABLE STORY.** *Depends on: S2 and S3.* This is the megalecture, and it is the
one text the owner will actually read. Requirements, and they are the point of the stage:

- **A popular-science narrative, not a syllabus.** One full story about generating functions, told so
  that it is interesting to read — simple, clear, engaging, not dry. Genre reference already settled:
  Étienne Ghys, *A Singular Mathematical Promenade* (`ZAMYSEL.md` §1).
- **Standing on the research already done, not on new material.** `OBEKT.md` holds the object, its
  specialisations with their verification coverage, the four views; `catalan/kartoteka/` holds 24
  findings; `SKELET.md` holds 36 statements. The story is assembled FROM these with addresses, and
  nothing in it may lack one.
- **Honest where the course is honest.** The fourth view is a promise, not a result; say so in the text.
- Every item of the structure gets an anchor `<!--id: god-NN-->`.

🔴 **THE YEAR STORY ALREADY EXISTS. S4 IS A REWRITE, NOT A FIRST DRAFT — corrected 19.09.**

An earlier version of this mandate said «there is no story about the year on disk». **That was false**,
and the owner corrected it. `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/` holds eight finished
chapters, 119 581 characters, in which the whole year's programme is folded into a story about **one
function**; `00-arhitektura.md` carries the throughline and a table mapping chapter → course blocks,
and all seven blocks are covered. The error came from repeating a verifier's fine distinction («this
is a story about the OBJECT, not about the YEAR») as a claim of emptiness — the exact failure this
wave exists to end, committed while writing the mandate against it.

**What is actually wrong with it is one thing: the owner could not read it.** It is dull. That is a
defect of style, and S4's job is to fix that defect — keeping the content, the throughline, the two
detective knots (André who never used the reflection; Rogers unnoticed for twenty-three years) and the
five existing SVG figures. Rewrite for readability; do not rebuild from nothing and do not re-derive
mathematics that is already proved.

The same correction applies to the specialisation story: **how the many particular cases fall out of
one object is researched and written** — `OBEKT.md §2` with verification coverage, `SKELET.md`
statements 4, 5, 8, the karkas section «Как одно вкладывается в другое», and the identification of the
object as the Al-Salam — Ismail polynomials. Nothing there is to be invented again.

Role `pisatel-plana`, paid by construction. Run the Russian editor gates before handing it over.

**S5 · FIRST PART — LINE → RAY → SEGMENT, BEFORE ANALYSIS.** *Depends on: S4.* How one board turns into
the next, and why each turn is forced rather than chosen. ⚠ The owner says outright this may **not fit
into two quarters** — so the stage reports what it costs in sessions and does not pretend it fits.
Anchors `<!--id: chast-NN-->`, each referencing a `god-NN`.

🔴 **Where the first part ARRIVES — stated by the owner 19.09.** The segment is the generalisation that
swallows the two boards before it. Take the segment from $0$ to $n$ and two points $A$, $B$ inside it
at some distance from the ends: three parameters, of which one can be pinned at zero, leaving **the
length of the path and the height — the number of cells**. For such trajectories one counts how many
there are, and one writes their generating function; that function specialises to everything that came
earlier. Many of the theorems about it come from the **reflection principle**, and the two things to
produce are a formula for the generating function and a formula for an individual coefficient.

**That is the destination of the first half, and it is the thing the first lecture models in
miniature.** The whole part is the same four-beat pattern as S7 — question from probability, identity
to sum, beautiful proof, packing into the generating function — run on boards of growing generality.

⚠ **Analysis is NOT in this part**, by the owner's decision of 19.09, recorded in
`kurs-puti-i-volny/ZAMYSEL.md §3` under `id: analiz-vo-vtoruyu-polovinu`. No asymptotics, no Stirling,
no differential equations anywhere in the first half. The stage does not smuggle them in as «just a
remark at the end», which is exactly how they were standing in the karkas at the end of topic 1.

**S6 · FIRST-QUARTER PLAN.** *Depends on: S5.* Six Saturdays, 19.09–24.10 (`proverki/kalendar_goda.py`).
The line with the weight on: `q`-binomials, partitions. Anchors `<!--id: chetvert-NN-->`, each
referencing a `chast-NN`. The quarter must state in its first line how it generalises lecture 1.

**S7 · FIRST-LECTURE PLAN — THE ONE THAT IS READ TODAY.** *Depends on: S6.* One session, 90 minutes,
blackboard, upper school. The line, no `q`: paths and binomial coefficients, Pascal, Vandermonde by
double counting, return to zero. **Detailed and concrete — a minute-by-minute plan of a single hour,
not a topic list.** Ends with the question that opens the quarter: what happens if we count not just
the path but the area under it. Anchors `<!--id: lekciya-NN-->`, each referencing a `chetvert-NN`.

🔴 **THE LINKAGE IS THE POINT, AND IT IS A GATE.** Year → part → quarter → lecture is one structure at
four magnifications. After S7, `python3 kurs-puti-i-volny/tools/indeks.py` resolves every `god-NN`,
`chast-NN`, `chetvert-NN` reference and prints **zero** dangling ids. A plan item referencing nothing
above it is an orphan: link it or delete it, there is no third outcome.

⚠ **If the stop threshold is reached before S7, S7 is what gets finished anyway** — it is the only
stage with a deadline outside the wave.

🔴 **DROPPING S5 IS NOT ALLOWED AS WRITTEN — corrected after verification.** S6 depends on S5 and its
anchors reference `chast-NN`; dropping S5 leaves S6 with nothing to reference and lights failure
clause (c) by construction. If something must be dropped: **S5 shrinks to a one-page skeleton with
anchors only and no prose**, which keeps the reference chain alive. S7 may then be written straight
from S6. Nothing else is droppable.

### 🔴 OUTPUT ADDRESSES — added after verification, because not one stage had one

Four paid writers with empty context would have put four texts in four different places, and clause
(f) would have been unjudgeable. Every stage now names what it PRODUCES:

| stage | PRODUCES — exact path |
|---|---|
| S1 | `kurs-puti-i-volny/INDEKS.md` (regenerated) · `kurs-puti-i-volny/SBORKA/SLEDUYUSHCHIY-ZAHOD.md` |
| S2 | `kurs-puti-i-volny/tools/graf.py` · its output `kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` |
| S3 | edits in place; new rows in `kurs-puti-i-volny/SBORKA/KARTA-rashozhdeniy.md`; new cards in `catalan/kartoteka/` |
| S4 | `kurs-puti-i-volny/RASSKAZ-god.md` |
| S5 | `kurs-puti-i-volny/plan/src/chast-1-do-analiza.md` |
| S6 | `kurs-puti-i-volny/plan/src/chetvert-1.md` |
| S7 | `kurs-puti-i-volny/plan/src/lekciya-1.md` |

Each new `.md` is registered the same move it is created:
`python3 ../disciplina/_generator/tools/register_doc.py <path> "<one phrase>"`.

### 🔴 S7 — HOW IT IS BUILT. OWNER, 19.09, AND IT OVERRIDES EVERYTHING ELSE ABOUT S7

**The first lecture is the first semester in miniature.** Not an introduction to it — a working model
of it, on the simplest board. Everything that follows this stage is subordinate to that sentence.

#### The four-beat pattern, repeated five times

This is the whole lecture, and it is also the whole semester:

> **a probabilistic question** → it turns into **a combinatorial identity that has to be summed** →
> **a beautiful proof is found for that identity** → and the result **is packaged as a statement about
> the generating function**.

🔴 **Algebra here is not a method of proof. It is the packing.** The question comes from probability,
the answer comes from the model, the identity is proved combinatorially — and only then does the
generating function say the same thing in one line. Never «let us prove this identity algebraically».

#### The selection gate — the whole reason this stage is hard

**An example goes in ONLY if it generalises.** Not «it is beautiful», not «it is in the boiler» —
**each of the five must name what it becomes later in the course**, and that name is the entry ticket.
Two examples whose generalisation is already known:

- **Vandermonde.** Cut the path at an intermediate moment. $\sum_j\binom mj\binom n{k-j}=\binom{m+n}k$,
  proved by double counting. Packed as $(1+z)^m(1+z)^n=(1+z)^{m+n}$ — cutting a path **is** multiplying
  generating functions. **Generalises into:** the transfer matrix on the segment, and every «cut and
  glue» argument of the year.
- **Expectation.** $\sum_k k\binom nk=n\,2^{n-1}$, proved by the committee-with-a-chairman double count.
  Packed as **the derivative of the generating function at 1**. **Generalises into:** any statistic on
  paths is a differential operator on the function — and that is precisely how the `q`-layer arrives
  next quarter, where $q\partial_q$ counts area.

🔴 **«Five» was the owner speaking loosely and is NOT a requirement — corrected 19.09.** There is no
required count and no required list. Vandermonde and expectation are offered as illustrations of what
passing the gate looks like; the position may drop both if the story comes out better without them.

**The criterion is a brilliant, finished, beautiful lecture — not a quota and not this particular
logic.** It must have its own internal logic and aesthetic: it is visible why each subject was chosen,
visible where the author is leading, everything develops without a jolt, and the whole thing is
packed well at the end. Deciding mid-work that all of this is nonsense and rebuilding it differently
is a legitimate outcome of a creative process, not a failure of the brief.

#### 🔴 What is NOT in the first lecture, by decision

- **No asymptotics, no Stirling, no differential equations.** Analysis moves to the second half of the
  course **as a whole**, and the first lecture does not trespass on it. This closes what `karkas.md`
  put at the end of topic 1 ($\sim1/\sqrt{\pi n}$) and removes cell A-III from this stage's scope.
- **Nothing that needs the ray.** No Catalan, no first return, no ballot numbers, no non-return
  probability. Those live on a board this lecture does not have yet.
- **No Pascal-triangle recreations** that lead nowhere: Sierpiński, Lucas, Kummer. Pretty and sterile.

#### Homework

Problems about **deep combinatorics and deep probability**, not about recurrences inside the triangle.
Each problem's fact must be *seeable* at the level of the generating function and packable as a
statement about it — that is the shape of the answer we are teaching, not the proof technique we are
drilling.

#### ⚠ THE PASCAL BOILER IS A DRAFT, NOT A LECTURE — correction of an earlier overclaim in this mandate

`lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/kotly/matematika.md` is 1102 lines with 17 proved
statements, and an earlier version of this section called it «the material is already on disk». **The
owner corrected that on 19.09 and he is right.** That lecture was built toward the return problem and
Catalan numbers — the ray, which we do not have here — and **it contains no generating functions at
all**, which is the entire point of ours. Parts of it are plainly unwanted (Sierpiński). Use it as a
**source of facts and of two or three good problems**, not as a skeleton. The skeleton is the
four-beat pattern above, and S7 is written from it, essentially from scratch.

Still worth taking from there, already proved: **Vandermonde** (statement 10) and **the sum of squares
as two walks meeting** (11–12) — both pass the selection gate. And one finished problem with a
memorable answer: three consecutive numbers of one row in ratio 1:2:3 — unique in the whole infinite
triangle, row 14, numbers 1001, 2002, 3003, checked by exhaustion to $n\le700$.

### 🔴 THE FIRST-QUARTER COMPOSITION IS SETTLED — use this, the karkas disagrees

`plan/src/karkas.md` gives quarter 1 as topics 1–6 ending with Franklin's involution. The owner's
decision of 18.09 (`SBORKA/KALENDAR-i-sostav.md`) removed topics 5 and 6 — Euler's pentagonal numbers
and Franklin — from the main course to the club, because they do not generalise. **The decision wins;
the karkas is stale here.** Quarter 1 is: lecture 1 (line, no `q`) plus the `q` line — Young diagrams,
Gaussian binomials, the generating function of partitions — and the remaining Saturdays begin Catalan.
S6 records this and does not re-open it.

## DOPOLNENIYA — OWNER ADDITIONS, WRITTEN HERE AS THEY ARRIVE

> 🔴 Added after verification: the canon calls this «the third half of the mandate», and the first
> version described the FORMAT without providing the PLACE. The owner wakes, writes Д1, and there is
> nowhere to put it. Here is the place.
>
> Record: `Д<N>` · time from `date` · text · GROUNDS (a measurement, not an impression) · TYPE ·
> STATUS. Types: `ПРАВКА-ЗАКОНА` (names the `F<N>` it amends) · `НОВАЯ-РАБОТА` · `ЗАПРЕТ` ·
> `ОТМЕНА-РЕШЕНИЯ`. At closing each `ПРАВКА-ЗАКОНА` is promoted into a decision or dropped with a
> named reason, and their COUNT is printed in the balance — it measures how good this mandate was.

### Д1 · 2026-09-19 00:54 · ТИП: `НОВАЯ-РАБОТА` · СТАТУС: выдано голове в чат

**Текст.** Нулевым ходом, ДО S1 и до любой другой работы: вывезти в git всё, что лежит вне его.

**ОСНОВАНИЕ — замер, не впечатление.** `git_zona.py check` на момент выдачи мандата:
**вне git 49 путей** — рождено и никогда не ставилось 21, правлено и не закоммичено 28. Среди
рождённых — вся работа ночи 18–19.09: `kurs-puti-i-volny/ARHITEKTURA.md`, `OBEKT.md`, `PAZL.md`,
`INDEKS.md`, вся папка `SBORKA/`, `tools/indeks.py`, `tools/dubli.py`, `proverki/kalendar_goda.py`,
сам этот мандат и заход `kod_pasporta-korpusa.md`. Это существует в одном экземпляре и умирает от
одного `git clean`.

**Почему это не сделал аналитик.** Из песочницы Cowork коммит оставляет мёртвый `index.lock` и
кладёт репозиторий — цена записана в `HANDOFF-2026-09-03.md` этой же арки. Голова работает
host-side и пишет в `.git` законно.

**Как.** `git_zona.py plan` → `git_zona.py commit --zone <зона>`, зонами, не одним ходом.
Разумное деление: (1) `kurs-puti-i-volny` — ночная работа аналитика; (2) папка этой арки — мандат,
заход, журнал; (3) `obzory/funkciya-putey-i-ee-uravneniya` — шапки восьми глав прогулки.
⚠ Звал `register_doc.py` — `_studio/docs/KARTA.md` уезжает в ТОТ ЖЕ коммит.
⚠ `--no-optional-locks` обязателен: у владельца может идти параллельная ручная работа.

**Чего НЕ делать.** Не коммитить чужое: в 49 путях есть работа других проектов
(`diskmat-57/`, `_fond/`, `spetsmat-2026/`) — она не наша, пальцем не трогать, в отчёт строкой.

**Готово, когда:** `git_zona.py check` по трём названным зонам зелёный, и число «вне git» в целом
по дереву упало не меньше чем на 21 — то есть ни один рождённый ночью файл больше не сирота.


### Д2 · 2026-09-19 00:58 · ТИП: `ПРАВКА-ЗАКОНА` (правит F4) · СТАТУС: выдано голове в чат

**Что решил владелец.** Планы года, полугодия, четверти и лекции **повторяют один и тот же список
пунктов** — год короче, четверть подробнее, но список ТОТ ЖЕ. Значит у этого списка обязан быть один
источник истины, иначе в одном месте курс состоит из трёх частей, в другом из четырёх.

**ОСНОВАНИЕ.** Это уже случилось и посчитано: `SBORKA/KARTA-rashozhdeniy.md` Р13 — три разных
разбиения состава года в трёх живых файлах; Р10 — число глав прогулки 6/7/8; Р5 — арифметика
сведения 20/23/41, ни одна не сходится. Все три от одной причины: список писали руками в нескольких
местах.

---

#### 🔴 ПОРЯДОК: СНАЧАЛА АРХИТЕКТУРА ОТДЕЛЬНОЙ ПОЗИЦИЕЙ, ПОТОМ НАПОЛНЕНИЕ

Требование владельца дословно: «в одном заходе архитектуру, в другом — заполнить эту структуру».
Не смешивать: позиция, которая проектирует форму и одновременно пишет содержание, всегда
подгоняет форму под то, что уже написала.

**S4а — АРХИТЕКТУРА ПУНКТА.** Проектирует и строит механизм, содержание не пишет.
**S4б и далее — НАПОЛНЕНИЕ.** Пишут пункты по готовой форме, форму не трогают.

---

#### Механизм: пункт — атом, планы — ВИДЫ над ним

Единственный дом списка — один файл пунктов. Планы всех четырёх увеличений **порождаются из него
скриптом** и руками не пишутся, ровно как `INDEKS.md`. Тогда «три части против четырёх»
невозможно: число не пишется, а считается.

**Поля пункта — предложение S4а, владелец правит.** Первые три — исторический стандарт этого курса,
и владелец назвал его прямо: «когда мы писали план на год, каждая лекция содержала красивую теорему,
красивый вопрос, красивую задачу — и она была классная, модная, интересная».

| поле | что это |
|---|---|
| `id` | `p-NN`, стабильный, по нему ссылаются все виды |
| `имя` | ⭐ название, которое, увидев главой в книжке, хочется прочитать |
| `вопрос` | ⭐ красивый вопрос, с которого пункт начинается |
| `teorema` | ⭐ красивая теорема — то самое «ого» |
| `задача` | ⭐ красивая задача |
| `доска` · `вес` | координата: прямая / луч / отрезок / предел · `q` выкл / вкл |
| `обобщается-в` | id пункта, которым это станет дальше. **Гейт отбора:** пункт без обобщения в курс не идёт |
| `опирается` | id пунктов, без которых этот не читается — рёбра графа |
| `адрес` | где материал: утверждение скелета, карточка картотеки, файл |

**Виды, которые порождает скрипт:**

- **план года** — все пункты, по строке: имя + вопрос;
- **план полугодия** — фильтр по половине, плюс теорема;
- **план четверти** — фильтр по четверти, все ⭐-поля целиком;
- **план лекции** — один пункт, развёрнутый в раскадровку.

**Гейты, которые это даёт бесплатно** (и они закрывают клаузу (c) провала):
сирот нет — у каждого пункта, кроме первого, есть `опирается`; висячих ссылок нет; сумма пунктов
по четвертям равна числу занятий из `proverki/kalendar_goda.py`; у каждого пункта заполнены все
три ⭐-поля — пустое ⭐ красное, потому что пункт без красивого вопроса и есть скучный пункт.

---

#### Что наполнить в ЭТУ волну, а что только завести

**Наполнить полностью:** первая четверть. Плюс два свода по пунктам — про обе половины
(до анализа и с анализом) и отдельно про часть «до анализа».

**Завести пустыми, с именем и координатой, без ⭐-полей:** четверти 2, 3, 4. Расписывать их сейчас
не нужно и вредно — форма ещё не обкатана.

**Критерий приёмки владельцем, дословно:** он читает выданные пункты и говорит «вау, хорошие
пункты, красиво звучит, здорово, всё интересно». Формального гейта у этого нет и быть не может —
но пустое ⭐-поле краснеет машинно, а скучное ⭐-поле ловит свежий читатель клаузы (e).

⚠ **Структура у нас уже есть** — `plan/src/karkas.md` с 32 темами, у каждой назван центральный
объект и «ого». S4а не изобретает её заново, а **переводит в машинную форму** и добавляет
недостающие поля. Требование владельца к результату: структура должна стать **самоценной и
красивой**, а не служебной таблицей.

### Д3 · 2026-09-19 01:14 · ТИП: `ПРАВКА-ЗАКОНА` (правит F6 и блок BYUDZHET-ROLI) · СТАТУС: принято головой

**Текст (владелец в чат, записано головой).** Рамку токенов можно увеличить; дешёвую модель жалеть меньше, чем дорогую; недельный лимит довести **не выше 45 %**.

**ОСНОВАНИЕ — замер.** `get_usage` в 01:14: недельный лимит (все модели) **38 %**, 5-часовое окно 11 %, контекст головы 337 890 из 1 000 000 (34 %). Запас волны до потолка владельца — **7 пунктов недельного лимита**. Бюджет головы 400k по блоку BYUDZHET-ROLI к этому моменту уже на 85 % израсходован — поэтому связывающий ресурс меняется: считаем не токены головы, а **недельный процент**.

**Как голова исполняет.** Процент снимается `get_usage` каждый круг и пишется в строку круга. **42 %** — не запускать ничего, кроме цепочки к лекции 1 (S4а → S4б); S4в (рассказ про год) переводится на меньшую модель или уходит долгом. **44 %** — доводить начатое, писать журнал и закрываться, не спрашивая. Порядок отказа: сначала S4в, потом верификаторы на Sonnet заменяются Haiku; S4б (Opus, лекция 1) не режется.

## HALF TWO — WRITTEN BY THE ORCHESTRATOR, ON RETURN

> Not written yet: the wave has not returned. STATUS stays `OPEN` until it has, and
> `--lint` says so out loud instead of passing in silence.

### WHAT WAS ASSEMBLED AND LAUNCHED

<NOT FILLED>

### WHAT IT REPAIRED ITSELF AND WHY IT WAS BROKEN

<NOT FILLED>

### VERDICTS

- **kod_pasporta-korpusa.md** — принято — S1 (Haiku 4.5, 137k tokens, 7 min, 8 commits): 80 of 81 files described, 17 of 24 cards linked from the corpus (88 links, 0 dangling), successor file written and registered. Head found and repaired by script (75a7e11a): 24 card descriptions were ONE identical placeholder naming the wrong project; the edit lay outside the brief's zone because the brief listed the cards in DOLG while forbidding catalan/kartoteka — a brief defect, not an executor one. Residual red: 'без описания: 1' is INDEKS.md itself, which the closed generator cannot describe — question V1 to the owner.
### WHAT WAS EXCLUDED AND WHY

<NOT FILLED>

### IRREVERSIBLE ACTIONS

<NOT FILLED>

### QUESTIONS TO THE OWNER — ANSWER IN PLACE, UNDER EACH

> 🔴 **A QUESTION HERE IS NOT A COMPLAINT — IT IS THE ONLY LAWFUL FORM OF
> «I could not do this because the decision is not mine».** An item excluded
> with a written reason that amounts to «I lacked the owner's decision» is not
> an outcome: it is a question that was never asked, and the orchestrator
> quietly decided for two people that there was no time to ask.
>
> **Form:** one `[Vn]` item per question. Each carries WHAT is blocked,
> WHAT was measured about it already, and the SHAPE of a usable answer — so the
> owner can reply in one line rather than reconstruct the problem. The owner
> writes the answer directly underneath, in place.
>
> **Empty is lawful** and means «nothing was blocked by a missing decision» —
> which is a claim, not a default, and `--lint` will not let it hide a REFUSED
> or a partially delivered wave.

- **[V1] May the head make a 3-line change to the closed `kurs-puti-i-volny/tools/indeks.py` so that the generated `INDEKS.md` carries its own `opisanie:` header?**
  BLOCKED: failure clause (a) of this mandate — `indeks.py` prints `без описания: 1`, and the one file is `INDEKS.md` itself: the generator overwrites it on every run, so no hand header survives (S1 tried, commit `105308d8`, erased by the next run). `tools/indeks.py` is in «Closed on 18.09, do not reopen», so the head did not touch it.
  MEASURED: `cd kurs-puti-i-volny && python3 tools/indeks.py` → `без описания: 1 (унаследованных 1, новых 0)`; `grep -v '^#' tools/DOLG-bez-opisaniya.txt` → `kurs-puti-i-volny/INDEKS.md`.
  USABLE ANSWER: «да» — the head adds a YAML header with `opisanie:` to the text `написать_индекс` emits and removes INDEKS.md from the DOLG file (one commit, reversible); or «нет» — clause (a) stays red and moves as a named debt.


### CLOSING PHASE — KNOWLEDGE BALANCE

> The four numbers below are the point of this section. `DELTA` is not
> stored, it is CHECKED: `--lint` recomputes `BORN` minus `CLOSED` and
> refuses a mismatch. `CARRIED` above zero REQUIRES the unjudged lessons
> to be listed BY NAME underneath — carried is lawful, silent is not.

**BORN:** `<NOT FILLED>`
**CLOSED:** `<NOT FILLED>`
**CARRIED:** `<NOT FILLED>`
**DELTA:** `<NOT FILLED>`

_Carried by name (one line each, or the single word `none`):_
<NOT FILLED>

### LINE-BY-LINE ANSWER TO EVERY FINALIZED ITEM

<NOT FILLED>

> One line per finalized item, and every item of the top half must get one: `done` or `not done` with the reason. This field is the point of the whole artifact.
- [F1] <NOT FILLED>
- [F2] <NOT FILLED>
- [F3] <NOT FILLED>
- [F4] <NOT FILLED>
- [F5] <NOT FILLED>
- [F6] <NOT FILLED>
