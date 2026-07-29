#!/usr/bin/env python3
"""Собирает словарь терминов лекции ИЗ ЛЕНТЫ и режет из него промпты для whisper.

Зачем: whisper на русской математической речи предсказуемо ломает термины и имена
(«функтор» → «фунтор», «Жуайаль» → «Жуаяль»). У whisper есть --prompt: текст,
задающий ожидаемую лексику. Потолок жёсткий — 224 токена, влезает не всё,
поэтому отбор идёт по «часто звучит × сильно ломается».

Выход:
  slovar-terminov.txt   — полный словарь с частотами (для меня при вычитке)
  prompt-obshchij.txt   — промпт на весь курс, если акт неизвестен
  prompt-<БЛОК>.txt     — промпт на блок A..E (точнее общего)

Каждый термин ПРОВЕРЯЕТСЯ на присутствие в ленте: чего в ленте нет — в промпт
не попадает и печатается отдельным списком. Так ловится термин, придуманный
по памяти вместо собранного из файлов.

Запуск: python3 tools/sobrat_slovar.py
"""

import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPETICIA = os.path.dirname(HERE)
LENTA = os.path.join(os.path.dirname(REPETICIA), "raskadrovka", "teksty")
TOKENIZER = os.path.join(REPETICIA, "models", "multilingual.tiktoken")

BLOKI = [
    ("A", "A-krasivaya.md"),
    ("B", "B-yazyk.md"),
    ("C", "C-zapret-retrakt.md"),
    ("D", "D-zapret-estestvennost.md"),
    ("E", "E-dva-mira.md"),
]

LIMIT_TOKENS = 224  # жёсткий потолок initial_prompt у whisper (n_text_ctx/2)

# ─────────────────────────────────────────────────────────────────────────────
# СЛОВАРЬ. Формат: (форма для промпта, стем для поиска в ленте, риск 1..3)
# Риск — насколько whisper это ломает: 3 = не знает слова вовсе (имена,
# редкие термины), 2 = искажает регулярно, 1 = обычно берёт верно.
# Отбор в промпт идёт по риск × частота, поэтому риск — не украшение.
# ─────────────────────────────────────────────────────────────────────────────

IMENA = [
    ("Жуайаль", r"Жуайал", 3),
    ("Андре Жуайаль", r"Андре", 3),
    ("Маклейн", r"Маклейн", 3),
    ("Сондерс Маклейн", r"Сондерс", 3),
    ("Эйленберг", r"Эйленберг", 3),
    ("Сэмюэл Эйленберг", r"Сэмюэл", 3),
    ("Гротендик", r"Гротендик", 3),
    ("Стоун", r"Стоун", 3),
    ("Маршалл Стоун", r"Маршалл", 3),
    ("Фробениус", r"Фробениус", 3),
    ("Брауэр", r"Брауэр", 3),
    ("Лёйтзен Брауэр", r"Лёйтзен", 3),
    ("Галуа", r"Галуа", 3),
    ("Кан", r"\bКана\b", 3),
    ("Ламбек", r"Ламбек", 3),
    ("Атья", r"Атьи|Атья", 3),
    ("Стинрод", r"Стинрод", 3),
    ("Воеводский", r"Воеводск", 3),
    ("Ленглендс", r"Ленглендс", 3),
    ("Макдональд", r"Макдональд", 3),
    ("Вандермонд", r"Вандермонд", 3),
    ("Паскаль", r"Паскал", 2),
    ("Кэли", r"Кэли", 3),
    ("Якоби", r"Якоби", 3),
    ("Бордман", r"Бордман", 3),
    ("Фогт", r"Фогт", 3),
    ("Фердинанд Георг", r"Фердинанд", 2),
    ("Принстон", r"Принстон", 2),
]

TERMINY = [
    ("функтор", r"функтор|Функтор", 3),
    ("естественное преобразование", r"естественн\w* преобразован", 2),
    ("ретракт", r"ретракт|Ретракт", 3),
    ("кобордизм", r"кобордизм|Кобордизм", 3),
    ("группоид", r"группоид|Группоид", 3),
    ("тангл", r"тангл|Тангл", 3),
    ("морфизм", r"морфизм", 2),
    ("изоморфизм", r"изоморфизм|Изоморфизм", 1),
    ("эндоморфизм", r"эндоморфизм", 3),
    ("автоморфизм", r"автоморфизм", 3),
    ("гомоморфизм", r"гомоморфизм", 2),
    ("биекция", r"биекц|Биекц", 2),
    ("инъекция", r"инъекц|Инъекц", 2),
    ("подкатегория", r"подкатегор|Подкатегор", 2),
    ("категория", r"категор|Категор", 1),
    ("стрелка", r"стрелк|Стрелк", 1),
    ("композиция", r"композиц|Композиц", 1),
    ("тождество", r"тождеств|Тождеств", 1),
    ("забывающий функтор", r"[Зз]абывани", 2),
    ("полный и строгий", r"[Сс]трогий", 2),
    ("эквивалентность категорий", r"эквивалентност|Эквивалентност", 1),
    ("решётка", r"решётк|Решётк", 2),
    ("булева алгебра", r"[Бб]улев", 2),
    ("ультрафильтр", r"ультрафильтр", 3),
    ("спектр", r"спектр|Спектр", 2),
    ("двойственность", r"двойственн|Двойственн", 2),
    ("гомологии", r"гомологи|Гомологи", 2),
    ("дифференциал", r"дифференциал|Дифференциал", 2),
    ("определитель", r"определител|Определител", 1),
    ("перестановка", r"перестановк|Перестановк", 1),
    ("занумерованное множество", r"занумерован", 3),
    ("нумерация", r"нумерац|Нумерац", 2),
    ("эквивариантный", r"квивариантн", 3),
    ("нерастягивающее", r"[Нн]ерастягиваю", 3),
    ("косы", r"[Кк]осы", 2),
    ("окружность", r"[Оо]кружност", 1),
    ("носитель", r"[Нн]оситель", 2),
    ("препятствие", r"[Пп]репятстви", 1),
    ("аксиомы", r"[Аа]ксиом", 1),
    ("коммутативный", r"оммутатив", 2),
    ("ассоциативность", r"ссоциативност", 2),
    ("группа", r"[Гг]рупп[аыоу]", 1),
    ("кольцо", r"[Кк]ольц", 1),
    ("модуль", r"[Мм]одул", 1),
    ("граф", r"[Гг]раф", 1),
    ("вершина", r"[Вв]ершин", 1),
    ("цикл", r"[Цц]икл", 1),
    ("образ и прообраз", r"[Пп]рообраз", 1),
    ("сопоставление", r"[Сс]опоставлен", 1),
    ("соответствие Галуа", r"[Сс]оответствие Галуа", 3),
]

# Обозначения категорий: в промпт идут СЛОВАМИ — вслух владелец говорит «Сет»,
# а не «\mathbf{Set}». Стем ищется по LaTeX-форме в ленте.
KATEGORII = [
    ("Сет", r"\\mathbf\{Set\}", 3),
    ("Групп", r"\\mathbf\{Grp\}", 3),
    ("ФинСет", r"\\mathbf\{FinSet\}", 3),
    ("Вект", r"\\mathbf\{Vect\}", 3),
    ("Топ", r"\\mathbf\{Top\}", 3),
    ("Мат", r"\\mathbf\{Mat\}", 2),
    ("Коб", r"\\mathbf\{Cob\}", 3),
    ("Ринг", r"\\mathbf\{Ring\}", 3),
    ("Рел", r"\\mathbf\{Rel\}", 3),
    ("Пос", r"\\mathbf\{Pos\}", 3),
    ("Мод", r"\\mathbf\{Mod\}", 2),
    ("Мет", r"\\mathbf\{Met\}", 2),
    ("Ман", r"\\mathbf\{Man\}", 3),
    ("Ли", r"\\mathbf\{Lie\}", 2),
    ("Гильб", r"\\mathbf\{Hilb\}", 3),
    ("Граф", r"\\mathbf\{Grph\}", 2),
    ("Аб", r"\\mathbf\{Ab\}", 3),
    ("ФинБул", r"\\mathbf\{FinBool\}", 3),
    ("Аут", r"\\mathrm\{Aut\}|\bAut\b", 3),
]

GRUPPY = [("ИМЕНА", IMENA), ("ТЕРМИНЫ", TERMINY), ("КАТЕГОРИИ (вслух)", KATEGORII)]

# Названо в задании как ломкое, но в ленте НЕТ — в промпт не идёт (бюджет дорог),
# лежит здесь, чтобы при вычитке я узнал слово, если владелец его произнёс.
VNE_LENTY = ["Морита", "Йонеда", "копредел", "топос", "пучок", "симплициальный"]


def token_counter():
    """Возвращает (функция подсчёта токенов, как считаем).

    Настоящий токенизатор whisper — multilingual.tiktoken из репозитория openai.
    Без него считаем по эвристике 0.37 токена на символ (измерено на этом же
    словаре); эвристика огрубляет, поэтому бюджет тогда берётся с запасом.
    """
    if os.path.exists(TOKENIZER):
        try:
            import tiktoken

            ranks = {
                base64.b64decode(t): int(r)
                for t, r in (
                    l.split() for l in open(TOKENIZER).read().splitlines() if l
                )
            }
            pat = (
                r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+|"""
                r""" ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
            )
            enc = tiktoken.Encoding(
                name="whisper-multilingual",
                explicit_n_vocab=len(ranks),
                pat_str=pat,
                mergeable_ranks=ranks,
                special_tokens={},
            )
            return (lambda s: len(enc.encode(s))), "токенизатор whisper"
        except Exception as e:  # tiktoken нет или файл битый — не падаем
            print("  ! токенизатор не поднялся (%s), иду по эвристике" % e)
    return (lambda s: int(len(s) * 0.37 * 1.15)), "эвристика 0.37 т/зн + 15% запас"


def read_lenta():
    teksty = {}
    for kod, imya in BLOKI:
        put = os.path.join(LENTA, imya)
        if not os.path.exists(put):
            sys.exit("НЕТ файла ленты: %s" % put)
        teksty[kod] = open(put, encoding="utf-8").read()
    return teksty


def schitat(teksty):
    """Частота каждого термина по блокам и всего. Отсутствующие — отдельно."""
    stroki, propal = [], []
    for gruppa, spisok in GRUPPY:
        for forma, stem, risk in spisok:
            rx = re.compile(stem)
            po_blokam = {k: len(rx.findall(t)) for k, t in teksty.items()}
            vsego = sum(po_blokam.values())
            if vsego == 0:
                propal.append((gruppa, forma, stem))
            else:
                stroki.append(
                    {
                        "gruppa": gruppa,
                        "forma": forma,
                        "risk": risk,
                        "bloki": po_blokam,
                        "vsego": vsego,
                    }
                )
    return stroki, propal


def sobrat_promt(stroki, blok, ntok, limit):
    """Жадно набивает промпт: РИСК главный, частота — тайбрейк.

    Почему не «риск × частота»: произведение отдаёт бюджет частым словам
    («морфизм» 22×2=44), которые whisper и так берёт верно, и выбрасывает
    имена («Жуайаль» 5×3=15), которые он без подсказки не напишет НИКОГДА.
    Ценность токена промпта — не в частоте слова, а в том, способен ли
    движок угадать его сам. Поэтому сначала весь риск 3, потом 2, потом 1.

    Порядок групп в промпте фиксирован — так текст читается как естественная
    фраза, а whisper на естественную фразу отзывается лучше, чем на список.
    """
    kand = []
    for s in stroki:
        chastota = s["vsego"] if blok is None else s["bloki"][blok]
        if chastota == 0:
            continue
        kand.append(((s["risk"], chastota), s["gruppa"], s["forma"]))
    kand.sort(key=lambda x: (-x[0][0], -x[0][1]))

    golova = "Лекция по теории категорий. "
    vzyato = {"ТЕРМИНЫ": [], "ИМЕНА": [], "КАТЕГОРИИ (вслух)": []}

    def sklejka(v):
        chasti = []
        if v["ТЕРМИНЫ"]:
            chasti.append("Термины: " + ", ".join(v["ТЕРМИНЫ"]) + ".")
        if v["ИМЕНА"]:
            chasti.append("Имена: " + ", ".join(v["ИМЕНА"]) + ".")
        if v["КАТЕГОРИИ (вслух)"]:
            chasti.append("Категории: " + ", ".join(v["КАТЕГОРИИ (вслух)"]) + ".")
        return golova + " ".join(chasti)

    for _, gruppa, forma in kand:
        vzyato[gruppa].append(forma)
        if ntok(sklejka(vzyato)) > limit:
            vzyato[gruppa].pop()  # не влез — откатываем и пробуем следующий
    tekst = sklejka(vzyato)
    vsego_vzyato = sum(len(v) for v in vzyato.values())
    return tekst, vsego_vzyato, len(kand)


def main():
    teksty = read_lenta()
    ntok, sposob = token_counter()
    print("Подсчёт токенов: %s" % sposob)

    stroki, propal = schitat(teksty)
    print(
        "Терминов в словаре: %d (проверено по ленте); не найдено в ленте: %d"
        % (len(stroki), len(propal))
    )
    for gruppa, forma, stem in propal:
        print("  ! НЕТ В ЛЕНТЕ, выброшен из промпта: %s / %s (%s)" % (forma, stem, gruppa))

    # ── slovar-terminov.txt ──────────────────────────────────────────────────
    out = [
        "СЛОВАРЬ ТЕРМИНОВ ЛЕКЦИИ «Зачем нужны категории»",
        "Собран командой из ленты: raskadrovka/teksty/[A-E]*.md (33 раздела).",
        "Не править руками — правь tools/sobrat_slovar.py и перезапусти.",
        "Частота = сколько раз стем встретился в ленте. Риск = насколько whisper ломает (3 — не знает слова).",
        "",
    ]
    for gruppa, _ in GRUPPY:
        svoi = [s for s in stroki if s["gruppa"] == gruppa]
        svoi.sort(key=lambda s: (-s["vsego"], s["forma"]))
        out.append("── %s (%d) ──" % (gruppa, len(svoi)))
        for s in svoi:
            po = " ".join(
                "%s:%d" % (k, v) for k, v in sorted(s["bloki"].items()) if v
            )
            out.append(
                "%-30s всего:%-4d риск:%d  %s" % (s["forma"], s["vsego"], s["risk"], po)
            )
        out.append("")
    out.append("── НАЗВАНО В ЗАДАНИИ, НО В ЛЕНТЕ НЕТ (в промпт не идёт) ──")
    out.append(", ".join(VNE_LENTY))
    if propal:
        out.append("")
        out.append("── ИЗ СЛОВАРЯ, НО СТЕМ НЕ НАШЁЛСЯ ──")
        for gruppa, forma, stem in propal:
            out.append("%s (%s) — стем /%s/" % (forma, gruppa, stem))
    put_slovar = os.path.join(REPETICIA, "slovar-terminov.txt")
    open(put_slovar, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("→ %s" % put_slovar)

    # ── промпты ──────────────────────────────────────────────────────────────
    zadaniya = [(None, "prompt-obshchij.txt")] + [
        (k, "prompt-%s.txt" % k) for k, _ in BLOKI
    ]
    for blok, imya in zadaniya:
        tekst, vzyato, kand = sobrat_promt(stroki, blok, ntok, LIMIT_TOKENS)
        t = ntok(tekst)
        if t > LIMIT_TOKENS:
            sys.exit("ПРОМПТ ПЕРЕЛИЛСЯ: %s — %d > %d" % (imya, t, LIMIT_TOKENS))
        put = os.path.join(REPETICIA, imya)
        open(put, "w", encoding="utf-8").write(tekst + "\n")
        print(
            "→ %-22s %3d/%d токенов, %3d знаков, терминов %d из %d доступных"
            % (imya, t, LIMIT_TOKENS, len(tekst), vzyato, kand)
        )


if __name__ == "__main__":
    main()
