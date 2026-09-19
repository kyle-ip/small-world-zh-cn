# Small World 2 — Simplified Chinese Pack

[![Release](https://img.shields.io/github/v/release/kyle-ip/small-world-zh-cn?label=release)](https://github.com/kyle-ip/small-world-zh-cn/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4)](https://github.com/kyle-ip/small-world-zh-cn/releases)
[![Status](https://img.shields.io/badge/status-unofficial-orange)](#disclaimer)

Unofficial **Simplified Chinese** language pack for the Steam version of *Small World 2*.

![Launcher / landscape art](./assets/Default-Landscape.png)

A single Windows EXE embeds strings, baked UI art, rulebook HTML, and CJK fonts. Enable installs Chinese resources and hooks the active Steam language slot (no need to switch Steam to Dutch or any fixed language). Disable restores the previous language pack.

> **Not affiliated with** [Days of Wonder](https://www.days-of-wonder.com/), Asmodee, or Valve. Personal / learning use only.

---

## Features

- Full UI string tables (`zh.lproj`) plus baked Chinese menu / race / power plates
- Compendium / rulebook pages in Simplified Chinese
- Thicker CJK UI fonts ([Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC), SIL OFL) under the font names Cocos already loads
- Rulebook CSS tweaks for high-resolution displays
- Hooks whatever language Steam is currently using (English, Japanese, …)
- Reversible: stock language pack and fonts are backed up under `%LOCALAPPDATA%\SmallWorld2-zh-cn\`
- One-file player build — no Python and no separate installer

## Requirements

| Role | Need |
|------|------|
| **Players** | Windows, Steam *Small World 2*, admin rights if the game is under `Program Files` |
| **Developers** | Python 3.11+, packages in [`requirements.txt`](requirements.txt) |

Steam app ID: `235620`.

Compatible with the unofficial [HD pack](https://github.com/kyle-ip/small-world-hd).

## Install (players)

1. Download **`SmallWorld-cn.exe`** from [Releases](https://github.com/kyle-ip/small-world-zh-cn/releases/latest).
2. Double-click the EXE.
3. Click **启用中文**, then start the game from Steam or via **启动游戏**.

You do **not** need to change the Steam language. Quit the game before toggling Chinese on or off. Steam “Verify integrity of game files” may restore official files — enable Chinese again afterward.

### CLI

```bat
SmallWorld-cn.exe --enable
SmallWorld-cn.exe --disable
SmallWorld-cn.exe --launch
SmallWorld-cn.exe --uninstall
```

| Flag | Meaning |
|------|---------|
| `--enable` | Install Chinese payload and enable the language hook |
| `--disable` | Restore the previous language pack / fonts |
| `--launch` | Start the game via Steam (does not change the Chinese switch by itself) |
| `--uninstall` | Remove the Chinese install and clear local config where applicable |

## Development

```bat
git clone https://github.com/kyle-ip/small-world-zh-cn.git
cd small-world-zh-cn
python -m pip install -r requirements.txt
python launcher\app.py
```

The clone includes a complete `payload/` (strings, images, compendium, OFL fonts). That is enough to run the launcher or rebuild the player EXE:

```bat
powershell -ExecutionPolicy Bypass -File tools\build_allinone.ps1
```

Icon extraction uses a local `SmallWorld.exe` when available (`icoextract`).

Regenerating baked art from English/Japanese sources additionally needs a *Small World 2* install and the scripts under `tools/` (see `docs/`).

### Repository layout

```text
payload/     Chinese assets (embedded into the EXE at build time)
launcher/    GUI, Steam language hook, payload install
tools/       Build, localization, and verification scripts
docs/        Design notes and known issues
installer/   Legacy Inno Setup flow (optional; EXE is the supported deliverable)
glossary/    Terminology reference
```

## Related projects

- [small-world-hd](https://github.com/kyle-ip/small-world-hd) — unofficial HD texture / polish overlay

## Disclaimer

This is an unofficial fan project for personal learning.

- Do **not** sell this patch.
- Do **not** redistribute *Small World 2* or official Days of Wonder assets as a standalone game dump.
- Bundled CJK fonts are **Noto Sans SC** ([SIL Open Font License](https://scripts.sil.org/OFL)).
- Use at your own risk; keep Steam verify / the built-in disable path available.
