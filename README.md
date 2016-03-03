2016-2-14
采用通用的 T9 GPStracer GPS 跟踪器

GPS服务器端代码
> 通过设定T9 向 IOT.kingstars.cn发送定位数据,服务端通过sock TCP端口</br>
> 获取信息,解码处理后通过API发送数据到物联平台 </br>
> 负责接收GPS设备上报的数据和下发命令指令</br>
> 负责接收GPS上传信息并整理后在发送给指定的API</br>


**T9 GPStracer GPS 跟踪器的指令:**

初始化指令通过绑定手机卡做认证,再通过发送短信进行初始化设定
功能	指令	说明
设置监护人号码	sos,13800138000  

* sos, 	设置成功回复：设备xx监护人手机已设置为:13800138000或设备xx主监护人号码已清空
* 设置失败回复：设备xx主监护人号码设置失败,格式出错
* 碰撞报警开关	zj,0/1	成功：+zj,0/1
* 失败：设备碰撞预警开关设置失败
* 定位方式设置	dwfs,0/1	成功：+DWFS,0/1
* 失败：设置指令出错
* 固定上传时间设置	time,hhmm,times	成功：设备成功设置守候模式下于hhmm点上报，每天上报times次
* 失败：设置指令出错
* 设置设备工作模式	MODE,0/1,0/1,XXXX	MODE,0   省电模式
* MODE,1,0,10  "设备进入跟踪模式，并将在10分钟后自动退出跟踪模式进入到省电模式" 
* MODE,1,1,1000  "设备进入跟踪模式，并将在10:00自动退出跟踪模式进入到省电模式"
* 设置定时回传间隔	ITV,15	成功回复：设备xx 设置位置上报频率是（15秒）
* 失败回复：FAIL
* 修改IP端口	IP1,222076219174,30002	成功回复：设备xx设置服务器和端口号失败。
* 失败回复：设备xx IP设置失败,格式出错
* 查询终端参数	SR	回复：各参数信息
* 恢复出厂设置	CLEAR	回复：终端参数重置成功,请重新设定参数。
* 恢复出厂设置，除IP和端口外，各状态恢复成默认值
* 设置GPS休眠开关	sleep,1	回复：SUCCESS
* 1：开启GPS休眠  0：关闭GPS休眠
* 终端重启	RESET	终端立即重启。
* 电话报警开关	DH,1	1回复：设备%s拨打监护人电话告警通知功能已开启，如需关闭请回复:dh,0
* 0回复：设备%s拨打监护人电话告警通知功能已关闭，如需开启请回复:dh,1
* 短信报警开关	CLOSE,1	回复：SUCCESS
* 0：开启短信报警   1：关闭短信报警
* 超速报警设置	CSBJ,120,1	CSBJ,120,1回复：超速报警开启,最大速度为(公里/小时) : 120
* CSBJ,120,0回复：超速报警关闭。
* 心跳间隔设置	XT,180	回复：SUCCESS
* 短信查车	C	回复：设备当前的位置信息
* 主动呼叫	CALL,13800138000	设备拨打电话13800138000
* 终端版本查询	VER	回复：设备的基础版本及应用版本
* 清空C盘文件	DFILE	所有的参数全部变为出厂设置
* IP列表修改	IPRS,2,183.62.138.13:3000,181.62.138.13:3001	回复：ipreset ok或ipreset fail（最多支持5个IP）
* 
* 查询IP链表	IPLOOK	回复：+iplist,number:n,ip1:port1,ipn:portn


2016-2-18 根据需求加入了百度坐标的转换函数,baidugps(lon,lat) 传入gps的lon,lat 返回json格式的百度坐标(python字典格式)



[20000][*MG20][1][681501000000433] ,[AB&][A][111924][22369121114032465][6][00][00]
[031114][&P][0460000027ba0f52][&B0000000000][&G000960][&M990][&N25][&O03][&Z]
[0][4][&T0001]#

*MG200695501000034550,BA&A1811553636369511428655860000010316&X460,0,12573,16940,48;12573,28675,59&B0100000000&G002240&M990&N23&O0300&T0015#

[*MG20][0][695501000034550],[BA&][A][181155][36363695114286558][6][00][00][010316][&X][460],[0],[12573],[16940],[48];12573,28675,59&B0100000000&G002240&M990&N23&O0300&T0015#

平台收到登录报文要发给设备一条数据：*MG20,YAB
平台收到心跳要发给设备一条数据：*MG20,YAH






