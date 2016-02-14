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
