# -*- coding: utf-8 -*-
__author__ = 'Gaoshine'

#引用urllib2库
import urllib
import urllib2
import json
from json import *

def jsonpost(GPSDataJson):
    values = {}
    #values['APIkey'] = 'Kingstar_6161266'
    #d =  {"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}
    try:
        d=JSONDecoder().decode(GPSDataJson)
        #values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'
        values["IMEI"] = d["IMEI"]
        values["battery"] = d["battery"]
        values["lon"] =  d["lon"]
        values["lat"] =  d["lat"]
        values["date"] =  d["date"]
        values["time"] = d["time"]

        data = urllib.urlencode(values)
        #data = 'GPSDataJson={"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'

        url = "http://page.kingstars.cn/index.php?m=Api&a=index"
        geturl = url + "&"+data
        print geturl
        request = urllib2.Request(geturl)
        response = urllib2.urlopen(request)
        r =response.read()
        print r
        #s = json.loads(r)
        #print s['status']
    except Exception,ex:
        print 'error',':',ex


def baidugps(lon,lat):
    values = {}
    #http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924;114.21892734521,29.575429778924&ak=C272f5eb78abb8c1ad9b0df264e000c8&output=json
    try:

        #values['GPSDataJson'] = '{"IMEI": "695501000029329", "battery": "99.0", "lon": "114.054145", "date": "2016-01-18", "time": "18:16:39", "lat": "22.615287"}'

        values["output"] =  'json'
        values["ak"] = 'C272f5eb78abb8c1ad9b0df264e000c8'
        values["coords"] =  str(lon) + ',' + str(lat)

        data = urllib.urlencode(values)

        url = "http://api.map.baidu.com/geoconv/v1"
        geturl = url + "/?"+data
        #print geturl
        request = urllib2.Request(geturl)
        response = urllib2.urlopen(request)
        r =response.read()
        #d=JSONDecoder().decode(r)
        #return d["result"]
        s = json.loads(r)
        return s["result"]
    except Exception,ex:
        print 'error',':',ex



def lbs(mcc,mnc,lac,ci):
    values = {}
    # LBS接口：http://api.cellocation.com/cell/?mcc=460&mnc=0&lac=12573&ci=63441&output=json
    try:

        values["output"] =  'json'
        values["mcc"] = mcc
        values["mnc"] = mnc
        values["ci"] = ci
        values["lac"] = lac

        data = urllib.urlencode(values)

        url = "http://api.cellocation.com/cell"
        geturl = url + "/?"+data
        print geturl
        request = urllib2.Request(geturl)
        response = urllib2.urlopen(request)
        r =response.read()
        d=JSONDecoder().decode(r)
        print d['errcode'],d['address']
        #return d["result"]
        #s = json.loads(r)
        #return s["result"]
        return r

    except Exception,ex:
        print 'error',':',ex
