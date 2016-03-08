# -*- coding: utf-8 -*-
#mysqldb
import time, MySQLdb
import json
from json import *

def findlbs(LBSDataJson):
    try:
        d=JSONDecoder().decode(LBSDataJson)
        mcc = d["mcc"]
        mnc = d["mnc"]
        lac = d["lac"]
        ci = d["ci"]
        imei =d["IMEI"]
        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #查询
        sql = "select * from  lbs where mmc=%d and mnc=%d and lac=%d and ci=%d"%(int(mcc),int(mnc),int(lac),int(ci))
        print sql
        n = cursor.execute(sql)
        row = cursor.fetchone()
        desc = cursor.description
        if row :
            print row[5],row[6],row[7]
            #{"errcode":0, "lat":"36.602612", "lon":"114.478172", "radius":"214", "address":"河北省邯郸市邯山区火磨街道东方新天地2号楼;火磨街与陵西南大街路口西北77米"}
            r ='{"errcode":0, "IMEI":"%s", "lat":"%s", "lon":"%s", "address":"%s"}' % (imei,row[5],row[6],row[7])

        else :
            r =  False
        return r

    except Exception, e:
        print e

def lbsadd(GPSDataJson,LBSDataJson):
    try:
        values = {}
        d=JSONDecoder().decode(LBSDataJson)
        e=JSONDecoder().decode(GPSDataJson)
        #values['GPSDataJson'] = '{"errcode":0, "lat":"36.602612", "lon":"114.478172", "radius":"214", "address":"河北省邯郸市邯山区火磨街道东方新天地2号楼;火磨街与陵西南大街路口西北77米"}'
        values["mcc"] = e["mcc"]
        values["mnc"] = e["mnc"]
        values["lac"] = e["lac"]
        values["ci"] =  e["ci"]
        values["lat"] =  d["lat"]
        values["lon"] =  d["lon"]
        values["address"] =  d["address"]

        #values["time"] = d["time"]

        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #插入
        sql = "insert into lbs  (lon,lat,mmc,mnc,lac,ci,adress) values ('%s','%s',%d,%d,%d,%d,'%s') "%(values["lon"],values["lat"],int(values["mcc"]),int(values["mnc"]),int(values["lac"]),int(values["ci"]),values["address"])
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

def pointadd(GPSDataJson,LBS):
    try:
        values = {}
        d=JSONDecoder().decode(GPSDataJson)
        #values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'
        values["IMEI"] = d["IMEI"]
        if LBS:
            values["battery"] = d["battery"]

        values["lon"] =  d["lon"]
        values["lat"] =   d["lat"]
        values["mdate"] =  str(d["date"] + ' ' +d["time"])
        #values["time"] = d["time"]

        #连接
        conn = MySQLdb.connect(host="localhost",user="root",passwd="kingstar",db="gis",charset="utf8")
        cursor = conn.cursor()
        #插入
        if LBS:
            sql = "insert into datapoint (lon,lat,battery,IMEI) values (%s,%s,%s,%s)"%(values["lon"],values["lat"],values["battery"],values["IMEI"])
        else:
            sql = "insert into datapoint (lon,lat,IMEI) values (%s,%s,%s)"%(values["lon"],values["lat"],values["IMEI"])

        print sql
        n = cursor.execute(sql)


    except Exception, e:
        print e
