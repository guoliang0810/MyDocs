import logging
#logging
#1.创建logging 日志器
#2.设置等级
#3.创建处理器（文件处理器 控制台处理器）
#4.设置等级
#5.创建格式器
#6.给处理器设置格式
#7.


class aw_log():
    def __init__(self, filename='test.log'):
        self.filename = filename
    def get_log(self):
        # 1.创建logging 日志器
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.fileHandler = logging.FileHandler(self.filename ,mode='a',encoding='utf-8')
        self.fileHandler.setLevel(logging.NOTSET)

        formatter = logging.Formatter('%(asctime)s -- %(funcName)s -- %(filename)s -- %(name)s -- %(message)s')
        self.fileHandler.setFormatter(formatter)
        self.logger.addHandler(self.fileHandler)
        # self.logger.debug('这是debug级别')

    def close(self):
        self.fileHandler.close()
        self.logger.removeHandler(self.fileHandler)


if __name__ == '__main__':
    lg = aw_log('1.log')
    lg.get_log()
    lg.logger.info('ceshi')
    lg.close()