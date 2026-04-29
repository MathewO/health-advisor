#!/usr/bin/env python3
"""
Build progress/review/<same-folder>/ with JPEG previews from full-res images.

- Source: each direct child of progress/ whose name matches YYYY-MM-DD_* (dated sets).
- Skips: review/, non-dated folders.
- Output: same relative path under progress/review/, **.jpg** per source image stem
  (e.g. 01-front-relaxed.png → 01-front-relaxed.jpg).

Requires Pillow. Run from repo root or this folder:
  python3 profile/body-comp/progress/generate-review-images.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

DATED_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}_")
SOURCE_EXT = {".png", ".jpg", ".jpeg", ".webp"}
# Tuned for fast IDE image preview (Cursor/VS Code); use full-res for real comparisons.
DEFAULT_MAX_EDGE = 800
DEFAULT_JPEG_QUALITY = 78


def iter_dated_folders(progress_root: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(progress_root.iterdir()):
        if not p.is_dir():
            continue
        if p.name == "review":
            continue
        if DATED_DIR.match(p.name):
            out.append(p)
    return out


def ensure_review_copy(
    src: Path,
    dest_dir: Path,
    max_edge: int,
    quality: int,
) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (src.stem + ".jpg")

    img = Image.open(src)
    try:
        from PIL import ImageOps

        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    img.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    rgb = img.convert("RGB")
    rgb.save(dest, format="JPEG", quality=quality, optimize=True)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate progress/review JPEG previews.")
    parser.add_argument(
        "--max-edge",
        type=int,
        default=DEFAULT_MAX_EDGE,
        help=f"Max width/height in pixels (default {DEFAULT_MAX_EDGE})",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_JPEG_QUALITY,
        help=f"JPEG quality 1-95 (default {DEFAULT_JPEG_QUALITY})",
    )
    args = parser.parse_args()

    progress_root = Path(__file__).resolve().parent
    review_root = progress_root / "review"
    review_root.mkdir(parents=True, exist_ok=True)

    count = 0
    for folder in iter_dated_folders(progress_root):
        dest_parent = review_root / folder.name
        for src in sorted(folder.iterdir()):
            if not src.is_file():
                continue
            if src.suffix.lower() not in SOURCE_EXT:
                continue
            try:
                ensure_review_copy(src, dest_parent, args.max_edge, args.quality)
                print(f"OK  {folder.name}/{src.name} → review/{folder.name}/{src.stem}.jpg")
                count += 1
            except Exception as e:
                print(f"ERR {src}: {e}", file=sys.stderr)

    out = sys.stderr if count == 0 else sys.stdout
    print(f"Done. {count} file(s) written under {review_root}", file=out)


if __name__ == "__main__":
    main()
