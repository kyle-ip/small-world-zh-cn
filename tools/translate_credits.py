# -*- coding: utf-8 -*-
"""Translate credits.html - only headers and role titles, keep names in English."""
import os
from html.parser import HTMLParser

CREDITS_PATH = r"c:\Program Files (x86)\Steam\steamapps\common\SmallWorld2\Resources\credits\credits.html"

CREDITS_TRANS = {
    "Adapted from the original board game": "改编自原版桌游",
    "designed by": "设计师",
    "Development": "开发",
    "Infrastructure": "基础设施",
    "Online Server": "在线服务器",
    "Asmodee.net Web Services": "Asmodee.net 网络服务",
    "Graphics & User Interface": "美术与用户界面",
    "Original Illustrations": "原版插画",
    "Music": "音乐",
    "Sound Effects": "音效",
    "Video Tutorial": "视频教程",
    "Localization Management": "本地化管理",
    "Chief Executive Officer": "首席执行官",
    "Head of Operations": "运营主管",
    "Director of Production": "制作总监",
    "Lead Line Producer": "首席制片",
    "Line Producer": "制片",
    "Accounting": "财务",
    "Office Manager": "办公室经理",
    "Marketing": "市场",
    "Chief Technical Officer": "首席技术官",
    "Head of R&D": "研发主管",
    "Analytics": "数据分析",
    "QA Lead": "质量保证主管",
    "QA Testers": "质量保证测试",
    "Beta Testers": "测试人员",
    "~ iPad ~": "~ iPad ~",
    "~ Android & Windows ~": "~ Android & Windows ~",
    "Kickstarter Backers": "Kickstarter 支持者",
    "Special thanks to our Kickstarter supporters": "特别感谢我们的 Kickstarter 支持者",
    "for your help in making this project a reality!": "感谢你们帮助实现这个项目！",
    '"Spiderines" Supporters': '"蜘蛛"支持者',
    '"Orcs" Supporters': '"兽人"支持者',
    "Graphics &amp; User Interface": "美术与用户界面",
    "~ Android &amp; Windows ~": "~ Android & Windows ~",
}


class CreditsTranslator(HTMLParser):
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
        normalized = stripped.replace('\u2018', "'").replace('\u2019', "'") \
                             .replace('\u201c', '"').replace('\u201d', '"')
        if normalized in CREDITS_TRANS:
            leading = data[:len(data) - len(data.lstrip())]
            trailing = data[len(data.rstrip()):]
            self.parts.append(leading + CREDITS_TRANS[normalized] + trailing)
        else:
            self.parts.append(data)

    def get_result(self):
        return ''.join(self.parts)


def main():
    with open(CREDITS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('lang="en"', 'lang="ja"')

    parser = CreditsTranslator()
    parser.feed(content)
    result = parser.get_result()

    with open(CREDITS_PATH, 'w', encoding='utf-8') as f:
        f.write(result)
    print("credits.html translated")


if __name__ == "__main__":
    main()
