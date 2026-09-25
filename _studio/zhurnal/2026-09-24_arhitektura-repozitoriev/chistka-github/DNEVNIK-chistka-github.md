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
