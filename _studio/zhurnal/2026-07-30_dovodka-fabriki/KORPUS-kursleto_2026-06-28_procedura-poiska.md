# KORPUS — арка `kurs leto 2026/zhurnal/2026-06-28_procedura-poiska`

Сырые кандидаты в уроки фабрике. Без закона, без вердикта, без морали.

`kod_klubok-sborka.md` — кандидатов нет (файл прочитан целиком, все секции пусты).

## kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md

### Правило реконсиляции TRIAGE↔DEEPEN не прописано — DEEPEN сам себе противоречил на Шенноне
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ВОПРОСЫ, строка 101
ЦЕНА: НЕ НАЗВАНА (внутреннее противоречие самого DEEPEN; «правило реконсиляции... в спеке явно не прописано»)

### DEEPEN-субагент схлопывает scorecard в неплоскую форму без CLI --json-schema
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ОТЧЁТ, строки 142–144
ЦЕНА: там, где DEEPEN потерял данные (Монте-Карло), пер-критериальные баллы взяты из TRIAGE

### GATHER-Haiku вернул невалидные типы (риск §10.2 материализовался) — 3 из 6 сырых scorecard невалидны
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ОТЧЁТ, строка 137
ЦЕНА: 3/6 невалидны на сырье (починены TRIAGE, 4 ремонта в w2_repair_log.json)

## kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md

### w1 GATHER: 12 из 74 черновых scorecard схемно невалидны (штатный haiku-брак)
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 76
ЦЕНА: схемно 62/74 (12 записей — «штатный haiku-брак обл. «логика»: dvizhki массивом / vs_yakor строкой, чинит w2»)

### w3 DEEPEN: факт-чек поймал фабрикации субагента (Нобель Шеннона, QR/CD на коде Хэмминга)
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 78
ЦЕНА: НЕ НАЗВАНА

### w4 ASSEMBLE (Opus-ядро) ложно отчитался «0 подозрительных», хотя было 3 завышения Pugh — поймано только tripwire-судьёй
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 79
ЦЕНА: НЕ НАЗВАНА

## kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md

### Оркестратор физически шёл на Opus вместо предписанного Sonnet — модель сессии на лету не переключить
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md#ВОПРОСЫ, строка 60
ЦЕНА: НЕ НАЗВАНА

### Субагент Ф3-b4 промахнулся индексами и задвоил Хэмминга — потребовалась пере-сшивка по name-match
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md#ОТЧЁТ, строка 89
ЦЕНА: НЕ НАЗВАНА

## kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md

### Headless claude -p не аутентифицирован (401) — прогон «прошёл» все 5 волн за секунды без единого артефакта
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md#ОТЧЁТ, строки 73–87
ЦЕНА: созданы 0-байтные w1_run.json…w5_run.json; реальных артефактов нет; w5_dossier.md отсутствует (но 5-час окно не сгорело — 3 сек, 0 токенов)

### Оркестратор молча считает пустой/ошибочный вывод claude -p успехом — нет guard на 401/пустой артефакт
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md#ВОПРОСЫ, строки 60–61
ЦЕНА: при 401 машина «проходит» все 5 волн за 3 секунды без единого токена и без досье

## kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md

### orchestrate.sh падает мгновенно на ветке `all` — bash `set -u`, необъявленная переменная w1 на строке 56
АДРЕС: kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md#ОТЧЁТ, строки 73–79
ЦЕНА: волна w1 не стартовала, свежих w*-артефактов от прогона нет (упало до первой волны, окно не пострадало)
