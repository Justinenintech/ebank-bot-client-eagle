# coding=utf-8
"""
User 模型dao操作
"""
from src.base.databasetools import Sqlite3Tools


class TradeRecordDao:
    def __init__(self):
        self.__db = Sqlite3Tools()

    def load(self, md5):
        sql = "select * from trade_record where md5='" + str(md5) + "'"
        return self.__db.load(sql)

    def query(self):
        sql = 'select * from trade_record'
        results = self.__db.query(sql)
        list = []
        for row in results:
            list.append({'trade_no': row[0], 'md5': row[1], 'amount': row[2], 'remark': row[3], 'date_time': row[4]})
        return list

    def insert(self, trade_no, md5, amount, remark, date_time):
        sql = "insert into trade_record(trade_no, md5, amount,remark,date_time) " \
              "VALUES ('" + \
              str(trade_no) + "','" + \
              str(md5) + "','" + \
              str(amount) + "','" + \
              str(remark) + "','" + \
              str(date_time) + \
              "') "
        self.__db.insert(sql)


if __name__ == '__main__':
    tr = TradeRecordDao()
    tr.insert('1', '2', '123.00', 'hh', '2021/09')
