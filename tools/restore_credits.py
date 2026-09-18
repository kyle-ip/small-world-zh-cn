# -*- coding: utf-8 -*-
"""Restore credits.html to English by reversing the translation."""
import os
from html.parser import HTMLParser

CREDITS_PATH = r"c:\Program Files (x86)\Steam\steamapps\common\SmallWorld2\Resources\credits\credits.html"

# Reverse of CREDITS_TRANS: Chinese -> English
ENGLISH_ORIGINAL = {
    "开发": "Development",
    "基础设施": "Infrastructure",
    "在线服务器": "Online Server",
    "Asmodee.net 网络服务": "Asmodee.net Web Services",
    "美术与用户界面": "Graphics & User Interface",
    "原版插画": "Original Illustrations",
    "音乐": "Music",
    "音效": "Sound Effects",
    "视频教程": "Video Tutorial",
    "本地化管理": "Localization Management",
    "首席执行官": "Chief Executive Officer",
    "运营主管": "Head of Operations",
    "制作总监": "Director of Production",
    "首席制片": "Lead Line Producer",
    "制片": "Line Producer",
    "财务": "Accounting",
    "办公室经理": "Office Manager",
    "市场": "Marketing",
    "首席技术官": "Chief Technical Officer",
    "研发主管": "Head of R&D",
    "数据分析": "Analytics",
    "质量保证主管": "QA Lead",
    "质量保证测试": "QA Testers",
    "测试人员": "Beta Testers",
    "Kickstarter 支持者": "Kickstarter Backers",
    "特别感谢我们的 Kickstarter 支持者": "Special thanks to our Kickstarter supporters",
    "感谢你们帮助实现这个项目！": "for your help in making this project a reality!",
    '"蜘蛛"支持者': '"Spiderines" Supporters',
    '"兽人"支持者': '"Orcs" Supporters',
    "改编自原版桌游": "Adapted from the original board game",
    "设计师": "designed by",
}


class CreditsRestorer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_tags = {'script', 'style'}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
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
        stripped = data.strip()
        if stripped in ENGLISH_ORIGINAL:
            leading = data[:len(data) - len(data.lstrip())]
            trailing = data[len(data.rstrip()):]
            self.parts.append(leading + ENGLISH_ORIGINAL[stripped] + trailing)
        else:
            self.parts.append(data)

    def get_result(self):
        return ''.join(self.parts)


def main():
    with open(CREDITS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('lang="ja"', 'lang="en"')

    parser = CreditsRestorer()
    parser.feed(content)
    result = parser.get_result()

    with open(CREDITS_PATH, 'w', encoding='utf-8') as f:
        f.write(result)
    print("credits.html restored to English")


if __name__ == "__main__":
    main()
