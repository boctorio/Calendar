# -*- coding:utf-8 -*-
import json, requests, time

# 获取contest api信息
response = requests.get('https://codeforces.com/api/contest.list')

# json数据格式转python数据格式
data = json.loads(response.text)

# 获取需要的result部分
data = data['result']

# 将其中一些元素进行更改，变成所需要的数据格式
for x in data:
    # print(x)
    x['start_time'] = x['startTimeSeconds']  # 转为详细时间
    x['end_time'] = x['startTimeSeconds']+x['durationSeconds']  # durationSeconds为比赛时长
    x['platform'] = 'Codeforces'  # 比赛平台
    x['contest_url'] = 'https://codeforces.com/contest/'+str(x['id'])  # 比赛链接

# python数据格式转json数据格式
data = json.dumps(data,ensure_ascii=False)

# 写入文档
f = open('../json/codeforces.json', 'w',encoding='utf-8')
f.write(data)
f.close()
# print("codeforces has been completed!")
