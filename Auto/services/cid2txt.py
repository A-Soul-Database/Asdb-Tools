import requests
from urllib.parse import urlparse, parse_qs
import json
def sec_to_min(sec):
    return f"{sec//60}:{sec%60}" if sec%60 >9 else f"{sec//60}:0{sec%60}"

Url = input("Enter the Note URL: \n")
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
content = json.loads(r["data"]["content"])
rolls = ""
time = 0
forbidden_Words = ["p1","p2","p3","p4","p5","p6","笔记轴"]
for item in content:
    if type(item["insert"]) == str:
        # Str 说明是内容
        cont = item["insert"].replace("\n", "").replace("└─","").replace(" ","")
        if len(cont) == 0 : continue
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

print(rolls)