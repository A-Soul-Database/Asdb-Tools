"""
        _    ____  ____  ____  
       / \  / ___||  _ \| __ ) 
      / _ \ \___ \| | | |  _ \ 
     / ___ \ ___) | |_| | |_) |
    /_/   \_\____/|____/|____/    workflow V1.0-alpha 

    Liveroom_Monitor (As Status)

    Record_Monitor 获取直播回放 -> video_comment 获取时间轴评论 -> (手动添加某些数据)
    -> 推送请求到字幕服务器 -> Process -> Push
    Dynamtic_Monitor  -> Add Data -> Push

    (Crontab) Comment_Grab 隔一段时间进行评论时间轴获取

    作为常驻进程,一定间隔内检查直播间数据,动态数据和直播时间轴

"""
import logging
import web.app
import sys
import json
from threading import Thread
from Bot.blibot import *
import Bot.blibot.global_var as gl
import time
import requests

Status = {
    "OnLiveList":[],
    "WaitForRecord":[],
    "SubtitleList":{},
    "PushTrigger":[],
    "NecessaryComment":[]
}

"""
Status = {
	"onlive": ["uid1"],
    "WaitForRecord":["uid1"],
    "SubtitleList":
        {
            "bv123":["1","2"] (Pages)
        },
    "PushTrigger":["bv"],
    "NecessaryComment":["bv1","bv2"]
    #全部轴,用于区分日常维护轴
}

{uid}_LiveDetail -> result in liveroom_monitor
{uid}_Dynamtics -> ...
"""

class Main:
    def __init__(self):
        try:
            self.config = json.loads(open("./config.json","r",encoding="utf-8").read())
        except:
            print("config.json not found")
            sys.exit(1)

        logging.info('trying to start ALL SERVICES ')
        try:
            logging.info('trying to start web interface')
            #web.app.app.run()
        except Exception as e:
            logging.error(e)
            logging.error('web interface start failed')
            exit()

        try:
            logging.info('trying to start monitors')
            Liveroom_Monitor_Thread = Thread(target=liveroom_Monitor.Liveroom_Bot,kwargs={"uid":self.config["bot"]["blibot"]["liveroom_monitor"]['uid'],"interval":self.config["bot"]["blibot"]["liveroom_monitor"]['interval']})
            Liveroom_Monitor_Thread.start()
            Status["Servers"].append("liveroom_Monitor_Thread")
            gl.set('Status',Status)
        except Exception as e:
            logging.error(e)
            logging.error('liveroom_Monitor start failed')
            exit()

        while True:
            time.sleep(self.config['interval'])
            if len(Status['OnSchdule']):
                try:
                    logging.info('trying to start Record_Monitor')
                    Trigger_Thread = Thread(target=Record_Monitor.Record_Bot,kwargs={"uid":Status["Record_monitor"]["uid"],"interval":self.config["bot"]["blibot"]["record_monitor"]['interval']})
                    Trigger_Thread.start()
                except:
                    logging.error('Record_Monitor start failed')
                    exit()
            
            if len(Status["SubtitleList"]):
                try:
                    for i in Status["SubtitleList"].keys():
                        url = f"{self.config['subtitle_server']}/addItem"
                        paras = {
                            "token":self.config['subtitle_server_token'],
                            "bv":i,
                            "p":','.join(Status["SubtitleList"][i]),
                            "type":"json"
                            #p的调用为 1,2 现在是["1","2"]
                        }
                        if len(self.config['subtitle_server_token']) == 0:
                            del paras['token']
                        SubThread = Thread(target=SubMonitor.SubMonitor,kwargs={"url":url,"paras":paras})
                        SubThread.start()

                except Exception as e:
                    logging.error(e)
                    logging.error('subtitle_server addItem failed')
                    exit()

            if len(Status["PushTrigger"]):
                pass


Main()