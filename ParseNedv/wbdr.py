from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from random import randint
#url = "https://omsk.mlsn.ru/pokupka-nedvizhimost/?isResale=1&page=1&viewMode=paper"


def wbdr(url):
    i=0
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x935")
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.get(url)
    time.sleep(randint(10,20))
    element = driver.find_elements_by_class_name("btn-contacts")
    if len(element) != 0:
        for k in element:
            #element = driver.find_element_by_class_name("btn-contacts")

            actions = ActionChains(driver)
            actions.move_to_element(k).perform()
            k.click()


            #
            i = i + 1
            if i%5==0:
                print(i,end="")

    response = driver.page_source
    driver.close()
    driver.quit()
    return response


    #print(response)




    #response = driver.page_source
    # soup = BeautifulSoup(response, "lxml")
    # soup = soup.findAll("div", class_="speed-progress-bar__value")
    # upload = soup[0].text.strip().split("=")[0].strip().split(" ")
    # download = soup[1].text.strip().split("=")[0].strip().split(
    #     " ")
    # tm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # driver.close()
# print(upload, download)

#wbdr(url)