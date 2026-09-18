#!/usr/bin/env python3
"""Convert ja-slot Chinese assets into a real zh language pack in payload/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "payload" / "Resources"


def fix_rules_language() -> None:
    xml = PAYLOAD / "zh.lproj" / "localizedStrings.xml"
    text = xml.read_text(encoding="utf-8")
    old = '<string key="RulesLanguage">ja</string>'
    new = '<string key="RulesLanguage">zh</string>'
    if old not in text and new not in text:
        raise SystemExit(f"RulesLanguage not found in {xml}")
    xml.write_text(text.replace(old, new), encoding="utf-8")
    print("RulesLanguage -> zh")


def fix_html(folder: Path) -> int:
    n = 0
    for path in folder.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated = (
            text.replace('lang="ja"', 'lang="zh"')
            .replace("/image/mdpi/ja/", "/image/mdpi/zh/")
            .replace("../image/mdpi/ja/", "../image/mdpi/zh/")
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            n += 1
    return n


def fix_pygmy_short() -> None:
    """Short Witch Doctor page was left in English; copy body from full zh page."""
    short = PAYLOAD / "compendium" / "zh-short" / "swdm_PygmyRace.html"
    full = PAYLOAD / "compendium" / "zh" / "swdm_PygmyRace.html"
    if not short.exists() or not full.exists():
        print("Pygmy short/full missing; skip")
        return
    short_text = short.read_text(encoding="utf-8")
    if "Witch Doctor" not in short_text and "Each time you lose" not in short_text:
        print("Pygmy short already Chinese; skip")
        return
    full_text = full.read_text(encoding="utf-8")
    # Prefer a short-style page: take first <p>...</p> from full if present
    import re

    paras = re.findall(r"<p>.*?</p>", full_text, flags=re.S)
    if not paras:
        raise SystemExit("No <p> in full Pygmy page")
    # Use first content paragraph (skip empty)
    body_p = next((p for p in paras if len(re.sub(r"<[^>]+>", "", p).strip()) > 20), paras[0])
    new_short = f"""<html lang="zh" dir="ltr">
<head>
  <meta name="viewport" content="initial-scale=1.0"/>
  <meta charset="UTF-8"/>
  <link rel="StyleSheet" href="../css/race_power.css" type="text/css"/>
  <link rel="StyleSheet" href="../css/races.css" type="text/css"/>
</head>

<body>
  
{body_p}
	
	<img id="footer" src="../image/hdpi/footer.jpg"/>
</body>
</html>
"""
    short.write_text(new_short, encoding="utf-8")
    print("Fixed zh-short/swdm_PygmyRace.html")


def main() -> None:
    if not (PAYLOAD / "zh.lproj").exists():
        raise SystemExit(f"Missing payload: {PAYLOAD}")
    fix_rules_language()
    for name in ("zh", "zh-short"):
        folder = PAYLOAD / "compendium" / name
        print(f"{name}: updated {fix_html(folder)} html files")
    fix_pygmy_short()
    print("migrate_to_zh done")


if __name__ == "__main__":
    main()
