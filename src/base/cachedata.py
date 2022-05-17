# coding=utf-8
import json

"""
缓存数据对象
"""


class CacheData:
    def __init__(self, token=None, trade_no='x', account=None, password=None):
        # sn 码
        self.token = token
        self.trade_no = trade_no
        self.account = account
        self.password = password
        self.count_alipay = 0
        self.count_wechat_pay = 0
        self.md5_list = []
        self.cookies = []

    @property
    def get_token(self):
        return str(self.token)

    @get_token.setter
    def set_token(self, value):
        self.token = str(value)

    @property
    def get_trade_no(self):
        return str(self.trade_no)

    @get_trade_no.setter
    def set_trade_no(self, value):
        self.trade_no = str(value)

    @property
    def get_account(self):
        return str(self.account)

    @get_account.setter
    def set_account(self, value):
        self.account = str(value)

    @property
    def get_password(self):
        return str(self.password)

    @get_password.setter
    def set_password(self, value):
        self.password = str(value)

    def toJson(self):
        '''
        json序列化
        :return:json字符串
        '''
        return json.dumps(self.__dict__)

    def toObj(self, value):
        '''
        转化成beanret对象
        :param value:json字符串
        :return:BeanRet对象
        '''
        self.__dict__ = json.loads(value)
        return self
