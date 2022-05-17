# coding=utf-8
from peewee import Model, SqliteDatabase

from setttings import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    """
    基础 实体类基础
    """

    class Meta:
        database = db
