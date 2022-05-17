# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vib_bank_driver.py
# Time       ：2022/3/17 11:34 AM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""

from loguru import logger
from selenium.common.exceptions import TimeoutException

from src.base.BrowserBase import BrowserBase
from src.base.enum.vib_bank_enum import VIBElementEnum
from src.base.tool import Tool


class VIBBankDriver(BrowserBase):
    """
    VIBBankDriver驱动器
    """

    def __init__(self):
        BrowserBase.__init__(self)
        self.t = Tool()
        # 登录入口
        self.login_url = VIBElementEnum.BANK_LOGIN_URL.value

    def run(self):
        """
        运行银行驱动
        """
        try:
            # 打开银行
            logger.info("---打开银行---")
            self.open_bank()
        except Exception as e:
            logger.error(e)

    def open_bank(self):
        """
        打开浏览器，并访问网银登录地址
        :return:
        """
        self.open_url(self.login_url)

    def input_username(self, username: str):
        """
        输入登录账号
        :param username: str
        :return:
        """
        self.type(VIBElementEnum.USERNAME.value, username)

    def input_password(self, password: str):
        """
        输入登录密码
        :param password: str
        :return:
        """
        self.type(VIBElementEnum.PASSWORD.value, password)

    def click_login(self):
        """
        点击登录
        :return:
        """
        self.click(VIBElementEnum.LOGIN.value)

    def get_login_error_text(self):
        """
        获取登录错误提示信息
        :return: str _text or False
        """
        _true_or_false = self.check_get_text(VIBElementEnum.LOGIN_ERROR.value,
                                             VIBElementEnum.LOGIN_ERROR_TEXT.value)
        return _true_or_false
        # try:
        #     _text = self.get_text(VIBElementEnum.LOGIN_ERROR.value)
        #     if _text.__eq__(VIBElementEnum.LOGIN_ERROR_TEXT.value):
        #         return True
        # except TimeoutException:
        #     return False

    def get_balance(self) -> str:
        """
        获取登录网银账号的余额
        :return:
        """
        _text = self.get_text(VIBElementEnum.BALANCE.value)
        return _text

    def click_transfer_inter(self):
        """
        跨行转账页面，否则采用URL直接进入
        :return:
        """
        self.open_url(VIBElementEnum.BANK_TRANSFER_INTER.value)

    def click_transfer_peer(self):
        """
        本行转账页面，否则采用URL直接进入
        :return:
        """
        self.open_url(VIBElementEnum.BANK_TRANSFER_PEER.value)

    def input_bank(self, bank):
        """
        输入要选择的银行简称
        :param bank:
        :return:
        """
        self.type(VIBElementEnum.TRANSFER_INTER_BANK_NAME.value, bank)

    def click_select_transfer_bank(self, bank):
        """
        选择要转账的银行
        :return:
        """
        # 输入要选择的银行
        self.input_bank(bank)
        # 选中银行
        self.click(VIBElementEnum.TRANSFER_INTER_SELECTED.value)

    def click_transfer_fast(self):
        """
        选中转账类型：快速转账模式
        """
        #     def TRANSFER_INTER_SELECTED_FAST_TYPE
        self.click(VIBElementEnum.TRANSFER_INTER_SELECTED_FAST_TYPE.value)

    def input_transfer_account(self, account: str):
        """
        输入收款人账号
        :param account: 1668868688
        :return:
        """
        self.type(VIBElementEnum.TRANSFER_INTER_ACCOUNT.value, account)

    def click_blank_space(self):
        """
        点击转账页面空白处
        """
        self.move_to_element(VIBElementEnum.TRANSFER_INTER_MOUSE_SPACE.value)
        self.click(VIBElementEnum.TRANSFER_INTER_MOUSE_SPACE.value)

    def input_transfer_amount(self, amount: int):
        """
        输入转账金额
        :param amount: 10000
        :return:
        """
        self.type(VIBElementEnum.TRANSFER_INTER_AMOUNT.value, amount)

    def input_transfer_remark(self, remark: str):
        """
        输入转账备注
        :return:
        """
        self.type(VIBElementEnum.TRANSFER_INTER_REMARK.value, remark)

    def click_transfer_next(self):
        """
        点击下一步
        :return:
        """
        self.click(VIBElementEnum.TRANSFER_INTER_NEXT.value)

    def get_otp_push_text(self):
        """
        用于判断是否已成功进入OTP页面，便于前端接收通知后，再加载倒计时
        :return: bool
        """
        is_true = self.check_get_text(VIBElementEnum.TRANSFER_INTER_OTP_PUSH.value,
                                      VIBElementEnum.TRANSFER_INTER_OTP_PUSH_TEXT.value)
        return is_true
        # try:
        #     _text = self.get_text(VIBElementEnum.TRANSFER_INTER_OTP_PUSH.value)
        #     if _text.__eq__(VIBElementEnum.TRANSFER_INTER_OTP_PUSH_TEXT.value):
        #         logger.debug("判断是否成功进入OTP页面：{}",_text)
        #         return True
        # except TimeoutException:
        #     return False

    def click_login_out(self):
        """
        退出登录
        :return:
        """
        self.click(VIBElementEnum.LOGIN_PERSONAL_INFORMATION.value)
        self.click(VIBElementEnum.LOGIN_OUT.value)

    def get_transfer_success(self):
        """
        获取支付是否成功的文字信息，判断是否成功支付
        :return:messageOpenSuccess
        """
        _true_or_false = self.check_get_text(VIBElementEnum.TRANSFER_SUCCESS.value,
                                             VIBElementEnum.TRANSFER_SUCCESS_TEXT.value)
        return _true_or_false
        # try:
        #     self.forced_wait()
        #     _success = self.get_text(VIBElementEnum.TRANSFER_SUCCESS.value)
        #     if _success.__eq__(VIBElementEnum.TRANSFER_SUCCESS_TEXT.value):
        #         return True
        # except TimeoutException:
        #     return False

    def check_otp_error(self):
        """
        判断OTP是否错误
        :return:
        """
        _true_or_false = self.check_get_text(VIBElementEnum.TRANSFER_OTP_ERROR.value,
                                             VIBElementEnum.TRANSFER_OTP_ERROR_TEXT.value)
        return _true_or_false
        # try:
        #     self.forced_wait()
        #     is_displayed = self.get_displayed(VIBElementEnum.TRANSFER_OTP_ERROR.value)
        #     if is_displayed.__eq__(VIBElementEnum.TRANSFER_OTP_ERROR_TEXT.value):
        #         return True
        #     # return is_displayed
        # except TimeoutException:
        #     return False

    def input_transfer_otp(self, otp):
        """
        输入OTP码
        :param otp: 983453
        :return:
        """
        for index, value in enumerate(otp):
            _otp = VIBElementEnum.TRANSFER_INTER_OTP.value
            _otp[1] = _otp[1] + str(index + 1)
            self.click(_otp)
            self.type(_otp, value)
            _otp[1] = 'txtOtp'

    def login(self, username: str, password: str):
        """
        步骤1，登录MB网银
        :param username: 银行账号
        :param password: 银行密码
        :param code: 银行验证码
        :return:
        """
        # nonlocal count       # Python3中引入的新关键字
        # 输入银行账号
        self.input_username(username)
        # 输入银行密码
        self.input_password(password)
        # code = input('手动输入验证码：')
        self.forced_wait()
        # 点击登录
        self.click_login()

    def transfer(self, bank_type: str, bank: str, payee_account: str, balance: int, remark: str):
        """
        步骤3，录入转账基本信息，并核对
        :param bank_type: 转账类型，Inter跨行，Peer本行
        :param bank: 要选中的转账银行
        :param payee_account: 收款人银行卡
        :param balance: 转账金额
        :param remark: 转账备注
        :return:
        """
        # 进入转账界面
        if bank_type == 'Inter':
            self.click_transfer_inter()
        elif bank_type == 'Peer':
            self.click_transfer_peer()
        # 输入银行编码，并选中银行
        self.click_select_transfer_bank(bank)
        # 选中快速转账模式
        self.click_transfer_fast()
        # 输入收款人银行卡 '1668868688'
        self.input_transfer_account(payee_account)
        # 点击空白处
        self.click_blank_space()
        # 输入转账金额
        self.input_transfer_amount(balance)
        # 输入转账备注
        self.input_transfer_remark(remark)
        # 点击下一步，进入otp等待输入页面
        self.click_transfer_next()

    def input_submit_otp(self, otp):
        """
        步骤5，接收，并提交OTP码
        :param otp: OTP验证码
        :return:
        """
        # 输入OTP码：
        # self.forced_wait()
        self.input_transfer_otp(otp)
        self.forced_wait()
        # 最后一步，提交已输入的OTP
        self.click_transfer_next()
