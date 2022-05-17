import socket

from loguru import logger

from src.base import http_re
from src.base.config import Config
from src.base.enum.api_enum import Api
from src.base.enum.task_status_type import TaskStatusAndType
# from src.base.log4py import logger
from src.base.return_code import ResponseCode
from src.dao.uid_dao import UidDao


class RegisterAndHeartbeatService:
    """
    注册与心跳服务
    """

    def __init__(self, ip, serial, code, service_type):
        self.ip = ip
        self.serial = serial
        self.code = code
        self.service_type = service_type

        cfg = Config()
        self.host = cfg.read("sys", "server_host")
        self.heartbeat_time = cfg.read("sys", "heartbeat_time")

        self.uid_dao = UidDao()
        self.bot = self.__register()

    def run(self):
        """
        运行入口
        """
        try:
            self.__heartbeat()
        except Exception as e:
            logger.error(e)

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def __register(self) -> str:
        """
        设备注册上线
        将支付宝账号,ip,序列号发送给服务器进行注册,用于领取任务
        """
        logger.info("---注册设备---")
        try:
            uid = self.uid_dao.get_id()
            if uid:
                logger.warning("bot 已经注册 id为-{}", str(uid.id))
                data = {
                    "id": uid.id,
                    "code": self.code,
                    "ip": str(self.get_ip()),
                    "serviceType": str(self.service_type),
                    "serialNo": str(self.serial),
                    "type": TaskStatusAndType.Web.value
                }
            else:
                data = {
                    "code": self.code,
                    "ip": str(self.get_ip()),
                    "serviceType": str(self.service_type),
                    "serialNo": str(self.serial),
                    "type": TaskStatusAndType.Web.value
                }
            if uid:
                token = uid.token
            else:
                token = None

            beanret = http_re.post(self.host + Api.Register_Device_Url.value, token=token, data=data)
            if beanret.code.__eq__(ResponseCode.Success.value):
                result_data = beanret.data
                id = result_data["id"]
                token = beanret.token
                if not uid and id:
                    logger.info("bot 注册id-{},token-{}", str(id), token)
                    self.uid_dao.insert(id, token)
                if uid:
                    self.uid_dao.updateToken(token)

                if uid and not str(uid.id).__eq__(id):
                    self.uid_dao.delete()
                    self.uid_dao.insert(id, token)
                    return result_data


            else:
                return None
        except Exception as e:
            logger.error('{}', e)

    def __heartbeat(self):
        """
        心跳保持
        """

        logger.info("---存活心跳上报---")
        uid = self.uid_dao.get_id()
        if not uid:
            return
        url = self.host + Api.Heartbeat_Url.get_heartbeat_url(str(uid.id))
        beanret = http_re.put(url, token=str(uid.token))
        token = beanret.token
        logger.debug('最新token-{}', token)
        if token:
            self.uid_dao.updateToken(token)
        logger.info("---存活心跳上报完成---")
