import time

from bs4 import BeautifulSoup
from selenium import webdriver
 
url = "http://regvk.com/id/"

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x935")
driver = webdriver.Chrome("chromedriver.exe", options=options)
k = 1
list_urls = []
list_numbers = []
with open("test.txt", "r") as target:
    for line in target:
        if line != "":
            list_urls.append(line)

for i in list_urls:
    try:
        i = i.strip()
        driver.get(url)
        elem = "/html/body/div/div/form/div[1]/p[2]/input"
        elem2 = "/html/body/div/div/form/div[2]/p/button"
        xp = driver.find_element_by_xpath(elem)
        time.sleep(2)

        xp.send_keys(i)
        time.sleep(2)
        driver.find_element_by_xpath(elem2).click()

        response = driver.page_source
        soup = BeautifulSoup(response, "lxml")
        soup = soup.find("div", class_="info").find_all("td")
        number = int(soup[1].contents[0].split(" ")[-1].strip())
        list_numbers.append(number)
        print(k, ";", i, ";", number)
        print(list_numbers)
    except:
        k = k + 1

# number1=[61052294, 98581330, 30487105, 104332051, 139923997, 61166138, 79145826, 157193952, 79690560, 68674315, 155862176, 45246659, 170580894, 132799222, 159146575, 164576778, 150451154, 64701856, 184435181, 156942049]
# number2=[103083994, 122628152, 107012240, 26147450, 67136012, 90000251, 23398121, 99045428, 118388868, 169847524, 180341768, 155590170, 168284815, 171719327,158004202, 107952616, 117412303, 111348662, 144181254, 45045130]
# number3=[71239327, 147350675, 144696914, 39830920, 121411271, 23168410, 164353276, 178623303, 177237500, 118960405]


print("dddd")
