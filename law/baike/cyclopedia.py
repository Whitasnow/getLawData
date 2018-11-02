# -*- coding: utf-8 -*-
import requests
import chardet
import json
from bs4 import BeautifulSoup

# 获取数据
url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
headers={'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
data = requests.get(url,headers=headers)
# 编码检测
charset = chardet.detect(data.content)
data.encoding=charset['encoding']
# print(data.text)

# 解析数据
# soup = BeautifulSoup(data.text,'lxml')
# print(soup)

