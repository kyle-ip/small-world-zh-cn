# Known gaps / follow-ups

## Coverage
- UI strings, race/power names, DLC titles: largely complete
- Compendium full + short HTML: largely complete
- Banner / UI baked-text images: largely complete

## Remaining gaps
- Region diagram JPGs still English (`Rules-regionsP*-en.jpg`)
- HD Royal Bonus expansion thumbnails may still show Japanese art
- Tutorial video remains English (YouTube)
- credits.html is shared across languages — not modified by this pack
- Some compendium sentences still read as machine-translated

## Fonts (v2.1.0+)
- Enabling Chinese installs **Noto Sans SC SemiBold/Bold** into `Resources/fonts/`
  (replacing the stock JP Noto Medium subset) so UI / expansion titles stay readable
  at high resolution. Stock fonts are backed up under
  `%LOCALAPPDATA%\SmallWorld2-zh-cn\backup_fonts\` and restored on uninstall.
- Rulebook HTML links `compendium/css/zh.css` for larger CJK-friendly sizing.

## Terminology already adjusted in v1.0.0
- Fauns → 羊人
- Barricade → 路障
- Were- → 变身
- Pygmy (Witch Doctor) short page translated

## How Chinese is selected

The helper detects your **current Steam game language** (e.g. Japanese → `ja.lproj`,
English → `en.lproj`) and junctions that folder to `zh.lproj`. Steam language is
**not** forced to Dutch anymore.

Use **启动游戏** / setup `--enable` after changing Steam language so the
correct slot is hooked. **关闭中文** restores the backed-up original pack.

Backups live under `%LOCALAPPDATA%\SmallWorld2-zh-cn\backup_lproj\`.
