#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГРАФ ЗАВИСИМОСТЕЙ ЛЕКЦИИ — карта связей, циклы, нарушения заявленного порядка.

    python3 _generator/tools/graf_zavisimostej.py <папка-лекции>

Код возврата: 0 — циклов и нарушений нет; 1 — есть хотя бы одно. Годится в ворота.

ЧТО ЭТО. Собирает граф зависимостей лекции ИЗ УЖЕ СУЩЕСТВУЮЩИХ ПОЛЕЙ карточек слайда
(`slaid.md`) и карточки лекции (`brief.md`) — без единого токена LLM. Формат связей — Я1
`../../disciplina/skills/slajdy/references/graf-zavisimostej.md` (второй репозиторий, вне зоны
этого файла — только читается человеком, не этим скриптом).

🔴 ЧЕГО ЭТОТ СКРИПТ НЕ ДЕЛАЕТ. Не переставляет слайды и не предлагает порядок — печатает три
вещи и ничего больше: резюме лекции, циклы, нарушения ЗАЯВЛЕННОГО (`slide_order` в `brief.md`)
порядка. Решение о порядке остаётся за человеком.

ОТКУДА БЕРЁТ ДАННЫЕ. Карточки слайда ищутся рекурсивно по канону Я1 `formaty.py`:
`<лекция>/**/slajdy/<imya>/slaid.md`. `brief.md` ищется тоже рекурсивно (лекция может держать
его не в корне, как `teorkat-vvedenie/src/brief.md`) — берётся первый по отсортированному пути.
Лекция без единой карточки нового формата (лекции до 2026-08-08, когда карточка была спроектирована)
— НЕ ошибка: скрипт печатает нулевое резюме, а не трейсбек.

ПОЧЕМУ SLIDE ID = `imya`. `vvedeno`/`formalno`/`dokazatelstvo_opiraetsya_na`/`primer_dlya.tsel`
и элементы `slide_order` — одна и та же система идентификаторов: `imya` карточки слайда (обычно
совпадает с именем папки `slajdy/<imya>/`, по докстроке `formaty.py`).

ГРАФ ОДИН, А НЕ ДВА (заход kod_rebra-blokov.md, Э1, решение владельца 2026-08-15,
дословно: «термин — это блок... можем просто вести стрелки к определениям — к местам, где
они определяются»). Прежняя редакция вела граф терминов и граф утверждений раздельно —
владелец разобрал это как дефект: связная компонента дробилась на кусок по терминам и кусок
по доказательствам, и «этот кусок замкнут сам на себя» не было видно целиком ни в одном из
них. Вершины единого графа (`build_graph`) — БЛОКИ, термин — метка на ребре, не вершина:

  · термин, введённый В ЭТОЙ лекции (встречается в чьём-то `vvodit`) — вершина `sid`
    карточки-хозяина;
  · термин БЕЗ хозяина в лекции (использован, но не введён здесь) — вершина-заглушка,
    сам термин своей текстовой формой (решение по «одной детали» Э1: это уже было
    фактическим поведением графа терминов, здесь только названо официально);
  · блок доказательства/примера — вершина `sid:tip` (`tip` ∈ `dokazatelstvo`, `primer`), а
    не голый `sid`: G-8 гарантирует не больше одного блока каждого типа на карточку, но
    карточка может нести до четырёх разных типов сразу, а `kategoriya-vect-iso` (мотивирующий
    пример захода) целит доказательство в блок ТОЙ ЖЕ карточки — голый `sid` дал бы
    самопетлю без содержания.

Ребро Y→X значит «X зависит от Y» — для терминов берётся из `opiraetsya_na` ХОЗЯИНА термина X
(слайда, где X встречается в `vvodit`), а не из любого использования X где угодно: только
определение термина зависит от другого термина в смысле этого графа, иначе цикл означал бы
«слайд использует термин» вместо «термин требует термин». Для доказательств/примеров — из
`dokazatelstvo_opiraetsya_na`/`primer_dlya.tsel` карточки. Нарушение порядка — отдельная
проверка для ТЕРМИНОВ, она НЕ ограничена хозяевами (см. ниже) и не относится к
доказательствам/примерам (порядок блоков на ленте у них не специфицирован).

НАРУШЕНИЕ ПОРЯДКА vs ЦИКЛ — разные проверки. Цикл — свойство графа терминов (граф ациклический
или нет, вне позиций на ленте). Нарушение порядка — сравнение позиции РАБОЧЕГО использования
термина (`opiraetsya_na` на любом слайде) с позицией хозяина в `slide_order`; легализуется
записью `bez_opredeleniya_namerenno` (см. спецификацию, вид 2) на позиции ≤ позиции использования
с верным `formalno`.

ДЕТЕРМИНИЗМ. Все обходы — по отсортированным ключам/спискам; никаких множеств без sorted() на
выходе, никаких временных меток. Два прогона на одном входе печатают побайтово одинаковый вывод.
"""
import sys
from pathlib import Path

_SBORKA = Path(__file__).resolve().parents[1] / "sborka"
sys.path.insert(0, str(_SBORKA))
import formaty  # noqa: E402  (read-only импорт, см. докстроку; путь — как у gejt_kartochki.py)
import bloki  # noqa: E402  (read-only импорт — та же карточка, что и gejt_kartochki.py читает
# для состава блоков; здесь нужен для охвата Э2 и вершин-блоков Э1 kod_rebra-blokov.md)


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def find_lecture_files(lecture_dir):
    """Лекция → (путь к brief.md|None, [пути к slaid.md], список ошибок чтения)."""
    briefs = sorted(lecture_dir.glob("**/brief.md"))
    cards = sorted(lecture_dir.glob("**/slajdy/*/slaid.md"))
    return (briefs[0] if briefs else None), cards


def load_slide_order(brief_path):
    """brief.md → [id, ...] заявленного порядка, или [] (нет файла/нет поля)."""
    if brief_path is None:
        return [], "brief.md не найден в дереве лекции"
    text = brief_path.read_text(encoding="utf-8")
    try:
        params, _ = formaty.parse_front_matter(text, sid=str(brief_path))
    except formaty.FormatSlaida as e:
        return [], "brief.md не разобран: %s" % e
    order = params.get("slide_order")
    if not order:
        return [], "поле slide_order пусто или отсутствует в brief.md"
    return _as_list(order), None


def load_cards(card_paths):
    """[путь] → ({id: params}, [строки-предупреждения о нечитаемых карточках])."""
    cards, warnings = {}, []
    for p in card_paths:
        text = p.read_text(encoding="utf-8")
        try:
            params, raw_body = formaty.parse_card(text, sid=str(p))
        except formaty.FormatSlaida as e:
            warnings.append("%s: не разобрана карточка — %s" % (p, e))
            continue
        sid = params.get("imya") or p.parent.name
        if sid in cards:
            warnings.append("%s: id '%s' уже занят карточкой %s — эта карточка пропущена"
                             % (p, sid, cards[sid].get("_path")))
            continue
        params["_path"] = str(p)
        params["_raw_body"] = raw_body  # Э2 kod_rebra-blokov.md: охват считается по блокам,
        # не только по полям — граф обязан знать состав раздела «Математика»
        # Виды 3–4 (новые поля) parse_card не нормализует — делаем это здесь,
        # тем же приёмом, что formaty.parse_card применяет к своим спискам.
        params.setdefault("dokazatelstvo_opiraetsya_na", [])
        if isinstance(params["dokazatelstvo_opiraetsya_na"], str):
            params["dokazatelstvo_opiraetsya_na"] = [params["dokazatelstvo_opiraetsya_na"]]
        params.setdefault("primer_dlya", [])
        if isinstance(params["primer_dlya"], dict):
            params["primer_dlya"] = [params["primer_dlya"]]
        cards[sid] = params
    return cards, warnings


def build_graph(cards):
    """{id: params} → (edges: {вершина: {вершина,...}}, host_of: {termin: [id,...]},
    labels: {(Y, X): метка}). ЕДИНЫЙ граф блоков — Э1 kod_rebra-blokov.md, см. докстроку
    модуля про три вида вершин. `labels` несёт термин/слово ребра — только для читаемого
    сообщения о цикле, на сам поиск цикла не влияет."""
    host_of = {}
    for sid, params in cards.items():
        for t in _as_list(params.get("vvodit")):
            host_of.setdefault(t, []).append(sid)

    edges, labels = {}, {}

    def add_edge(y, x, label):
        if y == x:
            return  # самопетля не несёт цикла и не несёт смысла — не заводим
        edges.setdefault(y, set()).add(x)
        labels[(y, x)] = label

    for sid, params in cards.items():
        defined_here = _as_list(params.get("vvodit"))
        if not defined_here:
            continue
        for e in _as_list(params.get("opiraetsya_na")):
            if not isinstance(e, dict) or not e.get("termin"):
                continue
            termin = e["termin"]
            hosts = host_of.get(termin)
            if hosts:
                for hy in hosts:
                    add_edge(hy, sid, termin)
            else:
                add_edge(termin, sid, termin)  # термин без хозяина в лекции — сам вершина-заглушка

    for sid, params in cards.items():
        target = "%s:dokazatelstvo" % sid
        for dep in _as_list(params.get("dokazatelstvo_opiraetsya_na")):
            if dep:
                add_edge(dep, target, "доказывает")
        p_target = "%s:primer" % sid
        for e in _as_list(params.get("primer_dlya")):
            if isinstance(e, dict) and e.get("tsel"):
                add_edge(e["tsel"], p_target, "пример для")

    return edges, host_of, labels


def _matematika_blocks(params, sid):
    """Карточка (params с `_raw_body`, положенным `load_cards`) → [bloki.Block,...] раздела
    «Математика — развёрнуто», или [] (тела нет — K3, либо блоки не разбираются). Нужно для
    охвата Э2: считать M (блоков dokazatelstvo/primer в лекции) можно только по составу
    блоков, поля шапки этого не говорят."""
    raw_body = params.get("_raw_body") or ""
    if not raw_body.strip():
        return []
    try:
        sections = bloki.parse_sections(raw_body, sid=sid)
    except bloki.FormatBlokov:
        return []
    return sections["matematika"]


def coverage(cards):
    """{id: params} → {'dokazatelstvo': (N, M, [sid без адреса,...]),
    'primer': (N, M, [...])}. M — блоков этого типа в лекции (верхняя граница возможных
    рёбер, Э0 kod_rebra-blokov.md), N — из них с непустым адресом в шапке."""
    out = {"dokazatelstvo": [0, 0, []], "primer": [0, 0, []]}
    for sid, params in sorted(cards.items()):
        tips = {b.tip for b in _matematika_blocks(params, sid)}
        if "dokazatelstvo" in tips:
            out["dokazatelstvo"][1] += 1
            if _as_list(params.get("dokazatelstvo_opiraetsya_na")):
                out["dokazatelstvo"][0] += 1
            else:
                out["dokazatelstvo"][2].append(sid)
        if "primer" in tips:
            out["primer"][1] += 1
            if _as_list(params.get("primer_dlya")):
                out["primer"][0] += 1
            else:
                out["primer"][2].append(sid)
    return {k: tuple(v) for k, v in out.items()}


def find_cycle(edges, nodes):
    """Первый найденный цикл (список узлов, начало=конец) детерминированным DFS, иначе None."""
    color = {}
    result = [None]

    def dfs(u, path):
        color[u] = 1
        path.append(u)
        for v in sorted(edges.get(u, ())):
            if result[0] is not None:
                return
            if color.get(v, 0) == 0:
                dfs(v, path)
            elif color.get(v) == 1:
                idx = path.index(v)
                result[0] = path[idx:] + [v]
                return
        if result[0] is None:
            path.pop()
            color[u] = 2

    for n in sorted(nodes):
        if result[0] is not None:
            break
        if color.get(n, 0) == 0:
            dfs(n, [])
    return result[0]


def find_order_violations(cards, position, host_of):
    """→ ([строки-нарушения], N связей «опирается на», проверенных)."""
    violations = []
    checked = 0
    # Легализации (вид 2): termin -> [(позиция записи, formalno), ...]
    legal = {}
    for sid, params in cards.items():
        pos = position.get(sid)
        for e in _as_list(params.get("bez_opredeleniya_namerenno")):
            if not isinstance(e, dict) or not e.get("termin"):
                continue
            legal.setdefault(e["termin"], []).append((pos, e.get("formalno")))

    for sid in sorted(cards):
        params = cards[sid]
        p_use = position.get(sid)
        for e in sorted(_as_list(params.get("opiraetsya_na")),
                         key=lambda e: e.get("termin", "") if isinstance(e, dict) else ""):
            if not isinstance(e, dict) or not e.get("termin"):
                continue
            checked += 1
            termin = e["termin"]
            hosts = host_of.get(termin, [])
            if not hosts:
                violations.append(
                    "на слайде %s рабочим образом использован «%s», но ни один слайд "
                    "не вводит его (нет vvodit)" % (sid, termin))
                continue
            if len(hosts) > 1:
                violations.append(
                    "термин «%s» введён на нескольких слайдах сразу: %s"
                    % (termin, ", ".join(sorted(hosts))))
                continue
            host = hosts[0]
            p_host = position.get(host)
            if p_use is None or p_host is None:
                continue  # вне заявленного slide_order — порядок сравнивать не с чем
            if p_use < p_host:
                ok = any(pos is not None and pos <= p_use and formalno == host
                         for pos, formalno in legal.get(termin, []))
                if not ok:
                    violations.append(
                        "на слайде %s рабочим образом использован «%s», а его дом — слайд %s, "
                        "который ниже" % (sid, termin, host))
    return violations, checked


def render(lecture_dir, cards, position, slide_order, brief_note, warnings):
    out = []
    edges, host_of, labels = build_graph(cards)
    cov = coverage(cards)

    depends_on = {t: {e["termin"] for e in _as_list(cards[hosts[0]].get("opiraetsya_na"))
                       if isinstance(e, dict) and e.get("termin")}
                  for t, hosts in host_of.items() if len(hosts) == 1}
    used_anywhere = set()
    for params in cards.values():
        for e in _as_list(params.get("opiraetsya_na")):
            if isinstance(e, dict) and e.get("termin"):
                used_anywhere.add(e["termin"])
    inputs = sorted(t for t in depends_on if not depends_on[t])
    deadends = sorted(t for t in depends_on if t not in used_anywhere)

    n_utverzhdenie_links = sum(len(_as_list(p.get("dokazatelstvo_opiraetsya_na")))
                               for p in cards.values())
    primer_before = sum(1 for p in cards.values() for e in _as_list(p.get("primer_dlya"))
                        if isinstance(e, dict) and e.get("napravlenie") == "do")
    primer_after = sum(1 for p in cards.values() for e in _as_list(p.get("primer_dlya"))
                       if isinstance(e, dict) and e.get("napravlenie") == "posle")

    out.append("── РЕЗЮМЕ ЛЕКЦИИ (%s) ──" % lecture_dir)
    out.append("слайдов с карточкой нового формата: %d" % len(cards))
    if not slide_order:
        out.append("slide_order: %s" % brief_note)
    elif not position:
        out.append("slide_order: %d слайдов заявлено, но ни один id не совпал с найденными "
                    "карточками (%d)" % (len(slide_order), len(cards)))
    else:
        out.append("slide_order: %d слайдов заявлено, из них с карточкой — %d"
                    % (len(slide_order), len(position)))
    out.append("терминов (введено через vvodit): %d" % len(host_of))
    out.append("  входы (ни на что не опираются): %s" % (", ".join(inputs) if inputs else "—"))
    out.append("  тупики (ничего не опирается на них — кандидаты на вырезание): %s"
                % (", ".join(deadends) if deadends else "—"))
    out.append("связей «доказательство опирается на утверждение»: %d" % n_utverzhdenie_links)
    out.append("примеров с направлением мотивации: %d (до цели: %d, после цели: %d)"
                % (primer_before + primer_after, primer_before, primer_after))
    if warnings:
        out.append("⚠ карточки, которые не удалось разобрать: %d" % len(warnings))
        for w in warnings:
            out.append("   %s" % w)
    if not cards:
        out.append("⚠ карточек формата slaid.md не найдено — граф пуст не потому, что лекция "
                    "чиста, а потому что нечего читать (лекция ещё не на новом формате карточки).")

    out.append("")
    out.append("── ГРАФ БЛОКОВ (термины + доказательства + примеры одним проходом, Э1) ──")
    nodes = set(edges) | {x for xs in edges.values() for x in xs}
    cycle = find_cycle(edges, nodes)
    nd, md, missing_d = cov["dokazatelstvo"]
    np_, mp, missing_p = cov["primer"]
    if cycle:
        metka = labels.get((cycle[0], cycle[1]), "")
        out.append("✗ ЦИКЛ: " + " → ".join(cycle) + (" (%s)" % metka if metka else ""))
    elif md and nd < md:
        # Э2: пустота/неполнота охвата не печатается зелёным — даже когда циклов и так нет
        out.append("⚠ циклов не найдено, но доказательств адресовано %d из %d, не все — "
                    "без адреса: %s" % (nd, md, ", ".join(missing_d)))
    else:
        out.append("✓ циклов нет (вершин %d, рёбер %d; доказательств адресовано %d из %d)"
                    % (len(nodes), sum(len(v) for v in edges.values()), nd, md))
    if mp and np_ < mp:
        out.append("⚠ примеров адресовано %d из %d, не все — без адреса: %s"
                    % (np_, mp, ", ".join(missing_p)))
    else:
        out.append("· примеров адресовано %d из %d" % (np_, mp))

    out.append("")
    out.append("── НАРУШЕНИЯ ЗАЯВЛЕННОГО ПОРЯДКА ──")
    if not slide_order:
        out.append("⚠ slide_order не задан (%s) — сравнивать использование термина с заявленным "
                    "порядком не с чем, раздел пропущен по данным, не по коду" % brief_note)
        violations, checked = [], 0
    elif not position:
        out.append("⚠ slide_order задан (%d), но ни один id не совпал с найденными карточками "
                    "(%d) — сравнивать не с чем" % (len(slide_order), len(cards)))
        violations, checked = [], 0
    else:
        violations, checked = find_order_violations(cards, position, host_of)
        if violations:
            for v in violations:
                out.append("✗ " + v)
        else:
            out.append("✓ нарушений нет, проверено %d слайдов и %d связей «опирается на»"
                        % (len(cards), checked))

    has_red = bool(cycle) or bool(violations)
    return "\n".join(out) + "\n", (1 if has_red else 0)


def main():
    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        print(__doc__.strip())
        sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.strip().splitlines()[0])
        sys.exit(2)
    lecture_dir = Path(args[0])
    if not lecture_dir.is_dir():
        print("❌ не папка: %s" % lecture_dir)
        sys.exit(2)

    brief_path, card_paths = find_lecture_files(lecture_dir)
    slide_order, brief_note = load_slide_order(brief_path)
    cards, warnings = load_cards(card_paths)
    position = {sid: i for i, sid in enumerate(slide_order) if sid in cards}
    unordered = sorted(set(cards) - set(slide_order))
    if unordered:
        warnings.append("вне slide_order (позиция неизвестна, порядок для них не проверяется): %s"
                         % ", ".join(unordered))

    text, rc = render(lecture_dir, cards, position, slide_order, brief_note, warnings)
    print(text, end="")
    sys.exit(rc)


if __name__ == "__main__":
    main()
