# ИНВЕНТАРЬ УСТАНОВЛЕННЫХ СКИЛЛОВ — полный вывод `inventar.py`

> Собран этапом 2 захода `kod_nochnaya-sborka.md` в ночь на 2026-08-06.
> Скрипт: `~/Documents/GitHub/disciplina/tools/inventar.py` — **печатает, а не решает**.
> Пересобрать: `python3 ~/Documents/GitHub/disciplina/tools/inventar.py`
> Путь к сессионному бандлу скрипт находит поиском заново при каждом запуске — он с идентификаторами сессии и завтра будет другим.

```
====================================================================================================
ИНВЕНТАРЬ УСТАНОВЛЕННЫХ СКИЛЛОВ — inventar.py
Только измерения. Решения принимает человек.
====================================================================================================

####################################################################################################
# БЛОК 1. ВСЕ УСТАНОВЛЕННЫЕ СКИЛЛЫ
####################################################################################################

Поиск бандла(ов) Cowork: find по SKILL.md внутри
  /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions
Найдено SKILL.md всего: 98
Из них сгруппировано в 'бандлы' (директория .../skills/<имя>/SKILL.md): 6 групп(а)

[группа 1] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills <- содержит 'skills-plugin' в пути (похоже на основной бандл сессии)
    скиллов: 56
[группа 2] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/rpm/plugin_011e6UhbCkoAGkCN3JgHvJY7/skills
    скиллов: 21
[группа 3] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/rpm/plugin_017FSfZwAM3GF7xTpsbDUHoA/skills
    скиллов: 7
[группа 4] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/rpm/plugin_0155zZVATbJU3jHUmPP9NvMC/skills
    скиллов: 2
[группа 5] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_7ce9420f-3b9c-44ae-99fe-039447e39a25/outputs/design-studio/skills
    скиллов: 1
[группа 6] /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/rpm/plugin_01LN2TCLUU2EaKaZLSYkwxK4/skills
    скиллов: 1

Кроме того, найдено SKILL.md НЕ в форме .../skills/<имя>/SKILL.md — это НЕ инвентарь
установленных скиллов (артефакты аплоадов/аутпутов сессий), но они существуют физически,
поэтому перечисляю честно, не пряча (10 шт.):
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_0c43a89e-92e1-4508-a866-b890e838bc67/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_1f9fbfc7-617f-43ff-a9e1-28b01e6dfa0b/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_2ee7fcae-182a-4557-9b92-f19f3aefb5f5/outputs/fractal-odyssey-editor/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_4c392175-f0b6-4bec-bebb-1ba5c60b69bd/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_a311e2ef-f86b-41cc-bfff-caf428a6a992/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_b0531a12-65b0-4131-bbc2-97903256a27d/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_d33a1792-40eb-4cc2-8e5d-033adcb98c06/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_de21845e-2b97-42f8-8b29-f79be66d4f30/uploads/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_e04677e8-72af-4f63-8ed9-f85998a5b1d6/outputs/_skillsrc/agentic-coding-session-brief/SKILL.md
    /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/88a737b4-e035-46ca-b581-5df7f6c134e5/850decbc-cc39-436d-946b-0fc60725c96f/local_f393164c-b670-443c-8af0-320712340737/uploads/SKILL.md

Для инвентаря (таблица ниже) взята группа: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills
  (обоснование выбора: путь содержит 'skills-plugin' и/или это крупнейшая найденная группа;
   остальные группы перечислены выше и НЕ включены в инвентарь ниже — не выбор молча,
   а явное решение, объявленное этой строкой.)

~/.claude/skills/ — скиллов: 3 (illustrate, mac-cleanup, tidy-files)
~/.claude/plugins/cache/ — найдено SKILL.md (со всеми версионными копиями): 5
                            уникальных имён скиллов: 3 (frontend-design, math-olympiad, session-report)
    (у 'math-olympiad' 2 физические копии — версионные/orphaned директории кэша плагинов:
        /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/math-olympiad/c6e193102892/skills/math-olympiad/SKILL.md
        /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/math-olympiad/unknown/skills/math-olympiad/SKILL.md
    (у 'session-report' 2 физические копии — версионные/orphaned директории кэша плагинов:
        /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/session-report/c6e193102892/skills/session-report/SKILL.md
        /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/session-report/unknown/skills/session-report/SKILL.md

~/.claude/plugins/marketplaces/ (витрина НЕустановленного, в инвентарь НЕ входит):
    SKILL.md найдено: 41

ИТОГО в инвентаре (бандл + ~/.claude/skills/ + уникальные плагины): 62

имя                                    источник                          файлов       байт    размер  строк SKILL.md
-------------------------------------------------------------------------------------------------------------------
agentic-coding-session-brief           бандл Cowork                           1      34886   34.1 КБ             310
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/agentic-coding-session-brief
algorithmic-art                        бандл Cowork                           4      61020   59.6 КБ             405
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/algorithmic-art
brainstorming                          бандл Cowork                           2       8359    8.2 КБ             190
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/brainstorming
canvas-design                          бандл Cowork                          83    5556656    5.3 МБ             130
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/canvas-design
cinematic-longread                     бандл Cowork                          18     284908  278.2 КБ             204
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/cinematic-longread
consolidate-memory                     бандл Cowork                           1       1983    1.9 КБ              35
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/consolidate-memory
content-studio                         бандл Cowork                           6     142004  138.7 КБ              86
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/content-studio
crafting-effective-readmes             бандл Cowork                          14      60214   58.8 КБ              78
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/crafting-effective-readmes
design-system-starter                  бандл Cowork                           6      72915   71.2 КБ             603
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/design-system-starter
doc-coauthoring                        бандл Cowork                           1      15815   15.4 КБ             375
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/doc-coauthoring
docx                                   бандл Cowork                          61    1130388    1.1 МБ              91
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/docx
excalidraw                             бандл Cowork                           2      18397   18.0 КБ             221
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/excalidraw
explain-usage                          бандл Cowork                           1       1384    1.4 КБ              12
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/explain-usage
festival-concept-designer              бандл Cowork                          36    1008189  984.6 КБ             120
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/festival-concept-designer
fractal-odyssey-editor                 бандл Cowork                           4     217997  212.9 КБ             231
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/fractal-odyssey-editor
frontend-design                        плагин (~/.claude/plugins/cache/)       1       8260    8.1 КБ              55
    путь: /Users/ivanyakovlev/.claude/plugins/cache/claude-code-plugins/frontend-design/1.1.0/skills/frontend-design
gsap-core                              бандл Cowork                           1      14792   14.4 КБ             254
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/gsap-core
gsap-performance                       бандл Cowork                           1       4139    4.0 КБ              79
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/gsap-performance
gsap-scrolltrigger                     бандл Cowork                           1      18390   18.0 КБ             296
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/gsap-scrolltrigger
gsap-timeline                          бандл Cowork                           1       4394    4.3 КБ             107
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/gsap-timeline
html-slides-studio                     бандл Cowork                         124    7747051    7.4 МБ             443
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/html-slides-studio
humanizer                              бандл Cowork                           2      23264   22.7 КБ             439
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/humanizer
illustrate                             ~/.claude/skills/                      1       4089    4.0 КБ              77
    путь: /Users/ivanyakovlev/.claude/skills/illustrate
karpathy-guidelines                    бандл Cowork                           1       9948    9.7 КБ             130
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/karpathy-guidelines
kt-channel-editor                      бандл Cowork                          10     286699  280.0 КБ             147
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/kt-channel-editor
mac-cleanup                            ~/.claude/skills/                     20     304155  297.0 КБ             204
    путь: /Users/ivanyakovlev/.claude/skills/mac-cleanup
manim-composer                         бандл Cowork                           5      22814   22.3 КБ             138
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/manim-composer
manim-skill                            бандл Cowork                          81     333237  325.4 КБ              63
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/manim-skill
manimce-best-practices                 бандл Cowork                          37     210744  205.8 КБ             151
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/manimce-best-practices
math-olympiad                          бандл Cowork                          10      61609   60.2 КБ             411
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/math-olympiad
math-olympiad                          плагин (~/.claude/plugins/cache/)      11      63617   62.1 КБ             411
    путь: /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/math-olympiad/c6e193102892/skills/math-olympiad
math-russian-terminology               бандл Cowork                           2      16423   16.0 КБ             137
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/math-russian-terminology
math-video-studio                      бандл Cowork                           4      24941   24.4 КБ             127
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/math-video-studio
math-writing-conventions               бандл Cowork                           1       9088    8.9 КБ              83
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/math-writing-conventions
mermaid-diagrams                       бандл Cowork                           9      85640   83.6 КБ             217
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/mermaid-diagrams
microinteractions                      бандл Cowork                           7     111291  108.7 КБ             239
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/microinteractions
morning                                бандл Cowork                           3      37103   36.2 КБ             136
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/morning
orchestrating-gsap-lenis               бандл Cowork                           1       4007    3.9 КБ             150
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/orchestrating-gsap-lenis
pdf                                    бандл Cowork                          12      58692   57.3 КБ             314
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/pdf
popsci-narrative                       бандл Cowork                           3      70826   69.2 КБ             413
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/popsci-narrative
popsci-research                        бандл Cowork                           1      40575   39.6 КБ             347
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/popsci-research
pptx                                   бандл Cowork                          56    1140868    1.1 МБ             238
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/pptx
project-kickoff                        бандл Cowork                           2      14251   13.9 КБ             178
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/project-kickoff
proof-self-review                      бандл Cowork                           1      13767   13.4 КБ             152
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/proof-self-review
refactoring-ui                         бандл Cowork                           6      73678   72.0 КБ             304
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/refactoring-ui
russian-editor                         бандл Cowork                           9      85993   84.0 КБ             696
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/russian-editor
schedule                               бандл Cowork                           1       2399    2.3 КБ              41
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/schedule
scrollytelling                         бандл Cowork                           1      28633   28.0 КБ             919
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/scrollytelling
session-handoff                        бандл Cowork                          12      82419   80.5 КБ             189
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/session-handoff
session-report                         плагин (~/.claude/plugins/cache/)       3      57756   56.4 КБ              42
    путь: /Users/ivanyakovlev/.claude/plugins/cache/claude-plugins-official/session-report/c6e193102892/skills/session-report
setup-cowork                           бандл Cowork                           1      12029   11.7 КБ              97
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/setup-cowork
site-cross-device-audit                бандл Cowork                          11     107809  105.3 КБ             193
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/site-cross-device-audit
skill-creator                          бандл Cowork                          18     227236  221.9 КБ             485
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/skill-creator
skill-judge                            бандл Cowork                           2      39784   38.9 КБ             752
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/skill-judge
the-interviewer                        бандл Cowork                           1      12786   12.5 КБ             121
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/the-interviewer
theme-factory                          бандл Cowork                          13     144106  140.7 КБ              59
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/theme-factory
threejs                                бандл Cowork                          14     162872  159.1 КБ              44
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/threejs
tidy-files                             ~/.claude/skills/                      2       8218    8.0 КБ              74
    путь: /Users/ivanyakovlev/.claude/skills/tidy-files
transposition-paper                    бандл Cowork                           1       7760    7.6 КБ              77
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/transposition-paper
visual-design-review                   бандл Cowork                           1       6857    6.7 КБ             116
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/visual-design-review
web-typography                         бандл Cowork                           6      72048   70.4 КБ             396
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/web-typography
xlsx                                   бандл Cowork                          53    1105545    1.1 МБ              99
    путь: /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/xlsx

####################################################################################################
# БЛОК 2. АВТОРСКИЕ vs ВНЕШНИЕ
####################################################################################################

Признак (придуман для этого скрипта, печатается для критики читателем):
  Смотрим на поле description: во фронтматтере SKILL.md. Считаем долю кириллических
  букв среди всех кириллических+латинских букв в этом тексте.
    доля >= 0.65  -> 'авторский' (описание написано по-русски => это писал владелец)
    доля <= 0.35  -> 'внешний'   (описание написано по-английски => пришло извне)
    иначе, либо description не найден -> 'спорный' (нет явного большинства, разобрать глазами)
  Обоснование: язык description — это язык автора, который его писал для себя/системы;
  почти все внешние (Anthropic/сторонние плагины) скиллы описаны по-английски, а те, что
  ставил себе владелец, — по-русски (см. свежие CLAUDE.md/MEMORY.md, они тоже по-русски).
  Это ЭВРИСТИКА, не факт авторства — переносить готовое чужое описание на русский или
  наоборот легко, поэтому спорные случаи вынесены отдельно, а не распиханы силой.

Авторские: 15
    agentic-coding-session-brief           — кириллица 673/793 = 0.85
    content-studio                         — кириллица 514/698 = 0.74
    fractal-odyssey-editor                 — кириллица 507/568 = 0.89
    kt-channel-editor                      — кириллица 515/579 = 0.89
    mac-cleanup                            — кириллица 494/554 = 0.89
    math-russian-terminology               — кириллица 462/484 = 0.95
    math-writing-conventions               — кириллица 692/720 = 0.96
    popsci-narrative                       — кириллица 438/491 = 0.89
    popsci-research                        — кириллица 773/825 = 0.94
    project-kickoff                        — кириллица 533/566 = 0.94
    proof-self-review                      — кириллица 614/620 = 0.99
    russian-editor                         — кириллица 381/387 = 0.98
    site-cross-device-audit                — кириллица 591/799 = 0.74
    tidy-files                             — кириллица 427/488 = 0.88
    transposition-paper                    — кириллица 679/705 = 0.96

Внешние: 47
    algorithmic-art                        — кириллицы 0, латиницы 271
    brainstorming                          — кириллицы 0, латиницы 322
    canvas-design                          — кириллицы 0, латиницы 234
    cinematic-longread                     — кириллицы 0, латиницы 661
    consolidate-memory                     — кириллицы 0, латиницы 74
    crafting-effective-readmes             — кириллицы 0, латиницы 122
    design-system-starter                  — кириллицы 0, латиницы 167
    doc-coauthoring                        — кириллицы 0, латиницы 358
    docx                                   — кириллицы 0, латиницы 654
    excalidraw                             — кириллицы 0, латиницы 236
    explain-usage                          — кириллицы 0, латиницы 151
    festival-concept-designer              — кириллица 164/772 = 0.21
    frontend-design                        — кириллицы 0, латиницы 170
    gsap-core                              — кириллицы 0, латиницы 430
    gsap-performance                       — кириллицы 0, латиницы 184
    gsap-scrolltrigger                     — кириллицы 0, латиницы 267
    gsap-timeline                          — кириллицы 0, латиницы 242
    html-slides-studio                     — кириллица 77/710 = 0.11
    humanizer                              — кириллицы 0, латиницы 461
    illustrate                             — кириллицы 0, латиницы 447
    karpathy-guidelines                    — кириллицы 0, латиницы 765
    manim-composer                         — кириллицы 0, латиницы 551
    manim-skill                            — кириллицы 0, латиницы 152
    manimce-best-practices                 — кириллицы 0, латиницы 385
    math-olympiad                          — кириллицы 0, латиницы 555
    math-olympiad                          — кириллицы 0, латиницы 555
    math-video-studio                      — кириллица 32/770 = 0.04
    mermaid-diagrams                       — кириллицы 0, латиницы 590
    microinteractions                      — кириллицы 0, латиницы 507
    morning                                — кириллицы 0, латиницы 265
    orchestrating-gsap-lenis               — кириллицы 0, латиницы 129
    pdf                                    — кириллицы 0, латиницы 353
    pptx                                   — кириллицы 0, латиницы 567
    refactoring-ui                         — кириллицы 0, латиницы 462
    schedule                               — кириллицы 0, латиницы 158
    scrollytelling                         — кириллицы 0, латиницы 227
    session-handoff                        — кириллицы 0, латиницы 503
    session-report                         — кириллицы 0, латиницы 125
    setup-cowork                           — кириллицы 0, латиницы 67
    skill-creator                          — кириллицы 0, латиницы 261
    skill-judge                            — кириллицы 0, латиницы 205
    the-interviewer                        — кириллицы 0, латиницы 768
    theme-factory                          — кириллицы 0, латиницы 206
    threejs                                — кириллица 15/516 = 0.03
    visual-design-review                   — кириллица 60/440 = 0.14
    web-typography                         — кириллицы 0, латиницы 468
    xlsx                                   — кириллицы 0, латиницы 752

Спорные (третья корзина, не распиханы силой): 0

####################################################################################################
# БЛОК 3. СВЕРКА С SHVY-lenta-reserch.md §C0/§C1
####################################################################################################

Секции найдены в файле: C0 да, C1 да

величина                                        заявлено в SHVY §C    измерено сейчас   совпало?
----------------------------------------------------------------------------------------------------
бандл Cowork, скиллов                                           56                 56         да
~/.claude/skills/, скиллов                                       3                  3         да
плагины, уникальных скиллов                                      3                  3         да
ВСЕГО установлено                                               62                 62         да

Дублей — текстом в SHVY заявлено: 9
Дублей — имён скиллов реально перечислено в таблице §C1 (bold+backtick): 10
РАСХОЖДЕНИЕ: сам текст SHVY §C1 называет число 9, но его же таблица
перечисляет 10 имён скиллов. Это расхождение внутри исходного документа,
не привнесённое этим скриптом — печатаю как есть, не решаю, какое число правильное.

имя (заявлено в §C1)                      установлен? (измерено)                                    где найден
----------------------------------------------------------------------------------------------------------------
html-slides-studio                                            да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/html-slides-studio
content-studio                                                да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/content-studio
popsci-research                                               да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/popsci-research
popsci-narrative                                              да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/popsci-narrative
the-interviewer                                               да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/the-interviewer
brainstorming                                                 да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/brainstorming
math-russian-terminology                                      да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/math-russian-terminology
russian-editor                                                да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/russian-editor
humanizer                                                     да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/humanizer
proof-self-review                                             да /Users/ivanyakovlev/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/850decbc-cc39-436d-946b-0fc60725c96f/88a737b4-e035-46ca-b581-5df7f6c134e5/skills/proof-self-review

####################################################################################################
# БЛОК 4. АВТОРСКИЕ СКИЛЛЫ: ЕСТЬ ЛИ КОПИЯ В GIT НА ДИСКЕ
####################################################################################################

Поиск: find /Users/ivanyakovlev/Documents/GitHub — по имени (регистронезависимо), файл или директория,
совпадающие с именем скилла, вне .git/. Для каждого совпадения проверяется, лежит ли
оно внутри git-репозитория (git rev-parse --is-inside-work-tree).

скилл (авторский)                        найден на диске?   в git-репозитории? где
------------------------------------------------------------------------------------------------------------------------
agentic-coding-session-brief                          НЕТ                    —
content-studio                                        НЕТ                    —
fractal-odyssey-editor                                 да                   да
    /Users/ivanyakovlev/Documents/GitHub/matema-fest (/Users/ivanyakovlev/Documents/GitHub/matema-fest/fractal-odyssey-editor)
kt-channel-editor                                     НЕТ                    —
mac-cleanup                                           НЕТ                    —
math-russian-terminology                              НЕТ                    —
math-writing-conventions                              НЕТ                    —
popsci-narrative                                      НЕТ                    —
popsci-research                                       НЕТ                    —
project-kickoff                                       НЕТ                    —
proof-self-review                                     НЕТ                    —
russian-editor                                        НЕТ                    —
site-cross-device-audit                               НЕТ                    —
tidy-files                                            НЕТ                    —
transposition-paper                                   НЕТ                    —

ИТОГО авторских скиллов: 15
  подтверждена копия в git-репозитории на диске: 1 — fractal-odyssey-editor
  НЕ найдено на диске / НЕ внутри git (пропадёт при потере аккаунта, если верно): 14 — agentic-coding-session-brief, content-studio, kt-channel-editor, mac-cleanup, math-russian-terminology, math-writing-conventions, popsci-narrative, popsci-research, project-kickoff, proof-self-review, russian-editor, site-cross-device-audit, tidy-files, transposition-paper

====================================================================================================
Конец инвентаря.
====================================================================================================
```
