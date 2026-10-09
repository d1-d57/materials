"""Базовая композиция аватарки «Пути и волны» (К2 «Хребты Каталана»).
Хребты — настоящие пути Дика (шаги ±1 под 45°, не ниже воды); отражение в воде — зеркало,
к низу рассыпается синусоидальной рябью. Выход: base-1024.png, krug-preview.png, krug-48.png."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W = 1024; CX = CY = W // 2; R = int(W * 0.425)   # круг ~85% холста
WATER = 600                                       # линия воды чуть ниже центра
SKY = (241, 230, 207); SKY2 = (248, 241, 226)
RED = (190, 58, 34); RED_DARK = (92, 32, 20); SNOW = (248, 244, 234)
BACK = (124, 150, 182); BLUE = (30, 78, 140); BLUE_DEEP = (16, 46, 92)

def dyck_ok(h):
    return h[0] == 0 and h[-1] == 0 and all(x >= 0 for x in h) and all(abs(a - b) == 1 for a, b in zip(h, h[1:]))

# передний хребет: 24 шага, вершина 7 — центральная «Фудзи» среди ступеней
FRONT = [0,1,2,1,2,3,4,3,4,5,6,7,6,5,4,5,4,3,2,3,2,1,0]
# дальний хребет: 36 шагов, пики по бокам, ниже переднего
BACKH = [0,1,2,3,4,3,4,5,6,5,4,3,2,3,2,1,2,1,2,3,4,3,4,5,6,7,6,5,4,3,2,3,2,1,0,1,0]
assert dyck_ok(FRONT) and dyck_ok(BACKH), "не путь Дика"

def ridge_poly(h, step, x0, y0):
    pts = [(x0 + i * step, y0 - v * step) for i, v in enumerate(h)]
    return pts

def layer(draw_fn):
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); draw_fn(d, im); return im

span = 2 * math.sqrt(R ** 2 - (WATER - CY) ** 2) * 1.12
f_step = span / (len(FRONT) - 1); b_step = span / (len(BACKH) - 1) * 1.05
x_left = CX - span / 2

img = Image.new("RGB", (W, W), SKY)
# небо: мягкий градиент бумаги + зерно
sky = Image.linear_gradient("L").resize((W, W))
img = Image.composite(Image.new("RGB", (W, W), SKY2), img, sky.point(lambda v: 255 - v))
random.seed(7)
grain = Image.effect_noise((W, W), 18).convert("L")
img = ImageChops.multiply(img, Image.merge("RGB", [grain.point(lambda v: 230 + v // 10)] * 3))
# едва видимая решётка точек в небе — намёк на клетки, по которым идёт точка
dots = layer(lambda d, im: [d.ellipse((x - 1.2, y - 1.2, x + 1.2, y + 1.2), fill=(150, 130, 100, 70))
                            for x in [x_left + i * f_step for i in range(-2, len(FRONT) + 2)]
                            for y in [WATER - j * f_step for j in range(1, 12)]])
img.paste(dots, (0, 0), dots)

def mountains(d, im, h, step, x0, color, snow=False):
    pts = ridge_poly(h, step, x0, WATER)
    d.polygon(pts + [(pts[-1][0], WATER), (pts[0][0], WATER)], fill=color + (255,))
    if snow:
        # тёмная корона и снег у вершин выше 5: снежная шапка до высоты v-1, рваная нижняя кромка
        for i, v in enumerate(h):
            if 0 < i < len(h) - 1 and h[i - 1] < v > h[i + 1] and v >= 4:
                px, py = pts[i]
                depth = step * (1.55 if v >= 6 else 0.85)
                left = (px - depth, py + depth); right = (px + depth, py + depth)
                jag = []
                n = 7
                for t in range(n + 1):
                    xx = left[0] + (right[0] - left[0]) * t / n
                    yy = left[1] + (step * 0.35 if t % 2 else 0)
                    jag.append((xx, yy))
                d.polygon([(px, py)] + [right] + jag[::-1][1:-1] + [left], fill=SNOW + (255,))

back = layer(lambda d, im: mountains(d, im, BACKH, b_step, CX - b_step * (len(BACKH) - 1) / 2, BACK))
front = layer(lambda d, im: mountains(d, im, FRONT, f_step, x_left, RED, snow=True))
# лёгкое затемнение переднего хребта к вершине (как у Хокусая: тёмная корона)
grad = Image.new("L", (W, W), 0); gd = ImageDraw.Draw(grad)
top = WATER - max(FRONT) * f_step
for y in range(int(top), WATER):
    t = max(0.0, 1 - (y - top) / (2.6 * f_step)); gd.line([(0, y), (W, y)], fill=int(150 * t))
crown = Image.new("RGBA", (W, W), RED_DARK + (0,)); crown.putalpha(ImageChops.multiply(grad, front.split()[3]))
img.paste(back, (0, 0), back); img.paste(front, (0, 0), front); img.paste(crown, (0, 0), crown)
# снег поверх короны
snowonly = layer(lambda d, im: None)
sn = layer(lambda d, im: mountains(d, im, FRONT, f_step, x_left, RED, snow=True))
mask = Image.eval(sn.convert("RGB"), lambda v: v)
snowmask = Image.new("L", (W, W), 0)
px = sn.load(); sm = snowmask.load()
for y in range(int(top) - 2, WATER):
    for x in range(W):
        r, g, b, a = px[x, y]
        if a and r > 240 and g > 235: sm[x, y] = 255
img.paste(Image.new("RGB", (W, W), SNOW), (0, 0), snowmask)

# вода
water = Image.new("RGB", (W, W - WATER), BLUE)
wg = Image.linear_gradient("L").resize((W, W - WATER))
water = Image.composite(Image.new("RGB", (W, W - WATER), BLUE_DEEP), water, wg)
img.paste(water, (0, WATER))
# отражение: зеркало верхней половины, тёмное, с горизонтальным сдвигом рядов по синусу, растущим с глубиной
above = img.crop((0, 0, W, WATER)).transpose(Image.FLIP_TOP_BOTTOM)
refl = Image.blend(above, Image.new("RGB", above.size, BLUE_DEEP), 0.38)
ref_alpha = Image.new("L", above.size, 0)
fa = front.split()[3].crop((0, 0, W, WATER)).transpose(Image.FLIP_TOP_BOTTOM)
ba = back.split()[3].crop((0, 0, W, WATER)).transpose(Image.FLIP_TOP_BOTTOM)
ref_alpha = ImageChops.lighter(fa, ba.point(lambda v: v * 0.7))
out = Image.new("RGB", (W, W - WATER)); oa = Image.new("L", (W, W - WATER))
for dy in range(W - WATER):
    amp = 0.0 if dy < 4 else min(22, 0.0025 * dy ** 1.75)
    off = int(amp * math.sin(dy / 4.0) + 0.6 * amp * math.sin(dy / 1.7 + 1.1))
    fade = max(0.0, 1 - (dy / 430) ** 2.2)
    band = 1.0 if dy < 40 else (1.0 if math.sin(dy / (1.4 + dy / 90)) > -0.75 + dy / 520 else 0.0)
    if dy < refl.size[1]:
        row = refl.crop((0, dy, W, dy + 1)); arow = ref_alpha.crop((0, dy, W, dy + 1)).point(lambda v: int(v * fade * band))
        out.paste(row, (off, dy)); oa.paste(arow, (off, dy))
img.paste(out, (0, WATER), oa)
# волны: светлые синусоидальные линии — сумма двух волн, гуще книзу
wl = layer(lambda d, im: None); d = ImageDraw.Draw(wl)
for j in range(12):
    y0 = WATER + 300 + j * 18 + j * j * 1.5
    if y0 > W: break
    a1 = 3 + j * 0.9; k1 = 2 * math.pi / (140 - j * 4); k2 = 2 * math.pi / 57
    pts = [(x, y0 + a1 * math.sin(k1 * x + j) + 0.45 * a1 * math.sin(k2 * x - 2 * j)) for x in range(0, W, 4)]
    d.line(pts, fill=(222, 232, 240, 60 + min(170, j * 30)), width=2 + j // 4)
img.paste(wl, (0, 0), wl)
# тонкая светлая линия воды
ImageDraw.Draw(img).line([(0, WATER), (W, WATER)], fill=SNOW, width=2)

img.save("base-1024.png")
# превью: круг, как в Telegram
m = Image.new("L", (W, W), 0); ImageDraw.Draw(m).ellipse((CX - R / 0.85 * 0.995, CY - R / 0.85 * 0.995, CX + R / 0.85 * 0.995, CY + R / 0.85 * 0.995), fill=255)
circ = Image.new("RGB", (W, W), (255, 255, 255)); circ.paste(img, (0, 0), m)
circ.save("krug-preview.png")
small = circ.resize((48, 48), Image.LANCZOS)
sheet = Image.new("RGB", (48 * 3 + 40, 64), (255, 255, 255)); sheet.paste(small, (8, 8))
sheet.paste(circ.resize((40, 40), Image.LANCZOS), (72, 12)); sheet.paste(circ.resize((96, 96), Image.LANCZOS).resize((48, 48)), (128, 8))
sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save("krug-48.png")
print("ok", FRONT.index(max(FRONT)), round(f_step, 1), round(b_step, 1))
