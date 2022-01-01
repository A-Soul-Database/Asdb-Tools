# Asdb自动化服务 Asdb Auto Services 
使用 `XmlRpc` 与进行沟通. 允许分布式部署
#### 结构 Structures
```struct
    -- logs 日志文件
    -- Down_Bili_Video.py   BiliBili视频下载
    -- Monitor_Liveroom.py  直播监控
    -- Monitor_Recoder.py   录播监控
    -- Process.py           文件处理
    -- Spider_TimeLine.py   时间轴爬取及校对
    -- Services_Config.json 服务配置文件
```

#### 设计
在`Client.py`中存在着`receiveSignal()`函数,用于处理各种信息作为触发器。规范格式如下

```RemoteCall
    service: ["Liveroom_Monitor","Record_Monitor","Dynamtic_Monitor","Download_Bili_Video"] #调用名,用于触发器
    info:{
        error:0/1,
        data:{}
    }
```
调用驻留服务时有两个函数 `rpcCall()` 及 `ping()`, 以 `Monitor_Liveroom.py` 为例,改服务不存在传参问题(For Asdb,若用于其他服务,请酌情修改结构),且不适用于多重调用,阻塞时为了防止超时  
故在设计时`RpcCall()` 会新开线程处理,确保后台服务正常运行可调用`ping()` 函数。  
返回时会直接调用 `receiveSignal()`,会`raise SystemExit`结束线程。  