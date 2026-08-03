#!/usr/bin/env python3
"""ЗАКРЫТИЕ СЕССИИ — выгружает знание из транскрипта, пока оно не забылось.

    python3 _generator/tools/zakryt_sessiyu.py <папка-арки>
    python3 _generator/tools/zakryt_sessiyu.py <папка-арки> --transcript <путь.jsonl>
    python3 _generator/tools/zakryt_sessiyu.py <папка-арки> --spisok

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Владелец наговаривает голосом: реплики длинные, рваные, с самоперебиванием, и
требование часто лежит в середине фразы про другое. Аналитик отвечает на то,
что услышал, — и теряет остальное. Проверка 03.08 независимым субагентом на
транскрипте этой самой арки нашла СЕМЬ потерь за одну сессию, среди них два
прямых переспроса владельца («что ты имеешь в виду под работой с кодом?»),
оставшихся без ответа, и его же вопрос о критерии завершения всей затеи.

Владелец сформулировал лечение сам: *«всегда питоном вычитывали весь
транскрипт… и записывали это куда-то, чтобы ничего точно не потерять»* — и
отдельно отметил, что это НЕ СТОИТ ТОКЕНОВ, в отличие от чтения моделью.

🔴 ГЛАВНОЕ ПРОЕКТНОЕ РЕШЕНИЕ: скрипт НЕ РЕШАЕТ, что важно.
Он выгружает ВСЕ реплики владельца дословно и размечает их эвристиками.
Решать, что важно, — работа аналитика, и она делается ПОСЛЕ выгрузки, глядя на
полный текст. Скрипт, который «умно фильтрует», потерял бы ровно то, что теряет
человек: сказанное вскользь.

Только stdlib.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Маркеры, по которым реплика помечается — НЕ отбрасывается, а именно помечается.
MARKERY = {
    "решение":   r"\b(давай|надо|нужно|должно|должен|обязательно|решил|решаем|выбираю|предлагаю)\b",
    "запрет":    r"\b(не надо|не нужно|нельзя|не делай|не хочу|запрещ|перестань|не буду)\b",
    "боль":      r"\b(бесит|проблем|плохо|ужас|кошмар|не нравится|не устраивает|мешает|раздражает|боюсь)\b",
    "вопрос":    r"\?",
    # ЛОВУШКА, пойманная прогоном: `(доллар)\b` не ловит «40 долларов» — граница
    # слова стоит после окончания, а не после корня. Поэтому корни с `\w*`.
    "число":     (r"(\d[\d\s.,]*|\bодин|\bдва|\bтри|\bчетыре|\bпять|\bшесть|\bсем|\bвосем|\bдевят|\bдесят|\bсотн|\bтысяч)"
                  r"\s*(%|процент\w*|доллар\w*|\$|минут\w*|час\w*|секунд\w*|дн(я|ей)|недел\w*|месяц\w*|"
                  r"слайд\w*|страниц\w*|запис\w*|штук\w*|раз\b|лекци\w*|задач\w*|токен\w*)"
                  r"|\$\s*\d"),
    "отложено":  r"\b(потом|позже|отложим|в следующий раз|не сейчас|когда-нибудь|в какой-то момент)\b",
}

OBESHCHANIYA = r"\b(сделаю|напишу|запишу|починю|проверю|разберу|соберу|добавлю|учту|верну?сь)\b"

# Маркер ответа владельца, пришедшего через виджет интервью (AskUserQuestion).
# Строка задаётся хостом и по-английски даже в русском чате — от языка сессии
# не зависит. Живёт здесь одной константой, чтобы фикстура ловила ровно её.
OTVET_VIDZHETA = "The user answered"


def najti_transcript(yavnyj):
    """Найти файл транскрипта. Явный путь важнее поиска.

    🔴 БЕЗ АННОТАЦИИ ТИПА НАРОЧНО. Здесь стояло `yavnyj: str | None` — синтаксис
    PEP 604, он появился в Python 3.10. Песочница аналитика новее машины
    владельца, поэтому у аналитика скрипт работал, а на боевой машине упал:
    `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'` —
    и уронил коммит вместе с фикстурой. Тот же класс, что «скиллы Cowork
    недоступны в Claude Code»: СРЕДА АНАЛИТИКА НЕ РАВНА СРЕДЕ ИСПОЛНЕНИЯ.
    Ловушка на этот синтаксис стоит в `fixtures/sessiya/PROGNAT.sh`.
    """
    if yavnyj:
        p = Path(yavnyj).expanduser()
        if not p.exists():
            sys.exit(f"❌ транскрипт не найден: {p}")
        return p

    # Известные места, где Claude держит транскрипты. Порядок — от частого к редкому.
    #
    # 🔴 ЦЕНА ПЕРВОЙ СТРОКИ СПИСКА, оплачена 03.08 в тот же день, что и сам файл.
    # Аналитик запустил скрипт из песочницы Cowork, ничего не нашёл и объявил
    # владельцу, что инструмент в этой среде не запускается в принципе. Владелец
    # не поверил — и был прав. В песочнице `~` это `/sessions/<имя>/`, а папка
    # транскриптов смонтирована уровнем ниже, в `<mnt>/.claude/projects/`, так
    # что `~/.claude/projects` мимо. Тот же класс, что аннотация типа ниже:
    # СРЕДА АНАЛИТИКА НЕ РАВНА СРЕДЕ ИСПОЛНЕНИЯ — и здесь она не равна даже
    # самой себе на соседней машине. Поэтому шаблонов НЕСКОЛЬКО, и «не нашёл»
    # никогда не значит «здесь не бывает».
    kandidaty: list[Path] = []
    for shablon in (
        "~/.claude/projects/*/*.jsonl",
        "/sessions/*/mnt/.claude/projects/*/*.jsonl",   # песочница Cowork
        "~/mnt/.claude/projects/*/*.jsonl",             # она же, от домашней папки
        "/var/folders/*/*/T/claude-hostloop-plugins/*/projects/*/*.jsonl",
        "~/Library/Application Support/Claude/**/*.jsonl",
    ):
        rasshirennyj = os.path.expanduser(shablon)
        try:
            out = subprocess.run(["bash", "-lc", f"ls -1t {rasshirennyj} 2>/dev/null | head -40"],
                                 capture_output=True, text=True, timeout=20).stdout
        except Exception:
            continue
        kandidaty += [Path(s) for s in out.split("\n") if s.strip()]

    kandidaty = [p for p in kandidaty if p.exists()]
    if not kandidaty:
        sys.exit("❌ транскрипт не найден автоматически. Передай путь: --transcript <файл.jsonl>\n"
                 "   Найти можно так: ls -1t ~/.claude/projects/*/*.jsonl | head")
    return max(kandidaty, key=lambda p: p.stat().st_mtime)


def tekst_bloka(soobshchenie) -> str:
    """Достать текст из записи транскрипта, какой бы формы она ни была.

    Форматы менялись и будут меняться. Поэтому: пробуем известные, а незнакомую
    форму НЕ ГЛОТАЕМ молча — она попадёт в счётчик `neponyatnyh`, и он печатается.
    """
    if isinstance(soobshchenie, str):
        return soobshchenie
    if isinstance(soobshchenie, list):
        return "\n".join(tekst_bloka(b) for b in soobshchenie)
    if isinstance(soobshchenie, dict):
        if soobshchenie.get("type") == "text" and "text" in soobshchenie:
            return soobshchenie["text"]
        if "content" in soobshchenie:
            return tekst_bloka(soobshchenie["content"])
        if "text" in soobshchenie:
            return soobshchenie["text"]
    return ""


def razobrat(path: Path):
    vladelec, analitik, neponyatnyh, vsego = [], [], 0, 0
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        vsego += 1
        try:
            d = json.loads(line)
        except Exception:
            neponyatnyh += 1
            continue
        rol = d.get("type") or (d.get("message") or {}).get("role")
        t = tekst_bloka(d.get("message") or d)
        t = re.sub(r"<[^>]{1,40}>", " ", t)          # служебные теги
        t = re.sub(r"[ \t]+", " ", t).strip()
        if not t or len(t) < 25:
            continue
        if rol in ("user", "human"):
            # 🔴 РЕПЛИКА ВЛАДЕЛЬЦА ОПОЗНАЁТСЯ ПО СТРУКТУРЕ, А НЕ ПО ГРЕПУ.
            # Здесь стояло `"tool_result" not in line[:400]`, и это отбрасывало
            # ЦЕЛЫЙ КЛАСС реплик владельца: ответы на интервью через виджет
            # AskUserQuestion приходят в транскрипт именно как `tool_result`
            # с текстом «The user answered: …». Поймано 03.08 на живом файле
            # этой самой сессии: владелец продиктовал в виджет два абзаца про
            # базу инцидентов и предохранитель — выгрузка потеряла бы их молча
            # и выглядела бы как «владелец ничего не говорил». Худший вид
            # поломки для этого инструмента (см. ловушку 3 фикстуры).
            #
            # Структурное правило: `content` строкой — владелец набрал сам;
            # `content` списком — смотрим на ТИПЫ блоков, а не на сам факт списка.
            #
            # 🔴 ВТОРАЯ ЦЕНА ЭТОГО МЕСТА, оплачена в тот же день. Первая редакция
            # структурного правила гласила «`content` списком — результаты
            # инструментов», и это ложно: роль `user` приходит списком `text`-блоков
            # тоже — когда клиент заворачивает обычное сообщение в блоки, и всегда,
            # когда владелец шлёт текст с вложением (`text` + `image`). Замер по 40
            # живым транскриптам: у роли `user` формы `list:tool_result` 4300,
            # `str` 252, `list:text` 2. Редкая — но это ровно тот класс потери,
            # против которого написан весь файл, и поймал её не разбор, а
            # положительный контроль фикстуры: он покраснел на первом же коммите.
            # Урок дословно тот же, что абзацем выше: грубая эвристика в
            # инструменте против тихой потери сама даёт тихую потерю.
            soderzhimoe = (d.get("message") or {}).get("content")
            if isinstance(soderzhimoe, str):
                vladelec.append(t)
            elif isinstance(soderzhimoe, list) and any(
                    isinstance(b, dict) and b.get("type") != "tool_result"
                    for b in soderzhimoe):
                vladelec.append(t)
            elif OTVET_VIDZHETA in t:
                vladelec.append(t)
        elif rol == "assistant":
            analitik.append(t)
    return vladelec, analitik, vsego, neponyatnyh


def metki(t: str) -> list[str]:
    return [imya for imya, rx in MARKERY.items() if re.search(rx, t, re.I)]


def main():
    ap = argparse.ArgumentParser(description="Выгрузить знание из транскрипта сессии")
    ap.add_argument("arka", help="папка арки, куда положить выгрузку")
    ap.add_argument("--transcript", help="путь к .jsonl (иначе ищется самый свежий)")
    ap.add_argument("--spisok", action="store_true", help="только показать найденные транскрипты")
    args = ap.parse_args()

    if args.spisok:
        subprocess.run(["bash", "-lc",
                        "ls -1t ~/.claude/projects/*/*.jsonl "
                        "/var/folders/*/*/T/claude-hostloop-plugins/*/projects/*/*.jsonl "
                        "2>/dev/null | head -20"])
        return

    arka = Path(args.arka).resolve()
    if not arka.is_dir():
        sys.exit(f"❌ нет папки арки: {arka}")

    tr = najti_transcript(args.transcript)
    vladelec, analitik, vsego, neponyatnyh = razobrat(tr)

    if not vladelec:
        sys.exit(f"❌ в транскрипте {tr.name} не найдено ни одной реплики владельца "
                 f"({vsego} записей, нераспознано {neponyatnyh}). Формат изменился — "
                 f"чинить `tekst_bloka`, а НЕ игнорировать: пустая выгрузка выглядит "
                 f"как «ничего важного не было».")

    data = datetime.now().strftime("%Y-%m-%d")
    out = arka / f"VYGRUZKA-{data}.md"

    L = [f"# ВЫГРУЗКА СЕССИИ {data} — сырьё для дневника, не сам дневник", "",
         "> Печатает `zakryt_sessiyu.py`, токенов не стоит. **Скрипт не решает, что важно** — "
         "он выгружает ВСЕ реплики владельца дословно и метит их эвристиками. "
         "Разносит аналитик, глядя на полный текст.", "",
         f"**Источник:** `{tr}`", "",
         f"**Охват:** записей в транскрипте {vsego} · реплик владельца {len(vladelec)} · "
         f"реплик аналитика {len(analitik)} · нераспознано {neponyatnyh}", "",
         "## Как разносить", "",
         "1. Пройти реплики владельца ПОДРЯД, каждую — в дневник арки одной строкой сути.",
         "2. Требования и решения — в `KARTA-ZNANIYA.md §4` или в дом по `KARTA.md`.",
         "3. Вопросы владельца (метка `вопрос`) — сверить, что на КАЖДЫЙ дан ответ.",
         "4. Обещания аналитика — сверить, что каждое стало задачей или сделано.",
         "5. Разнесённое пометить в дневнике отсечкой `<!-- РАЗНЕСЕНО ДО СЮДА: "
         f"{data} -->`.", "",
         "---", "", "## РЕПЛИКИ ВЛАДЕЛЬЦА — дословно, все, по порядку", ""]

    for i, t in enumerate(vladelec, 1):
        m = metki(t)
        L += [f"### В{i:02d}" + (f" · метки: {' · '.join(m)}" if m else ""), "", t, ""]

    # Обещания аналитика — отдельным списком, это самый частый вид потери.
    ob = [t for t in analitik if re.search(OBESHCHANIYA, t, re.I)]
    L += ["---", "", f"## ОБЕЩАНИЯ АНАЛИТИКА — {len(ob)} штук, каждое сверить с задачами", ""]
    for t in ob:
        frazy = [f.strip() for f in re.split(r"(?<=[.!?])\s+", t)
                 if re.search(OBESHCHANIYA, f, re.I)]
        for f in frazy[:3]:
            L.append(f"- {f[:300]}")

    # Вопросы владельца — второй по частоте вид потери.
    voprosy = []
    for i, t in enumerate(vladelec, 1):
        for f in re.split(r"(?<=[.!?])\s+", t):
            if "?" in f and len(f) > 30:
                voprosy.append(f"- **В{i:02d}:** {f.strip()[:300]}")
    L += ["", "---", "", f"## ВОПРОСЫ ВЛАДЕЛЬЦА — {len(voprosy)} штук, на каждый нужен ответ", ""] + voprosy

    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {out}")
    print(f"   записей {vsego} · реплик владельца {len(vladelec)} · обещаний {len(ob)} · вопросов {len(voprosy)}")
    if neponyatnyh:
        print(f"   ⚠ нераспознано строк: {neponyatnyh} — если это заметная доля, формат изменился")
    print(f"\n🔴 Дальше — РУКАМИ: разнести по дневнику и домам, ответить на вопросы, "
          f"поставить отсечку. Выгрузка сама ничего не закрывает.")


if __name__ == "__main__":
    main()
