from selenium import webdriver
import time
import tools.云打码.YDMHTTP as ydm

d = webdriver.Chrome()
d.implicitly_wait(10)
d.get('http://172.16.10.111/exam/login.do')
d.find_element_by_name('username').clear()
d.find_element_by_name('username').send_keys('19426100129')
d.find_element_by_name('password').clear()
d.find_element_by_name('password').send_keys('1223344')
time.sleep(2)
#截取图片：
img = d.find_element_by_id('imgObj')
ydm.get_pic(d,img,r'C:\Users\dell\Desktop\untitled\pachong\ceshi1704A\day14\1.png',r'new.png')

result = ydm.get_image('new.png')
time.sleep(20)
a = input('请输入验证码')




























