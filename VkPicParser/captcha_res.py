



def get_captcha_key():
    with open('captcha_key.txt','rt') as f:
        return f.read().replace('\n','')

RUCAPTCHA_KEY = get_captcha_key()
print()

def captcha_solve(captcha_link):
    from python_rucaptcha import ImageCaptcha,RuCaptchaControl
    answer = RuCaptchaControl.RuCaptchaControl(
        rucaptcha_key=RUCAPTCHA_KEY
    ).additional_methods(action="getbalance")
    print("Checking Rucaptcha balance: ", answer['serverAnswer'])
    image_link = captcha_link
    user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=image_link)

    if not user_answer['error']:
        # решение капчи
        # print(user_answer['captchaSolve'])
        # print(user_answer['taskId'])
        return user_answer['captchaSolve']
    elif user_answer['error']:
        # Тело ошибки, если есть
        print(user_answer['errorBody']['text'])
        print(user_answer['errorBody']['id'])
        return None



def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """
    res = captcha_solve(captcha.get_url())

    if res == None:
        print("Captcha solve error. Please, write manually")
        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    else:
        print("Captcha solved. Key is: ",res)
        key = res

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)








#######################################################################################