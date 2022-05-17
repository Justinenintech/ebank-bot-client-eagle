# coding=utf-8
import os
import sqlite3


class Sqlite3Tools:
    def __init__(self):
        """
        链接数据库
        :param dbPath: 数据库文件路径
        """
        _basedir = os.path.abspath(os.path.dirname(__file__))
        db = os.path.join(_basedir, '../data.db')
        self.dbPath = db

    def getConn(self):
        """
        获得链接
        :return:
        """
        return sqlite3.connect(self.dbPath)

    def insert(self, sql):
        """
        保存数据
        :param sql:
        :return:
        """
        conn = self.getConn()
        conn.execute(sql)
        conn.commit()
        conn.close()

    def delete(self, sql):
        """
        删除数据
        :param sql:
        :return:
        """
        conn = self.getConn()
        conn.execute(sql)
        conn.commit()
        conn.close()

    def update(self, sql):
        """
        修改数据
        :param sql:
        :return:
        """
        conn = self.getConn()
        conn.execute(sql)
        conn.commit()
        conn.close()

    def load(self, sql):
        """
        查询指定一条数据
        :param sql:
        :return:
        """
        conn = self.getConn()
        cursor = conn.cursor()
        results = cursor.execute(sql)
        obj = None
        for result in results:
            obj = result
        conn.close()
        return obj

    def query(self, sql):
        """
        查询集合
        :param sql:
        :return:
        """
        conn = self.getConn()
        cursor = conn.cursor()
        results = cursor.execute(sql)
        return results
