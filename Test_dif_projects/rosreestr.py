
import requests



url="http://reestr.nostroy.ru/reestr?sort=m.id&direction=asc&page=1"

r=requests.get(url)
print(r.text)