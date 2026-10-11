"""TikZ-рисунки клетчатых фигур для листка, разбора и шпаргалки 6.10 (одна функция на все три документа).
Толстая линия — граница фигуры или разрез между частями; чёрные клетки — серым (печать ч/б)."""
NB = ((1,0),(-1,0),(0,1),(0,-1))

def grid(h, w, region=None, tiles=None, black=(), holes=(), path=None, closed=False, marks=(), s=0.42, lw=1.3):
    region = {tuple(x) for x in region} if region else {(r, c) for r in range(h) for c in range(w)}
    holes = {tuple(x) for x in holes}; region -= holes
    black = {tuple(x) for x in black}; marks = {tuple(x) for x in marks}
    piece = {}
    for i, t in enumerate(tiles or []):
        for c in t: piece[tuple(c)] = i
    X = lambda c: f"{c*s:.3f}"; Y = lambda r: f"{-r*s:.3f}"
    L = [f"\\begin{{tikzpicture}}[baseline=(current bounding box.north)]"]
    for (r, c) in sorted(black & region):
        L.append(f"\\fill[black!45] ({X(c)},{Y(r)}) rectangle ({X(c+1)},{Y(r+1)});")
    for (r, c) in sorted(region):
        L.append(f"\\draw[black!35,line width=0.3pt] ({X(c)},{Y(r)}) rectangle ({X(c+1)},{Y(r+1)});")
    for (r, c) in sorted(holes):
        L.append(f"\\draw[black!50,densely dotted] ({X(c)},{Y(r)}) rectangle ({X(c+1)},{Y(r+1)});")
    seg = []
    for (r, c) in region:
        for (a, b, x1, y1, x2, y2) in ((-1,0,c,r,c+1,r), (1,0,c,r+1,c+1,r+1), (0,-1,c,r,c,r+1), (0,1,c+1,r,c+1,r+1)):
            n = (r+a, c+b)
            if n not in region or (tiles and piece.get(n) != piece.get((r, c))):
                seg.append(f"({X(x1)},{Y(y1)})--({X(x2)},{Y(y2)})")
    L.append(f"\\draw[line width={lw}pt,line cap=rect] " + " ".join(seg) + ";")
    for (r, c) in sorted(marks):
        L.append(f"\\fill ({(c+.5)*s:.3f},{-(r+.5)*s:.3f}) circle ({s*0.18:.3f});")
    if path:
        pts = "--".join(f"({(c+.5)*s:.3f},{-(r+.5)*s:.3f})" for r, c in path)
        L.append(f"\\draw[line width=1.1pt,rounded corners=1pt] {pts}{'--cycle' if closed else ''};")
        r0, c0 = path[0]; L.append(f"\\fill ({(c0+.5)*s:.3f},{-(r0+.5)*s:.3f}) circle ({s*0.2:.3f});")
    L.append("\\end{tikzpicture}")
    return "\n".join(L)

def polys(P, W, H, gap=None, u=0.3):
    L = [f"\\begin{{tikzpicture}}[baseline=(current bounding box.north)]",
         f"\\draw[black!25,line width=0.25pt] (0,0) grid[step={u}] ({W*u:.3f},{H*u:.3f});"]
    for name, pts in P.items():
        L.append("\\draw[line width=1pt,line join=round] " + "--".join(f"({x*u:.3f},{y*u:.3f})" for x, y in pts) + "--cycle;")
    if gap:
        L.append("\\fill[black] " + "--".join(f"({x*u:.3f},{y*u:.3f})" for x, y in gap) + "--cycle;")
    L.append("\\end{tikzpicture}")
    return "\n".join(L)
