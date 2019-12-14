from ast import literal_eval
import vk
import time
import random
from ClassesVK import Logger
from captcha_res import *
from ModulesVK import *
from captcha_res import *


def vk_parser(
    format_,
    direction,
    group_id_list,
    date_start,
    date_end,
    comments,
    likes,
    ads,
    token,
    list_of,
):
    mdir(direction)

    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)

    #
    params = combinator(
        vk_api, group_id_list, date_start, date_end, comments, likes, ads
    )

    for i in range(len(params)):
        list_of = list_of + get_group_posts(params[i], format_=format_)

    excel_creator(list_of)

    for i in list_of:
        download(i["video"], direction)


def vk_post(
    format_, path_folder, min_shift, token_post, owner_id, captcha_sid_, captcha_key_
):

    time_zero = take_time(token_post, owner_id)

    if time_zero == None:
        print("\nServer don't response")

    elif len(list_files_folder(path_folder, format_)) < 1:

        print("\nOutput objects folder is empty")

    else:

        print("\nStart posting objects {}".format(format_))

        time_of_post = time_zero + (min_shift * 60)
        i = 1

        while len(list_files_folder(path_folder, format_)) > 0:

            poster_result = poster(
                token_post,
                owner_id,
                path_folder,
                time_of_post,
                format_,
                captcha_sid_,
                captcha_key_,
            )

            if poster_result[0] != None:
                number_of_posts = get_posts_number(token_post, owner_id)
                print(
                    "\n\npost uploaded {}, number of posts <<< {} >>>\n".format(
                        i, number_of_posts
                    ),
                    poster_result[0:1],
                    datetime.datetime.fromtimestamp(time_of_post),
                )

                with open(poster_result[1]) as existing_file:
                    existing_file.close()
                    os.remove(poster_result[1])
                    print("{} removed\n".format(poster_result[1].split("\\")[1]))

                if number_of_posts != 150:
                    time_of_post = time_of_post + (min_shift * 60)

                    time.sleep(random.randint(1, 3) * 60)
                    i = i + 1
                else:
                    Logger(
                        "Access to adding post denied: cannot schedule more than 150 posts."
                    )
                    time.sleep(43200)

            else:
                error = poster_result[2]

                Logger(error)

                if "14. Captcha needed." in str(error):

                    link_captcha = error.captcha_img
                    captcha_sid_ = error.captcha_sid

                    captcha_key_ = captcha_solve(link_captcha)

                elif (
                    "214. Access to adding post denied: can only schedule 25 posts on a day"
                    in str(error)
                ):

                    catcha25_timer = timer(
                        datetime.datetime.fromtimestamp(take_time(token_post, owner_id))
                    )
                    time_of_post = time_of_post + catcha25_timer

                    # print(datetime.datetime.fromtimestamp(time_of_post))
                    time.sleep(random.randint(1, 3) * 60)

                elif (
                    "Access to adding post denied: cannot schedule more than 150 posts."
                    in str(error)
                ):

                    Logger(error)
                    time.sleep(43200)

                elif "charmap" in str(error):

                    # file_name_del = list_files_folder(path_folder, format_)[0]
                    with open(poster_result[1]) as existing_file:
                        # existing_file.close()
                        os.remove(existing_file)

                else:

                    break


if __name__ == "__main__":

    data = ""
    path = "params_public158329271.txt"
    with open(path, "r") as f:
        for lines in f:
            data = data + lines

    d = literal_eval(data)

    ####################   NEED TO CHANGE ###############
    direction = "Output_Pictures"
    format_ = "jpg"
    captcha_sid_ = ""
    captcha_key_ = ""
    #####################################################
    group_id_list = d["group_id_list"]
    date_start = d["date_start"]
    date_end = d["date_end"]
    comments = d["comments"]
    likes = d["likes"]
    ads = d["ads"]
    token = d["token_parser"]
    list_of = []

    path_folder = direction + "\\"
    min_shift = d["min_shift"]
    token_post = d["token_post"]
    owner_id = d["owner_id"]

    # test_line
    ###################################################

    a = input(
        "Select '0' for PARSER,\nselect '1' for POST,\nselect '2' for Parser&Post:  \n"
    )
    Logger(d)
    if a == "0":

        vk_parser(
            format_,
            direction,
            group_id_list,
            date_start,
            date_end,
            comments,
            likes,
            ads,
            token,
            list_of,
        )
        input("\nParsing was done")

    elif a == "1":

        vk_post(
            format_,
            path_folder,
            min_shift,
            token_post,
            owner_id,
            captcha_sid_,
            captcha_key_,
        )

    else:
        vk_parser(
            format_,
            direction,
            group_id_list,
            date_start,
            date_end,
            comments,
            likes,
            ads,
            token,
            list_of,
        )
        vk_post(
            format_,
            path_folder,
            min_shift,
            token_post,
            owner_id,
            captcha_sid_,
            captcha_key_,
        )

