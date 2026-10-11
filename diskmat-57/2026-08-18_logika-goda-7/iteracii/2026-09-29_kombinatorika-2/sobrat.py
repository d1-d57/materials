# -*- coding: utf-8 -*-
"""Собрать весь комплект итерации одной командой: python3 sobrat.py
Порядок важен: данные → карта → листок (пишет kanon.json) → контрольная → ДЗ → шпаргалка → гейты → табло."""
import subprocess, sys, os, glob
from pathlib import Path
H = Path(__file__).resolve().parent; os.chdir(H)
M = next(p / 'mashina-listka' for p in H.parents if (p / 'mashina-listka').is_dir())
def run(*a):
    print('▸', ' '.join(map(str, a))); r = subprocess.run([sys.executable, *map(str, a)])
    if r.returncode: sys.exit(f'остановлено на {a[0]} (код {r.returncode})')
for s in ['listok4.py', 'romby5.py', 'listok_29-09_dannye.py', 'kontrolnaya_29-09_dannye.py', 'dz_29-09_dannye.py', 'shpargalka_29-09_dannye.py']: run(s)
run(M / 'proverka.py', H); run(M / 'tablo.py', H)
