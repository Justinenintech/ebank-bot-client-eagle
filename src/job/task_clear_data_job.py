import time

from src.base.log4py import logger
from src.dao.task_dao import TaskDao


class TaskClearDataJob:
    """
    清理數據服務
    """

    def __init__(self):
        self.task_dao = TaskDao()

    def run(self):
        """
        清理數據
        """
        try:
            logger.info('%s', '每 1h 清理一天的数据')
            last_date_time = time.time() - 24 * 3600
            self.task_dao.delete(last_date_time)
        except Exception as e:
            logger.error(e)
