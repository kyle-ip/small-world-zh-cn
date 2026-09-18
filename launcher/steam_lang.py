#!/usr/bin/env python3
"""Steam language helpers for Small World 2 (appid 235620).

Chinese is enabled by junctioning the *currently active* Steam language slot
(``.lproj``) to ``zh.lproj``. Steam language itself is left unchanged, so the
user does not need to pick Dutch (or any specific language) in Steam.

``RulesLanguage`` inside the Chinese pack is ``zh``, so the compendium loads
from ``compendium/zh`` without touching other language folders.
"""
from __future__ import annotations

import ctypes
import json
import os
import re
import shutil
import subprocess
import winreg
from pathlib import Path

APPID = "235620"

# Steam API language name → .lproj folder code
STEAM_LANG_TO_CODE = {
    "english": "en",
    "german": "de",
    "french": "fr",
    "italian": "it",
    "spanish": "es",
    "japanese": "ja",
    "dutch": "nl",
    "schinese": "zh",
    "tchinese": "zh",
}

FILE_ATTRIBUTE_REPARSE_POINT = 0x400
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

CONFIG_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SmallWorld2-zh-cn"
CONFIG_PATH = CONFIG_DIR / "config.json"
BACKUP_ROOT = CONFIG_DIR / "backup_lproj"


def steam_root() -> Path:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
            value, _ = winreg.QueryValueEx(key, "SteamPath")
            return Path(value)
    except OSError:
        pass
    for candidate in (
        Path(r"C:\Program Files (x86)\Steam"),
        Path(r"C:\Program Files\Steam"),
    ):
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Steam install not found")


def library_folders(steam: Path) -> list[Path]:
    roots = [steam / "steamapps"]
    vdf = steam / "steamapps" / "libraryfolders.vdf"
    if not vdf.exists():
        return roots
    text = vdf.read_text(encoding="utf-8", errors="ignore")
    for match in re.finditer(r'"path"\s+"([^"]+)"', text):
        roots.append(Path(match.group(1)) / "steamapps")
    seen: set[str] = set()
    out: list[Path] = []
    for p in roots:
        key = str(p).lower()
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def find_appmanifest() -> Path:
    for folder in library_folders(steam_root()):
        path = folder / f"appmanifest_{APPID}.acf"
        if path.exists():
            return path
    raise FileNotFoundError(f"appmanifest_{APPID}.acf not found (is Small World 2 installed?)")


def find_game_dir() -> Path:
    manifest = find_appmanifest()
    text = manifest.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'"installdir"\s+"([^"]+)"', text)
    if not m:
        raise FileNotFoundError("installdir missing from appmanifest")
    return manifest.parent / "common" / m.group(1)


def read_steam_language(manifest: Path | None = None) -> str:
    path = manifest or find_appmanifest()
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(
        r'"UserConfig"\s*\{[^}]*?"language"\s+"([^"]+)"',
        text,
        flags=re.S,
    )
    if m:
        return m.group(1)
    m = re.search(r'"language"\s+"([^"]+)"', text)
    if m:
        return m.group(1)
    return "english"


def set_steam_language(language: str, manifest: Path | None = None) -> None:
    """Optional; Chinese enable no longer requires changing Steam language."""
    path = manifest or find_appmanifest()
    text = path.read_text(encoding="utf-8", errors="ignore")

    def replace_in_block(block_name: str, src: str) -> str:
        pattern = rf'("{block_name}"\s*\{{)(.*?)(\n\s*\}})'
        match = re.search(pattern, src, flags=re.S)
        if not match:
            return src
        body = match.group(2)
        if re.search(r'"language"\s+"[^"]+"', body):
            body2 = re.sub(
                r'"language"\s+"[^"]+"', f'"language"\t\t"{language}"', body, count=1
            )
        else:
            body2 = body.rstrip() + f'\n\t\t"language"\t\t"{language}"\n\t'
        return src[: match.start()] + match.group(1) + body2 + match.group(3) + src[match.end() :]

    updated = replace_in_block("UserConfig", text)
    updated = replace_in_block("MountedConfig", updated)
    if updated == text:
        updated = re.sub(r'"language"\s+"[^"]+"', f'"language"\t\t"{language}"', text, count=1)
    path.write_text(updated, encoding="utf-8")


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"chinese_enabled": False, "carrier_code": None, "steam_language": None}


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def zh_pack_installed(game_dir: Path | None = None) -> bool:
    root = game_dir or find_game_dir()
    return (root / "Resources" / "zh.lproj" / "localizedStrings.xml").exists()


def steam_lang_to_code(steam_lang: str) -> str:
    code = STEAM_LANG_TO_CODE.get(steam_lang.lower())
    if not code or code == "zh":
        # schinese not a real stock pack; fall back to english slot
        return "en"
    return code


def _is_reparse_point(path: Path) -> bool:
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    if attrs == INVALID_FILE_ATTRIBUTES:
        return False
    return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)


def _path_present(path: Path) -> bool:
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    return attrs != INVALID_FILE_ATTRIBUTES


def _remove_path(path: Path) -> None:
    if not _path_present(path):
        return
    if _is_reparse_point(path):
        r = subprocess.run(
            ["cmd", "/c", "rmdir", str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        if r.returncode != 0 and _path_present(path):
            raise RuntimeError(f"Failed to remove junction: {path}\n{r.stderr or r.stdout}")
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _lproj_path(game: Path, code: str) -> Path:
    return game / "Resources" / f"{code}.lproj"


def _backup_path(code: str) -> Path:
    return BACKUP_ROOT / f"{code}.lproj"


def _looks_like_zh_lproj(lproj: Path, game: Path) -> bool:
    zh_xml = game / "Resources" / "zh.lproj" / "localizedStrings.xml"
    xml = lproj / "localizedStrings.xml"
    if not xml.exists() or not zh_xml.exists():
        return False
    try:
        return xml.read_bytes() == zh_xml.read_bytes()
    except OSError:
        return False


def _find_hooked_carriers(game: Path) -> list[str]:
    """Return language codes whose .lproj is junctioned/copied to Chinese."""
    hooked: list[str] = []
    res = game / "Resources"
    if not res.exists():
        return hooked
    for path in res.glob("*.lproj"):
        code = path.name[: -len(".lproj")]
        if code == "zh":
            continue
        if _is_reparse_point(path) or _looks_like_zh_lproj(path, game):
            hooked.append(code)
    return hooked


def _restore_code(game: Path, code: str) -> None:
    carrier = _lproj_path(game, code)
    if _path_present(carrier):
        _remove_path(carrier)
    backup = _backup_path(code)
    if not backup.exists():
        # Migrate from 1.1.x dutch-carrier backups
        legacy = CONFIG_DIR / "backup_nl" / f"{code}.lproj"
        if legacy.exists():
            backup = legacy
    if backup.exists():
        shutil.copytree(backup, carrier)


def _clear_all_hooks(game: Path) -> None:
    """Restore any language slot previously used as Chinese carrier (incl. old nl)."""
    for code in set(_find_hooked_carriers(game) + ["nl", "ja", "en", "de", "fr", "es", "it"]):
        carrier = _lproj_path(game, code)
        if not _path_present(carrier):
            continue
        if _is_reparse_point(carrier) or _looks_like_zh_lproj(carrier, game):
            _restore_code(game, code)


def _backup_if_needed(game: Path, code: str) -> None:
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    dest = _backup_path(code)
    if dest.exists():
        return
    carrier = _lproj_path(game, code)
    if _path_present(carrier) and not _is_reparse_point(carrier) and not _looks_like_zh_lproj(
        carrier, game
    ):
        shutil.copytree(carrier, dest)


def _link_code_to_zh(game: Path, code: str) -> None:
    zh = game / "Resources" / "zh.lproj"
    if not zh.exists():
        raise FileNotFoundError(f"Missing Chinese assets: {zh}")
    carrier = _lproj_path(game, code)
    if _is_reparse_point(carrier):
        return
    if _path_present(carrier):
        _remove_path(carrier)
    r = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(carrier), str(zh)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    if r.returncode != 0:
        if _path_present(carrier):
            _remove_path(carrier)
        shutil.copytree(zh, carrier)


def chinese_hook_active(game_dir: Path | None = None) -> bool:
    game = game_dir or find_game_dir()
    return bool(_find_hooked_carriers(game))


def apply_chinese_enabled(enabled: bool) -> str:
    """Toggle Chinese on the active Steam language slot. Returns that Steam language name."""
    manifest = find_appmanifest()
    game = find_game_dir()
    cfg = load_config()
    steam_lang = read_steam_language(manifest)
    code = steam_lang_to_code(steam_lang)

    if enabled:
        if not zh_pack_installed(game):
            raise FileNotFoundError("Chinese pack not installed (zh.lproj missing)")

        # Drop previous carrier (e.g. old dutch/nl hook, or switched Steam language)
        _clear_all_hooks(game)

        _backup_if_needed(game, code)
        _link_code_to_zh(game, code)

        cfg["chinese_enabled"] = True
        cfg["carrier_code"] = code
        cfg["steam_language"] = steam_lang
        # Keep Steam language as-is — do not force dutch
        save_config(cfg)
        return steam_lang

    # disable: restore whatever we hooked
    carrier = cfg.get("carrier_code")
    if carrier:
        _restore_code(game, carrier)
    _clear_all_hooks(game)

    cfg["chinese_enabled"] = False
    cfg["carrier_code"] = None
    save_config(cfg)
    return steam_lang


def launch_game() -> None:
    steam = steam_root() / "steam.exe"
    if steam.exists():
        subprocess.Popen([str(steam), f"steam://rungameid/{APPID}"], close_fds=True)
        return
    exe = find_game_dir() / "SmallWorld.exe"
    subprocess.Popen([str(exe)], cwd=str(exe.parent), close_fds=True)
