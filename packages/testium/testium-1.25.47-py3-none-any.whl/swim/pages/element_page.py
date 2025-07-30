#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import random
from contextlib import suppress
from time import sleep

from appium.webdriver import WebElement
from loguru import logger
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from swim.pages.object_page import ObjectPage

case_down = False


class Element(object):

    def __init__(self, swim: ObjectPage, expression, dec, page_load_timeout=60, count=1):
        self.swim = swim
        self.driver = swim.driver
        self.page_load_timeout = page_load_timeout
        self.expression = expression
        self.count = count
        self.dec = dec
        self.by, self.value = expression
        self.desc = self.dec if self.dec else self.value

    def find_element(self, timeout=3, poll_frequency=0.5) -> WebElement:
        by, value = self.expression
        global case_down
        if not case_down:
            self.swim.screenshot_info()
        # logger.info(f"元素的描述是:{self.dec}")
        WebDriverWait(self.driver, timeout, poll_frequency).until(
            lambda x: x.find_elements(by=by, value=value))
        element = self.driver.find_element(by=by, value=value)
        element.locator = self.expression
        return element

    def find_elements(self, timeout=3, poll_frequency=0.5):
        """
        查找多个元素
        :param context: 上下文
        :return:
        """
        global case_down
        by, value = self.expression
        if not case_down:
            self.swim.screenshot_info()
        # logger.info(f"元素的描述是:{self.dec}")
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_elements(by=by, value=value))
        except Exception as e:
            pass
        elements = self.driver.find_elements(by=by, value=value)
        for element in elements:
            element.locator = self.expression
        return elements

    def click(self):
        """
        点击
        :return:
        """
        self.swim.click(self.find_element())
        sleep(1)
        logger.info(f"点击 {self.desc} 元素")

    def random_click(self, index=None):
        """
        随机点击元素或根据索引点击元素
        :param index: 元素索引，如果传入则点击对应索引的元素，否则随机点击
        :return: None
        """
        try:
            elements = self._get_valid_elements("随机点击")  # 优化：复用元素检查逻辑

            # 根据 index 判断是否随机选择或者按索引选择
            if index is not None:
                self._validate_index(index, len(elements))  # 验证索引范围
                target_element = elements[index]
                logger.info(f"根据索引点击元素: 描述={self.desc}, 索引={index}")
            else:
                target_element = random.choice(elements)
                logger.info(f"随机点击元素: 描述={self.desc}, 元素={target_element}")

            # 执行点击操作
            self._perform_click(target_element)

        except Exception as e:
            logger.exception(f"随机点击操作失败: {e}")
            raise

    def _get_valid_elements(self, operation_name):
        """
        检查并获取有效的元素列表
        """
        elements = self.find_elements()

        if not elements:
            logger.error(f"{operation_name}失败: 未找到任何可操作的元素，描述: {self.desc}")
            raise ValueError(f"No elements available for '{operation_name}', desc: {self.desc}")

        return elements

    def _validate_index(self, index, total_elements):
        """
        验证索引是否在范围内
        :param index: 索引值
        :param total_elements: 总元素数量
        :return: None
        """
        if not (0 <= index < total_elements):
            logger.error(f"索引超出范围: 索引={index}, 总元素数量={total_elements}")
            raise IndexError(f"Index {index} is out of range for total elements ({total_elements}).")

    def _perform_click(self, element):
        """
        执行点击操作
        """
        self.swim.click(element)
        sleep(2)  # 模拟点击后延迟操作，便于观察变化
        logger.info(f"元素点击成功: 描述={self.desc}, 元素={element}")

    def click_count(self, count):
        """
        点击指定索引的元素
        :param count: 元素索引，从 0 开始
        :return: None
        """
        try:
            elements = self.find_elements()  # 获取可操作的元素列表

            # 检查元素是否为空
            if not elements:
                logger.error(f"点击失败: 未找到任何可点击的元素，描述: {self.desc}")
                raise ValueError(f"No elements found to perform click for {self.desc}")

            # 验证索引是否有效
            if not (0 <= count < len(elements)):
                logger.error(f"无效索引: 索引={count}, 元素数量={len(elements)}, 描述: {self.desc}")
                raise IndexError(f"Index {count} is out of range for elements ({len(elements)} available).")

            # 执行点击操作
            self.swim.click(elements[count])
            logger.info(f"点击元素成功: {self.desc}, 点击的索引为 {count}")

        except ValueError as ve:
            logger.exception(f"点击操作失败 - 元素列表为空: {ve}")
            raise

        except IndexError as ie:
            logger.exception(f"点击操作失败 - 索引错误: {ie}")
            raise

        except Exception as e:
            logger.exception(f"点击操作失败 - 未确认的异常: {e}")
            raise

    def send_keys(self, values):
        """
        向输入框发送值
        :param values: 输入的值
        :return: None
        """
        try:
            # 检查输入值是否为 None 或空字符串
            if values is None or values == "":
                logger.warning(f"输入操作被跳过: 提供的输入值为空！描述: {self.desc}")
                return

            # 获取输入框元素
            element = self.find_element()

            if not element:
                logger.error(f"输入操作失败: 未找到输入框元素，描述: {self.desc}")
                raise ValueError(f"No input field found for '{self.desc}'")

            # 发送输入值
            self.swim.send_keys(element, values)
            logger.info(f"输入框输入完成: 描述={self.desc}, 输入值={values}")

        except Exception as e:
            logger.exception(f"输入操作失败 - 未确认的异常: {e}")
            raise

    def is_element(self, timeout=3, poll_frequency=0.5):
        """
        元素是否存在
        :return:
        """
        e = self.find_elements(timeout, poll_frequency) == []
        if e:
            logger.info(f"{self.desc} 元素不存在")
            return False
        else:
            # logger.info(f"该元素存在{self.find_elements()}")
            logger.info(f"{self.desc} 元素存在")
            return True

    def get_attribute(self, values):
        """
        获取元素属性
        :param values:
        :return:
        """
        attribute = self.swim.get_ele_attribute(self.find_element(), values)
        logger.info(f"获取到 {self.desc} 元素的 {values} 属性值: {attribute}")
        return attribute

    def tap_element(self, x=0, y=0):
        """
        按压元素
        :return:
        """
        logger.info(f"按压元素 {self.desc} 元素，偏移量 x: {x} y: {y}")
        return self.swim.tap(self.find_element(), x, y)

    def tap_element_count(self, count=0, x=0, y=0):
        """
        按压特定某个元素
        :return:
        """
        elements = self.find_elements()
        logger.info(f"按压元素 {self.desc} 元素，偏移量 x: {x} y: {y}")
        return self.swim.tap(elements[count], x, y)

    def old_tap_element(self, x=0, y=0):
        """
        按压元素
        :return:
        """
        logger.info(f"按压元素 {self.desc} 元素，偏移量 x: {x} y: {y}")
        return self.swim.old_tap(self.find_element(), x, y)

    def random_tap(self, x=0, y=0):
        """
        随机按压
        :return:
        """
        elements = self.find_elements()
        element = random.choice(elements)
        self.swim.tap(element, x, y)
        # sleep(2)
        logger.info(f"随机按压元素 {self.desc} 元素")

    def is_visibility_element(self):
        """
        判断元素是否可见
        :return:
        """

        with suppress(StaleElementReferenceException):
            if len(self.find_elements()) > 0:
                for element in self.find_elements():
                    if self.swim.is_visible_displayed(element):
                        logger.info(f"{self.desc} 元素可见")
                        return True
                    else:
                        logger.info(f"{self.desc} 元素不可见")
                        return False
            else:
                logger.info(f"{self.desc} 元素不可见")
                return False

    def is_visible_keyboard_element(self):
        """
        判断元素是否被键盘挡住
        :return:
        """

        with suppress(StaleElementReferenceException):
            for element in self.find_elements():
                if self.swim.is_visible_keyboard(element):
                    return True
                else:
                    return False

    def get_visibility_elements(self):
        """
        获取所有可见元素
        :return:
        """

        with suppress(StaleElementReferenceException):
            return [
                element for element in self.find_elements()
                if self.swim.is_visible_displayed(element)
            ]

    def get_size(self):
        """
        获取elements长度
        :return:
        """
        elements = self.find_elements()
        length = len(elements)
        logger.info(f"获取到的元素长度: {length} ")
        return length

    def element_long_press(self, duration=2000):
        """
        长按
        :param element:长按元素
        :param duration:长按时长
        :return:
        """
        self.swim.long_press(element=self.find_element(), duration=duration)
        sleep(1)
        logger.info(f"长按 {self.desc} 元素")

    def click_coordinate_center(self):
        """点击元素坐标中心"""
        coordinate = self.find_element().rect
        x = coordinate["x"]
        y = coordinate["y"]
        width = coordinate["width"]
        height = coordinate["height"]
        self.swim.touch_tap(x + width / 2, y + height / 2)
        sleep(1)
        logger.info(f"点击 {self.desc} 元素中心坐标")

    def click_payment_method(self, site):
        """点击支付方式"""
        if site in ["SA", "QA", "AE", "KW", "OM", "BH", "IL"]:
            x = 390
        else:
            x = 25
        coordinate = self.find_element().rect
        y = coordinate["y"]
        height = coordinate["height"]
        self.swim.touch_tap(x=x, y=y + height / 2)
        sleep(1)
