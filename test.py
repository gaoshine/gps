# -*- coding: utf-8 -*-
from gps import decodegps,isheart
from sql import find

#测试用GPS上传字串
#mGPS = '*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G000000&M990&N00&O0000&Z00&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G000000&M990&N08&O0000&Z60&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G001050&M990&N08&O0000&Z10&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&A1830232236912811403246260000220116&X460,0,10170,3872,97;10170,3922,99;10170,4033,100;10170,3573,100&B0000000000&G001020&M990&N07&O0900&Z14&T0003#*MG201695501000034550,AH&B0000000000&M990&N07&Z14&T0004#*MG201695501000034550,AB&P0460000027ba0f20&B0000000000&G001030&M990&N07&O0000&Z40&T0001#*MG201695501000034550,BQ&number:1,115.29.137.4:2332&T0002#*MG201695501000034550,AB&A0935232236909811403238560000230116&X460,0,10170,3872,94;10170,3923,88;10170,4033,95;10170,3922,101;10170,3573,102;9712,3582,105&B0000000000&G001150&M990&N09&O0900&Z44&T0003#'
mGPS ='*MG200695501000034550,BA&A1811553636369511428655860000010316&X460,0,12573,16940,48;12573,28675,59&B0100000000&G002240&M990&N23&O0300&T0015#*MG201695501000034550,AH&B0000000000&M990&N26&Z34&T0011#'
r = decodegps(mGPS)
print r
r = isheart(mGPS)
print r

find(52)