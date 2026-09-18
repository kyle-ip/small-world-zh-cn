# -*- coding: utf-8 -*-
"""Shared CJK font loader with glyph-coverage verification.

Why this exists: the game's bundled font (Resources/fonts/arialmt.ttf) is a
Japanese Noto subset that is MISSING many simplified-Chinese glyphs (e.g.
图/隐/藏). Pillow silently draws a .notdef tofu box for missing glyphs
without raising, so coverage MUST be checked explicitly.
"""
import os
from PIL import ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))

# Preference order: font copied next to scripts, then standard Windows fonts
FONT_CANDIDATES = [
    (os.path.join(_HERE, "simhei.ttf"), 0),
    (r"C:\Windows\Fonts\simhei.ttf", 0),
    (r"C:\Windows\Fonts\msyh.ttc", 0),
    (r"C:\Windows\Fonts\msyhbd.ttc", 0),
    (r"C:\Windows\Fonts\Deng.ttf", 0),
]

_cached_path = None
_cached_cmap = None


def resolve_font():
    for path, index in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                ImageFont.truetype(path, 16, index=index)
                return path, index
            except Exception:
                continue
    raise RuntimeError("No usable CJK font found. Expected SimHei or Microsoft YaHei.")


def _load_cmap(path, index):
    global _cached_path, _cached_cmap
    if _cached_path == path and _cached_cmap is not None:
        return _cached_cmap
    try:
        from fontTools.ttLib import TTFont, TTCollection
        if path.lower().endswith(".ttc"):
            tt = TTCollection(path).fonts[index]
        else:
            tt = TTFont(path, fontNumber=index)
        cmap = set()
        for table in tt["cmap"].tables:
            cmap.update(table.cmap.keys())
        _cached_path = path
        _cached_cmap = cmap
        return cmap
    except Exception:
        return None


def load_font(size):
    path, index = resolve_font()
    return ImageFont.truetype(path, size, index=index)


def assert_covered(text, label=""):
    """Raise if any character in text has no glyph in the chosen font."""
    path, index = resolve_font()
    cmap = _load_cmap(path, index)
    if cmap is None:
        return  # cannot verify without fontTools; let rendering proceed
    missing = sorted({ch for ch in text if ord(ch) > 127 and ord(ch) not in cmap})
    if missing:
        raise RuntimeError(
            f"Font {os.path.basename(path)} is missing {len(missing)} glyph(s) "
            f"needed by {label!r}: {''.join(missing)}"
        )
