import datetime
from doctorsCvs2 import cvs_doctors, excel_doctors
from rowExcelCreator1 import creator, excel_research_creator
# from creterialSearch3 import criteria_maker
from Combinators import csv_combinators,excel_combo
# from excelCreator5 import excel
from medClinic3 import csv_medclinic, excel_medic


def main():
    i = input(
        "Chose action:\n1 - parse db Research\n2 - parse PI doctors\n3 - parse Med Organization "
        "\n4 - Combination of the data\n5 - for all actions\n\n")

    if i == "1":
        creator()
        excel_research_creator()

    elif i == "2":
        cvs_doctors()
        excel_doctors()


    elif i == "3":
        csv_medclinic()
        excel_medic()


    elif i == "4":
        csv_combinators()
        excel_combo()


    else:

        creator()
        excel_research_creator()
        cvs_doctors()
        excel_doctors()
        csv_medclinic()
        excel_medic()
        csv_combinators()
        excel_combo()


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print("Duration: {}".format(end - start))
    input("\nPRESS any batton to complete.....")
