#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import json

import loguru
import requests


host_server = "10.102.14.22:8866"

class CleanCart(object):

    @staticmethod
    def get_http(email, uri):
        headers = {
            # Already added when you pass json= but not when you pass data=
            # 'Content-Type': 'application/json',
        }

        json_data = {
            'email': email,
        }

        response = requests.post(f'http://{host_server}/user/{uri}', headers=headers, json=json_data)
        if response.status_code == 200:
            if response.text is not None:
                data_info = json.loads(response.text).get("data")
                loguru.logger.info(f"接口请求成功:{response.json()}")
                return data_info
        else:
            loguru.logger.info(f"接口请求失败:{response.text}")
            return

    def clear_cart(self, email):
        clear_data = self.get_http(email, uri="deleteCart")
        loguru.logger.info(f"clear_cart======{clear_data}")
        return clear_data

    def clear_address(self, email):
        clear_data = self.get_http(email, uri="deleteAddress")
        loguru.logger.info(f"clear_address======{clear_data}")
        return clear_data


if __name__ == '__main__':
    CleanCart().clear_cart(email="zuizhong@gmail.com")
    CleanCart().clear_address(email="zuizhong@gmail.com")
