# Резкость фото: дисперсия лапласиана по центральной области (меньше — смазаннее). Запуск: python3 rezkost.py <папка> [порог]
import cv2,sys,glob,os
d=sys.argv[1]; thr=float(sys.argv[2]) if len(sys.argv)>2 else 60
R=[]
for f in sorted(glob.glob(os.path.join(d,'*.jp*g'))):
    g=cv2.imread(f,0); h,w=g.shape; c=g[h//8:-h//8,w//8:-w//8]
    R.append((cv2.Laplacian(c,cv2.CV_64F).var(),os.path.basename(f)))
for v,f in sorted(R): print(f'{v:8.1f}  {f}  {"<-- переснять?" if v<thr else ""}')
