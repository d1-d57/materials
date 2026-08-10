#!/bin/sh
# TOOL-CONTRACT-COVERS: bootstrap_zahod.py check_sborki.py
# Фикстуры РАЗДЕЛА «ГИГИЕНА». Гоняй ПОСЛЕ любой правки раздела в
# `bootstrap_zahod.py` (`gigiena_blok`, `_sosednij_repo`) или гейта С8 в
# `check_sborki.py`.
#
# Запуск:  sh _generator/tools/fixtures/gigiena/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Раздел ГИГИЕНА обязан рождаться в КАЖДОМ заходе (требование владельца
# 2026-08-09), а гейт С8 — краснеть на пустом слоте зоны. Оба свойства ломаются
# молча: раздел исчезает при разъезде анкора с шаблоном, гейт перестаёт краснеть
# при неверной регулярке — и ровно это уже случилось на первом живом прогоне
# (`\s*` вместо `[ \t]*` перепрыгивал пустую строку и захватывал следующую, то
# есть гейт на пустоту не краснел НИКОГДА). Ловушки 3 и 4 ниже сторожат именно
# этот класс: не «код написан», а «красное действительно наступает».
#
# 🔴 РАБОТАЕТ В ОДНОРАЗОВОМ РЕПОЗИТОРИИ. Генератор ПИШЕТ на диск (файл захода)
# и зовёт `register_doc.py` (строка в индекс) — гонять его по боевому дереву
# значило бы плодить мусорные заходы и мусорные строки `KARTA.md` при каждом
# прогоне хука. Приём тот же, что у `fixtures/register_doc` и `fixtures/korni`:
# инструменты копируются в `$T/_generator/tools/`, `korni.REPO` = `parents[2]`.
cd "$(dirname "$0")/../../../.." || exit 1
REPO=$(pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
fail=0

ok()   { echo "  ✅ $1"; }
bad()  { echo "  ❌ $1"; fail=1; }

# ── одноразовое дерево: инструменты + шаблон + индекс ────────────────────────
mkdir -p "$T/_generator" "$T/_studio/docs" "$T/_studio/zhurnal/proba-arka" "$T/zona-proby"
cp -R "$REPO/_generator/tools" "$T/_generator/tools" || exit 1
cp -R "$REPO/_generator/sborka" "$T/_generator/sborka" || exit 1
cp "$REPO/_studio/zhurnal/_TEMPLATE-zahod.md" "$T/_studio/zhurnal/" || exit 1
cp "$REPO/_studio/docs/KARTA.md" "$T/_studio/docs/KARTA.md" || exit 1
echo "заглушка" > "$T/zona-proby/README.md"
# 🔴 Дерево обязано быть ДОСТАТОЧНЫМ, а не минимальным: без `_INFRA-git/` и без
# файла, который шаблон называет в прозе, красными становятся С3/С6 — и ловушка
# «заполненный слот → зелёный» проверяла бы не то, что заявлено. Ложное красное
# в фикстуре стоит дороже пропуска: его перестают читать целиком.
cp -R "$REPO/_studio/zhurnal/_INFRA-git" "$T/_studio/zhurnal/_INFRA-git" || exit 1
mkdir -p "$T/_studio/zhurnal/2026-07-30_dovodka-fabriki"
cp "$REPO/_studio/zhurnal/2026-07-30_dovodka-fabriki/kod_registracia-bez-obhoda.md" \
   "$T/_studio/zhurnal/2026-07-30_dovodka-fabriki/" || exit 1
( cd "$T" && git init -q . && git add -A >/dev/null 2>&1 &&
  git -c user.email=f@f -c user.name=f commit -qm init >/dev/null 2>&1 &&
  git checkout -q -b zahod/proba ) || exit 1

Z="$T/_studio/zhurnal/proba-arka/kod_proba.md"
( cd "$T" && python3 _generator/tools/bootstrap_zahod.py _studio/zhurnal/proba-arka \
    proba --branch zahod/proba --zone "zona-proby/" --kanal app \
    --finalizirovano "ф1" --finalizirovano "ф2" \
    --opisanie "фикстура раздела ГИГИЕНА" ) > "$T/gen.log" 2>&1
if [ -f "$Z" ]; then ok "1. заход собрался"; else bad "1. заход НЕ собрался"; cat "$T/gen.log"; exit 1; fi

# ── ловушка 2: раздел рождается САМ, без единого флага под него ──────────────
if grep -q '^## 4\.1 .*ГИГИЕНА' "$Z"; then
    ok "2. раздел ГИГИЕНА рождается сам (флага под него нет вовсе)"
else
    bad "2. раздела ГИГИЕНА в свежесобранном заходе НЕТ"
fi

# ── ловушка 3: слот зоны заполнен из --zone, и гейт на этом ЗЕЛЁНЫЙ ──────────
if grep -q '^\*\*ЗОНА ГИГИЕНЫ:\*\* `zona-proby/`' "$Z"; then
    ok "3. слот зоны заполнен генератором из --zone"
else
    bad "3. слот зоны НЕ заполнен из --zone"
fi
( cd "$T" && python3 _generator/tools/check_sborki.py "$Z" ) > "$T/a.log" 2>&1
if [ $? -eq 0 ]; then ok "3б. заполненный слот — гейт ЗЕЛЁНЫЙ (rc=0)"
else bad "3б. заполненный слот, а гейт красный (rc=$?)"; grep '^❌' "$T/a.log"; fi

# ── ловушка 4: 🔴 ПУСТОЙ СЛОТ ОБЯЗАН КРАСНЕТЬ ────────────────────────────────
# Проверяется не «есть код проверки», а «красное наступает»: правило без того,
# что покраснеет, — надежда, а не правило (KONSTITUCIYA §11).
# Опустошаем ХВОСТ строки, каким бы он ни был: зона в разделе — это зона захода
# целиком (включая дописанный генератором путь файла-захода), и прибивать её
# литералом значит ломать ловушку при каждом изменении состава зоны. Ровно это и
# случилось на первом прогоне после починки — поймано строкой-сторожем ниже.
sed 's|^\*\*ЗОНА ГИГИЕНЫ:\*\* .*$|**ЗОНА ГИГИЕНЫ:**|' "$Z" > "$T/pusto.md"
if grep -q '^\*\*ЗОНА ГИГИЕНЫ:\*\*$' "$T/pusto.md"; then :
else bad "4. подготовка: слот не опустошён — ловушка НЕ проверена"; fi
( cd "$T" && python3 _generator/tools/check_sborki.py "$T/pusto.md" ) > "$T/b.log" 2>&1
rc=$?
if [ $rc -ne 0 ] && grep -q '❌ С8' "$T/b.log"; then
    ok "4. пустой слот зоны — С8 КРАСНЫЙ (rc=$rc)"
else
    bad "4. пустой слот зоны НЕ покраснел (rc=$rc) — гейт не краснеет никогда"
fi

# ── ловушка 5: раздела нет вовсе (заход собран руками) — С8 красный ──────────
grep -v '^## 4\.1 .*ГИГИЕНА' "$Z" | grep -v '^\*\*ЗОНА ГИГИЕНЫ:\*\*' > "$T/bez.md"
( cd "$T" && python3 _generator/tools/check_sborki.py "$T/bez.md" ) > "$T/c.log" 2>&1
if grep -q '❌ С8.*нет раздела' "$T/c.log"; then
    ok "5. заход без раздела (написан руками) — С8 красный"
else
    bad "5. заход без раздела прошёл гейт"
fi

# ── ловушка 6: Г2 различает «зона внутри репо» и «зона в соседнем репо» ──────
# Ложное «неприменимо, проверено при сборке» — та самая болезнь, ради которой
# заход и писался: соседний репозиторий забывали трижды за одни сутки.
if grep -q 'Г2\..*неприменимо' "$Z"; then
    ok "6. зона внутри репо — Г2 объявлен неприменимым ЯВНО, а не молча выброшен"
else
    bad "6. зона внутри репо, а Г2 не сказал «неприменимо»"
fi
SOSED=$(python3 - "$REPO" <<'PY'
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / "_generator" / "tools"))
import bootstrap_zahod as bz
R = pathlib.Path(sys.argv[1])
vnutri = bz._sosednij_repo("_generator/tools/", R)
snaruzhi = bz._sosednij_repo("disciplina/skills/", R)
print("OK" if vnutri is None and snaruzhi == "disciplina" else f"BAD {vnutri} {snaruzhi}")
PY
)
case "$SOSED" in
  OK) ok '6б. сосед disciplina виден И из worktree (дверь glavnyj_repo)' ;;
  *)  bad "6б. распознавание соседнего репозитория сломано: $SOSED" ;;
esac

# ── ловушка 7: Г3 несёт СНЯТУЮ базу сравнения, а не заглушку ────────────────
if grep -q 'Г3\..*branch --no-merged [a-zA-Z]' "$Z"; then
    ok "7. Г3 несёт снятую при сборке базу сравнения веток"
else
    bad "7. Г3 без базы сравнения — команда неисполнима"
fi

if [ $fail -eq 0 ]; then echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; else echo "ФИКСТУРЫ КРАСНЫЕ"; fi
exit $fail
