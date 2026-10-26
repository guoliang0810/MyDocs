from selenium.webdriver.common.by import By
from myBase.base_page import base
import time
from selenium import webdriver


class LoginPage(base):
    def __init__(self, driver, url):
        base.__init__(self, driver, url)

    def open_url(self):
        self.get_url()

    # 输入用户名
    def input_username(self, username):
        self.input_text(username, *(By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input'))

    # 密码
    def input_password(self, password):
        self.input_text(password, *(By.XPATH, '//*[@id="app"]/div/form/div[2]/div/div/input'))

    # 登录按钮
    def click_loginbutton(self):
        self.left_click(*(By.XPATH, '//*[@id="app"]/div/form/div[5]/div/button'))

    # 获取登录后页面元素
    def get_username_text(self):
        return self.get_element_text((By.CLASS_NAME, 'name'))


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'http://sx.baway.tech:8060/'
    b = LoginPage(driver, url)
    b.open_url()
    time.sleep(5)
    b.input_username('黄辉')
    b.input_password('123456')
    time.sleep(5)
    b.click_loginbutton()
    time.sleep(5)
    driver.close()

