"""
        _    ____  ____  ____  
       / \  / ___||  _ \| __ ) 
      / _ \ \___ \| | | |  _ \ 
     / ___ \ ___) | |_| | |_) |
    /_/   \_\____/|____/|____/    workflow Version V2.0.0-alpha 


    Asdb自动化服务客户端.
        Services 下的所有服务都可进行分布式部署,分布式部署时请注意端口开放及Ip绑定
        请注意版本对应

"""
import services
import time
import requests
from threading import Thread
import random
import os


Lists = {}
Got_Bv = []

#### __init Got_Bv
def __init__Got_Bv():
    global Got_Bv
    Source = "https://cdn.jsdelivr.net/gh/A-Soul-Database/A-Soul-Data@latest/"
    Main_Json = requests.get(f"{Source}/db/main.json").json()["LiveClip"]
    for i in Main_Json:
        Got_Bv += requests.get(f"{Source}/db/{i}/indexer.json").json()

class Single_Operation:
    def __init__(self,Latest_bv:str):
        # Get Latest Bv id
        self.bv = Latest_bv
        self.Change_Status(f"Start Processing {Latest_bv}")
        #Cp.Apply_Srt(Latest_bv)
        #self.Change_Status("Applied_Srt")
        filename = services.Components.Download_Bili_Video(Latest_bv,"./tmp_Video")["data"]["files"]
        self.Change_Status("Got_Download_Video")
        Objects = services.Components.Apply_detection("./tmp_Video",filename)
        self.Change_Status(f"Finished Object Detect. With result {Objects}")
        services.Components.JsonGenerator(Latest_bv,Objects)
        #TimeLine = Cp.Timeline_Monitor(Latest_bv)["data"]["rolls"]
        #self.Change_Status("Got Timeline")
        #Cp.Get_Srt_Result(bv)
        #Process.Auto()

    def Change_Status(self,status:str):
        Lists[self.bv]["Stage"] = status
        print(f"{self.bv} : {Lists[self.bv]}")

if __name__ == "__main__":
    #__init__Got_Bv()
    ### For Test Only
    Latest_bv = "BV1f34y1i7tT"
    Lists[Latest_bv] = {"Status":"Running","Start_Time":int(time.time()),"Stage":"Initializing"}
    Thread(target=Single_Operation,args=(Latest_bv,)).start()
    while 0:
        Latest_bv = services.Components.Record_Monitor()["data"]["Bv"]
        if Latest_bv not in Got_Bv and Latest_bv not in Lists.keys():
            Thread(target=Single_Operation,args=(Latest_bv,)).start()
            Lists[Latest_bv] = {"Status":"Running","Start_Time":time.time(),"Stage":"Initializing"}
            time.sleep(random.randint(3,5))