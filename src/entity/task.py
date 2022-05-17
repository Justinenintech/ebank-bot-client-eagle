# coding=utf-8
from peewee import PrimaryKeyField, IntegerField, CharField

from src.entity.base_model import BaseModel


class Task(BaseModel):
    """
    Task 实体,用于缓存数据
    """
    id = PrimaryKeyField()
    status = CharField()
    create_time = IntegerField()
    summary = CharField()

