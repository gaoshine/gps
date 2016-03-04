# -*- coding: utf-8 -*-
#mysqldb
import time, MySQLdb


#连接
conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="c365",charset="utf8")
cursor = conn.cursor()

#查询
n = cursor.execute("select * from billboard where id=10")
for row in cursor.fetchall():
    print row[0],row[1],row[2]

#关闭
cursor.close()
conn.close()

def find(mid):
    try:
        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="c365",charset="utf8")
        cursor = conn.cursor()
        #查询
        n = cursor.execute("select * from billboard where id=%d"%mid)
        for row in cursor.fetchall():
            print row[0],row[1],row[2]

    except Exception, e:
        print e