from src.base.enum.task_status_type import TaskStatusAndType
from src.base.log4py import logger
from src.dao.task_dao import TaskDao
from src.thread.task_notify_thread import TaskNotifyThread


class TaskCallbackJob:
    """
    回调数据服务
    """

    def __init__(self):
        self.task_dao = TaskDao()

    def run(self):
        """
        任务回调
        """
        try:
            task_list = self.task_dao.list(TaskStatusAndType.Success.value)
            if task_list.__len__() <= 0:
                logger.debug("没有任务需要回调")
                return

            # for task in task_list:
            #     withdraw_result = WithdrawResult(status=task.status, summary=task.summary)
            #     TaskNotifyThread(str(task.id), withdraw_result).start()

        except Exception as e:
            logger.error(e)
