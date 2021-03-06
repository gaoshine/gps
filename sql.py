# -*- coding: utf-8 -*-
# mysqldb
import time, MySQLdb
import json
from json import *
import logging


def findlbs(LBSDataJson):
    try:
        d = JSONDecoder().decode(LBSDataJson)
        mcc = d["mcc"]
        mnc = d["mnc"]
        lac = d["lac"]
        ci = d["ci"]
        imei = d["IMEI"]
        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 查询
        sql = "select * from  lbs where mmc=%d and mnc=%d and lac=%d and ci=%d" % (
        int(mcc), int(mnc), int(lac), int(ci))
        print sql
        n = cursor.execute(sql)
        row = cursor.fetchone()
        desc = cursor.description
        if row:
            # print row[5],row[6],row[7]
            # {"errcode":0, "lat":"36.602612", "lon":"114.478172", "radius":"214", "address":"河北省邯郸市邯山区火磨街道东方新天地2号楼;火磨街与陵西南大街路口西北77米"}
            r = '{"errcode":0, "IMEI":"%s", "lat":"%s", "lon":"%s", "address":"%s"}' % (imei, row[5], row[6], row[7])

        else:
            r = False
        return r

    except Exception, e:
        logging.warning("findlbs()  error in %s", e)


def lbsadd(GPSDataJson, LBSDataJson):
    try:
        values = {}
        d = JSONDecoder().decode(LBSDataJson)
        e = JSONDecoder().decode(GPSDataJson)
        # values['GPSDataJson'] = '{"errcode":0, "lat":"36.602612", "lon":"114.478172", "radius":"214", "address":"河北省邯郸市邯山区火磨街道东方新天地2号楼;火磨街与陵西南大街路口西北77米"}'
        values["mcc"] = e["mcc"]
        values["mnc"] = e["mnc"]
        values["lac"] = e["lac"]
        values["ci"] = e["ci"]
        values["lat"] = d["lat"]
        values["lon"] = d["lon"]
        values["address"] = d["address"]

        # values["time"] = d["time"]

        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 插入
        sql = "insert into lbs  (lon,lat,mmc,mnc,lac,ci,adress) values ('%s','%s',%d,%d,%d,%d,'%s') " % (
        values["lon"], values["lat"], int(values["mcc"]), int(values["mnc"]), int(values["lac"]), int(values["ci"]),
        values["address"])
        print 'lbsadd sql:  %s \n' % sql
        n = cursor.execute(sql)


    except Exception, e:
        print 'lbsadd errcode: %s \n' % e


def find(imei):
    try:
        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 查询
        n = cursor.execute("select * from datapoint where IMEI='%s'" % imei)
        for row in cursor.fetchall():
            print row[0], row[1], row[2]

    except Exception, e:
        print e


def pointadd(GPSDataJson, LBS):
    try:
        values = {}
        d = JSONDecoder().decode(GPSDataJson)
        # values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'
        values["IMEI"] = d["IMEI"]
        if LBS:
            values["battery"] = d["battery"]
            values["velocity"] = d["velocity"]
            values["direction"] = d["direction"]
            # values["mdate"] =  str(d["date"] + ' ' +d["time"])

        else:
            values["battery"] = "-1"
            # values["mdate"] =  str(d["date"] + ' ' +d["time"])

        values["lon"] = d["lon"]
        values["lat"] = d["lat"]



        # values["time"] = d["time"]

        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 插入
        if not  LBS:
            sql = "insert into datapoint (lon,lat,battery,IMEI) values (%s,%s,%s,%s)" % (
            values["lon"], values["lat"], values["battery"], values["IMEI"])
        else:
            sql = "insert into datapoint (lon,lat,battery,IMEI,velocity,direction) values (%s,%s,%s,%s,%s,%s)" % (
            values["lon"], values["lat"], values["battery"], values["IMEI"],values["velocity"],values["direction"])

        print 'pointadd sql: ',sql
        n = cursor.execute(sql)

        #把数据再向设备表里再写一遍
        if not LBS:
            sql = "update device set lon=\"%s\", lat =\"%s\" ,battery =%s  , address=\"\"  where imei=\"%s\" "  % ( values["lon"], values["lat"], values["battery"], values["IMEI"])
        else:
            sql = "update device set lon=\"%s\", lat =\"%s\" ,battery =%s ,velocity=\"%s\" , direction=\"%s\" , address=\"\"  where imei=\"%s\" "  % ( values["lon"], values["lat"], values["battery"],values["velocity"],values["direction"], values["IMEI"])

        print "into device: ",sql
        n = cursor.execute(sql)


        


    except Exception, e:
        print 'pointadd error in: ', e

#判断新接入的设备(imei),如果数据库里没有就添加上
def deviceadd(imei):
    try:
        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 查询
        sql =  "select * from device where IMEI = '%s' " % imei
        n = cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            # 插入
            sql = "insert into device (imei,isused) values (%s,%d)" % (imei,False)
            n = cursor.execute(sql)
            print "deviceadd  ",sql,"\n"
        else:
            pass     
        rd1 =  True
    except Exception,e:
        print 'deviceadd error in:', e
        rd1 = False

    try:
        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="logistics", charset="utf8")
        cursor = conn.cursor()
        # 查询
        sql =  "select * from ksoa_gps  where IMEI = '%s' " % imei
        n = cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            # 插入
            sql = "insert into ksoa_gps  (imei,isused) values (%s,%d)" % (imei,False)
            n = cursor.execute(sql)
        print "'deviceadd ksoa_gps  ",sql
        rd2 =  True
    except Exception,e:
        print 'deviceadd ksoa_gps error in:', e
        rd2 = False

    if (rd1 == True and rd2 == True):
        return True
    else:
        return False

#判断接入的设备(imei)的命令指令
def devicecmd(imei):
    cmdstr = ''
    r = ''
    try:
        # 连接
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 查询
        sql =  "select * from device where IMEI = '%s' " % imei
        n = cursor.execute(sql)
        print  sql
        row = cursor.fetchone()
        if  row:
            #
            cmdstr = row[15]
            sql = "update  device set cmdstr='' where  IMEI='%s'  " % imei
            n = cursor.execute(sql)
            print "devicecmd  ",sql,"\n"
        else:
            pass
        r =  cmdstr
    except Exception,e:
        print 'devicecmd error in:', e
        r = False
    return r


