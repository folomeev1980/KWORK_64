import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


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


def get_info(html):
    dictionary = []
    # dic={}

    # x=(html.find("<table class=\"detail-view table table-striped table-condensed\" id=\"yw1\">"))
    # html1=html[x:-1]
    #
    # try:
    soup1 = BeautifulSoup(html, "lxml")
    #     soup2 = BeautifulSoup(html1,"lxml")
    soup1 = soup1.find("div", class_="container fix-height").findAll("div", class_="book-container")
    for i in soup1:
        dictionary.append("https://english-e-reader.net" + i.find("a").get("href"))

    return dictionary


def get_files(url):

    try:
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('window-size=1920x1200')
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
    except Exception as e:
        print(e)
        driver.quit()

    try:
        element = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/h3")

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[2]/div[7]/div/div/button[1]").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[2]/div[8]/a").click()

        sleep(200)



    except Exception as e:
        print(e)

    driver.quit()


if __name__ == "__main__":

    html = get_html_("https://english-e-reader.net/level/elementary")
    links = (get_info(html))
    for index,i in enumerate(links):
        print(i, "\n{} from {}".format(str(index+1),str(len(links))))
        get_files(i)
