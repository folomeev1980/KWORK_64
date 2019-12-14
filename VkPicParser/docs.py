import requests

url="http://dogsfiles.com/index.php?ind=dogsbase&breed=339&op=search"
r=requests.get(url)

print(r.text)
