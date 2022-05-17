import threading

from src.base.log4py import logger
from src.service.base_service import BaseService


class TaskNotifyThread(threading.Thread):
    """
    通知结果异步化
    """

    def __init__(self, task_id, data):
        threading.Thread.__init__(self)
        self.task_id = task_id
        self.data = data
        self.base_service = BaseService()

    def run(self):
        """
        多线程任务执行
        """
        logger.info("--- 开始异步通知代付结果-%s ---", self.task_id)
        self.base_service._done_task(task_id=self.task_id, data=self.data)
        logger.info("--- 完成异步通知代付结果-%s ---", self.task_id)
