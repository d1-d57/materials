#!/bin/bash
# ЦЕПОЧКА НОЧИ, ЧАСТЬ 2 — остаток после принятого H1.
#
#   bash /Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-07-30_dovodka-fabriki/noch-2.sh
#
# H1 уже сдан (461 из 461, шлюз зелёный) и здесь НЕ перезапускается — отдельный
# файл нужен именно затем, чтобы принятая работа не ушла в повторный прогон.
#
# ЧТО ИЗМЕНИЛОСЬ ПРОТИВ noch.sh — три вещи, каждая оплачена прогоном H1:
#
# 1. СЧЁТ БЮДЖЕТА. `total_cost_usd` накопительный по сессии, а result-строк в
#    логе несколько. Наивная сумма дала $42.93 при реальных $25.03 и остановила
#    ночь вхолостую. Теперь: максимум внутри session_id, сумма по сессиям.
# 2. ДРОБЛЕНИЕ H2. Основная статья расхода H1 — не выход (221k токенов), а
#    кэш-чтение: 33 млн за 126 ходов, потому что контекст перечитывается на
#    каждом ходу. Четыре сессии по ~345 записей вместо одной на 1379.
# 3. ОТДЕЛЬНЫЙ СЧЁТ. Логи этой цепочки лежат в своей папке, потолок $80
#    относится к ОСТАТКУ и не включает уже потраченные на H1 $25.04.
set -u

REPO=/Users/ivanyakovlev/Documents/GitHub/materials
ARKA="$REPO/_studio/zhurnal/2026-07-30_dovodka-fabriki"
LOGI="$ARKA/noch-logi-2"
ITOG="$ARKA/ITOG-nochi-2.md"
BUDZHET=80.0
TAJMAUT_MIN=120

mkdir -p "$LOGI"
cd "$REPO" || exit 1

TO=""
command -v timeout  >/dev/null 2>&1 && TO="timeout"
command -v gtimeout >/dev/null 2>&1 && TO="gtimeout"

{ echo "# ИТОГ НОЧИ, ЧАСТЬ 2 — печатает noch-2.sh, руками не править"; echo "";
  echo "Старт: $(date '+%Y-%m-%d %H:%M') · потолок \$$BUDZHET на остаток (H1 со своими \$25.04 сюда не входит)"; echo ""; } > "$ITOG"
[ -z "$TO" ] && echo "⚠ \`timeout\` не найден — звенья идут без потолка по времени (\`brew install coreutils\`)." >> "$ITOG"

potracheno() {
  python3 - "$LOGI" <<'PY'
import json, pathlib, sys
po_sessii = {}
for p in pathlib.Path(sys.argv[1]).glob("*.jsonl"):
    for line in p.read_text(errors="ignore").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "result" and d.get("total_cost_usd"):
            k = (p.name, d.get("session_id") or "—")
            po_sessii[k] = max(po_sessii.get(k, 0.0), float(d["total_cost_usd"]))
print(f"{sum(po_sessii.values()):.2f}")
PY
}

# zveno <имя> <модель> <файл захода> <довесок к промпту>
zveno() {
  IMYA="$1"; MODEL="$2"; ZAHOD="$3"; DOVESOK="$4"
  BYLO=$(potracheno)
  echo "════ $IMYA · $MODEL · потрачено \$$BYLO из \$$BUDZHET"
  if python3 -c "import sys; sys.exit(0 if $BYLO >= $BUDZHET else 1)"; then
    echo "🔴 БЮДЖЕТ ИСЧЕРПАН (\$$BYLO) — $IMYA не запускается"
    { echo "## 🔴 ЦЕПОЧКА ВСТАЛА НА $IMYA — исчерпан бюджет"; echo "";
      echo "Потрачено \$$BYLO при потолке \$$BUDZHET. Работа предыдущих звеньев цела: вердикты пишутся дописыванием, и следующая пачка стартует с той же границы."; } >> "$ITOG"
    exit 2
  fi

  NACHALO=$(date +%s)
  PROMPT="Твой заход — файл $ARKA/$ZAHOD. Прочитай ТОЛЬКО его и то, что он называет поимённо; остальной проект не изучай. План, вопросы и отчёт пиши в этот же файл внизу (## ПЛАН / ## ВОПРОСЫ / ## ОТЧЁТ). Ничего сверх своей зоны не трогай. Работаешь ночью без человека: упёрся в развилку — запиши её в ## ВОПРОСЫ и продолжай с тем вариантом, который считаешь верным, объяснив выбор. $DOVESOK"

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
  STROK=$(grep -vc '^#' "$ARKA/verdikt-vladelca.tsv" 2>/dev/null); [ -z "$STROK" ] && STROK=0

  echo "──── $IMYA: rc=$RC · $MINUT мин · \$$ZVENO_USD · вердиктов всего $STROK"
  { echo "## $IMYA"; echo "";
    echo "- код возврата: **$RC**$([ $RC -eq 124 ] && echo ' (обрыв по таймауту)')";
    echo "- время: **$MINUT мин** · стоимость **\$$ZVENO_USD** · всего за часть 2 \$$STALO";
    echo "- строк в \`verdikt-vladelca.tsv\` после звена: **$STROK**"; echo ""; } >> "$ITOG"
}

# ═════════════════════════════════════════════════════════════════════════════
echo "── пересборка скелетов (0 токенов; заголовки и цитаты больше не обрезаны)"
python3 "$ARKA/prep_skelety.py" || { echo "🔴 скелеты не собрались — цепочка не стартует"; exit 1; }

zveno "H2a" opus "kod_razmetka-vladelca.md" "ТВОЙ ДИАПАЗОН: V0001–V0345, ровно 345 записей. Записи вне диапазона не трогай."
zveno "H2b" opus "kod_razmetka-vladelca.md" "ТВОЙ ДИАПАЗОН: V0346–V0690, ровно 345 записей. Вердикты пачки V0001–V0345 уже лежат в файле: дописывай в конец, чужие строки не трогай и файл не сортируй."
zveno "H2c" opus "kod_razmetka-vladelca.md" "ТВОЙ ДИАПАЗОН: V0691–V1035, ровно 345 записей. Вердикты V0001–V0690 уже лежат в файле: дописывай в конец, чужие строки не трогай."
zveno "H2d" opus "kod_razmetka-vladelca.md" "ТВОЙ ДИАПАЗОН: V1036–V1379, ровно 344 записи — последняя пачка. Дописав свои, прогони sobrat_razmetku.py vladelca: теперь он обязан стать ЗЕЛЁНЫМ на всех 1379. Красный — чини вердикты (свои и, если видишь брак формата, чужие). После зелёного напиши раздел РАЗБОР в POKRYTIE-karkasa.md по четырём пунктам заходa."
zveno "H2e-chisla" opus "kod_razmetka-vladelca.md" "ТВОЯ ЧАСТЬ — ТОЛЬКО ЧИСЛА: заполни verdikt-chisla.tsv по всем 269 строкам skelet-chisla.tsv (id, ПРИ КАКОМ МАСШТАБЕ, ФОРМА) и добейся зелёного sobrat_razmetku.py chisla. Ярусы уже размечены другими пачками — verdikt-vladelca.tsv не трогай."

echo "──── финальные шлюзы (0 токенов)"
for R in vladelca chisla; do
  V=$(python3 "$ARKA/sobrat_razmetku.py" "$R" 2>&1); S=$?
  { echo "**Шлюз \`sobrat_razmetku.py $R\`: код $S**"; echo '```'; echo "$V"; echo '```'; echo ""; } >> "$ITOG"
  echo "$V" | head -3
done

zveno "H3-inventar" sonnet "kod_inventar-arhitektury.md" ""

VSEGO=$(potracheno)
{ echo "---"; echo "";
  echo "**Часть 2 закончена $(date '+%Y-%m-%d %H:%M'). Потрачено \$$VSEGO из \$$BUDZHET.**"; } >> "$ITOG"
echo "════ ГОТОВО. Потрачено \$$VSEGO. Итог — $ITOG"
