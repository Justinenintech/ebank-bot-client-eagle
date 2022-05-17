# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : bidv_bank_app.py
# Time       ：2022/3/26 11:02 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import time
from time import sleep

from loguru import logger

from setttings import BIDV_PAY_FAILURE, BIDV_PAY_SUCCESS
from src.bank_driver.bidv_bank_driver import BIDVBankDriver
from src.base.enum.bidv_bank_enum import BIDVElementEnum
from src.base.enum.result_enum import ResultEnum
from src.base.tool import Tool
from src.entity.login_result import LoginResult
from src.entity.pay_result import PayResult
from src.service.base_service import BaseService


class BIDVBankApp(BaseService):
    """
    BIDVBank 应用
    """

    def __init__(self, bank_type, bank_code, payee_bank_code, payee_account, amount, order_no,
                 task_id):
        BaseService.__init__(self)
        self.t = Tool()
        self.bs = BaseService()
        self.bank_driver = BIDVBankDriver()
        self.payee_account = payee_account  # 收款人账号
        self.amount = amount  # 转账金额
        self.order_no = order_no  # 订单号
        self.task_id = task_id  # 任务
        self.bank_type = bank_type  # 转账类型
        self.bank_code = bank_code  # 转账人-银行编码 (待后端接口提供参数名称)
        self.payee_bank_code = payee_bank_code  # 收款人-银行编码 (待后端接口提供参数名称)
        self.payee_code_short = self.t.get_bank_code_params(self.bank_code,
                                                            self.payee_bank_code)  # 收款人银行编码（简称）
        self._get_proxy_count = 1

    def run(self) -> str:
        """
        运行 BIDVBankDriver
        """
        logger.debug("---打开BIDVBankDriver的驱动---")
        logger.debug("task_id={} >>> payee_account: {}, amount: {}, order_no: {}\n",
                     self.task_id,
                     self.payee_account,
                     self.amount,
                     self.order_no)

        # todo 測試通過後 打開下面，刪除上面
        base64_img = self.bank_driver.run()

        # 推送图形验证码
        self._push_captcha_base64Image(self.task_id, base64_img)

        while True:
            # 获取登录账号密码与验证码的信息
            bank_user_name, bank_login_pwd, code, is_refresh_captcha = self._get_login_info(
                self.task_id)
            # logger.info("bank_user_name：{} bank_login_pwd：{} code：{}", bank_user_name,
            #             bank_login_pwd, code)

            # 刷新驗證碼
            if is_refresh_captcha:
                logger.info("---刷新验证---")
                self.bank_driver.refresh_captcha_code()
                self.bank_driver.forced_wait()
                verify_code_base64 = self.bank_driver.get_captcha_base64()

                logger.info("---推送图形验证码---")
                self._push_captcha_base64Image(self.task_id, verify_code_base64)
                continue

            # 等待登錄賬號密碼
            if bank_user_name is None or bank_login_pwd is None or code is None or code == "null":
                logger.info("获取登录失败，等待500毫秒")
                sleep(.5)
                break
            logger.info("---获取登录信息，准备登录---")
            self.bank_driver.login(bank_user_name, bank_login_pwd, code)
            self.bank_driver.forced_wait()
            is_otp = self.bank_driver.check_login_otp()
            if is_otp:
                logger.debug("登录需要输入OTP")
                # 如果存在OTP，则推送OTP通知
                login_success_result = LoginResult(bank_trade_no='0000',
                                                   status=ResultEnum.Success.value,
                                                   base64ImageCaptcha=None,
                                                   showSecLoginCode="Y")
                self._push_otp_tradeno_result(login_success_result, self.task_id)

                # 等待获取 OTP
                otp = self._try_get_otp(BIDVElementEnum.BIDV_OTP_COUNTDOWN.value, self.task_id)
                if not otp:
                    _msg = "获取OTP信息超时，登录失败!"
                    _failed_result = PayResult(summary=_msg)
                    # 推送otp验证结果
                    self._push_otp_intermediate_result(_failed_result, self.task_id)
                    # 提交登录结果
                    self._push_login_result(_failed_result, self.task_id)
                    break

                logger.debug("---BIDVBankDriver  输入 otp [" + str(otp) + "]---")
                self.bank_driver.input_submit_otp(otp)  # 接收，并提交OTP
                self.bank_driver.forced_wait()
            else:
                logger.debug("登录不需要输入OTP")
                login_success_result = LoginResult(bank_trade_no='0000',
                                                   status=ResultEnum.Success.value,
                                                   base64ImageCaptcha=None,
                                                   showSecLoginCode=None)

                self._push_otp_tradeno_result(login_success_result, self.task_id)
            # 判断是否有错误提示信息
            is_msg = self.bank_driver.check_error_msg()
            logger.info("is_msg：{}", is_msg)
            (is_true, value), = is_msg.items()
            if is_true and value != 'OTP错误！':
                # logger.info("---登录银行失败---")
                self.bank_driver.refresh()
                login_failed_result = LoginResult()
                self._push_login_result(login_failed_result, self.task_id)
                verify_code_base64 = self.bank_driver.get_captcha_base64()

                logger.info("---推送图形验证码---")
                self._push_captcha_base64Image(self.task_id, verify_code_base64)
                continue
            if is_true and value == 'OTP错误！':
                _login_result = self.otp_failure()
                if _login_result.__dict__['status'].__eq__(ResultEnum.Failed.value):
                    self._push_login_result(_login_result, self.task_id)
                    self.bank_driver.dr_quit()
                    break

            self.bank_driver.forced_wait()
            # logger.info("登錄成功，跳出登錄等待，账户余额为：{}", self.bank_driver.get_balance())
            _balance = ''.join(list(filter(str.isdigit, self.bank_driver.get_balance())))
            # if _balance.isdigit():
            #     login_result = LoginResult(bank_trade_no='0000', status=ResultEnum.Success.value)
            #     # 推送otp验证结果
            #     self._push_otp_intermediate_result(login_result, self.task_id)
            #     # 推送登录结果
            #     self._push_login_result(login_result, self.task_id)
            logger.info("登錄成功，跳出登錄等待，账户余额为：{}", _balance)
            if int(_balance) < int(self.amount):
                _msg = "余额不足，结束继续转账业务，余额：%s,转账金额：%s" % (_balance, self.amount)
                logger.debug("余额不足，结束继续转账业务，余额：{},转账金额：{}", _balance, self.amount)
                # 推送登录结果
                login_result = LoginResult(bank_trade_no='0000', status=ResultEnum.Failed.value,
                                           errMsg=_msg)
                self._push_login_result(login_result, self.task_id)
                self.bank_driver.dr_quit()
                break
            logger.debug("---开始转账---")
            self.bank_driver.transfer(self.bank_type, self.payee_code_short, self.payee_account,
                                      self.amount,
                                      self.order_no)
            logger.debug("---确认转账信息，获取otp信息---")
            otp_img = self.bank_driver.get_otp_qr()
            otp_result = LoginResult(bank_trade_no='0000',
                                     status=ResultEnum.Success.value,
                                     base64ImageCaptcha=otp_img,
                                     showSecLoginCode=None)
            logger.info(">>> login_result: {}", otp_result.__dict__)
            self._push_otp_tradeno_result(otp_result, self.task_id)
            start = time.perf_counter()

            for i in range(120):
                time.sleep(1)
                is_true = self.bank_driver.check_transfer_success()
                if is_true:
                    self.status = ResultEnum.Success.value
                    self.bank_trade_no = "finish"
                    self.summary = "支付成功"
                    break
                # print('start', start)
                end = time.perf_counter()
                # print('end', end)
                # print("end - start", end - start)
                if end - start >= 120:
                    _text = self.bank_driver.check_transfer_failed()
                    _count = ''.join(list(filter(str.isdigit, _text)))
                    if int(_count) == 0:
                        self.status = ResultEnum.Failed.value
                        self.bank_trade_no = "finish"
                        self.summary = "超时，支付失败"
                        # print("end", end - start)
                        break
            pay_result = PayResult(payer=self.payee_account, status=self.status,
                                   bank_trade_no=self.order_no,
                                   summary=self.summary)
            # pay_result = self.assert_success_failed()
            # 推送otp验证结果
            self._push_otp_intermediate_result(pay_result, self.task_id)
            # 推送支付结果
            self._push_pay_result(pay_result, self.task_id)
            # 退出浏览器
            self.bank_driver.dr_quit()
            break

    def assert_success_failed(self):
        count = 0
        while True:
            logger.debug('count:{}', count)
            if count >= 120:
                self.bank_driver.check_transfer_failed()
                self.status = ResultEnum.Failed.value
                self.bank_trade_no = "finish"
                self.summary = "支付失败"
                break
            is_true = self.bank_driver.check_transfer_success()
            if is_true:
                self.status = ResultEnum.Success.value
                self.bank_trade_no = "finish"
                self.summary = "支付成功"
                break
            time.sleep(1)
            count += 1
        # 构造支付结果数据
        pay_result = PayResult(payer=self.payee_account, status=self.status,
                               bank_trade_no=self.order_no,
                               summary=self.summary)
        return pay_result

    def otp_failure(self):
        # 更新第一次OTP码错误信息
        self.status = ResultEnum.OTP_ERROR.value
        self.bank_trade_no = "finish"
        self.summary = "第%d次otp码错误, 登录失败" % self._get_proxy_count
        # 构造支付结果数据
        _result = PayResult(payer=self.payee_account, status=self.status,
                            bank_trade_no=self.order_no, summary=self.summary)
        logger.info('第1次otp码错误，登录失败', _result.__dict__)

        # 推送otp验证结果
        self._push_otp_intermediate_result(_result, self.task_id)
        # 等待输入OTP
        otp = self._try_get_otp(BIDVElementEnum.BIDV_OTP_COUNTDOWN.value, self.task_id)
        if not otp:
            _msg = "获取OTP信息超时，登录失败!"
            _failed_result = PayResult(summary=_msg)
            # 推送otp验证结果
            self._push_otp_intermediate_result(_failed_result, self.task_id)
            # 提交登录结果
            self._push_login_result(_failed_result, self.task_id)
            self.bank_driver.dr_quit()
            return

        logger.debug("---BIDVBankDriver  输入 otp [" + str(otp) + "]---")
        self.bank_driver.input_submit_otp(otp)  # 接收，并提交OTP
        self.bank_driver.forced_wait()

        # 判断是否有错误提示信息
        is_msg = self.bank_driver.check_error_msg()
        logger.info("is_msg：{}", is_msg)
        (is_true, value), = is_msg.items()
        if is_true and value == 'OTP错误！':
            # 更新支付结果信息，为Failure_otp
            self.status = ResultEnum.FAILED_OTP.value
            self.bank_trade_no = "finish"
            self.summary = "第%d次otp码错误，登录失败" % (
                    self._get_proxy_count + 1)
            logger.info("第{}次otp码错误，登录失败", (self._get_proxy_count + 1))
            # logger.info('self._get_proxy_count+1', self._get_proxy_count)
            pay_result = PayResult(payer=self.payee_account, status=self.status,
                                   bank_trade_no=self.order_no,
                                   summary=self.summary)
            # 推送otp验证结果
            self._push_otp_intermediate_result(pay_result, self.task_id)
            # 推送登录结果
            login_result = LoginResult(errMsg=self.summary)
            return login_result
        else:
            logger.info(">>>>>成功登录，推送余额!<<<<<<")
            self.status = ResultEnum.Success.value
            self.bank_trade_no = "finish"
            self.summary = "第%d次otp码正确，登录成功" % (self._get_proxy_count + 1)
            pay_result = PayResult(payer=self.payee_account, status=self.status,
                                   bank_trade_no=self.order_no,
                                   summary=self.summary)
            # 推送otp验证结果
            self._push_otp_intermediate_result(pay_result, self.task_id)
            logger.info("\n >>> {} : {}\n", self.summary, pay_result.__dict__)
            login_result = LoginResult(bank_trade_no='0000', status=ResultEnum.Success.value,
                                       errMsg=self.summary)
            return login_result
