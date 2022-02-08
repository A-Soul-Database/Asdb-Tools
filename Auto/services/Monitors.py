import random , time , json, requests

def Liveroom_Monitor(uid):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    info = requests.get(url,headers=headers).json()["data"]["live_room"]
    if info["live_status"]:
        return {"error":0,"data":{"uid":uid,"title":info["title"],"On_Live":info["live_status"]}}
    else:
        return {"error":0,"data":{"uid":uid,"On_Live":info["live_status"]}}

def Record_Monitor(uid:str="393396916"):
    def Analysis(bv:str):
        r = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]["pages"]
        multi_Part = 0
        for item in r:
            if "上" in item["part"]:
                multi_Part = 1
            if "下" in item["part"]:
                multi_Part = 2
        while multi_Part == 1:
            time.sleep(random.randint(3,5))
            Analysis(bv)
        return {"error":0,"data":{"Bv":bv}}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    info = requests.get(f"https://api.bilibili.com/x/space/arc/search?mid={uid}",headers=headers).json()["data"]["list"]["vlist"]
    for i in info:
        if "【直播录像】" in i["title"]:
            return Analysis(i["bvid"])

def Timeline_Monitor(bv,uid:str="53082699"):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    def cvid2content(cvid):
        def sec_to_min(sec):
            return f"{sec//60}:{sec%60}" if sec%60 >9 else f"{sec//60}:0{sec%60}"
        r = requests.get("https://api.bilibili.com/x/note/publish/info", params={"cvid": cvid},headers=header)
        content = json.loads(r["data"]["content"])
        rolls , time = "" , 0
        forbidden_Words = ["p1","p2","p3","p4","p5","p6"]
        for item in content:
            if type(item["insert"]) == str:
                # Str 说明是内容
                cont = item["insert"].replace("\n", "")
                if any(word in cont.lower() for word in forbidden_Words):
                    continue
                rolls += f"{time} {cont}\n"

            elif type(item["insert"]) == dict:
                # Dict 说明是时间轴
                try:
                    if "弹幕" in item["insert"]["tag"]["title"]:
                        break
                    time = sec_to_min(item["insert"]["tag"]["seconds"])
                except:
                    time = 0
        return {"error":0,"data":{"Bv":bv,"Content":rolls}}
    av = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=header).json()["data"]["aid"]
    replies = requests.get(f"https://api.bilibili.com/x/note/publish/list/archive?oid={av}&oid_type=0&pn=1&ps=10",headers=header).json()["data"]["list"]
    have_timeline = 0
    for item in replies:
        if item["author"]["mid"] == uid:
            have_timeline = 1
            return cvid2content(item["cvid"])
    if have_timeline == 0:
        time.sleep(random.randint(3,5))
        return Timeline_Monitor(bv,uid)