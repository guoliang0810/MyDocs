import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
wait = WebDriverWait(brower, 10)


def getLoginCookies():
    # get login taobao cookies
    url = "https://www.baidu.com/"
    brower.get("https://www.baidu.com/")
    while True:
        print("Please wait!")
        time.sleep(3)
        # if login in successfully, url  jump to www.taobao.com
        while brower.current_url ==  url:
            bwCookies  = brower.get_cookies()
            brower.quit()
            cookies = {}
            for item in bwCookies:
                cookies[item['name']] = item['value']
            outputPath = open('loginCookies.pickle', 'wb')
            pickle.dump(cookies, outputPath)
            outputPath.close()
            return cookies


def readLoginCookies():
    # if hava cookies file ,use it
    # if not , getTaobaoCookies()
    if os.path.exists('taobaoCookies.pickle'):
        readPath = open('taobaoCookies.pickle', 'rb')
        tbCookies = pickle.load(readPath)
    else:
        tbCookies = getLoginCookies()
    return tbCookies


if __name__ == '__main__':
    getLoginCookies()
    d = readLoginCookies()
    print(d)

