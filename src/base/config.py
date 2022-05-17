# coding=utf-8
import configparser
import os

class Config:

    def __init__(self):
        _basedir = os.path.abspath(os.path.dirname(__file__))
        # pitop 配置文件
        sys_conf = os.path.join(_basedir, '../../sys.conf')
        cf = configparser.ConfigParser()
        cf.read(sys_conf)
        self.cf = cf

    def read(self, key, value):
        return str(self.cf.get(key, value))
