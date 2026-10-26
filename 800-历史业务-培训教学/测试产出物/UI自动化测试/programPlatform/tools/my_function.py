import xlrd
import json
import yaml
import time
import yagmail
import HTMLTestReportEN
import os
#获取表格数据
def get_login_data(path):
    table = xlrd.open_workbook(path).sheet_by_name('Sheet1')
    lines = table.nrows
    clo = table.ncols
    big = []
    for line in range(lines):
        little = []
        for c in range(clo):
            value = table.cell_value(line,c)
            if type(value) == float:
                value = str(int(value))
            little.append(value)
        big.append(little)
    print(big)
    return big

def get_json_data(path):
    #str:  json
    data = open(path,'r').read()
    # json -> python
    pyobj = json.loads(data)
    print(pyobj)
    return pyobj['data']

def get_yaml_data():
    f = open('/Users/p/venv/bin/专高6/day8/configs/appconfig.yaml','r')
    data = yaml.load(f)
    return data

def get_time():
    tmp = str(int(time.time()))
    print(tmp)
    return tmp

def save_image(path,driver):
    my_path = path + get_time() + '.png'
    driver.save_screenshot(my_path)

def send_mail(path):
    mail = yagmail.SMTP(user='gengronglin_work@163.com',password='1064768802grl',host = 'smtp.163.com')
    mail.send(to=['gengronglin_work@163.com',],subject='testreport',attachments=[path,])

def make_reporter(path,suite):
    f = open(path,'wb+')
    runner = HTMLTestReportCN.HTMLTestRunner(stream=f,title='一家民宿',description='首页',tester='baijiacheng')
    runner.run(suite)
    f.close()





