import requests
from bs4 import BeautifulSoup


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
        soup = soup.find("div", class_="bx_catalog_text").findAll("span")
        s=0
        for i in soup:
            list_of_links.append(i.text)
            s=s+int(i.text[1:-1])
        print(s)
        return list_of_links
    except Exception as e:
        print(e)
        return list_of_links

url = "https://gis-zkh.ru/upravlaushie-kompanii-rossii/"
level1 = get_links_level1(get_html_(url))