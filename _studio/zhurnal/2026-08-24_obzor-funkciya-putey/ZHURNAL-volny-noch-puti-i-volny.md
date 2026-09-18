# ZHURNAL — wave noch-puti-i-volny

> Journal of the wave, written ALONG THE WAY, round by round. Every record: a PRICE as a number
> and a line ABOUT THE HEAD ITSELF. Mandate: `mandate_noch-puti-i-volny.md` (same folder).

## Round 0 — 2026-09-19 00:50 MSK — tooling and baselines, before S1

- **Tooling (OSNASTKA), measured by command:** caffeinate pid 25005 (TAKE ✅) · `indeks.py --proverit` rc=0 (TAKE ✅) · `topsort_karty.py --help` rc=0 · `dirizher.py --help` rc=0 · calendar `слотов 33, тем 32` (TAKE ✅) · model registry dated 2026-09-17T16:22 (two days stale), 9 alive of 25 → above 5, not refreshed (debt 10: no probing «just in case»).
- 🔴 **Duplicate baseline differs from the mandate: `dubli.py --porog 0.45` prints `пар выше порога: 7`, the mandate says 6.** The mandate's TAKE probe is therefore red by one pair. Not a wave failure — the baseline for clause (b) is recorded here as the MEASURED seven, by name:
  1. 0.989 `kurs-puti-i-volny/OBRAZEC-summy-kvadratov.md` ↔ `kurs-puti-i-volny/obrazec/src/obrazec.md`
  2. 0.546 `kurs-puti-i-volny/zahody/ZAHOD-formy-yakobi.md` ↔ `kurs-puti-i-volny/zahody/ZAHOD-sverka-koncepcii.md`
  3. 0.516 `obzory/funkciya-putey-i-ee-uravneniya/SKELET.md` ↔ `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA/00-obshchee.md`
  4. 0.502 `kurs-puti-i-volny/KOSTYAK.md` ↔ `kurs-puti-i-volny/otchety/RAZBOR-i-perestroyka.md`
  5. 0.467 `kurs-puti-i-volny/plan/src/karkas.md` ↔ `kurs-puti-i-volny/plan/src/plan.md`
  6. 0.465 `kurs-puti-i-volny/PERESTROYKA.md` ↔ `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/00-arhitektura.md`
  7. 0.455 `kurs-puti-i-volny/ARHITEKTURA.md` ↔ `kurs-puti-i-volny/ZAMYSEL.md`
  ЦЕНА: 1 pair of disagreement between a mandate probe and the disk, found in 1 command; had the head trusted the mandate's «6», clause (b) would have gone red at closing on an inherited pair.
- 🔴 **The whole 18.09 corpus lay OUTSIDE git at wave start:** `git status` shows untracked `kurs-puti-i-volny/{ARHITEKTURA,INDEKS,OBEKT,PAZL}.md`, `SBORKA/`, `tools/`, `proverki/kalendar_goda.py`, plus the mandate and `kod_pasporta-korpusa.md` themselves, and 1-line uncommitted edits in all 9 `LEKCIYA-v2/*.md`, `ZAMYSEL.md`, `catalan/kartoteka/KARTA-OBLASTI.md`, `catalan/NAVIGATION.md`. A worktree cut from `main` would not contain the tools S1–S3 stand on. ЦЕНА: 5 closed documents + 2 tools + the mandate = the entire input of the wave, 0 bytes of it in git. Repair: duty 14 of CIKL — the wave's first move is a commit of its assembly (this round).
- **Head's own counter:** 15 000 000 − 14 845 520 ≈ **155k** consumed so far (reading mandate 42 KB + SKILL 62 KB + CIKL 15 KB + S1 brief). Budget of the head 400k.
- **ГОЛОВА О СЕБЕ:** read 120 KB of discipline before the first action — 40% of the reading was the skill's debts and blind spots, not duties. Next head: read CIKL first, SKILL only §SUPERVISION/§ACCEPTANCE. ЦЕНА: ≈35k tokens of the head's 400k budget spent on sections that did not change a single move.

## Round 1 — 2026-09-19 01:14 MSK — Д1 executed, S1 launch channel chosen

- **Д1 (owner, 00:54) executed as the zeroth move — it had in fact been started before it arrived.** Commits: `01c41736` (mandate, S1 brief, journal, KARTA registration) · `b0adaa12` (kurs-puti-i-volny, 13 paths) · `07a677d8` (LEKCIYA-v2 headers) · `bab8789c` (catalan/kartoteka registration) · `8c5b4c80` (mandate with Д1, VYGRUZKA-2026-09-19). All pushed. Criterion: `git_zona.py check` ✅ on `kurs-puti-i-volny`, on the arc, on `obzory/funkciya-putey-i-ee-uravneniya`; whole tree «вне git» **49 → 23**, drop 26 ≥ 21. The 23 left are foreign and untouched: `_fond` 11, `diskmat-57` 9, `ucheniki` 2, `_illustracii` 1. ЦЕНА: 5 commits, ≈4k head tokens; the risk removed was the whole input of the wave (one `git clean` away from zero).
- 🔴 **Tool refusal, repaired:** `git_zona.py commit` refused (`GIT_ZONA_REPO` not set, tool lives in another repo) and printed rc=0 while doing NOTHING. ЦЕНА: 1 extra call; a head reading rc alone would have logged a commit that did not happen. Repair: `export GIT_ZONA_REPO="$PWD"` in every call; written into S1 ПРАВКА 1 item 3 so the executor does not pay it again.
- 🔴 **Free channel refused for S1, by construction, not by the pool:** `orkestr.py --rezhim progon --suho` found 3 live free models (inkling-small, inkling, codestral) and still failed: «в стартовой команде 0 вхождений `--model`». S1 was assembled with `--kanal app` — its start block is a paste-in prompt, not a command. `dirizher.py` is also unfit here: its launch prompt and worktrees assume a local `main`, and this repo has none (`git log main` → unknown revision; the main line is `arka/mat-kostyak`). ЦЕНА: the free door costs 0 tokens and S1 cannot use it; S1 goes to a Claude Code subagent on **Haiku 4.5** (small model, mandate item F6) instead of the brief's Sonnet 5. Consequence for S2/S3: their briefs are built by the head with `--kanal terminal --dvizhok opencode` so they CAN run free.
- **S1 ПРАВКА 1** written before launch (model, place, no worktree, reading method under 220k, commit rhythm, owner's 19.09 course shape for the successor file); `check_zahod.py` rc=0.
- **Head's own counter:** 15 000 000 − 14 805 373 ≈ **195k** consumed. 
- **ГОЛОВА О СЕБЕ:** spent ≈25k tokens reading conductor/runner internals to learn that neither fits this repo (no `main`). ЦЕНА: 25k of the head's 400k; the next head should run `orkestr.py --suho` FIRST — one call answers «can this brief go free?».
