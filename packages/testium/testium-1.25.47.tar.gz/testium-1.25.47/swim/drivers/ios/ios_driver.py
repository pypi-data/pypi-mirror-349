#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from appium import webdriver
from appium.options.ios import XCUITestOptions
from loguru import logger


class IOSDriver(object):

    def __init__(self, name="zzkko.com.ZZKKO"):
        """
        初始化
        :param name: 浏览器类型
        """
        self.name = name

    def app_remote(self, language='en', host='', port='', uuid='', wdaPort='', deviceName='',
                   deviceVersion='', platform='', bundleId='', event_tracking=None):
        """
        移动端
        :param bundleId:
        :param wdaPort:
        :param language:
        :param uuid: 设备id
        :param host: Appium-ip
        :param port: Appium-端口
        :param extendPort: iOS端口
        :param deviceName: 设备名称
        :param deviceVersion: 设备系统
        :param platform: 执行平台
        :return: 驱动
        """
        options = XCUITestOptions()
        options.process_arguments = event_tracking  # ios为json格式 {"env": {"auto_test_args": "商详分组$_session值"}}
        options.platformVersion = deviceVersion
        options.bundle_id = bundleId
        options.udid = uuid
        options.device_name = deviceName
        options.language = language
        options.wda_local_port = wdaPort
        options.new_command_timeout = 600
        # options.extendPort = extendPort
        # options.platform_name = "ios"
        # options.automation_name = "XCuiTest"
        # options.xcode_org_id = "QYF3Z86UT8"
        # options.xcode_signing_id = "iPhone Developer"
        # options.use_new_wda = True
        options.no_reset = False
        # options.use_prebuilt_wda = False
        # options.use_xctestrun_file = False
        # options.skip_log_capture = True
        # options = {
        #     "platformName": "ios",
        #     "applicationName": "Appium",
        #     "automationName": "XCuiTest",
        #     "bundleId": bundleId,
        #     "deviceName": "iOS",
        #     "platformVersion": deviceVersion,
        #     "udid": uuid,
        #     "noReset": False,
        #     "wdaLocalPort": wdaPort,
        #     "language": language,
        #     "newCommandTimeout": 600,
        #     # "locale": "en_US"
        #     "useNewWDA": False,
        #     "xcodeOrgId": "QYF3Z86UT8",
        #     "xcodeSigningId": "iPhone Developer",
        #     "usePrebuiltWDA": False,
        #     "useXctestrunFile": False,
        #     "skipLogCapture": True
        #
        # }
        logger.info(f"启动 {bundleId} ,地址是:{host}:{port} app")
        # driver = webdriver.Remote(f"http://{host}:{port}", desired_capabilities=options)
        driver = webdriver.Remote(f"http://{host}:{port}", options=options)
        logger.info(f"启动 {bundleId} ,地址是:{host}:{port} app 成功.")
        return driver

    def reset_ios_driver(self, uuid, language, host, port, wda_port, device_name, device_version, brand="wrc", event_tracking=None):
        """
        ios重启
        :return:
        """

        if brand == "ROMWE":
            bundle_id = "com.romwe.dotfashion"
        elif brand == "wrc":
            bundle_id = "zzkko.com.ZZKKO"
        else:
            bundle_id = brand
        driver = self.app_remote(uuid=uuid, language=language, host=host, port=port, wdaPort=wda_port,
                                 deviceName=device_name,
                                 deviceVersion=device_version, bundleId=bundle_id,event_tracking=event_tracking)
        return driver
