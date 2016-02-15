# -*- coding: utf-8 -*-
__author__ = 'Gaoshine'

#导入JSON
import json
import  string
#导入re模块
import re

#测试用GPS上传字串
#mGPS = '*MG201695501000029329,AB&A1816392236917211403248760000180116&X460,0,10170,3872,94;10170,3923,88;10170,3922,94;10170,3873,104;9712,3652,105&B0000000000&G000940&M990&N09&O1000&Z14&T0003#*MG201695501000029329,AH&B0000000000&M990&N09&Z14&T0004#*MG201695501000029329,AB&A1817242236909711403246760000180116&P0460000027ba0f20&B0000000000&G000880&M990&N07&O0900&Z14&T0001#*MG201695501000029329,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000029329,AB&A1818232236916211403248260000180116&X460,0,10170,3872,95;10170,3923,88;10170,3922,97;10170,3873,106;10170,4033,106&B0000000000&G000990&M990&N09&O1000&Z14&T0003#*MG201695501000029329,AH&B0000000000&M990&N08&Z14&T0004#*MG201695501000029329,AB&A1819072236914011403256260000180116&P0460000027ba0f20&B0000000000&G000430&M990&N09&O0600&Z14&T0001#*MG201695501000029329,BQ&number:1,115.29.137.4:2332&T0002#'
#mGPS = '*MG201695501000034717,AB&A1150373636429511428620060011260116&X460,0,12573,63411,48;12573,63412,51;12573,63410,56&B0000000000&G000540&M990&N31&O0800&Z44&T0003#*MG201695501000034717,AH&B0000000000&M990&N31&Z44&T0004#'
mGPS = '*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G000000&M990&N00&O0000&Z00&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G000000&M990&N08&O0000&Z60&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G001050&M990&N08&O0000&Z10&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&A1830232236912811403246260000220116&X460,0,10170,3872,97;10170,3922,99;10170,4033,100;10170,3573,100&B0000000000&G001020&M990&N07&O0900&Z14&T0003#*MG201695501000034550,AH&B0000000000&M990&N07&Z14&T0004#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G001030&M990&N07&O0000&Z40&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&A0935232236909811403238560000230116&X460,0,10170,3872,94;10170,3923,88;10170,4033,95;10170,3922,101;10170,3573,102;9712,3582,105&B0000000000&G001150&M990&N09&O0900&Z44&T0003#'
pattern = re.compile('MG201(\d{15}),AB&A(\d{6})(\d{8})(\d{9})([0-9])(\d{2})(\d{2})(\d{6})',re.IGNORECASE)

info = {}
items = re.findall(pattern,mGPS)
for item in items:
    print 'IMEI:' + item[0],'Time:' +  item[1] ,'lat:' + item[2] ,'lon:' +item[3],item[4],item[5],item[6],'Date:' +item[7]

    lon = item[3]
    lon = string.atof(lon[0:3]) + string.atof(lon[3:5])/60 + string.atof(lon[5:9])/600000
    lat = item[2]
    lat = string.atof(lat[0:2]) + string.atof(lat[2:4])/60 + string.atof(lat[4:8])/600000

    mdate =  item[7]
    mdate = '20' +mdate[4:6] + '-' +  mdate[2:4] + '-' +  mdate[0:2]
    mtime = item[1]
    mtime = mtime[0:2] + ':' + mtime[2:4] + ':' + mtime[4:6]

    info['lat'] =  "%.6f" % lat
    info['lon'] =  "%.6f" % lon
    info['time'] = mtime
    info['date'] = mdate
    info['IMEI'] = item[0]
    #break
#print items

pattern = re.compile('&M(\d{3})',re.S)
items = re.findall(pattern,mGPS)
for item in items:
    #print item[0]+item[1] +'.'+item[2]
    info['battery'] = item[0]+item[1] +'.'+item[2]
    break

jsonStr = json.dumps(info)
print 'GPSDataJson:' + jsonStr