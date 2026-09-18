# -*- coding: utf-8 -*-
"""
Small World 2 Chinese Localization Script
Translates en.lproj XML/strings into payload/Resources/zh.lproj
"""
import os
import shutil
import re

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_GAME_RES = os.path.abspath(os.path.join(_REPO, "..", "Resources"))
BASE = _GAME_RES  # read English sources from installed game
EN = os.path.join(BASE, "en.lproj")
ZH = os.path.join(_REPO, "payload", "Resources", "zh.lproj")
JA = ZH  # legacy alias used below

# ============================================================
# localizedStrings.xml translations
# ============================================================
LS_TRANSLATIONS = {
    "RulesLanguage": "zh",
    "LeaveGameMessageBox_Title": "离开游戏",
    "MessageBox_Yes": "是",
    "MessageBox_No": "否",
    "MessageBox_OK": "确定",
    "MessageBox_Cancel": "取消",
    "ComboDisplayIsPowerThenRace": "1",
    "PickComboController_Title": "选择种族与特殊能力组合",
    "ConquerSomeRegions_Message_Format": "%s，去征服一些地区吧！",
    "RedeployYourTroops_Message_Format": "%s，重新部署你的部队！",
    "RedeployYourDefeatedTroops_Message_Format": "%s，重新部署你被击败的部队！",
    "NextActionLabel_Conquer": "征服",
    "NextActionLabel_Redeploy": "重新部署",
    "NextActionLabel_ActivateNextCombo": "下一个",
    "NextActionLabel_FinishRedeployment": "完成",
    "NextActionLabel_FinishTurn": "完成",
    "NextActionLabel_MaraudingPhase": "第二阶段",
    "NextActiveCombo_Title": "准备就绪！",
    "NextActiveCombo_MessageFormat": "准备使用 %s。",
    "DeclineMessageBox_Title": "衰落",
    "DeclineMessageBox_Message": "你确定要让当前活跃种族进入衰落吗？",
    "PassAndPlay_PrepareToPlayTitle": "轮到你了！",
    "PassAndPlay_PrepareToPlayFormat": "%s，准备开始游戏！",
    "PassAndPlay_PlayButton": "开始",
    "AmazonRaceUIController_MessageFormat": "你需要将 %d 个亚马逊代币移回手牌。",
    "PriestessRaceUIController_Message": "请将象牙塔放置在你控制的一个地区。",
    "MaraudingMessageBox_Title": "第二次征服阶段",
    "MaraudingMessageBox_Message": "你想要攻击的地区需要掷强化骰；这将取消你的第二次征服阶段。\n\n你确定要攻击该地区吗？",
    "MercenaryMessageBox_Title": "雇佣兵",
    "MercenaryMessageBox_Message": "你想花费 1 枚胜利金币获得 +2 攻击加成吗？",
    "FireballMessageBox_Title": "火球攻击！",
    "FireballMessageBox_Message": "你想使用多少个火球来获得攻击加成？\n        1 个火球 = +2",
    "FireballMessageBox_AttackButton": "攻击",
    "RacePowerCombo_NameFormat": "%1$s %2$s",
    # Races
    "swdm::AmazonRace_Name": "亚马逊",
    "swdm::DwarfRace_Name": "矮人",
    "swdm::ElfRace_Name": "精灵",
    "swdm::GhoulRace_Name": "食尸鬼",
    "swdm::GiantRace_Name": "巨人",
    "swdm::HalflingRace_Name": "半身人",
    "swdm::HumanRace_Name": "人类",
    "swdm::OrcRace_Name": "兽人",
    "swdm::RatmenRace_Name": "鼠人",
    "swdm::SkeletonRace_Name": "骷髅",
    "swdm::SorcererRace_Name": "巫师",
    "swdm::TritonRace_Name": "人鱼",
    "swdm::TrollRace_Name": "巨魔",
    "swdm::WizardRace_Name": "法师",
    "swdm::GoblinRace_Name": "哥布林",
    "swdm::KoboldRace_Name": "狗头人",
    "swdm::GypsyRace_Name": "游牧民",
    "swdm::PriestessRace_Name": "女祭司",
    "swdm::WhiteLadyRace_Name": "白衣女士",
    "swdm::BarbarianRace_Name": "野蛮人",
    "swdm::HomunculiRace_Name": "人造人",
    "swdm::LeprechaunRace_Name": "小矮妖",
    "swdm::PixyRace_Name": "小精灵",
    "swdm::PygmyRace_Name": "巫医",
    "swdm::IgorRace_Name": "伊戈尔",
    "swdm::ShrubmenRace_Name": "灌木人",
    "swdm::FaunRace_Name": "羊人",
    "swdm::SlingmenRace_Name": "投石兵",
    "swdm::IceWitchesRace_Name": "冰雪女巫",
    "swdm::SkagsRace_Name": "斯卡斯",
    # Powers
    "swdm::AlchemistPower_Name": "炼金术士",
    "swdm::BerserkPower_Name": "狂暴",
    "swdm::BivouackingPower_Name": "露营",
    "swdm::CommandoPower_Name": "突击队",
    "swdm::DiplomatPower_Name": "外交官",
    "swdm::DragonMasterPower_Name": "驯龙师",
    "swdm::FlyingPower_Name": "飞行",
    "swdm::ForestPower_Name": "森林",
    "swdm::FortifiedPower_Name": "筑城",
    "swdm::HeroicPower_Name": "英雄",
    "swdm::HillPower_Name": "山丘",
    "swdm::MerchantPower_Name": "商人",
    "swdm::MountedPower_Name": "骑兵",
    "swdm::PillagingPower_Name": "掠夺",
    "swdm::SeafaringPower_Name": "航海",
    "swdm::SpiritPower_Name": "灵魂",
    "swdm::StoutPower_Name": "坚韧",
    "swdm::SwampPower_Name": "沼泽",
    "swdm::UnderworldPower_Name": "地下世界",
    "swdm::WealthyPower_Name": "富豪",
    "swdm::CursedPower_Name": "诅咒",
    "swdm::HordesOfPower_Name": "成群",
    "swdm::MaraudingPower_Name": "劫掠",
    "swdm::RansackingPower_Name": "洗劫",
    "swdm::WerePower_Name": "变身",
    "swdm::HistorianPower_Name": "历史学家",
    "swdm::PeaceLovingPower_Name": "和平主义",
    "swdm::BarricadePower_Name": "路障",
    "swdm::CatapultPower_Name": "投石机",
    "swdm::CorruptPower_Name": "腐化",
    "swdm::ImperialPower_Name": "帝国",
    "swdm::MercenaryPower_Name": "雇佣兵",
    "swdm::FireballPower_Name": "火球",
    "swdm::AquaticPower_Name": "水生",
    "swdm::BehemothPower_Name": "巨兽",
    "swdm::LavaPower_Name": "熔岩",
    "swdm::SoulTouchPower_Name": "灵魂触摸",
    "swdm::CopycatPower_Name": "模仿者",
    # Expansions
    "ExpansionTitle_Cursed": "诅咒！",
    "ExpansionTitle_GrandDames": "贵妇团",
    "ExpansionTitle_BeNotAfraid": "不要害怕...",
    "ExpansionTitle_RoyalBonus": "皇家奖励",
    "ExpansionTitle_SpiderWeb": "蛛网",
    # Quick Online
    "QuickOnlineGSC_NbPlayers": "玩家数量",
    "QuickOnlineGSC_EstimatedTimeToWaitLabel": "预计等待时间：",
    # Resume
    "ResumeGame_Title": "继续游戏",
    "ResumeGame_Message": "你上次的游戏没有完成。\n是否继续？",
    "ResumeGame_ResumeButton": "继续",
    # Local Play
    "LocalPlayWaitingPanel_Message": "请等待其他玩家加入游戏",
    "JoinableGameCell_LabelFormat": "%s 的游戏",
    "LocalGameError_Title": "网络错误",
    "LocalGameError_MessageFormat": "发生错误(%d, %s)",
    # In game errors
    "GameError_Title": "错误",
    "GameError_MessageFormat": "刚刚发生错误：%s",
    "GameError_QuitButton": "退出",
    "GameAborted_Title": "游戏中止",
    "GameAborted_MessageFormat": "%s 中止了这场游戏。",
    # No internet
    "NoInternetConnection_Title": "无网络连接",
    "NoInternetConnection_Message": "需要网络连接。",
    # Settings
    "SettingsScreen_LoginButton": "登录",
    "SettingsScreen_LogoutButtonFormat": "登出\n%s",
    "SettingsScreen_AutoRedeploySwitchLabel": "在线好友对战时\n自动重新部署",
    # Resume online
    "Withdraw_Label": "退出",
    "OnlinePlay_NoOpenGamesMessage": "没有可继续的开放游戏。",
    "WithdrawGame_Title": "退出游戏",
    "WithdrawGame_Message": "你确定要放弃这场游戏吗？",
    "TimeLeftBeforeTimeoutFormat": "剩余 %s",
    # Async
    "AsyncGame_YourTurn_Title": "轮到你了",
    "AsyncGame_YourTurn_Message": "现在轮到你了！\n你想现在进行这场在线游戏吗？",
    "AsyncGame_YourTurnInOtherGame_Message": "另一场在线游戏轮到你了。\n你想现在切换到那场游戏吗？",
    "AsyncGame_YourTurn_PlayButton": "开始",
    "AsyncGame_YourTurnInvite_Title": "邀请",
    "AsyncGame_YourTurnInvite_Message": "你被邀请参加这场在线游戏。\n你想现在开始吗？",
    "AsyncGame_YourTurnInviteInOtherGame_Message": "你被邀请参加另一场在线游戏。\n你想现在切换到那场游戏吗？",
    "AsyncGame_GameOver_Title": "游戏结束",
    "AsyncGame_GameOver_Message": "你的一场在线游戏结束了。",
    # Play online with buddies
    "OnlinePlay_NoBuddiesMessage": "你没有好友。",
    "OnlinePlay_ManageMyBuddiesButton": "管理好友",
    "OnlinePlay_PlayOnlineButton": "在线游戏",
    "OnlinePlay_InviteButton": "邀请",
    "OnlinePlay_UninviteButton": "取消邀请",
    "OnlinePlay_RemoveBuddyButton": "移除",
    "LoginNotFound_Title": "未找到玩家",
    "LoginNotFound_MessageFormat": "在玩家列表中找不到用户 %s。",
    "OnlinePlay_BuddyAlreadyAdded_Title": "好友已添加",
    "OnlinePlay_BuddyAlreadyAdded_MessageFormat": "%s 已在你的好友列表中。",
    "OnlinePlay_AddBuddyButton": "添加",
    "OnlinePlay_FindDowPlayerExplanation": "输入玩家登录名查找玩家。",
    "OnlinePlay_BuddyAdded_Title": "好友已添加。",
    "OnlinePlay_BuddyAdded_MessageFormat": "玩家 %s 已成功添加。",
    "OnlinePlay_NoRecentOpponentsMessage": "你没有近期对手。",
    "OnlinePlay_GameCenterCancelled": "此游戏的 Game Center 已停用。\n如需激活，请在 Game Center 应用中登录。",
    "OnlinePlay_GameCenterError": "Game Center 发生错误。\n请稍后重试。",
    "OnlinePlay_NoGCFriendsMessage": "你的 Game Center 好友列表为空。",
    # Duration
    "NbHours_Format": "%d 小时",
    "NbMinutes_Format": "%d 分钟",
    "NbSeconds_Format": "%d 秒",
    # High score
    "SubmitHighscoreMessageBox_Title": "新纪录！",
    "SubmitHighscoreMessageBox_MessageFormat": "你刚刚以 %d 分创下新纪录。\n是否将其记录到排行榜？",
    "SubmitHighscoreMessageBox_PlayerNameLabel": "你的名字：",
    "LeaderboardScreen_EmptyLeaderboard": "该排行榜为空。",
    "ScoreSubmittedOnline_Title": "分数已在线提交",
    "ScoreSubmittedOnline_MessageFormat": "%s，你以 %d 分提升了排名（第 %d 名）",
    "ScoreSubmittedOnline_SeeButton": "查看排名",
    # View product
    "ViewProduct_Title": "离开小小世界查看商品",
    "ViewProduct_MessageFormat": "你将被重定向到浏览器查看 %s 的信息。\n是否离开应用？",
    "OnlinePlay_GCFriendNotBoundToDow_Title": "好友未关联 DoW 账号",
    "OnlinePlay_GCFriendNotBoundToDow_MessageFormat": "%s 未关联 Days of Wonder 账号。",
    "LeaveGameMessageBox_Message": "你想暂时离开这场游戏吗？\n别担心，游戏会被保存。",
    "LeaderboardPeriod_Day": "日",
    "LeaderboardPeriod_Week": "周",
    "LeaderboardPeriod_Ever": "总",
    "NotApplicable": "不适用",
    "RecentOpponents_Label": "近期对手",
    "FindDOWPlayers_Label": "查找",
    "GameCenter_Label": "Game Center",
    "DefaultPlayerNameFormat": "玩家 %d",
    "BotName_Blue": "铁皮机器人",
    "BotName_Red": "B4P-b0t",
    "BotName_Yellow": "阿克塔机器人",
    "BotName_Green": "灌木机器人",
    "BotName_Purple": "椰子机器人",
    "LeaderboardPeriod_Provisional": "临时",
    "LeaderboardPeriod_Established": "正式",
    "ShopScreen_Speech": "嘿，看看这些来自 Days of Wonder 的精美桌游！",
    "SkipButton_Label": "跳过",
    "PickComboControllerCheck_Title": "查看可用的种族与特殊能力组合",
    "PickComboControllerOtherOpponent_TitleFormat": "%s 正在选择新组合",
    # SSO
    "SettingsScreen_LoginSettingsButton": "登录设置",
    "MessageBox_InviteButton": "邀请",
    "MessageBox_InviteTitle": "小小世界",
    "MessageBox_InviteMessage": "我邀请你玩小小世界！要和我一起玩，你需要购买应用并在线登录。",
    # Buddy management
    "OnlinePlay_CannotAddMyselfAsBuddy_Title": "操作被拒绝",
    "OnlinePlay_CannotAddMyselfAsBuddy_Message": "你不能将自己添加为好友！",
    "OnlinePlay_AdvancedSettingsButton": "高级设置",
    "OnlinePlay_BuddiesListButton": "好友列表",
    "OnlinePlay_AutoRedeploySwitchLabel": "自动重新部署",
    "OnlinePlay_RankedSwitchLabel": "排名游戏",
    "OnlinePlay_GameTurnTimeoutLabel": "每位玩家最长用时",
    "OnlinePlay_CannotResumeTitle": "无法继续游戏",
    "OnlinePlay_CannotResumeMessage": "抱歉，这场在线游戏已不可用",
    "OnlinePlay_CannotResumeMessageWithErrorFormat": "你无法继续此游戏，原因：\n%s",
    # Tutorial video
    "TutorialVideoID": "NoFJdtZ4BIg",
    # Berserk
    "BerserkDeclineOrRoll_Message": "作为狂暴种族，你现在可以掷骰进行征服或进入衰落。\n你想怎么做？",
    # Version check
    "OnlinePlay_CheckVersion_Title": "需要更新应用",
    "OnlinePlay_CheckVersion_MessageFormat": "你的应用需要更新才能在线游戏（你的版本：%s，需要版本或更高：%s）",
    # Local play
    "LocalPlay_NoOpenGamesMessage": "你的局域网中没有开放游戏。\n\n请创建一个或等待朋友创建新游戏后加入。\n\n同时请确保你已连接到 WiFi 网络。",
    # Chat
    "SendChatButton": "发送",
    "Buy": "购买",
    # Add buddy
    "AddBuddy_Title": "添加好友",
    "AddBuddy_MessageFormat": "你想将 %s 添加为好友吗？",
    # Online arena
    "OnlineArena_PrivateGameSwitchLabel": "私人游戏",
    "OnlineArena_SingleSessionButtonLabel": "单场游戏",
    "OnlineArena_TurnBasedButtonLabel": "多场游戏",
    "OnlineArena_UndefinedCustomTimeout": "?\n自定义",
    "LeaveGame_Label": "离开游戏",
    "PendingPlayer_Label": "等待中",
    "OpenGame_Label": "开放游戏",
    "NoOpenGames_Message": "没有开放游戏。\n你可以前往创建面板创建一个新游戏。",
    "DefaultGameNameFormat": "%s 的游戏",
    "DefinePassword_Title": "设置游戏密码",
    "DefinePassword_Message": "请为你的游戏输入密码。",
    "EnterGamePassword_Title": "私人游戏",
    "EnterGamePassword_Message": "请输入此游戏的密码。",
    "CustomTimeout_Title": "自定义时间设置",
    # Short duration
    "NbDays_Format": "%d 天",
    "NbDays_ShortFormat": "%d 天",
    "NbHours_ShortFormat": "%d 时",
    "NbMinutes_ShortFormat": "%d 分",
    "NbSeconds_ShortFormat": "%d 秒",
    # Chat profanity
    "ChatProfanity_OtherPlayer_Format": "%s 因使用脏话被静音几分钟。",
    "ChatProfanity_You": "你触发了脏话过滤器——你将被静音几分钟。",
    # Lobby
    "LeaveSingleSessionGameMessageBox_Title": "放弃单场游戏",
    "LeaveSingleSessionGameMessageBox_Message": "你想放弃这场单场游戏吗？你将被机器人取代。",
    # Resume online
    "DeclineInvitation_Button": "拒绝邀请",
    "InvitationPending_Label": "邀请待处理",
    "Resume_SingleSessionGame_Title": "进行中的单场游戏",
    "Resume_SingleSessionGame_Message": "你离开的一场单场游戏仍在进行中。是否继续？",
    # Invitation
    "InvitationDialog_Title": "在线游戏邀请",
    "InvitationDialog_Message": "%s 向你发起一场 %d 人在线游戏挑战。",
    "InvitationDialog_Decline_Button": "拒绝邀请",
    "InvitationDialog_See_Button": "查看邀请",
    "InvitationDialog_Accept_Button": "接受邀请",
    # Play screen
    "PlayScreen_InviteBuddies_Button": "邀请好友",
    # Stats
    "PlayerStats_VictimLabel": "是你最喜欢的对手",
    "ComboStats_MinLabel": "最低",
    "ComboStats_MaxLabel": "最高",
    # Invite buddies
    "OnlinePlay_FirstPlayerLabel": "先手玩家",
    # Player hotswap
    "PlayerHotswap_BecameRobot_Title": "玩家离开游戏",
    "PlayerHotswap_BecameRobot_MessageFormat": "%s 刚刚离开游戏。\n他现在被机器人取代",
    "PlayerHotswap_BecameRobotBecauseTimeout_MessageFormat": "%s 超时，已被机器人取代。",
    "PlayerHotswap_CameBack_Title": "玩家回归",
    "PlayerHotswap_CameBack_MessageFormat": "%s 刚刚回到游戏",
    # Timeout
    "GameTimeOut_Title": "超时",
    "GameTimeOut_MessageForLocalPlayerTimeout": "你超时了。\n你将被机器人取代且无法恢复。",
    "GameTimeOut_MessageForLocalPlayerTimeout_GameAborted": "你超时了。\n游戏已中止。",
    "OnlineArena_CustomTimeoutFormat": "自定义：\n%s",
    "NextActionLabel_MayRollDie": "掷骰",
    # Resume online
    "CancelInvitation_Button": "取消邀请",
    "InvitationFromNotification_Message": "你被挑战参加一场在线游戏。",
    "LoginButton": "登录",
    # Online error
    "OnlineServerDidNotRespond_Title": "在线错误",
    "OnlineServerDidNotRespond_Message": "在线服务器无响应。请检查你的网络连接。",
    "Error_Code": "错误代码：",
    # Server
    "WaitForServerResponse_Title": "服务器连接",
    "WaitForServerResponse_Message": "正在向在线服务器发送数据…",
    "CantInviteBuddyWithoutApp_MessageFormat": "%s 似乎还没有小小世界，因此无法被邀请游玩。",
    "CantInviteBuddyWithoutApp_Title": "无法邀请玩家",
    # Localization kit
    "DisconnectedControllerTitleId": "这里信号不好",
    "DisconnectedControllerConnectId": "连接一个控制器以继续",
    # Rate app
    "RateApp_Title": "为应用评分！",
    "RateApp_Message": "如果你喜欢这个应用，介意花点时间为它评分吗？\n不会超过一分钟。\n\n感谢你的支持！",
    "RateApp_Ok": "立即评分",
    "RateApp_No": "不用了，谢谢",
    "RateApp_Later": "稍后",
    "MessageBox_TryAgain": "重试",
    "NextActionLabel_BeforeEndConquerPhase": "特殊征服",
}

# ============================================================
# tooltips.xml translations
# ============================================================
TT_TRANSLATIONS = {
    "Tooltip_CreditsButton": "鸣谢",
    "Tooltip_RulesButton": "规则",
    "Tooltip_ShopButton": "商店",
    "Tooltip_LeaderboardsButton": "排行榜",
    "Tooltip_SettingsButton": "设置",
    "Tooltip_GameRulesTab": "游戏规则",
    "Tooltip_RegionsTab": "地区",
    "Tooltip_RacesTab": "种族",
    "Tooltip_PowersTab": "特殊能力",
    "Tooltip_UserGuideTab": "用户指南",
    "Tooltip_SoloLocalButton": "本地排名",
    "Tooltip_SoloWorldwideButton": "全球排名",
    "Tooltip_KarmaScoreIcons": "因果值与排名分数",
    "Tooltip_OnlineProvisionalButton": "临时排名",
    "Tooltip_OnlineEstablishedButton": "正式排名",
    "Tooltip_ChangeAvatarColor": "切换颜色",
    "Tooltip_SoloButton": "单人对战 AI",
    "Tooltip_FaceToFaceButton": "与朋友对战",
    "Tooltip_PassnPlayButton": "在同一台电脑上与朋友一起玩",
    "Tooltip_GamesInProgressButton": "你未完成的游戏",
    "Tooltip_OnlineQuickPlayButton": "开始快速多人游戏",
    "Tooltip_OnlineWithBuddiesButton": "开始多人游戏并邀请朋友一起玩",
    "Tooltip_LocalGameButton": "进行局域网游戏",
    "Tooltip_SelectFirstPlayerButton": "先手玩家",
    "Tooltip_RandomFirstPlayerButton": "随机先手玩家",
    "Tooltip_RestorePurchasesButton": "点击此处恢复已购买内容",
    "Tooltip_RabbitSwitch": "高级设置",
    "Tooltip_SWFilter": "仅显示拥有小小世界的朋友",
    "Tooltip_InviteBuddiesAddButton": "将此玩家添加到好友列表",
    "Tooltip_InviteBuddiesRemoveButton": "从好友列表中移除此玩家",
    "Tooltip_AutomaticRedeploySwitch": "如果你想在损失后手动重新部署代币，请关闭此选项。",
    "Tooltip_RankedGameSwitch": "如果你想进行非排名游戏，请关闭此选项。",
    "Tooltip_GameTurnTimeOutSegment": "设置每个回合的最大时长。超过此限制的玩家将被踢出游戏。",
    "Tooltip_ComboPickerGoToCompendiumButton": "前往规则书",
    "Tooltip_BackMenuQuitButton": "离开当前游戏",
    "Tooltip_BackMenuRulesButton": "游戏规则",
    "Tooltip_BackMenuSettingsButton": "设置",
    "Tooltip_DeclineButton": "让当前活跃种族进入衰落",
    "Tooltip_OpponentBannerButton": "显示该玩家的组合",
    "Tooltip_ActiveCombos": "活跃组合",
    "Tooltip_InDeclineCombos": "衰落组合",
    "Tooltip_StackOfTokensInYourHand": "你可用的代币",
    "Tooltip_PlayerAvatarButton": "高亮该玩家的征服区域",
    "Tooltip_MyScoreCoinButton": "你当前的分数",
    "Tooltip_NextAction_Redeploy": "重新部署代币",
    "Tooltip_NextAction_ActivateNextCombo": "使用你的活跃种族",
    "Tooltip_NextAction_FinishRedeployment": "完成当前操作",
    "Tooltip_NextAction_FinishTurn": "完成当前操作",
    "Tooltip_NextAction_MaraudingPhase": "进行第二次征服阶段",
    "Tooltip_OnlineArena_Karma": "因果等级",
    "Tooltip_OnlineArena_RankingScore": "排名分数",
    "Tooltip_OnlineArena_NbGames": "已进行的排名游戏数量",
    "Tooltip_OnlineArena_Language": "玩家语言",
    "Tooltip_OnlineArena_AvailablePlayers": "可用玩家列表",
    "Tooltip_OnlineArena_Search": "搜索",
    "Tooltip_OnlineArena_ChatHistory": "聊天记录",
    "Tooltip_OnlineArena_ChatBox": "聊天框 - 在此输入消息",
    "Tooltip_OnlineArena_SingleSessionButton": "单场游戏必须连续进行。断开连接的玩家将被机器人取代。",
    "Tooltip_OnlineArena_MultiSessionButton": "多场游戏可以暂停，并且可以同时进行多场。",
    "Tooltip_OnlineArena_PresetPlayerClock": "预设玩家时钟",
    "Tooltip_OnlineArena_CustomPlayerClock": "自定义玩家时钟。双击设置你自己的值。",
    "Tooltip_OnlineArena_NumPlayers": "玩家数量",
    "Tooltip_OnlineArena_StartingPlayer": "起始玩家",
    "Tooltip_OnlineArena_MinKarma": "最低因果等级",
    "Tooltip_OnlineArena_RankingToggle": "排名开关",
    "Tooltip_OnlineArena_GameName": "你的游戏名称",
    "Tooltip_OnlineArena_PrivateGameButton": "私人游戏需要密码",
    "Tooltip_OnlineArena_SingleSessionGame": "单场游戏必须连续进行。断开连接的玩家将被机器人取代。",
    "Tooltip_OnlineArena_MultiSessionGame": "多场游戏可以暂停，并且可以同时进行多场。",
    "Tooltip_OnlineArena_PlayerClock": "玩家时钟：分配给每位玩家完成整场游戏的时间。",
    "Tooltip_OnlineArena_Expansions": "本场游戏使用的扩展",
    "Tooltip_OnlineArena_GameRanked": "此游戏计入排名",
    "Tooltip_OnlineArena_GameNotRanked": "此游戏不计入排名",
    "Tooltip_OnlineArena_AutoRedeployment": "重新部署将由 AI 自动管理。",
    "Tooltip_OnlineArena_PrivateGame": "此游戏为私人游戏，你需要输入密码才能加入。",
    "Tooltip_NextAction_MayRollDie": "掷骰获得攻击加成",
    "Tooltip_NextAction_BeforeEndConquerPhase": "使用特殊能力征服",
}

# ============================================================
# errorMessages.xml translations
# ============================================================
EM_TRANSLATIONS = {
    "SWError_CannotResumeGame": "无法继续游戏",
    "SWError_ClientDisconnected": "客户端断开连接",
    "SWError_UnknownAuthError": "未知认证错误",
    "SWError_AccessDenied": "访问被拒绝",
    "SWError_ServerFull": "服务器已满",
    "SWError_MaintenanceMode": "维护模式",
    "SWError_NeedAuthentication": "需要认证",
    "SWError_UnknownGameType": "未知游戏类型",
    "SWError_UnknownDevice": "未知设备",
    "SWError_ServerDisconnected": "服务器断开连接",
    "SWError_BadVersion": "版本错误",
    "SWError_GameNotStarted": "游戏未开始",
    "SWError_WrongGame": "错误的游戏",
    "SWError_NoLocalPlayer": "无本地玩家",
    "SWError_UnknownError": "未知错误",
    "SWError_NotYourTurn": "不是你的回合",
    "SWError_UnknownPlayer": "未知玩家",
    "SWError_UnknownGame": "未知游戏",
    "SWError_TooManyOffers": "提议过多",
    "SWError_UnknownDeviceToken": "未知设备令牌",
    "SWError_ServerError": "服务器错误",
    "SWError_NotEnoughKarma": "因果值不足",
    "SWError_TooManyGames": "游戏过多",
    "SWError_GameFull": "游戏已满",
    "SWError_Ignored": "已忽略",
    "SWError_PasswordMismatch": "密码不匹配",
    "SWError_DuplicatePlayer": "重复玩家",
    "SWError_SaveIncompatible": "旧版不兼容的备份",
}

# ============================================================
# ssoStrings.xml translations
# ============================================================
SSO_TRANSLATIONS = {
    "ConnectionError_Title": "连接错误",
    "SSOController_Title": "认证",
    "SigninInProgressPanel_LabelFormat": "正在认证… %s",
    "MessageBox_SkipButton": "跳过",
    "MessageBox_BackButton": "返回",
    "AlreadyPlayedPanel_Title": "以前玩过在线版吗？",
    "AlreadyPlayedPanel_Message": "你已经有\nDays of Wonder 在线账号吗？",
    "AlreadyPlayedPanel_SubMessage": "我们将帮你找到账号",
    "LoginPanel_Title": "登录",
    "LoginPanel_Message": "请输入你的登录名或\n电子邮件地址",
    "LoginPanel_LoginEmailInvalid_Message": "无效的登录名或电子邮件",
    "LoginPanel_Placeholder": "登录名或电子邮件",
    "PasswordPanel_Title": "密码",
    "PasswordPanel_Message": "我们找到了你的账号。\n让我们登录吧。",
    "PasswordPanel_PasswordInvalid_Message": "无效的密码",
    "PasswordPanel_Placeholder": "密码",
    "PasswordPanel_Forgot_Button": "忘记密码？",
    "PasswordPanel_EmailSent_Message": "我们已向你发送电子邮件。请按照说明操作",
    "LinkPanel_Title": "账号已关联",
    "WelcomePanel_Title": "欢迎来到 Days of Wonder 在线！",
    "WelcomePanel_Placeholder": "电子邮件",
    "WelcomePanel_SubMessage": "我们将对你的电子邮件保密。",
    "AskEmailPanel_Title": "接收密码",
    "AskEmailPanel_Placeholder": "在此输入你的电子邮件地址",
    "AskEmailPanel_SubMessage": "我们将对你的电子邮件保密。",
    "AskEmailPanel_SpamBox": "接收 Days of Wonder 新闻",
    "AccountsShouldMergePanel_Title": "合并你的账号",
    "AccountsShouldMergePanel_Message": "你已经有另一个使用该电子邮件的账号。我们强烈建议你合并账号。为此，请前往 Days of Wonder 网站的账号详情，点击\"合并账号\"。",
    "FoundEmailPanel_Title": "输入密码",
    "FoundEmailPanel_Message": "我们找到了你的账号。我们已向你发送电子邮件。请按照其中的说明操作，然后在下方输入密码：",
    "FoundEmailPanel_Placeholder": "密码",
    "PasswordSentPanel_Title": "密码已发送",
    "PasswordSentPanel_Message": "包含登录名和密码的电子邮件已发送到你的地址。",
    "AccountCreatedPanel_Title": "账号已创建",
    "AccountCreatedPanel_Message": "激活电子邮件已发送到你的地址，请务必查收。未激活的账号将在 7 天后删除。",
    "LinkPanel_Message": "你的账号：Days of Wonder%s 现已关联。",
    "LinkPanel_Sub_Message": "、%s",
    "WelcomePanel_EmailMessage": "输入你的电子邮件地址。",
    "WelcomePanel_EmailInvalid_Message": "无效的电子邮件",
    "WelcomePanel_PasswordMessage": "输入你的密码。",
    "AskEmailPanel_Message": "你的 Days of Wonder 在线账号没有有效的电子邮件。输入你的电子邮件地址，你将收到密码。",
    "AskEmailPanel_EmailInvalid_Message": "无效的电子邮件",
    "LoginSettingsPanel_Title": "登录账号",
    "LoginSettingsPanel_LogoutButton": "登出",
    "LoginSettingsPanel_GetMyPasswordButton": "获取密码",
    "LoginSettingsPanel_EditMyProfileButton": "编辑个人资料",
    "LoginSettingsPanel_UpdateMyEmailButton": "更新电子邮件",
    "LoginSettingsPanel_SupportButton": "支持",
    "LoginSettingsPanel_Leave_Title": "离开小小世界",
    "LoginSettingsPanel_EditAccount_Message": "你将被重定向到浏览器查看账号。\n是否离开应用？",
    "LoginSettingsPanel_Support_Message": "你将被重定向到浏览器。\n是否离开应用？",
    "LoginSettingsPanel_LinkButton": "设置自动登录",
    "LoginSettingsPanel_RepairButton": "启用自动登录",
    "LoginSettingsPanel_SettingsButton": "打开应用设置",
    "LoginSettingsPanel_LoginButton": "登录",
    "LoginSettingsPanel_LinkErrorTitle": "此账号已关联",
    "LoginSettingsPanel_LinkErrorMessage": "此 %s 账号已关联到另一个 Days of Wonder 账号：%s",
    "PlatformUserIdChooserPanel_Title": "选择你的账号",
    "LoginError_Title": "错误",
    "LoginError_MessageFormat": "刚刚发生错误：%s",
    "EditLoginPanel_Placeholder": "登录名或电子邮件",
    "EditLoginPanel_Message": "请输入你的登录名",
    "EditLoginPanel_LoginExisting_Message": "此登录名已存在",
    "EditLoginPanel_LoginInvalid_Message": "无效：[A-Z][a-z][0-9]-_",
    "ValidatedAccountMessageBoxController_Title": "请先确认你的账号",
    "ValidatedAccountMessageBoxController_Message": "检查你的邮箱以获取账号确认邮件并按照说明操作。\n完成后，点击\"重试\"按钮。",
    "ValidatedAccountMessageBoxController_HelpMessage1": "找不到邮件？检查垃圾邮件文件夹。",
    "ValidatedAccountMessageBoxController_HelpMessage2": "还是没有？我们已发送到：",
    "ValidatedAccountMessageBoxController_HelpMessage3": "使用\"重新发送\"按钮再次接收。\n使用\"更改电子邮件\"按钮设置新的电子邮件地址。",
    "ValidatedAccountMessageBoxController_TryAgain": "重试",
    "ValidatedAccountMessageBoxController_CorrectEmail": "更改电子邮件",
    "ValidatedAccountMessageBoxController_SendAgain": "重新发送",
    "ValidatedAccountMessageBoxController_Help": "帮助",
    "ValidatedAccountMessageBoxController_ChangeEmailTitle": "更改你的电子邮件",
    "ValidatedAccountMessageBoxController_ChangeEmailMessage": "请输入新的电子邮件以验证账号：",
    "ValidatedAccountMessageBoxController_ChangeEmailIdentical": "电子邮件相同，未做更改",
    "ValidatedAccountMessageBoxController_ChangeEmailInvalid": "无效的电子邮件，未做更改",
    "ValidatedAccountMessageBoxController_ChangeEmailAlreadyTaken": "电子邮件已被占用，未做更改",
    "ValidatedAccountMessageBoxController_Validate": "验证",
    "ValidatedAccountMessageBoxController_Cancel": "取消",
    "PartnerLabelSteam": "Steam",
    "PartnerLabelAmazon": "Amazon",
    "PartnerLabelGoogle": "Google",
    "PartnerLabelGameCenter": "Game Center",
    "PartnerLabelPlayStationNetwork": "PlayStation™Network 账号",
    "AskEmailPanel_PrivacyBox": "接受隐私政策",
    "LoginSettingsPanel_UnlinkButton": "取消关联账号",
    "LoginSettingsPanel_RepairSettingsMessage": "打开应用设置并允许通讯录权限以启用账号关联自动登录。",
    "LoginSettingsPanel_RepairRationaleMessage": "允许访问你的通讯录以启用账号关联自动登录。",
    "LoginSettingsPanel_LinkSettingsMessage": "打开应用设置并允许通讯录权限以设置账号关联自动登录。",
    "LoginSettingsPanel_LinkRationaleMessage": "允许访问你的通讯录以设置账号关联自动登录。",
}


def translate_xml_file(en_path, out_path, translations):
    """Read English XML, apply translations, write to output."""
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for key, val in translations.items():
        # Match <string key="KEY">VALUE</string>
        pattern = r'(<string key="' + re.escape(key) + r'">)(.*?)(</string>)'
        def repl(m):
            return m.group(1) + val + m.group(3)
        content = re.sub(pattern, repl, content, flags=re.DOTALL)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  {os.path.basename(out_path)}: {len(translations)} strings")


def translate_strings_file(en_path, out_path, translations):
    """Read Apple .strings file, apply translations."""
    with open(en_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []
    for line in lines:
        m = re.match(r'^"([^"]+)"\s*=\s*"(.*)";\s*$', line)
        if m and m.group(1) in translations:
            out.append(f'"{m.group(1)}" = "{translations[m.group(1)]}";\n')
        else:
            out.append(line)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(out)
    print(f"  {os.path.basename(out_path)}: {len(translations)} strings")


def main():
    print("Translating XML/strings files to Chinese (ja.lproj)...")
    translate_xml_file(
        os.path.join(EN, "localizedStrings.xml"),
        os.path.join(JA, "localizedStrings.xml"),
        LS_TRANSLATIONS)
    translate_xml_file(
        os.path.join(EN, "tooltips.xml"),
        os.path.join(JA, "tooltips.xml"),
        TT_TRANSLATIONS)
    translate_xml_file(
        os.path.join(EN, "errorMessages.xml"),
        os.path.join(JA, "errorMessages.xml"),
        EM_TRANSLATIONS)
    translate_xml_file(
        os.path.join(EN, "ssoStrings.xml"),
        os.path.join(JA, "ssoStrings.xml"),
        SSO_TRANSLATIONS)

    # Localizable.strings
    ls_trans = {
        "YOUR_TURN_ACTION": "开始游戏",
        "YOUR_TURN": "现在轮到你了！",
        "YOUR_TURN_ROBOT": "现在轮到你了！",
        "YT_INVITE_ACTION": "开始游戏",
        "YOUR_TURN_INVITE": "你被邀请来玩！",
        "INVITATION_ACTION": "开始游戏",
        "CONFIRM_INVITATION": "你被邀请来玩！",
        "GAME_OVER_ACTION": "游戏结束",
        "GAME_OVER": "一场游戏刚刚结束",
    }
    translate_strings_file(
        os.path.join(EN, "Localizable.strings"),
        os.path.join(JA, "Localizable.strings"),
        ls_trans)

    print("Done! XML/strings files translated.")


if __name__ == "__main__":
    main()
