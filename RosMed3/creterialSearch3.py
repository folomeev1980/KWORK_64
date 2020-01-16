import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import csv
from selenium import webdriver
from googletrans import Translator

type_res = ["КИ", "ММКИ"]
zabolevanie = ["Гематология", "Онкология", "гематология", "онкология", "Онкогематология", 'Онкология']
dictionary_research_numbers = {}


def separator(s):
    s = s.replace(",", ";").replace(":", ";").replace(" ", ";").split(";")
    return list(s)


def create_csv():
    header = tuple(["Исследование",
                    "Inclusion",
                    "Exclusion"])

    with open("criteria.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)


def get_html(url):
    page = ""
    while page == '':
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
            page = requests.get(url, headers=headers)
            return page.text
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 10 seconds")
            # print("ZZzzzz...")
            sleep(10)
            # print("Was a nice sleep, now let me continue...")
            continue


def webdriver_url_parce(url):
    html = ""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get(url)
        html = (driver.page_source)
        driver.close()
        driver.quit()
        return html
    except:
        print("webdriver open fail")
        driver.close()
        driver.quit()
        return html


def get_html_link(url):
    spl = []
    dict = {"Inclusion Criteria": None, "Exclusion Criteria": None}
    k = 0

    while k <= 5:
        try:
            html = webdriver_url_parce(url)
            soup = BeautifulSoup(html, "lxml")
            res = soup.find("div", class_="ct-inner_content_wrapper").text.split(" ")[0]

            if res != "No":

                soup = soup.find("table", id="theDataTable").findAll('a')
                for sp in soup:
                    spl.append(sp.get("href"))

                link = "https://clinicaltrials.gov" + spl[-1]
                second_page = webdriver_url_parce(link)
                soup_second = BeautifulSoup(second_page, "lxml")
                soup_second = soup_second.find("div", id="main-content").find("div", id="tab-body").find("div",
                                                                                                         class_="tr-indent2").findAll(
                    "div", class_="tr-indent1")[1].findAll("div", class_="tr-indent2")[1].find("div",
                                                                                               class_="tr-indent2")
                soup_second = soup_second.findAll("ul")

                translator = Translator()
                inclose = translator.translate(soup_second[0].text.strip(), dest='ru')
                unclose = translator.translate(soup_second[1].text.strip(), dest='ru')

                dict["Inclusion Criteria"] = inclose.text
                dict["Exclusion Criteria"] = unclose.text
                return dict
                break

            else:
                return dict
                break

        except:
            k = k + 1
            continue


def excel_read_creteria():
    line_count = 0
    with open('clinics.csv', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if line_count >= 1:
                # print(str(row[12]),type_res)
                if row[12] in type_res:

                    result = list(set(zabolevanie) & set(separator(row[15])))

                    if len(result) > 0:
                        temp = (str(row[9]))
                        # print(temp)
                        dictionary_research_numbers[temp] = None
            line_count += 1


def make_all(i):
    url = "https://clinicaltrials.gov/ct2/results?cond=&term={}&cntry=&state=&city=&dist=".format(i)

    dictionary_research_numbers[i] = get_html_link(url)
    with open("criteria.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if dictionary_research_numbers[i] != None:
            a = i
            b = dictionary_research_numbers[i]["Inclusion Criteria"]
            c = dictionary_research_numbers[i]["Exclusion Criteria"]
            writer.writerow((a, b, c))
            print(a)


def criteria_maker():
    create_csv()
    excel_read_creteria()
    print("\nLengths of research\n", len(dictionary_research_numbers))
    #print(dictionary_research_numbers)
    # with Pool(7) as p:
    #     p.map(make_all, dictionary_research_numbers)
    #map(make_all, dictionary_research_numbers)
    for i in dictionary_research_numbers:
        make_all(i)


if __name__ == "__main__":
    criteria_maker()
