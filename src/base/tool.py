# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tool.py
# Time       ：2022/3/5 11:19 AM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import base64
import os
import re
import socket
import uuid
from urllib.request import urlretrieve
import yaml

from os.path import dirname, abspath

from PIL import Image, ImageChops

from setttings import EBANK_CODE


class Tool(object):

    def get_yaml(self):
        """
        从data.yaml文件获取数据
        :return:
        """
        test_data_file = os.path.abspath(EBANK_CODE)
        file = open(test_data_file, 'r', encoding='utf-8')
        data_yaml = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return data_yaml

    def get_bank_code_params(self, transfer_code: str, payee_code: str) -> str:
        """
        从yaml文件中读取，根据转账人银行编码，获取收款人银行编码（简称）
        :param transfer_code:
        :param payee_code:
        :return:
        """
        # 将接收到的驱动启动银行编码，转化为大写，再去yaml文件中读取
        # print('transfer_code.upper()', transfer_code.upper())
        _yaml = self.get_yaml()
        params = _yaml['ebank'].get(transfer_code.upper())  # 启动APP的包名
        res = params.get(payee_code.upper())
        return res

    def get_host_ip(self):
        """
        获取内网ip地址
        :return: 192.168.254.102
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def add_file_directory(self, directory) -> str:
        """
        如果不存在日志文件目录，则创建日志文件目录
        :return:
        """
        # project_path = os.getcwd()
        project_path = dirname(dirname(abspath(__file__)))
        file_path = os.path.join(project_path, directory)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        return file_path

    def compare_images(self, path_one, path_two, img_url):
        """
        比较图片是否一致
        :return:
        """
        urlretrieve(img_url, path_two)
        img_one = Image.open(path_one)
        img_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(img_one, img_two)
            if diff.getbbox() is None:
                os.remove(path_two)
                return True
            else:
                os.remove(path_two)
                return False
        except ValueError as e:
            os.remove(path_two)
            return "{0}\n{1}".format(e, "图片大小和对应的宽度不一致！")

    def img_to_base64(self, img_path):
        """
        图片验证码，转换为base64
        :param img_path: 图片保存地址
        :return: str base64
        """
        ext = img_path.split(".")[-1]
        with open(img_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        # base64_data = "data:image/png;base64,"+str(data)
        base64_data = "data:image/{ext};base64,{data}".format(ext=ext, data=data)
        # print(base64_data)
        return base64_data

    def decode_image(self, src):
        """
        解码图片
        :param src:  图片编码 eg: src="data:image/gif;base64,
        :return:  str 保存到本地的文件名
        """
        # 1、信息提取
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")

        else:
            raise Exception("Do not parse!")

        # 2、base64解码
        img = base64.urlsafe_b64decode(data)

        # 3、二进制文件保存
        filename = "{}.{}".format(uuid.uuid4(), ext)
        with open(filename, "wb") as f:
            f.write(img)

        return filename
