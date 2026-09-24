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
