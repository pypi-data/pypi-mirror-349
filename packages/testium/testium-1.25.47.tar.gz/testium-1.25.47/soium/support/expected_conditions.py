# from selenium.common.exceptions import (NoAlertPresentException, StaleElementReferenceException, NoSuchElementException,
#                                         WebDriverException)
#
# from ..common import get_locator
#

#
# class state_is_complete(object):
#     def __init__(self):
#         pass
#
#     def __call__(self, driver):
#         return driver.execute_script(
#             'return document.readyState == "complete"')
#
#
# class alert_is_present(object):
#     def __init__(self):
#         pass
#
#     def __call__(self, driver):
#         try:
#             alert = driver.switch_to.alert
#             return alert
#         except NoAlertPresentException:
#             return False
#
#
# class new_window_is_opened(object):
#     def __init__(self, current_handles):
#         self.current_handles = current_handles
#
#     def __call__(self, driver):
#         return len(driver.window_handles) > len(self.current_handles)
#
#
# class url_changes(object):
#     def __init__(self, url):
#         self.url = url
#
#     def __call__(self, driver):
#         return self.url != driver.current_url
#
#
# class url_contains(object):
#
#     def __init__(self, url):
#         self.url = url
#
#     def __call__(self, driver):
#         return self.url in driver.current_url
#
#
# class element_text_equals(object):
#     def __init__(self, element, text_):
#         self.element = element
#         self.text = text_
#
#     def __call__(self, driver):
#         return self.element.text == self.text
#
#
# class element_text_contains(object):
#     def __init__(self, element, text_):
#         self.element = element
#         self.text = text_
#
#     def __call__(self, driver):
#         return self.text in self.element.text
#
#
# class element_attribute_equals(object):
#     def __init__(self, element, name, value):
#         self.element = element
#         self.name = name
#         self.value = value
#
#     def __call__(self, driver):
#         return self.value in self.element.get_attribute(self.name)
#
#
# class visibility_of_element_located(object):
#
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         try:
#             return _element_if_visible(_find_element(driver, get_locator(self.locator)))
#         except StaleElementReferenceException:
#             return False
#
#
# class visibility_of_any_elements_located(object):
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         return [element for element in _find_elements(driver, get_locator(self.locator)) if
#                 _element_if_visible(element)]
#
#
# class presence_of_element_located(object):
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         return _find_element(driver, get_locator(self.locator))
#
#
# def _find_element(driver, by):
#     try:
#         return driver.find_element(*by)
#     except NoSuchElementException as e:
#         raise e
#     except WebDriverException as e:
#         raise e
#
#
# def _find_elements(driver, by):
#     try:
#         return driver.find_elements(*by)
#     except WebDriverException as e:
#         raise e
#
#
# def _element_if_visible(element, visibility=True):
#     return element if element.is_displayed() == visibility else False
