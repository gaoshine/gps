# -*- coding: utf-8 -*-
#mysqldb
import time, MySQLdb
import json
from json import *

def find(imei):
    try:
        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #查询
        n = cursor.execute("select * from datapoint where IMEI='%s'"%imei)
        for row in cursor.fetchall():
            print row[0],row[1],row[2]

    except Exception, e:
        print e

def pointadd(GPSDataJson):
    try:
        values = {}
        d=JSONDecoder().decode(GPSDataJson)
        #values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'
        values["IMEI"] = d["IMEI"]
        values["battery"] = d["battery"]
        values["lon"] =  d["lon"]
        values["lat"] =   d["lat"]
        values["mdate"] =  str(d["date"] + ' ' +d["time"])
        #values["time"] = d["time"]

        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #插入
        sql = "insert into datapoint (lon,lat,battery,IMEI) values (%s,%s,%s,%s)"%(values["lon"],values["lat"],values["battery"],values["IMEI"])
        print sql
        n = cursor.execute(sql)


    except Exception, e:
        print e
