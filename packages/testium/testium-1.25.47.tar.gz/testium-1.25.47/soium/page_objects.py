import time
from contextlib import suppress
from loguru import logger
from retry import retry
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from .base_page import Page
from .common import get_locator
from .support.wait import Wait

URL = 'http://api-testmp.wrccorp.cn'


class PageElement(object):
    def __init__(self, soium: Page, locator, timeout=3, describe=""):
        self.soium = soium
        self.driver = soium.driver
        self.locator = locator
        self.timeout = timeout
        self.describe = describe

    def find_element(self, context=None):
        if not context:
            context = self.driver
        # by, value = get_locator(self.locator)
        by, value = self.locator
        self.soium.screenshot_info()
        element = context.find_element(by=by, value=value)
        element.locator = self.locator
        return element

    def find_elements(self, context=None):
        # by, value = get_locator(self.locator)
        by, value = self.locator
        if not context:
            context = self.driver
        self.soium.screenshot_info()
        elements = context.find_elements(by=by, value=value)
        for element in elements:
            element.locator = self.locator
        return elements

    def find_visible_element(self, context=None):
        self.soium.screenshot_info()
        element = Wait(timeout=self.timeout).until(
            self.visibility_of_element_located,
            context=context,
            message=f"找不到可见元素{self.locator}.")
        element.locator = self.locator
        return element

    def find_visible_elements(self, context=None):
        self.soium.screenshot_info()
        elements = Wait(timeout=self.timeout).until(
            self.visibility_of_any_elements_located,
            context=context,
            message=f"找不到可见元素{self.locator}.")
        for element in elements:
            element.locator = self.locator
        return elements

    @retry(WebDriverException, tries=1, delay=2)
    def element_size(self, context=None):
        element = self.find_visible_element(context=context)
        return self.soium.element_size(element=element)

    @retry(WebDriverException, tries=1, delay=2)
    def switch_to_frame(self, context=None):
        element = self.find_visible_element(context=context)
        self.soium.switch_to_frame(element=element)

    @retry(WebDriverException, tries=1, delay=2)
    def scrolled_into_view(self, context=None):
        element = self.find_visible_element(context=context)
        self.soium.scrolled_into_view(element=element)

    @retry(WebDriverException, tries=1, delay=2)
    def get_text(self, context=None):
        element = self.find_visible_element(context=context)
        text = self.soium.get_text(element=element)
        return text

    @retry(WebDriverException, tries=1, delay=2)
    def get_attribute(self, name, context=None):
        element = self.find_element(context=context)
        value = self.soium.get_attribute(element=element, name=name)
        return value

    @retry(WebDriverException, tries=1, delay=2)
    def click(self, context=None):
        element = self.find_visible_element(context=context)
        self.driver.execute_script("arguments[0].style.border='3px solid yellow'", element)
        self.soium.click(element=element, describe=self.describe)

    @retry(WebDriverException, tries=1, delay=2)
    def scroll_click(self, context=None):
        element = self.find_visible_element(context=context)
        self.driver.execute_script("arguments[0].style.border='3px solid yellow'", element)
        self.soium.scrolled_into_view(element=element)
        time.sleep(2)
        self.soium.click(element=element, describe=self.describe)

    @retry(WebDriverException, tries=1, delay=2)
    def tap(self, context=None, x=None, y=None):
        """
        按压元素
        :return:
        """
        return self.soium.tap(self.find_visible_element(context=context), x, y)

    @retry(WebDriverException, tries=1, delay=2)
    def mouse_click(self, context=None, x=0, y=0):
        element = self.find_visible_element(context=context)
        self.soium.mouse_click(element=element, x=x, y=y)

    @retry(WebDriverException, tries=1, delay=2)
    def random_click(self, context=None):
        elements = self.find_visible_elements(context=context)
        self.soium.random_click(elements=elements, describe=self.describe)

    @retry(WebDriverException, tries=1, delay=2)
    def enter(self, context=None):
        element = self.find_visible_element(context=context)
        self.soium.enter(element=element)

    @retry(WebDriverException, tries=1, delay=2)
    def select(self, index=None, value=None, text=None, context=None):
        element = self.find_visible_element(context=context)
        self.soium.select(element=element, index=index, value=value, text=text)

    @retry(WebDriverException, tries=1, delay=2)
    def move_to_element(self, context=None):
        element = self.find_visible_element(context=context)
        self.soium.move_to_element(element=element)

    @retry(WebDriverException, tries=1, delay=2)
    def send_keys(self, value, clear=True, context=None):
        element = self.find_visible_element(context=context)
        self.soium.run_script("arguments[0].click();", element)
        self.soium.send_keys(element=element, value=value, clear=clear, describe=self.describe)

    @retry(WebDriverException, tries=1, delay=2)
    def clear(self, context=None):
        element = self.find_visible_element(context=context)
        self.soium.clear(element=element)


    def assert_element_text_equals(self, text_, context=None):
        current_text = self.get_text(context=context)
        result = current_text == text_
        if result:
            logger.info(f"The element {self.locator} text is {current_text}.")
        else:
            logger.info(
                f"The element {self.locator} text is not equal to {text_}, and the current text is {current_text}."
            )
        return result

    def assert_element_text_contains(self, text_, context=None):
        current_text = self.get_text(context=context)
        result = text_ in current_text
        if result:
            logger.info(
                f"The element {self.locator} text contains {text_}, and the current text is {current_text}."
            )
        else:
            logger.info(
                f"The element {self.locator} text does not contain {text_}, and the current text is {current_text}."
            )
        return result

    def assert_element_attribute_equals(self, name, value, context=None):
        current_value = self.get_attribute(name=name, context=context)
        result = value in current_value
        if result:
            logger.info(
                f"The value of the element {self.locator} attribute {name} is {value}."
            )
        else:
            logger.info(
                f"The value of the element {self.locator} attribute {name} is not equal to {value}, and the current "
                f"value is {current_value}. "
            )
        return result

    def is_visible(self, timeout, context=None):
        if Wait(timeout=timeout).until(self.visibility_of_any_elements_located,
                                       context=context):
            logger.info(f"{self.locator}元素存在, 且可见状态")
            return True
        else:
            logger.info(f"{self.locator}元素不存在, 且不可见状态")
            return False

    def is_enabled(self, timeout, context=None):
        if Wait(timeout=timeout).until(self.enablelity_of_any_elements_located,
                                       context=context):
            return True
        else:
            return False

    def visibility_of_element_located(self, context=None):
        elements = self.find_elements(context=context)
        with suppress(StaleElementReferenceException):
            for element in elements:
                if element.is_displayed():
                    return element

    def visibility_of_any_elements_located(self, context=None):
        with suppress(StaleElementReferenceException):
            return [
                element for element in self.find_elements(context=context)
                if element.is_displayed()
            ]

    def enablelity_of_any_elements_located(self, context=None):
        with suppress(StaleElementReferenceException):
            return [
                element for element in self.find_elements(context=context)
                if element.is_enabled()
            ]

    def swipe_down_until_element_displayed(self, context=None, px=500):
        """向下滑动直到元素可见"""

        for i in range(10):
            if self.is_visible(timeout=2, context=context) is False:
                self.soium.run_script(f"window.scrollBy(0, {px})")  # 无头模式下高度在500多
