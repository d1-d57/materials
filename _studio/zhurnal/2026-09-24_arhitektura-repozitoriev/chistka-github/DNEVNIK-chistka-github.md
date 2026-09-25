# DNEVNIK — chistka-github

Channel with the analyst for the pass `kod_chistka-github.md`. Entry form: `## <date> — <step>` + **done** · **next** · **surprise** · **question**.

## 2026-09-25 11:41 — step 0: git contour and plan

- **done:** worktree `materials-wt/chistka-github` on `zahod/chistka-github` (from `origin/claude/bold-faraday-wq09ql` 4491b7e5). Entry snapshot: unmerged `zahod/*` vs `origin/claude/bold-faraday-wq09ql` = 0 (only unmerged local branch: `main`); `status --porcelain` 0; unpushed 0; open requests 0. `git_zona.py check --zone chistka-github/` rc=0 (zone did not exist yet). Plan written to `## ПЛАН`. Corrections watcher started in the background.
- **next:** step 1 — fetch/prune every repository with more than one branch and write `before.tsv`.
- **surprise:** the §0.1 command `git branch --no-merged claude/bold-faraday-wq09ql` fails in the worktree (`malformed object name`, no local branch of that name) and `grep -c` turns the failure into a false `0`. I use `origin/claude/bold-faraday-wq09ql`.
- **question:** none.

## 2026-09-25 11:42 — step 1: measure

- **done:** `git fetch --prune --tags origin` in 11 main checkouts, all rc=0. `before.tsv`: materials 76, disciplina 627, spetsmat-179 136, matproekty-179 9, matproekty-179-stranica 1, ankety 3, moskva 2, matema-fest 2, digest 3, arhiv-london-avgust-2026 5, sayt-sistemy-konstantinova 4 — total 868 (`awk -F'\t' 'NR>1{s+=$2}END{print s}' before.tsv`). Trunks from `ls-remote --symref origin HEAD`: materials `arka/mat-kostyak`, all others `main`.
- **next:** step 2 — classify all 868 branches.
- **surprise:** `matproekty-179-stranica` (remote `d1-d57/projects`) has only 1 branch, so nothing to clean there; kept in the table for coverage.
- **question:** none.

## 2026-09-25 11:44 — step 2 + step 6 judgement: classify

- **done:** `/tmp/chistka/step2_classify.py` (tips from `ls-remote`, `merge-base --is-ancestor tip origin/<trunk>`) → `classes.tsv`, 868 rows = 868 in `before.tsv`: merged 631, park 208, unmerged 13, keep-trunk 11, keep-named 5, missing objects 0. Unmerged judged: tag+delete 9 (6 named by the brief + vneshnie-istorii, git-odna-dver, nadzor-zvonit as old and superseded), keep 3 (own branch, vid-blokov-vnedrenie, generator-rychaga), merge 1 (sayt tagging).
- **next:** step 3 — merge sayt `tagging` into `main`.
- **surprise:** park count is 208, not 209; disciplina `zahod/git-bez-zamkov` (q3) is already class merged.
- **question:** none (two keep proposals in VOPROSY 3–4).

## 2026-09-25 11:45 — step 3: sayt tagging → main

- **done:** in a temporary worktree of `main` (`/tmp/chistka/sayt-main`, plan D2; the owner's checkout stays on `tagging`): `git merge --no-ff tagging -m "влита ветка tagging (решение владельца 25.09)"` rc=0, no conflict; `git push origin main` 60a0e7d..014d18a rc=0. Criterion 6: `git merge-base --is-ancestor 35f31bf1f origin/main` rc=0. Temp worktree removed. `tagging` reclassified as merged in `classes.tsv`.
- **next:** step 4 — tags `arhiv/*` for 208 park + 9 closed unmerged branches.
- **surprise:** none.
- **question:** none.

## 2026-09-25 11:46 — step 4: arhiv tags

- **done:** `/tmp/chistka/step4_tags.py`: 217 lightweight tags `arhiv/<branch>` at the live tip (re-read by `ls-remote --heads` right before tagging), pushed in chunks of ≤50, verified by `git ls-remote --tags origin 'refs/tags/arhiv/*'`: 217 of 217 verified (materials 11, disciplina 169, spetsmat-179 34, matproekty-179 1, ankety 1, matema-fest 1); pre-existing conflicting tags 0; tips changed since classification 0. Table: `tags.tsv`.
- **next:** step 5 — delete in batches of ≤50 per repository, verifier subagent after each round.
- **surprise:** none.
- **question:** none.

## 2026-09-25 11:48 — step 5, round 1 (pilot): ankety

- **done:** `/tmp/chistka/step5_delete.py ankety`: 2 deleted (1 merged, 1 park via verified tag); guard re-checked right before the push. Verifier subagent (own script `/tmp/chistka/verifier/verify.py`): `checked 2 of 2, 0 failures`.
- **next:** rounds over all repositories, ≤50 per repo per round, verifier after each round.
- **surprise:** none.
- **question:** none.

## 2026-09-25 11:54 — step 5, round 2: all repositories

- **done:** 166 deleted (73 merged, 93 via verified tag): materials 50, disciplina 50, spetsmat-179 50, matproekty-179 8, moskva 1, matema-fest 1, arhiv-london 3, sayt 3. Verifier: `checked 168 of 168, 0 failures`. Small repos finished.
- **next:** round 3 onward — remaining disciplina 575, spetsmat-179 85, materials 21.
- **surprise:** none.
- **question:** none.

## 2026-09-25 12:03 — step 5, round 3

- **done:** 121 deleted (materials 21 — finished, disciplina 50, spetsmat-179 50). Verifier: `checked 289 of 289, 0 failures`.
- **next:** round 4 — remaining disciplina 525, spetsmat-179 35.
- **surprise:** the verifier run took 13 min (fetch of disciplina tags); rounds continue.
- **question:** none.

## 2026-09-25 12:13 — step 5, round 4

- **done:** 85 deleted (disciplina 50, spetsmat-179 35 — finished). Verifier: `checked 374 of 374, 0 failures`.
- **next:** rounds 5+ — disciplina only, 475 remaining.
- **surprise:** verifier runs take 14–24 min (per-row GitHub calls); asked it to read GitHub once per repo.
- **question:** none.
