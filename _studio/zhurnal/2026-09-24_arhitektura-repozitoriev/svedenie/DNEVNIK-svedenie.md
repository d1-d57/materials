# DNEVNIK — svedenie

## 2026-09-25 10:41 — step 0: entry snapshot
- **done:**
```
$ git branch --no-merged origin/claude/bold-faraday-wq09ql | grep -c zahod/
0
$ git status --porcelain | wc -l  (per repo, before step 1)
materials arka/mat-kostyak 147
disciplina main 206
ankety main 1
matema-fest main 1
matproekty-179 zahod/nepodtverzhdennye 9
spetsmat-bot main 8
vanya main 11
$ local branches (git for-each-ref refs/heads | wc -l), before
materials 11
disciplina 70
ankety 1
matema-fest 1
matproekty-179 2
spetsmat-bot 62
vanya 1
arhiv-london-avgust-2026 2
matemdigest-map 3
sayt-sistemy-konstantinova 2
moskva 1
```
- **next:** step 1, conservation, starting with materials.
- **surprise:** materials and matema-fest are PUBLIC repos; matproekty-179 is on zahod/nepodtverzhdennye, not main.
- **question:** none.

## 2026-09-25 10:43 — step 1: conservation, materials
- **done:** 7 commits on `arka/mat-kostyak` (_fond 18 · _studio 14 · diskmat-57 91 · kurs-puti-i-volny 16 · ucheniki 22 · scratchpad 22 · служебное 1), pushed `42826e76..e4310e14`. `git -C materials status --porcelain | wc -l` → 0 (before 147). No secrets by pattern scan; no book-sized or >5 MB files. `kurs-puti-i-volny/istochniki/CHTO-VNUTRI.md` (6 KB note) committed, not moved: it is the folder's index, not a book.
- **next:** disciplina, then the five small repos; then close the open requests (13 open).
- **surprise:** none.
- **question:** none.

## 2026-09-25 10:45 — step 1: conservation, all seven
- **done:**
```
$ git -C <repo> status --porcelain | wc -l   (after; before in step 0)
materials 0
disciplina 1
ankety 0
matema-fest 0
matproekty-179 0
spetsmat-bot 0
vanya 0
```
  disciplina: 7 commits (`beea8ce5f..d71fe4afc`, pushed); two by the valve `git_zona.py commit --no-verify` over OLD `check_uroki` debt (ot-maksa 9e4a228a5, _studio/zhurnal d71fe4afc — 177 files, 162 of them in `_INFRA-git`); remainder 1 = `--help/` junk → VOPROSY #1. ankety 89460ac · matema-fest 25bfd37 · matproekty-179 eca5b4e · spetsmat-bot 4 commits → f8aac4e · vanya 2 commits → 348e3ad — all pushed, no rejection. matproekty-179: `main` and `zahod/nepodtverzhdennye` were the same commit (0233d36), so I switched the checkout to `main` (the trunk) and committed there. Open requests in materials: 13 closed + 2 auto-requests from my first valve attempt auto-closed by the tool → `zayavki`: open 0.
- **next:** step 2, the 22 branches.
- **surprise:** `zayavka-zakryt` returns rc=1 after moving the file to `sdelano/` (it tries `git add` on the ignored `zayavki/` dir) — the close itself happened (sdelano 76 → 89). A first valve attempt failed because my own earlier `add` had left 176 paths staged; unstaged and retried per group.
- **question:** none (VOPROSY #1 is for the owner).

## 2026-09-25 10:53 — step 2: merges and tombstones
- **done:** coverage of the 22 branches: checked 22 of 22 (script over `/tmp/svedenie/cands.txt` × `actions.tsv`). Merged 10: disciplina `kanaly-razvedka-sud-pochinka` f7bdc4743 · `korpus-pravil-i-rychagov` 94e5b3130 · `potolok-iz-mandata` 2e3be7eeb · `rol-subagenta-kontrakt` 723fc2e73 · `generator-rychaga` up to 33ebd512e → 374e825b0 (KARTA by trunk side; rychag fixture 28/28) · `zhivost-modeli-…` 6952cd5fa (patch already in trunk) · `sudya-ne-perepisyvaet-cheloveka` 01f252877 (union; orkestr fixture rc=0) — pushed `d71fe4afc..fc4661ba1`; spetsmat-bot `volna-b-server` 8efd677 (content already in main, merge diff empty) — pushed; materials `claude/bold-faraday-wq09ql` (carries `perepis-diska`, `uborka-materials`) a8fc2794 — pushed `e4310e14..d4d497f6`. Already merged before: `git-bez-zamkov`. Left 11, each with a reason in VOPROSY #3–#13. Tombstones: 93 local branches closed (`zakryt-vetku`); 39 fully-merged branches refused because a same-name tombstone exists → VOPROSY #2. Local branches now: materials 9 (was 11) · disciplina 39 (70) · spetsmat-bot 4 (62) · matproekty-179 1 (2).
- **next:** step 3, the 114 kept worktrees.
- **surprise:** in `materials` the door `vlit-v-osnovnuyu` targets `main` = the published site; it refused on the zone check, nothing merged, `main` = origin/main = c9257e84 unchanged. I used `git_zona.py merge` into the current `arka/mat-kostyak` instead → VOPROSY #14. Four conflict branches were judged by a read-only subagent («выдано 4 позиций из 4 найденных»).
- **question:** none for the analyst.

## 2026-09-25 10:57 — step 3: kept worktrees
- **done:** 114 of 114 rows of `kept-worktrees.tsv` have a `drop-worktree` row, verified yes. Method: `mv` to `~/.Trash/svedenie-2026-09-25-worktrees/<repo>-wt/<name>` + `git worktree prune` (12 GB now in the Trash; restore command in each row). Worktrees left: spetsmat-bot 2 (main + `/private/tmp/baseline-759ef40`), disciplina 1, matproekty-179 1. 46 of them held non-ignored changes; each was dropped only after its non-ignored tree equalled its `origin/park/…` snapshot tree → VOPROSY #17.
- **next:** step 4, default branch of materials.
- **surprise:** premise of step 3 only partly true (46 dirty, all saved in park). My own slip: I moved `disciplina-wt/` to the Trash although it held a hidden `.logi-volny-10/`; moved it back within a minute, nothing lost → VOPROSY #15.
- **question:** none.

## 2026-09-25 10:58 — step 4: default branch of materials
- **done:** `gh api repos/d1-d57/materials/pages` → `build_type: workflow, source.branch: main`; `.github/workflows/hugo.yml` on `main` and on `arka/mat-kostyak`: `on: push: branches: ["main"]` + `workflow_dispatch`; environment `github-pages` deploy policy = branches `main`, `gh-pages` only. So publishing does not depend on the default branch. Ran `gh repo edit d1-d57/materials --default-branch arka/mat-kostyak` rc=0; `gh repo view … --json defaultBranchRef` → `arka/mat-kostyak`; Pages status after: `built`.
- **next:** step 5, the verifier subagent.
- **surprise:** none.
- **question:** none.

## 2026-09-25 11:21 — step 5: verifier
- **done:** separate subagent, method = GitHub side (`fetch`/`ls-remote`): merges 11/11, step-1 commits 23/23, tombstones 93/93, dropped worktrees 114/114 (46/46 park trees equal), trunks pushed 7/7, materials `main` unchanged (c9257e84, 2026-09-14), default branch ok → `checked 250 of 250, 0 failures`; answer ended «выдано 250 позиций из 250 найденных». Correction of my step-2 entry: the `sudya-ne-perepisyvaet-cheloveka` tombstone had been refused too (same-name tombstone), so same-name refusals are 40, not 39; tombstones 93.
- **next:** step 6 report, then merge `zahod/svedenie` into `arka/mat-kostyak`.
- **surprise:** tombstone tags `mogila/*` are local only (none on GitHub); no data depends on them — all 93 tips are in the trunks.
- **question:** none.
