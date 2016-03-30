# -*- coding: utf-8 -*-
# GPS服务器端代码,负责接收GPS设备上报的数据和下发命令指令,负责接收GPS上传信息并整理后在发送给指定的API1

import time, socket, threading
# 导入JSON
import json
import string
# 导入re模块
import re
from jsonpost import jsonpost, baidugps, lbs
from sql import find, pointadd, findlbs, lbsadd,deviceadd,devicecmd


def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        # 心跳和注册报文
        if isheart(data):
            print 'isheart \n'
            sock.send('*MG20YAH#')
            r = setmode(data)
            print '\nsetmode :',r,'\n' 
            if not (r == False):
               time.sleep(1)
               sock.send(r)
               #pass
               #r = '*MG2011GB0900,3#'
               #r = '*MG2011AH(P0,0,0)#'
               #time.sleep(3)
               #sock.send(r)
        if islogin(data):
            print 'islogin \n' 
            t = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            s = '*MG20YAB#*MG2011DE(%s)#' % t            
            sock.send(s)            
        # 解码GPS上传信息
        r = decodegps(data)
        if r != False:
            # 写入数据库
            pointadd(r, True)
            # 发送给API(写入车辆管理的定位数据)
            jsonpost(r, True)

        # 解码LBS上传信息
        r = getLBS(data)
        print 'getLBS result: %s \n' % r
        if r != False:
            # 判断
            r2 = findlbs(r)
            if r2 == False:
                r0 = lbs(r)
                lbsadd(r, r0)
                r2 = r0
            # 写入数据库
            pointadd(r2, False)
            # 发送给API(写入车辆管理的定位数据)
            jsonpost(r2, False)
        
        r = isstatus(data)
        print r
        mlog('gps', data)
        print 'Rev:%s' % data
        if data == 'exit' or not data:
            break
            sock.send('OK')
    sock.close()
    print 'Connection from %s:%s closed.' % addr


def mlog(TAG, txt):
    f = open('gps.log', 'a')
    localtime = time.asctime(time.localtime(time.time()))
    f.write(TAG + '/' + localtime + '/' + txt)
    f.close()


def decodegps(mGPS):
    pattern = re.compile('MG200(\d{15}),BA&A(\d{6})(\d{8})(\d{9})([0-9])(\d{2})(\d{2})(\d{6})', re.IGNORECASE)
    x = 0.0
    y = 0.0
    info = {}
    items = re.findall(pattern, mGPS)
    for item in items:
        print 'IMEI:' + item[0], 'Time:' + item[1], 'lat:' + item[2], 'lon:' + item[3], item[4], item[5], item[
            6], 'Date:' + item[7]

        lon = item[3]
        lon = string.atof(lon[0:3]) + string.atof(lon[3:5]) / 60 + string.atof(lon[5:9]) / 600000
        lat = item[2]
        lat = string.atof(lat[0:2]) + string.atof(lat[2:4]) / 60 + string.atof(lat[4:8]) / 600000

        mdate = item[7]
        mdate = '20' + mdate[4:6] + '-' + mdate[2:4] + '-' + mdate[0:2]
        mtime = item[1]
        mtime = mtime[0:2] + ':' + mtime[2:4] + ':' + mtime[4:6]
        x = lon
        y = lat
        info['lat'] = "%.6f" % lat
        info['lon'] = "%.6f" % lon
        info['time'] = mtime
        info['date'] = mdate
        info['IMEI'] = item[0]
        info['velocity'] = item[5]
        info['direction'] = item[6]
        break
    if (x + y) < 1:
        return False
    d = baidugps(x, y)  # 百度和gps坐标转换
    print d
    print d[0]['x'], d[0]['y']
    info['lon'] = d[0]['x']
    info['lat'] = d[0]['y']

    # print items
    #读取电池电量
    pattern = re.compile('&M(\d{3})', re.S)
    items = re.findall(pattern, mGPS)
    for item in items:
        # print item[0]+item[1] +'.'+item[2]
        info['battery'] = item[0] + item[1] + '.' + item[2]
        break

    #读取海拔
    pattern = re.compile('&G(\d{6})', re.S)
    items = re.findall(pattern, mGPS)
    for item in items:
        # print item[0]+item[1] +'.'+item[2]
        info['altitude'] = item[0] + item[1] +item[2] + item[3] +item[4] + '.' + item[5]
        break




    #读取方向
   # pattern = re.compile('&M(\d{3})', re.S)
   # items = re.findall(pattern, mGPS)
   # for item in items:
        # print item[0]+item[1] +'.'+item[2]
   #     info['direction'] = item[0] + item[1] + '.' + item[2]
   #     break




    jsonStr = json.dumps(info)
    print jsonStr
    return jsonStr


#  
def setmode(mGPS):
    pattern = re.compile('MG201(\d{15}),AH&B', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items:
        for item in items:
           imei = item
           jsonStr = devicecmd(imei)


        #jsonStr = '*MG2011GB0900,3#'
        #jsonStr = '*MG2011AH(P0,0,0)#'
    else:
        jsonStr = False
    print '\nsetmode: ',jsonStr
    return jsonStr

# u判断是否是心跳包
def isheart(mGPS):
    pattern = re.compile('MG201(\d{15}),AH&B', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items:
        for item in items:
           imei = item
           deviceadd(imei)

        jsonStr = True
    else:
        jsonStr = False
    # print jsonStr
    return jsonStr


# u判断是否是登陆包
def islogin(mGPS):
    pattern = re.compile('MG201(\d{15}),AB&A', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items:
        for item in items:
           imei = item
           deviceadd(imei)

        jsonStr = True
    else:
        jsonStr = False
    # print jsonStr
    return jsonStr



# 判断GSP是登陆包
def isstatus(mGPS):
    pattern = re.compile('MG200(\d+),AJ(.+)#', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items:
        for item in items:
           imei = item[0]
           status = item[1]         

        jsonStr = 'Status: %s,%s'% (imei,status)
    else:
        jsonStr = False
    # print jsonStr
    return jsonStr


def getLBS(mGPS):
    # mGPS = "*MG201695501000034550,AB&X460,0,12991,56417,85;12991,61522,63;12991,61521,70;12390,46707,74;12390,18807,75;12991,31585,76;12991,48010,80&B0000000000&G000580&M990&N13&O0000&Z00&T0003#"
    pattern = re.compile('MG20[01](\d+),(.*)&X(\d+),(\d+),(\d+),(\d+)', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items:
        print 'getLBS X : %s \n' % items
        for item in items:
            # print item[0],item[1],item[2],item[3]
            r = '{"errcode":0, "IMEI":"%s","mcc":"%s", "mnc":"%s", "lac":"%s", "ci":"%s"}' % (
            item[0], item[2], item[3], item[4], item[5])
        jsonStr = r
    else:
        pattern = re.compile('MG20[01](\d+),(.*)&P(\d{4})(\d{4})(\w{4})(\w{4})', re.IGNORECASE)
        items = re.findall(pattern, mGPS)
        print "getLBS P: %s" % items
        if items:
            # print items
            for item in items:
                # print item[0],item[1],item[2],item[3]
                r = '{"errcode":0, "IMEI":"%s","mcc":"%s", "mnc":"%s", "lac":"%s", "ci":"%s"}' % (
                item[0], item[2], item[3], int(item[4], 16), int(item[5], 16))
            jsonStr = r
        else:
            jsonStr = False

    # print jsonStr
    return jsonStr


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('0.0.0.0', 2332))
    s.listen(50)
    print 'Waiting for connection...'
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
