from progress.bar import Bar
import requests
import csv
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup
from random import randint
from time import sleep



def lst(l):
    s = ""
    for i in l:
        s = s + i + "####"
    return (s)


def create_csv():
    header = tuple(["номер id",
                    "медицинская организация"])

    with open("dbs\\medOrg.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        #writer.writerow(header)


def writer_csv(data):
    for dic in data:
        with open("dbs\\medOrg.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            a = dic["n_med"]
            b = dic["med_name"]

            writer.writerow((a, b))


def get_html(url):
    page = ""
    while page == '':
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
            page = requests.get(url, headers=headers)
            return page.text
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 10 seconds")
            # print("ZZzzzz...")
            sleep(10)
            # print("Was a nice sleep,


def get_info_for_each_page(html):
    list_dics = []

    soup = BeautifulSoup(html, "lxml")
    list_of_page = (soup.find_all("tr", class_="poi hi_sys"))
    for page in list_of_page:
        dic = {}
        list_some = []

        try:
            page_data = page.find_all("td")

            for td in page_data:
                list_some.append(td.text.strip())
            dic["n_med"] = list_some[1]
            dic["med_name"] = list_some[3]
            list_dics.append(dic)







        except:
            dic = {}
            list_dics.append(dic)
        sleep(randint(0, 1))

    # print(list_dics)
    return list_dics


def csv_medclinic():
    # url = "https://grls.rosminzdrav.ru/Ree_orgCI2.aspx?numDoc=&Name_Org=&region=&adr=&OrgOut=2&pageNum=1&order=num_doc&orderType=asc&datedoc=&CiAcrOrg=&status=1&except=0&all=0&isOld=0&num_doc_old=&date_doc_old=&name_org_old=&adr_old=&moduleId=2"
    i = 1
    k = 0
    sum = 0
    create_csv()
    while True:
        try:
            url = "https://grls.rosminzdrav.ru/Ree_orgCI2.aspx?numDoc=&Name_Org=&region=&adr=&OrgOut=2&pageNum={}&order=num_doc&orderType=asc&datedoc=&CiAcrOrg=&status=1&except=0&all=0&isOld=0&num_doc_old=&date_doc_old=&name_org_old=&adr_old=&moduleId=2".format(
                i)
            html = get_html(url)
            list_of_dics_one_page = get_info_for_each_page(html)
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
    print(i, "Pages\n", sum, "Med Clinics")


def excel_medic():
    book_new = Workbook()
    dic = {}
    sheet_new = book_new.active
    header = tuple(["ID_Med_Org",
                    "Name_Med_Org",

                    ])

    sheet_new.append(header)

    with open('dbs\\medOrg.csv', newline='', encoding='utf-8') as csv_file_clinics:
        csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
        for i in csv_reader_clinics:
            # print(lst(i[1:]))
            dic[lst(i[0:])] = None
            # try:
            #     i=[i[3],i[1],i[2],"","","","","",i[4]]
            #
            #     sheet_new.append(i)
            # except:
            #     pass

    for k in dic:
        try:
            i = k.split("####")[0:-1]

            i = [i[0], i[1]]
            #print(i)
            sheet_new.append(i)
        except:
            pass

        # print(k.split("####")[0:])
        # sheet_new.append()
    book_new.save("final_xls_tables\\Med_Org.xlsx")


if __name__ == "__main__":
    excel_medic()
