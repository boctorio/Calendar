import json,time,requests,re
from bs4 import BeautifulSoup


def start_time_change(s):
    # s = ''
    # for i in range(0,19):
    #     s += Time[i]
    cur_time = time.mktime(time.strptime(s,'%Y-%m-%d %H:%M'))
    return cur_time


def get_seconds(duration):
    h=duration[0]
    m=duration[1]
    times=int(h)*3600+int(m)*60
    return times


s='['
# f.write('[')
flag=0
for i in range(1,3):
    url= 'https://nanti.jisuanke.com/contest?page='+str(i)
    req=requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    data=soup.select('#app > div.jsk-panel.jsk-margin-top-0 > div.jsk-panel-bd.jsk-padding-top-sm > table > tbody > tr')
    solved = {}

    for d in data:
        if flag:
        	s+=','
            # f.write(',')
        flag=1
        contests_start_time = start_time_change(d.find_all('td')[3].get_text().strip())
        solved['start_time'] = contests_start_time

        length = d.find_all('td')[4].get_text()
        length = re.findall(r'\d+',length)
        solved['durationSeconds'] = get_seconds(length)
        solved['end_time'] = contests_start_time + solved['durationSeconds']
        solved['contest_url'] = 'https:'+ d.find('a')['href']
        solved['platform'] = '计蒜客'
        solved['name'] = d.find('a')['title']
        s+=json.dumps(solved)
        # f.write(json.dumps(solved))

s+=']'
f = open('../json/jisuanke.json','w')
# f.write(']')
f.write(s)
f.close()
# print('jisuanke has been completed!')