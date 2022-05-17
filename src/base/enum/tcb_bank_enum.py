# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tcb_bank_enum.py
# Time       ：2022/3/19 6:23 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class TCBElementEnum(Enum):
    """
    TCB-越南国际商业股份银行-银行转账业务-页面元素定位枚举类（TCB OTP倒计时5分钟，余额不足，在下一步会提示"余额不足"）
    """
    # VIB银行OTP倒计时，5分钟
    TCB_OTP_COUNTDOWN = 270
    # TCB银行登录界面URL
    BANK_LOGIN_URL = "https://ib.techcombank.com.vn/servlet/BrowserServlet"
    # TCB银行跨行转账界面URL
    BANK_TRANSFER_INTER = "https://ib.vib.com.vn/vi-vn/canhan2020v2/chuyentien/ngoaivib.aspx"
    # TCB银行本行转账页面URL
    BANK_TRANSFER_PEER = "https://ib.vib.com.vn/vi-vn/canhan2020v2/chuyentien/trongvib.aspx"
    # TCB银行编码
    TCB_BANK = "TCB"
    # 登录账号输入框
    USERNAME = ['id', 'signOnName']
    # USERNAME = '//*[@id="signOnName"]'
    # 登录密码输入框
    PASSWORD = ['id', 'password']
    # PASSWORD = '//*[@id="password"]'
    # 登录按钮
    LOGIN = ['name', 'btn_login']
    # LOGIN = '//*[@id="qwfs_content"]/div[3]/input'
    # 登录失败，提示文本信息，元素定位
    ERROR_MSG = ['id', 'lgn_error']
    # 登录失败，提示文本信息-非提示框：Bạn nhập sai tên truy cập/mật khẩu
    LOGIN_ERROR_TEXT = "Bạn nhập sai tên truy cập/mật khẩu"
    #
    # 登录成功后，获取可用余额 //*[@id="r1_AcctBalance714734932600"]/td[4]
    # BALANCE = ['xpath', '//*[@id=\"r1_AcctBalance610015050800\"]/td[4]']
    # BALANCE = ['xpath', '//*[@id="r1_AcctBalance714734932600"]/td[4]']

    # Transfers 主菜单
    TRANSFERS_MNU = ['name', 'AI.QCK.FT']
    # 同行转账页面  Chuyển trong TCB  //a[@href='javascript:docommand('FT,AI.QCK.INT.INP.TCB I F3')']
    # TRANSFER_PEER = ['xpath', '//*[@id="qck_left_link"]/ul[2]/li/a']  //*[@id="qck_left_link"]/li/a/img //*[@id="qck_left_link"]/li/a/img
    # TRANSFER_PEER = ['xpath', "//a[@href='javascript:docommand('FT,AI.QCK.INT.INP.TCB I F3')']"]
    # TRANSFER_PEER = ['xpath', '//*[@id="qck_left_link"]/li/a']
    # TRANSFER_PEER = ['link text', ' Chuyển trong TCB ']
    # 跨行转账页面  Chuyển ngoài TCB
    # TRANSFER_INTER = ['xpath', '//*[@id="qck_left_link"]/li/a']
    TRANSFER_INTER = ['xpath', '/html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/div[3]/div[2]/div/ul[3]/li/a']

    # 同行转账页面-收款人账号 fieldName:CREDIT.ACCT.NO fieldName:ACCT.NO.OTH
    TRANSFER_PEER_ACCOUNT = ['id', 'fieldName:CREDIT.ACCT.NO']
    # 点击姓名空白处
    TRANSFER_PEER_BLACK_SPACE = ['xpath', '//*[@id="tab1"]/tbody/tr[8]/td[4]']
    # 同行转账页面-用户名
    TRANSFER_PEER_PAYEE_NAME = ['id', 'fieldName:TAR.ACCT.NAME']
    # 同行/跨行-转账页面-转账金额
    TRANSFER_AMOUNT = ['id', 'fieldName:DEBIT.AMOUNT']
    # menu
    TRANSFER_MENU_LIST = ['id', 'qck_left_link']
    # 同行/跨行-转账页面-备注
    TRANSFER_REMARK = ['id', 'fieldName:PAY.DETAILS']
    # 余额不足，元素定位
    TRANSFER_INSUFFICIENT_BALANCE = ['class name', 'captionError']
    # 余额不足，文本信息
    TRANSFER_INSUFFICIENT_BALANCE_TEXT = "không đủ số dư để thực hiện giao dịch"
    # 跨行转账-银行名称非法文本信息 illegal bank
    TRANSFER_INTER_ILLEGAL_BANK = "không hợp lệ."
    # 同行\跨行-转账页面，下一步，进入确认转账页面 #
    TRANSFER_NEXT = ['xpath', '//*[@id="goButton"]/tbody/tr/td/table/tbody/tr/td[1]/a']
    # 同行转账页面，确认转账页面，提交按钮，进入获取OTP页面
    TRANSFER_CONFIRM = ['xpath', '//*[@id="contract_screen_div"]/table[3]/tbody/tr/td[2]/a']
    # 同行转账页面，获取OTP二维码
    TRANSFER_OTP_IMG = ['xpath', '//*[@id="qrcode"]/img']
    # 同行转账页面，OTP二维码输入框
    TRANSFER_OTP_INPUT = ['id', 'tokenCode']
    # 同行转账页面，OTP提交按钮
    TRANSFER_OTP_CONFIRM = ['xpath', '//*[@id="qwfs_content"]/div[3]/a[1]']
    # 同行转账页面，OTP错误，文本信息 元素定位：ERROR_MSG
    TRANSFER_OTP_ERROR_TEXT = "Bạn nhập sai Smart OTP"
    # 跨行转账页面，选择银行,需要点击空白处，或者点击账号编辑框
    TRANSFER_INTER_SELECT_BANK = ['id', 'preHTNGANHANG']
    # 跨行转账页面，账号
    TRANSFER_INTER_ACCOUNT = ['id', 'fieldName:PAYMENT.DETAILS:1']
    # 跨行转账页面，姓名
    TRANSFER_INTER_NAME = ['id', 'fieldName:AGENCY.CODE:1']
    # 判断转账是否成功的元素
    TRANSFER_SUCCESS = ['id', 'qwfs_title']
    # 判断转账是否成功的文本
    TRANSFER_SUCCESS_TEXT = "Giao dịch thành công."
    # 退出网银登录
    LOGIN_OUT = ['xpath', '//*[@id="qw_bc_ul_menu"]/li[3]/a']
