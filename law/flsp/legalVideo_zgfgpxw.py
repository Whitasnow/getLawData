# -*- coding: utf-8 -*-
import pymysql
import uuid
import re
from common.getDataDef import get_data
from bs4 import BeautifulSoup

# 新建连接
db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
cursor = db.cursor()

count=0
# 获取数据
for x in range(59,67):
    url='http://peixun.court.gov.cn/index.php?m=special&c=stindex&a=show&sid='+str(x)
    print(url)
    courtData=get_data(url)
    soup = BeautifulSoup(courtData,'lxml')
    tbody = soup.find_all('table')[1]
    trs = tbody.find_all('tr')
    for tr in trs:
        # tr = trs[1]
        a = tr.find('a')
        if a!=None:
            video_url = 'http://peixun.court.gov.cn/'+a.get('href')
            videoData = get_data(video_url)
            vsoup = BeautifulSoup(videoData,'lxml')
            # print(vsoup)
            video_name = vsoup.find('h3').get('title')
            vtbody = vsoup.find('table')
            # 无权观看的情况，pass
            if vtbody!=None:
                tds = vtbody.find_all('td')
                video_lecturer = tds[2].get_text()
                recording_time = tds[3].get_text()
                video_introduction = tds[4].get_text()
                source_code = 13
                video_source = url
                sql ="insert into t_law_video_info (`video_id`,`video_name`,`video_introduction`,`video_url`,`video_lecturer`,`recording_time`,`video_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(str(uuid.uuid1()),video_name,video_introduction,video_url,video_lecturer,recording_time,video_source,source_code))
                db.commit()
                count+=1
                print(count)
                print("-----------------------------------------------")
db.close