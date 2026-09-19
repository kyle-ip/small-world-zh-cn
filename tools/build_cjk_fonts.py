#!/usr/bin/env python3
"""Build CJK UI fonts for Small World 2 from Noto Sans SC VF.

Cocos UI loads Resources/fonts/{arialmt,futura-medium,futura-condensedmedium}.ttf
and arialboldmt.otf. The stock files are a thin JP Noto Medium subset that misses
many Simplified Chinese glyphs — causing tiny / fuzzy / uneven strokes at high res.

This script instantiates Noto Sans SC (OFL) at SemiBold / Bold, renames name tables
to match CCBI font names, and writes into payload/Resources/fonts/.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "payload" / "Resources" / "fonts"

VF_CANDIDATES = [
    Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
    Path(r"C:\Windows\Fonts\NotoSansSC-VariableFont_wght.ttf"),
    Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts" / "NotoSansSC-VF.ttf",
]

# Only ship weight masters; install copies arialmt → Futura filenames.
SPECS = [
    ("arialmt.ttf", 600, "Arial MT", "Medium", "ArialMT"),
    ("arialboldmt.otf", 700, "Arial MT", "Bold", "Arial-BoldMT"),
]


def find_vf() -> Path:
    for path in VF_CANDIDATES:
        if path.is_file():
            return path
    raise FileNotFoundError(
        "NotoSansSC-VF.ttf not found under Windows Fonts. "
        "Install 'Noto Sans SC' from Google Fonts first."
    )


def set_names(font: TTFont, family: str, subfamily: str, ps_name: str) -> None:
    full = f"{family} {subfamily}"
    name = font["name"]
    # Clear and rewrite common English name IDs used by FreeType / cocos
    for record in list(name.names):
        if record.nameID in (1, 2, 4, 6, 16, 17) and record.platformID in (1, 3):
            name.names.remove(record)
    # platform 3 (Windows), encoding 1 (Unicode BMP), lang 0x409
    for nid, value in (
        (1, family),
        (2, subfamily),
        (4, full),
        (6, ps_name),
        (16, family),
        (17, subfamily),
    ):
        name.setName(value, nid, 3, 1, 0x409)
        name.setName(value, nid, 1, 0, 0)  # Mac Roman fallback


def build_one(vf_path: Path, weight: int, family: str, subfamily: str, ps_name: str) -> TTFont:
    print(f"  instantiate wght={weight} → {ps_name} …")
    base = TTFont(str(vf_path))
    font = instantiateVariableFont(base, {"wght": weight}, inplace=False)
    set_names(font, family, subfamily, ps_name)
    # Prefer TrueType for .ttf; keep glyf
    return font


def main() -> int:
    vf = find_vf()
    print(f"Source VF: {vf} ({vf.stat().st_size // 1024} KB)")
    OUT.mkdir(parents=True, exist_ok=True)

    # Build unique weights once, then clone name tables / save
    cache: dict[int, TTFont] = {}
    for filename, weight, family, subfamily, ps_name in SPECS:
        if weight not in cache:
            cache[weight] = build_one(vf, weight, family, subfamily, ps_name)
        # Fresh copy of the instantiated font for each output name
        tmp = ROOT / "dist" / "build" / f"_font_{weight}.ttf"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        cache[weight].save(str(tmp))
        font = TTFont(str(tmp))
        set_names(font, family, subfamily, ps_name)
        out = OUT / filename
        font.save(str(out))
        font.close()
        print(f"  wrote {out.name} ({out.stat().st_size // 1024} KB)")

    # Keep a copy of medium as the shared body face for docs
    medium = OUT / "arialmt.ttf"
    for twin in ("futura-medium.ttf",):
        # already written with correct names; nothing else
        pass
    print(f"Done → {OUT}")
    print("Note: fonts are OFL (Noto Sans SC). Redistribute with license notice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
