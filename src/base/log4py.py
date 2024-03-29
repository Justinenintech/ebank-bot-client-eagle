# coding=utf-8
import logging
import logging.handlers
import sys

# 默认的配置DEBUG
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from setttings import SENTRY_DSN

LOG_LEVEL = logging.INFO  # 默认等级
LOG_FMT = '%(asctime)s - %(levelname)s: %(message)s'
# LOG_FMT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# 默认的时间格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
# 默认日志文件名称
LOG_FILENAME = 'log.log'
# sentry 開啟
if SENTRY_DSN:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.INFO
    )
    sentry_sdk.init(SENTRY_DSN,
                    traces_sample_rate=1.0,
                    integrations=[sentry_logging])


class Logger(object):
    def __init__(self):
        # 1. 获取一个logger对象
        self._logger = logging.getLogger()
        # 2. 设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        # 3. 设置日志输出
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        self._logger.addHandler(self._get_console_handler())
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''返回一个文件日志handler'''
        # 1. 获取一个文件日志handler
        filehandler = logging.handlers.TimedRotatingFileHandler(filename=filename, encoding="utf8", when='D',
                                                                interval=1, backupCount=3)
        # 2. 设置日志格式
        filehandler.setFormatter(self.formatter)
        # 3. 返回
        return filehandler

    def _get_console_handler(self):
        '''返回一个输出到终端日志handler'''
        # 1. 获取一个输出到终端日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 2. 设置日志格式
        console_handler.setFormatter(self.formatter)
        # 3. 返回handler
        return console_handler

    @property
    def logger(self):
        return self._logger


logger = Logger().logger

if __name__ == '__main__':
    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")
