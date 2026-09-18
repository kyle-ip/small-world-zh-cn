# -*- coding: utf-8 -*-
"""
Generate Chinese-localized images for Small World 2 (Japanese slot).

Method: EN and ja-original image packs share identical artwork and differ
only in baked-in text. We diff each pair to get an exact text mask, erase
the text with OpenCV inpainting, and draw Chinese (SimHei) in its place.
Images that are identical between packs contain no baked text and are
copied untouched.
"""
import os
import sys
import shutil

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

# Chinese text for each image (image filename -> Chinese text)
IMAGE_TEXT = {
    # End screen
    "End-title.png": "向王者致敬！",
    "End-waiting-title.png": "获胜者是...",
    # Buttons
    "GOButton_Off.png": "出发",
    "GOButton_On.png": "出发",
    "button-play.png": "开始游戏",
    "button-play-off.png": "开始游戏",
    "button-create-on.png": "创建",
    "button-create-off.png": "创建",
    "button-join-on.png": "加入",
    "button-join-off.png": "加入",
    "button-pick-combo.png": "选择",
    "button-ok-combo.png": "确定",
    "button-restore.png": "恢复购买",
    "button-hide-map.png": "隐藏地图",
    "button-show-map.png": "显示地图",
    "SW2-acceptbutton.png": "接受",
    "SW2-acceptbutton-off.png": "接受",
    # Main menu
    "MainMenu-woodPanel-play.png": "开始游戏",
    "MainMenu-woodPanel-storyMode.png": "剧情与教学模式",
    "MainMenu-woodPanel-tutorial.png": "观看教程",
    # Play screen
    "PlayScreen-woodPanel-FtoF.png": "面对面",
    "PlayScreen-woodPanel-gameProgress.png": "进行中的游戏",
    "PlayScreen-woodPanel-localGame.png": "本地游戏",
    "PlayScreen-woodPanel-onlineBuddies.png": "邀请好友",
    "PlayScreen-woodPanel-onlineQuick.png": "快速在线游戏",
    "PlayScreen-woodPanel-passNplay.png": "传玩模式",
    "PlayScreen-woodPanel-solo.png": "单人游戏",
    # Rules
    "Rules-gameRules.png": "游戏规则",
    "Rules-power.png": "特殊能力",
    "Rules-races.png": "种族",
    "Rules-regions.png": "地区",
    "Rules-title.png": "规则",
    "Rules-userGuide.png": "用户指南",
    # Settings
    "Settings-music.png": "音乐",
    "Settings-sound.png": "音效",
    # Shop
    "Shop-title.jpg": "商店",
    # Stats
    "Stat-button-name.png": "游戏统计",
    # Leaderboard
    "LeaderB-player.png": "玩家",
    "LeaderB-title.jpg": "排行榜",
    "LeaderB-titleOnline.png": "在线",
    "LeaderB-titleOtherMode.png": "面对面、本地、传玩",
    "LeaderB-titleSolo.png": "单人",
    "LeaderB-titleSoloWorldWide.png": "全球单人",
    # Online arena
    "online_arena-create-title-on.png": "创建",
    "online_arena-create-title-off.png": "创建",
    "online_arena-join-title-on.png": "加入",
    "online_arena-join-title-off.png": "加入",
    # Resume
    "resume-yourturn-on.png": "轮到你了！",
    "resume-yourturn-pending.png": "邀请待处理",
    # Combo
    "comboAvailable-title.png": "可用组合",
    # Titles
    "titles-advancedSettings.png": "高级设置",
    "titles-buddiesList.png": "好友列表",
    "titles-gameCreation.png": "创建游戏",
    "titles-gamesList.png": "游戏列表",
    "titles-inviteBuddies.png": "邀请好友",
    "titles-openGames.png": "开放游戏",
    # SD titles
    "SD-title-expansions.png": "扩展",
    "SD-title-players.png": "玩家",
    # Expansion text banners
    "ExpansionTopText_Cursed.png": "诅咒！",
    "ExpansionBottomText_Cursed.png": "诅咒！",
    "ExpansionTopText_GrandDames.png": "贵妇团",
    "ExpansionBottomText_GrandDames.png": "贵妇团",
    "ExpansionTopText_BeNotAfraid.png": "不要害怕",
    "ExpansionBottomText_BeNotAfraid.png": "不要害怕",
    "ExpansionTopText_RoyalBonus.png": "皇家奖励",
    "ExpansionBottomText_RoyalBonus.png": "皇家奖励",
    "ExpansionTopText_SpiderWeb.png": "蛛网",
    "ExpansionBottomText_SpiderWeb.png": "蛛网",
}


def main():
    for _, text in IMAGE_TEXT.items():
        cnfont.assert_covered(text, label="IMAGE_TEXT")

    os.makedirs(JA_COMMON, exist_ok=True)
    os.makedirs(JA_COMMON_HD, exist_ok=True)

    # Start from pristine English artwork for every image
    copied = 0
    for src_dir, dst_dir in [(EN_COMMON, JA_COMMON), (EN_COMMON_HD, JA_COMMON_HD)]:
        for fname in os.listdir(src_dir):
            shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, fname))
            copied += 1
    print(f"Copied {copied} base images from en to ja")

    replaced, notext, missing = 0, 0, []
    for fname, text in IMAGE_TEXT.items():
        is_jpg = fname.lower().endswith((".jpg", ".jpeg"))
        for en_dir, ja_ref_dir, dst_dir in [
            (EN_COMMON, JA_ORIG, JA_COMMON),
            (EN_COMMON_HD, JA_ORIG_HD, JA_COMMON_HD),
        ]:
            en_path = os.path.join(en_dir, fname)
            if not os.path.exists(en_path):
                continue
            ref_path = os.path.join(ja_ref_dir, fname)
            dst_path = os.path.join(dst_dir, fname)
            if not os.path.exists(ref_path):
                missing.append(fname)
                continue
            img = inpaint_localize(en_path, ref_path, text, jpg=is_jpg)
            if img is None:
                notext += 1
                continue
            if is_jpg:
                img.convert("RGB").save(dst_path, "JPEG", quality=95)
            else:
                img.save(dst_path)
            replaced += 1

    print(f"Replaced text in {replaced} images; {notext} had no baked text (copied as-is)")
    if missing:
        print(f"WARNING no JA reference for: {sorted(set(missing))}")


if __name__ == "__main__":
    main()
