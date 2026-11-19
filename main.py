#!/usr/bin/env python3
"""Sum up 19 November 2026 world news in one image.

Entry point for the make.fun bounty news-image-20261119.
Writes the pre-built image to /output/entry.png.
No network, no randomness, no timestamps: running it twice
produces byte-identical output, as the bounty requires.
The image itself is the entry; this program only places it
where the grader expects it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = "/output/entry.png"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
print(f"wrote {OUT}")
