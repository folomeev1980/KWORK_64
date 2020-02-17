# with open("cities.txt", "r") as f:
#     for line in f:
#         if len(line) > 3:
#             s = ""
#             for j in line:
#                 if j == " ":
#                     j = ""
#                 if j == "-":
#                     j = ""
#                 s = s + j.lower()
#             with open("rewrite_cities.txt", "a") as w:
#                 w.write(s)

import requests

header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0'}
url="https://2gis.ru/bryansk/search/%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80"

print(requests.get(url,headers=header).text)