#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборщик сайта курса. Один источник — god.json, одна команда — этот файл.

    python3 build.py            # собрать в dist/
    python3 build.py --proverit # только счёт, ничего не писать

Три экрана (ТЗ-sajt.md §3):
  dist/index.html          — год целиком, календарь по неделям, тумблер курс/кружок
  dist/blok-<slug>.html    — блок: опорные точки из karta, опорные задачи, список недель
  dist/nedelya-NN.html     — занятие: пустой каркас под будущее наполнение

Весь видимый текст берётся из god.json либо из белого списка god.json["interfejs"].
Ничего не сочиняется — проверяется gejt_teksta.py.
"""
import json, os, re, sys, html

TUT = os.path.dirname(os.path.abspath(__file__))
IST = os.path.join(TUT, 'god.json')
DIST = os.path.join(TUT, 'dist')

# ── нарезка года на недели ─────────────────────────────────────────────────
# Неделя = пара = два подряд идущих урока потока четверти. В поток входят
# только blok и kontrolnaya: kruzhok — параллельная дорожка (третий урок),
# vne-setki по определению вне сетки. Неделя может делиться между двумя
# элементами — это законно и должно быть видно.
POTOK = ('blok', 'kontrolnaya')

# Разделитель перечислений в данных — ТОЧКА С ПРОБЕЛАМИ. Голая «·» встречается
# внутри формул («8·7», «8·7/2») и резать по ней нельзя: так формула рвётся надвое.
RAZD = ' · '


def slug(s):
    tab = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z',
           'и':'i','й':'j','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
           'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch',
           'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'}
    out = []
    for ch in s.lower():
        if ch in tab:
            out.append(tab[ch])
        elif ch.isalnum():
            out.append(ch)
        else:
            out.append('-')
    return re.sub(r'-+', '-', ''.join(out)).strip('-')


def razobrat(g):
    """Возвращает (chetverti, bloki, nedeli).

    chetvert: nomer, daty, chasy, potok[], kruzhok, vne_setki[], nedeli[]
    blok:     imya, slug, chasy, domen, na_styke, podzag, karta, opornye, nedeli[]
    nedelya:  nomer, chetvert, doli[(element, chasov_v_neделе)]
    """
    chetverti, bloki, nedeli = [], [], []
    n = 0
    for c in g['chetverti']:
        potok = [e for e in c['elementy'] if e['tip'] in POTOK]
        summa = sum(e['chasy'] for e in potok)
        if summa != c['chasy']:
            sys.exit('ЧЕТВЕРТЬ %s: поток даёт %d уроков, в chasy стоит %d — данные не подгоняю'
                     % (c['nomer'], summa, c['chasy']))
        if summa % 2:
            sys.exit('ЧЕТВЕРТЬ %s: %d уроков — нечётно, неделя переползает границу четверти'
                     % (c['nomer'], summa))
        ch = {'nomer': c['nomer'], 'daty': c['daty'], 'chasy': c['chasy'],
              'potok': [], 'kruzhok': None, 'vne_setki': [], 'nedeli': []}
        # поток в уроках: для каждого урока — его элемент
        uroki, smeshenie = [], 0
        for e in potok:
            item = dict(e)
            item['_start'] = smeshenie          # первый урок элемента, 0-based внутри четверти
            item['_ch'] = ch
            if e['tip'] == 'blok':
                item['slug'] = slug(e['imya'])
                item['nedeli'] = []
                bloki.append(item)
            ch['potok'].append(item)
            uroki += [item] * e['chasy']
            smeshenie += e['chasy']
        for e in c['elementy']:
            if e['tip'] == 'kruzhok':
                k = dict(e)
                k['slug'] = 'kruzhok-' + slug(c['nomer'])
                k['nedeli'] = []
                k['_ch'] = ch
                ch['kruzhok'] = k
            elif e['tip'] == 'vne-setki':
                ch['vne_setki'].append(dict(e))
        for k in range(0, len(uroki), 2):
            n += 1
            a, b = uroki[k], uroki[k + 1]
            doli = [(a, 2)] if a is b else [(a, 1), (b, 1)]
            ned = {'nomer': n, 'chetvert': ch, 'doli': doli, '_start': k}
            nedeli.append(ned)
            ch['nedeli'].append(ned)
            for el, _ in doli:
                if el['tip'] == 'blok':
                    el['nedeli'].append(ned)
            if ch['kruzhok'] is not None:
                ch['kruzhok']['nedeli'].append(ned)
        chetverti.append(ch)
    return chetverti, bloki, nedeli


# ── вид ────────────────────────────────────────────────────────────────────
E = lambda s: html.escape(str(s), quote=True)

# Цвет — по разделу математики. Пять земляных тонов одной насыщенности:
# ни один не кричит громче другого, но все громче контроля.
CSS = """
:root{
  --paper:#f6f1e7; --card:#fcfaf5; --ink:#2b2724; --ink2:#4f4942;
  --soft:#6b6155; --faint:#9b9186; --line:#e3dac7; --line2:#efe8d8;
  --acc:#b3503c; --accbg:#f7e8e0;
  --serif:Georgia,'Times New Roman',serif;
  --sans:-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
  --d-O:#a68a4e; --d-A:#b25f3c; --d-K:#5f7f4a; --d-V:#4a7292; --d-D:#7d4f78;
  --d-Z:#3f7d75;
  --ktr:#a79d90; --ktr-bg:#eae3d5;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans);
  -webkit-font-smoothing:antialiased}
a{color:inherit}
.oborot{max-width:1680px;margin:0 auto;padding:0 34px 20px}

/* ── шапка ── */
.shapka{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap;
  padding:22px 0 15px;border-bottom:1px solid var(--line)}
.shapka h1{font:700 30px/1.15 var(--serif);margin:0;letter-spacing:-.01em}
.shapka .razmer{font:14px/1.4 var(--serif);color:var(--ink2)}
.demo{font:600 11.5px/1 var(--sans);text-transform:uppercase;letter-spacing:.12em;
  color:var(--acc);background:var(--accbg);border-radius:20px;padding:7px 14px}
.nazad{font:600 13.5px/1 var(--sans);color:var(--soft);text-decoration:none;
  border-bottom:1px solid var(--line);padding-bottom:2px}
.nazad:hover{color:var(--acc);border-bottom-color:var(--acc)}
.shapka .spacer{flex:1}

/* ── тумблер: две радиокнопки, ни строки JS ── */
.tumbler>input{position:absolute;opacity:0;width:0;height:0;pointer-events:none}
.perekl{display:inline-flex;gap:3px;background:var(--card);border:1px solid var(--line);
  border-radius:24px;padding:3px;margin:16px 0 0}
.perekl label{font:600 13px/1 var(--sans);color:var(--soft);padding:8px 17px;
  border-radius:22px;cursor:pointer;user-select:none}
.perekl label:hover{color:var(--ink)}
#t-kurs:checked~.perekl label[for=t-kurs],
#t-kruzhok:checked~.perekl label[for=t-kruzhok]{background:var(--ink);color:var(--paper)}
#t-kurs:focus-visible~.perekl label[for=t-kurs],
#t-kruzhok:focus-visible~.perekl label[for=t-kruzhok]{outline:2px solid var(--acc);outline-offset:2px}
#t-kruzhok:checked~.kalendar .tr-kurs{display:none}
#t-kurs:checked~.kalendar .tr-kruzhok{display:none}

/* ── четверть ── */
/* Четверть — две колонки: слева подпись, справа лента и линейка недель.
   «N недель» стоит вплотную к линейке, а не в шапке: иначе связь между
   пронумерованными клетками и словом «недели» приходится угадывать
   (находка верификатора понятности 2026-08-20). */
.chetv{margin:16px 0 0;display:grid;grid-template-columns:100px minmax(0,1fr);
  column-gap:12px;align-items:start}
.chetv-hd{grid-column:1;grid-row:1;padding-top:2px}
.chetv-hd .rim{font:700 21px/1 var(--serif);color:var(--ink);display:inline}
.chetv-hd .cw{font:600 11.5px/1 var(--sans);text-transform:uppercase;letter-spacing:.09em;
  color:var(--faint);margin-left:6px}
.chetv-hd .dts{display:block;font:13px/1.35 var(--serif);color:var(--ink2);margin-top:6px}
.chetv .lenta{grid-column:2;grid-row:1}
.nw{grid-column:1;grid-row:2;text-align:right;font:12px/24px var(--sans);
  color:var(--faint);padding-right:2px}
.chetv .linejka{grid-column:2;grid-row:2}
.chetv .vne{grid-column:2;grid-row:3;justify-self:start}

/* лента: сетка в УРОКАХ, 20 колонок на все четверти — уроки выровнены по
   вертикали, а короткая четверть честно не достаёт до правого края */
.lenta{display:grid;grid-template-columns:repeat(20,minmax(0,1fr));
  grid-auto-rows:124px;gap:5px;align-items:stretch}
/* у кружка одна дорожка на четверть — низкая лента, чтобы не зияла пустотой */
.tr-kruzhok .lenta{grid-auto-rows:92px}
.linejka{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:5px;margin-top:4px}

/* блок — большой прямоугольник, главная масса страницы */
.blok{position:relative;display:flex;flex-direction:column;justify-content:flex-start;
  border-radius:7px;padding:11px 11px 0;text-decoration:none;overflow:hidden;
  background:var(--c);color:#fdfbf6;transition:transform .12s ease, box-shadow .12s ease}
.blok:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(43,39,36,.22)}
.blok .im{font:700 18px/1.14 var(--serif);letter-spacing:-.005em;padding-right:62px}
.blok .pz{font:11.5px/1.28 var(--sans);color:rgba(253,251,246,.82);margin-top:4px;
  flex:0 1 auto;min-height:0;overflow:hidden;max-height:3.84em}
.blok .niz{margin-top:auto;padding-bottom:7px;min-width:0;flex:none;position:relative;
  display:flex;align-items:center;gap:8px}
.blok .dm{font:600 9.5px/1.15 var(--sans);text-transform:uppercase;min-width:0;
  letter-spacing:.045em;color:rgba(253,251,246,.76);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.blok .ug{position:absolute;top:10px;right:11px;display:flex;align-items:center;gap:7px}
.blok .ch{font:600 10.5px/1 var(--sans);color:rgba(253,251,246,.7);white-space:nowrap}
/* клетки недель внутри блока — белые волоски по границам пар */
.blok .setka{position:absolute;inset:0;display:grid;pointer-events:none}
.blok .setka i{border-left:1px solid rgba(253,251,246,.34)}
.blok .setka i:first-child{border-left:0}
.blok .setka i.pol{border-left-style:dashed;border-left-color:rgba(253,251,246,.2)}
/* на стыке двух разделов — нарочная двухцветная диагональ */
/* Блок на стыке двух разделов красится нарочно двухтонно. Тона — ДВА ОТТЕНКА
   СОБСТВЕННОГО раздела: второго раздела в god.json нет, и красить блок цветом
   соседа значило бы утверждать факт, которого владелец не давал. */
.blok.styk{background:
  repeating-linear-gradient(126deg,
    var(--c) 0 15px,
    color-mix(in srgb, var(--c) 72%, #fdfbf6) 15px 30px)}
.blok .styk-l{flex:none;font:600 9px/1 var(--sans);text-transform:uppercase;
  letter-spacing:.08em;color:rgba(253,251,246,.9);
  border:1px solid rgba(253,251,246,.45);border-radius:12px;padding:3px 6px}

/* контрольная — узкая деликатная полоска, прижата к низу ленты */
.ktr{align-self:end;height:24px;border-radius:5px;background:var(--ktr-bg);
  border:1px solid var(--line);display:flex;align-items:center;justify-content:center;
  padding:0 1px;overflow:hidden;text-decoration:none}
.ktr.chetv{height:16px;background:transparent;border-style:dashed}
.ktr:hover{border-color:var(--acc)}
.ktr:hover .k{color:var(--acc)}
.ktr .k{font:600 8px/1.1 var(--sans);text-transform:lowercase;letter-spacing:0;
  color:var(--ktr);white-space:nowrap;text-overflow:ellipsis;overflow:hidden}

/* линейка недель — сплошной хребет 1..33, расщеплённая неделя двухцветна */
.ned{position:relative;display:block;height:24px;border-radius:4px;text-decoration:none;
  font:600 11px/24px var(--sans);color:var(--ink2);text-align:center;
  background:var(--nb);border:1px solid var(--line2)}
.ned:hover{color:var(--acc);border-color:var(--acc)}
.ned.split{box-shadow:inset 0 0 0 1px var(--card)}

/* вне сетки */
.vne{display:inline-flex;align-items:baseline;gap:9px;margin-top:7px;padding:5px 11px;
  border:1px dashed var(--line);border-radius:5px;background:var(--card)}
.vne .i{font:600 13px/1 var(--serif);color:var(--ink2)}
.vne .c{font:11.5px/1 var(--sans);color:var(--faint)}

/* ── страница блока / занятия ── */
.uzko{max-width:1180px;margin:0 auto;padding:0 34px 80px}
.zag{padding:34px 0 0}
.zag h1{font:700 38px/1.1 var(--serif);margin:0 0 12px;letter-spacing:-.015em}
.zag .pz{font:19px/1.5 var(--serif);color:var(--ink2);margin:0 0 16px;max-width:44em}
.metki{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:6px}
.metka{font:600 11px/1 var(--sans);text-transform:uppercase;letter-spacing:.09em;
  color:#fdfbf6;background:var(--c);border-radius:20px;padding:7px 13px;
  text-decoration:none;display:inline-block}
a.metka:hover{filter:brightness(1.12)}
.metka.tih{color:var(--soft);background:transparent;border:1px solid var(--line)}
.metka .tochka{font-style:normal;color:var(--faint);margin:0 6px}
.metka b{font-weight:600;color:var(--ink2);text-transform:none;letter-spacing:.02em}
.grp{font:12.5px/1.4 var(--sans);text-transform:uppercase;letter-spacing:.09em;
  color:var(--faint);margin:0 0 16px}
.sect{margin:44px 0 0;padding-top:26px;border-top:1px solid var(--line)}

.tochki{counter-reset:t;margin:0;padding:0;list-style:none;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:26px 40px}
.tochki li{counter-increment:t;position:relative;padding-left:38px}
.tochki li::before{content:counter(t);position:absolute;left:0;top:1px;
  width:26px;height:26px;border-radius:50%;background:var(--c);color:#fdfbf6;
  font:700 12.5px/26px var(--sans);text-align:center}
.tochki .t{font:700 20px/1.28 var(--serif);margin:0 0 9px}
.tochki .ch{display:flex;flex-wrap:wrap;gap:6px}
.tochki .ch span{font:14px/1.4 var(--sans);color:var(--ink2);background:var(--card);
  border:1px solid var(--line2);border-radius:5px;padding:5px 10px}

.zadachi{display:flex;flex-wrap:wrap;gap:8px;margin:0}
.zadachi span{font:15px/1.45 var(--serif);color:var(--ink2);background:var(--card);
  border:1px solid var(--line2);border-radius:6px;padding:8px 13px}

.spisok{margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));
  gap:0 30px}
.spisok a{display:flex;align-items:baseline;gap:11px;padding:12px 2px;
  border-bottom:1px solid var(--line2);text-decoration:none}
.spisok a:hover .n{color:var(--acc)}
.spisok .n{font:600 17px/1.3 var(--serif);color:var(--ink)}
.spisok .d{font:12.5px/1.3 var(--sans);color:var(--faint);margin-left:auto}

.karkas{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:30px;
  margin-top:8px}
.karkas .box{background:var(--card);border:1px solid var(--line2);border-radius:8px;
  padding:20px 22px;min-height:190px}
.karkas .box .grp{margin-bottom:0}

.podval{margin-top:56px;padding-top:18px;border-top:1px solid var(--line);
  display:flex;gap:16px;flex-wrap:wrap;align-items:center}

/* узкое окно: имя мельче, чтобы не лезло под угол — но подзаголовок ОСТАЁТСЯ:
   он и есть то, ради чего на календарь смотрят */
@media(max-width:1400px){
  .blok .im{font:700 16px/1.15 var(--serif);padding-right:56px}
  .blok .pz{font-size:11px}
  .blok .dm{font-size:9px;letter-spacing:.03em}
  .ktr .k{font-size:7px;letter-spacing:-.01em}
}
/* Ниже этого порога сетка-календарь перестаёт быть читаемой: клетка урока
   становится уже слова «контрольная». Порог измерен, а не выбран на глаз —
   раскладка становится вертикальной, блок на всю ширину. */
@media(max-width:1300px){
  .oborot,.uzko{padding:0 16px 50px}
  .chetv{display:block}
  .chetv-hd{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
    margin-bottom:7px;padding-bottom:5px;border-bottom:1px solid var(--line2)}
  .chetv-hd .dts{display:inline;margin-top:0}
  .nw{text-align:left;line-height:1.4;margin:7px 0 3px}
  .shapka h1{font-size:23px}
  .zag h1{font-size:27px}
  .lenta{grid-template-columns:1fr;grid-auto-rows:auto;gap:7px}
  .lenta>*{grid-column:1/-1!important}
  .blok{min-height:96px;padding:12px 13px 0}
  .blok .pz{max-height:none;font-size:12px}
  .blok .pz{display:block}
  .blok .setka{display:none}
  /* На узком экране плашка контрольной НЕ во всю ширину: иначе она получает ту же
     массу, что тема на шесть часов, и математика опять проигрывает контролю. */
  .ktr{height:auto;padding:6px 11px;width:52%;justify-content:flex-start}
  .ktr.chetv{height:auto;width:38%}
  .ktr.chetv .c{display:block}
  .linejka{grid-template-columns:repeat(5,minmax(0,1fr))}
  .chetv-hd .nw{margin-left:0;width:100%}
  .tochki{grid-template-columns:1fr;gap:22px}
}
"""


def stranica(titul, telo, klass=''):
    return ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n</head>\n<body%s>\n%s\n</body>\n</html>\n'
            % (E(titul), CSS, (' class="%s"' % klass) if klass else '', telo))


def cvet(el):
    return 'var(--d-%s)' % el.get('domen', 'O')


def dm_html(el):
    """Подпись раздела. Совпала с именем блока («Разгон» — раздел «разгон») —
    не печатается: повтор читается как сбой генерации, а не как разметка."""
    d = DOMENY[el['domen']]
    if norm_imya(d) == norm_imya(el['imya']):
        return ''
    return '<span class="dm">%s</span>' % E(d)


def norm_imya(s):
    return re.sub(r'[^a-zа-яё0-9]+', '', s.lower().replace('ё', 'е'))


def setka_nedel(el):
    """Волоски по границам пар внутри блока: клетки недель видны."""
    n = el['chasy']
    kl = []
    for i in range(n):
        gl = 'pol' if (el['_start'] + i) % 2 else ''
        kl.append('<i class="%s"></i>' % gl)
    return ('<span class="setka" style="grid-template-columns:repeat(%d,1fr)">%s</span>'
            % (n, ''.join(kl)))


def chasy_slovo(n):
    if n % 10 == 1 and n % 100 != 11:
        return 'час'
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return 'часа'
    return 'часов'


def lenta_kursa(ch):
    out = []
    for el in ch['potok']:
        span = el['chasy']
        if el['tip'] == 'blok':
            st = 'grid-column:span %d;--c:%s' % (span, cvet(el))
            kl = 'blok'
            styk = ''
            if el.get('na-styke'):
                kl += ' styk'
                styk = '<span class="styk-l">на стыке</span>'
            out.append(
                '<a class="%s" style="%s" href="blok-%s.html">%s'
                '<span class="ug"><span class="ch">%d %s</span></span>'
                '<span class="im">%s</span><span class="pz">%s</span>'
                '<span class="niz">%s%s</span></a>'
                % (kl, st, el['slug'], setka_nedel(el),
                   el['chasy'], chasy_slovo(el['chasy']),
                   E(el['imya']), E(el['podzag']), dm_html(el), styk))
        else:
            kl = 'ktr chetv' if el.get('chetvertnaya') else 'ktr'
            nom = ch['nedeli'][el['_start'] // 2]['nomer']
            out.append('<a class="%s" style="grid-column:span %d" href="nedelya-%02d.html">'
                       '<span class="k">контрольная</span></a>' % (kl, span, nom))
    return ''.join(out)


def lenta_kruzhka(ch):
    k = ch['kruzhok']
    if k is None:
        return ''
    n_ned = len(ch['nedeli'])
    setka = ('<span class="setka" style="grid-template-columns:repeat(%d,1fr)">%s</span>'
             % (n_ned, '<i></i>' * n_ned))
    return ('<a class="blok" style="grid-column:span %d;--c:var(--d-Z)" href="blok-%s.html">'
            '%s<span class="ug"><span class="ch">%d %s</span></span>'
            '<span class="im">кружок</span><span class="pz">%s</span></a>'
            % (ch['chasy'], k['slug'], setka,
               k['chasy'], chasy_slovo(k['chasy']), E(k['podzag'])))


def linejka(ch, rezhim):
    out = []
    for ned in ch['nedeli']:
        if rezhim == 'kruzhok':
            fon = 'color-mix(in srgb, var(--d-Z) 30%, var(--card))'
            spl = ''
        else:
            cv = []
            for el, _ in ned['doli']:
                cv.append(cvet(el) if el['tip'] == 'blok' else 'var(--ktr)')
            if len(cv) == 1:
                fon = 'color-mix(in srgb, %s 30%%, var(--card))' % cv[0]
                spl = ''
            else:
                fon = ('linear-gradient(90deg,'
                       'color-mix(in srgb, %s 34%%, var(--card)) 0 50%%,'
                       'color-mix(in srgb, %s 34%%, var(--card)) 50%% 100%%)' % (cv[0], cv[1]))
                spl = ' split'
        out.append('<a class="ned%s" style="--nb:%s" href="nedelya-%02d.html">%d</a>'
                   % (spl, fon, ned['nomer'], ned['nomer']))
    return ''.join(out)


def chetvert_blok(ch, rezhim):
    lenta = lenta_kruzhka(ch) if rezhim == 'kruzhok' else lenta_kursa(ch)
    vne = ''
    if rezhim == 'kurs':
        for v in ch['vne_setki']:
            vne += ('<div class="vne"><span class="i">%s</span><span class="c">%s</span></div>'
                    % (E(v['imya']), E(v['chto'])))
    return ('<section class="chetv">'
            '<div class="chetv-hd"><span class="rim">%s</span>'
            '<span class="cw">четверть</span><span class="dts">%s</span></div>'
            '<div class="lenta">%s</div>'
            '<div class="nw">%d недель</div>'
            '<div class="linejka">%s</div>%s</section>'
            % (E(ch['nomer']), E(ch['daty']), lenta,
               len(ch['nedeli']), linejka(ch, rezhim), vne))


def god_stranica(g, chetverti):
    tr = []
    for rezhim in ('kurs', 'kruzhok'):
        tr.append('<div class="tr-%s">%s</div>'
                  % (rezhim, ''.join(chetvert_blok(c, rezhim) for c in chetverti)))
    # Из kurs.podzagolovok берётся ПЕРВЫЙ сегмент: хвост «строка раскрывается по
    # нажатию» описывал забракованную версию и на этой странице был бы ложью.
    razmer = g['kurs']['podzagolovok'].split(RAZD)[0].strip()
    telo = ('<div class="oborot">'
            '<header class="shapka"><h1>%s</h1><span class="razmer">%s</span>'
            '<span class="spacer"></span>'
            '<span class="demo">демо-версия</span></header>'
            '<div class="tumbler">'
            '<input type="radio" name="tr" id="t-kurs" checked>'
            '<input type="radio" name="tr" id="t-kruzhok">'
            '<div class="perekl">'
            '<label for="t-kurs">основной курс</label>'
            '<label for="t-kruzhok">кружок</label></div>'
            '<div class="kalendar">%s</div></div>'
            '</div>' % (E(g['kurs']['nazvanie']), E(razmer), ''.join(tr)))
    return stranica(g['kurs']['nazvanie'], telo)


def tochki_html(karta, cv):
    li = []
    for k in karta:
        chasti = ''.join('<span>%s</span>' % E(x.strip())
                         for x in k['chto'].split(RAZD) if x.strip())
        li.append('<li><span class="t">%s</span><span class="ch">%s</span></li>'
                  % (E(k['tema']), chasti))
    return '<ol class="tochki" style="--c:%s">%s</ol>' % (cv, ''.join(li))


def spisok_nedel(nedeli):
    a = []
    for n in nedeli:
        ktr = ''
        for el, _ in n['doli']:
            if el['tip'] == 'kontrolnaya':
                ktr = '<span class="d">контрольная</span>'
        a.append('<a href="nedelya-%02d.html"><span class="n">неделя %d</span>%s</a>'
                 % (n['nomer'], n['nomer'], ktr))
    return '<div class="spisok">%s</div>' % ''.join(a)


def blok_stranica(g, el, kruzhok=False):
    cv = 'var(--d-Z)' if kruzhok else cvet(el)
    imya = 'кружок' if kruzhok else el['imya']
    metki = ['<span class="metka" style="--c:%s">%s</span>'
             % (cv, E('кружок' if kruzhok else DOMENY[el['domen']]))]
    metki.append('<span class="metka tih">%s четверть</span>' % E(el['_ch']['nomer'])
                 if kruzhok else
                 '<span class="metka tih">%d %s</span>' % (el['chasy'], chasy_slovo(el['chasy'])))
    if not kruzhok and el.get('na-styke'):
        metki.append('<span class="metka tih">на стыке</span>')
    zadachi = ''
    if not kruzhok and el.get('opornye'):
        chasti = ''.join('<span>%s</span>' % E(x.strip().rstrip('.'))
                         for x in el['opornye'].split(RAZD) if x.strip())
        zadachi = ('<section class="sect"><p class="grp">опорные задачи</p>'
                   '<div class="zadachi">%s</div></section>' % chasti)
    telo = ('<div class="uzko">'
            '<header class="shapka"><a class="nazad" href="index.html">к году</a>'
            '<span class="spacer"></span><span class="demo">демо-версия</span></header>'
            '<div class="zag"><div class="metki">%s</div><h1>%s</h1><p class="pz">%s</p></div>'
            '<section class="sect"><p class="grp">опорные точки</p>%s</section>'
            '%s'
            '<section class="sect"><p class="grp">занятия</p>%s</section>'
            '<div class="podval"><a class="nazad" href="index.html">к году</a></div>'
            '</div>'
            % (''.join(metki), E(imya), E(el['podzag']),
               tochki_html(el['karta'], cv), zadachi, spisok_nedel(el['nedeli'])))
    return stranica(imya, telo)


def nedelya_stranica(g, ned):
    ch = ned['chetvert']
    metki = ['<span class="metka tih">%s четверть</span>' % E(ch['nomer'])]
    ssylki = []
    for el, chas in ned['doli']:
        if el['tip'] == 'blok':
            metki.append('<a class="metka" style="--c:%s" href="blok-%s.html">%s</a>'
                         % (cvet(el), el['slug'], E(el['imya'])))
            ssylki.append(el)
        else:
            metki.append('<span class="metka tih">контрольная'
                         '<i class="tochka">·</i><b>%s</b></span>' % E(el['chto']))
    if ch['kruzhok'] is not None:
        metki.append('<a class="metka" style="--c:var(--d-Z)" href="blok-%s.html">кружок</a>'
                     % ch['kruzhok']['slug'])
    niz = ['<a class="nazad" href="index.html">к году</a>']
    for el in ssylki:
        niz.append('<a class="nazad" href="blok-%s.html">к блоку</a>' % el['slug'])
    telo = ('<div class="uzko">'
            '<header class="shapka"><a class="nazad" href="index.html">к году</a>'
            '<span class="spacer"></span><span class="demo">демо-версия</span></header>'
            '<div class="zag"><div class="metki">%s</div><h1>неделя %d</h1></div>'
            '<section class="sect"><div class="karkas">'
            '<div class="box"><p class="grp">что было на уроке</p></div>'
            '<div class="box"><p class="grp">домашнее задание</p></div>'
            '</div></section>'
            '<div class="podval">%s</div>'
            '</div>' % (''.join(metki), ned['nomer'], ''.join(niz)))
    return stranica('неделя %d' % ned['nomer'], telo)


# ── прогон ─────────────────────────────────────────────────────────────────
def main():
    tolko_schet = '--proverit' in sys.argv
    g = json.load(open(IST, encoding='utf-8'))
    global DOMENY
    DOMENY = g['kurs']['domeny']

    chetverti, bloki, nedeli = razobrat(g)

    # Y — из данных, посчитано ЭТОЙ ЖЕ командой, а не взято из захода
    y_blok = sum(1 for c in g['chetverti'] for e in c['elementy'] if e['tip'] == 'blok')
    y_kruzhok = sum(1 for c in g['chetverti'] for e in c['elementy'] if e['tip'] == 'kruzhok')
    y_ned = sum(c['chasy'] for c in g['chetverti']) // 2
    y_karta = sum(len(e['karta']) for c in g['chetverti'] for e in c['elementy']
                  if e['tip'] in ('blok', 'kruzhok'))

    kruzhki = [c['kruzhok'] for c in chetverti if c['kruzhok'] is not None]

    if tolko_schet:
        print('источник        : %s' % IST)
        print('четвертей       : %d' % len(chetverti))
        print('уроков          : %d' % sum(c['chasy'] for c in g['chetverti']))
        print('недель          : %d' % y_ned)
        print('блоков          : %d' % y_blok)
        print('дорожек кружка  : %d' % y_kruzhok)
        print('пунктов karta   : %d' % y_karta)
        return 0

    if not os.path.isdir(DIST):
        os.makedirs(DIST)

    pisali = []

    def polozhit(imya, soder):
        put = os.path.join(DIST, imya)
        with open(put, 'w', encoding='utf-8') as f:
            f.write(soder)
        pisali.append(imya)

    polozhit('index.html', god_stranica(g, chetverti))
    for el in bloki:
        polozhit('blok-%s.html' % el['slug'], blok_stranica(g, el))
    for k in kruzhki:
        polozhit('blok-%s.html' % k['slug'], blok_stranica(g, k, kruzhok=True))
    for n in nedeli:
        polozhit('nedelya-%02d.html' % n['nomer'], nedelya_stranica(g, n))

    x_blok = len(bloki)
    x_kruzhok = len(kruzhki)
    x_ned = len(nedeli)
    x_karta = sum(len(e['karta']) for e in bloki) + sum(len(k['karta']) for k in kruzhki)
    rasshep = sum(1 for n in nedeli if len(n['doli']) > 1)

    print('источник         : %s' % IST)
    print('собрано в        : %s' % DIST)
    print('страница года    : 1 из 1')
    print('страниц блоков   : %d из %d' % (x_blok, y_blok))
    print('страниц кружка   : %d из %d' % (x_kruzhok, y_kruzhok))
    print('страниц занятий  : %d из %d' % (x_ned, y_ned))
    print('недель в году    : %d из %d, расщеплённых между двумя элементами %d'
          % (x_ned, y_ned, rasshep))
    print('пунктов karta    : %d из %d' % (x_karta, y_karta))
    print('файлов записано  : %d' % len(pisali))

    bed = []
    if x_blok != y_blok:
        bed.append('блоки: %d из %d' % (x_blok, y_blok))
    if x_kruzhok != y_kruzhok:
        bed.append('кружок: %d из %d' % (x_kruzhok, y_kruzhok))
    if x_ned != y_ned:
        bed.append('недели: %d из %d' % (x_ned, y_ned))
    if x_karta != y_karta:
        bed.append('karta: %d из %d' % (x_karta, y_karta))
    if not (x_blok and x_ned and x_karta):
        bed.append('охват 0 при непустом источнике')
    if bed:
        print('ОХВАТ НЕ ПОЛОН: ' + ' · '.join(bed))
        return 1
    print('охват полон')
    return 0


if __name__ == '__main__':
    sys.exit(main())
