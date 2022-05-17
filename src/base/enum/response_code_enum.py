# coding=utf-8
from enum import Enum


class ResponseCodeEnum(Enum):
    """
    成功
    """
    Success = "0000"

    """
    刷新验证码
    """
    Refresh_Captcha = "8000"
