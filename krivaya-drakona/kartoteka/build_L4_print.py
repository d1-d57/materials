#!/usr/bin/env python3
"""СБОРКА ПЕЧАТНОГО ЛИСТКА Л4: шаблон + фигура → L4-print.html

    python3 kartoteka/gen_l4_figs.py && python3 kartoteka/build_L4_print.py

Зачем сборщик, а не вклейка руками. У Л1 SVG вклеен в печатный файл руками, и это записанная
асимметрия-риск: правка генератора в листок сама не доедет. Здесь дыра закрыта — фигура
подставляется командой, как у Л2.
"""
import pathlib, sys, re

HERE = pathlib.Path(__file__).resolve().parent
tmpl = (HERE / 'L4-print-tmpl.html').read_text()
fig_path = HERE / 'L4-fig-ranks.svg'

if not fig_path.exists():
    sys.exit('✗ нет L4-fig-ranks.svg — сначала: python3 kartoteka/gen_l4_figs.py')

fig = fig_path.read_text().strip()
if '{{FIG_RANKS}}' not in tmpl:
    sys.exit('✗ в шаблоне нет метки {{FIG_RANKS}} — сборка невозможна')

out = tmpl.replace('{{FIG_RANKS}}', fig)

# гейт сборки: метка подставлена, размеры у SVG заданы явно (иначе WeasyPrint схлопнет)
if '{{' in out:
    sys.exit('✗ в собранном файле осталась неподставленная метка')
if not re.search(r'<svg[^>]*width="\d+mm"[^>]*height="\d+mm"', out):
    sys.exit('✗ у SVG нет явных width/height в мм — во WeasyPrint он схлопнется')

(HERE / 'L4-print.html').write_text(out)
print(f'✓ L4-print.html собран: шаблон {len(tmpl)} + фигура {len(fig)} знаков')
