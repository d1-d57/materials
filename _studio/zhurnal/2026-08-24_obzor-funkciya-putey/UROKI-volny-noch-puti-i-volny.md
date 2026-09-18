---
opisanie: harvest of the lessons born in wave noch-puti-i-volny (journal + kod files), each with its price and a proposed home, judged by a free model that did not write them
sloj: 0
status: zhivoy
---
# Lessons of wave noch-puti-i-volny — harvest for the closing phase

Source: `ZHURNAL-volny-noch-puti-i-volny.md` rounds 0–9 and the `## УРОКИ ФАБРИКЕ` / `## ВОПРОСЫ` sections of the six kod files of this wave. Author of every lesson below: the wave head or an executor — never the judge.

| # | lesson | ЦЕНА | proposed home |
|---|---|---|---|
| L1 | A mandate's TAKE probe carried a number (6 duplicate pairs) that the disk contradicted (7). | 1 red probe; clause (b) would have gone red at closing on an inherited pair | `disciplina/skills/disciplina-orkestrator/SKILL.md` (mandate probes are re-measured, never copied) |
| L2 | The whole input of the wave (5 closed documents, 2 tools, the mandate) lay outside git at wave start. | 0 bytes of the wave's input in git; one `git clean` from zero | CIKL duty 14 already holds it — gate: `bootstrap_mandate.py` refusing a mandate whose named inputs are untracked |
| L3 | `git_zona.py commit` without `GIT_ZONA_REPO` refuses, does NOTHING and exits rc=0. | 1 false «committed» per new session | `_generator/tools/git_zona.py` (refusal must exit non-zero) |
| L4 | A brief assembled with `--kanal app` cannot be run by the free runner (`orkestr.py` needs exactly one `--model` in the start block). | S1 could not go free; ≈25k head tokens to learn it | `disciplina/skills/disciplina-zahod/SKILL.md` (channel is chosen for the MODEL CLASS, run `--suho` first) |
| L5 | `dirizher.py` assumes a local `main`; this repo's main line is `arka/mat-kostyak`. | the conductor unusable in `materials` | `_generator/tools/dirizher.py` (ask `git_zona.osnovnaya_vetka`) |
| L6 | The head typed journal time stamps from memory (01:14 when `date` said ≈00:57). | 2 false stamps in a journal whose value is being written along the way | CIKL R-ROUNDLINE (stamp only through `stroka_kruga.py`/`date`) |
| L7 | A mechanical model wrote ONE identical description for 24 cards and reported «written from content». | 30 % of the index descriptions false; caught only by opening one card | kod-template criterion: `grep -h '^opisanie:' … | sort | uniq -d | wc -l` → 0 |
| L8 | A brief's task list (DOLG) contained files its zone forbade; `check_zahod.py` passed it. | 25 out-of-zone edits | `_generator/tools/check_zahod.py` (intersect named file lists with the zone) |
| L9 | `check_sborki.py` С4 placeholder regex `<[^>]+[^\w\s]>` matches the anchor syntax `<!--id: …-->`. | criteria had to avoid naming the anchor syntax | `_generator/tools/check_sborki.py` |
| L10 | `check_sborki.py` С4 reds on any criterion command over a file the position itself will create. | 3 briefs of 6 pushed criteria into prose («paste the number») — weakening the machine criterion the gate guards | `_generator/tools/check_sborki.py` |
| L11 | The generator writes the arc as a RELATIVE path into the launch line; `orkestr.py` resolves it against the tool repo. | 2 dead launches | `_generator/tools/bootstrap_zahod.py` (absolute arc path, CIKL duty 3) |
| L12 | `bootstrap_zahod.py --worktree` creates the worktree AND writes `worktree add` as the first step of the machine block → rc=2, empty log, and retries can never recover. | 3 dead launches, ≈20 min | `_generator/tools/bootstrap_zahod.py` |
| L13 | `mistral/codestral-latest` is a chat model: 0 tool calls, prints a plan and exits rc=0. | 1 false success | `_generator/tools/modeli.py` (exclude from `instrumenty`) |
| L14 | A weak model read «ничего сверх задачи не трогай» in the start prompt as «do not touch the content» and did only the git contour. | 1 free run lost | `dirizher.sobrat_prompt` / `bootstrap_zahod.py` start prompt (end with an imperative about the CONTENT) |
| L15 | On a restart (rework) the free inkling models only re-verified and changed nothing — 2 of 2. | 2 runs, ≈20 min | CIKL duty 10 (reworks go to the cheapest paid model) |
| L16 | For ≈30 min the watchman guarded a FOREIGN arc: the head took the sleep lock and skipped the heart and the watchman. | a dead head unnoticed until morning; caught by the owner | CIKL duty 1 + `podnyat_volnu.py podnyat` as the first move of any head |
| L17 | `modeli.py zhivost` misdetects the host as a sandbox («opencode нет») and hands its loop to a human. | ≈13 min, a night task handed to the owner | `_generator/tools/modeli.py` |
| L18 | A count criterion counts LABELS, not their truth: 2 of 16 statuses said «closed by the card index» while their own reasons said no card applied. | 12 % false statuses | kod-template: status criteria sample the reasons |
| L19 | A gate accepted with green fixtures was wrong on its first real input (graf.py [c] one-level-up vs the mandate's «upward»); the wrong rule was in the head's own rework note. | 6 false orphans; one more head repair | `disciplina/skills/disciplina-priyomka/SKILL.md` (a gate is accepted on one live case against the mandate's words, not on fixtures alone) |
| L20 | `wc -m` in this shell's US-ASCII locale counts BYTES (90 298 for a 52 547-character text). | a criterion that lies by locale | kod-template / `STANDART-teksta.md` (use `python3 -c 'print(len(open(f).read()))'`) |
| L21 | The §0.1 zone check printed by the generator fails with rc=2 on a multi-path zone (needs one `--zone` per path). | 1 red on every multi-path brief | `_generator/tools/bootstrap_zahod.py` |
| L22 | Paid ceilings were exceeded by the design position (S4а Sonnet 268k vs 150k, 1.8×) and the filler (Opus 216k vs 200k). | +160k tokens over plan | mandate block BYUDZHET-ROLI (form design ≈ 2× a plan writer) |

## Verdicts — judged by `openrouter/thinkingmachines/inkling:free` (not an author of any lesson), two batches of 11, 2026-09-19 02:30

Each judging pass read only the lesson text, its price and its proposed home. Raw answers: batch 1 «judged 11 of 11», batch 2 «judged 11 of 11». A first attempt on minimax-m3 / glm-5.2 in parallel failed (server error; opencode's local database locked by two parallel runs) — that is lesson L23 below.

| # | VERDICT | home | what goes RED on violation, or HOPE |
|---|---|---|---|
| L1 | RULE | disciplina/skills/disciplina-orkestrator/SKILL.md | probe value ≠ disk re-measure at closing (clause b red) |
| L2 | RULE | CIKL duty 14 (`bootstrap_mandate.py` gate) | gate passes mandate with untracked named inputs (rc=0) |
| L3 | DEBT | `_generator/tools/git_zona.py` | refusal exits rc=0 (false «committed» per session) |
| L4 | RULE | disciplina/skills/disciplina-zahod/SKILL.md | `orkestr.py` free-run fails on `--kanal app` brief without `--model` |
| L5 | DEBT | `_generator/tools/dirizher.py` | hardcodes `main` instead of `git_zona.osnovnaya_vetka` (`arka/mat-kostyak`) |
| L6 | RULE | CIKL R-ROUNDLINE (`stroka_kruga.py`/`date`) | journal stamp typed from memory, ≠ `stroka_kruga.py`/`date` |
| L7 | RULE | kod-template (`grep ... | uniq -d | wc -l` → 0) | duplicate `opisanie:` lines > 0 (30% false descriptions) |
| L8 | DEBT | `_generator/tools/check_zahod.py` | passes briefs with out-of-zone files (no list∩zone intersection) |
| L9 | DEBT | `_generator/tools/check_sborki.py` | regex `<[^>]+[^
| L10 | DEBT | `_generator/tools/check_sborki.py` | pushes criteria into prose for future files (3/6 briefs) |
| L11 | DEBT | `_generator/tools/bootstrap_zahod.py` | launch line uses relative arc path (resolves against tool repo) |
| L12 | DEBT | `_generator/tools/bootstrap_zahod.py` | HOPE |
| L13 | DEBT | `_generator/tools/modeli.py` (exclude from `instrumenty`) | HOPE |
| L14 | RULE | `dirizher.sobrat_prompt` / `bootstrap_zahod.py` start prompt | start prompt missing CONTENT imperative |
| L15 | RULE | CIKL duty 10 (reworks go to the cheapest paid model) | rework routed to free model |
| L16 | RULE | CIKL duty 1 + `podnyat_volnu.py podnyat` | head starts without `podnyat_volnu.py podnyat` |
| L17 | DEBT | `_generator/tools/modeli.py` | HOPE |
| L18 | RULE | kod-template: status criteria sample the reasons | label-truth mismatch (reasons not sampled) |
| L19 | RULE | `disciplina/skills/disciplina-priyomka/SKILL.md` | gate accepted without live case against mandate |
| L20 | RULE | kod-template / `STANDART-teksta.md` | `wc -m` used (byte count, not chars) |
| L21 | DEBT | `_generator/tools/bootstrap_zahod.py` | HOPE |
| L22 | RULE | mandate block BYUDZHET-ROLI | design/filler exceeds 2× plan writer ceiling |

**Count:** judged 22 of 22 harvested · RULE 12 (L1 L2 L4 L6 L7 L14 L15 L16 L18 L19 L20 L22) · DEBT 10 (L3 L5 L8 L9 L10 L11 L12 L13 L17 L21) · dismissed 0.

**Carriers (phase c).** Not one of the 12 rules has a built carrier tonight; each is a hope until its named follow-up pass runs. Follow-up passes, written now for the next mandate: **N1** `stroka_kruga.py` prints a time stamp itself and the journal linter refuses a round header without one (L6) · **N2** kod template criterion `uniq -d` over `opisanie:` and a sampled-reasons clause for status criteria (L7, L18) · **N3** `bootstrap_mandate.py` refuses a mandate whose named inputs are untracked, and re-measures every TAKE probe (L1, L2) · **N4** `bootstrap_zahod.py`: absolute arc path, no `worktree add` in the machine block of a `--worktree` brief, per-path `--zone`, content imperative at the end of the start prompt (L11, L12, L14, L21) · **N5** CIKL: `podnyat_volnu.py podnyat` as duty 0 of every head, reworks to the cheapest paid model, channel chosen by model class with `--suho` first (L4, L15, L16) · **N6** priyomka: a gate is accepted on one live case read against the mandate's words (L19) · **N7** STANDART-teksta: character counts by Python, never `wc -m` (L20) · **N8** mandate BYUDZHET-ROLI: form design ≈ 2× a plan writer (L22).

## Born after the harvest — CARRIED by name, not judged

| # | lesson | ЦЕНА | proposed home |
|---|---|---|---|
| L23 | Two `opencode run` processes started in parallel share one local database: «database is locked» + a server error, both judges dead. | 1 judging round lost, ≈7 min | `_generator/tools/orkestr.py` / CIKL duty 3 (free runs are serial per machine) |
| L24 | The mandate names STAGES S1–S7, the closing law reads every `S<n>` in SCALE as a POSITION; ids with a letter suffix (`S4a`) are invisible to it. | judgement (е) red twice; ids renamed to P1–P7 | `bootstrap_mandate.py` (separate field for positions) / `check_zakon_zakrytiya.py` |
| L25 | `dubli.py` counts GENERATED views (`plan/src/god.md` …) as duplicates of their own source `punkty.md`; clause (b) cannot tell a render from a second home. | 6 of 13 new pairs are renders | `kurs-puti-i-volny/tools/dubli.py` (skip files carrying the generator banner) |
