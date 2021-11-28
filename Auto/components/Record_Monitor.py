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
        "22625025":"672346917","22632424":"672353429","22634198":"351609538","22637261":"672328094"
        ,"22625027":"672342685","22632157":"703007996"
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
        Page_Names = []
        Return_Pages = []
        Pages = r.json()["data"]["pages"]
        ForbiddenWords = ["弹幕"]
        for i in Pages:
            if any(word in i["part"] for word in ForbiddenWords):
                pass
            else:
                Page_Names.append(i["part"])
                Return_Pages.append(i["page"])
                
        if ("上" in Page_Names) and ("下" not in Page_Names):
            time.sleep(self.interval)
            self.Analysis(bv)

        Liveroom_Id = r.json()['data']['desc'].split("\n")[0].replace("https://live.bilibili.com/","").replace("/","")
        WaitForRecord = gl.get('WaitForRecord')
        WaitForRecord.remove(self.LiveroomToUid[Liveroom_Id])
        gl.set('WaitForRecord',WaitForRecord)
        #说明已有录播,删除队列任务
        SubList = gl.get('SubtitleList')
        SubList[bv] = Return_Pages
        gl.set('SubtitleList',SubList)
        #添加任务到字幕队列和评论获取队列
        NecessaryCommentList = gl.get('NecessaryComment')
        NecessaryCommentList.append(bv)
        gl.set('NecessaryComment',NecessaryCommentList)
        #添加任务到评论获取队列
        #线程结束
        return Return_Pages


if __name__ == "__main__":
    Record_Bot()