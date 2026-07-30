# KORPUS — файлы `kurs leto 2026/zhurnal/` напрямую (без арки-подпапки)

Сырые кандидаты в уроки фабрике. Без закона, без вердикта, без морали.

## kurs leto 2026/zhurnal/kod_uborka-renumber.md

### Renumber порядок в istochnik/ осиротил собранный HTML и разбросал стале-номера «ЛN» по прозе другой лекции
АДРЕС: kurs leto 2026/zhurnal/kod_uborka-renumber.md#ЗАДАНИЕ, строка 5
ЦЕНА: build.py именует выходной HTML по porjadok → появился новый _out/L6-optimizaciya.html, старый _out/L2-optimizaciya.html осиротел; в L4-kriptografiya.md устарели голые номера «ЛN» (сами ссылки →[id] целы)

### beklog.md ссылается на удалённый _out/L2-optimizaciya.html — check_docs.py упал, ссылку не починили
АДРЕС: kurs leto 2026/zhurnal/kod_uborka-renumber.md#ВОПРОСЫ, строка 84
ЦЕНА: check_docs.py теперь падает на этом одном нарушении (exit 1) — раньше был зелёным, потому что осиротевший файл ещё физически лежал в _out/
