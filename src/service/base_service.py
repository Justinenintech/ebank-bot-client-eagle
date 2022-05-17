# coding=utf-8
import time
from time import sleep

from loguru import logger

from src.base import http_re
from src.base.config import Config
from src.base.enum.api_enum import Api
from src.base.enum.response_code_enum import ResponseCodeEnum
from src.base.enum.result_enum import ResultEnum
from src.base.enum.task_enum import TaskEnum
from src.base.enum.task_status_type import TaskStatusAndType
from src.base.http_re import put, get, post
# from src.base.log4py import logger
from src.base.return_code import ResponseCode
from src.dao.task_dao import TaskDao
from src.dao.uid_dao import UidDao
from src.entity.login_result import LoginResult
from src.entity.pay_result import PayResult


class BaseService:
    def __init__(self):
        """
        配置系统默认使用数据
        """
        self.uid_dao = UidDao()
        self.task_dao = TaskDao()
        self._otp_beanret = {}
        # 系统配置文件信息
        cfg = Config()
        self.host = cfg.read("sys", "server_host")
        self.image_download_path = cfg.read("sys", "image_download_path")
        # 读取频率
        self.frequency_time = cfg.read("sys", "frequency_time")

        # vietinbank 配置文件读取
        self.vietinbank_login_url = cfg.read("vietinbank", "bank_login_url")
        # 银行转账页面
        self.bank_transfer_page_url = cfg.read("vietinbank", "bank_transfer_page_url")

        # techcombank 配置文件读取
        self.techcombank_login_url = cfg.read("techcombank", "bank_login_url")

        # mbbank 配置文件读取
        self.mbbank_login_url = cfg.read("mbbank", "bank_login_url")
        self.mb_bank_transfer_page_url = cfg.read("mbbank", "bank_transfer_page_url")

        # msbbank 配置文件读取
        self.msbbank_login_url = cfg.read("msbbank", "bank_login_url")
        self.msbbank_verify_code_url = cfg.read("msbbank", "bank_verify_code_url")

        # bidv 配置文件读取
        self.bidvbank_login_url = cfg.read("bidvbank", "bank_login_url")
        self.bidvbank_transfer_page_url = cfg.read("bidvbank", "bank_transfer_page_url")

        # vib 配置文件读取
        self.vibbank_login_url = cfg.read("vibbank", "bank_login_url")
        self.vibbank_transfer_page_url = cfg.read("vibbank", "bank_transfer_page_url")

    def _pull_task(self) -> dict:
        """
        拉取任務
        :return: 任務
        """

        try:
            uid = self.uid_dao.get_id()
            if not uid:
                return None

            beanret = http_re.get(url=str(self.host + Api.Get_Task_Url.get_task_url(str(uid.id))),
                                  token=str(uid.token))
            self._otp_beanret = beanret
            if beanret.code.__eq__(ResponseCode.Success.value):
                task_data = beanret.data
                task_id = str(task_data[TaskEnum.TASK_ID.value])
                task = self.task_dao.get(task_id)
                if task:
                    logger.warning('task-{} 已经存在', task_id)
                    return None
                else:
                    logger.info('拉到的任务id,进行本地缓存-{}', task_id)
                    self.task_dao.insert(task_id, TaskStatusAndType.Bot_Doing.value, time.time())
                    return task_data
            else:
                beanret.token = None
                logger.info("beanret.to_json():{}",beanret.to_json())
                return None

        except Exception as e:
            logger.error('{}', e)
            return None

    def _try_get_task_detail(self, task_id) -> dict:
        """
        拉取任务详情，用于验证码之后
        """
        # 尝试获取任务详情
        url = self.host + str(Api.Get_Task_Detail_Url.value) \
            .replace("{taskId}", task_id)
        count = 0
        while True:
            if count >= 240:
                logger.error("!!!获取验证码后任务详情 超时等待，支付失败!!!")
                return None

            logger.info("---尝试获取验证码后任务详情---")
            r = get(url)
            if str(r.code).__eq__(ResponseCodeEnum.Success.value):
                task = r.data
                if task:
                    return task
            sleep(1)
            count += 1

    def _push_qr_base64Image_get_otp(self, task_id, qr_base64) -> str:
        """
        推送二维码字节流
        :param task_id: 任务id
        :param qr_base64: 二维码字符串
        :return: otp
        """
        logger.info("推送图形验证码")
        url = self.host + str(Api.Push_Qr_Task_Url.value) \
            .replace("{taskId}", task_id)
        task = {
            "id": task_id,
            "qrCode": str(qr_base64)
        }

        post(url, data=task)

    def _push_captcha_base64Image(self, task_id, captcha):
        """
        推送图形验证码
        :param task_id: 任务id
        :param captcha: base64Image
        """
        logger.info("推送图形验证码")
        url = self.host + str(Api.Push_Captcha_Task_Url.value) \
            .replace("{taskId}", task_id)
        task = {
            "id": task_id,
            "captcha": str(captcha)
        }

        post(url, data=task)

    def _done_task(self, task_id, data):
        """
        任务完成
        :param task_id: 任务id
        """
        logger.info("修改任务为完成")
        url = self.host + str(Api.Done_Task_Url.value) \
            .replace("{taskId}", task_id)
        task = {
            "id": task_id,
            "result": str(data)
        }

        put(url, data=task)

    def _try_get_otp(self, countdown: int, task_id) -> str:
        """
        获取otp
        :param trade_no: 交易码
        :param task_id: 任务id
        :return: otp
        """

        # 尝试获取otp
        url = self.host + str(Api.Get_Otp_Url.value) \
            .replace("{taskId}", task_id)
        count = 0
        while True:
            if count >= int(countdown):  # 240
                logger.error("!!!获取otp 超时等待，支付失败!!!")
                return None

            logger.info("---尝试获取otp---")
            r = get(url)
            if str(r.code).__eq__(ResponseCodeEnum.Success.value):
                otp_code = r.data
                if otp_code:
                    logger.info("获取到otp：{}，长度：{}", str(otp_code), len(otp_code))
                    return otp_code
            sleep(1)
            count += 1

    def _push_login_result(self, data, task_id):
        """
        登录结果接口
        :param data:  结果数据
        :param task_id: 任务id
        :return:
        """

        logger.info("登录结果接口")
        url = self.host + str(Api.Login_Error_Result_Url.value) \
            .replace("{taskId}", task_id)

        put(url, data=data)

    def _push_otp_tradeno_result(self, data, task_id):
        """
        推送 otp 交易信息结果
        :param data:  结果数据
        :param task_id: 任务id
        :return:
        """

        logger.info("推送 otp 交易信息结果接口")
        url = self.host + str(Api.Otp_Tradeno_Url.value) \
            .replace("{taskId}", task_id)

        put(url, data=data)

    def _push_pay_result(self, result_data, task_id):
        """
        支付结果
        :param result_data: 结果数据
        :param task_id: 任务id
        :return:
        """
        logger.info("支付结果")
        url = self.host + str(Api.Pay_Result_Url.value) \
            .replace("{taskId}", task_id)

        put(url, data=result_data)

    def _push_otp_intermediate_result(self, result_data, task_id):
        """
        推送opt验证结果 接口
        :param result_data: 结果数据
        :param task_id: 任务id
        :return:
        """
        logger.info("推送opt验证结果")
        url = self.host + str(Api.Otp_Intermediate_State.value) \
            .replace("{taskId}", task_id)

        put(url, data=result_data)

    def _get_login_info(self, task_id):
        """
        获取登录信息
        :param task_id: 任务id
        :return: 登录用的账号密码，验证码信息
        """
        logger.info("登录结果")
        uid = self.uid_dao.get_id()
        if not uid:
            return None

        url = self.host + str(Api.Login_Info_Url.value) \
            .replace("{botId}", str(uid.id)) \
            .replace("{taskId}", task_id)
        count = 0
        while True:
            if count >= 270:
                logger.error("!!!获取登录信息 超时等待，登录失败!!!")
                login_failed_result = LoginResult(errMsg="获取登录信息超时，登录失败!")
                self._push_login_result(login_failed_result.__dict__, task_id)
                # username,password,captcha,is_refresh_captcha
                return None, None, None, None
            logger.debug("count:{}",count)
            logger.info("---尝试获取登录信息---")
            r = get(url)
            logger.debug("str(r.code):{}", str(r.code))
            logger.debug("ResponseCodeEnum.Success.value:{}", ResponseCodeEnum.Success.value)
            if str(r.code).__eq__(ResponseCodeEnum.Success.value):
                data = r.data
                logger.debug("data:{}", data)
                # username,password,captcha,is_refresh_captcha
                return data['userName'], data['password'], data['captcha'], False
            elif str(r.code).__eq__(ResponseCodeEnum.Refresh_Captcha.value):
                # username,password,captcha,is_refresh_captcha
                return None, None, None, True
            # if str(r.code).__eq__(ResponseCodeEnum.Success.value):
            #     data = r.data
            #     logger.debug("data:{}",data)
            #     # username,password,captcha,is_refresh_captcha
            #     return data['userName'], data['password'], data['captcha'], False
            # elif str(r.code).__eq__(ResponseCodeEnum.Refresh_Captcha.value):
            #     # username,password,captcha,is_refresh_captcha
            #     return None, None, None, True
            sleep(1)
            count += 1
# # 1.拉取任务
# task = self._pull_task()
# if not task:
#     return
#
#         # 读取数据
#         logger.debug("---读取数据---")
#         task_id = str(task[TaskEnum.TASK_ID.value])
# payee_account = str(task[TaskEnum.PAYEE_BANK_CARD.value])
