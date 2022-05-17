# coding=utf-8
from src.base.log4py import logger
from src.base.singleton import Singleton
from src.entity.uid import Uid


class UidDao(Singleton):
    """
    uid dao层
    """

    def get_id(self) -> Uid:
        """
        查询id
        :return: Uid
        """
        try:
            uid = Uid.get()
            return uid
        except Exception as e:
            logger.error(e)
            return None

    def insert(self, id, token) -> None:
        """
        插入一条id
        :param id: id
        """
        Uid.create(id=id, token=token)

    def update(self, id) -> None:
        """
        更新下id
        :param id: id
        """
        try:
            Uid.update(id=id).execute()
        except Exception as e:
            logger.error(e)

    def updateToken(self, token) -> None:
        """
        更新 token
        :param token: 會話
        """
        try:
            Uid.update(token=token).execute()
        except Exception as e:
            logger.error(e)

    def delete(self) -> None:
        """
        删除uid
        """
        Uid.delete().execute()
