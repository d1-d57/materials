# RUNBOOK.md — как запускать процедуру (Max 20x)

> Самодостаточная папка-машина. Ночной агент берёт контракт ИЗ НЕЁ. Перед прогоном — прочесть этот файл целиком.

## 0. Перед стартом
- **zip-бэкап** `procedura/` (точка отката; папка не под git):
  `zip -rq ../procedura_backup_$(date +%Y%m%d_%H%M%S).zip procedura`
- Убедиться: Claude Code **≥ v2.1.154** (Dynamic Workflows), аккаунт **Max 20x**, права пред-авторизованы.
- `chmod +x procedura/orchestrate.sh`.

## 1. Поток (5 волн, durable после каждой)
```
GATHER → TRIAGE → DEEPEN → ASSEMBLE → DOSSIER
Haiku    Sonnet   Sonnet    Opus(скупо) Sonnet
w1       w2       w3        w4          w5
jsonl    jsonl    jsonl     json        md
```
Durable-цепь в `artifacts/`:
`w1_candidates.jsonl → w2_survivors.jsonl → w3_deepened.jsonl → w4_assembly.json → w5_dossier.md`

## 2. Вызов на волну
Каждая волна — отдельный `claude -p` (workflow межсессийно не резюмится):
```bash
claude -p "выполни procedura/waveN по контракту" \
  --output-format json \
  --json-schema procedura/scorecard.schema.json \
  --bare \
  --allowedTools "Read,Write,Edit,Bash,Agent" \
  --permission-mode acceptEdits
```
`--json-schema` впечатывает `scorecard.schema.json` в `structured_output` (типизированный контракт на уровне CLI). Оркестратор `orchestrate.sh` оборачивает это и проставляет тиринг.

## 3. Тиринг моделей (раздельные бакеты лимитов → не конкурируют)
- `CLAUDE_CODE_SUBAGENT_MODEL` на волну: **w1=haiku**, **w2/w3/w5=sonnet**.
- **Opus — ТОЛЬКО воркеры ядра w4** (через `model:` в их определении), не на уровне оркестратора.
- Рубрику + якорь **кэшируем** (shared context) — не считается в ITPM, множит эффективный инпут.

## 4. Запуск
```bash
cd "<...>/2026-06-28_procedura-poiska"
./procedura/orchestrate.sh all        # все волны
./procedura/orchestrate.sh w3         # resume с волны 3 (после троттла)
./procedura/orchestrate.sh w3 w4 w5   # с 3-й до конца
```

## 5. Оговорки Max 20x (несущее)
- **ОДИН инстанс.** Параллельные выжигают 5-час окно вдвое быстрее.
- Прогон должен влезть в **одно 5-час окно**; волны нарезаны под комфортный размер.
- **Opus только в ядре w4** (недельные Opus-капы душат; авто Opus→Sonnet на 50% окна).
- **Троттл между волнами** → resume следующей волной (durable на диске, предыдущие готовы).
- **Троттл ВНУТРИ волны** → волна перезапускается целиком (durable прошлых волн не теряется).

## 6. Resume (несущее)
Workflow сам межсессийно НЕ резюмится. Resume = перезапустить нужную волну: `./orchestrate.sh wN`. Всё, что до неё, уже лежит в `artifacts/`.

## 7. Анти-хак (на что смотреть в прогоне)
- Якорь `anchor.md` сверяется каждое поколение ASSEMBLE.
- **TRIPWIRE:** счёт судьи растёт, а ранг к якорю — нет → СТОП, флаг, выигрышу не верить. Трейс — в `w4_assembly.json`.
- Судья — свежий изолированный контекст + иной тир, чем автор.

## 8. Выход
`artifacts/w5_dossier.md` — досье решения, к которому просыпается владелец (финальный вкусовой проход за ним).

**Время + токены прогона:** `artifacts/run_log.txt` — время каждой волны и общее; токены (in+out) — best-effort из JSON-ответа `claude -p` каждой волны. Точный счётчик токенов всегда виден в самом Claude Code (`/cost`).
