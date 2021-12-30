# _*_ coding:utf-8 _*_
"""
Bili 视频下载
bv:str 
p:list
qn{
    16: 360P mp4
    32: 480P flv
    64: 720P flv
    ------ 以下需要登录Cookies才能下载
    80: 1080P flv
    116: 1080P60F flv
}
"""
import requests
from contextlib import closing
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./logs/BiliViodeoDownloadr.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2','./',)

def Download_Bili_Video(bv:str,p:list=[],qn:str="16",path:str="") -> bool:
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Referer":"https://www.bilibili.com/",
    }

    def Get_Info(p)->dict:
        """
            获取视频分P等信息
        """
        Bili_Video_Info_Api = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
        Bili_Video_Info_Json = requests.get(Bili_Video_Info_Api,headers=headers).json()

        if len(Bili_Video_Info_Json["data"]["pages"]) < len(p) or len(p)==0:
            #print("请求的分P数大于视频分P数或未指定分P,下载全部分P")
            p = [str(i) for i in range(1,len(Bili_Video_Info_Json["data"]["pages"])+1)]
            
        infos = {
            "bv":bv,
            "cover":Bili_Video_Info_Json["data"]["pic"],
            "title":Bili_Video_Info_Json["data"]["title"],
            "p":[],
        }
        rolling = p[:]
        for i in rolling:
            #循环获得每个分P的信息格式 ["分P","Cid","名字(P1 录播/)"]
            if "弹幕" in Bili_Video_Info_Json["data"]["pages"][int(i)-1]["part"]:
                p.remove(i)
            else:
                infos["p"].append([i, Bili_Video_Info_Json["data"]["pages"][int(i)-1]["cid"], Bili_Video_Info_Json["data"]["pages"][int(i)-1]["part"] ])
                #Asdb 特有:去除带有 【弹幕】 的所有分P
        return infos

    def Video_Download(infos:dict)->bool:
        """
            下载视频
        """
        def down(url,name)->bool:
            #下载单个视频的函数
            with closing(requests.session().get(url,headers=headers,stream=True)) as response:
                chunk_size = 1024
                with open(f"components/tmp/{path}{name}", "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                logging.info(f"{name} 下载完成")
            return True
        result = False
        formats = "mp4" if qn == "16" else "flv"
        p = 1
        for i in range(len(infos["p"])):
            url = f"https://api.bilibili.com/x/player/playurl?bvid={infos['bv']}&cid={infos['p'][i][1]}&qn={qn}&otype=json"
            Video_Info_Json = requests.get(url,headers=headers).json()
            Video_Durl = Video_Info_Json["data"]["durl"][0]["url"]
            name = infos["bv"] if len(infos["p"]) == 1 else f"{infos['bv']}-{str(p)}"
            p+=1
            Video_Name = f"{name}.{formats}"
            logging.info(Video_Name)
            result = down(Video_Durl,Video_Name)
                
        return result

    return Video_Download(Get_Info(p))


try:
    import json
    port = int(json.loads(open("./Services_Config.json","r","utf-8").read())["BiliVideoDownloader"]["xmlRpcPort"])
except Exception:
    port = 5008 #默认端口5008

BiliVideoDownloadServier = SimpleXMLRPCServer(("localhost", port))
BiliVideoDownloadServier.register_function(Download_Bili_Video, "Download_Bili_Video")
BiliVideoDownloadServier.serve_forever()
