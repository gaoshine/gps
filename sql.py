# -*- coding: utf-8 -*-
#mysqldb
import time, MySQLdb
import json
from json import *

def findlbs(mcc,mnc,lac,ci):
    try:
        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #查询
        sql = "select * from  lbs where mmc=%d and mnc=%d and lac=%d and ci=%d"%(mcc,mnc,lac,ci)
        print sql
        n = cursor.execute(sql)
        row = cursor.fetchone()
        if row :
            print row[0],row[1],row[2]
            r = True
        else :
            r =  False
        return r

    except Exception, e:
        print e

def lbsadd(mcc,mnc,lac,ci,GPSDataJson):
    try:
        values = {}
        d=JSONDecoder().decode(GPSDataJson)
        #values['GPSDataJson'] = '{"errcode":0, "lat":"36.602612", "lon":"114.478172", "radius":"214", "address":"河北省邯郸市邯山区火磨街道东方新天地2号楼;火磨街与陵西南大街路口西北77米"}'
        values["mcc"] = mcc
        values["mnc"] = mnc
        values["lac"] =  lac
        values["ci"] =   ci
        values["lat"] =  d["lat"]
        values["lon"] =  d["lon"]
        values["address"] =  d["address"]

        #values["time"] = d["time"]

        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #插入
        sql = "insert into lbs  (lon,lat,mmc,mnc,lac,ci,adress) values ('%s','%s',%d,%d,%d,%d,'%s') "%(values["lon"],values["lat"],values["mcc"],values["mnc"],values["lac"],values["ci"],values["address"])
        print sql
        n = cursor.execute(sql)


    except Exception, e:
        print e



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
