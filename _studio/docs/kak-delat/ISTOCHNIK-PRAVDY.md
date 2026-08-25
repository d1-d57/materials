# ISTOCHNIK-PRAVDY.md → ПЕРЕЕХАЛ

> 🔴 **Дом правила «где что живёт» теперь в репозитории `disciplina`: `disciplina/skills/disciplina-istochnik-pravdy/ISTOCHNIK-PRAVDY.md`.** Копия в `materials/_meta/disciplina/ISTOCHNIK-PRAVDY.md` снесена 2026-08-25 (заход vynos-kanona). Здесь остался только указатель.

🔴 **Ссылка вида `ISTOCHNIK-PRAVDY.md §<раздел>` теперь ведёт СЮДА, а раздела здесь нет.** Все разделы переехали целиком и под теми же номерами в `disciplina/skills/disciplina-istochnik-pravdy/ISTOCHNIK-PRAVDY.md`:

| раздел | о чём |
|---|---|
| `§1` | где что живёт — один дом на сущность |
| `§2` | правило одного дома |
| `§3` | что краснеет — пять ворот `check_kartoteka.py --gates`; включая `§Что гейт НЕ судит` |
| `§4` | чек-лист перед коммитом |

Ищи раздел там — номера не менялись.

**Как мы вообще работаем — идёшь в `_meta/`.** Заход, коммит, арка, дневник — всё оттуда и одним языком.

| Что нужно | Куда |
|---|---|
| где что живёт, правило одного дома, пять ворот, чек-лист перед коммитом | `disciplina/skills/disciplina-istochnik-pravdy/ISTOCHNIK-PRAVDY.md` |
| как писать заход исполнителю и как принимать отчёт | `disciplina/skills/disciplina-zahod/RUKOVODSTVO-zahodami.md` |
| любая работа с git | `disciplina/skills/disciplina-git/GIT-disciplina.md` |
| канон арок | `disciplina/skills/disciplina-arka/ARKA.md` |
| что этот дом вообще есть и чего он НЕ делает | `../../../_meta/README.md` |

⚠ **Реестр корней, по которому судят ворота, — `../../../_generator/tools/korni.py`.** С 2026-08-06 в нём пять индексируемых корней, а не один: у `_meta/` и `_illustracii/` свои `docs/KARTA.md`, и дверь `register_doc.py` пишет в индекс ТОГО корня, которому путь принадлежит. Формулировки §1 и §4, называющие `_studio/docs/KARTA.md` буквально, читать как «индекс своего корня».

**Почему файл не удалён, а стал указателем.** На старый адрес ссылались 13 живых мест по всему репозиторию (дата данных 2026-08-06; пересчёт — `grep -rlF 'ISTOCHNIK-PRAVDY.md' --include='*.md' --include='*.py' --include='*.sh' . | grep -v '^_meta/'`) — меньше, чем у соседей, но указатель ставится не по числу: он ставится потому, что ссылки лежат вне зоны захода, который делал перенос (`../../zhurnal/2026-08-05_faza-lenty/kod_vynos-meta.md`). Указатель снимается вместе с последней ссылкой на него, не раньше.

*История файла целиком уехала вместе с содержанием: `git log --follow _meta/disciplina/ISTOCHNIK-PRAVDY.md`.*
