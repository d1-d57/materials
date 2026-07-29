#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Порождение слоя Фазы II из ленты Фазы I — арка 7, шаги 1–2 захода kod_verstka.md.

  python3 teorkat-vvedenie/src/tools/porodit.py            # порождает + печатает инвентарь
  python3 teorkat-vvedenie/src/tools/porodit.py --inventar # ТОЛЬКО инвентарь, ничего не пишет

Вход  — teorkat-vvedenie/raskadrovka/teksty/*.md (лента, READ-ONLY, не трогается).
Выход — src/content/<id>.md · src/illustrations/*.svg · инвентарь на stdout.

Порождение МЕХАНИЧЕСКОЕ намеренно: 55 разделов, переписанных руками, дают ошибки
переноса, которых потом не видно. Что снимается при переносе (заход §ШАГ 1):
  · `> поле:*` целиком — режиссура для читателя ленты, включая пометку раскладки;
  · `<figure>`/`<figcaption>`/весь html — G6 требует regex `<[a-zA-Z]` == 0 в content;
  · строки `🖼 Портрет … {N}` — это плейсхолдер илл., а не текст слайда.
Что преобразуется по форме (диалект генератора беднее ленты, см. ПЛАН П3/П4):
  · <table> → список `- ` построчно (таблиц диалект не знает вовсе);
  · $$X$$   → отдельный абзац `{.formula} $X$` (regex \$(.+?)\$ ломается на $$).
Что НЕ меняется: сам текст, дословно.
"""
import re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LENTA = ROOT / "teorkat-vvedenie" / "raskadrovka" / "teksty"
SRC = ROOT / "teorkat-vvedenie" / "src"
BLOCKS = ["A-krasivaya.md", "B-yazyk.md", "C-zapret-retrakt.md",
          "D-zapret-estestvennost.md", "E-dva-mira.md"]

TRANS = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya",
}


def slug(text, limit=34):
    out = []
    for ch in text.lower():
        if ch in TRANS:
            out.append(TRANS[ch])
        elif ch.isascii() and (ch.isalnum()):
            out.append(ch)
        else:
            out.append("-")
    s = re.sub(r"-+", "-", "".join(out)).strip("-")
    return s[:limit].strip("-")


# ───────────────────────── разбор ленты ─────────────────────────
def split_sections(text):
    """[(заголовок, тело)] по разделам `^## `. Шапка файла отбрасывается."""
    parts = re.split(r"^## ", text, flags=re.M)
    out = []
    for chunk in parts[1:]:
        nl = chunk.find("\n")
        out.append((chunk[:nl].strip(), chunk[nl + 1:]))
    return out


FIGURE_RE = re.compile(r"<figure\b([^>]*)>(.*?)</figure>", re.S)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S)
VIEWBOX_RE = re.compile(r'viewBox="([\d.\s-]+)"')
TABLE_RE = re.compile(r"<table>.*?</table>", re.S)
POLE_RE = re.compile(r"^> поле:.*$", re.M)
PORTRAIT_RE = re.compile(r"^🖼 .*$", re.M)


# `[^$]+`, а НЕ `.+`: жадное `.+` матчит и строку с ВНУТРЕННИМИ долларами
# («$\sum…$ при $n\ge1$» считалось одной цельной формулой), и склейка равенства
# уносила условие внутрь формулы. Цена — ниже, в COND_RE.
MATH_WHOLE = re.compile(r"^\$([^$]+)\$$")
# Ячейка «выражение» может нести УСЛОВИЕ хвостом: `$…$ при $n\ge1$`. Равенство
# тогда собирается вокруг ВЫРАЖЕНИЯ, а условие уезжает за формулу.
COND_RE = re.compile(r"^\$([^$]+)\$\s*(.+)$")


def table_to_list(html):
    """<table> → строки списка `- `. Диалект генератора таблиц не знает вовсе
    (`render_md` умеет только <p> и <ul>), а html в content запрещён гейтом G6 —
    значит таблица линеаризуется. Как именно, решает ШАПКА, и это не косметика:
    первый прогон склеивал все ячейки через ' · ', и на снятом кадре строка
    «5 · Σ(−1)^k C(n,k) при n≥1 · 0» читалась как ПРОИЗВЕДЕНИЕ, то есть
    линеаризация врала про математику. Поэтому:

      · таблица «выражение | чему равно» → одно равенство: два матполя
        сливаются в одну формулу, номер строки становится ярлыком;
      · таблица в две колонки → `**ключ** — значение` (тире, не точка-разделитель);
      · таблица в три и более колонок → имена столбцов идут ЛЕЙБЛАМИ к значениям,
        иначе список теряет то, что несла шапка («группа», «инвариант»).
    """
    head = [h.strip() for h in re.findall(r"<th>(.*?)</th>", html, re.S)]
    rows = re.findall(r"<tr>(.*?)</tr>", html, re.S)
    is_eq = bool(head) and head[-1].lower().startswith("чему равно")
    items = []
    for r in rows:
        if "<th>" in r:
            continue
        cells = [c.strip() for c in re.findall(r"<td>(.*?)</td>", r, re.S)]
        cells = [c for c in cells if c]
        if not cells:
            continue
        if is_eq:
            num = cells[0] if len(cells) > 2 else None
            left, right = cells[-2], cells[-1]
            # 🔴 Порядок сборки равенства решает СМЫСЛ, а не косметику. Строка 5
            # ленты несёт условие в колонке «выражение»: `$\sum…$ при $n\ge1$` |
            # `$0$`. Наивная склейка «левое = правое» ставит знак равенства ПОСЛЕ
            # условия и печатает на слайд «при n ≥ 1 = 0» — ложное утверждение
            # вместо условия. Поэтому условие-хвост уезжает ЗА формулу:
            #   `$\sum… = 0$ при $n\ge1$`.
            # Слова те же и ни одно не выброшено; переставлен только порядок, и
            # переставлять его тут законно — у ячеек таблицы линейного порядка нет,
            # его выбирает линеаризация. Нашёл свежий верификатор, я это место
            # прочитал как «неуклюже, но верно» и ошибся.
            mr = MATH_WHOLE.match(right)
            ml, mc = MATH_WHOLE.match(left), COND_RE.match(left)
            if ml and mr:
                body = "$%s=%s$" % (ml.group(1), mr.group(1))
            elif mc and mr:
                body = "$%s=%s$ %s" % (mc.group(1), mr.group(1), mc.group(2).strip())
            else:
                body = "%s = %s" % (left, right)
            items.append("- " + (("**%s.** " % num) if num else "") + body)
        elif len(cells) == 2:
            items.append("- **%s** — %s" % (cells[0], cells[1]))
        else:
            tail = " · ".join(
                "%s: %s" % (head[i].lower(), c) if i < len(head) else c
                for i, c in enumerate(cells[1:], start=1))
            items.append("- **%s** — %s" % (cells[0], tail))
    return "\n".join(items)


# ── опорные точки (Р23) ──
# «выделенное цветное СЛОВО-надзаголовок у левого поля, формулировка ниже на всю
# ширину, БЕЗ точки в конце». В ленте это `**Определение.** <текст>` одной строкой,
# то есть инлайн-акцент — а Р23 требует ОТДЕЛЬНОГО надзаголовка. Слова те же, меняется
# только форма подачи; цвета — из Р23: определение зелёным, утверждение/теорема
# стальным, задача кирпичным. «Пример» в словаре Р23 нет — остаётся инлайн-акцентом.
OP_CLS = {"Определение": "op-def", "Утверждение": "op-utv", "Теорема": "op-utv",
          "Задача": "op-task"}
OP_RE = re.compile(r"^\*\*(Определение|Утверждение|Теорема|Задача)([^*]*?)\.?\*\*\s*", re.M)


def opornye_tochki(text):
    def sub(m):
        word, tail = m.group(1), m.group(2).strip()
        label = (word + " " + tail).strip()
        return "{.%s} %s\n\n" % (OP_CLS[word], label)
    return OP_RE.sub(sub, text)


# ── СЦЕНЫ (арка 8) ────────────────────────────────────────────────────────────
# «Правила сколько сцен нет — это драматургия, а не норма» (заход, ШАГ 5). Чтобы
# драматургия не превратилась в мой вкус, разложенный по 55 слайдам, признак взят
# ИЗ САМОГО ТЕКСТА: перечень раскрывается по кликам ровно тогда, когда вводящий его
# абзац объявляет пошаговый разбор — кончается двоеточием и несёт одно из слов
# ниже. Владелец про это дословно: «вот формулировка, потом кликнул — первая часть,
# ещё кликнул — вторая». Все прочие перечни (галерея видов, восемь функторов,
# семь тождеств) показываются разом: там смысл в объёме списка, а не в порядке.
# Условие двойное: абзац ОБЯЗАН кончаться двоеточием (то есть анонсировать
# следующий список) И нести пошаговое слово где-то внутри. Первая версия требовала
# слово в самом конце и промахнулась мимо «Почему при чётном нет:» — то есть мимо
# единственного места блока A, где на слайде идёт настоящее доказательство по шагам.
SHAG_RE = re.compile(r"(по шагам|почему|причём по-разному|три попытки|"
                     r"разберём|по порядку|шаг за шагом)", re.I)


def sceny(text):
    """Разметить пошаговые перечни шорткатами `{@N|…}`. Возвращает (текст, число сцен).

    Раскрытие пишется ИНЛАЙНОМ (`- {@2|…}`), а не ведущим тегом: `render_md`
    прогоняет элементы списка через `render_inline_md` и `_attrs_from_tag` к ним
    НЕ применяет — ведущий `{@2}` у пункта уехал бы на слайд буквальным текстом.
    """
    blocks = re.split(r"(\n\s*\n)", text)
    out, mx = [], 1
    for i, b in enumerate(blocks):
        items = [l for l in b.split("\n") if l.strip()]
        is_list = bool(items) and all(l.lstrip().startswith("- ") for l in items)
        prev = next((blocks[j] for j in range(i - 1, -1, -1)
                     if blocks[j].strip()), "")
        pv = prev.strip()
        if is_list and len(items) >= 3 and pv.endswith(":") and SHAG_RE.search(pv):
            new = []
            for k, l in enumerate(items):
                body = l.lstrip()[2:].strip()
                new.append("- {@%d|%s}" % (k + 2, body))
                mx = max(mx, k + 2)
            out.append("\n".join(new))
        else:
            out.append(b)
    return "".join(out), mx


def parse_section(title, body):
    """Раздел ленты → dict со всем, что нужно и content, и вёрстке."""
    layout = None
    m = re.search(r"^> поле:mn \*\*Раскладка\.\*\* (.*)$", body, re.M)
    if m:
        layout = m.group(1).strip()

    figures = []
    for fm in FIGURE_RE.finditer(body):
        attrs, inner = fm.group(1), fm.group(2)
        sm = SVG_RE.search(inner)
        if not sm:
            continue
        svg = sm.group(0)
        vb = VIEWBOX_RE.search(svg)
        w = h = None
        if vb:
            nums = [float(x) for x in vb.group(1).split()]
            if len(nums) == 4:
                w, h = nums[2], nums[3]
        am = re.search(r'aria-label="([^"]*)"', svg)
        figures.append({
            "svg": svg, "mn": 'class="mn"' in attrs, "w": w, "h": h,
            "aria": (am.group(1) if am else ""),
        })

    portraits = [p.strip() for p in PORTRAIT_RE.findall(body)]

    # ── текст слайда ──
    text = FIGURE_RE.sub("", body)
    text = TABLE_RE.sub(lambda m: "\n" + table_to_list(m.group(0)) + "\n", text)
    text = POLE_RE.sub("", text)
    text = PORTRAIT_RE.sub("", text)
    # выключная формула отдельным абзацем
    # [ \t]*$ — НЕ \s*$: жадное \s* съедает пустую строку-разделитель и склеивает
    # выключную формулу со следующим абзацем в один <p> (поймано на s12 при первом прогоне)
    # \displaystyle — не косметика, а РАЗВЕДЕНИЕ КЛЮЧЕЙ: кэш формул ключуется TeX'ом,
    # и когда та же формула стоит и абзацем, и в строке текста (после линеаризации
    # таблицы тождеств это случилось дважды), один режим рендера побеждает другой.
    # С префиксом ключи различны по построению, а пределы у \sum встают над и под
    # сигмой без блочной обёртки katex-display, которая рвала бы абзац.
    text = re.sub(r"^\$\$(.+?)\$\$[ \t]*$",
                  lambda m: "{.formula} $\\displaystyle %s$" % m.group(1).strip(),
                  text, flags=re.M)
    # Пунктуация после формулы ПРИКЛЕИВАЕТСЯ к ней словосоединителем U+2060.
    # Поймано глазом на s03: строка начиналась с «. Совпало» — точка ушла на
    # следующую строку отдельно от формулы, к которой относится. Мест таких 115,
    # то есть это системный дефект переноса, а не случай одного слайда. Канон
    # («формулу НЕ разрывать переносом строки») лечится здесь тем же приёмом:
    # соединитель — обычный символ, html в content по-прежнему нулевой (G6).
    # \u26a0 \u0417\u0430\u043c\u0435\u043d\u0430 \u041e\u0411\u042f\u0417\u0410\u041d\u0410 \u0441\u043e\u0431\u0438\u0440\u0430\u0442\u044c\u0441\u044f \u043a\u043e\u043d\u043a\u0430\u0442\u0435\u043d\u0430\u0446\u0438\u0435\u0439, \u0430 \u043d\u0435 \u043e\u0434\u043d\u043e\u0439 \u043d\u0435raw-\u0441\u0442\u0440\u043e\u043a\u043e\u0439: \u0432
    # "$\u2060\1" \u043f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \1 \u2014 \u044d\u0442\u043e \u041d\u0415 \u043e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0441\u044b\u043b\u043a\u0430, \u0430 \u0432\u043e\u0441\u044c\u043c\u0435\u0440\u0438\u0447\u043d\u044b\u0439 \x01,
    # \u0438 \u043f\u0435\u0440\u0432\u044b\u0439 \u043f\u0440\u043e\u0433\u043e\u043d \u044d\u0442\u043e\u0439 \u0441\u0442\u0440\u043e\u043a\u0438 \u041c\u041e\u041b\u0427\u0410 \u0443\u0434\u0430\u043b\u0438\u043b \u0432\u0441\u0435 115 \u0437\u043d\u0430\u043a\u043e\u0432 \u043f\u0443\u043d\u043a\u0442\u0443\u0430\u0446\u0438\u0438 \u0438\u0437 43
    # \u0444\u0430\u0439\u043b\u043e\u0432. \u041d\u0438 \u043b\u0438\u043d\u0442\u0435\u0440, \u043d\u0438 audit.py \u0442\u0430\u043a\u043e\u0433\u043e \u043d\u0435 \u0432\u0438\u0434\u044f\u0442 (html \u043d\u0435 \u043f\u043e\u044f\u0432\u0438\u043b\u0441\u044f, overflow
    # \u043d\u0435 \u0438\u0437\u043c\u0435\u043d\u0438\u043b\u0441\u044f) \u2014 \u043f\u043e\u0439\u043c\u0430\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043d\u0430 \u0441\u043d\u044f\u0442\u043e\u043c \u043a\u0430\u0434\u0440\u0435: \u00ab\u0438\u043d\u0432\u0430\u0440\u0438\u0430\u043d\u0442\u043d\u044b \u0442\u043e\u043b\u044c\u043a\u043e \u2205 \u0438 U
    # \u0440\u0430\u0437\u043c\u0435\u0440\u044b 0 \u0438 n\u00bb \u0431\u0435\u0437 \u0437\u0430\u043f\u044f\u0442\u043e\u0439. \u041f\u043e\u044d\u0442\u043e\u043c\u0443 \u043d\u0438\u0436\u0435 \u0441\u0442\u043e\u0438\u0442 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 \u0432\u0435\u0440\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440:
    # \u0441\u043d\u044f\u0442\u0438\u0435 \u0441\u043e\u0435\u0434\u0438\u043d\u0438\u0442\u0435\u043b\u044f \u041e\u0411\u042f\u0417\u0410\u041d\u041e \u0432\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0442\u044c \u0438\u0441\u0445\u043e\u0434\u043d\u0443\u044e \u0441\u0442\u0440\u043e\u043a\u0443 \u043f\u043e\u0431\u0430\u0439\u0442\u043d\u043e.
    # \u041f\u0435\u0440\u0432\u0430\u044f \u043f\u043e\u043f\u044b\u0442\u043a\u0430 \u0441\u0442\u0430\u0432\u0438\u043b\u0430 \u043c\u0435\u0436\u0434\u0443 \u0444\u043e\u0440\u043c\u0443\u043b\u043e\u0439 \u0438 \u0442\u043e\u0447\u043a\u043e\u0439 \u0441\u043b\u043e\u0432\u043e\u0441\u043e\u0435\u0434\u0438\u043d\u0438\u0442\u0435\u043b\u044c U+2060 \u2014
    # \u0438 \u043d\u0430 \u0441\u043d\u044f\u0442\u043e\u043c \u043a\u0430\u0434\u0440\u0435 s03 \u043f\u0435\u0440\u0435\u043d\u043e\u0441 \u043e\u0441\u0442\u0430\u043b\u0441\u044f: Chrome \u043d\u0435 \u0441\u043e\u0431\u043b\u044e\u0434\u0430\u0435\u0442 WJ \u0440\u044f\u0434\u043e\u043c \u0441
    # \u0430\u0442\u043e\u043c\u0430\u0440\u043d\u044b\u043c \u0438\u043d\u043b\u0430\u0439\u043d\u043e\u043c, \u0430 `.katex .base` \u2014 \u044d\u0442\u043e inline-block. \u0420\u0430\u0431\u043e\u0442\u0430\u044e\u0449\u0438\u0439 \u043f\u0440\u0438\u0451\u043c:
    # \u0437\u043d\u0430\u043a \u0443\u0435\u0437\u0436\u0430\u0435\u0442 \u0412\u041d\u0423\u0422\u0420\u042c \u0444\u043e\u0440\u043c\u0443\u043b\u044b \u043a\u0430\u043a \text{.}, \u0438 \u0440\u0430\u0437\u0440\u044b\u0432\u0430\u0442\u044c \u0442\u0430\u043c \u043d\u0435\u0447\u0435\u0433\u043e. \u0421\u0438\u043c\u0432\u043e\u043b
    # \u0442\u043e\u0442 \u0436\u0435, \u0442\u0435\u043a\u0441\u0442 \u043b\u0435\u043d\u0442\u044b \u043d\u0435 \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u0430\u043d, html \u0432 content \u043f\u043e-\u043f\u0440\u0435\u0436\u043d\u0435\u043c\u0443 0 (G6).
    # Дефис в том же списке: на кадре s24 составное «$G$-множество» разъехалось —
    # «G» в конце строки, «-множество» в начале следующей. Дефис — законная точка
    # переноса, поэтому он уезжает внутрь формулы ровно как точка. Таких мест 5.
    # 🔴 Правило ОБЯЗАНО работать по ПАРЕ `$…$`, а не по одиночному `$`. Версия
    # `re.sub(r"\$-(?=\w)", …)` поймала ОТКРЫВАЮЩИЙ доллар в «$-i$» и выдала на
    # слайд литерал «\text{-}i»: минус уехал наружу формулы обычным текстом.
    # Поймано глазом на кадре s37 — и НЕ поймано ни гейтами, ни моей же проверкой
    # на обратимость: обратная замена честно возвращала исходную строку, то есть
    # обратимость не равна правильности. Отсюда вторая проверка — на чётность `$`.
    _do = text
    text = re.sub(r"\$([^$]+)\$([.,;:!?]|-(?=\w))",
                  lambda m: "$%s\\text{%s}$" % (m.group(1), m.group(2)), text)
    if re.sub(r"\\text\{([.,;:!?-])\}\$", r"$\1", text) != _do:
        raise SystemExit(
            "\u041b\u041e\u0421\u0421\u041e\u0412\u042b\u0419 \u043f\u0435\u0440\u0435\u043d\u043e\u0441 \u043f\u0443\u043d\u043a\u0442\u0443\u0430\u0446\u0438\u0438 \u0432 \u0444\u043e\u0440\u043c\u0443\u043b\u0443 \u043d\u0430 \u0440\u0430\u0437\u0434\u0435\u043b\u0435 %r: \u043e\u0431\u0440\u0430\u0442\u043d\u0430\u044f "
            "\u0437\u0430\u043c\u0435\u043d\u0430 \u043d\u0435 \u0432\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0435\u0442 \u0438\u0441\u0445\u043e\u0434\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442. \u0413\u0435\u0439\u0442\u044b \u044d\u0442\u043e\u0442 \u043a\u043b\u0430\u0441\u0441 \u043d\u0435 \u043b\u043e\u0432\u044f\u0442." % title)
    if text.count("$") != _do.count("$") or text.count("$") % 2:
        raise SystemExit(
            "\u041f\u0410\u0420\u041d\u041e\u0421\u0422\u042c `$` \u0441\u043b\u043e\u043c\u0430\u043d\u0430 \u043d\u0430 \u0440\u0430\u0437\u0434\u0435\u043b\u0435 %r (\u0431\u044b\u043b\u043e %d, \u0441\u0442\u0430\u043b\u043e %d): \u0437\u043d\u0430\u0447\u0438\u0442 "
            "\u043f\u0440\u0430\u0432\u0438\u043b\u043e \u0437\u0430\u0446\u0435\u043f\u0438\u043b\u043e \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u044e\u0449\u0438\u0439 \u0434\u043e\u043b\u043b\u0430\u0440 \u0438 \u043c\u0438\u043d\u0443\u0441/\u0442\u043e\u0447\u043a\u0430 \u0443\u0435\u0445\u0430\u043b\u0438 \u043d\u0430\u0440\u0443\u0436\u0443 "
            "\u0444\u043e\u0440\u043c\u0443\u043b\u044b \u043e\u0431\u044b\u0447\u043d\u044b\u043c \u0442\u0435\u043a\u0441\u0442\u043e\u043c \u2014 \u0440\u043e\u0432\u043d\u043e \u0434\u0435\u0444\u0435\u043a\u0442 s37."
            % (title, _do.count("$"), text.count("$")))
    text = opornye_tochki(text)
    # схлопнуть пустые строки до одной, обрезать края
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n \t")
    text, scenes = sceny(text)

    return {"title": title, "layout": layout, "figures": figures,
            "portraits": portraits, "text": text, "scenes": scenes}


def load_all():
    slides = []
    for fname in BLOCKS:
        blk = fname[0]
        for title, body in split_sections((LENTA / fname).read_text(encoding="utf-8")):
            s = parse_section(title, body)
            s["block"] = blk
            slides.append(s)
    return slides


# ───────────────────────── инвентарь ─────────────────────────
def visible_chars(text):
    """Знаки, которые реально видит зал: без разметки списков, без `{.formula}`,
    формула считается своей длиной в TeX (иного объективного измерителя нет)."""
    t = re.sub(r"^\{\.[\w-]+\}\s*", "", text, flags=re.M)
    t = re.sub(r"^- ", "", t, flags=re.M)
    t = t.replace("**", "").replace("\u2060", "")
    return len(re.sub(r"\s+", " ", t).strip())


def archetype_lenty(s):
    """Архетип раскладки — из пометки ленты, а не из моего вкуса (07-verstka/DOK.md:
    «арка 7 реализует принятую раскладку»)."""
    lay = (s["layout"] or "").lower()
    if "на всю ширину" in lay:
        return "лестница-во-всю-ширину"
    if "крупная горизонтальная иллюстрация снизу" in lay:
        return "илл-полосой-снизу"
    if "полоса пустая" in lay or "полоса справа пустая" in lay:
        return "доска-пустая"
    return "рейка-справа"


def archetype(s):
    """То же, но с одной поправкой на РЕАЛЬНОСТЬ: лента назначила рейку и слайдам,
    у которых иллюстрации в итоге нет вовсе («лента рисовала только обязательный
    минимум», заход §ШАГ 2). Рейка шириной 344px под пустотой — это 24% слайда,
    не занятых ничем, при том что текст на этом же слайде не влезает. Такой слайд
    получает геометрию «доска-пустая»: узкая полоса и текст на всю оставшуюся
    ширину. Пометка ленты при этом не подменяется — она печатается отдельно
    (archetype_lenty), и расхождение видно в инвентаре."""
    a = archetype_lenty(s)
    if a == "рейка-справа" and not s["figures"] and not s["portraits"]:
        return "доска-пустая"
    return a


def main():
    slides = load_all()
    only_inv = "--inventar" in sys.argv

    # обложка = первый раздел ленты; в slide_order не входит (служебный слой)
    cover, content = slides[0], slides[1:]
    ids = ["s%02d" % (i + 1) for i in range(len(content))]

    if not only_inv:
        (SRC / "content").mkdir(parents=True, exist_ok=True)
        (SRC / "illustrations").mkdir(parents=True, exist_ok=True)
        for old in (SRC / "content").glob("*.md"):
            old.unlink()
        for old in (SRC / "illustrations").glob("*"):
            old.unlink()

    rows, ill_index = [], {}
    for sid, s in zip(ids, content):
        names = []
        for k, f in enumerate(s["figures"]):
            nm = "%s-%s" % (sid, slug(s["title"]))
            if len(s["figures"]) > 1:
                nm += "-%d" % (k + 1)
            names.append(nm)
            if not only_inv:
                (SRC / "illustrations" / (nm + ".svg")).write_text(
                    f["svg"] + "\n", encoding="utf-8")
        for k, p in enumerate(s["portraits"]):
            for pm in re.finditer(r"Портрет ([^{·]+)\{(\d+)\}", p):
                who, num = pm.group(1).strip(), pm.group(2)
                nm = "portret-%s-%s" % (num, slug(who, 24))
                names.append(nm)
                if not only_inv:
                    (SRC / "illustrations" / (nm + ".html")).write_text(
                        '<div class="ph-portret"><span>%s</span></div>\n' % who,
                        encoding="utf-8")
        ill_index[sid] = names
        if not only_inv:
            (SRC / "content" / (sid + ".md")).write_text(s["text"] + "\n", encoding="utf-8")
        rows.append((sid, s["block"], s["title"], visible_chars(s["text"]),
                     archetype(s), len(s["figures"]), len(names) - len(s["figures"]),
                     [(f["w"], f["h"]) for f in s["figures"]]))

    print("── ИНВЕНТАРЬ ЛЕНТЫ (всё счётом, ни одно число руками) ──")
    print("разделов в ленте: %d   из них обложка: 1   содержательных слайдов: %d"
          % (len(slides), len(content)))
    print("обложка: «%s» — %d знаков (в slide_order НЕ входит)"
          % (cover["title"], visible_chars(cover["text"])))
    print()
    print("%-5s %-2s %-46s %5s  %-22s %s" % ("id", "бл", "раздел", "знак", "архетип", "илл"))
    for sid, blk, title, ch, arch, nfig, nport, aspects in rows:
        mark = "  " if nfig or nport else " ∅"
        print("%-5s %-2s %-46s %5d  %-22s %d+%dп%s"
              % (sid, blk, title[:46], ch, arch, nfig, nport, mark))
    chars = sorted(r[3] for r in rows)
    print()
    print("знаки: медиана %d · макс %d · мин %d · сумма %d"
          % (chars[len(chars) // 2], chars[-1], chars[0], sum(chars)))
    from collections import Counter
    print("архетипы (исполняемые):", dict(Counter(r[4] for r in rows)))
    print("архетипы (как назначила лента):", dict(Counter(archetype_lenty(s) for s in content)))
    dem = [i for i, s in zip(ids, content) if archetype(s) != archetype_lenty(s)]
    print("поправлено на реальность (рейка без илл. → узкая полоса): %s" % (dem or "нет"))
    sc = {i: s["scenes"] for i, s in zip(ids, content) if s["scenes"] > 1}
    print("слайдов со сценами: %d · сцен сверх первой: %d · где: %s"
          % (len(sc), sum(v - 1 for v in sc.values()), sc))
    print("слайдов без единой илл.: %d из %d" % (sum(1 for r in rows if not r[5] and not r[6]), len(rows)))
    print("фигур всего: %d · портретов-плейсхолдеров: %d"
          % (sum(r[5] for r in rows), sum(r[6] for r in rows)))
    wide = [(r[0], a) for r in rows for a in r[7] if a[0] and a[1] and a[1] / a[0] < 0.6]
    print("фигур с h/w < 0.6 (горизонтальных по природе): %d" % len(wide))
    if not only_inv:
        print()
        print("записано: content/*.md — %d · illustrations/* — %d"
              % (len(list((SRC / 'content').glob('*.md'))),
                 len(list((SRC / 'illustrations').glob('*')))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
