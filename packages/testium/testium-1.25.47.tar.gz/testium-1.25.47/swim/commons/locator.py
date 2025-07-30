#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


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

    @staticmethod
    def IOS_PREDICATE(value):
        return AppiumBy.IOS_PREDICATE, value

    @staticmethod
    def ANDROID_UIAUTOMATOR(value):
        return AppiumBy.ANDROID_UIAUTOMATOR, value

    @staticmethod
    def ANDROID_VIEWTAG(value):
        return AppiumBy.ANDROID_VIEWTAG, value

    @staticmethod
    def ANDROID_DATA_MATCHER(value):
        return AppiumBy.ANDROID_DATA_MATCHER, value

    @staticmethod
    def ANDROID_VIEW_MATCHER(value):
        return AppiumBy.ANDROID_VIEW_MATCHER, value

    @staticmethod
    def KEY(value):
        value = value.replace("'", "\'") if "'" in value else value
        return By.XPATH, f"//*[@text='{value}'] | //*[@content-desc='{value}']"

    @staticmethod
    def CONTAINS_KEY(value):
        value = value.replace("'", "\'") if "'" in value else value
        return By.XPATH, f"//*[contains(@text,'{value}')] | //*[contains(@content-desc,'{value}')]"

    @staticmethod
    def Image(value):
        return AppiumBy.IMAGE, value

    @staticmethod
    def JS_ID(value):
        return f'return document.getElementById("{value}")'

    @staticmethod
    def JS_CSS(value):
        return f'return document.querySelector("{value}")'

    @staticmethod
    def RT_JS_XPATH(value):
        return f'return document.evaluate("{value}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'

    @staticmethod
    def JS_XPATH(value):
        return f'document.evaluate("{value}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'

    @staticmethod
    def JS_CLASS(value):
        return f'return document.getElementsByClassName("{value}")'

    @staticmethod
    def JS_NAME(value):
        return f'return document.getElementsByTagName("{value}")'
