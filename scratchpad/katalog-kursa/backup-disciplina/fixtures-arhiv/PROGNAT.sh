#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: check_arhiv.py
# Fixtures of the cancelled-decision gate (check_arhiv.py).
# Run after every edit of check_arhiv.py:  bash _generator/tools/fixtures/arhiv/PROGNAT.sh
#
# A gate that can PASS must have a fixture on which it FAILS, otherwise nobody knows whether it
# checks anything or prints green into the void. Two layers here:
#   traps   - small source+file trees, each with an expected exit code and an expected phrase;
#   mutants - the tool is COPIED and broken by one anchored replacement (abort unless the anchor
#             occurs exactly once), and the matching trap must then give a DIFFERENT exit code.
#             A trap that a broken tool survives proves nothing; this layer proves the traps bite.
# Portability: macOS BSD userland, no in-place editors, no GNU-only flags; the text substitution
# is done by python3.
set -u

KOREN="$(cd "$(dirname "$0")/../../.." && pwd)"
GATE="$KOREN/tools/check_arhiv.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

BANNER="$(python3 -c "import sys; sys.path.insert(0, sys.argv[1]); import check_arhiv; print(check_arhiv.BANNER)" "$KOREN/tools")"
MARK="$(python3 -c "import sys; sys.path.insert(0, sys.argv[1]); import check_arhiv; print(check_arhiv.SECTION_MARK)" "$KOREN/tools")"

pad () { n="$1"; i=0; while [ "$i" -lt "$n" ]; do echo "filler $i"; i=$((i+1)); done; }

head_of_source () {                 # head_of_source <file> : preamble of a decision-home source
  printf '%s\n' '# Z' '## §5. CANCELLED' > "$1"
}

entry () {                          # entry <file> <id> <address-block-or-empty>
  printf '%s\n' "### \`$2\`" '`отменено: 2026-09-01`' '' >> "$1"
  if [ -n "$3" ]; then printf '%s\n' "**Где лежит непочиненным:** $3" '' >> "$1"; fi
}

banner_file () {                    # banner_file <file> <id> <banner-line-number>
  { printf '%s\n' '---' 'opisanie: x' '---'
    pad $(( $3 - 4 ))
    echo "$BANNER"
    echo "Cancelled by entry $2 (ZAMYSEL.md)."
    pad 5; } > "$1"
}

marked_file () {                    # marked_file <file> <id> <total-lines> <mark-line-number>
  pad $(( $3 )) > "$1.tmp"
  python3 -c "
import sys
lines = open(sys.argv[1], encoding='utf-8').read().splitlines()
n = int(sys.argv[4])
lines[n - 1] = '> ' + sys.argv[3] + ' ' + sys.argv[2] + ' - ZAMYSEL.md. Section is cancelled.'
open(sys.argv[5], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
" "$1.tmp" "$2" "$MARK" "$4" "$1"
  rm -f "$1.tmp"
}

expect () {                         # expect <label> <want-rc> <phrase-or-dash> <python-args...>
  label="$1"; want="$2"; phrase="$3"; shift 3
  vyvod="$(python3 "$@" 2>&1)"; got=$?
  if [ "$got" != "$want" ]; then
    echo "  ✗ $label: exit $got, expected $want"; OK=1
  elif [ "$phrase" != "-" ] && ! printf '%s' "$vyvod" | grep -qF -- "$phrase"; then
    echo "  ✗ $label: exit $got as expected, but the phrase «$phrase» is missing from the verdict"; OK=1
  else
    echo "  ✓ $label: exit $got"
  fi
}

run_case () {                       # run_case <case> -> exit code of the ORIGINAL tool, output kept
  zam="$TMP/$1/ZAMYSEL.md"
  [ -f "$zam" ] || zam="$TMP/$1/nested/ZAMYSEL.md"
  python3 "${TOOL:-$GATE}" "$zam" --koren "$TMP/$1" ${EXTRA:-} >/dev/null 2>&1
  echo $?
}

echo "── TRAPS ──"

# healthy: one banner file, one section-mark file; both name their entry
mkdir -p "$TMP/zdorovaya"; Z="$TMP/zdorovaya/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3`'; entry "$Z" frame-b '`b.md:5`'
banner_file "$TMP/zdorovaya/a.md" frame-a 5; marked_file "$TMP/zdorovaya/b.md" frame-b 12 6
expect "zdorovaya (banner + section mark)      " 0 "проверено 2 из 2" "$GATE" "$Z" --koren "$TMP/zdorovaya"

# no mark at all on a named file
mkdir -p "$TMP/bez-pometki"; Z="$TMP/bez-pometki/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3`'; entry "$Z" frame-b '`b.md:5`'
banner_file "$TMP/bez-pometki/a.md" frame-a 5; pad 12 > "$TMP/bez-pometki/b.md"
expect "bez-pometki (file named, no mark)      " 1 "no mark: frame-b: b.md:5" "$GATE" "$Z" --koren "$TMP/bez-pometki"

# banner below line 10 does not count
mkdir -p "$TMP/banner-nizhe-10"; Z="$TMP/banner-nizhe-10/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3`'; banner_file "$TMP/banner-nizhe-10/a.md" frame-a 12
expect "banner-nizhe-10 (banner at line 12)    " 1 "no mark: frame-a: a.md:3" "$GATE" "$Z" --koren "$TMP/banner-nizhe-10"

# section mark 25 lines away from the named line does not count
mkdir -p "$TMP/pometka-daleko"; Z="$TMP/pometka-daleko/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-b '`b.md:5`'; marked_file "$TMP/pometka-daleko/b.md" frame-b 40 30
expect "pometka-daleko (mark 25 lines away)    " 1 "no mark: frame-b: b.md:5" "$GATE" "$Z" --koren "$TMP/pometka-daleko"

# window boundary: distance 8 counts, distance 9 does not, on both sides of the named line
for spec in "posle-8:5:13:0" "posle-9:5:14:1" "do-8:20:12:0" "do-9:20:11:1"; do
  nm="${spec%%:*}"; rest="${spec#*:}"; naz="${rest%%:*}"; rest="${rest#*:}"; met="${rest%%:*}"; want="${rest#*:}"
  mkdir -p "$TMP/g-$nm"; Z="$TMP/g-$nm/ZAMYSEL.md"; head_of_source "$Z"
  entry "$Z" frame-b "\`b.md:$naz\`"; marked_file "$TMP/g-$nm/b.md" frame-b 40 "$met"
  expect "granica $nm (named $naz, mark $met)     " "$want" "-" "$GATE" "$Z" --koren "$TMP/g-$nm"
done

# banner names ANOTHER entry: it does not cover this one
mkdir -p "$TMP/chuzhoj-id"; Z="$TMP/chuzhoj-id/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3`'; banner_file "$TMP/chuzhoj-id/a.md" other-frame 5
expect "chuzhoj-id (banner of another entry)   " 1 "no mark: frame-a: a.md:3" "$GATE" "$Z" --koren "$TMP/chuzhoj-id"

# the source has an entry line but no backticked id heading: the gate saw nothing -> RED, not green
mkdir -p "$TMP/bez-zagolovka"; Z="$TMP/bez-zagolovka/ZAMYSEL.md"; head_of_source "$Z"
printf '%s\n' '### Plain heading, no id' '`отменено: 2026-09-01`' '' >> "$Z"
expect "bez-zagolovka (coverage 0 of 1)        " 1 "parsed 0 of 1" "$GATE" "$Z" --koren "$TMP/bez-zagolovka"

# continuation `:N` inherits the previous file: the second address is far from the mark
mkdir -p "$TMP/prodolzhenie"; Z="$TMP/prodolzhenie/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3` and `:60`'; marked_file "$TMP/prodolzhenie/a.md" frame-a 70 4
expect "prodolzhenie (bare :N inherits a.md)   " 1 "no mark: frame-a: a.md:60" "$GATE" "$Z" --koren "$TMP/prodolzhenie"

# one address resolves and is marked, one names a file that does not exist
mkdir -p "$TMP/neraz"; Z="$TMP/neraz/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`a.md:3`'; entry "$Z" frame-b '`ghost.md:3`'; banner_file "$TMP/neraz/a.md" frame-a 5
expect "neraz (unresolved is reported, green)  " 0 "ЗЕЛЁНЫЙ С ДЫРОЙ" "$GATE" "$Z" --koren "$TMP/neraz"
expect "neraz --strogo (unresolved is red)     " 1 "--strogo" "$GATE" "$Z" --koren "$TMP/neraz" --strogo

# every named address is unresolved: the gate saw no file at all -> RED
mkdir -p "$TMP/vse-neraz"; Z="$TMP/vse-neraz/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-b '`ghost.md:3`'
expect "vse-neraz (saw no file)                " 1 "none of the 1 named" "$GATE" "$Z" --koren "$TMP/vse-neraz"

# an entry without a 'where it still lies' block: nothing to check, said out loud
mkdir -p "$TMP/bez-bloka"; Z="$TMP/bez-bloka/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-c ''
expect "bez-bloka (entry without addresses)    " 0 "1 without a 'where it still lies' block" "$GATE" "$Z" --koren "$TMP/bez-bloka"

# empty source: not silent, says there is nothing to check
mkdir -p "$TMP/pustoj"; head_of_source "$TMP/pustoj/ZAMYSEL.md"
expect "pustoj (0 entries, said out loud)      " 0 "nothing to check" "$GATE" "$TMP/pustoj/ZAMYSEL.md" --koren "$TMP/pustoj"

# second resolution step: the file lies at the repository root, not next to the source
mkdir -p "$TMP/koren/nested"; Z="$TMP/koren/nested/ZAMYSEL.md"; head_of_source "$Z"
entry "$Z" frame-a '`top.md:3`'; banner_file "$TMP/koren/top.md" frame-a 5
expect "koren (file at the root, not beside)   " 0 "marked 1" "$GATE" "$Z" --koren "$TMP/koren"

# wrong calls: three exits of the family, and "misused" must be told apart from "defect"
expect "misuse: no argument                    " 2 "-" "$GATE"
expect "misuse: no such file                   " 2 "-" "$GATE" "$TMP/none-such/ZAMYSEL.md"
expect "misuse: unknown flag                   " 2 "-" "$GATE" "$TMP/zdorovaya/ZAMYSEL.md" --bogus
expect "misuse: negative window                " 2 "-" "$GATE" "$TMP/zdorovaya/ZAMYSEL.md" --okno -1

echo "── MUTANTS (the tool is broken on purpose; the trap must change its exit code) ──"
MUTANTS=0; CAUGHT=0

mutate () {   # mutate <label> <trap-case> <extra-flags-or-dash> <old> <new> [<old2> <new2>]
  label="$1"; caso="$2"; extra="$3"; old="$4"; new="$5"; old2="${6:-}"; new2="${7:-}"
  MUTANTS=$((MUTANTS+1))
  mut="$TMP/mutant.py"
  python3 -c "
import sys
src = open(sys.argv[1], encoding='utf-8').read()
pairs = [(sys.argv[3], sys.argv[4])] + ([(sys.argv[5], sys.argv[6])] if sys.argv[5] else [])
for old, new in pairs:
    if src.count(old) != 1:
        print('ANCHOR-DRIFT: %r occurs %d times' % (old, src.count(old))); sys.exit(3)
    src = src.replace(old, new)
open(sys.argv[2], 'w', encoding='utf-8').write(src)
" "$GATE" "$mut" "$old" "$new" "$old2" "$new2"
  if [ $? != 0 ]; then echo "  ✗ $label: anchor not found exactly once - update the mutant"; OK=1; return; fi
  [ "$extra" = "-" ] && extra=""
  orig="$(TOOL="$GATE" EXTRA="$extra" run_case "$caso")"
  muta="$(TOOL="$mut" EXTRA="$extra" run_case "$caso")"
  if [ "$orig" != "$muta" ]; then
    CAUGHT=$((CAUGHT+1)); echo "  ✓ $label: original exit $orig, mutant exit $muta - caught by trap $caso"
  else
    echo "  ✗ $label: the trap $caso did NOT notice the broken tool (both exit $orig)"; OK=1
  fi
}

mutate "M1  banner window 10 -> 40            " banner-nizhe-10 - 'BANNER_LINES = 10' 'BANNER_LINES = 40'
mutate "M2  banner needs no entry id          " chuzhoj-id - 'and any(entry_id in ln for ln in head)' 'and True'
mutate "M3  default section window 8 -> 200   " pometka-daleko - 'DEFAULT_WINDOW = 8' 'DEFAULT_WINDOW = 200'
mutate "M4  coverage zero/partial is not red  " bez-zagolovka - 'if y > 0 and x == 0:' 'if False:' 'elif x < y:' 'elif False:'
mutate "M5  unmarked counted as marked        " bez-pometki - '(res["marked"] if how else res["unmarked"])' 'res["marked"]'
mutate "M6  bare :N does not inherit the file " prodolzhenie - 'a.group(1) or prev' 'a.group(1)'
mutate "M7  --strogo ignores unresolved       " neraz --strogo 'if strogo and res["unresolved"]:' 'if False:'
mutate "M8  'saw no file' is not red          " vse-neraz - 'if res["named"] > 0 and res["resolved"] == 0:' 'if False:'
mutate "M9  root resolution step removed      " koren - 'bases = [src.parent, root]' 'bases = [src.parent]'
mutate "M10 window after the line +3          " g-posle-9 - 'hi = min(len(lines), addr_line + window)' 'hi = min(len(lines), addr_line + window + 3)'
mutate "M11 window before the line +3         " g-do-9 - 'lo = max(0, addr_line - 1 - window)' 'lo = max(0, addr_line - 4 - window)'

echo "── TOTAL: mutants caught $CAUGHT of $MUTANTS · $([ $OK = 0 ] && echo 'everything as expected' || echo 'THERE ARE DISCREPANCIES')"
exit $OK
