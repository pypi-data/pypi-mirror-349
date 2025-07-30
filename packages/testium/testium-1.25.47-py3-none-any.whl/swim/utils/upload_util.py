# -*- coding:utf-8 -*-
import inspect
import os
from importlib import import_module
import yaml
import requests
import re
from loguru import logger
# import git
import json
from datetime import datetime


authorization = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbm9ueW1vdXNVc2VyIiwiYXV0aCI6InVzZXIiLCJpc3MiOiJzaGVpbiIsImV4cCI6NDEwMjMyOTYwMCwiaWF0IjoxNjUyNzY1NzU5fQ.UtLfIAWLHGtGvgPacPm4Ty_fwQeRmskVpvCwO86kdMU"


def upload_test_case(test_name="", test_module="", test_args="", author="", level="", cmdb_name="", cid="",
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

    url = "https://tep.wrccorp.cn/api/testing/testcase/upload"

    test_path = {
        "test_cases/test_checkout_pay": "功能-下单支付",
        "test_cases/test_customer_service_items": "功能-客服&客项",
        "test_cases/test_good_details": "功能-商品详情",
        "test_cases/test_home_navigation": "功能-首页&导航",
        "test_cases/test_list_search_recommend": "功能-列表&搜推",
        "test_cases/test_shopping_cart": "功能-购物车",
        "test_cases/test_user_member": "功能-用户&会员",
        "test_special_cases": "功能-特殊用例",
        "test_event_track/test_checkout_pay": "埋点-下单支付",
        "test_event_track/test_customer_service_items": "埋点-客服&客项",
        "test_event_track/test_good_details": "埋点-商品详情",
        "test_event_track/test_home_navigation": "埋点-首页&导航",
        "test_event_track/test_list_search_recommend": "埋点-列表&搜推",
        "test_event_track/test_shopping_cart": "埋点-购物车",
        "test_event_track/test_user_member": "埋点-用户&会员",

    }

    for key, value in test_path.items():
        if key in test_args:
            test_module = value
            break
    if test_module == "":
        test_module = "其他用例"

    if test_brand == "romwe-android":
        app_id = "1691333576202784768"
    elif test_brand == "wrc-android":
        app_id = "1636663249002958848"
    elif test_brand == "wrc-ios":
        app_id = "1565212314486050816"
    elif test_brand == "romwe-ios":
        app_id = "1694689876483641344"
    else:
        app_id = "1565212314486050816"

    try:
        pattern = r"-(P\d+)"
        level = re.search(pattern, test_name).group(1)
        # test_name = test_name.split('-')[0]
        test_name = re.sub("-P.*", "", test_name)
    except Exception as e:
        level = "P1"

    payload = {
        "name": test_name,
        "description": test_name,
        "parameters": test_args,
        "module": test_module,
        "sort": 200,
        "enabled": True,
        "caseUse": False,
        "appId": app_id,
        "level": level,
    }

    headers = {
        "content-type": "application/json",
        "authorization": authorization
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.text)
    logger.info(response.text)


# class UploadCase:
#     @staticmethod
#     def get_classes_and_methods(name):
#         class_name = ''
#         method_names = []
#         case_names = []
#         module = import_module(name)
#         classes = inspect.getmembers(module, inspect.isclass)
#         for class_name, class_obj in classes:
#             methods = inspect.getmembers(class_obj, inspect.isfunction)
#             for method in methods:
#                 if "test_" in method[0]:
#                     method_names.append(method[0])
#                     strcase = method[1].__doc__
#                     if strcase:
#                         strcase = strcase.replace(" ", "").replace("\n", "")
#                     case_names.append(strcase)
#         return class_name, method_names, case_names
#
#     @classmethod
#     def generate_directory_structure(cls, root_dir):
#         data = {
#             "filename": os.path.basename(root_dir),
#             "children": []
#         }
#         for item in os.listdir(root_dir):
#             item_path = os.path.join(root_dir, item)
#             if os.path.isfile(item_path):
#                 if "test_" in item:
#                     file_info = {}
#                     file_info["filename"] = item
#                     if ".py" in item and "test_" in item and ".pyc" not in item:
#                         class_name, method_names, case_names = cls().get_classes_and_methods(
#                             item_path.replace('/', '.').replace(".py", ""))
#                         file_info["class_name"] = class_name
#                         file_info["method_names"] = method_names
#                         file_info["case_names"] = case_names
#                     data["children"].append(file_info)
#             else:
#                 if "test_" in item:
#                     data["children"].append(cls().generate_directory_structure(item_path))
#         return data
#
#     @classmethod
#     def send_case(cls, path, author="", cmdb_name="", cid="",
#                   test_brand=None, name=None,
#                   message=None):
#         url = "https://tep.wrccorp.cn/api/testing/testcase/uploadCasesByBranch"
#         authorization = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbm9ueW1vdXNVc2VyIiwiYXV0aCI6InVzZXIiLCJpc3MiOiJzaGVpbiIsImV4cCI6NDEwMjMyOTYwMCwiaWF0IjoxNjUyNzY1NzU5fQ.UtLfIAWLHGtGvgPacPm4Ty_fwQeRmskVpvCwO86kdMU"
#
#         data = cls().generate_directory_structure(path)
#         str_data = json.dumps(data)
#         bool_data = 0
#         with open("src/resources/case.txt", "r+") as f:
#             str_old_data = f.read()
#             if str_old_data != str_data:
#                 f.write(str_data)
#             else:
#                 bool_data = 1
#         if bool_data:
#             logger.info("没有要上传的用例")
#             return 0
#         case_list = []
#         if test_brand == "romwe-android":
#             app_id = "1691333576202784768"
#         elif test_brand == "wrc-android":
#             app_id = "1636663249002958848"
#         elif test_brand == "wrc-ios":
#             app_id = "1565212314486050816"
#         elif test_brand == "romwe-ios":
#             app_id = "1565212314486050816"
#         else:
#             app_id = "1565212314486050816"
#
#         with open('src/resources/model_name.yaml', 'r') as file:
#             yaml_mode_name = yaml.safe_load(file)
#
#         tests = "tests"
#         for i in data["children"]:
#             case_type = tests + ("/" + i["filename"])
#             for j in i["children"]:
#                 mode_file = case_type + ("/" + j["filename"])
#                 mode_name = i["filename"] + "/" + j["filename"]
#                 try:
#                     mode_name = yaml_mode_name[i["filename"]][j["filename"]]
#                 except:
#                     pass
#                 j["mode_name"] = mode_name
#                 if "children" in j.keys():
#                     for case in j["children"]:
#                         py_and_class = mode_file + ("/" + case["filename"])
#                         py_and_class += ("::" + case["class_name"])
#                         for case_i in range(len(case["case_names"])):
#                             func_name = py_and_class + ("::" + case["method_names"][case_i])
#                             try:
#                                 pattern = r"-(P\d+)"
#                                 level = re.search(pattern, case["case_names"][case_i]).group(1)
#                             except Exception as e:
#                                 level = "P1"
#
#                             case_info = {
#                                 "appId": app_id,
#                                 "caseUse": False,
#                                 "description": case["case_names"][case_i],
#                                 "enabled": True,
#                                 "level": level,
#                                 "module": mode_name,
#                                 "name": case["case_names"][case_i],
#                                 "parameters": func_name,
#                                 "sort": 200
#                             }
#                             case_list.append(case_info)
#         case_body = {"appId": app_id,
#                      "branch": str(git.Repo(search_parent_directories=True).active_branch).split("/")[-1],
#                      "cases": case_list}
#         # print(case_body)
#         headers = {
#             "content-type": "application/json",
#             "authorization": authorization
#         }
#         # logger.info("开始上传用例，当前时间是:%s" % datetime.now())
#         response = requests.request("POST", url, json=case_body, headers=headers)
#         # logger.info("用例上传结束，当前时间是:%s" % datetime.now())
#         logger.info(response.text)
#
#
# if __name__ == '__main__':
#     UploadCase().send_case("tests")