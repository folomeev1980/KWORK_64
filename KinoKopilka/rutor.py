from bs4 import BeautifulSoup
from random import choice
import requests




def get_proxy():
    html = requests.get("https://free-proxy-list.net").text
    soup = BeautifulSoup(html, "lxml")
    trs = soup.find("table", id="proxylisttable").find_all("tr")[1:20]

    proxies = []
    for tr in trs:
        tds = tr.find_all("td")
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = "https" if "yes" in tds[6].text.strip() else "http"
        if schema == "https":
            proxy = {"schema": schema, "address": ip + ":" + port}

            proxies.append(proxy)
    return choice(proxies)


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    while True:
        try:
            p = get_proxy()
            proxy = {p["schema"]: p["address"]}
            print(proxy)
            r = requests.get(url, proxies=proxy, headers=headers, timeout=5)
        except:
            r = ""
        if r != "":
            break
    return r.text



def get_rutor(url):
    html=get_html(url)
    soup = BeautifulSoup(html, "lxml")
    print(soup.text)


if __name__=="__main__":
    get_rutor("http://rutor.info/search/0/0/000/4/Шестеро вне закона")

