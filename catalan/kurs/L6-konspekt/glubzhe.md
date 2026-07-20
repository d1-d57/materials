---
tab: Глубже
status: chernovik
poryadok: 2
registr: читаемый
---

# Глубже: рекурренты · честное доказательство · Чжун–Феллер

## Как заполнять треугольник Нараяны

Простого паскалева «сложи двух соседей сверху» у Нараяны **нет** (проверил — аддитивной рекурренты с постоянными коэффициентами не существует; треугольник глубже паскалева). Но заполнить рекуррентно можно двумя способами.

*Техфакт. Построчно, мультипликативно.* В строке $n$ начинаешь с $N(n,1)=1$ и идёшь вправо: $N(n,k) = N(n,k-1)\cdot\dfrac{(n-k+1)(n-k+2)}{k(k-1)}$. Строка $n=6$ рождается за пять умножений: $1 \to 15 \to 50 \to 50 \to 15 \to 1$.

*Логика. Первого возврата (комбинаторная).* Путь Дика $= U\,P_1\,D\,P_2$; пиков ровно $\operatorname{peaks}(P_1)+\operatorname{peaks}(P_2)$, плюс один, если $P_1$ пусто. Отсюда $N(n,k) = N(n-1,k-1) + \sum_{i\ge 1,\ j} N(i,j)\,N(n-1-i,\ k-j)$.

Обе — тени одного факта: производящая функция $F(x,y)=\sum N(n,k)x^n y^k$ из того же первого возврата удовлетворяет квадратному уравнению

$$xF^2 + (xy - x - 1)\,F + 1 = 0,$$

которое при $y=1$ превращается в каталановское $xF^2 - F + 1 = 0$. Вот и мост к производящим функциям.

<div style="font-family:'SF Mono',ui-monospace,monospace;text-align:center;line-height:1.75;font-size:.95em;color:#2b2b33">1<br>1&nbsp;&nbsp;&nbsp;1<br>1&nbsp;&nbsp;&nbsp;3&nbsp;&nbsp;&nbsp;1<br>1&nbsp;&nbsp;&nbsp;6&nbsp;&nbsp;&nbsp;6&nbsp;&nbsp;&nbsp;1<br>1&nbsp;&nbsp;10&nbsp;&nbsp;20&nbsp;&nbsp;10&nbsp;&nbsp;1<br>1&nbsp;&nbsp;15&nbsp;&nbsp;50&nbsp;&nbsp;50&nbsp;&nbsp;15&nbsp;&nbsp;1</div>

## Честное доказательство формулы (через отражение)

> поле: Каюсь: прежний «путь через баллотное условие» был с неверным множителем (там неявно $1/n$, а реальная доля путей Дика среди двусторонних — $n/(k(n-k+1))$). Вот корректная версия — и она на твоём инструменте, отражении.

Путь Дика с $k$ пиками записывается как $U^{a_1}D^{b_1}\cdots U^{a_k}D^{b_k}$, все $a_i,b_i\ge 1$, $\sum a_i = \sum b_i = n$. Пусть $A_i = a_1+\dots+a_i$ и $B_i = b_1+\dots+b_i$. Высота после $i$-го спуска равна $A_i - B_i$, поэтому **условие Дика** равносильно $A_i \ge B_i$ для всех $i$.

Значит надо сосчитать пары цепочек $0\lt A_1\lt\dots\lt A_{k-1}\lt n$ и $0\lt B_1\lt\dots\lt B_{k-1}\lt n$ с $A_i\ge B_i$. Это ровно «две непересекающиеся дорожки»: **отражение** (лемма Линдстрёма–Гесселя–Вьенно) даёт определитель $2\times2$

$$N(n,k)=\binom{n-1}{k-1}^{2}-\binom{n-1}{k}\binom{n-1}{k-2}=\frac1n\binom nk\binom n{k-1}.$$

Отсюда сразу $\sum_k N(n,k)=C_n$ (каждый путь имеет от $1$ до $n$ пиков) и симметрия $N(n,k)=N(n,n{+}1{-}k)$.

## Чжун–Феллер

*Статус.* Среди $C(2n,n)$ петель (длины $2n$, из $0$ в $0$) число тех, у кого ровно $2k$ шагов лежит **выше оси**, одинаково для всех $k=0,\dots,n$ и равно $C_n$. То есть $C(2n,n)=(n+1)\,C_n$.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 470" font-size="16"><rect width="980" height="470" fill="#fbfaf7"/><text x="40" y="46" font-family="Georgia, 'Times New Roman', serif" font-size="26" fill="#2b2b33">Чжун–Феллер: (n+1) равных групп по времени над осью</text><text x="40" y="76" font-family="'Helvetica Neue', Arial, sans-serif" font-size="15" fill="#8a8a95">n=2: все C(4,2)=6 петель из 0 в 0. Зелёное — шаги выше оси, красное — ниже. Групп три, в каждой по C₂=2.</text><text x="130" y="130" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" fill="#2b2b33">0 шагов выше: <tspan font-weight="bold">2</tspan></text><line x1="90" y1="200" x2="170" y2="200" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="90" y1="200" x2="110" y2="217" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="110" y1="217" x2="130" y2="200" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="130" y1="200" x2="150" y2="217" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="150" y1="217" x2="170" y2="200" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><circle cx="90" cy="200" r="2.4" fill="#2b2b33"/><circle cx="110" cy="217" r="2.4" fill="#2b2b33"/><circle cx="130" cy="200" r="2.4" fill="#2b2b33"/><circle cx="150" cy="217" r="2.4" fill="#2b2b33"/><circle cx="170" cy="200" r="2.4" fill="#2b2b33"/><line x1="90" y1="330" x2="170" y2="330" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="90" y1="330" x2="110" y2="347" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="110" y1="347" x2="130" y2="364" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="130" y1="364" x2="150" y2="347" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="150" y1="347" x2="170" y2="330" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><circle cx="90" cy="330" r="2.4" fill="#2b2b33"/><circle cx="110" cy="347" r="2.4" fill="#2b2b33"/><circle cx="130" cy="364" r="2.4" fill="#2b2b33"/><circle cx="150" cy="347" r="2.4" fill="#2b2b33"/><circle cx="170" cy="330" r="2.4" fill="#2b2b33"/><text x="440" y="130" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" fill="#2b2b33">2 шага выше: <tspan font-weight="bold">2</tspan></text><line x1="400" y1="200" x2="480" y2="200" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="400" y1="200" x2="420" y2="183" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="420" y1="183" x2="440" y2="200" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="440" y1="200" x2="460" y2="217" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="460" y1="217" x2="480" y2="200" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><circle cx="400" cy="200" r="2.4" fill="#2b2b33"/><circle cx="420" cy="183" r="2.4" fill="#2b2b33"/><circle cx="440" cy="200" r="2.4" fill="#2b2b33"/><circle cx="460" cy="217" r="2.4" fill="#2b2b33"/><circle cx="480" cy="200" r="2.4" fill="#2b2b33"/><line x1="400" y1="330" x2="480" y2="330" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="400" y1="330" x2="420" y2="347" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="420" y1="347" x2="440" y2="330" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/><line x1="440" y1="330" x2="460" y2="313" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="460" y1="313" x2="480" y2="330" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><circle cx="400" cy="330" r="2.4" fill="#2b2b33"/><circle cx="420" cy="347" r="2.4" fill="#2b2b33"/><circle cx="440" cy="330" r="2.4" fill="#2b2b33"/><circle cx="460" cy="313" r="2.4" fill="#2b2b33"/><circle cx="480" cy="330" r="2.4" fill="#2b2b33"/><text x="750" y="130" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" fill="#2b2b33">4 шагов выше: <tspan font-weight="bold">2</tspan></text><line x1="710" y1="200" x2="790" y2="200" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="710" y1="200" x2="730" y2="183" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="730" y1="183" x2="750" y2="166" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="750" y1="166" x2="770" y2="183" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="770" y1="183" x2="790" y2="200" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><circle cx="710" cy="200" r="2.4" fill="#2b2b33"/><circle cx="730" cy="183" r="2.4" fill="#2b2b33"/><circle cx="750" cy="166" r="2.4" fill="#2b2b33"/><circle cx="770" cy="183" r="2.4" fill="#2b2b33"/><circle cx="790" cy="200" r="2.4" fill="#2b2b33"/><line x1="710" y1="330" x2="790" y2="330" stroke="#9a9488" stroke-width="1.4" stroke-dasharray="3 3"/><line x1="710" y1="330" x2="730" y2="313" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="730" y1="313" x2="750" y2="330" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="750" y1="330" x2="770" y2="313" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><line x1="770" y1="313" x2="790" y2="330" stroke="#2e7d4f" stroke-width="3" stroke-linecap="round"/><circle cx="710" cy="330" r="2.4" fill="#2b2b33"/><circle cx="730" cy="313" r="2.4" fill="#2b2b33"/><circle cx="750" cy="330" r="2.4" fill="#2b2b33"/><circle cx="770" cy="313" r="2.4" fill="#2b2b33"/><circle cx="790" cy="330" r="2.4" fill="#2b2b33"/><text x="40" y="454" font-family="Georgia, 'Times New Roman', serif" font-size="16" fill="#2b2b33">Значит C(2n,n) = (n+1)·Cₙ: здесь 6 = 3·2. Время над осью распределено РОВНО.</text></svg>
<figcaption>$n=2$: все 6 петель делятся по времени над осью на три равные группы по 2. Зелёное — выше оси, красное — ниже.</figcaption>
</figure>

Доказательство — «нижняя точка / разрежь-переставь у пересечения оси», тот же образ, что в цикл-лемме.

Связь с курсом: цикл-лемма для суммы $+1$ — это «ровно один хороший поворот». Общий случай, сумма $+l$, даёт ровно $l$ хороших поворотов — **баллотные числа**. Чжун–Феллер — усиленная версия, где каждый из $l$ нулей получает свою роль (Кирстед–Троттер); Снивли–Уэст выводят CF именно из неё. Предел CF — закон арксинуса (вне школьного курса).

## Карта методов и две оставшиеся лекции

За курс задействованы: триангуляции (раздутие/рекуррента), отражение, цикл-лемма (частный случай), биекции плюс первый возврат, возвращение/баллотировка. Ещё в области есть:

- **Общая цикл-лемма → баллот → Чжун–Феллер → Нараяна** — один приём, разные статистики.
- **Производящие функции** — алгебраическое зеркало: первый возврат превращается в квадрат, из него — замкнутые формулы (Лагранж).
- **Определители / непересекающиеся пути (LGV)** — то, чем доказали Нараяну; даёт и формулу крюков.

Предложение (обсуждаемо): предпоследняя лекция — «веер» (общая цикл-лемма → баллот → CF → Нараяна); последняя — производящие функции как другой метод и передышка (держать установку «ГФ = запакованный первый возврат», не «ряды ради рядов»).

> поле:foot Черновик-конспект, вкладка «Глубже». Сверено кодом: обе рекурренты, определитель $=\frac1n\binom nk\binom n{k-1}$, ГФ-квадрат, Чжун–Феллер ($n\le4$). Полный вывод LGV-определителя — по запросу.
