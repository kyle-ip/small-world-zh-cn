# -*- coding: utf-8 -*-
"""
Translate compendium HTML files from English to Chinese.
Processes both full (en) and short (en-short) versions.
"""
import os
import re

COMPENDIUM_GAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Resources", "compendium")
)
COMPENDIUM_OUT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "payload", "Resources", "compendium")
)
COMPENDIUM = COMPENDIUM_GAME  # EN sources; writers below should target zh/zh-short under COMPENDIUM_OUT


# ============================================================
# Comprehensive translation dictionary for compendium text
# ============================================================
TRANS = {
    # Race names
    "Amazons": "亚马逊", "Dwarves": "矮人", "Elves": "精灵", "Ghouls": "食尸鬼",
    "Giants": "巨人", "Halflings": "半身人", "Humans": "人类", "Orcs": "兽人",
    "Ratmen": "鼠人", "Skeletons": "骷髅", "Sorcerers": "巫师", "Tritons": "人鱼",
    "Trolls": "巨魔", "Wizards": "法师", "Goblins": "哥布林", "Kobolds": "狗头人",
    "Nomads": "游牧民", "Priestesses": "女祭司", "White Ladies": "白衣女士",
    "Barbarians": "野蛮人", "Homunculi": "人造人", "Leprechauns": "小矮妖",
    "Pixies": "小精灵", "Witch Doctors": "巫医", "Igors": "伊戈尔",
    "Shrubmen": "灌木人",     "Fauns": "羊人", "Slingmen": "投石兵",
    "Ice Witches": "冰雪女巫", "Skags": "斯卡斯",
    # Power names
    "Alchemist": "炼金术士", "Berserk": "狂暴", "Bivouacking": "露营",
    "Commando": "突击队", "Diplomat": "外交官", "Dragon Master": "驯龙师",
    "Flying": "飞行", "Forest": "森林", "Fortified": "筑城", "Heroic": "英雄",
    "Hill": "山丘", "Merchant": "商人", "Mounted": "骑兵", "Pillaging": "掠夺",
    "Seafaring": "航海", "Spirit": "灵魂", "Stout": "坚韧", "Swamp": "沼泽",
    "Underworld": "地下世界", "Wealthy": "富豪", "Cursed": "诅咒",
    "Hordes Of": "成群", "HordesOf": "成群", "Marauding": "劫掠",
    "Ransacking": "洗劫", "Were": "狼人", "Historian": "历史学家",
    "Peace Loving": "和平主义", "Barricade": "街垒", "Catapult": "投石机",
    "Corrupt": "腐化", "Imperial": "帝国", "Mercenary": "雇佣兵",
    "Fireball": "火球", "Aquatic": "水生", "Behemoth": "巨兽", "Lava": "熔岩",
    "Soul-Touch": "灵魂触摸", "Copycat": "模仿者",
    "DragonMaster": "驯龙师",
    # Game terms
    "Race": "种族", "Races": "种族", "Special Power": "特殊能力",
    "Special Powers": "特殊能力", "Region": "地区", "Regions": "地区",
    "Race Token": "种族代币", "Race Tokens": "种族代币", "Combo": "组合",
    "Combos": "组合", "Victory Coin": "胜利金币", "Victory Coins": "胜利金币",
    "Coin": "金币", "Coins": "金币", "Conquer": "征服", "Conquers": "征服",
    "Conquering Regions": "征服地区", "Redeploy": "重新部署",
    "Redeploying Tokens": "重新部署代币", "Decline": "衰落", "In Decline": "衰落中",
    "Going In Decline": "进入衰落", "Going in Decline": "进入衰落",
    "Goes in Decline": "进入衰落", "Turn": "回合", "Game Turn": "游戏回合",
    "Conquest Die": "征服骰", "Markers": "标记", "Marker": "标记",
    "Mountains": "山脉", "Dragon": "龙", "Heroes": "英雄",
    "Karma": "因果", "Rank Score": "排名分数", "Ranking & Karma": "排名与因果",
    "Ranked games": "排名游戏", "Player Clock": "玩家时钟",
    "Single Session": "单场游戏", "Multi Session": "多场游戏",
    "Single Session vs Multi Session": "单场游戏与多场游戏",
    "Online Arena": "在线竞技场", "Settings": "设置", "Game Settings": "游戏设置",
    "Chat": "聊天", "Support": "支持", "Contact us": "联系我们",
    "Goal of the Game": "游戏目标", "Goal of the game": "游戏目标",
    "Picking a Race": "选择种族", "Picking a new Race": "选择新种族",
    "Picks a new Race": "选择新种族", "Scoring": "计分", "Scores": "分数",
    "Races and Special Power Combo's": "种族与特殊能力组合",
    "Race and Special Power Combo": "种族与特殊能力组合",
    "Race Tokens with their colored side up are active; those with their grayed-out side up, in Decline.": "彩色面朝上的种族代币为活跃状态；灰色面朝上的为衰落状态。",
    "Red": "红色", "Green": "绿色", "Red Regions": "红色地区", "Green Regions": "绿色地区",
    "Lost Tribes": "失落部落", "Lost Tribes that occupy the board at game start": "游戏开始时占据地图的失落部落",
    "Description": "描述", "More Description": "更多描述", "More description": "更多描述",
    "Optional Text": "可选文本", "Optional description (not shown in combo picking UI)": "可选描述（不在组合选择界面显示）",
    "Minimum": "最低", "Automatic Redeployment": "自动重新部署", "Automatic Redeploy\u00adment": "自动重新部署",
    "Type of game:": "游戏类型：", "Number of players required to start this game.": "开始此游戏所需的玩家数量。",
    "Whether the game is Private or Public. Private games require a password.": "游戏是私人还是公开。私人游戏需要密码。",
    "Give a short memorable name to your game.": "为你的游戏起一个简短易记的名字。",
    "Expansions in play in this game.": "本场游戏使用的扩展。",
    "List of Open Games": "开放游戏列表",
    "Creating a New Game": "创建新游戏",
    "Invite Buddies": "邀请好友",
    "Presence & In-game Chat": "在线状态与游戏内聊天",
    "Presence Indicator": "在线状态指示器",
    "Useful Things To Know": "须知事项",
    "Lairs from the Trolls race": "巨魔种族的巢穴",
    "Encampments from the Bivouacking Special Power": "露营特殊能力的营地",
    "Fortresses from the Fortified Special Power": "筑城特殊能力的堡垒",
    "Holes-in-the-Ground from the Halflings race": "半身人种族的地洞",
    "Copycat (by Andrew Capel)": "模仿者（Andrew Capel 设计）",
    "Ice Witches (by Andrew Capel)": "冰雪女巫（Andrew Capel 设计）",
    "Lava (by Alex Gurski)": "熔岩（Alex Gurski 设计）",
    "Skags (by Randy Pitchford)": "斯卡斯（Randy Pitchford 设计）",
    "Slingmen (by Bill Gurski)": "投石兵（Bill Gurski 设计）",
    "Soul-Touch (by Randy Pitchford)": "灵魂触摸（Randy Pitchford 设计）",
    # Full sentences - Races
    "Four additional Amazon tokens may be used for conquest only, not for defense. So you start your initial turn with 6 + 4 = 10 Amazon tokens (plus any additional ones you may get from the Special Power associated with your Amazons, depending on your combo).": "额外的 4 个亚马逊代币只能用于征服，不能用于防御。因此你的初始回合以 6 + 4 = 10 个亚马逊代币开始（加上你可能从与亚马逊关联的特殊能力获得的额外代币，取决于你的组合）。",
    "At the end of each of your Troop Redeployments, you must remove 4 Amazon tokens from the map, by drag-and-dropping them back onto your tokens area. Make sure to leave at least 1 Amazon token in each Region, if possible. These 4 tokens become available again, for Attack only, at the start of your next turn.": "在每次部队重新部署结束时，你必须从地图上移除 4 个亚马逊代币，通过拖放将它们放回你的代币区域。如果可能，请确保每个地区至少留下 1 个亚马逊代币。这 4 个代币在下一回合开始时再次可用，但仅用于攻击。",
    "Each Mine Region your Dwarves occupy is worth 1 bonus Victory coin, at the end of your turn. This power is kept even when the Dwarves are In Decline.": "在你的回合结束时，矮人占据的每个矿产地区价值 1 枚额外胜利金币。即使矮人进入衰落，此能力仍然保留。",
    "When the enemy conquers one of your Regions, you keep all your Elf tokens for redeployment at the end of the current player's turn, rather than losing 1 Elf token.": "当敌人征服你的一个地区时，你保留所有精灵代币在当前玩家回合结束时重新部署，而不是损失 1 个精灵代币。",
    "In addition, unlike other Races, once In Decline your Ghouls can continue to conquer new Regions in the following turns, playing exactly as if they were still Active tokens.": "此外，与其他种族不同，一旦进入衰落，你的食尸鬼可以在接下来的回合中继续征服新地区，就像它们仍然是活跃代币一样。",
    "Your Ghoul tokens all stay on the map when going into Decline, instead of the usual 1 token per Region.": "进入衰落时，你的食尸鬼代币全部留在地图上，而不是通常的每个地区 1 个代币。",
    "Your Giants may conquer any Region adjacent to a Mountain Region they occupy at a cost of 1 less Giant token than normal. A minimum of 1 Giant token is still required.": "你的巨人可以征服与他们占据的山脉地区相邻的任何地区，所需巨人士币比正常少 1 个。仍需至少 1 个巨人士币。",
    "Your Halfling tokens may enter the map through any Region of the map, not just border ones. A Hole-in-the-Ground will be placed in each of the first 2 Regions you conquer, making them immune to enemy conquests as well as racial and special powers.": "你的半身人士币可以通过地图上的任何地区进入地图，而不仅仅是边境地区。你征服的前 2 个地区各放置一个地洞，使其免疫敌人的征服以及种族和特殊能力。",
    "Your Holes-in-the-Ground are removed (and you lose the protection they confer) when your Halflings go into Decline, or when you choose to abandon a Region containing a Hole-in-the-Ground.": "当你的半身人进入衰落，或你选择放弃包含地洞的地区时，你的地洞被移除（你失去它们提供的保护）。",
    "Each Farmland Region your Humans occupy is worth 1 bonus Victory coin, at the end of your turn.": "在你的回合结束时，人类占据的每个农田地区价值 1 枚额外胜利金币。",
    "Each non-empty Region your Orcs conquered this turn is worth 1 bonus Victory coin, at the end of your turn.": "在你的回合结束时，兽人本回合征服的每个非空地区价值 1 枚额外胜利金币。",
    "During your Troop Redeployment, you receive 1 new Skeleton token for every 2 non-empty Regions you conquered this turn. It's automatically added to the troops you redeploy at the end of your turn.": "在部队重新部署期间，你每征服 2 个非空地区就获得 1 个新的骷髅代币。它会自动添加到你回合结束时重新部署的部队中。",
    "The number of Skeletons is limited to 20 tokens.": "骷髅数量上限为 20 个代币。",
    "Once per turn per opponent, your Sorcerers can conquer a Region by substituting one of your opponent's Active tokens with one of your own. To do so, simply drag-and-drop the Wand icon from your hand onto the token you want to replace with a new Sorcerer.": "每回合对每个对手一次，你的巫师可以用你自己的一个代币替换对手的一个活跃代币来征服地区。要这样做，只需将手牌中的魔杖图标拖放到你想用新巫师替换的代币上。",
    "Your number of Sorcerer tokens is limited to 18. If there are no more tokens, then you cannot conquer a new Region in this way. If an Elf is converted by a Sorcerer, the Elf does lose his token.": "你的巫师代币数量上限为 18 个。如果没有更多代币，则无法以此方式征服新地区。如果精灵被巫师转化，精灵确实会失去代币。",
    "The token your Sorcerers replaces must be the only race token in its Region and that Region must be one your Sorcerers are able to conquer. A single Troll token with its Troll's Lair is considered alone; likewise for a Race token in a Fortress or on a Mountain; these markers provide no protection to a lone Race token.": "你的巫师替换的代币必须是该地区唯一的种族代币，且该地区必须是你的巫师能够征服的。带巨魔巢穴的单个巨魔代币被视为单独的；堡垒中或山脉上的种族代币也是如此；这些标记不保护单独的种族代币。",
    "Note: If an Elf is converted by a Sorcerer, the Elf does lose his token.": "注意：如果精灵被巫师转化，精灵确实会失去代币。",
    "Your Tritons may conquer all Coastal Regions (those bordering a Sea or Lake) at a cost of 1 less Triton token than normal. A minimum of 1 Triton token is still required.": "你的人鱼可以征服所有沿海地区（与海洋或湖泊接壤的地区），所需人士币比正常少 1 个。仍需至少 1 个人鱼代币。",
    "Only Seafaring races may occupy the Seas and the Lake.": "只有航海种族可以占据海洋和湖泊。",
    "Place a Troll's Lair in each Region your Trolls occupy.": "在你的巨魔占据的每个地区放置一个巨魔巢穴。",
    "The Troll's Lair augments your region's defense by 1 and stays in the Region even after your Trolls go into Decline. The Troll's Lair disappears if you abandon the Region or when an enemy conquers it.": "巨魔巢穴使你地区的防御 +1，即使巨魔进入衰落后仍留在该地区。如果你放弃该地区或敌人征服它，巨魔巢穴消失。",
    "Each Magic Region your Wizards occupy is worth 1 bonus Victory coin, at the end of your turn.": "在你的回合结束时，法师占据的每个魔法地区价值 1 枚额外胜利金币。",
    "You may conquer any In Decline Region at a cost of 1 less Goblin token than normal. A minimum of 1 token is still required.": "你可以征服任何衰落中的地区，所需哥布林代币比正常少 1 个。仍需至少 1 个代币。",
    "You may never occupy (nor conquer) a Region with less than 2 Kobold tokens. When going In Decline however, keep a single token in each Region, as normal.": "你永远不能用少于 2 个狗头人代币占据（或征服）一个地区。但进入衰落时，像平常一样在每个地区保留 1 个代币。",
    "You may conquer any Region of the map except Seas and Lakes. These Regions do not need to be adjacent or contiguous to ones you already occupy.": "你可以征服地图上除海洋和湖泊外的任何地区。这些地区不需要与你已占据的地区相邻或相连。",
    "Once per turn, you may place the Catapult in a region you occupy to conquer any region that is 1 region away (but not adjacent) at 1 less token than usual. The Catapult may be used to attack a region beyond the Lake, but not over Seas.": "每回合一次，你可以将投石机放置在你占据的地区，以征服距离 1 个地区（但不相邻）的任何地区，所需代币比平常少 1 个。投石机可以攻击湖泊对岸的地区，但不能越过海洋。",
    "The region with the Catapult is immune to enemy conquests as well as their racial and special powers.": "有投石机的地区免疫敌人的征服以及他们的种族和特殊能力。",
    "The Catapult disappears when you go into Decline.": "投石机在你进入衰落时消失。",
    "When a Region is conquered this way, they immediately take 1 Victory coin from the stash. They may conquer Regions beyond the Lake, but not over the Seas.": "当以此方式征服地区时，他们立即从储备中取走 1 枚胜利金币。他们可以征服湖泊对岸的地区，但不能越过海洋。",
    "If the Loot marker is a Skag Attack marker, the conquest is cancelled and the opponent loses one token (he cannot retry any attack against this region during this turn).": "如果战利品标记是斯卡斯攻击标记，征服被取消且对手损失 1 个代币（他本回合不能重试对该地区的任何攻击）。",
    "Otherwise, the opponent collects the Loot token.": "否则，对手收集战利品代币。",
    "When they go In Decline, all your In-Decline Priestesses stack together to form a single \"Ivory Tower\" pile in one of the Regions they occupy, abandoning all other regions. Each turn, you score 1 bonus Victory coin for each Priestess in the Ivory Tower, in lieu of your usual In Decline scoring.": "进入衰落时，你所有衰落中的女祭司堆叠在一起，在她们占据的一个地区形成一个单一的\"象牙塔\"堆，放弃所有其他地区。每回合，象牙塔中的每个女祭司为你获得 1 枚额外胜利金币，代替你通常的衰落计分。",
    "Beware: Your Ivory Tower may still be conquered like any other Region (with enough Race tokens or a Dragon)! If your Priestesses were Fortified, their Ivory Tower can be built atop a single Fortress.": "注意：你的象牙塔仍可能像其他任何地区一样被征服（用足够的种族代币或龙！）如果你的女祭司有筑城能力，她们的象牙塔可以建在单个堡垒之上。",
    "Once In Decline, your White Ladies become immune to your opponents' conquests and racial and special powers!": "一旦进入衰落，你的白衣女士对对手的征服以及种族和特殊能力免疫！",
    "Your Barbarians cannot redeploy their troops, at the end of each turn.": "你的野蛮人在每回合结束时不能重新部署部队。",
    "If your final conquest attempt fails, the unused Barbarians remain off the board until the start of your next turn.": "如果你最后的征服尝试失败，未使用的野蛮人留在棋盘外，直到下一回合开始。",
    "Each time a Homunculi Race combo is bypassed, in addition to a Victory coin, a Homunculus token is automatically added to the combo. These tokens are added to those normally received when the Homunculi combo is finally picked, along with any Victory coins.": "每次跳过人造人种族组合时，除了胜利金币外，还会自动向该组合添加 1 个人造人代币。这些代币会添加到最终选择人造人组合时通常获得的代币中，以及任何胜利金币。",
    "During Redeployment, you may drag 1 Pot of Gold in each region your Leprechauns occupy (but never more than 1 per region). Each Pot of Gold still present at the start of your next turn goes into your Victory stash and is worth 1 coin.": "在重新部署期间，你可以在小矮妖占据的每个地区拖动 1 罐金币（但每个地区不超过 1 罐）。在下一回合开始时仍存在的每罐金币进入你的胜利储备，价值 1 枚金币。",
    "If an opponent conquers one of these regions before your next turn, he gets the Pot of Gold instead. Any remaining Pot of Gold can be reused during subsequent redeployments, until they're all gone.": "如果对手在下一回合前征服其中一个地区，他将获得金币罐。任何剩余的金币罐可以在后续重新部署中重复使用，直到全部用完。",
    "During your Troop Redeployment, all of your Pixies, except one per region they occupy, leave the board. They remain off the board until the start of your next turn.": "在部队重新部署期间，你所有的小精灵，除了每个占据地区留 1 个外，都离开棋盘。它们留在棋盘外，直到下一回合开始。",
    "Each time you lose a Witch Doctor token, the reinforcement die is rolled and you receive as many new Witch Doctors as there are pips on the die (up to the maximum number of Witch Doctors available). Deploy them on the board at the end of the current player's turn.": "每次你失去 1 个巫医代币时，掷强化骰，你获得的新巫医数量等于骰子的点数（最多不超过可用巫医的最大数量）。在当前玩家回合结束时将它们部署到棋盘上。",
    "You collect all Race tokens (Lost Tribes and all Player's race tokens, including your own) lost in conquests. At the beginning of your turn, these collected tokens spawn new Igor tokens, at a rate of 1 new Igor per set of collected tokens equal to the number of players in your game.": "你收集所有在征服中损失的种族代币（失落部落和所有玩家的种族代币，包括你自己的）。在你的回合开始时，这些收集的代币生成新的伊戈代币生成速率为每收集等于游戏玩家数量的代币生成 1 个新伊戈尔。",
    "In a 4 player game, 4 collected tokens spawn 1 new Igor token; in a 2 player game, they'd spawn 2 new Igors; in a 3 player game, they'd spawn 1 new Igor, with 1 collected token left for later use. And in a 5 player game, you'd still need to collect 1 more token before spawning an Igor.": "在 4 人游戏中，4 个收集的代币生成 1 个新伊戈尔代币；在 2 人游戏中，生成 2 个新伊戈尔；在 3 人游戏中，生成 1 个新伊戈尔，剩余 1 个收集的代币供以后使用。在 5 人游戏中，你还需要再收集 1 个代币才能生成 1 个伊戈尔。",
    "All Forest regions occupied by Shrubmen become immune to opponents' conquests, racial and special powers, even when In Decline.": "灌木人占据的所有森林地区对对手的征服、种族和特殊能力免疫，即使在衰落中也是如此。",
    "Slingmen may conquer a Region that is one Region away from one they currently occupy, provided they do not control a Region adjacent to it.": "投石兵可以征服距离其当前占据地区 1 个地区的地区，前提是他们不控制与该地区相邻的地区。",
    "At the end of their Redeployment phase, Ice Witches may place their Winter markers in their own Regions or any adjacent Region (there cannot be more than 1 Winter marker per Region though).": "在重新部署阶段结束时，冰雪女巫可以将她们的冬季标记放置在自己的地区或任何相邻地区（但每个地区不能超过 1 个冬季标记）。",
    "Ice Witches collect 1 Winter marker for each Magic Source they control at the end of their Redeployment phase.": "冰雪女巫在重新部署阶段结束时，每控制一个魔法源收集 1 个冬季标记。",
    "It remains on the board as long as the Ice Witches are active. Regions with a Winter marker that are not controlled by an Ice Witch earn 1 less Victory coin than usual.": "只要冰雪女巫活跃，它就留在棋盘上。有冬季标记但不被冰雪女巫控制的地区比平常少获得 1 枚胜利金币。",
    # Power descriptions
    "Collect 2 bonus Victory coins at the end of each turn your race hasn't yet gone into Decline.": "在你的种族尚未进入衰落的每个回合结束时，收集 2 枚额外胜利金币。",
    "Collect 1 bonus Victory Coin for each Coastal Region you occupy. Each non-Coastal Region brings 1 less Victory Coin than usual.": "你占据的每个沿海地区收集 1 枚额外胜利金币。每个非沿海地区比平常少获得 1 枚胜利金币。",
    "Collect 1 bonus Victory coin for any Region you occupy at turn's end.": "回合结束时，你占据的任何地区收集 1 枚额外胜利金币。",
    "Collect 1 bonus Victory coin for each Forest Region you occupy at turn's end.": "回合结束时，你占据的每个森林地区收集 1 枚额外胜利金币。",
    "Collect 1 bonus Victory coin for each Hill Region you occupy at turn's end.": "回合结束时，你占据的每个山丘地区收集 1 枚额外胜利金币。",
    "Collect 1 bonus Victory coin for each Swamp Region you occupy at turn's end.": "回合结束时，你占据的每个沼泽地区收集 1 枚额外胜利金币。",
    "Collect 1 bonus coin from any opponent each time they successfully conquer one of your active regions.": "每次对手成功征服你的一个活跃地区时，从该对手处收集 1 枚额外金币。",
    "Collect 3 bonus Victory coins at the end of each turn during which you attacked no active Race.": "在你没有攻击任何活跃种族的每个回合结束时，收集 3 枚额外胜利金币。",
    "Collect 3 bonus coins each time your Barricade troops occupy 4 regions or less at the end of your turn.": "每次你的街垒部队在回合结束时占据 4 个或更少地区时，收集 3 枚额外金币。",
    "Collect 7 bonus Victory coins, once only, at the end of your first turn.": "仅在第一回合结束时，收集 7 枚额外胜利金币。",
    "Collect 1 bonus Victory coin for each Race In Decline at the time you select the Historians. While you're active, collect 1 bonus Victory coin each time another Race goes In Decline, and 1 final bonus coin when your own Historians go In Decline!": "选择历史学家时，每个衰落中的种族收集 1 枚额外胜利金币。在你活跃期间，每当另一个种族进入衰落时收集 1 枚额外胜利金币，当你自己的历史学家进入衰落时再收集 1 枚最终额外金币！",
    "Each non-empty Region you conquer this turn is worth 1 bonus Victory coin at turn's end.": "你本回合征服的每个非空地区在回合结束时价值 1 枚额外胜利金币。",
    "You may conquer any Hill or Farmland Region with 1 less Race token than normal. A minimum of 1 token is still required.": "你可以征服任何山丘或农田地区，所需种族代币比正常少 1 个。仍需至少 1 个代币。",
    "You may conquer any Region with 1 less Race token than normal. A minimum of 1 token is still required.": "你可以征服任何地区，所需种族代币比正常少 1 个。仍需至少 1 个代币。",
    "You may conquer any Region with a Cavern with 1 less Race token than normal. A minimum of 1 token is still required. All Regions with a Cavern are also considered adjacent to each other for your conquest purposes.": "你可以征服任何有洞穴的地区，所需种族代币比正常少 1 个。仍需至少 1 个代币。所有有洞穴的地区在征服目的上也被视为彼此相邻。",
    "As long as your Seafaring race is active, you may conquer the Seas and the Lake, considering them as 3 empty Regions.": "只要你的航海种族活跃，你就可以征服海洋和湖泊，将它们视为 3 个空地区。",
    "You may go In Decline at the end of a regular turn of conquests, after scoring, instead of spending an entire turn going into Decline.": "你可以在常规征服回合结束时，计分后进入衰落，而不是花费整个回合进入衰落。",
    "When the Race tokens associated with your Spirit Special Power go into Decline, they never count toward the limit regarding having a single In Decline race on the map at any given time.": "当与你的灵魂特殊能力关联的种族代币进入衰落时，它们不计入地图上任何时候只能有一个衰落种族的限制。",
    "In other words, your In Decline Spirits never leave the map (except when taking losses from opponents' conquests), though other races sent In Decline may go away when a new race goes into decline.": "换句话说，你衰落中的灵魂永远不会离开地图（除非因对手征服而损失），但其他进入衰落的种族可能会在新种族进入衰落时消失。",
    "You may thus end up with two different races In Decline on the map at the same time and score for them both. If a third race you control goes into Decline, your Spirits remain on the board, although the other race already In Decline disappears, as normal.": "因此，你可能最终在地图上同时有两个不同的衰落种族并为它们计分。如果你控制的第三个种族进入衰落，你的灵魂留在棋盘上，但另一个已衰落的种族照常消失。",
    "Each turn you may break camp and settle in any new Region you occupy. Encampments are never lost during an attack on the Region they are in: they are redeployed at the end of the current player's turn. When the Race they were associated with goes into Decline, they disappear.": "每回合你可以拔营并在你占据的任何新地区定居。营地在其所在地区遭受攻击时永远不会丢失：它们在当前玩家回合结束时重新部署。当它们关联的种族进入衰落时，它们消失。",
    "Deploy the 5 Encampment tokens in any of your Region(s), during your Troop Redeployment phase. Each Encampment counts as 1 Race token toward the defense of the Region in which it is placed (thereby protecting a single Race token with an Encampment from the Sorcerer's Racial Power).": "在部队重新部署阶段，将 5 个营地代币部署到你的任何地区。每个营地在其所在地区的防御中算作 1 个种族代币（从而保护带有营地的单个种族代币免受巫师种族能力的影响）。",
    "Multiple Encampments may be placed in the same Region to obtain a higher defense bonus.": "可以在同一地区放置多个营地以获得更高的防御加成。",
    "At the end of your turn, place each of your 2 Heroes in 2 different Regions you occupy. These 2 Regions are now immune to enemy conquests and to their racial and special powers, until your Heroes move.": "在回合结束时，将你的 2 个英雄放置在你占据的 2 个不同地区。这 2 个地区现在免疫敌人的征服以及他们的种族和特殊能力，直到你的英雄移动。",
    "The Heroes disappear when you go into Decline.": "英雄在你进入衰落时消失。",
    "At the end of your turn, you receive 1 Fireball marker for each Magic Source you occupy. The Fireballs count as 2 Race tokens, but may only be used during an attack in one of your following turns. They are discarded once used.": "在回合结束时，你占据的每个魔法源获得 1 个火球标记。火球算作 2 个种族代币，但只能在你后续回合的攻击中使用。使用后即丢弃。",
    "Several Fireballs may be used to conquer a single Region. You still need a minimum of 1 Race token to occupy the Region.": "可以使用多个火球征服一个地区。你仍需至少 1 个种族代币来占据该地区。",
    "Once per turn, you may conquer a Region using a single Race token, regardless of the number of enemy tokens defending it. To do so, simply drag-and-drop the Dragon from your hand onto the region you want to conquer.": "每回合一次，你可以使用单个种族代币征服一个地区，无论防守该地区的敌人士币有多少。要这样做，只需将手牌中的龙拖放到你想征服的地区上。",
    "The conquered Region is now immune to enemy conquests and to their racial and special powers until your Dragon moves.": "被征服的地区现在免疫敌人的征服以及他们的种族和特殊能力，直到你的龙移动。",
    "During each new turn, you may move your Dragon to a different Region you wish to conquer. Your Dragon disappears when you go into Decline.": "在每个新回合中，你可以将龙移动到你想征服的另一个地区。龙在你进入衰落时消失。",
    "You may use your 2 Hordes of tokens exactly as if they were additional active Race tokens of your own Race. They disappear when you go In Decline, however.": "你可以使用你的 2 个成群代币，就好像它们是你自己种族的额外活跃种族代币一样。但它们在你进入衰落时消失。",
    "When the Marauder appears floating over your troops, excess troops from your first wave of conquests automatically go back in your hand, letting you play through a second wave of conquests - before your final conquest attempt, if any.": "当劫掠者出现在你的部队上方时，你第一波征服中多余的部队自动回到手牌，让你进行第二波征服——在你最后的征服尝试之前（如果有的话）。",
    "Randomly select and place 1 Loot marker face down in each Region you conquer.": "随机选择并在你征服的每个地区面朝下放置 1 个战利品标记。",
    "If you abandon a Region, leave the Loot token behind. When you go in Decline, or at the end of your last turn if you didn't go in Decline, reveal all Loot tokens in your regions and collect them.": "如果你放弃一个地区，留下战利品代币。当你进入衰落时，或者如果你没有进入衰落则在最后一回合结束时，揭开你地区中的所有战利品标记并收集它们。",
    "You may look at it only after you have selected it and placed it on the board. When an opponent conquers one of your regions, reveal the Loot marker.": "你只能在选择并将其放置到棋盘上后查看它。当对手征服你的一个地区时，揭开战利品标记。",
    "You may use the Reinforcement die before each of your conquests, rather than just the last one. Roll the die first; select the Region you wish to conquer; the number of Race tokens required to conquer this region will automatically adjust, based on your die roll.": "你可以在每次征服前使用强化骰，而不仅仅是最后一次。先掷骰；选择你想征服的地区；征服该地区所需的种族代币数量将根据你的掷骰结果自动调整。",
    "You must pay 3 Victory coins, not 1, to skip the Race that is Cursed when selecting a Race and Special Power combo. Cursed gives no additional Special Power.": "选择种族和特殊能力组合时，你必须支付 3 枚胜利金币而不是 1 枚来跳过被诅咒的种族。诅咒不提供额外的特殊能力。",
    "At the beginning of each of your turns, you may place the Copycat marker on one of the six Powers from the combo list next to the board.": "在每回合开始时，你可以将模仿者标记放置在棋盘旁边组合列表中的六个能力之一上。",
    "Your active Race benefits from this Power's effect until the beginning of your next turn, or until an opponent chooses it as his combo. When a Power's effect stops, you lose all these Special Power tokens.": "你的活跃种族从此能力的效果中受益，直到下一回合开始，或直到对手选择它作为其组合。当能力效果停止时，你失去所有这些特殊能力代币。",
    "For each Region in excess of 3 which your Imperial troops occupy at the end of your turn, collect 1 bonus coin. (i.e., if your Imperial troops occupy 5 regions at turn's end, you receive 2 bonus coins.)": "你的帝国部队在回合结束时占据的地区超过 3 个时，每超出 1 个收集 1 枚额外金币。（即，如果你的帝国部队在回合结束时占据 5 个地区，你获得 2 枚额外金币。）",
    "Each time you successfully conquer a Region containing an opponent's active Race token, you immediately receive 1 Victory coin from that player's Coins stash (unless he has no coins left).": "每次你成功征服包含对手活跃种族代币的地区时，你立即从该玩家的金币储备中获得 1 枚胜利金币（除非他没有金币了）。",
    "Each time you conquer a region, you may spend 1 Victory coin to reduce the number of tokens you need to conquer the region by 2 tokens. To do so, simply drag-and-drop the sword icon from your hand onto the region you wish to conquer.": "每次你征服一个地区时，你可以花费 1 枚胜利金币将征服该地区所需的代币数量减少 2 个。要这样做，只需将手牌中的剑图标拖放到你想征服的地区上。",
    "You cannot spend more than 1 Victory coin per Conquest to increase your Mercenary bonus.": "每次征服你不能花费超过 1 枚胜利金币来增加雇佣兵加成。",
    "If you use Mercenary during your final conquest attempt, you may decide to do so after you roll your reinforcement die. A minimum of 1 token is still required to occupy the region.": "如果你在最后的征服尝试中使用雇佣兵，你可以在掷强化骰后决定这样做。仍需至少 1 个代币来占据该地区。",
    "Your 2 Behemoths behave like stacks of tokens matching the number of Swamp regions you occupy, for attack AND for defense. The number of tokens in each Behemoth is adjusted each time you capture or lose a Swamp region.": "你的 2 个巨兽在攻击和防御时都表现为与你占据的沼泽地区数量相匹配的代币堆。每次你占领或失去一个沼泽地区时，每个巨兽中的代币数量都会调整。",
    "A Behemoth must always be accompanied by at least one Race token. If the region it occupies is conquered, only the accompanying Race token is lost; redeploy your Behemoth at the end of your attacker's turn, as normal.": "巨兽必须始终伴随至少 1 个种族代币。如果它占据的地区被征服，只有伴随的种族代币损失；像平常一样在攻击者回合结束时重新部署你的巨兽。",
    "At the end of your turn, for each Mountain Region you occupy, you may place 1 Lava Token in any Region adjacent to that Mountain Region (excluding Regions protected by Special and Racial Powers).": "在回合结束时，你占据的每个山脉地区可以放置 1 个熔岩代币在与该山脉地区相邻的任何地区（不包括受特殊和种族能力保护的地区）。",
    "The Region may not be entered by any other player until after the beginning of your next turn. At the beginning of your next turn, remove all Lava Tokens from the board and proceed as usual.": "在下一回合开始之前，任何其他玩家都不能进入该地区。在下一回合开始时，从棋盘上移除所有熔岩代币并照常进行。",
    "When your Soul-Touch Race goes In Decline, it automatically revives your In-Decline Race. Instead of picking a new Race on your next turn you activate your previous In Decline Race.": "当你的灵魂触摸种族进入衰落时，它自动复活你衰落中的种族。你不需要在下一回合选择新种族，而是激活你之前衰落的种族。",
    "You may keep the tokens that In Decline Race already had on the board, flipping them back to their Active side; or take them back in your hand if you like. You get the rest (if any) of the Race tokens (and Markers, if any) you would receive if this was a new combo pick, and immediately play a full turn with them.": "你可以保留衰落种族已在棋盘上的代币，将它们翻回活跃面；或者如果你愿意，将它们收回手牌。你获得如果这是一个新组合选择时会收到的其余种族代币（和标记，如果有的话），并立即用它们进行完整的一回合。",
    "Tokens In Decline are not impacted (so Ghouls In Decline are immune to this power and may still attack you).": "衰落中的代币不受影响（因此衰落中的食尸鬼对此能力免疫，仍可攻击你）。",
    "You cannot ransack In-Decline Ghouls.": "你不能洗劫衰落中的食尸鬼。",
    "You have no love for In Decline Ghouls though, and may attack them without forfeiting your Peace-loving bonus.": "你对衰落中的食尸鬼没有好感，可以攻击它们而不失去和平主义加成。",
    "At the end of your turn, before you click on Done, you may select one opponent whose Active race you did not attack this turn and choose to make peace with her. To do so, drag-and-drop the Dove icon from your hand onto that player's avatar.": "在回合结束时，点击完成之前，你可以选择一个本回合你没有攻击其活跃种族的对手并选择与她和解。要这样做，将手牌中的鸽子图标拖放到该玩家的头像上。",
    "That player is now at peace with you and cannot attack your active race during her turn. You may make peace with a different opponent each turn, or stay at peace with the same one.": "该玩家现在与你和解，在她的回合中不能攻击你的活跃种族。你可以每回合与不同的对手和解，或与同一对手保持和解。",
    "Your Special Power has no effect during the day (odd numbered game turn).": "你的特殊能力在白天（奇数游戏回合）没有效果。",
    "Each night (even numbered game turn), you may conquer all Regions with 2 less Race tokens than normal. A minimum of 1 token is still required.": "每个夜晚（偶数游戏回合），你可以征服所有地区，所需种族代币比正常少 2 个。仍需至少 1 个代币。",
    "Once per turn, as long as your Fortified Race is active, you may place 1 Fortress in a Region you occupy. The Fortress is worth 1 bonus Victory coin at turn's end, unless you are In Decline. The Fortress also augments your Region's defense by 1, even if you are In Decline.": "每回合一次，只要你的筑城种族活跃，你可以在你占据的地区放置 1 个堡垒。堡垒在回合结束时价值 1 枚额外胜利金币，除非你处于衰落中。堡垒还使你地区的防御 +1，即使你处于衰落中。",
    "The Fortress goes back in your hand if you abandon the Region or when an enemy conquers it. There can only ever be a maximum of 1 Fortress per Region, and a maximum of 6 Fortresses on the map.": "如果你放弃该地区或敌人征服它，堡垒回到你的手牌。每个地区最多只能有 1 个堡垒，地图上最多有 6 个堡垒。",
    "You keep these Regions even once you go into Decline, and continue scoring for them for as long as you have tokens there.": "即使你进入衰落，你仍保留这些地区，并只要你在那里有代币就继续为它们计分。",
    "A Winter marker permanently augments the Region's defense by 1.": "冬季标记永久使该地区的防御 +1。",
    "No Race benefit; their sheer number is enough!": "无种族优势；它们纯粹的数量就足够了！",
    "If you've entirely wiped a player's Race off the map during your turn, that Race can't re-enter the map until the start of that player's next turn.": "如果你在回合中将某个玩家的种族从地图上完全消灭，该种族要到该玩家下一回合开始才能重新进入地图。",
    "During Troop Redeployment, collect 1 new Race token for each active region you conquered this turn. Your victims also receive 1 new Race token for each of their regions you conquered.": "在部队重新部署期间，你本回合征服的每个活跃地区收集 1 个新种族代币。你的受害者也为你征服的每个他们的地区获得 1 个新种族代币。",
    "These conquests must be done at the start of your turn, before any conquest by your Active race. And you may attack your own currently Active race with your In Decline Ghouls, if you wish.": "这些征服必须在回合开始时进行，在你的活跃种族进行任何征服之前。如果你愿意，你可以用衰落中的食尸鬼攻击你自己当前活跃的种族。",
    # Rules
    "The various type of denizens inhabiting Small World. Each Race has its own unique banner, set of tokens and minor rules change(s) which usually benefits its owner.": "居住在小小世界的各种居民类型。每个种族都有自己独特的旗帜、代币套装和通常有利于其拥有者的轻微规则变更。",
    "Each Special Power slightly changes some of the game's rules, usually to its owner's benefit. Special Powers are randomly paired with Races at game start, making each game unique.": "每个特殊能力都会略微改变游戏的某些规则，通常有利于其拥有者。特殊能力在游戏开始时与种族随机配对，使每场游戏都独一无二。",
    "Note that some Special Powers only apply on a given turn (for instance \"Wealthy\" only works on your first turn, \"Stout\" only works if you go into Decline, etc.).": "请注意，某些特殊能力仅在特定回合生效（例如\"富豪\"仅在你的第一回合生效，\"坚韧\"仅在你进入衰落时生效等）。",
    "For more details on a specific Race, check its entry in the Small World Compendium.": "有关特定种族的更多详细信息，请查看小小世界规则书中的条目。",
    "For more details on a specific Special Power, check its entry in the Small World Compendium.": "有关特定特殊能力的更多详细信息，请查看小小世界规则书中的条目。",
    "For more details on a specific Region type, check its entry in the Small World Compendium.": "有关特定地区类型的更多详细信息，请查看小小世界规则书中的条目。",
    "A combo is the combination of 1": "组合是 1 个",
    "Together, these banners define the powers and rules changes a player can use to her advantage when playing this Race's": "这些旗帜共同定义了玩家在使用此种族时可以利用的能力和规则变更",
    "banners, taken by the player when picking a new Race.": "旗帜，由玩家在选择新种族时获取。",
    "The number of Race Tokens a player receives varies based on the sum of the 2 white numbers in orange circles for that Race & Special Power combo.": "玩家获得的种族代币数量根据该种族与特殊能力组合中橙色圆圈内 2 个白色数字之和而变化。",
    "The one at the top is free": "最上面的一个是免费的",
    "All other Combos automatically cost 1": "所有其他组合自动花费 1",
    "for each skipped Combo above them": "每跳过上面的一个组合",
    "If you pick a Combo with Coins on it, you automatically gain these coins.": "如果你选择一个带有金币的组合，你自动获得这些金币。",
    "To conquer a": "要征服一个",
    "Region, drag a": "地区，将",
    "from the bottom of the screen onto the Region you wish to conquer.": "从屏幕底部拖放到你想征服的地区上。",
    "When moving Race Tokens onto it, the Region's borders turn": "将种族代币移到其上时，地区的边界变为",
    "if the Region can be conquered; and": "如果该地区可以被征服；以及",
    "or": "或",
    "if the Region is highlighted in Red, you can't conquer it.": "如果地区以红色高亮，你不能征服它。",
    "if the Region is highlighted in Green, you may conquer it.": "如果地区以绿色高亮，你可以征服它。",
    "Drop your Race Token over the Region; the game will automatically stack together the number of tokens required to conquer it.": "将你的种族代币放到地区上；游戏会自动堆叠征服该地区所需的代币数量。",
    "The tokens dropped will stay in the Region until the end of your turn, at which point you may": "放下的代币将留在该地区，直到你的回合结束，届时你可以",
    "some of them into other Regions you occupy.": "其中一些到你占据的其他地区。",
    "The usual cost to conquer a Region is 2 Race Tokens + 1 additional token for each": "征服一个地区的通常成本是 2 个种族代币 + 每个额外 1 个代币",
    "(Lost Tribe, other player's Race Tokens, Mountain, etc.) in the Region.": "（失落部落、其他玩家的种族代币、山脉等）在该地区中。",
    "They either increase the cost of Conquering the Region by 1 Race Token each:": "它们每个都使征服该地区的成本增加 1 个种族代币：",
    "Dragons and some other characters make a Region immune to attack; etc.": "龙和其他一些角色使地区免疫攻击；等。",
    "Or make that Region immune to opponents' conquests and racial & special powers:": "或使该地区对对手的征服和种族与特殊能力免疫：",
    "On the last conquest of your turn, if you are short of tokens to conquer a Region, a": "在你回合的最后一次征服中，如果你缺少代币来征服一个地区，一个",
    "may appear in the corner of your Race Token, indicating how many pips you will need to roll to successfully conquer this Region.": "可能出现在你的种族代币角落，指示你需要掷出多少点数才能成功征服该地区。",
    "The Small World Conquest Die has 3 blank sides and a 1- , 2- and 3-pips sides, so don't be surprised if your attempt fails!": "小小世界征服骰有 3 个空白面和 1、2、3 点面，所以如果你的尝试失败不要惊讶！",
    "If you do not have enough tokens left, this is your final conquest attempt for the turn. As usual, a minimum of 1 token is still required to attempt any conquest.": "如果你没有足够的代币了，这是你本回合最后的征服尝试。像往常一样，仍需至少 1 个代币来尝试任何征服。",
    "At the end of your turn, you receive 1": "在你的回合结束时，你获得 1",
    "for each": "每个",
    "you occupy at the end of a": "你在结束时占据的",
    "turn.": "回合。",
    "You may also collect additional coins as a result of your": "你也可能因你的",
    "benefits.": "而获得额外金币。",
    "Players scores are kept secret and hidden from other players until the end of the game, when the player with the most Coins is declared the winner.": "玩家分数保密并对其他玩家隐藏，直到游戏结束时金币最多的玩家被宣布为获胜者。",
    "At the end of the game, the player with the most Coins wins.": "游戏结束时，金币最多的玩家获胜。",
    "Each player starts the game with 5 Coins.": "每位玩家以 5 枚金币开始游戏。",
    "You score Coins each time your": "你每次得分金币当你的",
    "You spend Coins each time you skip a": "你每次花费金币当你跳过一个",
    "you wish to skip": "你想跳过的",
    "paid for": "支付",
    "x6": "x6",
    "x10": "x10",
    "This gives you a chance to reorganize your tokens, bolstering the defenses of some": "这让你有机会重新组织代币，加强一些的防御",
    "at the expense of others; you must always keep at least 1 Race Token in each Region you conquered, however.": "以牺牲其他地区为代价；但你必须始终在你征服的每个地区保留至少 1 个种族代币。",
    "You may rearrange your": "你可以重新安排你的",
    "over a": "在一个",
    "occupy a": "占据一个",
    "occupy, even if your tokens are": "占据，即使你的代币",
    "When this occurs, you will usually lose your Combo's benefits, but your now inactive Race Tokens remain on the map and continue scoring; and you will be able to Pick a new Combo at the start of your next turn.": "发生这种情况时，你通常会失去组合的优势，但你现在不活跃的种族代币留在地图上并继续计分；你将能在下一回合开始时选择新组合。",
    "After a few turns of conquests, your": "经过几回合的征服后，你的",
    "will usually find itself over-extended and little capable of defending itself from others, or conquering more": "通常会发现自己过度扩张，几乎无法防御他人，或征服更多",
    ". When this occurs, you may want to consider going In Decline by pressing this icon at the start of your turn.": "。发生这种情况时，你可能想考虑在回合开始时按此图标进入衰落。",
    "Doing so will automatically flip your": "这样做会自动将你的",
    "upside down, and discard all your Race Tokens, except 1 in each region, onto their In Decline side.": "翻面，并丢弃你所有的种族代币，除了每个地区留 1 个，翻到衰落面。",
    "You may only have a single Race In Decline at any time. If another of your Races goes In Decline, the previous one immediately vanishes from the map.": "你在任何时候只能有一个衰落种族。如果你的另一个种族进入衰落，前一个立即从地图上消失。",
    "All tokens in this Region are taken in hand by the defeated player and treated as if the Region were conquered (except there is no loss of tokens).": "该地区中的所有代币被战败玩家收回手中，视为该地区被征服（除了没有代币损失）。",
    "Although rarely recommended, you may abandon a Region at the start of your turn, by dragging your Race Tokens out and back onto your tokens' reserve.": "虽然很少推荐，但你可以在回合开始时放弃一个地区，将你的种族代币拖出并放回代币储备区。",
    "1 Victory Coin is placed in each Region that you abandon at the beginning of your turn. You cannot conquer these Regions again this turn, but you receive the coins they hold as a bonus at turn's end.": "在你回合开始时放弃的每个地区放置 1 枚胜利金币。你本回合不能再次征服这些地区，但你在回合结束时获得它们持有的金币作为奖励。",
    "If another player was present in a Region you conquered, he automatically loses 1 of his Race Tokens. Any other tokens in that Region automatically go back to his reserve, from where they may be redeployed at the end of your turn.": "如果另一个玩家在你征服的地区中，他自动失去 1 个种族代币。该地区中的任何其他代币自动回到他的储备区，从那里可以在你回合结束时重新部署。",
    "In 3 to 5 player games, if some players have seen their Regions conquered, they may redeploy the troops that occupied these regions (minus any losses) onto other Regions where they still have troops, if possible.": "在 3 到 5 人游戏中，如果一些玩家的地区被征服，他们可以将占据这些地区的部队（减去任何损失）重新部署到他们仍有部队的其他地区，如果可能的话。",
    "Tokens of a same Race get stacked together to conquer": "同一种族的代币堆叠在一起以征服",
    "enough Race Tokens": "足够的种族代币",
    "left to conquer that Region.": "来征服该地区。",
    "The currency that is:": "货币是：",
    "used to keep track of the players'": "用于跟踪玩家的",
    "Small World contains numerous game Markers.": "小小世界包含众多游戏标记。",
    "An area of the Small World map, delimited with a white border.": "小小世界地图上以白色边界划定的区域。",
    "On the map, each token's owner is identified by a small colored strip in its corner, matching the color of that owner's avatar.": "在地图上，每个代币的所有者通过其角落的小色条识别，与该所有者头像的颜色匹配。",
    "When first entering the board, usually only border regions are accessible": "首次进入棋盘时，通常只有边境地区可进入",
    "Either because you're not allowed to:": "要么因为你不被允许：",
    "Or because:": "要么因为：",
    # Guides
    "After connecting with your Days of Wonder account, you get a screen divided in 3 parts. From left to right:": "连接你的 Days of Wonder 账号后，你会看到一个分为 3 部分的屏幕。从左到右：",
    "There you will find:": "在那里你会发现：",
    "By default, you are presented with the list of open games. Each game contains a number of icons giving details about that game.": "默认情况下，你会看到开放游戏列表。每场游戏包含多个图标，提供有关该游戏的详细信息。",
    "Select a game to see the players who've already joined it. Push on Join to enter this game.": "选择一个游戏查看已加入的玩家。点击加入进入此游戏。",
    "You can also create a game of your own, with the settings of your choice, and wait for others to join it.": "你也可以创建自己的游戏，使用你选择的设置，并等待其他人加入。",
    "There are 2 different types of online games you can play: Single Session games and Multi Session games.": "你可以玩 2 种不同类型的在线游戏：单场游戏和多场游戏。",
    "By definition you can only ever play ONE Single Session game at a time.": "根据定义，你一次只能玩一场单场游戏。",
    "game is meant to be played in a single real-time session, without anyone leaving the game at anytime (even just to check e-mail!).": "游戏意在单一实时会话中进行，任何人都不能在任何时候离开游戏（即使只是查看电子邮件！）。",
    "If you voluntarily quit a Single Session game mid-way, you will automatically lose. A bot will take your place so that others can still finish their game.": "如果你中途主动退出单场游戏，你将自动失败。机器人将取代你的位置，以便其他人仍能完成游戏。",
    "game is played asynchronously: it can be \"paused\" and is usually played over a longer period of time.": "游戏是异步进行的：它可以被\"暂停\"，通常在较长时间内进行。",
    "You can play several Multi Session games in parallel, playing one turn in one game, switching to another game to play 1 turn then, going out to check e-mails, etc. No bot will take over in your place unless your": "你可以同时玩多场多场游戏，在一场游戏中玩一回合，切换到另一场游戏玩 1 回合，然后出去查看电子邮件等。除非你的，否则不会有机器人取代你",
    "Whether the game is": "游戏是否",
    "ranked or not": "计入排名",
    "is activated or not.": "是否激活。",
    "Whether": "是否",
    "Otherwise, the opponent collects the Loot token.": "否则，对手收集战利品代币。",
    "You don't have": "你没有",
    "Whether the game is Private or Public. Private games require a password.": "游戏是私人还是公开。私人游戏需要密码。",
    "If you create a Private game, give it a password and make sure to communicate it to others, or they won't be able to join in!": "如果你创建私人游戏，给它设置密码并确保告知他人，否则他们将无法加入！",
    "Type of game:": "游戏类型：",
    "You can log in using your Days of Wonder (\"DoW\") account from this screen. The Login Settings button will allow you to perform more sophisticated actions, such as linking your DoW account to your Game Center account, switching to another DoW account, and even managing your DoW account profile directly on the Web! Check it out if you would like to choose a better-sounding Login Name, change your password, or pick up an Avatar.": "你可以从此屏幕使用你的 Days of Wonder（\"DoW\"）账号登录。登录设置按钮允许你执行更复杂的操作，例如将你的 DoW 账号关联到 Game Center 账号，切换到另一个 DoW 账号，甚至直接在网上管理你的 DoW 账号资料！如果你想选择一个更好听的登录名、更改密码或选择头像，请查看它。",
    "You can change your preferred color by tapping on the banner at the top of the screen.": "你可以通过点击屏幕顶部的旗帜来更改你偏好的颜色。",
    "In Solo, Face-to-Face and Pass-and-Play, you can select the starting player by tapping on the race flag. Use the ? icon to set the starting player randomly.": "在单人、面对面和传玩模式中，你可以通过点击种族旗帜来选择先手玩家。使用 ? 图标随机设置先手玩家。",
    "In Solo, Face-to-Face, Pass-and-Play and Local Game, you can change the names of human players by tapping on them and typing a new name.": "在单人、面对面、传玩和本地游戏中，你可以通过点击人类玩家并输入新名称来更改他们的名字。",
    "In Pass-and-Play games, you can play with a mix of bots and real players. Tap repeatedly on a slot to cycle through the 3 possible settings (bot, human player, no player).": "在传玩游戏中，你可以混合使用机器人和真实玩家。反复点击一个槽位以在 3 种可能的设置之间循环（机器人、人类玩家、无玩家）。",
    "To manage Buddies in your Days of Wonder account, and invite them to a game, visit the Invite Buddies screen.": "要管理你的 Days of Wonder 账号中的好友并邀请他们加入游戏，请访问邀请好友屏幕。",
    "To send an invitation to some buddies, select them in your Buddy List to the left and add them to the game you want them to join. Choose the game's parameters and push the Invite button. You can check the status of your invitation in the \"Games in Progress\" screen. Same thing for games to which you were invited.": "要向一些好友发送邀请，在左侧好友列表中选择他们并将他们添加到你想让他们加入的游戏中。选择游戏参数并点击邀请按钮。你可以在\"进行中的游戏\"屏幕中查看邀请状态。你被邀请的游戏也是如此。",
    "In your Buddy List, friends who already own Small World 2 will have a \"SW\" icon next to their name. You can also send a Private Message to those friends of yours who don't own the game yet. They will be able to read their Private Messages directly on the Days of Wonder Web site.": "在你的好友列表中，已拥有小小世界 2 的朋友名字旁边会有\"SW\"图标。你也可以向那些还没有游戏的朋友发送私人消息。他们将能够直接在 Days of Wonder 网站上阅读他们的私人消息。",
    "You can add players to your Buddy List by reviewing the list of recent opponents, by performing a search in the Days of Wonder database, or by looking up your Game Center friends (iPad version only).": "你可以通过查看近期对手列表、在 Days of Wonder 数据库中搜索或查找你的 Game Center 好友（仅限 iPad 版本）将玩家添加到好友列表。",
    "If you don't remember or like typing the DoW Login Names of other players, you can do it from the Web! Go to": "如果你不记得或不喜欢输入其他玩家的 DoW 登录名，你可以从网上操作！前往",
    "www.daysofwonder.com/mybuddies": "www.daysofwonder.com/mybuddies",
    "and add the names of your buddies from there.": "并从那里添加你好友的名字。",
    "You don't have": "你没有",
    "Karma is represented by 1 to 5 dots (from worse to best) located to the right of a player' banner. The number located below the Karma dots is that player's Ranking Score.": "因果值由 1 到 5 个点（从差到好）表示，位于玩家旗帜右侧。因果点下方的数字是该玩家的排名分数。",
    "is a system designed to encourage proper (and discourage improper) behavior when playing with others.": "是一个旨在鼓励与他人游戏时正确（并阻止不当）行为的系统。",
    "As a new player, you start with 50 Karma points (2.5 dots). When you play an online game to its completion, you earn 1 additional Karma point (up to a maximum of 100). When you abandon a game in mid-play, before its normal completion, you lose 5 points.": "作为新玩家，你以 50 点因果值（2.5 个点）开始。当你完成一场在线游戏时，你获得 1 点额外因果值（最多 100 点）。当你在游戏正常完成前中途放弃游戏时，你失去 5 点。",
    "are games in which the ranking option was turned ON when the game was created. Our ranking is based on the same classic ELO system used in international Chess tournaments.": "是创建游戏时排名选项已开启的游戏。我们的排名基于国际象棋比赛中使用的相同经典 ELO 系统。",
    "Each player's Player Clock automatically starts counting down when it's that player turn to play and pauses as soon as that player's done with their turn, just like a player's clock in a game of speed Chess.": "每位玩家的玩家时钟在轮到该玩家游戏时自动开始倒计时，并在该玩家完成回合时立即暂停，就像国际象棋比赛中的玩家时钟一样。",
    "for each player. These Player Clocks control how much time each player has to play": "为每位玩家。这些玩家时钟控制每位玩家有多少时间来玩",
    "the entire game": "整场游戏",
    "If you don't play your turn within your allotted": "如果你未在分配的",
    "time limit, or if you abandon a game before it finishes, you automatically lose the game and your ranking will be impacted.": "时间限制内玩你的回合，或者如果你在游戏结束前放弃游戏，你将自动输掉游戏，你的排名将受到影响。",
    "If a player runs out of time, he/she automatically loses that game; a bot takes over for him/her so that others with time left on their clock can still finish the game if they wish.": "如果玩家时间用完，他/她自动输掉该游戏；机器人取代他/她，以便其他时钟上还有时间的玩家仍能完成游戏（如果他们愿意）。",
    "(time allocated to each player for the entire duration of the game).": "（分配给每位玩家完成整场游戏的时间）。",
    "runs out!": "用完！",
    "page. Note that you can set a custom value for the Player Clock instead of using the proposed presets by clicking on the third button.": "页面。请注意，你可以通过点击第三个按钮来设置玩家时钟的自定义值，而不是使用建议的预设值。",
    "The Online Arena is the area where you create or join online games against other players.": "在线竞技场是你创建或加入与其他玩家对战的在线游戏的区域。",
    "visually tells you whether that player is in your game or not: when you see a little": "直观地告诉你该玩家是否在你的游戏中：当你看到一个小",
    "light just under his Avatar, that player is currently in that very same game you are currently in. When his light is": "灯在他的头像下方，该玩家当前就在你当前所在的同一场游戏中。当他的灯是",
    "instead, he is currently connected, but in some other part of the application: playing another online game, looking at his Buddy List, waiting in the Online Arena, etc. Finally, when his light is": "时，他当前已连接，但在应用的其他部分：玩另一场在线游戏、查看好友列表、在在线竞技场等待等。最后，当他的灯是",
    "dimmed": "暗淡",
    ", that player is currently off-line.": "时，该玩家当前离线。",
    "currently connected and waiting to play. Clicking on a name reveals details about that player:": "当前连接并等待游戏。点击一个名字可显示该玩家的详细信息：",
    "list of players": "玩家列表",
    ", listing the games you can join or create.": "，列出你可以加入或创建的游戏。",
    "join/create panel": "加入/创建面板",
    "chat area": "聊天区域",
    ", to type messages and discuss with others. Even though Small World can be ruthless at times, please keep a moderate tone, and make Fair Play your first goal; we want everyone to have fun!": "，输入消息并与他人讨论。尽管小小世界有时可能很残酷，请保持温和的语气，把公平竞争作为你的首要目标；我们希望每个人都能玩得开心！",
    "When in game, any discussion you are having is private and limited to the sole players in that game; whereas discussions in the": "在游戏中，你进行的任何讨论都是私人的，仅限于该游戏中的玩家；而在",
    "chat area": "聊天区域",
    " are public and visible to everyone.": "中的讨论是公开的，对所有人可见。",
    "Though Small World can be ruthless at times, please remember to keep a friendly behavior and moderate tone. Fair play and friendliness are the rules; please make sure you follow this spirit and keep the game enjoyable for everyone!": "尽管小小世界有时可能很残酷，请记住保持友好的行为和温和的语气。公平竞争和友好是规则；请确保你遵循这种精神，让每个人都能享受游戏！",
    "? While in-game, tap on the little balloon next to your Avatar and type your message. To see an earlier discussion, simply open the Chat History panel (when allowed to). Doing so will also let you to insert some cool animated \"emoticons\" in front of your messages - just don't abuse these, even if they're fun!": "？在游戏中，点击头像旁边的小气球并输入你的消息。要查看之前的讨论，只需打开聊天记录面板（在允许的情况下）。这样做还可以让你在消息前插入一些酷炫的动画\"表情\"——只是不要滥用，即使它们很有趣！",
    "Check out the combo of your opponents by tapping on the \"+\" located to the right side of their banners. Grayed out banners correspond to races in Decline.": "点击对手旗帜右侧的\"+\"查看他们的组合。灰色的旗帜对应衰落中的种族。",
    "Do a single tap on any player's combo to reveal details on the corresponding race and power. Tap on the Compendium icon at the bottom of these pages to display the full Compendium and check other races or powers.": "单击任何玩家的组合以显示相应种族和能力的详细信息。点击这些页面底部的规则书图标以显示完整规则书并查看其他种族或能力。",
    "To see all Regions of the map occupied by a given player's tokens, hold your finger on that player's combo banners. All the regions occupied by this combo will be automatically highlighted. This is especially useful if you are color-blind or playing on a small screen with a large number of players.": "要查看地图上被某个玩家代币占据的所有地区，按住该玩家的组合旗帜。该组合占据的所有地区将自动高亮。如果你是色盲或在小屏幕上与大量玩家游戏，这特别有用。",
    "To check your score, tap on the Gold coin next to your avatar. If you are in a Face-to-Face game, shield that coin with your hand first, to keep it hidden from your opponent.": "要查看你的分数，点击头像旁边的金币。如果你在面对面游戏中，先用手遮住该金币，以防止对手看到。",
    "To check your total number of Coins, at any point during the game, tap on the coin immediately below your avatar. Hide the result with your other hand, if need be.": "要在游戏中的任何时候查看你的金币总数，点击头像正下方的金币。如有需要，用另一只手遮住结果。",
    "At the start of your turn, you can empty some of the regions your tokens occupy by dragging-and-dropping them back into your hand - the wood-grained border where your tokens sit before coming on board.": "在回合开始时，你可以通过拖放将代币放回手牌——木纹边框，即代币在进入棋盘前所在的位置——来清空你代币占据的一些地区。",
    "To speed things up, redeployments are automatic by default; but you can override this choice, in games you create.": "为了加快速度，重新部署默认为自动；但在你创建的游戏中，你可以覆盖此选择。",
    "Automatic Redeployment": "自动重新部署",
    "Be mindful that doing so will add extra back-and-forth turns between the players that must redeploy, slowing your games down. We recommend switching Auto Redeploy OFF only for these ultra-competitive games where you and other players think you must absolutely control the most minute details of every troop redeployment.": "请注意，这样做会在需要重新部署的玩家之间增加额外的往返回合，减慢你的游戏速度。我们建议仅在你和其他玩家认为你必须绝对控制每次部队重新部署的最微小细节的超竞争游戏中关闭自动重新部署。",
    "We did a considerable amount of testing before shipping this game. However, there is always a risk a particular combo doesn't behave has planned or something isn't as clear as it should be.": "我们在发布此游戏前做了大量测试。然而，总有可能某个特定组合的行为不符合计划，或者某些内容不够清晰。",
    "So instead, please take some time to head to our forums on": "所以，请花点时间前往我们的论坛",
    "A forum where thousands of like-minded players gather and discuss the game; many of them know Small World like the back of their hand, are usually happy to answer questions from newbies, and collectively much faster to reply than we could ever hope to be!": "一个成千上万志同道合的玩家聚集讨论游戏的论坛；他们中的许多人对小小世界了如指掌，通常乐于回答新手的问题，而且集体回复速度比我们所能期望的要快得多！",
    "We are open to feedback. However, please be aware that when you post questions in the forms of Reviews on the Apple App Store, we have no way to reply or contact you!": "我们欢迎反馈。但是，请注意，当你在 Apple App Store 以评论形式发布问题时，我们无法回复或联系你！",
    "A Support page in the \"": "一个支持页面在\"",
    " area, where you will find answers to some common questions and where you will be able to report any bona-fide bug that might have escaped our attention.": "\"区域，你可以在那里找到一些常见问题的答案，并能够报告任何可能逃过我们注意的真实错误。",
    "And up-to-the-minute information on all our board games, cardboard and online.": "以及我们所有桌游、纸板和在线游戏的最新信息。",
    "Care to": "想",
    "Contact us": "联系我们",
    "of Small World.": "的小小世界。",
    "The game parameters are the same as described in the": "游戏参数与",
    "During the 1st turn of the game, each player:": "在游戏的第一回合，每位玩家：",
    "In Follow-on turns, each player either:": "在后续回合中，每位玩家要么：",
    "When picking a new": "选择新的",
    ", preparing to pick a new Race": "，准备选择新种族",
    "then": "然后",
    "and": "和",
    "and 1": "和 1",
    "and gained from": "并从",
    "some": "一些",
    "some Coins": "一些金币",
    "of the map your": "你的地图",
    "than your opponents.": "比你的对手。",
    "Your goal is to score more": "你的目标是获得更多",
    "green": "绿色",
    "yellow": "黄色",
    ", etc.": "等。",
    ", you can choose from 6 different Combos:": "，你可以从 6 个不同的组合中选择：",
    ", you can't conquer it.": "，你不能征服它。",
    ", you may conquer it.": "，你可以征服它。",
    "at the end of your turn, by pressing Redeploy.": "在你的回合结束时，按重新部署。",
    "Conquers more Regions": "征服更多地区",
    "www.daysofwonder.com": "www.daysofwonder.com",
    # Fragments split by <a> tags
    "All online games (both": "所有在线游戏（",
    ") rely on a": "）依赖于",
    "used to keep track of the players'": "用于跟踪玩家的",
    ", drag a": "，将",
    "If the Region's border is highlighted in": "如果地区的边界高亮为",
    ", you can't conquer it.": "，你不能征服它。",
    ", when": "，当",
    "When you drag a": "当你拖动一个",
    ", if the Region is highlighted in Green, you may conquer it.": "，如果地区以绿色高亮，你可以征服它。",
    "The": "这",
    "or": "或",
    "then": "然后",
    "and": "和",
    "and 1": "和 1",
    "some": "一些",
    "of the map your": "你的地图",
    "than your opponents.": "比你的对手。",
    "Your goal is to score more": "你的目标是获得更多",
    "for each": "每个",
    "you occupy at the end of a": "你在结束时占据的",
    "turn.": "回合。",
    "You may also collect additional coins as a result of your": "你也可能因你的",
    "benefits.": "而获得额外金币。",
    "You score Coins each time your": "你每次得分金币当你的",
    "You spend Coins each time you skip a": "你每次花费金币当你跳过一个",
    "you wish to skip": "你想跳过的",
    "paid for": "支付",
    "This gives you a chance to reorganize your tokens, bolstering the defenses of some": "这让你有机会重新组织代币，加强一些的防御",
    "at the expense of others; you must always keep at least 1 Race Token in each Region you conquered, however.": "以牺牲其他地区为代价；但你必须始终在你征服的每个地区保留至少 1 个种族代币。",
    "You may rearrange your": "你可以重新安排你的",
    "over a": "在一个",
    "occupy a": "占据一个",
    "occupy, even if your tokens are": "占据，即使你的代币",
    "After a few turns of conquests, your": "经过几回合的征服后，你的",
    "will usually find itself over-extended and little capable of defending itself from others, or conquering more": "通常会发现自己过度扩张，几乎无法防御他人，或征服更多",
    ". When this occurs, you may want to consider going In Decline by pressing this icon at the start of your turn.": "。发生这种情况时，你可能想考虑在回合开始时按此图标进入衰落。",
    "Doing so will automatically flip your": "这样做会自动将你的",
    "upside down, and discard all your Race Tokens, except 1 in each region, onto their In Decline side.": "翻面，并丢弃你所有的种族代币，除了每个地区留 1 个，翻到衰落面。",
    "Tokens of a same Race get stacked together to conquer": "同一种族的代币堆叠在一起以征服",
    "enough Race Tokens": "足够的种族代币",
    "left to conquer that Region.": "来征服该地区。",
    "The currency that is:": "货币是：",
    "at the end of a": "在结束时",
    "Whether": "是否",
    "ranked or not": "计入排名",
    "is activated or not.": "是否激活。",
    "You don't have": "你没有",
    "game, with the": "游戏，带有",
    "from the bottom of the screen onto the Region you wish to conquer.": "从屏幕底部拖放到你想征服的地区上。",
    "When moving Race Tokens onto it, the Region's borders turn": "将种族代币移到其上时，地区的边界变为",
    "if the Region can be conquered; and": "如果该地区可以被征服；以及",
    "A": "一个",
    "may appear in the corner of your Race Token, indicating how many pips you will need to roll to successfully conquer this Region.": "可能出现在你的种族代币角落，指示你需要掷出多少点数才能成功征服该地区。",
    "On the last conquest of your turn, if you are short of tokens to conquer a Region, a": "在你回合的最后一次征服中，如果你缺少代币来征服一个地区，一个",
    "Either because you're not allowed to:": "要么因为你不被允许：",
    "Or because:": "要么因为：",
    "Some": "一些",
    "and gained from": "并从",
    "banners, taken by the player when picking a new Race.": "旗帜，由玩家在选择新种族时获取。",
    "A combo is the combination of 1": "组合是 1 个",
    "The one at the top is free": "最上面的一个是免费的",
    "All other Combos automatically cost 1": "所有其他组合自动花费 1",
    "for each skipped Combo above them": "每跳过上面的一个组合",
    "If you pick a Combo with Coins on it, you automatically gain these coins.": "如果你选择一个带有金币的组合，你自动获得这些金币。",
    "To conquer a": "要征服一个",
    "Region, drag a": "地区，将",
    "The tokens dropped will stay in the Region until the end of your turn, at which point you may": "放下的代币将留在该地区，直到你的回合结束，届时你可以",
    "some of them into other Regions you occupy.": "其中一些到你占据的其他地区。",
    "The usual cost to conquer a Region is 2 Race Tokens + 1 additional token for each": "征服一个地区的通常成本是 2 个种族代币 + 每个额外 1 个代币",
    "(Lost Tribe, other player's Race Tokens, Mountain, etc.) in the Region.": "（失落部落、其他玩家的种族代币、山脉等）在该地区中。",
    "They either increase the cost of Conquering the Region by 1 Race Token each:": "它们每个都使征服该地区的成本增加 1 个种族代币：",
    "Dragons and some other characters make a Region immune to attack; etc.": "龙和其他一些角色使地区免疫攻击；等。",
    "Or make that Region immune to opponents' conquests and racial & special powers:": "或使该地区对对手的征服和种族与特殊能力免疫：",
    "No Race benefit; their sheer number is enough!": "无种族优势；它们纯粹的数量就足够了！",
    "Some of them are:": "其中包括：",
    "Small World contains numerous game Markers.": "小小世界包含众多游戏标记。",
    "An area of the Small World map, delimited with a white border.": "小小世界地图上以白色边界划定的区域。",
    "On the map, each token's owner is identified by a small colored strip in its corner, matching the color of that owner's avatar.": "在地图上，每个代币的所有者通过其角落的小色条识别，与该所有者头像的颜色匹配。",
    "When first entering the board, usually only border regions are accessible": "首次进入棋盘时，通常只有边境地区可进入",
    "Note that some Special Powers only apply on a given turn (for instance \"Wealthy\" only works on your first turn, \"Stout\" only works if you go into Decline, etc.).": "请注意，某些特殊能力仅在特定回合生效（例如\"富豪\"仅在你的第一回合生效，\"坚韧\"仅在你进入衰落时生效等）。",
    "If you've entirely wiped a player's Race off the map during your turn, that Race can't re-enter the map until the start of that player's next turn.": "如果你在回合中将某个玩家的种族从地图上完全消灭，该种族要到该玩家下一回合开始才能重新进入地图。",
    "During Troop Redeployment, collect 1 new Race token for each active region you conquered this turn. Your victims also receive 1 new Race token for each of their regions you conquered.": "在部队重新部署期间，你本回合征服的每个活跃地区收集 1 个新种族代币。你的受害者也为你征服的每个他们的地区获得 1 个新种族代币。",
    "These conquests must be done at the start of your turn, before any conquest by your Active race. And you may attack your own currently Active race with your In Decline Ghouls, if you wish.": "这些征服必须在回合开始时进行，在你的活跃种族进行任何征服之前。如果你愿意，你可以用衰落中的食尸鬼攻击你自己当前活跃的种族。",
    "Skags and Soul-Touch are licenses from Borderlands & Borderlands 2 – © 2009-2017 Gearbox Software, LLC. Borderlands & Borderlands 2 are published by 2K Games, Inc. All trademarks are property of their respective owners. All rights Reserved.": "斯卡斯和灵魂触摸是 Borderlands & Borderlands 2 的许可 – © 2009-2017 Gearbox Software, LLC。Borderlands & Borderlands 2 由 2K Games, Inc. 发行。所有商标均为其各自所有者的财产。保留所有权利。",
    ", if the Region is highlighted in Red, you can't conquer it.": "，如果地区以红色高亮，你不能征服它。",
    "required to join this game.": "需要加入此游戏。",
    "Each player's online": "每位玩家的在线",
    "are public and visible to everyone.": "是公开的，对所有人可见。",
    "otherwise.": "否则。",
    "At the end of each turn, you receive 1": "在每个回合结束时，你获得 1",
    "required to start this game.": "开始此游戏所需。",
    "Number of players": "玩家数量",
    "The Lost Tribes are remnants of long-forgotten civilizations that have fallen into decline but still populate some Regions at game start.": "失落部落是被遗忘已久的文明的残余，它们已经衰落但在游戏开始时仍占据一些地区。",
    ", preparing to pick a new Race": "，准备选择新种族",
    "We did a considerable amount of testing before shipping this game. However, there is always a risk a particular combo doesn't behave has planned or something isn't as clear as it should be.": "我们在发布此游戏前做了大量测试。然而，总有可能某个特定组合的行为不符合计划，或者某些内容不够清晰。",
    " game is played asynchronously: it can be \"paused\" and is usually played over a longer period of time.": "游戏是异步进行的：它可以被\"暂停\"，通常在较长时间内进行。",
    "\" area, where you will find answers to some common questions and where you will be able to report any bona-fide bug that might have escaped our attention.": "\"区域，你可以在那里找到一些常见问题的答案，并能够报告任何可能逃过我们注意的真实错误。",
    "OR": "或",
    ", preparing to pick a new Race\nthen": "，准备选择新种族，然后",
    "game is played asynchronously: it can be \"paused\" and is usually played over a longer period of time.": "游戏是异步进行的：它可以被\"暂停\"，通常在较长时间内进行。",
    "You can play several Multi Session games in parallel, playing one turn in one game, switching to another game to play 1 turn then, going out to check e-mails, etc. No bot will take over in your place unless your ": "你可以同时玩多场多场游戏，在一场游戏中玩一回合，切换到另一场游戏玩 1 回合，然后出去查看电子邮件等。除非你的",
    'game is played asynchronously: it can be "paused" and is usually played over a longer period of time. \n  You can play several Multi Session games in parallel, playing one turn in one game, switching to another game to play 1 turn then, going out to check e-mails, etc. No bot will take over in your place unless your': '游戏是异步进行的：它可以被"暂停"，通常在较长时间内进行。\n  你可以同时玩多场多场游戏，在一场游戏中玩一回合，切换到另一场游戏玩 1 回合，然后出去查看电子邮件等。除非你的',
    "We did a considerable amount of testing before shipping this game. However, there is always a risk a particular combo doesn't  behave has planned or something isn't as clear as it should be.": "我们在发布此游戏前做了大量测试。然而，总有可能某个特定组合的行为不符合计划，或者某些内容不够清晰。",
}


from html.parser import HTMLParser
import io

class _HtmlTranslator(HTMLParser):
    """Parse HTML and translate only text content (not tags/attributes)."""
    def __init__(self, translations):
        super().__init__()
        self.trans = translations
        self.parts = []
        self.skip_tags = {'script', 'style'}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
        # Rebuild the tag with attributes unchanged
        attr_str = ''
        for k, v in attrs:
            if v is None:
                attr_str += f' {k}'
            else:
                attr_str += f' {k}="{v}"'
        self.parts.append(f'<{tag}{attr_str}>')

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1
        self.parts.append(f'</{tag}>')

    def handle_startendtag(self, tag, attrs):
        attr_str = ''
        for k, v in attrs:
            if v is None:
                attr_str += f' {k}'
            else:
                attr_str += f' {k}="{v}"'
        self.parts.append(f'<{tag}{attr_str}/>')

    def handle_data(self, data):
        if self.skip_depth > 0:
            self.parts.append(data)
            return
        # Normalize curly quotes to straight quotes for lookup
        stripped = data.strip()
        normalized = stripped.replace('\u2018', "'").replace('\u2019', "'") \
                             .replace('\u201c', '"').replace('\u201d', '"') \
                             .replace('\u00a0', ' ').replace('\u200b', '')
        if normalized in self.trans:
            leading = data[:len(data) - len(data.lstrip())]
            trailing = data[len(data.rstrip()):]
            self.parts.append(leading + self.trans[normalized] + trailing)
        else:
            self.parts.append(data)

    def get_result(self):
        return ''.join(self.parts)


def translate_html_file(src_path, dst_path):
    """Translate an HTML file from English to Chinese - only text nodes."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change lang attribute and image paths BEFORE parsing (these are attribute values)
    content = content.replace('lang="en"', 'lang="zh"')
    content = content.replace('/en/', '/zh/')
    content = content.replace('/image/mdpi/en/', '/image/mdpi/zh/')

    # Translate only text content via HTML parser
    parser = _HtmlTranslator(TRANS)
    parser.feed(content)
    result = parser.get_result()

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(result)


def main():
    # Translate full version (en -> zh payload)
    en_dir = os.path.join(COMPENDIUM_GAME, "en")
    zh_dir = os.path.join(COMPENDIUM_OUT, "zh")
    count = 0
    for fname in os.listdir(en_dir):
        if not fname.endswith('.html'):
            continue
        translate_html_file(
            os.path.join(en_dir, fname),
            os.path.join(zh_dir, fname))
        count += 1
    print(f"Full version: translated {count} HTML files -> {zh_dir}")

    # Translate short version (en-short -> zh-short)
    en_short_dir = os.path.join(COMPENDIUM_GAME, "en-short")
    zh_short_dir = os.path.join(COMPENDIUM_OUT, "zh-short")
    count = 0
    for fname in os.listdir(en_short_dir):
        if not fname.endswith('.html'):
            continue
        translate_html_file(
            os.path.join(en_short_dir, fname),
            os.path.join(zh_short_dir, fname))
        count += 1
    print(f"Short version: translated {count} HTML files -> {zh_short_dir}")
    print("Done!")


if __name__ == "__main__":
    main()
