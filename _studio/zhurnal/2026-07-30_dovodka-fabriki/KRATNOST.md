# KRATNOST — сводка кратности по корпусу кандидатов

Счёт, не закон: сколько раз похожий механизм поломки встретился независимо, и по каким адресам. Группировка — по МЕХАНИЗМУ поломки (что именно сломалось и как), а не по теме лекции или арке. Единица — запись корпуса (`### ` в `KORPUS-*.md`); всего записей в корпусе: **461**.

Метод построения: сначала — систематический грепом-проход по формулировкам (повторяющиеся инциденты вроде «rc=128», «коммит на 89 файлов», «/cost недоступен» узнаются по почти дословным повторам текста в разных файлах — это ожидаемо: многие заходы независимо цитируют один и тот же известный инцидент фабрики), затем — по смысловой близости оставшихся записей. Группы отсортированы по убыванию кратности; группы кратности 1 в конце — это не менее ценные находки, просто без независимого повторения (пока).

---

## 1. Канонический документ описывает состояние, которое разошлось с живыми файлами/кодом (устарел, противоречит, не совпадает) — 22 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md#ОТЧЁТ, строки 99–101
- _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md#ВОПРОСЫ, строка 96
- _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md#ПЛАН, строка 79
- _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md#ВОПРОСЫ, строка 109
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md#ПЛАН, строки 62–73
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 211
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 213
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 217
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md#ОТЧЁТ, строка 257
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 83–85
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 57–60
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 77–82
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ВОПРОСЫ, строки 251–260
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#ЗАДАНИЕ, строки 93–99
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 101–104
- _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ, строки 204–206
- _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ, строки 175–177
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 72–76
- _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строки 71–73
- catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md#ОТЧЁТ, строки 114–115
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md#ВОПРОСЫ, строка 105
- kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md#ВОПРОСЫ, строка 109

## 2. Инструмент `/cost`/точный счётчик токенов недоступен в среде — время/токены даны оценкой — 17 вхожд.
- catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md#ОТЧЁТ, строки 123–124
- catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md#ОТЧЁТ, строка 82
- catalan/zhurnal/2026-07-03_programma-kursa/kod_krever-extract.md#ОТЧЁТ, строки 168–169
- catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md#ОТЧЁТ, строка 105
- catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md#ОТЧЁТ, строка 149
- catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md#ОТЧЁТ, строки 67–68
- catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md#ОТЧЁТ, строки 100–101
- catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md#ОТЧЁТ, строка 164
- catalan/zhurnal/2026-07-05_mir1/kod_skelet-mir1.md#ОТЧЁТ, строка 95
- catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md#ОТЧЁТ, строки 193–194
- kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_svap-tz-v2.md#ОТЧЁТ, строка 137
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md#ОТЧЁТ, строка 114
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md#ОТЧЁТ, строка 189
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_ideal-L2.md#ОТЧЁТ, строка 121
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md#ОТЧЁТ, строка 159
- kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator-visual.md#ОТЧЁТ, строка 90
- kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md#ОТЧЁТ, строка 154

## 3. Гейт даёт неверный сигнал (зелёный при дефекте или красный на здоровом) из-за узости самой проверки — 15 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md#ЗАДАНИЕ, строки 6–10, 85
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md#ЗАДАНИЕ, строка 83
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md#ЗАДАНИЕ, строка 84
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#ЗАДАНИЕ, строка 77
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#УРОКИ ФАБРИКЕ, строки 189–191
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ЗАДАНИЕ, строка 119
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ОТЧЁТ, строки 497–513
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md#ЗАДАНИЕ, строка 33
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md#ЗАДАНИЕ, строка 34
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#ЗАДАНИЕ, строка 70
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#УРОКИ ФАБРИКЕ, строки 150–154
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 133–136
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 159–163
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ОТЧЁТ, строка 268
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ОТЧЁТ, строка 270

## 4. Параллельный/соседний заход или сессия задевает чужую зону (общий коммит, общий индекс, общая ветка) — 14 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md#ВОПРОСЫ, строка 127
- _studio/zhurnal/2026-07-11_geometria-6-nagliadnaya/kod_reserch-geometria.md#ВОПРОСЫ, строка 83
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vneshnyaya.md#ЗАДАНИЕ, строки 3–5
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md#УРОКИ ФАБРИКЕ, строки 156–158
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md#УРОКИ ФАБРИКЕ, строки 129–131
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md#ВОПРОСЫ, строки 162–166
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md#ЗАДАНИЕ, строка 17
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строка 232
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md#ЗАДАНИЕ, строка 201
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ЗАДАНИЕ, строка 92
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ЗАДАНИЕ, строка 101
- _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ЗАДАНИЕ, строка 57
- _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 41
- _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 81

## 5. Коммит без явных путей (`git commit` без pathspec/`add`) забирает чужой застейдженный индекс целиком — 12 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md#ЗАДАНИЕ, строка 7
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#УРОКИ ФАБРИКЕ, строки 160–164
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md#ЗАДАНИЕ, строки 94–96
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md#ЗАДАНИЕ, строки 155–157
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строка 224
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md#ЗАДАНИЕ, строка 26
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ЗАДАНИЕ, строка 21
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ЗАДАНИЕ, строка 25
- _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ЗАДАНИЕ, строка 13
- _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ЗАДАНИЕ, строка 66
- _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 98
- _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 73

## 6. Код возврата `rc=128` (сбой прав окружения) прочитан как содержательный результат команды — 10 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ЗАДАНИЕ, строка 29
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md#ЗАДАНИЕ, строка 29
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строка 118
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md#ЗАДАНИЕ, строка 57
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ЗАДАНИЕ, строка 38
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ЗАДАНИЕ, строка 42
- _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ЗАДАНИЕ, строка 22
- _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ЗАДАНИЕ, строка 27
- _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 28
- _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 29

## 7. Новый `.md` не зарегистрирован в `KARTA.md §6` — документ-сирота — 10 вхожд.
- _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md#ВОПРОСЫ, строка 119
- _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md#УРОКИ ФАБРИКЕ, строки 334–337
- _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#УРОКИ ФАБРИКЕ, строки 181–184
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строка 41
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md#ЗАДАНИЕ, строка 25
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ЗАДАНИЕ, строка 20
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ЗАДАНИЕ, строка 24
- _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ЗАДАНИЕ, строка 12
- _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md#ВОПРОСЫ, строки 92–94; #ОТЧЁТ, строки 117–121
- _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 12

## 8. Незакоммиченная работа соседа/аналитика лежит в рабочем дереве на момент точки отката — 9 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md#ОТЧЁТ, строки 119–123
- _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md#ЗАДАНИЕ, строки 18–25
- _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md#УРОКИ ФАБРИКЕ, строки 81–83
- _studio/zhurnal/2026-07-23_vneshnie-istorii/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 37–41
- _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md#ОТЧЁТ, строки 321–323
- _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md#ПЛАН, строки 199–203
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ, строки 291–302
- _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 80
- _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md#ВОПРОСЫ, строка 96

## 9. Осиротевший `.git/index.lock` (свой или чужой) блокирует коммиты — 7 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md#ПЛАН, строка 85
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ, строки 65–66
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 43–46
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md#УРОКИ ФАБРИКЕ, строки 112–113
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md#ЗАДАНИЕ, строки 10, 14
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ЗАДАНИЕ, строка 17
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md#ЗАДАНИЕ, строка 21

## 10. Контракт зоны предписывает `git add → git commit`, что при живущем в репо авто-коммите/общем индексе не даёт узкий коммит — 7 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md#УРОКИ ФАБРИКЕ, строки 99–101
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md#ВОПРОСЫ, строка 140
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ЗАДАНИЕ, строка 143
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 97–100
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 105–108
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 145–148
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 132–136

## 11. Внешний источник недоступен из среды (таймаут, TLS, 404, WebFetch не вытягивает содержимое) — 6 вхожд.
- _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md#ОТЧЁТ, строка 76
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md#ОТЧЁТ, строки 116, 165
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md#ВОПРОСЫ, строка 148
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md#УРОКИ ФАБРИКЕ, строки 64–66
- _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md#ОТЧЁТ, строки 225–228
- catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md#ОТЧЁТ, строки 108–109

## 12. Аналитик утверждает факт (мотивация/предпосылка), не проверив источник — опровергается позже — 5 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md#ЗАДАНИЕ, строка 30
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md#ОТЧЁТ, строка 192
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md#ЗАДАНИЕ, строки 47–48
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md#ОТЧЁТ, строка 299
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 365–378

## 13. Канвас-симуляция (buffon) не соблюдает жизненный цикл: не с нуля, не сбрасывается, не запускается при показе — 5 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md#ОТЧЁТ, строка 144
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 227
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 108
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 113
- buffon/WORKLIST.md#§7 A3, строка 214

## 14. Субагент обрывается по сети/каналу («Connection closed», рейт-лимит) посреди задачи — 5 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md#ОТЧЁТ, строка 336
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ, строки 74–76
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ, строки 71–72
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 51–56
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 83–86

## 15. Правило, которое эталонный дек `buffon` применяет к себе (масштаб/цвет/золото/подсветка/пример проваливает свой аудит), не выглядит перенесённым в общий канон фабрики — 5 вхожд.
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 114
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 109
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 110
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 111
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 112

## 16. Нулевой греп по корпусу принят за доказательство отсутствия понятия — предмет на деле есть — 4 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md#ЗАДАНИЕ, строка 63
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md#ЗАДАНИЕ, строка 67
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md#ЗАДАНИЕ, строка 40
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md#ОТЧЁТ, строки 181–182

## 17. Браузер Playwright недоступен/не скачивается в песочнице — рендер обходится системным Chrome или харнесс не переживает сессию — 4 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md#ОТЧЁТ, строка 149
- buffon/WORKLIST.md#§3 «Идеи на будущее», строка 115
- buffon/ZAHOD-01.md#ПЛАН, строка 189
- catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md#ОТЧЁТ, строки 152–155

## 18. Субагент выдумывает факт/цитату/атрибуцию, которых нет в источнике — 4 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md#ОТЧЁТ, строка 135
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md#УРОКИ ФАБРИКЕ, строки 77–79
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md#ПЛАН, строка 108
- kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 78

## 19. Число/счётчик, вписанное руками в шапку/статус, устарело или было неверным с самого начала — 3 вхожд.
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md#ПЛАН, строки 118–122
- _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md#ВОПРОСЫ, строка 240
- catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md#ПЛАН, строка 109

## 20. Независимый свежий верификатор ловит дефект, который автор правки не заметил (слепое пятно автора) — 3 вхожд.
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1.md#ОТЧЁТ, строки 124–126
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md#ОТЧЁТ, строка 225
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ОТЧЁТ, строки 371–376

## 21. Пре-коммит хук на общем/глобальном файле блокирует коммит по чужому, не относящемуся к зоне долгу — 3 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#УРОКИ ФАБРИКЕ, строки 193–195
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md#ВОПРОСЫ, строка 142
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#УРОКИ ФАБРИКЕ, строки 148–152

## 22. Работа/правило осталось вне границ этого захода — перенос отложен на будущее и не сделан — 3 вхожд.
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md#ОТЧЁТ, строки 64–67
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md#ВОПРОСЫ, строка 60
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md#ОТЧЁТ, строки 112–113

## 23. Скрытая/фоновая вкладка браузера троттлит анимацию/observer, создавая ложное впечатление «замерло» — 3 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md#УРОКИ ФАБРИКЕ, строки 63–65
- buffon/ZAHOD-02.md#ОТЧЁТ, строка 93
- buffon/ZAHOD-02.md#ОТЧЁТ, строка 108

## 24. Заход рассчитан на инструмент спавна субагентов, которого в среде исполнителя нет — 3 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md#УРОКИ ФАБРИКЕ, строки 58–60
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md#УРОКИ ФАБРИКЕ, строки 90–91
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md#ОТЧЁТ, строка 227

## 25. Грep по подстроке засчитывает случайные вхождения внутри других слов — 3 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 323–332
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 349–364
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#ОТЧЁТ, строки 210–212

## 26. Предпосылка о содержании источника (книга/канон) оказалась ложной при прямой проверке — 2 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md#ВОПРОСЫ, строка 175
- _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md#ЗАДАНИЕ, строки 32–33

## 27. Счётчик/парсер ломается на конкретной форме текста (регистр, синтаксис), которую не предусмотрели — 2 вхожд.
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ПЛАН, строки 118–121
- kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md#ВОПРОСЫ, строка 137

## 28. Место/формат, который заход требует использовать, нигде не зафиксирован явно — 2 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md#ПЛАН, строка 76
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 212

## 29. Исполнитель/аналитик придумал решение вместо того, чтобы свериться с решением владельца — 2 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 210
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md#ЗАДАНИЕ, строки 49–50

## 30. Инструмент/счётчик физически недоступен из окружения агента — 2 вхожд.
- kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_L4-html-v4.md#ОТЧЁТ, строка 153
- kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md#ВОПРОСЫ, строка 107

## 31. Скачанный источник оказался неполным или не тем изданием — 2 вхожд.
- _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md#ОТЧЁТ, строка 72
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md#ВОПРОСЫ, строка 117

## 32. Свежий верификатор/скрипт-проверка сам содержит баг, дающий ложный красный — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ОТЧЁТ, строки 231–232
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#ОТЧЁТ, строки 231–232

## 33. Regex с кириллицей матчится по-разному на разных платформах (BSD/macOS) — молчаливый пустой результат — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md#УРОКИ ФАБРИКЕ, строки 105–106
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 164–168

## 34. Аналитик писал адреса/факты по вторичному источнику (отчёту предыдущего захода), а не по живому файлу — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 117–120
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 179–182

## 35. Гейт/фикстура физически проверяет не тот путь/не ту область, что заявлено — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md#ЗАДАНИЕ, строка 57
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ПЛАН, строки 118–119

## 36. Перепаковка контента на сцены/абзацы сбивает нумерацию или ломает якорь — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md#УРОКИ ФАБРИКЕ, строки 60–62
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md#УРОКИ ФАБРИКЕ, строки 90–92

## 37. Инструмент приёмки/скрипт написан под один формат ПЛАНа/отчёта, а реальный не совпадает — 2 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#УРОКИ ФАБРИКЕ, строки 162–166
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 65–68

## 38. Поле/род/якорь, на который ссылается заход или гейт, не существует в актуальной схеме — 2 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md#ВОПРОСЫ, строка 110
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 103–105

## 39. Защитная мера (страховка результата в файл) появилась в тексте захода только после первого падения — до неё были потери — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ, строки 78–80
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 87–90

## 40. Правило «зона = папка целиком» ломается, когда в той же папке пишет ещё и аналитик — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ, строки 82–84
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 91–94

## 41. Обязательный пункт критерия стоит последним по приоритету — недобор по построению — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ, строки 86–88
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 95–100

## 42. Мёртвая URL-ссылка в реестре источников теряет источник молча — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ, строки 68–69
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 47–50

## 43. Требование дословного цитирования у каждой строки конфликтует с ограничением на объём цитирования — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 67–69
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 61–64

## 44. Гейт долга не покрывает целую категорию источников (например, `web/`) — 2 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 75–77
- _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 69–72

## 45. Аналитик придумывает мотивацию/аргумент вместо чтения готового материала в картотеке — придуманное потом отвергается — 2 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md#ЗАДАНИЕ, строки 45–58
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#ЗАДАНИЕ, строка 57

## 46. Визуальные/логические баги дожили необнаруженными до реальной живой лекции — 2 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строки 9–10
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#ЗАДАНИЕ, строки 99–102

## 47. model-mismatch-cost — 1 вхожд.
- kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md#ВОПРОСЫ, строка 60

## 48. scene-verbatim-review-not-live — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 215

## 49. model-contract-mismatch-between-docs — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md#ОТЧЁТ, строка 142

## 50. count-discrepancy-generic — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 95–97

## 51. template-registry-out-of-sync — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md#ЗАДАНИЕ, строки 8–14

## 52. orphaned-artifact-after-rename — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#УРОКИ ФАБРИКЕ, строки 166–170

## 53. Инструкция владельца не попала в канон или была проигнорирована повторно — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 85–88

## 54. Отрицательный вывод построен по слишком крупной единице источника (оглавление) и оказался ложным — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#УРОКИ ФАБРИКЕ, строки 154–158

## 55. Дата, продиктованная в тексте захода, разошлась с реальной датой исполнения — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md#УРОКИ ФАБРИКЕ, строки 94–96

## 56. Служебный разделитель машинного формата совпал с символом внутри содержимого и сломал разбор — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 107–109

## 57. Субагент вернул выводы из аннотации/пересказа вместо прямого чтения текста источника — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md#УРОКИ ФАБРИКЕ, строки 210–214

## 58. Заявленный охват («N из M») завышен относительно фактического — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#ПЛАН, строки 205–207

## 59. Дословная цитата владельца потеряна/заменена перефразировкой при консолидации — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md#ОТЧЁТ, строки 322–323

## 60. Гейт на общем/репо-глобальном файле красит коммиты в чужих, не касающихся зонах — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 280–295

## 61. Код возврата гейта не различает «есть дефект» и «неверный вызов/опечатка» — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 296–307

## 62. Гейт печатает охват только при красном вердикте — зелёный не даёт понять, что реально проверено — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 308–322

## 63. Файл-результат прошлого прогона неотличим от нового при повторном запуске той же командой — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 333–348

## 64. Контракт зоны предписывает переключение на ветку, которая физически не содержит нужного проекта — 1 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ, строки 62–63

## 65. Предупреждение о долге в шапке не снято, хотя долг уже закрыт другим заходом — 1 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 63–65

## 66. Ответ субагента приходит тихо обрезанным — не падением, а потерей без сигнала — 1 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 71–73

## 67. Честная текстовая приписка («не читал») механически глушит гейт, рассчитанный на другое — 1 вхожд.
- _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#УРОКИ ФАБРИКЕ, строки 79–81

## 68. Заход, получающий вывод аналитика как данность, структурно не может его оспорить — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 213–279

## 69. Авто-срабатывающий механизм (хук/функция) не имеет собственной записи в реестре id — 1 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md#ОТЧЁТ, строка 93

## 70. Запрещённый решением скилл всё ещё вызывается в живых файлах — 1 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md#ОТЧЁТ, строка 100

## 71. Значение поля подставлено «по смыслу» без проверки по живому источнику — 1 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md#ВОПРОСЫ, строка 95

## 72. Конвенция, изобретённая предыдущим заходом, оказалась вытеснена другим реальным каноном — 1 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md#ЗАДАНИЕ, строки 18–19

## 73. Значение поля записано в одной кодировке (англ. yes/no), а контракт требует другую (да/нет) — 1 вхожд.
- _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md#ВОПРОСЫ, строка 104

## 74. Чтение файла с вшитым base64-блоком раздувает контекст и обрезается инструментом — 1 вхожд.
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md#ОТЧЁТ, строки 172–178

## 75. Верификатор находит, что реализация верна, а описывающая её проза — нет — 1 вхожд.
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md#ОТЧЁТ, строки 209–215

## 76. Документ ссылается на плейсхолдеры/переменные, которых реальный код не знает — 1 вхожд.
- _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md#ПЛАН, строки 55–61

## 77. Гейт сверяет по слишком грубой/строгой гранулярности (полная строка вместо цитаты), ломаясь на легитимных форматах — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md#ОТЧЁТ, строка 143

## 78. Числовой порог гейта не учитывает жанровый профиль материала — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md#ОТЧЁТ, строка 145

## 79. Необязательный шаг ревью (свежий рецензент) пропущен — прошли ошибки, которые он бы поймал — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md#ОТЧЁТ, строка 146

## 80. Слайды/модели строились без заранее спланированной финальной структуры (роутер/список ретайра) — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 218

## 81. Источник даёт только частичный текст (определения), не полный материал слайда — 1 вхожд.
- _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md#ОТЧЁТ, строка 225

## 82. Счётчик по внешнему источнику разошёлся со старой картой/индексом — 1 вхожд.
- _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md#ОТЧЁТ, строка 88

## 83. Контракт зоны отдаёт файл исполнителю, а его параллельно и вживую правит аналитик — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md#ВОПРОСЫ, строка 115

## 84. Конфликт лицензии источника с коммерческим характером курса не решён — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md#ВОПРОСЫ, строка 173

## 85. Ранее проделанная работа (OCR и т.п.) обесценена появлением лучшего источника — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md#ОТЧЁТ, строки 256–266

## 86. Ресурс докачан/задублирован вне отслеживаемого процесса инвентаризации — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md#ВОПРОСЫ, строка 176

## 87. Повторное упоминание прецедента используется как довод не делегировать суждение субагенту — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md#ЗАДАНИЕ, строка 94

## 88. Карточка числится в одной лекции роутера, а по факту принадлежит другой — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md#ВОПРОСЫ, строка 173

## 89. Скрипт-гейт имеет слепое пятно для конкретного рода/типа карточки — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md#ОТЧЁТ, строка 215

## 90. Статус «частично» механически прочитан скриптом как «пройдено» — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md#ОТЧЁТ, строка 208

## 91. Критерий обещал снятие гейта, которое фактическая работа не обеспечила — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md#УРОКИ ФАБРИКЕ, строки 62–64

## 92. Аналитик исключил нужную папку из зоны и отправил искать материал, для которого эта папка — единственный дом — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md#ЗАДАНИЕ, строки 7–9

## 93. Буквальное прочтение критерия объявило бы дефектным заведомо здоровый материал — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md#ВОПРОСЫ, строка 178

## 94. Собственный верификатор-скрипт исполнителя содержит баг, дающий ложные срабатывания — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md#ОТЧЁТ, строка 295

## 95. OCR ломает нелатинские/специальные символы, из-за чего последующий греп по ним не находит ничего — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md#ЗАДАНИЕ, строка 27

## 96. Карточка/ссылка указывает неверное место в источнике (не тот раздел/страница) — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md#ОТЧЁТ, строка 192

## 97. Аналитик ссылается на файл как на живой источник, хотя тот уже удалён/влит в другой документ — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#ЗАДАНИЕ, строки 12–16

## 98. Аналитик держит в голове вывод, основанный на неверной ссылке карточки — 1 вхожд.
- _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#ЗАДАНИЕ, строка 64

## 99. Git-подмодуль висит как gitlink без записи в `.gitmodules` — 1 вхожд.
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md#ВОПРОСЫ, строка 238

## 100. Разметку/рендер движка нельзя проверить прямо из песочницы (нет визуального просмотра) — 1 вхожд.
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md#УРОКИ ФАБРИКЕ, строки 97–98

## 101. Гейт `check_view` даёт ложный красный на корректных markdown-ссылках — 1 вхожд.
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md#УРОКИ ФАБРИКЕ, строки 100–101

## 102. Заход строит обязательный гейт на неверном факте о содержимом предыдущего отчёта — 1 вхожд.
- _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md#ПЛАН, строки 111–119

## 103. Файл-реестр путей указывает неверный путь к тому, что он должен точно знать — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 99–101

## 104. Число, вписанное в шапку до завершения письма, устарело к моменту сдачи файла — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 111–113

## 105. Собственный отчёт о покрытии артефакта противоречит верной таблице рядом — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 115–117

## 106. Утверждение о безопасности/состоянии верно лишь для части заявленной области — 1 вхожд.
- _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ, строки 119–121

## 107. Пояснительный комментарий не обновлён после того, как код изменился — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md#ВОПРОСЫ, строка 131

## 108. Отрицательный вывод оперся на источник/папку, не относящуюся к предмету вывода — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#УРОКИ ФАБРИКЕ, строки 142–146

## 109. Независимая перепроверка находит отдельный класс пропусков, не покрытый исходным методом — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md#ОТЧЁТ, строки 419–420

## 110. Находка предыдущего верификатора не подтвердилась при новой проверке по живому файлу — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md#ПЛАН, строки 105–106

## 111. Заход путает номера утверждений в собственном тексте задания — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md#ПЛАН, строка 107

## 112. Движок рендера скрывает часть содержимого (хвост доказательства) при свёрнутом состоянии — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md#ЗАДАНИЕ, строка 6

## 113. Буквальное числовое требование критерия технически недостижимо из-за модели рендера (иная HTML-структура) — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md#ПЛАН, строка 73

## 114. Критерий владельца допускает два взаимоисключающих прочтения — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#ВОПРОСЫ, строка 136

## 115. Гейт читает формулу как обычный текст и не распознаёт код-спаны — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#УРОКИ ФАБРИКЕ, строки 98–102

## 116. Инструмент приёмки считает маркеры грепом без якоря начала строки — ловит случайные совпадения — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#УРОКИ ФАБРИКЕ, строки 104–108

## 117. Долг закрыт словами вместо содержательного вывода — закрытие оказалось ложным — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#УРОКИ ФАБРИКЕ, строки 138–142

## 118. Инструмент принимает один формат пути (папку), а контракт зоны требует другой (файл) — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#УРОКИ ФАБРИКЕ, строки 144–148

## 119. Счётчик в шапке документа считает сам себя, ломая собственный вывод — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#УРОКИ ФАБРИКЕ, строки 156–160

## 120. Два обязательных требования канона/контракта взаимно исключают друг друга — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md#ВОПРОСЫ, строка 223

## 121. Гейт и приёмщик оба ломаются на одном и том же классе — документ, цитирующий свой же служебный маркер — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 69–72

## 122. Критерий отбора появился в каноне уже ПОСЛЕ приёмки — исходное ТЗ его не содержало — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 73–76

## 123. Правило, записанное на ранней фазе арки, не дошло до более поздней фазы той же арки — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 77–80

## 124. Владелец трижды переформулировал различение, аналитик дважды скатился к прежней ошибке — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 81–84

## 125. Заход называет опорной папку, содержимое которой не относится к задаче — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 109–112

## 126. Правило уже записано в каноне, но дважды подряд не сработало на практике — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 113–116

## 127. Аналитик принимает работающий в моменте процесс за оборванный и выносит ложный вердикт «не принято» — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 125–128

## 128. Уроки, помеченные как «без цены», при проверке оказались с ценой — гейт судил оформление, не суть — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 129–132

## 129. Фикстуры гейта (нарочно содержащие то, что гейт должен ловить) блокируют весь репозиторий — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 137–140

## 130. Аналитик читает сбой окружения (rc, среда) как факт о самом предмете работы — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 141–144

## 131. Верификатор отчитывается находками, а не охватом — охват пришлось восстанавливать отдельно — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 169–173

## 132. CLI-флаг (`--help`) принят скриптом-скаффолдом за содержательное имя аргумента — 1 вхожд.
- _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 174–178

## 133. Заход поручает дополнить дайджест, уже полностью сделанный в тот же день — 1 вхожд.
- _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md#ВОПРОСЫ, строка 93

## 134. Валидатор id по regex-маске не распознаёт кириллические идентификаторы существующих узлов — 1 вхожд.
- _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md#ПЛАН, строка 73

## 135. Число в заголовке не совпадает ни с фактическим счётом, ни со сводным числом в другом документе — 1 вхожд.
- _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md#УРОКИ ФАБРИКЕ, строки 85–87

## 136. Путь коммита зоны рвётся на мелочах по нескольку раз за сессию — 1 вхожд.
- _studio/zhurnal/2026-07-23_vneshnie-istorii/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 42–48

## 137. Требование к верификатору по объёму равно полному повторению всей проверяемой стадии — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md#УРОКИ ФАБРИКЕ, строки 329–332

## 138. Файл исключён из чтения как «регенерируемый», хотя внутри него есть НЕ регенерируемая секция — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ, строки 208–210

## 139. Гейт «битых ссылок» ловит любой токен в обратных кавычках, а не только настоящий id — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ, строки 212–214

## 140. Секции канона, на которые ссылаются карточки, физически отсутствуют в файле — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md#ОТЧЁТ, строка 383

## 141. Заход предписывает голый git, который запрещён корневым каноном (велит `git_zona.py`) — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md#УРОКИ ФАБРИКЕ, строки 216–219

## 142. Классификационная ось предыдущего захода не переводится один-в-один в ось текущего — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#УРОКИ ФАБРИКЕ, строки 171–174

## 143. Критерий описывает источник через один синтаксис, тогда как часть материала оформлена иначе — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#УРОКИ ФАБРИКЕ, строки 176–179

## 144. Вердикт «на глаз/на ощущение» разошёлся с результатом точной счётной команды — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#ОТЧЁТ, строка 273

## 145. Гейт не отличает содержательную ссылку от простого упоминания той же строки в тексте — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ, строки 179–181

## 146. Гейт не учитывает, что в репозитории несколько экземпляров одноимённого канонического файла — 1 вхожд.
- _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ, строки 183–185

## 147. Два инструмента рендера (гейт и харнесс) используют разные браузеры и расходятся в поведении — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ, строки 253–262

## 148. Пометка о проверке («всё сверено») относится не ко всему документу, как заявлено — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ, строки 264–274

## 149. Рецепт визуальной проверки не переживает повторное применение — ломается по второму разу — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ, строки 276–289

## 150. Диагностика гейтов написана по памяти об инциденте, а не по живому скану — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#УРОКИ ФАБРИКЕ, строки 100–103

## 151. Критерий готовности требует зелёного результата именно там, где заведомо есть настоящий долг — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#УРОКИ ФАБРИКЕ, строки 105–108

## 152. Гейт даёт структурно неустранимое ложное срабатывание на конкретном классе слайдов — 1 вхожд.
- _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ВОПРОСЫ, строки 178–179

---

## Разное — не сведено к общему механизму (кратность 1 каждое, всего 131)

Каждая запись ниже — самостоятельное наблюдение без найденного повтора в остальном корпусе на момент сборки этой сводки. Кратность 1 — законный результат, не брак пробы.

- **Ни заход, ни прочитанные DOK не называют, куда физически кладётся папка `<лекция>/`** — _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md#ВОПРОСЫ, строка 102
- **Точка отката уже существовала («создана в предыдущей частичной попытке этого захода»), пере-коммитить было нечего** — _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md#ПЛАН, строка 78
- **Путь к трекеру в тексте самого захода был бы битой ссылкой, если брать буквально из места, где живёт `ARKA.md`; исполнитель вычислил прав...** — _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md#ПЛАН, строка 80
- **Команда `rm` по glob-маске `.pyc` молча не сработала из-за zsh-nomatch — недоудаление тестовой арки заметили только по повторному grep-сч...** — _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md#ОТЧЁТ, строка 115
- **Повторное упоминание прецедента с субагентом, приписавшим Пирсу категории запятой по одному совпадению грепа — довод не делегировать выбо...** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md#ЗАДАНИЕ, строка 113
- **Вердикт «дыр не найдено» прошлой арки на деле означал охват 2 лекций из 9, но читался как проверка всех девяти** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md#ЗАДАНИЕ, строка 100
- **Грep=0 по PDF-корпусу принят за доказательство отсутствия — записано «у Ловера NNO нет», хотя предмет есть в Part III** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md#ЗАДАНИЕ, строка 46
- **Параллельный запуск двух заходов в одной зоне/ветке уже приводил к тому, что авто-коммит одной зоны утаскивал файлы другой** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md#ЗАДАНИЕ, строки 6–8
- **Шапка VYCHITANO.md заявляла «Статус: ПУСТОЙ (2026-07-16)» при десятке реально записанных дайджестов внутри файла** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md#ОТЧЁТ, строка 319
- **SPEKA §Опоры зала утверждала, что курс Nottingham «держится на Haskell» — греп по всем 4 конспектам дал 0 вхождений слова Haskell** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md#ОТЧЁТ, строки 269–272
- **STANDART-uzla.md перечисляет роды карточек без «находка», но в KARTA-OBLASTI.md уже есть карточки под родом «находка» — исполнитель вынуж...** — _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-topos.md#ВОПРОСЫ, строка 117
- **KARTA-OBLASTI.md содержал лишний третий фенс, из-за чего парность разъезжалась для всей второй половины файла** — _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md#ОТЧЁТ, строки 267–268
- **1. Контракт зоны предписал `git checkout main`, но проект живёт на `teorkat-istochniki`** — _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 39–42
- **7. Ответы субагентов приходят ОБРЕЗАННЫМИ — это не падение, а тихая потеря** — _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 65–68
- **9. Честная приписка «этот файл я НЕ читал» ЗАГЛУШАЕТ механический гейт** — _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 73–76
- **Исполнитель не видит статус живого субагента, мерил время суммой sleep вместо стенных часов и отступил слишком рано** — _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md#УРОКИ ФАБРИКЕ, строки 115–117
- **Критерий «непомеченных утверждений — ноль» не различает математические и педагогические оценки** — _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md#УРОКИ ФАБРИКЕ, строки 119–120
- **Некоммиченный вал ~109 позиций по шести проектам разом скопился на ветке, названной под другую задачу** — _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md#ЗАДАНИЕ, строка 15
- **Обязательный раздел §E, который критерий предыдущего захода объявлял условием принятия файла, не был поставлен вовсе, и это не поймано в ...** — _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md#ОТЧЁТ, строки 155–181
- **Стандарт «отрицательный вердикт несёт охват в себе» не защищает от того, что сам охват усечён процессной ошибкой** — _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md#ОТЧЁТ, строки 311–316
- **Внесение нового определения создало прямое противоречие со старой строкой «не-говорим» поля П8, которую задача не разрешала исполнителю т...** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md#ВОПРОСЫ, строки 129–130
- **`commit` без явных путей после `--` забрал в один коммит чужие незавершённые файлы** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#ЗАДАНИЕ, строка 144
- **Заход вписал в документ производный факт (адреса вхождений) руками, в том же абзаце, где предупреждает не делать так** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#УРОКИ ФАБРИКЕ, строки 157–163
- **Критерий готовности жёстко привязан к месту в документе, которое то же задание разрешает переносить** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md#УРОКИ ФАБРИКЕ, строки 165–171
- **Кириллические символьные классы в regex матчатся побайтово на BSD-инструментах и дают пустой матч при rc=0** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md#ЗАДАНИЕ, строка 32
- **Пропуск add и коммит без явных путей после `--` — те же два git-инцидента 21.07** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md#ЗАДАНИЕ, строки 70–72
- **Грепом по подстроке «тривиально»/«условно» ловится «нетривиально»/«безусловно» — уже случалось дважды** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md#ЗАДАНИЕ, строка 42
- **Критерий готовности предписывает вызов гейта в форме, которая печатает красный на здоровом документе** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md#УРОКИ ФАБРИКЕ, строки 168–170
- **Два из пяти предписанных действий в задании адресованы в места, которых в живом файле нет** — _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md#УРОКИ ФАБРИКЕ, строки 172–174
- **Инструмент приёмки сам напечатал зелёное на упавшей проверке** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 61–64
- **«Оглавление, прочитанное глазами» назначено достаточной опорой отрицательного вывода — а оно бывает слишком крупным** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 89–92
- **🔴 Диагноз аналитика «гейт штрафует за чужой долг» оказался ЛОЖНЫМ — виноват был не гейт, а грязный индекс** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 93–96
- **Критерий готовности предписывал вызов гейта в форме, которая печатает КРАСНЫЙ на здоровом документе** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 121–124
- **Заход вписал производный факт руками — в том самом абзаце, где предупреждает, что так делать нельзя** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 149–153
- **Критерий готовности привязан к МЕСТУ, которое задание сам же разрешает изменить** — _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 154–158
- **Опубликованная в шапке выхода счётная команда стала находить собственные заголовки в своём же тексте после публикации и давала неверный р...** — _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md#ОТЧЁТ, строки 275–276
- **render.py снимал слайды в несуществующей сцене .scene-99 — пачечный рендер показывал пустую доску** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ, строки 240–251
- **G13/G15 краснели на деке, уже достигшем цели H6 (сцены порождаются сборкой, в src их нет)** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 225
- **G15 требовал каскад CSS под data-scene-until, которого движку не нужно** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 226
- **G12 был слеп ровно к перегруженной обложке Паскаля, ради которой заведён — content/sl-title.md был 1 байт** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 228
- **Счёт слов G12 считал разделители (—, ·, …) словами, давая ±3 слова у порога 25** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 229
- **G7 рвался на здоровой ленте Паскаля пятью независимыми способами** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 230
- **`}` внутри TeX ломал разбор шорткатов {blur@…}, sostoyanie.py не повторял приём build_deck.py** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 231
- **Диапазонные маркеры {@5-8} и {@-6} читались неверно — {@-6} не виделся вовсе** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 232
- **G7=N/A не влияет на код возврата — хук, судящий по exit code, пропустит дек без шага 6** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 237
- **H6 считает все .scene-N без различения сгенерированного блока — цель «ноль совпадений» станет недостижимой** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md#ОТЧЁТ, строка 239
- **Служебные слайды верстались руками в каждом деке, правки владельца следующей большой правкой возвращались обратно** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ЗАДАНИЕ, строка 8
- **Гейт render-identity не может ни провалиться, ни пройти — недетерминирован даже при сверке файла с самим собой** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ, строки 113–115
- **Реестр гейтов объявил поблажку G7 закрытой, а в коде sostoyanie.py она не реализована** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ, строки 117–119
- **Параллельный коммит аналитика в 02:23 подмёл три правленых файла исполнителя под чужое сообщение** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ, строки 121–123
- **Новый структурный G12 пропустил перегрузку обложки через санкционированные поля brief.md** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ, строки 125–127
- **Действующий (до правки) G12 счётом слов не ловил уже перегруженную обложку Паскаля, ради которой заведён заход** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ПЛАН, строка 135
- **Канонный финал с вертикальной иллюстрацией уезжал за нижний край холста** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ОТЧЁТ, строки 257–258
- **Плейсхолдер {{ SLIDES }} с пробелами не распознавался — порождение молча выключалось, дек собирался пустым** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md#ОТЧЁТ, строка 269
- **1. Обсуждали как нерешённые две задачи, которые уже стояли решёнными в собственном тексте проекта** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 39–43
- **2. Вписал в собственный документ число, которое не сходится с его же таблицей** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 44–48
- **3. Проектировал габарит нового артефакта на глаз, имея живой эталон в том же репозитории** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 49–53
- **4. Считал снятие блюра отдельной сценой** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 54–58
- **5. Три конкурирующие мотивации к одному факту выдавались за богатство выбора** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 59–66
- **6. Габарит артефакта сверили с эталоном по ЧИСЛУ сцен, а не по плотности содержания** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 67–71
- **8. Каскады сцен в CSS выписаны руками и обрывались на `.scene-5`** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 77–81
- **9. Карта разворачивания классов в рецепте визуального гейта была неполной** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 82–86
- **10. `cairosvg` масштабирует по атрибуту `width` и игнорирует пропорции `viewBox`** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 87–91
- **11. Маркер сцены `{@N}` не работает внутри пункта списка** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 92–96
- **12. Жёсткая спека + эталонный SVG + обязательный «посмотри PNG» позволили распараллелить рисование на четырёх агентов** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 97–101
- **13. У дек-движка кэш KaTeX статический: новая формула валит сборку линтером** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 102–106
- **14. У Cowork нет браузера, и визуальная доводка ушла кругами через владельца** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 107–111
- **17. Гейт render-identity не может ни провалиться, ни пройти, а на него ссылаются критерии заходов и слой 2 гейта G11** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 122–126
- **20. Перенос величины из рукописного места в порождаемое не отменяет гейт, а меняет ему адрес** — _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 137–140
- **git checkout в общей папке молча откатил дерево — файл откатился ночью, поймал владелец вручную** — _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ЗАДАНИЕ, строка 10
- **Карта кусков называет домом математики восемь карточек, которых в картотеке физически нет** — _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ, строки 67–68
- **Юникодные подстрочные индексы (U+208B) в SVG-метке молча не рисуются в шрифте вида** — _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ, строки 70–71
- **Заход требует «~10 вкладок», а движок делает вкладку отдельным файлом — конфликт с зоной в один файл** — _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ, строки 73–74
- **Три определения (ретракт/сечение, группоид, скелет) отсутствуют и в маткостяке, и в картотеке** — _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md#ВОПРОСЫ, строки 102–103
- **1. Скаффолд `bootstrap_arka.py` создаёт NAVIGATOR/PLAN/TZ заглушками, и наличие файлов выглядит как закрытый Ф0** — _studio/zhurnal/2026-07-28_teksty-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 39–42
- **2. Для математического содержания у фабрики нет ни одного гейта, и правдоподобная проза проходит как работа** — _studio/zhurnal/2026-07-28_teksty-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 43–46
- **3. Аналитик трижды за сессию отложил сильный материал ради слабого, и каждый раз по методической причине** — _studio/zhurnal/2026-07-28_teksty-l1/UROKI-FABRIKE.md#УРОКИ ФАБРИКЕ, строки 47–82
- **`bootstrap_arka.py` принял флаг `--help` за имя арки и сфабриковал папку-сироту, которая ушла в git-план** — _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ЗАДАНИЕ, строки 6, 42
- **Пометка «удалить» в HANDOFF не удалила дубль `ZAPROS-fable-2-vneshnie.md` — заметка не механизм** — _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ЗАДАНИЕ, строки 6, 42
- **Задание содержало ложную цену: утверждало, что дубль «пролежал неделю» после пометки к удалению — проверка по mtime и HANDOFF показала то...** — _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ЗАДАНИЕ, строка 42; #ОТЧЁТ, строка 125
- **Триггер фикстуры (поднимается хуком) уже, чем защита, которую она проверяет** — _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md#ОТЧЁТ, строки 122–123
- **Запуск `git_zona.py` не из корня репозитория падал без диагностики** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 37
- **Инлайн `#`-комментарий в команде ломался в zsh владельца, уходя в argv** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 38
- **`commit` без предварительного `plan` не был очевиден как двухшаговый процесс** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 39
- **Заглушка `== <переписать>` в `.commit-plan` требовала ручной правки, о которой владелец не знал, а вписывать её должен был другой писатель** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строка 40
- **Урок о поломке коммитов выжил только потому, что был вшит в конкретный файл-заход** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ЗАДАНИЕ, строки 57–59
- **Новый файл `INCIDENTY.md` требует регистрации в KARTA §6, но регистрация вне зоны исполнителя — оставлена как открытый вопрос** — _studio/zhurnal/_INFRA-git/kod_commit-ux.md#ВОПРОСЫ, строка 130
- **За четыре сессии ~15 поломок сведены к одному повторяющемуся классу: лекарством была проза (заметка/канон/урок), которая не переносится н...** — _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 6
- **Фикстура `git_zona` поднимается хуком только при правке `git_zona.py`, на правку `bootstrap_*` не срабатывает — триггер уже охвата защиты** — _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 6
- **Гейт с ложными срабатываниями блокирует здоровые коммиты всем троим писателям — паттерн «сейф-код стал опасностью»** — _studio/zhurnal/_INFRA-git/kod_tool-contract.md#ЗАДАНИЕ, строка 7
- **Сервер-хелпер превью не имеет TCC-доступа к `~/Documents/GitHub/...` — файл пришлось копировать в домашнюю папку для рендера** — buffon/ZAHOD-02.md#ОТЧЁТ, строка 92
- **Заявленный в ЗАХОД-01 (и повторённый в WORKLIST §7 как «✔ опровергнут замером») факт «окружность и многоугольники — одинаковый шаг ~4.1 п...** — buffon/ZAHOD-04.md#ВОПРОСЫ, пункт 1 (строки 153, 171)
- **SPISOK-skachat.md назвал файл, которого на сайте-источнике не существует (seminar8_catalan.pdf)** — catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md#ОТЧЁТ, строки 99–106
- **В базе (карте) была неточная библиографическая ссылка — arXiv-номер Diaconis–Hicks не соответствовал факту** — catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md#ОТЧЁТ, строка 72
- **PDF Пака оказался старым OCR-сканом 1994 года — текстовый слой местами искажён** — catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md#ОТЧЁТ, строка 66
- **Заход прямо ссылается на прошлый инцидент с «роем» субагентов как причину запрета субагентов** — catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md#ЗАДАНИЕ, строка 5
- **Живой рендер в браузере не прогнан — песочница не имеет доступа к внешним CDN (KaTeX, Google Fonts)** — catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md#ОТЧЁТ, строка 138
- **Дисциплина VYCHITANO.md заведена именно для того, чтобы прекратить повторяющееся перечитывание одних и тех же PDF по кругу** — catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md#ЗАДАНИЕ, строка 6
- **Дайджесты двух источников (Selig-Zhu, Bender-Williamson), собранные субагентами, не попали в VYCHITANO.md при первом проходе** — catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md#ОТЧЁТ, строки 90–93
- **Токены и время не залогированы — дана только оценка «на глаз» вместо измерения** — catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_illustracii-build-doc.md#ОТЧЁТ, строки 139–141
- **Скролл-транспорт preview-пейна браузера оказался нестабилен — скриншот не ловил проскролленное состояние** — catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md#ОТЧЁТ, строки 180–181
- **Объём правки (+215/−27 строк) превысил заявленный в заходе стоп-порог ~150 строк — исполнитель не остановился и не задал вопрос, продолжи...** — catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md#ОТЧЁТ, строки 186–188
- **Research-субагенты сами породили под-агентов трёх уровней вложенности** — kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md#ОТЧЁТ, строка 192
- **Прошлый («v1») судья вынес вердикт «фейков нет», но веб-ресёрч следующего прохода нашёл минимум 6 фактических ошибок в том же материале** — kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md#ОТЧЁТ, строки 156–160
- **Квота ТЗ «45/45» (мин. математики / мин. научпопа на лекцию) на практике вышла ~35/50–55, а не 45/45** — kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md#ВОПРОСЫ, строка 148
- **Харнесс не отдаёт точные счётчики токенов основного цикла — время/токены по фазам даны приближённо** — kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md#ОТЧЁТ, строка 180
- **Заход открывается указанием на перерасход бюджета в прошлый раз, отсюда явный запрет вложенной делегации субагентов в этом заходе** — kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_html-v3.md#ЗАДАНИЕ, строка 6
- **Правило реконсиляции TRIAGE↔DEEPEN не прописано — DEEPEN сам себе противоречил на Шенноне** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ВОПРОСЫ, строка 101
- **DEEPEN-субагент схлопывает scorecard в неплоскую форму без CLI --json-schema** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ОТЧЁТ, строки 142–144
- **GATHER-Haiku вернул невалидные типы (риск §10.2 материализовался) — 3 из 6 сырых scorecard невалидны** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md#ОТЧЁТ, строка 137
- **w1 GATHER: 12 из 74 черновых scorecard схемно невалидны (штатный haiku-брак)** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 76
- **w4 ASSEMBLE (Opus-ядро) ложно отчитался «0 подозрительных», хотя было 3 завышения Pugh — поймано только tripwire-судьёй** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md#ОТЧЁТ, строка 79
- **Субагент Ф3-b4 промахнулся индексами и задвоил Хэмминга — потребовалась пере-сшивка по name-match** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md#ОТЧЁТ, строка 89
- **Headless claude -p не аутентифицирован (401) — прогон «прошёл» все 5 волн за секунды без единого артефакта** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md#ОТЧЁТ, строки 73–87
- **Оркестратор молча считает пустой/ошибочный вывод claude -p успехом — нет guard на 401/пустой артефакт** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md#ВОПРОСЫ, строки 60–61
- **orchestrate.sh падает мгновенно на ветке `all` — bash `set -u`, необъявленная переменная w1 на строке 56** — kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md#ОТЧЁТ, строки 73–79
- **Заход ориентировался на «8» честных флагов, по факту в старте лекции их было 9** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md#ОТЧЁТ, строка 108
- **Общий генераторный баг: узкая таблица _CMD пропускает сырой LaTeX на экран во всех лекциях** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ЗАДАНИЕ, строка 9
- **Правило \in→∈ частично матчило начало \int, тихо подменяя интеграл на неверный символ** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ОТЧЁТ, строка 147
- **Общий генераторный баг: fields_of() не останавливался перед строкой-сноской «> поле:…», честные флаги рендерились дважды** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ЗАДАНИЕ, строки 10–11
- **Собственный критерий приёмки захода (grep-паттерн) технически ловит не то, что заявлено** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ПЛАН, строка 116
- **При закрытии критерия найдены ещё 2 артефакта того же класса («бэкслеш на экране»), уже присутствовавшие в бэкапе до этой сессии, вне дву...** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md#ОТЧЁТ, строки 165–166
- **Ожидание захода «2 моно-плейсхолдера портретов» не подтвердилось фактом — вышел только 1** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md#ОТЧЁТ, строка 180
- **Общий расход токенов по сессии не инструментирован, точная цифра из захода недоступна** — kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md#ОТЧЁТ, строка 158
- **Фан-аут 7 субагентов Sonnet рекурсивно расплодился в 50+ вложенных агентов** — kurs leto 2026/zhurnal/2026-07-01_struktura-i-svyazi/kod_usilenie-svyazey.md#ОТЧЁТ, строки 116–118
- **Два CANON-дока никогда не были зарегистрированы в NAVIGATION.md** — kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md#ОТЧЁТ, строки 110–112 (см. также #ВОПРОСЫ, строки 92–93)
- **Папка snapshots/ существует, но не описана в «Карте папок» NAVIGATION.md** — kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md#ОТЧЁТ, строки 116–117 (см. также #ВОПРОСЫ, строка 94)
- **Независимый верификатор дал 4 ложных срабатывания «битая ссылка»** — kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md#ОТЧЁТ, строка 143
- **Headless Chrome на машине держит жёсткий пол ширины окна ≈500px, игнорируя --window-size** — kurs leto 2026/zhurnal/2026-07-09_sayt-rasshirenie/kod_ekran2.md#ОТЧЁТ, строка 114
- **Renumber порядок в istochnik/ осиротил собранный HTML и разбросал стале-номера «ЛN» по прозе другой лекции** — kurs leto 2026/zhurnal/kod_uborka-renumber.md#ЗАДАНИЕ, строка 5
- **beklog.md ссылается на удалённый _out/L2-optimizaciya.html — check_docs.py упал, ссылку не починили** — kurs leto 2026/zhurnal/kod_uborka-renumber.md#ВОПРОСЫ, строка 84

---

**Сверка:** сумма вхождений по группам (330) + разное (131) = **461**. Число записей корпуса = **461**. Совпадает.