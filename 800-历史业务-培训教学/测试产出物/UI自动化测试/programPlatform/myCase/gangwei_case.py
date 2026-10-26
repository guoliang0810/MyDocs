import unittest
from selenium import webdriver
from myPage.login_page import LoginPage
from myPage.gangwei_page import gangweipage
import time


class Bw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://sx.baway.tech:8060/'
        cls.driver = webdriver.Chrome()
        cls.lp = LoginPage(cls.driver, cls.url)
        cls.gw = gangweipage(cls.driver, cls.url)
        cls.lp.open_url()
        cls.driver.maximize_window()
        time.sleep(3)
        cls.lp.input_username('黄辉')
        cls.lp.input_password('123456')
        time.sleep(4)
        cls.lp.click_loginbutton()
        time.sleep(10)

    def setUp(self):
        print('开始测试==========')

    def tearDown(self):
        print('结束测试==========')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_gwchakan(self):
        time.sleep(10)
        self.gw.click_cha()
        time.sleep(5)

    def test_gwsousuo(self):
        time.sleep(5)
        self.driver.get('http://sx.baway.tech:8060/highPost')
        self.gw.gw_search('测试工程师')
        time.sleep(4)


if __name__ == '__main__':
    unittest.main()