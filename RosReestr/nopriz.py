
import requests
from bs4 import BeautifulSoup
import csv


def writer_csv_include(dic):
    try:
        with open("include_nopriz.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
           # print(dic)
            if len(dic) == 5:
                writer.writerow(tuple(dic))

            else:
                print("csv len false")
    except Exception as e:
        print(str(e))

def writer_csv_exclude(dic):
    try:
        with open("exclude_nopriz.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
           # print(dic)
            if len(dic) == 5:
                writer.writerow(tuple(dic))

            else:
                print("csv len false")
    except Exception as e:
        print(str(e))


def get_html_(url):
    k = 0
    page = ""
    while page == '' or k < 5:
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
        soup = soup.find("tbody").findAll("a")
        #     # http://reestr.nostroy.ru/reestr/clients/152/members/389634
        for i in soup:
            # print(i.get("href"))
            list_of_links.append("http://reestr.nopriz.ru" + i.get("href"))
        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_info(html):
    dictionary = []
    try:
        soup = BeautifulSoup(html, "lxml")
        try:
            part1 = soup.find("table", class_="table").findAll("tr")[2].findAll("td")[1].text.strip()
        except:
            part1 = ""
        try:
            part2 = soup.find("table", class_="table").findAll("tr")[7].findAll("td")[1].text.strip()
        except:
            part2 = ""
        try:
            part3 = soup.find("table", class_="table").findAll("tr")[8].findAll("td")[1].text.strip()
        except:
            part3 = ""
        try:
            part4 = soup.find("table", class_="table").findAll("tr")[9].findAll("td")[1].text.strip()
        except:
            part4 = ""
        try:
            part5 = soup.find("table", class_="table").findAll("tr")[10].findAll("td")[1].text.strip()
        except:
            part5 = ""

        dictionary.append(part1)
        dictionary.append(part2)
        dictionary.append(part3)
        dictionary.append(part4)
        dictionary.append(part5)

        return dictionary






    except Exception as e:
        print(str(e))
        return dictionary


# def main():
#     url = "http://reestr.nopriz.ru/reestr?us_registrationNumber=&us_fullDescription=&s_title=%D0%AF%D0%B2%D0%BB%D1%8F%D0%B5%D1%82%D1%81%D1%8F%20%D1%87%D0%BB%D0%B5%D0%BD%D0%BE%D0%BC&m_fullDescription=&m_inn=&m_ogrnip=&m_registryRegistrationDate=&m_director=&sort=us.registrationNumber&direction=asc&page=1"
#     html = get_html_(url)
#     get_links(html)
#     get_info(get_html_("http://reestr.nopriz.ru/reestr/clients/319/members/19448802"))


def main():
    n = input("Является членом СРO - 0\nИсключен - 1\n")

    if n == "0":
        for index, j in enumerate(range(1, 2857)):  # link = 'http://reestr.nostroy.ru/reestr/clients/152/members/389651'

            list_of_links = []
            # url = "http://reestr.nostroy.ru/reestr?m_fulldescription=&m_shortdescription=&m_inn=&m_ogrnip=&bms_id=1&bmt_id=&u_registrationnumber=&sort=m.id&direction=asc&page={}".format(j)
            url = "http://reestr.nopriz.ru/reestr?us_registrationNumber=&us_fullDescription=&s_title=%D0%AF%D0%B2%D0%BB%D1%8F%D0%B5%D1%82%D1%81%D1%8F%20%D1%87%D0%BB%D0%B5%D0%BD%D0%BE%D0%BC&m_fullDescription=&m_inn=&m_ogrnip=&m_registryRegistrationDate=&m_director=&sort=us.registrationNumber&direction=asc&page={}".format(
                j)

            html = get_html_(url)
            list_of_links.extend(get_links(html))

            for link in list_of_links:
                html = get_html_(link)
                writer_csv_include(get_info(html))

            print(index + 1)
    else:
        for index, j in enumerate(range(1, 1881)):  # link = 'http://reestr.nostroy.ru/reestr/clients/152/members/389651'

            list_of_links = []
            # url = "http://reestr.nostroy.ru/reestr?m_fulldescription=&m_shortdescription=&m_inn=&m_ogrnip=&bms_id=1&bmt_id=&u_registrationnumber=&sort=m.id&direction=asc&page={}".format(j)
            url = "http://reestr.nopriz.ru/reestr?us_registrationNumber=&us_fullDescription=&s_title=%D0%98%D1%81%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD&m_fullDescription=&m_inn=&m_ogrnip=&m_registryRegistrationDate=&m_director=&sort=us.registrationNumber&direction=asc&page={}".format(j)

            html = get_html_(url)
            list_of_links.extend(get_links(html))

            for link in list_of_links:
                html = get_html_(link)
                writer_csv_exclude(get_info(html))

            print(index + 1)







if __name__ == "__main__":
    main()
