from selenium.webdriver.common.by import By
from myBase.base_page import base
import time
from selenium import webdriver


class LoginPage(base):
    def __init__(self, driver, url):
        base.__init__(self, driver, url)

    def open_url(self):
        self.get_url()

    def click_xiangmu(self):
        self.left_click(*(By.XPATH, '//*[@id="app"]/div/section/div/div[1]/div[1]/div[1]/ul/li[2]'))

    def get_list_text(self):
        self.get_element_text(*(By.XPATH, '//*[@id="app"]/div/section/div/div[2]/div[1]/div/div/div[1]/div[1]/span'))
