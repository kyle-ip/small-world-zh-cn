#!/usr/bin/env python3
"""Copy payload zh* into the detected Small World 2 install (dev / CLI install)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "payload" / "Resources"
sys.path.insert(0, str(ROOT / "launcher"))
import steam_lang  # noqa: E402


MAPPINGS = [
    ("zh.lproj", Path("zh.lproj")),
    (Path("compendium") / "zh", Path("compendium") / "zh"),
    (Path("compendium") / "zh-short", Path("compendium") / "zh-short"),
    (Path("compendium") / "image" / "mdpi" / "zh", Path("compendium") / "image" / "mdpi" / "zh"),
]


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    game = steam_lang.find_game_dir()
    res = game / "Resources"
    print(f"Game: {game}")
    for rel_src, rel_dst in MAPPINGS:
        src = PAYLOAD / rel_src
        dst = res / rel_dst
        if not src.exists():
            raise SystemExit(f"Missing payload: {src}")
        print(f"  {src.name if isinstance(rel_src, str) else rel_src} -> {dst}")
        copytree(src, dst)

    # Optional: install launcher scripts beside game
    launch_dst = game / "SmallWorld2-zh-cn-Launcher"
    launch_dst.mkdir(exist_ok=True)
    for name in ("app.py", "steam_lang.py"):
        shutil.copy2(ROOT / "launcher" / name, launch_dst / name)
    bat = launch_dst / "启用中文启动器.bat"
    bat.write_text(
        "@echo off\r\n"
        "chcp 65001 >nul\r\n"
        "cd /d \"%~dp0\"\r\n"
        "py -3 app.py 2>nul || python app.py\r\n",
        encoding="utf-8",
    )
    print("Installed launcher folder:", launch_dst)
    print("Done.")


if __name__ == "__main__":
    main()
