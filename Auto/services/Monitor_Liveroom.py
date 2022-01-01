# _*_ coding:utf-8 _*_
"""
是否在直播呢
Asdb Services
Version V2.0.0 - alpha
https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp
"""
import json
import requests
import time
from threading import Thread
import logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./logs/LiveroomMonitor.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

try:
    port = int(json.loads(open("./Services_Config.json","r","utf-8").read())["liveroom_monitor"]["xmlRpcPort"])
    host = json.loads(open("./Services_Config.json","r","utf-8").read())["liveroom_monitor"]["xmlRpcHost"]
    Client_Server = json.loads(open("./Services_Config.json","r","utf-8").read())["liveroom_monitor"]["xmlClientHost"]
except:
    port = 5005
    Client_Server = "http://localhost:5002"

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    'References':'https://www.bilibili.com/',
}

def Liveroom_Bot(uid:list=["672342685","672328094","351609538","672353429","672346917"],interval:int=60,mode:int=1) -> None:
    """
        mode:
            0: 在开播和下播时才会发送消息
            1: 每隔interval send message
    """
    def get_live_status(uid:str):
        On_Live = False
        Send = bool(mode)
        while True:
            url = "https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp".format(uid=uid)
            r = requests.get(url,headers=headers)
            if r.json()["data"]["live_room"]["liveStatus"] == 1:
                #开播
                Send = On_Live == False and bool(mode)==False if bool(mode) == False else True #开播发送信息 (我也不知道在写什么,总之能运行就是了)
                On_Live = True   
            elif r.json()["data"]["live_room"]["liveStatus"] == 0 and On_Live:
                #直播结束
                Send = True #下播发送信息
                On_Live = False
            if Send:
                ServerProxy(Client_Server).receiveSignal("Liveroom_Monitor",{"error":0,"data":{"uid":uid,"info":r.json()["data"]["live_room"],"On_Live":On_Live}}) #直接扔所有信息过去,没必要在这里整合,使其耦合度增加
            Send = bool(mode)
            time.sleep(interval)

    for i in uid:
        t = Thread(target=get_live_status,args=(i,))
        t.start()

def rpcCall(*args,**kwargs):
    Called = False
    if Called:
        return {"error":1,"msg":"Already Called"}
    Thread(target=Liveroom_Bot,args=args,kwargs=kwargs).start()
    Called = True
    return {"error":0,"msg":"start success"}


def ping():
    return "pong"

if __name__ == "__main__":
    """
    uid = ["672342685","672328094","351609538","672353429","672346917"]
    a = Liveroom_Bot(uid)
    """

    server = SimpleXMLRPCServer((host, port))  # 如果进行分布式访问,请务必将localhost改为Ip地址(或localhost)
    server.register_function(rpcCall,"Liveroom_Bot")
    server.register_function(ping)
    server.serve_forever()