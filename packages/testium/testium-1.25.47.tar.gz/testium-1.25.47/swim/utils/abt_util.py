#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import json

import loguru
import requests

from swim.utils.clean_util import host_server


class AbtUtil(object):

    def __init__(self, ip):
        headers = {
            # Already added when you pass json= but not when you pass data=
            # 'Content-Type': 'application/json',
        }
        json_data = {
            'ip': ip,
        }
        response = requests.post(f'http://{host_server}/user/getAbt', headers=headers, json=json_data)
        if response.status_code == 200:
            if response.text is not None:
                self.abt_info = json.loads(response.text).get("data")
            # loguru.logger.info(f"接口请求成功:{response.json()}")
        else:
            loguru.logger.info(f"接口请求失败:{response.text}")

    def get_person_abt_siteUid(self):
        site_uid = self.abt_info.get("siteUid")
        loguru.logger.info(f"get_person_abt_siteUid==={site_uid}")
        return site_uid

    def get_person_abt_appVersion(self):
        app_version = self.abt_info.get("appVersion")
        loguru.logger.info(f"get_person_abt_appVersion==={app_version}")
        return app_version

    def get_person_abt_localCountry(self):
        local_country = self.abt_info.get("localCountry")
        loguru.logger.info(f"get_person_abt_localCountry==={local_country}")
        return local_country

    def get_person_abt_abtBody(self):
        abt_body = self.abt_info.get("abtBody")
        # loguru.logger.info(f"get_person_abt_abtBody==={abt_body}")
        return abt_body

    def get_person_abt_url(self):
        abt_url = self.abt_info.get("url")
        loguru.logger.info(f"get_person_abt_url==={abt_url}")
        return abt_url

    def get_person_abt_token(self):
        abt_token = self.abt_info.get("token")
        loguru.logger.info(f"get_person_abt_token==={abt_token}")
        return abt_token

    def get_person_abt_appLanguage(self):
        app_language = self.abt_info.get("appLanguage")
        loguru.logger.info(f"get_person_abt_appLanguage==={app_language}")
        return app_language


if __name__ == '__main__':
    AbtUtil("10.102.251.9").get_person_abt_token()
