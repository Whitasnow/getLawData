# -*- coding: utf-8 -*-
import pymysql
import uuid
import re
from common.getDataDef import post_data
from common.getDataDef import get_data
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# 新建连接
db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
cursor = db.cursor()

# 获取数据libid=04、02、03
url = 'http://www.chinatrial.com/lib/flsp/FlspSearch.aspx?libid=04'
driver = webdriver.Firefox()
driver.get(url)
count=0
# 愚蠢的手动翻页获取数据
for i in range(1, 6):
    time.sleep(6)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    # divdatalist = soup.select("#divdatalist")
    lists = soup.select(".vBox4List")

    for list in lists:
    # list = lists[0]
        video_name = list.find('h1').get_text()
        video_url = 'http://www.chinatrial.com/lib/flsp/'+list.find('p').find('a').get('href')
        video_creator = list.find_all('td')[0].get_text()
        recording_time = list.find_all('td')[1].get_text()
        video_introduction = list.find_all('td')[2].get_text()
        video_source = url
        sql ="insert into t_law_video_info (`video_id`,`video_name`,`video_introduction`,`video_url`,`video_creator`,`recording_time`,`video_source`) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(str(uuid.uuid1()),video_name,video_introduction,video_url,video_creator,recording_time,video_source))
        db.commit()
        count+=1
        print(count)
        print("-----------------------------------------------")
    db.close