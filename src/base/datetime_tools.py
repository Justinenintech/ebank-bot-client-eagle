# coding=utf-8
import time


def HH():
    return time.strftime("%H", time.localtime())


def HH_MM_SS():
    return time.strftime("%H:%M:%S", time.localtime())


def YYYY_mm_dd_HH_MM_SS():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def YYYY_MM_DD():
    return time.strftime("%Y-%m-%d", time.localtime())
