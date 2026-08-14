#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: kadry.py
# Фикстуры скриншотера характерных слайдов (kadry.py, заход pravila-kadra Э6).
# Гонять после каждой правки:  bash _generator/tools/fixtures/kadry/PROGNAT.sh
#
# Три исхода rc — RC_MISUSE(2)/RC_DEFECT(1)/RC_OK(0) — и каждый должен быть
# ДОСТИЖИМ реальным вызовом, не только присутствовать в коде:
#   net_papki   — папки лекции не существует: rc=2 (позвали неверно), не 1.
#   net_dista   — `--dist` указывает на несуществующий файл: rc=2.
#   pusto       — пустая (валидная) папка лекции: `sborka/deck.py` внутри упадёт
#                 на отсутствии slajdy/brief.md — rc=1 («инструмент запустился,
#                 но не смог» — это дефект входа лекции, не вызова kadry.py).
#   zhivoj_dist — готовый собранный дек (`fixtures/sborka/zhivoj-teorkat/dist/
#                 index.html`, 3 слайда) через `--dist`: не пересобирает,
#                 сразу скриншотит — rc=0 и минимум один PNG на диске.
set -u

KOREN="$(cd "$(dirname "$0")/../../.." && pwd)"          # = .../_generator
KADRY="$KOREN/tools/kadry.py"
FIX="$(cd "$(dirname "$0")" && pwd)"
ZHIVOJ_DIST="$KOREN/tools/fixtures/sborka/zhivoj-teorkat/dist/index.html"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

pusk () {                       # pusk <имя> <ожидаемый-код> -- <аргументы kadry.py>
  imya="$1"; zhdem="$2"; shift 2
  if [ "$1" = "--" ]; then shift; fi
  python3 "$KADRY" "$@" >"$TMP/$imya.out" 2>&1
  got=$?
  if [ "$got" != "$zhdem" ]; then
    echo "  ✗ $imya: код $got, ожидался $zhdem"
    echo "    вывод: $(tail -3 "$TMP/$imya.out")"
    OK=1
  else
    echo "  ✓ $imya: код $got"
  fi
}

echo "── ФИКСТУРЫ kadry.py ──"
pusk "net_papki" 2 -- "$TMP/net-takoj-papki" --out "$TMP/out1"
pusk "net_dista" 2 -- "$KOREN" --dist "$TMP/net-takogo-fajla.html" --out "$TMP/out2"

mkdir -p "$TMP/pustaya-lekcia"
pusk "pusto" 1 -- "$TMP/pustaya-lekcia" --out "$TMP/out3"

pusk "zhivoj_dist" 0 -- "$KOREN" --dist "$ZHIVOJ_DIST" --out "$TMP/out4"
if [ "$OK" = 0 ]; then
  n=$(find "$TMP/out4" -name '*.png' 2>/dev/null | wc -l | tr -d ' ')
  if [ "${n:-0}" -lt 1 ]; then
    echo "  ✗ zhivoj_dist: rc=0, но ни одного PNG в $TMP/out4"
    OK=1
  else
    echo "  ✓ zhivoj_dist: $n PNG на диске"
  fi
fi

echo "── ИТОГ: $([ $OK = 0 ] && echo 'всё как ожидалось' || echo 'ЕСТЬ РАСХОЖДЕНИЯ')"
exit $OK
