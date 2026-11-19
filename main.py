#!/usr/bin/env python3
"""19 Nov 2026 front-page image — entry point.

The picture is already drawn (entry.png in this folder). All this
program does is place a byte-identical copy where the grader looks
for it: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when
that variable is not set.

Why a copy and not a redraw: the grader runs this program in a
container where the repository is mounted read-only, so writing
the picture next to this script would fail. The output folder is
the only writable place, so the copy goes there.

Deterministic by construction: the same entry.png bytes go in,
the same bytes come out, on every run.
"""
import os
import shutil
import sys

FOLDER = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(FOLDER, "entry.png")


def main():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(PICTURE, target)
    size = os.path.getsize(target)
    print("wrote", target, size, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
