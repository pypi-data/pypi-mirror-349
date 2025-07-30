#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import time
from functools import wraps

import loguru
import requests

from swim.plugins.pytest_plugins import lg
from swim.utils.upload_util import authorization


def loge(info=None):
    """独立的日志记录"""
    if info is None:
        info = "日志里面没有信息"
    lg(info)


class LogInfoUtil(object):

    @staticmethod
    def time_this(func):
        """
        Decorator that reports the execution time.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # start = time.time()
            time_start = time.time()
            loguru.logger.info(f"函数开始执行:{time_start}")
            result = func(*args, **kwargs)
            # end = time.time()
            time_end = time.time()
            loguru.logger.info(f"函数执行完成:{time_end}")
            loguru.logger.info(f"函数名称:{func.__name__}, 执行的时间预计花费:{time_end - time_start}秒")
            return result

        return wrapper

    @staticmethod
    def logged(name=None, message=None):
        """
        Add logging to a function. level is the logging
        level, name is the logger name, and message is the
        log message. If name and message aren't specified,
        they default to the function's module and name.
        """

        def decorate(func):
            log_name = authorization if name else func.__name__
            # log_msg = message if message else func.__name__
            log_msg = message if message else func.__doc__

            @wraps(func)
            def wrapper(*args, **kwargs):
                # loge(f"执行名称:{func.__name__}, 执行信息:{log_msg}")
                loge(f"执行步骤:{log_msg}")
                loguru.logger.info(f"函数名称:{log_name}, 函数的描述名称:{log_msg}")
                # loguru.logger.info(f"函数名称:{func.__name__}")
                return func(*args, **kwargs)

            return wrapper

        return decorate


def tep_test_case(test_name="", test_module="", test_args="", author="", level="", cmdb_name="", cid="",
                  test_brand=None, name=None,
                  message=None):
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

    def decorate(func):
        log_name = name if name else func.__name__
        log_msg = message if message else func.__doc__
        url = "https://tep.wrccorp.cn/api/testing/testcase/upload"
        if test_brand == "rw-and":
            app_id = "1691333576202784768"
        elif test_brand == "she-and":
            app_id = "1636663249002958848"
        elif test_brand == "she-ios":
            app_id = "1565212314486050816"
        elif test_brand == "rw-ios":
            app_id = "1565212314486050816"
        else:
            app_id = "1565212314486050816"
        payload = {
            "name": test_name,
            "description": test_name,
            "parameters": test_args,
            "module": test_module,
            "sort": 200,
            "enabled": True,
            "caseUse": False,
            "appId": app_id
        }

        headers = {
            "content-type": "application/json",
            "authorization": authorization
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # loge(f"执行名称:{func.__name__}, 执行信息:{log_msg}")
            loge(f"执行步骤:{log_msg}")
            loguru.logger.info(f"函数名称:{log_name}, 函数的描述名称:{log_msg}")
            # loguru.logger.info(f"函数名称:{func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorate


