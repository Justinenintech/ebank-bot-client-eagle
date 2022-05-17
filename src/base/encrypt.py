# coding=utf-8
import hashlib
import time


def md5_key(text):
    '''
    mdd5加密
    :param text:
    :return:
    '''
    hash = hashlib.md5()
    hash.update(text.encode("utf8"))
    return hash.hexdigest()


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
