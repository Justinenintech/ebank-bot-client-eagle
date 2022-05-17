# coding=utf-8

"""
缓存数据工具
"""
import os


class CacheDataClient(object):
    def __init__(self):
        _basedir = os.path.abspath(os.path.dirname(__file__))
        cache_json = os.path.join(_basedir, 'cache.json')
        self.cachePath = cache_json

    def read(self):
        '''
        读取缓存
        :return:jsonData数据
        '''
        file = open(self.cachePath, 'r')
        jsonData = file.read()
        return jsonData

    def write(self, jsonData):
        '''
        写入缓存
        :param jsonData:json 格式数据
        '''
        file = open(self.cachePath, 'w')
        file.write(jsonData)
        file.flush()
