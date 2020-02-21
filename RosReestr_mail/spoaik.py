# http://sro-sso.ru/reestr_sro/view?id=52


import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support
from time import sleep
from datetime import datetime

global_lst = []


class Count:
    c = 0


count = Count()


def writer_csv_include(dic):
    mail = "Эл.почта.:"
    if mail not in dic:
        dic[mail] = ""
    else:
        print(dic[mail])

    try:
        with open("spoaik.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            if dic[mail] != "":
                t = (dic[mail],

                     )

                writer.writerow(t)
    except Exception as e:
        print(e)



def get_html_(url):
    # sleep(0.5)
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
    dic = {}

    try:
        soup = BeautifulSoup(html, "lxml")
        #
        soup = soup.find("div", id="tabs-1").findAll("p")


        for i in soup:
            if "Эл.почта.:" in i.text:
                temp=i.text.split("Эл.почта.:")[-1]
                temp=temp.strip()
                if " " in temp:

                    temp=temp.split(" ")[0]


                dic["Эл.почта.:"]=temp
        return dic
    except Exception as e:

        print(str(e))
        return dic


if __name__ == "__main__":
    # url="http://reestr.uralsro.ru/view?id=227"
    for i in range(1, 1000):
        print(i)
        html = get_html_("http://sroaik.ru/get_register_data.php?id={}".format(str(i)))
        writer_csv_include(get_info(html))
    # html = get_html_("http://www.srorosk.ru/register/view?id=1")
    # print(get_info(html))
