# encoding: utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText

# #设置账号：
# fs = "gengronglin_work@163.com"
# js = "gengronglin_work@163.com"
# sqm = '1064768802grl'
#
# #构建邮件：
# path = '/Users/p/venv/bin/untitled/day11/Report_EN.html'
# f = open(path,encoding='utf-8')
# msg = MIMEText(f.read(),'html','utf-8')
# msg['subject'] = Header('主题内容','utf-8')
# msg['from'] = Header(fs,'utf-8')
# msg['to'] = Header(js)
#
# #实现邮件发送的四个步骤：
# s = smtplib.SMTP_SSL('smtp.163.com',465)
# #授权登录：
# s.login(fs,sqm)
# #发送
# s.sendmail(fs,[js,],msg.as_string())

class SendMail():
    def __init__(self,fs,js,sqm,host):
        self.fs = fs
        self.js = js
        self.sqm = sqm
        self.host = host
    #主题，path
    def send_html(self,subject,path):
        f = open(path,encoding='utf-8')
        msg = MIMEText(f.read(),'html','utf-8')
        msg['subject'] = Header(subject,'utf-8')
        msg['from'] = Header(self.fs,'utf-8')
        msg['to'] = Header(self.js)
        self.login(msg)
    #抽出公用方法：
    def login(self,msg):
        s = smtplib.SMTP_SSL(self.host,465)
        s.login(self.js,self.sqm)
        s.sendmail(self.fs,[self.js,],msg.as_string())
        s.quit()
if __name__ == '__main__':
    mail = SendMail("gengronglin_work@163.com","gengronglin_work@163.com",'1064768802grl','smtp.163.com')
    mail.send_html('周考',r'/Users/p/venv/bin/untitled/day11/Report_EN.html')
















