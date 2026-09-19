#!/usr/bin/env python3
"""Install / remove Chinese payload files under the Small World 2 game directory."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def bundle_payload_root() -> Path:
    """Path to packaged payload/Resources (dev tree or PyInstaller _MEIPASS)."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "payload" / "Resources"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[1] / "payload" / "Resources"


CONFIG_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SmallWorld2-zh-cn"
FONT_BACKUP = CONFIG_DIR / "backup_fonts"

PAYLOAD_MAP = [
    ("zh.lproj", Path("zh.lproj")),
    (Path("compendium") / "zh", Path("compendium") / "zh"),
    (Path("compendium") / "zh-short", Path("compendium") / "zh-short"),
    (Path("compendium") / "image" / "mdpi" / "zh", Path("compendium") / "image" / "mdpi" / "zh"),
]

# Shared CSS overrides (rulebook / expansion HTML)
CSS_MAP = [
    (Path("compendium") / "css" / "zh.css", Path("compendium") / "css" / "zh.css"),
]

FONT_FILES = (
    "arialmt.ttf",
    "futura-medium.ttf",
    "futura-condensedmedium.ttf",
    "arialboldmt.otf",
)

# Payload may ship only masters; expand to the filenames Cocos expects.
FONT_MASTERS = {
    "arialmt.ttf": "arialmt.ttf",
    "futura-medium.ttf": "arialmt.ttf",
    "futura-condensedmedium.ttf": "arialmt.ttf",
    "arialboldmt.otf": "arialboldmt.otf",
}


def zh_files_present(game_dir: Path) -> bool:
    return (game_dir / "Resources" / "zh.lproj" / "localizedStrings.xml").exists()


def _backup_stock_fonts(game_dir: Path) -> None:
    src_dir = game_dir / "Resources" / "fonts"
    FONT_BACKUP.mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        src = src_dir / name
        dst = FONT_BACKUP / name
        if src.is_file() and not dst.exists():
            shutil.copy2(src, dst)


def _install_fonts(game_dir: Path) -> None:
    src_dir = bundle_payload_root() / "fonts"
    if not src_dir.is_dir():
        return
    _backup_stock_fonts(game_dir)
    dst_dir = game_dir / "Resources" / "fonts"
    dst_dir.mkdir(parents=True, exist_ok=True)
    for dest_name, master_name in FONT_MASTERS.items():
        src = src_dir / dest_name
        if not src.is_file():
            src = src_dir / master_name
        if src.is_file():
            shutil.copy2(src, dst_dir / dest_name)


def _restore_fonts(game_dir: Path) -> None:
    dst_dir = game_dir / "Resources" / "fonts"
    if not FONT_BACKUP.is_dir():
        return
    for name in FONT_FILES:
        bak = FONT_BACKUP / name
        if bak.is_file():
            shutil.copy2(bak, dst_dir / name)


def install_fonts(game_dir: Path) -> None:
    """Install CJK UI fonts (idempotent; backs up stock fonts once)."""
    _install_fonts(game_dir)


def restore_fonts(game_dir: Path) -> None:
    """Restore stock UI fonts from backup (if present)."""
    _restore_fonts(game_dir)


def install_payload(game_dir: Path) -> None:
    src_root = bundle_payload_root()
    if not (src_root / "zh.lproj" / "localizedStrings.xml").exists():
        raise FileNotFoundError(f"Bundled Chinese payload missing: {src_root}")
    res = game_dir / "Resources"
    for rel_src, rel_dst in PAYLOAD_MAP + CSS_MAP:
        src = src_root / rel_src
        dst = res / rel_dst
        if not src.exists():
            raise FileNotFoundError(f"Missing payload part: {src}")
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    _install_fonts(game_dir)


def uninstall_payload(game_dir: Path) -> None:
    res = game_dir / "Resources"
    for _rel_src, rel_dst in PAYLOAD_MAP + CSS_MAP:
        dst = res / rel_dst
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
    _restore_fonts(game_dir)
