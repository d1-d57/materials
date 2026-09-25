# VOPROSY — chistka-github

Form: `<object> — <what it is> — PROPOSED: <default> — because <reason>`

1. `## ГИГИЕНА ВХОДА` of `kod_chistka-github.md` — the section says the git-contour subagent fills it, while §0.1 says no subagent is needed when the contour is empty — PROPOSED: the executor fills the entry snapshot with command output when no subagent runs (done in this pass) — because otherwise the section stays empty and gate Г12 of the acceptance is red by construction.
2. §0.1 self-check `git branch --no-merged claude/bold-faraday-wq09ql` — fails in a worktree that has no local branch of that name (`fatal: malformed object name`), and `| grep -c` prints `0`, so the failure reads as "clean" — PROPOSED: the generator prints `origin/claude/bold-faraday-wq09ql` in this command — because a gate that turns an error into a green zero is exactly the false green the canon forbids.
