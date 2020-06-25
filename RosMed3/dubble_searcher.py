import requests

url_orig=    "https://grls.rosminzdrav.ru/CiPermitionReg.aspx?PermYear=0&DateInc=&NumInc=&DateBeg=&DateEnd=&Protocol=&RegNm=&Statement=&ProtoNum=&idCIStatementCh=&Qualifier=&CiPhase=&RangeOfApp=&Torg=&LFDos=&Producer=&Recearcher=&sponsorCountry=&MedBaseCount=&CiType=&PatientCount=&OrgDocOut=2&Status=1%2c2%2c3%2c4&NotInReg=0&All=0&PageSize={}&order=date_perm&orderType=desc&pagenum=".format(
        10000)

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

print(get_html(url_orig))