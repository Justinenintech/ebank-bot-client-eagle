# coding=utf-8
from peewee import PrimaryKeyField, TextField

from src.entity.base_model import BaseModel


class Uid(BaseModel):
    """
    uid 实体
    """
    id = PrimaryKeyField()
    token = TextField()
