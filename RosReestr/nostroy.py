import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool,freeze_support
from time import sleep
from datetime import datetime



global_lst=[]

class Count:
    c=0


count=Count()



def writer_csv(dic):
    try:
        with open("true_sro.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            if len(dic) == 7:
                writer.writerow(tuple(dic))

            else:
                print("csv len false")
    except Exception as e:
        print(str(e))



def get_html_(url):
    #sleep(0.5)
    k = 0
    page = ""
    while page == '':
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
            page = requests.get(url, headers=headers)
            return page.text
            break
        except:
            k += 1
            print("Connection refused by the doctor server..")
            print("Let me sleep for 10 seconds")
            # print("ZZzzzz...")
            sleep(10)
            # print("Was a nice sleep, now let me continue...")
            continue


def get_links(html):
    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find("tbody").findAll("tr", class_="sro-link")
        # http://reestr.nostroy.ru/reestr/clients/152/members/389634
        for i in soup:
            list_of_links.append("http://reestr.nostroy.ru" + i.get("rel"))
        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_info(html):
    dictionary = []
    try:
        soup = BeautifulSoup(html, "lxml")
        part1 = soup.find("tbody").findAll("tr")[3:6]
        part2 = soup.find("tbody").findAll("tr")[11:15]
        part = part1 + part2
        for i in part:
            dictionary.append(i.find("td").text.strip())
        #global_lst.append(dictionary)
        return dictionary
    except Exception as e:
        print(str(e))
        return dictionary


def make_all(url):
    count.c+=1

    html = get_html_(url)
    list_of_links_=get_links(html)

    for link in list_of_links_:
        html = get_html_(link)
        #global_lst.append(get_info(html))
        writer_csv(get_info(html))
    print(count.c*2)


def main():
    n = input("Является членом СРO - 0\nИсключен - 1\n")

    if n == "0":
        for index,j in enumerate(range(3001,6553)):#link = 'http://reestr.nostroy.ru/reestr/clients/152/members/389651'

            list_of_links = []
            url = "http://reestr.nostroy.ru/reestr?m_fulldescription=&m_shortdescription=&m_inn=&m_ogrnip=&bms_id=1&bmt_id=&u_registrationnumber=&sort=m.id&direction=asc&page={}".format(j)


            html = get_html_(url)
            list_of_links.extend(get_links(html))


            for link in list_of_links:
                html = get_html_(link)
                writer_csv(get_info(html))


            print(index+1)


# def main():
#
#     #6552
#     url = "http://reestr.nostroy.ru/reestr?m_fulldescription=&m_shortdescription=&m_inn=&m_ogrnip=&bms_id=1&bmt_id=&u_registrationnumber=&sort=m.id&direction=asc&page={}"
#     urls=[url.format(str(i)) for i in range(1,3001)]
#
#     with Pool(2) as p:
#         p.map(make_all,urls)
#
#     #print(global_lst)
#     #writer_csv(global_lst)




    # print(urls)



if __name__ == "__main__":
    freeze_support()
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

