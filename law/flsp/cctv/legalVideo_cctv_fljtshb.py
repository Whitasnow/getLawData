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
    url = 'http://tv.cctv.com/lm/fljtshb/videoset/index.shtml'
    # url = 'http://tv.cctv.com/lm/pingan365/videoset/index.shtml'
    courtData=get_data(url)
    # 解析数据
    soup = BeautifulSoup(courtData,'lxml')
    # print(soup)
    lists = soup.select(".text")
    # lists = soup.find_all('li')
    for list in lists:
        href = list.find('a').get('href')
        urls.append(href)
    print(len(urls))
    return urls


def do_insert(href):
    # 新建连接
    db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
    cursor = db.cursor()

    cctv_data = get_data(href)
    print(href)
    # cctv_data = get_data("http://news.cntv.cn/2014/02/20/VIDE1392875460487310.shtml")
    cctv_soup  =BeautifulSoup(cctv_data,'lxml')
    title = cctv_soup.find('h3')
    video_url = href
    url = 'http://tv.cctv.com/lm/fljtshb/videoset/index.shtml'
    video_source = url
    source_code = 23
    related_articles = cctv_soup.select('#content_body')
    if related_articles!=[]:
        related_articles = related_articles[0].get_text().replace('\n','')
    elif related_articles==[]:
        related_articles = cctv_soup.select('.cnt_bd')
        if related_articles!=[]:
            related_articles = related_articles[0].get_text().replace('\n','')

    wenben = cctv_soup.select(".text_box_02")
    if title!=None and wenben!=[]:
        video_introduction = ''
        if wenben[0].find_all('p')!=None:
            if len(wenben[0].find_all('p'))>2:
                video_introduction = wenben[0].find_all('p')[2].get_text()
        title_info = title.get_text().split()
        if len(title_info) >=3:
            video_name = title_info[2]
            if len(title_info) ==4:
                video_name = title_info[2]+title_info[3]
            recording_time = title_info[1]
            sql ="insert into t_law_video_info (`video_id`,`video_name`,`related_articles`,`video_introduction`,`video_url`,`recording_time`,`video_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(str(uuid.uuid1()),video_name,related_articles,video_introduction,video_url,recording_time,video_source,source_code))
            db.commit()
            print("-----------------------------------------------")
        elif (title.get_text().find("]")!=-1 and title.get_text().find("(")!=-1):
            title_info = re.split('[])]',title.get_text())
            if len(title_info) ==3:
                video_name = title_info[1]
            recording_time = title_info[2]
            sql ="insert into t_law_video_info (`video_id`,`video_name`,`related_articles`,`video_introduction`,`video_url`,`recording_time`,`video_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(str(uuid.uuid1()),video_name,related_articles,video_introduction,video_url,recording_time,video_source,source_code))
            db.commit()
            print("-----------------------------------------------")
    elif title==None or wenben==[]:
        title = cctv_soup.find('h1')
        title_info = title.get_text().split()
        if len(title_info) >=3:
            video_name = title_info[2]
            if len(title_info) ==4:
                video_name = title_info[2]+title_info[3]
            recording_time = title_info[1]
            sql ="insert into t_law_video_info (`video_id`,`video_name`,`related_articles`,`video_url`,`recording_time`,`video_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(str(uuid.uuid1()),video_name,related_articles,video_url,recording_time,video_source,source_code))
            db.commit()
            print("-----------------------------------------------")
        elif (title.get_text().find("]")!=-1 and title.get_text().find("(")!=-1):
            title_info = re.split('[](]',title.get_text())
            if len(title_info) ==3:
                video_name = title_info[1]
                recording_time = title_info[2]
                sql ="insert into t_law_video_info (`video_id`,`video_name`,`related_articles`,`video_url`,`recording_time`,`video_source`,`source_code`) values(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(str(uuid.uuid1()),video_name,related_articles,video_url,recording_time,video_source,source_code))
                db.commit()
                print("-----------------------------------------------")

if __name__=='__main__':
    pool = Pool(3)
    urls = get_lists()
    sys.setrecursionlimit(10000)
    # count = 0
    # temp = []
    # for url in urls:
    #     # if count>=2000 and count<2500:
    #     if count>=1500 and count<2000:
    #     # if count>=1000 and count<1500:
    #     # if count>=500 and count<1000:
    #     # if count<500:
    #         temp.append(url)
    #     count+=1
    # print(len(temp))
    # pool.map(do_insert, temp)
    pool.map(do_insert, urls)
    pool.close()
    pool.join()
