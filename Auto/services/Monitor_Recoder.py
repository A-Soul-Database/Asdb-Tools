# _*_ coding:utf-8 _*_
"""
看看录播是否更新吧！
https://api.bilibili.com/x/space/arc/search?mid={uid}
https://api.bilibili.com/x/web-interface/view?bvid={bvid}
"""
import requests
import time
from threading import Thread
import datetime
from xmlrpc.client import ServerProxy
import logging

### initialize
try:
    import json
    url = json.loads(open("./Services_Config.json","r","utf-8").read())["liveroom_monitor"]["xmlClientHost"]
except Exception:
    url = "http://127.0.0.1:5002"

Rpcserver = ServerProxy(url)
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


class Record_Bot:

    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        'References':'https://www.bilibili.com/',
    }


    def __init__(self,uid:str="393396916",interval:int=60) -> None:
        self.uid = uid
        self.interval = interval
        #self.Monitor()

    def Monitor(self):
        url = "https://api.bilibili.com/x/space/arc/search?mid={uid}".format(uid=self.uid)
        print("Start Monitoring")
        lastBv = ""
        while True:
            r = requests.get(url,headers=self.headers)
            today = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))
            for i in r.json()["data"]["list"]["vlist"]:
                if i["created"] < today: #只查看今天的录播
                    break

                if "直播录像" in i["title"] and lastBv != i["bvid"]:
                    lastBv = i["bvid"]
                    t = Thread(target=self.Analysis,args=(i["bvid"],))
                    t.start()
            time.sleep(self.interval)

    
    def Analysis(self,bv:str):
        r = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={bvid}".format(bvid=bv),headers=self.headers)
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
            time.sleep(self.interval)
            self.Analysis(bv)
        
        Rpcserver.#调用Rpc的函数返回值
        return Return_Pages

    
if __name__ == "__main__":
    Record_Bot().Monitor()
