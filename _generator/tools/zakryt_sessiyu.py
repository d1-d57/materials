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
        if not t:
            continue
        if rol in ("user", "human"):
            # 🔴 ПОРОГ ДЛИНЫ К РЕПЛИКАМ ВЛАДЕЛЬЦА НЕ ПРИМЕНЯЕТСЯ — НАРОЧНО.
            # Здесь стояло общее `len(t) < 25 → пропустить`, и на живом транскрипте
            # 03.08 оно съело реплику «Опять упал, вот» (15 символов, со скриншотом
            # падения коммита). Нашёл независимый верификатор, не автор. Порог —
            # это ровно «скрипт решает, что важно», запрещённое докстрингом:
            # сказанное коротко теряется человеком первым, и инструмент обязан
            # его как раз удержать. Для аналитика порог оставлен: там он режет
            # служебный шум, а не знание.
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
            #
            # 🔴 ТРЕТЬЯ ЦЕНА, и она же цена «правила из одного признака».
            # Редакция «список с не-`tool_result` блоком = владелец» дала на живом
            # транскриптe ПЯТЬ ложных реплик из двадцати двух: загрузка скилла,
            # `[Request interrupted by user]`, `Continue from where you left off` и
            # две подписи `[Image: original …]` — всё это текстовые блоки роли
            # `user`, порождённые ХОСТОМ, а не владельцем. Нашёл независимый
            # верификатор другим методом (18 против 22), автор бы не увидел.
            # Замер по всем транскриптам обеих сред показал, что одного признака
            # не хватает ни в какую сторону: `content` строкой ЕСТЬ у 203 записей
            # `origin=task-notification` (это не владелец), а поля `origin` НЕТ
            # вовсе у 733 настоящих реплик владельца в старых транскриптах.
            # Поэтому признаков ДВА, и они разведены:
            #   origin == "human"          → владелец, чем бы ни был content;
            #   origin другой, но заданный → НЕ владелец (служебная запись хоста);
            #   origin отсутствует         → старый формат: строка = владелец,
            #                                список = только ответ виджета.
            soderzhimoe = (d.get("message") or {}).get("content")
            istochnik = d.get("origin")
            if isinstance(istochnik, dict):
                istochnik = istochnik.get("kind")
            if istochnik == "human":
                vladelec.append(t)
            elif istochnik:
                pass                       # служебная запись хоста, не владелец
            elif isinstance(soderzhimoe, str):
                vladelec.append(t)
            elif any(isinstance(b, dict) and b.get("type") == "tool_result"
                     and tekst_bloka(b).lstrip().startswith(OTVET_VIDZHETA)
                     for b in (soderzhimoe or [])):
                # 🔴 МАРКЕР ИЩЕТСЯ В НАЧАЛЕ БЛОКА, А НЕ ГДЕ УГОДНО В ТЕКСТЕ.
                # Здесь стояло `OTVET_VIDZHETA in t`, и это давало ЛОЖНЫЕ реплики:
                # любой `Read` файла, который строку «The user answered» лишь
                # ЦИТИРУЕТ, засчитывался репликой владельца. Поймано 03.08 первым
                # же живым прогоном `dnevnik.py`: гейт объявил 4 реплики владельца
                # вместо 1 — тремя «репликами» оказались чтение самого файла-захода,
                # чтение ЭТОГО файла и вывод прогона фикстуры. Цена не в цифре:
                # шумящий гейт отключают (`KONSTITUCIYA` Р31), и вместе с шумом
                # уезжает вся польза. Проверено на 5 живых ответах виджета в
                # 4 транскриптах: маркер стоит в позиции 0 блока всегда.
                vladelec.append(t)
        elif rol == "assistant" and len(t) >= 25:
            analitik.append(t)
    return vladelec, analitik, vsego, neponyatnyh


def metki(t: str) -> list[str]:
    return [imya for imya, rx in MARKERY.items() if re.search(rx, t, re.I)]


# Порог свежести транскрипта для сторожа `origin`, в часах. 🔴 СВЕЖЕСТЬ, А НЕ
# КАЛЕНДАРНАЯ ГРАНИЦА ФОРМАТА: у роли `user` поля `origin` НЕТ ВООБЩЕ в 733
# записях старых транскриптов (см. `dnevnik.py razobrat` — старый формат
# поддержан нарочно), так что проверка «доля без origin» на архивном
# транскрипте будет ложно тревожной ПОСТОЯННО. На СВЕЖЕМ (только что
# записанном текущим хостом) транскрипте поле обязано быть у каждой записи —
# отсутствие там и есть сигнал деградации разбора. 24 часа — эмпирический
# выбор под цикл этого проекта («второе закрытие в тот же день» — обычный
# случай); окончательный порог и то, когда предупреждение обязано стать
# ошибкой, — решение аналитика, см. `## ВОПРОСЫ`/отчёт.
SVEZHEST_CHASOV = 24


def dolya_bez_origin(tr: Path):
    """Доля записей-КАНДИДАТОВ в реплику владельца без поля `origin`.

    Возвращает (без_origin, всего_kandidatov). 🔴 СЧИТАЕТ НЕ ВСЕ ЗАПИСИ РОЛИ
    user — ЖИВОЙ прогон на настоящем транскрипте этой сессии показал, почему:
    первая редакция считала буквально все, и дала 53 из 54 — ложная тревога,
    потому что записи роли `user`, целиком состоящие из `tool_result`
    (обёртка результата инструмента), НИКОГДА не несут `origin` и не должны:
    это не реплика, а синтетика хоста. Кандидат — запись, где `content`
    строка ИЛИ список с хотя бы одним блоком, который НЕ `tool_result»
    (тот же структурный признак, что делит содержимое в `razobrat`, но здесь
    не копируется её разбор — только черновая структурная фильтрация, чтобы
    сторож считал то же множество, где отсутствие `origin` вообще что-то значит.
    """
    bez, vsego_kandidatov = 0, 0
    for line in tr.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        rol = d.get("type") or (d.get("message") or {}).get("role")
        if rol not in ("user", "human"):
            continue
        soderzhimoe = (d.get("message") or {}).get("content")
        kandidat = isinstance(soderzhimoe, str) or (
            isinstance(soderzhimoe, list)
            and any(isinstance(b, dict) and b.get("type") != "tool_result" for b in soderzhimoe)
        )
        if not kandidat:
            continue
        vsego_kandidatov += 1
        if "origin" not in d:
            bez += 1
    return bez, vsego_kandidatov


def storozh_formata_origin(tr: Path):
    """Печатает предупреждение, если СВЕЖИЙ транскрипт теряет поле `origin`.

    Ожидание — ноль: у свежего транскрипта хост обязан класть `origin` в
    каждую запись. Молчит, когда чисто (Р31) — печатает только при находке.
    """
    vozrast_chasov = (datetime.now().timestamp() - tr.stat().st_mtime) / 3600
    if vozrast_chasov > SVEZHEST_CHASOV:
        return
    bez, vsego_kandidatov = dolya_bez_origin(tr)
    if bez:
        print(f"⚠ сторож формата: {bez} из {vsego_kandidatov} записей-кандидатов "
              f"в реплику владельца БЕЗ поля origin в свежем транскрипте "
              f"(младше {SVEZHEST_CHASOV}ч) — хостовый формат мог измениться молча, "
              f"проверить разбор в tekst_bloka/razobrat вручную")


def pechat_uborki_vetok():
    """Печать (НЕ гейт): какие ветки можно подмести — и ОДНА команда на все.

    🔴 ЗАЧЕМ ЗДЕСЬ. Закрытие сессии — единственный момент, когда уборка не
    мешает живой работе: заходы дня уже приняты, а новые ещё не заведены.
    Ветки заводятся заходом и не закрываются никогда (замер 04.08: 18 веток
    при пяти живых, 16 из них при удалении не теряют ничего) — и любой сторож
    на такой куче становится шумом ПО ПОСТРОЕНИЮ, сколько его ни чини.

    🔴 НИЧЕГО НЕ УДАЛЯЕТ САМА, и это не осторожность ради осторожности:
    закрытие сессии идёт под аналитиком, часто из песочницы, где запись в
    `.git` запрещена вовсе. Печатается список и одна строка, которую владелец
    исполняет сам (`GIT-disciplina §0`). Молчит, когда подметать нечего (Р31).
    """
    tools = Path(__file__).resolve().parent
    r = subprocess.run(["python3", str(tools / "git_zona.py"), "poteri"],
                       cwd=tools.parent.parent, capture_output=True, text=True)
    vyvod = (r.stdout or "") + (r.stderr or "")
    if "Безопасны" not in vyvod:
        return
    print("\n── ветки, которые можно закрыть (печать, ничего не удалено) ──")
    pechataem = False
    for stroka in vyvod.splitlines():
        if stroka.strip().startswith("✅ Безопасны"):
            pechataem = True
        elif stroka.strip().startswith("Охват:"):
            print("   " + stroka.strip())
            break
        if pechataem and stroka.strip():
            print("   " + stroka.strip())
    print("\n   Подмести ВСЕ безопасные разом — одна команда (обратимо: каждой\n"
          "   ставится надгробие `mogila/<имя>`, воскрешение — одной командой):")
    print("     python3 _generator/tools/git_zona.py zakryt-vetku --vse-zelenye")
    if r.returncode != 0:
        print("\n   ⚠ Есть ветки с НЕПЕРЕНЕСЁННОЙ работой (см. вывод `poteri` выше "
              "по списку) —\n     они в подметание не войдут: их сперва переносят.")


def zaregistrirovat_dokument(put_dokumenta: Path, opisanie: str):
    """Зовёт `register_doc.py` — единственную дверь для нового `.md` в `_studio/`.

    🔴 БЕЗ ЭТОГО ВЫГРУЗКА — ДОКУМЕНТ-СИРОТА. `zakryt_sessiyu.py` пишет
    `VYGRUZKA-<дата>.md` и раньше не звал дверь регистрации: ворота 5
    (`KONSTITUCIYA §9`) на это красили НЕ саму выгрузку, а СЛЕДУЮЩИЙ коммит —
    вместе с ним падала вся чужая зона в нём. Живая цена 03.08: коммит
    дневника арки упал с `rc=1` на `VYGRUZKA-2026-08-03.md:1 — документ-сирота`,
    и вместе с ним не доехали пять путей. Лечение то же, что у
    `bootstrap_arka.py`: инструмент, создающий `.md`, зовёт дверь тем же ходом.
    Ошибку регистрации НЕ делаем фатальной для самой выгрузки — файл уже
    записан и содержит знание независимо от исхода регистрации; печатаем
    результат, чтобы аналитик увидел и, если нужно, зарегистрировал вручную.
    """
    tools_dir = Path(__file__).resolve().parent
    repo = tools_dir.parent.parent
    r = subprocess.run(
        ["python3", str(tools_dir / "register_doc.py"), str(put_dokumenta), opisanie],
        cwd=repo, capture_output=True, text=True,
    )
    if r.returncode == 0:
        print(f"✅ документ зарегистрирован дверью: {put_dokumenta.name}")
    else:
        print(f"⚠ register_doc.py НЕ зарегистрировал {put_dokumenta.name} "
              f"(код {r.returncode}) — зарегистрируй вручную:")
        print(f"   python3 {tools_dir / 'register_doc.py'} {put_dokumenta} \"{opisanie}\"")
        if r.stdout.strip():
            print("   " + r.stdout.strip().replace("\n", "\n   "))
        if r.stderr.strip():
            print("   " + r.stderr.strip().replace("\n", "\n   "))


def main() -> int:
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
        return 0

    arka = Path(args.arka).resolve()
    if not arka.is_dir():
        sys.exit(f"❌ нет папки арки: {arka}")

    tr = najti_transcript(args.transcript)
    storozh_formata_origin(tr)
    vladelec, analitik, vsego, neponyatnyh = razobrat(tr)

    if not vladelec:
        sys.exit(f"❌ в транскрипте {tr.name} не найдено ни одной реплики владельца "
                 f"({vsego} записей, нераспознано {neponyatnyh}). Формат изменился — "
                 f"чинить `tekst_bloka`, а НЕ игнорировать: пустая выгрузка выглядит "
                 f"как «ничего важного не было».")

    data = datetime.now().strftime("%Y-%m-%d")
    out = arka / f"VYGRUZKA-{data}.md"
    # 🔴 ВТОРОЕ ЗАКРЫТИЕ В ТОТ ЖЕ ДЕНЬ НЕ ЗАТИРАЕТ ПЕРВОЕ. Длинные дни с двумя
    # сессиями у этого проекта норма, а имя файла несёт только дату. Молчаливая
    # перезапись убила бы выгрузку утренней сессии целиком — и незаметно, потому
    # что файл на месте и выглядит свежим.
    nomer_vygruzki = 2
    while out.exists():
        out = arka / f"VYGRUZKA-{data}-{nomer_vygruzki}.md"
        nomer_vygruzki += 1

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
        # Три знака — тот же номер, что уходит в `dnevnik.py nomer()`; ширина
        # обязана совпадать, иначе человек, сверяющий выгрузку с дневником
        # глазами, увидит два разных номера для одной реплики.
        L += [f"### В{i:03d}" + (f" · метки: {' · '.join(m)}" if m else ""), "", t, ""]

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
                voprosy.append(f"- **В{i:03d}:** {f.strip()[:300]}")
    L += ["", "---", "", f"## ВОПРОСЫ ВЛАДЕЛЬЦА — {len(voprosy)} штук, на каждый нужен ответ", ""] + voprosy

    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {out}")
    print(f"   записей {vsego} · реплик владельца {len(vladelec)} · обещаний {len(ob)} · вопросов {len(voprosy)}")
    if neponyatnyh:
        print(f"   ⚠ нераспознано строк: {neponyatnyh} — если это заметная доля, формат изменился")
    import dostavit_urok
    uroki = arka / "UROKI-FABRIKE.md"
    if uroki.is_file():
        dostavit_urok.cmd_plan(uroki)
    print(f"\n🔴 Дальше — РУКАМИ: разнести по дневнику и домам, ответить на вопросы, "
          f"поставить отсечку. Выгрузка сама ничего не закрывает.")

    zaregistrirovat_dokument(out, f"Выгрузка сессии {data} — сырьё для дневника арки {arka.name}")

    # Уборка веток — здесь, а не отдельной командой: у владельца не должно
    # появиться ни одного нового хода (см. докстроку pechat_uborki_vetok).
    pechat_uborki_vetok()

    # Счёт незакрытого (заход zamykanie-reestrov, Б3) — ПЕЧАТЬ, не гейт: владелец
    # «не готов пользоваться фабрикой, пока не закрыты все отчёты и инциденты»,
    # а красный на сотнях унаследованных пунктов очереди читать не будут (Р31,
    # тот же урок, что уже оплачен priyomka.py). Здесь — единственный момент, а
    # не отдельная команда, которую забудут вызвать.
    # 🔴 `otchet()`, не `main()`: `main()` разбирает `sys.argv` (Ш4, заход
    # `instrument-podklyuchen`) — вызванный ИЗ ПРОЦЕССА zakryt_sessiyu.py, он
    # читал бы ЕГО argv (`--transcript ...`) и падал `unrecognized arguments`.
    # `otchet()` — чистая функция, без argparse; поведение здесь остаётся
    # глобальным, как было (эта точка вызова не сужается Ш4 — сужается только
    # `bootstrap_zahod.py`, у которого есть своя арка-область).
    print()
    import schet_nezakrytogo
    print(schet_nezakrytogo.otchet())

    # Разбор инцидентов — ГЕЙТ, не печать (в отличие от уборки веток выше):
    # неразобранный класс красит закрытие сессии красным, а не ждёт, пока
    # кто-нибудь вспомнит (`kod_gejt-razbora.md`; было 90 строк за 10 дней,
    # разобрана одна). Красный код здесь СТАНОВИТСЯ кодом возврата всей
    # функции ниже — тем же приёмом, что и `dnevnik.cmd_proverit`.
    tools_dir = Path(__file__).resolve().parent
    print("\n── разбор инцидентов (check_incidenty.py) ──")
    r_incidenty = subprocess.run(
        ["python3", str(tools_dir / "check_incidenty.py")], cwd=tools_dir.parent.parent)
    rc_incidenty = r_incidenty.returncode

    # Часть A.1: `proverit` зовётся ПОСЛЕДНИМ ходом закрытия сессии, а не в
    # pre-commit — коммит и сессия не совпадают, посреди сессии дневник
    # законно неполон, и хук, повешенный на коммит, шумел бы зря (Р31: гейт,
    # который шумит зря, отключат). Закрытие сессии — единственный момент,
    # когда «дневник полон» вообще имеет смысл проверять. Код возврата этой
    # сверки СТАНОВИТСЯ кодом возврата всего инструмента: выгрузка удалась,
    # но дневник неполон → ненулевой выход и внятная строка, что делать.
    from dnevnik import cmd_proverit  # отложенный импорт: dnevnik.py импортирует ЭТОТ модуль
    print("\n── сверка полноты дневника арки (dnevnik.py proverit) ──")
    rc = cmd_proverit(argparse.Namespace(arka=str(arka), transcript=str(tr)))
    if rc == 0:
        print("✅ дневник арки полон — все реплики владельца разнесены")
    else:
        print("\n🔴 Выгрузка сделана, но дневник арки НЕПОЛОН — закрыть сессию нельзя, "
              "пока не разнесены реплики выше.")
    if rc_incidenty != 0:
        print("\n🔴 Есть неразобранные классы инцидентов (см. вывод выше) — "
              "закрыть сессию нельзя, пока не пополнен VERDIKTY.md.")
    return rc or rc_incidenty


if __name__ == "__main__":
    sys.exit(main())
