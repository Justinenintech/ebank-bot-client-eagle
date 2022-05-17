# coding=utf-8
import json

from src.base.enum.result_enum import ResultEnum
from src.base.enum.yn_enum import YNEnum


class LoginResult:
    """
    登录结果信息
    """

    def __init__(self, payee_card=None,
                 status=ResultEnum.Failed.value,
                 bank_trade_no=None,
                 balance=None,
                 base64ImageCaptcha=None,
                 showSecLoginCode=None,
                 errMsg=None):
        self.payeeCard = payee_card
        self.status = status
        self.bankTradeNo = bank_trade_no
        self.balance = balance
        self.errMsg = errMsg
        self.base64ImageCaptcha = base64ImageCaptcha
        self.showSecLoginCode = YNEnum.Yes.value if showSecLoginCode else YNEnum.NO.value
        self.isBase64Image = YNEnum.Yes.value if base64ImageCaptcha else YNEnum.NO.value
        print('self.showSecLoginCode',self.showSecLoginCode)

    def to_json(self):
        return json.dumps(self.__dict__)
