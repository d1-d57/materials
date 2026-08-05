#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: check_lenta.py
# Фикстуры гейта формы ленты (check_lenta.py, 2026-08-05).
# Гонять после каждой правки check_lenta.py:  bash _generator/tools/fixtures/lenta/PROGNAT.sh
#
# 🔴 Гейт, который может ПРОЙТИ, обязан иметь фикстуру, на которой он ПАДАЕТ, — иначе неизвестно,
# проверяет он что-нибудь или печатает зелёное в пустоту. Здесь четыре:
#   zdorovaya  — копия живого эталона: ЗЕЛЁНЫЙ. Красное здесь = ложный гейт, чинится ГЕЙТ;
#   slomannaya — та же копия с восемью точечными порчами: КРАСНЫЙ, и в вердикте обязаны быть
#                названы все восемь пунктов, а не «что-нибудь»;
#   povtor     — одна правка: две единицы с одинаковым заголовком (класс H, три слайда снял
#                владелец, ни одного — гейт): КРАСНЫЙ;
#   pustaya    — фронтматтер есть, содержания нет: КРАСНЫЙ. Пустая лента — не чистая лента.
set -u

KOREN="$(cd "$(dirname "$0")/../../.." && pwd)"
GATE="$KOREN/tools/check_lenta.py"
DVIZHOK="$KOREN/build_doc.py"
FIX="$(cd "$(dirname "$0")" && pwd)"
PNG_ETALON="$KOREN/../_studio/konvejer/06-tekst/ETALON-png"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

pusk () {                       # pusk <имя> <ожидаемый-код> [<ожидаемые пункты через пробел>]
  imya="$1"; zhdem="$2"; shift 2
  rabota="$TMP/$imya"
  mkdir -p "$rabota"
  cp "$FIX/$imya/lenta.md" "$rabota/lenta.md"
  cp -R "$PNG_ETALON" "$rabota/lenta-png" 2>/dev/null || true
  python3 "$DVIZHOK" "$rabota" >/dev/null 2>&1
  vyvod="$(python3 "$GATE" "$rabota/lenta.md" 2>&1)"
  got=$?
  if [ "$got" != "$zhdem" ]; then
    echo "  ✗ $imya: код $got, ожидался $zhdem"
    OK=1
  else
    echo "  ✓ $imya: код $got"
  fi
  for p in "$@"; do
    if ! printf '%s' "$vyvod" | grep -q "^     $p "; then
      echo "      ✗ пункт $p не назван в вердикте — порча этого пункта прошла мимо"
      OK=1
    fi
  done
}

echo "── ФИКСТУРЫ ГЕЙТА ФОРМЫ ЛЕНТЫ ──"
pusk "zdorovaya"  0
pusk "slomannaya" 1  L1 L2 L3 L4 L5 L6 L7 L11
pusk "povtor"     1  L8
pusk "pustaya"    1  L7

echo "── ИТОГ: $([ $OK = 0 ] && echo 'всё как ожидалось' || echo 'ЕСТЬ РАСХОЖДЕНИЯ')"
exit $OK
