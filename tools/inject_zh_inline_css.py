#!/usr/bin/env python3
"""Inject strong inline CJK CSS into zh HTML (WebView-safe, ASCII-only names)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!--sw2zh-inline-->"
INLINE = """<!--sw2zh-inline-->
  <style type="text/css">
  html{font-size:20px!important}
  html,body,p,li,a,a.toc_item,h1,h2,h3,div,span,ul,ol{
    font-family:"SW2Zh","Microsoft YaHei",SimHei,sans-serif!important;
    font-weight:bold!important;
  }
  body,p,li{line-height:1.55!important}
  a,a.toc_item{font-size:1.2em!important;text-shadow:0 0 .6px currentColor,0 0 .6px currentColor}
  p,li{font-size:1.15em!important}
  h1{font-size:1.45em!important}
  </style>
"""


def patch(text: str) -> str | None:
    if MARKER in text:
        # Replace existing broken/old block
        text = re.sub(
            r"<!--sw2zh-inline-->.*?</style>\s*",
            "",
            text,
            count=1,
            flags=re.I | re.S,
        )
    low = text.lower()
    if re.search(r"<style>\s*</style>", text, flags=re.I):
        return re.sub(r"<style>\s*</style>", INLINE, text, count=1, flags=re.I)
    idx = low.rfind("</head>")
    if idx < 0:
        return None
    return text[:idx] + INLINE + text[idx:]


def main() -> None:
    n = 0
    for sub in ("zh", "zh-short"):
        root = ROOT / "payload" / "Resources" / "compendium" / sub
        for html in root.rglob("*.html"):
            original = html.read_text(encoding="utf-8")
            updated = patch(original)
            if updated and updated != original:
                html.write_text(updated, encoding="utf-8")
                n += 1
    print(f"inline patched {n}")


if __name__ == "__main__":
    main()
