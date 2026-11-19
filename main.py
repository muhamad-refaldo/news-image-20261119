#!/usr/bin/env python3
"""Sum up 19 November 2026 world news in one image.

Writes the pre-built image to /output/entry.png.
No network, no randomness, no timestamps: running it twice
produces byte-identical output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = "/output/entry.png"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
print(f"wrote {OUT}")
