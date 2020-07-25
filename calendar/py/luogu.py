# -*- coding:utf-8 -*-
import json,requests,time,html
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
url = "https://www.luogu.com.cn/contest/list?page=1&_contentOnly=1"
req = requests.get(url,headers=headers)
# print(req)
data = req.json()['currentData']['contests']['result']
# print(data)
for x in data:
    x['start_time'] = x['startTime']
    x['end_time'] = x['endTime']
    x['platform'] = '洛谷'
    x['contest_url'] = 'https://www.luogu.com.cn/contest/'+str(x['id'])
    x['durationSeconds'] = x['end_time'] - x['start_time']
data = json.dumps(data,ensure_ascii=False)
f = open('../json/luogu.json','w',encoding='utf-8')
f.write(data)
f.close()
# print('Luogu has been completed!')