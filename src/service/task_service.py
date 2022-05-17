# coding=utf-8
from loguru import logger

from src.bank_app.bidv_bank_app import BIDVBankApp
from src.bank_app.mb_bank_app import MBBankApp
from src.bank_app.tcb_bank_app import TCBBankApp
from src.bank_app.vib_bank_app import VIBBankApp
from src.base.enum.bank_enum import BankEnum
from src.base.enum.task_enum import TaskEnum
# from src.base.log4py import logger
from src.service.base_service import BaseService


class TaskService(BaseService):
    """
    银行业务处理
    """

    def __init__(self):
        BaseService.__init__(self)

    def run(self):
        """
        业务入口
        1.拉取任务
        2.银行控制
        3.任务完成处理
        """

        # 1.拉取任务
        task = self._pull_task()
        if not task:
            return

        # 读取数据
        logger.debug("---读取数据---")
        task_id = str(task[TaskEnum.TASK_ID.value])
        order_no = str(task[TaskEnum.ORDER_NO.value])
        payee_account = str(task[TaskEnum.PAYEE_BANK_CARD.value])
        payee_name = str(task[TaskEnum.PAYEE_NAME.value])
        bank_login_pwd = str(task[TaskEnum.BANK_LOGIN_PASSWORD.value])
        bank_user_name = str(task[TaskEnum.BANK_USER_NAME.value])
        amount = str(task[TaskEnum.AMOUNT.value])
        bank_code = str(task[TaskEnum.BANK_CODE.value])
        bank_type = str(task[TaskEnum.BANK_TYPE.value])
        app_driver_code = str(task[TaskEnum.App_Driver_Code.value])
        payee_bank_code = str(task[TaskEnum.PAYEE_BANK_CODE.value])

        logger.info("\n ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓"
                    + "\n task_id: {}"
                    + "\n order_no: {}"
                    + "\n bank_user_name: {}"
                    + "\n bank_login_pwd: {}"
                    + "\n payee_account: {}"
                    + "\n payee_name: {}"
                    + "\n bank_code: {}"
                    + "\n amount: {}"
                    + "\n bank_type: {}"
                    + "\n app_driver_code: {}"
                    + "\n payee_bank_code: {}"
                    + "\n ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑", task_id, order_no,
                    bank_user_name,
                    bank_login_pwd, payee_account, payee_name, bank_code, amount, bank_type,
                    app_driver_code,
                    payee_bank_code)

        # 2.启动银行控制
        self.__run_bank_driver(bank_type, bank_code, payee_bank_code, payee_account, payee_name,
                               amount, order_no, task_id)

    def __run_bank_driver(self, bank_type, bank_code, payee_bank_code, payee_account, payee_name,
                          amount, order_no,
                          task_id):
        """
        启动银行 驱动
        :param bank_code: 银行编码
        :param bank_user_name: 网银登录用户名
        :param bank_login_pwd: 网银登录密码
        :param payee_account: 收款人账号
        :param amount: 金额
        :param order_no: 订单号
        :param task_id: 任务id
        """

        # if str(BankEnum.VietinBank.value).lower().__eq__(bank_code.lower()):
        #     logger.debug("---打开VietinBank---")
        #     vietin_bank_app = VietinBankApp(bank_user_name, bank_login_pwd,
        #                                     payee_account, amount, order_no, task_id)
        #     vietin_bank_app.run()

        # elif str(BankEnum.TechcomBank.value).lower().__eq__(bank_code.lower()):
        #     logger.debug("---打开TechcomBank---")
        #     techcom_bank_app = TechcomBankApp(payee_account, amount, order_no, task_id)
        #     techcom_bank_app.run()

        if str(BankEnum.MBBank.value).lower().__eq__(bank_code.lower()):
            logger.debug("---打开MBBank---")
            mb_bank_app = MBBankApp(bank_code, payee_bank_code, payee_account, amount, order_no,
                                    task_id)
            mb_bank_app.run()
        elif str(BankEnum.VIBBank.value).lower().__eq__(bank_code.lower()):
            logger.debug("---打开VIBBank---")
            vib_bank_app = VIBBankApp(bank_type, bank_code, payee_bank_code, payee_account, amount,
                                      order_no,
                                      task_id)
            vib_bank_app.run()
        elif str(BankEnum.TCBBank.value).lower().__eq__(bank_code.lower()):
            logger.debug("---打开TCBBank---")
            tcb_bank_app = TCBBankApp(bank_type, bank_code, payee_bank_code, payee_account,
                                      payee_name, amount, order_no,
                                      task_id)
            tcb_bank_app.run()
        elif str(BankEnum.BIDVBank.value).lower().__eq__(bank_code.lower()):
            logger.debug("---打开BIDVBank---")
            bidv_bank_app = BIDVBankApp(bank_type, bank_code, payee_bank_code, payee_account, amount, order_no,
                                      task_id)
            bidv_bank_app.run()
        #
        # elif str(BankEnum.MsbBank.value).lower().__eq__(bank_code.lower()):
        #     logger.debug("---打开MsbBank---")
        #     msb_bank_app = MsbBankApp(payee_account, amount, order_no, task_id)
        #     msb_bank_app.run()
        #
        # elif str(BankEnum.BIDVBank.value).lower().__eq__(bank_code.lower()):
        #     logger.debug("---打开BidvBank---")
        #     bidv_bank_app = BIDVBankApp(payee_account, amount, order_no, task_id)
        #     bidv_bank_app.run()
