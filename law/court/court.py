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
        # courtname=courtnames[1]
        baikeUrl = 'https://baike.baidu.com/item/'+courtname
        courtData=get_data(baikeUrl)
        # 解析数据
        soup = BeautifulSoup(courtData,'lxml')

        # 获取所有信息
        allText=soup.find_all(attrs={"label-module": "para"})
        # print(len(allText))
        # for aa in allText:
        #     print(aa.get_text())
        #     # print(aa.find('div',{'class':'para'}).get_text())
        # print(soup)

        # allText中头部包含的para，设置偏移值
        lemmaSummary=soup.find(attrs={"label-module": "lemmaSummary"})
        if lemmaSummary is not None:
         lemmaSummaryPara=lemmaSummary.find_all(attrs={"label-module": "para"})
        offset=len(lemmaSummaryPara)

        #初始化信息
        introduction = []
        build = []
        honor = []
        organization = []
        geographic = []
        leader = []
        #查看目录有多少项信息
        dics=soup.find_all('li', {'class': 'level1'})
        dicCount=1-(1-offset)
        # print(len(dics))
        for dic in dics:
            id = dic.find('a').get_text()
            if id=='法院简介':
                introduction=allText[dicCount].get_text()
            elif id=='法院建设':
                build=allText[dicCount].get_text()
            elif id=='所获荣誉':
                honor=allText[dicCount].get_text()
            elif id=='机构设置':
                organization=allText[dicCount].get_text()
            elif id=='地理位置':
                geographic=allText[dicCount].get_text()
            elif id=='现任领导':
                leader=allText[dicCount].get_text()
            dicCount +=1



        if introduction==[]:
            introduction=''
        print('法院简介:',introduction)
        if build==[]:
            build=''
        print('法院建设:',build)
        if honor==[]:
            honor=''
        print('所获荣誉:',honor)
        if organization==[]:
            organization=''
        print('机构设置:',organization)
        if geographic==[]:
            geographic=''
        elif geographic!=[]:
            geographic=geographic.replace('\n','').replace(' ','')
        print('地理位置:',geographic)
        if leader==[]:
            leader=''
        print('机构设置:',leader)
        print(baikeUrl)

        sql ="insert into t_court_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(str(uuid.uuid1()),courtname,introduction,build,honor,organization,geographic,baikeUrl,leader))
        db.commit()
    count+=1
    print(count)
    print("-----------------------------------------------")

db.close