#!/usr/bin/env python3
"""Sanity-check installed zh pack and Steam paths."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "launcher"))
import steam_lang  # noqa: E402


def main() -> None:
    game = steam_lang.find_game_dir()
    xml = game / "Resources" / "zh.lproj" / "localizedStrings.xml"
    print("game:", game)
    print("zh.lproj:", xml.exists())
    if xml.exists():
        text = xml.read_text(encoding="utf-8")
        print("RulesLanguage=zh:", 'key="RulesLanguage">zh</string>' in text)
        print("has Chinese UI sample:", "选择种族" in text)
    print("compendium/zh:", (game / "Resources/compendium/zh").is_dir())
    print("steam language:", steam_lang.read_steam_language())
    setup = ROOT / "dist" / "SmallWorld2-zh-CN-Setup-1.0.0.exe"
    print("setup exe:", setup.exists(), setup if setup.exists() else "")


if __name__ == "__main__":
    main()
