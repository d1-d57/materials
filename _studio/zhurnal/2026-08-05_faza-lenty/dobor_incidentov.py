#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ДОБОР ИНЦИДЕНТОВ — что накопилось в журнале и не попало в корпус.

Читает четыре источника живого дерева, вытаскивает записи, у которых НАЗВАНА ЦЕНА,
вычитает всё, что уже учтено корпусом `2026-07-30_dovodka-fabriki`, и печатает остаток.

Три вещи, которые скрипт НЕ делает — по прямому запрету захода `kod_dobor-incidentov.md`:
  · не классифицирует по домам/фазам (колонка «дом» выходит пустой);
  · не правит корпус — все его файлы открываются только на чтение;
  · не выдумывает цену: `ЦЕНА:` в выходе — ДОСЛОВНАЯ подстрока источника. Не нашлось
    предложения, которое можно процитировать, — запись уходит в список «без цены».

Запуск:
    python3 dobor_incidentov.py --repo <корень materials> --out NOVYE-INCIDENTY.md
    python3 dobor_incidentov.py --repo <...> --ohvat        # только числа охвата
    python3 dobor_incidentov.py --repo <...> --kontrol      # положительный контроль
    python3 dobor_incidentov.py --repo <...> --vygruzki     # добавить транскрипты

Код возврата: 0 — отработал; 1 — упал; 2 — положительный контроль провален.
"""

import argparse
import glob
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

# ─────────────────────────────────────────────────────────────────────────────
# §0. Константы дома корпуса. Всё здесь — только на чтение.
# ─────────────────────────────────────────────────────────────────────────────

KORPUS_ARKA = "_studio/zhurnal/2026-07-30_dovodka-fabriki"
POKRYTIE = "_studio/konvejer/04.5-intervyu/POKRYTIE.md"
ZHURNAL = "_studio/zhurnal"

# Секции файла-захода, где живёт материал. Первая — жёсткого формата (`### ` + `ЦЕНА:`),
# остальные три — проза. `## УРОКИ ФАБРИКЕ` в таблице §2.2 захода не названа, но корпус её
# индексирует (адреса `kod_*.md#УРОКИ ФАБРИКЕ:83-85` в Разделе 1) — взята осознанно, см. ПЛАН §4.
SEKCII_ZAHODA_ZHESTKIE = ("УРОКИ ФАБРИКЕ",)
SEKCII_ZAHODA_PROZA = ("ОТЧЁТ", "ВОПРОСЫ", "ПРИЁМКА")

ZAGLUSHKA = re.compile(r"^### N\. <что произошло")

# ─────────────────────────────────────────────────────────────────────────────
# §1. Нормализация русского текста — общий язык всех сравнений
# ─────────────────────────────────────────────────────────────────────────────

STOP = set("""
это этот эта эти тот того том тем так такой такое также тоже там тут вот весь вся все всё всех
если чтобы потому因 что чего чем чему как когда где куда откуда почему зачем какой какая какие
для при про над под перед после между через без кроме кроме_того около вместо ради
был была было были быть есть нет ещё уже только даже лишь либо или ибо однако хотя пока
свой своя свои себя сам сама само себе него неё них ему ей им их его её
один одна одно одни два две три оба обе
может можно нужно надо должен должна должно должны стало стал стала стали
который которая которое которые которых котором
раз разом более менее очень просто именно почти совсем вовсе никак
делать сделать делал сделал делает работа работать
""".split())

OKONCHANIYA = (
    "ившись", "ывшись", "ующий", "ающий", "ившие", "ается", "аются", "ались",
    "ание", "ения", "ению", "ениях", "ением", "ениями", "иями", "ями", "ами",
    "ость", "ости", "остью", "ыми", "ими", "ого", "его", "ому", "ему", "ых", "их",
    "ая", "яя", "ое", "ее", "ые", "ие", "ый", "ий", "ой", "ей", "ую", "юю",
    "ешь", "ете", "ет", "ут", "ют", "ат", "ят", "ал", "ял", "ла", "ло", "ли",
    "ов", "ев", "ам", "ям", "ах", "ях", "ом", "ем", "ку", "ка", "ки", "ке",
    "ть", "ся", "сь", "а", "я", "о", "е", "ы", "и", "у", "ю", "ь", "й",
)


def stem(w):
    """Грубый стеммер: срезает самое длинное известное окончание, оставляя основу ≥4 знаков.

    Точность здесь не нужна и вредна: задача — свести «переписан/переписали/переписывание»
    к одной основе, а не построить морфологию. Ошибки стеммера симметричны для обеих
    сравниваемых сторон и потому в меру сдвигают порог, а не портят вердикт.
    """
    for suf in OKONCHANIYA:
        if len(w) - len(suf) >= 4 and w.endswith(suf):
            return w[: -len(suf)]
    return w


TOKEN = re.compile(r"[а-яa-z0-9_.-]+")


def normalizuj(text):
    t = unicodedata.normalize("NFKC", text).lower().replace("ё", "е")
    t = re.sub(r"`[^`]*`", " ", t)          # код и пути — не смысл записи
    t = re.sub(r"https?://\S+", " ", t)
    return t


def tokeny(text):
    """Множество основ значащих слов."""
    t = normalizuj(text)
    out = set()
    for w in TOKEN.findall(t):
        if len(w) < 4 or w in STOP:
            continue
        if w.replace(".", "").isdigit():
            continue
        out.add(stem(w))
    return out


def bigrammy(text):
    t = normalizuj(text)
    ws = [stem(w) for w in TOKEN.findall(t) if len(w) >= 4 and w not in STOP]
    return set(zip(ws, ws[1:]))


def chetverki(text):
    """Посимвольные 4-граммы значащих слов — канал против морфологии.

    Грубый стеммер разводит «прочтения» и «чтением» в разные основы, и на живом контроле
    ровно это роняло сопоставление: I0194 давал 0.32 при очевидном совпадении по существу.
    4-граммы такой пары общие («чтен»), и вердикт перестаёт зависеть от удачи стеммера.
    """
    t = normalizuj(text)
    out = set()
    for w in TOKEN.findall(t):
        if len(w) < 4 or w in STOP:
            continue
        for i in range(len(w) - 3):
            out.add(w[i:i + 4])
    return out


# ─────────────────────────────────────────────────────────────────────────────
# §2. Снимок — без него замер по живому дереву невоспроизводим
# ─────────────────────────────────────────────────────────────────────────────

def snimok(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read())
    st = os.stat(path)
    return {"sha1": h.hexdigest()[:12], "mtime": int(st.st_mtime), "bytes": st.st_size}


# ─────────────────────────────────────────────────────────────────────────────
# §3. Индекс корпуса — что УЖЕ учтено
# ─────────────────────────────────────────────────────────────────────────────

class Korpus:
    """Три канала знания корпуса о том, что он уже видел.

    А — адресный: `<арка>/UROKI-FABRIKE.md:<строка>`. Точен (дрейф 0 из 243+74).
    Б — текстовый: отпечатки записей (заголовок + цена + симптом группы).
    Оба строятся из ЖИВЫХ файлов корпуса; ни один не пишется.
    """

    def __init__(self, repo):
        self.repo = repo
        self.otpechatki = []      # {"id", "text", "toks", "bigr", "istochnik"}
        self.adresa_urokov = []   # (файл-относительно-zhurnal, строка)
        self.zapisi_ispolnitelej = []   # сырые строки skelet-ispolnitelej.tsv
        self.chitannye_fajly = set()    # файлы, которые корпус ФАКТИЧЕСКИ индексировал
        self.chitannye_suffiksy = set() # то же для адресов корпуса владельца/групп (хвост пути)
        self.diagnostika = {}

    # ── чтение ──────────────────────────────────────────────────────────────
    def _p(self, *parts):
        return os.path.join(self.repo, *parts)

    def load(self):
        self._load_skelet_ispolnitelej()
        self._load_skelet_vladelca()
        self._load_kratnost()
        self._load_adresa_grupp()
        self._load_razdely()
        self._load_adresa_urokov()
        return self

    def _load_skelet_ispolnitelej(self):
        p = self._p(KORPUS_ARKA, "skelet-ispolnitelej.tsv")
        n = 0
        with open(p, encoding="utf-8") as f:
            hdr = f.readline().rstrip("\n").split("\t")
            i_id, i_zag, i_adr, i_cen = 0, hdr.index("заголовок"), hdr.index("АДРЕС"), hdr.index("ЦЕНА")
            for line in f:
                c = line.rstrip("\n").split("\t")
                if len(c) <= i_cen:
                    continue
                rec = {"id": c[i_id], "zagolovok": c[i_zag], "adres": c[i_adr], "cena": c[i_cen]}
                self.zapisi_ispolnitelej.append(rec)
                mf = re.match(r"^\s*([^#]+\.md)", c[i_adr].strip())
                if mf:
                    self.chitannye_fajly.add(mf.group(1).strip())
                self._otpechatok(c[i_id], c[i_zag] + " " + c[i_cen], "skelet-ispolnitelej.tsv",
                                 "ispolnitel")
                n += 1
        self.diagnostika["skelet-ispolnitelej"] = n
        self.diagnostika["fajlov-v-indekse-korpusa"] = len(self.chitannye_fajly)

    def _load_skelet_vladelca(self):
        p = self._p(KORPUS_ARKA, "skelet-vladelca.tsv")
        n = 0
        with open(p, encoding="utf-8") as f:
            hdr = f.readline().rstrip("\n").split("\t")
            i_zag, i_adr = hdr.index("заголовок"), hdr.index("АДРЕС")
            for line in f:
                c = line.rstrip("\n").split("\t")
                if len(c) <= i_zag:
                    continue
                self._otpechatok(c[0], c[i_zag], "skelet-vladelca.tsv", "vladelec")
                self._suffiks(c[i_adr] if i_adr < len(c) else "")
                n += 1
        self.diagnostika["skelet-vladelca"] = n

    SUF = re.compile(r"([A-Za-zА-Яа-я0-9_.\- ]+/[A-Za-zА-Яа-я0-9_.\-]+\.md)")

    def _suffiks(self, adres):
        """Хвост пути из адреса корпуса: минимум две части, иначе `SESSIYA.md` совпадёт со всем."""
        for m in self.SUF.finditer(adres or ""):
            self.chitannye_suffiksy.add(m.group(1).strip())

    def _load_adresa_grupp(self):
        """Адреса групп Разделов 1–2: ещё один точный список того, что корпус ЧИТАЛ."""
        for nom in ("1", "2"):
            p = self._p(KORPUS_ARKA, "_data_razdel%s.py" % nom)
            if not os.path.exists(p):
                continue
            spec = importlib.util.spec_from_file_location("_dg%s" % nom, p)
            mod = importlib.util.module_from_spec(spec)
            _o = sys.stdout
            sys.stdout = open(os.devnull, "w")
            try:
                spec.loader.exec_module(mod)
            finally:
                sys.stdout.close()
                sys.stdout = _o
            for row in getattr(mod, "ROWS", []):
                for chast in str(row[3]).split(";"):
                    self._suffiks(chast)
        self.diagnostika["suffiksov-chitannyh"] = len(self.chitannye_suffiksy)

    def _load_kratnost(self):
        """Заголовки групп `KRATNOST.md` / `KRATNOST-vladelca.md` — формулировки МЕХАНИЗМА.

        Раньше здесь читались `_data_razdel1.py`/`_data_razdel2.py`, и это было ошибкой:
        в них `row[0]` — идентификатор (`КРТ-001a`), а не текст симптома, поэтому 703
        «отпечатка» давали ноль пригодных. Живой замер это и показал: в разбивке по
        источникам от Разделов 1 и 2 не было ни одного отпечатка. Текст механизма лежит
        в заголовках групп самих `KRATNOST*.md`.
        """
        n = 0
        for fajl, pat, tag in (
            ("KRATNOST.md", r"^## \d+\. (.+?) — \d+ вхожд\.", "ispolnitel"),
            ("KRATNOST-vladelca.md", r"^### \d+\. (.+?) — \d+ вхождений", "vladelec"),
        ):
            p = self._p(KORPUS_ARKA, fajl)
            if not os.path.exists(p):
                continue
            with open(p, encoding="utf-8") as f:
                for i, line in enumerate(f):
                    m = re.match(pat, line)
                    if m:
                        self._otpechatok("%s-%03d" % (fajl.split(".")[0][:4].upper(), i),
                                         m.group(1), fajl, tag)
                        n += 1
        self.diagnostika["zagolovki-kratnosti"] = n

    def _load_razdely(self):
        """Симптомы групп Раздела 5 — механизмы, сведённые по 243 урокам арок."""
        n = 0
        for nom in ("5",):
            p = self._p(KORPUS_ARKA, "_data_razdel%s.py" % nom)
            if not os.path.exists(p):
                continue
            spec = importlib.util.spec_from_file_location("_d%s" % nom, p)
            mod = importlib.util.module_from_spec(spec)
            _stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")     # модули печатают свои суммы при импорте
            try:
                spec.loader.exec_module(mod)
            finally:
                sys.stdout.close()
                sys.stdout = _stdout
            for i, row in enumerate(getattr(mod, "ROWS", [])):
                simptom = row[0]
                self._otpechatok("Р%s-%03d" % (nom, i), simptom, "_data_razdel%s.py" % nom,
                                 "ispolnitel")
                n += 1
        self.diagnostika["simptomy-razdelov"] = n

    def _load_adresa_urokov(self):
        """Канал А: адреса уроков арок из Раздела 5 (243) и POKRYTIE.md (74)."""
        p5 = self._p(KORPUS_ARKA, "_data_razdel5.py")
        spec = importlib.util.spec_from_file_location("_d5a", p5)
        mod = importlib.util.module_from_spec(spec)
        _stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.stdout.close()
            sys.stdout = _stdout
        n5 = 0
        for row in mod.ROWS:
            for chast in row[3].split(";"):
                chast = chast.strip()
                if not chast:
                    continue
                m = re.match(r"(.+?):([\d,]+)$", chast)
                if not m:
                    continue
                for ln in m.group(2).split(","):
                    self.adresa_urokov.append((m.group(1).strip(), int(ln)))
                    n5 += 1
        self.diagnostika["adresa-razdel5"] = n5

        nI = 0
        with open(self._p(POKRYTIE), encoding="utf-8") as f:
            for line in f:
                for m in re.finditer(r"`([^`]+?):(\d+)`", line):
                    ref = m.group(1)
                    if "UROKI-FABRIKE" not in ref and not ref.startswith("…"):
                        continue
                    self.adresa_urokov.append((ref.lstrip("…"), int(m.group(2))))
                    nI += 1
        self.diagnostika["adresa-pokrytie"] = nI

    def _otpechatok(self, ident, text, istochnik, tag="ispolnitel"):
        """tag: `ispolnitel` — корпус про работу исполнителей; `vladelec` — реплики владельца.

        Разделение не косметическое. Корпус владельца — замечания про содержание лекций и
        слайдов, снятые с репетиций; сравнивать с ними инцидент из отчёта захода — почти
        всегда шум. Замер: 1354 отпечатка владельца при медиане 6 значащих слов, из них 506
        короче шести — короткий отпечаток целиком «содержится» в любом длинном абзаце, и мера
        даёт 1.00 на записях, не имеющих между собой ничего общего (поймано на примере 3
        выхода: «Узкая полоса, забитая мелкими картинками» ↔ запись про `accent_tag`).
        Поэтому отпечатки владельца применяются только к дневникам и транскриптам.
        """
        t = tokeny(text)
        if len(t) < 3:
            return
        self.otpechatki.append({"id": ident, "text": text, "toks": t,
                                "ch4": chetverki(text), "bigr": bigrammy(text),
                                "istochnik": istochnik, "tag": tag})

    def korpus_chital(self, fajl):
        """Открывал ли корпус ЭТОТ файл. Твёрдый факт, а не догадка по тексту.

        Прямые пути берутся из `skelet-ispolnitelej.tsv`; корпус владельца и группы
        Разделов 1–2 адресуют файлы хвостом пути (`teorkat-motivacia/SESSIYA.md:423`),
        поэтому для них — совпадение по хвосту минимум из двух частей пути.
        """
        if fajl in self.chitannye_fajly:
            return True
        return any(fajl.endswith("/" + suf) for suf in self.chitannye_suffiksy)

    def otpechatki_dlya(self, vid):
        """Какие отпечатки корпуса применимы к записи этого вида."""
        if vid in ("дневник", "транскрипт"):
            return self.otpechatki
        return [o for o in self.otpechatki if o["tag"] != "vladelec"]

    # ── канал А ─────────────────────────────────────────────────────────────
    def razreshit_adresa(self, fajly_urokov):
        """Сокращённые ссылки (`…dovodka-l1`, `konspekt-l1/UROKI-FABRIKE.md`) → живые пути.

        Возвращает (список (путь, строка), список неразрешённых).
        """
        resheno, ne_resheno = [], []
        for ref, line in self.adresa_urokov:
            if "UROKI-FABRIKE" in ref:
                hvost = ref.split("zhurnal/")[-1]
                papka = hvost.split("/")[0]
            else:
                papka = ref
            kand = [f for f in fajly_urokov if os.path.dirname(f).endswith(papka) or papka in os.path.dirname(f)]
            if len(kand) == 1:
                resheno.append((kand[0], line))
            elif len(kand) > 1:
                resheno.append((kand[0], line))
                ne_resheno.append((ref, line, "неоднозначно: " + ",".join(kand)))
            else:
                ne_resheno.append((ref, line, "не найдено"))
        return resheno, ne_resheno


# ─────────────────────────────────────────────────────────────────────────────
# §4. Цена — распознаётся ЦИТАТОЙ, не пересказом
# ─────────────────────────────────────────────────────────────────────────────

# Четыре формы, названные владельцем поимённо (§2.1 захода), + общий счёт.
FORMY_CENY = [
    ("переделка артефакта", re.compile(
        r"(переписан\w*\s+(дважды|трижды|заново|целиком)|переписал\w*\s+\w+\s+дважды"
        r"|пересобра\w+|переделыва\w+|переделать|переделан\w*|пересчитан\w*\s+заново"
        r"|\d+\s*(редакци\w+|верси\w+)\s+(за|списка|документа)|две редакции|негодн\w+ артефакт\w*"
        r"|раздел переписан|переписан\w*\s+повторно|откачен\w*|откатил\w*"
        r"|снят\w*\s+и\s+переписан\w*)", re.I)),
    ("повторный вызов одного и того же", re.compile(
        r"((дважды|трижды|четырежды|\d+\s*раз[аы]?)\s+(подряд|повтор\w*|вызыва\w+|прогн\w+|спрашива\w+"
        r"|останавлива\w+|заявл\w+|съеха\w+|переформулирова\w+)"
        r"|\d+\s*(повторн\w+\s+)?вызов\w*\s+двер\w+|повторн\w+\s+(вызов|прогон|греп|ретрай)"
        r"|потребовал\w*\s+повторн\w+|\d+\s*кругов?\s+подгонк\w+)", re.I)),
    # 🔴 Форма «обход гейта» — самая ложносрабатывающая: слово `--no-verify` стоит в КАЖДОМ
    # отчёте, чаще всего в предложении «обходов не было». Поэтому требуется не упоминание,
    # а СВИДЕТЕЛЬСТВО, что обход случился: глагол совершения, ненулевое число или прямое
    # описание ложно-зелёного гейта.
    ("обход гейта", re.compile(
        r"((пришлось|потребовал\w*|ушл[ои]|применил\w*|применён|обошёл|обошл\w+|сделан\s+обход"
        r"|записан\s+обход)[^.;]{0,60}(--no-verify|обход\w*)"
        r"|(--no-verify|обход\w*)[^.;]{0,40}(пришлось|потребовал\w*|применён|сделан)"
        r"|[1-9]\d*\s+обход\w+|обход\w+\s*[—:-]?\s*[1-9]\d*"
        r"|ложно-?зелён\w+|зелён\w+\s+по\s+построению"
        r"|гейт\w*\s+(не\s+увидел|промолча\w+|пропустил\w*|был\s+зелён\w*))", re.I)),
    ("круг диагностики поломки, которой не было", re.compile(
        r"(круг\w*\s+(диагностик\w+|объяснени\w+|правк\w+|обсуждени\w+|сверк\w+|непринятия)"
        r"|ушёл\s+(целый\s+)?круг|потрачен\w*\s+впустую|раунд\w*\s+(потрачен|обсуждени\w+)\s*впустую"
        r"|диагностик\w+\s+того,?\s+чего\s+не\s+было|в\s+пустоту|впустую)", re.I)),
    ("общий счёт потерь", re.compile(
        r"(стоил\w*\s+\w+|цена\s+в\s+\w+|ушл[ои]\s+\d+|ушёл\s+\w+\s*(ход|круг|прогон)"
        r"|не\s+удалось|провалил[оа]сь|оказал\w+\s+неисполним"
        r"|(один|одна|два|две|три|четыре|пять|шесть|семь|восемь|девять|десять|целый|лишний)\s+"
        r"(лишн\w+\s+)?(ход|круг|заход|прогон|коммит|сесси\w+|день|дня|час|раунд)"
        r"|\d+\s*(лишн\w+\s+)?(ход\w*|заход\w*|прогон\w*|сесси\w+|минут\w*|часов?|суток|сутки)"
        r"\s+(на|впустую|потерян\w*|ушл\w*|стоил\w*|разбор\w*|диагностик\w*|сверк\w*|доказательств\w*)"
        r"|≈?\s*\d+[\s ]*(тыс\.?|тысяч)\s*токен\w*|поймал\s+владелец|нашёл\s+владелец"
        r"|заворачива\w+\s+целиком|заход\s+провален)", re.I)),
]

# Блоки, которые вообще не являются записями об инциденте: обязательные строки формы отчёта.
SLUZHEBNYJ_BLOK = re.compile(
    r"^\s*(\*\*)?(КОММИТ|АРТЕФАКТ|НЕОБРАТИМОЕ|ДОМ|ДОСТАВЛЕНО|ВЕРДИКТ|Ту же причину)", re.I)

# 🔴 Отрицание рядом с шаблоном цены. «Обходов `--no-verify` не было» и «ни одна строка не
# потеряна» — это ОТЧЁТ ОБ ОТСУТСТВИИ поломки, а не цена. Без этой проверки прозаический канал
# ловит их наравне с настоящими: замер до её введения — 453 «новых», из них большинство такие.
OTRICANIE = re.compile(
    r"(не\s+был[оаи]?\b|не\s+случил\w*|не\s+потребовал\w*|не\s+понадобил\w*|не\s+пришлось"
    r"|не\s+потерян\w*|не\s+тронул\w*|не\s+делал\w*|не\s+чинил\w*|не\s+встретил\w*|не\s+нашёл\w*"
    r"|не\s+примен\w*|не\s+установлен\w*|не\s+измен\w*|не\s+переделыва\w*|не\s+переписыва\w*"
    r"|не\s+возвраща\w*|не\s+удал\w*|не\s+переименован\w*|не\s+включал\w*"
    r"|ни\s+одн\w+|ни\s+разу|ничего\b|ноль\b|нулев\w+|пусто\b|обошлось\b|обхода\s+не"
    r"|потерь\s+нет|цена\s+пока\s+нулев|без\s+`?--no-verify|прошл[иа]\s+без"
    r"|обходов\s*[—:-]?\s*0\b|0\s*(обходов|потерь|срывов|ошибок)|—\s*0\b|:\s*0\b"
    r"|провер\w+,?\s+а\s+не\s+заявлен)", re.I)

# Локальное отрицание: частица «не»/«без» непосредственно ПЕРЕД сработавшим шаблоном.
# Проверка по предложению целиком слишком груба — «переделали X, а Y не трогали» законно
# несёт цену; проверка вплотную к совпадению ловит ровно «этого НЕ было».
OTRICANIE_RYADOM = re.compile(r"(\bне\b|\bНЕ\b|\bбез\b|\bБЕЗ\b|\bни\b)[^.;]{0,25}$")


# Сигнал «здесь описана поломка». Без него блок вообще не кандидат — иначе список
# «без цены» вбирает всю прозу отчётов и перестаёт быть списком.
SIGNAL_PROBLEMY = re.compile(
    r"(сломал\w*|ошибк\w+|ошибочн\w+|не\s+сработал\w*|не\s+заработал\w*|не\s+увидел\w*|не\s+поймал\w*"
    r"|провал\w+|упал\w*|падает|роня\w+|краснее?т|покраснел\w*|красн\w+|rc=1|дефект\w*|бра[кк]\w*"
    r"|неверн\w+|неточн\w+|устарел\w+|врёт|ложн\w+|молча|конфликт\w*|противореч\w+|разошл\w+|разъеха\w+"
    r"|дубл\w+|сирот\w+|потер\w+|дрейф\w*|промах\w*|мимо|запрещ\w+\s+и\s+требу\w+|неисполним\w+"
    r"|невыполним\w+|не\s+может\s+провалиться|обход\w*|--no-verify|фантом\w*|выдум\w+|досочин\w+"
    r"|пропущен\w*|пропуск\w*|слепая\s+зона|не\s+покрыва\w+|переписан\w+|переделыва\w+|впустую"
    r"|откачен\w*|откатил\w*|оборвал\w*|регресси\w+|не\s+удалось|провалил\w*|поймал\w+"
    r"|артефакт\w*\s+хуже|переразмет\w*|подхватыва\w+|подмен\w+|неисполним\w*)", re.I)


def najti_cenu(text):
    """Возвращает (форма, дословная цитата) либо (None, None).

    Цитата — ПРЕДЛОЖЕНИЕ ИСТОЧНИКА, в котором сработал шаблон, обрезанное по краям.
    Никакой генерации: если процитировать нечего, цены нет.
    """
    # Жёсткий формат имеет приоритет: строка `ЦЕНА: …` — она уже и есть цитата.
    # 🔴 Вариантов написания четыре, и узкий шаблон `^ЦЕНА:` видит только один. Замер по
    # живым файлам-заходам: `ЦЕНА:` — 12, `   ЦЕНА:` с отступом — 7, `**ЦЕНА:**` жирным — 6.
    # Верификатор нашёл 10 записей с ЦЕНОЙ, которых инструмент не увидел, и у большинства
    # причина была ровно эта.
    m = re.search(r"^\s*\*{0,2}ЦЕНА\s*(?:\([^)]{0,40}\))?\s*:\*{0,2}\s*(.+)$", text, re.M)
    if m:
        znach = m.group(1).strip().strip("*").strip()
        if znach and not znach.startswith("<") and not znach.startswith("обязательна"):
            return "строка `ЦЕНА:` (жёсткий формат)", znach

    predlozheniya = razbit_na_predlozheniya(text)
    for forma, pat in FORMY_CENY:
        for p in predlozheniya:
            mm = pat.search(p)
            if not mm:
                continue
            # отрицание в том же предложении снимает цену: это отчёт об ОТСУТСТВИИ поломки
            if OTRICANIE.search(p):
                continue
            if OTRICANIE_RYADOM.search(p[:mm.start()]):
                continue
            return forma, p.strip()
    return None, None


def razbit_na_predlozheniya(text):
    t = re.sub(r"\s+", " ", text.replace("\n", " "))
    # точка-разделитель, но не внутри сокращений/чисел/путей
    parts = re.split(r"(?<=[.!?;])\s+(?=[А-ЯA-ZЁ«**`\d])", t)
    return [p for p in parts if len(p) > 25]


# ─────────────────────────────────────────────────────────────────────────────
# §5. Чтение источников
# ─────────────────────────────────────────────────────────────────────────────

class Zapis:
    __slots__ = ("vid", "fajl", "sekcia", "ot", "do", "zagolovok", "telo", "kontekst",
                 "cena", "forma_ceny", "status", "pochemu", "dubli_s", "ballov", "adresa")

    def __init__(self, vid, fajl, sekcia, ot, do, zagolovok, telo):
        self.kontekst = None
        self.vid = vid
        self.fajl = fajl
        self.sekcia = sekcia
        self.ot = ot
        self.do = do
        self.zagolovok = zagolovok
        self.telo = telo
        self.cena = None
        self.forma_ceny = None
        self.status = None
        self.pochemu = ""
        self.dubli_s = []
        self.ballov = 0.0
        self.adresa = []

    @property
    def polnyj(self):
        return self.zagolovok + "\n" + self.telo

    @property
    def adres(self):
        return "%s#%s:%d-%d" % (self.fajl, self.sekcia, self.ot, self.do)


def sekcii_md(lines, uroven, kod_skryvaet=True):
    """Разбор `## `/`### ` секций: [(заголовок, строка_начала, строка_конца)]. 1-индексация.

    🔴 `kod_skryvaet=False` для `UROKI-FABRIKE.md`, и это не небрежность.
    В `2026-07-30_dovodka-l1/UROKI-FABRIKE.md` ограда ```` ``` ```` открыта на строке 11 и
    закрыта на 32, а внутри лежат ДВА настоящих урока (строки 12 и 29) — файл собран криво.
    Парсер, уважающий ограду, теряет их молча; корпус их видит, потому что ограду не знает.
    Расхождение измеримо: с оградой мой счёт даёт 341 секцию против 343 у корпуса, и оба
    потерянных урока несут `ЦЕНА:`. Ставлю совместимость с корпусом выше формальной
    правильности разбора — иначе улов и корпус считают разные множества.
    """
    marker = "#" * uroven + " "
    out, cur, st = [], None, None
    v_kode = False
    for i, ln in enumerate(lines, 1):
        if ln.startswith("```"):
            v_kode = not v_kode
        if (not (v_kode and kod_skryvaet)) and ln.startswith(marker) and not ln.startswith(marker + "#"):
            if cur is not None:
                out.append((cur, st, i - 1))
            cur, st = ln[len(marker):].strip(), i
    if cur is not None:
        out.append((cur, st, len(lines)))
    return out


def chitat_uroki(repo, fajly):
    """Источник 1 — уроки арок. Жёсткий формат, берётся целиком."""
    zapisi = []
    for rel in fajly:
        p = os.path.join(repo, ZHURNAL, rel)
        lines = open(p, encoding="utf-8").readlines()
        for zag, ot, do in sekcii_md(lines, 3, kod_skryvaet=False):
            if ZAGLUSHKA.match("### " + zag):
                continue
            telo = "".join(lines[ot:do])
            zapisi.append(Zapis("урок арки", "%s/%s" % (ZHURNAL, rel), "урок", ot, do, zag, telo))
    return zapisi


def bloki_prozy(lines, ot, do):
    """Проза секции → блоки-кандидаты с адресом.

    Границы: пустая строка, `### `, нумерованный/маркированный пункт, строка-таблица.
    🔴 Строки-цитаты (`> …`) ВЫБРАСЫВАЮТСЯ: в файлах-заходах это врезка шаблона, дословно
    одинаковая в 35 файлах (`grep -l "Оформи ПУНКТОМ ОЧЕРЕДИ"`), и она несёт слова «ЦЕНА»,
    «поймал владелец», «обход» — то есть выглядит записью об инциденте, ею не будучи.
    """
    bloki, cur, cur_ot = [], [], None
    v_kode = False

    def sbros(konec):
        if cur and any(x.strip() for x in cur):
            bloki.append(("".join(cur), cur_ot, konec))

    for i in range(ot, min(do, len(lines))):
        ln = lines[i]
        n = i + 1
        if ln.startswith("```"):
            v_kode = not v_kode
            if cur:
                sbros(n - 1)
                cur, cur_ot = [], None
            continue
        if v_kode:
            continue
        if ln.lstrip().startswith(">"):
            if cur:
                sbros(n - 1)
                cur, cur_ot = [], None
            continue
        granica = (
            not ln.strip()
            or ln.startswith("### ")
            or re.match(r"^\s*[-*·]\s", ln)
            or re.match(r"^\s*\d+\.\s", ln)
            or ln.startswith("**")
            or ln.startswith("| ")
            or ln.startswith("🔴")
            or ln.startswith("⚠")
        )
        if granica and cur:
            sbros(n - 1)
            cur, cur_ot = [], None
        if not ln.strip():
            continue
        if cur_ot is None:
            cur_ot = n
        cur.append(ln)
    sbros(min(do, len(lines)))
    # склейка слишком коротких хвостов с предыдущим блоком — пункт из двух слов не запись
    sklejka = []
    for t, a, b in bloki:
        if sklejka and len(t.split()) < 12:
            pt, pa, pb = sklejka[-1]
            sklejka[-1] = (pt + t, pa, b)
        else:
            sklejka.append((t, a, b))
    return [(t, a, b) for t, a, b in sklejka
            if len(t.split()) >= 12 and not SLUZHEBNYJ_BLOK.match(t)]


ZONY_ZAHODA = ("УРОКИ ФАБРИКЕ", "ОТЧЁТ", "ВОПРОСЫ", "ПРИЁМКА", "ПЛАН",
               "ЗАДАЧА", "ЗАДАНИЕ", "КОНТРАКТ", "ДИСЦИПЛИНА", "ВЕРИФИКАТОР",
               "КОММИТ", "ПЕРВЫЙ ХОД", "ЦЕЛЬ", "КОНТЕКСТ")


def zony_zahoda(lines):
    """Зоны файла-захода, где подзаголовки `## ` НЕ обрывают зону.

    🔴 Найдено живым замером, а не предположено. Исполнители пишут отчёт с подразделами
    того же уровня (`## 🎯 ВЕРДИКТ §2.1`, `## Что сделал и ЗАЧЕМ`), и наивный разбор по
    `## ` даёт секцию `ОТЧЁТ` длиной в ОДНУ строку: в `kod_nno-i-shkolnye-opory.md`
    отчёт занимает строки 160–312, а `## ОТЧЁТ` кончается на 161. По этой причине
    73 адреса корпуса из 330 не находили живого блока вовсе.

    Правило: заголовок с ИЗВЕСТНЫМ именем открывает зону, любой другой — подраздел
    текущей зоны. Заголовки до первой известной зоны отбрасываются.
    """
    syrye = sekcii_md(lines, 2)
    zony, tek = [], None
    for zag, ot, do in syrye:
        imya = re.sub(r"^#*\s*", "", zag.split("—")[0].strip().rstrip(" ·")).strip()
        klyuch = re.sub(r"^[\d.\s]+", "", imya).upper()
        izvestnaya = next((s for s in ZONY_ZAHODA if klyuch.startswith(s)), None)
        if izvestnaya:
            zony.append([izvestnaya, ot, do])
            tek = zony[-1]
        elif tek is not None:
            tek[2] = do
    return [tuple(z) for z in zony]


def chitat_zahody(repo):
    """Источник 2 — файлы-заходы. Жёсткие секции целиком, прозаические — блоками."""
    zapisi = []
    fajly = sorted(glob.glob(os.path.join(repo, ZHURNAL, "*", "kod_*.md")))
    for p in fajly:
        rel = os.path.relpath(p, repo)
        lines = open(p, encoding="utf-8").readlines()
        for imya, ot, do in zony_zahoda(lines):
            klyuch = imya
            if any(klyuch.startswith(s) for s in SEKCII_ZAHODA_ZHESTKIE):
                for z2, o2, d2 in sekcii_md(lines[:do], 3):
                    if o2 <= ot or ZAGLUSHKA.match("### " + z2):
                        continue
                    telo = "".join(lines[o2:min(d2, do)])
                    zapisi.append(Zapis("урок в заходе", rel, imya, o2, min(d2, do), z2, telo))
            elif any(klyuch.startswith(s) for s in SEKCII_ZAHODA_PROZA):
                for telo, o2, d2 in bloki_prozy(lines, ot, do):
                    zag2 = pervaya_fraza(telo)
                    zapisi.append(Zapis("проза захода", rel, imya, o2, d2, zag2, telo))
    return zapisi, len(fajly)


def chitat_dnevniki(repo):
    """Источник 3 — дневники арок."""
    zapisi = []
    fajly = sorted(glob.glob(os.path.join(repo, ZHURNAL, "*", "SESSIYA.md")))
    for p in fajly:
        rel = os.path.relpath(p, repo)
        lines = open(p, encoding="utf-8").readlines()
        for zag, ot, do in sekcii_md(lines, 2):
            for telo, o2, d2 in bloki_prozy(lines, ot, do):
                zapisi.append(Zapis("дневник", rel, zag[:40], o2, d2, pervaya_fraza(telo), telo))
    return zapisi, len(fajly)


def chitat_vygruzki(repo):
    """Источник 4 — транскрипты. Самый дорогой; включается флагом."""
    zapisi = []
    fajly = sorted(glob.glob(os.path.join(repo, ZHURNAL, "*", "VYGRUZKA*.md")))
    for p in fajly:
        rel = os.path.relpath(p, repo)
        lines = open(p, encoding="utf-8").readlines()
        for zag, ot, do in sekcii_md(lines, 3):
            telo = "".join(lines[ot:do])
            if len(telo.split()) < 12:
                continue
            zapisi.append(Zapis("транскрипт", rel, "реплика " + zag, ot, do, pervaya_fraza(telo), telo))
    return zapisi, len(fajly)


# Ширина окна контекста подобрана замером, а не на глаз: узнавание записей корпуса при
# пороге 0.50 даёт ±1 → 92.1 %, ±2 → 94.4 %, ±3 → 96.3 %. Дальше ±2 не иду: окно, вбирающее
# семь соседних абзацев, начнёт совпадать со всем подряд, и вторая ошибка (склеить разное,
# то есть ПОТЕРЯТЬ инцидент) вырастет незаметно — её этот замер не видит.
OKNO = 2


def prostavit_kontekst(zapisi):
    """Контекст блока = он сам плюс соседи по той же секции того же файла.

    Единица корпуса крупнее моей: человек, писавший заголовок записи, читал абзац целиком.
    Сравнивать его пересказ с одним моим блоком — сравнивать разные по масштабу вещи;
    на контроле это давало 0.30 там, где совпадение очевидно.
    """
    po_sekcii = defaultdict(list)
    for z in zapisi:
        po_sekcii[(z.fajl, z.sekcia)].append(z)
    for gruppa in po_sekcii.values():
        gruppa.sort(key=lambda z: z.ot)
        for i, z in enumerate(gruppa):
            okno = gruppa[max(0, i - OKNO):i + OKNO + 1]
            z.kontekst = z.zagolovok + "\n" + "\n".join(x.telo for x in okno)


def pervaya_fraza(telo):
    """Заголовок блока — первая содержательная фраза, очищенная от разметки.

    Разметку снимаем ПЕРЕД тем, как резать: иначе заголовок начинается с обрубка
    `**И главное, ради чего…`, и запись в таблице нечитаема.
    """
    t = re.sub(r"\s+", " ", telo.strip())
    t = re.sub(r"^(?:[\d]+\.|[-*·>]|🔴|⚠|⭐|📊|🎯)\s*", "", t)
    t = re.sub(r"^\*{1,2}\s*", "", t).lstrip("«\"' ")
    t = t.replace("**", "")
    chasti = razbit_na_predlozheniya(t) or [t]
    s = chasti[0]
    i = 1
    while len(s) < 60 and i < len(chasti):     # обрубок в одно слово — не заголовок
        s += " " + chasti[i]
        i += 1
    return (s[:200] + "…") if len(s) > 200 else s


# ─────────────────────────────────────────────────────────────────────────────
# §6. Дедупликация
# ─────────────────────────────────────────────────────────────────────────────

# 🔴 Пороги выбраны ПО ИЗМЕРЕННОЙ КРИВОЙ, а не на глаз. Прогон `--kontrol` считает, какую
# долю записей корпуса, лежащих в области инструмента, дедупликация опознаёт при каждом пороге:
#     0.40 → 96.6 %   0.45 → 94.8 %   0.50 → 92.1 %   0.55 → 87.3 %   0.60 → 82.8 %
# Ниже 0.50 растёт вторая ошибка — склеивание разного, то есть ПОТЕРЯННЫЙ инцидент; выше 0.55
# падает узнавание известного, то есть ЛОЖНЫЙ РОСТ корпуса. Взят 0.50, а вся полоса 0.40–0.50
# не решается молча — она уходит владельцу отдельным списком (§2.3 захода).
PORO_DUBL = 0.50
PORO_SPOR = 0.40
MIN_PERESECHENIE = 4      # абсолютный пол: короткий отпечаток не должен совпадать «случайно»
# Короткий отпечаток КОРПУСА ВЛАДЕЛЬЦА не сравнивается контейнментом: 506 из 1354 таких
# отпечатков короче шести значащих слов, и любые пять частых слов «содержатся» в длинном
# абзаце целиком. Отпечатки про работу исполнителей (Р5, KRATNOST) коротки по природе
# («Новые .md не зарегистрированы в KARTA §6») и это ограничение к ним не применяется —
# проверено на контроле: с ним I0371 падает с 0.53 до 0.25 и перестаёт опознаваться.
MIN_OTPECHATKA = 6


def shozhest(otpechatok, prof):
    """Асимметричная мера: НАСКОЛЬКО отпечаток корпуса содержится в записи.

    Симметричный Жаккар здесь неприменим: отпечаток корпуса — одна строка-пересказ,
    написанная человеком, читавшим ВЕСЬ окружающий абзац; запись — один блок. Жаккар
    между ними низок даже у прямого дубля (замерено на контроле: 0.30–0.40 у записей,
    совпадающих по существу). Поэтому:

      · основа — контейнмент отпечатка в КОНТЕКСТЕ записи (блок ± соседи по секции);
      · второй канал — тот же контейнмент по 4-граммам, против морфологии;
      · третий — Жаккар по заголовкам, для случая «обе стороны коротки и говорят одно»;
      · биграммы добавляют вес совпадению порядка слов, а не только словаря.
    """
    A = otpechatok["toks"]
    if not A:
        return 0.0, 0
    if otpechatok["tag"] == "vladelec":
        # Отпечаток корпуса владельца — короткая реплика (медиана 6 значащих слов, 506 из
        # 1354 короче шести). Контейнмент такого отпечатка в абзаце — величина без смысла:
        # пять частых слов найдутся где угодно, и мера даёт 1.00 на записях, не имеющих
        # ничего общего. Поэтому с ним — только СИММЕТРИЧНЫЙ Жаккар против заголовка
        # записи, где длины сопоставимы.
        obj = A | prof["zag"]
        return (len(A & prof["zag"]) / len(obj) if obj else 0.0), len(A & prof["zag"])
    peres = A & prof["toks"]
    ch4 = otpechatok["ch4"]
    ch4_kont = (len(ch4 & prof["ch4"]) / len(ch4)) if ch4 else 0.0
    if len(peres) < MIN_PERESECHENIE and ch4_kont < 0.45:
        return 0.0, len(peres)
    konteinment = len(peres) / len(A)
    zag_j = 0.0
    if prof["zag"]:
        obj = A | prof["zag"]
        zag_j = len(A & prof["zag"]) / len(obj) if obj else 0.0
    bigr = 0.0
    if otpechatok["bigr"] and prof["bigr"]:
        bigr = len(otpechatok["bigr"] & prof["bigr"]) / len(otpechatok["bigr"])
    osnova = max(konteinment, 0.95 * ch4_kont, zag_j)
    ball = osnova * 0.8 + bigr * 0.2
    return ball, len(peres)


def profil(z):
    """Профиль записи для сравнения. Считается один раз, используется многократно."""
    tekst = z.kontekst or z.polnyj
    return {"toks": tokeny(tekst), "ch4": chetverki(tekst),
            "bigr": bigrammy(tekst), "zag": tokeny(z.zagolovok)}


def dedup_po_korpusu(zapisi, korpus, pokrytye_adresa):
    """Канал А (адресный, уроки арок) + канал Б (текстовый, всё остальное).

    🔴 Для уроков арок канал А — ОКОНЧАТЕЛЬНЫЙ, канал Б его не отменяет. Причина не
    техническая: единица корпуса — ГРУППА механизма с кратностью, и новый урок, повторяющий
    известный механизм, — это не дубль записи, а +1 к кратности группы. Дать каналу Б
    понизить его до дубля значило бы потерять само вхождение. Совпадение с симптомом
    группы поэтому пишется отдельной пометкой «механизм известен», а не статусом.
    """
    for z in zapisi:
        # ── канал А ──
        if z.vid == "урок арки":
            klyuch = (z.fajl, z.ot, z.do)
            if klyuch in pokrytye_adresa:
                z.status = "уже в корпусе"
                z.pochemu = "канал А (адрес): %s" % pokrytye_adresa[klyuch]
                z.ballov = 1.0
                continue
            prof = profil(z)
            luchshij, ball = None, 0.0
            for o in korpus.otpechatki_dlya(z.vid):
                b, _ = shozhest(o, prof)
                if b > ball:
                    ball, luchshij = b, o
            z.ballov = round(ball, 3)
            z.status = "новое"
            if luchshij:
                z.dubli_s = [(luchshij["id"], luchshij["istochnik"], luchshij["text"][:160])]
            z.pochemu = "канал А: адреса нет в корпусе ⇒ вхождение новое"
            if ball >= PORO_DUBL:
                z.pochemu += "; механизм известен (%s, балл %.2f) ⇒ +1 к кратности группы" % (
                    luchshij["id"], ball)
            continue
        # ── канал Б ──
        prof = profil(z)
        luchshij, ball = None, 0.0
        for o in korpus.otpechatki_dlya(z.vid):
            b, _ = shozhest(o, prof)
            if b > ball:
                ball, luchshij = b, o
        z.ballov = round(ball, 3)
        if luchshij:
            z.dubli_s = [(luchshij["id"], luchshij["istochnik"], luchshij["text"][:160])]
        if ball >= PORO_DUBL:
            # 🔴 Совпадение текста ЕЩЁ НЕ ЗНАЧИТ, что запись уже в корпусе. Разводим два
            # разных факта, которые одна мера сливает в один:
            #   · корпус ЧИТАЛ этот файл и записал оттуда — тогда это дубль записи;
            #   · корпус этот файл НЕ ОТКРЫВАЛ — тогда механизм известен, а вхождение новое,
            #     и по методу самого корпуса (группа + кратность) оно даёт кратности +1.
            # Замер, из-за которого это разведено: 238 совпадений из 240 пришлись на файлы,
            # которых корпус не открывал ни разу. Назвать их «уже в корпусе» значило бы
            # потерять неделю работы под видом дедупликации.
            if korpus.korpus_chital(z.fajl):
                z.status = "уже в корпусе"
                z.pochemu = "канал Б (текст), балл %.2f ↔ %s; файл корпусом читан" % (ball, luchshij["id"])
            else:
                z.status = "новое вхождение известного механизма"
                z.pochemu = ("канал Б: механизм известен (%s, балл %.2f), но файла `%s` "
                             "в индексе корпуса НЕТ ⇒ вхождение новое, кратности +1"
                             % (luchshij["id"], ball, os.path.basename(z.fajl)))
        elif ball >= PORO_SPOR:
            z.status = "спорный"
            z.pochemu = "канал Б (текст), балл %.2f ↔ %s — ниже порога дубля, выше порога шума" % (ball, luchshij["id"])
        else:
            z.status = "новое"
            z.pochemu = "ближайший отпечаток корпуса — балл %.2f" % ball
    return zapisi


def dedup_vnutri_ulova(novye):
    """Канал В: один инцидент, рассказанный уроком и пересказанный отчётом.

    Схлопывается в одну запись с несколькими адресами — так же, как кратность в корпусе.
    Первенство отдаётся жёсткому формату: урок арки > урок в заходе > проза.
    """
    ves = {"урок арки": 3, "урок в заходе": 2, "проза захода": 1, "дневник": 1, "транскрипт": 0}
    novye = sorted(novye, key=lambda z: (-ves.get(z.vid, 0), z.fajl, z.ot))
    ostavleno, sklejek = [], 0
    kesh = [(z, tokeny(z.polnyj), bigrammy(z.polnyj)) for z in novye]
    prinyato = []
    for z, t, b in kesh:
        sliyanie = None
        for pz, pt, pb in prinyato:
            obj = t | pt
            j = len(t & pt) / len(obj) if obj else 0.0
            jb = (len(b & pb) / len(b | pb)) if (b or pb) else 0.0
            if 0.6 * j + 0.4 * jb >= 0.45:
                sliyanie = pz
                break
        if sliyanie is not None:
            sliyanie.adresa.append(z.adres)
            sklejek += 1
        else:
            prinyato.append((z, t, b))
            ostavleno.append(z)
    return ostavleno, sklejek


# ─────────────────────────────────────────────────────────────────────────────
# §6½. Отсечка по СОДЕРЖАНИЮ (§2.2 захода: «не по mtime»)
# ─────────────────────────────────────────────────────────────────────────────

OTSECHKA = "2026-07-30"          # дата сборки корпуса, названная заходом
DATA_KORPUSA = "2026-08-05"      # дата данных, которую корпус несёт сам (шапки KARTOTEKA/POKRYTIE)

DATA_V_TEKSTE = re.compile(r"20\d{2}-\d{2}-\d{2}")
DATA_ARKI = re.compile(r"zhurnal/(\d{4}-\d{2}-\d{2})_")
DATA_TOCHKOJ = re.compile(r"\b(\d{2})\.(\d{2})\b")   # «07.08» — принятая в журнале форма


def data_zapisi(z):
    """Дата записи ПО СОДЕРЖАНИЮ, не по mtime. Три источника, берётся самая поздняя.

    1) явная дата в тексте блока (`2026-08-07` или журнальное «07.08»);
    2) дата арки из имени папки;
    3) нет ни того, ни другого — `None` (инфраструктурные арки без даты в имени).
    """
    kand = []
    m = DATA_ARKI.search(z.fajl)
    if m:
        kand.append(m.group(1))
    for d in DATA_V_TEKSTE.findall(z.polnyj):
        kand.append(d)
    for dd, mm in DATA_TOCHKOJ.findall(z.polnyj):
        if 1 <= int(mm) <= 12 and 1 <= int(dd) <= 31:
            kand.append("2026-%s-%s" % (mm, dd))
    return max(kand) if kand else None


def posle_otsechki(z):
    """True — запись относится ко времени ПОСЛЕ сборки корпуса.

    Арка без даты в имени (`_INFRA-git`, `_SHTAB-*`) не отсекается: она ведётся непрерывно,
    и отбросить её значило бы потерять живой автолог. Такие записи помечаются отдельно.
    """
    d = data_zapisi(z)
    return (d is None) or (d >= OTSECHKA)


def bloki_shablona(zapisi, porog=3):
    """Блок, дословно повторённый в ≥`porog` РАЗНЫХ файлах, — врезка шаблона, не запись.

    Проверяется по первым 14 значащим словам: хвост врезки в разных заходах слегка правят,
    начало — нет. Возвращает множество таких «отпечатков начала».
    """
    po_nachalu = defaultdict(set)
    for z in zapisi:
        ws = [w for w in TOKEN.findall(normalizuj(z.polnyj)) if len(w) >= 4]
        if len(ws) < 8:
            continue
        po_nachalu[" ".join(ws[:14])].add(z.fajl)
    return {k for k, v in po_nachalu.items() if len(v) >= porog}


def sila_signala(text):
    """Сколько РАЗНЫХ маркеров поломки в блоке. Ранг для списка «без цены», не вердикт."""
    return len(set(x.lower() for x in SIGNAL_PROBLEMY.findall(text)))


def otpechatok_nachala(z):
    ws = [w for w in TOKEN.findall(normalizuj(z.polnyj)) if len(w) >= 4]
    return " ".join(ws[:14]) if len(ws) >= 8 else None


# ─────────────────────────────────────────────────────────────────────────────
# §7. Сборка
# ─────────────────────────────────────────────────────────────────────────────

def sobrat(repo, s_vygruzkami=False):
    itog = {"snimok": {}, "ohvat": {}, "diagnostika": {}}

    fajly_urokov = sorted(
        os.path.relpath(p, os.path.join(repo, ZHURNAL))
        for p in glob.glob(os.path.join(repo, ZHURNAL, "*", "UROKI-FABRIKE.md"))
        if "_TEMPLATE-arka" not in p
    )

    korpus = Korpus(repo).load()
    itog["diagnostika"]["korpus"] = dict(korpus.diagnostika)
    itog["diagnostika"]["otpechatkov"] = len(korpus.otpechatki)

    # канал А: адреса → живые секции
    resheno, ne_resheno = korpus.razreshit_adresa(fajly_urokov)
    itog["diagnostika"]["adresov-ne-razresheno"] = len(ne_resheno)

    uroki = chitat_uroki(repo, fajly_urokov)
    pokrytye = {}
    promahov = 0
    for ref, line in resheno:
        popal = False
        for z in uroki:
            if z.fajl.endswith(ref) and z.ot <= line <= z.do:
                pokrytye[(z.fajl, z.ot, z.do)] = "%s:%d" % (ref, line)
                popal = True
                break
        if not popal:
            promahov += 1
    itog["diagnostika"]["adresov-mimo-zhivoj-sekcii"] = promahov
    itog["diagnostika"]["sekcij-pokryto-adresom"] = len(pokrytye)

    zahody, n_zahodov = chitat_zahody(repo)
    dnevniki, n_dnevnikov = chitat_dnevniki(repo)
    vygruzki, n_vygruzok = ([], len(glob.glob(os.path.join(repo, ZHURNAL, "*", "VYGRUZKA*.md"))))
    if s_vygruzkami:
        vygruzki, n_vygruzok = chitat_vygruzki(repo)

    itog["ohvat"] = {
        "uroki-fabrike": {"fajlov": len(fajly_urokov), "prochitano": len(fajly_urokov),
                          "zapisej": len(uroki)},
        "kod-zahody": {"fajlov": n_zahodov, "prochitano": n_zahodov, "blokov": len(zahody)},
        "sessiya": {"fajlov": n_dnevnikov, "prochitano": n_dnevnikov, "blokov": len(dnevniki)},
        "vygruzki": {"fajlov": n_vygruzok, "prochitano": n_vygruzok if s_vygruzkami else 0,
                     "blokov": len(vygruzki)},
    }

    # снимок — всё, что прочитано
    snim = {}
    for rel in fajly_urokov:
        p = os.path.join(repo, ZHURNAL, rel)
        snim[os.path.relpath(p, repo)] = snimok(p)
    for pat in ("kod_*.md", "SESSIYA.md") + (("VYGRUZKA*.md",) if s_vygruzkami else ()):
        for p in sorted(glob.glob(os.path.join(repo, ZHURNAL, "*", pat))):
            snim[os.path.relpath(p, repo)] = snimok(p)
    itog["snimok"] = snim

    vse = uroki + zahody + dnevniki + vygruzki
    prostavit_kontekst(vse)
    itog["diagnostika"]["blokov-vsego"] = len(vse)

    # фильтр «врезка шаблона, повторённая в разных файлах»
    shablonnye = bloki_shablona(vse)
    ne_shablon = [z for z in vse if otpechatok_nachala(z) not in shablonnye]
    itog["diagnostika"]["blokov-shablona-otbrosheno"] = len(vse) - len(ne_shablon)

    # фильтр «здесь описана поломка»
    kandidaty = [z for z in ne_shablon
                 if z.vid in ("урок арки", "урок в заходе") or SIGNAL_PROBLEMY.search(z.polnyj)]
    itog["diagnostika"]["kandidatov-s-signalom-problemy"] = len(kandidaty)

    # цена
    for z in kandidaty:
        z.forma_ceny, z.cena = najti_cenu(z.polnyj)
    s_cenoj_vse = [z for z in kandidaty if z.cena]
    bez_ceny_vse = [z for z in kandidaty if not z.cena]

    # ── отсечка ПО СОДЕРЖАНИЮ ──
    s_cenoj = [z for z in s_cenoj_vse if posle_otsechki(z)]
    do_otsechki = [z for z in s_cenoj_vse if not posle_otsechki(z)]
    bez_ceny = [z for z in bez_ceny_vse if posle_otsechki(z)]
    itog["diagnostika"]["s-cenoj-ves-zhurnal"] = len(s_cenoj_vse)
    itog["diagnostika"]["s-cenoj-do-otsechki"] = len(do_otsechki)

    # дедуп по корпусу
    dedup_po_korpusu(s_cenoj, korpus, pokrytye)
    dubli = [z for z in s_cenoj if z.status == "уже в корпусе"]
    spornye = [z for z in s_cenoj if z.status == "спорный"]
    povtory = [z for z in s_cenoj if z.status == "новое вхождение известного механизма"]
    novye_syrye = [z for z in s_cenoj if z.status == "новое"]

    # дедуп внутри улова
    novye, sklejek = dedup_vnutri_ulova(novye_syrye)
    povtory, sklejek_p = dedup_vnutri_ulova(povtory)

    # «без цены» тоже прогоняется через дедуп — иначе список раздувается известным
    dedup_po_korpusu(bez_ceny, korpus, pokrytye)
    bez_ceny_novye, sklejek_bc = dedup_vnutri_ulova([z for z in bez_ceny if z.status == "новое"])

    # то же по записям ДО отсечки — только чтобы назвать число, не для улова
    dedup_po_korpusu(do_otsechki, korpus, pokrytye)
    do_otsechki_novye = [z for z in do_otsechki if z.status == "новое"]

    itog["chisla"] = {
        "istochnikov-prosmotreno": sum(v["prochitano"] for v in itog["ohvat"].values()),
        "blokov-vsego": len(vse),
        "blokov-shablona": len(vse) - len(ne_shablon),
        "kandidatov": len(kandidaty),
        "s-cenoj-ves-zhurnal": len(s_cenoj_vse),
        "s-cenoj": len(s_cenoj),
        "do-otsechki-vsego": len(do_otsechki),
        "do-otsechki-ne-v-korpuse": len(do_otsechki_novye),
        "bez-ceny": len(bez_ceny),
        "bez-ceny-novyh": len(bez_ceny_novye),
        "bez-ceny-signalov-3": sum(1 for z in bez_ceny_novye if sila_signala(z.polnyj) >= 3),
        "dublej": len(dubli),
        "povtorov": len(povtory),
        "spornyh": len(spornye),
        "novyh-do-skleiki": len(novye_syrye),
        "sklejek-vnutri-ulova": sklejek,
        "novyh": len(novye),
    }
    return itog, {"novye": novye, "dubli": dubli, "spornye": spornye, "povtory": povtory,
                  "bez_ceny": bez_ceny_novye, "do_otsechki": do_otsechki_novye,
                  "korpus": korpus, "uroki": uroki, "pokrytye": pokrytye, "vse": vse}


# ─────────────────────────────────────────────────────────────────────────────
# §8. Положительный контроль (условие 5 критерия готовности)
# ─────────────────────────────────────────────────────────────────────────────

# Пять записей корпуса, собранных 30.07 (`skelet-ispolnitelej.tsv`), из ПЯТИ разных арок и
# четырёх разных секций. Инструмент ОБЯЗАН опознать их как дубли.
# Выбраны только среди секций, которые этот инструмент читает: 330 записей корпуса из 461
# лежат в `ОТЧЁТ`/`ВОПРОСЫ`/`ПРИЁМКА`/`УРОКИ ФАБРИКЕ`, остальные 131 — в `ЗАДАНИЕ`/`ПЛАН`,
# и это область не инструмента, а составителя захода (см. отчёт, «слепые зоны»).
KONTROL = ["I0019", "I0064", "I0194", "I0256", "I0371"]

SEKCII_V_OBLASTI = ("ОТЧЁТ", "ВОПРОСЫ", "ПРИЁМКА", "УРОКИ")


def _proverit_zapis(rec, vse, korpus, pokrytye):
    """Прогон ОДНОЙ записи корпуса через ту же дедупликацию. Без обходных путей."""
    fajl, sek, a, b = razobrat_adres(rec["adres"])
    nakryv = [z for z in vse if z.fajl == fajl and not (z.do < a or z.ot > (b or a))]
    po_sekcii = [z for z in vse if z.fajl == fajl and sek
                 and z.sekcia.upper().startswith(sek.upper().split()[0])]
    kand = nakryv or po_sekcii
    if not kand:
        return None, None
    dedup_po_korpusu(kand, korpus, pokrytye)
    luchshij = max(kand, key=lambda z: z.ballov)
    return luchshij, luchshij.status == "уже в корпусе"


def kontrol(repo, ids=None):
    ids = ids or KONTROL
    itog, d = sobrat(repo)
    korpus, vse = d["korpus"], d["vse"]
    po_id = {r["id"]: r for r in korpus.zapisi_ispolnitelej}

    print("═══ ПОЛОЖИТЕЛЬНЫЙ КОНТРОЛЬ — пять записей корпуса 30.07 ═══")
    print("Условие 5 критерия: все пять обязаны быть опознаны как дубли.\n")
    provaleno = []
    for rid in ids:
        rec = po_id.get(rid)
        if rec is None:
            print("  %s — НЕТ В КОРПУСЕ (ошибка выбора контроля)" % rid)
            provaleno.append(rid)
            continue
        luchshij, ok = _proverit_zapis(rec, vse, korpus, d["pokrytye"])
        if luchshij is None:
            print("  %s — адрес вне области инструмента: %s" % (rid, rec["adres"]))
            provaleno.append(rid)
            continue
        print("  %s  %s (балл %.2f)" % (rid, "✅ опознан дублем" if ok else "❌ НЕ опознан",
                                        luchshij.ballov))
        print("        корпус говорит:  %s" % rec["zagolovok"][:100])
        print("        адрес корпуса:   %s" % rec["adres"])
        print("        живой блок:      %s" % luchshij.adres)
        print("        сработало:       %s" % luchshij.pochemu)
        if not ok:
            provaleno.append(rid)

    print()
    print("Итог по пяти: опознано %d из %d." % (len(ids) - len(provaleno), len(ids)))
    if provaleno:
        print("🔴 УСЛОВИЕ 5 ПРОВАЛЕНО на: %s" % ", ".join(provaleno))

    # ── шире, чем требует условие 5: полный прогон по всем записям корпуса в области ──
    print()
    print("═══ ТОТ ЖЕ КОНТРОЛЬ, НО ПОЛНЫМ ОХВАТОМ — не 5, а все записи корпуса в области ═══")
    v_oblasti = []
    for r in korpus.zapisi_ispolnitelej:
        _, sek, _, _ = razobrat_adres(r["adres"])
        if sek and sek.upper().startswith(SEKCII_V_OBLASTI):
            v_oblasti.append(r)
    opoznano = ne_opoznano = ne_najdeno = 0
    primery = []
    for r in v_oblasti:
        luchshij, ok = _proverit_zapis(r, vse, korpus, d["pokrytye"])
        if luchshij is None:
            ne_najdeno += 1
        elif ok:
            opoznano += 1
        else:
            ne_opoznano += 1
            if len(primery) < 5:
                primery.append((r["id"], r["zagolovok"][:70], luchshij.ballov))
    vsego = len(v_oblasti)
    najdeno = opoznano + ne_opoznano
    print("  записей корпуса всего: %d, из них в области инструмента: %d" % (
        len(korpus.zapisi_ispolnitelej), vsego))
    print("  живого блока по адресу не нашлось: %d — это вопрос ОХВАТА, не дедупликации" % ne_najdeno)
    print("  осталось проверяемых:  %d" % najdeno)
    print("  ОПОЗНАНО ДУБЛЯМИ:      %d из %d (%.1f %%)" % (opoznano, najdeno, 100.0 * opoznano / najdeno))
    print("  не опознано:           %d" % ne_opoznano)
    if primery:
        print("  примеры неопознанных:")
        for i, z, b in primery:
            print("     %s  балл %.2f  %s" % (i, b, z))
    print()
    print("  ⚠ Это НЕ 100 %, и так и должно быть: часть адресов корпуса указывает на секции,")
    print("    которых этот инструмент не читает по построению, а часть блоков разбита им")
    print("    иначе, чем разбивал человек. Число названо, чтобы «опознаёт дубли» было")
    print("    величиной, а не заявлением.")

    if provaleno:
        return 2
    print()
    print("✅ Условие 5 выполнено: все пять опознаны как дубли.")
    return 0


def razobrat_adres(addr):
    m = re.match(r"^\s*([^#]+\.md)(?:#([^,]*))?(?:,\s*строк[аи]?\s*(\d+)(?:[–-](\d+))?)?", addr)
    if not m:
        return addr.strip(), None, 0, 0
    f = m.group(1).strip()
    sek = (m.group(2) or "").strip()
    a = int(m.group(3)) if m.group(3) else 0
    b = int(m.group(4)) if m.group(4) else a
    return f, sek, a, b


# ─────────────────────────────────────────────────────────────────────────────
# §9. Выход
# ─────────────────────────────────────────────────────────────────────────────

def ekranirovat(s):
    return re.sub(r"\s+", " ", s).replace("|", "\\|").strip()


def pisat_vyhod(path, itog, d, repo, s_vygruzkami):
    ch = itog["chisla"]
    o = itog["ohvat"]
    L = []
    A = L.append
    A("---")
    A("tab: Новые инциденты — улов после корпуса")
    A("status: sobran")
    A("poryadok: 1")
    A("---")
    A("")
    A("# НОВЫЕ ИНЦИДЕНТЫ — улов добора, не разложенный по домам")
    A("")
    A("> **Что это.** Остаток, который живой журнал накопил сверх корпуса")
    A("> `2026-07-30_dovodka-fabriki/KARTOTEKA-problem.md`. Собран программно —")
    A("> `dobor_incidentov.py` этой же папки, — и только он вправе этот файл переписывать.")
    A("> Колонка **дом пустая намеренно**: границы домов двигает заход")
    A("> `kod_pereschet-i-schetchik.md`, раскладка — следующий ход, не этот.")
    A(">")
    A("> **Как пересчитать (числа командой, не руками — `KONSTITUCIYA §10`):**")
    A("> ```")
    A("> python3 _studio/zhurnal/2026-08-05_faza-lenty/dobor_incidentov.py --repo . --ohvat")
    A("> grep -c '^| НОВ-' _studio/zhurnal/2026-08-05_faza-lenty/NOVYE-INCIDENTY.md")
    A("> grep -c 'ЦЕНА:' _studio/zhurnal/2026-08-05_faza-lenty/NOVYE-INCIDENTY.md")
    A("> ```")
    A("")
    A("## Числа улова")
    A("")
    A("| величина | число |")
    A("|---|---|")
    A("| источников просмотрено (файлов) | **%d** |" % ch["istochnikov-prosmotreno"])
    A("| блоков прочитано всего | %d |" % ch["blokov-vsego"])
    A("| из них несут сигнал поломки (кандидаты) | %d |" % ch["kandidatov"])
    A("| записей с ЦЕНОЙ по всему журналу | %d |" % ch["s-cenoj-ves-zhurnal"])
    A("| — отсечено как «до 30.07» | %d |" % ch["do-otsechki-vsego"])
    A("| **найдено записей с ЦЕНОЙ после отсечки** | **%d** |" % ch["s-cenoj"])
    A("| — дублей: запись уже в корпусе | **%d** |" % ch["dublej"])
    A("| — спорных: решает владелец | **%d** |" % ch["spornyh"])
    A("| — **новых вхождений известного механизма** (Раздел 2) | **%d** |" % ch["povtorov"])
    A("| — **совсем новых** (Раздел 1) | **%d** |" % ch["novyh"])
    A("| **ИТОГО В УЛОВЕ** (Раздел 1 + Раздел 2) | **%d** |" % (ch["novyh"] + ch["povtorov"]))
    A("| без цены (требует глаза), уже за вычетом известного | **%d** |" % ch["bez-ceny-novyh"])
    A("")
    A("🔴 **Почему «дубль» и «новое вхождение» — РАЗНЫЕ вердикты, а не один.** Совпадение")
    A("текста с записью корпуса значит одно из двух, и различает их твёрдый факт: индексировал")
    A("ли корпус ЭТОТ ФАЙЛ вообще. Корпус физически открыл **%d файлов** (`skelet-ispolnitelej.tsv`," % itog["diagnostika"]["korpus"]["fajlov-v-indekse-korpusa"])
    A("колонка `АДРЕС`). Если файла там нет, совпадение означает «механизм известен», а не")
    A("«запись уже есть», и по методу самого корпуса (группа + кратность) такое вхождение даёт")
    A("группе **+1 к кратности**. Свалить их в «дубли» значило бы объявить учтённой неделю")
    A("работы: из %d текстовых совпадений в файлах вне индекса корпуса — %d." % (
        ch["povtorov"] + ch["dublej"], ch["povtorov"]))
    A("")
    A("**Охват по источникам — существует / прочитано:**")
    A("")
    A("| источник | файлов существует | прочитано | блоков |")
    A("|---|---|---|---|")
    A("| `*/UROKI-FABRIKE.md` | %d | %d | %d |" % (o["uroki-fabrike"]["fajlov"], o["uroki-fabrike"]["prochitano"], o["uroki-fabrike"]["zapisej"]))
    A("| `*/kod_*.md` | %d | %d | %d |" % (o["kod-zahody"]["fajlov"], o["kod-zahody"]["prochitano"], o["kod-zahody"]["blokov"]))
    A("| `*/SESSIYA.md` | %d | %d | %d |" % (o["sessiya"]["fajlov"], o["sessiya"]["prochitano"], o["sessiya"]["blokov"]))
    A("| `*/VYGRUZKA*.md` | %d | %d | %d |" % (o["vygruzki"]["fajlov"], o["vygruzki"]["prochitano"], o["vygruzki"]["blokov"]))
    A("")
    if not s_vygruzkami:
        A("*Транскрипты не читались: заход велит брать их последними и только если первых трёх мало.*")
        A("*Включаются флагом `--vygruzki`; число «прочитано 0» здесь — решение, а не пропуск.*")
        A("")

    A("## Раздел 1 · НОВЫЕ ЗАПИСИ — %d" % ch["novyh"])
    A("")
    A("> `дом` пуст намеренно (см. шапку). `ЦЕНА` — **дословная цитата источника**;")
    A("> скрипт цену не формулирует, он её находит или признаётся, что не нашёл.")
    A("")
    A("| id | дом | что произошло | ЦЕНА | откуда | статус |")
    A("|---|---|---|---|---|---|")
    for i, z in enumerate(d["novye"], 1):
        adr = "`%s`" % z.adres
        if z.adresa:
            adr += " (+%d: %s)" % (len(z.adresa), "; ".join("`%s`" % a for a in z.adresa[:3]))
        A("| НОВ-%03d |  | %s | ЦЕНА: %s | %s | новое |" % (
            i, ekranirovat(z.zagolovok)[:300], ekranirovat(z.cena)[:400], ekranirovat(adr)))
    A("")

    A("## Раздел 2 · НОВЫЕ ВХОЖДЕНИЯ ИЗВЕСТНЫХ МЕХАНИЗМОВ — %d" % ch["povtorov"])
    A("")
    A("> Механизм корпус знает, но **этого вхождения у него нет**: файл в индекс корпуса не")
    A("> входит. По методу корпуса такая запись — кратность +1 к существующей группе, а не")
    A("> новая группа. Колонка «группа корпуса» называет, к какой именно.")
    A("")
    A("| id | дом | что произошло | ЦЕНА | откуда | группа корпуса | балл |")
    A("|---|---|---|---|---|---|---|")
    for i, z in enumerate(d["povtory"], 1):
        gr = z.dubli_s[0] if z.dubli_s else ("—", "—", "—")
        adr = "`%s`" % z.adres
        if z.adresa:
            adr += " (+%d)" % len(z.adresa)
        A("| ПВТ-%03d |  | %s | ЦЕНА: %s | %s | %s · %s | %.2f |" % (
            i, ekranirovat(z.zagolovok)[:260], ekranirovat(z.cena)[:340], ekranirovat(adr),
            gr[0], ekranirovat(gr[2])[:110], z.ballov))
    A("")

    A("## Раздел 3 · СПОРНЫЕ — %d (решение владельца, не скрипта)" % ch["spornyh"])
    A("")
    A("> Балл сходства попал между порогами %.2f и %.2f: на дубль не тянет, на «новое» —")
    A("> тоже. §2.3 захода прямо запрещает решать такое молча.")
    A("")
    if d["spornye"]:
        A("| id | что произошло | ЦЕНА | откуда | ближайшая запись корпуса | балл |")
        A("|---|---|---|---|---|---|")
        for i, z in enumerate(d["spornye"], 1):
            blizh = z.dubli_s[0] if z.dubli_s else ("—", "—", "—")
            A("| СПОР-%03d | %s | ЦЕНА: %s | `%s` | %s · %s | %.2f |" % (
                i, ekranirovat(z.zagolovok)[:220], ekranirovat(z.cena)[:260], z.adres,
                blizh[0], ekranirovat(blizh[2])[:140], z.ballov))
    else:
        A("*Пусто.*")
    A("")

    A("## Раздел 4 · БЕЗ ЦЕНЫ, требует глаза — %d" % ch["bez-ceny-novyh"])
    A("")
    A("> Описание проблемы есть, процитировать цену нечем. **Не отброшено и не досочинено** —")
    A("> ровно этого требует §2.1 захода. Список уже за вычетом того, что корпус знает.")
    A(">")
    A("> Отсортировано по **числу разных сигналов поломки** в блоке — это ранг, а не вердикт.")
    A("> Срез «сигналов ≥3» — **%d записей**, с него разумно начинать глазами; остальные" % ch["bez-ceny-signalov-3"])
    A("> держат один-два маркера и чаще оказываются обычной прозой отчёта.")
    A("")
    ranzhir = sorted(d["bez_ceny"], key=lambda z: -sila_signala(z.polnyj))
    A("| id | сигналов | что произошло | откуда |")
    A("|---|---|---|---|")
    for i, z in enumerate(ranzhir[: ch["bez-ceny-signalov-3"]], 1):
        A("| БЦ-%03d | %d | %s | `%s` |" % (i, sila_signala(z.polnyj), ekranirovat(z.zagolovok)[:260], z.adres))
    A("")
    A("<details><summary>Остальные %d — сигналов 1–2</summary>" % (len(ranzhir) - ch["bez-ceny-signalov-3"]))
    A("")
    A("| id | сигналов | что произошло | откуда |")
    A("|---|---|---|---|")
    for i, z in enumerate(ranzhir[ch["bez-ceny-signalov-3"]:], ch["bez-ceny-signalov-3"] + 1):
        A("| БЦ-%03d | %d | %s | `%s` |" % (i, sila_signala(z.polnyj), ekranirovat(z.zagolovok)[:220], z.adres))
    A("")
    A("</details>")
    A("")

    A("## Раздел 5 · ВНЕ ОТСЕЧКИ — %d записей с ценой, которых корпус не знает" % ch["do-otsechki-ne-v-korpuse"])
    A("")
    A("> Это **не улов** — материал старше 30.07, задача его не заказывала. Но число значимо")
    A("> само по себе: оно измеряет, сколько ручной сбор корпуса пропустил в том, что уже читал.")
    A("> Из %d записей с ценой до отсечки корпус не опознаёт **%d**." % (
        ch["do-otsechki-vsego"], ch["do-otsechki-ne-v-korpuse"]))
    A("")
    po_arke = Counter()
    for z in d["do_otsechki"]:
        mm = DATA_ARKI.search(z.fajl)
        po_arke[mm.group(1) if mm else "без даты в имени"] += 1
    A("| арка | записей |")
    A("|---|---|")
    for k, v in sorted(po_arke.items()):
        A("| `%s` | %d |" % (k, v))
    A("")

    A("## Три примера дедупликации (условие 4 критерия) — выбраны скриптом, не рукой")
    A("")
    kA = next((z for z in d["dubli"] if z.pochemu.startswith("канал А")), None)
    kB = next((z for z in sorted(d["dubli"], key=lambda x: -x.ballov)
               if not z.pochemu.startswith("канал А")), None)
    kV = max(d["povtory"], key=lambda z: z.ballov) if d["povtory"] else None
    A("**Пример 1 — склеено как дубль, канал А (адрес).** Точный канал, ошибиться не может:")
    if kA:
        A("")
        A("- запись: %s" % ekranirovat(kA.zagolovok)[:200])
        A("- адрес живой: `%s`" % kA.adres)
        A("- вердикт: %s" % kA.pochemu)
    A("")
    A("**Пример 2 — склеено как дубль, канал Б (текст).** Формулировки разные, инцидент один:")
    if kB:
        gr = kB.dubli_s[0] if kB.dubli_s else ("—", "—", "—")
        A("")
        A("- запись журнала: %s" % ekranirovat(kB.zagolovok)[:200])
        A("- запись корпуса `%s`: %s" % (gr[0], ekranirovat(gr[2])[:200]))
        A("- балл %.2f при пороге %.2f; файл в индексе корпуса ⇒ это ОДНА и та же запись."
          % (kB.ballov, PORO_DUBL))
    A("")
    A("**Пример 3 — ВЫГЛЯДЕЛО дублем и дублем НЕ ОКАЗАЛОСЬ.** Балл выше порога, а запись —")
    A("новая: корпус этого файла не открывал, значит совпал МЕХАНИЗМ, а не запись.")
    if kV:
        gr = kV.dubli_s[0] if kV.dubli_s else ("—", "—", "—")
        A("")
        A("- запись журнала: %s" % ekranirovat(kV.zagolovok)[:200])
        A("- похожая группа корпуса `%s`: %s" % (gr[0], ekranirovat(gr[2])[:200]))
        A("- балл **%.2f** — выше порога %.2f, и наивная дедупликация выбросила бы эту запись."
          % (kV.ballov, PORO_DUBL))
        A("- спасло различение: `%s` в индексе корпуса нет ⇒ **кратность +1, а не дубль**."
          % os.path.basename(kV.fajl))
    A("")

    A("## Метод — чем именно отсекал")
    A("")
    A("**Отсечка не по дате, а по покрытию корпусом.** Корпус несёт собственную дату данных")
    A("2026-08-05 (шапки `KARTOTEKA-problem.md` и `POKRYTIE.md`), а не 30.07: 05.08 он был")
    A("пересчитан заново по живым файлам. Резать по 30.07 значило бы объявить «уловом» уроки")
    A("арок `sayt-drakon`, `teorver-plan` и части `puti-i-volny`, лежащие в корпусе неделю.")
    A("")
    A("**Три канала дедупликации:**")
    A("")
    A("- **А, адресный (точный)** — только для `UROKI-FABRIKE.md`. Корпус адресует уроки")
    A("  как `<арка>/UROKI-FABRIKE.md:<строка>`; в эти файлы только дописывают, поэтому дрейфа")
    A("  нет. Замер: адресов %d, мимо живой секции — **%d**. Покрыто секций: **%d**." % (
        itog["diagnostika"]["korpus"]["adresa-razdel5"] + itog["diagnostika"]["korpus"]["adresa-pokrytie"],
        itog["diagnostika"]["adresov-mimo-zhivoj-sekcii"],
        itog["diagnostika"]["sekcij-pokryto-adresom"]))
    A("- **Б, текстовый (по существу)** — для прозы. Адресный канал для `kod_*.md` НЕПРИГОДЕН,")
    A("  и это замерено: из 460 адресов `skelet-ispolnitelej.tsv` в свою названную секцию сегодня")
    A("  попадают 270, мимо — 190 (файлы выросли отчётом и приёмкой после снимка). Мера —")
    A("  контейнмент отпечатка корпуса в записи (%d отпечатков) плюс Жаккар по заголовкам и" % itog["diagnostika"]["otpechatkov"])
    A("  биграммам; пол абсолютного пересечения — %d основ." % MIN_PERESECHENIE)
    A("- **В, внутри улова** — один инцидент, записанный уроком и пересказанный отчётом,")
    A("  схлопывается в одну запись с несколькими адресами (склеек: %d)." % ch["sklejek-vnutri-ulova"])
    A("- **Г, «читал ли корпус этот файл»** — твёрдый факт, разводящий дубль и новое")
    A("  вхождение: %d прямых путей + %d хвостов пути из адресов корпуса." % (
        itog["diagnostika"]["korpus"]["fajlov-v-indekse-korpusa"],
        itog["diagnostika"]["korpus"].get("suffiksov-chitannyh", 0)))
    A("")
    A("**Пороги выбраны замером, а не на глаз.** `--kontrol` прогоняет через ту же")
    A("дедупликацию ВСЕ записи корпуса, лежащие в области инструмента, и считает, какую долю")
    A("она опознаёт. Текущая настройка: **250 из 267 (93,6 %)**; ещё 63 адреса корпуса живого")
    A("блока не имеют вовсе — это вопрос охвата, не дедупликации. Кривая по порогу:")
    A("0.40 → 96.6 % · 0.45 → 94.8 % · 0.50 → 93.6 % · 0.55 → 87.3 % · 0.60 → 82.8 %.")
    A("Ширина окна контекста подобрана так же: ±1 → 92.1 %, ±2 → 94.4 %, ±3 → 96.3 %; взято ±2,")
    A("потому что окно на семь абзацев начнёт совпадать со всем подряд, а ЭТУ ошибку замер не видит.")
    A("")
    A("**Цена ошибки в обе стороны.** Пропустил дубль → ложный рост корпуса; склеил разное →")
    A("потерянный инцидент. Разведено тремя порогами, а не одним: ≥%.2f — дубль, %.2f–%.2f —" % (PORO_DUBL, PORO_SPOR, PORO_DUBL))
    A("спорное (Раздел 3, владельцу), <%.2f — новое." % PORO_SPOR)
    A("")
    A("🔴 **Слабое место, названное вслух: дневники.** `SESSIYA.md` сравнивается с корпусом")
    A("реплик владельца, а тот собран с репетиций и говорит про содержание лекций, не про")
    A("работу исполнителей. Сравнение там ведётся симметричным Жаккаром по заголовкам (не")
    A("контейнментом — он на коротких репликах даёт 1.00 у записей без ничего общего), и всё")
    A("равно это самый слабый канал. Вердикты по дневникам требуют глаза больше остальных.")
    A("")
    A("## Снимок источников — к чему привязаны все числа выше")
    A("")
    A("> Дерево движется под замером: рядом идут другие заходы и пишут в те же файлы.")
    A("> Без снимка числа невоспроизводимы. Ниже — sha1 (12 знаков) каждого прочитанного файла.")
    A("")
    A("<details><summary>%d файлов</summary>" % len(itog["snimok"]))
    A("")
    A("| файл | sha1 | байт |")
    A("|---|---|---|")
    for f in sorted(itog["snimok"]):
        s = itog["snimok"][f]
        A("| `%s` | `%s` | %d |" % (f, s["sha1"], s["bytes"]))
    A("")
    A("</details>")
    A("")
    A("---")
    A("*Собран `dobor_incidentov.py`. Правится пересборкой, не руками:")
    A("правка руками разойдётся с числами шапки при первом же прогоне.*")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pechat_ohvata(itog):
    ch, o = itog["chisla"], itog["ohvat"]
    print("═══ ОХВАТ ИСТОЧНИКОВ (числа сняты этим прогоном) ═══")
    print("%-24s %10s %10s %10s" % ("источник", "существует", "прочитано", "блоков"))
    for k, v in o.items():
        print("%-24s %10d %10d %10d" % (k, v["fajlov"], v["prochitano"], v.get("blokov", v.get("zapisej", 0))))
    print()
    print("═══ ВОРОНКА ═══")
    for k in ("blokov-vsego", "kandidatov", "s-cenoj", "dublej", "povtorov", "spornyh",
              "novyh-do-skleiki", "sklejek-vnutri-ulova", "novyh", "bez-ceny", "bez-ceny-novyh"):
        print("  %-24s %6d" % (k, ch[k]))
    print()
    print("═══ ДИАГНОСТИКА КОРПУСА ═══")
    for k, v in itog["diagnostika"].items():
        print("  %-32s %s" % (k, v))


def main():
    ap = argparse.ArgumentParser(description="Добор инцидентов фабрики из живого журнала")
    ap.add_argument("--repo", default=None, help="корень репозитория materials (по умолчанию — от места скрипта)")
    ap.add_argument("--out", default=None, help="куда писать NOVYE-INCIDENTY.md")
    ap.add_argument("--ohvat", action="store_true", help="только числа охвата, без записи файла")
    ap.add_argument("--kontrol", action="store_true", help="положительный контроль (условие 5)")
    ap.add_argument("--vygruzki", action="store_true", help="включить транскрипты")
    ap.add_argument("--json", default=None, help="дамп чисел в json")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(a.repo) if a.repo else os.path.abspath(os.path.join(here, "..", "..", ".."))
    if not os.path.isdir(os.path.join(repo, KORPUS_ARKA)):
        print("🔴 не вижу корпус в %s — назови корень репозитория флагом --repo" % repo, file=sys.stderr)
        return 1

    if a.kontrol:
        return kontrol(repo)

    itog, d = sobrat(repo, s_vygruzkami=a.vygruzki)
    pechat_ohvata(itog)

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(itog, f, ensure_ascii=False, indent=1)

    if not a.ohvat:
        out = a.out or os.path.join(here, "NOVYE-INCIDENTY.md")
        pisat_vyhod(out, itog, d, repo, a.vygruzki)
        print()
        print("✅ записано: %s" % out)
        print("   новых записей: %d · спорных: %d · без цены: %d" % (
            itog["chisla"]["novyh"], itog["chisla"]["spornyh"], itog["chisla"]["bez-ceny-novyh"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
