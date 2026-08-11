#!/usr/bin/env python3
"""Единственный дом таблицы «имя модели → ARN» (Bedrock, `us-east-1`,
аккаунт `811345154057`).

    python3 _generator/tools/modeli.py <ввод>   # <канон> → <ARN>, rc=0
                                                 # нераспознано → список
                                                 # принимаемых имён в stderr, rc=1

ЗАЧЕМ. Под Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`) флаг `--model` принимает НЕ
словесный алиас, а полный ARN application inference profile — алиас
разворачивается в id модели, на который ключ не выдан, и прогон падает с
`AccessDenied`. `bootstrap_zahod.py` подставлял в терминальную команду
буквально `a.model.lower()`, то есть слово. Этот модуль разводит два
представления: человекочитаемое каноническое имя (для текста захода) и ARN
(для исполняемой команды) — и разбирает свободный ввод человека терпимо к
тому, как он думает о модели (регистр/разделители/устаревшие имена).
"""
import re
import sys

PREFIX = "arn:aws:bedrock:us-east-1:811345154057:application-inference-profile/"

# Таблица переносится ДОСЛОВНО из задания.
TABLICA = {
    "Opus 5": "d78ovu0ye0t4",
    "Sonnet 5": "gn8yl4ks1php",
    "Fable 5": "bd6ejgogwtde",
    "Opus 4.8": "wan1xtwl8oy8",
    "Sonnet 4.6": "dge7bavuds6y",
    "Haiku 4.5": "m1whrq3hqdll",
}

# Голое родовое имя → ТЕКУЩАЯ старшая модель (владелец подтвердил на интервью:
# совместимость со старыми командами журнала и докстрингом генератора).
RODOVYE = {
    "sonnet": "Sonnet 5",
    "opus": "Opus 5",
    "haiku": "Haiku 4.5",
    "fable": "Fable 5",
}


def _normalizovat(s):
    """Регистр и разделители (пробел/дефис/точка/подчёркивание) не важны."""
    s = re.sub(r"[\s\-_.]+", "", s.strip().lower())
    if s.startswith("claude"):
        s = s[len("claude"):]
    return s


_PO_NORME = {_normalizovat(имя): имя for имя in TABLICA}
_PO_NORME.update({rod: имя for rod, имя in RODOVYE.items()})


def razobrat(vvod):
    """`(канон, ARN)` по свободному вводу человека.

    Не распознала — поднимает `ValueError` с текстом, называющим ВСЕ
    принимаемые имена.
    """
    vvod = (vvod or "").strip()
    if vvod.startswith("arn:aws:bedrock:"):
        return vvod, vvod
    norma = _normalizovat(vvod)
    kanon = _PO_NORME.get(norma)
    if kanon is None:
        prinimaemye = ", ".join(sorted(set(TABLICA) | set(RODOVYE)))
        raise ValueError(
            f"не распознал модель «{vvod}». Принимаются: {prinimaemye} "
            f"(регистр/разделители/ведущее «claude» не важны) — или готовый "
            f"ARN (`{PREFIX}...`).")
    return kanon, PREFIX + TABLICA[kanon]


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("Таблица:")
        for имя, хвост in TABLICA.items():
            print(f"  {имя} → {PREFIX}{хвост}")
        print("Родовые имена: " + ", ".join(f"{r}→{k}" for r, k in RODOVYE.items()))
        return 0
    try:
        kanon, arn = razobrat(argv[0])
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    print(f"{kanon} → {arn}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
