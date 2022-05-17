# coding=utf-8
# import logging.config

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from src.base.config import Config
from src.base.tool import Tool
from src.service.register_heartbeat_service import RegisterAndHeartbeatService
from src.service.task_service import TaskService

if __name__ == '__main__':
    # log = logging.getLogger(__name__)
    t = Tool()
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # logging.getLogger('apscheduler.executors.default').propagate = False

    try:
        cfg = Config()
        # ip = cfg.read("sys", "ip")
        ip = t.get_host_ip()
        serial = cfg.read("sys", "serial")
        code = cfg.read("sys", "code")
        service_type = cfg.read("sys", "service_type")
        heartbeat_time = cfg.read("sys", "heartbeat_time")
        frequency_time = cfg.read("sys", "frequency_time")

        # 注册,心跳服务
        logger.info('>>>>> Starting register heartbeat server <<<<<')
        register_heartbeat_service = RegisterAndHeartbeatService(ip=ip, serial=serial, code=code,
                                                                 service_type=service_type)
        scheduler.add_job(register_heartbeat_service.run, "interval", seconds=int(heartbeat_time))

        # 任务服务
        logger.info('>>>>> Starting task service <<<<<')
        scheduler.add_job(TaskService().run, "interval", seconds=int(frequency_time))

        logger.info('>>>>> Starting task callback job  server <<<<<')
        # scheduler.add_job(TaskCallbackJob().run, "interval", seconds=3)

        logger.info('>>>>> Starting task job  server <<<<<')
        # scheduler.add_job(TaskClearDataJob().run, "interval", seconds=10 * 3600)

        scheduler.start()
    except Exception as e:
        logger.exception(e)
