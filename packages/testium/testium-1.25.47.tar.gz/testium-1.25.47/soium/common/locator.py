#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy



class Locator(object):
    """
    定位类型
    """

    @staticmethod
    def ID(value):
        return By.ID, value

    @staticmethod
    def CSS(value):
        return By.CSS_SELECTOR, value

    @staticmethod
    def XPATH(value):
        return By.XPATH, value

    @staticmethod
    def NAME(value):
        return By.NAME, value

    @staticmethod
    def TAG_NAME(value):
        return By.TAG_NAME, value

    @staticmethod
    def CLASS_NAME(value):
        return By.CLASS_NAME, value

    @staticmethod
    def LINK_TEXT(value):
        return By.LINK_TEXT, value

    @staticmethod
    def PARTIAL_LINK_TEXT(value):
        return By.PARTIAL_LINK_TEXT, value

    @staticmethod
    def IOS_CLASS_CHAIN(value):
        return AppiumBy.IOS_CLASS_CHAIN, value
