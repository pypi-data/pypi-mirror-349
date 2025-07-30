#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import wda
from loguru import logger


class UsbDriver(object):

    def __init__(self, uuid):
        self.uuid = uuid

    def app_usb(self):
        driver = wda.USBClient()
        logger.info(f"启动 {self.uuid} app 成功.")
        return driver
