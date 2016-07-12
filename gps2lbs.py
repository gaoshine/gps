# -*- coding: utf-8 -*-
# mysqldb
import time, MySQLdb
import json
from json import *
import logging
#引用urllib2库
import urllib
import urllib2
import re
from threading import Timer 


#判断新接入的设备(imei),如果数据库里没有就添加上
def deviceaddress():
    lat = ''
    lon = ''
    imei = ''
    address = ''
    print 'deviceaddress: \n'
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="gis", charset="utf8")
        cursor = conn.cursor()
        # 查询
        sql =  "select * from device where address = '' and lat <>''  " 
        n = cursor.execute(sql)
        row = cursor.fetchone()
        if  row:
            #更新
            lat = row[4]
            lon = row[3]
            imei =row[1]

            address =  baidugps2address(lon,lat)
            print 'address:',lat,lon,imei,address
            sql = "update  device set address = '%s',lasttime=now()  where  IMEI= '%s' " % (address,imei)
            
            n = cursor.execute(sql)
            print "deviceaddress  ",sql,"\n"
            rd1 =  True
        else:
            rd1 =  False
    except Exception,e:
        print 'deviceaddress error in:', e
        rd1 = False

    if rd1:    
        try:
        # 连接
            conn = MySQLdb.connect(host="localhost", user="root", passwd="kingstar", db="logistics", charset="utf8")
            cursor = conn.cursor()
            # 更新
            sql = "update  ksoa_gps set address = '%s'  where  IMEI= '%s' " % (address,imei)
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


def baidugps2address(lon,lat):
    values = {}
    #http://api.map.baidu.com/geocoder/v2/?ak=E4805d16520de693a3fe707cdc962045&callback=renderReverse&location=39.983424,116.322987&output=json&pois=1
    #http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924;114.21892734521,29.575429778924&ak=C272f5eb78abb8c1ad9b0df264e000c8&output=json
    try:

        #values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'

        values["output"] =  'json'
        #values["callback"] =  'renderReverse'

        values["ak"] = 'C272f5eb78abb8c1ad9b0df264e000c8'
        values["location"] =  str(lat) + ',' + str(lon)

        data = urllib.urlencode(values)

        url = "http://api.map.baidu.com/geocoder/v2"

        geturl = url + "/?"+data
        #print geturl
        request = urllib2.Request(geturl)
        response = urllib2.urlopen(request)
        r =response.read()
        print r

        s = json.loads(r)
        return s["result"]["formatted_address"]
    except Exception,ex:
        print 'error',':',ex

def timer(n):
    while True:
        print time.strftime('%Y-%m-%d %X',time.localtime())
        deviceaddress()
        time.sleep(n)



if __name__ == '__main__':

    timer(15)
