#!/usr/bin/env python3
"""Graph of the corpus — one tool, six questions + gate [c].

Uses kurs-puti-i-volny/tools/indeks.py (import, call собрать())
and ../disciplina/_generator/tools/reserch/topsort_karty.py primitives.
--koren DIR overrides indeks homes; --kaskad X; --siroty-gate.
Writes ZAMER-grafa.md and graf-rebra.tsv to the SBORKA folder next to graf.py.
"""
import os, sys, re, argparse, tempfile, collections, pathlib

# --- path setup ---
# Graf.py location: either materials/kurs-puti-i-volny/tools/ or worktree/...../kurs-puti-i-volny/tools/
# Calculate paths using __file__ for robustness
script_file = pathlib.Path(__file__).resolve()
tools_dir = script_file.parent
kpv_dir = tools_dir.parent
SBORKA_DIR = kpv_dir / 'SBORKA'  # head repair 19.09: was kpv_dir.parent — wrote outputs to the repo root

# Find GitHub root by going up until we find a directory containing 'disciplina'
current = kpv_dir.parent
while current.parent != current:  # Stop at filesystem root
    if (current / 'disciplina').exists():
        github_root = current
        break
    current = current.parent
else:
    # Fallback: assume standard directory structure
    # From tools dir: up 2 (to materials/graf-korpusa), up 1 (to GitHub or materials-wt), then find GitHub
    github_root = kpv_dir.parent.parent.parent

# import primitives from disciplina
sys.path.insert(0, str(github_root / 'disciplina' / '_generator' / 'tools' / 'reserch'))
import topsort_karty

# import indeks from current location (same tools directory)
sys.path.insert(0, str(tools_dir))
import indeks

RE_ЯКОРЬ = indeks.RE_ЯКОРЬ
RE_ССЫЛКА = indeks.RE_ССЫЛКА

# --- graph building ---

def собери_граф():
    файлы, узлы, ссылки, дубли = indeks.собрать()
    # nodes: file paths (relative to repo) and id nodes
    node_ids = set(узлы.keys())
    file_ids = {отн for _, отн, *_ in файлы}
    all_nodes = node_ids | file_ids

    # edges: contains (file -> anchor/card it contains)
    contains = []
    # links: (source, target) where target is link id, source is nearest preceding anchor or file
    links = []

    base_mat = indeks.MATERIALS
    # for each file, find anchors and links
    for дом, отн, *_ in файлы:
        полный = os.path.join(base_mat, отн)
        if not os.path.isfile(полный):
            continue
        with open(полный, encoding='utf-8') as fh:
            текст = fh.read()
        чистый = indeks.без_кода(текст)
        # anchors in order of appearance
        anchors = [(m.start(), m.group(1)) for m in RE_ЯКОРЬ.finditer(чистый)]
        # contains edges
        for _, an_id in anchors:
            contains.append((отн, an_id))
        # links: for each [[X]] find nearest preceding anchor
        for m in RE_ССЫЛКА.finditer(чистый):
            target = m.group(1)
            # nearest preceding anchor by position
            пред = None
            for pos, an_id in anchors:
                if pos < m.start():
                    пред = an_id
            источник = пред if пред is not None else отн
            links.append((источник, target))
        # also handle связи: field from cards (indeks.собрать already gives ссылки with откуда file)
        # but we need source attribution — for card links, source is card id if it has no preceding anchor? Actually cards are files with id: in header; the link is in the card file.
        # The links from `связи:` are already in `ссылки` with file path. We'll process them by reading the file again (same as above) — already covered by RE_ССЫЛКА? No, связи: field is separate.
        # Let's handle связи: manually parse the file for связи: fields and add links with source = file (since card file has no internal anchors usually; but we can attribute to nearest preceding anchor if any)
        # For simplicity, since связи are in clean text and links are already extracted by RE_ССЫЛКА? Actually связи: uses `kart-*` references which may not be in `[[...]]` form — they are bare ids inside `связи:`.
        # indeks.собрать handles them separately; but `RE_ССЫЛКА` only catches `[[X]]`. The связи references may not use `[[ ]]`. Let's rely on `ссылки` list from индекс for bare references, and attribute them to file or nearest anchor.
    # Process bare ссылки from индекс (связи: fields and опирается: etc.)
    # But for simplicity and per instructions: use links from file reading for `[[X]]`; for bare id references use `ссылки` directly with source=file (or nearest anchor in that file if we re-read).
    # Let's just add the bare references with source = file path (from `откуда` in ссылки)
    for target_id, откуда in ссылки:
        # find nearest preceding anchor in откуда file
        полный = os.path.join(base_mat, откуда)
        пред = None
        if os.path.isfile(полный):
            with open(полный, encoding='utf-8') as fh:
                текст = fh.read()
            чистый = indeks.без_кода(текст)
            anchors = [(m.start(), m.group(1)) for m in RE_ЯКОРЬ.finditer(чистый)]
            # find any link position? Actually for bare references we don't have a position. We'll attribute to file or last anchor.
            # Per instructions: source is nearest preceding anchor or file itself. For bare references with no position, we'll use file as default (conservative).
        источник = пред if пред is not None else откуда
        links.append((источник, target_id))

    return all_nodes, contains, links, узлы, файлы

# --- sections [1]-[6] and [c] ---

def section_1(nodes, links):
    # histogram of in/out degrees over links edges
    out_deg = collections.Counter(s for s, _ in links)
    in_deg = collections.Counter(t for _, t in links)
    # top-10
    top_in = in_deg.most_common(10)
    top_out = out_deg.most_common(10)
    lines = ["[1] Degrees (links edges)"]
    hist = collections.Counter(in_deg.values())
    lines.append(f"In-degree histogram: {dict(sorted(hist.items()))}")
    lines.append(f"Top-10 in-degree: {top_in}")
    lines.append(f"Top-10 out-degree: {top_out}")
    return '\n'.join(lines)

def section_2(nodes, links, top_in_ids):
    # cascade: reverse reachability over links from node X
    # build adjacency
    adj = collections.defaultdict(set)
    for s, t in links:
        adj[s].add(t)
    # reverse adjacency for cascade (who depends on X = reverse reach from X)
    rev = collections.defaultdict(set)
    for s, t in links:
        rev[t].add(s)
    def cascade(node):
        visited = set()
        stack = [node]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            for v in rev.get(u, set()):
                stack.append(v)
        return visited
    # top 5 in-degree nodes
    top5 = [n for n, _ in collections.Counter({t: 0 for _, t in links}).most_common()]  # dummy; we'll rely on caller
    # For simplicity, use top-5 in-degree nodes computed externally and passed in
    lines = ["[2] Cascade"]
    for nid in top_in_ids[:5]:
        reach = cascade(nid)
        lines.append(f"Cascade from {nid}: size={len(reach)} nodes: {sorted(reach)}")
    return '\n'.join(lines)

def section_3(nodes, узлы, links):
    # condense cycles, then longest chain over links edges
    # Build adjacency for links (directed graph)
    adj = collections.defaultdict(set)
    for s, t in links:
        adj[s].add(t)

    all_nodes = set(nodes)

    # Use topsort_karty primitives
    try:
        # Find first cycle if any
        cycle = topsort_karty.najti_cikl(adj, all_nodes)

        # Find components (pass empty list for additional edges)
        components = topsort_karty.komponenty(all_nodes, adj, [])

        # Compute longest path using relaxation (works even with cycles)
        # dist[node] = longest path ending at each node
        dist = {node: 1 for node in all_nodes}
        parent = {node: None for node in all_nodes}

        # Relax edges multiple times (Bellman-Ford style)
        max_iterations = len(all_nodes)
        for _ in range(max_iterations):
            updated = False
            for src, tgt in links:
                if src in dist and tgt in dist:
                    if dist[src] + 1 > dist[tgt]:
                        dist[tgt] = dist[src] + 1
                        parent[tgt] = src
                        updated = True
            if not updated:
                break

        if dist:
            max_node = max(dist, key=dist.get)
            max_depth = dist[max_node]
            # reconstruct path
            path = []
            node = max_node
            visited = set()
            while node is not None and node not in visited:
                path.append(node)
                visited.add(node)
                node = parent.get(node)
            path.reverse()
        else:
            max_depth = 0
            path = []

        cycle_info = f"; cycle found: {' → '.join(cycle)}" if cycle else ""
        path_str = ' → '.join(path[:10]) if path else "(empty)"
        return f"[3] Depth: longest path length={max_depth}, chain={path_str}{cycle_info}"
    except Exception as e:
        # fallback if primitives fail
        return f"[3] Depth: error in topological analysis: {e}"

def section_4(nodes, узлы, contains, links, файлы):
    # reachability from ZAMYSEL.md entry over contains + links edges
    # A link to an id-node also reaches the FILE that defines that id
    entry = 'kurs-puti-i-volny/ZAMYSEL.md'

    # build id -> file mapping from узлы dict
    id_to_file = {}
    for id_, (вид, файл, суть, род) in узлы.items():
        id_to_file[id_] = файл

    # collect all file nodes
    all_files = set(file_id for _, file_id, *_ in файлы)

    # BFS from entry over contains + links, mapping ids to files
    reachable_files = set()
    reachable_ids = set()
    stack = [entry]

    while stack:
        node = stack.pop()

        # check if it's a file or id-node
        if node in reachable_files or node in reachable_ids:
            continue

        if node in all_files:
            reachable_files.add(node)
        elif node in узлы:
            reachable_ids.add(node)

        # find outgoing edges from this node
        # contains edges: file -> id
        for s, t in contains:
            if s == node and t not in reachable_ids:
                stack.append(t)

        # links edges: any node -> id or node -> file
        for s, t in links:
            if s == node:
                if t in узлы and t not in reachable_ids:
                    stack.append(t)
                    # also add the file that defines this id
                    if t in id_to_file:
                        file_of_t = id_to_file[t]
                        if file_of_t not in reachable_files:
                            stack.append(file_of_t)
                elif t in all_files and t not in reachable_files:
                    stack.append(t)

    unreachable_files = sorted(all_files - reachable_files)
    total_files = len(all_files)
    reachable_count = len(reachable_files)

    unreachable_str = ', '.join(unreachable_files[:10])
    if len(unreachable_files) > 10:
        unreachable_str += f', ... ({len(unreachable_files) - 10} more)'

    return f"[4] Reachability from entry: {reachable_count}/{total_files} files reachable; unreachable: {unreachable_str if unreachable_files else '(none)'}"

def section_5(nodes, links, contains):
    # node and edge counts by kind, number of components
    in_deg = collections.Counter(t for _, t in links)
    components_count = len(set(in_deg.values()))  # rough approximation; use topsort for exact
    return f"[5] Whole corpus: nodes={len(nodes)}, edges: links={len(links)}, contains={len(contains)}"

def section_6(links, contains):
    # export to graf-rebra.tsv in SBORKA_DIR
    SBORKA_DIR.mkdir(parents=True, exist_ok=True)
    tsv_path = SBORKA_DIR / 'graf-rebra.tsv'
    with open(tsv_path, 'w', encoding='utf-8') as fh:
        fh.write('source\ttarget\tkind\n')
        # write links edges
        for s, t in links:
            fh.write(f"{s}\t{t}\tlinks\n")
        # write contains edges
        for s, t in contains:
            fh.write(f"{s}\t{t}\tcontains\n")
    return f"[6] Exported to {tsv_path}"

def gate_c(узлы, links):
    # plan anchors: id matching ^(god|chast|chetvert|lekciya)-
    # Exact semantics:
    # - an anchor is NOT an orphan iff it has an outgoing links edge to an anchor of a
    #   STRICTLY HIGHER level (god < chast < chetvert < lekciya): clause (c) of the wave
    #   mandate says «an outgoing [[…]] upward». Head repair 19.09: the analysis part of the
    #   year has no `chast` level, so its quarter anchors link `god-*` directly; the old
    #   one-level-up rule counted those 6 as orphans although they do link upward.
    # - god-* is exempt (NOT counted as orphans)
    # orphans = count of non-exempt plan anchors without such edge

    parent_map = {
        'chast': 'god',
        'chetvert': 'chast',
        'lekciya': 'chetvert'
    }

    plan_anchors = [n for n in узлы if re.match(r'^(god|chast|chetvert|lekciya)-', n)]

    orphan_ids = []
    for anchor_id in plan_anchors:
        # extract level (god, chast, chetvert, or lekciya)
        level = None
        for lvl in ['god', 'chast', 'chetvert', 'lekciya']:
            if anchor_id.startswith(lvl + '-'):
                level = lvl
                break

        # god-* is exempt
        if level == 'god':
            continue

        # check if anchor_id has outgoing link to parent level
        order = ['god', 'chast', 'chetvert', 'lekciya']
        higher = tuple(l + '-' for l in order[:order.index(level)])
        has_parent_link = False
        for source, target in links:
            if source == anchor_id and target.startswith(higher):
                has_parent_link = True
                break

        if not has_parent_link:
            orphan_ids.append(anchor_id)

    orphans = len(orphan_ids)
    return f"[c] Plan anchors: {len(plan_anchors)} · orphans: {orphans}", orphans

# --- main ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--koren', default=None)
    parser.add_argument('--kaskad', default=None)
    parser.add_argument('--siroty-gate', action='store_true')
    args = parser.parse_args()

    if args.koren:
        # override indeks MATERIALS
        indeks.MATERIALS = os.path.abspath(args.koren)
        indeks.ДОМА = [("test", args.koren)]
        global SBORKA_DIR
        SBORKA_DIR = pathlib.Path(args.koren).resolve() / 'SBORKA'  # fixture runs never write into the tree

    nodes, contains, links, узлы, файлы = собери_граф()
    # compute in-degree for top nodes
    in_deg = collections.Counter(t for _, t in links)
    top1_in = in_deg.most_common(1)
    top5_in = in_deg.most_common(5)

    out_lines = []
    out_lines.append(section_1(nodes, links))
    out_lines.append(section_2(nodes, links, [n for n, _ in top5_in]))
    out_lines.append(section_3(nodes, узлы, links))
    out_lines.append(section_4(nodes, узлы, contains, links, файлы))
    out_lines.append(section_5(nodes, links, contains))
    out_lines.append(section_6(links, contains))

    # compute gate [c] and handle --siroty-gate
    gate_line, orphans_count = gate_c(узлы, links)
    out_lines.append(gate_line)

    # write ZAMER-grafa.md to SBORKA_DIR
    SBORKA_DIR.mkdir(parents=True, exist_ok=True)
    zamer_path = SBORKA_DIR / 'ZAMER-grafa.md'
    with open(zamer_path, 'w', encoding='utf-8') as fh:
        fh.write('---\n')
        fh.write('opisanie: измерение графа корпуса курса «Пути и волны»\n')
        fh.write('---\n')
        fh.write('# ZAMER-grafa\n\n')
        for line in out_lines:
            fh.write(line + '\n')
        # successor context
        fh.write("\n## For the writing stages\n")
        if top1_in:
            fh.write(f"Top in-degree hub: {top1_in[0][0]} (degree={top1_in[0][1]})\n")
        fh.write("See sections [3]-[4] for depth and unreachable files.\n")

    # print output
    for line in out_lines:
        print(line)
    print(f"ZAMER-grafa.md written to {zamer_path}")

    # handle --siroty-gate flag
    if args.siroty_gate:
        sys.exit(1 if orphans_count > 0 else 0)

    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())
