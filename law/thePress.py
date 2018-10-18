# -*- coding: utf-8 -*-
import pymysql
import uuid

# 新建连接
db = pymysql.connect(host="192.168.5.210",user="root",password="root",db="law",charset='utf8')
cursor = db.cursor()


sql ="insert into t_court_info values(%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.execute(sql,(str(uuid.uuid1()),"1", '',"1","1","1","1","1"))
db.commit()


db.close
