# KARTA — единственный индекс проекта фабрики

> **КОГДА читать:** первым (Правило №0), точка входа. · **ЧТО дописывать сюда:** регистрацию любого нового `.md` (§6) + маршрут (§1′). Это ЕДИНСТВЕННЫЙ индекс — второго списка доков нет. · **КУДА дальше:** §1.

Вход в проект — Правило №0 (`../README.md`): **KARTA → KONSTITUCIYA → RESHENIYA → OTKRYTYE-ZADACHI**. Только потом частная задача. Многосоставная работа → арка (`kak-delat/ARKA.md`).

## §1. Читать — по ситуации
| Ситуация | Дом |
|---|---|
| что свято / можно ли менять | `KONSTITUCIYA.md` |
| почему так решено | `pochemu-i-videnie/RESHENIYA.md` |
| где мы / что дальше | `sostoyanie/OTKRYTYE-ZADACHI.md` (📍 борд) |
| история кратко | `sostoyanie/SVODKI.md` |
| дизайн фабрики / карта 10 шагов | `spravka/ARHITEKTURA-FABRIKI.md` |
| профили/циферблаты курс-проекта (масштаб, вкл. лекция↔курс) | `spravka/PROFILI-CIFERBLATY.md` |
| прайор-арт / обоснования | `spravka/PRAJOR-ART.md` |
| как вести арку | `kak-delat/ARKA.md` |
| как писать заход исполнителю | `kak-delat/RUKOVODSTVO-zahodami.md` |
| программа короткого курса (лёгкий профиль, без полного конвейера) | `kak-delat/PROGRAMMA-KURSA.md` |
| собрать / понять шаг производства дека | `../konvejer/00-KONVEJER.md` → нужный `NN-*.md` |
| движки сборки markdown→HTML (дек / документ) | `../../_generator/DVIZHKI.md` |
| верхняя часть Фазы I (идея → костяк-текст) | `spravka/FAZA-1-REDESIGN.md` |
| поведение аналитика | `../COWORK.md` |
| вход исполнителя | `../CLAUDE.md` |

## §1′. Дописывать — тип → его ЕДИНСТВЕННЫЙ дом
| Появилось | Дом |
|---|---|
| осевшее решение / «почему» / отвергнутое | `pochemu-i-videnie/RESHENIYA.md` |
| статус / шаг / открытый вопрос | `sostoyanie/OTKRYTYE-ZADACHI.md` |
| идея на будущее | беклог в `sostoyanie/OTKRYTYE-ZADACHI.md` |
| архитектурная деталь | `spravka/ARHITEKTURA-FABRIKI.md` |
| находка ресёрча + ссылка | `spravka/PRAJOR-ART.md` |
| неизменный принцип | `KONSTITUCIYA.md` |
| сводка сессии/арки | `sostoyanie/SVODKI.md` |
| нарратив хода / детали | дневник арки `zhurnal/<арка>/SESSIYA.md` |
| **любой новый `.md`** | **строку в §6 — ТЕМ ЖЕ ходом** (иначе сирота) |

## §2. Источник правды — у сущности ОДИН дом
Решения → `RESHENIYA`. Статус/задачи → `OTKRYTYE-ZADACHI`. Принципы → `KONSTITUCIYA`. Дизайн/шаги (карта) → `ARHITEKTURA-FABRIKI`; спека каждого шага (как исполнять) → `../konvejer/NN-*.md`. Ресёрч → `PRAJOR-ART`. История → `SVODKI`. Продукт (генератор/эталоны) → `../../_generator`, `../../dandelin`, `../../buffon`.

## §6. Карта документов (все `.md`)
**Корень `_studio/`:** `../README.md` (Правило №0) · `../CLAUDE.md` (вход исполнителя) · `../COWORK.md` (вход аналитика).
**`docs/`:** `KARTA.md` (этот индекс) · `KONSTITUCIYA.md`.
**`docs/kak-delat/`:** `kak-delat/ARKA.md` · `kak-delat/RUKOVODSTVO-zahodami.md` · `kak-delat/PROGRAMMA-KURSA.md` (курс-масштаб: программа короткого курса, лёгкий профиль; перенесено из kurs-fabrika 2026-07-10).
**`docs/pochemu-i-videnie/`:** `pochemu-i-videnie/RESHENIYA.md`.
**`docs/sostoyanie/`:** `sostoyanie/OTKRYTYE-ZADACHI.md` · `sostoyanie/SVODKI.md`.
**`docs/spravka/`:** `spravka/ARHITEKTURA-FABRIKI.md` · `spravka/PRAJOR-ART.md` · `spravka/FAZA-1-BLUEPRINT.md` · `spravka/FAZA-1-REDESIGN.md` (ранние стадии Фазы I пересобраны 2026-07-11 — заменяет 0–4 блюпринта) · `spravka/PROFILI-CIFERBLATY.md` (курс-масштаб: профили + циферблаты, вкл. новый лекция↔курс; перенесено из kurs-fabrika 2026-07-10) · `spravka/PAPKA-LEKCII.md` (канон папки лекции: все слои Фазы I+II в одной папке; арка «оркестрация» 2026-07-10).
**`../konvejer/`** (шаги производства дека): `../konvejer/00-KONVEJER.md` (индекс шагов) · `ALGORITM.md` (единая управляющая линия ОБЕИХ фаз: driver, гейты, развилки, стыки) · `GEJTY.md` (реестр гейтов как данные для трекера; арка «оркестрация») · `KATALOG.md` (каталог функций «инструмент-под-задачу»: станции + микрофункции; арка «оркестрация») · `ZHURNAL.md` (формат журнала вызовов для трекера; арка «оркестрация») · `FORMAT-ISTOCHNIKA.md` (контракт хранения дека — выход фабрики). Каждый шаг — папка-пакет `NN-<имя>/` из `DOK.md` (документация, паттерн SKILL.md) + `ZAHOD.md` (промт под Claude Code) + `PRIMERY.md` (примеры). Фаза II: `06-tekst/` · `07-verstka/` · `08-sceny/` · `09-illustracii/` · `10-sborka-qa/`. Фаза I (greenfield; пересобрана под редизайн 2026-07-11 — карточный граф + котлы математика‖научпоп в двухвкладочном doc-виде, нарратив отдельной стадией, скиллы внутрь Р17; развилки владельцу в `../zhurnal/2026-07-10_sborka-konvejera/kod_faza1-redesign.md`): `01-brief/` · `02-reserch/` · `03-matbaza/` · `04-gibrid-istochnik/` · `05-raskadrovka/`.
**Инфра фабрики (в `../../_generator/`):** `skeleton/` (пустой greenfield-`src/` = «шаг 0»; несёт `base.css` канон-base) · `svgo.config.mjs` (Р10 id-prefix) · `audit.py` (QA слой 3; прогон — на машине с браузером) · `tools/bootstrap_lekcia.py` (бутстрап папки лекции по `PAPKA-LEKCII.md`; арка «оркестрация») · `tools/sostoyanie.py` (трекер состояния лекции — read-only аудит гейтов `GEJTY.md` + сверка журнала; арка «оркестрация») · `tools/bootstrap_arka.py` (бутстрап папки АРКИ копией `_TEMPLATE-arka/` с подстановкой; жизненный цикл арки, `ARKA §10` / Р22).
**`zhurnal/`:** `../zhurnal/PRO-ETU-PAPKU.md` · `../zhurnal/_TEMPLATE-arka/` (шаблон-скелет арки: `NAVIGATOR`+`PLAN`+`SESSIYA`+`TZ` с плейсхолдерами; копируется `bootstrap_arka.py`; арка «оркестрация» ⑤, Р22) (+ арки `<дата_тема>/`).

## §7. Модель памяти
Две памяти: **долгая** (дома `docs/`) vs **локальная** (папка арки `zhurnal/<арка>/`). Долгую читаем раз на входе в арку, дальше на дистиллятах. Один дом на сущность; durable из арки → по домам при закрытии. «Осталось только в дневнике — не существует.» Механика — `kak-delat/ARKA.md`.

## Стадия
М1 закрыта; М2 (архитектура) — design закрыт, проект поставлен на рельсы. Сейчас: дособрать скелет → арка «гибрид-источник». Детали — `sostoyanie/OTKRYTYE-ZADACHI.md`.

---
*Единственный индекс. Полный вход — Правило №0 (`../README.md`).*
