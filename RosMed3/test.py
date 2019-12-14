from RosMed3.rosmed import excel_edit
import csv

def read_csv():
    # dic = {}
    dic = []
    with open('doctors.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            # dic[row[0]] = row[1]
            dic.append([row[0], row[1], row[2]])

    return dic

dic=read_csv()
print(len(dic))
excel_edit(dic)
