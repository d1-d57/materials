#!/usr/bin/env bash
# orchestrate.sh — оркестратор-над-волнами (волна-за-волной, durable I/O).
#
# Workflow МЕЖСЕССИЙНО НЕ резюмится (стартует заново; resume только внутри сессии Code).
# Поэтому КАЖДАЯ ВОЛНА — отдельный вызов `claude -p`: читает durable-артефакт прошлой
# волны и пишет свой. Троттл 5-час окна между волнами → resume = просто перезапустить
# следующую волну (предыдущие лежат на диске в artifacts/). Внутри волны троттл →
# волна перезапускается ЦЕЛИКОМ (поэтому волны режем под комфортный размер).
#
# Использование:
#   ./orchestrate.sh all          # все 5 волн подряд
#   ./orchestrate.sh w3           # только волна 3 (resume после троттла)
#   ./orchestrate.sh w3 w4 w5     # с волны 3 до конца
#
# ПОРТАТИВНОСТЬ: без bash-4 фич (declare -A, mapfile) — работает и на bash 3.2,
# который стоит на macOS по умолчанию (иначе падало `line: w1: unbound variable`).
# Флаги claude -p (--json-schema/--bare) добавляются ТОЛЬКО если их знает твоя версия
# claude (на Маке может быть старее дизайна) — контракт всё равно держат промпты волн
# + валидация в TRIAGE/DEEPEN. Тиринг — через CLAUDE_CODE_SUBAGENT_MODEL. ОДИН инстанс.

set -euo pipefail

PROC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ART="$PROC_DIR/artifacts"
SCHEMA="$PROC_DIR/scorecard.schema.json"
mkdir -p "$ART"

# --- лог времени/токенов прогона (для владельца; всегда логируем) ---
RUN_LOG="$ART/run_log.txt"
RUN_START=$(date +%s)
echo "=== RUN start $(date '+%F %T %Z') ===" >> "$RUN_LOG"

# --- какие флаги поддерживает установленный claude (версия может быть старее дизайна) ---
CLAUDE_HELP="$(claude --help 2>&1 || true)"
COMMON_FLAGS=(--output-format json)
if printf '%s' "$CLAUDE_HELP" | grep -q -- '--json-schema'; then
  COMMON_FLAGS+=(--json-schema "$SCHEMA")
else
  echo "ПРИМЕЧАНИЕ: claude не знает --json-schema → контракт держат промпты волн + валидация TRIAGE/DEEPEN (это ок, пилот так и работал)." | tee -a "$RUN_LOG"
fi
if printf '%s' "$CLAUDE_HELP" | grep -q -- '--bare'; then
  COMMON_FLAGS+=(--bare)
fi
COMMON_FLAGS+=(--allowedTools "Read,Write,Edit,Bash,Agent" --permission-mode acceptEdits)

# Тиринг модели по волне (case вместо `declare -A` — портативно для bash 3.2).
# w1=haiku (ширина); w2/w3/w4/w5=sonnet на оркестраторе (Opus — только в воркерах ядра
# w4 через `model:` в их определении, не здесь).
model_for () {
  case "$1" in
    w1) echo haiku ;;
    *)  echo sonnet ;;
  esac
}

run_wave () {
  local wave="$1" model="$2"
  local w_start w_end secs toks raw
  w_start=$(date +%s)
  raw="$ART/${wave}_run.json"
  echo ">>> [$wave] модель субагентов=$model  $(date '+%H:%M:%S')"
  CLAUDE_CODE_SUBAGENT_MODEL="$model" \
    claude -p "Выполни procedura/${wave}.md по контракту в procedura/. \
Читай durable-артефакт предыдущей волны из procedura/artifacts/ и запиши свой туда же. \
Промпт волны самодостаточен — следуй ему дословно." \
    "${COMMON_FLAGS[@]}" | tee "$raw"
  w_end=$(date +%s); secs=$(( w_end - w_start )); toks="?"
  if command -v jq >/dev/null 2>&1; then
    toks=$(jq -r '(.usage.input_tokens // 0) + (.usage.output_tokens // 0)' "$raw" 2>/dev/null || echo "?")
  fi
  echo "[$wave] время=${secs}s токены(in+out)=${toks}" | tee -a "$RUN_LOG"
  echo "<<< [$wave] готово  $(date '+%H:%M:%S')"
}

ORDER=(w1 w2 w3 w4 w5)

# Разбор аргумента: all | список волн | стартовая волна → до конца.
pick_waves () {
  if [[ $# -eq 0 || "$1" == "all" ]]; then printf '%s\n' "${ORDER[@]}"; return; fi
  if [[ $# -eq 1 && "$1" =~ ^w[1-5]$ ]]; then
    local started=0 w
    for w in "${ORDER[@]}"; do
      [[ "$w" == "$1" ]] && started=1
      [[ $started -eq 1 ]] && echo "$w"
    done
    return
  fi
  printf '%s\n' "$@"
}

# while-read вместо `mapfile` — портативно для bash 3.2.
WAVES=()
while IFS= read -r _w; do
  if [ -n "$_w" ]; then WAVES+=("$_w"); fi
done < <(pick_waves "$@")

if [ "${#WAVES[@]}" -eq 0 ]; then echo "Нет волн к прогону (аргумент: '$*')."; exit 1; fi
echo "Волны к прогону: ${WAVES[*]}"
for w in "${WAVES[@]}"; do
  run_wave "$w" "$(model_for "$w")"
done
RUN_END=$(date +%s); RUN_SECS=$(( RUN_END - RUN_START ))
echo "=== ИТОГ: общее время $(( RUN_SECS/60 ))м $(( RUN_SECS%60 ))с; токены по волнам — в $RUN_LOG ===" | tee -a "$RUN_LOG"
echo "ВСЁ. Итог — procedura/artifacts/w5_dossier.md"
