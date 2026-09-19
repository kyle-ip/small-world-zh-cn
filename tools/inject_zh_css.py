#!/usr/bin/env python3
"""Inject ../css/zh.css into zh / zh-short HTML pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = '  <link rel="StyleSheet" href="../css/zh.css" type="text/css"/>\n'


def patch_file(html: Path) -> bool:
    text = html.read_text(encoding="utf-8")
    if "css/zh.css" in text:
        return False
    lower = text.lower()
    idx = lower.rfind("</head>")
    if idx < 0:
        return False
    html.write_text(text[:idx] + LINK + text[idx:], encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for sub in ("zh", "zh-short"):
        root = ROOT / "payload" / "Resources" / "compendium" / sub
        for html in root.rglob("*.html"):
            if patch_file(html):
                n += 1
    print(f"patched {n} html files")


if __name__ == "__main__":
    main()
