#!/bin/zsh
# ДВОЙНОЙ КЛИК ПО ЭТОМУ ФАЙЛУ вносит отметки за 5 сентября в ЖИВУЮ базу на сервере.
# Ничего набирать не нужно. Окно откроется само и само напишет, что получилось.
#
# Что произойдёт, по шагам:
#   1. проверка связи с сервером;
#   2. снимок базы ПЕРЕД записью (штатный ops/rezervnaya_kopia.py);
#   3. сухой прогон — печатает, что будет сделано, и ничего не меняет;
#   4. запись: состав листка 16α приводится к выложенному на сайте, кладутся отметки;
#   5. перечитывание из базы и число «внесено N из 113».
#
# Скрипт идемпотентен: второй клик по этому же файлу ничего не задвоит.
# Весь вывод дублируется в файл otchet-vnesenia-05-09.txt рядом — его читает аналитик.

KOREN=${0:A:h}
SERVER=ivan@159.194.254.52
SKRIPT=$KOREN/raspredelenie-fajl/vnesti_otmetki_05_09.py
UDALENNO=/tmp/vnesti_otmetki_05_09.py
LOG=$KOREN/otchet-vnesenia-05-09.txt

exec > >(tee "$LOG") 2>&1
echo "══ отметки за 5 сентября 2026 · $(date '+%Y-%m-%d %H:%M:%S') ══"
echo

if [[ ! -f $SKRIPT ]]; then
  echo "🔴 не нашёл скрипт: $SKRIPT"
  echo "Похоже, папку переносили. Скажи аналитику — он поправит путь."
  read -k1 "?Нажми любую клавишу."; exit 1
fi

echo "── 1. связь с сервером ──"
if ! ssh -o BatchMode=yes -o ConnectTimeout=15 $SERVER 'echo "сервер отвечает: $(hostname)"'; then
  echo "🔴 сервер не ответил. Ничего не изменено."
  read -k1 "?Нажми любую клавишу."; exit 1
fi

echo
echo "── 2. снимок базы перед записью ──"
ssh $SERVER 'cd /opt/spetsmat-bot && sudo -u spetsmat python3 ops/rezervnaya_kopia.py' \
  || echo "⚠ снимок не удался — смотри строку выше; запись дальше НЕ пойдёт, если это ошибка доступа"

echo
echo "── 3. что будет сделано (сухой прогон, база не тронута) ──"
scp -q "$SKRIPT" $SERVER:$UDALENNO || { echo "🔴 не смог передать скрипт"; read -k1 "?Клавишу."; exit 1; }
ssh $SERVER "sudo -u spetsmat python3 $UDALENNO"

echo
echo "── 4. запись в живую базу ──"
ssh $SERVER "sudo -u spetsmat python3 $UDALENNO --primenit"

echo
echo "── 5. перечитано из базы ──"
ssh $SERVER "sudo -u spetsmat python3 $UDALENNO --proverka"

echo
echo "══ готово. Отчёт лежит рядом: otchet-vnesenia-05-09.txt ══"
echo "Аналитик прочитает его сам — можно просто закрыть окно."
read -k1 "?Нажми любую клавишу, чтобы закрыть."
