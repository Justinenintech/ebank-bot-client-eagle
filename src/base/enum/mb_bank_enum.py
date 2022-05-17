# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : enum_mbbank.py
# Time       ：2022/3/3 8:55 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class MBElementEnum(Enum):
    """
    MB银行转账业务-页面元素定位枚举类
    """
    # MB银行OTP倒计时，两分钟
    MB_OTP_COUNTDOWN = 110
    # MB银行登录界面URL
    BANK_LOGIN_URL = "https://online.mbbank.com.vn/pl/login"
    # MB银行转账界面URL
    BANK_TRANSFER_URL = "https://online.mbbank.com.vn/transfer/inhouse"

    # MB银行编码
    MB_BANK = "MBbank"
    # 图形验证码
    CAPTCHA = ['css selector', '.ng-star-inserted:nth-child(1)']
    # 刷新验证码按鈕
    REFRESH_CAPTCHA = ['id', 'refresh-captcha']
    # 登录账号输入框
    USERNAME = ['id', 'user-id']
    # 登录密码输入框
    PASSWORD = ['id', 'new-password']
    # 验证码输入框
    VERIFY_CODE = ['css selector', '.pl-upper']
    # 登录按钮
    LOGIN = ['css selector', '.mat-button-wrapper']
    # 登录失败，弹出提示框的关闭按钮
    ERROR_BTN = ['css selector', '.btn-primary']

    # 出现错误弹窗，空白处
    ERROR_BTN_BACKDROP = ['css selector', '.cdk-overlay-backdrop']

    # otp错误，弹出框
    OTP_ERROR_BTN = ['xpath',
                     "//button[contains(.,'ĐỒNG Ý')]"]

    OTP_ERROR_TEXT = ['xpath',
                      "//span[contains(.,'Mã xác thực không chính xác. Bạn vui lòng thử lại!')]"]
    # 登录失败，密码错误- Mã lỗi: GW21  .fc-header
    ERROR_CODE = ['css selector', '.fc-header']
    # 登录成功判断
    LOGIN_SUCCESS = ['css selector', '.welcome-back']
    # 登录成功-首页余额
    BALANCE = ['css selector', '.gtt-2 > .balance']
    # Transfers主菜单
    TRANSFERS_MNU = ['id', 'MNU_GCME_050000']
    # Transfer money-转账页面
    TRANSFER_MONEY = ['css selector', '#MNU_GCME_050301 > .mat-tree-node > .ng-tns-c182-2']
    # 判断是否成功进入转账页面 'Chuyển tiền tới tài khoản ngân hàng
    TRANSFER_MONEY_TEXT = ['css selector', '.lbl-begin']
    # 用于判断的文本信息 assert
    ASSERT_IN_TRANSFER = 'Chuyển tiền tới tài khoản ngân hàng'

    ASSERT_PAYEE_PAYER = ['class name', 'multiline-select']

    # 下一步
    TRANSFER_MONEY_CONTINUE = ['css selector', '.btn-next .btn']
    # 打开银行选择下拉框
    TRANSFER_BANK_SELECT = ['xpath', '//*[@id="mat-select-3"]/div/div[1]/span']
    # 搜索要选择的银行
    TRANSFER_BANK_SEARCH = ['css selector', '.mat-select-search-inner > .mat-select-search-input']
    # 选中银行
    TRANSFER_BANK_SELECTED = ['xpath',
                              '/html/body/div[2]/div[2]/div/div/div/mat-option/span/div/span']
    # 收款人账号 （假设输入账号错误，账号无效 Mã lỗi: 201
    TRANSFER_RECEIVER_ACCOUNT = ['css selector', '.form-group:nth-child(3) .form-control']
    # 收款人姓名
    TRANSFER_RECEIVER_NAME = ['css selector', '.form-group:nth-child(4) .form-control']
    # 越南盾输入框
    TRANSFER_VND_AMOUNT = ['css selector', '.form-group:nth-child(5) .form-control']
    # 备注输入框
    TRANSFER_SUMMARY = ['css selector', '.form-group:nth-child(6) .form-control']
    # otp二维码
    OTP_QR_XPATH = ['css selector', '.aclass > img']
    # 發送otp 按鈕
    SEND_VERIFY_CODE_BTN = ['css selector', '#cdk-step-content-0-2 > div > div > button']

    # 确认收款款人信息
    RECEIVER_INFO_CONFIRM_BTN = ['xpath', '//*[@id="cdk-step-content-0-1"]/div/div/div/div/button']

    # otp输入框
    OTP_INPUT = ['name', 'otp']
    # 输入otp 之后点击确认按钮
    OTP_SUBMIT_BTN = ['css selector', '.dialog-action > .btn']

    # 转账成功保存截图的按钮
    # "assets/images/email.png"
    SUCCESS_ICON_XPATH = ['xpath',
                          '/html/body/app-root/div/ng-component/div[1]/div/div/div[1]/div/div/div/mbb-transfer-management/div/mbb-transfer-inhouse/div/div[2]/div/div/mat-vertical-stepper/div[4]/div/div/div/div/mbb-transfer-sucsess/div[1]/div[1]/img']
