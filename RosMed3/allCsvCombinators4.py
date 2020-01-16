import os
import csv

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
    a = os.path.exists("clinics.csv")
    b = os.path.exists("doctors.csv")
    c = os.path.exists("criteria.csv")

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
                    "Для чего",
                    "Критерии Включения",
                    "Критерии Исключения"
                    ])
    with open("medlist_combination.csv", "w", newline='', encoding='ansi', ) as f:
        csv_writer_medlist = csv.writer(f, delimiter=';')
        csv_writer_medlist.writerow(header)


def csv_combinators():
    if check():

        create_csv()

        with open('clinics.csv', newline='', encoding='utf-8') as csv_file_clinics:
            csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
            for index, line_from_clinic in enumerate(csv_reader_clinics):

                combo_line = line_from_clinic[0:-1] + ["", "", ""]

                with open("doctors.csv", newline='', encoding='utf-8') as csv_file_doctors:
                    csv_reader_doctors = csv.reader(csv_file_doctors, delimiter=';')
                    for line_from_doctor in csv_reader_doctors:
                        if line_from_doctor[0] == "{}_{}_{}".format(line_from_clinic[7], line_from_clinic[8],
                                                                    line_from_clinic[1]) and blanker(
                            line_from_doctor[2]) in blanker(line_from_clinic[17]):
                            combo_line = line_from_clinic[0:-1]
                            combo_line.append(line_from_doctor[1])
                            combo_line.append(line_from_doctor[3])
                            combo_line.append(line_from_doctor[4])

                with open("medlist_combination.csv", "a", newline='', encoding='ansi',
                          errors="ignore") as csv_file_medlist:
                    csv_writer_medlist = csv.writer(csv_file_medlist, delimiter=';')
                    # print(combo_line)
                    csv_writer_medlist.writerow(tuple(combo_line))

                    print(index, combo_line[-3])





    else:
        print("Please files (clinics.csv, doctors.csv, criteria.csv) exist")


def csv_dictionares_combinator():
    if check():
        clinics = {}
        doctors = {}
        criteria = {}

        minx = 10000
        miny = 10000

        create_csv()

        with open('clinics.csv', newline='', encoding='utf-8') as csv_file_clinics:
            csv_reader_clinics = csv.reader(csv_file_clinics, delimiter=';')
            for index, line_from_clinic in enumerate(csv_reader_clinics):
                if index > 0:
                    key1 = "{}_{}_{}".format(line_from_clinic[7], line_from_clinic[8], line_from_clinic[1])
                    key2 = line_from_clinic[17]
                    key3 = line_from_clinic[9]
                    if len(key2) < minx:
                        minx = len(key2)
                    clinics[key1 + "****" + key2 + "****" + key3] = line_from_clinic

        with open("doctors.csv", newline='', encoding='utf-8') as csv_file_doctors:
            csv_reader_doctors = csv.reader(csv_file_doctors, delimiter=';')
            for index, line_from_doctor in enumerate(csv_reader_doctors):
                if index > 0:
                    key3 = line_from_doctor[0]
                    key4 = line_from_doctor[2]
                    if len(key4) < miny:
                        miny = len(key4)

                    doctors[key3 + "++++" + key4] = line_from_doctor

        with open("criteria.csv", newline='', encoding='utf-8') as csv_file_criteria:
            csv_reader_criteria = csv.reader(csv_file_criteria, delimiter=';')
            for index, line_from_criteria in enumerate(csv_reader_criteria):
                if index > 0:
                    key6 = line_from_criteria[0]

                    criteria[key6] = line_from_criteria

        # print(len(clinics),len(doctors))
        # print(minx,miny)
        # print(clinics)

        s = 1
        z = 0
        for count, c in enumerate(clinics):
            combo = clinics[c][0:-1] + ["", "", "", "", "", ""]
            result = list(set(zabolevanie) & set(separator(combo[15])))
            # print(combo)
            first = c.split("****")
            for d in doctors:
                second = d.split("++++")

                if first[0] == second[0] and blanker(second[1]) in blanker(first[1]):
                    combo[18] = doctors[d][1]
                    combo[19] = doctors[d][3]
                    combo[20] = doctors[d][4]
                    break

            if len(result) > 0:
                combo[21] = pacient(combo[10])
                # print(combo)

            if first[2] in criteria:
                combo[22] = criteria[first[2]][1]
                combo[23] = criteria[first[2]][2]

            with open("medlist_combination.csv", "a", newline='', encoding='ansi',
                      errors="ignore") as csv_file_medlist:
                csv_writer_medlist = csv.writer(csv_file_medlist, delimiter=';')
                csv_writer_medlist.writerow(tuple(combo))
            if count % 500 == 0:
                print("Processed line ...  ", count)
    else:
        print("Please files (clinics.csv, doctors.csv, criteria.csv) exist")

# if __name__=="__main__":
#     csv_dictionares_combinator()
