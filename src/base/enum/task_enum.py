# coding=utf-8
from enum import Enum


class TaskEnum(Enum):
    """
    任务返回数据的属性
    """

    TASK_ID = 'id'
    ORDER_NO = 'orderNo'
    PAYEE_BANK_CARD = 'payeeBankCard'
    BANK_USER_NAME = 'payerUsername'
    BANK_LOGIN_PASSWORD = 'payerLoginPassword'
    PAYEE_ACCOUNT = 'payeeAccount'
    TYPE = 'type'
    AMOUNT = 'amount'
    BANK_CODE = 'bankCode'
    BANK_TYPE = 'bankType'
    App_Driver_Code = 'appDriverCode'
    OTP = 'otp'
    PAYEE_BANK_CODE = 'payeeBankCode'
    PAYEE_NAME = 'payee'
