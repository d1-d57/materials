# Disk census of the owner's Mac, 2026-09-25 (pass kod_perepis-diska)

This is a read-only census. Nothing was committed, pushed, deleted, moved or stashed outside this zone. The five TSV files next to this report hold the raw rows. Every number below comes from them or from a command named here.

Terms used below:
- **tree**: a git working tree. It is either a **main checkout** (it has a `.git` directory) or a **linked worktree** (it has a `.git` file).
- **repository**: one git object store. A main checkout and all of its worktrees share one repository.
- **funnel rule**: the one mass-action class assigned to each row (the codes are in §2).
- **default**: `origin/<default_branch>`, taken from `origin/HEAD` after `git fetch --prune origin`.

## 1. Census summary

**Coverage: checked 352 of 352.** Y = `find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l` = 352 (13 main checkouts + 339 linked worktrees). `repos.tsv` has 352 data rows. `find` also prints `Permission denied` on `~/Documents/GitHub/proba-dolg-nedostupnaya-fixture`. That folder cannot be read, adds nothing to Y, and is row `R8-unclear` in `folders.tsv`.

**Nothing changed: 0 rows** with `porcelain_before != porcelain_after`: `awk -F'\t' 'NR>1 && $8!=$9' repos.tsv | wc -l` → 0. Two full runs of the script both gave 0.

| file | data rows |
|---|---|
| `repos.tsv` | 352 |
| `branches.tsv` | 331 (local branches of the 13 main checkouts) |
| `folders.tsv` | 28 |
| `sessions.tsv` | 426 (Claude Code project folders; 2602 `*.jsonl` in total) |
| `big-files.tsv` | 100 (out of 6556 files over 1 MB) |

**Roots.**
- R1 `~/Documents/GitHub` holds 65 GB (`du -sh`). **52 GB of that is `disciplina-wt/`** (226 worktrees, about 230 MB each). `spetsmat-bot-wt` holds 4.5 GB and `materials-wt` 4.6 GB.
- R2 `~/Documents` has 6 folders besides `GitHub`. The books folder is **`Книги`** (1707 MB, 683 files).
- R3 `~/Downloads` has 7 folders plus 38 loose files.
- R4: the home root holds 5 loose files. The Claude folder is `~/Claude` (44 files). No folder in `~/Documents` has "claude" in its name.
- R5 `~/.claude/projects` has 426 subfolders.

**Fetch.** 10 repositories fetched `ok`, 0 fetches failed, and 3 were skipped as `no-origin`.

**`origin_url=none`: 3 main checkouts:**
- `london-avgust-2026`: 30 commits, a standalone project.
- `materials/carshering/carsharing_archive`: a repository nested INSIDE `materials`.
- `spetsmat/spetsmat_db`: a repository nested inside the non-git folder `spetsmat`.

These three repositories exist only on this disk.

**Main checkouts (13):**

| main checkout | rule | dirty / untracked | HEAD branch | first → last commit | commits |
|---|---|---|---|---|---|
| ankety | R3-park | 1 / 0 | main | 08-29 → 09-20 | 20 |
| disciplina | R3-park | 36 / 170 | main | 08-06 → 09-24 | 7865 |
| london-avgust-2026 | R2-push (no origin) | 0 / 0 | main | 08-21 → 09-18 | 30 |
| matema-fest | R3-park | 0 / 1 | main | 06-06 → 09-17 | 14 |
| matemdigest-map | R2-push | 0 / 0 | rabota | 07-10 → 09-17 | 125 |
| materials | R3-park | 40 / 107 | arka/mat-kostyak | 06-13 → 09-24 | 1647 |
| materials/carshering/carsharing_archive | R3-park (no origin) | 5 / 1 | master | 06-25 → 06-25 | 6 |
| matproekty-179-stranica | R1-ok | 0 / 0 | main | 08-29 → 09-18 | 36 |
| matproekty-179 | R3-park | 5 / 4 | zahod/nepodtverzhdennye | 08-27 → 09-20 | 228 |
| moskva | R1-ok | 0 / 0 | main | 09-06 → 09-24 | 32 |
| spetsmat-bot | R3-park | 5 / 3 | main | 09-02 → 09-24 | 1662 |
| spetsmat/spetsmat_db | R3-park (no origin) | 0 / 1 | tagging | 06-16 → 06-26 | 330 |
| vanya | R3-park | 6 / 5 | main | 08-19 → 09-17 | 8 |

All dates are in 2026. The dates are HEAD history. All-refs spans are in §3.

**Branches (`branches.tsv`, 331 rows):**
- `in_default`: yes 226, no 95, n/a 10 (the 10 belong to the three no-origin repositories).
- `has_upstream`: yes 193, no 138.
- **57 branches are neither in the default nor pushed** (no upstream, or `ahead>0`). These 57 are the real "exists only on this disk" work in the branch dimension.

## 2. Funnel distribution

The rules are the analyst's R1–R8, first match wins. New codes that I propose: **R9**, **R10**, **R0-holder**, **R0-empty**. The interpretations were decided in `## ПЛАН` before the run.
- `R9-wt-done`: a clean worktree whose HEAD commit is already in the default. It can be removed and nothing is lost.
- `R10-wt-residue`: a worktree whose HEAD is in the default and whose ONLY dirt, judged by path names from `git status`, is untracked `scratchpad/` content and/or tool-generated files. The generated-file names are `*.log`, `MODELI-ZHIVOST.json`, `zamer-skillov.json`, `*/dist/*` and `docs/index.html`.
- `R0-holder`: a container folder in R1 that holds only worktrees.
- `R0-empty`: an empty folder.

**`repos.tsv`, column `funnel_rule` (with the proposed R9/R10):**
```
Counter(funnel_rule) = {'R1-ok': 9, 'R10-wt-residue': 44, 'R2-push': 22, 'R3-park': 167, 'R9-wt-done': 110}   sum=352 rows=352
  R1-ok            objects=   9  MB=    1567.9
  R10-wt-residue   objects=  44  MB=    5411.5
  R2-push          objects=  22  MB=    5150.6
  R3-park          objects= 167  MB=   35749.4
  R9-wt-done       objects= 110  MB=   13599.6
by kind: main R1-ok 2 · R2-push 2 · R3-park 9 | worktree R1-ok 7 · R2-push 20 · R3-park 158 · R9-wt-done 110 · R10-wt-residue 44
```

**`repos.tsv`, column `funnel_rule_strict` (the analyst's rules exactly, no new codes):**
```
Counter(funnel_rule_strict) = {'R1-ok': 119, 'R2-push': 22, 'R3-park': 211}   sum=352 rows=352
  R1-ok   objects= 119  MB= 15167.5
  R2-push objects=  22  MB=  5150.6
  R3-park objects= 211  MB= 41160.9
```

**`folders.tsv`:**
```
Counter(funnel_rule) = {'R0-empty': 2, 'R0-holder': 4, 'R5-norepo': 4, 'R6-books': 6, 'R7-junk': 6, 'R8-unclear': 6}   sum=28 rows=28
  R0-empty    objects= 2  MB=    0.0   ankety-wt, moskva-wt
  R0-holder   objects= 4  MB=    0.0   disciplina-wt, matemdigest-map-wt, materials-wt, matproekty-179-wt
  R5-norepo   objects= 4  MB=  134.4   Готовимся к ЕГЭ, nlogn-otsluzhka, GitHub/scratchpad, spetsmat-bot-wt (52 loose .md at container level)
  R6-books    objects= 6  MB= 1990.0   Книги, spetsmat-179, Downloads/книжки, Downloads/Листки, Downloads/Брессу…pdf (a folder), Downloads/[loose files]
  R7-junk     objects= 6  MB=   67.0   Downloads/4-5 заславский, 7И, Скриншоты, Спецмат_179__25_29, ~/[loose files], ~/Claude
  R8-unclear  objects= 6  MB=  200.2   spetsmat (1097 own files + spetsmat_db inside), Zoom, huggingface, клипы, мои документы, proba-dolg-nedostupnaya-fixture (unreadable)
```

**Worktrees by container:**

| container | R1-ok | R2-push | R3-park | R9-wt-done | R10-wt-residue |
|---|---|---|---|---|---|
| disciplina-wt (226) | 6 | 12 | 134 | 46 | 28 |
| spetsmat-bot-wt (94) | 0 | 1 | 15 | 62 | 16 |
| materials-wt (16) | 1 | 6 | 9 | 0 | 0 |
| matproekty-179-wt (2) | 0 | 0 | 0 | 2 | 0 |
| matemdigest-map-wt (1) | 0 | 1 | 0 | 0 | 0 |

`materials-wt/perepis-diska`, this pass's own worktree, is one of the R2-push rows: its branch had no upstream at measuring time. It is pushed at delivery.

**What this means for pass 2:**
1. **154 of the 339 worktrees (R9 + R10), holding about 19 GB, can go by two mass rules.** R9 is `worktree remove`. R10 is the same, after a scripted check that the residue really is residue. This is the biggest cheap win on the disk.
2. **The analyst's R4-dup can never fire under "first match wins".** Every repository is either clean (R1/R2) or dirty (R3), so the rows never reach R4. Its dimension is also empty: no two main checkouts share an `origin_url`. I propose moving it to a flag column (`dup_group`, present and empty in `repos.tsv`).
3. **R3-park is the real remainder: 158 worktrees and 9 main checkouts.** Of the 158 worktrees:
   - 102 have HEAD already in the default. Their dirt is new uncommitted work on top of merged work, or residue that my name patterns did not catch.
   - 47 have HEAD not in the default.
   - 9 have residue-only dirt but HEAD not in the default.

   The heaviest dirty worktrees:

   | worktree | dirty tracked lines | untracked lines |
   |---|---|---|
   | `materials-wt/modeli` | 843 | 0 |
   | `materials-wt/dovodka-solvera` | 0 | 65 |
   | `spetsmat-bot-wt/zamer-noch2` | 43 | 0 |
   | `materials-wt/obratnyj-progon` | 0 | 27 |
   | `materials-wt/solver-v3-dyhanie` | 0 | 27 |

4. **The most common single residue line** (162 worktrees have exactly one porcelain line):

   | residue line | worktrees |
   |---|---|
   | `M _generator/tools/.hook-otkaz-chuzhoj-volny.log` (disciplina) | 14 |
   | `M docs/index.html` (spetsmat-bot) | 9 |
   | `M doma/zahody/MODELI-ZHIVOST.json` (disciplina) | 5 |
   | `?? scratchpad/` (disciplina, materials, spetsmat-bot) | several |

   These are tracked files that tools rewrite in every worktree, so this is a candidate for `.gitignore`, a factory lesson (see `## ВОПРОСЫ` of the brief).

## 3. Chronology

**Commits per month, all refs** (`git log --all --format=%cI`). There are no commits at all from 2026-01 through 2026-05.

| repository | 06 | 07 | 08 | 09 | first → last (all refs) | span, days |
|---|---|---|---|---|---|---|
| matema-fest | 2 | 8 | 2 | 2 | 06-06 → 09-17 | 103 |
| materials | 5 | 529 | 1017 | 164 | 06-13 → 09-25 | 104 |
| spetsmat_db (no origin) | 330 | 0 | 0 | 0 | 06-16 → 06-26 | 10 |
| carsharing_archive (no origin) | 6 | 0 | 0 | 0 | 06-25 → 06-25 | 0 |
| matemdigest-map | 0 | 20 | 136 | 5 | 07-10 → 09-17 | 69 |
| disciplina | 0 | 0 | 1864 | 6059 | 08-06 → 09-24 | 49 |
| vanya | 0 | 0 | 6 | 2 | 08-19 → 09-17 | 29 |
| london-avgust-2026 (no origin) | 0 | 0 | 29 | 3 | 08-21 → 09-18 | 28 |
| matproekty-179 | 0 | 0 | 33 | 195 | 08-27 → 09-20 | 24 |
| ankety | 0 | 0 | 3 | 17 | 08-29 → 09-20 | 22 |
| matproekty-179-stranica | 0 | 0 | 9 | 27 | 08-29 → 09-18 | 20 |
| spetsmat-bot | 0 | 0 | 0 | 1677 | 09-02 → 09-24 | 22 |
| moskva | 0 | 0 | 0 | 39 | 09-06 → 09-24 | 18 |

**Month by month since 2026-01:**

| month | repos started | repos last touched | Claude Code projects active* | worktrees created** |
|---|---|---|---|---|
| 01–05 | 0 | 0 | 0 | 0 |
| 06 | 4 | 2 (spetsmat_db, carsharing_archive) | 0 | 0 |
| 07 | 1 | 0 | 0 | 0 |
| 08 | 6 | 0 | 36 | 32 |
| 09 | 2 | 11 | 390 | 307 |

- \* A project counts as active in a month when that month falls between the oldest and newest `*.jsonl` mtime of the project. The oldest `*.jsonl` on disk is from **2026-08-21**.
- \*\* Birth time of the `.git` file. This counts only worktrees that still exist; removed ones are not visible.

**Checking the owner's recollection:**
- **"Cowork in use since about early June 2026": consistent, and not refuted.**
  - The first commit on the disk is 2026-06-06 (`matema-fest`), then 06-13 (`materials`) and 06-16 (`spetsmat_db`).
  - There are no commits before June.
  - The old Cowork project folder `~/Documents/Готовимся к ЕГЭ` has files dated 06-22 → 07-06. `~/Claude` has files from 07-03.
  - What is missing: Cowork's own storage lives in `~/Library`, which this pass skips. The data dates the start of git work, not the start of Cowork itself.
- **"The disciplina plugin and skills about a month later" (so about early July): refuted as stated; the data says about two months later.**
  - `disciplina` has its first commit on **2026-08-06**, and that commit already contains `SKILL.md` files.
  - In `materials`, the first `SKILL.md` appears on 2026-08-08.
  - No repository has any `SKILL.md` in July.
  - The caveat: skills kept outside git (for example in `~/.claude/skills`) are invisible to this pass, so "skills in July, outside git" cannot be excluded.
- **"The orchestrator and waves since about late August": waves confirmed; the orchestrator's name is older.**
  - Worktrees: 32 were created in all of August. There was a jump on **08-25 (10 in one day)**, and then 307 in September.
  - The first file with `volna` ("wave") in its name: disciplina 2026-08-30, materials 2026-09-14. The first with `dirizh` ("conductor"): disciplina 2026-08-30.
  - A path containing `orkestr` is already in `materials` on **2026-07-10**. Whether that is the same orchestrator cannot be told without reading content.
  - `zahod/*` branches exist on origin since 07-28 (`zahod/dek-paskal-v2`).

**Started and abandoned within ≤2 days of the first commit:** `materials/carshering/carsharing_archive` (6 commits, all on 2026-06-25, no origin). `spetsmat_db` was active for 10 days (06-16 → 06-26) and then went silent, with no origin.

**Active for more than a month** (all-refs span over 30 days):
- `materials` (104 days)
- `matema-fest` (103, but only 14 commits)
- `matemdigest-map` (69)
- `disciplina` (49)

`vanya` (29) and `london-avgust-2026` (28) are just under the line.

**Claude Code transcripts:** 426 project folders hold 2602 `*.jsonl`. The oldest is from 2026-08-21, which is later than the first worktree (08-06). This suggests older transcripts were pruned (Claude Code keeps them for a limited period by default), so the session column cannot say anything before about 08-21.

## 4. Duplicates

- **No duplicate main checkouts:** 13 main checkouts have 10 distinct origins plus 3 `none`, so there is no R4-dup group.
  - `matproekty-179` (`matproekty-179.git`) and `matproekty-179-stranica` (`projects.git`) are different repositories.
  - `matemdigest-map` is `digest.git`.
- **Name collision:** `spetsmat-bot` has origin `d1-d57/spetsmat-179.git`, and at the same time `~/Documents/GitHub/spetsmat-179/` is a NON-git folder of 21 books. The same name refers to two unrelated things.
- **Big files copied across worktrees.** Each worktree is a full checkout, so every tracked big file is multiplied. The (name, size) groups over all 6556 files over 1 MB:

  | file | size | copies |
  |---|---|---|
  | `_backup_infra_20260710-043240.zip` | 7.4 MB | 242 |
  | `H1-razmetka-osej.jsonl` and `H2a…H2e`, `H3` | 1–4 MB each | 242 each |
  | three 3.3 MB HTML reports | 3.3 MB each | 238 each |
  | `luaotfload-characters.lua`, `UnicodeData.txt` | — | 207 each |

  These copies are most of `disciplina-wt`'s 52 GB. Removing R9/R10 worktrees removes them. The side data, including paths, is in the script's `side.json` and is not delivered here.
- **The same book in several places (by name and size):**
  - `Дневник математического кружка.pdf` (79.8 MB) is in `~/Downloads/книжки/` and also, as `burago-dnevnik-kruzhka-god-1.pdf`, in `materials/_fond/biblioteka/` (untracked there). Their sizes match, but their names differ.
  - `genkin-itenberg-fomin_len-kruzhki.djvu` (7.5 MB) has 17 copies.
  - `09_Индукция.pdf` has 176 copies (it is in the worktrees).

## 5. Surprises

1. **`disciplina-wt` is 52 GB out of the 65 GB in `~/Documents/GitHub`.** 226 live worktrees of one repository; 46 of them are clean and merged (R9), and 28 are residue-only (R10).
2. **Three repositories have no remote.** Two of them are NESTED inside other folders: `materials/carshering/carsharing_archive` (inside the `materials` checkout) and `spetsmat/spetsmat_db`. A cloud session can see none of the three.
3. **The walk found one git tree beyond the census predicate:** `materials/kurs leto 2026/6-lending/lendingi` has a `.git` at depth 6. It is NOT among the Y = 352 trees and has no row.
4. **Three main checkouts are not on their default branch:** `materials` is on `arka/mat-kostyak`, `matproekty-179` on `zahod/nepodtverzhdennye`, and `matemdigest-map` HEAD is `rabota`.
5. **50 worktrees have a detached HEAD.**
6. **Tracked files that tools rewrite in every worktree** (`.hook-otkaz-chuzhoj-volny.log`, `MODELI-ZHIVOST.json`, `zamer-skillov.json`, `docs/index.html`) make otherwise finished worktrees look dirty. This is why the strict rules put 211 trees into R3-park instead of about 167.
7. **`~/Documents/GitHub/spetsmat-bot-wt/` holds 52 loose `.md` files** next to its 94 worktrees, at the container level, outside any git tree.
8. **`~/Downloads/Брессу - … .pdf` is a folder, not a file.**
9. **The home root holds 13 MB of database and bundle backups:**
   - `matemdigest-BACKUP-2026-08-16.bundle`
   - `spetsmat-baza-lokalnaya-2026-09-10.db` with its `-shm`/`-wal` files
   - `spetsmat-baza-rezerv-2026-09-10.db`

   The live `-wal` file means some process may hold this database open.
10. **`~/Documents/GitHub/proba-dolg-nedostupnaya-fixture` cannot be read** (permission denied). Judging by its name, it is a test fixture left on the real disk.
11. **The brief's base ref `claude/bold-faraday-wq09ql` exists only as `origin/…`**, not as a local branch. So `git branch --no-merged claude/bold-faraday-wq09ql` fails with `malformed object name` while `grep -c` still prints 0: a false green.

## 6. Method (for rerunning)

The script is `/tmp/perepis-diska/perepis.py`, and its full text is attached in `## ОТЧЁТ` of the brief. The order inside it:
1. `status --porcelain` for all 352 trees.
2. `fetch --prune origin` once per repository.
3. All the other measurements.
4. `status --porcelain` again.

All git calls use `--no-optional-locks`. File content is never read, except the first `#` line of `README.md`/`CLAUDE.md`. Residue classes come from `git status` path names only.
