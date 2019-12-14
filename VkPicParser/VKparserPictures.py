import vk
import os
from ast import literal_eval
from openpyxl import Workbook
import datetime
from requests import get


def photo_video_choice(post):
    post_dic = {}

    if post['attachments'][0]["type"] == "photo":
        # print(post)
        photo = dict(post['attachments'][0]["photo"]["sizes"][-1])
        post_dic['video'] = photo["url"]
        #post_dic['video'] = None
        return post_dic
    else:
        # print("ok")
        # print()
        # video = dict(post['attachments'][0]["doc"]["url"])
        # print(post['attachments'][0]["doc"]["url"])
        # post_dic['video'] = post['attachments'][0]["doc"]["url"]
        post_dic['video'] = None
        return post_dic


def get_comments(vk_api, owner_id, post_id):
    comments = vk_api.wall.getComments(
        owner_id=owner_id * (-1), post_id=post_id, count=100, need_likes=1, v=5.101)
    comments_number = comments["count"] // 100

    comments = (comments["items"])
    likes = comments[0]["likes"]["count"]
    text = comments[0]["text"]

    for i in range(1, comments_number + 1):
        comments = comments + vk_api.wall.getComments(
            owner_id=owner_id * (-1), post_id=post_id, need_likes=1, count=100, v=5.101, offset=i * 100)["items"]

    for index, comment in enumerate(comments):
        if comment["likes"]["count"] > likes:
            likes = comment["likes"]["count"]
            text = comment["text"]

    return {"text_comment": text, "likes_comment": likes}


def get_group_posts(*args):
    args = args[0]
    print(args)
    vk_api = args[0]
    owner_id = args[1]
    date1 = args[2]

    date2 = args[3]
    namber_comments_of = args[4]
    likes = args[5]
    ads = args[6]

    post_dic = {}
    posts_list = []
    exception_numbers = 0
    date_start = datetime.datetime(date1[0], date1[1], date1[2])
    date_end = datetime.datetime(date2[0], date2[1], date2[2], 23, 59)

    posts = vk_api.wall.get(owner_id=owner_id * (-1),
                            count=100, filter=all, v=5.101)

    count_numbers = posts["count"] // 100

    posts = posts["items"]

    # Получаем первую дату поста

    for i in range(1, count_numbers + 1):
        print("Reading {} block {}".format(i, owner_id))

        temp = vk_api.wall.get(owner_id=owner_id * (-1), count=100, filter=all,
                               v=5.101, offset=i * 100)["items"]

        start_block = datetime.datetime.fromtimestamp(temp[0]["date"])
        end_block = datetime.datetime.fromtimestamp(temp[len(temp) - 1]["date"])

        if start_block > date_start:
            if end_block < date_end:
                posts = posts + temp
                print("posts block --{}-- is writting".format(i * 100))
        else:
            break

        # time.sleep(2)

    for index, post in enumerate(posts):
        try:
            d = datetime.datetime.fromtimestamp(post['date'])
            # print(d,date_start,date_end)
            if d >= date_start:
                if d <= date_end:

                    post_dic["date"] = d
                    post_dic["id"] = post["id"]
                    post_dic["text"] = post["text"]
                    post_dic['marked_as_ads'] = post['marked_as_ads']
                    # video = dict(post['attachments'][0]["doc"]["preview"]["video"])
                    post_dic['video'] = (photo_video_choice(post))['video']
                    # post_dic['filesize'] = (dict(video)['file_size'])
                    post_dic['comments'] = post['comments']["count"]

                    if post_dic['comments'] > 0:
                        dic_ret = get_comments(vk_api, owner_id, post_dic["id"])
                        post_dic['text_comment'] = dic_ret["text_comment"]
                        post_dic['likes_comment'] = dic_ret["likes_comment"]
                    else:
                        post_dic['text_comment'] = ""
                        post_dic['likes_comment'] = ""

                    post_dic['post_likes'] = post['likes']["count"]
                    post_dic['reposts'] = post['reposts']["count"]
                    post_dic['views'] = post['views']["count"]

                    if post_dic["date"] != "":
                        if post_dic['comments'] > namber_comments_of:
                            if post_dic['likes_comment'] > likes:
                                if post_dic['marked_as_ads'] == ads:
                                    if post_dic["video"] != None:
                                        posts_list.append(post_dic)



        except:
            exception_numbers += 1
            # post_dic = {"date": "", "id": "", "text": "", 'marked_as_ads': "", 'video': "",
            #             'comments': "", 'text_comment': "", 'likes_comment': "", 'post_likes': "", 'reposts': "",
            #             'views': ""}

        if index % 10 == 0:
            print("{} posts  {} was parsed".format(owner_id, index))
        post_dic = {}
    print("Exception numbers is {} from {} pages x 100 posts ".format(
        exception_numbers, count_numbers))

    return posts_list


def excel_creator(dic_list):
    print("Start to create xlx file")
    # dir = os.path.abspath(os.curdir)
    list_of_items = []

    book = Workbook()
    sheet = book.active
    # post_dic = {"date": "", "id": "", "text": "", 'marked_as_ads': "", 'video': "",
    # 'filesize': "", 'comments': "", 'text_comment': "", 'post_likes': "",
    # 'likes_comment': "", 'reposts': "", 'views': ""}
    sheet.append(["Дата и время", "Название поста", "Реклама", "Колличество комментов",
                  "Текст лучшего коммента", "Колличество лайков лучшего коммента", "Название Файла",
                  "Ссылка на гифку для скачивания"])
    for dic in dic_list:
        list_of_items.append(dic["date"])
        list_of_items.append(dic["text"])
        list_of_items.append(dic['marked_as_ads'])
        list_of_items.append(dic['comments'])
        list_of_items.append(dic['text_comment'])
        list_of_items.append(dic['likes_comment'])
        list_of_items.append(filename(dic['video']))
        list_of_items.append('=HYPERLINK("{}", "{}")'.format(
            dic["video"], "Ссылка на Гифку"))
        #
        sheet.append(list_of_items)
        list_of_items = []

    book.save("VK_list.xlsx")
    print("file was done")


def combinator(a, list_, *args):
    combinator_list = []

    for i in list_:
        temp = [a] + [i] + list(args)
        temp = (tuple(temp))
        combinator_list.append(temp)

    return combinator_list


def filename(url):
    # dir = os.path.abspath(os.curdir)
    if url[-3:] == "jpg":
        file_name = url.split("/")[-1]
        file_name = file_name[:-3] + "jpg"

    else:
        file_name = url.split("/")[-1][0:21] + ".non"

    return file_name


def download(url):
    dir = os.path.abspath(os.curdir)
    if url[-3:] == "jpg":
        file_name = url.split("/")[-1]
        file_name = file_name[:-3] + "jpg"

    else:
        file_name = url.split("/")[-1][0:21] + ".non"

    print("Downloading...   ", dir + "\Output_Pictures\\" + file_name)

    try:
        # open in binary mode
        with open(dir + "\Output_Pictures\\" + file_name, "wb") as file:
            # get request
            response = get(url)
            # write to file
            file.write(response.content)
            file.close()
    except Exception as e:
        print((e))
        with open('log.txt', "a") as file:
            file.write(str(datetime.datetime.now()) + "  ...parser...  " + str(e))
        file.close()


def mdir():
    mypath = "Output_Pictures"
    if not os.path.isdir(mypath):
        os.makedirs(mypath)


def main():
    #
    #

    mdir()

    data = ""
    path = 'params.txt'
    with open(path, 'r') as f:
        for lines in f:
            data = data + lines
    d = (literal_eval(data))

    group_id_list = d["group_id_list"]
    date_start = d["date_start"]
    date_end = d["date_end"]
    comments = d["comments"]
    likes = d["likes"]
    ads = d["ads"]
    token = d["token_parser"]
    list_of = []

    # print(token)
    # token = "c245d97cc245d97cc245d97cddc228922acc245c245d97c9fd9c6af99ad638667c086c5"
    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)

    params = combinator(vk_api, group_id_list, date_start, date_end, comments, likes, ads)

    # with Pool(10) as p:
    #     p.map(get_group_posts,params)
    #
    # print(list_of)
    #
    for i in range(len(params)):
        list_of = list_of + get_group_posts(params[i])

    excel_creator(list_of)

    for i in list_of:
        download(i['video'])

if __name__ == "__main__":
    # multiprocessing.freeze_support()
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print("Duration: {}".format(end - start))
