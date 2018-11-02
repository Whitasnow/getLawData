# -*- coding: utf-8 -*-
import pymysql
import uuid
from common.getDataDef import get_data
from bs4 import BeautifulSoup
import sys
from multiprocessing import Pool
import re

def get_lists():
    urls = []
    # 获取数据libid=04、02、03
    url = 'http://english.gov.cn/policies/policywatch/'
    courtData=get_data(url)
    # 解析数据
    soup = BeautifulSoup(courtData,'lxml')
    # print(soup)
    lists = soup.select(".list-container")[0].select("li")
    for list in lists:
        urls.append('http://english.gov.cn'+list.find('a').get('href'))
    print(len(urls))
    # print(urls)
    return urls


def do_insert(href):
    print(href)
    wwzl_url = href
    url = 'http://english.gov.cn/policies/policywatch/'
    wwzl_source = url
    source_code = 3

    # 新建连接
    db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
    cursor = db.cursor()

    zzzfw_data = get_data(href)
    if zzzfw_data!=None:
        zzzfw_soup  =BeautifulSoup(zzzfw_data,'lxml')
        title = zzzfw_soup.find('h3')
        wwzl_title = title.get_text()
        zuozhe_riqi_info = zzzfw_soup.select(".adio")
        if len(zuozhe_riqi_info)==2:
            wwzl_promulgator = zuozhe_riqi_info[0].get_text()
            wwzl_content = zzzfw_soup.find("content").get_text()
            print(len(wwzl_content))
            tag = zuozhe_riqi_info[1]
            tag.span.extract()
            tag.span.extract()
            promulgation_date = tag.get_text().replace('\n','')
            if len(wwzl_content)<20000:
                sql ="insert into t_wwzl_info (`wwzl_id`,`wwzl_title`,`wwzl_promulgator`,`promulgation_date`,`wwzl_content`,`wwzl_url`,`wwzl_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(str(uuid.uuid1()),wwzl_title,wwzl_promulgator,promulgation_date,wwzl_content,wwzl_url,wwzl_source,source_code))
                db.commit()
                print("-----------------------------------------------")
            else:
                print('字段太长'+href)
        else:
            print('zuozhe_riqi_info出错')

if __name__=='__main__':
    # do_insert('http://english.gov.cn/policies/latest_releases/2018/11/01/content_281476371228670.htm')
    pool = Pool(3)
    urls = get_lists()
    sys.setrecursionlimit(10000)
    pool.map(do_insert, urls)
    pool.close()
    pool.join()