---
id: ryober-ne-menshe-chem-vershin
tema: derevya
priyom: komponenta-bez-ciklov-est-derevo
uroven: 7-8
bez_otveta: da
proverka: esli ciklov net, kazhdaya komponenta — derevo, ryober v nej na odno menshe chem vershin; summiruя po komponentam, ryober strogo menshe chem vershin. Provereno vruchnuyu 2026-08-28
status: gotova
istochnik: Docenko 54 №11; Shen 28 №6
---

## Условие
Докажите, что если в графе рёбер не меньше, чем вершин, то в нём есть цикл — путь по рёбрам, возвращающийся в исходную вершину и не проходящий ни по одному ребру дважды.

## Решение
От противного: пусть циклов нет.

Разобьём граф на компоненты связности. Каждая компонента связна и циклов не содержит, то есть является деревом, а в дереве рёбер на одно меньше, чем вершин.

Сложим по всем компонентам. Если компонент c, а вершин всего n, то рёбер ровно n − c, и это строго меньше n, потому что компонента хотя бы одна.

Получилось, что рёбер меньше, чем вершин, — противоречие с условием. Значит цикл есть.
