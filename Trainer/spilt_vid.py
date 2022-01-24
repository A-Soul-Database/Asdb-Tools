#coding:utf8
## spilt video
## while choosing video to train, we single broadcast is best

import json,os,random
baseurl = "D:\\projects\\as\\A-Soul-Data\\db"

db_main = json.loads(open(baseurl+"\\main.json",encoding="utf-8").read())

dbs = db_main["LiveClip"]

bvs = []

def main_parse(main_json):
    # we perfer to choose single broadcast,and make sure all scene and people, skin are included
    for item in main_json:
        if random.randint(0,10)>8:
            bvs.append([item["bv"] if item["clip"] ==1 else item["bv"]+"-"+ str(clips+1) for clips in range(item["clip"])]) # Solve multi-p problem

main_Json = []
for i in dbs:
    main_Json+= json.loads(open(baseurl+"\\"+i+"\\main.json",encoding="utf-8").read())
main_parse(main_Json)
all = []
for i in bvs:
    if type(i) == list:
        all+=i

for i in all:
    os.system(f"D:\\asdataset\\collections\\vid\\{i}.mp4")