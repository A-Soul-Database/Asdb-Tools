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
import logging
import sys
import json
from xmlrpc import server
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

try:
    Config = json.loads(open("./Client_Config.json","r",encoding="utf-8").read())
except:
    logger.error("请检查配置文件是否存在或配置文件是否正确")
    sys.exit(0)
RpcServer = SimpleXMLRPCServer((Config["xmlRpcHost"],Config["xmlRpcPort"]))


def receiveSignal(service:str,info:dict):
    """
    接收xmlrpc消息
    service: ["Liveroom_Monitor","Record_Monitor","Dynamtic_Monitor"]
    info:{
        error:0/1,
        data:{}
    }
    """
    logging.error(f"erro : {service}:{info}") if info["error"] else logging.info(f"{service}:{info}")


def _init_necessary_Services():

    #启动直播爬虫和录播爬虫
    """
    result = ServerProxy(Config["bot"]["Record_monitor"]["xmlRpc"]).RecordMonitor()
    logging.error(f"error : {result}") if result["error"] else logging.info(f"{result}")
    """
    print(Config)
    result = ServerProxy(Config["bot"]["liveroom_monitor"]["xmlRpc"]).Liveroom_Bot()
    logging.error(f"error : {result}") if result["error"] else logging.info(f"{result}")


if __name__ == "__main__":
    _init_necessary_Services()
    RpcServer.register_function(receiveSignal, "receiveSignal")
    RpcServer.serve_forever()