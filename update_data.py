import re

with open(r'C:\Users\2jordan3\WorkBuddy\2026-06-10-07-46-32\worldcup-v8.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 更新8场比分
replacements = [
    ('{id:15,g:"C",t:"06-20 09:00",h:"巴西",a:"海地",v:"费城林肯金融球场"}',
     '{id:15,g:"C",t:"06-20 09:00",h:"巴西",a:"海地",v:"费城林肯金融球场",r:"3-0"}'),
    ('{id:16,g:"C",t:"06-20 06:00",h:"苏格兰",a:"摩洛哥",v:"波士顿吉列球场"}',
     '{id:16,g:"C",t:"06-20 06:00",h:"苏格兰",a:"摩洛哥",v:"波士顿吉列球场",r:"0-1"}'),
    ('{id:21,g:"D",t:"06-20 11:00",h:"土耳其",a:"巴拉圭",v:"旧金山李维斯球场"}',
     '{id:21,g:"D",t:"06-20 11:00",h:"土耳其",a:"巴拉圭",v:"旧金山李维斯球场",r:"0-1"}'),
    ('{id:22,g:"D",t:"06-20 03:00",h:"美国",a:"澳大利亚",v:"西雅图Lumen球场"}',
     '{id:22,g:"D",t:"06-20 03:00",h:"美国",a:"澳大利亚",v:"西雅图Lumen球场",r:"2-0"}'),
    ('{id:27,g:"E",t:"06-21 04:00",h:"德国",a:"科特迪瓦",v:"多伦多BMO球场"}',
     '{id:27,g:"E",t:"06-21 04:00",h:"德国",a:"科特迪瓦",v:"多伦多BMO球场",r:"2-1"}'),
    ('{id:28,g:"E",t:"06-21 08:00",h:"厄瓜多尔",a:"库拉索",v:"堪萨斯城箭头球场"}',
     '{id:28,g:"E",t:"06-21 08:00",h:"厄瓜多尔",a:"库拉索",v:"堪萨斯城箭头球场",r:"0-0"}'),
    ('{id:33,g:"F",t:"06-21 01:00",h:"荷兰",a:"瑞典",v:"休斯顿NRG球场"}',
     '{id:33,g:"F",t:"06-21 01:00",h:"荷兰",a:"瑞典",v:"休斯顿NRG球场",r:"5-1"}'),
    ('{id:34,g:"F",t:"06-21 12:00",h:"突尼斯",a:"日本",v:"蒙特雷BBVA球场"}',
     '{id:34,g:"F",t:"06-21 12:00",h:"突尼斯",a:"日本",v:"蒙特雷BBVA球场",r:"0-4"}'),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f'OK: {new[:60]}...')
    else:
        print(f'MISS: {old[:60]}...')

# 2. 更新时间戳
html = html.replace('数据更新：2026-06-19 15:12', '数据更新：2026-06-21 22:16')

# 3. 更新射手榜 - 更新已有球员进球数
scorer_updates = [
    ('{r:3,p:"维尼修斯",t:"巴西",g:1,m:1}', '{r:1,p:"维尼修斯",t:"巴西",g:2,m:2}'),
    ('{r:3,p:"翁达夫",t:"德国",g:1,m:1}', '{r:1,p:"翁达夫",t:"德国",g:3,m:2}'),
    ('{r:3,p:"萨默维尔",t:"荷兰",g:1,m:1}', '{r:3,p:"萨默维尔",t:"荷兰",g:2,m:2}'),
    ('{r:3,p:"镰田大地",t:"日本",g:1,m:1}', '{r:3,p:"镰田大地",t:"日本",g:2,m:2}'),
    ('{r:3,p:"萨伊巴里",t:"摩洛哥",g:1,m:1}', '{r:3,p:"萨伊巴里",t:"摩洛哥",g:2,m:2}'),
    ('{r:1,p:"乔纳森·大卫",t:"加拿大",g:3,m:2}', '{r:1,p:"乔纳森·大卫",t:"加拿大",g:3,m:2}'),  # 不变
]

for old, new in scorer_updates:
    if old in html:
        html = html.replace(old, new)
        print(f'Scorer OK: {new[:50]}...')
    else:
        print(f'Scorer MISS: {old[:50]}...')

# 4. 在射手榜末尾添加第2轮新进球球员（在最后一个射手条目后，]之前）
new_scorers = """{r:3,p:"库尼亚",t:"巴西",g:2,m:2},
{r:3,p:"布罗比",t:"荷兰",g:2,m:2},
{r:3,p:"加克波",t:"荷兰",g:2,m:2},
{r:3,p:"上田绮世",t:"日本",g:2,m:2},
{r:3,p:"加拉尔萨",t:"巴拉圭",g:1,m:2},
{r:3,p:"弗里曼",t:"美国",g:1,m:2},
{r:3,p:"凯西",t:"科特迪瓦",g:1,m:2},
{r:3,p:"埃兰加",t:"瑞典",g:1,m:2},
{r:3,p:"伊东纯也",t:"日本",g:1,m:2}
"""

# 找到SCORERS数组的结束位置
old_end = '{r:3,p:"特博霍·莫科埃纳",t:"南非",g:1,m:2}\n]'
new_end = '{r:3,p:"特博霍·莫科埃纳",t:"南非",g:1,m:2},\n' + new_scorers + ']'
html = html.replace(old_end, new_end)
print('Scorers added!')

with open(r'C:\Users\2jordan3\WorkBuddy\2026-06-10-07-46-32\worldcup-v8.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done! File updated.')

# 复制到index.html
with open(r'C:\Users\2jordan3\WorkBuddy\2026-06-10-07-46-32\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html updated!')
