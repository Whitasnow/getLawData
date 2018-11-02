# -*- coding: utf-8 -*-
import requests
import chardet
import time
from selenium import webdriver

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
    # charset = chardet.detect(data.content)
    # data.encoding=charset['encoding']
    if data!=None:
        return data.text

def post_data(url,form_data):
    # 获取数据
    # url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
    headers={'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
    try:
        # data = requests.get(url,headers=headers)
        data = requests.post(url,headers=headers,data=form_data)
    except requests.exceptions.ConnectionError as e:
        print("请求错误，url：",url)
        print("错误详情：",e)
        data=None
    # 编码检测
    charset = chardet.detect(data.content)
    data.encoding=charset['encoding']
    return data.text


def selenium_data(url):
    # 获取数据
    # url='http://baike.baidu.com/cms/s/court/court-data.json?t=201891616'
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    print(html)
    # driver.quit()
    # return html

    #获取总页数（通过二次定位方法进行定位）
    # print(driver)
    # total_pages = len(driver.find_element_by_class_name('page-inner').find_element_by_tag_name('a'))
    # print ('The total page is %s'%total_pages)
    #再次获取所分页，并执行翻页操作
    # print(driver)
    # total_page = driver.find_element_by_class_name('page-inner').find_elements_by_tag_name('a')
    # print(len(total_page))
    # for page in total_page:
    #     print(page.text)
    # for page in total_page:
    #      page.click()

if __name__ == '__main__':
    selenium_data('http://www.chinatrial.com/lib/flsp/FlspSearch.aspx?libid=04')