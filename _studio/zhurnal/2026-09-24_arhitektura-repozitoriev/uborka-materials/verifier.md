# Verifier log — step F

Independent, read-only verification that every `tombstone` / `drop-worktree` / `move` row in `actions.tsv` is safe: the object's last commit is present on GitHub (an ancestor of, or equal to, the remote sha named in `saved_ref`), and — for worktree/move rows — that the local path is actually gone.

## Batch 1 — 2026-09-25 01:53

**Input snapshot:** `actions.tsv` was being actively appended to by a concurrent process while this batch ran (grew from 75 to 124 data rows between 01:45 and 01:53, all of the new rows being step-B `push` rows for the `disciplina` repo). To keep M well-defined, a frozen copy was taken at **2026-09-25 01:53:33** and saved to `/tmp/uborka/verify/actions_snapshot.tsv` (124 data rows); all checks in this batch ran against that snapshot. The set of `tombstone`/`drop-worktree`/`move` rows was unchanged by the later appends (still 37).

**Script:** `/tmp/uborka/verify/verify.py` (python3, no arguments). Method per row kind, exactly per the verifier mandate:
- `tombstone`: parsed `<repo>#<branch>` from `object`, 40-hex last commit from `note`, remote branch from `saved_ref`; ran `git -C <repo> ls-remote origin refs/heads/<ref>` then `git -C <repo> merge-base --is-ancestor <last> <remote_sha>`.
- `drop-worktree`: parsed main repo from `git -C <path>` in `restore`, resolved the 12-hex `HEAD` in `note` via `git rev-parse`, checked ancestry against `saved_ref`'s remote branch the same way; additionally confirmed the worktree path no longer exists on disk and is absent from `git -C <main> worktree list`.
- `move` (repo relocation, e.g. rows for `spetsmat_db`, `london-avgust-2026`, `carsharing_archive`): read NEW path from `restore`'s `mv <NEW> <OLD>`, compared every `git for-each-ref refs/heads` sha at NEW against `git ls-remote --heads origin`, and confirmed OLD no longer exists.
- `move` (empty-folder-to-Trash rows, `saved_ref` = `-`, note "empty folder"): confirmed the Trash path from `restore` exists and is an empty directory.

Sanity check of the ancestry logic itself: ran `git merge-base --is-ancestor` in `materials` with a deliberately unrelated commit (tip of `origin/main`) against the `arka/mat-kostyak` remote sha — it correctly failed (exit 1), confirming the check is discriminating, not trivially passing.

### Failures

None.

### Counts per action kind

| action | checked | failures |
|---|---|---|
| tombstone | 14 | 0 |
| drop-worktree | 16 | 0 |
| move | 7 | 0 |

checked 37 of 37 removals, 0 failures
