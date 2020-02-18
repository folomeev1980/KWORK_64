# http://sro-sso.ru/reestr_sro/view?id=52


import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool,freeze_support
from time import sleep
from datetime import datetime



global_lst=[]

class Count:
    c=0


count=Count()



def writer_csv_include(dic):
    if 'Веб-сайт организации' not in dic:
        dic['Веб-сайт организации']=""
    if 'Электронная почта организации' not in dic:
        dic['Электронная почта организации']=""
    if 'Телефон' not in dic:
        dic['Телефон']=""
    if 'Сведения о руководителе' not in dic:
        dic['Сведения о руководителе']=""
    if 'Юридический адрес' not in dic:
        dic['Юридический адрес']=""
    if 'Сокращенное наименование' not in dic:
        dic['Сокращенное наименование'] = ""


    try:
        with open("sro_sso.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            t=( dic['Сокращенное наименование'],
                dic['ИНН'],
                dic['Сведения о руководителе'],
                dic['Юридический адрес'],
                dic['Веб-сайт организации'],
                dic['Электронная почта организации'],
                dic['Телефон']


            )
            # if len(dic) == 7:
            writer.writerow(t)
    except Exception as e:
        print(e)



#
#
# def writer_csv_exclude(dic):
#     try:
#         with open("exclude_nostroy.csv", "a", newline='') as f:
#             writer = csv.writer(f, delimiter=';')
#             if len(dic) == 7:
#                 writer.writerow(tuple(dic))
#
#             else:
#                 print("csv len false")
#     except Exception as e:
#         print(str(e))



def get_html_(url):
    #sleep(0.5)
    k = 0
    page = ""
    while page == '':
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
            page = requests.get(url, headers=headers)
            return page.text
            break
        except:
            k += 1
            print("Connection refused by the doctor server..")
            print("Let me sleep for 10 seconds")
            # print("ZZzzzz...")
            sleep(10)
            # print("Was a nice sleep, now let me continue...")
            continue


def get_info(html):
    dictionary = []
    dic={}

    x=(html.find("<table class=\"detail-view table table-striped table-condensed\" id=\"yw1\">"))
    html1=html[x:-1]

    try:
        soup1 = BeautifulSoup(html, "lxml")
        soup2 = BeautifulSoup(html1,"lxml")
        part1=soup1.find("table",class_="detail-view table table-striped table-condensed").findAll("tr")[1:5]
        part2 = soup2.find("table", class_="detail-view table table-striped table-condensed").findAll("tr")[0:]


        part = part1 + part2

        for i in part:
            dictionary.append(i.find("td").text.strip())
            dic[i.find("th").text.strip()]=i.find("td").text.strip()

        #global_lst.append(dictionary)
        #print(dic)
        return dic
    except Exception as e:
        print(str(e))
        return dic


if __name__=="__main__":
    for i in range(1,100000):
        print(i)
        html=get_html_("http://sro-sso.ru/reestr_sro/view?id={}".format(str(i)))
        writer_csv_include(get_info(html))