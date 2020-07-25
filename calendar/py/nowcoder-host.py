# -*- coding:utf-8 -*-
import json,requests,time,html
from bs4 import  BeautifulSoup


url = 'https://ac.nowcoder.com/acm/contest/vip-index'
req = requests.get(url)
soup = BeautifulSoup(req.text,'lxml')
data = soup.select('body > div.nk-container.acm-container > div.nk-main.with-banner-page.clearfix.js-container > div.nk-content > div.platform-mod > div.platform-item.js-item ')
s='['
# f.write('[')
flag=0
for d in data:
    if flag:
    	s+=','
        # f.write(',')
    flag=1

    solved = d['data-json']
    solved = html.unescape(solved).encode('utf-8')
    solved = json.loads(solved)
    # print(solved)
    solved['start_time'] = int(solved['contestStartTime']/1000)
    solved['end_time'] = int(solved['contestEndTime']/1000)
    solved['durationSeconds'] = int(solved['contestDuration']/1000)
    solved['name'] = solved['contestName']
    solved['platform'] = '牛客'
    solved['contest_url'] = 'https://ac.nowcoder.com'+d.find('a')['href']
    s+=json.dumps(solved,ensure_ascii=False)
    # f.write(json.dumps(solved,ensure_ascii=False))
s+=']'
# f.write(']')
f = open('../json/nowcoder-host.json','w',encoding='utf-8')
f.write(s)
f.close()
# print('Nowcoder school has been Completed!')
