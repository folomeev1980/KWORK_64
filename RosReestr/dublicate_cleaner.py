import csv


def get_cvs_links(filename):
    dic = {}
    with open(filename, newline='') as csv_file_links:
        csv_reader_links = csv.reader(csv_file_links, delimiter=';')
        for index, link in enumerate(csv_reader_links):
            print(link)
            dic[link[4]] = link

    return (dic)

def write_cvs_links(filename,dic):
    with open(filename, "a", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # print(dic)
        for key in dic:
            #print(dic[key])
            writer.writerow(tuple(dic[key]))


input=get_cvs_links("giszkh_all.csv")
write_cvs_links("giszkh_all_no_duplicate_copy.csv",input)