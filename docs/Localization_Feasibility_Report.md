# Small World 2 — Chinese Localization Patch/Plugin Feasibility Report

> Analysis Date: 2026-09-18
> Game Directory: `c:\Program Files (x86)\Steam\steamapps\common\SmallWorld2`

---

## 1. Game Architecture Overview

### 1.1 Engine & Tech Stack

| Item | Details |
|------|---------|
| **Game Engine** | cocos2d-x (C++) |
| **Executable** | `SmallWorld.exe` |
| **UI Description Format** | `.ccbi` (CocosBuilder binary files) |
| **Sprite Atlases** | `.plist` (Cocos2d texture atlas config) |
| **Rules Book / Credits** | HTML (rendered via embedded WebKit) |
| **Network** | Steam API + libcurl |
| **Local Storage** | SQLite3 |
| **Audio / Input** | SDL2 |

### 1.2 Key Dependencies

- `WebKit.dll` / `JavaScriptCore.dll` — Embedded browser for rendering the Compendium (rules book) and credits page
- `libxml2.dll` / `libxslt.dll` — XML parsing (localization files)
- `glew32.dll` / `cairo.dll` — Graphics rendering
- `steam_api.dll` — Steam integration

---

## 2. Localization System Analysis

### 2.1 Directory Structure

The game uses Apple-style `.lproj` directories for multilingual resources:

```
Resources/
├── en.lproj/          English
├── fr.lproj/          French
├── de.lproj/          German
├── es.lproj/          Spanish
├── it.lproj/          Italian
├── ja.lproj/          Japanese
├── nl.lproj/          Dutch
├── compendium/        Rules book (HTML)
│   ├── en/  en-short/
│   ├── ja/  ja-short/
│   └── ...
└── fonts/             Font files
```

**There is currently no Chinese (zh) language pack.**

### 2.2 Text Resources

Each `.lproj` directory contains the following text files:

| File | String Count | Content |
|------|-------------|---------|
| `localizedStrings.xml` | 281 | Main UI text, race/power names, messages |
| `tooltips.xml` | 77 | Tooltips |
| `errorMessages.xml` | 28 | Error messages |
| `ssoStrings.xml` | 91 | Login / authentication |
| `Localizable.strings` | 9 | Push notifications (Apple .strings format) |
| **Total** | **~486** | |

**Text format example** (`localizedStrings.xml`):
```xml
<string key="swdm::AmazonRace_Name">Amazons</string>
<string key="MessageBox_OK">OK</string>
```

Text is loaded via **key-value pairs** with no hardcoded strings — translation difficulty is low.

### 2.3 Image Resources

Each `.lproj` directory contains `common/` and `common-hd/` subdirectories with localized images containing baked-in text:

- **180 (common) + 180 (common-hd) = 360 images**
- Includes button labels, titles, race/power icon text, etc.
- The Italian pack additionally provides `images.xml` (translation reference, not used at runtime)

### 2.4 Rules Book (Compendium)

The rules book is in HTML format, rendered via embedded WebKit:

- **Full version**: 107 HTML files (races, powers, rules, guides)
- **Short version**: 71 HTML files
- Uses jQuery 1.9.1 + CSS styling

### 2.5 Credits Page

- `Resources/credits/credits.html` — Single HTML file

---

## 3. Font Support Analysis

### 3.1 Font Files

| File | Actual Font | Size |
|------|------------|------|
| `arialmt.ttf` | Noto Sans Medium | 1.15 MB |
| `futura-medium.ttf` | Identical to arialmt.ttf | 1.15 MB |
| `futura-condensedmedium.ttf` | Noto Sans Condensed Medium | 1.15 MB |

### 3.2 Chinese Character Support

- **Total glyphs**: 6,588
- **CJK Unified Ideographs**: **5,932** (U+4E00–U+9FFF range)
- **Hiragana**: 174
- **Katakana**: 180
- **Hangul**: 0

**Conclusion**: The built-in font already supports common Chinese characters (covering ~88% of GB2312's 6,763 characters). **No font replacement is needed to display Chinese.**

### 3.3 Text Rendering

UI text is rendered via cocos2d-x's `CCLabelTTF`, using TrueType fonts with dynamic glyph generation for Chinese characters.

---

## 4. Language Switching Mechanism

### 4.1 Language Detection

The game determines the current language via three methods:

1. **System language**: Calls Windows API `GetUserDefaultUILanguage()`
2. **Command-line argument**: `SmallWorld.exe language=ja`
3. **In-game settings**

### 4.2 Supported Language List

The supported languages hardcoded in the executable are:
```
de | en | es | fr | ja | nl
```
(Italian `it` has a language pack but is not in this list — possibly added in a later patch.)

### 4.3 Language-to-Resource Mapping

The game maps the `LanguageType` enum to a 2-letter language code, then loads the `<code>.lproj/` directory. If the system language is not in the supported list, it **falls back to English (en.lproj)**.

**Key issue**: A Chinese system language would be recognized but not in the supported list, so it falls back to English — **a Chinese language pack cannot be loaded directly.**

### 4.4 Online Considerations

- The language code is sent to the Days of Wonder online server
- The `RulesLanguage` field determines which language's compendium HTML to load
- Online play includes a version check

---

## 5. Localization Approach Evaluation

### 5.1 Approach Comparison

| Approach | Description | Feasibility | Risk | Reversibility |
|----------|-------------|-------------|------|---------------|
| **A: Replace Japanese pack** | Overwrite `ja.lproj` with Chinese, launch with `language=ja` | ★★★★★ | Low | Fully reversible |
| **B: Replace English pack** | Overwrite `en.lproj` with Chinese, default launch is Chinese | ★★★★ | Low | Reversible |
| **C: Add zh language pack** | Create `zh.lproj`, patch executable to recognize Chinese | ★★ | High (may trigger Steam verification / version check) | Difficult |
| **D: DLL proxy injection** | Intercept language detection via proxy DLL | ★★★ | Medium | Reversible |

### 5.2 Recommended Approach: A (Replace Japanese Pack + Command-Line Launch)

**Rationale**:
1. The Japanese pack already uses the CJK font, so Chinese display works seamlessly
2. No executable modification — does not trigger Steam integrity verification
3. Fully reversible — delete Chinese files to restore
4. Flexible switching via launch parameters

**Implementation Steps**:
1. Back up the original `ja.lproj` directory and `compendium/ja/`, `compendium/ja-short/`
2. Write Chinese translations into all XML/strings files under `ja.lproj/`
3. Write Chinese rules book HTML into `compendium/ja/` and `compendium/ja-short/`
4. Create 360 Chinese-localized images (or use a text-overlay approach)
5. Provide launcher batch files:
   - `Launch-Chinese.bat`: `SmallWorld.exe language=ja`
   - `Launch-Original.bat`: Normal launch (uses system language)

### 5.3 Lossless Enable/Disable Scheme

**Directory structure design**:
```
SmallWorld2/
├── Resources/
│   ├── ja.lproj/              ← Currently active (Chinese or original)
│   ├── ja.lproj.original/     ← Original Japanese backup
│   └── ja.lproj.chinese/      ← Chinese translation
├── Enable-Chinese.bat         ← Switch to Chinese (symlink/copy)
├── Restore-Original.bat       ← Restore original Japanese
└── docs/                      ← This document
```

**Switch script logic**:
```
Enable-Chinese.bat:
  1. Back up current ja.lproj (if not already backed up)
  2. Delete ja.lproj
  3. Copy ja.lproj.chinese as ja.lproj
  4. Launch game: SmallWorld.exe language=ja

Restore-Original.bat:
  1. Delete ja.lproj
  2. Copy ja.lproj.original as ja.lproj
  3. Launch game normally
```

---

## 6. Workload Estimation

| Task | Workload | Difficulty | Notes |
|------|----------|------------|-------|
| Translate 486 XML strings | Medium | Low | MT then human proofread |
| Translate 178 compendium HTML | Large | Medium | Game terminology, requires board game knowledge |
| Create 360 localized images | Large | Medium-High | Needs art, or text-rendering alternative |
| Translate credits page | Small | Low | Single HTML file |
| Write switch scripts | Small | Low | Batch files sufficient |

---

## 7. Potential Risks & Considerations

### 7.1 Online Functionality Risk
- Using the `ja` language code may affect online matchmaking (system may match you with Japanese players)
- Online version check will not fail due to language pack modification (executable is untouched)
- **Recommendation**: Use original version for online play; use Chinese for single-player / local play

### 7.2 Font Limitations
- 5,932 Chinese characters cover the vast majority of common text
- Rare characters may display as boxes — test in advance
- If race/power names contain rare characters, consider homophone alternatives

### 7.3 Image Localization
- 360 images is a large workload. Options:
  - **Option 1**: Localize only key button/title images (~50 core UI images)
  - **Option 2**: Explore whether the `images.xml` mechanism can overlay text on images (requires runtime verification)
  - **Option 3**: Recreate all images (most complete but time-consuming)

### 7.4 Steam Integrity Verification
- Not modifying the executable, only replacing resource files — **will not trigger Steam file verification failure**
- However, Steam updates may overwrite modified files — reapply the patch after updates

---

## 8. Conclusion

### Overall Feasibility: ★★★★☆ (High)

**Favorable factors**:
1. ✅ All text resources are external (XML/strings), no hardcoded strings
2. ✅ Built-in font supports 5,932 Chinese characters — no font replacement needed
3. ✅ Rules book is in HTML format — easy to translate
4. ✅ Command-line language parameter supported — flexible switching
5. ✅ No executable modification needed — safe and reversible

**Unfavorable factors**:
1. ⚠️ Game does not natively support Chinese — must borrow the Japanese language pack
2. ⚠️ 360 localized images require significant effort
3. ⚠️ Language code is Japanese during online play — may affect matchmaking

**Recommendation**: Adopt **Approach A (replace Japanese pack)**. Prioritize text translation and core images; translate the rules book in stages. Provide a one-click enable/disable script for lossless switching.

---

## 9. Next Steps

1. **POC verification**: Translate a subset of strings in `ja.lproj/localizedStrings.xml` to test Chinese display
2. **Terminology glossary**: Establish official Chinese names for races/powers (refer to Small World board game translations)
3. **Image approach decision**: Evaluate image localization workload and alternatives
4. **Launcher development**: Write Chinese/original one-click switch scripts
