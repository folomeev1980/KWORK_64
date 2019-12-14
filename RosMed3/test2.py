from RosMed3.rosmed import excel_edit
import csv

def read_csv():
    dic = {}
    with open('doctors.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            dic[row[0]] = row[1]

    return dic

dic=read_csv()
#print(dic["25.10.2019_31.12.2019_621"])
print(dic["25.10.2019_15.03.2022_620"])
#print(len(dic))
#excel_edit(dic)
