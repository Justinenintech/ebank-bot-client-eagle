# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bidv_bank_enum.py
# Time       ：2022/3/25 10:34 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class BIDVElementEnum(Enum):
    """
    BIDV银行转账业务-页面元素定位枚举类
    """
    # BIDV银行OTP倒计时，两分钟
    BIDV_OTP_COUNTDOWN = 110
    BIDV_QRCODE_COUNTDOWN = 120
    # BIDV银行登录界面URL
    BANK_LOGIN_URL = "https://smartbanking.bidv.com.vn/dang-nhap"
    # BIDV银行跨行转账界面URL
    TRANSFER_INTER_URL = "https://smartbanking.bidv.com.vn/chuyen-tien/ngoai-bidv"
    # BIDV银行同行转账界面URL
    TRANSFER_PEER_URL = "https://smartbanking.bidv.com.vn/chuyen-tien/noi-bo"

    # BIDV银行编码
    BIDV_BANK = "BIDVbank"
    # 登录账号输入框
    USERNAME = ['xpath', "//input[@type='text']"]
    # 登录密码输入框
    PASSWORD = ['id', 'app_password_matKhau']
    # 验证码输入框
    VERIFY_CODE = ['css selector', '.input-ic-right']
    # 登录按钮
    SUBMIT_BTN = ['css selector', '.ubtn-text']
    # 获取图形验证码，需要截图保存验证码
    # CAPTCHA = ['css selector', '.login-captcha > img']
    CAPTCHA = ['class name', 'login-captcha']
    # 刷新验证码按鈕
    REFRESH_CAPTCHA = ['css selector', '.ubtn-sm > .ic-lg']
    # 操作失败，弹出提示框的确认按钮
    ERROR_BTN = ['css selector', '.col-12 > .ubtn']

    # 错误提示信息元素定位
    # ERROR_MSG = ['css selector', '.modal-body']
    ERROR_MSG = ['class name', 'modal-body']
    # 验证码错误
    ERROR_CAPTCHA = 'Mã kiểm tra không chính xác hoặc đã hết hiệu lực.'
    # otp错误文本信息
    ERROR_OTP = "Mã xác nhận OTP không đúng. Quý khách vui lòng kiểm tra lại."
    # 验证码失效文本信息
    ERROR_CAPTCHA_TIME_OUT = 'Mã xác nhận đã hết thời gian hiệu lực 2 phút. Quý khách vui lòng nhấn "Nhận lại mã" hoặc thực hiện đăng nhập lại ứng dụng.'
    # 登录信息不正确，5次或以上，服务将被锁定
    ERROR_USERNAME_PASSWORD = 'Thông tin đăng nhập không chính xác. Quý khách lưu ý: Dịch vụ SmartBanking sẽ bị khóa nếu Quý khách nhập sai mật khẩu 5 lần trở lên.'
    # Quý khách đã nhận quá số mã xác nhận OTP kích hoạt ứng dụng trong ngày (30 lần).
    ERROR_OTP_EXCEEDED_LIMIT = "Quý khách đã nhận quá số mã xác nhận OTP kích hoạt ứng dụng trong ngày (30 lần)."
    # 用于判断是否进入OTP-元素定位
    LOGIN_OTP_CHECK = ['css selector', '.p']
    # 用于判断是否进入OTP-文本信息
    LOGIN_OTP_CHECK_TEXT = "Không nhận được mã xác nhận? Gửi Lại"
    # 登录，OTP输入框 OTP长度：6位
    LOGIN_OTP_INPUT = ['css selector', '.input']

    # 登录后，取消参与疫情活动
    # CANCEL = ['css selector', '#app_modal_831708431.ubg-light-blue']
    CANCEL = ['xpath', "//button[contains(.,'Hủy')]"]

    # 默认为隐藏余额，显示按钮
    BALANCE_SHOW = ['css selector', '.eye2']

    # 登录成功-首页获取余额
    BALANCE = ['css selector', '.row-5 > .col-auto:nth-child(1)']

    # 进入收款人编辑页面
    TRANSFER_INTER_PROFILE = ['css selector', '.col-auto:nth-child(2) > .profile__img-2']

    # 银行选择下拉框
    TRANSFER_INTER_SELECT_BANK = ['class name', 'select2-selection.select2-selection--single']

    # 收款人银行简称 如：MB
    TRANSFER_INTER_SEARCH_BANK = ['css selector', '.select2-search__field']
    # 选中银行
    TRANSFER_INTER_SELECTED_BANK = ['xpath', "//ul[@class='select2-results__options']/li"]

    # 收款人银行账号
    TRANSFER_INTER_ACCOUNT = ['css selector', '.input-flex']

    # 收款人银行信息编辑页面，确认按钮 classname     # 输入银行信息，确认按钮 ubtn-text
    TRANSFER_INTER_PROFILE_CONFIRM = ['css selector', '.accountToChange']

    # 跨行收款金额
    TRANSFER_INTER_AMOUNT = ['xpath', '//app-money-input/input']

    # 备注
    TRANSFER_INTER_REMARK = ['css selector', '.textarea-autosize']

    # 跨行-转账
    TRANSFER_INTER_CONFIRM = ['xpath', "//span[contains(.,'Tiếp tục')]"]
    # 推送OTP二维码
    TRANSFER_INTER_OTP_IMG = ['css selector', '.qrcode > img']

    # 转账成功，文字判断 Giao dịch thành công
    TRANSFER_SUCCESS = ['css selector', '.box-title']
    TRANSFER_SUCCESS_TEXT = "Giao dịch thành công"

    # 判断交易失败 css=.b > .color-primary
    TRANSFER_FAILED = ['css selector', '.b > .color-primary']
