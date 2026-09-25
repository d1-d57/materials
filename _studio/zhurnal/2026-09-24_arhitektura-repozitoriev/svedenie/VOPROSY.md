# VOPROSY — svedenie

Form: `<object> — <what it is> — PROPOSED: <default> — because <reason>`

1. `disciplina/--help/` (6 files, 2026-09-21) — test-fixture output of a tool that was called with `--help` as its target path (`--help/_generator/tools/gejt_proby.py`, `--help/skills/proba/RESHENIYA.md`, lessons named "proba"); the hook refuses it and it is not work — PROPOSED: move it to `~/.Trash/` (or `git_zona.py purge --yes`, which exists for names with a leading `-`), not commit — because committing a test artifact into the trunk is not conservation. Left in place; it is the only remainder in `disciplina` (`status --porcelain` → 1 line).
