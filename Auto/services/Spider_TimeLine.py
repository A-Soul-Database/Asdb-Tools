"""
Comments.py
BiliBIli 评论爬虫
定时获取时间轴评论
!!!前提是已经有了完整录播
https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=1&oid={av}&mode=0   || root={} 楼中楼,root表示根id pn={} 表示楼中楼的页数
"""
import requests
import time
import re
import sys
from xmlrpc.server import SimpleXMLRPCServer
def Spider_TimeLine(bv:str,uid:list) -> None:
    def Monitor(interval:int=60)->None:
        """
        每隔interval就可以更新一次
        """
        while True:
            result = GetComments()
            if CalculateAllTime(result):
                print(f"\r更新成功\n{result['contents']}",end="")
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
            step = 0
            result = []
            while True:
                url = f"https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={step}&type=1&oid={av}&root={root}"
                r = requests.get(url,headers=headers)
                if r.json()["data"]["replies"] == None:
                    break
                for i in r.json()["data"]["replies"]:
                    if i["member"]["mid"] in uid:
                        result.append(i["content"]["message"])
                step += 1
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
                    returning["contents"] = r.json()["data"]["top"]["upper"]["content"]["message"]
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
                        returning["contents"]= i["content"]["message"]
                        returning["contents"]+=Comments_In_Floor(i["rpid"])
                start += 1
                time.sleep(1)
        return returning


    def CalculateAllTime(result:str):
        """通过轴时间计算是否达到要求"""
        if len(result["contents"]) == 0:
            #说明一个轴都没有,继续loop
            return False
        results = result["contents"].replace(" ","")
        results = results.replace("：",":")
        def to_seconds(a):
            if a.count(":") == 3:
                return int(a.split(":")[0])*3600+int(a.split(":")[1])*360+int(a.split(":")[2])
            return int(a.split(":")[0])*60+int(a.split(":")[1])
        comments_time = re.findall(r'[0-9]*:[0-9]*:[0-9]*',results)
        results = re.sub(r'[0-9]*:[0-9]*:[0-9]*',"",results)#替换回去,以免下面出现重复提取
        comments_time += re.findall(r'[0-9]*:[0-9]*',results)
        comments_time = [fn for fn in comments_time if fn != ":"]
        
        last_time = 0
        timeline_duration = 0
        for i in comments_time:
            if to_seconds(i) > last_time:
                last_time = to_seconds(i)
            else:
                timeline_duration += last_time
                last_time = to_seconds(i)
                #新分P,于是把之前的分P归档
        timeline_duration += last_time
        if timeline_duration > duration*0.8:
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

if __name__ == "__main__":
    #a = Spider_TimeLine("BV1Mr4y1S7B3",["53082699"])
    try:
        import json
        port = int(json.loads(open("./Services_Config.json","r","utf-8").read())["SpiderTimeLine"]["xmlRpcPort"])
    except Exception:
        port = 5010

    server = SimpleXMLRPCServer(("localhost", port))
    server.register_function(Spider_TimeLine)
    server.serve_forever()