#!/usr/bin/env python3
"""Print EXIF DateTimeOriginal for each *.png under progress/*/."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def datetime_original(path: Path) -> str | None:
    img = Image.open(path)
    ex = img.getexif()
    if not ex:
        return None
    try:
        sub = ex.get_ifd(0x8769)
        if sub:
            dt = sub.get(36867) or sub.get(36868)
            if dt:
                return str(dt)
    except Exception:
        pass
    for tag in (36867, 306, 36868):
        v = ex.get(tag)
        if v:
            return str(v)
    return None


def main() -> None:
    root = Path(__file__).resolve().parent
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        print(f"=== {folder.name}")
        for png in sorted(folder.glob("*.png")):
            print(f"  {png.name}  {datetime_original(png)}")


if __name__ == "__main__":
    main()
