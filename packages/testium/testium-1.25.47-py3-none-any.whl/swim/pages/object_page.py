#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import pathlib
import time
from contextlib import suppress
from datetime import datetime

from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from loguru import logger
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import base64
import cv2
import numpy as np
import requests
import json
import ast

target = 0

site_orc_lang = {
    "US": "eng",
    "FR": "fra",
    "SA": "ara",
    "CN": "chi_sim",
}


class ObjectPage(object):

    def __init__(self, driver):
        self.driver = driver

    def get(self, url):
        """
        打开页面
        :param url: 页面链接
        :return:
        """
        logger.info(f"打开 {url} 链接.")
        with suppress(TimeoutException):
            self.driver.get(url=url)

    def maximize_window(self):
        """
        窗口最大化
        :return:
        """
        logger.info("最大化窗口.")
        self.driver.maximize_window()

    def click(self, element):
        """
        普通点击
        :param element:
        :return:
        """
        # logger.info(f"开始点击")
        element.click()

    def send_keys(self, element, values):
        """
        普通输入
        :param element:
        :param values:
        :return:
        """
        # logger.info(f"开始输入")
        element.send_keys(values)

    def switch_to_accept(self):
        """
        同意弹框
        """
        self.driver.switch_to.alert.accept()
        logger.info(f"已同意弹框")

    def get_ele_attribute(self, element, values):
        """
         获取属性
        :param element:
        :param values:
        :return:
        """
        # logger.info(f"开始获取元素属性")
        return element.get_attribute(values)

    def swipe_up(self, t=500, n=1, px1=0.5, py1=0.75, py2=0.25):
        """
        向上滑动屏幕
        :param t:
        :param n:
        :param px1:
        :param py1:
        :param py2:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * px1
        y1 = l['height'] * py1
        y2 = l['height'] * py2
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)
            time.sleep(1)

    def swipe_down(self, t=500, n=1, px1=0.5, py1=0.25, py2=0.75):
        """
        向下滑动屏幕
        :param t:
        :param n:
        :param px1:
        :param py1:
        :param py2:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * px1
        y1 = l['height'] * py1
        y2 = l['height'] * py2
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)
            time.sleep(1)

    def swipe_left(self, t=500, n=1, px1=0.75, py1=0.5, py2=0.25):
        """
        向左滑动屏幕
        :param t:
        :param n:
        :param px1:
        :param py1:
        :param py2:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * px1
        y1 = l['height'] * py1
        x2 = l['width'] * py2
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)
            time.sleep(1)

    def swipe_right(self, t=500, n=1, px1=0.25, py1=0.5, py2=0.75):
        """
        向右滑动屏幕
        :param t:
        :param n:
        :param px1:
        :param py1:
        :param py2:
        :return:
        """
        l = self.driver.get_window_size()
        x1 = l['width'] * px1
        y1 = l['height'] * py1
        x2 = l['width'] * py2
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)
            time.sleep(1)

    def swipe_down_element(self, element):
        """
        向下滑动到某个元素
        :param element:
        :return:
        """
        is_find = False
        max_count = 5
        while max_count > 0:
            if self.driver.find_elements(element):
                logger.info("向下滑动到:{}".format(element))
            else:
                self.swipe_down()
                max_count -= 1
                logger.info("向下滑动")

    def get_phone_size(self):
        """
        获取屏幕的大小
        :return:
        """
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        return width, height

    def get_wm_size(self):
        """通过adb命令获取屏幕宽高"""
        cmd = "wm size"
        screen_size = self.driver.execute_script("mobile: shell", {"command": cmd}).replace('\r\n', '')
        if "Override size:" in screen_size:  # 适配三星S23Ultra曲面屏
            size = screen_size.split("Override size:")[1]
        else:
            size = screen_size.split(":")[1]
        width, height = size.split("x")
        return int(width), int(height)

    def tap(self, element, x=0, y=0):
        """
        W3C规则，元素偏移点击
        :return:
        """

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action_tool = actions.w3c_actions.pointer_action
        action_tool.move_to(element, x=x, y=y)
        action_tool.pointer_down()
        action_tool.release()
        actions.perform()

    def consecutive_tap(self, element, count=1):
        """
        连续点击 count是连续点击的次数
        """
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action_tool = actions.w3c_actions.pointer_action
        action_tool.move_to(element, x=0, y=0)
        for _ in range(count):
            action_tool.pointer_down()
            action_tool.pause(0.1)
            action_tool.pointer_up()
            action_tool.pause(0.1)
        actions.perform()

    def old_tap(self, element, x, y):
        """
        按压
        :return:
        """
        actions = TouchAction(self.driver)
        actions.tap(element, x, y)
        actions.perform()
        time.sleep(2)

        # actions = ActionChains(self.driver)
        # actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        # action_tool = actions.w3c_actions.pointer_action
        # action_tool.move_to(element)
        # action_tool.pointer_down(tilt_x=x, tilt_y=y)
        # action_tool.release()
        # actions.perform()

    def touch_tap(self, x, y, duration=100):  # 点击坐标  ,x1,x2,y1,y2,duration
        """
        method explain:点击坐标
        parameter explain：【x,y】坐标值,【duration】:给的值决定了点击的速度
        Usage:
            device.touch_coordinate(277,431)      #277.431为点击某个元素的x与y值
        """
        screen_width = self.driver.get_window_size()['width']  # 获取当前屏幕的宽
        screen_height = self.driver.get_window_size()['height']  # 获取当前屏幕的高
        a = (float(x) / screen_width) * screen_width
        x1 = int(a)
        b = (float(y) / screen_height) * screen_height
        y1 = int(b)
        self.driver.tap([(x1, y1), (x1, y1)], duration)

    def location_tap(self, x, y):
        """
        W3C规则，坐标点击
        :return:
        """

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action_tool = actions.w3c_actions.pointer_action
        action_tool.move_to_location(x=x, y=y)
        action_tool.pointer_down()
        action_tool.release()
        actions.perform()

    def tap_size(self):
        """坐标点击"""

        # 设定系数,控件在当前手机的坐标位置除以当前手机的最大坐标就是相对的系数了
        # 188.8当前控件的X轴坐标位置，1069是屏幕手机最右下角X轴坐标位置
        rel_a1 = 188.8 / 1069
        # 941.5当前控件的Y轴坐标位置，1916是屏幕手机最右下角Y轴坐标位置
        rel_b1 = 941.5 / 1916
        # 获取当前手机屏幕大小x,y
        x, y = self.get_phone_size()
        # 屏幕坐标乘以系数即为用户要点击位置的具体坐标
        self.driver.tap([(rel_a1 * x, rel_b1 * y)])

    def screen_pinch(self):
        """
        放大操作
        :return:
        """

        screenX, screenY = self.get_phone_size()
        first_finger = TouchAction(self.driver)
        second_finger = TouchAction(self.driver)
        zoomFinger = MultiAction(self.driver)
        first_finger.press(x=screenX * 0.4, y=screenY * 0.4).wait(1000).move_to(x=screenX * 0.2,
                                                                                y=screenY * 0.2).wait(
            1000).release()
        second_finger.press(x=screenX * 0.6, y=screenY * 0.6).wait(1000).move_to(x=screenX * 0.8,
                                                                                 y=screenY * 0.8).release()
        zoomFinger.add(first_finger, second_finger)
        zoomFinger.perform()

    #
    def screen_zoom(self):
        """
        缩小操作
        :return:
        """
        screenX, screenY = self.get_phone_size()
        first_finger = TouchAction(self.driver)
        second_finger = TouchAction(self.driver)
        zoomFinger = MultiAction(self.driver)
        first_finger.press(x=screenX * 0.2, y=screenY * 0.2).wait(1000).move_to(x=screenX * 0.4,
                                                                                y=screenY * 0.4).wait(
            1000).release()
        second_finger.press(x=screenX * 0.8, y=screenY * 0.8).wait(1000).move_to(x=screenX * 0.6, y=screenY * 0.6).wait(
            1000).release()

        zoomFinger.add(first_finger, second_finger)
        zoomFinger.perform()

    def get_driver_capabilities(self):
        """
        获取设置的capabilities
        :return:
        """

        return self.driver.capabilities

    def get_device_uid(self):
        """获取设备的udid"""

        uid = self.get_driver_capabilities().get("udid")
        logger.info(f"该设备的udid是:{uid}")
        return uid

    def get_device_bundleId(self):
        """获取当前设备的包名"""
        platform_name = self.get_driver_capabilities().get("platformName")
        if platform_name == 'Android':
            app_package = self.get_driver_capabilities().get("appPackage")
        else:
            app_package = self.get_driver_capabilities().get("bundleId")
        logger.info(f"该设备的包名是:{app_package}")
        return app_package

    def get_device_language(self):
        """获取当前appium参数语言"""

        language = self.get_driver_capabilities().get("language")
        logger.info(f"该设备的appium参数语言:{language}")
        return language

    def is_visible_displayed(self, element):
        """
         判断元素是否可见
        :param element:
        :return:
        """

        return element.is_displayed()

    def is_visible_keyboard(self, element):
        """
        判断元素是否被键盘挡住
        :param element:
        :return:
        """
        # 获取待检测元素的位置信息
        element_location = element.location
        element_size = element.size

        # 获取键盘状态
        is_keyboard_visible = self.driver.is_keyboard_shown()

        # 获取屏幕大小
        screen_size = self.driver.get_window_size()

        # 计算键盘高度
        keyboard_height = 0
        if is_keyboard_visible:
            keyboard_height = screen_size['height'] - element_location['y'] - element_size['height']

        # 判断元素是否被键盘挡住
        if keyboard_height < element_location['y']:
            logger.info("元素被键盘挡住")
            return True
        else:
            logger.info("元素未被键盘挡住")
            return False
        # return element.is_displayed()

    def screenshot_info(self):
        """截图"""

        path = f"./result/screenshots/"
        today = datetime.today()
        current_date = str(today.year) + '_' + str(today.month) + '_' + str(today.day)
        img_name = f'{current_date}_{int(time.time() * 1000)}.png'
        file_name = f"{path}/{img_name}"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with suppress(BaseException):
            self.driver.get_screenshot_as_file(file_name)
        return file_name

    def target_screenshot_info(self):
        """目标截图"""

        path = f"./result/target_screenshots"
        global target
        target += 1
        img_name = f'target{target}.png'
        file_name = f"{path}/{img_name}"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with suppress(BaseException):
            self.driver.get_screenshot_as_file(file_name)
        return file_name

    def take_temp_screenshot(self):
        """截临时图"""
        path = f"./result/temp_screenshots"
        img_name = f'{int(time.time() * 1_000_000)}.png'
        file_name = f"{path}/{img_name}"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with suppress(BaseException):
            self.driver.get_screenshot_as_file(file_name)
        return file_name

    #
    # def find_elements(self, context):
    #     pass
    def set_time_out(self, time_seconds):
        self.driver.implicitly_wait(time_seconds)

    def long_press(self, element, x=None, y=None, duration=2000):
        """
        长按
        :param element:长按元素
        :param duration:长按时长
        :return:
        """
        x_position = element.location['x'] + element.size['width'] / 2
        y_position = element.location['y'] + element.size['height'] / 2
        self.real_move(x_position, y_position, x_position, y_position, down_time=2)
        # actions = TouchAction(self.driver)
        # actions.long_press(el=element, x=x, y=y, duration=duration).release().perform()
        # time.sleep(1)

    def launch_app(self):
        """重新启动app"""
        app_package = self.get_device_bundleId()
        self.driver.terminate_app(app_package)
        time.sleep(1)
        self.driver.activate_app(app_package)
        time.sleep(1)

    def click_element_center(self, element):
        """
        点击element中心
        """
        x_position = element.location['x'] + element.size['width'] / 2
        y_position = element.location['y'] + element.size['height'] / 2
        TouchAction(self.driver).tap(x=x_position, y=y_position).perform()

    def is_visible_displayed_h5(self, element):
        """
         h5页面判断元素是否可见
        :param element:
        :return:
        """
        y = element.location["y"]
        width, height = self.get_phone_size()
        if y <= 0 or y >= height:
            return False
        return True

    def click_by_decimal_point(self, decimal_x, decimal_y):
        x, y = self.get_phone_size()
        TouchAction(self.driver).tap(x=x * decimal_x, y=y * decimal_y).perform()

    def click_by_json_point(self, jsonelement):
        x_position = jsonelement['@x'] + jsonelement['@width'] / 2
        y_position = jsonelement['@y'] + jsonelement['@height'] / 2
        TouchAction(self.driver).tap(x=x_position, y=y_position).perform()

    def swipe_to_visible_h5(self, element, up_y=0, down_y=0, swipe_length=0.5):
        """
         h5页面滑动到指定元素
        :param element: up_y，down_y：指定显示区域  down_y<目标y轴<up_y，默认0，0为全屏
        :return:
        """
        count = 10
        width, height = self.get_phone_size()
        y = element.location["y"]
        up_y = up_y * width
        if down_y == 0:
            down_y = height
        else:
            down_y = height * down_y
        while count:
            if y <= up_y:
                self.swipe_down(py2=swipe_length + 0.25)
            elif y >= down_y:
                self.swipe_up(py2=0.75 - swipe_length)
            else:
                break
            count -= 1
            time.sleep(0.5)
            y = element.location["y"]

    def real_move(self, start_x, start_y, end_x, end_y, down_time=0, up_time=0):
        """
         精准距离滑动
        :param element: start_x，start_y：起点坐标  end_x，end_y：终点坐标，down_time：设置起点处长按，up_time：设置终点处长按
        :return:
        """
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action_tool = actions.w3c_actions.pointer_action
        action_tool.move_to_location(start_x, start_y)
        action_tool.pointer_down()
        action_tool.pause(down_time)
        action_tool.move_to_location(end_x, end_y)
        action_tool.pause(up_time)
        action_tool.release()
        actions.perform()

    def get_image_base64(self):
        """
        截图转base64
        """
        screenshot_base64 = self.driver.get_screenshot_as_base64()
        x, y = self.get_phone_size()
        return screenshot_base64, x, y

    def element_crop_image(self, element):
        """
        元素抠图
        """
        coordinate = element.rect
        x = coordinate["x"]
        y = coordinate["y"]
        width = coordinate["width"]
        height = coordinate["height"]
        screenshot_base64 = self.get_image_base64()
        return self.crop_image(
            image_base64=screenshot_base64,
            x=x,
            y=y,
            width=width,
            height=height
        )

    def crop_image(self, image_base64: tuple, x: int, y: int, width: int, height: int) -> str:
        """
        抠图
        """
        img_data = base64.b64decode(image_base64[0])
        # 原始比例
        primordial_x = image_base64[1]
        primordial_y = image_base64[2]
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        current_y, current_x, _ = img.shape
        # 计算真实比例
        # 公倍比
        ratio_y = current_y / primordial_y
        ratio_x = current_x / primordial_x
        # 还原真实比例
        x = int(x * ratio_x)
        y = int(y * ratio_y)
        width = int(width * ratio_x)
        height = int(height * ratio_y)
        crop_img = img[y:y + height, x:x + width]
        _, buffer = cv2.imencode('.jpg', crop_img)
        crop_img_base64 = base64.b64encode(buffer).decode()
        return crop_img_base64

    def get_element_rect(self, ele):
        width, height = self.get_phone_size()
        x = ele.location["x"]
        y = ele.location["y"]
        if x == -1:
            x = 0
        if x + ele.size["width"] == width + 1:
            end_x = 1
        else:
            end_x = (x + ele.size["width"]) / width
        start_x = x / width
        start_y = y / height
        end_y = (y + ele.size["height"]) / height
        if start_x < 0:
            start_x = 0
            logger.info("元素没有完整显示在屏幕内")
        if end_x > 1:
            end_x = 1
            logger.info("元素没有完整显示在屏幕内")
        if end_y > 1:
            end_y = 1
            logger.info("元素没有完整显示在屏幕内")
        if start_y < 0:
            start_y = 0
            logger.info("元素没有完整显示在屏幕内")
        rect = [start_x, start_y, end_x, end_y]
        return rect

    def crop_image_by_rect(self, rect):
        """
        抠图
        """
        image_base64 = self.driver.get_screenshot_as_base64()
        img_data = base64.b64decode(image_base64)
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if rect:
            height, width, channels = img.shape
            img = img[int(rect[1] * height):int(rect[3] * height),
                  int(rect[0] * width):int(rect[2] * width)]
        _, buffer = cv2.imencode('.jpg', img)
        crop_img_base64 = base64.b64encode(buffer).decode()
        return crop_img_base64

    def ocr_find_text(self, find_str, site=None, ele=None, rect=None, index=-1, img_base64=None, oem=1, psm=3,
                      image_path=None, ispattern="false",rev_rgb="false"):
        """ocr查找元素位置"""

        if site in site_orc_lang:
            orc_lang = site_orc_lang[site]
        else:
            orc_lang = "eng"
        if image_path:
            with open(image_path, 'rb') as f:
                # 读取图片的所有二进制数据
                image = f.read()
        else:
            if ele:
                rect = self.get_element_rect(ele)
                image_base64 = self.element_crop_image(element=ele)
            elif rect:
                image_base64 = self.crop_image_by_rect(rect)
            else:
                image_base64, _, _ = self.get_image_base64()
            image = base64.b64decode(image_base64)
        file_info = {'image': image}
        url = "http://10.102.245.53:9988/image/find"
        data = {
            'text_lang': orc_lang,
            'index': index,
            'find_str': find_str,
            'oem': oem,
            'psm': psm,
            'image_base64': img_base64,
            'ispattern': ispattern,
            'rev_rgb': rev_rgb
        }
        try:
            response = requests.post(url, files=file_info, data=data)
            if response.status_code != 200:
                assert False, f"请求失败: {response.text}"
            result_list = []
            for i in json.loads(response.text)["info"]:
                if rect:
                    ast_i = ast.literal_eval(i)
                    result_list.append(
                        ((rect[2] - rect[0]) * ast_i[0] + rect[0], (rect[3] - rect[1]) * ast_i[1] + rect[1]))
                else:
                    result_list.append(ast.literal_eval(i))
            return result_list
        except Exception as e:
            print(e)

    def ocr_click(self, find_str, site=None, ele=None, rect=None, index=-1, img_base64=None, oem=1, psm=3,
                  image_path=None, ispattern="false", rev_rgb="false"):
        """ocr点击"""
        w, h = self.get_phone_size()
        point_list = self.ocr_find_text(find_str, site=site, ele=ele, rect=rect, index=index, img_base64=img_base64,
                                        oem=oem,
                                        psm=psm,
                                        image_path=image_path, ispattern=ispattern,rev_rgb=rev_rgb)
        if point_list:
            self.driver.tap([(point_list[0][0] * w, point_list[0][1] * h)])
        else:
            logger.info("未找到元素")

    def ocr_point_click(self, ocr_point):
        w, h = self.get_phone_size()
        self.driver.tap([(ocr_point[0][0] * w, ocr_point[0][1] * h)])
