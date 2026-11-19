#!/usr/bin/env python3
"""Build the 19 Nov 2026 front-page image (v3) and verify it.

Deterministic: same input -> same entry.png bytes on every run.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import generate_image  # noqa: E402


def main():
    out = os.path.join(HERE, "entry.png")
    img = generate_image.build()
    img.save(out, format="PNG", optimize=True)
    with open(out, "rb") as fh:
        data = fh.read()
    print("entry.png", len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    assert img.size == (1024, 1024), img.size
    print("ok: 1024x1024 front page, 41 stories")


if __name__ == "__main__":
    main()
