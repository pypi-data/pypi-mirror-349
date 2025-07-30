#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import copy
import json
import os
import pathlib
import pytest
import shutil
import time
from PIL import Image
from loguru import logger
from jsonpath import jsonpath
from urllib.parse import urlparse, parse_qs
from soium.support.constants import Header, Host, Uri
from soium.support.util import Util
from soium.plugins import PytestParser

URL_MAP = {
    "test": Host.TEP_TEST_URL,
    "release": Host.TEP_URL
}

driver_new = None  # 存放webdriver

etp_rules = {}  # 存放测试用例etp规则

specify_img_path = f"./result/specify_screenshots/"  # 存放软断言失败的截图
img_path = f"./result/screenshots/"  # 存放失败的截图


def pytest_addoption(parser):
    """
    https://docs.pytest.org/en/6.2.x/example/simple.html
    https://docs.pytest.org/en/6.2.x/reference.html
    :param parser:
    :return:
    """
    parser.addoption("--json_report", action="store", default="remote")  # 传入remote报告则发送远程服务器,local则创建本地报告.
    parser.addoption("--brand", action="store", default="wrc")
    parser.addoption("--site", action="store", default="US")
    parser.addoption("--browser", action="store", default=2)
    parser.addoption("--platform", action="store")
    parser.addoption("--host", action="store", default="127.0.0.1")  # mobile端传的
    parser.addoption("--port", action="store", default="4723")  # mobile端传的
    parser.addoption("--hub", action="store", default="127.0.0.1:4444")  # desktop端传的
    parser.addoption("--email", action="store", default="")
    parser.addoption("--password", action="store", default="")
    parser.addoption("--extendPort", action="store", default="")  # mobile端/iOS传的
    parser.addoption("--deviceName", action="store", default="")  # mobile端/iOS传的
    parser.addoption("--deviceVersion", action="store", default="")  # mobile端/iOS传的
    parser.addoption("--devicePlatform", action="store", default="")  # mobile端/iOS传的
    parser.addoption("--udid", action="store", default="")  # mobile端/iOS传的
    parser.addoption("--jobId", action="store", default="")
    parser.addoption("--taskId", action="store", default="388")
    parser.addoption("--appKey", action="store", default="wrc_pc")
    parser.addoption("--envTag", action="store", default="online")
    parser.addoption("--eventTracking", action="store", default="")
    parser.addoption("--tepEnv", action="store", default="release")
    parser.addoption("--extraParams", action="store", default="")


def pytest_configure(config):
    """允许插件和conftest文件执行初始配置。"""

    config.addinivalue_line(
        "markers", "important: test fail send message to WXWork"
    )
    config.addinivalue_line(
        "markers", "report: test case report to TEP"
    )
    config.addinivalue_line(
        "markers", "run: test case run conditions"
    )
    report = config.option.json_report
    if not report:
        return
    plugin = GenerateReport(config)
    config.report = plugin
    config.pluginmanager.register(plugin)


def pytest_unconfigure(config):
    """退出测试之前调用"""

    global driver_new
    plugin = getattr(config, "report")
    if plugin:
        del config.report
        config.pluginmanager.unregister(plugin=plugin)
    if driver_new:
        driver_new.quit()


def step(name):
    GenerateReport.lgs.append(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}-{name}\n')


def compress_img_PIL_info(file_name, compress_rate=1):
    """压缩图片"""

    img = Image.open(file_name)
    w, h = img.size
    img_resize = img.resize((int(w * compress_rate), int(h * compress_rate)))
    img_resize.save(file_name)
    logger.info("图片压缩完成")


def tep_test_case(test_name="", test_module="", test_args="", author="", level="P1", cmdb_name="", cid="",
                  test_platform=None, name=None, message=None, tep_env="release"):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    用例名称     name
    用例描述    description
    用例模块     module
    执行参数   parameters
    排序值   sort
    是否启用 enabled
    应用编号  appId
    过程管理使用 caseUse
    """

    url = URL_MAP[tep_env] + Uri.TESTCASE_UPLOAD
    app_id_map = {
        "PC": ["1553362379985784832", "1554383689478180864"],
        "PWA": ["1553362423820455936", "1556525945005936640"]
    }
    for app in app_id_map[test_platform.upper()]:
        payload = {
            "name": test_name,
            "description": test_name,
            "parameters": test_args,
            "module": test_module,
            "level": level,
            "sort": 200,
            "enabled": True,
            "caseUse": False,
            "appId": app
        }
        response = Util.basic_tep_request("POST", url, json=payload)
        logger.info("用例上报接口：" + response.text)


def tep_test_case_etp_rules(case_path=None, brand=None, test_platform=None, tep_env="release"):
    """获取tep测试用例对应etp规则"""

    global etp_rules
    res = None
    url = URL_MAP[tep_env] + Uri.TESTCASE_ETP
    app_id_map = {
        "wrc_PC": "1553362379985784832",
        "wrc_PWA": "1553362423820455936",
        "ROMWE_PC": "1554383689478180864",
        "ROMWE_PWA": "1556525945005936640"
    }
    app_name = brand + "_" + test_platform.upper()
    data = {
        "parameters": case_path,
        "appId": app_id_map[app_name],
    }
    res = Util.basic_tep_request("get", url, params=data)
    if res:
        etp_case_path = jsonpath(res, "$..case_parameters")[0]
        assert etp_case_path == case_path, "用例路径不一致"
        etp_rules["cases"] = jsonpath(res, "$..etp_case_list")[0]
        etp_rules["tokenId"] = jsonpath(res, "$..session")[0]
        etp_rules["__is_debug__"] = 0


def get_tep_marketing_url(task, job, site, terminal, page_type, tep_env="release"):
    """获取营销活动url"""

    # pageType:1（M2A）/2（直投）
    # terminal:pc/m/app
    # site:国家简称
    url = URL_MAP[tep_env] + Uri.MARKETING
    params = {
        'taskId': task,
        'jobId': job,
        'site': site,
        'pageType': page_type,
        'terminal': terminal,
    }
    result = Util.basic_tep_request("get", url, params=params)
    return result


def get_tep_marketing_url_goods_id(res):
    """获取营销活动链接中的goods_id"""

    good_ids = []
    for r in res:
        if isinstance(r, dict):
            # 获取查询参数
            params = parse_qs(urlparse(r["link"]).query)
            # 获取goods_id值
            goods_id = params.get("goods_id", [None])[0]
            good_ids.append(goods_id)
    return good_ids


def pytest_generate_tests(metafunc):
    """参数化"""

    if "test_marketing_m2a_new" in metafunc.function.__name__:
        task = metafunc.config.getoption("--taskId")
        job = metafunc.config.getoption("--jobId")
        site = metafunc.config.getoption("--site")
        terminal = "m2a" if metafunc.config.getoption("--platform") == "pwa" else "pc"
        if "marketing_m2a" in metafunc.fixturenames:
            page_type = '1'
            res = get_tep_marketing_url(task, job, site, terminal, page_type)
            goods = get_tep_marketing_url_goods_id(res)
            metafunc.parametrize('marketing_m2a', res, ids=goods)
        else:
            logger.info("暂不支持非m2a类型的链接")


class GenerateReport(object):
    lgs = []

    def __init__(self, config):
        self.failureMessages = {}
        self.config = config
        self.report_info = {}
        self.image = []
        self.browsers = {
            "1": "Safari",
            "2": "Chrome",
            "3": "Firefox",
            "5": "Edge",
            "6": "IE",
        }
        # self.screenshots_size = {"width": "100%", "height": "610px"}
        self.parser = PytestParser(
            report=self.config.getoption("--json_report"),
            brand=self.config.getoption("--brand"),
            site=self.config.getoption("--site"),
            browser=self.config.getoption("--browser"),
            platform=self.config.getoption("--platform"),
            host=self.config.getoption("--host"),
            port=self.config.getoption("--port"),
            hub=self.config.getoption("--hub"),
            email=self.config.getoption("--email"),
            password=self.config.getoption("--password"),
            extendPort=self.config.getoption("--extendPort"),
            deviceName=self.config.getoption("--deviceName"),
            deviceVersion=self.config.getoption("--deviceVersion"),
            devicePlatform=self.config.getoption("--devicePlatform"),
            udid=self.config.getoption("--udid"),
            jobId=self.config.getoption("--jobId"),
            taskId=self.config.getoption("--taskId"),
            envTag=self.config.getoption("--envTag"),
            appKey=self.config.getoption("--appKey"),
            eventTracking=self.config.getoption("--eventTracking"),
            tepEnv=self.config.getoption("--tepEnv"),
            extraParams=self.config.getoption("--extraParams"),
        )

    def pytest_runtest_setup(self, item):
        global specify_img_path
        names = item.nodeid.split("::")
        className = names[-2]
        methodName = names[-1]
        self.report_info["className"] = className
        self.report_info["methodName"] = methodName
        self.report_info["description"] = item.obj.__doc__
        self.report_info["important"] = False
        # self.report_info["images"] = []
        self.report_info["jobId"] = self.parser.jobId
        self.report_info["appKey"] = self.parser.appKey
        self.report_info["taskId"] = self.parser.taskId
        self.report_info["startDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.report_info["site"] = self.parser.site
        if "test_marketing_m2a_new" in methodName:
            self.report_info["methodName"] = methodName.split("[")[0]
            self.report_info["description"] = item.obj.__doc__ + "_" + methodName.split("[")[-1].split("]")[0]
            self.report_info["martetLinkData"] = item.callspec.params["marketing_m2a"]
        important_mark = item.get_closest_marker("important")
        if important_mark and important_mark.args[0]:
            self.report_info["important"] = True
        sotest_id_mark = item.get_closest_marker("sotest")
        sotest_id = sotest_id_mark.kwargs.get("id") if sotest_id_mark else ""
        self.report_info["sotestId"] = ",".join(sotest_id) if sotest_id else ""
        # report_mark = item.get_closest_marker("report")
        # jenkins_home = os.getenv("JENKINS_HOME")
        # logger.info(f"jenkins_home信息：{jenkins_home}")
        # if report_mark and report_mark.kwargs and not jenkins_home:  # jenkins上运行不上报用例
        #     report_mark.kwargs["test_args"] = item.nodeid
        #     report_mark.kwargs["test_name"] = item.obj.__doc__
        #     report_mark.kwargs["test_platform"] = self.parser.platform
        #     report_mark.kwargs["tep_env"] = self.parser.tepEnv
        #     tep_test_case(**report_mark.kwargs)
        run_mark = item.get_closest_marker("run")
        if run_mark and run_mark.kwargs:
            brand = run_mark.kwargs.get("brand")
            site = run_mark.kwargs.get("site")
            reversed = run_mark.kwargs.get("reversed")
            env = run_mark.kwargs.get("env")
            if reversed and isinstance(reversed, bool):
                if env and isinstance(env, str) and self.parser.envTag == env:
                    self.report_info["logger"] = f"env不符合执行条件，当前是：{self.parser.envTag}，条件是：非{env}"
                    pytest.skip("env不符合执行条件")
                if brand and isinstance(brand, str) and self.parser.brand == brand:
                    self.report_info["logger"] = f"brand不符合执行条件，当前是：{self.parser.brand}，条件是：非{brand}"
                    pytest.skip("brand不符合执行条件")
                if site and isinstance(site, list) and self.parser.site in site:
                    self.report_info["logger"] = f"站点不符合执行条件，当前是：{self.parser.site}，条件是：非{site}"
                    pytest.skip("站点不符合执行条件")
            else:
                if env and isinstance(env, str) and env != self.parser.envTag:
                    self.report_info["logger"] = f"env不符合执行条件，当前是：{self.parser.envTag}，条件是：{env}"
                    pytest.skip("env不符合执行条件")
                if brand and isinstance(brand, str) and self.parser.brand != brand:
                    self.report_info["logger"] = f"brand不符合执行条件，当前是：{self.parser.brand}，条件是：{brand}"
                    pytest.skip("brand不符合执行条件")
                if site and isinstance(site, list) and self.parser.site not in site:
                    self.report_info["logger"] = f"站点不符合执行条件，当前是：{self.parser.site}，条件是：{site}"
                    pytest.skip("站点不符合执行条件")
        if "test_event_track" in item.nodeid:
            tep_test_case_etp_rules(case_path=item.nodeid, brand=self.parser.brand, test_platform=self.parser.platform)
            self.report_info["session"] = etp_rules.get("tokenId") if etp_rules.get("tokenId") else ""
        pathlib.Path(specify_img_path).mkdir(parents=True, exist_ok=True)
        shutil.rmtree(specify_img_path)
        logger.info("测试启动-开始执行用例")

    def pytest_runtest_teardown(self, item):

        if "test_event_track" in item.nodeid:
            global etp_rules
            etp_rules = {}
        if "className" in self.report_info.keys():
            steps = copy.deepcopy(self.lgs)
            if self.report_info.get("status") != 2:
                self.report_info["logger"] = "".join(steps)
            self.report_info["failureMessages"] = self.failureMessages
        else:
            self.report_info["logger"] = ""
        self.lgs.clear()
        logger.info("测试结束")
        try:
            if "gray" in self.parser.envTag:
                global driver_new
                driver_new.execute_script("window.uploadCoverage(88888888);")
                time.sleep(5)
                logger.info("灰度环境覆盖率上报正常")
        except:
            logger.info("灰度环境覆盖率上报失败！！！！")

    def upload_report(self):
        """更新上传报告信息"""

        if self.parser.report == "local":
            path = f"./result/{self.parser.envTag}/report/{self.parser.brand}/{self.parser.platform}/{self.parser.site}"
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            report_name = f"{path}/{time.time()}.json"
            with open(report_name, "w", encoding="utf-8") as report:
                json.dump(self.report_info, report, ensure_ascii=False)
        else:
            logger.info(f"上传新报告的数据是:{self.report_info} 结果")
            url = URL_MAP[self.parser.tepEnv] + Uri.TESTCASE_REPORT
            r = Util.basic_tep_request("post", url, json=self.report_info)
            logger.info(f"新报告json数据上传完成, 返回的结果:{r}")
        self.report_info.clear()
        self.failureMessages.clear()
        self.lgs.clear()
        self.image.clear()

    def assert_upload_images(self, status_info):
        """判断成功/失败传图数量"""

        global img_path
        global specify_img_path
        pathlib.Path(img_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(specify_img_path).mkdir(parents=True, exist_ok=True)
        files = os.listdir(img_path)
        files.sort()
        specify_files = os.listdir(specify_img_path)
        specify_files.sort()
        num_images = 10
        total_images = len(files)
        if total_images > 0:
            if status_info == 3:  # 成功取最后1张数据
                # if total_images > num_images:
                #     interval = (total_images - 1) // (num_images - 1)
                #     files = [files[i * interval] for i in range(num_images)]
                #     files = files[:num_images]
                # self.upload_images_url(img_path, files)
                if len(specify_files) > 0:
                    self.upload_images_url(specify_img_path, specify_files)
                self.upload_images_url(img_path, files[-1:])
            elif status_info == 1:  # 失败取特定图片+最近图片，共10张
                if len(specify_files) == 0:
                    logger.info("不存在指定上传图片，只取10张最近图片")
                    if total_images > num_images:
                        files = files[-10:]
                    self.upload_images_url(img_path, files)
                elif len(specify_files) < num_images:
                    logger.info("存在指定上传图片，且小于10张，取指定图片+最近图片，共10张")
                    if total_images > (num_images - len(specify_files)):
                        files = files[-(num_images - len(specify_files)):]
                    self.upload_images_url(specify_img_path, specify_files)
                    self.upload_images_url(img_path, files)
                else:
                    logger.info("存在指定上传图片，大于等于10张，只取10张指定图片")
                    self.upload_images_url(specify_img_path, specify_files[-10:])
            else:
                logger.info(f"该状态是:{status_info}---目前支持的上传的图片状态成功[3]/失败[1]，其他状态不执行上传图片到服务器")
        else:
            step(f"没有获取到图片，截图异常")
            shutil.rmtree(img_path)
            shutil.rmtree(specify_img_path)
            logger.info(f"没有获取到图片，截图异常")

    def upload_images_url(self, path, files):
        """更新图片到图片服务器"""

        for file in files:
            compress_img_PIL_info(f'{path}/{file}')
        payload = {'pathFlag': 'testimg'}
        for file in files:
            fo = open(f'{path}/{file}', 'rb')
            try:
                file_info = [('image', (f'{file}', fo, 'image/png'))]
                url = Host.IMG_URL + Uri.IMG_SERVER_UPLOAD
                data = Util.basic_tep_request("POST", url, flag=2, data=payload, files=file_info)
                result = data.get('result')
                if result:
                    img_url = result[0].get('path')
                    logger.info(f"图片地址=={img_url}")
                    self.image.append(img_url)
                else:
                    logger.info(f"图片上传接口返回json：{data}异常,没有图片结果。")
            except Exception as e:
                logger.exception("图片读取上传异常", e)
            finally:
                fo.close()
        self.report_info["images"] = self.image
        if self.parser.report == "remote":
            try:
                shutil.rmtree(path)
            except OSError as e:
                logger.exception(e)
            else:
                logger.info("图片文件夹已清空")
        else:
            logger.info("本地文件不删除")

    def web_driver_exception(self, call, rep):
        """
        web异常名称
        """

        name = call.excinfo.typename
        self.failureMessages["cause"] = f"新报告异常用例:{rep.head_line}, 异常报错名称:{name}"
        logger.info(f"异常的name是:{name}")

    def case_result_solve_for_setup(self, rep):

        if rep.outcome == "skipped":
            self.report_info["status"] = 3
        else:
            self.report_info["status"] = 1

    def case_result_solve_for_call(self, call, rep):

        self.report_info["endDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info("测试结束，浏览器准备关闭")
        status_map = {"failed": 1, "skipped": 2, "passed": 3}
        if rep.outcome in status_map.keys():
            self.report_info["status"] = status_map[rep.outcome]
            if self.report_info["status"] == 1:
                self.failureMessages["type"] = 1  # 默认状态1, 接口定义
                if rep.longreprtext:
                    logger.info(f"报错日志: {rep.longreprtext}")
                    res_lst = self.failureMessages["content"] = rep.longreprtext.split(
                        "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ")
                    if len(res_lst) == 1:
                        self.failureMessages["content"] = res_lst[0]
                    elif len(res_lst) > 1:
                        self.failureMessages["content"] = res_lst[1]
                    else:
                        self.failureMessages["content"] = "结束报错内容为空"
                else:
                    self.failureMessages["content"] = "关闭报错内容为空"
                self.web_driver_exception(call, rep)
        else:
            self.report_info["status"] = 1

    def case_result_solve_for_teardown(self, rep):

        status = self.report_info.get('status')
        if status not in [1, 2, 3]:
            self.report_info["status"] = 1
            self.failureMessages["type"] = 1  # 默认状态1, 接口定义
            if rep.longreprtext == "":
                if rep.caplog != '':
                    self.failureMessages[
                        "content"] = f"异常的用例:{rep.head_line},报错日志:{rep.caplog},设备hub{self.parser.hub}"
                    self.failureMessages[
                        "cause"] = f"caplog不为空异常的用例:{rep.head_line},报错日志:{rep.caplog.split(':')[-1]}"
                else:
                    self.failureMessages[
                        "content"] = f"请检查selenium服务:,设备hub{self.parser.hub}是否启动。或者检查网络/浏览器异常关闭"
                    self.failureMessages["cause"] = f"caplog为空异常的用例:{rep.head_line},pytest框架初始化驱动失败"
            else:
                if rep.longreprtext:
                    logger.info(f"报错日志: {rep.longreprtext}")
                    res_lst = self.failureMessages["content"] = rep.longreprtext.split(
                        "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ")
                    if len(res_lst) == 1:
                        self.failureMessages["content"] = res_lst[0]
                    elif len(res_lst) > 1:
                        self.failureMessages["content"] = res_lst[1]
                    else:
                        self.failureMessages["content"] = "结束报错内容为空"
                else:
                    self.failureMessages["content"] = "结束报错内容为空"
                self.failureMessages[
                    "cause"] = f"longreprtext不为空异常的用例:{rep.head_line}, 设备hub{self.parser.hub}"
            self.report_info["endDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            status = 1
        self.assert_upload_images(status)
        self.upload_report()

    # @pytest.mark.hookwrapper(hookwrapper=True)
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, call):
        # execute all other hooks to obtain the report object


        outcome = yield
        rep = outcome.get_result()
        if rep.when == "setup":
            logger.info("浏览器准备启动。。。。")
            self.case_result_solve_for_setup(rep)
        elif rep.when == "call":
            self.case_result_solve_for_call(call, rep)
        elif rep.when == "teardown":
            self.case_result_solve_for_teardown(rep)

    def init_driver(self):
        """驱动"""

        browser = self.init_browser()
        site = self.parser.site
        udid = self.parser.udid
        hub = self.parser.hub
        host = self.parser.host
        port = self.parser.port
        envTag = self.parser.envTag
        extendPort = self.parser.extendPort
        deviceName = self.parser.deviceName
        deviceVersion = self.parser.deviceVersion
        devicePlatform = self.parser.devicePlatform
        if self.parser.platform == "pc":
            if self.parser.udid == "":
                driver = browser.remote(hub=hub, envTag=envTag, site=site)
            else:  # Ipad 端
                host, port = self.parser.hub.split(":")
                driver = browser.remote(host=host,
                                        port=port,
                                        udid=udid,
                                        extendPort=extendPort,
                                        deviceName=deviceName,
                                        deviceVersion=deviceVersion,
                                        platform=devicePlatform)
        elif self.parser.platform == "pwa":
            driver = browser.remote(host=host,
                                    port=port,
                                    udid=udid,
                                    extendPort=extendPort,
                                    deviceName=deviceName,
                                    deviceVersion=deviceVersion,
                                    platform=devicePlatform,
                                    envTag=envTag,
                                    site=site)
        else:
            raise NameError(f"请输入正确的platform。 选项有：pwa , pc")
        return driver

    def init_browser(self):
        browser = self.parser.browser
        platform = self.parser.platform
        udid = self.parser.udid
        browsers = self.browsers[str(browser)]
        if platform == "pc":
            if udid == "":
                from ..webdriver import Web
                driver = Web(name=browsers)
            else:
                from ..webdriver import App
                driver = App(name=browsers)
        else:
            from ..webdriver import App
            driver = App(name=browsers)
        return driver

    @pytest.fixture
    def driver(self):
        try:
            self._driver = self.init_driver()
            yield self._driver
            self._driver.quit()
        except BaseException as ex:
            print(ex)
            raise ex

    @pytest.fixture
    def new_driver(self):
        global driver_new
        try:
            if driver_new is None:
                driver_new = self.init_driver()
            else:  # 判断浏览器是否已启动，如浏览器异常关闭则下次重新启动
                driver_new.execute_script("javascript:void(0);")
            yield driver_new
        except Exception as e:
            exception_name = type(e).__name__
            logger.info(f"浏览器驱动启动异常：{exception_name}, 浏览器驱动信息：{driver_new}")
            logger.info(f"浏览器驱动报错信息：{e}")
            if exception_name not in ["NoSuchWindowException", "InvalidSessionIdException"]:
                if driver_new:
                    driver_new.quit()
            driver_new = None
            raise e

    @pytest.fixture
    def site(self):
        return self.parser.site

    @pytest.fixture
    def brand(self):
        return self.parser.brand

    @pytest.fixture
    def platform(self):
        return self.parser.platform

    @pytest.fixture
    def envTag(self):
        return self.parser.envTag

    @pytest.fixture
    def email(self):
        return self.parser.email

    @pytest.fixture
    def password(self):
        return self.parser.password

    @pytest.fixture
    def hub(self):
        platform = self.parser.platform
        if platform == "pc":
            return self.parser.hub
        elif platform == "pwa":
            return self.parser.host + ":" + self.parser.port

    @pytest.fixture
    def case_etp_rules(self):
        return etp_rules

    @pytest.fixture
    def job_id(self):
        return self.parser.jobId

    @pytest.fixture
    def extra_params(self):
        return self.parser.extraParams

    @pytest.fixture
    def device_info(self):
        if self.parser.platform == "pc":
            info = self.browsers[str(self.parser.browser)] + "_" + self.parser.hub
            return info
        elif self.parser.platform == "pwa":
            info = self.parser.devicePlatform + self.parser.deviceVersion + "_" + self.browsers[str(self.parser.browser)]
            return info

    @pytest.fixture
    def task_id(self):
        return self.parser.taskId

