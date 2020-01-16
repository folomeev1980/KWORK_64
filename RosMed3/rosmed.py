import datetime
from doctorsCvs2 import cvs_doctors
from rowExcelCreator1 import creator
from creterialSearch3 import criteria_maker
from allCsvCombinators4 import csv_dictionares_combinator
from excelCreator5 import excel


def main():
    i = input(
        "Chose action:\n1 - parse db researches\n2 - parse db doctors\n3 - parse "
        "criteria\n4 - Combination full data\n5 - generate xls file\n6 - for all actions\n\n")

    if i == "1":
        creator()

    elif i == "2":
        cvs_doctors()

    elif i == "3":
        criteria_maker()

    elif i == "4":
        csv_dictionares_combinator()

    elif i == "5":
        excel()
    else:

        creator()
        cvs_doctors()
        criteria_maker()
        csv_dictionares_combinator()
        excel()


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print("Duration: {}".format(end - start))
    input("\nPRESS any batton to complete.....")
