# http://sro-sso.ru/reestr_sro/view?id=52


import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support
from time import sleep
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
global_lst = []


class Count:
    c = 0


count = Count()


def writer_csv_include(dic):
    mail = "e-mail:"
    if mail not in dic:
        dic[mail] = ""
    else:
        print(dic[mail])

    try:
        with open("srodoms.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            if dic[mail] != "":
                t = (dic[mail],

                     )

                writer.writerow(t)
    except Exception as e:
        print(e)


def get_html_(url):
    # sleep(0.5)
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


def get_info(url):
    dic={}
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1200')
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
    except Exception as e:
        print(e)
        driver.quit()

    try:
        element = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[15]/div/div[1]")

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        txt=driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[13]/span[2]/span/strong/span/a[2]").text
        print(txt)



        return dic
    except Exception as e:

        print(str(e))
        return dic


if __name__ == "__main__":

    for i in range(134, 150):
        print(i)
        url = "http://srodms.ru/index.php?option=com_content&view=article&id={}".format(str(i))
        writer_csv_include(get_info(url))
