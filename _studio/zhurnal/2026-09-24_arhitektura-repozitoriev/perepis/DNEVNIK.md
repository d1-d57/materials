# Running log of the census pass kod_perepis-diska

Newest entry at the bottom. Times come from `date`. Each number is followed by the command that measured it.

## 2026-09-25 00:27 — before ПРАВКА 1: done (retroactive entry)
- **done:** Retroactive, written after ПРАВКА 1 was read. The whole census was done under the old edition of the brief, so there are no start/end entries per root. Timestamps come from `git log --format='%h %ci'`:
  - plan and Y = 352 at 00:14 (`6e01325c`), where Y = `find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l`;
  - two full script runs, R1–R5 in one process;
  - six files at 00:26 (`b6c409b5`), first push at that point;
  - queue items at 00:27 (`3e2afe3a`).
  
  Coverage is 352 of 352 (`awk -F'\t' 'NR>1' perepis/repos.tsv | wc -l`), with 0 porcelain mismatches (`awk -F'\t' 'NR>1 && $8!=$9' perepis/repos.tsv | wc -l`).
- **next:** fill `## ОТЧЁТ`, run the hygiene block, push after every commit.
- **surprise:** ПРАВКА 1 arrived after the census was finished, so its criterion "≥10 entries with start/end for each root" cannot be met honestly. I did not invent the missing entries.
- **question:** is one retroactive entry plus the entries from now on enough to count? My choice: yes, per the correction's own "ничего не переделывай" clause.

## 2026-09-25 00:28 — report written, delivery
- **done:** `## ОТЧЁТ` and the entry snapshot are filled, and the script is attached (`fa5488e8`, pushed). Checks: `git_zona.py check --zone` on both zone paths → ✅; `bootstrap_zahod.py --proverit-doma` → rc=0; `ls perepis/ | wc -l` → 7.
- **next:** the analyst's acceptance. No merge and no `worktree drop` (§2.6).
- **surprise:** none. Checked for new corrections with `git show origin/claude/bold-faraday-wq09ql:…kod_perepis-diska.md | grep '^### ПРАВКА'`: only ПРАВКА 1.
- **question:** none.
