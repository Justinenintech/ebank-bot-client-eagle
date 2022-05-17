# coding=utf-8
import base64
import os
import random
from urllib import request

from src.base.log4py import logger

"""
图片下载
下载完成后，返回绝对路径
"""


def download_img(img_url, download_path, api_token="") -> str:
    logger.info("download_path: %s", download_path)
    # 设置http header
    header = {"Authorization": "Bearer " + api_token}

    # 检查要下载的目标目录是否存在
    isExist = os.path.exists(download_path)
    if not isExist:
        os.makedirs(download_path)
        logger.info("已自动创建目录：%s", download_path)
    else:
        logger.info("目标目录已存在")

    req = request.Request(img_url, headers=header)
    try:
        response = request.urlopen(req)
        img_name = "%s.png" % (random.randint(100000, 999999))
        logger.info("图片：%s", img_name)
        filename = download_path + img_name
        logger.info("下载图片返回状态码：name: %s, code: %s", filename, response.getcode())
        if response.getcode() == 200:
            with open(filename, "wb") as f:
                # 将内容写入图片
                f.write(response.read())
                logger.debug("图片下载完成")
            return filename
    except:
        return "failed"


"""
读取图片，并返回Base64格式
"""


def readFile2Base64(filePath) -> str:
    # 二进制方式打开文件
    f = open(filePath, 'rb')
    # 读取文件内容，转换为base64编码
    ls_f = base64.b64encode(f.read())
    f.close()
    return ls_f.decode('utf-8')


if __name__ == '__main__':
    img_url = "https://ebank.msb.com.vn/IBSRetail/servlet/ImageServlet"
    img_path = download_img(img_url,
                            "D:\\Documents\\IdeaProjects\\borong205@gmail.com\\vietnam-bot-client\\download\\msbbank\\")
    ls_f = readFile2Base64(img_path)
    base64 = "data:image/png;base64,%s" % (ls_f)
    logger.info("下载好的图片地址：%s, base64: %s", img_path, base64)
    # 读取到base64后删除原文件
    os.remove(img_path)
