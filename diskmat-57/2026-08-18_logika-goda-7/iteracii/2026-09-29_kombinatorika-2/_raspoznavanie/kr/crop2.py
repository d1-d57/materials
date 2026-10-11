import sys
from PIL import Image, ImageOps, ImageEnhance
f,rot,x0,y0,x1,y1,sc,out=sys.argv[1:9]
im=Image.open(f'img/{f}.jpeg').rotate(int(rot),expand=True)
W,H=im.size
c=im.crop((int(float(x0)*W),int(float(y0)*H),int(float(x1)*W),int(float(y1)*H)))
c=c.resize((int(c.width*float(sc)),int(c.height*float(sc))),Image.LANCZOS)
c=ImageOps.autocontrast(c.convert('L'),cutoff=1)
c.save(f'recheck/{out}.png'); print(c.size)
