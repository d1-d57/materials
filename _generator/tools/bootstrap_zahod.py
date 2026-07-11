#!/usr/bin/env python3
"""Scaffold — генерит файл-заход `kod_<тема>.md` из `_studio/zhurnal/_TEMPLATE-zahod.md`
с ОБЯЗАТЕЛЬНЫМ контрактом зоны (ветка · зона · коммит · запрет).

Использование:
    python3 bootstrap_zahod.py <папка-арки> <тема> --branch <ветка> --zone "<пути>" [--model Sonnet]

Пример:
    python3 bootstrap_zahod.py _studio/zhurnal/2026-07-11_reserch-zadach zapusk \\
        --branch fibonacci-l1 --zone "graph-course/" --model Sonnet

Зачем: заход НИКОГДА не пишется с нуля — Cowork вызывает этот скрипт, и контракт зоны
вшивается автоматически (RUKOVODSTVO §Зона изменений и git). --branch и --zone ОБЯЗАТЕЛЬНЫ:
без ветки и зоны заход не создаётся в принципе. Cowork дозаполняет `<...>` (контекст, задача,
критерий, что читать). Владелец руками ничего не вставляет.

Идемпотентен: существующий kod-файл НЕ перезатирает. Только stdlib.
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials
TEMPLATE = REPO_ROOT / "_studio" / "zhurnal" / "_TEMPLATE-zahod.md"


def main(argv):
    p = argparse.ArgumentParser(
        description="Генерит kod_<тема>.md с вшитым контрактом зоны.",
        epilog="--branch и --zone обязательны: контракт зоны — не опция.",
    )
    p.add_argument("arka_dir", help="папка арки (относительно корня репо или абсолютная)")
    p.add_argument("tema", help="короткий слаг темы → имя файла kod_<тема>.md")
    p.add_argument("--branch", required=True, help="ветка, на которой работает заход")
    p.add_argument("--zone", required=True, help="пути зоны (что МОЖНО менять), одной строкой")
    p.add_argument("--model", default="Sonnet", help="модель (по умолчанию Sonnet)")
    a = p.parse_args(argv)

    if not TEMPLATE.is_file():
        print(f"ОШИБКА: шаблон не найден — {TEMPLATE}", file=sys.stderr)
        return 1

    arka = Path(a.arka_dir)
    if not arka.is_absolute():
        arka = REPO_ROOT / arka
    if not arka.is_dir():
        print(f"ОШИБКА: папка арки не найдена — {arka}", file=sys.stderr)
        return 1

    dst = arka / f"kod_{a.tema}.md"
    if dst.exists():
        print(f"ОШИБКА: заход уже существует — {dst} (не затираю)", file=sys.stderr)
        return 1

    text = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{ТЕМА}}", a.tema)
        .replace("{{МОДЕЛЬ}}", a.model)
        .replace("{{ВЕТКА}}", a.branch)
        .replace("{{ЗОНА}}", a.zone)
    )
    dst.write_text(text, encoding="utf-8")

    print(f"Готово: {dst}")
    print("Контракт зоны вшит (ветка/зона/коммит/запрет). Дальше Cowork дозаполняет <...>:")
    print("  контекст · цель · что читать (якоря) · задача + критерий-что-провалится.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
