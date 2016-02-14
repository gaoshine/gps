# -*- coding: utf-8 -*-
# GPS服务器端代码,负责接收GPS设备上报的数据和下发命令指令,负责接收GPS上传信息并整理后在发送给指定的API

import time, socket, threading

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        mlog('gps',data)
        print 'Rev:%s' % data
        if data == 'exit' or not data:
            break
	    sock.send('OK')
    sock.close()
    print 'Connection from %s:%s closed.' % addr

def mlog(TAG,txt):
    f = open('gps.log','a')
    localtime = time.asctime(time.localtime(time.time()))
    f.write(TAG + '/' + localtime + '/' + txt)
    f.close()

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


