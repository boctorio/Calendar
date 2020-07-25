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


s='['
# f.write('[')
flag=0
for i in range(1,7):
    # print(i)
    url = 'https://atcoder.jp/contests/archive?page='+str(i)
    req = requests.get(url)
    soup=BeautifulSoup(req.text,'lxml')
    data=soup.select('#main-container > div.row > div.col-lg-9.col-md-8 > div.panel.panel-default > div > table > tbody > tr')

    solved = {}
    for d in data:
        if flag:
        	s+=','
            # f.write(',')
        flag=1
        contests_start_time = start_time_change(d.find('time').get_text())
        contests_length = d.find_all('td')[2].get_text()

        solved['start_time'] = contests_start_time
        solved['contest_url'] = 'https://atcoder.jp'+d.find_all('a')[1]['href']
        solved['name'] = d.find_all('a')[1].get_text()
        solved['durationSeconds'] = get_seconds(contests_length)
        solved['end_time'] = contests_start_time+solved['durationSeconds']
        solved['platform'] = 'AtCoder'
        s+=json.dumps(solved,ensure_ascii=False)
        # f.write(json.dumps(solved,ensure_ascii=False))
        # print(solved)
    # print('Page '+str(i)+" has been competed!")
    time.sleep(2)
s+=']'
# f.write(']')
f = open('../json/atcoder-recent.json', 'w')
f.write(s)
f.close()
# print('atcoder-recent has been completed!')
