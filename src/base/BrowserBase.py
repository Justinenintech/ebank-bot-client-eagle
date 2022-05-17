# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : BrowserBase.py
# Time       ：2022/3/23 3:43 PM
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import random
import time

from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *  # 导入所有的异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.base.WebDrivers import WebDrivers


class BrowserBase(object):
    def __init__(self):
        self.driver = WebDrivers()
        self._driver_base = self.driver.driver_instance

    def find_element(self, selector, timeout=30):
        """
                Positioning element, parameter selector is element ancestor type
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'su')))
                判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0
                :param selector: selector = ("id","xxx"),driver.find_element(selector)
                :param timeout: 10
                :return:poll_frequency=2
                """
        try:
            # ignored_exceptions = (
            #     NoSuchElementException, StaleElementReferenceException,)ignored_exceptions=ignored_exceptions
            element = WebDriverWait(self._driver_base, timeout, poll_frequency=.5,).until(
                EC.presence_of_element_located(
                    selector))
            logger.info(
                'Successful positioning of elements.Positioning method and values used：{}',
                selector)
            return element
        except NoSuchElementException:
            logger.error(
                'Error positioning of elements,Positioning method and values used：{}', selector,
                exc_info=1)

    def find_elements(self, selector, timeout=30):
        """
        Locate a set of elements
        :param selector: selector = ("id","xxx"),driver.find_element(selector)
        :param timeout: 10
        :return:
        """
        try:
            elements = WebDriverWait(self._driver_base, timeout, .5).until(
                EC.presence_of_all_elements_located(selector))
            logger.info(
                'Successful positioning of elements.Positioning method and values used：%s' % selector)
            return elements
        except NoSuchElementException:
            logger.error(
                'Error positioning of elements,Positioning method and values used：%s' % selector,
                exc_info=1)

    def find_element_visibility_of_located(self, selector, timeout=30):
        """
        Positioning element, parameter selector is element ancestor type
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'su')))
        判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0
        :param selector: selector = ("id","xxx"),driver.find_element(selector)
        :param timeout: 10
        :return:poll_frequency=2
        """
        try:
            # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)ignored_exceptions=ignored_exceptions
            element = WebDriverWait(self._driver_base, timeout, poll_frequency=.5,).until(
                EC.visibility_of_element_located(
                    selector))  # visibility_of_element_located presence_of_element_located
            logger.info(
                'Successful positioning of elements.Positioning method and values used：{}',
                selector)
            return element
        except NoSuchElementException:
            logger.error(
                'Error positioning of elements,Positioning method and values used：{}', selector,
                exc_info=1)

    def open_url(self, url):
        """
        open URL
        :param url:
        :return:
        """
        self._driver_base.get(url)

    def maximize_window(self):
        """
        Maximize the current browser window
        :return:
        """
        self._driver_base.maximize_window()

    def dr_quit(self):
        """
        Exit driver
        :return:
        """
        self._driver_base.quit()

    def type(self, selector, value):
        """
        Enter content in the input box
        :param selector:
        :param value:
        :return:
        """
        element = self.find_element_visibility_of_located(selector)
        try:
            element.clear()
            self.forced_wait()
            element.send_keys(value)
            logger.info('Input content：{}', value)
        except Exception as e:
            logger.exception('Content input error：{}', e)
            # self.save_window_snapshot('Content input error')

    def get_text(self, selector, timeout=5):
        """
        Get element text information.
        :param selector:
        :param timeout:
        :return:

        Usage:
        driver.get_text("i,el")
        """
        _is_displayed = self.get_displayed(selector)
        if _is_displayed:
            el = self.find_element_visibility_of_located(selector, timeout)
            logger.info("Obtained text：{}", el.text)
            return el.text
        else:
            logger.info("text元素不可见!")

    def check_get_text(self, selector, text, timeout=10):
        """
        判断元素的text信息是否满足预期
        :param selector:
        :param text:
        :param timeout:
        :return: bool
        """
        element = WebDriverWait(self._driver_base, timeout, poll_frequency=1, ).until(
            EC.text_to_be_present_in_element(selector, text))
        logger.debug("element:{}", element)
        if element:
            return True
        else:
            return False

    def click(self, selector):
        """
        Click element
        :param selector:
        :return:
        """

        # noinspection PyBroadException
        element = WebDriverWait(self._driver_base, 10, poll_frequency=1, ).until(
            EC.element_to_be_clickable(selector))
        logger.debug("click element:{}", element)
        # element = self.find_element(selector)
        element.click()
        # try:
        #     # ActionChains(self.driver).click(element).perform()
        #     self.forced_wait()
        #     is_enabled = self.get_enabled(selector)
        #     isdisplay = self.get_displayed(selector)
        #     if is_enabled and isdisplay:
        #         element.click()
        #         logger.info(
        #             'Click on the element success,location method and value used：{}', selector)
        # except ElementClickInterceptedException:
        #     self.click(selector)

    def get_attribute(self, selector, attribute, timeout=5):
        """
         Gets the value of an element attribute.
        :param selector:
        :param attribute:
        :param timeout:
        :return:

        usage:
        driver.get_attribute("i,el","type")
        """
        # self.forced_wait()
        el = self.find_element(selector, timeout)
        return el.get_attribute(attribute)

    def get_enabled(self, selector, timeout=5):
        """
        Determine if the page element is clickable
        :param selector: 元素定位
        :param timeout: 秒
        :return: Boolean value
        """
        if self.find_element(selector, timeout).is_enabled():
            return True
        else:
            return False

    def get_displayed(self, selector):
        """
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("i,el")
        """
        el = self.find_element(selector)
        return el.is_displayed()

    @staticmethod
    def forced_wait():
        """
        Forced wait
        :return:
        """
        # seconds = [.5, .6, .7, .8, 1]
        seconds = [.8, .9, 1]
        second = random.sample(seconds, 1)
        time.sleep(second[0])
        logger.info('Forced wait {} second', second[0])

    @staticmethod
    def wait_time(seconds):
        """
        Forced wait
        :param seconds: 等待时间 秒
        :return:
        """
        time.sleep(seconds)
        logger.info('Forced wait %d second' % seconds)

    def close_browser(self):
        """
        Close the browser
        :return:
        """
        self._driver_base.close()

    def move_to_element(self, selector):
        """
        Mouse hover operation
        :param selector:
        :return:
        """
        element = self.find_element(selector)
        ActionChains(self._driver_base).move_to_element(element).perform()

    def get_text_list(self, selector):
        """
        Get multiple elements based on the selector, get the text list of the element
        :param selector:
        :return: list
        """
        el_list = self.find_element(selector)
        results = []
        for el in el_list:
            results.append(el.text)
        return results

    def count_elements(self, selector, elector):
        """
        Find the number of elements.
        :param selector: 定位符
        :param elector: 定位符 //a
        :return:
        """
        el = self.find_element(selector)
        els = el.find_elements(By.XPATH, elector)
        return len(els)

    def switch_to_default(self):
        """
        Switch to the specified frame
        :return:
        Usage:
        driver.switch_to_frame("i,el")
        """
        try:
            self._driver_base.switch_to.default_content()
            logger.info('Switch frame successfully')
        except BaseException:
            logger.error('Switch frame failed', exc_info=1)

    def switch_to_current_window(self):
        try:
            self._driver_base.current_window_handle()
            logger.info('Switch frame successfully')
        except BaseException:
            logger.error('Switch frame failed', exc_info=1)

    def save_window_snapshot(self, img_path, img_name):
        """
        save screen snapshot
        :param img_path: the image file path
        :param img_name: the image file name
        :return:
        """
        try:
            self._driver_base.get_screenshot_as_file('{}/{}.png'.format(img_path, img_name))
            logger.info('Screenshot saved successfully!')
        except BaseException as e:
            logger.error('Screenshot failed!', format(e), exc_info=1)

    def select_by_visible_text(self, selector, text):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self.find_elements(selector)
        Select(el).select_by_visible_text(text)

    def refresh(self, url=None):
        """
        refresh page
        If the url is null, the current page is refreshed, otherwise the specified page is refreshed.
        :param url: 默认值是空的
        :return:
        """
        if url is None:
            self._driver_base.refresh()
        else:
            self._driver_base.get(url)

    def js_focus_element(self, selector):
        """
        Focusing element
        :param selector:
        :return:
        """
        target = self.find_element(selector)
        self._driver_base.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """
        Scroll to the top
        :return:
        """
        js = "var q=document.documentElement.scrollTop=0"
        self._driver_base.execute_script(js)
        logger.info('JavaScript execution is successful，JavaScript content is：%s' % js)

    def js_scroll_end(self):
        """
        Scroll to the bottom
        :return:
        """
        js = "var q=document.documentElement.scrollTop=100000"
        self._driver_base.execute_script(js)
        logger.info('JavaScript execution is successful，JavaScript content is：%s' % js)
