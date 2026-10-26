from selenium.webdriver.common.by import By
from myBase.base_page import base
import time


class gangweipage(base):
    def __init__(self,driver,url):
        base.__init__(self,driver,url)

    # 打开地址
    def open_url(self):
        self.get_url()

    def click_gangwei(self):
        self.left_click(*(By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input'))

    # 岗位查看
    def click_cha(self):
        # self.find_elements(*(By.CLASS_NAME, 'el-tooltip operation_btn'))[0].click()
        self.left_click(*(By.XPATH, '//*[@id="app"]/div/section/div/div[2]/div/div[2]/div[2]/div/div[3]/table/tbody/tr[1]/td[7]/div/img'))

    # 岗位搜索
    def gw_search(self, text):
        self.input_text(text, *(By.XPATH, '//*[@id="app"]/div/section/div/div[2]/div/div[2]/div[1]/div/input'))

