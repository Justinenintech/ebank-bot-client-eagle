# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bidv_bank_driver.py
# Time       ：2022/3/25 2:14 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import time
from selenium.webdriver.support import expected_conditions as EC

from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from setttings import BIDV_CAPTCHA, BIDV_CAPTCHA_PNG
from src.base.BrowserBase import BrowserBase
from src.base.enum.bidv_bank_enum import BIDVElementEnum
from src.base.tool import Tool


class BIDVBankDriver(BrowserBase):
    """
    BIDVBank驱动器
    """

    def __init__(self):
        BrowserBase.__init__(self)
        # 工具类
        self._tool = Tool()
        # 登录入口
        self._url_login = BIDVElementEnum.BANK_LOGIN_URL.value
        # 跨行转账
        self._url_inter = BIDVElementEnum.TRANSFER_INTER_URL.value
        # 同行转账
        self._url_peer = BIDVElementEnum.TRANSFER_PEER_URL.value

        # 验证码失效提示信息
        self._captcha_time_out = BIDVElementEnum.ERROR_CAPTCHA_TIME_OUT.value
        # 验证码错误提示信息
        self._captcha_err = BIDVElementEnum.ERROR_CAPTCHA.value
        # 登录信息不正确
        self._user_pwd_err = BIDVElementEnum.ERROR_USERNAME_PASSWORD.value
        # OTP错误
        self._otp_err = BIDVElementEnum.ERROR_OTP.value
        # 超出接收次数
        self._otp_exceeded_limit = BIDVElementEnum.ERROR_OTP_EXCEEDED_LIMIT.value

    def run(self) -> str:
        """
        运行银行驱动
        """
        try:
            # 打开银行
            # logger.info("---打开银行---")
            self.open_bank()

            # 登录银行
            # logger.info("---读取验证码---")
            base64_img = self.get_captcha_base64()
            return base64_img
        except Exception as e:
            logger.error(e)
            return None

    def open_bank(self):
        """
        访问网银登录地址
        :return:
        """
        self.open_url(self._url_login)

    def input_username(self, username: str):
        """
        输入登录账号
        :param username: str
        :return:
        """
        self.type(BIDVElementEnum.USERNAME.value, username)

    def input_password(self, password: str):
        """
        输入登录密码
        :param password: str
        :return:
        """
        self.type(BIDVElementEnum.PASSWORD.value, password)

    def input_captcha_code(self, captcha):
        """
        输入验证码
        :param captcha: 验证码
        :return:
        """
        self.type(BIDVElementEnum.VERIFY_CODE.value, captcha)

    def get_captcha_base64(self) -> str:
        """
        获取登录图形验证码，base64
        :return: str
        """
        _captcha = self.find_element_visibility_of_located(BIDVElementEnum.CAPTCHA.value)
        _captcha.screenshot(BIDV_CAPTCHA_PNG)
        time.sleep(1)
        base64_img = self._tool.img_to_base64(BIDV_CAPTCHA_PNG)
        return base64_img

    def refresh_captcha_code(self):
        """
        刷新验证码按钮
        :return:
        """
        self.click(BIDVElementEnum.REFRESH_CAPTCHA.value)

    def click_login(self):
        """
        点击登录
        :return:
        """
        self.click(BIDVElementEnum.SUBMIT_BTN.value)

    def check_error_msg(self):
        """
        判断错题提示信息
        :return:
        """
        _msg_dict = {self._captcha_time_out: {True: "验证码过期！"},
                     self._captcha_err: {True: "验证码错误！"},
                     self._otp_err: {True: "OTP错误！"},
                     self._user_pwd_err: {
                         True: "登录信息不正确，5次或以上，服务将被锁定！"},
                     self._otp_exceeded_limit: {True: "每天接收OTP次数不能超过30次！"}
                     }
        try:
            self.forced_wait()
            _text = self.get_text(BIDVElementEnum.ERROR_MSG.value, 5)
            if _text is not None:
                self.click(BIDVElementEnum.ERROR_BTN.value)
                return _msg_dict.get(_text)
            else:
                return {False: "没有发现错误！"}
        except TimeoutException:
            return {False: "超时，没有发现错误！"}

    def check_error_otp_btn(self):
        """
        检查错误弹窗是否出现
        :return:
        """
        try:
            self.forced_wait()
            is_enabled = self.get_enabled(BIDVElementEnum.SUBMIT_BTN.value)
            logger.debug("is_enabled:{}",is_enabled)
            if is_enabled:
                return True
        except TimeoutException:
            return False

    def check_login_otp(self) -> bool:
        """
        登录时，用于判断是否有OTP
        :return: str _text or False
        """
        true_or_false = self.check_get_text(BIDVElementEnum.LOGIN_OTP_CHECK.value,
                                            BIDVElementEnum.LOGIN_OTP_CHECK_TEXT.value)
        return true_or_false
        # try:
        #     self.forced_wait()
        #     # _is_enabled = self.check_error_otp_btn()
        #     element = WebDriverWait(self._driver_base, 10, poll_frequency=1,).until(
        #         EC.text_to_be_present_in_element(BIDVElementEnum.LOGIN_OTP_CHECK.value,BIDVElementEnum.LOGIN_OTP_CHECK_TEXT.value))
        #     logger.debug("element:{}",element)
        #     if element:
        #         _text = self.get_text(BIDVElementEnum.LOGIN_OTP_CHECK.value)
        #         logger.debug("_text:{}", _text)
        #         if _text.__eq__(BIDVElementEnum.LOGIN_OTP_CHECK_TEXT.value):
        #             return True
        # except TimeoutException:
        #     return False

    def input_otp(self, otp: str):
        """
        输入OTP
        :param otp: str 6位
        :return:
        """
        self.type(BIDVElementEnum.LOGIN_OTP_INPUT.value, otp)

    def submit_otp(self):
        """
        提交OTP
        :return:
        """
        self.click(BIDVElementEnum.SUBMIT_BTN.value)

    def click_cancel(self):
        """
        点击取消按钮，不参与
        :return:
        """
        # self.click(BIDVElementEnum.CANCEL.value)
        try:
            self.click(BIDVElementEnum.CANCEL.value)
        except TimeoutException:
            return "不存在弹出广告"

    def get_balance(self):
        """
        获取余额
        :return:
        """
        self.forced_wait()
        self.click_cancel()
        # self.forced_wait()
        self.click(BIDVElementEnum.BALANCE_SHOW.value)  # 展示已隐藏的余额
        self.forced_wait()
        balance = self.get_text(BIDVElementEnum.BALANCE.value)
        logger.debug('balance:{}', balance)
        return balance

    def open_transfer_inter(self):
        """
        进入跨行转账
        :return:
        """
        self.open_url(self._url_inter)

    def open_transfer_peer(self):
        """
        进入同行转账
        :return:
        """
        self.open_url(self._url_peer)

    def click_inter_profile(self):
        """
        跨行，进入收款人编辑页面
        :return:
        """
        self.forced_wait()
        self.move_to_element(BIDVElementEnum.TRANSFER_INTER_PROFILE.value)
        self.click(BIDVElementEnum.TRANSFER_INTER_PROFILE.value)

    def click_inter_select_bank(self):
        """
        跨行，展开银行下拉框进行操作
        :return:
        """
        self.forced_wait()
        self.click(BIDVElementEnum.TRANSFER_INTER_SELECT_BANK.value)

    def selected_inter_bank(self, bank_code: str):
        """
        跨行，选中银行
        :param bank_code:
        :return:
        """
        el = self.find_elements(BIDVElementEnum.TRANSFER_INTER_SELECTED_BANK.value)
        # 判断需要的元素在哪里，点击
        for _ in el:
            if bank_code in _.text:
                _.click()
                break

    def input_inter_account(self, account: str):
        """
        输入收款人账号
        :param account: str 收款人账号
        :return:
        """
        self.type(BIDVElementEnum.TRANSFER_INTER_ACCOUNT.value, account)

    def click_inter_profile_confirm(self):
        """
        收款人基本信息，提交按钮
        :return:
        """
        self.click(BIDVElementEnum.TRANSFER_INTER_PROFILE_CONFIRM.value)

    def input_inter_amount(self, amount: int):
        """
        转账金额
        :param amount: int
        :return:
        """
        self.type(BIDVElementEnum.TRANSFER_INTER_AMOUNT.value, amount)

    def input_inter_remark(self, remark: str):
        """
        备注
        :return:
        """
        self.click(BIDVElementEnum.TRANSFER_INTER_REMARK.value)
        self.type(BIDVElementEnum.TRANSFER_INTER_REMARK.value, remark)

    def get_otp_qr(self):
        """
        获取OTP图片信息
        :return:
        """
        # self.js_scroll_end()
        try:
            self.forced_wait()
            base64_img = self.get_attribute(BIDVElementEnum.TRANSFER_INTER_OTP_IMG.value, 'src')
            logger.info('获取OTP图片信息:{}', base64_img)
            return base64_img
        except TimeoutException:
            base64_img = self.get_attribute(BIDVElementEnum.TRANSFER_INTER_OTP_IMG.value, 'src')
            logger.info('获取OTP图片信息:{}', base64_img)
            return base64_img

    def click_inter_confirm(self):
        """
        转账，提交按钮
        :return:
        """
        self.click(BIDVElementEnum.TRANSFER_INTER_CONFIRM.value)

    def check_transfer_success(self):
        """
        判断转账是否成功
        :return: str _text or False
        """
        try:
            # self.forced_wait()
            _text = self.get_text(BIDVElementEnum.TRANSFER_SUCCESS.value)
            logger.debug("_text:{}", _text)
            if _text.__eq__(BIDVElementEnum.TRANSFER_SUCCESS_TEXT.value):
                return True
        except TimeoutException:
            return False

    def check_transfer_failed(self):
        """
        获取倒计的值
        :return:
        """
        try:
            # self.forced_wait()
            _text = self.get_text(BIDVElementEnum.TRANSFER_FAILED.value)
            logger.debug("_text:{}", _text)
        except TimeoutException:
            return False

    def login(self, username: str, password: str, captcha: str):
        # 输入账号
        self.input_username(username)
        # 输入密码
        self.input_password(password)
        # captcha = input("验证码：")
        # 输入验证码
        self.input_captcha_code(captcha)
        # 点击登录
        self.click_login()

    def input_submit_otp(self, otp: str):
        """
        输入OTP，并提交
        :param otp: str otp码
        :return:
        """
        self.input_otp(otp)
        self.submit_otp()

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
            self.open_transfer_inter()
        elif bank_type == 'Peer':
            self.open_transfer_peer()
        # 进入收款人编辑页面
        self.click_inter_profile()
        self.forced_wait()
        # 展开银行下拉框
        self.click_inter_select_bank()
        # 选中银行
        self.selected_inter_bank(bank)
        # 输入收款人银行卡 '1668868688'
        self.input_inter_account(payee_account)
        # 提交收款人
        self.click_inter_profile_confirm()
        self.forced_wait()
        # 输入转账金额
        self.input_inter_amount(balance)
        # 输入转账备注
        self.input_inter_remark(remark)
        # 点击下一步，进入otp二维码推送页面
        self.click_inter_confirm()

#
# b = BIDVBankDriver()
# b.open_bank()
# b.forced_wait()
# b.input_username('0762345171')
# b.input_password('Aa123123@')
# print(b.get_captcha_base64())
# # b.login('0762345171', 'Aa123123@')
# code = input("验证码：")
# b.input_captcha_code(code)
# b.click_login()
#
# # nets = b.check_error_msg()
# # (key, value), = nets.items()
# # # logger.debug('nets:{}',nets)
# # # logger.debug('nets:{}',type(nets))
# # logger.debug('key:{}', key)
# # logger.debug('value:{}', value)
# # b.refresh() if key else "没有发现错误提示"
#
# is_otp = b.check_login_otp()
# logger.debug("is_otp:{}", is_otp)
# if is_otp:
#     otp = input("OTP：")
#     # b.input_otp(otp)
#     # b.submit_otp()
#     b.input_submit_otp(otp)
# time.sleep(300)
# nets = b.check_error_msg()
# (key, value), = nets.items()
# b.refresh() if key else "没有发现错误提示"
# # 如果验证码2分钟超时，则要重新去输入用户名登录
# # b.click_black_space()
#
# b.get_balance()
# b.open_transfer_inter()
# b.click_inter_profile()
# b.forced_wait()
# b.click_inter_select_bank()
#
# # 提取此下拉框中的所有元素
# lis = b.find_elements(['xpath', "//ul[@class='select2-results__options']/li"])
#
# # 判断需要的元素在哪里，点击
# for li in lis:
#     if "MB" in li.text:
#         li.click()
#         break
#
# b.input_inter_account('0374299563')
# b.click_inter_profile_confirm()
# b.forced_wait()
#
# b.input_inter_amount(10000)
# b.input_inter_remark('eagle transfer money')
# b.click_inter_confirm()
# b.forced_wait()
# logger.debug("otp:{}", b.get_otp_qr())
# while True:
#     count = 0
#     if count >= 120:
#         b.check_transfer_failed()
#         print('交易失败')
#     is_true = b.check_transfer_success()
#     if is_true:
#         print("交易成功")
