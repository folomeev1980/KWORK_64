import csv
lst=[]
lst2={}
with open('nedv_omsk.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for index,row in enumerate(readCSV):
        #print(row[2])
        lst2[row[2]+row[-1]]=row


    print(index)
    print(len(lst2))




with open('nedv_omsk_cleaning.csv', mode='a') as speed_test:
    speed_test = csv.writer(speed_test, delimiter=';', lineterminator='\n')
    for row in lst2:
        temp=tuple(lst2[row])
        #print(temp)
        speed_test.writerow(temp)
