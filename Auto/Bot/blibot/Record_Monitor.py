"""
看看录播是否更新吧！
https://api.bilibili.com/x/space/arc/search?mid={uid}
https://api.bilibili.com/x/web-interface/view?bvid={bvid}
"""
import requests
import time
import Bot.blibot.global_var as gl
from threading import Thread
class Record_Bot:
    LiveroomToUid = {
        "672346917":"22625025","672353429":"22632424","351609538":"22634198","672328094":"22637261",
        "672342685":"22625027","703007996":"22632157"
    }

    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        'References':'https://www.bilibili.com/',
    }

    def __init__(self,uid:str="393396916",interval:int=10) -> None:
        self.uid = uid
        self.interval = interval
        self.Monitor()

    def Monitor(self):
        url = "https://api.bilibili.com/x/space/arc/search?mid={uid}".format(uid=self.uid)
        latest_Bv = ""
        latest_title = ""
        while True:
            r = requests.get(url,headers=self.headers)
            if latest_Bv == "" or latest_title == "":
                latest_Bv = r.json()["data"]["list"]["vlist"][0]["bvid"]
                latest_title = r.json()["data"]["list"]["vlist"][0]["title"]
            else:
                if r.json()["data"]["list"]["vlist"][0]["bvid"] != latest_Bv:
                    latest_Bv = r.json()["data"]["list"]["vlist"][0]["bvid"]
                    latest_title = r.json()["data"]["list"]["vlist"][0]["title"]
                    if "直播录像" in latest_title:
                        t = Thread(target=self.Analysis,args=(latest_Bv,))
                        t.start()
            time.sleep(self.interval)
            if len(gl.get('Status')['WaitForRecord']) == 0:
                #终止线程
                break
    
    def Analysis(self,bv:str):
        r = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={bvid}".format(bv=bv),headers=self.headers)
        returning_Ps = []
        Pages = r.json()["data"]["pages"]
        ForbiddenWords = ["弹幕"]
        for i in Pages:
            if any(word in i["part"] for word in ForbiddenWords):
                pass
            else:
                returning_Ps.append([i["part"],i["page"]])
                
        if ("上" in returning_Ps) and ("下" not in returning_Ps):
            time.sleep(self.interval)
            self.Analysis(bv)
        
        return returning_Ps
if __name__ == "__main__":
    Record_Bot()