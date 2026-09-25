import pathlib, sys
sys.path.insert(0, "/Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools")
import check_arhiv as ca

Z = "kurs-puti-i-volny/ZAMYSEL.md"
K = "kurs-puti-i-volny/"
BANNERS = {
    K + "KOSTYAK.md":
        "> УСТАРЕЛ — cancelled by entry centralnyj-obekt-okruzhnost, %s:290 (2026-09-02); kept as a source of material, not as truth (%sARHITEKTURA.md:98)." % (Z, K),
    K + "README.md":
        "> УСТАРЕЛ — frozen at 2026-08-05 (%sARHITEKTURA.md:100); cancelled by entries centralnyj-obekt-okruzhnost (%s:290) and chetyre-chetverti (%s:321); the entry point is ZAMYSEL.md." % (K, Z, Z),
    K + "plan/src/plan.md":
        "> ОТМЕНЁН — rejected by the owner 2026-08-06 (field «ЗАБРАКОВАН» in this file); the composition moved to plan/src/punkty.md (%sARHITEKTURA.md:99)." % K,
    K + "otchety/RASSKAZ-dva-sposoba.md":
        "> УСТАРЕЛ — written on a spine that was abandoned (%sREESTR-reserchey.md:43); keep as a draft, not as a plan." % K,
    K + "zahody/ZAHOD-okruzhnost-i-nepreryvnyj-predel.md":
        "> ОТМЕНЁН — the owner redefined the frame the same day (%sREESTR-reserchey.md:35); see ZAHOD-okruzhnost.md." % K,
    K + "zahody/ZAHOD-formy-yakobi.md":
        "> ОТМЕНЁН — this brief stands on the cancelled frame of entry centralnyj-obekt-okruzhnost, %s:302 (cancelled 2026-09-02); do not run it as is." % Z,
    K + "zahody/ZAHOD-sverka-koncepcii.md":
        "> ОТМЕНЁН — this brief stands on the cancelled frame of entry centralnyj-obekt-okruzhnost, %s:302 (cancelled 2026-09-02); do not run it as is." % Z,
}
# section marks: file -> (line-number-to-insert-BEFORE (1-based), expected prefix of that line, mark text)
M = ca.SECTION_MARK
MARKS = {
    K + "HREBET-kursa.md": (14, "## Хребет: четыре четверти",
        "> %s chetyre-chetverti — %s:321. The quarter framing of the year below is cancelled (replaced by plan/src/karkas.md); the measurements and materials in this file stay valid." % (M, Z)),
    K + "REESTR-reserchey.md": (18, "### Линия хребта и плана года",
        "> %s chetyre-chetverti — %s:321. The register keeps HREBET-kursa.md as the central position of the year plan; the quarter framing is cancelled, the rows of this register stay valid." % (M, Z)),
    K + "otchety/RAZBOR-i-perestroyka.md": (78, "**Второе, ради которого всё.**",
        "> %s centralnyj-obekt-okruzhnost — %s:290. The circle as the carrying object is cancelled (2026-09-02); the circle = strip identity itself stands (%s:292)." % (M, Z, Z)),
    "_studio/zhurnal/2026-08-24_obzor-funkciya-putey/NAVIGATOR.md": (9, "> 🔴 **Здесь стоял отменённый образец",
        "> %s zhanr-burbaki — %s:309. The Bourbaki survey-talk genre is cancelled (2026-09-02); the genre model is the Gys promenade (%s:121)." % (M, Z, Z)),
}

new = {}
for path, reason in BANNERS.items():
    lines = pathlib.Path(path).read_text(encoding="utf-8").split("\n")
    assert lines[0] == "---", (path, "no frontmatter at line 1")
    close = next(i for i in range(1, len(lines)) if lines[i] == "---")
    assert close <= 7, (path, "frontmatter closes too late for the 10-line rule", close)
    assert not any(ca.BANNER in l for l in lines[:12]), (path, "banner already present")
    lines[close + 1:close + 1] = [ca.BANNER, reason]
    assert ca.BANNER in lines[:10][close + 1 - 0] or True
    new[path] = "\n".join(lines)
for path, (at, prefix, text) in MARKS.items():
    lines = pathlib.Path(path).read_text(encoding="utf-8").split("\n")
    assert lines[at - 1].startswith(prefix), (path, at, lines[at - 1][:60])
    assert not any(ca.SECTION_MARK in l for l in lines), (path, "mark already present")
    lines[at - 1:at - 1] = [text, ""]
    new[path] = "\n".join(lines)
for path, txt in new.items():
    pathlib.Path(path).write_text(txt, encoding="utf-8")
    print("written", path)
