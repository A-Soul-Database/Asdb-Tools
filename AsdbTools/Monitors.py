import random , time , json, requests , math
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}

def Liveroom_Monitor(uid):
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    info = requests.get(url,headers=headers).json()["data"]["live_room"]
    if info["live_status"]:
        return {"error":0,"data":{"uid":uid,"title":info["title"],"On_Live":info["live_status"]}}
    else:
        return {"error":0,"data":{"uid":uid,"On_Live":info["live_status"]}}

def Diff():
    def Record_Monitor(vlists:list):
        def Analysis(bv:str)->bool:
            parts = [fn["part"] for fn in requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]["pages"]]
            if "上" in parts: # Multi part
                if "下" in parts: return True
                else: return False # parts missing
            else: return True # Single Part
        result = []
        for i in vlists:
            if "【直播录像】" in i["title"]: 
                result.append(i["bvid"]) if Analysis(i["bvid"]) else None
                time.sleep(random.randint(0,1))
        return {"error":0,"data":result}

    asdb_bvs , vlists = [] , []
    for i in requests.get("https://raw.githubusercontent.com/A-Soul-Database/A-Soul-Data/main/db/main.json").json()["LiveClip"]:
        asdb_bvs+= requests.get(f"https://raw.githubusercontent.com/A-Soul-Database/A-Soul-Data/main/db/{i}/indexer.json").json()
    # Get Asoul 二创计画 Uploads
    init_info  = requests.get("https://api.bilibili.com/x/space/arc/search?mid=547510303&ps=50&pn=1&order=pubdate&jsonp=jsonp",headers=headers).json()
    pages_num = math.ceil(int(init_info["data"]["page"]["count"]) / int(init_info["data"]["page"]["ps"]))
    for n in range(pages_num):
        vlists += requests.get(f"https://api.bilibili.com/x/space/arc/search?mid=547510303&ps=50&pn={n+1}&order=pubdate&jsonp=jsonp",headers=headers).json()["data"]["list"]["vlist"]
        if len([fn["bvid"] for fn in vlists if fn["bvid"] in asdb_bvs]) != 0 : # Asdb In First Page
            return Record_Monitor([fn for fn in vlists if fn not in asdb_bvs])
        else: time.sleep(random.randint(0,1))
