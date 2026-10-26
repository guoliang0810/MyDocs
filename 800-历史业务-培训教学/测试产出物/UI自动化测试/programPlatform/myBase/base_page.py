# encoding: utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.logger import AutoTestLog
import time


class base():
    def __init__(self, driver, url):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.base_url = url

    # 1、进入
    def get_url(self):
        self.driver.get(self.base_url)

    # 2、找元素
    def find_element(self, *locator):
        print(locator)
        #print(*locator)
        return self.driver.find_element(*locator)

    # 3、点击
    def left_click(self, *locator):
        print(locator)
        #print(*locator)
        #调用自己的元素查找
        a = self.find_element(*locator)
        ActionChains(self.driver).click(a).perform()

    # 一组元素的获取：
    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    # 鼠标悬浮：
    def move_to_element(self, *locator):
        a = self.find_element(*locator)
        ActionChains(self.driver).move_to_element(a).perform()

    # 4、清除
    def clear_text(self, *locator):
       self.find_element(*locator).clear()

    # 5、输入值
    def input_text(self,text, *locator):
        input = self.find_element(*locator)
        input.send_keys(text)

    def find_element_by_webdriverWait(self, locator):
        element = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((locator[0],locator[1])))
        return element

    # 滚动到某个视图：
    def scroll_to_view(self,*locator):
        a = self.find_element(*locator)
        jsstr = 'arguments[0].scrollIntoView()'
        self.driver.execute_script(jsstr,a)

    # 窗口切换：
    def swtch_to_window(self,number):
        wins = self.driver.window_handles
        self.driver.switch_to.window(wins[number])

    # 验证信息：
    def get_attribuit_value(self, name, *locator):
        return self.find_element(*locator).get_attribute(name)

    def get_utl_text(self):
        return self.driver.current_url

    def get_current_title(self):
        return self.driver.title

    def get_element_text(self,*locator):
        return self.find_element(*locator).text

    # 二次定位
    def find_element_agin(self,towlocator, *locator, ):
        a = self.find_element(*locator)
        b = a.find_element(towlocator)
        return b


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'http://sx.baway.tech:8060'
    # driver.get(url)
    b = base(driver, url)
    b.get_url()
    time.sleep(5)
    #logc = (By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input')
    # driver.find_element(*logc).send_keys('huanghui')
    b.input_text('huanghui', *(By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input'))
    time.sleep(3)
    driver.close()





