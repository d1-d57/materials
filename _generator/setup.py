#!/usr/bin/env python3
# Шим на две строки. Он не «legacy на всякий случай», он несущий: pip 21.2.4 в
# боевой среде не умеет PEP 660 и на папке с одним pyproject.toml отвечает
# «File "setup.py" or "setup.cfg" not found. Directory cannot be installed in
# editable mode». Метаданные — в setup.cfg, здесь только точка входа сборки.
from setuptools import setup

setup()
