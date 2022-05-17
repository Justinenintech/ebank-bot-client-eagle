# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb_bank_app.py
# Time       ：2022/3/17 2:26 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from loguru import logger
from selenium.common.exceptions import TimeoutException

from setttings import MB_ASSERT_PAY_ONE, MB_ASSERT_PAY_TWO
from src.base.BrowserBase import BrowserBase
from src.base.enum.mb_bank_enum import MBElementEnum
from src.base.enum.result_enum import ResultEnum
from src.base.tool import Tool

from src.entity.login_result import LoginResult


class MBBankDriver(BrowserBase):
    """
    mbBank驱动器
    """

    def __init__(self):
        BrowserBase.__init__(self)
        # 工具类
        self.t = Tool()
        # 登录入口
        self.login_url = MBElementEnum.BANK_LOGIN_URL.value
        # 转账页面
        self.transfer_page_url = MBElementEnum.BANK_TRANSFER_URL.value

    def run(self) -> str:
        """
        运行银行驱动
        """
        try:
            # 打开银行
            logger.info("---打开银行---")
            self.open_bank()

            # 登录银行
            logger.info("---读取验证码---")
            base64_img = self.get_captcha_base64()
            return base64_img
        except Exception as e:
            logger.error(e)
            return None

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
        self.type(MBElementEnum.USERNAME.value, username)

    def input_password(self, password: str):
        """
        输入登录密码
        :param password: str
        :return:
        """
        self.type(MBElementEnum.PASSWORD.value, password)

    def input_captcha_code(self, code):
        """
        输入验证码
        :param code:
        :return:
        """
        self.type(MBElementEnum.VERIFY_CODE.value, code)

    def get_captcha_base64(self) -> str:
        """
        获取登录图形验证码，base64
        :return: str
        """
        base64_img = self.get_attribute(MBElementEnum.CAPTCHA.value, 'src')
        return base64_img

    def get_transfer_success_img(self):
        """
        校验支付成功的图片，来判断是否成功支付
        :return:
        """
        try:
            self.forced_wait()
            img_url = self.get_attribute(MBElementEnum.SUCCESS_ICON_XPATH.value, 'src')
            is_img = self.t.compare_images(MB_ASSERT_PAY_ONE, MB_ASSERT_PAY_TWO, img_url)
            return is_img
        except TimeoutException:
            return False

    def refresh_captcha_code(self):
        """
        刷新验证码按钮
        :return:
        """
        self.click(MBElementEnum.REFRESH_CAPTCHA.value)

    def click_login(self):
        """
        点击登录
        :return:
        """
        self.click(MBElementEnum.LOGIN.value)

    def click_error_btn(self):
        """
        登录失败，弹出提示框确定按钮
        :return:
        """
        # self.forced_wait()
        self.click(MBElementEnum.ERROR_BTN.value)

    def check_error_pop(self):
        """
        检查错误弹窗是否出现
        :return:
        """
        try:
            self.forced_wait()
            is_enabled = self.get_enabled(MBElementEnum.ERROR_BTN.value)
            return is_enabled
        except TimeoutException:
            return False

    def get_error_code(self) -> str:
        """
        获取弹出提示框 错误编码 Mã lỗi: GW21
        :return: str _text
        """
        _text = self.get_text(MBElementEnum.ERROR_CODE.value)
        return _text

    def get_captcha_error_text(self) -> str:
        """
        获取验证码错误，弹出提示框 信息编号  Mã lỗi: GW283
        :return: str _text
        """
        _text = self.get_text(MBElementEnum.CAPTCHA_ERROR_TEXT.value)
        return _text

    def get_login_success_text(self) -> str:
        """
        获取登录成功后，银行首页的欢迎信息 welcome-back
        :return:
        """
        _text = self.get_text(MBElementEnum.LOGIN_SUCCESS.value)
        return _text

    def get_balance(self) -> str:
        """
        获取登录网银账号的余额
        :return:
        """
        self.forced_wait()
        _text = self.get_text(MBElementEnum.BALANCE.value)
        return _text

    def click_transfer_money(self):
        """
        通过左侧菜单进入转账页面，否则采用URL直接进入
        :return:
        """
        self.open_url(MBElementEnum.BANK_TRANSFER_URL.value)

    def click_transfer_continue(self):
        """
        进入转账页面之后，点击继续，进入转账信息录入页面
        :return:
        """
        self.forced_wait()
        self.click(MBElementEnum.TRANSFER_MONEY_CONTINUE.value)

    def get_payer_account(self):
        self.forced_wait()
        _text = self.get_text(MBElementEnum.ASSERT_PAYEE_PAYER.value)
        return _text

    def click_select_transfer_bank(self, bank):
        """
        选择要转账的银行
        :return:
        """
        # 点击选择银行下拉框
        self.click(MBElementEnum.TRANSFER_BANK_SELECT.value)
        # 输入要选择的银行
        self.input_bank(bank)
        # 选中银行
        self.click(MBElementEnum.TRANSFER_BANK_SELECTED.value)

    def input_bank(self, bank):
        """
        输入要选择的银行简称
        :param bank:
        :return:
        """
        self.type(MBElementEnum.TRANSFER_BANK_SEARCH.value, bank)

    def input_transfer_account(self, account: str):
        """
        输入收款人账号
        :param account: 1668868688
        :return:
        """
        self.type(MBElementEnum.TRANSFER_RECEIVER_ACCOUNT.value, account)

    def input_transfer_amount(self, amount: int):
        """
        输入转账金额
        :param amount: 10000
        :return:
        """
        self.type(MBElementEnum.TRANSFER_VND_AMOUNT.value, amount)

    def input_transfer_summary(self, summary: str):
        """
        输入转账备注
        :return:
        """
        self.type(MBElementEnum.TRANSFER_SUMMARY.value, summary)

    def click_confirm_transfer_information(self):
        """
        输入所有必填信息之后，确认收款信息(元素定位待调整)
        :return:
        """
        self.click(MBElementEnum.RECEIVER_INFO_CONFIRM_BTN.value)

    def click_transfer_otp(self):
        """
        确认转账
        :return:
        """
        self.forced_wait()
        self.click(MBElementEnum.SEND_VERIFY_CODE_BTN.value)

    def get_otp_qr(self):
        """
        获取OTP图片信息（元素定位待调整）
        :return:
        """
        self.forced_wait()
        base64_img = self.get_attribute(MBElementEnum.OTP_QR_XPATH.value, 'src')
        logger.info('获取OTP图片信息:{}', base64_img)
        return base64_img

    def input_otp_code(self, otp: str):
        """
        输入OTP码（元素定位待调整）OTP_INPUT | OTP_INPUT_XPATH
        :return:
        """
        self.type(MBElementEnum.OTP_INPUT.value, otp)

    def click_otp_submit(self):
        """
        提交，完整转账操作的最后一步（元素定位待调整） OTP_SUBMIT_BTN | OTP_SUBMIT_BTN_XPATH
        :return:
        """
        self.click(MBElementEnum.OTP_SUBMIT_BTN.value)

    def login(self, username: str, password: str, code: str):
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
        # 输入验证码
        self.input_captcha_code(code)
        # 点击登录
        self.click_login()

    def transfer(self, bank: str, payee_account: str, balance: int, summary: str):
        """
        步骤3，录入转账基本信息，并核对
        :param bank: 要选中的转账银行
        :param payee_account: 收款人银行卡
        :param balance: 转账金额
        :param summary: 转账备注
        :return:
        """
        # 下一步，进入转账操作界面
        self.click_transfer_continue()
        # 选择MB银行 (mb)
        self.click_select_transfer_bank(bank)
        # 输入收款人银行卡 '1668868688'
        self.input_transfer_account(payee_account)
        # 输入转账金额
        self.input_transfer_amount(balance)
        # 输入转账备注
        self.input_transfer_summary(summary)
        # 确认转账信息
        self.click_confirm_transfer_information()

    def send_confirm_otp(self):
        """
        步骤4，确认转账，并获取otp码
        :return: base64
        """
        # 确认转账
        self.click_transfer_otp()
        # 获取otp码
        base64_img = self.get_otp_qr()
        login_success_result = LoginResult(bank_trade_no='0000',
                                           status=ResultEnum.Success.value,
                                           base64ImageCaptcha=base64_img)
        return login_success_result

    def input_submit_otp(self, otp):
        """
        步骤5，接收，并提交OTP码
        :param otp: 支付需要的OTP码
        :return:
        """
        # 输入OTP码：
        self.input_otp_code(otp)

        # 最后一步，提交已输入的OTP
        self.click_otp_submit()
