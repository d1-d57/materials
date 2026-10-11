# Ресёрч: как показывать 12–13-летним результаты по задачам — 2026-10-11 ~01:20

> Выполнил субагент (веб-поиск) по заданию аналитика в сессии «интервью-2»; самоотчёт: «выдано 28 позиций из 33 найденных». Сжато аналитиком без потери ссылок. Платформенная часть Telegram НЕ повторялась — она уже есть: `vanya/zhurnal/2026-09-28_organajzer/RESERCH-telegram-mini-app-dizajn-2026-09-28.md` и аксиомы `vanya/pochta/kod/pochta/veb/VERSTKA.md`.

## 1. Психология обратной связи
- Butler & Nisan 1986 (261 шестиклассник): только «комментарии» дали рост и интерес; баллы на творческих задачах = отсутствию обратной связи. [RYSK](https://blog.mathed.net/2011/08/rysk-butlers-effects-on-intrinsic.html)
- Butler 1988: баллы + комментарий ≈ одни баллы. Guskey: баллы там нормативные (место в классе); падение интереса — в нижних 25 %. Решает, куда знак переводит внимание. [Guskey, EdWeek](https://edweek.org/education/opinion-grades-versus-comments-what-does-the-research-really-tell-us/2019/06)
- Kluger & DeNisi 1996 (607 эффектов): d=.41, но >⅓ случаев — ухудшение; вредит обратная связь про «я»/сравнение. [обзор](https://explore.psychsafety.com/n/kluger-denisi-1996/)
- Hattie & Timperley 2007: уровни задача/процесс/саморегуляция/личность; «молодец» хуже всего; полезное отвечает «что дальше». [BERA](https://www.bera.ac.uk/blog/how-to-optimise-the-use-of-hattie-and-timperleys-feedback-levels-for-student-learning)
- Black & Wiliam 1998: формативное оценивание сильнее у слабых; отметки толкают к сравнению. [SERC](https://serc.carleton.edu/resources/16361.html)
- Koenka et al.: отметки vs ничего — результат выше, мотивация ниже; vs комментарии — хуже по обоим. Lipnevich & Smith 2009: отметка гасит эффект комментария. [Duke](https://scholars.duke.edu/publication/1427115) · [L&S 2009](https://people.bath.ac.uk/edspd/Weblinks/MA_Ass/Resources/Feedback/Lipnevich%20&%20Smith%202009%20EAEA.pdf)
- Growth mindset: эффект интервенций ≈0 (Sisk 2018 d≈0.08; Macnamara 2023); устойчиво — похвала «за ум» вредит (Mueller & Dweck 1998). [Sisk](https://englelab.gatech.edu/articles/2018/Sisk,%20Burgoyne%20et%20al.%20(2018)%20-%20Mindset%20and%20Academic%20Achievement.pdf) · [Macnamara](https://Www.Gwern.net/doc/statistics/meta-analysis/2023-macnamara.pdf) · [Mueller & Dweck](https://www.columbia.edu/cu/psychology/courses/3615/Readings/Mueller_Dweck.pdf)
- Arens 2017 (5135 семиклассников): тревожность растёт при низком положении в классе, через самооценку. [peDOCS](https://www.pedocs.de/volltexte/2021/21754/)
- ⚠ Прямых исследований «явный − против пустой клетки» и «показ всего нерешённого» НЕ найдено.

## 2. Как платформы показывают прогресс
- Khan Academy: 5 уровней владения, уровень падает при ошибках. [help](https://support.khanacademy.org/hc/tr/articles/5548760867853)
- IXL SmartScore: асимметрия штрафа выше 90 — массовые жалобы (анекдотически: уход от трудного). [IXL](https://www.ixl.com/research/smartscore) · [Boddle](https://www.boddlelearning.com/article/ixl-punishes-wrong-answers)
- Duolingo: фарм XP, тревога лиг. [arXiv 2203.16175](https://arxiv.org/pdf/2203.16175)
- Brilliant: мгновенный разбор после ответа; критика — неясен прогресс. [Common Sense](https://www.commonsense.org/education/reviews/brilliant)
- Seesaw: всё приватно, сравнения нет. [help](https://help.seesaw.me/hc/en-gb/articles/203008899)
- Google Classroom: Assigned/Missing/Done со счётчиками; с 2024 «missing» = черновой 0. [Keeler](https://alicekeeler.com/2021/03/22/students-find-missing-work-in-google-classroom/) · [Google](https://workspaceupdates.googleblog.com/2024/07/adding-missing-grade-state-to-gradebook-google-classroom.html)
- МЭШ: тематическое оценивание — средний балл по теме. [Мел](https://mel.fm/novosti/2156043-moskovskiye-roditeli-smogut-otslezhivat-uchebny-progress-shkolnikov-v-mesh)
- Листки матшкол: «+» в ведомость, при неудаче ничего; рейтинг возникает сам и демотивирует слабую половину. [Ковальджи, Канель-Белов](https://arxiv.org/pdf/1502.01893.pdf)

## 3. UI-паттерны
- Прогрессивное раскрытие: не глубже двух уровней, ясная подпись раскрывающего. [NN/g](https://nngroup.com/articles/progressive-disclosure/)
- Аккордеоны на телефоне: обзор, но могут дезориентировать. [NN/g](https://www.nngroup.com/videos/accordions-on-mobile/)
- Формулы на телефоне не переносятся; эмпирики нет. [MathUI](https://ceur-ws.org/Vol-3377/mathui2.pdf)
- Сетка — для сканирования однотипного, список — когда главное текст. [UX Planet](https://uxplanet.org/mobile-ux-design-list-view-and-grid-view-8f129b56fd5b)

## 4. Подводные камни
- Смена режима показа даёт просадку на 1–2 цикла; готовить детей заранее, отметка — информация, не вердикт. [NCME](https://ncme.org/wp-content/uploads/2026/07/Educator-Note-3-Should-You-Show-the-Grade.pdf)
- Отметки хуже для мальчиков и слабых (Швеция); «только комментарии» в 7 кл. по математике — чуть хуже и раздражение у части. [Chartered College](https://my.chartered.college/research-hub/what-does-research-tell-us-about-effective-marking-in-maths/)
- Родительские порталы в реальном времени — тревога, слежка (мнение). [IHE](https://www.insidehighered.com/blogs/just-visiting/shut-down-parent-portals-dangers-real-time-data) · [Т—Ж](https://t-j.ru/dnevnik-lico-uchenika/)
- Лидерборды разжигают сравнение (50 магистрантов). [LMU](https://epub.ub.uni-muenchen.de/96762)

## Выводы для интерфейса (субагент; помечены уровнем доказательности)
- [данные] Никаких рейтингов, средних по классу, мест.
- [практика] Листок «+»/пусто = традиция; пусто = «ещё думаешь».
- [вывод] «−» в ДЗ/КР нейтрален только рядом с задачей и с действием (перерешать/досдать); как голый итог — скорее вреден, особенно для слабых.
- [данные] Оценки не на одном экране с будущими комментариями.
- [данные] Схему показа зафиксировать с первого дня и объяснить детям заранее.
- [практика] Нет экрана «всё нерешённое» и меток «missing»; лучше один следующий шаг.
- [практика] Сетка «+/−/·» по мероприятию, условия свёрнуты, ≤2 уровней.
- [вывод] Условия короткие, длинные выражения отдельной строкой.
