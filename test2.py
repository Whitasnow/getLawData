# -*- coding: utf-8 -*-
import re
from common.getDataDef import get_data
from bs4 import BeautifulSoup

# 获取数据
url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
courtNameData=get_data(url)
courtnames = re.findall(r"courtName\":\"(.+?)\"", courtNameData)

count=1
# for courtname in courtnames:
# print(courtname)
courtname='辽宁省高级人民法院'
baikeUrl = 'https://baike.baidu.com/item/'+courtname
courtData=get_data(baikeUrl)
# 解析数据
soup = BeautifulSoup(courtData, 'lxml')
main_content = soup.find("div", class_="main-content")
para_title = main_content.find(attrs={"label-module": "para-title"})
para = main_content.find(attrs={"label-module": "para"})
# print(para_title.previous_sibling)
print(para.next_element )
