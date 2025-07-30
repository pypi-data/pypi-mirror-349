import re
import json
import jsonpath
import requests
import pytest
from loguru import logger

from soium.support.constants import Header, Host, Uri

"""
    引用平台的接口操作地址和购物车
"""


class Util(object):

    @staticmethod
    def basic_tep_request(method, url, flag=1, **kwargs):
        """tep请求基础封装"""

        header_map = {
            1: Header.TEP_HEADER,
            2: ""
        }
        try:
            response = requests.request(method=method, url=url, headers=header_map[flag], **kwargs)
            res = response.json()
            logger.info(f"接口返回数据：{res}")
            return res
        except:
            assert False, "接口请求发生异常"

    @staticmethod
    def get_user_member_id_method(brand=None, email=None, data_center=None):
        """获取用户member id"""

        if brand == "wrc":
            brand_id = 7
        else:
            brand_id = 9

        if data_center == "central":  # 中央站迁移微软云
            data_center = "azure"
        # 数据中心eur:欧洲数据中心，azure:微软数据中心，central:中央数据中心，us:美国数据中心
        data = {
            "alias": email,  # 要删除店配地址的邮箱
            "alias_type": 1,
            "area_abbr": "",
            "area_code": "13643",
            "brand_id": brand_id,
            "data_center": data_center
        }
        logger.info(f"查询用户memberId的参数：{data}")
        url = Host.TEP_URL + Uri.MEMBER_ID
        res = Util.basic_tep_request("post", url, json=data)
        user = res.get("info")
        member_id = user[0].get("member_id") if user else ""
        return member_id

    @staticmethod
    def delete_pickup_address_method(country_id=None, member_id=None, brand=None, data_center=None):
        """删除用户店配地址"""

        if brand == "wrc":
            brand_id = 7
        else:
            brand_id = 9
        if data_center == "central":  # 中央站迁移微软云
            data_center = "azure"
        data = {
            "country_id": country_id,
            "member_id": member_id,
            "brand_id": brand_id,
            "data_center": data_center
        }
        logger.info(f"删除用户店配地址的参数：{data}")
        url = Host.TEP_URL + Uri.DELETE_PICKUP_ADDRESS
        res= Util.basic_tep_request("post", url, json=data)
        info = res.get("info")
        result = info.get("result") if info else 0
        assert result == 1, "删除店配地址失败"

    @staticmethod
    def report_payment_info(status, case_name, job_id, method_name, case_name_suffix_list=None, start_date="", end_date=""):
        """tep上报支付方式运行结果"""

        data = {
            'type': 'extra',
            # 'caseName': 'test_member_belong_to-XX支付渠道',
            'caseName': case_name,
            'methodName': method_name,
            'jobId': job_id,
            'status': status,
            'case_name_suffix_list': case_name_suffix_list,
            'startDate': start_date,
            'endDate': end_date
        }
        url = Host.TEP_URL + Uri.PAYMENT_REPORT
        logger.info(f"传入参数数据{data}")
        res = Util.basic_tep_request("post", url, json=data)
        return res

    @staticmethod
    def get_white_cookies(site_host):
        """获取cookie白名单"""

        url = Host.TEP_URL + Uri.WHITE_COOKIES
        data = {"domain": site_host}
        logger.info(f"请求参数：{data}")
        res = Util.basic_tep_request("get", url, params=data)
        if res.get("success") is True:
            return res.get("data").get("list")
        else:
            pytest.assume(False), "获取白名单cookie接口请求失败"

    @staticmethod
    def add_white_cookies(cookie_name, site_host, expiry):
        """新增cookie白名单"""

        url = Host.TEP_URL + Uri.ADD_COOKIES
        data = {"cookieName": cookie_name, "domain": site_host, "hostname": site_host, "expiration": expiry}
        logger.info(f"请求参数：{data}")
        res = Util.basic_tep_request("post", url, json=data)
        if res.get("success") is True:
            logger.info("添加白名单cookie接口请求成功")
        else:
            pytest.assume(False), "添加白名单cookie接口请求失败"

    @staticmethod
    def query_mail_record(data_center, **kwargs):
        """查询用户邮件记录"""

        url = Host.TEP_URL + Uri.MAIL_RECORD + "?dataCenter=%s" % data_center
        logger.info(f"请求参数：{kwargs}")
        res = Util.basic_tep_request(method="post", url=url, json=kwargs)
        return res

    @staticmethod
    def query_sms_record(data_center, **kwargs):
        """查询用户短信记录"""

        url = Host.TEP_URL + Uri.SMS_RECORD + "?dataCenter=%s" % data_center
        logger.info(f"请求参数：{kwargs}")
        res = Util.basic_tep_request(method="post", url=url, json=kwargs)
        return res

    @staticmethod
    def query_whatsapp_record(data_center, **kwargs):
        """查询用户whatsapp记录"""

        url = Host.TEP_URL + Uri.WHATSAPP_RECORD + "dataCenter=%s" % data_center
        logger.info(f"请求参数：{kwargs}")
        res = Util.basic_tep_request(method="post", url=url, json=kwargs)
        return res

    @staticmethod
    def query_mail_content(data_center, content_id):
        """查询用户邮件内容，近一个月"""

        url = Host.TEP_URL + Uri.MAIL_CONTENT
        data = {"content_id": content_id, "dataCenter": data_center}
        logger.info(f"请求参数：{data}")
        res = Util.basic_tep_request(method="get", url=url, params=data)
        return res

    @staticmethod
    def get_email_verify_code(data_center=None, brand=None, receiver=None, page_num=1, page_size=10):  # 获取邮箱验证码

        data = {
            "brand": brand,
            "query_type": "receiver",
            "receiver": receiver,
            "page_num": page_num,
            "page_size": page_size
        }
        mail_res = Util.query_mail_record(data_center, **data)
        record = jsonpath.jsonpath(mail_res, "$..data")[0]
        content_res = Util.query_mail_content(data_center, content_id=record[0]["content_id"])
        place_holder_res = json.loads(jsonpath.jsonpath(content_res, "$..placeholder")[0])
        return place_holder_res["verification_code"]

    @staticmethod
    def get_phone_verify_code(data_center=None, brand=None, receiver=None, page_num=1, page_size=10):  # 获取邮箱验证码

        data = {
            "brand": brand,
            "query_type": "receiver",
            "receiver": receiver,
            "page_num": page_num,
            "page_size": page_size
        }
        res = Util.query_sms_record(data_center, **data)
        latest_record = jsonpath.jsonpath(res, "$..data")[0][0]
        verify_code = re.findall(r"(\d{5,6})", latest_record["content"])[0]
        return verify_code

    @staticmethod
    def upload_risk_verify_sdk_data(task_id=None, data_key=None, data=None):  # 上报风控sdk数据

        request_data = {
            "taskId": task_id,
            "dataKey": data_key,
            "data": data
        }
        logger.info(f"请求参数是: {request_data}")
        url = Host.RISK_URL + Uri.RISK_SDK_UPLOAD
        res = Util.basic_tep_request(method="post", url=url, json=request_data)
        assert res.get("code") == "0" and res.get("msg").lower() == "ok", "风控sdk数据上传失败"


# email_data = {
#     "data_center": "us",
#     "brand": "wrc",
#     "receiver": "tbb3@163.com",
#     "page_num": 1,
#     "page_size": 10
# }
# phone_data = {
#     "data_center": "central",
#     "brand": "wrc",
#     "receiver": "15005858585",
#     "page_num": 1,
#     "page_size": 10
# }
# Util.query_sms_record(**data)
# print(Util.get_email_verify_code(**email_data))
# print(Util.get_phone_verify_code(**phone_data))


# Util.get_white_cookies("fr.wrc.com")
# Util.add_white_cookies("memberId", site_host="fr.wrc.com")
# Util.report_payment_info(status=1, case_name="测试支付", job_id="1797922453075533824", method_name="test_payement", start_date="2024-06-05 09:00:00", end_date="2024-06-05 09:10:00")
