import sys
from PIL import Image
# usage: crop.py foto rot x0 y0 x1 y1 scale out   (box in ROTATED coords as fractions 0-1)
f,rot,x0,y0,x1,y1,sc,out=sys.argv[1:9]
im=Image.open(f'img/{f}.jpeg')
im=im.rotate(int(rot),expand=True)
W,H=im.size
b=(int(float(x0)*W),int(float(y0)*H),int(float(x1)*W),int(float(y1)*H))
c=im.crop(b)
c=c.resize((int(c.width*float(sc)),int(c.height*float(sc))),Image.LANCZOS)
c.save(f'recheck/{out}.png'); print(c.size)
