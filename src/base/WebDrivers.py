# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : WebDrivers.py
# Time       ：2022/3/23 3:42 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""

try:

    import sys
    import os

    from fp.fp import FreeProxy
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from setttings import BROWSER_PATH, STEALTH
    from fake_useragent import UserAgent
    from selenium.webdriver import Chrome
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.chrome.service import Service
    import time

    print('all module are loaded ')

except Exception as e:

    print("Error ->>>: {} ".format(e))


class DriverOptions(object):

    def __init__(self):
        self.options = Options()
        prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
        self.options.add_experimental_option('prefs', prefs)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--incognito")
        self.options.add_argument('--disable-gpu')
        # self.options.add_argument('--disk-cache-dir=./cache')
        # self.options.add_argument('--user-data-dir=./userdata')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("--disable-infobars")

        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36")


class WebDrivers(DriverOptions):

    def __init__(self):
        DriverOptions.__init__(self)
        self.driver_instance = self.init_driver()

    def init_driver(self):
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        ser = Service(BROWSER_PATH)
        driver = webdriver.Chrome(service=ser, options=self.options)
        with open(STEALTH) as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
        return driver
