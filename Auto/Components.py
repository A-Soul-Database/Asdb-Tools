import os
import requests
import json
import time
import git
import shutil
import stat
import random
###
def Liveroom_Monitor(uid):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    info = requests.get(url,headers=headers).json()["data"]["live_room"]
    if info["live_status"]:
        return {"error":0,"data":{"uid":uid,"title":info["title"],"On_Live":info["live_status"]}}
    else:
        return {"error":0,"data":{"uid":uid,"On_Live":info["live_status"]}}
###

def Download_Bili_Video(bv,path):
    os.path.exists(path) or os.makedirs(path)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    info = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]["pages"]
    urls = []
    for i in info:
        if "弹幕" not in i["part"]:
            urls.append(i["page"])
    filename = []
    for item in urls:
        name = bv+"-"+item["part"] if len(urls) > 1 else bv
        cmd = f"you-get --format dash-flv360 --output-dir {path} --output-filename {name}  https://www.bilibili.com/video/{bv}?p={item}"
        os.system(cmd)
        filename.append(f"{name}.mp4")
    return {"error":0,"data":{"files":filename}}

###
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
###
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
        Timeline_Monitor(bv,uid)

def Apply_Srt(bv):
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)
        #func(path)
    shutil.rmtree("./SrtTmp",onerror=remove_readonly) if os.path.exists("./SrtTmp") else None
    # Clone Project
    repo = git.Repo.clone_from("https://github.com/A-Soul-Database/ActionsGui.git","./SrtTmp")
    config = json.loads(open("./SrtTmp/config.json").read())
    config["url"] = bv
    open("SrtTmp/Config.json","w",encoding="utf-8").write(json.dumps(config).replace("'",'"'))
    repo.index.add('.')
    repo.index.commit("Srt Apply")
    repo.remote().push()
    shutil.rmtree("./SrtTmp",onerror=remove_readonly)
    return {"error":0,"data":{"Bv":bv}}

def Apply_detection(path,filename):
    object = {"Staff":[],"Skin":[],"Components":[]}
    for i in filename:
        os.system(f"python3 ./yolov5/detect.py --source=../{path}/{i}")
        objinfo = json.loads(open("./yolov5/asdb.txt").read())
        object["Staff"] += objinfo["Staff"]
        object["Skin"] += objinfo["Skin"]
    return {"error":0,"data":{"Staff":object["Staff"],"Skin":object["Skin"]}}

def JsonGenerator(bv,date,time,title,scene,liveRoom,staff,clip,skin):
    return {
	"date": date,
	"time": time,
	"liveRoom": liveRoom,
	"bv": bv,
	"title": title,
	"scene": scene,
	"type": ["chat", "song", "dance"],
	"staff": staff,
	"clip": clip,
	"items": [{
			"name": "game",
			"item": []
		}, {
			"name": "song",
			"item": [
			]
		},
		{
			"name": "dance",
			"item": [
			]
		}
	],
	"skin": skin,
	"platform":["B","D"],
	"tags": []
}