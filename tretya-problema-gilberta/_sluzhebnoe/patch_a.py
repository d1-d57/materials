import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
rep("popsci article on Hilbert's third problem + drafts","popsci article (Hilbert third problem) + drafts")
rep("2. `grep -c '^\\*\\*ЗАКРЫВАЕТ:\\*\\*'` in RESHENIYA:","2. `grep -c '^\\*\\*ЗАКРЫВАЕТ:\\*\\*' skills/{mat-blok,math-style-editor,illustracii,lenta}/RESHENIYA.md`:")
rep("= 9; `grep -c 'жёсткий перенос' skills/lenta/references/FORMA.md` = 0.",
    "= 9.\n5. The false FORMA row is gone: `grep -c 'жёсткий перенос' skills/lenta/references/FORMA.md` falls from the build-time 1 to zero.")
rep("5. Nothing lost:","6. Nothing lost:")
rep("6. Two commit hashes","7. Two commit hashes")
rep("**Coverage line inside the verdict:** «lessons","8. Live run on the real object, not only the counts: `python3 _generator/tools/check_lenta.py /Users/ivanyakovlev/Documents/GitHub/materials/tretya-problema-gilberta/LENTA/lenta.md` → rc=0 and «это не лента … L9 чиста» (snapshot 2026-10-03: exactly that) — the FORMA edits must not break the gate on the accepted article.\n**Coverage line inside the verdict:** «lessons")
rep("Модель: Sonnet 5 — <одна фраза почему; см. шапку захода>.","Модель: Sonnet 5 — тексты правил и уроков готовы в черновиках, работа — расстановка и вызовы дверей.")
rep("Ты исполнитель в репозитории /Users/ivanyakovlev/Documents/GitHub/disciplina-wt/pravila-teksty.",
    "Ты исполнитель. Сессия открыта в /Users/ivanyakovlev/Documents/GitHub/disciplina (основная папка); работать будешь в /Users/ivanyakovlev/Documents/GitHub/disciplina-wt/pravila-teksty.")
rep("Первым ходом: python3 _generator/tools/git_zona.py worktree add pravila-teksty --branch zahod/pravila-teksty, затем чтение захода",
    "Первым ходом: прочитай заход из основной папки и исполни §0.1 — субагент забирает в основную ветку хвост Cowork, В ТОМ ЧИСЛЕ папку арки _studio/zhurnal/2026-10-03_pravila-statya и _studio/docs/KARTA.md (арка собрана из песочницы и в git её ещё нет; без этого рабочая папка её не увидит). Только потом: python3 _generator/tools/git_zona.py worktree add pravila-teksty --branch zahod/pravila-teksty, затем")
p.write_text(s,encoding="utf-8"); print("patched")
