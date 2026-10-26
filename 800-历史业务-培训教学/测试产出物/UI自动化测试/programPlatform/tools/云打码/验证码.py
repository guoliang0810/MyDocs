from PIL import Image
import pytesseract
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
d.save_screenshot(r'C:\Users\耿荣栓\PycharmProjects\untitled1\ceshi1708A\day6\云打码\1.png')
img = d.find_element_by_id('imgObj')

#对坐标进行处理：
location = img.location
size = img.size
print(location,size)
left = location['x']
right = location['y']
w = int(left) + int(size['width'])
h = int(right) + int(size['height'])
image = Image.open(r'C:\Users\dell\Desktop\untitled\pachong\ceshi1704A\day14\1.png')
img1 = image.crop((left*1.5,right*1.5,w*1.5,h*1.5))
img1.save('new.png')
time.sleep(5)

text = pytesseract.image_to_string(Image.open('new.png'))
print(text)
time.sleep(5)

result = ydm.get_image('new.png')
print('result',result)




























