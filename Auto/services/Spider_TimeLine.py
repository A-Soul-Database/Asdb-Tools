"""
Comments.py
BiliBIli 评论爬虫
定时获取时间轴评论
!!!前提是已经有了完整录播
https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=1&oid={av}&mode=0   || root={} 楼中楼,root表示根id pn={} 表示楼中楼的页数
Asdb Auto Services
Version V2.0.0 - alpha
"""
import requests
import time
import re
import logging
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
def Spider_TimeLine(bv:str,uid:list=["53082699"]) -> None:
    def Monitor(interval:int=60)->None:
        """
        每隔interval就可以更新一次
        """
        while True:
            result = GetComments()
            if CalculateAllTime(result):
                print(f"\r{bv}更新成功\n",end="")
                ServerProxy(Client_Server).receiveSignal("TimeLine",{"error":0,"data":{"BV":bv,"Content":result['contents']}})
                raise SystemExit
                break
            else:
                time.sleep(interval)
                GetComments()
            time.sleep(interval)
        return True

    def GetComments()->dict:
        """
        获取评论
            楼中楼:[[]]使用 list嵌套
        """

        def Comments_In_Floor(root:str)->str:
            """
            获取楼中楼(单个)
            """
            step = 1
            result = []
            while True:
                url = f"https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={step}&type=1&oid={av}&root={root}"
                r = requests.get(url,headers=headers)
                if r.json()["data"]["replies"] == None:
                    #没有回复
                    break
                for i in r.json()["data"]["replies"]:
                    if i["member"]["mid"] in uid:
                        result.append(i["content"]["message"])
                step += 1
            return result
            return '\n'.join(result)


        returning = {
            "code":0,
            "uid":uid,
            "contents":[]
        }
        if len(uid) == 0:
            return returning
        else:
            #先看置顶(我也不到置顶会不会在普通评论里占坑)
            r = requests.get(f"https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=1&oid={av}&mode=0",headers=headers)
            try:
                if str(r.json()["data"]["top"]["upper"]["mid"]) in uid:
                    returning["code"] = 1
                    returning["contents"].append(r.json()["data"]["top"]["upper"]["content"]["message"])
                    returning["contents"] += Comments_In_Floor(r.json()["data"]["top"]["upper"]["rpid"])
                    return returning
            except TypeError:
                print("\r没有置顶",end="")
            #再看普通评论
            start = 0
            while True:
                url = f"https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={start}&type=1&oid={av}"
                r = requests.get(url,headers=headers)
                if r.json()["data"]["replies"] == None:
                    break
                for i in r.json()["data"]["replies"]:
                    if str(i["member"]["mid"]) in uid:
                        returning["code"] = 1
                        returning["contents"].append(i["content"]["message"])
                        returning["contents"] += Comments_In_Floor(i["rpid"])
                start += 1
                time.sleep(1)
        return returning


    def CalculateAllTime(result:str):
        """通过轴时间计算是否达到要求"""
        if len(result["contents"]) == 0:
            #说明一个轴都没有,继续loop
            return False
        
        def to_seconds(a):
            return int(a.split(":")[0])*3600+int(a.split(":")[1])*60+int(a.split(":")[2]) if a.count(":") == 3 else int(a.split(":")[0])*60+int(a.split(":")[1]) #hh:mm:ss / mm:ss to second
            
        Comment_All_time = 0 #轴总时间
        
        result["contents"] = [ i for i in result["contents"] if i.count(":") != 0] #没轴的去掉

        for i in result["contents"]:
            #轴可能会包含多个P的情况 P1: 00:00 - 1:00:00 P2: 00:00 - 1:00:00
            i = i.replace("：",":")
            comments_time = re.findall(r'[0-9]*:[0-9]*:[0-9]*',i)
            i = re.sub(r'[0-9]*:[0-9]*:[0-9]*',"",i) #替换回去,以免下面出现重复提取
            comments_time += re.findall(r'[0-9]*:[0-9]*',i)
            comments_time = [fn for fn in comments_time if fn != ":"] #去除 : 单独的行数
            ### 开始计算时间
            Comment_All_time += to_seconds(comments_time[-1]) - to_seconds(comments_time[0])
        
        result["contents"].reverse() #处理之后的时间顺序需要反转

        if Comment_All_time > duration*0.8:
            #说明轴已经达到了所有分P的80%,即代表轴已经完成
            return True
        else:
            return False


    def Convert2Av(bv:str)->str:
        """
        Bv 转 Av
        @mcfx zhihu
        """
        table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr={}
        for i in range(58):
            tr[table[i]]=i
        s=[11,10,3,8,4,6]
        xor=177451812
        add=8728348608
        r=0
        for i in range(6):
            r+=tr[bv[s[i]]]*58**i
        return (r-add)^xor


    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    }
    av = Convert2Av(bv)
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    r = requests.get(url,headers=headers)
    duration = 0
    #计算总录播时长
    for i in r.json()["data"]["pages"]:
        if "弹幕" not in i["part"]:
            duration += i["duration"]
    return Monitor()

def ping():
    return "pong"

def rpcCall(*args,**kwargs):
    Called = False
    if Called:
        return {"error":1,"msg":"Already Called"}
    Thread(target=Spider_TimeLine,args=args,kwargs=kwargs).start()
    Called = True
    return {"error":0,"msg":"start success"}

if __name__ == "__main__":
    #a = Spider_TimeLine("BV1Mr4y1S7B3",["53082699"])
    try:
        import json
        port = int(json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["SpiderTimeLine"]["xmlRpcPort"])
        host = json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["SpiderTimeLine"]["xmlRpcHost"]
        Client_Server = json.loads(open("./Services_Config.json","r",encoding="utf-8").read())["SpiderTimeLine"]["xmlClientHost"]
    except Exception:
        host = "localhost"
        port = 5010
        Client_Server = "http://localhost:5002"

    server = SimpleXMLRPCServer(("0.0.0.0", port))
    server.register_function(rpcCall,"Spider_TimeLine")
    server.register_function(ping,"ping")
    print("SpiderTimeLine服务已启动")
    server.serve_forever()
    