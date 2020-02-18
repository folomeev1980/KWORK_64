#http://docgroup.ru/www/reestr.nsf/SRO01?OpenView&Start=1&Count=10000


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
    if 'ИНН' not in dic:
        dic['ИНН'] = ""
    if 'Место нахождения  (для ЮЛ)' not in dic:
        dic['Место нахождения  (для ЮЛ)'] = ""
    if 'Телефон' not in dic:
        dic['Телефон'] = ""
    if 'Эл.адрес' not in dic:
        dic['Эл.адрес'] = ""
    if 'Фамилия, Имя, Отчество лица, осуществляющего функции единоличного исполнительного органа ЮЛ' not in dic:
        dic['Фамилия, Имя, Отчество лица, осуществляющего функции единоличного исполнительного органа ЮЛ'] = ""
    if 'Сокращенное наименование ЮЛ' not in dic:
        dic['Сокращенное наименование ЮЛ'] = ""


    try:
        with open("sro23.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            t=( dic['Сокращенное наименование ЮЛ'],
                dic['ИНН'],
                dic['Место нахождения  (для ЮЛ)'],
                dic['Телефон'],
                dic['Эл.адрес'],
                dic['Фамилия, Имя, Отчество лица, осуществляющего функции единоличного исполнительного органа ЮЛ'],


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


def get_main_info(html):
    dictionary = []
    dic={}



    try:
        soup = BeautifulSoup(html, "lxml")
        soup=soup.find("tbody").findAll("tr")
        for i in soup:
            dictionary.append("http://docgroup.ru"+i.find("a").get("href"))

        return dictionary
    except Exception as e:
        print(str(e))
        return dictionary



def get_info(html):

    dic={}

    try:
        soup = BeautifulSoup(html, "lxml")
        #print(soup)
        soup=soup.find("div",class_="datagrid").find("table", border="0", cellpadding="0", cellspacing="0", width="100%").find("table", border="1", width="100%").findAll("tr")
        for i in soup:
            temp=i.findAll("td")
            #print(temp[0].text,temp[1].text)
            dic[temp[0].text.strip()]=temp[1].text.strip()



        return dic
    except Exception as e:
        print(str(e))
        return dic


if __name__=="__main__":
    url="http://docgroup.ru/www/reestr.nsf/SRO01?OpenView&Start=1&Count=10000"
    html = get_html_(url)
    links=get_main_info(html)
    # print(links[0])
    # get_info(links[0])

    for index,i in enumerate(links):

        writer_csv_include(get_info(get_html_(i)))
        print(index+1)