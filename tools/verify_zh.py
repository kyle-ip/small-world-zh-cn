#!/usr/bin/env python3
from pathlib import Path

t = Path("payload/Resources/zh.lproj/localizedStrings.xml").read_text(encoding="utf-8")
checks = [
    ("RulesLanguage zh", 'key="RulesLanguage">zh</string>' in t),
    ("羊人", "羊人" in t),
    ("变身", "变身" in t),
    ("路障", "路障" in t),
    ("选择种族", "选择种族" in t),
]
for name, ok in checks:
    print(("OK" if ok else "FAIL"), name)
