# -*- coding:utf-8 -*-
import json,requests,time
from bs4 import BeautifulSoup


def start_time_change(Time):
    s = ''
    for i in range(0,19):
        s += Time[i]
    cur_time = time.mktime(time.strptime(s,'%Y-%m-%d %H:%M:%S'))
    cur_time -= 3600
    return cur_time


def get_seconds(duration):
    h,m=duration.strip().split(':')
    times=int(h)*3600+int(m)*60
    return times

url = 'https://atcoder.jp/contests/'
req = requests.get(url)
soup=BeautifulSoup(req.text,'lxml')
data=soup.select('#contest-table-upcoming>div>div>table>tbody>tr')

solved = {}
s='['
# f.write('[')
flag=0
for d in data:
    if flag:
    	s+=','
        # f.write(',')
    flag=1
    contests_start_time=d.find('time').get_text()
    contests_start_time=start_time_change(contests_start_time)

    contests_url='https://atcoder.jp'+d.find_all('a')[1]['href']

    contests_name=d.find_all('a')[1].get_text()

    contests_length=d.find_all('td')[2].get_text()

    solved['name'] = contests_name
    solved['contest_url'] = contests_url
    solved['start_time'] = contests_start_time
    solved['durationSeconds'] = get_seconds(contests_length)
    solved['end_time'] = contests_start_time+solved['durationSeconds']
    solved['platform'] = 'AtCoder'
    s+=json.dumps(solved,ensure_ascii=False)
    # f.write(json.dumps(solved,ensure_ascii=False))
s+=']'
f = open('../json/atcoder-upcoming.json', 'w')
f.write(s)
# f.write(']')
f.close()
# print('atcoder-upcoming has been completed!')