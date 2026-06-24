# -*- coding: utf-8 -*-
import re

f = r"C:\Users\2jordan3\WorkBuddy\2026-06-10-07-46-32\worldcup-v8.html"
with open(f, "r", encoding="utf-8") as fh:
    html = fh.read()

orig = html

# 1. 更新4场比赛比分 (添加 r 字段)
replacements_scores = [
    ('{id:63,g:"K",t:"06-24 01:00",h:"葡萄牙",a:"乌兹别克斯坦",v:"休斯顿NRG球场"},',
     '{id:63,g:"K",t:"06-24 01:00",h:"葡萄牙",a:"乌兹别克斯坦",v:"休斯顿NRG球场",r:"5-0"},'),
    ('{id:64,g:"K",t:"06-24 09:00",h:"哥伦比亚",a:"刚果民主共和国",v:"瓜达拉哈拉阿克伦球场"},',
     '{id:64,g:"K",t:"06-24 09:00",h:"哥伦比亚",a:"刚果民主共和国",v:"瓜达拉哈拉阿克伦球场",r:"1-0"},'),
    ('{id:69,g:"L",t:"06-24 04:00",h:"英格兰",a:"加纳",v:"波士顿吉列球场"},',
     '{id:69,g:"L",t:"06-24 04:00",h:"英格兰",a:"加纳",v:"波士顿吉列球场",r:"0-0"},'),
    ('{id:70,g:"L",t:"06-24 07:00",h:"巴拿马",a:"克罗地亚",v:"多伦多BMO球场"},',
     '{id:70,g:"L",t:"06-24 07:00",h:"巴拿马",a:"克罗地亚",v:"多伦多BMO球场",r:"0-1"},'),
]

for old, new in replacements_scores:
    if old not in html:
        print("WARN: 未找到 -> " + old[:50])
    html = html.replace(old, new)

# 2. 更新穆尼奥斯: g:1,m:1 -> g:2,m:2 (首轮+本轮各1球)
old_munoz = '{r:3,p:"穆尼奥斯",t:"哥伦比亚",g:1,m:1}'
new_munoz = '{r:1,p:"穆尼奥斯",t:"哥伦比亚",g:2,m:2}'
if old_munoz in html:
    html = html.replace(old_munoz, new_munoz)
    print("OK: 穆尼奥斯已更新为2球")
else:
    print("WARN: 穆尼奥斯未找到")

# 3. SCORERS数组: 在结尾 ] 前添加新进球球员
#    找到 SCORERS 数组的结尾 "]\nvar ASSISTS"
new_scorers = """{r:3,p:"萨拉赫",t:"埃及",g:2,m:2},
{r:3,p:"亚马尔",t:"西班牙",g:1,m:2},
{r:3,p:"奥亚萨瓦尔",t:"西班牙",g:2,m:2},
{r:3,p:"哈兰德·彼得森",t:"挪威",g:1,m:2},
{r:3,p:"特雷泽盖",t:"埃及",g:1,m:2},
{r:3,p:"登贝莱",t:"法国",g:1,m:2},
{r:3,p:"萨尔",t:"塞内加尔",g:2,m:2},
{r:1,p:"C罗",t:"葡萄牙",g:2,m:2},
{r:3,p:"门德斯",t:"葡萄牙",g:1,m:2},
{r:3,p:"莱奥",t:"葡萄牙",g:1,m:2},
{r:3,p:"布迪米尔",t:"克罗地亚",g:1,m:2}
]"""

old_scorers_end = """{r:3,p:"萨拉赫",t:"埃及",g:2,m:2},
{r:3,p:"亚马尔",t:"西班牙",g:1,m:2},
{r:3,p:"奥亚萨瓦尔",t:"西班牙",g:2,m:2},
{r:3,p:"哈兰德·彼得森",t:"挪威",g:1,m:2},
{r:3,p:"特雷泽盖",t:"埃及",g:1,m:2},
{r:3,p:"登贝莱",t:"法国",g:1,m:2},
{r:3,p:"萨尔",t:"塞内加尔",g:2,m:2}
]"""

if old_scorers_end in html:
    html = html.replace(old_scorers_end, new_scorers)
    print("OK: SCORERS已添加C罗/门德斯/莱奥/布迪米尔")
else:
    print("WARN: SCORERS结尾未找到")

# 4. ASSISTS数组: 在结尾 ] 前添加新助攻
new_assists_end = """{r:4,p:"托马斯-阿桑特",t:"加纳",a:1,m:1},
{r:4,p:"B费",t:"葡萄牙",a:1,m:2},
{r:4,p:"坎塞洛",t:"葡萄牙",a:1,m:2},
{r:4,p:"金特罗",t:"哥伦比亚",a:1,m:2}
]"""

old_assists_end = """{r:4,p:"托马斯-阿桑特",t:"加纳",a:1,m:1}
]"""

if old_assists_end in html:
    html = html.replace(old_assists_end, new_assists_end)
    print("OK: ASSISTS已添加B费/坎塞洛/金特罗")
else:
    print("WARN: ASSISTS结尾未找到")

# 5. 更新时间戳
html = html.replace("数据更新：2026-06-23 16:35", "数据更新：2026-06-24 14:36")

# 写回文件
with open(f, "w", encoding="utf-8") as fh:
    fh.write(html)

# 统计变更
print("=== 更新完成 ===")
print("比分更新: 4场 (葡萄牙5-0/哥伦比亚1-0/英格兰0-0/巴拿马0-1)")
print("射手榜: C罗2球(新)/门德斯1球/莱奥1球/布迪米尔1球/穆尼奥斯升至2球")
print("助攻榜: B费/坎塞洛/金特罗各1助攻")
print("时间戳: 2026-06-24 14:36")
print("文件大小变化: %d -> %d 字节" % (len(orig), len(html)))
