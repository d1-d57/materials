# Канал Claude Code — ЗАПУСК полного прогона (v2, скрипт починен)

> Для Claude Code: твой **единственный** файл-заход. Читай только его. **ОПС-заход**: машину НЕ строишь и НЕ правишь — **запускаешь**. План/вопросы/отчёт — в секции внизу.

---
**📋 Текст владельцу для пересылки в Code (готов):**
> Claude Code, твой заход — файл `/Users/ivanyakovlev/Documents/GitHub/kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/kod_zapusk-progona-2.md`. Прочитай ТОЛЬКО его. Остальной проект не изучай, файлы внутри `procedura/` не читай и не правь. Отчёт пиши в этот же файл, секция `## ОТЧЁТ`.
---

## ЗАДАЧА (запустить и не мешать)

**КОНТЕКСТ.** В `procedura/` собрана и пилотом проверена машина поиска курса (5 волн). Прошлый запуск упал из-за bash-бага в `orchestrate.sh` (`declare -A` на bash 3.2) — **баг уже починен и протестирован аналитиком** (портативность bash 3.2 + флаги claude добавляются адаптивно). Твоя задача — запустить полный прогон **в фоне**, убедиться, что волна 1 пошла, и сказать владельцу, где смотреть результат.

### 0. ПЕРВЫЙ ХОД
- Рабочая папка: `/Users/ivanyakovlev/Documents/GitHub/kurs leto 2026/zhurnal/2026-06-28_procedura-poiska/`.
- zip-бэкап (точка отката): `zip -rq "procedura_backup_$(date +%Y%m%d_%H%M%S).zip" procedura`.
- `chmod +x procedura/orchestrate.sh`; проверь `claude --version`.
- Короткий ПЛАН в `## ПЛАН`, затем действуй.

### 0.5 АРХИВ ПИЛОТНЫХ АРТЕФАКТОВ (чтобы прогон стартовал чисто, не на пилотных данных)
```bash
cd "/Users/ivanyakovlev/Documents/GitHub/kurs leto 2026/zhurnal/2026-06-28_procedura-poiska"
mkdir -p procedura/artifacts/_pilot
mv procedura/artifacts/w1_candidates.jsonl procedura/artifacts/w2_survivors.jsonl \
   procedura/artifacts/w2_repair_log.json procedura/artifacts/w3_deepened.jsonl \
   procedura/artifacts/_pilot/ 2>/dev/null || true
```

### 1. ГРАНИЦЫ (жёстко)
- **НЕ читай и НЕ правь** файлы внутри `procedura/` (rubric / grid / wave* / schema / anchor / orchestrate). Машина готова и починена — не «улучшай».
- **НЕ гоняй волны сам** субагентами/Task. Волны запускает ТОЛЬКО `orchestrate.sh`.
- **НЕ блокируйся на часы** — запусти в фоне и выходи.

### 2. ЗАПУСК — в фоне (переживает закрытие сессии, не даёт Маку уснуть)
```bash
cd "/Users/ivanyakovlev/Documents/GitHub/kurs leto 2026/zhurnal/2026-06-28_procedura-poiska"
nohup caffeinate -i ./procedura/orchestrate.sh all > procedura/artifacts/run_full.log 2>&1 &
echo "PID прогона: $!"
```
- Подожди ~90 сек, покажи `tail -n 30 procedura/artifacts/run_full.log`. Норма старта: строка `Волны к прогону: w1 w2 w3 w4 w5`, затем `>>> [w1] модель субагентов=haiku ...`. (Строка `ПРИМЕЧАНИЕ: claude не знает --json-schema` — это **норма**, не ошибка: контракт держат промпты + валидация.)
- **Если в логе ошибка ДО `>>> [w1]`** (нет `claude`, неизвестный флаг, отказ прав) — **НЕ перезапускай вслепую**, вынеси лог дословно в `## ОТЧЁТ` и `## ВОПРОСЫ`. Это первый реальный запуск substrata `claude -p`; если флаг не тот — упадёт дёшево на старте w1, 5-час окно не сгорит.

### 3. ОТЧЁТ → секция `## ОТЧЁТ`
- PID прогона + время старта; подтверждение, что w1 пошла (хвост лога).
- **Где смотреть владельцу:** итог — `procedura/artifacts/w5_dossier.md`; прогресс — `procedura/artifacts/run_full.log`; время + токены по волнам — `procedura/artifacts/run_log.txt`.
- **Resume при троттле Max 20x:** `./procedura/orchestrate.sh wN` (предыдущие волны на диске). Одно 5-час окно, ОДИН инстанс, Opus авто→Sonnet при недельном капе.
- НЕ жди завершения; прогон идёт сам.

## ПЛАН
1. zip-бэкап `procedura/` (точка отката).
2. Архив пилотных артефактов в `procedura/artifacts/_pilot/`.
3. `chmod +x orchestrate.sh`; проверить `claude --version`.
4. Запуск в фоне: `nohup caffeinate -i ./procedura/orchestrate.sh all`.
5. Подождать ~90 сек, показать хвост `run_full.log`, проверить что w1 пошла.
6. Отчёт: PID, время старта, хвост лога, где смотреть владельцу.

Границы: внутрь `procedura/` не читаю/не правлю, волны сам не гоняю, не блокируюсь.

## ВОПРОСЫ
1. **Как должен аутентифицироваться `claude -p` внутри `orchestrate.sh`?** Интерактивная сессия Claude Code (в которой я работаю) авторизована, но дочерний headless-процесс `claude -p` получает **401 Invalid authentication credentials**. Нужен способ дать прогону валидные креды: либо `export ANTHROPIC_API_KEY=...` перед запуском оркестратора (API-ключ), либо headless-логин/токен подписки для `claude -p`. Без этого ни одна волна не выполнится. Это вопрос окружения/кредов — решение владельца, не правка машины.
2. **Оркестратор молча считает пустой/ошибочный вывод `claude -p` успехом** (создаёт 0-байтный `wN_run.json`, печатает `<<< [wN] готово`, идёт дальше). Это не моя зона (машину не правлю), но аналитику стоит знать: при 401 машина «проходит» все 5 волн за 3 секунды без единого токена и без досье. Желателен guard: упасть, если `wN_run.json` пуст / вывод содержит `authentication_error`.

## ОТЧЁТ

**Итог: прогон НЕ состоялся — `claude -p` не аутентифицируется (401). Перезапуск вслепую НЕ делал. 5-час окно НЕ сгорело (3 сек, 0 токенов).**

### Что сделал (по плану)
- zip-бэкап: `procedura_backup_20260628_135321.zip` (точка отката).
- Пилотные артефакты убраны в `procedura/artifacts/_pilot/` (w1_candidates, w2_survivors, w2_repair_log, w3_deepened) — старт чистый.
- `chmod +x procedura/orchestrate.sh`; `claude --version` = **2.1.96**.
- Запуск в фоне: `nohup caffeinate -i ./procedura/orchestrate.sh all > .../run_full.log 2>&1 &`, **PID 39221**, старт **2026-06-28 13:53:32 MSK**.

### Что произошло (диагноз)
Процесс отработал и **завершился за 3 секунды** (не повис в фоне). Стартовая строка в норме (`Волны к прогону: w1 w2 w3 w4 w5`, далее `>>> [w1] модель субагентов=haiku`), bash-бага НЕТ — починка оркестратора рабочая. Но:
- все 5 волн отчитались `готово` за 0–1 с с **пустыми токенами** (`токены(in+out)=`);
- созданы **0-байтные** `w1_run.json … w5_run.json`;
- реальных артефактов нет: `w1_candidates.jsonl` … **`w5_dossier.md` отсутствует**.

Смоук-тест подложки (НЕ прогон волны, проверка `claude -p`):
```
$ claude -p "Ответь одним словом: ок"
exit=1
stdout=[Failed to authenticate. API Error: 401 {"type":"error","error":
{"type":"authentication_error","message":"Invalid authentication credentials"},
"request_id":"req_011CcVY4BAhJZmtgzebTUTJ9"}]
```
**Корень: headless-вызовы `claude -p`, которыми оркестратор гоняет волны, не имеют валидной аутентификации.** Это НЕ bash-баг и НЕ проблема флагов/`--json-schema` (та строка-примечание — норма). Это креды окружения для неинтерактивного `claude`. Оркестратор воспринял 401-вывод как пустой успех и прошёл все волны вхолостую → см. `## ВОПРОСЫ §2`.

### Что НЕ трогал
Внутрь `procedura/` (rubric/grid/wave*/schema/anchor/orchestrate) не читал и не правил. Аутентификацию не настраивал (вне границ ОПС-захода + риск). Волны субагентами/Task не гонял. Пустые `wN_run.json` и старый `run_log.txt` оставил как есть для аналитика.

### Где смотреть владельцу
- Лог провала: `procedura/artifacts/run_full.log` и `procedura/artifacts/run_log.txt`.
- Досье (когда прогон реально пройдёт): `procedura/artifacts/w5_dossier.md` — **сейчас отсутствует**.

### Следующий шаг (после решения по кредам — см. `## ВОПРОСЫ §1`)
Когда `claude -p` будет авторизован (напр. `export ANTHROPIC_API_KEY=...` в той же сессии перед запуском), повторить запуск из §2 захода. Бэкап и архив пилота уже сделаны — повтор стартует чисто.
