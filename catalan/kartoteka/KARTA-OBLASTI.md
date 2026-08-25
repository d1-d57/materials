---
tab: Карта картотеки
status: chernovik
poryadok: 0
registr: рабочий
---

# КАРТА ОБЛАСТИ — картотека курса «Числа Каталана»: находки захода matbaza-skeleta

> Рабочая память агента (STANDART: `fibonacci/kartoteka/STANDART-uzla.md`): карточка = структурная находка + указатель источник, не определение. Каждый `id`, упомянутый в чьих-то `связях`, обязан резолвиться здесь. Карточки лежат по одной на файл рядом с этой картой.

## Индекс по роду

- **затравка:** `kart-starter-parametr`
- **мостик:** `kart-normirovka-starta` `kart-polyusa-spektr` `kart-jtp-mesto` `kart-okruzhnost-kanal`
- **утверждение:** `kart-porog-ngr` `kart-izobrazheniya-otrazhenie` `kart-q-kontinuanty`
- **находка:** `kart-obshchee-prostee` `kart-chebyshev-smysl`

---

## Резолв id (суть одной строкой)

| id | суть | файл |
|---|---|---|
| `kart-starter-parametr` | старт обязан быть параметром: при $x=0$ рост $m$ даёт луч (28 навсегда), не прямую (56) | [карточка](kart-starter-parametr.md) |
| `kart-porog-ngr` | порог $n\ge r$ биномиальной специализации точный: при $n \lt r$ выживают отражения $j\ne0$ | [карточка](kart-porog-ngr.md) |
| `kart-normirovka-starta` | площадь от старта = стандартная минус моном ⇒ $q$-ответ не зависит от сдвига старта | [карточка](kart-normirovka-starta.md) |
| `kart-izobrazheniya-otrazhenie` | метод изображений и принцип отражения — один сюжет; с весом площади показатели квадратичны | [карточка](kart-izobrazheniya-otrazhenie.md) |
| `kart-polyusa-spektr` | полюса дроби = корни $U_{m+1}$ = спектр оператора; следствие — кристаллографическое ограничение | [карточка](kart-polyusa-spektr.md) |
| `kart-q-kontinuanty` | В1 закрыт: при произвольных концах и весе площади форма есть ($q$-континуанты); спектра при $q\ne1$ нет | [карточка](kart-q-kontinuanty.md) |
| `kart-jtp-mesto` | В2: JTP входит инструментом; обобщение с JTP как специализацией — Вейль — Кац/Макдональд, не путевой объект | [карточка](kart-jtp-mesto.md) |
| `kart-obshchee-prostee` | В3: общее доказывается не дороже частного (изображения/спектр/континуанты), частное требует разборов выживания | [карточка](kart-obshchee-prostee.md) |
| `kart-chebyshev-smysl` | В4: Чебышёв = правило Якоби для обратной матрицы шага — два минора-хвоста на полный определитель-спектр | [карточка](kart-chebyshev-smysl.md) |
| `kart-okruzhnost-kanal` | окружность — второй канал оператора шага; площади без края нет, переход отрезок↔окружность нечестен | [карточка](kart-okruzhnost-kanal.md) |

## Нити (маршруты)

- **«почему объект устроен так»:** `kart-starter-parametr` → `kart-porog-ngr` → `kart-normirovka-starta` → `kart-okruzhnost-kanal`
- **«четыре взгляда на одну формулу»:** `kart-chebyshev-smysl` → `kart-polyusa-spektr` → `kart-izobrazheniya-otrazhenie` → `kart-q-kontinuanty`
- **«место классики»:** `kart-jtp-mesto` → `kart-izobrazheniya-otrazhenie`
