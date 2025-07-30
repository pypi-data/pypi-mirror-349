import random
from appium import webdriver
from appium.options.common import AppiumOptions
from loguru import logger
from soium.support.proxy_config import ProxyConfig


class WebDriver(object):
    def __init__(self, name="Chrome"):
        self.name = name
        self.timeout = "60"

    def get_proxy(self, envTag, site):

        proxy = None
        if "gray" in envTag:
            proxy = ProxyConfig().get_site_proxy(site, envTag)
        return proxy


    def remote(self, udid, host="127.0.0.1", port="4723", extendPort='', deviceName='', deviceVersion='',
               platform='Android', envTag='release', site=''):
        desired_caps = {
            "browserName": self.name,
            "platformName": platform,
            "appium:udid": udid,
            "appium:noReset": True,
            "appium:newCommandTimeout": 3000,
            "appium:hideKeyboard": True,
            "resetKeyboard": True,
            "appium:autoGrantPermissions": True,
            "appium:skipServerInstallation": False,
            # "appium:systemPort": port
        }
        if platform.lower() == 'ios':
            desired_caps.setdefault('appium:automationName', 'XCUITest')
            desired_caps.setdefault('wdaLocalPort', extendPort)
            desired_caps.update({"browserName": "safari"})
        else:
            desired_caps.setdefault('appium:automationName', "UiAutomator2")
        proxy = self.get_proxy(envTag=envTag, site=site)
        if proxy:
            desired_caps.update(
                {"appium:chromeOptions": {"args": [f"--proxy-server={proxy}", "--disable-notifications"]}}
            )
        driver=webdriver.Remote(f"http://{host}:{port}", options=AppiumOptions().load_capabilities(desired_caps))
        driver.set_page_load_timeout(self.timeout)
        logger.info(f"启动 {self.name} 浏览器.")
        return driver
