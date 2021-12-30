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
import sys
import json
import time
import requests
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./Main_log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

class Main:
    def __init__(self):
        try:
            self.Config = json.loads(open("./Client_Config.json","r",encoding="utf-8").read())
        except:
            logging.error("config.json not found")
            sys.exit(1)

        #Start Record Monitor
        


if __name__ == "__main__":
    Main()
