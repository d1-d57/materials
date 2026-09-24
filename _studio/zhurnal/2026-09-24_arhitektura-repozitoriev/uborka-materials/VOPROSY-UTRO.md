# VOPROSY-UTRO — morning questions to the owner (pass uborka-materials)

One line per object: `<object> — <what it is> — PROPOSED: <default action> — because <reason>`. Answer "yes" to accept the proposal. Every object here is saved and untouched.

- `~/Documents/GitHub/materials/carshering/carsharing_archive_backup_2026-06-25/` — a 29-entry backup folder made on 2026-06-25 before the carsharing structure migration; not a git repo of its own — PROPOSED: move to Trash — because it is the flat pre-migration copy of the same study, whose migrated version with full git history is now on GitHub as `d1-d57/arhiv-carsharing-issledovanie` (I did not diff the two file by file).
- `materials` branch `zahod/perepis-diska` — the disk census pass (accepted by the analyst), 16 commits ahead of `arka/mat-kostyak`, merges clean — PROPOSED: merge it into `arka/mat-kostyak` in the daytime together with the analyst branch `claude/bold-faraday-wq09ql` (which already contains it) — because tonight's merge would have moved HEAD of your main checkout, which holds your uncommitted work.
- `materials` branches `zahod/uborka-pered-pauzoj`, `zahod/dovodka-fazy-intervyu` — both fully inside the trunk; `git_zona.py zakryt-vetku` refused because an older tombstone with the same name already exists — PROPOSED: leave them — because they cost nothing and the tool guards the older tombstone on purpose.
