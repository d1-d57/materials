# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.lib.colors import Color, HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import pypdfium2 as pdfium

F2="/tmp/fonts2"
for n,f in [('Lora','LoraReg'),('Lora-Bold','LoraBold'),('Lora-SemiBold','LoraSemi'),('Lora-Italic','LoraItalic'),('Lora-BoldItalic','LoraBoldItalic')]:
    pdfmetrics.registerFont(TTFont(n,f'{F2}/{f}.ttf'))
registerFontFamily('Lora',normal='Lora',bold='Lora-Bold',italic='Lora-Italic',boldItalic='Lora-BoldItalic')
L="/usr/share/fonts/truetype/lato"
pdfmetrics.registerFont(TTFont('Lato',f'{L}/Lato-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Lato-Bold',f'{L}/Lato-Bold.ttf'))
registerFontFamily('Lato',normal='Lato',bold='Lato-Bold')

PAPER=HexColor('#F3EBD9'); INK=HexColor('#26221B'); MUTED=HexColor('#8A7C68')
ACC='#9E4632'; ACCENT=HexColor(ACC); HAIR=Color(0x26/255,0x22/255,0x1B/255,alpha=0.26)
W,H=A4; LM=RM=54; TM=56; BM=52; CW=W-LM-RM
c=canvas.Canvas('/tmp/poster.pdf',pagesize=A4)
c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)

def para(html,font,size,leading,color,x,top,width):
    st=ParagraphStyle('s',fontName=font,fontSize=size,leading=leading,textColor=color,alignment=TA_LEFT)
    P=Paragraph(html,st); w,h=P.wrap(width,100000); P.drawOn(c,x,top-h); return top-h
def tracked_c(cx,y,text,font,size,color,cs):
    w=stringWidth(text,font,size)+(len(text)-1)*cs
    t=c.beginText(cx-w/2,y); t.setFont(font,size); t.setFillColor(color); t.setCharSpace(cs); t.textOut(text); t.setCharSpace(0); c.drawText(t); return w
def rule(y):
    c.setStrokeColor(HAIR); c.setLineWidth(0.9); c.line(LM,y,W-RM,y)

cur=H-TM
tracked_c(W/2,cur-9,"ПО ЧЕТВЕРГАМ · 16 ИЮЛЯ — 27 АВГУСТА · 19:00 МСК",'Lato-Bold',9.5,MUTED,2.4); cur=cur-9-20
cur=para('Пределы<br/>вычислимого','Lora-Bold',53,55,INK,LM,cur,CW); cur-=16
cur=para('Летний курс: семь лекций о том, что вычислительная машина может, чего не может, и кто это выяснил.','Lora-Italic',14.5,19.5,MUTED,LM,cur,440); cur-=18
c.setFont('Lato',10); c.setFillColor(MUTED); c.drawString(LM,cur-3,"1936"); c.drawRightString(W-RM,cur-3,"1950")
lx0=LM+38; lx1=W-RM-38
c.setStrokeColor(HAIR); c.setLineWidth(0.9); c.line(lx0,cur,lx1,cur)
c.setFillColor(ACCENT); c.circle(lx0,cur,2.0,fill=1,stroke=0); c.line(lx1-5,cur+2.6,lx1,cur); c.line(lx1-5,cur-2.6,lx1,cur)
cur=cur-3-20
cur=para('Математики придумали компьютер как гипотетический инструмент за десять лет до первого механизма. Они открывали его возможности — и обнаруживали их пределы. Так появилась техника, на которой в вашем телефоне держится все: шифрование переписки, сжатие музыки, поисковая выдача, расписания рейсов, ответы чат-бота.','Lora',14,19,INK,LM,cur,CW); cur-=20

# --- LECTURE PLATE (divider) ---
rule(cur); cur-=15
tracked_c(W/2,cur-10,"СЕМЬ ЛЕКЦИЙ",'Lato-Bold',10,MUTED,3.0); cur=cur-10-13
c.setFillColor(ACCENT); c.setFont('Lora-SemiBold',15.5)
c.drawCentredString(W/2,cur-15.5,"Вычислимость · Сложность · Информация · Криптография"); cur-=15.5+19
c.setFont('Lora-SemiBold',15.5); c.setFillColor(ACCENT)
c.drawCentredString(W/2,cur-15.5,"Случайность · Оптимизация · Мышление"); cur=cur-15.5-14
rule(cur); cur-=20

# --- TWO COLUMNS ---
gap=30; colW=(CW-gap)/2; colL=LM; colR=LM+colW+gap; ctop=cur
p2='Наш курс — об этих изобретениях. Мы поймем, почему компьютеры так изменили жизнь и где они бессильны, через семь лекций.'
p3='Как всегда, будем открывать все заново: изучать примеры, доказывать теоремы, решать упражнения. Столкнемся с самыми красивыми сюжетами в логике, комбинаторике, теории чисел, теории вероятностей, выпуклой геометрии и анализе.'
p4='Компьютер создали ученые военного поколения: в Блетчли под Лондоном они ломали немецкие шифры, в Лос-Аламосе делали бомбу. Мы пройдем их путем между двумя вопросами <b>Алана Тьюринга</b>: <i>«чего машина не может»</i> и <i>«может ли она думать»</i>. Нам помогут <b>фон Нейман</b> и <b>Гёдель</b>, <b>Шеннон</b>, <b>Колмогоров</b> и <b>Винер</b>. Каждый из них упёрся в собственный предел не только в математике, но и в жизни.'
bL=para(p2,'Lora',11,15.3,INK,colL,ctop,colW); bL=para(p3,'Lora',11,15.3,INK,colL,bL-12,colW)
bR=para(p4,'Lora',11,15.3,INK,colR,ctop,colW)
cur=min(bL,bR)-20
rule(cur); cur-=18
cur=para('Если это про вас, <font color="'+ACC+'"><b>напишите мне</b></font>. Собираю небольшую группу.','Lora',13.5,17.5,INK,LM,cur,CW)
print("CTA bottom y:",round(cur,1)," (BM",BM,")  cols L,R:",round(bL,1),round(bR,1))
c.showPage(); c.save()
doc=pdfium.PdfDocument('/tmp/poster.pdf'); doc[0].render(scale=150/72).to_pil().save('/tmp/poster.png')
