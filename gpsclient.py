# -*- coding: utf-8 -*-
import socket,time

HOST ='127.0.0.1'
PORT = 2332
gps ={}
gps['reg'] ='*MG201695501000034550,AB&A1806143636391211428674060000010316&P04600000311d422c&B0100000000&G002690&M990&N30&O0400&Z34&T0002#'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('Helo')
data = s.recv(1024)
print 'Received', repr(data)
time.sleep(1)
s.sendall(gps['reg'])
data = s.recv(1024)
s.close()
print 'Received', repr(data)