import random
import time
import pathlib
import pytest
from datetime import datetime
from contextlib import contextmanager
from contextlib import suppress
from loguru import logger
from retry import retry
from selenium.common.exceptions import WebDriverException, NoAlertPresentException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from .common import add_border
from .support.wait import Wait
import os

coupon_close_nums = 0


class Page(object):
    def __init__(self, driver, page_load_timeout=60):
        self.driver = driver
        self.page_load_timeout = page_load_timeout
        self.set_page_load_timeout(time_to_wait=page_load_timeout)

    def get(self, url):
        logger.info(f"打开 {url} 链接.")
        with suppress(TimeoutException):
            self.driver.get(url=url)
        self.wait_for_page_to_load()

    def quit(self):
        logger.info("退出浏览器.")
        self.driver.quit()

    def close(self):
        logger.info("Close the current TAB.")
        self.driver.close()

    def forward(self):
        logger.info("Next page.")
        with suppress(TimeoutException):
            self.driver.forward()
        self.wait_for_page_to_load()

    def back(self):
        logger.info("Previous page.")
        with suppress(TimeoutException):
            self.driver.back()
        self.wait_for_page_to_load()

    def pause(self):
        logger.info("Stop loading the page")
        self.driver.execute_script('window.stop();')

    def refresh(self):
        logger.info("刷新页面.")
        with suppress(TimeoutException):
            self.driver.refresh()
        self.wait_for_page_to_load()

    def maximize_window(self):
        logger.info("最大化窗口.")
        self.driver.maximize_window()

    def minimize_window(self):
        logger.info("Minimize window.")
        self.driver.minimize_window()

    def run_script(self, js, *args):
        logger.info(f"运行脚本js：{js} 参数：{args}")
        result = self.driver.execute_script(js, *args)
        return result

    @staticmethod
    def wait(secs):
        logger.info(f"Wait for {secs} seconds.")
        time.sleep(secs)
    def wait_for_page_to_load(self):
        if not Wait(timeout=self.page_load_timeout).until(
                method=self.assert_state_is_complete):
            try:
                self.pause()
            except TimeoutException:
                raise TimeoutError(f"页面加载超时.")

    def set_page_load_timeout(self, time_to_wait):
        logger.info(f"初始化启动中, 设置页面超时为 {time_to_wait} 秒。")
        self.driver.set_page_load_timeout(time_to_wait=time_to_wait)

    def implicitly_wait(self, time_to_wait):
        logger.info(f"Set implicitly wait for {time_to_wait} seconds.")
        self.driver.implicitly_wait(time_to_wait=time_to_wait)

    @property
    def window_handles(self):
        window_handles = self.driver.window_handles
        logger.info(f"Current has {len(window_handles)} tabs.")
        return window_handles

    @property
    def current_window_handle(self):
        logger.info(f"获取当前标签.")
        return self.driver.current_window_handle

    def switch_to_window(self, handle=None, index=None):
        logger.info(f"切换标签.")
        if index:
            tabs = self.window_handles
            self.driver.switch_to.window(tabs[index])
        elif handle:
            self.driver.switch_to.window(handle)
        else:
            raise ValueError('请输入制表符或制表符光标.')

    def switch_to_frame(self, element):
        logger.info(f"Switch to framework {element.locator}.")
        self.driver.switch_to.frame(frame_reference=element)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    @property
    def get_title(self):
        title = self.driver.title
        logger.info(f"Current title is {title}.")
        return title

    @property
    def get_url(self):
        url = self.driver.current_url
        logger.info(f"当前网址是 {url}.")
        return url

    @property
    def get_source(self):
        logger.info("Get page source.")
        page_source = self.driver.page_source
        return page_source

    @property
    def get_state(self):
        state = self.driver.execute_script("return document.readyState")
        logger.info(f"Current page state is {state}.")
        return state

    @property
    def window_size(self):
        width = self.driver.execute_script("return window.screen.availWidth")
        height = self.driver.execute_script("return window.screen.availHeight")
        logger.info(
            f"The current page width is {width}px and height is {height}px.")
        return {"width": width, "height": height}

    @staticmethod
    def element_size(element):
        height, width = element.size["height"], element.size["width"]
        logger.info(
            f"The element {element.locator} is {width}px wide and {height}px high."
        )
        return {"width": width, "height": height}

    def get_cookie(self, name, attr='value'):
        cookie = self.driver.get_cookie(name=name)
        if attr != 'all':
            cookie = cookie[attr]
        logger.info(f"Cookie '{name}' is {cookie}.")
        return cookie

    def get_cookies(self, attr='value'):
        cookies = self.driver.get_cookies()
        if attr != 'all':
            cookies_ = {}
            for cookie in self.driver.get_cookies():
                cookies_[cookie['name']] = cookie['value']
            cookies = cookies_
        logger.info(f"Cookies 是 {cookies}.")
        return cookies

    def add_cookie(self, cookie_dict):
        logger.info(f"Add {cookie_dict} to current cookies.")
        self.driver.add_cookie(cookie_dict)

    def delete_all_cookies(self):
        logger.info("Delete all cookies.")
        self.driver.delete_all_cookies()

    def accept_alert(self, timeout=5):
        if Wait(timeout=timeout).until(self.assert_alert_is_present):
            self.driver.switch_to.alert.accept()
        else:
            raise TimeoutError(f"No alert shown for {timeout} seconds.")

    def dismiss_alert(self, timeout=5):
        if Wait(timeout=timeout).until(self.assert_alert_is_present):
            self.driver.switch_to.alert.dismiss()
        else:
            raise TimeoutError(f"No alert shown for {timeout} seconds.")

    @property
    def get_alert_text(self, timeout=5):
        if Wait(timeout=timeout).until(self.assert_alert_is_present):
            return self.driver.switch_to.alert.text
        else:
            raise TimeoutError(f"No alert shown for {timeout} seconds.")

    def get_img(self, filename):
        if self.driver.get_screenshot_as_file(filename=filename):
            logger.info(
                f"Saves a screenshot of the current window to {filename}.")
        else:
            logger.warning("Screenshot save failed.")
            filename = 'failed'
        return filename

    def get_base64(self):
        logger.info("Gets the screenshot of the current window as a base64.")
        base64 = self.driver.get_screenshot_as_base64()
        return base64

    # def touch_to_scroll(self, xoffset, yoffset):
    #     logger.info(f"Touch and scroll, moving by {xoffset} and {yoffset}.")
    #     try:
    #         TouchActions(self.driver).scroll(xoffset=xoffset,
    #                                          yoffset=yoffset).perform()
    #     except WebDriverException:
    #         page_x_offset = self.driver.execute_script(
    #             "return window.pageXOffset")
    #         page_y_offset = self.driver.execute_script(
    #             "return window.pageYOffset")
    #         self.driver.execute_script(
    #             f"window.scrollTo({xoffset + page_x_offset},{yoffset + page_y_offset})"
    #         )

    def scrolled_into_view(self, element):
        logger.info(f"Scroll to element {element.locator}.")
        self.driver.execute_script(
            'arguments[0].scrollIntoView({block: "center", behavior: "auto"});',
            element,
        )

    @staticmethod
    def is_displayed(element):
        return element.is_displayed()

    @staticmethod
    def is_enabled(element):
        return element.is_enabled()

    def get_text(self, element):
        self.scrolled_into_view(element=element)
        text = element.text
        logger.info(f"元素 {element.locator} 的文本是 {text}.")
        return text

    @staticmethod
    def get_attribute(element, name):
        value = element.get_attribute(name)
        logger.info(
            f"元素 {element.locator} 的属性 '{name}' 是 {value}."
        )
        return value

    @staticmethod
    def element_exists_click(driver, by, value):
        try:
            element = driver.find_element(by=by, value=value)
            logger.info(f"元素存在：{value}")
        except NoSuchElementException:
            logger.info(f"元素不存在：{value}")
        else:
            element.click()

    @retry((ElementClickInterceptedException,), tries=2, delay=0.5)
    def click(self, element, describe=None):
        global coupon_close_nums
        logger.info(f"单击元素 {element.locator}, 点击操作是:{describe}.")
        add_border(driver=self.driver, element=element)
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            coupon_pc = (
                "div.c-vue-coupon .she-close>svg,"
                "div.c-vue-coupon .icon-close,"
                "div.c-vue-coupon .btn-default,"
                "span.btn-default,"  # new style:special deals:easy
                "div.dialog-top img,"  # new style:special deals:complex、big title
                "svg.btn-new"
            )
            coupon_pwa = (
                "div.S-dialog__body svg, "
                "div.c-coupon-box i, "
                "svg.revisit_close, "
                "header.dialog-header__icon-gift img, "
                "span.btn-default,"
                "svg.btn-new"
            )
            cookie_pwa = (
                "button#onetrust-accept-btn-handler,"
                "div.c-onetrust-backup button.S-button__primary,"
                "button.sui-button-common__primary,"
                "div.cmp_c_2,"
                "div.actions>button.sui-button-common.sui-button-common__primary"
            )
            cookie_pc = (
                "button#onetrust-accept-btn-handler,"
                "div.c-onetrust-backup button:first-of-type,"
                "div.cmp_c_1102 .cmp_c_2"
            )
            subscribe_pwa = (
                "div.subscribe-footer>button:first-of-type"
            )
            if isinstance(self.driver, AppiumWebDriver):
                self.element_exists_click(self.driver, By.CSS_SELECTOR, coupon_pwa)
                self.element_exists_click(self.driver, By.CSS_SELECTOR, cookie_pwa)
                self.element_exists_click(self.driver, By.CSS_SELECTOR, subscribe_pwa)
            else:
                self.element_exists_click(self.driver, By.CSS_SELECTOR, coupon_pc)
                self.element_exists_click(self.driver, By.CSS_SELECTOR, cookie_pc)
            raise ElementClickInterceptedException
        except WebDriverException:
            self.scrolled_into_view(element=element)
            element.click()

    @retry((WebDriverException,), tries=1, delay=2)
    def tap(self, element, x, y):
        """
        按压
        :return:
        """
        actions = TouchAction(self.driver)
        actions.tap(element, x, y)
        actions.perform()

    @retry((WebDriverException,), tries=1, delay=2)
    def mouse_click(self, element, x=0, y=0):
        logger.info(f"Click the element {element.locator}.")
        add_border(driver=self.driver, element=element)
        try:
            ActionChains(self.driver).move_by_offset(x, y).click(on_element=element).perform()
        except WebDriverException:
            self.scrolled_into_view(element=element)
            ActionChains(self.driver).move_by_offset(x, y).click(on_element=element).perform()

    @retry((WebDriverException,), tries=1, delay=2)
    def random_click(self, elements, describe=None):
        element = random.choice(elements)
        logger.info(f"随机点击元素 {element.locator}, 随机操作是:{describe}.")
        add_border(driver=self.driver, element=element)
        try:
            element.click()
        except WebDriverException:
            self.scrolled_into_view(element=element)
            element.click()

    def enter(self, element):
        logger.info(f"元素 {element.locator} 执行 Enter.")
        add_border(driver=self.driver, element=element)
        element.send_keys(value=Keys.ENTER)

    def move_to_element(self, element):
        logger.info(f"将鼠标移到元素 {element.locator} 上.")
        add_border(driver=self.driver, element=element)
        ActionChains(self.driver).move_to_element(to_element=element).perform()

    def long_press_operate(self, x, y, duration):
        TouchAction(self.driver).long_press(x=x, y=y, duration=duration).release().perform()
        
    def press(self, x, y):
        TouchAction(self.driver).press(x=x, y=y).perform()

    def click_tap(self, x, y):
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def send_keys(self, element, value, clear=True, describe=None):
        logger.info(f"元素 {element.locator} 输入 {value}, 输入操作是:{describe}.")
        add_border(driver=self.driver, element=element)
        if clear:
            self.driver.execute_script("arguments[0].select();", element)
            time.sleep(0.5)
            element.send_keys(Keys.DELETE)
            time.sleep(0.5)
        element.send_keys(value)

    def clear(self, element):
        add_border(driver=self.driver, element=element)
        self.driver.execute_script("arguments[0].select();", element)
        time.sleep(0.5)
        element.send_keys(Keys.DELETE)
        time.sleep(0.5)

    def select(self, element, index=None, value=None, text=None):
        add_border(driver=self.driver, element=element)
        if value:
            logger.info(f"select {element.locator} value is {value}.")
            Select(webelement=element).select_by_value(value=value)
        elif index:
            logger.info(f"select {element.locator} index is {index}.")
            Select(webelement=element).select_by_index(index=index)
        else:
            logger.info(f"select {element.locator} text is {text}.")
            Select(webelement=element).select_by_visible_text(text=text)

    def assert_state_is_complete(self):
        return self.driver.execute_script(
            'return document.readyState == "complete"')

    def assert_alert_is_present(self):
        try:
            alert = self.driver.switch_to.alert
            return alert
        except NoAlertPresentException:
            return False

    def assert_new_window_is_opened(self, current_handles):
        return len(self.driver.window_handles) > len(current_handles)

    def assert_url_changes(self, url):
        return url != self.driver.current_url

    def assert_url_contains(self, url):
        return url in self.driver.current_url

    @contextmanager
    def assert_jump_to(self, new_tab=False):
        url = self.get_url
        handles = self.window_handles if new_tab else None
        yield
        if new_tab:
            Wait(timeout=self.page_load_timeout).until(
                self.assert_new_window_is_opened,
                current_handles=handles,
                message="No new window opens.")
            current_handles = self.window_handles
            new_handles = (set(current_handles).difference(set(handles))).pop()
            self.switch_to_window(handle=new_handles)
        Wait(timeout=self.page_load_timeout).until(
            self.assert_url_changes,
            url=url,
            message="Did not jump to the new link.")

    # 向上滑动滚动条到顶部
    def scroll_to_top(self, px=None):
        if px:
            self.run_script(f"window.scrollTo(0, -{px})")
        else:
            self.run_script("window.scrollTo(0, -0)")

    # 向下滑动滚动条到底部
    def scroll_to_bottom(self, px=None):
        if px:
            self.run_script(f"window.scrollTo(0, {px})")
        else:
            self.run_script("window.scrollTo(0, document.body.scrollHeight)")

    # 获取设备尺寸
    def get_device_size(self):

        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    # 滑动
    def swipe_element(self, x1, y1, x2, y2, t=200):
        self.driver.swipe(x1, y1, x2, y2, t)

    # 向上滑动
    def swipe_up(self, x1=0.5, y1=0.75, x2=0.5, y2=0.25, t=200):

        x, y = self.get_device_size()
        self.driver.swipe(x * x1, y * y1, x * x2, y * y2, t)

    # 向下滑动
    def swipe_down(self, x1=0.5, y1=0.25, x2=0.5, y2=0.75, t=200):
        x, y = self.get_device_size()
        self.driver.swipe(x * x1, y * y1, x * x2, y * y2, t)

    def loop_swipe_down(self, px=500, num=10):
        """向下滑动10次"""

        for i in range(num):
            self.run_script(f"window.scrollBy(0, {px})")  # 无头模式下高度在500多
            time.sleep(2)

    def adb_execute(self, cmd):
        return self.driver.execute_script("mobile: shell", {"command": cmd}).replace('\r\n', '')

    def setting_input_method_type(self, var):
        """设置设备的输入法
            :param var: sou_gou, appium, Gboard
        """
        input_method={
            'sou_gou': 'com.sohu.inputmethod.sogou.xiaomi/.SogouIME',
            'appium': 'io.appium.settings/.UnicodeIME',
            'Gboard': 'com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME'
            }
        cmd = f'ime set {input_method[var]}'
        logger.info(f"设置键盘输入法开始，当前设置的输入法为：{var}")
        return self.adb_execute(cmd)
    
    def press_keycode_number(self, keycode):
        """键盘数字方法"""

        self.driver.press_keycode(keycode)
        logger.info(f'input keyevent KEYCODE_{keycode}')

    def switch_into_native_app(self):
        """切换进入到NATIVE窗口方法"""

        self.driver.switch_to.context(self.driver.update_settings({"nativeWebTap": True}).contexts[0])
        
    def switch_into_webview(self):
        """切回webview窗口方法"""

        self.driver.switch_to.context(self.driver.update_settings({"nativeWebTap": False}).contexts[1])

    def screenshot_info(self, specify_path=False):
        """截图"""

        if specify_path:
            path = f"./result/specify_screenshots/"
        else:
            path = f"./result/screenshots/"
        today = datetime.today()
        current_date = str(today.year) + '_' + str(today.month) + '_' + str(today.day)
        img_name = f'{current_date}_{int(time.time() * 1000)}.png'
        file_name = f"{path}/{img_name}"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with suppress(BaseException):
            self.driver.get_screenshot_as_file(file_name)

    def assume_false(self, desc):
        """软断言失败截图"""

        pytest.assume(False)
        logger.info(f"断言失败：{desc}")
        self.screenshot_info(True)

    def click_other(self, x, y, element):
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action_tool = actions.w3c_actions.pointer_action
        action_tool.move_to(element)
        action_tool.pointer_down(tilt_x=x, tilt_y=y)
        action_tool.release()
        actions.perform()

    def get_page_elements_attribute(self, ele, attribute, num=10):
        """获取页面元素属性值"""

        return self.driver.execute_script(
            f"return Array.from(document.querySelectorAll('{ele}')).map(item => item.getAttribute('{attribute}')).slice(0, {num});")

    def get_page_elements_text(self, ele, num=10):
        """获取页面元素文本值"""

        return self.driver.execute_script(
            f"return Array.from(document.querySelectorAll('{ele}')).map(item => item.textContent).slice(0, {num});")



