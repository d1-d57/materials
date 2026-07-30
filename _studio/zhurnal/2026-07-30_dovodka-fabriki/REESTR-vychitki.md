# REESTR-vychitki — след чтения (кто/когда/с каким хэшем)

Единица строки — СЕКЦИЯ одного файла, не файл целиком (Р50). Хэш — `git hash-object <файл>` из корня репо; самоинвалидируется, если файл дописали после пометки. Проверка — `python3 check_vychitka.py` (rc=0 при нулевом расхождении).

Нет секции в файле → строки о ней нет (не пишем 0 про несуществующую секцию). `кандидатов найдено = 0` — законный результат (секция прочитана и пуста), отличается от «не читал» самим фактом строки.

Исключены из охвата (READ-ONLY, уже прочитаны или запрещены к чтению отдельным пунктом захода — см. `## ПЛАН`):
- 20 файлов `_studio/zhurnal/2026-07-28_konspekt-l1/*.md` — прочитаны закрытием арки `konspekt-l1`.
- 3 файла `_studio/zhurnal/2026-07-30_dovodka-fabriki/{kod_etalon-dif,kod_gejty-lint,kod_vychitka}.md` — сегодняшние, аналитик их знает.
- `_studio/zhurnal/2026-07-30_dovodka-l1/kod_opros.md` — арка меняется параллельно, заход прямо запрещает трогать даже на чтение.
- `teorkat-vvedenie/kod_check-speka.md` — та же причина, папка названа отдельно.

(20+3+1+1 = 25 исключений всего; критерий готовности п.1 в заходе называет только первые 23 — расхождение на 2 файла объяснено выше и в `## ВОПРОСЫ` захода.)

| путь | секция | строк в секции | хэш блоба | кандидатов найдено | дата чтения |
|---|---|---|---|---|---|
| _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md | ЗАДАНИЕ | 72 | 0029ded17fd81267bebc13ed89c4e4e17a2f122c | 5 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md | ПЛАН | 20 | 0029ded17fd81267bebc13ed89c4e4e17a2f122c | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md | ВОПРОСЫ | 3 | 0029ded17fd81267bebc13ed89c4e4e17a2f122c | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md | ОТЧЁТ | 31 | 0029ded17fd81267bebc13ed89c4e4e17a2f122c | 1 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_bootstrap-guard.md | УРОКИ ФАБРИКЕ | 6 | 0029ded17fd81267bebc13ed89c4e4e17a2f122c | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_commit-ux.md | ЗАДАНИЕ | 104 | ca04425f1f4e6ca13cfef386217e94f50460eac6 | 10 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_commit-ux.md | ПЛАН | 17 | ca04425f1f4e6ca13cfef386217e94f50460eac6 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_commit-ux.md | ВОПРОСЫ | 5 | ca04425f1f4e6ca13cfef386217e94f50460eac6 | 1 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_commit-ux.md | ОТЧЁТ | 33 | ca04425f1f4e6ca13cfef386217e94f50460eac6 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_commit-ux.md | УРОКИ ФАБРИКЕ | 6 | ca04425f1f4e6ca13cfef386217e94f50460eac6 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md | ЗАДАНИЕ | 73 | 2a76053dac4bc74e2f92ffbbfbae2d54e16403e8 | 1 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md | ПЛАН | 13 | 2a76053dac4bc74e2f92ffbbfbae2d54e16403e8 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md | ВОПРОСЫ | 8 | 2a76053dac4bc74e2f92ffbbfbae2d54e16403e8 | 2 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md | ОТЧЁТ | 26 | 2a76053dac4bc74e2f92ffbbfbae2d54e16403e8 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_terminal-kanal.md | УРОКИ ФАБРИКЕ | 3 | 2a76053dac4bc74e2f92ffbbfbae2d54e16403e8 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_tool-contract.md | ЗАДАНИЕ | 86 | b10edaeee4f25584379b69b56880d7d339ca0747 | 7 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_tool-contract.md | ПЛАН | 2 | b10edaeee4f25584379b69b56880d7d339ca0747 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_tool-contract.md | ВОПРОСЫ | 2 | b10edaeee4f25584379b69b56880d7d339ca0747 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_tool-contract.md | ОТЧЁТ | 3 | b10edaeee4f25584379b69b56880d7d339ca0747 | 0 | 2026-07-30 |
| _studio/zhurnal/_INFRA-git/kod_tool-contract.md | УРОКИ ФАБРИКЕ | 6 | b10edaeee4f25584379b69b56880d7d339ca0747 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md | ЗАДАНИЕ | 80 | c80e885a9f3da88dfbd3049d3cb399d0204dff2f | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md | ПЛАН | 18 | c80e885a9f3da88dfbd3049d3cb399d0204dff2f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md | ВОПРОСЫ | 6 | c80e885a9f3da88dfbd3049d3cb399d0204dff2f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_bootstrap.md | ОТЧЁТ | 25 | c80e885a9f3da88dfbd3049d3cb399d0204dff2f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md | ЗАДАНИЕ | 75 | 0a97a789dbce5458fbfbac4d1a419f199a0b6325 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md | ПЛАН | 16 | 0a97a789dbce5458fbfbac4d1a419f199a0b6325 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md | ВОПРОСЫ | 6 | 0a97a789dbce5458fbfbac4d1a419f199a0b6325 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_gid.md | ОТЧЁТ | 30 | 0a97a789dbce5458fbfbac4d1a419f199a0b6325 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md | ЗАДАНИЕ | 64 | fb0badda3ddc07ebbc45cd1ab2663607ec78e9b2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md | ПЛАН | 13 | fb0badda3ddc07ebbc45cd1ab2663607ec78e9b2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md | ВОПРОСЫ | 3 | fb0badda3ddc07ebbc45cd1ab2663607ec78e9b2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_katalog.md | ОТЧЁТ | 23 | fb0badda3ddc07ebbc45cd1ab2663607ec78e9b2 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md | ЗАДАНИЕ | 71 | 2edd2cb02b97d7cf30cfbed461db85d2b6e2d3a3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md | ПЛАН | 20 | 2edd2cb02b97d7cf30cfbed461db85d2b6e2d3a3 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md | ВОПРОСЫ | 6 | 2edd2cb02b97d7cf30cfbed461db85d2b6e2d3a3 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_spina.md | ОТЧЁТ | 25 | 2edd2cb02b97d7cf30cfbed461db85d2b6e2d3a3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md | ЗАДАНИЕ | 74 | 73b0f7766600872115226e1991108fa37ca66a99 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md | ПЛАН | 25 | 73b0f7766600872115226e1991108fa37ca66a99 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md | ВОПРОСЫ | 15 | 73b0f7766600872115226e1991108fa37ca66a99 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_orkestracia/kod_treker.md | ОТЧЁТ | 26 | 73b0f7766600872115226e1991108fa37ca66a99 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-kursfabrika.md | ЗАДАНИЕ | 35 | d0adf7bf5d99aa9d9e985112b42accf69702056e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-kursfabrika.md | ПЛАН | 12 | d0adf7bf5d99aa9d9e985112b42accf69702056e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-kursfabrika.md | ВОПРОСЫ | 7 | d0adf7bf5d99aa9d9e985112b42accf69702056e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-kursfabrika.md | ОТЧЁТ | 15 | d0adf7bf5d99aa9d9e985112b42accf69702056e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md | ЗАДАНИЕ | 36 | a82ba3507e8c8c6879e5a7917534e0bbe3b8ee1f | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md | ПЛАН | 17 | a82ba3507e8c8c6879e5a7917534e0bbe3b8ee1f | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md | ВОПРОСЫ | 10 | a82ba3507e8c8c6879e5a7917534e0bbe3b8ee1f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_absorb-prizemlenie.md | ОТЧЁТ | 36 | a82ba3507e8c8c6879e5a7917534e0bbe3b8ee1f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md | ЗАДАНИЕ | 44 | f8053c22283e83e9031303d6b84e02abeeac44db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md | ПЛАН | 40 | f8053c22283e83e9031303d6b84e02abeeac44db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md | ВОПРОСЫ | 23 | f8053c22283e83e9031303d6b84e02abeeac44db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md | ОТЧЁТ | 108 | f8053c22283e83e9031303d6b84e02abeeac44db | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_doc-dvizhok.md | ЗАДАНИЕ | 53 | d347c12c533a7aa3cf495e13dea5f1a7bfabe77d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_doc-dvizhok.md | ПЛАН | 38 | d347c12c533a7aa3cf495e13dea5f1a7bfabe77d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_doc-dvizhok.md | ВОПРОСЫ | 11 | d347c12c533a7aa3cf495e13dea5f1a7bfabe77d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_doc-dvizhok.md | ОТЧЁТ | 23 | d347c12c533a7aa3cf495e13dea5f1a7bfabe77d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md | ЗАДАНИЕ | 60 | 3698ce74efe5a749fefddff83564a646debd832b | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md | ПЛАН | 16 | 3698ce74efe5a749fefddff83564a646debd832b | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md | ВОПРОСЫ | 12 | 3698ce74efe5a749fefddff83564a646debd832b | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md | ОТЧЁТ | 26 | 3698ce74efe5a749fefddff83564a646debd832b | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1.md | ЗАДАНИЕ | 44 | 05b09b27baf1714253b529274397a510fb14a74a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1.md | ПЛАН | 26 | 05b09b27baf1714253b529274397a510fb14a74a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1.md | ВОПРОСЫ | 22 | 05b09b27baf1714253b529274397a510fb14a74a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_faza1.md | ОТЧЁТ | 41 | 05b09b27baf1714253b529274397a510fb14a74a | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md | ЗАДАНИЕ | 41 | 39d55fecf79af075ecac3bfc51eaf84ada35b185 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md | ПЛАН | 77 | 39d55fecf79af075ecac3bfc51eaf84ada35b185 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md | ВОПРОСЫ | 17 | 39d55fecf79af075ecac3bfc51eaf84ada35b185 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-10_sborka-konvejera/kod_infra.md | ОТЧЁТ | 72 | 39d55fecf79af075ecac3bfc51eaf84ada35b185 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md | ЗАДАНИЕ | 89 | d42bed6c4b757ea823d145e3f8dbba8676dd13c8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md | ПЛАН | 22 | d42bed6c4b757ea823d145e3f8dbba8676dd13c8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md | ВОПРОСЫ | 10 | d42bed6c4b757ea823d145e3f8dbba8676dd13c8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_kurs-avtonom.md | ОТЧЁТ | 28 | d42bed6c4b757ea823d145e3f8dbba8676dd13c8 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-dobiv.md | ЗАДАНИЕ | 64 | 257eefd15599feb70fecd5960e6f05f988091dff | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-dobiv.md | ПЛАН | 2 | 257eefd15599feb70fecd5960e6f05f988091dff | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-dobiv.md | ВОПРОСЫ | 2 | 257eefd15599feb70fecd5960e6f05f988091dff | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-dobiv.md | ОТЧЁТ | 1 | 257eefd15599feb70fecd5960e6f05f988091dff | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md | ЗАДАНИЕ | 100 | 8ffdcda5df0ac6b057c95ca5d54795392d0450c9 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md | ПЛАН | 70 | 8ffdcda5df0ac6b057c95ca5d54795392d0450c9 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md | ВОПРОСЫ | 25 | 8ffdcda5df0ac6b057c95ca5d54795392d0450c9 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-modeli.md | ОТЧЁТ | 60 | 8ffdcda5df0ac6b057c95ca5d54795392d0450c9 | 8 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md | ЗАДАНИЕ | 72 | efa11e34ba8f48acd5f0ed80ce903d48a9e3b7f7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md | ПЛАН | 50 | efa11e34ba8f48acd5f0ed80ce903d48a9e3b7f7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md | ВОПРОСЫ | 7 | efa11e34ba8f48acd5f0ed80ce903d48a9e3b7f7 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_fibonacci-kurs/kod_lekcia1-pereverstka.md | ОТЧЁТ | 42 | efa11e34ba8f48acd5f0ed80ce903d48a9e3b7f7 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_geometria-6-nagliadnaya/kod_reserch-geometria.md | ЗАДАНИЕ | 58 | 6f8443a3fd8319085422dc6c52edacecfe62fb82 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_geometria-6-nagliadnaya/kod_reserch-geometria.md | ПЛАН | 21 | 6f8443a3fd8319085422dc6c52edacecfe62fb82 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_geometria-6-nagliadnaya/kod_reserch-geometria.md | ВОПРОСЫ | 7 | 6f8443a3fd8319085422dc6c52edacecfe62fb82 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_geometria-6-nagliadnaya/kod_reserch-geometria.md | ОТЧЁТ | 23 | 6f8443a3fd8319085422dc6c52edacecfe62fb82 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_informacia-i-kody/kod_skachivanie-istochnikov-L1.md | ЗАДАНИЕ | 40 | 1ad16147d7a597335b034ef033b1ec6ea5dc61a7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_informacia-i-kody/kod_skachivanie-istochnikov-L1.md | ПЛАН | 6 | 1ad16147d7a597335b034ef033b1ec6ea5dc61a7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_informacia-i-kody/kod_skachivanie-istochnikov-L1.md | ВОПРОСЫ | 2 | 1ad16147d7a597335b034ef033b1ec6ea5dc61a7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_informacia-i-kody/kod_skachivanie-istochnikov-L1.md | ОТЧЁТ | 22 | 1ad16147d7a597335b034ef033b1ec6ea5dc61a7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md | ЗАДАНИЕ | 43 | 85790ea2fa83987aef62f4abd125fb7c739a98ad | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md | ПЛАН | 17 | 85790ea2fa83987aef62f4abd125fb7c739a98ad | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md | ВОПРОСЫ (дубль-заголовок в источнике, объединено строки 61-64) | 4 | 85790ea2fa83987aef62f4abd125fb7c739a98ad | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-11_reserch-zadach/kod_zapusk-korpusa.md | ОТЧЁТ | 28 | 85790ea2fa83987aef62f4abd125fb7c739a98ad | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md | ЗАДАНИЕ | 91 | fe4470b2cd69342462ad702444c9ddd614ca850a | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md | ПЛАН | 21 | fe4470b2cd69342462ad702444c9ddd614ca850a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md | ВОПРОСЫ | 5 | fe4470b2cd69342462ad702444c9ddd614ca850a | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_riehl-lccc.md | ОТЧЁТ | 90 | fe4470b2cd69342462ad702444c9ddd614ca850a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md | ЗАДАНИЕ | 158 | ad813eec7025a539fc83cd1f9fee0e92713b79d2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md | ПЛАН | 12 | ad813eec7025a539fc83cd1f9fee0e92713b79d2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md | ВОПРОСЫ | 7 | ad813eec7025a539fc83cd1f9fee0e92713b79d2 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-landshaft/kod_vychitka-istochnikov.md | ОТЧЁТ | 106 | ad813eec7025a539fc83cd1f9fee0e92713b79d2 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md | ЗАДАНИЕ | 86 | d57a5085fa2158cd1742ae2c003306a71f298fe2 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md | ПЛАН | 13 | d57a5085fa2158cd1742ae2c003306a71f298fe2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md | ВОПРОСЫ | 5 | d57a5085fa2158cd1742ae2c003306a71f298fe2 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vhodyashchee.md | ОТЧЁТ | 61 | d57a5085fa2158cd1742ae2c003306a71f298fe2 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_biblioteka-vneshnyaya.md | ЗАДАНИЕ (весь файл — мёртвый заход-заглушка, других секций нет) | 9 | f8de988f3bafd703151afbc7d67d494ba99cd8d1 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md | ЗАДАНИЕ | 101 | fe867bcf80e49c2c30b6a20e6a9e7c9516f99654 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md | ПЛАН | 12 | fe867bcf80e49c2c30b6a20e6a9e7c9516f99654 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md | ВОПРОСЫ | 5 | fe867bcf80e49c2c30b6a20e6a9e7c9516f99654 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_chego-net.md | ОТЧЁТ | 27 | fe867bcf80e49c2c30b6a20e6a9e7c9516f99654 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md | ЗАДАНИЕ | 122 | 0b74cf1fd3154d15c8906a1482565527a4569fe5 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md | ПЛАН | 20 | 0b74cf1fd3154d15c8906a1482565527a4569fe5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md | ВОПРОСЫ | 8 | 0b74cf1fd3154d15c8906a1482565527a4569fe5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_dajdzhesty-i-mit.md | ОТЧЁТ | 55 | 0b74cf1fd3154d15c8906a1482565527a4569fe5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md | ЗАДАНИЕ | 153 | 236969ba48b5f23158bab24373f63ec3f91b3cd1 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md | УРОКИ ФАБРИКЕ | 10 | 236969ba48b5f23158bab24373f63ec3f91b3cd1 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md | ПЛАН | 30 | 236969ba48b5f23158bab24373f63ec3f91b3cd1 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md | ВОПРОСЫ | 2 | 236969ba48b5f23158bab24373f63ec3f91b3cd1 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_gejty-kursa.md | ОТЧЁТ | 43 | 236969ba48b5f23158bab24373f63ec3f91b3cd1 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md | ЗАДАНИЕ | 132 | 71ac21ac5fd02ead9371301229e5d4a8f4619d7e | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md | ПЛАН | 36 | 71ac21ac5fd02ead9371301229e5d4a8f4619d7e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md | ВОПРОСЫ | 12 | 71ac21ac5fd02ead9371301229e5d4a8f4619d7e | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_karta-lekciy-8.md | ОТЧЁТ | 43 | 71ac21ac5fd02ead9371301229e5d4a8f4619d7e | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md | ЗАДАНИЕ | 122 | f54774dc0047fd6e7cda724c8bc40ec5e0257c9c | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md | УРОКИ ФАБРИКЕ | 10 | f54774dc0047fd6e7cda724c8bc40ec5e0257c9c | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md | ПЛАН | 26 | f54774dc0047fd6e7cda724c8bc40ec5e0257c9c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md | ВОПРОСЫ | 7 | f54774dc0047fd6e7cda724c8bc40ec5e0257c9c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_khl-kontent.md | ОТЧЁТ | 31 | f54774dc0047fd6e7cda724c8bc40ec5e0257c9c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | ЗАДАНИЕ | 69 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | УРОКИ ФАБРИКЕ (первое вхождение) | 6 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | ПЛАН | 31 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | ВОПРОСЫ | 6 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | ОТЧЁТ | 18 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-kontent.md | УРОКИ ФАБРИКЕ (второе вхождение) | 3 | b0124cecf84a8f2b36492d103e7a3280eef33da7 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md | ЗАДАНИЕ | 70 | 3a9fa6f0a33f253cec88fa681bda200b7da1c7f8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md | УРОКИ ФАБРИКЕ | 10 | 3a9fa6f0a33f253cec88fa681bda200b7da1c7f8 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md | ПЛАН | 34 | 3a9fa6f0a33f253cec88fa681bda200b7da1c7f8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md | ВОПРОСЫ | 10 | 3a9fa6f0a33f253cec88fa681bda200b7da1c7f8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-programma.md | ОТЧЁТ | 23 | 3a9fa6f0a33f253cec88fa681bda200b7da1c7f8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md | ЗАДАНИЕ | 55 | caf6eb96755d5ab556f31b7fef2be59caaf4cdfe | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md | УРОКИ ФАБРИКЕ | 10 | caf6eb96755d5ab556f31b7fef2be59caaf4cdfe | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md | ПЛАН | 12 | caf6eb96755d5ab556f31b7fef2be59caaf4cdfe | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md | ВОПРОСЫ | 4 | caf6eb96755d5ab556f31b7fef2be59caaf4cdfe | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-l5-vlivanie.md | ОТЧЁТ | 18 | caf6eb96755d5ab556f31b7fef2be59caaf4cdfe | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md | ЗАДАНИЕ | 108 | 65e63b87ba3a79f3d3bf0d824eee49f02fd1345e | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md | ПЛАН | 23 | 65e63b87ba3a79f3d3bf0d824eee49f02fd1345e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md | ВОПРОСЫ | 6 | 65e63b87ba3a79f3d3bf0d824eee49f02fd1345e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_l4-motivaciya.md | ОТЧЁТ | 41 | 65e63b87ba3a79f3d3bf0d824eee49f02fd1345e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md | ЗАДАНИЕ | 109 | 7bd1e77071dca889ac3980e227d4b9eba15354ad | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md | ПЛАН | 66 | 7bd1e77071dca889ac3980e227d4b9eba15354ad | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md | ВОПРОСЫ | 12 | 7bd1e77071dca889ac3980e227d4b9eba15354ad | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_molchalivye-opory.md | ОТЧЁТ | 55 | 7bd1e77071dca889ac3980e227d4b9eba15354ad | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md | ЗАДАНИЕ | 116 | 37f336a1347df5dd0f84c2d8595adb12ca7f17e5 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md | ПЛАН | 25 | 37f336a1347df5dd0f84c2d8595adb12ca7f17e5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md | ВОПРОСЫ | 9 | 37f336a1347df5dd0f84c2d8595adb12ca7f17e5 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_motivacii-l1-l8-l9.md | ОТЧЁТ | 186 | 37f336a1347df5dd0f84c2d8595adb12ca7f17e5 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md | ЗАДАНИЕ | 105 | fc8eddbb09dce63d449d2c8ad1b86c1e024a3f1f | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md | ПЛАН | 39 | fc8eddbb09dce63d449d2c8ad1b86c1e024a3f1f | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md | ВОПРОСЫ | 15 | fc8eddbb09dce63d449d2c8ad1b86c1e024a3f1f | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_nno-i-shkolnye-opory.md | ОТЧЁТ | 153 | fc8eddbb09dce63d449d2c8ad1b86c1e024a3f1f | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md | ЗАДАНИЕ | 181 | 48a8c6e84193455a99f5f93ca17240116edc694a | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md | УРОКИ ФАБРИКЕ | 14 | 48a8c6e84193455a99f5f93ca17240116edc694a | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md | ПЛАН | 25 | 48a8c6e84193455a99f5f93ca17240116edc694a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md | ВОПРОСЫ | 7 | 48a8c6e84193455a99f5f93ca17240116edc694a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_shov-l4-l5.md | ОТЧЁТ | 58 | 48a8c6e84193455a99f5f93ca17240116edc694a | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md | ЗАДАНИЕ | 108 | b432364a70dd33edd2c6c47fad889b6cabd7f130 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md | ПЛАН | 31 | b432364a70dd33edd2c6c47fad889b6cabd7f130 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md | ВОПРОСЫ | 32 | b432364a70dd33edd2c6c47fad889b6cabd7f130 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_vneshnyaya-merka.md | ОТЧЁТ | 156 | b432364a70dd33edd2c6c47fad889b6cabd7f130 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-most.md | ЗАДАНИЕ | 91 | a8d91d29534592dabc456bb95f9c06dcd927f274 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-most.md | ПЛАН | 15 | a8d91d29534592dabc456bb95f9c06dcd927f274 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-most.md | ВОПРОСЫ | 6 | a8d91d29534592dabc456bb95f9c06dcd927f274 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-most.md | ОТЧЁТ | 80 | a8d91d29534592dabc456bb95f9c06dcd927f274 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-topos.md | ЗАДАНИЕ | 88 | 8d98ec460d1a3f5733949e15577ff63878d9044e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-topos.md | ПЛАН | 26 | 8d98ec460d1a3f5733949e15577ff63878d9044e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-topos.md | ВОПРОСЫ | 7 | 8d98ec460d1a3f5733949e15577ff63878d9044e | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/kod_zona-c-topos.md | ОТЧЁТ | 78 | 8d98ec460d1a3f5733949e15577ff63878d9044e | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md | ЗАДАНИЕ | 69 | f5b60b9a03421756d0612d30166e9445a295f626 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md | УРОКИ ФАБРИКЕ | 20 | f5b60b9a03421756d0612d30166e9445a295f626 | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md | ПЛАН | 24 | f5b60b9a03421756d0612d30166e9445a295f626 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md | ВОПРОСЫ | 7 | f5b60b9a03421756d0612d30166e9445a295f626 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_dobrat-vshir.md | ОТЧЁТ | 113 | f5b60b9a03421756d0612d30166e9445a295f626 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md | ЗАДАНИЕ | 57 | 92ecde994fbe1deb51edaa16dfc7233ab846a0d5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md | УРОКИ ФАБРИКЕ | 16 | 92ecde994fbe1deb51edaa16dfc7233ab846a0d5 | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md | ПЛАН | 30 | 92ecde994fbe1deb51edaa16dfc7233ab846a0d5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md | ВОПРОСЫ | 7 | 92ecde994fbe1deb51edaa16dfc7233ab846a0d5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_obogatit-vvedenie.md | ОТЧЁТ | 49 | 92ecde994fbe1deb51edaa16dfc7233ab846a0d5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md | ЗАДАНИЕ | 60 | a7e7ee72af7edd4a5f2bfad340dff8ac065bb2ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md | УРОКИ ФАБРИКЕ | 28 | a7e7ee72af7edd4a5f2bfad340dff8ac065bb2ae | 6 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md | ПЛАН | 36 | a7e7ee72af7edd4a5f2bfad340dff8ac065bb2ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md | ВОПРОСЫ | 7 | a7e7ee72af7edd4a5f2bfad340dff8ac065bb2ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/kod_poisk-primerov.md | ОТЧЁТ | 143 | a7e7ee72af7edd4a5f2bfad340dff8ac065bb2ae | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md | ЗАДАНИЕ | 105 | f760f8c272ff4b7823438b7ebb5a9ef7ec9f04db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md | УРОКИ ФАБРИКЕ | 16 | f760f8c272ff4b7823438b7ebb5a9ef7ec9f04db | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md | ПЛАН | 25 | f760f8c272ff4b7823438b7ebb5a9ef7ec9f04db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md | ВОПРОСЫ | 8 | f760f8c272ff4b7823438b7ebb5a9ef7ec9f04db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md | ОТЧЁТ | 72 | f760f8c272ff4b7823438b7ebb5a9ef7ec9f04db | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md | ЗАДАНИЕ | 114 | e9d0ea1758bfae38109ec089a5a37d5b35abcdc3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md | ПЛАН | 20 | e9d0ea1758bfae38109ec089a5a37d5b35abcdc3 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md | ВОПРОСЫ | 3 | e9d0ea1758bfae38109ec089a5a37d5b35abcdc3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md | ОТЧЁТ | 2 | e9d0ea1758bfae38109ec089a5a37d5b35abcdc3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_poisk-listkov.md | ЗАДАНИЕ | 71 | 80ed0320c0efc9993d11c7334866b72fae36f87d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_poisk-listkov.md | УРОКИ ФАБРИКЕ | 4 | 80ed0320c0efc9993d11c7334866b72fae36f87d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_poisk-listkov.md | ПЛАН | 2 | 80ed0320c0efc9993d11c7334866b72fae36f87d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_poisk-listkov.md | ВОПРОСЫ | 2 | 80ed0320c0efc9993d11c7334866b72fae36f87d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_poisk-listkov.md | ОТЧЁТ | 1 | 80ed0320c0efc9993d11c7334866b72fae36f87d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md | ЗАДАНИЕ | 109 | 426d95f628f8db8c6b3eb2ec9f7e4cb0711bb009 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md | ПЛАН | 126 | 426d95f628f8db8c6b3eb2ec9f7e4cb0711bb009 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md | ВОПРОСЫ | 7 | 426d95f628f8db8c6b3eb2ec9f7e4cb0711bb009 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md | ОТЧЁТ | 69 | 426d95f628f8db8c6b3eb2ec9f7e4cb0711bb009 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md | ЗАДАНИЕ | 94 | 8b8f141805562acc8943aa8a273d0c35c0d84546 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md | УРОКИ ФАБРИКЕ (дубль-заголовок в источнике, объединено) | 14 | 8b8f141805562acc8943aa8a273d0c35c0d84546 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md | ПЛАН | 27 | 8b8f141805562acc8943aa8a273d0c35c0d84546 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md | ВОПРОСЫ | 7 | 8b8f141805562acc8943aa8a273d0c35c0d84546 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md | ОТЧЁТ | 210 | 8b8f141805562acc8943aa8a273d0c35c0d84546 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md | ЗАДАНИЕ | 90 | 00b420dbcfced208959c541b20df3605044e60ca | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md | УРОКИ ФАБРИКЕ | 32 | 00b420dbcfced208959c541b20df3605044e60ca | 7 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md | ПЛАН | 55 | 00b420dbcfced208959c541b20df3605044e60ca | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md | ВОПРОСЫ | 9 | 00b420dbcfced208959c541b20df3605044e60ca | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-20_vvedenie-sborka/kod_nochnaya-karta-oblastej.md | ОТЧЁТ | 87 | 00b420dbcfced208959c541b20df3605044e60ca | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md | ЗАДАНИЕ | 56 | ca40048640313dc29718e4e1d654bcd0bd0bdfb5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md | УРОКИ ФАБРИКЕ | 11 | ca40048640313dc29718e4e1d654bcd0bd0bdfb5 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md | ПЛАН | 59 | ca40048640313dc29718e4e1d654bcd0bd0bdfb5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md | ВОПРОСЫ | 9 | ca40048640313dc29718e4e1d654bcd0bd0bdfb5 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-b.md | ОТЧЁТ | 123 | ca40048640313dc29718e4e1d654bcd0bd0bdfb5 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md | ЗАДАНИЕ | 96 | ae8807eb94cc755983fecfd70d94ddfe87bf7546 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md | УРОКИ ФАБРИКЕ | 10 | ae8807eb94cc755983fecfd70d94ddfe87bf7546 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md | ПЛАН | 31 | ae8807eb94cc755983fecfd70d94ddfe87bf7546 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md | ВОПРОСЫ | 6 | ae8807eb94cc755983fecfd70d94ddfe87bf7546 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_vychitano.md | ОТЧЁТ | 68 | ae8807eb94cc755983fecfd70d94ddfe87bf7546 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md | ЗАДАНИЕ | 135 | d69e7ecc6adbd8cb0c9c5635db76d883dde97114 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md | УРОКИ ФАБРИКЕ | 36 | d69e7ecc6adbd8cb0c9c5635db76d883dde97114 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md | ПЛАН | 30 | d69e7ecc6adbd8cb0c9c5635db76d883dde97114 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md | ВОПРОСЫ | 52 | d69e7ecc6adbd8cb0c9c5635db76d883dde97114 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_zamykanie.md | ОТЧЁТ | 203 | d69e7ecc6adbd8cb0c9c5635db76d883dde97114 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md | ЗАДАНИЕ | 89 | a323f0372a9aa5a38bf2f294b9a68b6d4ad8801d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md | УРОКИ ФАБРИКЕ | 6 | a323f0372a9aa5a38bf2f294b9a68b6d4ad8801d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md | ПЛАН | 21 | a323f0372a9aa5a38bf2f294b9a68b6d4ad8801d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md | ВОПРОСЫ | 6 | a323f0372a9aa5a38bf2f294b9a68b6d4ad8801d | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_klassifikacia-kartoteki.md | ОТЧЁТ | 24 | a323f0372a9aa5a38bf2f294b9a68b6d4ad8801d | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md | ЗАДАНИЕ | 61 | 2f17e103da61964e0dc61d1b23f34ca072e85c29 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md | УРОКИ ФАБРИКЕ | 6 | 2f17e103da61964e0dc61d1b23f34ca072e85c29 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md | ПЛАН | 22 | 2f17e103da61964e0dc61d1b23f34ca072e85c29 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md | ВОПРОСЫ | 6 | 2f17e103da61964e0dc61d1b23f34ca072e85c29 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_napolnit-bazu-l1.md | ОТЧЁТ | 21 | 2f17e103da61964e0dc61d1b23f34ca072e85c29 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md | ЗАДАНИЕ | 78 | a44614094f10f3a1de1e0ca9534e92f7a55c6db8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md | УРОКИ ФАБРИКЕ | 14 | a44614094f10f3a1de1e0ca9534e92f7a55c6db8 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md | ПЛАН | 21 | a44614094f10f3a1de1e0ca9534e92f7a55c6db8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md | ВОПРОСЫ | 2 | a44614094f10f3a1de1e0ca9534e92f7a55c6db8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/kod_polnyj-prohod-vneshnie.md | ОТЧЁТ | 35 | a44614094f10f3a1de1e0ca9534e92f7a55c6db8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md | ЗАДАНИЕ | 82 | e72060e31a960dc37e49d9711eb626e0a9ba9263 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md | УРОКИ ФАБРИКЕ | 3 | e72060e31a960dc37e49d9711eb626e0a9ba9263 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md | ПЛАН | 44 | e72060e31a960dc37e49d9711eb626e0a9ba9263 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md | ВОПРОСЫ | 7 | e72060e31a960dc37e49d9711eb626e0a9ba9263 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_absorb-vstrechi.md | ОТЧЁТ | 43 | e72060e31a960dc37e49d9711eb626e0a9ba9263 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md | ЗАДАНИЕ | 150 | 0dadc293083c61568e65aeb9e0c3fe29809b0da8 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md | УРОКИ ФАБРИКЕ | 22 | 0dadc293083c61568e65aeb9e0c3fe29809b0da8 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md | ПЛАН | 76 | 0dadc293083c61568e65aeb9e0c3fe29809b0da8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md | ВОПРОСЫ | 23 | 0dadc293083c61568e65aeb9e0c3fe29809b0da8 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_chitaemost.md | ОТЧЁТ | 283 | 0dadc293083c61568e65aeb9e0c3fe29809b0da8 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md | ЗАДАНИЕ | 61 | 8b5c35faf77df02c21b9bfefe3ac0e862316eca8 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md | УРОКИ ФАБРИКЕ | 3 | 8b5c35faf77df02c21b9bfefe3ac0e862316eca8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md | ПЛАН | 17 | 8b5c35faf77df02c21b9bfefe3ac0e862316eca8 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md | ВОПРОСЫ | 4 | 8b5c35faf77df02c21b9bfefe3ac0e862316eca8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dokat-pod-kat.md | ОТЧЁТ | 77 | 8b5c35faf77df02c21b9bfefe3ac0e862316eca8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md | ЗАДАНИЕ | 178 | 51efe324ed9dbfe0a37d858bdf8791210cfea832 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md | УРОКИ ФАБРИКЕ | 5 | 51efe324ed9dbfe0a37d858bdf8791210cfea832 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md | ПЛАН | 14 | 51efe324ed9dbfe0a37d858bdf8791210cfea832 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md | ВОПРОСЫ | 7 | 51efe324ed9dbfe0a37d858bdf8791210cfea832 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_dvizhok-format.md | ОТЧЁТ | 48 | 51efe324ed9dbfe0a37d858bdf8791210cfea832 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md | ЗАДАНИЕ | 89 | d819a762d4d88c32afb927e92587834527c31779 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md | УРОКИ ФАБРИКЕ | 20 | d819a762d4d88c32afb927e92587834527c31779 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md | ПЛАН | 24 | d819a762d4d88c32afb927e92587834527c31779 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md | ВОПРОСЫ | 7 | d819a762d4d88c32afb927e92587834527c31779 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_kostyak-rez.md | ОТЧЁТ | 136 | d819a762d4d88c32afb927e92587834527c31779 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md | ЗАДАНИЕ | 54 | 47f468d20a104e0f0651fb2622bc1bb2dbdfba5c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md | УРОКИ ФАБРИКЕ | 7 | 47f468d20a104e0f0651fb2622bc1bb2dbdfba5c | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md | ПЛАН | 33 | 47f468d20a104e0f0651fb2622bc1bb2dbdfba5c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md | ВОПРОСЫ | 5 | 47f468d20a104e0f0651fb2622bc1bb2dbdfba5c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_maclane-smith.md | ОТЧЁТ | 271 | 47f468d20a104e0f0651fb2622bc1bb2dbdfba5c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md | ЗАДАНИЕ | 129 | 3b41a067de4840a0b05863de1fe0786843252e16 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md | УРОКИ ФАБРИКЕ | 38 | 3b41a067de4840a0b05863de1fe0786843252e16 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md | ПЛАН | 37 | 3b41a067de4840a0b05863de1fe0786843252e16 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md | ВОПРОСЫ | 24 | 3b41a067de4840a0b05863de1fe0786843252e16 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_mat-kostyak.md | ОТЧЁТ | 77 | 3b41a067de4840a0b05863de1fe0786843252e16 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md | ЗАДАНИЕ | 59 | 9c2b1a6abd6eb54523cdcbe9d255d203f1dfb573 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md | УРОКИ ФАБРИКЕ | 7 | 9c2b1a6abd6eb54523cdcbe9d255d203f1dfb573 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md | ПЛАН | 16 | 9c2b1a6abd6eb54523cdcbe9d255d203f1dfb573 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md | ВОПРОСЫ | 6 | 9c2b1a6abd6eb54523cdcbe9d255d203f1dfb573 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_navigacija.md | ОТЧЁТ | 25 | 9c2b1a6abd6eb54523cdcbe9d255d203f1dfb573 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md | ЗАДАНИЕ | 84 | 5a139bc6d8ee8f2920e7d01a7895be0e1b929e05 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md | УРОКИ ФАБРИКЕ | 11 | 5a139bc6d8ee8f2920e7d01a7895be0e1b929e05 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md | ПЛАН | 23 | 5a139bc6d8ee8f2920e7d01a7895be0e1b929e05 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md | ВОПРОСЫ | 10 | 5a139bc6d8ee8f2920e7d01a7895be0e1b929e05 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_pereverstka.md | ОТЧЁТ | 87 | 5a139bc6d8ee8f2920e7d01a7895be0e1b929e05 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md | ЗАДАНИЕ | 102 | 485d8f4e3a522c65f653a4cda6b503773a9deb24 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md | УРОКИ ФАБРИКЕ | 9 | 485d8f4e3a522c65f653a4cda6b503773a9deb24 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md | ПЛАН | 14 | 485d8f4e3a522c65f653a4cda6b503773a9deb24 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md | ВОПРОСЫ | 5 | 485d8f4e3a522c65f653a4cda6b503773a9deb24 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_razbor-kartoteki.md | ОТЧЁТ | 24 | 485d8f4e3a522c65f653a4cda6b503773a9deb24 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md | ЗАДАНИЕ | 165 | fc8469649c0bc66d9038deb629de8030ac89f1ae | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md | УРОКИ ФАБРИКЕ | 14 | fc8469649c0bc66d9038deb629de8030ac89f1ae | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md | ПЛАН | 36 | fc8469649c0bc66d9038deb629de8030ac89f1ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md | ВОПРОСЫ | 11 | fc8469649c0bc66d9038deb629de8030ac89f1ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_resheniya.md | ОТЧЁТ | 168 | fc8469649c0bc66d9038deb629de8030ac89f1ae | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md | ЗАДАНИЕ | 86 | cb21c6c84afde8c73d588dc7bd81e4eb1018e2c3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md | УРОКИ ФАБРИКЕ | 11 | cb21c6c84afde8c73d588dc7bd81e4eb1018e2c3 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md | ПЛАН | 30 | cb21c6c84afde8c73d588dc7bd81e4eb1018e2c3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md | ВОПРОСЫ | 75 | cb21c6c84afde8c73d588dc7bd81e4eb1018e2c3 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/kod_riehl-a.md | ОТЧЁТ | 33 | cb21c6c84afde8c73d588dc7bd81e4eb1018e2c3 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | ЗАДАНИЕ | 179 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | УРОКИ ФАБРИКЕ (первое вхождение) | 4 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | ПЛАН | 31 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | ВОПРОСЫ | 27 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | ОТЧЁТ | 85 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_brillianty-l1.md | УРОКИ ФАБРИКЕ (второе вхождение) | 11 | 8ba94f693a229d3c11c1026a93590d752d23bed0 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md | ЗАДАНИЕ | 201 | 118e3f74bb9f9cc6c44384da547371d7bfaf5e03 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md | УРОКИ ФАБРИКЕ | 17 | 118e3f74bb9f9cc6c44384da547371d7bfaf5e03 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md | ПЛАН | 55 | 118e3f74bb9f9cc6c44384da547371d7bfaf5e03 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md | ВОПРОСЫ | 14 | 118e3f74bb9f9cc6c44384da547371d7bfaf5e03 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_konsolidacia-l1.md | ОТЧЁТ | 173 | 118e3f74bb9f9cc6c44384da547371d7bfaf5e03 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | ЗАДАНИЕ | 149 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | УРОКИ ФАБРИКЕ (первое вхождение) | 3 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | ПЛАН | 32 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | ВОПРОСЫ | 22 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | УРОКИ ФАБРИКЕ (второе вхождение) | 14 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_poisk-listochki.md | ОТЧЁТ | 86 | ea0baf316327afb99bab14de3f03c9c6baaff9b8 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md | ЗАДАНИЕ | 164 | 07603535fe93713452a71d50c00a1af18f9b58be | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md | УРОКИ ФАБРИКЕ | 21 | 07603535fe93713452a71d50c00a1af18f9b58be | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md | ПЛАН | 34 | 07603535fe93713452a71d50c00a1af18f9b58be | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md | ВОПРОСЫ | 16 | 07603535fe93713452a71d50c00a1af18f9b58be | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_priruchenie-vneshnego.md | ОТЧЁТ | 83 | 07603535fe93713452a71d50c00a1af18f9b58be | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_razbor-korpusa-l1.md | ЗАДАНИЕ | 158 | ca054ec6cda9a44c6b38605176b324c22560e147 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_razbor-korpusa-l1.md | УРОКИ ФАБРИКЕ | 6 | ca054ec6cda9a44c6b38605176b324c22560e147 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_razbor-korpusa-l1.md | ПЛАН | 2 | ca054ec6cda9a44c6b38605176b324c22560e147 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_razbor-korpusa-l1.md | ВОПРОСЫ | 2 | ca054ec6cda9a44c6b38605176b324c22560e147 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_razbor-korpusa-l1.md | ОТЧЁТ | 3 | ca054ec6cda9a44c6b38605176b324c22560e147 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md | ЗАДАНИЕ | 172 | b4ee52df5d309e6d06d7ba4d73892ace162a41a6 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md | УРОКИ ФАБРИКЕ | 17 | b4ee52df5d309e6d06d7ba4d73892ace162a41a6 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md | ПЛАН | 35 | b4ee52df5d309e6d06d7ba4d73892ace162a41a6 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md | ВОПРОСЫ | 7 | b4ee52df5d309e6d06d7ba4d73892ace162a41a6 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-25_lekcia-1/kod_svedenie-i-gejty.md | ОТЧЁТ | 127 | b4ee52df5d309e6d06d7ba4d73892ace162a41a6 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md | ЗАДАНИЕ | 237 | d2f03dc29153dd9c3cbcb6897e063ce277bb9353 | 6 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md | УРОКИ ФАБРИКЕ | 66 | d2f03dc29153dd9c3cbcb6897e063ce277bb9353 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md | ПЛАН | 124 | d2f03dc29153dd9c3cbcb6897e063ce277bb9353 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md | ВОПРОСЫ | 38 | d2f03dc29153dd9c3cbcb6897e063ce277bb9353 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal-v2.md | ОТЧЁТ | 177 | d2f03dc29153dd9c3cbcb6897e063ce277bb9353 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md | ЗАДАНИЕ | 214 | 254d3e471cb77911b2a181ab93bd4c1075332ebc | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md | УРОКИ ФАБРИКЕ | 6 | 254d3e471cb77911b2a181ab93bd4c1075332ebc | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md | ПЛАН | 2 | 254d3e471cb77911b2a181ab93bd4c1075332ebc | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md | ВОПРОСЫ | 2 | 254d3e471cb77911b2a181ab93bd4c1075332ebc | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_dek-paskal.md | ОТЧЁТ | 3 | 254d3e471cb77911b2a181ab93bd4c1075332ebc | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md | ЗАДАНИЕ | 97 | 60e688d0a3b68306091d99ec65293453bca18375 | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md | УРОКИ ФАБРИКЕ | 16 | 60e688d0a3b68306091d99ec65293453bca18375 | 2 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md | ПЛАН | 57 | 60e688d0a3b68306091d99ec65293453bca18375 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md | ВОПРОСЫ | 16 | 60e688d0a3b68306091d99ec65293453bca18375 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md | ОТЧЁТ | 66 | 60e688d0a3b68306091d99ec65293453bca18375 | 10 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md | ЗАДАНИЕ | 106 | 5c2eec461bb3da1383731b58082237a894528573 | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md | УРОКИ ФАБРИКЕ | 22 | 5c2eec461bb3da1383731b58082237a894528573 | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md | ПЛАН | 64 | 5c2eec461bb3da1383731b58082237a894528573 | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md | ВОПРОСЫ | 17 | 5c2eec461bb3da1383731b58082237a894528573 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/kod_sluzhebnye-slajdy.md | ОТЧЁТ | 82 | 5c2eec461bb3da1383731b58082237a894528573 | 4 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md | ЗАДАНИЕ | 64 | aa581c6f11d7d9613bb9406a0a0eb36bddde5cda | 5 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md | УРОКИ ФАБРИКЕ | 15 | aa581c6f11d7d9613bb9406a0a0eb36bddde5cda | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md | ПЛАН | 16 | aa581c6f11d7d9613bb9406a0a0eb36bddde5cda | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md | ВОПРОСЫ | 9 | aa581c6f11d7d9613bb9406a0a0eb36bddde5cda | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/kod_skelet-konspekt-l1.md | ОТЧЁТ | 47 | aa581c6f11d7d9613bb9406a0a0eb36bddde5cda | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md | ЗАДАНИЕ | 26 | 9845cdca3f397b37ad9acbedfab512c7da667aaa | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md | ПЛАН | 40 | 9845cdca3f397b37ad9acbedfab512c7da667aaa | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md | ВОПРОСЫ | 5 | 9845cdca3f397b37ad9acbedfab512c7da667aaa | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_biblioteka-dobor.md | ОТЧЁТ | 56 | 9845cdca3f397b37ad9acbedfab512c7da667aaa | 4 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md | ЗАДАНИЕ | 42 | a369ea8429e2a9562ba5161528c011c242ce6ec8 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md | ПЛАН | 13 | a369ea8429e2a9562ba5161528c011c242ce6ec8 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md | ВОПРОСЫ | 4 | a369ea8429e2a9562ba5161528c011c242ce6ec8 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_dobor-skelet.md | ОТЧЁТ | 23 | a369ea8429e2a9562ba5161528c011c242ce6ec8 | 3 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_krever-extract.md | ЗАДАНИЕ | 36 | 01d46e5cf1e8bd4ae8beea1d304108bc13f93ddb | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_krever-extract.md | ПЛАН | 20 | 01d46e5cf1e8bd4ae8beea1d304108bc13f93ddb | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_krever-extract.md | ВОПРОСЫ | 2 | 01d46e5cf1e8bd4ae8beea1d304108bc13f93ddb | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_krever-extract.md | ОТЧЁТ | 111 | 01d46e5cf1e8bd4ae8beea1d304108bc13f93ddb | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skachat-mir2.md | ЗАДАНИЕ | 27 | 5185ba6e6d45f1dcc352afdec96692bf01d6a8e7 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skachat-mir2.md | ПЛАН | 7 | 5185ba6e6d45f1dcc352afdec96692bf01d6a8e7 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skachat-mir2.md | ВОПРОСЫ | 3 | 5185ba6e6d45f1dcc352afdec96692bf01d6a8e7 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skachat-mir2.md | ОТЧЁТ | 18 | 5185ba6e6d45f1dcc352afdec96692bf01d6a8e7 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md | ЗАДАНИЕ | 61 | 8608a7ac45a1cde4369f05c020395d18587e416b | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md | ПЛАН | 11 | 8608a7ac45a1cde4369f05c020395d18587e416b | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md | ВОПРОСЫ | 8 | 8608a7ac45a1cde4369f05c020395d18587e416b | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_skelet-mir2.md | ОТЧЁТ | 26 | 8608a7ac45a1cde4369f05c020395d18587e416b | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md | ЗАДАНИЕ | 62 | ef3f707fe626e8280129aedc896b768015ca7d0d | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md | ПЛАН | 34 | ef3f707fe626e8280129aedc896b768015ca7d0d | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md | ВОПРОСЫ | 8 | ef3f707fe626e8280129aedc896b768015ca7d0d | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_statya-mir2.md | ОТЧЁТ | 45 | ef3f707fe626e8280129aedc896b768015ca7d0d | 2 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md | ЗАДАНИЕ | 28 | ab2267ec0875241f50d3855b3ceca3c496f34c1a | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md | ПЛАН | 10 | ab2267ec0875241f50d3855b3ceca3c496f34c1a | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md | ВОПРОСЫ | 5 | ab2267ec0875241f50d3855b3ceca3c496f34c1a | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-03_programma-kursa/kod_vychitano-backfill.md | ОТЧЁТ | 25 | ab2267ec0875241f50d3855b3ceca3c496f34c1a | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md | ЗАДАНИЕ | 40 | 574e9825cb37f51047df420de8d0d1ad1443f300 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md | ПЛАН | 36 | 574e9825cb37f51047df420de8d0d1ad1443f300 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md | ВОПРОСЫ | 4 | 574e9825cb37f51047df420de8d0d1ad1443f300 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_biblioteka-mir1.md | ОТЧЁТ | 56 | 574e9825cb37f51047df420de8d0d1ad1443f300 | 2 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md | ЗАДАНИЕ | 108 | 4275661fd93f3ec17f6855ee9f8f114c90654838 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md | ПЛАН | 24 | 4275661fd93f3ec17f6855ee9f8f114c90654838 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md | ВОПРОСЫ | 4 | 4275661fd93f3ec17f6855ee9f8f114c90654838 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_html-obshchiy.md | ОТЧЁТ | 28 | 4275661fd93f3ec17f6855ee9f8f114c90654838 | 2 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_skelet-mir1.md | ЗАДАНИЕ | 55 | 9cf68a75fa7b71dc6f8000a11ccc42535f69da3c | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_skelet-mir1.md | ПЛАН | 20 | 9cf68a75fa7b71dc6f8000a11ccc42535f69da3c | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_skelet-mir1.md | ВОПРОСЫ | 5 | 9cf68a75fa7b71dc6f8000a11ccc42535f69da3c | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-05_mir1/kod_skelet-mir1.md | ОТЧЁТ | 15 | 9cf68a75fa7b71dc6f8000a11ccc42535f69da3c | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_illustracii-build-doc.md | ЗАДАНИЕ | 73 | cf9292974a85f6b46610a4cee4803ea1392d0ee0 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_illustracii-build-doc.md | ПЛАН | 31 | cf9292974a85f6b46610a4cee4803ea1392d0ee0 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_illustracii-build-doc.md | ВОПРОСЫ | 5 | cf9292974a85f6b46610a4cee4803ea1392d0ee0 | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_illustracii-build-doc.md | ОТЧЁТ | 32 | cf9292974a85f6b46610a4cee4803ea1392d0ee0 | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md | ЗАДАНИЕ | 96 | 84cb6fe953f4ff596e6916a202d79c61ea911ffb | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md | ПЛАН | 43 | 84cb6fe953f4ff596e6916a202d79c61ea911ffb | 1 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md | ВОПРОСЫ | 9 | 84cb6fe953f4ff596e6916a202d79c61ea911ffb | 0 | 2026-07-30 |
| catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/kod_port-oformlenia-v-build-doc.md | ОТЧЁТ | 46 | 84cb6fe953f4ff596e6916a202d79c61ea911ffb | 3 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-27_arhitektura-pamyati/kod_perenos-biblioteki.md | ЗАДАНИЕ | 47 | 7d0d9778326c2b91aa2d388dc13db667165619e0 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-27_arhitektura-pamyati/kod_perenos-biblioteki.md | ПЛАН | 25 | 7d0d9778326c2b91aa2d388dc13db667165619e0 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-27_arhitektura-pamyati/kod_perenos-biblioteki.md | ВОПРОСЫ | 6 | 7d0d9778326c2b91aa2d388dc13db667165619e0 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-27_arhitektura-pamyati/kod_perenos-biblioteki.md | ОТЧЁТ | 28 | 7d0d9778326c2b91aa2d388dc13db667165619e0 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md | ЗАДАНИЕ | 119 | 775688f88dd764d65ac928da9eedd751fc51eca4 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md | ПЛАН | 24 | 775688f88dd764d65ac928da9eedd751fc51eca4 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md | ВОПРОСЫ | 10 | 775688f88dd764d65ac928da9eedd751fc51eca4 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_dobor-do-10.md | ОТЧЁТ | 41 | 775688f88dd764d65ac928da9eedd751fc51eca4 | 3 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_html-v3.md | ЗАДАНИЕ | 78 | c2cf754a7757a2d0fbe282e8b1a7b854898f18ab | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_html-v3.md | ПЛАН | 19 | c2cf754a7757a2d0fbe282e8b1a7b854898f18ab | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_html-v3.md | ВОПРОСЫ | 6 | c2cf754a7757a2d0fbe282e8b1a7b854898f18ab | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_html-v3.md | ОТЧЁТ | 28 | c2cf754a7757a2d0fbe282e8b1a7b854898f18ab | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_L4-html-v4.md | ЗАДАНИЕ | 70 | 44de7be99ac26c1b823e21bc042446a6f0f850e3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_L4-html-v4.md | ПЛАН | 32 | 44de7be99ac26c1b823e21bc042446a6f0f850e3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_L4-html-v4.md | ВОПРОСЫ | 9 | 44de7be99ac26c1b823e21bc042446a6f0f850e3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_L4-html-v4.md | ОТЧЁТ (дубль-заголовок в источнике, объединено) | 47 | 44de7be99ac26c1b823e21bc042446a6f0f850e3 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_svap-tz-v2.md | ЗАДАНИЕ | 61 | 5cb23358e42934bd9173f333ec9ddd706ec5eb06 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_svap-tz-v2.md | ПЛАН | 24 | 5cb23358e42934bd9173f333ec9ddd706ec5eb06 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_svap-tz-v2.md | ВОПРОСЫ | 5 | 5cb23358e42934bd9173f333ec9ddd706ec5eb06 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_nauchpop-chernovik/kod_svap-tz-v2.md | ОТЧЁТ | 47 | 5cb23358e42934bd9173f333ec9ddd706ec5eb06 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_klubok-sborka.md | ЗАДАНИЕ | 69 | 87e7bf84b044dcb73a4e2216b69513259775fe11 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_klubok-sborka.md | ВОПРОСЫ | 9 | 87e7bf84b044dcb73a4e2216b69513259775fe11 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_klubok-sborka.md | ОТЧЁТ | 40 | 87e7bf84b044dcb73a4e2216b69513259775fe11 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md | ЗАДАНИЕ | 75 | ca42aa761e3366a9e4a116558c160b86fc325c0a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md | ПЛАН | 21 | ca42aa761e3366a9e4a116558c160b86fc325c0a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md | ВОПРОСЫ | 8 | ca42aa761e3366a9e4a116558c160b86fc325c0a | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_procedura-poiska.md | ОТЧЁТ | 48 | ca42aa761e3366a9e4a116558c160b86fc325c0a | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md | ЗАДАНИЕ | 46 | de02cf805f45780e19dc61a9719824670a0b61cd | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md | ПЛАН | 17 | de02cf805f45780e19dc61a9719824670a0b61cd | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md | ВОПРОСЫ | 7 | de02cf805f45780e19dc61a9719824670a0b61cd | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_progon-subagentami.md | ОТЧЁТ | 25 | de02cf805f45780e19dc61a9719824670a0b61cd | 3 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md | ЗАДАНИЕ | 38 | 0bcc16f302eaaf9056b2f0e182c94640ae536928 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md | ПЛАН | 19 | 0bcc16f302eaaf9056b2f0e182c94640ae536928 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md | ВОПРОСЫ | 4 | 0bcc16f302eaaf9056b2f0e182c94640ae536928 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_razvedka-sborka.md | ОТЧЁТ | 44 | 0bcc16f302eaaf9056b2f0e182c94640ae536928 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md | ЗАДАНИЕ | 48 | c97c7a5ea805849655eec324c03dbc7789c9d747 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md | ПЛАН | 10 | c97c7a5ea805849655eec324c03dbc7789c9d747 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md | ВОПРОСЫ | 4 | c97c7a5ea805849655eec324c03dbc7789c9d747 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md | ОТЧЁТ | 35 | c97c7a5ea805849655eec324c03dbc7789c9d747 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md | ЗАДАНИЕ | 40 | f4aece1bcceb08016e325731df4699f70a62ef72 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md | ПЛАН | 8 | f4aece1bcceb08016e325731df4699f70a62ef72 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md | ВОПРОСЫ | 13 | f4aece1bcceb08016e325731df4699f70a62ef72 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona.md | ОТЧЁТ | 30 | f4aece1bcceb08016e325731df4699f70a62ef72 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator-visual.md | ЗАДАНИЕ | 44 | a7f60f802672658580ae315c868ea6cd621f2a57 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator-visual.md | ПЛАН | 13 | a7f60f802672658580ae315c868ea6cd621f2a57 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator-visual.md | ВОПРОСЫ | 6 | a7f60f802672658580ae315c868ea6cd621f2a57 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator-visual.md | ОТЧЁТ | 27 | a7f60f802672658580ae315c868ea6cd621f2a57 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md | ЗАДАНИЕ | 83 | f1388175ef63d88b672004b3e06a769eb42bdf4f | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md | ПЛАН | 19 | f1388175ef63d88b672004b3e06a769eb42bdf4f | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md | ВОПРОСЫ | 17 | f1388175ef63d88b672004b3e06a769eb42bdf4f | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_edinyy-istochnik/kod_generator.md | ОТЧЁТ | 37 | f1388175ef63d88b672004b3e06a769eb42bdf4f | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md | ЗАДАНИЕ | 58 | 9a6e05905ee45f4452f6d68b4a9010909927d49a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md | ПЛАН | 18 | 9a6e05905ee45f4452f6d68b4a9010909927d49a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md | ВОПРОСЫ | 4 | 9a6e05905ee45f4452f6d68b4a9010909927d49a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_dobor-L2.md | ОТЧЁТ | 35 | 9a6e05905ee45f4452f6d68b4a9010909927d49a | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md | ЗАДАНИЕ | 106 | be7b9e7d1f6c3696f62d0cff6f33749bbc9f38b4 | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md | ПЛАН | 23 | be7b9e7d1f6c3696f62d0cff6f33749bbc9f38b4 | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md | ВОПРОСЫ | 3 | be7b9e7d1f6c3696f62d0cff6f33749bbc9f38b4 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_fix-latex.md | ОТЧЁТ | 59 | be7b9e7d1f6c3696f62d0cff6f33749bbc9f38b4 | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md | ЗАДАНИЕ | 72 | 81127778e4ca2e2dcff40dcce77672d17006280e | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md | ПЛАН | 15 | 81127778e4ca2e2dcff40dcce77672d17006280e | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md | ВОПРОСЫ | 10 | 81127778e4ca2e2dcff40dcce77672d17006280e | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_html-L2.md | ОТЧЁТ | 92 | 81127778e4ca2e2dcff40dcce77672d17006280e | 2 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_ideal-L2.md | ЗАДАНИЕ | 44 | 167ac867260acedcf193ca5e8c0f1b40c1def879 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_ideal-L2.md | ПЛАН | 20 | 167ac867260acedcf193ca5e8c0f1b40c1def879 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_ideal-L2.md | ВОПРОСЫ | 3 | 167ac867260acedcf193ca5e8c0f1b40c1def879 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_ideal-L2.md | ОТЧЁТ | 54 | 167ac867260acedcf193ca5e8c0f1b40c1def879 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md | ЗАДАНИЕ | 122 | 7d7a0a675f33e452673ddd29b3add06643575c4a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md | ПЛАН | 12 | 7d7a0a675f33e452673ddd29b3add06643575c4a | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md | ВОПРОСЫ | 4 | 7d7a0a675f33e452673ddd29b3add06643575c4a | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_pravki-L6.md | ОТЧЁТ | 22 | 7d7a0a675f33e452673ddd29b3add06643575c4a | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md | ЗАДАНИЕ | 79 | b6b36f6568e4b61497a5b2aaec0eca6ecdd1d214 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md | ПЛАН | 23 | b6b36f6568e4b61497a5b2aaec0eca6ecdd1d214 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md | ВОПРОСЫ | 14 | b6b36f6568e4b61497a5b2aaec0eca6ecdd1d214 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-06-30_L2-optimizaciya/kod_sborka-L2.md | ОТЧЁТ | 43 | b6b36f6568e4b61497a5b2aaec0eca6ecdd1d214 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-01_struktura-i-svyazi/kod_usilenie-svyazey.md | ЗАДАНИЕ | 82 | 61d34c6090eb45e896f765d3ecf2bed0f22d539b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-01_struktura-i-svyazi/kod_usilenie-svyazey.md | ВОПРОСЫ | 8 | 61d34c6090eb45e896f765d3ecf2bed0f22d539b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-01_struktura-i-svyazi/kod_usilenie-svyazey.md | ОТЧЁТ | 30 | 61d34c6090eb45e896f765d3ecf2bed0f22d539b | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md | ЗАДАНИЕ | 64 | 192bcb15fd8dadee2d80b4c48f2f1236888ab684 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md | ПЛАН | 25 | 192bcb15fd8dadee2d80b4c48f2f1236888ab684 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md | ВОПРОСЫ | 7 | 192bcb15fd8dadee2d80b4c48f2f1236888ab684 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_perenos-i-checker.md | ОТЧЁТ | 55 | 192bcb15fd8dadee2d80b4c48f2f1236888ab684 | 3 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_sync-pilot.md | ЗАДАНИЕ | 53 | 7c977fb625a869f6fbf06af7d617d249f18d507b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_sync-pilot.md | ПЛАН | 15 | 7c977fb625a869f6fbf06af7d617d249f18d507b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_sync-pilot.md | ВОПРОСЫ | 4 | 7c977fb625a869f6fbf06af7d617d249f18d507b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-02_edinoe-okno-pamyati/kod_sync-pilot.md | ОТЧЁТ | 30 | 7c977fb625a869f6fbf06af7d617d249f18d507b | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-07_reklama-seriya/kod_finalnaya-dovodka-kartochek.md | ЗАДАНИЕ | 110 | 06d49ffb530f4726ef74f72568240abe340143b3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-07_reklama-seriya/kod_finalnaya-dovodka-kartochek.md | ПЛАН | 2 | 06d49ffb530f4726ef74f72568240abe340143b3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-07_reklama-seriya/kod_finalnaya-dovodka-kartochek.md | ВОПРОСЫ | 2 | 06d49ffb530f4726ef74f72568240abe340143b3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-07_reklama-seriya/kod_finalnaya-dovodka-kartochek.md | ОТЧЁТ | 1 | 06d49ffb530f4726ef74f72568240abe340143b3 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-09_sayt-rasshirenie/kod_ekran2.md | ЗАДАНИЕ | 95 | ea0db4dd6daa6241e198bf6c9ead4e828d367ab6 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-09_sayt-rasshirenie/kod_ekran2.md | ВОПРОСЫ | 3 | ea0db4dd6daa6241e198bf6c9ead4e828d367ab6 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/2026-07-09_sayt-rasshirenie/kod_ekran2.md | ОТЧЁТ | 20 | ea0db4dd6daa6241e198bf6c9ead4e828d367ab6 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/kod_uborka-renumber.md | ЗАДАНИЕ | 63 | 39bc185865fd88dc981c78fe6ff35c9da6d19276 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/kod_uborka-renumber.md | ПЛАН | 20 | 39bc185865fd88dc981c78fe6ff35c9da6d19276 | 0 | 2026-07-30 |
| kurs leto 2026/zhurnal/kod_uborka-renumber.md | ВОПРОСЫ | 4 | 39bc185865fd88dc981c78fe6ff35c9da6d19276 | 1 | 2026-07-30 |
| kurs leto 2026/zhurnal/kod_uborka-renumber.md | ОТЧЁТ | 26 | 39bc185865fd88dc981c78fe6ff35c9da6d19276 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-21_mat-kostyak/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 182 | ff29de9dd943c81f45c3bfee7a9c1e2340c113f9 | 29 | 2026-07-30 |
| _studio/zhurnal/2026-07-27_paskal-lekcia-sborka/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 140 | 213db26db3b3b050cbaf7c0cc970011b03fd6300 | 17 | 2026-07-30 |
| _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 100 | 9e3dfc89dacac2894a358b73e1585d25072023a6 | 14 | 2026-07-30 |
| _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 378 | 5a200ad59052ae98bb1fdc8caf12bc65c7746209 | 8 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_teksty-l1/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 82 | f4d23e43999fbe028e22cf09d3e6468d775235d1 | 3 | 2026-07-30 |
| _studio/zhurnal/2026-07-23_vneshnie-istorii/UROKI-FABRIKE.md | УРОКИ ФАБРИКЕ (весь файл, 73-урочный источник) | 48 | 3cf633dbc460f223c4f80aeea1aca57bb70d3b57 | 2 | 2026-07-30 |
| buffon/WORKLIST.md | (весь файл — реестр правок эталонного дека, читан целиком особым вниманием) | 239 | 23de4143313413f23f06c6285edb631404a4f63b | 9 | 2026-07-30 |
| buffon/ZAHOD-01.md | (весь файл — заход эталонного дека, читан целиком особым вниманием) | 305 | 49372f457328cc39d0e1166b489e8c85ec3d6069 | 1 | 2026-07-30 |
| buffon/ZAHOD-02.md | (весь файл — заход эталонного дека, читан целиком особым вниманием) | 120 | 5f3c7991f73688b4e82631640905e93c5a5b10f0 | 3 | 2026-07-30 |
| buffon/ZAHOD-03.md | (весь файл — заход эталонного дека, читан целиком особым вниманием) | 192 | c362c106e710bbf5b0fd2d7211c271444b4a4367 | 0 | 2026-07-30 |
| buffon/ZAHOD-04.md | (весь файл — заход эталонного дека, читан целиком особым вниманием) | 194 | b6346b3ccccce4e8558e3f6dea9790a795c7704e | 1 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_konspekt-l1/kod_upakovka.md | (весь файл — читан ДОПОЛНИТЕЛЬНО для точечной пробы 526→97, см. `PROBA-526-97.md`; вне обязательных 118 файлов и вне общего корпуса — 11 найденных там кандидатов с ценой описаны в `PROBA-526-97.md`, не в `KORPUS-*.md`) | 566 | d35419a5147dfea1034a1fc2cb9f421d5b14bf87 | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_konspekt-l1/kod_razrez.md | (весь файл — читан ДОПОЛНИТЕЛЬНО для точечной пробы 526→97, см. `PROBA-526-97.md`; вне обязательных 118 файлов и вне общего корпуса) | 574 | 1a1a61956cfc02b59667f3546a90cf781a37b91c | 0 | 2026-07-30 |
| _studio/zhurnal/2026-07-28_konspekt-l1/UROKI-FABRIKE.md | (весь файл, 97 уроков — читан для сверки в рамках пробы 526→97, ВЕРДИКТОВ не менял) | 614 | 41525b6f4be2d9dad875e47c2e9aa9fb760c72c1 | 0 | 2026-07-30 |
