#!/bin/bash
# ЦЕПОЧКА НОЧИ — три захода подряд, шлюзы между ними без единого токена.
#
#   bash /Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-07-30_dovodka-fabriki/noch.sh
#
# ЧТО ДЕЛАЕТ
#   Н1 разметка осей (корпус исполнителей) → шлюз → Н2 разметка владельца →
#   шлюз → Н3 инвентарь архитектуры → итоговый отчёт в ITOG-nochi.md.
#
# ПРЕДОХРАНИТЕЛЬ БЮДЖЕТА
#   После каждого звена складывается `total_cost_usd`, который CLI сам пишет в
#   лог. Превысили потолок — цепочка встаёт, следующее звено не стартует.
#   Честное ограничение: проверка возможна МЕЖДУ звеньями, не внутри. Против
#   разгона внутри звена стоит таймаут.
#
# ЧТО ОСТАНАВЛИВАЕТ ЦЕПОЧКУ
#   · превышен бюджет
#   · звено не создало НИ ОДНОГО артефакта (значит сломана среда, а не работа)
#   Брак в разметке цепочку НЕ останавливает: заходы работают с разными
#   корпусами и друг от друга не зависят. Брак фиксируется и судится утром.
set -u

REPO=/Users/ivanyakovlev/Documents/GitHub/materials
ARKA="$REPO/_studio/zhurnal/2026-07-30_dovodka-fabriki"
LOGI="$ARKA/noch-logi"
ITOG="$ARKA/ITOG-nochi.md"
BUDZHET=40.0          # потолок в долларах на всю ночь
TAJMAUT_MIN=180       # потолок в минутах на одно звено

mkdir -p "$LOGI"
cd "$REPO" || exit 1

TO=""
command -v timeout  >/dev/null 2>&1 && TO="timeout"
command -v gtimeout >/dev/null 2>&1 && TO="gtimeout"

echo "# ИТОГ НОЧИ — печатает noch.sh, руками не править" >  "$ITOG"
echo ""                                                  >> "$ITOG"
echo "Старт: $(date '+%Y-%m-%d %H:%M')"                   >> "$ITOG"
echo ""                                                  >> "$ITOG"
[ -z "$TO" ] && echo "⚠ \`timeout\` не найден — звенья идут без потолка по времени. Ставится через \`brew install coreutils\`." >> "$ITOG"

# --- сумма потраченного по всем логам ночи -----------------------------------
potracheno() {
  python3 - "$LOGI" <<'PY'
import json, pathlib, sys
s = 0.0
for p in pathlib.Path(sys.argv[1]).glob("*.jsonl"):
    for line in p.read_text(errors="ignore").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "result" and d.get("total_cost_usd"):
            s += float(d["total_cost_usd"])
print(f"{s:.2f}")
PY
}

# --- одно звено: имя · модель · файл захода ----------------------------------
zveno() {
  IMYA="$1"; MODEL="$2"; ZAHOD="$3"
  BYLO=$(potracheno)
  echo "════ $IMYA · модель $MODEL · потрачено \$$BYLO из \$$BUDZHET"
  if python3 -c "import sys; sys.exit(0 if $BYLO >= $BUDZHET else 1)"; then
    echo "🔴 БЮДЖЕТ ИСЧЕРПАН (\$$BYLO) — $IMYA не запускается, цепочка встала"
    { echo "## 🔴 ЦЕПОЧКА ВСТАЛА НА $IMYA — исчерпан бюджет"; echo "";
      echo "Потрачено \$$BYLO при потолке \$$BUDZHET. Звено не запускалось."; } >> "$ITOG"
    exit 2
  fi

  NACHALO=$(date +%s)
  PROMPT="Твой заход — файл $ARKA/$ZAHOD. Прочитай ТОЛЬКО его и то, что он называет поимённо; остальной проект не изучай. План, вопросы и отчёт пиши в этот же файл внизу (## ПЛАН / ## ВОПРОСЫ / ## ОТЧЁТ). Ничего сверх своей зоны не трогай. Работаешь ночью без человека: если упёрся в развилку, которую не решить — запиши её в ## ВОПРОСЫ и продолжай с тем вариантом, который считаешь верным, объяснив выбор."

  if [ -n "$TO" ]; then
    $TO "${TAJMAUT_MIN}m" claude -p --verbose --output-format stream-json \
      --model "$MODEL" --dangerously-skip-permissions "$PROMPT" </dev/null \
      > "$LOGI/$IMYA.jsonl" 2>"$LOGI/$IMYA.err"
  else
    claude -p --verbose --output-format stream-json \
      --model "$MODEL" --dangerously-skip-permissions "$PROMPT" </dev/null \
      > "$LOGI/$IMYA.jsonl" 2>"$LOGI/$IMYA.err"
  fi
  RC=$?
  MINUT=$(( ( $(date +%s) - NACHALO ) / 60 ))
  STALO=$(potracheno)
  ZVENO_USD=$(python3 -c "print(f'{$STALO - $BYLO:.2f}')")

  echo "──── $IMYA завершено: rc=$RC · $MINUT мин · \$$ZVENO_USD"
  { echo "## $IMYA"; echo "";
    echo "- код возврата: **$RC**$([ $RC -eq 124 ] && echo ' (обрыв по таймауту)')";
    echo "- время: **$MINUT мин**";
    echo "- стоимость звена: **\$$ZVENO_USD**, всего за ночь \$$STALO"; } >> "$ITOG"
}

# --- шлюз: собрать разметку скриптом и записать вердикт сборки ---------------
shlyuz() {
  REZHIM="$1"; IMYA="$2"
  echo "──── шлюз $IMYA: сборка режима $REZHIM"
  VYVOD=$(python3 "$ARKA/sobrat_razmetku.py" "$REZHIM" 2>&1)
  SRC=$?
  { echo "";
    echo "**Шлюз (0 токенов), \`sobrat_razmetku.py $REZHIM\`:** код $SRC";
    echo '```'; echo "$VYVOD"; echo '```'; echo ""; } >> "$ITOG"
  echo "$VYVOD" | head -3
}

# --- проверка, что звено вообще что-то сделало -------------------------------
zhivo() {
  FAJL="$1"; IMYA="$2"
  # ВНИМАНИЕ: `grep -vc` печатает 0 и при этом возвращает rc=1. Приписка
  # `|| echo 0` в этом месте добавляла ВТОРОЙ ноль, строка становилась «0 0»,
  # и сравнение падало с «integer expression expected» — поймано прогоном.
  STROK=$(grep -vc '^#' "$FAJL" 2>/dev/null)
  [ -z "$STROK" ] && STROK=0
  if [ "$STROK" -lt 1 ]; then
    echo "🔴 $IMYA не создало ни одной строки в $(basename "$FAJL") — среда сломана, цепочка встала"
    { echo "## 🔴 ЦЕПОЧКА ВСТАЛА ПОСЛЕ $IMYA"; echo "";
      echo "В \`$(basename "$FAJL")\` ноль содержательных строк. Это не брак разметки, а признак сломанной среды: следующие звенья запускать бессмысленно, они сожгут бюджет впустую. Смотри \`noch-logi/$IMYA.err\`."; } >> "$ITOG"
    exit 3
  fi
  echo "──── $IMYA живо: $STROK строк вердикта"
}

# ═════════════════════════════════════════════════════════════════════════════
echo "── предподготовка скелетов (0 токенов)"
python3 "$ARKA/prep_skelety.py" || { echo "🔴 скелеты не собрались — ночь не стартует"; exit 1; }

zveno  "H1-razmetka-osej"      opus   "kod_razmetka-osej.md"
zhivo  "$ARKA/verdikt-osej.tsv"        "H1-razmetka-osej"
shlyuz osi                             "H1-razmetka-osej"

zveno  "H2-razmetka-vladelca"  opus   "kod_razmetka-vladelca.md"
zhivo  "$ARKA/verdikt-vladelca.tsv"    "H2-razmetka-vladelca"
shlyuz vladelca                        "H2-razmetka-vladelca"
shlyuz chisla                          "H2-razmetka-vladelca"

zveno  "H3-inventar"           sonnet "kod_inventar-arhitektury.md"

VSEGO=$(potracheno)
{ echo "---"; echo "";
  echo "**Ночь закончена $(date '+%Y-%m-%d %H:%M'). Всего потрачено \$$VSEGO из \$$BUDZHET.**"; } >> "$ITOG"
echo "════ ГОТОВО. Потрачено \$$VSEGO. Итог — $ITOG"
