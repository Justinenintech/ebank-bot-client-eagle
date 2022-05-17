# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vib_bank_app.py
# Time       ：2022/3/17 2:26 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from time import sleep

from loguru import logger

from src.bank_driver.tcb_bank_driver import TCBBankDriver
from src.base.enum.result_enum import ResultEnum
from src.base.enum.tcb_bank_enum import TCBElementEnum
from src.base.tool import Tool
from src.entity.login_result import LoginResult
from src.entity.pay_result import PayResult
from src.service.base_service import BaseService


class TCBBankApp(BaseService):
    """
    TCBBank 应用
    """

    def __init__(self, bank_type, bank_code, payee_bank_code, payee_account, payee_name, amount,
                 order_no,
                 task_id):
        BaseService.__init__(self)
        # self.bank_user_name = bank_user_name
        # self.bank_login_pwd = bank_login_pwd
        self.t = Tool()
        self.bs = BaseService()
        self.bank_driver = TCBBankDriver()
        self.bank_type = bank_type  # 转账类型
        self.payee_account = payee_account  # 收款人账号
        self.payee_name = payee_name  # 收款人姓名
        self.amount = amount  # 转账金额
        self.order_no = order_no  # 订单号
        self.task_id = task_id  # 任务
        self.bank_code = bank_code  # 转账人-银行编码 (待后端接口提供参数名称)
        self.payee_bank_code = payee_bank_code  # 收款人-银行编码 (待后端接口提供参数名称)
        self.payee_code_short = self.t.get_bank_code_params(self.bank_code,
                                                            self.payee_bank_code)  # 收款人银行编码（简称）
        # self.mbbank = '(mb)'  # 收款人银行编码（简称）
        self._get_proxy_count = 1

    def run(self) -> str:
        """
        运行 MBBankDriver
        """
        logger.debug("---打开MBBank的驱动---")
        logger.debug("task_id={} >>> payee_account: {}, payee_name: {},amount: {}, order_no: {}\n",
                     self.task_id,
                     self.payee_account,
                     self.payee_name,
                     self.amount,
                     self.order_no)

        # bank_driver = MBBankDriver(payee_account=self.payee_account, balance=self.amount, summary="watson test money")

        # todo 測試通過後 打開下面，刪除上面
        # bank_driver = MBBankDriver(payee_account=self.payee_account, balance=self.amount, summary=self.order_no)
        self.bank_driver.run()

        while True:
            # 获取登录账号密码与验证码的信息
            bank_user_name, bank_login_pwd, code, is_refresh_captcha = self._get_login_info(
                self.task_id)
            logger.info("bank_user_name：{} bank_login_pwd：{} code：{}", bank_user_name,
                        bank_login_pwd)

            # 等待登錄賬號密碼
            if bank_user_name is None or bank_login_pwd is None:
                logger.info("获取登录失败，等待500毫秒")
                sleep(.5)
                break
            logger.info("---获取登录信息，准备登录---")
            self.bank_driver.login(bank_user_name, bank_login_pwd)

            # 判断弹窗是否可以见
            _is_err_text = self.bank_driver.get_login_error_text()
            logger.info("is_enabled：{}", _is_err_text)

            if _is_err_text:
                logger.info("---登录银行失败---")
                login_failed_result = LoginResult()
                self._push_login_result(login_failed_result, self.task_id)
                continue
            else:
                logger.info("登錄成功，跳出登錄等待，账户余额为：{}", self.bank_driver.get_balance())
                login_result = LoginResult(bank_trade_no='0000', status=ResultEnum.Success.value)
                self._push_login_result(login_result, self.task_id)
                # 推送银行流水号，余额等信息
                logger.debug("---开始转账---")
                self.bank_driver.transfer(self.bank_type, self.payee_code_short, self.payee_account,self.payee_name,
                                          self.amount,
                                          self.order_no)
                logger.debug("---确认转账信息，获取otp信息---")
                otp_result = self.bank_driver.send_confirm_otp()
                logger.info(">>> login_result: {}", otp_result.__dict__)
                self._push_otp_tradeno_result(otp_result, self.task_id)

                # 等待获取 OTP
                otp = self._try_get_otp(TCBElementEnum.TCB_OTP_COUNTDOWN.value, self.task_id)
                if not otp:
                    pay_failed_result = PayResult()
                    # 推送otp验证结果
                    self._push_otp_intermediate_result(pay_failed_result, self.task_id)
                    self._push_pay_result(pay_failed_result, self.task_id)
                    return

                logger.debug("---MsbBank  输入 otp [" + str(otp) + "]---")
                self.bank_driver.input_submit_otp(otp)  # 接收，并提交OTP
                self.bank_driver.forced_wait()

                logger.info(">>>>>检查是否支付成功<<<<<<")
                is_success = self.bank_driver.get_transfer_success_img()
                otp_displayed = self.bank_driver.check_error_pop()
                logger.info("otp_displayed：{}", otp_displayed)
                logger.info("is_success：{}", is_success)
                if is_success:
                    logger.info(">>>>>进入支付成功，推送消息!<<<<<<{}", is_success)
                    _result = self.otp_success()
                    # 推送otp验证结果
                    self._push_otp_intermediate_result(_result, self.task_id)
                    # 推送支付结果
                    self._push_pay_result(_result, self.task_id)
                    self.bank_driver.dr_quit()
                    break
                if otp_displayed:
                    self.bank_driver.click_error_btn()
                    logger.info(">>>>检查到OTP错误，需要重新获取并推送OTP!<<<<<<{}", otp_displayed)
                    _result = self.otp_failure()
                    # 推送otp验证结果
                    self._push_otp_intermediate_result(_result, self.task_id)
                    # 推送支付结果
                    self._push_pay_result(_result, self.task_id)
                    self.bank_driver.dr_quit()
                    break

    def otp_success(self):
        try:
            logger.info(">>>>>支付成功!<<<<<")
            # 更新支付结果信息
            self.status = ResultEnum.Success.value
            self.bank_trade_no = "finish"
            self.summary = "支付成功"
        except Exception:
            # 更新支付结果信息
            self.status = ResultEnum.Failed.value
            self.bank_trade_no = "finish"
            self.summary = "支付失败"
            # 构造支付结果数据
        pay_result = PayResult(payer=self.payee_account, status=self.status,
                               bank_trade_no=self.order_no,
                               summary=self.summary)
        return pay_result

    def otp_failure(self):
        # logger.info("OTP错误：{}", self.bank_driver.get_enabled(MbbankElementEnum.ERROR_BTN.value))
        # 更新第一次OTP码错误信息
        self.status = ResultEnum.OTP_ERROR.value
        self.bank_trade_no = "finish"
        self.summary = "第一次 %d otp码错误, 支付失败" % self._get_proxy_count
        # 构造支付结果数据
        _result = PayResult(payer=self.payee_account, status=self.status,
                            bank_trade_no=self.order_no, summary=self.summary)
        logger.info('第一次otp码错误，支付失败', _result.__dict__)

        # 推送otp验证结果
        self._push_otp_intermediate_result(_result, self.task_id)
        # 第二次获取OTP
        # self.forced_wait()
        otp_result = self.bank_driver.send_confirm_otp()
        # otp_result = '839232312'
        logger.info("第二次获取OTP", otp_result)
        # 第二次推送OTP
        # self.forced_wait()
        self._push_otp_tradeno_result(otp_result, self.task_id)
        # self.forced_wait()
        # 等待输入OTP
        otp = self._try_get_otp(self.task_id)
        # otp = '89894434'
        logger.info('otp：{}', otp)

        if not otp:
            pay_failed_result = PayResult()
            # 推送otp验证结果
            self._push_otp_intermediate_result(pay_failed_result, self.task_id)
            # 推送支付结果
            self._push_pay_result(pay_failed_result, self.task_id)
            return
        logger.info("---MsbBank  输入 otp [" + str(otp) + "]---")
        # 输入OTP码：
        self.bank_driver.forced_wait()
        self.bank_driver.input_otp_code(otp)

        # 最后一步，提交已输入的OTP
        self.bank_driver.click_otp_submit()
        # bank_driver.get_submit_otp(otp)  # 接收，并提交OTP
        # is_success = self.bank_driver.isElementPresent(MbbankElementEnum.SUCCESS_ICON_XPATH.value)
        _displayed = self.bank_driver.check_error_pop()
        if _displayed:
            # 更新支付结果信息，为Failure_otp
            self.status = ResultEnum.FAILED_OTP.value
            self.bank_trade_no = "finish"
            self.summary = "第%d次otp码错误，退出" % (
                    self._get_proxy_count + 1)
            logger.info("第{}次otp码错误，退出", (self._get_proxy_count + 1))
            logger.info('self._get_proxy_count+1', self._get_proxy_count)
            pay_result = PayResult(payer=self.payee_account, status=self.status,
                                   bank_trade_no=self.order_no,
                                   summary=self.summary)
            return pay_result
        else:
            logger.info(">>>>>进入支付成功，推送消息!<<<<<<{}", _displayed)
            self.status = ResultEnum.Success.value
            self.bank_trade_no = "finish"
            self.summary = "第 %d 次支付成功" % (self._get_proxy_count + 1)
            pay_result = PayResult(payer=self.payee_account, status=self.status,
                                   bank_trade_no=self.order_no,
                                   summary=self.summary)
            logger.info("\n >>> 第 {} 次支付成功: {}\n", self.summary, pay_result.__dict__)
            return pay_result
