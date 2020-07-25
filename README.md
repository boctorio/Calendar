#全网比赛日历



全网比赛日历以各大OJ的比赛信息为主，通过爬虫将比赛信息爬取过来，并将其保存在json文件中，并通过前端js文件将其转化为可供用户查看的格式。接下来我将会把其实现步骤按照前端（HTML, CSS, JS）、后端（python, json）以及 Linux服务器的顺序进行介绍。

## 全览

全网比赛日历结构为：

![全览](/readme/all.png)

每一个文件夹对应一种文件类型（ python 文件夹中有额外的 linux 脚本），分别对应前面介绍的功能。

对于该比赛日历，我们需要的数据有：**比赛链接**，**比赛名称**，**比赛开始时间**，**比赛结束时间**，**比赛平台**，**比赛时长**等信息，因此在处理时要根据上述数据进行筛选。同时我们也需要对数据进行命名以便于处理，命名如下：

```
contest_url: 比赛链接
name: 比赛名称
start_time: 比赛开始时间
end_time: 比赛结束时间
platform: 比赛平台
durationSeconds: 比赛时长（该变量由于是在开发时临时添加，因此命名与其他命名有所不同）
```

为了方便处理，涉及到的时间信息均以Unix时间戳的形式进行存储。（时间戳参见百度词条：[Unix时间戳](https://baike.baidu.com/item/unix%E6%97%B6%E9%97%B4%E6%88%B3/2078227?fr=aladdin)）。



## 后端

### python

python文件主要实现比赛数据爬取功能，在该项目中，我一共爬取了四个大型OJ的比赛信息（牛客、计蒜客、Codeforces、AtCoder），由于某些会将比赛分为几种进行展示（如牛客分为牛客系列赛和高校校赛两类，自主创建比赛不在爬虫名单内）因此会写多个爬虫文件进行爬取。接下来以 Codeforces 和为例进行学习。

#### Codeforces

codeforces提供给我们了比赛信息的api，因此我们可以通过该api获取到对应的数据，而不需要我们自己去进行处理数据。更多关于codeforces的api参见网址：[Codeforces Api](http://codeforces.com/apiHelp) 

Codeforces提供的比赛信息api为：https://codeforces.com/api/contest.list ，其数据类型为json，为了获得想要的信息，我们需要先将其转化成python数据格式，之后再进行处理。

```python
#codeforces.py
# -*- coding:utf-8 -*-
#爬虫需要用到的库，json用于格式转换，requests用于请求网页数据，time库用于处理时间信息（其他ppy文件中会用到）
import json, requests, time

# 获取contest api信息，此时reponse中已经获取到了该api提供的数据信息,此时该信息格式为json格式。
response = requests.get('https://codeforces.com/api/contest.list')

# json数据格式转python数据格式，这样我们就可以处理获得想要的数据。
data = json.loads(response.text)

# 获取需要的result部分，这里类似于c++中的map，可以在该句代码前面输出data查看数据结构。
data = data['result']

# 将其中一些元素进行更改，变成所需要的数据格式。
for x in data:
    # print(x)
    x['start_time'] = x['startTimeSeconds']  # 转为详细时间
    x['end_time'] = x['startTimeSeconds']+x['durationSeconds']  # durationSeconds为比赛时长
    x['platform'] = 'Codeforces'  # 比赛平台
    x['contest_url'] = 'https://codeforces.com/contest/'+str(x['id'])  # 比赛链接

# python数据格式转json数据格式，方便进行存储调用
data = json.dumps(data,ensure_ascii=False)

# 写入文档。写入文档操作必须在文件结尾处，后续将会讲解原因。
f = open('../json/codeforces.json', 'w',encoding='utf-8')
f.write(data)
f.close()
# print("codeforces has been completed!")

```

#### 计蒜客

计蒜客以及其他各大OJ一般都没有配置可用的api接口，因此需要我们自己处理数据。相对应的，代码量也要比Codeforces多得多。

```Python
# python库，其中BeautifulSoup库用于处理HTML文档。
import json,time,requests,re
from bs4 import BeautifulSoup

# 将时间处理为时间戳的格式，由于该OJ获取到的时间为“年：月：日 时：分”的格式，因此需要根据其格式进行相对应的转换。
def start_time_change(s):
    cur_time = time.mktime(time.strptime(s,'%Y-%m-%d %H:%M'))
    return cur_time

# 此处也为特殊处理，将比赛时长变为秒的形式。
def get_seconds(duration):
    h=duration[0]
    m=duration[1]
    times=int(h)*3600+int(m)*60
    return times

# s为最终的json数据，可以在文件最后输出s的值去查看s的储存数据格式。
s='['
# flag也为特殊处理，由于json格式的特殊性，每个数据都需要用逗号隔开，因此用flag判断需不需要添加逗号。
flag=0

# 获取前三页的比赛信息，之后的比赛信息由于时效性可以选择不爬取。
for i in range(1,3):
  	# 下列三行为获取对应的html文档。由于req的值并非为html文档，因此需要用BeautifulSoup进行处理。
    url= 'https://nanti.jisuanke.com/contest?page='+str(i)
    req=requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    
    # 此处需要根据实际情况去获取对应的值，我会在下方介绍对应的获取方法。
    data=soup.select('#app > div.jsk-panel.jsk-margin-top-0 > div.jsk-panel-bd.jsk-padding-top-sm > table > tbody > tr')
    
    # solved 为元素集合，参见下列代码。
    solved = {}

    for d in data:
        # 处理逗号问题。
        if flag:
        	s+=','
        flag=1
        
        # 处理信息，这里有不懂的可以输出调试或去百度或Google一下。
        contests_start_time = start_time_change(d.find_all('td')[3].get_text().strip())
        solved['start_time'] = contests_start_time

        length = d.find_all('td')[4].get_text()
        length = re.findall(r'\d+',length)
        solved['durationSeconds'] = get_seconds(length)
        solved['end_time'] = contests_start_time + solved['durationSeconds']
        solved['contest_url'] = 'https:'+ d.find('a')['href']
        solved['platform'] = '计蒜客'
        solved['name'] = d.find('a')['title']
        
        # 将 solved 存储的单个比赛数据加入到s当中。
        s+=json.dumps(solved)
# json结尾加 ‘]’ ，之后写入文件。
s+=']'
f = open('../json/jisuanke.json','w')
f.write(s)
f.close()
```

在获取比赛信息对应的元素时，我们需要用html的结构去获取想要的元素（如 body > table > ul ），这一步浏览器给我们提供了比较完备的方案，具体步骤如下：

1. 进入检查界面：

   ![](/readme/step1.png)

2. 利用浏览器的元素获取指针获取到想要的元素对应的位置，此时会在element界面显示出选中的元素的位置：

   ![](/readme/step2.png)

3. 找到需要的元素，右键进行如下操作，此时就可以将选择器信息复制到粘贴板，在本例中，我们需要的是\<td>元素：

   ![](/readme/step3.png)

动图如下：

![](/readme/step.mp4)

在点击完copy selecter后，我们的粘贴板会得到如下信息：

```
#app > div.jsk-panel.jsk-margin-top-0 > div.jsk-panel-bd.jsk-padding-top-sm > table > tbody > tr:nth-child(1)
```

其中nth-child(1)表示第一个tr元素，由于我们需要获取到所有的tr元素，因此需要将其删除掉，这样就得到了所有的tr元素：

```
#app > div.jsk-panel.jsk-margin-top-0 > div.jsk-panel-bd.jsk-padding-top-sm > table > tbody > tr
```



### JSON

JSON是一种轻量的数据交换语言，易于阅读。python爬取的所有比赛信息均存放在JSON文件中。其中all_contest.json 是所有的比赛的集合，该文件通过Union.py进行整合。Union文件主要以处理文本为主，将所有的OJ比赛处理之后放在all_contest.json中，因此就不继续展开讲解了。之后前端也是通过调用该文件加载比赛信息。



## 前端

前段以耳熟能详的HTML+CSS+JavaScript进行开发。不细展开讲了，主要讲一下js文件。

### main.js

Main.js主要用来处理json文件数据，并将该数据传到index.html中。由于爱处理是比较复杂，因此我只讲每个函数的作用即可，具体实现可以下去自己研究。

1. 确定头部信息。

对于该比赛日历，首先我们需要确定比赛日历的结构，我初步将其设为每次显示七天，当天设为第二个位置，这样可以使得用户获得最多的有用的信息量（当天+后来五天），以及留出来第一个位置用于用户进行补题或其他操作。

因此我们首先要计算出当天的日期，根据当天日期的前后日期以及对应的星期几，这里对应的函数为load_head()：

![](/readme/table.png)

2. 初始化日期对应数组。

在加载完头部信息之后，我们需要加载比赛信息。由于我们使用JSON文件进行存储，不能够利用诸如数据库的查询等功能，因此需要我们预先设置好每天对应的比赛信息。这里我们开了一个数组daily_contests，其大小为10\*12\*32\*20，表示10年/12月/32天/20场比赛，每个元素代表一个比赛，由于我在爬取比赛信息时只保留了前半年以及之后的比赛，因此数组需要一个2019的修正，因此daily_contests\[year]\[month]\[day][contest_num]表示第2019+year年month月day天第contest_num场比赛的信息。同时我们需要再开一个数组contest_num用来记录每天的比赛数量，其大小为10\*12\*32。这样我们就几乎保证了所有的比赛不会越界。其对应的函数为Init_array()。

3. 处理比赛信息。

在初始化完成比数组后，我们就需要将json中的数据处理一下添加到数组当中。这一步直接用Insert()函数进行封装。我们需要处理每个比赛对应的年月日比赛编号信息，将其对应到数组当中，以便后续处理。

4. 加载比赛信息到HTML文档。

在处理完比赛信息后，我们就需要将比赛信息加载到前端，加载时需要遵循HTML语法，所以文本处理代码量偏多。在加载时，由于我们添加了弹窗功能，而其功能需要设置id属性，因此号需要额外处理一下id属性。这一步主要在detail()函数中处理。



## Linux

该项目需要放在服务器进行运行，而爬虫文件由于数量过多，而且后续可能还会持续添加，因此不能使用运行单个python文件的方式在服务器上跑，所以就需要写一个脚本文件。脚本具体内容如下：

```
#/bin/bash

flag=1
files=./*.py
while [ $flag == 1 ]
do
	for file in $files
	do
		if [ "$file" != "./Union.py" ] && [ -f $file ]
		then
			python3 $file
		fi
	done
	python3 Union.py
	sleep 7200
done

```

该脚本名字为RunForContests，放在py文件夹下。其中files为所在文件夹下所有py文件（利用了 ‘ * ’ 通配符）然后开始利用while循环持续运行该脚本。

在for循环中，我们遍历所有python文件，然后运行（python3 $file）。但是Union.py除外，因为该文件的目的是整合所有的json文件，因此需要在所有爬虫完成之后运行。为了减少服务器（自己的以及OJ的）压力，我设置了每两个小时爬取一次。这个时间也可以根据实际情况进行改变。

在linux上运行该文件的命令是，需要注意的是现必须在RunForContests所在文件夹下运行，否则需要修改下列命令的文件目录参数：

```
nohup ./RunForContests &
```

Nohup 和 &的作用可以百度或Google去学习。该脚本在运行时可能会输出一些信息，这些信息都将输出到nohup.out文件中，韵词如果遇到错误也可以去查看该文件。

## 属性配置

由于运行该文件需要python环境，因此需要预先配置python环境（该项目为python3环境），这个可以去网上查相关博客。

如果有其他问题，可以联系我（Boctorio，QQ1614466758）。文档若有描述不清楚的地方，后续会慢慢进行修改补充。
