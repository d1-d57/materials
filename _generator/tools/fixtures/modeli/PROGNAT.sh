#!/bin/sh
# TOOL-CONTRACT-COVERS: modeli.py
# ↑ ОХВАТ: разбор свободного ввода `--model` в каноническое имя + ARN
# (`modeli.razobrat` и CLI `modeli.py`).
#
# Запуск:  sh _generator/tools/fixtures/modeli/PROGNAT.sh
# Ожидание: последняя строка «ЛОВУШЕК: X из Y зелёных» при X = Y, exit 0.
#
# ЛОВУШКИ (не менее двенадцати, задание Ш3):
#   1.  sonnet → Sonnet 5 (родовое имя = текущая старшая модель)
#   2.  Sonnet → то же (регистр не важен)
#   3.  SONNET → то же (регистр не важен)
#   4.  Sonnet 5 → то же (каноническое имя дословно)
#   5.  sonnet-5 → то же (разделители не важны)
#   6.  Claude Sonnet 5 → то же (ведущее слово claude выкидывается)
#   7.  opus → Opus 5 (родовое имя = текущая старшая модель)
#   8.  Opus 4.8 → Opus 4.8 (устаревшее имя НЕ отказ, законное значение таблицы)
#   9.  haiku → Haiku 4.5 (родовое имя)
#   10. fable → Fable 5 (родовое имя)
#   11. готовый ARN → сквозняком без изменений (уже начинается с arn:aws:bedrock:)
#   12. марсоход → rc=1, в stderr список принимаемых имён
#   13. пустая строка → rc=1 (нераспознаваемое, не законное значение)
#   14. --help → rc=0 без трейсбека (обязателен по CLI-контракту)
set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)
P="$TOOLS/modeli.py"
ARN_PREFIX="arn:aws:bedrock:us-east-1:811345154057:application-inference-profile/"

VSEGO=0
ZELENYH=0

proverit() {  # <описание> <ввод> <ожидаемое ИМЯ→ARN одной строкой на stdout> <ожидаемый rc>
  OPIS="$1"; VVOD="$2"; OZHIDANIE="$3"; RC_OZH="$4"
  VSEGO=$((VSEGO + 1))
  OUT=$(python3 "$P" "$VVOD" 2>/tmp/modeli-fixture-err.$$) && RC=0 || RC=$?
  ERR=$(cat /tmp/modeli-fixture-err.$$); rm -f /tmp/modeli-fixture-err.$$
  if [ "$RC" != "$RC_OZH" ]; then
    echo "  ❌ $OPIS: rc=$RC, ожидался $RC_OZH. stdout=«$OUT» stderr=«$ERR»"
    return
  fi
  if [ "$RC_OZH" = "0" ]; then
    [ "$OUT" = "$OZHIDANIE" ] && { echo "  ✅ $OPIS"; ZELENYH=$((ZELENYH + 1)); } \
      || echo "  ❌ $OPIS: stdout=«$OUT», ожидался «$OZHIDANIE»"
  else
    echo "$ERR" | grep -q "$OZHIDANIE" && { echo "  ✅ $OPIS"; ZELENYH=$((ZELENYH + 1)); } \
      || echo "  ❌ $OPIS: stderr не содержит «$OZHIDANIE». stderr=«$ERR»"
  fi
}

proverit "1. sonnet → Sonnet 5"          "sonnet"           "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "2. Sonnet → Sonnet 5"          "Sonnet"           "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "3. SONNET → Sonnet 5"          "SONNET"           "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "4. Sonnet 5 → Sonnet 5"        "Sonnet 5"         "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "5. sonnet-5 → Sonnet 5"        "sonnet-5"         "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "6. Claude Sonnet 5 → Sonnet 5" "Claude Sonnet 5"  "Sonnet 5 → ${ARN_PREFIX}gn8yl4ks1php" 0
proverit "7. opus → Opus 5"              "opus"             "Opus 5 → ${ARN_PREFIX}d78ovu0ye0t4" 0
proverit "8. Opus 4.8 → Opus 4.8 (устаревшее — не отказ)" "Opus 4.8" "Opus 4.8 → ${ARN_PREFIX}wan1xtwl8oy8" 0
proverit "9. haiku → Haiku 4.5"          "haiku"            "Haiku 4.5 → ${ARN_PREFIX}m1whrq3hqdll" 0
proverit "10. fable → Fable 5"           "fable"            "Fable 5 → ${ARN_PREFIX}bd6ejgogwtde" 0

echo "── ловушка 11: готовый ARN → сквозняком без изменений"
VSEGO=$((VSEGO + 1))
CHUZHOJ_ARN="arn:aws:bedrock:us-east-1:811345154057:application-inference-profile/marsohod9000"
OUT11=$(python3 "$P" "$CHUZHOJ_ARN")
[ "$OUT11" = "$CHUZHOJ_ARN → $CHUZHOJ_ARN" ] && { echo "  ✅ 11. ARN проезжает НАСКВОЗЬ"; ZELENYH=$((ZELENYH + 1)); } \
  || echo "  ❌ 11. ARN искажён: «$OUT11»"

echo "── ловушка 12: марсоход → rc=1, список принимаемых имён в stderr"
VSEGO=$((VSEGO + 1))
if OUT12=$(python3 "$P" марсоход 2>/tmp/modeli-fixture-12.$$); then
  echo "  ❌ 12. нераспознаваемый ввод дал rc=0"
else
  ERR12=$(cat /tmp/modeli-fixture-12.$$)
  echo "$ERR12" | grep -q "Sonnet 5" && echo "$ERR12" | grep -q "sonnet" \
    && { echo "  ✅ 12. rc=1, список принимаемых имён в stderr"; ZELENYH=$((ZELENYH + 1)); } \
    || echo "  ❌ 12. rc=1, но список имён не найден в stderr: «$ERR12»"
fi
rm -f /tmp/modeli-fixture-12.$$

echo "── ловушка 13: пустая строка → rc=1"
VSEGO=$((VSEGO + 1))
if python3 "$P" "" >/dev/null 2>/tmp/modeli-fixture-13.$$; then
  echo "  ❌ 13. пустая строка дала rc=0"
else
  echo "  ✅ 13. пустая строка → rc=1"; ZELENYH=$((ZELENYH + 1))
fi
rm -f /tmp/modeli-fixture-13.$$

echo "── ловушка 14: --help → rc=0 без трейсбека"
VSEGO=$((VSEGO + 1))
if OUT14=$(python3 "$P" --help 2>&1); then
  echo "$OUT14" | grep -qi "traceback" && echo "  ❌ 14. --help дал трейсбек" \
    || { echo "  ✅ 14. --help → rc=0, без трейсбека"; ZELENYH=$((ZELENYH + 1)); }
else
  echo "  ❌ 14. --help вернул rc≠0"
fi

echo "ЛОВУШЕК: $ZELENYH из $VSEGO зелёных"
[ "$ZELENYH" = "$VSEGO" ] && exit 0 || exit 1
