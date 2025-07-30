#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from appium import webdriver
from loguru import logger
from appium.options.android import UiAutomator2Options


class AndroidDriver(object):

    def __init__(self, name="com.zzkko"):
        """
        初始化
        :param name: 浏览器类型
        """
        self.name = name

    def app_remote(self, language='en', host='', port='', uuid='', wdaPort='', extendPort='', deviceName='',
                   deviceVersion='', platform='', country='', appPackage='', appActivity='', event_tracking=None):
        """
        移动端
        :param country:
        :param udid: 设备id
        :param host: Appium-ip
        :param port: Appium-端口
        :param extendPort: iOS端口
        :param deviceName: 设备名称
        :param deviceVersion: 设备系统
        :param platform: 执行平台
        :return: 驱动
        """
        # country = self.country_change(country)
        options = UiAutomator2Options()
        options.optional_intent_arguments = event_tracking  # Android为字符串拼接 "--es env {\"auto_test_args\":[\"商详-商详分组\"]\\,\"session\":\"session值\"}"
        options.platform_name = "Android"
        options.app_package = appPackage
        options.device_name = deviceName
        options.platformVersion = deviceVersion
        options.no_reset = True
        options.udid = uuid
        options.automation_name = "UIAutomator2"
        options.app_activity = appActivity
        if appPackage == "com.romwe":
            language = self.language_change(language, country)
            options.language = language
            options.locale = country
        if country == "AT":
            options.language = language
            options.locale = country
        options.skip_server_installation = False
        options.new_command_timeout = 600
        options.auto_grant_permissions = True

        # options = {
        #     "platformName": "Android",
        #     "appName": "wrc",
        #     "noReset": False,
        #     # "udid": uuid,
        #     "appPackage": 'com.zzkko',
        #     "automationName": "UIAutomator2",
        #     'appActivity': 'com.wrc.welcome.WelcomeActivity',
        #     "platformVersion": deviceVersion,
        #     "language": language,
        #     "locale": country,
        #     # "unicodeKeyboard": True,
        #     # "resetKeyboard": True,
        #     # "autoGrantPermissions": True,
        #     "skipServerInstallation": False,
        #     "newCommandTimeout": 600
        #
        # }
        driver = webdriver.Remote(f"http://{host}:{port}", options=options)
        logger.info(f"启动 {appPackage} app 成功.")
        return driver

    def language_change(self, language, country):
        if language == "es-mx": language = "es"
        return language
    #
    # def country_change(self, country):
    #     if country == "UK": country = "GB"
    #     return country
