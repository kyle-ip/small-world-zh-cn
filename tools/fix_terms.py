#!/usr/bin/env python3
"""One-shot terminology polish for zh localizedStrings.xml."""
from __future__ import annotations

import re
from pathlib import Path

XML = (
    Path(__file__).resolve().parents[1]
    / "payload"
    / "Resources"
    / "zh.lproj"
    / "localizedStrings.xml"
)

FIXES = {
    "RulesLanguage": "zh",
    "swdm::FaunRace_Name": "羊人",
    "swdm::BarricadePower_Name": "路障",
    "swdm::WerePower_Name": "变身",
}


def set_key(text: str, key: str, value: str) -> str:
    pattern = rf'(<string key="{re.escape(key)}">)(.*?)(</string>)'
    new_text, n = re.subn(pattern, rf"\g<1>{value}\g<3>", text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Failed to set {key} (matches={n})")
    return new_text


def main() -> None:
    text = XML.read_text(encoding="utf-8")
    for key, value in FIXES.items():
        text = set_key(text, key, value)
    XML.write_text(text, encoding="utf-8")
    for key in FIXES:
        m = re.search(rf'<string key="{re.escape(key)}">(.*?)</string>', text)
        print(f"{key} = {m.group(1)}")


if __name__ == "__main__":
    main()
