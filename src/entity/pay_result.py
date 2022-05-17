# coding=utf-8
import json

from src.base.enum.result_enum import ResultEnum


class PayResult:
    """
    支付结果类
    """

    def __init__(self, payer=None, status=ResultEnum.Failed.value, bank_trade_no=None, summary=None):
        self.payer = payer
        self.status = status
        self.bankTradeNo = bank_trade_no
        self.summary = summary

    def to_json(self):
        return json.dumps(self.__dict__)
