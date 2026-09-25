# REPORT — chistka-github

## GITHUB AFTER THE CLEANUP

1. Branches on GitHub: **868 → 19**, and no work was lost. Every deleted branch was checked by an independent verifier, which ended with `checked 849 of 849, 0 failures`.
2. materials 76 → 5: `arka/mat-kostyak` (trunk), `main` (the published site), `claude/bold-faraday-wq09ql` (the analyst's branch), `zahod/chistka-github` (this pass), `zahod/vid-blokov-vnedrenie` (a paused draft that needs your decision, VOPROSY 3).
3. disciplina 627 → 2: `main` (trunk), `zahod/generator-rychaga` (holds only rescue backups; only 5 days old, so it waits for you, VOPROSY 4).
4. spetsmat-179 136 → 1, matproekty-179 9 → 1, ankety 3 → 1, moskva 2 → 1, matema-fest 2 → 1, sayt-sistemy-konstantinova 4 → 1, matproekty-179-stranica 1 → 1: only the trunk `main` remains.
5. digest 3 → 3: `main`, `rabota`, `zahod/stil-noch`. These are your two separate lines, kept until the repository is split.
6. arhiv-london-avgust-2026 5 → 2: `main` and `pages` (the Pages branch).
7. **217 tags `arhiv/<old branch name>` were created**, one for every park branch and every closed unfinished branch: materials 11, disciplina 169, spetsmat-179 34, matproekty-179 1, ankety 1, matema-fest 1. To see them: `git tag -l 'arhiv/*'` after `git fetch --tags`.
8. To bring a branch back: `actions.tsv` holds the exact command for every row (`git push origin <tip>:refs/heads/<branch>`).
9. Merged: sayt-sistemy-konstantinova `tagging` → `main` (merge commit 014d18a, clean, pushed). This pass's own branch is merged into `arka/mat-kostyak`.
10. On this Mac: 40 local branches that were fully merged were removed (`local.tsv`). `disciplina-wt/`, `matproekty-179-wt/` and `disciplina/--help/` went to the Trash. The stray worktree `/private/tmp/baseline-759ef40` was removed; its commit is in `main` on GitHub.
11. Left for later: the two kept branches above (VOPROSY 3–4), plus two fixes to the brief generator (VOPROSY 1–2). `vanya` was not touched.

## Numbers and how they were measured

| repo | before | delete (merged) | tag+delete | keep | after (live `ls-remote --heads`) | live `arhiv/*` tags |
|---|---|---|---|---|---|---|
| materials | 76 | 60 | 11 | 5 | 5 | 11 |
| disciplina | 627 | 456 | 169 | 2 | 2 | 169 |
| spetsmat-179 | 136 | 101 | 34 | 1 | 1 | 34 |
| matproekty-179 | 9 | 7 | 1 | 1 | 1 | 1 |
| matproekty-179-stranica | 1 | 0 | 0 | 1 | 1 | 0 |
| ankety | 3 | 1 | 1 | 1 | 1 | 1 |
| moskva | 2 | 1 | 0 | 1 | 1 | 0 |
| matema-fest | 2 | 0 | 1 | 1 | 1 | 1 |
| digest | 3 | 0 | 0 | 3 | 3 | 0 |
| arhiv-london-avgust-2026 | 5 | 3 | 0 | 2 | 2 | 0 |
| sayt-sistemy-konstantinova | 4 | 3 | 0 | 1 | 1 | 0 |
| **total** | **868** | **632** | **217** | **19** | **19** | **217** |

- `before`: `git ls-remote --heads origin | wc -l` after `fetch --prune --tags` (`before.tsv`).
- Classes: `classes.tsv`. Actions, with the restore command on each row: `actions.tsv`. There are 868 rows, 868 of them unique, which covers every branch counted in `before.tsv`.
- The 208 park branches and 9 unfinished branches that were closed got tags (`tags.tsv`). Each tag was checked on GitHub against the branch's live tip before that branch was deleted.
- Deletions ran in 14 rounds, at most 50 per repository per round. Right before each push, the script checked again that the branch tip was unchanged and was reachable either from the trunk on GitHub or from its tag on GitHub. After every round, a separate verifier subagent re-checked all deletions so far with its own script (`verifier.md`). K was 0 after every round.
- Closed unfinished branches (tag+delete):
  - Named by the brief: disciplina `zahod/byudzhety-i-rashod`, `zahod/roli-i-dver-brifa`, `zahod/dobor-s-mesta`, `zahod/git-zona-zona-shire-kontrakta`, `zahod/snimok-nazyvaet-avtora`; spetsmat `zahod/B1-v14-vid`.
  - Judged old and superseded: materials `arka/vneshnie-istorii` (the trunk carries its arc further), disciplina `zahod/git-odna-dver` (the single git door has had 86 trunk commits since), spetsmat `zahod/nadzor-zvonit` (all 3 of its files are in the trunk).
