import requests
from bs4 import BeautifulSoup
import csv
from time import sleep


def writer_csv(dic):
    temp = []
    try:
        with open("nashdom.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # print(len(dic))
            if dic['Контактный телефон'] == "Web-сайт застройщика":
                dic['Контактный телефон'] = "-"
            if len(dic) == 6:

                temp.append(dic['Полное наименование'])
                temp.append(dic['Фактический адрес'])
                temp.append(dic['ИНН'])
                temp.append(dic['Руководитель компании'])
                temp.append(dic['Контактный телефон'])
                temp.append(dic['E-mail застройщика'])
                writer.writerow(tuple(temp))

            else:
                print("csv len false")
    except Exception as e:
        print(str(e))


def get_html_(url):
    sleep(0.5)
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
    dic = {}

    result = []
    try:
        list_of_links = []
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find("div", class_="styles__Table-sc-17it3za-0 cvQGSX").findAll("a")
        # print(soup)
        # print(soup)
        for i in soup:
            # list1.append(i.get("href"))
            dic[i.get("href")] = ""
        # for j in dic:
        #     list2.append(j)

        for k in dic:
            if k != None:
                if len(k.split("/")[-1]) < 6:
                    result.append(k)
        # print(result)
        # print(len(result))

        return result
    except Exception as e:
        print(e)
        return result


def get_info(html):
    temp = []
    dictionary = {}
    try:
        soup = BeautifulSoup(html, "lxml")
        soup1 = soup.find("div", class_="styles__BuilderCardContent-ub2eu9-3 hGQsdw").findAll("p")
        soup2 = soup.find("div", class_="styles__BuilderCardContent-ub2eu9-3 hGQsdw").findAll("a")

        #
        #
        for i in soup1:
            temp.append(i.text)

        mail = soup2[-1].get("href")
        if mail[0:4] == "mail":
            temp.append(mail.split(":")[1])
        else:
            temp.append("")

        for t in range(len(temp)):
            if temp[t] == 'ИНН':
                dictionary[temp[t]] = temp[t + 1]
            if temp[t] == 'Полное наименование':
                dictionary[temp[t]] = temp[t + 1]
            if temp[t] == 'Фактический адрес':
                dictionary[temp[t]] = temp[t + 1]
            if temp[t] == 'Руководитель компании':
                dictionary[temp[t]] = temp[t + 1]
            if temp[t] == 'Контактный телефон':
                dictionary[temp[t]] = temp[t + 1]
            if temp[t] == 'E-mail застройщика':
                dictionary[temp[t]] = temp[t + 1]
        #print(dictionary)
        return dictionary



    except Exception as e:
        print(str(e))
        return dictionary


def main():
    for index,j in enumerate(range(47)):
        url = "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/?page={}&limit=100".format(str(j))

        html = get_html_(url)
        links = get_links(html)

        for link in links:
            writer_csv(get_info(get_html_(link)))
        print(index)


if __name__ == "__main__":
    main()
