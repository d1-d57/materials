# REPORT — pass uborka-materials (night of 2026-09-25)

## THE WORLD THIS MORNING

1. **Disk:** `~/Documents/GitHub` was **66 GB**, now **17 GB** (`du -sh ~/Documents/GitHub`, before and after). The space came from removing 225 working copies (worktrees) whose work is all on GitHub.
2. **Three projects that existed only on this Mac are now private repositories on GitHub**, each with a card `KARTOCHKA.md`:
   - Konstantinov-system site → **github.com/d1-d57/sayt-sistemy-konstantinova**; the folder moved from `~/Documents/GitHub/spetsmat/spetsmat_db` to **`~/Documents/GitHub/sayt-sistemy-konstantinova`** (everything inside, including the database file, moved with it).
   - London guide → **github.com/d1-d57/arhiv-london-avgust-2026**; folder renamed to **`~/Documents/GitHub/arhiv-london-avgust-2026`**.
   - Carsharing study → **github.com/d1-d57/arhiv-carsharing-issledovanie**; the folder `materials/carshering/carsharing_archive` is in the **Trash** as `carsharing_archive-2026-09-25` (you decided to remove it from the disk; do not empty the Trash before you are happy).
3. **Your unfinished work is untouched.** `materials` (147 changed files) and `disciplina` (206) look exactly as they did last night; a copy of the `materials` changes is also saved on GitHub as the branch `park/2026-09-25/materials-main`.
4. **Working copies:** of 339 extra working copies, 225 were removed (all work saved on GitHub first, checked twice by a separate verifier). **114 were kept** because they hold local files git does not track (bot databases, scratch folders) — they are listed in `kept-worktrees.tsv`, and the question is in `VOPROSY-UTRO.md`.
5. **Branches:** 175 local branches whose work is already in the main line were closed (each leaves a tombstone tag and can be revived). All other local branches were pushed to GitHub. Every branch is laid out in `branches-<repo>.tsv` with a proposal (merge / conflict / stale).
6. **Merges:** one — the accepted pass `zahod/git-bez-zamkov` into `disciplina/main` (its content was already there; this only closes the history). Nothing was merged into `materials`; nothing into any site.
7. **Nothing was deleted from GitHub.** New branches there: `park/2026-09-25/…` (snapshots of unsaved changes, 204 of them).
8. **What to do first:** open **`VOPROSY-UTRO.md`** (this folder) and answer the lines — most need only "yes". Then empty the Trash only if you agree with what is in it.
9. **Open arcs:** 35 arc folders have no "closed" banner — `arki-otkrytye.tsv` is the input for a later closing pass.
10. **Addresses:** all files of this pass are in `materials` branch `zahod/uborka-materials`, folder `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/uborka-materials/`.

## Counters (computed by `python3 /tmp/uborka/counters.py`)

```
Counter(action) over actions.tsv: {'card': 3, 'create-repo': 3, 'drop-worktree': 225, 'merge': 1, 'move': 16, 'park': 204, 'push': 131, 'skip': 163, 'tombstone': 175} — sum 921 = rows 921
by step: A/card=3, A/create-repo=3, A/move=3, A/push=2, B/push=12, B4/skip=6, B4/tombstone=14, B5/skip=2, C/drop-worktree=16, C/move=4, C/park=9, D/park=1, E2/drop-worktree=209, E2/park=193, E2/skip=114, E3-B2/park=1, E3-B2/push=117, E3-B4/skip=31, E3-B4/tombstone=161, E3-B5/merge=1, E3-B5/skip=6, E4/move=9, E4/skip=4
Counter(proposal) over branches-ankety.tsv: {'already-in-trunk': 2} — sum 2 = rows 2
Counter(proposal) over branches-arhiv-london-avgust-2026.tsv: {'already-in-trunk': 4, 'stale': 1} — sum 5 = rows 5
Counter(proposal) over branches-disciplina.tsv: {'already-in-trunk': 192, 'clean-merge-candidate': 6, 'conflict': 7} — sum 205 = rows 205
Counter(proposal) over branches-matema-fest.tsv: {'already-in-trunk': 1} — sum 1 = rows 1
Counter(proposal) over branches-matemdigest-map.tsv: {'already-in-trunk': 1, 'conflict': 2} — sum 3 = rows 3
Counter(proposal) over branches-materials.tsv: {'already-in-trunk': 21, 'clean-merge-candidate': 2, 'conflict': 1} — sum 24 = rows 24
Counter(proposal) over branches-matproekty-179-stranica.tsv: {'already-in-trunk': 1} — sum 1 = rows 1
Counter(proposal) over branches-matproekty-179.tsv: {'already-in-trunk': 5} — sum 5 = rows 5
Counter(proposal) over branches-moskva.tsv: {'already-in-trunk': 2} — sum 2 = rows 2
Counter(proposal) over branches-sayt-sistemy-konstantinova.tsv: {'already-in-trunk': 3, 'clean-merge-candidate': 1} — sum 4 = rows 4
Counter(proposal) over branches-spetsmat-bot.tsv: {'already-in-trunk': 76, 'conflict': 2} — sum 78 = rows 78
Counter(proposal) over branches-vanya.tsv: {'already-in-trunk': 1} — sum 1 = rows 1
```

## Coverage

- `branches-materials.tsv`: checked 24 of Y_b = 24 local branches.
- Worktrees of `materials-wt`: 16 of 16 (Y_w = 17 minus this pass's own) have a row (16 drop-worktree, 9 of them parked first).
- Worktree containers: disciplina-wt 226 of 226, spetsmat-bot-wt 94 of 94, matproekty-179-wt 2 of 2, matemdigest-map-wt 1 of 1 have a row (drop, park, or skip with reason). `not-reached: budget` — none.
- Verifier: see `verifier.md`, last line.
- `du -sh ~/Documents/GitHub`: before 66G, after 17G.

## Not done / out of scope, named
- Merges in `materials` (any merge into `arka/mat-kostyak` would move the HEAD of your main checkout, which step D forbids) — `zahod/perepis-diska` proposed for the daytime.
- 37 branches (materials 6, disciplina 29, spetsmat-bot 2) refused by `git_zona.py zakryt-vetku` because an older tombstone of the same name exists — left as they are.
- A `spetsmat-bot` worktree registered at `/private/tmp/baseline-759ef40` (detached) — outside the four containers, not touched.
- `~/Documents/GitHub/proba-dolg-nedostupnaya-fixture` (unreadable, census row R8) — not touched.
- `materials-wt/disciplina` is a symlink to `~/Documents/GitHub/disciplina` that tools rely on — kept.
