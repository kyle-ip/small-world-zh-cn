# -*- coding: utf-8 -*-
"""Localize race/power banner images via EN/JA diff + inpainting.

EN and ja-original banners share the same artwork; only the name text
differs, so inpaint_localize() erases the original name and draws Chinese
in its place. Compendium banners are byte-identical to common banners, so
the same EN/JA pair is reused there.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cnfont
from inpaint_text import inpaint_localize

BASE = r"c:\Program Files (x86)\Steam\steamapps\common\SmallWorld2\Resources"
EN_COMMON = os.path.join(BASE, "en.lproj", "common")
EN_COMMON_HD = os.path.join(BASE, "en.lproj", "common-hd")
JA_ORIG = os.path.join(BASE, "ja.lproj.original", "common")
JA_ORIG_HD = os.path.join(BASE, "ja.lproj.original", "common-hd")
JA_COMMON = os.path.join(BASE, "ja.lproj", "common")
JA_COMMON_HD = os.path.join(BASE, "ja.lproj", "common-hd")
COMPENDIUM_MDPI_JA = os.path.join(BASE, "compendium", "image", "mdpi", "ja")

RACE_NAMES = {
    "swdm_AmazonRace.png": "亚马逊",
    "swdm_DwarfRace.png": "矮人",
    "swdm_ElfRace.png": "精灵",
    "swdm_GhoulRace.png": "食尸鬼",
    "swdm_GiantRace.png": "巨人",
    "swdm_HalflingRace.png": "半身人",
    "swdm_HumanRace.png": "人类",
    "swdm_OrcRace.png": "兽人",
    "swdm_RatmenRace.png": "鼠人",
    "swdm_SkeletonRace.png": "骷髅",
    "swdm_SorcererRace.png": "巫师",
    "swdm_TritonRace.png": "人鱼",
    "swdm_TrollRace.png": "巨魔",
    "swdm_WizardRace.png": "法师",
    "swdm_WhiteLadyRace.png": "白衣女士",
    "swdm_ShrubmenRace.png": "灌木人",
    "swdm_PixyRace.png": "小精灵",
    "swdm_SkagsRace.png": "斯卡斯",
    "swdm_KoboldRace.png": "狗头人",
    "swdm_GypsyRace.png": "游牧民",
    "swdm_LeprechaunRace.png": "小矮妖",
    "swdm_GoblinRace.png": "哥布林",
    "swdm_IceWitchesRace.png": "冰雪女巫",
    "swdm_PygmyRace.png": "巫医",
    "swdm_SlingmenRace.png": "投石兵",
    "swdm_IgorRace.png": "伊戈尔",
    "swdm_FaunRace.png": "农牧神",
    "swdm_PriestessRace.png": "女祭司",
    "swdm_BarbarianRace.png": "野蛮人",
    "swdm_HomunculiRace.png": "人造人",
}

POWER_NAMES = {
    "swdm_AlchemistPower.png": "炼金术士",
    "swdm_BerserkPower.png": "狂暴",
    "swdm_BivouackingPower.png": "露营",
    "swdm_CommandoPower.png": "突击队",
    "swdm_DiplomatPower.png": "外交官",
    "swdm_DragonMasterPower.png": "驯龙师",
    "swdm_FlyingPower.png": "飞行",
    "swdm_ForestPower.png": "森林",
    "swdm_FortifiedPower.png": "筑城",
    "swdm_HeroicPower.png": "英雄",
    "swdm_HillPower.png": "山丘",
    "swdm_MerchantPower.png": "商人",
    "swdm_MountedPower.png": "骑兵",
    "swdm_PillagingPower.png": "掠夺",
    "swdm_SeafaringPower.png": "航海",
    "swdm_SpiritPower.png": "灵魂",
    "swdm_StoutPower.png": "坚韧",
    "swdm_SwampPower.png": "沼泽",
    "swdm_UnderworldPower.png": "地下世界",
    "swdm_WealthyPower.png": "富豪",
    "swdm_AquaticPower.png": "水生",
    "swdm_BarricadePower.png": "街垒",
    "swdm_BehemothPower.png": "巨兽",
    "swdm_CatapultPower.png": "投石机",
    "swdm_CorruptPower.png": "腐化",
    "swdm_CursedPower.png": "诅咒",
    "swdm_CopycatPower.png": "模仿者",
    "swdm_FireballPower.png": "火球",
    "swdm_HistorianPower.png": "历史学家",
    "swdm_HordesOfPower.png": "成群",
    "swdm_ImperialPower.png": "帝国",
    "swdm_LavaPower.png": "熔岩",
    "swdm_MaraudingPower.png": "劫掠",
    "swdm_MercenaryPower.png": "雇佣兵",
    "swdm_PeaceLovingPower.png": "和平主义",
    "swdm_RansackingPower.png": "洗劫",
    "swdm_SoulTouchPower.png": "灵魂触摸",
    "swdm_WerePower.png": "狼人",
}

ALL_NAMES = {}
ALL_NAMES.update(RACE_NAMES)
ALL_NAMES.update(POWER_NAMES)

# Small handwritten rule text baked into the bottom of a few banners.
SUBTEXT = {
    "swdm_AmazonRace.png": "仅攻击时",
    "swdm_AlchemistPower.png": "每回合",
    "swdm_WealthyPower.png": "仅一次",
}


def main():
    for _, chinese in ALL_NAMES.items():
        cnfont.assert_covered(chinese, label="banner")
    for _, chinese in SUBTEXT.items():
        cnfont.assert_covered(chinese, label="banner-sub")

    count = 0
    for fname, chinese in ALL_NAMES.items():
        sub = SUBTEXT.get(fname)

        # SD (common): EN artwork vs JA original text
        en = os.path.join(EN_COMMON, fname)
        ref = os.path.join(JA_ORIG, fname)
        dst = os.path.join(JA_COMMON, fname)
        if os.path.exists(en) and os.path.exists(ref):
            img = inpaint_localize(en, ref, chinese, subtext=sub, plaque=True)
            if img is not None:
                img.save(dst)
                count += 1
        else:
            print(f"  WARN: missing pair for {fname}")

        # HD
        en_hd = os.path.join(EN_COMMON_HD, fname)
        ref_hd = os.path.join(JA_ORIG_HD, fname)
        dst_hd = os.path.join(JA_COMMON_HD, fname)
        if os.path.exists(en_hd) and os.path.exists(ref_hd):
            img = inpaint_localize(en_hd, ref_hd, chinese, subtext=sub, plaque=True)
            if img is not None:
                img.save(dst_hd)

        # Compendium banner shares identical EN artwork with common
        dst_comp = os.path.join(COMPENDIUM_MDPI_JA, fname)
        if os.path.exists(dst_comp) and os.path.exists(en) and os.path.exists(ref):
            img = inpaint_localize(en, ref, chinese, subtext=sub, plaque=True)
            if img is not None:
                img.save(dst_comp)

    # In-decline tokens: same artwork desaturated, mirrored plaque on the
    # right half. Power decline tokens have no plaque text and are skipped.
    DECLINE_SKIP = {"swdm_FortifiedPowerInDecline.png",
                    "swdm_SeafaringPowerInDecline.png",
                    "swdm_SpiritPowerInDecline.png",
                    "NeutralPowerInDecline.png"}
    for fname in sorted(os.listdir(EN_COMMON)):
        if "InDecline" not in fname or not fname.endswith(".png"):
            continue
        if fname in DECLINE_SKIP:
            # Tokens without a name plaque: keep the pristine EN artwork
            # everywhere (overwrite any earlier bad localization).
            for en_d, dst_d in ((EN_COMMON, JA_COMMON), (EN_COMMON_HD, JA_COMMON_HD),
                                (EN_COMMON, COMPENDIUM_MDPI_JA)):
                src = os.path.join(en_d, fname)
                if os.path.exists(src) and os.path.isdir(dst_d):
                    shutil.copyfile(src, os.path.join(dst_d, fname))
            continue
        chinese = ALL_NAMES.get(fname.replace("InDecline.png", ".png"))
        if not chinese:
            continue
        for en_d, ref_d, dst_d in ((EN_COMMON, JA_ORIG, JA_COMMON),
                                   (EN_COMMON_HD, JA_ORIG_HD, JA_COMMON_HD)):
            en = os.path.join(en_d, fname)
            ref = os.path.join(ref_d, fname)
            if os.path.exists(en):
                img = inpaint_localize(en, ref if os.path.exists(ref) else None,
                                       chinese, plaque="decline")
                if img is not None:
                    img.save(os.path.join(dst_d, fname))
                    count += 1
        dst_comp = os.path.join(COMPENDIUM_MDPI_JA, fname)
        en = os.path.join(EN_COMMON, fname)
        ref = os.path.join(JA_ORIG, fname)
        if os.path.exists(dst_comp) and os.path.exists(en):
            img = inpaint_localize(en, ref if os.path.exists(ref) else None,
                                   chinese, plaque="decline")
            if img is not None:
                img.save(dst_comp)

    # JP-only banner (no EN counterpart): localize straight from the
    # Japanese original using the engraved-letter detector alone.
    for fname, chinese in {"swdm_LavaPower_JP.png": "熔岩"}.items():
        for orig_d, dst_d in ((JA_ORIG, JA_COMMON), (JA_ORIG_HD, JA_COMMON_HD)):
            src = os.path.join(orig_d, fname)
            if os.path.exists(src):
                img = inpaint_localize(src, None, chinese, plaque=True)
                if img is not None:
                    img.save(os.path.join(dst_d, fname))
                    count += 1

    print(f"Localized {count} banner images")


if __name__ == "__main__":
    main()
