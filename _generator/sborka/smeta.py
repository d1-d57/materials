#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-hand — ФАЗЫ 2.5 и 3.1 конвейера
# (`bootstrap_lekcii.LIFECYCLE_TMPL`). Отвечает «влезет ли» ДО сборки и без
# браузера, потому и стоит на фазе 2, а не в хуке.
"""Смета вмещения — «влезет ли текст» БЕЗ браузера, на фазе 2, до написания текста.
Заход svedenie-i-smeta, Э2.3/Э2.4/Э2.6.

🔴 ЕДИНИЦА ИЗМЕРЕНИЯ — СТРОКА, а не слово. Абзац из двух слов занимает строку
целиком; слово не единица вёрстки. Отсюда и вся арифметика ниже.

🔴 ФОРМУЛУ НЕ ПРИДУМЫВАЮТ, ЕЁ КАЛИБРУЮТ (заход, главное архитектурное решение).
Ни одна константа здесь не вписана «на глаз»: каждая снята командой, которая
названа рядом с ней, тем же браузером, которым меряет солвер (`vmeshchenie.izmerit`).
Придуманная формула — это второй источник правды о вёрстке, и он молча разойдётся
с первым. Против расхождения стоит гейт `--sverit` (Э2.4): смета, разошедшаяся с
браузером, краснеет НА СЕБЕ, а не на слайде.

  python3 _generator/sborka/smeta.py <лекция>                      # смета по всем карточкам
  python3 _generator/sborka/smeta.py <лекция>/slajdy/<sid>         # одна карточка
  python3 _generator/sborka/smeta.py --byudzhet <tip_verstki> <liniya>   # Э2.6: бюджет в строках ДО текста
  python3 _generator/sborka/smeta.py --sverit <лекция>             # Э2.4: гейт расхождения (нужен браузер)
  python3 _generator/sborka/smeta.py --proverit-geometriyu         # пересиять геометрию замером и сверить
"""
import argparse
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))

from slaid import compile_slide_html  # noqa: E402

# ═══════════════════ ЗАМЕРЕННЫЕ ЧИСЛА — каждое с командой ═══════════════════
# 🔴 `KONSTITUCIYA §10`: не число, а команда, которая его считает. Все значения
# ниже — вывод ОДНОЙ команды, воспроизводимой в любой момент:
#
#     python3 _generator/sborka/zamer_smety.py --vse teorkat-vvedenie/L2
#
# Дата данных 2026-08-08. Пересняли — сверьте `--proverit-geometriyu`.

# ── Э2.1. ГЕОМЕТРИЯ ЗОНЫ. Замер (`--geometriya`) дал ТОЧНО аффинную картину:
# `liniya` двигает ОДИН размер (ширину у вертикальной полосы, высоту у
# горизонтальной), второй не трогает вовсе. Поэтому здесь не таблица из девяти
# строк, а её ровно воспроизводящая формула — и `--proverit-geometriyu` каждый
# раз доказывает, что она воспроизводит замер без единого пикселя расхождения.
HOLST_W, HOLST_H = 1440, 810      # viewport деки (`deck.py`, `vmeshchenie`)
ZONA_PAD_X, ZONA_PAD_Y = 128, 92  # `.zone.copy{padding:46px 64px}` (base/tipy), снято замером
TOLKO_TEKST_PAD_X, TOLKO_TEKST_PAD_Y = 192, 128  # `tipy.tolko_tekst`: grid padding 64px 96px

# Цена заголовка на экране (`zagolovok_na_ekrane`) — он стоит ВНУТРИ зоны
# (`tipy._text_zone`) и съедает её высоту изнутри.
# БЫЛО 78.44 = 44px × 1.15 + margin 28px. СТАЛО 128.99 = var(--t-frametitle) 76px
# × var(--lh-frametitle) 1.333 + margin 28px — заголовок перевешен на роль темы
# `frametitle` (заход primenenie-vizuala, Ш2). Число не вписано от руки: это
# `zamer_smety.py` через `vmeshchenie.izmerit`, проба типа `tolko_tekst`
# (`zamer_smety.py:211`), сверяется ловушкой 37 каждым коммитом. Сама формула
# сметы НЕ менялась — обновлена калибровка под изменившийся CSS.
# ⚠ ОХВАТ, две слепые зоны, обе объявлены:
#   1) на калибровочной L2 заголовок пуст у 15 карточек из 15 (`grep -c
#      'zagolovok_na_ekrane: ""' teorkat-vvedenie/L2/slajdy/*/slaid.md`) — ветка
#      калибровкой не проверена, как и до этого захода;
#   2) НОВАЯ: у заголовка теперь ДВЕ роли, а константа одна. Типы с иллюстрацией
#      (`polosa_*`, `kompozit`) берут узкую роль --t-frametitle-n: 64 × 1.4 + 28 =
#      117.6px, то есть смета завышает их цену на ~11px. Разводить константу по
#      типу слайда — это правка МОДЕЛИ сметы, а её этот заход трогать не мог
#      (§2: солвер не трогаем); переподбор идёт следующим заходом, там и место.
ZAGOLOVOK_PX = 128.99

# ── Э2.2. ТРИ КОНСТАНТЫ ШРИФТА (`zamer_smety.py --konstanty teorkat-vvedenie/L2`)
# k_znak — средняя ширина знака, делённая на кегль. n=14 слайдов, разброс НУЛЕВОЙ
# (min=median=max=0.5353): шрифт один, кегль один, мерить больше нечего.
K_ZNAK = 0.5353

# k_acc — во сколько раз ЖИРНЫЙ акцент (`.acc{font-weight:700}`, base.css:144)
# шире обычного знака той же пробы: 1.0658, n=14, разброс нулевой (та же команда,
# `--konstanty` — это метрика гарнитуры, а не свойство текста слайда).
# Найдено разбором остаточного расхождения: `vektornye-prostranstva` — абзац с
# двумя `.acc`, смета 4 строки против браузерных 4.98. Шесть процентов ширины на
# длинном абзаце — это ровно одна недосчитанная строка.
K_ACC = 1.0658

# h_formula — высота выносной формулы в долях СТРОКИ. n=8, медиана 1.0159.
# 🔴 «Выносная формула» здесь — НЕ `$$…$$`: такого синтаксиса в конвейере нет
# вовсе (`build_deck.render_inline_md` знает ровно `$…$`), и `.katex-display` не
# встречается в корпусе ни разу. Выносная — это АБЗАЦ ИЗ ОДНОЙ ФОРМУЛЫ, и замер
# говорит: он занимает ровно одну строку (1.016), а не «полторы» и не «две».
H_FORMULA = 1.0159

# k_inline — сколько знаков-эквивалентов занимает инлайн-формула. n=111 формул.
# 🔴 Мера длины формулы — ГЛИФЫ (`знаков ≈ −0.1567 + 1.2018 × глифов`), а НЕ длина
# TeX. Обе модели снял один и тот же замер, и он же их рассудил:
#
#     мера          остаток медиана   остаток p95
#     длина TeX          1.95             8.32
#     глифы              0.78             3.51
#
# Причина механическая: `\mathbb R^{n+1}` — пятнадцать знаков исходника и четыре
# глифа на экране; управляющие последовательности занимают место в источнике и
# ноль в вёрстке, и никакой единый коэффициент этого не выправит. Глифы берутся
# из `.katex-html` СКОМПИЛИРОВАННОГО слайда — браузер для этого по-прежнему не
# нужен, KaTeX уже положил их в статический HTML.
#
# 🔴 Коэффициент 1.20 говорит вещь, ради которой всё и затевалось: глиф формулы
# ШИРЕ среднего знака прозы на 20%. Наивный счёт знаков `$…$` ЗАВЫШАЕТ (считает
# управляющие последовательности), счёт СЛОВ ЗАНИЖАЕТ (формула = одно слово по
# пробелам) — обе прежние меры врали, в разные стороны. Это и есть механическая
# причина, по которой слайд на 64% словесного бюджета вылезал на 22%.
K_GLIF_A = -0.1567
K_GLIF_B = 1.2018


def znakov_formuly(glifov):
    """Число глифов формулы → знаков-эквивалентов прозы (подгонка МНК, Э2.2)."""
    return max(0.0, K_GLIF_A + K_GLIF_B * glifov)

# ── Дефолты токенов (`_generator/skeleton/tokens.css`) — не дубль, а падение
# назад, когда карточка своих значений не несёт (на L2 так у всех 15).
KEGL_DEFAULT = 38.0
LH_DEFAULT = 1.5278
BLOK_DEFAULT = 26.0

# ── Отступы, не выражаемые через `--blok` (`base.css`, прочитано, не угадано).
LI_GAP_PX = 10.0        # `.tlist li + li{margin-top:10px}`
OP_NEXT_GAP_PX = 4.0    # `.t-body p.op-def + p{margin-top:4px}` (и op-utv/op-task)
LI_PAD_EM = 1.15        # `.tlist li{padding-left:1.15em}` — сужает строку пункта
OP_FIRST_EM = 0.18      # `.t-body > p.op-*:first-child{margin-top:.18em}` — em СВОЕГО кегля
OP_KEGL_EM = 0.80       # `.op-def,.op-utv,.op-task{font-size:.80em}` (base.css:193)
OP_LH = 1.12            # там же: `line-height:1.12` — своя, не `--lh` зоны

OP_CLASSES = ("op-def", "op-utv", "op-task")

# 🔴 ПУСТЫЕ ТЕГИ. `HTMLParser` зовёт `handle_starttag` и на `<br>` (без слэша), а
# парного `handle_endtag` не будет никогда. Стек глубины от этого съезжал НАВСЕГДА,
# и все последующие абзацы верхнего уровня переставали опознаваться как прямые
# дети зоны — молча, без единой ошибки. Цена: на `buffon/sl-grid` смета видела
# ОДИН блок вместо трёх и занижала на 6.9 строки. На калибровочной L2 `<br>` не
# встречается ни разу, поэтому калибровка этого не видела — нашёл верификатор §3
# на не-калибровочном материале.
PUSTYE_TEGI = frozenset(("br", "img", "hr", "input", "meta", "link", "source",
                          "area", "base", "col", "embed", "param", "track", "wbr"))

# `.lestnica .lst` / `.spisok .lst` — `display:block` (base.css:153), то есть
# КАЖДАЯ ступенька занимает свою строку, а не течёт в общий абзац.
LST_GAP_PX = 10.0       # `.spisok .lst + .lst{margin-top:10px}`
LST_PAD_EM = 1.15       # `.lestnica .lst,.spisok .lst{padding-left:1.15em}`

# 🔴 ОБЛАСТЬ ПРИМЕНИМОСТИ, объявленная числом, а не умолчанием.
# Смета пакует знаки ВПЛОТНУЮ, браузер переносит ПО СЛОВАМ — рваный правый край
# съедает тем больше, чем ýже колонка. Замер верификатора §3 на не-калибровочном
# материале: при 40–64 знаках в строке (весь корпус L2, 14 карточек из 14)
# расхождение не выходит за 1.03 строки; при 33 знаках (`demo-karta/s02-polosa-v`)
# сверх нормы тоже ничего; при 22 знаках (`dandelin/s09p`) смета ЗАНИЖАЕТ на 2.95
# строки. Занижение — опасная сторона: оно даёт ПРОПУСК переполнения, а не ложную
# тревогу. Поэтому ниже проверенной границы смета не угадывает, а ОТКАЗЫВАЕТСЯ —
# тот же приём «честного отступления», что у солвера (`vmeshchenie`, Э3).
# Граница = наименьшая ПРОВЕРЕННАЯ ширина (33), а не наибольшая сломанная (22).
ZNAKOV_V_STROKE_MIN = 33


# ═════════════════════════ ГЕОМЕТРИЯ ЗОНЫ (Э2.1) ═════════════════════════
def _px(x):
    """Округление доли холста в целые px ТАК ЖЕ, КАК ЭТО ДЕЛАЕТ БРАУЗЕР: половина
    идёт ВВЕРХ. `round()` Python округляет половину к чётному, и на `liniya`
    25/45/65/85 (810×доля даёт ровно .5) смета промахивалась на пиксель против
    замера на 4 точках из 20 — поймано `--proverit-geometriyu`, а не рассуждением."""
    return math.floor(x + 0.5)


def geometriya(tip_verstki, liniya=None):
    """(W, H) контентного бокса текстовой зоны в px. Воспроизводит замер
    `zamer_smety.py --geometriya` точно — см. `--proverit-geometriyu`."""
    if tip_verstki == "polosa_gorizontalnaya":
        if liniya is None:
            raise ValueError("polosa_gorizontalnaya требует liniya")
        return (HOLST_W - ZONA_PAD_X, _px(HOLST_H * liniya / 100.0) - ZONA_PAD_Y)
    if tip_verstki == "polosa_vertikalnaya":
        if liniya is None:
            raise ValueError("polosa_vertikalnaya требует liniya")
        return (_px(HOLST_W * liniya / 100.0) - ZONA_PAD_X, HOLST_H - ZONA_PAD_Y)
    if tip_verstki == "tolko_tekst":
        return (HOLST_W - TOLKO_TEKST_PAD_X - ZONA_PAD_X,
                HOLST_H - TOLKO_TEKST_PAD_Y - ZONA_PAD_Y)
    raise ValueError("тип вёрстки %r текстовой зоны не имеет либо не поддержан сметой "
                     "(поддержаны: polosa_gorizontalnaya, polosa_vertikalnaya, tolko_tekst)"
                     % tip_verstki)


class NeBerus(Exception):
    """Вход внутри поддержанных типов, но ВНЕ проверенной области применимости.
    Отдельный класс, а не `ValueError`: «я этого не умею» и «ты дал ерунду» —
    разные ответы, и смешивать их в отчёте нельзя."""


# ═════════════ РАЗБОР СКОМПИЛИРОВАННОГО СЛАЙДА НА БЛОКИ ═════════════
class _ZonaParser(HTMLParser):
    """Верхнеуровневые блоки текстовой зоны + длина каждого В ЗНАКАХ, где формула
    посчитана по числу ВИДИМЫХ ГЛИФОВ (ветка `.katex-html`), а не по длине своего
    TeX-исходника и не по всему тексту KaTeX-разметки разом.

    🔴 Почему разбирается ГОТОВЫЙ HTML, а не карточка заново: второй разборщик
    markdown — это второй источник правды о том, что попадёт на слайд, и он
    разойдётся с `build_deck.render_md` на первом же краевом случае. Смета
    читает ровно то, что соберёт дека, и потому не может «не знать» про сцены,
    шторки и классы блоков."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bloki = []           # [{"tip": "p"|"li", "segmenty": [...], "klassy": [...], "ul": int|None}]
        self._stack = []
        self._zona_depth = None   # глубина, на которой открылась .t-body
        self._cur = None          # текущий накапливаемый блок
        self._katex_depth = None  # глубина открытия span.katex
        self._html_depth = None   # глубина открытия .katex-html внутри формулы
        self._glify = []
        self._ul_index = 0
        self._v_ul = None
        self._zagolovok = False
        self.est_zagolovok = False
        self._lst_depth = None    # глубина открытия .lst (display:block внутри абзаца)
        self._acc_depth = None    # глубина открытия .acc (жирный — шире обычного)

    # ── служебное
    @staticmethod
    def _klassy(attrs):
        d = dict(attrs)
        return (d.get("class") or "").split()

    def handle_starttag(self, tag, attrs):
        # пустой тег в стек НЕ кладём — закрывающего для него не придёт (см.
        # PUSTYE_TEGI). Но перенос строки он делает настоящий: `<br>` закрывает
        # текущий сегмент абзаца и открывает следующий.
        if tag in PUSTYE_TEGI:
            if tag == "br" and self._cur is not None and self._katex_depth is None:
                self._cur["segmenty"].append([])
            return
        self._stack.append(tag)
        d = len(self._stack)
        kl = self._klassy(attrs)

        if self._zona_depth is None:
            if "t-body" in kl:
                self._zona_depth = d
            return

        if self._katex_depth is not None:
            # внутри формулы считаем ТОЛЬКО ветку `.katex-html` — видимые глифы.
            # `.katex-mathml` рядом несёт тот же смысл для скринридеров, и её
            # текст удвоил бы длину формулы вдвое-втрое.
            if self._html_depth is None and "katex-html" in kl:
                self._html_depth = d
            return
        if "katex" in kl:
            self._katex_depth = d
            self._glify = []
            return

        if "zagolovok" in kl:
            self._zagolovok = True
            self.est_zagolovok = True
            return

        if "acc" in kl and self._acc_depth is None:
            self._acc_depth = d

        # ступенька `.lst` — блочная: своя строка, свой отступ слева
        if "lst" in kl and self._cur is not None and self._lst_depth is None:
            self._lst_depth = d
            self._cur["segmenty"].append([])
            self._cur.setdefault("lst", 0)
            self._cur["lst"] += 1
            return

        # верхний уровень зоны — прямые дети
        if d == self._zona_depth + 1:
            if tag == "ul":
                self._ul_index += 1
                self._v_ul = self._ul_index
            elif tag == "p":
                self._open("p", kl)
        elif self._v_ul is not None and tag == "li":
            self._open("li", kl)

    def _open(self, tip, kl):
        # блок хранится СЕГМЕНТАМИ: перенос `<br>` и блочная ступенька `.lst`
        # рвут строку принудительно, и суммировать знаки через них нельзя —
        # три коротких физических строки схлопнулись бы в одну расчётную.
        # 🔴 Сегмент хранит СПИСОК СЛОВ, а не сумму знаков. Причина — Расхождение 2
        # верификатора §3: `ceil(знаков / знаков_в_строке)` это НИЖНЯЯ оценка, а не
        # оценка. Браузер переносит по пробелам и слово пополам не рвёт, поэтому
        # строка систематически недозаполняется; формула вдобавок неразрывна
        # (`.katex{white-space:nowrap}`, base.css:191) и уезжает вниз целиком.
        # Предъявленный контрпример: карточка из одиннадцати слов по 26 знаков —
        # смета говорила «влезает, запас 4.16 строки», браузер обрезал текст.
        # Занижение — опасная сторона ошибки: это ПРОПУСК переполнения.
        self._cur = {"tip": tip, "segmenty": [[]], "klassy": kl, "ul": self._v_ul}

    def handle_startendtag(self, tag, attrs):
        """`<br/>` со слэшем. Базовый `HTMLParser` разворачивает его в пару
        starttag+endtag, и закрытие снимало со стека ЧУЖОЙ кадр (пустые теги мы
        туда не кладём) — стек уезжал в другую сторону, а блоки терялись так же
        молча, как и на `<br>` без слэша. Обе формы обязаны вести себя одинаково;
        сторожит это прямая проба в `fixtures/sborka/PROGNAT.sh`."""
        self.handle_starttag(tag, attrs)
        if tag not in PUSTYE_TEGI:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in PUSTYE_TEGI:
            return
        d = len(self._stack)
        if self._html_depth is not None and d == self._html_depth:
            self._html_depth = None
        elif self._katex_depth is not None and d == self._katex_depth:
            # формула закрылась — её вклад в длину абзаца в знаках-эквивалентах
            n_glif = len(re.sub(r"\s+", "", "".join(self._glify)))
            self._katex_depth = None
            if self._cur is not None:
                # формула — ОДНО неразрывное слово (`.katex{white-space:nowrap}`)
                self._cur["segmenty"][-1].append(znakov_formuly(n_glif))
                self._cur.setdefault("formul", 0)
                self._cur["formul"] += 1
                self._cur.setdefault("glif_len", 0)
                self._cur["glif_len"] += n_glif
        elif self._acc_depth is not None and d == self._acc_depth:
            self._acc_depth = None
        elif self._lst_depth is not None and d == self._lst_depth:
            self._lst_depth = None
            if self._cur is not None:
                self._cur["segmenty"].append([])
        elif self._zagolovok and tag == "div":
            self._zagolovok = False
        elif self._cur is not None and tag == self._cur["tip"]:
            self.bloki.append(self._cur)
            self._cur = None
        elif tag == "ul" and self._v_ul is not None and d == self._zona_depth + 1:
            self._v_ul = None
        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        if self._zona_depth is None or self._zagolovok:
            return
        if self._katex_depth is not None:
            if self._html_depth is not None:
                self._glify.append(data)
            return
        if self._cur is not None:
            # текст рвётся на слова по пробелам — ровно так, как это делает вёрстка.
            # Прилипание к предыдущему слову (`)` после формулы, запятая) — не новое
            # слово: ведущий пробел его и отличает.
            seg = self._cur["segmenty"][-1]
            hvost = not data[:1].isspace()
            k = K_ACC if self._acc_depth is not None else 1.0
            for i, slovo in enumerate(data.split()):
                if i == 0 and hvost and seg:
                    seg[-1] += len(slovo) * k
                else:
                    seg.append(len(slovo) * k)


def _bloki_slajda(slide_path):
    """Карточка → (params, блоки зоны). Браузер НЕ нужен."""
    sid, html = compile_slide_html(slide_path)
    p = _ZonaParser()
    p.feed(html)
    # параметры карточки нужны для kegl/lh/blok и типа вёрстки
    from formaty import parse_card
    md = Path(slide_path)
    if md.is_dir():
        md = md / "slaid.md"
    params, _ = parse_card(md.read_text(encoding="utf-8"), sid=sid)
    return sid, params, p.bloki, p.est_zagolovok


# ═════════════════════════ ФОРМУЛА СМЕТЫ (Э2.3) ═════════════════════════
def _chislo(params, key, default):
    v = params.get(key)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def smeta_slajda(slide_path):
    """Одна карточка → смета. Чистый питон, без браузера."""
    sid, params, bloki, est_zag = _bloki_slajda(slide_path)
    tip = params.get("tip_verstki")
    liniya = _chislo(params, "liniya", None)
    W, H = geometriya(tip, liniya)

    kegl = _chislo(params, "kegl_px", KEGL_DEFAULT)
    lh = _chislo(params, "mezhstrochye", LH_DEFAULT)
    blok_px = _chislo(params, "otstup_bloka", BLOK_DEFAULT)

    stroka_px = lh * kegl
    strok_v_zone = math.floor(H / stroka_px)
    znakov_v_stroke = math.floor(W / (K_ZNAK * kegl))
    # пункт списка уже, чем абзац, на свой отступ (`.tlist li{padding-left:1.15em}`)
    znakov_v_stroke_li = math.floor((W - LI_PAD_EM * kegl) / (K_ZNAK * kegl))
    if znakov_v_stroke < ZNAKOV_V_STROKE_MIN:
        raise NeBerus(
            "%d знаков в строке — уже проверенной границы %d (зона %dpx, кегль %g). "
            "На такой колонке смета систематически ЗАНИЖАЕТ объём (перенос по словам "
            "съедает край), а занижение — это пропуск переполнения. Мерь браузером: "
            "`gejt_vmeshcheniya.py`"
            % (znakov_v_stroke, ZNAKOV_V_STROKE_MIN, W, kegl))

    # 🔴 Заголовок входит И в высоту, И в счёт строк. Раньше он попадал только в
    # `vysota_px`, а `smeta_strok` — то самое число, которое сравнивает гейт
    # `--sverit`, — оказывалось занижено ровно на 78.44/58.06 = 1.35 строки на
    # каждой карточке с заголовком. Вердикт «влезает» при этом был верен, и
    # потому расхождение не кричало (нашёл верификатор §3: кластер −1.33/−1.34/
    # −1.35 на `demo-karta` и `zhivoj-teorkat`).
    vysota_px = ZAGOLOVOK_PX if est_zag else 0.0
    strok = vysota_px / stroka_px
    detali = []
    prev = None
    for b in bloki:
        if b["tip"] == "li":
            shirina = znakov_v_stroke_li
        elif b.get("lst"):
            shirina = math.floor((W - LST_PAD_EM * kegl) / (K_ZNAK * kegl))
        else:
            shirina = znakov_v_stroke
        # 🔴 Абзац из двух слов — это строка (заход, Э2.3): у `ulozhit` минимум 1.
        # Считаем ПОСЕГМЕНТНО: `<br>` и `.lst` рвут строку принудительно, и
        # укладка через разрыв дала бы одну расчётную строку вместо трёх.
        segmenty = [s for s in b["segmenty"] if s] or [[]]
        # `.op-def/.op-utv/.op-task` — свой кегль 0.8em и свой межстрочный 1.12
        # (`base.css:192-193`): их строка НИЖЕ основной (34.05px против 58.06), и
        # знаков в неё влезает по-другому. Одна `stroka_px` на все блоки завышала
        # такой блок на 0.41 строки (Расхождение 3 верификатора §3).
        est_op = any(k in OP_CLASSES for k in b["klassy"])
        kegl_bloka = OP_KEGL_EM * kegl if est_op else kegl
        stroka_bloka_px = (OP_LH * kegl_bloka) if est_op else stroka_px
        shirina_bloka = (math.floor(shirina * kegl / kegl_bloka) if est_op else shirina)
        n = sum(ulozhit(s, shirina_bloka) for s in segmenty)
        znakov = sum(sum(s) for s in b["segmenty"])
        # абзац, состоящий ровно из одной формулы, — «выносная»: её высота снята
        # замером и равна H_FORMULA строки, а не расчётной ширине текста
        if b.get("formul") == 1 and znakov <= znakov_formuly(b.get("glif_len", 0)) + 2:
            n = max(n, H_FORMULA)
        zazor = _zazor_px(prev, b, blok_px, kegl)
        # ступеньки внутри одного абзаца разделены `.spisok .lst + .lst`
        if b.get("lst", 0) > 1:
            zazor += LST_GAP_PX * (b["lst"] - 1)
        vysota_px += zazor + n * stroka_bloka_px
        strok += n * (stroka_bloka_px / stroka_px) + zazor / stroka_px
        detali.append({"tip": b["tip"], "znakov": round(znakov, 1), "strok": n,
                        "segmentov": len(segmenty), "lst": b.get("lst", 0),
                        "zazor_strok": round(zazor / stroka_px, 3)})
        prev = b

    return {
        "sid": sid, "tip_verstki": tip, "liniya": liniya,
        "W": W, "H": H, "kegl": kegl, "lh": lh, "blok_px": blok_px,
        "stroka_px": round(stroka_px, 3),
        "strok_v_zone": strok_v_zone,
        "znakov_v_stroke": znakov_v_stroke,
        "smeta_strok": round(strok, 2),
        "smeta_px": round(vysota_px, 1),
        "vlezaet": vysota_px <= H,
        "zapas_strok": round((H - vysota_px) / stroka_px, 2),
        "blokov": len(bloki), "detali": detali,
    }


def ulozhit(slova, znakov_v_stroke):
    """Слова → число СТРОК жадной укладкой, ровно как переносит браузер:
    слово целиком либо влезает в остаток строки, либо уезжает на следующую.
    Пробел между словами — один знак. Слово длиннее строки (длинная формула)
    занимает свою строку целиком и не рвётся (`white-space:nowrap`).

    🔴 Это замена `ceil(сумма_знаков / знаков_в_строке)`, которая была НИЖНЕЙ
    оценкой и давала пропуски переполнения (Расхождение 2 верификатора §3)."""
    if znakov_v_stroke <= 0:
        return 1
    strok, tekushchaya = 1, 0.0
    for w in slova:
        if tekushchaya <= 0:
            tekushchaya = w
        elif tekushchaya + 1 + w <= znakov_v_stroke:
            tekushchaya += 1 + w
        else:
            strok += 1
            tekushchaya = w
    return strok


def _zazor_px(prev, cur, blok_px, kegl):
    """Зазор ПЕРЕД блоком `cur` в px — ровно правила `base.css`, прочитанные, не
    угаданные.

    🔴 Поправка владельца: зазор — ДРОБНОЕ число строк, не «+1». Здесь он и
    остаётся дробным: считается в px и делится на `stroka_px` уже вызывающим.
    Кегль в отношении `blok_koef / lh` сокращается — потому зазор от кегля не
    зависит, и это проверка, что формула ВЫВЕДЕНА, а не подогнана."""
    if prev is None:
        # 🔴 Три правила `base.css` — БЕЗ комбинатора, они срабатывают и на ПЕРВОМ
        # ребёнке зоны, и margin там не схлопывается (у зоны есть padding-top):
        #   `.t-body ul.tlist{margin-top:var(--blok)}`     (base.css:26)
        #   `.t-body p.formula{margin-top:var(--blok)}`    (base.css:187)
        #   `.t-body p.op-*{margin-top:var(--blok)}`, но `:first-child` → .18em
        # Раньше первый блок безусловно получал 0. Доказательство одной карточкой
        # (верификатор §3): `napominanie` — единственная в L2, чья зона начинается
        # с `<ul>`; её расхождение было ровно −0.42 строки = 26/58.06 = 0.448, и
        # с этой правкой она даёт 7.96 против браузерных 7.94.
        if any(k in OP_CLASSES for k in cur["klassy"]):
            # `.18em` — от СОБСТВЕННОГО кегля элемента (0.8em), не от кегля зоны
            return OP_FIRST_EM * OP_KEGL_EM * kegl
        if cur["tip"] == "li" or "formula" in cur["klassy"]:
            return blok_px
        return 0.0
    if cur["tip"] == "li" and prev["tip"] == "li" and prev.get("ul") == cur.get("ul"):
        return LI_GAP_PX                      # `.tlist li + li`
    if cur["tip"] == "p" and any(k in OP_CLASSES for k in prev["klassy"]):
        return OP_NEXT_GAP_PX                 # `.t-body p.op-* + p`
    return blok_px                            # `p + p`, `ul.tlist`, `ul.tlist + p`


# ═════════════════════════ Э2.6. ОБРАТНЫЙ ХОД ═════════════════════════
def byudzhet(tip_verstki, liniya, kegl=KEGL_DEFAULT, lh=LH_DEFAULT, blok_px=BLOK_DEFAULT):
    """Бюджет В СТРОКАХ до написания текста — ответ фазе 2 на «влезет ли
    четвёртый блок», когда текста ещё нет."""
    W, H = geometriya(tip_verstki, liniya)
    stroka_px = lh * kegl
    strok = math.floor(H / stroka_px)
    znakov = math.floor(W / (K_ZNAK * kegl))
    # та же граница применимости, что и в смете по написанному: обратный ход не
    # вправе выдать бюджет там, где прямой ход отказывается считать
    if znakov < ZNAKOV_V_STROKE_MIN:
        raise NeBerus(
            "%s при liniya=%g даёт %d знаков в строке — уже проверенной границы %d. "
            "Смета на такой колонке занижает объём; выбери liniya шире либо мерь "
            "браузером после сборки." % (tip_verstki, liniya, znakov, ZNAKOV_V_STROKE_MIN))
    zazor_strok = blok_px / stroka_px
    return {"tip_verstki": tip_verstki, "liniya": liniya, "W": W, "H": H,
            "strok_v_zone": strok, "znakov_v_stroke": math.floor(W / (K_ZNAK * kegl)),
            "zazor_strok": round(zazor_strok, 3), "kegl": kegl, "lh": lh}


def _pechat_byudzheta(b):
    print("%s, liniya=%s → зона %dx%d px, кегль %g" % (
        b["tip_verstki"], b["liniya"], b["W"], b["H"], b["kegl"]))
    print("  БЮДЖЕТ: %d строк в зоне, %d знаков в строке, зазор между блоками %.2f строки"
          % (b["strok_v_zone"], b["znakov_v_stroke"], b["zazor_strok"]))
    z = b["zazor_strok"]
    for n_blokov, imena in ((3, "определение ≈3, пример ≈5, утверждение ≈3"),
                             (4, "плюс четвёртый блок")):
        rashod = n_blokov - 1
        ostatok = b["strok_v_zone"] - rashod * z
        print("  при %d блоках на зазоры уходит %.2f строки → на текст остаётся %.1f (%s)"
              % (n_blokov, rashod * z, ostatok, imena))


# ═════════════════════════ Э2.4. ГЕЙТ РАСХОЖДЕНИЯ ═════════════════════════
# 🔴 Без него первые три пункта сгниют за неделю: смета — это ВТОРАЯ модель
# вёрстки рядом с браузером, и расходиться она будет молча. Гейт краснеет НА
# СМЕТЕ («оценщик разошёлся с реальностью, калибруй»), а не на слайде.
#
# ДОПУСК — 1.5 строки, и это ЗАМЕРЕННОЕ число, а не круглое.
# Распределение |смета − браузер| по 14 мереным карточкам L2 (`--sverit --dopusk 999`):
#   0.02 0.02 0.03 0.03 0.03 0.05 0.05 0.42 0.93 0.95 0.96 0.96 0.98 1.03
# максимум 1.03 строки. Порог — наименьшее значение, при котором ни одна карточка
# не краснеет ложно (1.03), округлённое вверх до половины строки → 1.5.
#
# 🔴 Почему нельзя было взять «на глаз» побольше: допуск в 2.5 строки при зоне в
# 6 строк не отличает работающую смету от сломанной, и гейт стал бы украшением.
# Первая редакция сметы (формула по длине TeX) давала максимум 2.03 — и именно
# отказ расширить допуск под неё заставил найти настоящую меру длины формулы
# (глифы вместо знаков TeX). Допуск здесь — инструмент калибровки, а не отчётность.
#
# Пересняли калибровку — пересчитайте и это число той же командой:
#     python3 _generator/sborka/smeta.py --sverit teorkat-vvedenie/L2 --dopusk 999
DOPUSK_STROK = 1.5


def sverit(lekcija, dopusk=DOPUSK_STROK, isportit=1.0):
    """Смета против браузера по всем карточкам лекции. Возвращает список строк
    сверки; красным считается расхождение больше допуска."""
    import tempfile
    import vmeshchenie
    from playwright.sync_api import sync_playwright

    lek = Path(lekcija)
    slides = sorted((lek / "slajdy").glob("*/slaid.md"))
    out = []
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": HOLST_W, "height": HOLST_H}, device_scale_factor=1)
        p = Path(tmp) / "s.html"
        for md in slides:
            sid = md.parent.name
            try:
                s = smeta_slajda(md)
            except (ValueError, NeBerus) as e:
                out.append({"sid": sid, "propushcheno": str(e)})
                continue
            except Exception as e:
                # лекция без `math/katex.json` роняла сверку трейсбеком и теряла
                # вердикт по всем остальным карточкам (верификатор §3)
                out.append({"sid": sid, "propushcheno": "%s: %s" % (type(e).__name__, e)})
                continue
            _, html = compile_slide_html(md)
            p.write_text(html, encoding="utf-8")
            r = vmeshchenie.izmerit(page, p)
            stroka_px = r["line_height_px"] or s["stroka_px"]
            brauzer_strok = r["content_extent"] / stroka_px
            # `isportit` — проба «гейт умеет провалиться» (`--isportit`): смета
            # умножается на заведомо неверный множитель, и гейт ОБЯЗАН покраснеть.
            # Гейт, который не может покраснеть, — не гейт, а украшение; это ровно
            # тот приём, которым устроены ловушки фикстур этого репозитория.
            s["smeta_strok"] = round(s["smeta_strok"] * isportit, 2)
            out.append({
                "sid": sid,
                "smeta_strok": s["smeta_strok"],
                "brauzer_strok": round(brauzer_strok, 2),
                "zona_strok": s["strok_v_zone"],
                "rashozhdenie": round(s["smeta_strok"] - brauzer_strok, 2),
                "smeta_vlezaet": s["vlezaet"],
                "brauzer_vlezaet": r["content_extent"] <= r["content_h"] + 0.5,
            })
        b.close()
    for row in out:
        if "rashozhdenie" in row:
            row["gejt"] = "❌" if abs(row["rashozhdenie"]) > dopusk else "✅"
    return out


# ═════════════════════ ПРОВЕРКА ГЕОМЕТРИИ ЗАМЕРОМ ═════════════════════
def proverit_geometriyu():
    """Формула `geometriya()` обязана воспроизводить ЗАМЕР без расхождения.
    Это и есть страховка от «смета живёт своей жизнью»: padding поменяют в
    `tipy.py`/`base.css` — здесь покраснеет, а не разъедется молча."""
    import json
    import subprocess
    cmd = [sys.executable, str(SBORKA / "zamer_smety.py"), "--geometriya"]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(SBORKA.parent.parent))
    if r.returncode != 0:
        print("замер не отработал (rc=%d):\n%s" % (r.returncode, r.stderr[-2000:]), file=sys.stderr)
        return 2
    d = json.loads(r.stdout)["geometriya"]
    plohih, vsego = 0, 0
    for tip, rows in d["tipy"].items():
        for row in rows:
            vsego += 1
            liniya = row["liniya"] if tip.startswith("polosa_") else None
            W, H = geometriya(tip, liniya)
            ok = (abs(W - row["W"]) < 0.51 and abs(H - row["H"]) < 0.51)
            if not ok:
                plohih += 1
                print("❌ %s liniya=%s: формула %dx%d, замер %sx%s"
                      % (tip, row["liniya"], W, H, row["W"], row["H"]))
    zag = d["zagolovok_px"]
    if abs(zag - ZAGOLOVOK_PX) > 0.51:
        plohih += 1
        print("❌ ZAGOLOVOK_PX=%s, замер %s" % (ZAGOLOVOK_PX, zag))
    vsego += 1
    if plohih:
        print("\nГЕОМЕТРИЯ РАЗОШЛАСЬ С ЗАМЕРОМ: %d из %d точек" % (plohih, vsego))
        return 1
    print("✅ геометрия сметы воспроизводит замер точно: проверено %d точек из %d" % (vsego, vsego))
    return 0


# ═════════════════════════════════ CLI ═════════════════════════════════
def _tablica(rows):
    print("%-28s %6s %6s %6s  %s" % ("слайд", "смета", "зона", "запас", "вердикт"))
    for r in rows:
        if "propushcheno" in r:
            print("%-28s %6s %6s %6s  ⚪ %s" % (r["sid"], "—", "—", "—", r["propushcheno"][:60]))
            continue
        print("%-28s %6.2f %6d %6.2f  %s" % (
            r["sid"], r["smeta_strok"], r["strok_v_zone"], r["zapas_strok"],
            "влезает" if r["vlezaet"] else "❌ НЕ ВЛЕЗАЕТ"))


def main():
    ap = argparse.ArgumentParser(description="Смета вмещения — влезет ли текст, без браузера")
    ap.add_argument("cel", nargs="?", help="папка лекции или папка/файл слайда")
    ap.add_argument("--byudzhet", nargs=2, metavar=("TIP_VERSTKI", "LINIYA"))
    ap.add_argument("--sverit", metavar="LEKCIJA", help="Э2.4: гейт расхождения смета↔браузер")
    ap.add_argument("--dopusk", type=float, default=DOPUSK_STROK)
    ap.add_argument("--isportit", type=float, default=1.0, metavar="МНОЖИТЕЛЬ",
                     help="проба: умножить смету на заведомо неверный множитель — "
                          "гейт обязан покраснеть (доказательство, что он умеет)")
    ap.add_argument("--proverit-geometriyu", action="store_true")
    a = ap.parse_args()

    if a.proverit_geometriyu:
        return proverit_geometriyu()

    if a.byudzhet:
        tip, liniya = a.byudzhet
        # 🔴 Кривой вход отвергается ВНЯТНО, а не трейсбеком: неизвестный тип
        # вёрстки и нечисловая `liniya` — самые вероятные опечатки на фазе 2,
        # где этой командой и пользуются. Спутник-фикстура сторожит оба случая.
        try:
            liniya_f = float(liniya)
        except ValueError:
            print("ОШИБКА: liniya должна быть числом, получено %r" % liniya, file=sys.stderr)
            return 2
        try:
            _pechat_byudzheta(byudzhet(tip, liniya_f))
        except (ValueError, NeBerus) as e:
            print("ОШИБКА: %s" % e, file=sys.stderr)
            return 2
        return 0

    if a.sverit:
        if not (Path(a.sverit) / "slajdy").is_dir():
            print("ОШИБКА: %s — не папка лекции (нет подпапки slajdy/)" % a.sverit, file=sys.stderr)
            return 2
        rows = sverit(a.sverit, dopusk=a.dopusk, isportit=a.isportit)
        if a.isportit != 1.0:
            print("⚠ ПРОБА ПОРЧИ: смета умножена на %g — гейт обязан покраснеть\n" % a.isportit)
        print("%-28s %7s %8s %7s %s" % ("слайд", "смета", "браузер", "расх.", "гейт"))
        krasnyh = 0
        merenyh = 0
        for r in rows:
            if "propushcheno" in r:
                print("%-28s %7s %8s %7s ⚪ %s" % (r["sid"], "—", "—", "—", r["propushcheno"][:50]))
                continue
            merenyh += 1
            if r["gejt"] == "❌":
                krasnyh += 1
            print("%-28s %7.2f %8.2f %7.2f %s" % (
                r["sid"], r["smeta_strok"], r["brauzer_strok"], r["rashozhdenie"], r["gejt"]))
        print("\nдопуск: %.2f строки" % a.dopusk)
        if krasnyh:
            print("ГЕЙТ РАСХОЖДЕНИЯ КРАСНЫЙ: оценщик разошёлся с реальностью на %d карточке(ах) "
                  "из %d — калибруй смету, слайды тут ни при чём." % (krasnyh, merenyh),
                  file=sys.stderr)
            return 1
        print("ГЕЙТ РАСХОЖДЕНИЯ ЗЕЛЁНЫЙ: смета сошлась с браузером на всех %d мереных карточках "
              "(в допуске %.2f строки)." % (merenyh, a.dopusk))
        return 0

    if not a.cel:
        ap.error("нужна лекция/слайд, либо --byudzhet, либо --sverit")

    cel = Path(a.cel)
    if (cel / "slajdy").is_dir():
        slides = sorted((cel / "slajdy").glob("*/slaid.md"))
        if not slides:
            print("ОШИБКА: в %s/slajdy нет ни одной карточки slaid.md" % cel, file=sys.stderr)
            return 2
    else:
        md = cel / "slaid.md" if cel.is_dir() else cel
        if not md.is_file():
            print("ОШИБКА: %s — не папка лекции (нет slajdy/) и не карточка слайда"
                  % cel, file=sys.stderr)
            return 2
        slides = [md]
    rows = []
    for md in slides:
        try:
            rows.append(smeta_slajda(md))
        except (ValueError, NeBerus) as e:
            rows.append({"sid": Path(md).parent.name, "propushcheno": str(e)})
    _tablica(rows)
    merenyh = [r for r in rows if "propushcheno" not in r]
    ne_vlezaet = [r for r in merenyh if not r["vlezaet"]]
    print("\nСМЕТА: не влезает %d из %d мереных карточек (всего карточек %d, "
          "без текстовой зоны/неподдержанный тип — %d)"
          % (len(ne_vlezaet), len(merenyh), len(rows), len(rows) - len(merenyh)))
    if ne_vlezaet:
        print("не влезают: %s" % ", ".join(r["sid"] for r in ne_vlezaet))
    return 0


if __name__ == "__main__":
    sys.exit(main())
