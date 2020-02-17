import requests
from bs4 import BeautifulSoup
import csv
from time import sleep


def writer_csv(lst):
    temp = []
    try:
        with open("list_of giszkh.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for i in lst:

                writer.writerow([i])

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


def get_links_level1(html):
    dic = {}

    result = []
    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find("div", class_="bx_catalog_text").findAll("a")

        for i in soup:
            list_of_links.append("https://gis-zkh.ru" + i.get("href"))

        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_links_level2(html):
    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        # print(soup)
        soup = soup.find("ul", class_="bx_catalog_text_ul").findAll("a")

        for i in soup:
            list_of_links.append("https://gis-zkh.ru" + i.get("href"))
        #
        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_links_level3(html):
    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        # print(soup)
        soup = soup.find("ul", class_="bx_catalog_text_ul").findAll("a")

        for i in soup:
            list_of_links.append("https://gis-zkh.ru" + i.get("href"))
        #
        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_links_level4(html):
    try:
        list_of_links = []
        list_of_added_links = []
        soup = BeautifulSoup(html, "lxml")
        # print(soup)
        l = soup.find("div", class_="catalog-section").findAll("a")

        for i in l:
            if i.get("href") != None:
                if ("https://gis-zkh.ru" + i.get("href"))[-2:] != "20":
                    list_of_links.append("https://gis-zkh.ru" + i.get("href"))
                else:
                    list_of_added_links.append("https://gis-zkh.ru" + i.get("href"))

        if len(list_of_added_links) > 0:
            new_lst = []
            form = list_of_added_links[0].split("=")[0]
            max_ind = int(list_of_added_links[0].split("&SIZEN")[0].split("=")[1])

            for j in range(1, max_ind + 1):
                list_of_links.extend(get_added(form + "={}&SIZEN_1=20".format(str(j))))

            # list_of_added_links = list_of_added_links[:-1]
            # for k in list_of_added_links:
            #
            # print(max_ind)
            # print(form)
            # =134&SIZEN_1=20

        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_link_info(html):
    try:
        list_of_links = []

        soup = BeautifulSoup(html, "lxml")
        soup.f
        header = soup.find("h3", class_="text-center").text.strip()
        list_of_links.append(header)
        ruk = soup.find("div", class_="col-lg-5 ank-text").text

        # for i in ruk:
        #     print(i)
        #     print(i.findNext().text)
        # print(ruk1)
        # if "<b>Контактная информация</b>" in ruk:
        #     print("ok")
        # print(ruk)
        ruk = ruk.replace("\t\t\t", ":")
        ruk = ruk.replace("\n", ":")
        ruk = ruk.replace(":::", ":")
        ruk = ruk.split(":")
        # print(ruk)
        #print(ruk)
        for i in range(len(ruk)):
            if ruk[i] == 'Руководитель':
                list_of_links.append(ruk[i + 1])
            if ruk[i] == 'Телефон':
                list_of_links.append(ruk[i + 1])
            if ruk[i] == 'E-mail':
                list_of_links.append(ruk[i + 1])
            if ruk[i] == 'ИНН':
                list_of_links.append(ruk[i + 1])
            if ruk[i] == 'Адрес':
                list_of_links.append(ruk[i + 1])

        # list_of_links.append(ruk[3])
        # list_of_links.append(ruk[5])
        # list_of_links.append(ruk[7])
        # list_of_links.append(ruk[12])
        # list_of_links.append(ruk[16])

        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def get_added(url):
    html = get_html_(url)

    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        # print(soup)
        l = soup.find("div", class_="catalog-section").findAll("a")
        for i in l:
            if i.get("href") != None:
                if ("https://gis-zkh.ru" + i.get("href"))[-2:] != "20":
                    list_of_links.append("https://gis-zkh.ru" + i.get("href"))

        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links


def link_maker():
    level2 = []
    level3 = []
    level4 = []
    url = "https://gis-zkh.ru/upravlaushie-kompanii-rossii/"
    level1 = get_links_level1(get_html_(url))

    # url="https://gis-zkh.ru/upravlaushie-kompanii-rossii/khanty_mansiyskiy_avtonomnyy_okrug_yugra/"
    for link in level1:
        level2.extend(get_links_level2(get_html_(link)))

    for index, link in enumerate(level2):
        level3.extend(get_links_level3(get_html_(link)))
        if index % 100 == 0:
            print(index)
    for index, link in enumerate(level3):
        level4.extend(get_links_level4(get_html_(link)))
        if index % 100 == 0:
            print(index, len(level3))

    # print(level4)
    print(len(level4))
    writer_csv(level4)


def get_cvs_links():
    dic = {}
    with open("list_of giszkh.csv", newline='') as csv_file_links:
        csv_reader_links = csv.reader(csv_file_links, delimiter=';')
        for index, link in enumerate(csv_reader_links):
            # print(link)
            dic[str(link)] = None

    return (dic)


def writer_csv_list(dic):
    try:
        with open("giszkh_all.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            #print(dic)
            if len(dic) == 6:
                writer.writerow(tuple(dic))

            # else:
            #     print("csv len false")
    except Exception as e:
        print(str(e))


def main():
    #
    #
    links = get_cvs_links()
    # print(len(links))

    # link_maker()

    # url = "https://gis-zkh.ru/upravlaushie-kompanii-rossii/khanty_mansiyskiy_avtonomnyy_okrug_yugra/r_n_nefteyuganskiy/"
    # # print(get_links_level2(get_html_(url)))
    #
    # print(get_links_level3(get_html_(url)))
    #
    # url = "https://gis-zkh.ru/upravlaushie-kompanii-rossii/g_moskva/g_moskva/g_moskva/"
    # print(len(get_links_level4(get_html_(url))))
    # print(get_links_level4(get_html_(url)))

    # url='https://gis-zkh.ru/upravlaushie-kompanii-rossii/altayskiy_kray/g_aleysk/g_aleysk/munitsipalnoe_unitarnoe_predpriyatie_proizvodstvennoe_zhilishchno_eksplutatsionnoe_upravlenie_1_goro/'
    # html=get_html_(url)
    # print(get_link_info(html))

    dic = get_cvs_links()
    # print(dic)
    # lis=[]
    for index, key in enumerate(dic):
        # lis.append(key)
        key = (str(key)[2:-2])

        writer_csv_list(get_link_info(get_html_(key)))
        if index%100==0:
            print(index)


if __name__ == "__main__":
    main()
