# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : unit.py
# Time       ：2022/3/9 7:32 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import sqlite3
import os

class SimpleTool(object):
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    def __init__(self, filename="data"):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        PROJECT_ABSOLUTE_PATH = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.file_path = PROJECT_ABSOLUTE_PATH + '/' + filename + ".db"
        # (self.file_path)
        self.db = sqlite3.connect(self.file_path)
        self.c = self.db.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()
