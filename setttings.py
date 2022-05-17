# coding=utf-8
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

sys_conf = os.path.join(_basedir, 'sys.conf')
# 日誌配置
LOGGIN_CONF = os.path.join(_basedir, 'logging.conf')

# 数据库配置
DATABASE_PATH = os.path.join(_basedir, 'data.db')

# 浏览器驱动
BROWSER_PATH = os.path.join(_basedir, 'chromedriver')

# stealth
STEALTH = os.path.join(_basedir, 'stealth.min.js')

# 每个银行内部其他银行的银行编码
EBANK_CODE = os.path.join(_basedir, 'ebank_code.yaml')

# sentry 的秘鑰配置
SENTRY_DSN = "http://ec1002d7de324eaa9e9b509faf30f146@35.186.158.193/9"

# 用于MB银行校验是否成功支付
MB_ASSERT_PAY_ONE = os.path.join(_basedir, 'src/images/mb/assert',
                                 'success.png')
MB_ASSERT_PAY_TWO = os.path.join(_basedir, 'src/images/mb/assert',
                                 'down_success.png')
MB_PAY_FAILURE = os.path.join(_basedir, 'src/images/mb/pay_failure')
MB_PAY_SUCCESS = os.path.join(_basedir, 'src/images/mb/pay_success')

# VIB
VIB_PAY_FAILURE = os.path.join(_basedir, 'src/images/vib/pay_failure')
VIB_PAY_SUCCESS = os.path.join(_basedir, 'src/images/vib/pay_success')
# BIDV
BIDV_CAPTCHA_PNG = os.path.join(_basedir, 'src/images/bidv/assert', 'captcha.png')
BIDV_CAPTCHA = os.path.join(_basedir, 'src/images/bidv/assert')
BIDV_PAY_FAILURE = os.path.join(_basedir, 'src/images/bidv/pay_failure')
BIDV_PAY_SUCCESS = os.path.join(_basedir, 'src/images/bidv/pay_success')
print(BIDV_CAPTCHA)
del os
