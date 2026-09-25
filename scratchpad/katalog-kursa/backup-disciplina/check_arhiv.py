#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CANCELLED-DECISION GATE: a cancelled document must say so about itself.

    python3 _generator/tools/check_arhiv.py <ZAMYSEL.md>
    python3 _generator/tools/check_arhiv.py <ZAMYSEL.md> --strogo
    python3 _generator/tools/check_arhiv.py <ZAMYSEL.md> --koren <dir> --okno 8 --tiho

Exit code: 0 - every resolved address carries a cancellation mark;
           1 - an address without a mark, or the coverage is zero / incomplete;
           2 - called wrongly (no source, no such file, unknown flag).

WHY. The decision home of a course (`ZAMYSEL.md`) records every cancelled decision as
an entry starting with a backticked `отменено:` line, and names, under "where it still
lies uncured", the files and lines that keep standing on the cancelled decision. The
home knew where the mines were; the mined files said nothing, and nothing checked it:
an analyst leaned twice in one session on a cancelled document as on a live source.
This gate closes exactly that gap: every file named by a cancellation entry must carry
a mark that says so, in one of two forms (both must NAME the cancelling entry's id):

    whole file   - a banner in the first 10 lines of the file, plus the entry id in
                   those same 10 lines (the one-line reason);
    one section  - a line with the section-mark token within OKNO lines (default 8)
                   of the named line, plus the entry id on that same line.

A banner silences the file as a whole, so it is for files that are cancelled entirely;
a live file with one cancelled section takes the section mark, not the banner.

COVERAGE PRINTS WITH THE VERDICT: "проверено X из Y", where Y is the number of
cancellation entries counted straight from the source text BEFORE any parsing, and X
the number the gate actually parsed. X = 0 with a non-empty source is RED, not green:
a gate that saw nothing is not a clean source.

Idiom of the family (`_generator/DVIZHKI.md`): stdlib only, deterministic, no network,
exit 1 on red, blind zones printed always (also when green).
"""
import argparse
import re
import sys
from pathlib import Path

RC_OK, RC_DEFECT, RC_MISUSE = 0, 1, 2

BANNER_LINES = 10
DEFAULT_WINDOW = 8

# Marks are assembled from parts on purpose: a marker this tool SEARCHES for must not
# stand whole in the tool's own prose, or the gate finds itself (see check_tool_contract).
BANNER = " ".join(("🗄", "АРХИВ", "—", "ГЕЙТ", "НЕ", "СУДИТ"))
SECTION_MARK = " ".join(("🚫", "ОТМЕНЕНО", "ЗАПИСЬЮ"))

ENTRY_LINE_RE = re.compile(r"^`отменено:", re.M)
HEADING_RE = re.compile(r"^#{2,3}\s", re.M)
ENTRY_ID_RE = re.compile(r"^#{2,3}\s+`([^`\n]+)`")
BLOCK_RE = re.compile(r"[Гг]де\s+(?:ещё\s+)?лежит\s+непочиненным")
TOKEN_RE = re.compile(r"`([^`\n]+)`")
ADDR_RE = re.compile(r"^([^\s:`]*\.md)?:(\d+)$")
PATHLIKE_RE = re.compile(r"^[\w./-]+$")

NE_PROVERYAEM = [
    "truthfulness of the cancellation itself: the gate takes a recorded cancellation as given "
    "and never judges whether the owner was right to cancel",
    "addresses written in prose or in any shape other than a backticked `path.md:N` - they are "
    "listed by name when seen, but nothing verifies a mark for them",
    "files that stand on a cancelled decision but are not named by the entry: only what the "
    "source names is checked",
    "that a mark sits on the RIGHT section: only proximity to the named line and the entry id "
    "on the mark; line numbers were true on the date of the entry and drift when a file is "
    "edited",
    "addresses that resolve neither next to the source nor at the repository root: reported "
    "by name as unresolved, judged only under --strogo",
    "the wording of the reason after the mark, and whether a whole-file banner is deserved",
]


def read_source(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def find_repo_root(start):
    for cand in (start, *start.parents):
        if (cand / ".git").exists():
            return cand
    return start


def parse_entries(source):
    """-> (Y, X, entries, unparsed). Y is counted from the raw text before parsing."""
    y = len(ENTRY_LINE_RE.findall(source))
    starts = [m.start() for m in HEADING_RE.finditer(source)]
    starts.append(len(source))
    entries, x = [], 0
    for a, b in zip(starts, starts[1:]):
        chunk = source[a:b]
        n = len(ENTRY_LINE_RE.findall(chunk))
        if n == 0:
            continue
        m = ENTRY_ID_RE.match(chunk)
        if not m:
            continue
        x += n
        block = BLOCK_RE.search(chunk)
        entries.append((m.group(1), chunk[block.end():] if block else None))
    return y, x, entries


def extract_addresses(block):
    """Backticked `path.md:N` tokens of one block; a bare `:N` inherits the previous file."""
    found, noline, prev = [], [], None
    for m in TOKEN_RE.finditer(block):
        tok = m.group(1)
        a = ADDR_RE.match(tok)
        if a:
            path = a.group(1) or prev
            if path is None:
                noline.append(tok)
                continue
            prev = path
            found.append((path, int(a.group(2))))
        elif PATHLIKE_RE.match(tok) and ("/" in tok or tok.endswith(".md")):
            noline.append(tok)
    return found, noline


def resolve(path, bases):
    for base in bases:
        cand = base / path
        if cand.is_file():
            return cand
    return None


def find_mark(lines, addr_line, entry_id, window):
    head = lines[:BANNER_LINES]
    if any(BANNER in ln for ln in head) and any(entry_id in ln for ln in head):
        return "banner"
    lo = max(0, addr_line - 1 - window)
    hi = min(len(lines), addr_line + window)
    for ln in lines[lo:hi]:
        if SECTION_MARK in ln and entry_id in ln:
            return "section"
    return None


def judge(source_path, window, koren):
    source = read_source(source_path)
    if source is None:
        return None
    y, x, entries = parse_entries(source)
    src = Path(source_path).resolve()
    root = Path(koren).resolve() if koren else find_repo_root(src.parent)
    bases = [src.parent, root]
    res = {"Y": y, "X": x, "entries": len(entries), "no_block": [], "named": 0,
           "resolved": 0, "marked": [], "unmarked": [], "unresolved": [], "noline": [],
           "root": str(root)}
    seen = set()
    for entry_id, block in entries:
        if block is None:
            res["no_block"].append(entry_id)
            continue
        found, noline = extract_addresses(block)
        res["noline"] += ["%s: `%s`" % (entry_id, t) for t in noline]
        for path, line_no in found:
            res["named"] += 1
            target = resolve(path, bases)
            if target is None:
                res["unresolved"].append("%s: %s:%d" % (entry_id, path, line_no))
                continue
            res["resolved"] += 1
            key = (str(target), line_no, entry_id)
            if key in seen:
                continue
            seen.add(key)
            lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
            how = find_mark(lines, line_no, entry_id, window)
            label = "%s: %s:%d" % (entry_id, path, line_no)
            (res["marked"] if how else res["unmarked"]).append(
                label + (" [%s]" % how if how else ""))
    return res


def report(res, source_path, strogo, tiho):
    red = []
    y, x = res["Y"], res["X"]
    if y > 0 and x == 0:
        red.append("parsed 0 of %d entries: the gate did not see the source, "
                   "this is not a clean source" % y)
    elif x < y:
        red.append("parsed %d of %d entries: the rest have no `### `id`` heading above them"
                   % (x, y))
    if res["named"] > 0 and res["resolved"] == 0:
        red.append("none of the %d named addresses resolved to a file: the gate saw no file"
                   % res["named"])
    if res["unmarked"]:
        red.append("%d named address(es) carry no cancellation mark" % len(res["unmarked"]))
    if strogo and res["unresolved"]:
        red.append("--strogo: %d named address(es) do not resolve" % len(res["unresolved"]))

    if not tiho:
        print("── ГЕЙТ ОТМЕНЁННОГО (check_arhiv) ──")
        print("  %s" % source_path)
        print("  проверено %d из %d записей отменено: (Y counted from the source text before "
              "parsing; %d without a 'where it still lies' block, nothing to check there)"
              % (x, y, len(res["no_block"])))
        print("  addresses named %d · resolved %d · marked %d · unmarked %d · unresolved %d"
              % (res["named"], res["resolved"], len(res["marked"]), len(res["unmarked"]),
                 len(res["unresolved"])))
        print("  resolution: next to the source, then at %s" % res["root"])
        print("\n  ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ — список закрытый:")
        for item in NE_PROVERYAEM:
            print("     · %s" % item)
        if y == 0:
            print("\n  nothing to check: the source holds 0 `отменено:` entries "
                  "(if this is the wrong file, that is not an error of the gate)")
        if res["unresolved"]:
            print("\n  UNRESOLVED (blind, named): %s" % "; ".join(res["unresolved"]))
        if res["noline"]:
            print("\n  NOT IN `path.md:N` FORM (blind, named): %s" % "; ".join(res["noline"]))
        if res["marked"]:
            print("\n  marked: %s" % "; ".join(res["marked"]))

    if red:
        if not tiho:
            print("\n  ✗ КРАСНЫЙ — %d finding(s):" % len(red))
            for r in red:
                print("     · %s" % r)
            for u in res["unmarked"]:
                print("     ✗ no mark: %s" % u)
        return RC_DEFECT

    if not tiho:
        if res["unresolved"]:
            print("\n  ✓ ЗЕЛЁНЫЙ С ДЫРОЙ: every resolved address is marked, but %d address(es) "
                  "could not be resolved and stay unjudged (use --strogo to make that red)"
                  % len(res["unresolved"]))
        else:
            print("\n  ✓ ЗЕЛЁНЫЙ: every named address carries a cancellation mark")
    return RC_OK


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_arhiv.py",
        description=__doc__.strip().splitlines()[0],
        epilog="Marks: whole file - banner within the first %d lines; one section - "
               "section-mark token within --okno lines of the named line; both must name "
               "the cancelling entry id. Exit: 0 clean, 1 defect, 2 misuse." % BANNER_LINES)
    ap.add_argument("zamysel", help="decision-home file holding `отменено:` entries")
    ap.add_argument("--koren", help="repository root for the second address resolution step")
    ap.add_argument("--okno", type=int, default=DEFAULT_WINDOW,
                    help="section-mark window in lines around the named line (default %d)"
                         % DEFAULT_WINDOW)
    ap.add_argument("--strogo", action="store_true",
                    help="an address that does not resolve is red, not just reported")
    ap.add_argument("--tiho", action="store_true", help="exit code only")
    args = ap.parse_args(argv)
    if args.okno < 0:
        print("check_arhiv: --okno must be >= 0", file=sys.stderr)
        return RC_MISUSE
    res = judge(args.zamysel, args.okno, args.koren)
    if res is None:
        print("check_arhiv: cannot read source: %s" % args.zamysel, file=sys.stderr)
        return RC_MISUSE
    return report(res, args.zamysel, args.strogo, args.tiho)


if __name__ == "__main__":
    sys.exit(main())
