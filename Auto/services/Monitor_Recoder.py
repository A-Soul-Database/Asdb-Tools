# _*_ coding:utf-8 _*_
"""
看看录播是否更新吧！
Asdb Services
Version: V2.0.0-alpha
https://api.bilibili.com/x/space/arc/search?mid={uid}
https://api.bilibili.com/x/web-interface/view?bvid={bvid}
"""
import requests
import time
from threading import Thread,Lock
import datetime
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import logging
### initialize
try:
    import json
    Client_Server = json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["Record_monitor"]["xmlClientHost"]
    host = json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["Record_monitor"]["xmlRpcHost"]
    port = json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["Record_monitor"]["xmlRpcPort"]
except Exception:
    host = "http://localhost"
    Client_Server = "http://127.0.0.1:5002"
    port = 5007

Rpcserver = ServerProxy(Client_Server)
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./logs/RecoderMonitor.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)


headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    'References':'https://www.bilibili.com/',
}

Sended = []
SendedLock = Lock()

def RecordMonitor(uid:str="393396916",interval:int=60) -> None:

    def Monitor():
        url = "https://api.bilibili.com/x/space/arc/search?mid={uid}".format(uid=uid)
        print("Start Monitoring")
        lastBv = ""
        while True:
            r = requests.get(url,headers=headers)
            today = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) #今天0点的时间戳
            for i in r.json()["data"]["list"]["vlist"]:
                if i["created"] < today: #只查看今天的录播
                    break
                
                if "直播录像" in i["title"] and lastBv != i["bvid"]:
                    lastBv = i["bvid"]
                    if lastBv in Sended: #已经发送过信号就不再发送了
                        continue
                    t = Thread(target=Analysis,args=(i["bvid"],))
                    t.start()
                    t.join()
            time.sleep(interval)

        
    def Analysis(bv:str):
        r = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={bvid}".format(bvid=bv),headers=headers)
        Page_Names = []
        Return_Pages = []
        Pages = r.json()["data"]["pages"]
        ForbiddenWords = ["弹幕"]
        double_page = 0
        for i in Pages:
            if any(word in i["part"] for word in ForbiddenWords):
                pass
            else:
                if "上" in i["part"]:
                    double_page = 1
                if "下" in i["part"]:
                    double_page = 2
                Page_Names.append(i["part"])
                Return_Pages.append(i["page"])
            
            
        if double_page == 1:
            time.sleep(interval)
            Analysis(bv)

        Rpcserver.receiveSignal("Record_Monitor",{
            "error":0,
            "data":{
                "BV":bv
            }
        })

        SendedLock.acquire()
        global Sended
        Sended.append(bv)
        SendedLock.release() 
        raise SystemExit #结束线程

    Monitor()

def ping():
    return "pong"

def rpcCall(*args,**kwargs):
    Called = False
    if Called:
        return {"error":1,"msg":"Already Called"}
    Thread(target=RecordMonitor,args=args,kwargs=kwargs).start()
    Called = True
    return {"error":0,"msg":"start success"}

if __name__ == "__main__":
    server = SimpleXMLRPCServer((host,port))
    server.register_function(rpcCall, "RecordMonitor")
    server.register_function(ping, "ping")
    server.serve_forever()