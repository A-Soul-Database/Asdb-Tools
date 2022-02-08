import os
import requests
import json
import git
import shutil
import stat

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

def Apply_Srt(bv):
        # 转换字幕
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
        # 目标检测
    object = {"Staff":[],"Skin":[],"Components":[]}
    for i in filename:
        os.system(f"py ./yolov5/detect.py --source={path}/{i}")
        objinfo = json.loads(open("./asdb.txt").read())
        object["Staff"] += objinfo["Staff"]
        object["Skin"] += objinfo["Skin"]
    return {"error":0,"data":{"Staff":object["Staff"],"Skin":object["Skin"]}}

def JsonGenerator(bv,Objects,time,scene,liveRoom):
        #根据已有的数据生成Json文件
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    info = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]
    
    date,title,clip,staff,skin = info["pubdate"].srtftime("%Y-%m-%d") , info["title"] , len([fn for fn in info["pages"] if "弹幕" not in fn]) , Objects["data"]["Staff"], {}
    for i in Objects["data"]["Skin"]:
        if i.count("-") > 1: i = '-'.join(i.split("-")[:2]) # 去除后面的修饰符 如Ava-Sleep-2 -> Ava-Sleep
        name = i.split("-")[0][:1]
        clothes = i.split("-")[1]
        skin.get(name) and skin[name].append(clothes) or skin.update({name:[clothes]})

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