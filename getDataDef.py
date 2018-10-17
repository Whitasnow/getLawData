# -*- coding: utf-8 -*-
import requests
import chardet

def get_data(url):
    # 获取数据
    # url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
    headers={'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
    try:
        data = requests.get(url,headers=headers)
    except requests.exceptions.ConnectionError as e:
        print("请求错误，url：",url)
        print("错误详情：",e)
        data=None
    # 编码检测
    charset = chardet.detect(data.content)
    data.encoding=charset['encoding']
    return data.text