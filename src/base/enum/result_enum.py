# coding=utf-8
from enum import Enum


class ResultEnum(Enum):
    """
    成功
    """
    Success = "Success"

    """
    失败
    """
    Failed = "Failure"

    """
    OTP输入错误，最多允许重试1次
    """
    OTP_ERROR = "Otp_error"

    """
    OTP最终错误
    """
    FAILED_OTP = "Failure_otp"