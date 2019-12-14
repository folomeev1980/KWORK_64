import requests
from RosMed2.Spec import get_append_list_of_doctors
from selenium import webdriver
from bs4 import BeautifulSoup

#river = webdriver.Chrome('chromedriver.exe')

url="https://grls.rosminzdrav.ru/CIExpert.aspx?expGUID=6BD61328-C9B0-48AA-8421-F9BB44F6D5BD"

# driver.get(url)
#
# page2="/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td[2]/a"
# page3="/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td[3]/a"
#
# ######"/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/div[2]/table/tbody/tr[3]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td[3]/a"
#
#
# driver.find_element_by_xpath(page2).click()
# html2=driver.page_source
# driver.find_element_by_xpath(page3).click()
# html3=driver.page_source






# soup = BeautifulSoup(html3, "lxml")
# list_of_doctors=[]
# tds = soup.find("table", class_="ts1").find_all("tr", class_="hi_sys")
# for td in tds:
#     temp = td.find_all("td")
#     a = (temp[-2].text.strip().split("-"))
#
#     b = (temp[-1].text.strip().split()[1][1:])
#     list_of_doctors.append([a[0], a[1], b])
# print(list_of_doctors)
print(get_append_list_of_doctors(url))
# driver.quit()