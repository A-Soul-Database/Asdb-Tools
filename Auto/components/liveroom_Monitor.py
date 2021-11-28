"""
是否在直播呢
https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp
"""
import sys
import requests
import time
from threading import Thread
import Bot.blibot.global_var as gl
import logging
Status = gl.get('Status')


class Liveroom_Bot:
    
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        'References':'https://www.bilibili.com/',
    }

    def __init__(self,uid,interval:int=10) -> None:
        self.uid = []
        self.interval = interval
        if type(uid) == str:
            self.uid.append(uid)
        elif type(uid) == list:
            self.uid = uid
        elif type(uid) == int:
            self.uid.append(str(uid))
        else:
            sys.exit("uid type error")
        
        for i in uid:
            t = Thread(target=self.get_live_status,args=(i,))
            t.start()

    def get_live_status(self,uid:str):
        result = {
            "onLive":False,
            "start_time":"",
            "end_time":"",
            "title":"",
        }
        while True:
            url = "https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp".format(uid=uid)
            r = requests.get(url,headers=self.headers)

            if r.json()["data"]["live_room"]["liveStatus"] == 1:
                logging.info("\r{name} {uid} is on streaming with title {title}".format(uid=uid,title=r.json()['data']["live_room"]["title"],name=r.json()["data"]["name"]),end="")
                result["onLive"] = True
                Status["OnLive"].append(uid)
                if len(result["start_time"]) == 0:
                    result["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    result["title"] = r.json()['data']["live_room"]["title"]
            else:
                #logging.info("{name} {uid} is not on streaming".format(uid=uid,name=r.json()["data"]["name"]))
                try:
                    Status["OnLive"].remove(uid)
                except:
                    pass
                if result["onLive"]:
                    Status["WaitForRecord"].append(uid)
                    result["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    logging.info("LiveStream end with result ",result)
                    result["onLive"] = False
                    logging.info("\n")
                    #直播结束
            time.sleep(self.interval)
            gl.set('Status',Status)
            gl.set(f'{uid}_LiveDetail',result)
            

if __name__ == "__main__":
    uid = ["672342685","672328094","351609538","672353429","672346917"]
    a = Liveroom_Bot(uid)