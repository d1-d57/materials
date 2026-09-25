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
