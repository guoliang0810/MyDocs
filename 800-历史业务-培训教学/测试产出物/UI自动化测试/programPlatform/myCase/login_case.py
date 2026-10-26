
from selenium import webdriver
import unittest
import HTMLTestRunner
from tools.test_log import aw_log
from myPage.login_page import LoginPage
import time


class LoginCase(unittest.TestCase):

    def setUp(self):
        self.url = 'http://sx.baway.tech:8060/'
        self.driver = webdriver.Chrome()
        self.lp = LoginPage(self.driver, self.url)
        self.lp.open_url()
        self.log = aw_log('login.log')
        self.log.get_log()
        self.log.logger.info('kaishiceshi ')

    def tearDown(self) -> None:
        self.log.get_log()
        self.log.logger.info('jieshuceshi ')
        self.driver.close()

    def test_login(self):
        time.sleep(3)
        self.lp.input_username('黄辉')
        self.lp.input_password('123456')
        time.sleep(4)
        self.lp.click_loginbutton()
        time.sleep(5)
        # username_text = self.lp.get_username_text()
        gw_text = self.driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div[1]/div[1]/div[1]/ul/li[1]').text
        print(gw_text)
        self.assertEqual(first='岗位', second=gw_text, msg='登录失败')
        time.sleep(2)


if __name__ == '__main__':
    unittest.main()
