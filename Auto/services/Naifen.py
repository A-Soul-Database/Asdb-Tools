import json
import requests
from lxml import etree
import re
baseurl = "D:\\projects\\as\\A-Soul-Data\\db"

db_main = json.loads(open(baseurl+"\\main.json",encoding="utf-8").read())
dbs = db_main["LiveClip"]
main_Json = []
for i in dbs:
    main_Json+= json.loads(open(baseurl+"\\"+i+"\\main.json",encoding="utf-8").read())
# get naifen item

compareInfo = {}
r = requests.get("https://nf.asoul-rec.com/ASOUL-REC/")
Onedrive_naifen = r.content.decode("utf-8").encode("utf-8")
elements = etree.HTML(Onedrive_naifen)
Naifen_urls = elements.xpath("//a[@class='item']/text()")
for item in main_Json:

    date = item["date"].split("-")
    month = date[1] if len(date[1]) == 2 else "0"+date[1]
    day = date[2] if len(date[2]) == 2 else "0"+date[2]
    date_naifenify = "20"+".".join([date[0],month,day])

    for naifen in Naifen_urls:
        have = False
        if date_naifenify in naifen:
            pass
print(compareInfo)