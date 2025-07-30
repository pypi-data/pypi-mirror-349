#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import random

from loguru import logger
from selenium import webdriver
from selenium.webdriver.safari.options import Options
ip_list = ["10.102.14.28:8899", "10.102.14.27:8899"]  # 28:资产编号630, 27:资产编号571
ip_list_us = ["10.102.14.28:8999", "10.102.14.27:8999"]
ip_proxy = random.choice(ip_list)
ip_proxy_us = random.choice(ip_list_us)

def get_proxy(envTag, site, options):
    """
    获取代理
    :param envTag:  环境
    :param site:  站点
    :param options: 浏览器参数
    :return: 浏览器参数
    """

    if envTag == "gray":
        if site in ["US", "US_ES"]:
            proxy = ip_proxy_us
        else:
            proxy = ip_proxy
        options.add_argument("--proxy-server=%s" % proxy)
        logger.info("走代理请求:" + proxy + "环境变量:" + envTag)
    return options


def browser_edge(envTag, site):
    """
    edge浏览器
    :param envTag: 环境
    :param site: 站点
    :return: 代理
    """

    options = webdriver.EdgeOptions()
    options.add_argument("browserName=MicrosoftEdge")
    return get_proxy(envTag, site, options)


def browser_chrome(envTag, site):
    """
    chrome浏览器
    :param envTag: 环境
    :param site: 站点
    :return: 代理
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return get_proxy(envTag, site, options)


def browser_firefox(envTag, site):
    """
    firefox浏览器
    :param envTag: 环境
    :param site: 站点
    :return: 代理
    """
    options = webdriver.FirefoxOptions()
    return get_proxy(envTag, site, options)


def browser_safari(envTag, site):
    """
    safari浏览器
    :param envTag: 环境
    :param site: 站点
    :return: 代理
    """
    options = Options()
    options.add_argument("browserName=safari")
    options.add_argument("platformName=mac")
    return get_proxy(envTag, site, options)


def browser_ie(envTag, site):
    """
    ie浏览器
    :param envTag: 环境
    :param site: 站点
    :return: 代理
    """
    options = webdriver.IeOptions()
    options.add_argument("browserName=internet explorer")
    options.add_argument("platformName=windows")
    return get_proxy(envTag, site, options)


class BrowserDriver(object):
    """
    驱动-桌面端
    """

    def __init__(self, name="Chrome"):
        self.name = name

    def select_browser(self, command_executor, envTag, site):
        """
        选择浏览器
        :param command_executor: 参数
        :param envTag: 环境
        :param site: 站点
        :return: 驱动
        """

        browser_type = self.name
        if browser_type == "chrome":
            options = browser_chrome(envTag, site)
        elif browser_type == "firefox":
            options = browser_firefox(envTag, site)
        elif browser_type == "safari":
            options = browser_safari(envTag, site)
        elif browser_type == "ie":
            options = browser_ie(envTag, site)
        elif browser_type == "edge":
            options = browser_edge(envTag, site)
        else:
            raise NameError(f"请输入正确的浏览器名称。 选项有：Chrome、Firefox、Safari")
        driver = webdriver.Remote(
            command_executor=command_executor,
            options=options,
        )
        logger.info(f"启动服务:{command_executor}, 浏览器是:{browser_type}.")
        return driver

    def web_remote(self, hub="127.0.0.1:4444", envTag="online", site="site", *args, **kwargs):
        """
        桌面驱动
        :param hub: ip端口
        :param envTag: 环境
        :param site: 站点
        :param args: 参数
        :param kwargs: 个数
        :return:
        """
        command_executor = f"{hub}/wd/hub"
        driver = self.select_browser(command_executor, envTag, site)
        driver.maximize_window()
        return driver
