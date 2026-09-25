# verifier — chistka-github

Run 2026-09-25 12:25:27 — command: `python3 /tmp/chistka/verifier/verify.py`

Source: `actions.tsv` (868 rows total, 849 deletion rows).

| repo | deletion rows | checked | via trunk | via tag | failures |
|---|---|---|---|---|---|
| ankety | 2 | 2 | 1 | 1 | 0 |
| arhiv-london-avgust-2026 | 3 | 3 | 3 | 0 | 0 |
| disciplina | 625 | 625 | 456 | 169 | 0 |
| matema-fest | 1 | 1 | 0 | 1 | 0 |
| materials | 71 | 71 | 60 | 11 | 0 |
| matproekty-179 | 8 | 8 | 7 | 1 | 0 |
| moskva | 1 | 1 | 1 | 0 | 0 |
| sayt-sistemy-konstantinova | 3 | 3 | 3 | 0 | 0 |
| spetsmat-179 | 135 | 135 | 101 | 34 | 0 |
| **total** | 849 | 849 | 632 | 217 | 0 |

## Failures

no failures

## Notes (informational)

- non-deletion actions present in the file (not checked): keep

## Coverage (before.tsv vs actions.tsv)

| repo | remote_branches (before) | rows in actions.tsv | match |
|---|---|---|---|
| materials | 76 | 76 | yes |
| disciplina | 627 | 627 | yes |
| spetsmat-179 | 136 | 136 | yes |
| matproekty-179 | 9 | 9 | yes |
| matproekty-179-stranica | 1 | 1 | yes |
| ankety | 3 | 3 | yes |
| moskva | 2 | 2 | yes |
| matema-fest | 2 | 2 | yes |
| digest | 3 | 3 | yes |
| arhiv-london-avgust-2026 | 5 | 5 | yes |
| sayt-sistemy-konstantinova | 4 | 4 | yes |

rows 868 of 868; duplicates (repo, branch): none; repos not in before.tsv: none

## Live GitHub state vs actions.tsv

| repo | live heads | keep rows | heads OK | live arhiv/* tags | tag+delete rows | tags OK |
|---|---|---|---|---|---|---|
| materials | 5 | 5 | yes | 11 | 11 | yes |
| disciplina | 2 | 2 | yes | 169 | 169 | yes |
| spetsmat-179 | 1 | 1 | yes | 34 | 34 | yes |
| matproekty-179 | 1 | 1 | yes | 1 | 1 | yes |
| matproekty-179-stranica | 1 | 1 | yes | 0 | 0 | yes |
| ankety | 1 | 1 | yes | 1 | 1 | yes |
| moskva | 1 | 1 | yes | 0 | 0 | yes |
| matema-fest | 1 | 1 | yes | 1 | 1 | yes |
| digest | 3 | 3 | yes | 0 | 0 | yes |
| arhiv-london-avgust-2026 | 2 | 2 | yes | 0 | 0 | yes |
| sayt-sistemy-konstantinova | 1 | 1 | yes | 0 | 0 | yes |

live branches that are not a keep row: none

keep rows whose branch is not live: none

arhiv/* tags differing from tag+delete rows (either side): none

criteria (2)-(4): ALL PASS

checked 849 of 849, 0 failures
