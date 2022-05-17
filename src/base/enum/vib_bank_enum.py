# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vib_bank_enum.py
# Time       ：2022/3/16 2:33 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class VIBElementEnum(Enum):
    """
    VIB-越南国际商业股份银行-银行转账业务-页面元素定位枚举类
    """
    # VIB银行OTP倒计时，两分钟
    VIB_OTP_COUNTDOWN = 110
    # VIB银行登录界面URL
    BANK_LOGIN_URL = "https://ib.vib.com.vn/vi-vn/login2020.aspx"
    # VIB银行跨行转账界面URL
    BANK_TRANSFER_INTER = "https://ib.vib.com.vn/vi-vn/canhan2020v2/chuyentien/ngoaivib.aspx"
    # VIB银行本行转账页面URL
    BANK_TRANSFER_PEER = "https://ib.vib.com.vn/vi-vn/canhan2020v2/chuyentien/trongvib.aspx"
    # VIB银行编码
    VIB_BANK = "VIB"
    # 登录账号输入框
    USERNAME = ['id', 'Username']
    # 登录密码输入框
    PASSWORD = ['id', 'Password']
    # 登录按钮
    LOGIN = ['id', 'buttonLogin']
    # 登录失败，提示信息-非提示框：'Tên đăng nhập/mật khẩu không chính xác, bạn vui lòng nhập lại
    LOGIN_ERROR = ['css selector', '.error']
    # 登录失败，用于判断的文本信息
    LOGIN_ERROR_TEXT = "Tên đăng nhập/mật khẩu không chính xác, bạn vui lòng nhập lại."
    # 登录成功后，获取可用余额
    BALANCE = ['css selector', '.blue:nth-child(2)']

    # Transfers 主菜单
    TRANSFERS_MNU = ['css selector', 'li:nth-child(2) .tooltip']
    # 跨行转账页面
    TRANSFER_INTER = ['css selector', 'li:nth-child(3) td:nth-child(2)']

    # 转账记录页面-下一步
    TRANSFER_RECORD_NEXT = ['id', 'main-btn-transfer']
    # 转账记录页面-搜索框
    TRANSFER_RECORD_SEARCH_ACCOUNT = ['id', 'txtSearch']
    # 转账记录页面-列表框-账号
    TRANSFER_RECORD_TABLE_ACCOUNT = ['css selector', '.td-inner-conts > .blue']
    # 转账记录页面-未勾选-提示框-按钮
    TRANSFER_RECORD_NEXT_ERR_BTN = ['css selector', '#errorMessageModal .btn']
    # 转账记录页面-未勾选-提示框-提示信息：Vui lòng chọn tài khoản
    TRANSFER_RECORD_NEXT_ERR_TEXT = ['id', 'errorMessageModalMesage']

    # 跨行转账页面-选中银行输入框
    TRANSFER_INTER_BANK_NAME = ['id', 'receivedBank']
    # 跨行转账页面-选中银行
    TRANSFER_INTER_SELECTED = ['css selector', '.dropdown-item']
    # 跨行转账页面-是否勾选快速汇款 id=rbFast
    TRANSFER_INTER_SELECTED_FAST_TYPE = ['id', 'rbFast']
    # 跨行转账页面-收款人账号
    TRANSFER_INTER_ACCOUNT = ['id', 'txtAcctNo']
    # 跨行转账页面-移动空白处
    TRANSFER_INTER_MOUSE_SPACE = ['css selector', '.btn-footer']
    # 跨行转账页面-点击空白处
    TRANSFER_INTER_BLANK_SPACE = ['css', 'html']
    # 跨行转账页面-备注
    TRANSFER_INTER_REMARK = ['id', 'txtDescription']
    # 跨行转账页面-转账金额
    TRANSFER_INTER_AMOUNT = ['id', 'txtAmount']
    # 跨行转账页面-下一步
    TRANSFER_INTER_NEXT = ['id', 'btnNext']
    # 跨行转账页面-是否进入OTP页面，元素定位，用于OTP接口推送
    TRANSFER_INTER_OTP_PUSH = ['css selector', '.uppercase:nth-child(1)']
    # 跨行转账页面-是否进入OTP页面，判断文本信息是否正确，用于OTP接口推送
    TRANSFER_INTER_OTP_PUSH_TEXT = "XÁC NHẬN THÔNG TIN"
    # 跨行转账页面-输入otp
    TRANSFER_INTER_OTP = ['id', 'txtOtp']
    # 跨行转账页面-OTP错误
    TRANSFER_OTP_ERROR = ['id', 'lblOTPError']
    # 跨行转账页面-OTP错误文本
    TRANSFER_OTP_ERROR_TEXT = "Mã OTP không chính xác, bạn vui lòng nhập lại"
    # 判断转账是否成功的元素
    TRANSFER_SUCCESS = ['id', 'messageOpenSuccess']
    # 判断转账是否成功的文本
    TRANSFER_SUCCESS_TEXT = "GIAO DỊCH THÀNH CÔNG"
    # 右上角个人信息
    LOGIN_PERSONAL_INFORMATION = ['css selector', '.dropdown-toggle > img']
    # 退出网银登录
    LOGIN_OUT = ['css selector', '.li-logout > a']
