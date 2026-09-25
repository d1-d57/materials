# REPORT — pass svedenie (2026-09-25)

## WHAT CHANGED TODAY

1. **Old uncommitted work is committed and on GitHub**, in folder-sized commits: materials 7, disciplina 7, spetsmat-bot 4, vanya 2, ankety 1, matema-fest 1, matproekty-179 1 (23 commits). All seven checkouts are clean, except `disciplina/--help/` — a test artifact, not work (question 1) — and `vanya`, where another session started new work at 11:08, after my commit; I left it alone (question 18).
2. **Branches merged (10):** disciplina `kanaly-razvedka-sud-pochinka`, `korpus-pravil-i-rychagov`, `potolok-iz-mandata`, `rol-subagenta-kontrakt`, `generator-rychaga` (without its last commit of backup copies), `zhivost-modeli-dovozit-a-ne-otvechaet`, `sudya-ne-perepisyvaet-cheloveka`; spetsmat-bot `volna-b-server`; materials `zahod/perepis-diska` and `zahod/uborka-materials` (via the analyst's branch `claude/bold-faraday-wq09ql`, also merged). `git-bez-zamkov` was already merged.
3. **Branches left (11), one reason each:** `byudzhety-i-rashod` and `roli-i-dver-brifa` — you stopped them unfinished; `dobor-s-mesta` — clashes with a duplicate already merged; `git-zona-zona-shire-kontrakta` — its only change wipes its own brief; `snimok-nazyvaet-avtora` and spetsmat `B1-v14-vid` — main rejected them on purpose and did it differently; london `pages`, matemdigest `rabota` and `stil-noch` — separate histories; sayt `tagging` — 219 commits of its own line; materials `main` — the site, never merged.
4. **Local branches before → after:** disciplina 70 → 39 · spetsmat-bot 62 → 4 · materials 11 → 9 · matproekty-179 2 → 1 · others unchanged (ankety 1, matema-fest 1, vanya 1, arhiv-london 2, matemdigest-map 3, sayt 2, moskva 1). 93 merged branches got a tombstone; 40 more are fully merged but the tool refused them (a tombstone of the same name exists) — question 2.
5. **Worktrees removed: 114 of 114** (spetsmat-bot 74, disciplina 38, matproekty-179 2). They are in the Trash, `~/.Trash/svedenie-2026-09-25-worktrees/` (12 GB) — empty the Trash to free the space. 46 of them held real edits, not only ignored files; each was removed only after proving its edits are in its `park/…` branch on GitHub — so those 46 park branches are now the only copy (question 17).
6. **Default branch of `materials` on GitHub is now `arka/mat-kostyak`.** The site is untouched: it is built by a workflow on push to `main`.
7. **Next pass (deleting on GitHub) will find:** branches fully merged into the trunk — disciplina 456, spetsmat-bot 100, materials 60, matproekty-179 7, arhiv-london 3, sayt 2, ankety 1, moskva 1; park branches — disciplina 163, spetsmat-bot 33, materials 10, ankety 1, matproekty-179 1, vanya 1 (46 of the park branches must NOT go, see point 5).
8. **Zero loss:** an independent verifier subagent checked every action from GitHub's side — `checked 250 of 250, 0 failures` (`verifier.md`).

## Details

- Log: `DNEVNIK-svedenie.md`; every action with its restore command: `actions.tsv`; questions: `VOPROSY.md`; independent check: `verifier.md`.
- A trap found on the way: in `materials`, `git_zona.py vlit-v-osnovnuyu` treats `main` (the site) as the trunk. It refused on the zone check and merged nothing; I merged with `git_zona.py merge` into `arka/mat-kostyak` instead (question 14).
- My own slip: I moved `disciplina-wt/` to the Trash although it held a hidden log folder; moved it back at once, nothing lost.
