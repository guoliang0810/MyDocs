
import unittest
import os
import HTMLTestRunner
import yagmail as yagmail


class RunCase(unittest.TestCase):
    def testcase01(self):
        case_path = os.getcwd()
        print(case_path)
        f = open('1.html', 'wb')
        #print(case_path)
        suite = unittest.defaultTestLoader.discover(case_path, 'bw*.py')
        #runner = unittest.TextTestRunner()
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='This is first report', description='aaa')
        runner.run(suite)

        # email1 = yagmail.SMTP(user='2205425010@qq.com', password='crcmlqloqgeodjje', host='smtp.qq.com', port=465)
        # email1.send(to='94582447@qq.com', subject='测试报告', contents=['注册,登录,修改密码', '1.html'])


if __name__ == '__main__':
    unittest.main()