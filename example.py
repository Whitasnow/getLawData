# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 获取数据
url='https://book.douban.com/latest'
headers={'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
data = requests.get(url,headers=headers)
# print(data.text)

# 解析数据
soup = BeautifulSoup(data.text,'lxml')
# print(soup)
books_left = soup.find('ul',{'class':'cover-col-4 clearfix'})
books_left = books_left.find_all('li')

books_right = soup.find('ul',{'class':'cover-col-4 pl20 clearfix'})
books_right = books_right.find_all('li')

books = list(books_left)+list(books_right)

img_urls = []
titles = []
ratings = []
authors = []
details = []
for book in books:
    #图书封面url
    img_url = book.find_all('a')[0].find('img').get('src')
    img_urls.append(img_url)
    #图书标题
    title = book.find_all('a')[1].get_text()
    titles.append(title)
    # 评价
    rating = book.find('p',{'class':'rating'}).get_text()
    rating = rating.replace('\n','').replace(' ','')
    ratings.append(rating)
    # 作者
    author = book.find('p',{'class':'color-gray'}).get_text()
    author = author.replace('\n','').replace(' ','')
    authors.append(author)
    # 图书简介
    detail = book.find_all('p')[2].get_text()
    detail = detail.replace('\n','').replace(' ','')
    details.append(detail)

    print("img_urls",img_urls)
    print("titles",titles)
    print("ratings",ratings)
    print("authors",authors)
    print("details",details)