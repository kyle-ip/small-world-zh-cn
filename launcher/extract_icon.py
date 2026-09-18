#!/usr/bin/env python3
"""Extract the real icon resource from SmallWorld.exe (via icoextract)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT.parent / "SmallWorld.exe"
OUT = Path(__file__).resolve().parent / "app.ico"
OUT_INSTALLER = ROOT / "installer" / "app.ico"


def main() -> None:
    from icoextract import IconExtractor

    if not EXE.exists():
        raise SystemExit(f"Not found: {EXE}")
    IconExtractor(str(EXE)).export_icon(str(OUT), num=0)
    OUT_INSTALLER.parent.mkdir(parents=True, exist_ok=True)
    OUT_INSTALLER.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes) from {EXE.name}")


if __name__ == "__main__":
    main()
