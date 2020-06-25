import requests
from ast import literal_eval
import json
import time

def make_url(lst):
    urls_lst=[]
    for i in lst:
        a="https://poe.ninja/api/data/itemoverview?league=Delirium&type="+i
        urls_lst.append((i,a))
    return urls_lst


def get_json(url):
    r=requests.get(url,timeout=10)
    #print("######",r.text,"********")
    return r.json()

def get_names(jsn,price=1.0):
    names=[]
    a=(jsn["lines"])
    for i in a:
        if float(i["chaosValue"])>=price and (i["count"])>=5:
            print(i["name"],i["chaosValue"])
            names.append((i["name"],i["baseType"]))
    return names

def get_names_basetype(jsn,price=1.0) :
    names_bt=[]

    a=(jsn["lines"])

    for i in a:
        if float(i["chaosValue"])>=price and (i["count"])>=5:
            print(i["name"],i["chaosValue"])

            names_bt.append((i["levelRequired"],i["name"],i["variant"]))
    return names_bt


def check(s):
    if s==None:
        return ""
    else:
        return s




dic1={
"Essence":"\
Show\n\
  Class \"Currency\"\n\
  BaseType \"{}\"\n\
  SetTextColor 30 188 255\n\
  SetBackgroundColor 55 76 84 215\n\
  SetBorderColor 30 188 255 194\n\
  SetFontSize 35\n\
  PlayAlertSound 3 150\n\
  MinimapIcon 2 Blue Circle\n\
  PlayEffect Blue Temp",\


"DivinationCard":"\
Show\n\
  Class \"Divination Card\"\n\
  BaseType \"{}\"\n\
  SetTextColor 0 255 0\n\
  SetBorderColor 0 255 0\n\
  PlayAlertSound 7 270\n\
  SetFontSize 50\n\
  PlayEffect Green\n\
  MinimapIcon 1 Green Circle",\



"BaseType":"\
Show\n\
  ItemLevel >= {}\n\
  BaseType \"{}\"\n\
  {}Item True\n\
  SetTextColor 0 0 0\n\
  SetBackgroundColor 181 164 74 170\n\
  SetBorderColor 0 0 0\n\
  SetFontSize 25"



  # text block insert here





}

def remover(s):
    if s.count("ElderItem True")>0:

        return s
    elif s.count("ShaperItem True")>0:

        return s
    else:
        s=s.replace("  Item True\n","")
        return s


def main():
    data=""
    path = 'params.txt'
    with open(path, 'r') as f:
        for lines in f:
          data=data+lines
    d=(literal_eval(data))



    # Params

    # list_=["Essence","DivinationCard","BaseType"]
    # price=58.0
    price=d["price"]
    list_=d["list_"]
    dic=d["dic"]
    txt=d["text_"]
    txt1 = d["text__"]



    a=make_url(list_)
    #print(a)
    list_for_write=[]
    for i in a:
        #print(i)
        if i[0]!="BaseType":
            if i[0] in ["UniqueJewel","UniqueFlask","UniqueWeapon","UniqueArmour","UniqueAccessory"]:

                names1 = get_names(get_json(i[1]), price)
                for j in names1:
                    list_for_write.append(dic[i[0]].format(j[1]))



            else:
                names1=get_names(get_json(i[1]),price)
                for j in names1:
                    list_for_write.append(dic[i[0]].format(j[0]))


        else:
            names2=get_names_basetype(get_json(i[1]),price)
            for k in names2:
                list_for_write.append(remover(dic[i[0]].format(k[0],k[1],check(k[2]))))

    f=open('name.filter',"w",encoding='utf-8')
    f.write(txt + '\n')
    for index in list_for_write:
        f.write(index + '\n')
    f.write(txt1 + '\n')
    f.close()




if __name__=="__main__":

        main()





