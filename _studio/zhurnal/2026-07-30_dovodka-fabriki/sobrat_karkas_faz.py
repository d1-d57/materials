#!/usr/bin/env python3
"""Join групп KRATNOST.md/KRATNOST-vladelca.md с id из skelet-*.tsv;
извлечение 316 уроков арок и вычитание 74, покрытых классом И (POKRYTIE.md).
Запуск: python3 sobrat_karkas_faz.py [ispolnitelej|vladelca|urokov|git|all]
Только чтение; ничего не пишет на диск (кроме stdout/json при --json).
"""
import re, sys, json, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))  # .../materials-wt/razbros-po-fazam

def load_skelet(path, addr_col):
    """АДРЕС -> id, из tsv с шапкой '# id\tфайл\t...' или '# id\tисточник\t...'."""
    addr2id = {}
    dupes = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        idx = header.index(addr_col)
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            cols = line.split("\t")
            if len(cols) <= idx:
                continue
            rid = cols[0]
            addr = cols[idx].strip()
            if addr in addr2id and addr2id[addr] != rid:
                dupes.append((addr, addr2id[addr], rid))
            addr2id[addr] = rid
    return addr2id, dupes

def parse_kratnost_ispolnitelej(path):
    """KRATNOST.md: '## N. <title> — K вхожд.' + буллеты-адреса (весь текст строки-адрес),
    плюс финальный '## Разное' с буллетами '**...** — <адрес>'."""
    groups = []  # (num, title, count, [addr,...])
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # обычные группы
    for m in re.finditer(r'^## (\d+)\. (.+?) — (\d+) вхожд\.\n((?:^-.*\n?)*)', text, re.M):
        num, title, count, body = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        addrs = [ln[2:].strip() for ln in body.strip().split("\n") if ln.startswith("- ")]
        groups.append((int(num), title, count, addrs))
    # Разное
    mm = re.search(r'^## Разное.*?\n(.*?)\n---\n', text, re.S | re.M)
    razn_addrs = []
    if mm:
        for ln in mm.group(1).split("\n"):
            ln = ln.strip()
            if ln.startswith("- **"):
                am = re.search(r'—\s*([^—]+?/[^—]+?\.md#[^*]+?)\s*$', ln)
                if am:
                    razn_addrs.append(am.group(1).strip())
    return groups, razn_addrs

def parse_kratnost_vladelca(path):
    """KRATNOST-vladelca.md: '### N. <title> — K вхождений' + буллеты '- **quote** — `addr`[ · **ЧИСЛО:** ...]'."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    section = text.split("## 1. Группы с полными списками адресов", 1)[1]
    section = section.split("## 2. ВСЕ найденные", 1)[0]
    groups = []
    for m in re.finditer(r'^### (\d+)\. (.+?) — (\d+) вхождений\n(.*?)(?=^### |\Z)', section, re.M | re.S):
        num, title, count, body = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        addrs = []
        for ln in body.split("\n"):
            ln = ln.strip()
            if not ln.startswith("- "):
                continue
            am = re.search(r'`([^`]+)`', ln)
            if am:
                addrs.append(am.group(1).strip())
        groups.append((int(num), title, count, addrs))
    return groups

def join_report(groups, addr2id, label):
    out = []
    total_addr = 0
    total_matched = 0
    unmatched_all = []
    for num, title, count, addrs in groups:
        ids = []
        unmatched = []
        for a in addrs:
            rid = addr2id.get(a)
            if rid:
                ids.append(rid)
            else:
                unmatched.append(a)
        total_addr += len(addrs)
        total_matched += len(ids)
        unmatched_all.extend(unmatched)
        out.append({"num": num, "title": title, "count": count, "n_addrs": len(addrs),
                     "n_ids": len(ids), "ids": ids, "unmatched": unmatched})
    return {"label": label, "groups": out, "total_addr": total_addr,
            "total_matched": total_matched, "unmatched_all": unmatched_all}

STUB_RE = re.compile(r'^### N\. <что произошло')

def extract_uroki(zhurnal_dir):
    """Все ### -секции всех */UROKI-FABRIKE.md (кроме заглушек шаблона)."""
    lessons = []
    files = sorted(glob.glob(os.path.join(zhurnal_dir, "*", "UROKI-FABRIKE.md")))
    for fp in files:
        rel = os.path.relpath(fp, os.path.dirname(zhurnal_dir))  # zhurnal/<arka>/UROKI-FABRIKE.md
        with open(fp, encoding="utf-8") as f:
            lines = f.readlines()
        cur = None
        cur_start = None
        for i, ln in enumerate(lines, 1):
            if ln.startswith("### "):
                if cur is not None:
                    lessons.append({"file": rel, "line": cur_start, "end": i - 1, "title": cur,
                                     "body": "".join(lines[cur_start:i-1])})
                if STUB_RE.match(ln.strip()):
                    cur = None
                    continue
                cur = ln[4:].strip()
                cur_start = i
        if cur is not None:
            lessons.append({"file": rel, "line": cur_start, "end": len(lines), "title": cur,
                             "body": "".join(lines[cur_start:])})
    return lessons

def parse_pokrytie_addrs(path):
    """POKRYTIE.md таблицы: `zhurnal/<arka>/UROKI-FABRIKE.md:LINE` (первое упоминание файла)
    или сокращённое `…<хвост-имени-арки>:LINE` (повтор того же/похожего файла).
    Возвращает список (raw_ref, line), raw_ref — полный путь либо хвост после '…'."""
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            for m in re.finditer(r'`([^`]+?):(\d+)`', ln):
                ref, line = m.group(1), int(m.group(2))
                if "UROKI-FABRIKE" in ref or ref.startswith("…"):
                    out.append((ref.lstrip("…"), line))
    return out

def resolve_pokrytie_refs(pokr_raw, lesson_files):
    """Сопоставить сокращённые ссылки POKRYTIE.md с реальными путями UROKI-FABRIKE.md по хвосту имени папки арки."""
    resolved = []
    unresolved = []
    for ref, line in pokr_raw:
        if "UROKI-FABRIKE" in ref:
            resolved.append((ref, line))
            continue
        # ref — хвост имени папки арки (с датой или без), ищем файл, чья папка на него оканчивается
        cands = [f for f in lesson_files if os.path.dirname(f).endswith(ref) or ref in os.path.dirname(f)]
        if len(cands) == 1:
            resolved.append((cands[0], line))
        elif len(cands) > 1:
            resolved.append((cands[0], line))  # неоднозначно — берём первый, честно логируем
            unresolved.append((ref, line, "неоднозначно: " + ",".join(cands)))
        else:
            unresolved.append((ref, line, "не найдено"))
    return resolved, unresolved

def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    D = ROOT

    if what in ("ispolnitelej", "all"):
        addr2id, dupes = load_skelet(os.path.join(D, "skelet-ispolnitelej.tsv"), "АДРЕС")
        groups, razn = parse_kratnost_ispolnitelej(os.path.join(D, "KRATNOST.md"))
        rep = join_report(groups, addr2id, "ispolnitelej(КРТ)")
        razn_ids = [addr2id[a] for a in razn if a in addr2id]
        razn_unmatched = [a for a in razn if a not in addr2id]
        print(f"=== KRATNOST.md (КРТ) === всего id в skelet: {len(addr2id)} дублей-адресов: {len(dupes)}")
        print(f"групп: {len(rep['groups'])}, адресов всего {rep['total_addr']}, сматчено {rep['total_matched']}, не сматчено {len(rep['unmatched_all'])}")
        print(f"Разное: {len(razn)} адресов, сматчено {len(razn_ids)}, не сматчено {len(razn_unmatched)}")
        if rep["unmatched_all"]:
            print("НЕ СМАТЧЕНО (ispolnitelej):")
            for a in rep["unmatched_all"][:30]:
                print("  ", a)
        if razn_unmatched:
            print("НЕ СМАТЧЕНО (Разное):")
            for a in razn_unmatched[:30]:
                print("  ", a)
        with open(os.path.join(D, "_join_ispolnitelej.json"), "w", encoding="utf-8") as f:
            json.dump({"groups": rep["groups"], "razn_ids": razn_ids, "razn_unmatched": razn_unmatched,
                       "total_corpus": len(addr2id)}, f, ensure_ascii=False, indent=1)

    if what in ("vladelca", "all"):
        addr2id, dupes = load_skelet(os.path.join(D, "skelet-vladelca.tsv"), "АДРЕС")
        groups = parse_kratnost_vladelca(os.path.join(D, "KRATNOST-vladelca.md"))
        rep = join_report(groups, addr2id, "vladelca(КРВ)")
        print(f"\n=== KRATNOST-vladelca.md (КРВ) === всего id в skelet: {len(addr2id)} дублей-адресов: {len(dupes)}")
        print(f"групп: {len(rep['groups'])}, адресов всего {rep['total_addr']}, сматчено {rep['total_matched']}, не сматчено {len(rep['unmatched_all'])}")
        if rep["unmatched_all"]:
            print("НЕ СМАТЧЕНО (vladelca), первые 40:")
            for a in rep["unmatched_all"][:40]:
                print("  ", a)
        with open(os.path.join(D, "_join_vladelca.json"), "w", encoding="utf-8") as f:
            json.dump({"groups": rep["groups"], "total_corpus": len(addr2id)}, f, ensure_ascii=False, indent=1)

    if what in ("urokov", "all"):
        zhurnal_dir = os.path.join(REPO, "_studio", "zhurnal")
        lessons = extract_uroki(zhurnal_dir)
        lesson_files = sorted(set(l["file"] for l in lessons))
        pokr_raw = parse_pokrytie_addrs(os.path.join(REPO, "_studio", "konvejer", "04.5-intervyu", "POKRYTIE.md"))
        pokr_resolved, pokr_unresolved = resolve_pokrytie_refs(pokr_raw, lesson_files)
        covered = []
        remaining = []
        covered_hits = {i: [] for i in range(len(lessons))}
        for idx, l in enumerate(lessons):
            hit_refs = [(pf, pl) for pf, pl in pokr_resolved
                        if pf == l["file"] and l["line"] <= pl <= l["end"]]
            if hit_refs:
                covered.append(l)
                covered_hits[idx] = hit_refs
            else:
                remaining.append(l)
        print(f"\n=== UROKI-FABRIKE.md === секций всего: {len(lessons)}, ссылок в POKRYTIE: {len(pokr_raw)} (не разрешено: {len(pokr_unresolved)})")
        print(f"покрыто (совпало с POKRYTIE, класс И): {len(covered)}, остаток: {len(remaining)}")
        if pokr_unresolved:
            print("НЕ РАЗРЕШЕНО (POKRYTIE ссылки):")
            for r in pokr_unresolved[:20]:
                print("  ", r)
        with open(os.path.join(D, "_uroki_ostatok.json"), "w", encoding="utf-8") as f:
            json.dump({"covered_n": len(covered), "covered": covered, "remaining": remaining,
                       "total": len(lessons), "pokr_refs": len(pokr_raw), "unresolved": pokr_unresolved},
                       f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
