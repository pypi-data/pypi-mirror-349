import random
import requests
import jsonpath

from loguru import logger
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from soium.support.proxy_config import ProxyConfig

# "10.102.14.27:8899" "10.102.14.28:8899",
# 8:资产编号0559（Linux）, 27:资产编号0571, 20:资产编号0591, 37:资产编号0150（Linux）, 19:资产编号1025（Linux）, 10.102.14.29, 10.102.14.33, 10.102.14.30, 10.102.14.5 这四台是MAC Mini


def get_proxy(envTag, site, options):
    """代理判断"""
    if "gray" in envTag:
        proxy = ProxyConfig().get_site_proxy(site, envTag)
        options.add_argument("--proxy-server=%s" % proxy)
        logger.info("走代理请求:" + proxy + "环境变量:" + envTag)
    return options



def browser_chrome(envTag, site, platform_name):
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")

    if platform_name == "Linux":
        options.add_argument("--headless")  # 不加这个linux服务启动会失败
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1960,1080")
    # options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.geolocation": 2}  # 禁止位置权限
    options.add_experimental_option("prefs", prefs)
    return get_proxy(envTag, site, options)


def browser_firefox(envTag, site):
    options = webdriver.FirefoxOptions()
    return get_proxy(envTag, site, options)


def browser_safari(envTag, site):
    options = Options()
    options.add_argument("browserName=safari")
    options.add_argument("platformName=mac")
    return get_proxy(envTag, site, options)


def browser_ie(envTag, site):
    options = webdriver.IeOptions()
    options.add_argument("browserName=internet explorer")
    options.add_argument("platformName=windows")
    return get_proxy(envTag, site, options)


def browser_edge(envTag, site):
    options = webdriver.EdgeOptions()
    options.add_argument("browserName=MicrosoftEdge")
    return get_proxy(envTag, site, options)


class WebDriver(object):
    def __init__(self, name="Chrome"):
        self.name = name

    def select_browser(self, command_executor, envTag, site, platform_name):
        """选择浏览器"""

        browser_type = self.name
        if browser_type == "Chrome":
            options = browser_chrome(envTag, site, platform_name)
        elif browser_type == "Firefox":
            options = browser_firefox(envTag, site)
        elif browser_type == "Safari":
            options = browser_safari(envTag, site)
        elif browser_type == "IE":
            options = browser_ie(envTag, site)
        elif browser_type == "Edge":
            options = browser_edge(envTag, site)
        else:
            raise NameError(f"请输入正确的浏览器名称。 选项有：Chrome、Firefox、Safari")
        driver = webdriver.Remote(
            command_executor=command_executor,
            options=options,
        )
        logger.info(f"启动服务:{command_executor}, 浏览器是:{browser_type}.")
        return driver

    def remote(self, hub="127.0.0.1:4444", envTag="online", site="site", *args, **kwargs):
        command_executor = f"{hub}/wd/hub"
        selenium_status = requests.get("http://" + command_executor + "/status").json()
        platform_name = jsonpath.jsonpath(selenium_status, '$..osInfo')[0]["name"]
        logger.info(f"{hub}，系统是：{platform_name}")
        driver = self.select_browser(command_executor, envTag, site, platform_name)
        driver.maximize_window()
        return driver
