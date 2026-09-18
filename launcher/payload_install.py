#!/usr/bin/env python3
"""Install / remove Chinese payload files under the Small World 2 game directory."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path


def bundle_payload_root() -> Path:
    """Path to packaged payload/Resources (dev tree or PyInstaller _MEIPASS)."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "payload" / "Resources"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[1] / "payload" / "Resources"


PAYLOAD_MAP = [
    ("zh.lproj", Path("zh.lproj")),
    (Path("compendium") / "zh", Path("compendium") / "zh"),
    (Path("compendium") / "zh-short", Path("compendium") / "zh-short"),
    (Path("compendium") / "image" / "mdpi" / "zh", Path("compendium") / "image" / "mdpi" / "zh"),
]


def zh_files_present(game_dir: Path) -> bool:
    return (game_dir / "Resources" / "zh.lproj" / "localizedStrings.xml").exists()


def install_payload(game_dir: Path) -> None:
    src_root = bundle_payload_root()
    if not (src_root / "zh.lproj" / "localizedStrings.xml").exists():
        raise FileNotFoundError(f"Bundled Chinese payload missing: {src_root}")
    res = game_dir / "Resources"
    for rel_src, rel_dst in PAYLOAD_MAP:
        src = src_root / rel_src
        dst = res / rel_dst
        if not src.exists():
            raise FileNotFoundError(f"Missing payload part: {src}")
        if dst.exists():
            shutil.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)


def uninstall_payload(game_dir: Path) -> None:
    res = game_dir / "Resources"
    for _rel_src, rel_dst in PAYLOAD_MAP:
        dst = res / rel_dst
        if dst.exists():
            shutil.rmtree(dst)
