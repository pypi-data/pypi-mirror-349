#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import copy
import json
import os
import pathlib
import random
import shutil
import string
import time

import cv2
import pytest
import requests
import yaml
# from PIL import Image
from loguru import logger

from swim.drivers.android.android_driver import AndroidDriver
from swim.drivers.browser.browser_driver import BrowserDriver
from swim.drivers.ios.ios_driver import IOSDriver
from swim.pages.object_page import ObjectPage
from swim.plugins import PytestParser, Report, FailureMessages, StatusInt, WhenInfo
from swim.utils.language_util import LanguageUtil

# URL = 'http://api-testmp.wrccorp.cn'
# URL = 'http://tep.wrccorp.cn'
URL_IMAGE = "http://imgdeal-test01.wrc.com/index.php/uploadimg"
authorization = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbm9ueW1vdXNVc2VyIiwiYXV0aCI6InVzZXIiLCJpc3MiOiJzaGVpbiIsImV4cCI6NDEwMjMyOTYwMCwiaWF0IjoxNjUyNzY1NzU5fQ.UtLfIAWLHGtGvgPacPm4Ty_fwQeRmskVpvCwO86kdMU"

TEP_TEST_ETP_URL = "https://tep.wrccorp.cn/api/testing/testcase/etp"  # 正式环境: tep.wrccorp.cn 测试环境: tep-test.wrccorp.cn
event_track_param = None  # 全局变量, 构造埋点参数。传给埋点SDK
session_value = None  # 全局变量session。上传埋点报告时用到
newest_driver = None  # 全局变量newest_driver,重启ios时用到
driver = None
market_data = {}


def pytest_addoption(parser):
    """
        https://docs.pytest.org/en/6.2.x/example/simple.html
        https://docs.pytest.org/en/6.2.x/reference.html
        :param parser:
        :return:
        """
    parser.addoption("--report", action="store", default="local")  # 传入remote报告则发送远程服务器,local则创建本地报告.
    parser.addoption("--terminal", action="store", default="ios")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--udid", action="store", default="")
    parser.addoption("--env", action="store", default="")
    parser.addoption("--local", action="store", default="appium")
    parser.addoption("--email", action="store", default="")
    parser.addoption("--site", action="store", default="us")
    parser.addoption("--password", action="store", default="")
    parser.addoption("--job", action="store", default="388")
    parser.addoption("--host", action="store", default="127.0.0.1")
    parser.addoption("--port", action="store", default="4723")
    parser.addoption("--task", action="store", default="388")
    parser.addoption("--extendPort", action="store", default="8100")
    parser.addoption("--brand", action="store", default="wrc")
    parser.addoption("--deviceName", action="store", default="ios")
    parser.addoption("--devicePlatform", action="store", default="ios")
    parser.addoption("--deviceVersion", action="store", default="14.2")
    parser.addoption("--eventTracking", action="store", default="")
    parser.addoption("--appKey", action="store", default="wrc_ios_py")
    parser.addoption("--bundleId", action="store", default='zzkko.com.ZZKKO')
    parser.addoption("--useProxy", action="store", default='false')
    parser.addoption("--appVersion", action="store", default='8.3.8')
    parser.addoption("--tepEnv", action="store", default='release')
    parser.addoption("--extraParams", action="store", default="")
    parser.addoption("--coverageEnable", action="store", default="false")
    parser.addoption("--appPack", action="store", default="")
    parser.addoption("--appActivity", action="store", default="")


def pytest_configure(config):
    """
    允许插件和conftest文件执行初始配置。
    :param config:
    :return:
    """

    report = config.option.report
    if not report:
        return
    plugin = GenerateReport(config)
    config.report = plugin
    config.pluginmanager.register(plugin)


def pytest_unconfigure(config):
    """
    退出测试之前调用
    :param config:
    :return:
    """

    plugin = getattr(config, "report")
    if plugin:
        del config.report
        config.pluginmanager.unregister(plugin=plugin)


# def compress_img_PIL_info(file_name, compress_rate=0.5):
#     """压缩图片"""
#
#     img = Image.open(file_name)
#     w, h = img.size
#     img_resize = img.resize((int(w * compress_rate), int(h * compress_rate)))
#     img_resize.save(file_name)
#     logger.info("图片压缩完成")


def lg(name):
    """
    自定义日志
    :param name:
    :return:
    """
    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}-{name}')
    GenerateReport.lgs.append(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}-{name}\n')


def get_handle_tep_deeplink_url(task, site, terminal, page_type, job_id):
    headers = {
        'Authorization': authorization,
    }

    params = {
        'taskId': task,
        'site': site,
        'pageType': page_type,
        'terminal': terminal,
        'jobId': job_id,
    }
    market_data["site"] = site
    market_data["terminal"] = terminal
    market_data["pageType"] = page_type
    response = requests.get('https://tep.wrccorp.cn/api/testing/marketLink', params=params, headers=headers).json()
    logger.info(f"接口返回数据Kafka-link消息数据{response}")
    out_in = []
    for item in response:
        output = []
        if isinstance(item, dict):
            for s in item['link'].split("data={", 1)[1].split(","):
                if 'ad_type' in s or 'goods_id' in s:
                    output.append(s)
            str_info = {'&'.join(output): item['link']}
            out_in.append(str_info)
    return out_in


def get_tep_deeplink_goods_ids(task, site, terminal, page_type, job_id):
    global data_deeplink
    data_deeplink = get_handle_tep_deeplink_url(task, site, terminal, page_type, job_id)
    goods_ids = [list(item.keys())[0] for item in data_deeplink]
    return goods_ids


def get_tep_deeplink_url(target_goods_id):
    # 循环遍历列表中的每个字典
    for item in data_deeplink:
        # 检查目标goods_id是否在字典的键中
        if target_goods_id in item:
            # 获取与目标goods_id对应的wrclink链接
            wrclink = item[target_goods_id]
            market_data["link"] = wrclink
            return wrclink


def get_handle_tep_m2a_url(task, site, terminal, page_type, job_id):
    headers = {
        'Authorization': authorization,
    }

    params = {
        'taskId': task,
        'site': site,
        'pageType': page_type,
        'terminal': terminal,
        'jobId': job_id,
    }
    market_data["site"] = site
    market_data["terminal"] = terminal
    market_data["pageType"] = page_type
    response = requests.get('https://tep.wrccorp.cn/api/testing/marketLink', params=params, headers=headers).json()
    logger.info(f"接口返回数据Kafka-m2a消息数据{response}")
    out_in = []
    for item in response:
        output = []
        if isinstance(item, dict):
            for s in item['link'].split("?")[1].split("&"):
                if 'ad_type=' in s or 'goods_id=' in s:
                    output.append(s)
            str_info = {'&'.join(output): item['link']}
            out_in.append(str_info)
    return out_in


def get_tep_m2a_goods_ids(task, site, terminal, page_type, job_id):
    global data_m2a
    data_m2a = get_handle_tep_m2a_url(task, site, terminal, page_type, job_id)
    goods_ids = [list(item.keys())[0] for item in data_m2a]
    return goods_ids


def get_tep_m2a_url(target_goods_id):
    # 循环遍历列表中的每个字典
    for item in data_m2a:
        # 检查目标goods_id是否在字典的键中
        if target_goods_id in item:
            # 获取与目标goods_id对应的wrclink链接
            wrclink = item[target_goods_id]
            market_data["link"] = wrclink
            return wrclink


def pytest_generate_tests(metafunc):
    if "test_marketing_cases" in metafunc.module.__file__:
        task = metafunc.config.getoption("--task")  # 获取输入task_id参数值
        site = metafunc.config.getoption("--site")  # 获取输入--site参数值
        job_id = metafunc.config.getoption("--job")  # 获取输入--site参数值
        if "params_m2a" in metafunc.fixturenames:
            terminal = "m2a"  # 获取输入参数值
            page_type = '1'
            params = get_tep_m2a_goods_ids(task, site, terminal, page_type, job_id)
            metafunc.parametrize('params_m2a', params)
        elif "params_link" in metafunc.fixturenames:
            terminal = "app"  # 获取输入参数值
            page_type = '2'
            params = get_tep_deeplink_goods_ids(task, site, terminal, page_type, job_id)
            metafunc.parametrize('params_link', params)


def resize_image(image_path, out_path=None, scale_factor=0.5, quality=70):
    # 读取图片
    img = cv2.imread(image_path)

    # 计算新的分辨率
    new_width = int(img.shape[1] * scale_factor)
    new_height = int(img.shape[0] * scale_factor)

    # 调整尺寸，使用 INTER_AREA 插值算法
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    if out_path is None:
        out_path = image_path
    # cv2.imwrite(out_path, resized_img)
    cv2.imwrite(out_path, resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])


def get_new_img_files(path, old_files):
    """压缩图片"""
    start_time = time.time()
    logger.info("开始压缩，图片数量：%s张" % len(old_files))
    new_files = []
    for i in old_files:
        new_img = i.split('.')[0] + ".jpg"
        resize_image(path + '/' + i, out_path=path + '/' + new_img)
        new_files.append(new_img)
    logger.info("压缩完成，累计耗时：%s秒" % (time.time() - start_time))
    return new_files


def compress_single_img(file_name):
    """压缩单张图片"""
    resize_image(file_name)


def upload_image_by_file_name(file_name):
    """更新图片到图片服务器,并且返回url list"""
    image_url = ""
    payload = {'pathFlag': 'testimg'}
    fo = open(f'{file_name}', 'rb')
    try:
        compress_single_img(file_name)
        file_short_name = file_name.split("/")[-1]
        file_info = [('image', (f'{file_short_name}', fo, 'image/png'))]
        data = requests.request("POST", URL_IMAGE, data=payload, files=file_info)
        sta_code = data.status_code
        if sta_code == 200:
            data_json = data.json()
            logger.info(f"接口返回数据:{data_json}")
            result = data_json.get('result')
            if result:
                image_url = result[0].get('path')
                # 删除该文件
                os.remove(file_name)
            else:
                logger.info(f"图片上传接口返回json{data_json}异常,没有图片结果。")
        else:
            image_url = "upload failed"
            logger.info(f"图片上传接口返回code{sta_code}异常")
    except Exception as e:
        image_url = "upload failed"
        logger.exception("图片读取上传异常", e)
    finally:
        fo.close()
    return image_url


class GenerateReport(object):
    lgs = []
    pocodriver = None

    def __init__(self, config):
        self.screenshots_size = {"width": "375px", "height": "667px"}
        self.config = config
        self.report = dict()
        self.image = list()
        self.report_info = dict()
        self.test_case = dict()
        self.failureMessages = dict()
        self.report_cls = Report
        self.failure = FailureMessages
        self.status_int = StatusInt
        self.when_info = WhenInfo
        self.case_settings = dict()
        self.parser = PytestParser(
            report=self.config.getoption("--report"),
            terminal=self.config.getoption("--terminal"),
            browser=self.config.getoption("--browser"),
            uuid=self.config.getoption("--udid"),
            local=self.config.getoption("--local"),
            brand=self.config.getoption("--brand"),
            site=self.config.getoption("--site"),
            password=self.config.getoption("--password"),
            email=self.config.getoption("--email"),
            host=self.config.getoption("--host"),
            port=self.config.getoption("--port"),
            wda_port=self.config.getoption("--extendPort"),
            device_version=self.config.getoption("--deviceVersion"),
            device_name=self.config.getoption("--deviceName"),
            bundle_id=self.config.getoption("--bundleId"),
            job_id=self.config.getoption("--job"),
            task_id=self.config.getoption("--task"),
            app_key=self.config.getoption("--appKey"),
            user_proxy=self.config.getoption("--useProxy"),
            tep_env=self.config.getoption("--tepEnv"),
            event_tracking=self.config.getoption("--eventTracking"),
            extraParams=self.config.getoption("--extraParams"),
            coverage_enable=self.config.getoption("--coverageEnable"),
            app_pack=self.config.getoption("--appPack"),
            app_activity=self.config.getoption("--appActivity"),
        )

    def get_case_settings(self):
        path = f"./src/resources/case_settings.yaml"
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            return data
        else:
            return {}

    def assert_upload_images(self, status_info):
        """判断成功/失败传图数量"""

        path = f"./result/screenshots"
        target_path = f"./result/target_screenshots"  # 指定目标截图文件夹
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        files = os.listdir(path)
        files.sort()
        num_images = 10
        total_images = len(files)
        if total_images > 0:
            if status_info == self.status_int.success.value:  # 成功随机取1张数据
                if os.path.exists(target_path):  # 判断有指定目标截图文件夹
                    target_files = os.listdir(target_path)
                    target_files.sort()
                    files = files[-1:]
                    files = get_new_img_files(path, files)  # 压缩图片
                    self.upload_images_url(path, files)  # 上传图片
                    target_files = get_new_img_files(target_path, target_files)
                    self.upload_images_url(target_path, target_files)  # 上传制定目标图片
                else:
                    files = files[-1:]
                    # if total_images > num_images:
                    #     interval = (total_images - 1) // (num_images - 1)
                    #     files = [files[i * interval] for i in range(num_images)]
                    #     files = files[:num_images]
                    files = get_new_img_files(path, files)
                    self.upload_images_url(path, files)
            elif status_info == self.status_int.fail.value:  # 失败取最后10张数据
                if total_images > num_images:
                    files = files[-10:]
                files = get_new_img_files(path, files)
                self.upload_images_url(path, files)
            else:
                logger.info(
                    f"该状态是:{status_info}---目前支持的上传的图片状态成功[3]/失败[1]，其他状态不执行上传图片到服务器")
        else:
            lg(f"没有获取到图片，截图异常")
            shutil.rmtree(path)
            logger.info(f"没有获取到图片，截图异常")

    def upload_report(self):
        """更新上传报告信息"""

        if self.parser.report == "local":
            path = f"./result/report/{self.parser.terminal}/{self.parser.site}"
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            report_name = f"{path}/{time.time()}.json"
            with open(report_name, "w", encoding="utf-8") as report:
                json.dump(self.report_info, report, ensure_ascii=False)
        else:
            logger.info(f"上传新报告的数据是:{json.dumps(self.report_info, ensure_ascii=False)} 结果")
            try:
                if self.parser.tep_env == "test":
                    URL = 'http://tep-test.wrccorp.cn'  # tep测试环境域名
                else:
                    URL = 'http://tep.wrccorp.cn'  # tep生产环境域名
                # r = requests.post(f"{URL}/testing/report/record",
                #                   json=self.report_info,
                #                   headers={"Authorization": "%s" % authorization})
                r = requests.post(f"{URL}/api/testing/report/record",
                                  json=self.report_info,
                                  headers={"Authorization": "%s" % authorization})
                logger.info(f"新报告json数据上传完成, 返回的结果:{r.text}")
            except Exception as e:
                logger.info(f"上传接口的异常是:{e}")
        self.report_info.clear()
        self.failureMessages.clear()
        self.lgs.clear()
        self.image.clear()

    def upload_images_url(self, path, files):
        """更新图片到图片服务器"""

        # for file in files:
        #     compress_img_PIL_info(f'{path}/{file}')
        payload = {'pathFlag': 'testimg'}
        for file in files:
            fo = open(f'{path}/{file}', 'rb')
            # logger.info(f"上传的图片是:{fo}")
            try:
                file_info = [('image', (f'{file}', fo, 'image/png'))]
                data = requests.request("POST", URL_IMAGE, data=payload, files=file_info)
                sta_code = data.status_code
                if sta_code == 200:
                    data_json = data.json()
                    logger.info(f"接口返回数据:{data_json}")
                    result = data_json.get('result')
                    if result:
                        img_url = result[0].get('path')
                        # logger.info(f"图片地址=={img_url}")
                        self.image.append(img_url)
                    else:
                        logger.info(f"图片上传接口返回json{data_json}异常,没有图片结果。")
                else:
                    logger.info(f"图片上传接口返回code{sta_code}异常")
            except Exception as e:
                logger.exception("图片读取上传异常", e)
            finally:
                fo.close()
        self.report_info[self.report_cls.images.value] = self.image
        if self.parser.report == "remote":
            try:
                shutil.rmtree(path)
                logger.info("图片文件夹已清空")
            except OSError as e:
                logger.exception(e)
        else:
            logger.info("本地文件不删除")

    def driver_exception(self, call, rep):
        """
        web异常名称
        """

        name = call.excinfo.typename
        self.failureMessages[self.failure.cause.value] = f"新报告异常用例:{rep.head_line}, 异常报错名称:{name}"
        logger.info(f"异常的name是:{name}")

    def pytest_collection(self, session):
        """
        测试开始-设备还没有打开
        :param session:
        :return:
        """
        sta = session.exitstatus
        logger.info(f"pytest_collection-用例收集的状态{sta}")

    def pytest_collection_finish(self, session):
        """
        测试开始前-设备还没有打开
        :param session:
        :return:
        """

        sta = session.exitstatus
        logger.info(f"pytest_collection_finish-用例收集的完成状态---{sta}")

    def pytest_runtest_logstart(self, nodeid, location):
        """
        测试开始前-设备还没有打开
        :param nodeid:
        :param location:
        :return:
        """

        logger.info(f"pytest_runtest_logstart---{nodeid}")

    def pytest_runtest_logfinish(self, nodeid, location):
        """
        测试设备已经退出--
        :param nodeid:
        :param location:
        :return:
        """
        logger.info(f"pytest_runtest_logfinish---{nodeid}")

    def pytest_runtest_setup(self, item):
        """
        测试开始-设备准备打开
        :param item:
        :return:
        """
        logger.info(f"pytest_runtest_setup")
        global event_track_param, session_value  # 全局变量

        case_data = self.get_case_settings()
        if item.name in case_data:
            self.case_settings = case_data[item.name]
        else:
            self.case_settings = dict()

        terminal = item.config.option.terminal
        brand = item.config.option.brand.lower()
        test_brand = brand + "-" + terminal

        etp_case_list = None
        session = None
        # test_name = item.obj.__doc__
        # upload_util.upload_test_case(test_name=test_name, test_args=item.nodeid,
        #                              test_brand=test_brand)
        try:
            app_id = self.get_app_id(test_brand=test_brand)
            test_string = item.nodeid
            # 判断是否包含 'test_event_track' 目录
            if test_string.find('test_event_track') != -1:
                param = item.nodeid
                if '[' in param:
                    param = item.nodeid.split("[")[0]  # 解决test_page_goods_detail_click_auto_block_main[login0]用例绑定异常处理
                try:
                    etp_case_list, session = self.get_tep_response_data(query_param=param, app_id=app_id)
                except:
                    logger.info(f"{param}没有绑定etp规则")
            elif 'mock' in test_string:
                characters = string.ascii_letters + string.digits
                session = ''.join(random.sample(characters * 3, 24))
            else:
                etp_case_list = ''
                logger.info("不包含 'test_event_track' 目录，功能用例")
            session_value = session  # session赋值
        except AttributeError as e:
            logger.info(f"获取TEP埋点用例AttributeError，异常信息：{e}")
        except IndexError as e:
            logger.info(f"获取TEP埋点用例IndexError，异常信息：{e}")

        try:
            # iOS埋点传参为json格式 {"env": {"auto_test_args": "商详分组$_session值"}}一期
            # event_track_param = etp_case_list[0] + "$_" + session
            # event_track_param = {"env": {"auto_test_args": event_track_param}}
            # logger.warning(f"event_track={event_track_param}")
            # iOS埋点传参为json格式:'auto_test_args' = {str) “6617b577e4b03043746b651f＄_ios-卡支付页点击点击事件＄_ios-卡支付页页面埋点 二期
            # iOS埋点传参为json格式（Mock格式）:'auto_test_args' = {str) “925$_6617b577e4b03043746b651f＄_ios-卡支付页点击点击事件＄_ios-卡支付页页面埋点 三期
            # iOS埋点传参为json格式:'auto_test_args' = {str) “$_67da633be4b0f4c51b5cdcac$_$_ios-卡支付页页面埋点（支持deeplink，onelink在链接中自定义校验规则，写在token后的$_后，$_可不填但不可省略）四期
            mock_id = ""  # 暂时为空
            if "^" in item.obj.__doc__:
                mc_id = item.obj.__doc__.split("^")[-1]
                if mc_id:
                    mock_id = mc_id
            if item.config.option.terminal == "ios":  # 终端iOS
                etp_case_list_str = ''
                if etp_case_list:
                    for i in range(len(etp_case_list)):
                        etp_case_list_str += "$_" + etp_case_list[i]
                else:
                    etp_case_list_str = "$_" + "mock-function"
                key = "$_" + session + etp_case_list_str
                index = key[1:].index("$")
                key = key[:index + 1] + "$_" + key[index + 1:]
                if mock_id:
                    event_track_param = mock_id + key
                else:
                    event_track_param = key
                event_track_param = {"env": {"auto_test_args": event_track_param}}
                logger.warning(f"event_track={event_track_param}")
            else:
                # Android传参为字符串，且需要转义。支持1条埋点自动化用例绑定1个或多个ETP用例。
                # "--es env {\"auto_test_args\":[\"商详-商详分组\"]\\,\"session\":\"session值\"}"
                # event_track_param = "--es env {'auto_test_args':[" + etp_case_list_str + "],'session':'" + session + "','mock_id':'" + mock_id + "'}"
                etp_case_list_str = ''
                if etp_case_list:
                    for i in etp_case_list:
                        i = "'" + i + "',"  # 列表元素遍历并拼接为字符串
                        etp_case_list_str += i
                    etp_case_list_str = etp_case_list_str[:-1]  # 字符串截取
                    etp_case_list_str = etp_case_list_str.replace(" ", "\\ ")  # 为用例中的空格添加转义

                else:
                    etp_case_list_str = "$_" + "mock-function"
                event_track_param = "--es env {'auto_test_args':[" + etp_case_list_str + "],'session':'" + session + "','group_list':['android端自动化公共字段：android_autoest_common_fields']}"
                if mock_id:
                    event_track_param = "--es env {'auto_test_args':[" + etp_case_list_str + "],'session':'" + session + "','mock_id':'" + mock_id + "'}"
                # logger.warning(f"转义前event_track={event_track_param}")
                event_track_param = event_track_param.replace("'", "\\'").replace(",", "\\,")  # 为埋点参数中的的引号、逗号添加转义
                # logger.warning(f"转义后event_track={event_track_param}")
        except TypeError as e:
            logger.info(f"获取埋点参数TypeError，异常信息：{e}")
        except IndexError as e:
            logger.info(f"获取埋点参数IndexError，异常信息：{e}")

        if item.own_markers:
            if item.own_markers[0].name == "important":
                logger.info(item.own_markers[0].name)
                self.report_info[self.report_cls.important.value] = True
        else:
            self.report_info[self.report_cls.important.value] = False
        # test_name = item.obj.__doc__
        # class_doc =item.parent.obj.__doc__

        # upload_util.upload_test_case(test_name=test_name, test_args=item.nodeid,
        #                              test_brand=test_brand)
        # upload_util.UploadCase().send_case("tests")
        # if terminal == "ios":
        #     host = item.config.option.host
        #     uuid = item.config.option.udid
        #     IosShell.ios_remove_proxy(server_host=host, server_port="8429", uuid=uuid)
        names = item.nodeid.split("::")
        class_name = names[-2]
        methodName = names[-1]
        if 'ad_type' in methodName:
            description_name = item.obj.__doc__ + methodName.split("[")[1].split("]")[0]
            method_name = methodName.replace('[', '_').split("]")[0]
        else:
            description_name = item.obj.__doc__
            method_name = methodName
        self.report_info[self.report_cls.class_name.value] = class_name
        self.report_info[self.report_cls.method_name.value] = method_name
        self.report_info[self.report_cls.description.value] = description_name
        # self.report_info[self.report_cls.important.value] = False
        # self.report_info["images"] = []
        self.report_info[self.report_cls.job_id.value] = self.parser.job_id
        self.report_info[self.report_cls.app_key.value] = self.parser.app_key
        self.report_info[self.report_cls.task_id.value] = self.parser.task_id
        # self.report_info[self.report_cls.start_date.value] = datetime.now().astimezone().isoformat(
        #     timespec='milliseconds')
        self.report_info[self.report_cls.start_date.value] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.report_info[self.report_cls.site.value] = self.parser.site
        self.report_info[self.report_cls.session.value] = session  # 获取session，请求tep获取
        self.report_info[self.report_cls.etp_case_list.value] = etp_case_list
        logger.info("测试启动")
        sotest_id_mark = item.get_closest_marker("sotest")
        sotest_id = sotest_id_mark.kwargs.get("id") if sotest_id_mark else ""
        self.report_info["sotestId"] = ",".join(sotest_id) if sotest_id else ""
        run_mark = item.get_closest_marker("run")
        if run_mark and run_mark.kwargs:
            brand = run_mark.kwargs.get("brand")
            site = run_mark.kwargs.get("site")
            if reversed and isinstance(reversed, bool):
                if brand and isinstance(brand, str) and self.parser.brand == brand:
                    self.report_info["logger"] = f"brand不符合执行条件，当前是：{self.parser.brand}，条件是：非{brand}"
                    self.report_info[self.report_cls.status.value] = self.status_int.skip.value
                    pytest.skip("brand不符合执行条件")
                if site and isinstance(site, list) and self.parser.site in site:
                    self.report_info["logger"] = f"站点不符合执行条件，当前是：{self.parser.site}，条件是：非{site}"
                    self.report_info[self.report_cls.status.value] = self.status_int.skip.value
                    pytest.skip("站点不符合执行条件")
            else:
                if brand and isinstance(brand, str) and self.parser.brand != brand:
                    self.report_info["logger"] = f"brand不符合执行条件，当前是：{self.parser.brand}，条件是：{brand}"
                    self.report_info[self.report_cls.status.value] = self.status_int.skip.value
                    pytest.skip("brand不符合执行条件")
                if site and isinstance(site, list) and self.parser.site not in site:
                    self.report_info["logger"] = f"站点不符合执行条件，当前是：{self.parser.site}，条件是：{site}"
                    self.report_info[self.report_cls.status.value] = self.status_int.skip.value
                    pytest.skip("站点不符合执行条件")

    def pytest_runtest_call(self, item):  # 中
        """
        测试中-设备已打开
        :param item:
        :return:
        """

        logger.info(f"pytest_runtest_call---初始化完成，开始执行用例:{item.originalname}")

    def pytest_runtest_teardown(self, item, nextitem):
        """
        测试app-已经准备退出/-设备
        :param item:
        :param nextitem:
        :return:
        """
        if "className" in self.report_info.keys():
            steps = copy.deepcopy(self.lgs)
            if self.report_info.get(self.report_cls.status.value) != self.status_int.skip.value:
                self.report_info[self.report_cls.logger.value] = "".join(steps)
            else:
                self.report_info[self.report_cls.status.value] = 3  # 平台展示跳过的用例会有异常，故先改成功
            self.report_info[self.report_cls.failure_messages.value] = self.failureMessages
        else:
            self.report_info[self.report_cls.logger.value] = ""
        self.lgs.clear()
        logger.info("测试结束")

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """
        测试收集-测试设备已打开
        :param item:
        :param call:
        :return:
        """
        outcome = yield
        rep = outcome.get_result()
        if rep.when == self.when_info.setup.value:
            logger.info("准备启动。。。。")
        elif rep.when == self.when_info.call.value:
            # self.report_info[self.report_cls.end_date.value] = datetime.now().astimezone().isoformat(
            #     timespec='milliseconds')
            self.report_info[self.report_cls.end_date.value] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.report_info[self.report_cls.martet_link_data.value] = market_data
            logger.info("测试结束，准备关闭")
            if rep.outcome == self.when_info.failed.value:
                self.report_info[self.report_cls.status.value] = self.status_int.fail.value  # 失败状态1, 接口定义
                self.failureMessages[self.failure.type_info.value] = self.status_int.fail.value  # 默认状态1, 接口定义
                if "_ _ _" in rep.longreprtext:
                    self.failureMessages[self.failure.content.value] = rep.longreprtext.split(
                        "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")[1]
                else:
                    self.failureMessages[self.failure.content.value] = rep.longreprtext
                self.driver_exception(call, rep)
            elif rep.outcome == "skipped":
                self.report_info[self.report_cls.status.value] = self.status_int.success.value  # 平台展示会有异常，故先改成功
            elif rep.outcome == "passed":
                self.report_info[self.report_cls.status.value] = self.status_int.success.value
            else:
                self.report_info[self.report_cls.status.value] = self.status_int.fail.value
        elif rep.when == self.when_info.teardown.value:
            status = self.report_info.get(self.report_cls.status.value)
            self.report_info[self.report_cls.martet_link_data.value] = market_data
            if status not in [self.status_int.fail.value, self.status_int.success.value, self.status_int.skip.value]:
                self.report_info[self.report_cls.status.value] = self.status_int.fail.value
                self.failureMessages[self.failure.type_info.value] = self.status_int.fail.value
                if rep.longreprtext == str():
                    if rep.caplog != str():
                        self.failureMessages[
                            self.failure.content.value] = f"异常的用例:{rep.head_line},报错日志:{rep.caplog}"
                        self.failureMessages[
                            self.failure.cause.value] = f"异常的用例:{rep.head_line},报错日志:{rep.caplog.split(':')[-1]}"
                    else:
                        self.failureMessages[
                            self.failure.content.value] = f"请检查服务:{self.parser.host}:{self.parser.port}是否启动。或者检查网络/浏览器异常关闭"
                        self.failureMessages[
                            self.failure.cause.value] = f"异常的用例:{rep.head_line},pytest框架初始化驱动失败"
                else:
                    self.failureMessages[self.failure.content.value] = rep.longreprtext.split(
                        "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")[1]
                    self.failureMessages[self.failure.cause.value] = f"异常的用例:{rep.head_line}"
                # self.report_info[self.report_cls.end_date.value] = datetime.now().astimezone().isoformat(
                #     timespec='milliseconds')
                self.report_info[self.report_cls.end_date.value] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                status = self.status_int.fail.value

            self.report_info[self.report_cls.session.value] = session_value  # session全局变量
            logger.info(f"session_value={session_value}")
            if self.parser.report == "remote":
                self.assert_upload_images(status)
                self.upload_report()

    def pytest_deselected(self, items):
        """
        测试开始前-设备还没有打开
        :param items:
        :return:
        """

        # for i in range(len(items)):
        logger.info(f"忽略或者是未选中要执行的测试用例第pytest_deselected")

    def pytest_report_header(self, config, start_path):
        """
        测试开始前-设备还没有打开
        :param config:
        :param start_path:
        :return:
        """
        project_name = start_path.name
        path = start_path
        tup = config.invocation_params.args
        for everyOne in tup:
            logger.info(f"执行参数是{everyOne}")
        logger.info(f"执行项目名称是{project_name}, 执行项目的目录是:{path}")

    # def pytest_report_collectionfinish(self, config, start_path, startdir, items):
    #     """
    #     测试开始前/后-设备没有打开
    #     :param config:
    #     :param start_path:
    #     :param startdir:
    #     :param items:
    #     :return:
    #     """
    #     # if items != None:
    #     #     for i in range(len(items)):
    #     #         logger.info(f"执行用例名称{items[i].name}")
    #     # else:
    #     #     logger.info(f"没有可执行的用例")
    #     logger.info(f"代码所处的文件夹位置:---{start_path}---代码所处的文件夹路径:{startdir}")

    def pytest_report_teststatus(self, report, config):
        """
        测试中-设备已打开一会
        :param report:
        :param config:
        :return:
        """

        if report.outcome == 'passed':
            logger.info(f"执行启动状态通过")
        if report.skipped is False:
            logger.info("执行启动状态用例没有跳过")


    def pytest_runtest_logreport(self, report):
        """
        测试中-设备已打开，上传报告
        :param report:
        :return:
        """

        logger.info(f"pytest_runtest_logreport-{report.outcome}")

    def init_driver(self):
        """
        初始化驱动
        :return:
        """
        logger.info("init_driver")
        terminal = self.parser.terminal.lower()
        browser = self.parser.browser.lower()
        uuid = self.parser.uuid
        site = self.parser.site.upper()
        host = self.parser.host
        port = self.parser.port
        wda_port = self.parser.wda_port
        device_version = self.parser.device_version
        device_name = self.parser.device_name
        language = LanguageUtil().language_info(site)
        country = LanguageUtil().country_info(site)
        logger.warning(f"全局变量event_track={event_track_param}")
        lg(f"设备id {uuid}, 服务器IP {host}, 设备端口 {port}, 转发端口 {wda_port}, 执行的站点 {site}, 邮箱 {self.parser.email}, 密码 {self.parser.password}")
        if terminal == "android":
            if self.parser.app_pack and self.parser.app_activity:
                app_package = self.parser.app_pack
                app_activity = self.parser.app_activity
            elif self.parser.brand == "ROMWE":
                app_package = "com.romwe"
                app_activity = 'com.romwe.work.home.SplashUI'
            else:
                app_package = "com.zzkko"
                app_activity = 'com.wrc.welcome.WelcomeActivity'
            self.driver = AndroidDriver().app_remote(uuid=uuid, language=language, country=country, host=host,
                                                     port=port,
                                                     wdaPort=wda_port, deviceName=device_name,
                                                     deviceVersion=device_version, appPackage=app_package,
                                                     appActivity=app_activity, event_tracking=event_track_param)
            return self.driver
        elif terminal == "ios":
            pass
        elif terminal == "pc":
            brs = {
                "1": "safari",
                "2": "chrome",
                "3": "firefox",
                "4": "edge",
                "5": "ie",
            }[browser]
            self.driver = BrowserDriver(name=brs).web_remote()
            return self.driver
        else:
            raise NameError(f"请输入正确参数。 选项有：ios、android、pc")

    def ios_init_driver(self):
        """
        初始化驱动
        :return:
        """
        logger.info("ios_init_driver")
        terminal = self.parser.terminal.lower()
        browser = self.parser.browser.lower()
        uuid = self.parser.uuid
        site = self.parser.site.upper()
        host = self.parser.host
        port = self.parser.port
        wda_port = self.parser.wda_port
        device_version = self.parser.device_version
        device_name = self.parser.device_name
        language = LanguageUtil().language_info(site)
        bundle_id = self.case_settings.get("bundle_id") or self.parser.bundle_id
        logger.warning(f"全局变量event_track={event_track_param}")
        # lg(f"设备id {uuid}, 服务器IP {host}, 设备端口 {port}, 转发端口 {wda_port}, 执行的站点 {site}, 邮箱 {self.parser.email}, 密码 {self.parser.password}")
        if terminal == "ios":
            if self.parser.brand == "ROMWE":
                bundle_id = "com.romwe.dotfashion"
            self.driver = IOSDriver().app_remote(uuid=uuid, language=language, host=host, port=port, wdaPort=wda_port,
                                                 deviceName=device_name,
                                                 deviceVersion=device_version, bundleId=bundle_id,
                                                 event_tracking=event_track_param)
            return self.driver
        elif terminal == "android":
            pass
        elif terminal == "pc":
            brs = {
                "1": "safari",
                "2": "chrome",
                "3": "firefox",
                "4": "edge",
                "5": "ie",
            }[browser]
            self.driver = BrowserDriver(name=brs).web_remote()
            return self.driver
        else:
            raise NameError(f"请输入正确参数。 选项有：ios、android、pc")

    @pytest.fixture(autouse=True, scope="module")
    def driver(self):
        """
        驱动
        :return:
        """
        logger.info("driver,module级别")
        try:
            global driver
            driver = self.init_driver()
            yield driver
            ObjectPage(driver).screenshot_info()
            if hasattr(driver, 'context'):
                if self.parser.terminal == "android":
                    if self.parser.app_pack and self.parser.app_activity:
                        app_id = self.parser.app_pack
                    elif self.parser.brand == "ROMWE":
                        app_id = "com.romwe"
                    else:
                        app_id = "com.zzkko"
                else:
                    if self.parser.brand == "ROMWE":
                        app_id = "com.romwe.dotfashion"
                    else:
                        app_id = "zzkko.com.ZZKKO"
                if self.parser.terminal != "android":
                    driver.terminate_app(app_id)
                driver.quit()
        except BaseException as ex:
            print(ex)
            raise ex

    @pytest.fixture(autouse=True, scope="function")
    def ios_driver(self):
        """
        驱动
        :return:
        """
        global newest_driver
        logger.info("ios_driver,function级别")
        try:
            ios_driver = self.ios_init_driver()
            newest_driver = ios_driver
            yield ios_driver
            ios_driver = newest_driver
            ObjectPage(ios_driver).screenshot_info()
            if hasattr(ios_driver, 'context'):
                if self.parser.terminal == "android":
                    if self.parser.brand == "ROMWE":
                        app_id = "com.romwe"
                    else:
                        app_id = "com.zzkko"
                else:
                    if self.parser.brand == "ROMWE":
                        app_id = "com.romwe.dotfashion"
                    else:
                        app_id = "zzkko.com.ZZKKO"
                ios_driver.terminate_app(app_id)
                ios_driver.quit()
        except BaseException as ex:
            print(ex)
            raise ex

    @pytest.fixture(scope="function")
    def pwa_driver(self):
        """切换pwa驱动"""
        browsers = "Chrome"
        uuid = self.parser.uuid
        site = self.parser.site.upper()
        host = self.parser.host
        port = self.parser.port
        from soium.webdriver.appium.webdriver import WebDriver
        pwa_webdriver = WebDriver(name=browsers)
        pwa_driver = pwa_webdriver.remote(host=host,
                                          port=port,
                                          udid=uuid,
                                          extendPort="",
                                          site=site)
        global driver
        driver = pwa_driver
        return driver

    @pytest.fixture(scope="module")
    def refresh_driver(self):
        """刷新APP驱动"""
        global driver
        driver = self.init_driver()
        return driver

    # @pytest.fixture(autouse=True, scope="function")
    # def poco_driver(self):
    #     """
    #     poco驱动
    #     :return:
    #     """
    #     if "airtest" in self.config.option.keyword:
    #         logger.info("poco start")
    #         connect_device("ios:///127.0.0.1:%s" % self.config.option.extendPort)
    #         self.pocodriver = iosPoco()
    #         return self.pocodriver

    @pytest.fixture
    def terminal(self):
        """
        终端
        :return:
        """
        return self.parser.terminal

    @pytest.fixture(autouse=True, scope="module")
    def job_id(self):
        """
        jobID
        :return:
        """
        return self.parser.job_id

    @pytest.fixture(autouse=True, scope="module")
    def email(self):
        """
        邮箱
        :return:
        """
        return self.parser.email

    @pytest.fixture(autouse=True, scope="module")
    def site(self):
        """
        站点
        :return:
        """
        return self.parser.site

    @pytest.fixture(autouse=True, scope="module")
    def password(self):
        """
        密码
        :return:
        """
        return self.parser.password

    @pytest.fixture(autouse=True, scope="module")
    def host(self):
        """
        服务器ip
        :return:
        """
        return self.parser.host

    @pytest.fixture(autouse=True, scope="module")
    def user_proxy(self):
        """
        用户代理
        :return:
        """
        return self.parser.user_proxy

    @pytest.fixture(autouse=True, scope="session")
    def user_uuid(self):
        """
        设备udid
        :return:
        """
        return self.parser.uuid

    @pytest.fixture(autouse=True, scope="session")
    def user_report(self):
        """
        用户报告
        :return:
        """
        return self.parser.report

    @pytest.fixture(autouse=True, scope="module")
    def task_id(self):
        """task id"""
        return self.parser.task_id

    @pytest.fixture(autouse=True, scope="session")
    def user_testname(self):
        """
        用例名称
        :return:
        """
        return self.config.option.keyword

    @pytest.fixture(autouse=True, scope="module")
    def coverage_enable(self):
        """
        覆盖率是否开启
        :return:
        """
        return self.parser.coverage_enable

    @pytest.fixture(autouse=True, scope="module")
    def extra_params(self):
        return self.parser.extraParams

    @pytest.fixture(autouse=True, scope="function")
    def set_capability_event(self, driver):
        """更新埋点参数，传递给脚本启动悬浮球，function级别"""
        terminal = self.parser.terminal.lower()
        if terminal == "android" and event_track_param is not None:
            driver.capabilities['optionalIntentArguments'] = event_track_param

    def get_tep_response_data(self, query_param, app_id):
        """
        请求TEP接口，获取ETP测试用例绑定关系及session
        param: query_param 用例方法名，相对路径，即item.nodeid；
        app_id: TEP测试平台app id
        return: etp_case_list, session
        """
        logger.info(f"请求TEP参数query_param: {query_param},app_id: {app_id}")
        # query_param = 'tests/test_event_track/test_good_details/test_goods_detail_core_event_track.py::TestGoodsDetailCoreEventTrack::test_page_goods_detail_page_view'
        querystring = {"parameters": query_param, "appId": app_id}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": authorization
        }
        response = requests.request("GET", TEP_TEST_ETP_URL, headers=headers, params=querystring)
        logger.info(f"TEP响应数据response={response.text}")
        lg(f"TEP响应数据response={response.text}")
        response_data = json.loads(response.text)  # 转为json
        logger.info(f"TEP响应数据data={response_data.get('data')}")
        # 获取 response_data 中的 'data' 字段
        data = response_data.get('data')

        # 判断 etp_case_list 是否为空，空则抛出异常
        etp_case_list = data.get('etp_case_list')
        if not etp_case_list:
            raise ValueError('绑定的埋点规则 is empty in the response data')

        # 判断 session 是否为空，空则抛出异常
        session = data.get('session')
        if not session:
            raise ValueError('启动Appium-session is empty in the response data')

        # 如果 etp_case_list 和 session 都不为空，继续处理它们的值
        etp_case_list = data.get('etp_case_list')
        session = data.get('session')
        return etp_case_list, session

    def get_app_id(self, test_brand='wrc-ios'):
        """获取app_id，避免TEP平台获取ETP用例重复"""
        if test_brand == "romwe-android":
            app_id = "1691333576202784768"
        elif test_brand == "wrc-android":
            app_id = "1636663249002958848"
        elif test_brand == "wrc-ios":
            app_id = "1565212314486050816"
        elif test_brand == "romwe-ios":
            app_id = "1565212314486050816"
        else:
            app_id = "1565212314486050816"
        # logger.info(f"test_brand={test_brand},app_id={app_id}")
        return app_id
