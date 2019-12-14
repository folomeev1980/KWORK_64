import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from wbdr import *
import csv
import datetime


def pager(n, type_):
    if type_ == "1":
        temp = "https://omsk.mlsn.ru/pokupka-nedvizhimost/?page={}&viewMode=paper"
    if type_ == "2":
        temp = "https://omsk.mlsn.ru/pokupka-nedvizhimost/?isNewBuilding=1&page={}&viewMode=paper"
    if type_ == "3":
        temp = "https://omsk.mlsn.ru/pokupka-dachi-i-uchastki/?page={}&viewMode=paper"
    if type_ == "4":
        temp = "https://omsk.mlsn.ru/pokupka-kommercheskaja-nedvizhimost/?page={}&viewMode=paper "

    for k in range(1, n, 1):

        url = temp.format(k)
        print(url)
        r = wbdr(url)
        soup = BeautifulSoup(r, "lxml")

        trs = soup.find("table", class_="table grid-view mode-paper").find("tbody").findAll("tr")
        i = 1
        for tr in trs:
            try:
                type1 = tr.find("td", class_="paper col-realty-type").find("span", class_="main-param").text.strip()
                type2 = tr.find("td", class_="paper col-realty-type").find("div").text.strip()
                type = type1 + "\n" + type2
                adress = tr.find("td", class_="paper col-address").text.strip()
                link = tr.find("td", class_="paper col-address").find("a").get("href")
                price = tr.find("td", class_="paper col-price").text.strip().split("\xa0")[::-1][1:][::-1]

                d = ""
                for j in price:
                    d = d + j
                price = d

                seller = tr.find("td", class_="paper col-seller").text.strip()

                contact_name = tr.find("td", class_="paper col-contacts").find("div", class_="main-param").text.strip()
                contact_phone = tr.find("td", class_="paper col-contacts").find("div", class_="phone-item").text.strip()




            except:

                type = ""
                adress = ""
                link = ""
                price = ""
                seller = ""
                contact_name = ""
                contact_phone = ""

            finally:
                if type != "":
                    row = (type, adress, link, price, seller, contact_name, contact_phone)
                    with open('nedv_omsk.csv', mode='a') as speed_test:
                        speed_test = csv.writer(speed_test, delimiter=';', lineterminator='\n')
                        # print(row)
                        speed_test.writerow(row)
        with open("log.txt", "a") as logfile:
            logfile.write(str(datetime.datetime.now())[0:16] + "   page {}".format(k) + "\n")

        print("   page {}".format(k))


if __name__ == "__main__":
    flag = True
    with open('nedv_omsk.csv', mode='w') as speed_test:
        pass

    while flag:
        type_ = input(
            "Укажите тип сканируемых объектов:\n 1 - Квартиры и комнаты\n 2 - Квартиры в новостройках\n 3 - Дома, участки, дачи\n 4 - Комерческая Недвижимость\n\n")
        if type_ in ["1", "2", "3", "4"]:
            flag = False
    #

    try:
        pager(1000, type_)
    except Exception as e:
        print(str(e))
        with open("log.txt", "a") as logfile:
            logfile.write(str(datetime.datetime.now())[0:16] + "\t\t" + str(e) + "\n")
        input("\n\nPress any key to finish")
