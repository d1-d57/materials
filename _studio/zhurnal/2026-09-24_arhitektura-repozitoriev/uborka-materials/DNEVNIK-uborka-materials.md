# DNEVNIK — pass uborka-materials

Running log of the night pass. Entry form: date — step; done · next · surprise · question.

## 2026-09-25 01:40 — start (§0.1 git contour)
- **done:** worktree `materials-wt/uborka-materials` on `zahod/uborka-materials` from `origin/claude/bold-faraday-wq09ql` (23fe54df). `git branch --no-merged origin/claude/bold-faraday-wq09ql | grep -c zahod/` → 0. `git_zona.py check --zone uborka-materials/` → rc=0 (zone did not exist yet). `gh auth status` → logged in as d1-d57, scopes repo. Baselines: materials main checkout `status --porcelain | wc -l` = 147; Y_b = 24; Y_w = 17 (16 besides this pass's own worktree). Correction watcher started in background.
- **next:** step A (three disk-only repositories).
- **surprise:** `schet_nezakrytogo.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev` run from this worktree printed "no file fell into the area" — no counts taken (it probably resolves the materials root, not the worktree). `london-avgust-2026` is not quite disk-only: it has a remote `publikacia` → d1-d57/bzzaawyodp (unrelated history, per its last commit message).
- **question:** none.

## 2026-09-25 01:45 — step A (three disk-only repositories)
- **done:** 3 private repos created (`gh repo create`), all local branches pushed and verified hash-for-hash (`for-each-ref refs/heads` vs `ls-remote --heads origin`): sayt-sistemy-konstantinova 4/4, arhiv-london-avgust-2026 5/5, arhiv-carsharing-issledovanie 1/1. Dirt saved first as "archive snapshot" commits (spetsmat_db bf12848, carsharing 2391666), no files >5 MB. KARTOCHKA.md committed and pushed in each (spetsmat_db: on `tagging` = its HEAD, and on `main` = GitHub default via temp index). Moves: spetsmat/spetsmat_db → GitHub/sayt-sistemy-konstantinova; london-avgust-2026 → arhiv-london-avgust-2026; carsharing_archive → ~/.Trash/carsharing_archive-2026-09-25. materials porcelain still 147. 11 rows in actions.tsv.
- **next:** step B (materials branches).
- **surprise:** ssh to GitHub fails ("Host key verification failed"), so origin uses https (gh credential helper) instead of git@github.com. carsharing_archive had a stale empty `.git/index.lock` from 2026-07-10 — moved aside to /tmp/uborka/, not deleted. Old-path mentions are text only (docs and code comments), none is a live import; listed in actions.tsv notes, not edited.
- **question:** carsharing_archive_backup_2026-06-25 → VOPROSY-UTRO.md.

## 2026-09-25 01:47 — step B (materials branches)
- **done:** `fetch --prune`; Y_b = 24. B2: 12 branches pushed (not on origin or ahead), 0 parked, 0 failed (`/tmp/uborka/branches.py … --push`). B3: `branches-materials.tsv` 24 rows = Y_b; proposals: already-in-trunk 21, clean-merge-candidate 2 (zahod/perepis-diska, this pass's own branch), conflict 1 (main). B4: 4 branches closed with tombstones (arka/katalog-kursa, zahod/graf-korpusa, zahod/konsolidaciya-korpusa, zahod/proba-podnyat-volnu-samotest); 2 refused by the tool (tombstone already exists) → skip; 13 in-trunk branches are still checked out in worktrees → B4 again after step C. B5: 0 merges.
- **next:** step C (materials-wt worktrees), then B4 for the branches it frees, then step F verifier.
- **surprise:** any B5 merge into `arka/mat-kostyak` would move HEAD of the main checkout (it has that branch checked out), which step D forbids — so in `materials` B5 cannot happen tonight at all. `zahod/perepis-diska` also fails (b) on the letter.
- **question:** 2 lines added to VOPROSY-UTRO.md.

## 2026-09-25 01:50 — step C (materials-wt worktrees) + B4 round 2
- **done:** `/tmp/uborka/wt.py <materials> <materials-wt/> C`: 16 of 16 other worktrees handled — 9 dirty ones parked to `park/2026-09-25/wt-<name>` (verified by `ls-remote`), all 16 dropped via `git_zona.py worktree drop <path> --force` after the HEAD/park ref was verified on GitHub; porcelain of every tree equal before/after park. 0 kept for local-only files. 4 empty folders in materials-wt (sajt-kursa-wt, slajdy-media-wt, sloi-i-obrez-wt, vlitie-i-vitrina-kursa-wt) moved to Trash. B4 round 2: 10 more in-trunk branches tombstoned; 4 refused (zahod/chistka-hvostov, dobivka-dolgov, vlit-i-uspokoitsya, vlitie-i-vitrina-kursa — tool refusal, see actions.tsv). materials main porcelain still 147.
- **next:** step F verifier on all removals so far (A, B4, C) in background; step D meanwhile (snapshot only, no removal).
- **surprise:** `materials-wt/disciplina` is a symlink to `~/Documents/GitHub/disciplina` (it makes `../disciplina` resolve from inside a materials worktree) — left in place.
- **question:** none.

## 2026-09-25 01:51 — step D (materials main checkout) + E1 (hooks)
- **done:** D: snapshot parked with a temp index (§2.3) as 62dda697 → `origin/park/2026-09-25/materials-main` (`ls-remote` prints it). Porcelain before D = 147, after D = 147; HEAD unchanged; index file md5 identical before/after. 0 files >5 MB. The snapshot differs from HEAD by 184 files (+25854/−310). E1: `hooks.tsv` — 13 rows (12 main checkouts + carsharing in Trash), `git config --get core.hooksPath`.
- **next:** wait for the verifier of batch 1, then E2 (worktree containers), E3 (branches of the other repos).
- **surprise:** in zsh `"$C:refs/..."` is the `:r` modifier — the first push of the park failed with a mangled refspec; fixed with `${C}`. Nothing else was affected (the worktree script is Python).
- **question:** none.

## 2026-09-25 01:57 — E3 (branches of 11 repos, save + layout), G1, E4; E2 running
- **done:** E3 B2/B3: `branches.py` over 11 repos, trunk = `origin/HEAD` (all `origin/main`): pushed 117 branches (disciplina 72, spetsmat-bot 42, ankety 1, matemdigest-map 1, matproekty-179 1), parked 1 (spetsmat-bot, non-fast-forward), failed 0; tables `branches-<repo>.tsv`. matemdigest-map: 2 branches have histories unrelated to main → proposal `conflict` (merge_dry_run `conflict:unrelated-histories`). Verifier batch 1: `checked 37 of 37 removals, 0 failures`. G1: `arki-otkrytye.tsv` — 61 arc folders, 35 without the `АРКА ЗАКРЫТА` banner (materials 19, disciplina 16). E4: ankety-wt, moskva-wt empty → Trash; 4 owner-content objects → VOPROSY-UTRO.md.
- **next:** E2 finishes (spetsmat-bot-wt, disciplina-wt) → verifier batch 2 → E3 B4/B5 → G2 report.
- **surprise:** the census's "52 loose .md in spetsmat-bot-wt" are not loose: `find spetsmat-bot-wt -maxdepth 1 -type f` → 0; they are READMEs inside worktrees plus one non-git folder `etalon-raspil/` (55 files). Many spetsmat-bot worktrees hold git-ignored databases (`data/*.db`, `-wal`, `-shm`) and `secrets/` — those worktrees are saved but kept (plan rule), not dropped.
- **question:** none new for the analyst.

## 2026-09-25 02:13 — step E2 (worktree containers) + E3 B5 (merges)
- **done:** E2 (`/tmp/uborka/wt.py` per container): matemdigest-map-wt 1/1 dropped; matproekty-179-wt 2/2 saved but kept (ignored `poster/fonts/`, `poster/out/`, `scratchpad/…`); spetsmat-bot-wt 94: 31 parked, 20 dropped, 74 kept (ignored databases `data/*.db`, `secrets/`); disciplina-wt 226: 162 parked, 188 dropped, 38 kept (ignored `scratchpad/<name>/` folders). Every worktree has a row. 7 empty unregistered folders (6 in disciplina-wt, the emptied matemdigest-map-wt) → Trash. E3 B5: `zahod/git-bez-zamkov` merged into disciplina `main` by `git_zona.py vlit-v-osnovnuyu` (beea8ce5f, pushed fast-forward; the merge result tree equals the old main tree — the content had already been adopted); `zahod/kanaly-razvedka-sud-pochinka` refused (its worktree is alive — kept in E2); 4 other disciplina candidates and spetsmat's `tagging` fail condition (b). disciplina main checkout porcelain 206 before = 206 after.
- **next:** verifier batch 2 (running) → B4 tombstones in 11 repos (192 candidates, dry run) → verifier batch 3 → G2 report.
- **surprise:** `vlit-v-osnovnuyu` committed its own incident autolog (08f19aa0d) before the merge — the tool's standard behaviour, now on origin/main too. Action kind `merge` is not in the action list of §2.1; I used `merge` for that one row.
- **question:** 114 kept worktrees → grouped lines in VOPROSY-UTRO.md (after the verifier).
