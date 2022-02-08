# Asdb Collection Items
# For Asdb Automatically Depolyment
from base64 import encode
from collections import Counter
import itertools
all = []
face = ['Ava','Bella','Carol','Diana','Eileen'] # High Weight
skin = ['Ava-Official','Bella-Official','Carol-Official','Diana-Official','Eileen-Official','Ava-Group','Bella-Group','Carol-Group','Diana-Group','Eileen-Group','Ava-Swim','Bella-Swim',
'Carol-Swim','Diana-Swim','Eileen-Swim','Ava-Birthday','Bella-Birthday','Carol-Birthday','Diana-Birthday','Eileen-Birthday',
'Ava-Year','Bella-Year','Carol-Year','Diana-Year','Eileen-Year','Ava-Christmas','Bella-Christmas','Carol-Christmas','Diana-Christmas','Eileen-Christmas',
'Ava-Sleep-1','Ava-Sleep-2','Bella-Sleep','Carol-Sleep','Diana-Sleep','Eileen-Sleep','Ava-LegendWorld','Bella-LegendWorld','Carol-LegendWorld','Diana-LegendWorld',
'Eileen-LegendWorld','Bella-Sport','Bella-Jk','Diana-Swim-Without-Outer','Diana-Creamy'] # Medium Weight
components = ['Glasses','Fox-Tail','Fox-Ear','Rabbit-Ear','Rabbit-Gloves','Bear-Ear','Bear-Gloves','Cat-Ear','Cat-Gloves','Wolf-Ear','Wolf-Gloves','Wolf-Tail','Fox-Gloves'] #Low Weight
Skin_Double_Check = ['Eileen-Group-Shoes','Eileen-Sleep-Breast','Bella-Group-Shoes','Diana-Group-Skirt','Diana-Year-Shoes','Ava-Birthday-Breast']
stuffs = ['Projector','Projector-LASER'] # Medium Weight

def receive(source):
    all.append(source)

def save():
    def caculate_percentage(dictt:dict,typ:str)->list:
        all_length = 0
        newDict = {}
        for k in dictt.items():
            if k[1] is not None:
                all_length += k[1]
        for k,v in dictt.items():
            if v is not None:
                newDict[k] = round(v/all_length*100,2)
        
        # Analysis
        if typ == "Stuff":
            return newDict.keys()
        if typ == "Skin":
        #Freeze Basis People
            Skin_Staff_Item = len([fn for fn in newDict.keys() if fn.split("-")[0] in face])
            if Skin_Staff_Item == len(result['Staff']):
                return [fn for fn in newDict.keys()]
        dicts = []
        for k,v in newDict.items():
            if v > 0.5:
                dicts.append(k)
            else:
                print("{} is not enough".format(k))
        return dicts


    all_in_one = list(itertools.chain.from_iterable(all))
    times = Counter(all_in_one)
    # Archive the data
    rec_face, rec_skin, rec_stuff = {} , {}, {} 
    for k,v in times.items():
        if k in components:
            pass
            # 可以改为Continue
        rec_face[k] = v if k in face else None
        
        if k in Skin_Double_Check:
            it = k[:k.rfind('-')]
            if rec_skin.get(it) is not None:
                if rec_skin.get(it) < v:
                    rec_skin[it] = v
            else:
                rec_skin[it] = v

        if k in skin:
            if rec_skin.get(k) is not None:
                if rec_skin.get(k) < v:
                    rec_skin[k] = v
            else:
                rec_skin[k] = v

        rec_stuff[k] = v if k in stuffs else None
    result = {
        "Staff":[],
        "Skin":[],
        "Components":[],
    }
    result["Staff"] = caculate_percentage(rec_face,"Staff")
    result["Skin"] = caculate_percentage(rec_skin,"Skin")  
    #result["Components"] = caculate_percentage(rec_stuff,"Stuff")
    open("asdb.txt","w",encoding="utf-8").write(str(result).replace("'",'"'))