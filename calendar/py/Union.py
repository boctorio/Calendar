#coding = utf-8
import os,json,requests,time

filePath = '../json/'

all_file = os.listdir(filePath)
# print(all_file)
s='['
# f1.write('[')
flag=0
str=['start_time','end_time','contest_url','durationSeconds','platform','name']
now_time = time.time()
for url in all_file:
    if url == 'all_contest.json':
        continue
    f2 = open(r'../json/'+url,'r',encoding='utf-8')
    text = f2.read()
    contests = json.loads(text)
    for c in contests:
        if now_time-c['start_time']>180*86400 :
            continue
        if flag:
        	s+=','
            # f1.write(',')
        flag=1
        s+='{'
        # f1.write('{')
        flag2=0

        for S in str:
            if flag2:
            	s+=','
                # f1.write(',')
            flag2=1
            s+='"'+S+'":'+json.dumps(c[S],ensure_ascii=False)
            # f1.write('"'+s+'":'+json.dumps(c[s],ensure_ascii=False))
        s+='}'
        # f1.write('}')

s+=']'
# f1.write(']')
f1 = open('../json/all_contest.json','w',encoding='utf-8')
f1.write(s)
f1.close()
# print('All contests has been union!')