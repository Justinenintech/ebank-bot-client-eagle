# coding=utf-8
from src.base.log4py import logger
from src.base.singleton import Singleton
from src.entity.task import Task


class TaskDao(Singleton):
    """
    Task dao层
    """

    def get(self, id) -> Task:
        """
        查询id
        :return: Uid
        """
        try:
            task = Task.get(Task.id == id)
            return task
        except Exception as e:
            logger.error(e)
            return None

    def insert(self, id, status, create_time) -> None:
        """
        插入一条id
        :param id: id
        :param status: 状态
        :param create_time: 创建时间
        """
        Task.create(id=id, status=status, create_time=create_time)

    def update(self, id, status, summary=None):
        """
        更新状态
        :param id: 任务id
        :param status: 状态
        """
        try:
            Task.update(status=status, summary=summary).where(Task.id == id).execute()
        except Exception as e:
            logger.error(e)

    def delete(self, create_time) -> None:
        """
        删除任务
        :param create_time: 创建时间
        """
        Task.delete().where(Task.create_time <= create_time).execute()

    def list(self, status) -> list:
        """
        查询任务集合
        :param status: 状态
        :return: 任务集合
        """
        task_list = Task.select().where(Task.status == status)
        return task_list
