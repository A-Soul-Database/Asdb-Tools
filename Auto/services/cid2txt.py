import requests
from urllib.parse import urlparse, parse_qs
import json
def sec_to_min(sec):
    min_tmp,sec_tmp = str(sec//60),str(sec%60)
    #return f"{sec//60}:{sec%60}" if sec%60 >9 else f"{sec//60}:0{sec%60}"
    if int(sec_tmp) < 10: sec_tmp = f"0{sec_tmp}"
    if int(min_tmp) < 10: min_tmp = f"0{min_tmp}"
    return f"{min_tmp}:{sec_tmp}"

def Cid2Txt(Url,staff):
    try:
        result = urlparse(Url)
        if "/read/cv" in result.path:
            cvid = result.path.split("cv")[1]
        else:
            cvid = parse_qs(result.query)['cvid'][0]
    except:
        print("Invalid URL")
        exit()
    r = requests.get("https://api.bilibili.com/x/note/publish/info", params={"cvid": cvid},
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}).json()
    av = r["data"]["arc"]["oid"]
    bv = requests.get(f"https://api.bilibili.com/x/web-interface/view?aid={av}").json()["data"]["bvid"]
    content = json.loads(r["data"]["content"])
    rolls = ""
    stff = []
    p,time,last_time = 1,0,0

    forbidden_Words = ["p1","p2","p3","p4","p5","p6","笔记轴"]
    stff_words = ["《","》"]
    for item in content:
        if type(item["insert"]) == str:
            # Str 说明是内容
            cont = item["insert"].replace("\n", "").replace("└─","").replace(" ","")
            if len(cont) == 0 : continue
            if any(word in cont for word in stff_words): stff.append([cont.split("《")[1].split("》")[0],f"{p}-{time}",[staff]])
            if any(word in cont.lower() for word in forbidden_Words): continue
            if cont in rolls: break
            rolls += f"{time} {cont}\n"

        elif type(item["insert"]) == dict:
            # Dict 说明是时间轴
            try:
                if last_time > item["insert"]["tag"]["seconds"]:p+=1
                last_time = item["insert"]["tag"]["seconds"]
                time = sec_to_min(item["insert"]["tag"]["seconds"])
            except:
                time = 0

    open(f"{bv}.txt","w",encoding="utf-8").write(rolls)
    print(stff)

if __name__ == "__main__":
    url = input()
    staff = input()
    Cid2Txt(url,staff)
