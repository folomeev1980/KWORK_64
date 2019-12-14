import datetime
import os


class Logger():
    def __init__(self, error):
        self.error = str(error)

        if "214. Access to adding post denied" in self.error:
            self.error = "214. Access to adding post denied: can only schedule 25 posts on a day."

        elif "14. Captcha needed" in self.error:
            self.error = "14. Captcha needed."

        elif "Access to adding post denied: cannot schedule more than 150 posts." in self.error:
            self.error="Access to adding post denied: cannot schedule more than 150 posts."

        else:
            pass

        with open('log.txt', "a") as file:
            print(self.error)
            file.write(str(datetime.datetime.now())[0:16] + "\t\t" + self.error + "\n")


class DirectoryManipulation():
    pass
