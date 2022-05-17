# coding=utf-8
import time

from loguru import logger
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
from src.base.BrowserBase import BrowserBase
from src.base.enum.result_enum import ResultEnum
from src.base.enum.tcb_bank_enum import TCBElementEnum
# from src.base.test import WebDriver
from src.base.tool import Tool

from src.entity.login_result import LoginResult


class TCBBankDriver(BrowserBase):
    """
    TCBBank驱动器
    """

    def __init__(self):
        BrowserBase.__init__(self)
        # 工具类
        self.t = Tool()
        # 登录入口
        self.login_url = TCBElementEnum.BANK_LOGIN_URL.value

    def run(self):
        """
        运行银行驱动
        """
        try:
            # 打开银行
            logger.info("---打开银行---")
            self.open_url(self.login_url)
            # self.open_bank()
        except Exception as e:
            logger.error(e)

    def open_bank(self):
        """
        打开浏览器，并访问网银登录地址
        :return:
        """
        # self.driver
        # self.
        self.open_url(self.login_url)

    def input_username(self, username: str):
        """
        输入登录账号
        :param username: str
        :return:
        """
        self.type(TCBElementEnum.USERNAME.value, username)

    def input_password(self, password: str):
        """
        输入登录密码
        :param password: str
        :return:
        """
        self.type(TCBElementEnum.PASSWORD.value, password)

    def get_transfer_success_img(self) -> bool:
        """
        校验支付成功的图片，来判断是否成功支付
        :return:bool
        """
        try:
            self.forced_wait()
            img_url = self.get_attribute(TCBElementEnum.SUCCESS_ICON_XPATH.value, 'src')
            logger.debug('img_png：{}', img_url)
            is_img = self.t.compare_images(img_url)
            # print()
            logger.debug("is_img vs down_img：{}", is_img)
            logger.debug('img_png_check：{}',
                         img_url.__eq__('https://online.mbbank.com.vn/assets/images/email.png'))
            return is_img
        except TimeoutException:
            return False

    def click_login(self):
        """
        点击登录
        :return:
        """
        self.click(TCBElementEnum.LOGIN.value)

    def get_login_error_text(self):
        """
        获取登录错误提示信息
        :return: str _text or False
        """
        try:
            _text = self.get_text(TCBElementEnum.ERROR_MSG.value)
            if _text.__eq__(TCBElementEnum.LOGIN_ERROR_TEXT.value):
                return True
        except TimeoutException:
            return False

    def get_balance(self) -> str:
        """
        获取登录网银账号的余额
        :return:
        """
        _text = self.get_text(TCBElementEnum.BALANCE.value)
        return _text

    def click_transfer_inter(self):
        """
        跨行转账页面，采用点击菜单栏的模式
        :return:
        """
        self.forced_wait()
        self.click(TCBElementEnum.TRANSFERS_MNU.value)
        self.forced_wait()
        self.click(TCBElementEnum.TRANSFER_INTER.value)
        # bank_select = WebDriverWait(driver=self.driver, timeout=300, poll_frequency=0.2) \
        #     .until(lambda x: x.find_element_by_xpath('//*[@id="qck_left_link"]/ul[2]/li/a'))
        # bank_select.click()

    def menu_list(self):
        res = self.get_text_list(TCBElementEnum.TRANSFER_MENU_LIST.value)
        logger.debug('res:{}', res)
        return res

    # def visit_domain_lists(self, span_text):
    #     link_domain_url = data['links'].get('link_domain_url')
    #     counts = self.count_elements(link_domain_url, '//a')
    #     # log1.info(counts)
    #     lines = self.find_element(link_domain_url)
    #     eles = lines.find_elements_by_xpath('//a')
    #     spans = lines.find_elements_by_xpath('//h2')
    #     for i in range(counts):
    #         if spans[i].text == span_text:
    #             _url = eles[i].get_attribute("href")
    #             log1.info("_url：%s" % _url)
    #             eles[i].click()
    #             # self.forced_wait(5)
    #             # self.get_new_handle()
    #             self.forced_wait(5)
    #             open_url = self.driver.current_url
    #             log1.info("open_url：%s" % open_url)
    #             assert _url.split("/")[2] == open_url.split("/")[
    #                 2], "进入官网站失败，网页中地址{%s}，打开的网站{%s}" % (
    #                 _url, open_url)
    #             log1.info("成功进入官网，打开的网站{%s}" % open_url)
    #             self.save_window_snapshot("线路检测：%s" % open_url)
    #             self.forced_wait(5)
    #             return _url, open_url

    def click_transfer_peer(self):
        """
        同行转账页面，采用点击菜单栏的模式
        :return:
        """
        self.click(TCBElementEnum.TRANSFERS_MNU.value)
        self.forced_wait()
        # self.click(TCBElementEnum.TRANSFER_PEER.value)

    def input_peer_payee_account(self, account: str):
        """
        同行、跨行，输入收款人账号
        :param account: 1668868688
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_PEER_ACCOUNT.value, account)

    def get_peer_payee_name(self):
        self.click(TCBElementEnum.TRANSFER_AMOUNT.value)
        # self.wait_time(3)
        time.sleep(3)
        name = self.get_attribute(TCBElementEnum.TRANSFER_PEER_PAYEE_NAME.value, 'value')
        logger.debug("name:{}", name)

    def input_transfer_amount(self, amount: int):
        """
        同行、跨行，输入转账金额
        :param amount: 10000
        :return: disabled_TAR.ACCT.NAME
        """
        self.click(TCBElementEnum.TRANSFER_AMOUNT.value)
        # self.wait_time(2)
        self.type(TCBElementEnum.TRANSFER_AMOUNT.value, amount)

    def click_blank_space(self):
        """
        同行，转账-点击空白处
        :return:
        """
        self.click(TCBElementEnum.TRANSFER_PEER_BLANK_SPACE.value)

    def input_transfer_remark(self, summary: str):
        """
        同行、跨行，输入转账备注
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_REMARK.value, summary)

    def click_confirm_transfer_information(self):
        """
        同行，跨行，输入所有必填信息之后，确认收款信息
        :return:
        """
        self.click(TCBElementEnum.TRANSFER_NEXT.value)

    def click_select_transfer_bank(self, bank_code):
        """
        跨行，选择要转账的银行
        :return:
        """
        self.forced_wait()
        # 输入要选择的银行
        self.input_inter_bank(bank_code)
        el = self.find_elements(TCBElementEnum.TRANSFER_MENU_LIST.value)
        # 判断需要的元素在哪里，点击
        for _ in el:
            if bank_code in _.text:
                _.click()
                break
        # 点击账号编辑框位置
        # self.click(TCBElementEnum.TRANSFER_INTER_ACCOUNT.value)

    def input_inter_bank(self, bank):
        """
        跨行，输入要选择的银行简称
        :param bank: 根据银行编码获取要输入的内容
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_INTER_SELECT_BANK.value, bank)

    def input_inter_payee_account(self, account):
        """
        跨行，输入收款人账号
        :param account: account
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_INTER_ACCOUNT.value, account)

    def input_inter_payee_name(self, name):
        """
        跨行，输入收款人姓名
        :param name: account
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_INTER_NAME.value, name)

    def click_transfer_otp(self):
        """
        确认转账，获取OTP
        :return:
        """
        self.click(TCBElementEnum.TRANSFER_CONFIRM.value)

    def get_otp_qr(self):
        """
        获取OTP图片信息
        :return:
        """
        self.forced_wait()
        base64_img = self.get_attribute(TCBElementEnum.TRANSFER_OTP_IMG.value, 'src')
        logger.info('获取OTP图片信息:{}', base64_img)
        return base64_img

    def input_otp_code(self, otp: str):
        """
        输入OTP码，OTP_INPUT | OTP_INPUT_XPATH
        :return:
        """
        self.type(TCBElementEnum.TRANSFER_OTP_INPUT.value, otp)

    def click_otp_submit(self):
        """
        提交OTP，完整转账操作的最后一步
        :return:
        """
        self.click(TCBElementEnum.TRANSFER_OTP_CONFIRM.value)

    def get_otp_error_text(self):
        """
        获取OTP错误提示信息
        :return: str _text or False
        """
        _true_or_false = self.check_get_text(TCBElementEnum.ERROR_MSG.value,
                                             TCBElementEnum.TRANSFER_OTP_ERROR_TEXT.value)
        return _true_or_false
        # try:
        #     _text = self.get_text(TCBElementEnum.ERROR_MSG.value)
        #     if _text.__eq__(TCBElementEnum.TRANSFER_OTP_ERROR_TEXT.value):
        #         return True
        # except TimeoutException:
        #     return False

    def get_transfer_success(self):
        """
        判断支付是否成功
        :return: bool True or False
        """
        _true_or_false = self.check_get_text(TCBElementEnum.TRANSFER_SUCCESS.value,
                                             TCBElementEnum.TRANSFER_SUCCESS_TEXT.value)
        return _true_or_false
        # try:
        #     _text = self.get_text(TCBElementEnum.TRANSFER_SUCCESS.value)
        #     if _text.__eq__(TCBElementEnum.TRANSFER_SUCCESS_TEXT.value):
        #         return True
        # except TimeoutException:
        #     return False

    def login_out(self):
        """
        退出网银登录
        :return:
        """
        self.click(TCBElementEnum.LOGIN_OUT.value)

    def accept_alert(self):
        """
        Accept warning box.
        Usage: driver.accept_alert()
        :return:
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        Dismisses the alert available.

        Usage:
        driver.dismissAlert()
        """
        self.driver.switch_to.alert.dismiss()

    def login(self, username: str, password: str):
        """
        步骤1，登录TCB网银
        :param username: 银行账号
        :param password: 银行密码
        :return:
        """
        # nonlocal count       # Python3中引入的新关键字
        # 输入银行账号
        self.input_username(username)
        # 输入银行密码
        self.input_password(password)
        # 点击登录
        self.click_login()

    def transfer(self, bank_type: str, bank: str, payee_account: str, payee_name: str, balance: int,
                 remark: str):
        """
        步骤3，录入转账基本信息，并核对
        :param bank_type: 转账类型
        :param bank: 要选中的转账银行
        :param payee_account: 收款人账号
        :param payee_name: 收款人姓名
        :param balance: 转账金额
        :param remark: 转账备注
        :return:
        """
        # 进入转账界面
        if bank_type == 'Inter':
            # 进入跨行转账页面
            self.click_transfer_inter()
            # td_values =  self.get_text_list()
            # for i in range(len(td_values)):
            # 选择收款人银行
            self.click_select_transfer_bank(bank)
            # 输入收款人账号
            self.input_inter_payee_account(payee_account)
            # 输入收款人姓名
            self.input_inter_payee_name(payee_name)
            # 输入转账金额
            self.input_transfer_amount(balance)
            # 输入转账备注
            self.input_transfer_remark(remark)
            # 进入确认转账页面
            self.click_confirm_transfer_information()
        elif bank_type == 'Peer':
            # 进入同行转账页面
            self.click_transfer_peer()
            # 输入收款人银行卡 '1668868688'
            self.input_peer_payee_account(payee_account)
            # 获取收款人姓名：
            self.get_peer_payee_name()
            # 输入转账金额
            self.input_transfer_amount(balance)
            # 输入转账备注
            self.input_transfer_remark(remark)
            # 进入确认转账页面
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
        :param otp: otp验证码
        :return:
        """
        # 输入OTP码：
        self.input_otp_code(otp)
        # 最后一步，提交已输入的OTP
        self.click_otp_submit()

#
# t = TCBBankDriver()
# t.open_browser('https://ib.techcombank.com.vn/servlet/BrowserServlet')
# # t.open_bank()
# # t.accept_alert()
# # t.dismiss_alert()
# t.login('thachminhtien99', 'Aa123456')
# # time.sleep(2)
# # t.get_balance()
# # 进入同行转账页面
# # t.click_transfer_inter()
# # t.click_transfer_peer()
# # counts = t.count_elements(TCBElementEnum.TRANSFER_MENU_LIST.value, '//a')
# # logger.debug("counts:{}",counts)
# # eles = t.find_elements(TCBElementEnum.TRANSFER_MENU_LIST.value)
# # for i in range(counts):
# #     if eles[i].text == 'Chuyển ngoài TCB':
# #         logger.debug("eles[i].text:{}", eles[i].text)
# #         eles[i].click()
# #     logger.debug("eles[i].text:{}",eles[i].text)
# # url = eles[2].get_attribute("onclick")
# # teest = eles[2].text
# # if teest == 'Chuyển ngoài TCB':
# #     logger.info(1212121212)
# # logger.info("teest:{}",teest)
# # text1= eles[2].find_elements(By.LINK_TEXT,'Chuyển ngoài TCB')
# # logger.info("text1:{}",text1)
# #     lines = self.find_element(link_domain_url)
# #     eles = lines.find_elements_by_xpath('//a')
# #     spans = lines.find_elements_by_xpath('//h2')
# #     for i in range(counts):
# #         if spans[i].text == span_text:
# # t.find_elements()
# # text = eles[2].text()
# # logger.debug("text:{}",text)
# # logger.info("onclick：{}" , url)
# # eles[2].click()
# # for i in range(counts):
# #     t.get_text()
#
# # t.menu_list()
# # time.sleep(100)
# t.transfer('Inter','QUOC TE (VIB)','014851865','TRAN THI HIEN',10000,'eagle test name')
# # t.transfer('Peer', 'QUOC TE (VIB)', '19038162742017', 'LE THI THUY', 10000, 'eagle test name')
# img = t.send_confirm_otp()
# logger.debug(img)
# otp = input("输入OTP")
# t.input_submit_otp(otp)
#
# is_true = t.get_transfer_success()
# if is_true:
#     logger.debug("支付成功")
# else:
#     logger.debug("支付失败")
#
# time.sleep(30)
# t.login_out()
# time.sleep(30)
# t.dr_quit()
