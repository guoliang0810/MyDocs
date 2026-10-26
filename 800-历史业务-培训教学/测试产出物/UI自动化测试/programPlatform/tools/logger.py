# encoding: utf-8
import logging
import datetime
import os


class AutoTestLog:
    def __init__(self):
        self.logger = logging.getLogger() # 创建一个logger
        self.logger.setLevel(logging.DEBUG) #指定日志级别
        # 以时间命名log文件名
        base_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件路径
        log_path = base_path + '/logs/' # log文件路径
        file_name = datetime.datetime.now().strftime("%y-%m-%d %H:%M") + '.log' #以时间命名文件名
        log_name = log_path + file_name # log文件名
        print(log_name)
        # 将日志写入磁盘
        self.file_handle = logging.FileHandler(log_name,'a',encoding='utf-8')
        self.file_handle.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        self.file_handle.setFormatter(file_formatter)
        # 给logger添加handler
        self.logger.addHandler(self.file_handle)
        ch = logging.StreamHandler()
        ch.setFormatter(file_formatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger

    # 关闭handle
    def close_handle(self):
        self.logger.removeHandler(self.file_handle)
        self.file_handle.close()

if __name__ == '__main__':
    l = AutoTestLog()
    l1 = l.get_log()
    l1.info('123')
