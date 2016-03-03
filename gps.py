# -*- coding: utf-8 -*-
# GPS服务器端代码,负责接收GPS设备上报的数据和下发命令指令,负责接收GPS上传信息并整理后在发送给指定的API1

import time, socket, threading
# 导入JSON
import json
import string
# 导入re模块
import re
from jsonpost import jsonpost, baidugps


def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        #心跳和注册报文
        if isheart(data):
            sock.send('*MG20,YAH#')
        if islogin(data):
            sock.send('*MG20,YAB#')

        jsonpost(decodegps(data))
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
        break
    if (x + y) < 1:
        return
    d = baidugps(x, y)  #百度和gps坐标转换
    print d
    print d[0]['x'], d[0]['y']
    info['lon'] = d[0]['x']
    info['lat'] = d[0]['y']

    # print items

    pattern = re.compile('&M(\d{3})', re.S)
    items = re.findall(pattern, mGPS)
    for item in items:
        # print item[0]+item[1] +'.'+item[2]
        info['battery'] = item[0] + item[1] + '.' + item[2]
        break

    jsonStr = json.dumps(info)
    # print jsonStr
    return jsonStr

#u判断是否是心跳包
def isheart(mGPS):
    pattern = re.compile('MG201(\d{15}),AH&B', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items :
        jsonStr = True
    else:
        jsonStr = False
    # print jsonStr
    return jsonStr

#u判断是否是登陆包
def islogin(mGPS):
    pattern = re.compile('MG201(\d{15}),AB&A', re.IGNORECASE)
    items = re.findall(pattern, mGPS)
    if items :
        jsonStr = True
    else:
        jsonStr = False
    # print jsonStr
    return jsonStr




if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('0.0.0.0', 2332))
    s.listen(5)
    print 'Waiting for connection...'
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
