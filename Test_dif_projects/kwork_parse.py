import requests
from selenium import webdriver

url="https://spb.saturn.net/catalog/?search=&s=%D0%BE&sp%5Bname%5D=1&sp%5Bshort_text%5D=1&sp%5Bartikul%5D=1&price_min=0&price_max=1000000"


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get(url)

print(driver.page_source)
            #

# headers = {
#     'User-Agent': 'My User Agent 1.0',
#     'From': 'youremail@domain.com'  # This is another valid field
# }
#
# r=requests.get(url)
#
# print(r.text)