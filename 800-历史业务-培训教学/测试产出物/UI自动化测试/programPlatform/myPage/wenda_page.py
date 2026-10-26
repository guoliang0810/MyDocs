from selenium.webdriver.common.by import By
from myBase.base_page import base
import time


class gangweipage(base):
    def __init__(self,driver,url):
        base.__init__(self,driver,url)

    # 打开地址
    def open_url(self):
        self.get_url()