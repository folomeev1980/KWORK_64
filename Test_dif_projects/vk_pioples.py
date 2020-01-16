import vk_api
import time
import csv
#3838

def create_csv(id):


    with open("ids.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((id,))


vk_session = vk_api.VkApi('+79211703064', '0205lazarev2')
vk_session.auth()



vk = vk_session.get_api()
users=vk.users.search(age_from=15,age_to=17,country=3,has_photo=1,count=100)
comments_number = users["count"] // 100
print(comments_number)
users = (users["items"])
for j in users:
    create_csv(j["id"])
print(users[0]["id"],"0")
time.sleep(2)



for index,i in enumerate(range(1, comments_number + 1)):
    users = vk.users.search(age_from=15,age_to=17,country=3,has_photo=1,count=100,offset=i * 100)
    users = (users["items"])
    #print(users)
    for j in users:
        create_csv(j["id"])
    print(users[0]["id"],index+1)
    time.sleep(2)