import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from progress.bar import Bar
from openpyxl import Workbook, load_workbook

def lst(l):
    s = ""
    for i in l:
        s = s + i + "####"
    return (s)



def create_csv():
    header = tuple(["Словарная метка",
                    "ФИО",
                    "Организация, проводящая КИ",
                    "Код врача",
                    "День рождения врача"])

    with open("dbs\\doctors.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        #writer.writerow(header)


def get_html_(url):
    page = ""
    while page == '':
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
            page = requests.get(url, headers=headers)
            return page.text
            break
        except:
            print("Connection refused by the doctor server..")
            print("Let me sleep for 10 seconds")
            # print("ZZzzzz...")
            sleep(10)
            # print("Was a nice sleep, now let me continue...")
            continue


def get_list_of_doctors(url):
    list_of_doctors = []
    # print(url)
    if url != "":

        clinics = get_html_(url)

        soup = BeautifulSoup(clinics, "lxml")
        try:
            tds = soup.find("table", class_="ts1").findAll("tr", class_="hi_sys")

            for td in tds:
                temp = td.findAll("td")
                # print(temp)
                a = (temp[-2].text.strip().split("-"))

                b = (temp[-1].text.strip().split()[1][1:])

                c = temp[2]
                c = str(c).split(">")[1]
                c = c.split("<")[0].strip()

                list_of_doctors.append([a[0], a[1], b, c])
                # print(list_of_doctors)


        except Exception as e:
            # print(e, "except by list of doctors",url)
            list_of_doctors = []

        return list_of_doctors

    else:

        return list_of_doctors


def get_append_list_of_doctors(url):
    list_of_doctors = []
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
    except Exception as e:

        driver.quit()

    k = 2

    while True:

        try:
            # print("ok")
            page = "/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td[{}]/a".format(
                k)
            driver.find_element_by_xpath(page).click()
            html = driver.page_source
            # print(html)

            soup = BeautifulSoup(html, "lxml")

            tds = soup.find("table", class_="ts1").findAll("tr", class_="hi_sys")
            for td in tds:
                temp = td.findAll("td")
                c = temp[2]
                c = str(c).split(">")[1]
                c = c.split("<")[0].strip()

                a = (temp[-2].text.strip().split("-"))

                b = (temp[-1].text.strip().split()[1][1:])
                list_of_doctors.append([a[0], a[1], b, c])

            k = k + 1
            # time.sleep(2)


        except Exception as e:
            # print("End pages",e)
            break
            # driver.quit()
    driver.quit()

    return list_of_doctors


def get_info_for_each_page_(html):
    list_dics = []
    soup = BeautifulSoup(html, "lxml")

    list_of_page = (soup.findAll("tr", class_="hi_sys poi"))
    # print(list_of_page)

    for st, page in enumerate(list_of_page):

        dic = {}
        list_some = []

        try:
            doctor_link = "https://grls.rosminzdrav.ru/" + \
                          page.get("onclick").split("'")[1]

            doctors_list = get_list_of_doctors(doctor_link)



        except:
            doctors_list = []

        try:

            page_data = page.findAll("td")

            for td in page_data:
                list_some.append(td.text.strip())

            # print(list_some[6])

            if int(list_some[6]) <= 20:
                list_some.append(doctors_list)
            else:
                list_some.append(doctors_list)
                # print(doctor_link)
                list_some[-1].extend(get_append_list_of_doctors(doctor_link))

            # print(list_some)
            dic["code"] = list_some[1]
            dic["famaly"] = list_some[2]
            dic["name"] = list_some[3]
            dic["fathername"] = list_some[4]
            dic["numer_of_ki"] = list_some[6]
            dic["birthday"] = list_some[7]
            dic["doctors_list"] = list_some[8]

            # print(dic)

            list_dics.append(dic)


        except Exception as e:
            print(e, "Ошибка ")
            dic = {}
            list_dics.append(dic)

    return list_dics


def writer_csv(data):
    for dic in data:
        for j in dic["doctors_list"]:
            with open("dbs\\doctors.csv", "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                a = "{} {} {}".format(dic["famaly"], dic["name"], dic["fathername"])
                b = "{}_{}_{}".format(j[0], j[1], j[2])
                c = j[-1]
                d = dic["code"]
                e = dic["birthday"]

                writer.writerow((b, a, c, d, e))


def cvs_doctors():
    i = 1
    k = 0
    sum = 0
    create_csv()
    while True:
        try:
            url = "https://grls.rosminzdrav.ru/ciexperts.aspx?F=&N=&P=&D=&ExpertID=&order=fio&orderType=desc&moduleId=2&pageSize=30&pageNum={}".format(
                i)
            html = get_html_(url)
            list_of_dics_one_page = get_info_for_each_page_(html)
            if len(list_of_dics_one_page) == 0:
                k = k + 1
            sum = sum + len(list_of_dics_one_page)
            writer_csv(list_of_dics_one_page)
            i = i + 1
            print(sum)
            if k > 5:
                break
        except Exception as e:
            if k > 5:
                break
    print(i, "Pages\n", sum, "Doctors")


def excel_doctors():
    book_new = Workbook()
    dic = {}
    sheet_new = book_new.active
    header = tuple(["ID_PI",
                    "FIO",
                    "Organization",
                    "Email",
                    "Phone",
                    "VK",
                    "Facebook",
                    "Instagram",
                    "Birthday",
                    ])

    sheet_new.append(header)

    with open('dbs\\doctors.csv', newline='', encoding='utf-8') as csv_file_clinics:
        csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
        for i in csv_reader_clinics:
            #print(lst(i[1:]))
            dic[lst(i[1:])]=None
            # try:
            #     i=[i[3],i[1],i[2],"","","","","",i[4]]
            #
            #     sheet_new.append(i)
            # except:
            #     pass

    for k in dic:
        try:
            i=k.split("####")[0:-1]

            i = [i[2], i[0], i[1], "", "", "", "", "", i[3]]
            #print(i)
            sheet_new.append(i)
        except:
            pass



        # print(k.split("####")[0:])
        #sheet_new.append()
    book_new.save("final_xls_tables\\PI.xlsx")


if __name__ == "__main__":
    excel_doctors()
# cvs_doctors()
