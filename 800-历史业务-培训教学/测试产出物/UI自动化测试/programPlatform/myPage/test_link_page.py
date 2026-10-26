# encoding: utf-8
from selenium.webdriver.common.by import By
from myBase.base_page import base
import time
class commit(base):
    def __init__(self,driver,url):
        base.__init__(self,driver,url)

    def open_url(self):
        self.get_url()

    def input_nickname(self):
        self.input_text('郭老师',(By.XPATH,'//*[@id="app"]/div/form/div[1]/div/div[1]/input'))
        time.sleep(3)

    def input_password(self):
        self.input_text('123456',(By.XPATH,'//*[@id="app"]/div/form/div[2]/div/div/input'))
        time.sleep(20)

    def click_teacher(self):
        self.left_click((By.XPATH,'//*[@id="app"]/div/form/div[4]/div/div/label[2]'))
        time.sleep(1)

    def click_login_button(self):
        self.left_click((By.CLASS_NAME,'el-button--primar'))
        time.sleep(2)

    def choose_xueyuan(self):
        self.left_click((By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]'))
        time.sleep(1)

    def create_position(self):
        self.left_click((By.CLASS_NAME,'el-icon-plus'))
        time.sleep(1)

    def positioin_name(self):
        self.input_text('软件测试工程师',By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/form/div/div[1]/div/div/div/input')
        time.sleep(1)

    def click_zhuanye(self):
        self.left_click(By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/form/div/div[2]/div/div/div/div/input')
        time.sleep(1)
        self.left_click(By.XPATH,'/html/body/div[5]/div[1]/div[1]/ul/li[8]')
        time.sleep(1)

    def write_des(self):
        self.input_text('看到即使分开的三舅弗兰克觉得舒服反倒是',(By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/textarea'))
        time.sleep(2)

    def write_renwu(self):
        self.input_text('看到就分开的三舅分李松打开芳姐的奋斗奋斗奋斗',(By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/textarea'))
        time.sleep(2)

    def click_commit(self):
        self.left_click((By.XPATH,'//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div[2]/button[2]'))
        time.sleep(10)