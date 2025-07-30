import time

from selenium.webdriver.common.by import By



def get_locator(locator):
    locator_list = {
        # selenium
        "css": By.CSS_SELECTOR,
        "id_": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
        "tag": By.TAG_NAME,
        "class_name": By.CLASS_NAME,
    }
    by, value = locator
    return locator_list[by], value


def add_border(driver, element, clear=True):
    previous_style = element.get_attribute(name="style")
    driver.execute_script(
        "arguments[0].setAttribute('style', 'border: 2px solid red; font-weight: bold;');",
        element)
    if clear:
        driver.execute_script(
            "var target = arguments[0];"
            "var previousStyle = arguments[1];"
            "setTimeout("
            "function() {"
            "target.setAttribute('style', previousStyle);"
            "},400"
            ");", element, previous_style)
