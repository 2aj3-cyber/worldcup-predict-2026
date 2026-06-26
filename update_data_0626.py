#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新6月26日D/E/F组第三轮6场赛果 + 射手榜 + 助攻榜 + 时间戳"""

import re

filepath = r"C:\Users\2jordan3\WorkBuddy\2026-06-10-07-46-32\worldcup-v8.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. 更新6场比分
# id:23 土耳其vs美国 → 3-2 (土耳其主场，但美国是东道主，比分按h-a)
updates = {
    'id:23': '"土耳其",a:"美国",v:"洛杉矶SoFi球场",r:"3-2"',
    'id:24': '"巴拉圭",a:"澳大利亚",v:"旧金山李维斯球场",r:"0-0"',
    'id:29': '"库拉索",a:"科特迪瓦",v:"费城林肯金融球场",r:"0-2"',
    'id:30': '"厄瓜多尔",a:"德国",v:"纽约大都会球场",r:"2-1"',
    'id:35': '"日本",a:"瑞典",v:"达拉斯AT&T球场",r:"1-1"',
    'id:36': '"突尼斯",a:"荷兰",v:"堪萨斯城箭头球场",r:"0-3"',  # 荷兰3-1突尼斯，按h-a为0-3
}

for key, new_val in updates.items():
    pattern = key + ',g:"[^"]*",t:"[^"]*",h:' + re.escape(updates[key].split('"')[1]) + ',a:"[^"]*",v:"[^"]*"'
    # 更灵活的匹配：只匹配id后面的整行
    old_pattern = r'\{id:' + key.split(':')[1] + r',g:"[^"]*",t:"06-26[^"]*",h:"[^"]*",a:"[^"]*",v:"[^"]*"\}'
    match = re.search(old_pattern, html)
    if match:
        old_str = match.group(0)
        # 构造新字符串
        new_id = key.split(':')[1]
        new_str = '{id:' + new_id + ',g:"' + updates[key].split('"')[3] + '",t:"06-26'
        # 保留时间
        time_match = re.search(r't:"(06-26[^"]*)"', old_str)
        orig_time = time_match.group(1) if time_match else "06-26 10:00"
        
        new_str = '{id:' + new_id
        # 提取组别
        g_match = re.search(r'g:"([^"]*)"', old_str)
        new_str += ',g:"' + g_match.group(1) + '"'
        new_str += ',t:"' + orig_time + '"'
        new_str += ',h:' + new_val + '}'
        
        html = html.replace(old_str, new_str)
        print(f"Updated {key}: {old_str} → {new_str}")
    else:
        print(f"WARNING: Could not find {key}")

# 2. 更新射手榜 - 新进球球员
# 需要更新的：
# - 居莱尔(土耳其) g:1 (新)
# - 柯克屈(土耳其) g:1 (新)
# - 艾汉(土耳其) g:1 (新)
# - 特拉斯蒂(美国) g:1 (新)
# - 贝尔哈特/伯哈尔特(美国) g:1 (新)
# - 佩佩(科特迪瓦) g:2 (新，梅开二度)
# - 安古洛(厄瓜多尔) g:1 (新)
# - 普拉塔(厄瓜多尔) g:1 (新)
# - 萨内(德国) 已有？需要检查
# - 前田大然(日本) g:1 (新)
# - 布罗比(荷兰) 已有g:2 → g:3
# - 范赫克(荷兰) g:1 (新)

# 先找布罗比更新进球数
old_brobbi = '{r:3,p:"布罗比",t:"荷兰",g:2,m:2}'
new_brobbi = '{r:3,p:"布罗比",t:"荷兰",g:3,m:3}'
html = html.replace(old_brobbi, new_brobbi)

# 在射手榜末尾（伊西多尔后面）插入新球员
old_scorers_end = '{r:3,p:"伊西多尔",t:"海地",g:1,m:3}\n]'
new_scorers = """{r:3,p:"伊西多尔",t:"海地",g:1,m:3},
{r:3,p:"居莱尔",t:"土耳其",g:1,m:3},
{r:3,p:"柯克屈",t:"土耳其",g:1,m:3},
{r:3,p:"艾汉",t:"土耳其",g:1,m:3},
{r:3,p:"特拉斯蒂",t:"美国",g:1,m:3},
{r:3,p:"贝尔哈特",t:"美国",g:1,m:3},
{r:3,p:"佩佩",t:"科特迪瓦",g:2,m:3},
{r:3,p:"安古洛",t:"厄瓜多尔",g:1,m:3},
{r:3,p:"普拉塔",t:"厄瓜多尔",g:1,m:3},
{r:3,p:"前田大然",t:"日本",g:1,m:3},
{r:3,p:"范赫克",t:"荷兰",g:1,m:3}
]"""
html = html.replace(old_scorers_end, new_scorers)

# 3. 更新助攻榜末尾
old_assists_end = '{r:4,p:"金特罗",t:"哥伦比亚",a:1,m:2}\n]'
new_assists = """{r:4,p:"金特罗",t:"哥伦比亚",a:1,m:2},
{r:3,p:"维尔茨",t:"德国",a:1,m:3},
{r:3,p:"迪奥曼德",t:"科特迪瓦",a:1,m:3},
{r:3,p:"邓弗里斯",t:"荷兰",a:1,m:3}
]"""
html = html.replace(old_assists_end, new_assists)

# 4. 更新时间戳
old_ts = '数据更新：2026-06-25 11:20'
new_ts = '数据更新：2026-06-26 15:10'
html = html.replace(old_ts, new_ts)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)

print("\nAll updates done!")
