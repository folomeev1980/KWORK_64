import os
import csv
from progress.bar import Bar
import requests
import csv
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup
from random import randint
from time import sleep





files_exist = True
zabolevanie = ["Гематология", "Онкология", "гематология", "онкология", "Онкогематология", 'Онкология']


def separator(s):
    s = s.replace(",", ";").replace(":", ";").replace(" ", ";").split(";")
    return list(s)


def blanker(s):
    n = ""
    for i in s:
        if i in "\'\"<>:; .,-":
            pass
        else:
            n = n + i
    return n


def blanker2(s):
    n = ""
    for i in s:
        if i in "ао":
            n = n + i
        else:
            pass
    return n


def pacient(s):
    l = ["пациент", "Пациент", "Детей", "детей", "Терап", "терап", "Лечен", "лечен"]
    otvet = ""

    for i in l:
        ind = s.find(i)
        if ind != -1:
            otvet = "Для " + s[ind:]
            break

    return otvet


def check():
    # print(files_exist)
    a = os.path.exists("dbs\\clinics.csv")
    b = os.path.exists("dbs\\doctors.csv")
    c = os.path.exists("dbs\\medOrg.csv")

    return a * b * c


def create_csv():
    header = tuple(["номер п/п",
                    "Номер РКИ",
                    "Дата создания РКИ",
                    "Наименование ЛП",
                    "Организация, проводящая КИ",
                    "Страна разраб-ка",
                    "Организация, привлеченная разработчиком ЛП",
                    "Начало (дата)",
                    "Окончание (дата)",
                    "№ протокола",
                    "Протокол",
                    "Фаза КИ",
                    "Вид КИ",
                    "Колич. мед. орг-й",
                    "Колич. пациент.",
                    "Области применения",
                    "Состояние",
                    "Перечень медицинских организаций, в которых предполагается проведение клинических исследований",
                    "ФИО Главного Исследователя",
                    "Код врача",
                    "День рождения врача",
                    "Код клиники",

                    ])
    with open("dbs\\medlist_combination.csv", "w", newline='', encoding='ansi', ) as f:
        csv_writer_medlist = csv.writer(f, delimiter=';')
       # csv_writer_medlist.writerow(header)


def csv_combinators():
    if check():

        create_csv()

        with open('dbs\\clinics.csv', newline='', encoding='utf-8') as csv_file_clinics:
            csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
            for index, line_from_clinic in enumerate(csv_reader_clinics):
                temp=[index,"","",line_from_clinic[0]]
                combo_line = line_from_clinic[0:-1] + ["", "", "", ""]
                #print(len(combo_line))
                #print("{}_{}_{}".format(line_from_clinic[7], line_from_clinic[8],line_from_clinic[1]))

                with open("dbs\\doctors.csv", newline='', encoding='utf-8') as csv_file_doctors:
                    csv_reader_doctors = csv.reader(csv_file_doctors, delimiter=';')
                    for line_from_doctor in csv_reader_doctors:
                        if line_from_doctor[0] == "{}_{}_{}".format(line_from_clinic[7], line_from_clinic[8],
                                                                    line_from_clinic[1]) and blanker(
                            line_from_doctor[2]) in blanker(line_from_clinic[17]):
                            combo_line = line_from_clinic[0:-1]
                            combo_line.append(line_from_doctor[1])
                            combo_line.append(line_from_doctor[3])
                            combo_line.append(line_from_doctor[4])
                            temp[2] = line_from_doctor[3]
                            break



                with open("dbs\\medOrg.csv", newline='', encoding='utf-8') as csv_file_org:
                    csv_reader_org = csv.reader(csv_file_org, delimiter=';')
                    for line_from_org in csv_reader_org:
                        if blanker(line_from_org[1]) in blanker(line_from_clinic[17]):
                            # combo_line = line_from_clinic[0:-1]
                            # combo_line.append(line_from_doctor[1])
                            # combo_line.append(line_from_doctor[3])
                            combo_line.append(line_from_org[0])
                            temp[1]=line_from_org[0]
                            break
                print(temp)
                with open("dbs\\medlist_combination.csv", "a", newline='', encoding='ansi',
                          errors="ignore") as csv_file_medlist:
                    csv_writer_medlist = csv.writer(csv_file_medlist, delimiter=';')

                   # csv_writer_medlist.writerow(tuple(combo_line))
                   #a=[index, str(combo_line[-1]),str(combo_line[-3]),str(combo_line[0])]
                    csv_writer_medlist.writerow(tuple(temp))


                   # print(index, combo_line[-1]+"  "+combo_line[-3]+"  "+combo_line[0])





    else:
        print("Please files (clinics.csv, doctors.csv, criteria.csv) exist")


def excel_combo():
    book_new = Workbook()
    dic = {}
    sheet_new = book_new.active
    header = tuple(["ID_Clin_Registry",
                    "ID_Med_Org",
                     "ID_PI",
                    "ID_Research"

                    ])

    sheet_new.append(header)

    with open('dbs\\medlist_combination.csv', newline='', encoding='utf-8') as csv_file_clinics:
        csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
        for i in csv_reader_clinics:
    #         # print(lst(i[1:]))
    #         dic[lst(i[0:])] = None
    #         # try:
    #         #     i=[i[3],i[1],i[2],"","","","","",i[4]]
    #         #
    #         #     sheet_new.append(i)
    #         # except:
    #         #     pass
    #
    # for k in dic:
    #     try:
    #         i = k.split("####")[0:-1]
    #
    #         i = [i[0], i[1]]
    #         # print(i)
            sheet_new.append(i)
        # except:
        #     pass

        # print(k.split("####")[0:])
        # sheet_new.append()
    book_new.save("final_xls_tables\\Clin_Registry.xlsx")


if __name__ == "__main__":
    csv_combinators()
