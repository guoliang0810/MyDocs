
import unittest
import os
import HTMLTestRunner
import yagmail as yagmail


class RunCase(unittest.TestCase):
    def testcase01(self):
        case_path = os.getcwd()
        print(case_path)
        f = open('report.html', 'wb')
        #print(case_path)
        suite = unittest.defaultTestLoader.discover(case_path, '*case.py')
        #runner = unittest.TextTestRunner()
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='八维生产实训平台测试报告', description='aaa')
        runner.run(suite)

        # email1 = yagmail.SMTP(user='2205425010@qq.com', password='crcmlqloqgeodjje', host='smtp.qq.com', port=465)
        # email1.send(to='94582447@qq.com', subject='测试报告', contents=['注册,登录,修改密码', '1.html'])


if __name__ == '__main__':
    unittest.main()