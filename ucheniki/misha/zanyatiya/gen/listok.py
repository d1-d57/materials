# Генератор печатного листка для Миши в формате 20.09 (PT Serif, сжато, условия + поля).
import sys
CSS=open(__file__.replace('listok.py','listok.css')).read()
def grid(R,C,cut=(),mm=5,color=False,dots=False,corner=False,fill=None):
    s=10; W=C*s; H=R*s; out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 {W+2} {H+2}" style="width:{C*mm}mm" role="img">']
    for r in range(R):
        for c in range(C):
            x,y=c*s,r*s
            if (r,c) in cut:
                out.append(f'<line x1="{x+2}" y1="{y+2}" x2="{x+8}" y2="{y+8}" stroke="#888" stroke-width=".6"/><line x1="{x+8}" y1="{y+2}" x2="{x+2}" y2="{y+8}" stroke="#888" stroke-width=".6"/>'); continue
            f='#bdb6aa' if color and (r+c)%2==0 else '#fff'
            out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{f}" stroke="#1f1b17" stroke-width=".5"/>')
            if dots:
                v=fill[r][c] if fill else '.'
                cf={'1':'#1f1b17','0':'#fff'}.get(v)
                if cf: out.append(f'<circle cx="{x+5}" cy="{y+5}" r="3.6" fill="{cf}" stroke="#1f1b17" stroke-width=".6"/>')
            if corner and r==R-1 and c==0:
                out.append(f'<text x="{x+5}" y="{y+7.2}" font-size="7" text-anchor="middle">⚑</text>')
    out.append('</svg>'); return ''.join(out)
def numgrid(rows,ineq=(),boxes=False,mm=10):
    n=len(rows); s=10; gap=4; W=n*s+(n-1)*gap
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 {W+2} {W+2}" style="width:{W/10*mm/1.4:.1f}mm" role="img">']
    X=lambda j:j*(s+gap)
    for i,r in enumerate(rows):
        for j,ch in enumerate(r):
            out.append(f'<rect x="{X(j)}" y="{X(i)}" width="{s}" height="{s}" fill="{"#e8e2d6" if ch!="." else "#fff"}" stroke="#1f1b17" stroke-width=".6"/>')
            if ch!='.': out.append(f'<text x="{X(j)+5}" y="{X(i)+7.6}" font-size="7.5" text-anchor="middle" font-family="PT Serif,Georgia,serif">{ch}</text>')
    for (a,b) in ineq:
        (i1,j1),(i2,j2)=a,b
        if i1==i2: x=(X(min(j1,j2))+s+X(max(j1,j2)))/2; y=X(i1)+7; t='&lt;' if j1<j2 else '&gt;'
        else: x=X(j1)+5; y=(X(min(i1,i2))+s+X(max(i1,i2)))/2+2.5; t='∧' if i1<i2 else '∨'
        out.append(f'<text x="{x}" y="{y}" font-size="6" text-anchor="middle" font-weight="700">{t}</text>')
    if boxes:
        m=X(2)-gap/2; out.append(f'<line x1="{m}" y1="-1" x2="{m}" y2="{W+1}" stroke="#9e2b25" stroke-width=".8"/><line x1="-1" y1="{m}" x2="{W+1}" y2="{m}" stroke="#9e2b25" stroke-width=".8"/>')
    out.append('</svg>'); return ''.join(out)
def P(n,t): return f'<div class="p"><span class="n">{n}</span> {t}</div>'
u='<u class="s">&nbsp;</u>'; U='<u class="m">&nbsp;</u>'
def build(title,body): return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
if __name__=='__main__':
    t4=["0.1.","1..1",".0.0","0..."]; t4b=["0...","1...","0.01","1..1"]; t6=["1..00.",".1.0.1","..0..0","1..10.",".1..0.",".0.1.0"]; t6c=["....1.","1....1",".10..1","1100.0","......","1..0.."]
    b=['<h1>Занятие 27 сентября</h1>']
    b.append('<h2>1. Остров рыцарей и лжецов</h2><p class="step">Рыцари всегда говорят правду, лжецы всегда лгут.</p>')
    b.append(P(1,f'Аня: «Боря — лжец». Боря: «Мы оба рыцари». &nbsp; Аня — {U}, Боря — {U}'))
    b.append(P(2,'Аня: «Боря — рыцарь». Боря: «Аня — рыцарь». Кто есть кто? Найди <b>все</b> варианты.')+'<div class="lines"><span class="fill"></span></div>')
    b.append(P(3,'Аня: «Боря — лжец». Боря: «Вика — лжец». Вика: «Аня и Боря оба лжецы».'))
    b.append(f'<div class="p sub">Может ли Вика быть рыцарем? {U} &nbsp; Аня — {U}, Боря — {U}, Вика — {U}</div>')
    b.append(P(4,f'В шеренгу встали пятеро. Каждый сказал: «Слева от меня рыцарей больше, чем справа». Сколько в шеренге рыцарей? {u}'))
    b.append(P(5,f'За круглым столом трое. Каждый сказал: «Среди двух моих соседей ровно один рыцарь». Сколько рыцарей может быть за столом? {U}'))
    b.append(P(6,'На доске четыре фразы: «Все фразы здесь верные», «Здесь ровно одна неверная фраза», «Здесь ровно две неверные», «Здесь ровно три неверные». Какие из них верные? Найди все варианты.')+'<div class="lines"><span class="fill"></span></div>')
    b.append('<h2>2. Доминошки на доске</h2><p class="step">Доминошка закрывает две соседние клетки. Закрыть доску — положить доминошки без наложений так, чтобы закрылись все клетки.</p>')
    b.append('<div class="two"><div class="txt">'+P(7,f'Закрой доски 2×3 и 3×4. Можно ли закрыть 3×3? {U}')+P(8,f'Доска 8×8. Сколько нужно доминошек? {u} Отрезали один угол — можно закрыть? {U} Отрезали два противоположных угла — сколько клеток осталось? {u}')+'</div><div class="grids">'+grid(2,3,mm=4)+grid(3,4,mm=4)+grid(3,3,mm=4)+'</div></div>')
    b.append('<div class="two"><div class="txt">'+P(9,'Доска 4×4 без двух противоположных углов. Попробуй закрыть. Потом раскрась её в шахматном порядке.'))
    b.append(f'<div class="p sub">Углы одного цвета или разного? {U} Одна доминошка закрывает тёмных {u}, светлых {u}. На доске тёмных {u}, светлых {u}. Можно закрыть? {U}</div>')
    b.append(P(10,f'Можно ли закрыть 8×8 без двух противоположных углов? {U} Почему?')+'<div class="lines"><span class="fill"></span></div>')
    b.append('</div><div class="grids">'+grid(4,4,{(0,0),(3,3)},mm=5)+grid(4,4,{(0,0),(3,3)},mm=5)+'</div></div>')
    b.append('<div class="two"><div class="txt">'+P(11,f'Доска 5×5. Сколько на ней клеток? {u}')+f'<div class="p sub">Вырезали клетку рядом с углом. Можно закрыть? {U} &nbsp; А если вырезать угол? {U}</div>'+'</div><div class="grids">'+grid(5,5,{(0,1)},mm=5)+grid(5,5,{(0,0)},mm=5)+'</div></div>')
    s1=[".432","3.14","...3","23.."]; s2=[".32.","24..",".142","...3"]; s3=[".4..","13.4",".24.",".1.."]
    f1=([".4..",".3..","..1.","4..."],[((1,1),(1,2)),((0,3),(0,2)),((0,0),(1,0)),((1,3),(1,2)),((2,2),(2,3))])
    f2=(["...3","..3.","....","3..."],[((1,0),(1,1)),((2,2),(2,3)),((1,0),(2,0)),((1,2),(0,2)),((2,2),(2,1)),((0,3),(1,3))])
    b.append('<h2 class="pb">3. Головоломки</h2>')
    b.append('<p class="step"><b>Судоку.</b> Числа 1–4: в каждой строке, столбце и квадрате 2×2 все разные. <b>Двоичный код.</b> Чёрный или белый кружок в каждую клетку; в строке и столбце поровну; три одинаковых подряд нельзя; одинаковых строк и столбцов нет. <b>Футошики.</b> Числа 1–4, в строке и столбце разные; знаки &lt; и &gt; выполняются.</p>')
    b.append('<div class="grids">'+numgrid(s1,boxes=True)+numgrid(s2,boxes=True)+grid(4,4,dots=True,fill=t4,mm=8.5)+grid(4,4,dots=True,fill=t4b,mm=8.5)+numgrid(*f1)+numgrid(*f2)+numgrid(s3,boxes=True)+grid(6,6,dots=True,fill=t6,mm=7)+'</div>')
    b.append('<h2>4. Ладья в угол</h2><p class="step">Двое по очереди двигают ладью влево или вниз на сколько угодно клеток. Кто поставит её в левый нижний угол ⚑, тот выиграл.</p>')
    b.append('<div class="two"><div class="txt">'+P(12,f'Ладья стоит в нижнем ряду, ход твой. Кто выиграет? {U}')+P(13,'Разметь доску. <b>В</b> — ладья тут, ход твой, и ты выигрываешь. <b>П</b> — проигрываешь.')+P(14,f'Где стоят клетки П? {U}')+P(15,f'Доска 8×8, ладья в правом верхнем углу. Кто выиграет: первый или второй? {U}')+'</div><div class="grids">'+grid(6,6,corner=True,mm=8)+'</div></div>')
    open(sys.argv[1],'w').write(build('Занятие 27 сентября',''.join(b)))
