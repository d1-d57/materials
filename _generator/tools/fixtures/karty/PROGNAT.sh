#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: check_karty.py
# Фикстуры гейта согласованности карты (check_karty.py, 2026-08-09).
# Гонять после каждой правки: bash _generator/tools/fixtures/karty/PROGNAT.sh
#
# 🔴 ГЕЙТ, НЕ ПРОВЕРЕННЫЙ НА РАЗРЫВЕ, НЕ ПРОВЕРЕН ВОВСЕ. Реестр строится ровно для
# того, чтобы карта не протухла в третий раз; если гейт не краснеет на порванной
# согласованности, мы получили третью прозу, только в табличной обёртке.
# Ловушки — по одной на КАЖДЫЙ инвариант, плюс зелёная, плюс две на форму:
#   1  И1 · новый .py на диске без строки реестра
#   2  И2 · строка реестра без файла
#   3  И3 · ЖИВОЙ без кто-зовёт, и без объявления причины
#   4  И4 · фаза называет гейтом инструмент, которого нет
#   5  зелёная · всё согласовано
#   6  ФОРМА · клетка пуста МОЛЧА (прочерк вместо `нет: <причина>`)
#   7  И3 · реестр объявляет «зовущего нет», а он есть — реестр отстал от дерева
#   8  И4 · у фазы нет .py-гейта и нет объявления «нет .py-гейта:»
#   9  законная пустота с причиной — зелёная, но объявленная вслух
#
# 🔴 ФИКСТУРА НЕ ПИШЕТ В ПРОВЕРЯЕМЫЙ РЕПОЗИТОРИЙ: всё дерево одноразовое (`mktemp -d`),
# гейт наводится на него через `KARTY_REPO`, а вызываемый им `check_tool_contract.py` —
# через `GIT_ZONA_REPO`/`TOOL_CONTRACT_HOME`. Иначе каждый прогон регресса пачкал бы
# зону и ронял Г1 у того, кто регресс прогнал (урок захода `gigiena-i-svedenie`).
set -u

GATE="$(cd "$(dirname "$0")/../.." && pwd)/check_karty.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

T="$TMP/derevo"
KARTA="$T/_studio/konvejer/KARTA-ZHIVOGO-KONVEJERA.md"
mkdir -p "$T/_generator/tools" "$T/_generator/sborka" "$T/_studio/konvejer"

# Два инструмента: `pod_zovom.py` зовут (его basename назван в теле `zovushchij.py`),
# `zovushchij.py` зовёт сам себя из хука — оба зелёные по «живой точке вызова».
cat > "$T/_generator/tools/pod_zovom.py" <<'PY'
#!/usr/bin/env python3
"""Гейт-пример: его зовут."""
PY
cat > "$T/_generator/tools/zovushchij.py" <<'PY'
#!/usr/bin/env python3
"""Зовёт pod_zovom.py — так у того появляется живая точка вызова."""
PY
mkdir -p "$T/.githooks"
cat > "$T/.githooks/pre-commit" <<'SH'
#!/bin/sh
# zovushchij.py
SH

# Шапка карты: таблица фаз §1 (колонка «Гейт» — пятая) и раздел реестра §5.
sobrat_kartu () {              # sobrat_kartu <гейт-фазы-1> <строки-реестра-файл>
  {
    echo "## 1. Живой конвейер Ф1…Ф7 — одной таблицей"
    echo
    echo "| Фаза | Решение фазы | Артефакт | Дом на диске | Гейт | Верификатор |"
    echo "|---|---|---|---|---|---|"
    echo "| **1 · Проба** | решение | артефакт | дом | $1 | свежий агент |"
    echo
    echo "## 5. РЕЕСТР ИНСТРУМЕНТОВ — машиночитаемый, сторожится гейтом"
    echo
    echo "| файл | фаза / роль | кто зовёт | чем проверен | статус |"
    echo "|---|---|---|---|---|"
    cat "$2"
    echo
    echo "## 6. Хвост"
  } > "$KARTA"
}

reestr_bazovyj () {
  cat > "$TMP/reestr.md" <<'MD'
| `_generator/tools/pod_zovom.py` | Ф1 · проба | инстр.: `zovushchij.py` | `fixtures/karty/PROGNAT.sh` | ЖИВ |
| `_generator/tools/zovushchij.py` | инфраструктура | хук `.githooks/pre-commit` | `fixtures/karty/PROGNAT.sh` | ЖИВ |
MD
}

pusk () {                      # pusk <имя> <ожидаемый-код> <ожидаемая-подстрока|->
  KARTY_REPO="$T" GIT_ZONA_REPO="$T" TOOL_CONTRACT_HOME="$T/_generator/tools" \
    python3 "$GATE" > "$TMP/$1.out" 2>&1
  got=$?
  if [ "$got" != "$2" ]; then
    echo "  ✗ $1: код $got, ожидался $2"
    cat "$TMP/$1.out"
    OK=1
    return
  fi
  if [ "$3" != "-" ] && ! grep -q "$3" "$TMP/$1.out"; then
    echo "  ✗ $1: код верный ($got), но в выводе нет «$3» — виновник не назван"
    cat "$TMP/$1.out"
    OK=1
    return
  fi
  echo "  ✓ $1: код $got"
}

echo "── ФИКСТУРЫ ГЕЙТА СОГЛАСОВАННОСТИ КАРТЫ ──"

# 5 (первой: базовое состояние обязано быть зелёным, иначе остальные ловушки лгут).
reestr_bazovyj
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "5-vsyo-soglasovano" 0 "ГЕЙТ СОГЛАСОВАННОСТИ: реестр сходится"

# 1 · И1: новый инструмент на диске, строки в реестре нет.
cat > "$T/_generator/sborka/novyj.py" <<'PY'
#!/usr/bin/env python3
"""Новый инструмент, вписать в реестр забыли."""
PY
pusk "1-i1-net-stroki" 1 "_generator/sborka/novyj.py"
rm -f "$T/_generator/sborka/novyj.py"

# 2 · И2: строка реестра есть, файла нет.
reestr_bazovyj
echo '| `_generator/tools/prizrak.py` | инфраструктура | хук | `fixtures/karty/PROGNAT.sh` | ЖИВ |' >> "$TMP/reestr.md"
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "2-i2-net-fajla" 1 "prizrak.py"

# 3 · И3: ЖИВОЙ, которого никто не зовёт, и причина не объявлена.
cat > "$T/_generator/tools/sirota.py" <<'PY'
#!/usr/bin/env python3
"""Инструмент, которого не зовёт никто."""
PY
reestr_bazovyj
echo '| `_generator/tools/sirota.py` | инфраструктура | хук `.githooks/pre-commit` | `fixtures/karty/PROGNAT.sh` | ЖИВ |' >> "$TMP/reestr.md"
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "3-i3-zhivoj-bez-zovushchego" 1 "sirota.py"

# 9 · та же сирота, но пустота ОБЪЯВЛЕНА с причиной — зелёное и напечатанное вслух.
reestr_bazovyj
echo '| `_generator/tools/sirota.py` | инфраструктура | нет: точки вызова нет, дом хука вне зоны — пункт очереди | `fixtures/karty/PROGNAT.sh` | ЖИВ |' >> "$TMP/reestr.md"
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "9-zakonnaya-pustota-zelyonaya" 0 "объявленных пустот"
rm -f "$T/_generator/tools/sirota.py"

# 7 · И3 в обратную сторону: реестр объявляет «зовущего нет», а эвристика его находит.
# 🔴 ЭТО НЕ КРАСНОЕ, А НАПЕЧАТАННОЕ РАСХОЖДЕНИЕ — и ловушка сторожит именно это.
# Первая редакция краснела здесь, и независимая сверка показала, почему это неверно:
# `has_live_trigger` считает вызовом упоминание имени в докстринге соседа, а реестр
# заполняется замером настоящих вызовов и потому строже. Красное наказывало бы за
# правду; но и молчать нельзя — расхождение печатается поимённо.
reestr_bazovyj
cat > "$TMP/reestr.md" <<'MD'
| `_generator/tools/pod_zovom.py` | Ф1 · проба | нет: зовущего не нашлось | `fixtures/karty/PROGNAT.sh` | ЖИВ |
| `_generator/tools/zovushchij.py` | инфраструктура | хук `.githooks/pre-commit` | `fixtures/karty/PROGNAT.sh` | ЖИВ |
MD
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "7-i3-rashozhdenie-napechatano" 0 "расхождение по"

# 4 · И4: фаза называет гейтом инструмент, которого нет ни в реестре, ни на диске.
reestr_bazovyj
sobrat_kartu '`net_takogo.py`' "$TMP/reestr.md"
pusk "4-i4-gejt-fazy-ne-sushchestvuet" 1 "net_takogo.py"

# 8 · И4: у фазы не назван ни один .py и нет объявления «нет .py-гейта:».
reestr_bazovyj
sobrat_kartu 'глазами владельца' "$TMP/reestr.md"
pusk "8-i4-pustaya-kletka-molcha" 1 "не назван НИ ОДИН инструмент"

# 8б · та же клетка, но с объявлением — зелёное.
reestr_bazovyj
sobrat_kartu 'глазами владельца · **нет .py-гейта:** проверка авторская, инструмента нет' "$TMP/reestr.md"
pusk "8b-obyavlennoe-otsutstvie-gejta" 0 "-"

# 6 · ФОРМА: клетка «чем проверен» — прочерк вместо `нет: <причина>`.
reestr_bazovyj
cat > "$TMP/reestr.md" <<'MD'
| `_generator/tools/pod_zovom.py` | Ф1 · проба | инстр.: `zovushchij.py` | — | ЖИВ |
| `_generator/tools/zovushchij.py` | инфраструктура | хук `.githooks/pre-commit` | `fixtures/karty/PROGNAT.sh` | ЖИВ |
MD
sobrat_kartu '`pod_zovom.py`' "$TMP/reestr.md"
pusk "6-forma-pustaya-kletka" 1 "пуста МОЛЧА"

if [ "$OK" = "0" ]; then
  echo "✅ ФИКСТУРЫ КАРТЫ: все ловушки сработали."
else
  echo "❌ ФИКСТУРЫ КАРТЫ: есть провалы (см. выше)."
fi
exit "$OK"
