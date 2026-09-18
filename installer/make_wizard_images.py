#!/usr/bin/env python3
"""Generate Inno Setup wizard bitmaps (modern light theme)."""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("需要 Pillow: pip install Pillow") from exc

OUT = Path(__file__).resolve().parent


def font(size: int):
    for name in (
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        p = Path(name)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def make_side() -> None:
    # Classic Inno modern side image ~164x314 at 100%; larger looks better
    w, h = 164, 314
    img = Image.new("RGB", (w, h), (232, 242, 252))
    draw = ImageDraw.Draw(img)
    # soft gradient bars
    for y in range(h):
        t = y / h
        r = int(220 + 20 * t)
        g = int(235 + 10 * t)
        b = int(250 - 10 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # box icon
    cx, cy = w // 2, h // 2 - 20
    draw.rounded_rectangle([cx - 36, cy - 28, cx + 36, cy + 20], radius=6, outline=(50, 120, 200), width=3)
    draw.polygon(
        [(cx - 40, cy - 28), (cx, cy - 48), (cx + 40, cy - 28)],
        outline=(50, 120, 200),
    )
    draw.ellipse([cx - 18, cy - 8, cx + 18, cy + 28], outline=(50, 120, 200), width=3)
    draw.text((w // 2, h - 48), "ZH-CN", font=font(18), fill=(40, 90, 160), anchor="mm")
    img.save(OUT / "wizard-side.bmp")


def make_small() -> None:
    img = Image.new("RGB", (55, 55), (232, 242, 252))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([8, 14, 47, 42], radius=4, outline=(50, 120, 200), width=2)
    draw.text((27, 28), "中", font=font(18), fill=(40, 90, 160), anchor="mm")
    img.save(OUT / "wizard-small.bmp")


if __name__ == "__main__":
    make_side()
    make_small()
    print("Wrote wizard-side.bmp / wizard-small.bmp")
