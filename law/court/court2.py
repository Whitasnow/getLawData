# -*- coding: utf-8 -*-
import pymysql
import uuid
import re
from common.getDataDef import get_data
from bs4 import BeautifulSoup

# 新建连接
db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
cursor = db.cursor()

# 获取数据
url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
courtNameData=get_data(url)
courtnames = re.findall(r"courtName\":\"(.+?)\"", courtNameData)

count=0
for courtname in courtnames:
    if count >2571:
        print(courtname)
    print(courtname)
    count+=1
    print(count)
    print("-----------------------------------------------")

db.close