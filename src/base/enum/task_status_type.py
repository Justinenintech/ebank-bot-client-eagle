# coding=utf-8
from enum import Enum


class TaskStatusAndType(Enum):
    """
    任務狀態,類型
    """
    App = "App"
    Web = "Web"
    Bot_Doing = "Bot_Doing"
    Bot_Done = "Bot_Done"
    Failure = "Failure"
