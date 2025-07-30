#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from loguru import logger


class ProxyConfig(object):

    def us_proxy(self, env):
        """美国代理"""

        proxy_map = {
            "gray": ["10.102.245.23:8899"],
            "gray2": ["10.102.245.23:8999"],
            "gray3": ["10.102.245.23:9988"],
            "gray4": ["10.102.245.23:9998"],
        }
        proxy = random.choice(proxy_map[env])
        logger.info("走代理请求:" + proxy + "环境变量:" + env)
        return proxy

    def eur_proxy(self, env):
        """欧洲代理"""

        proxy_map = {
            "gray": ["10.102.245.24:8899", "10.102.245.41:8899"],
            "gray2": ["10.102.245.24:8999", "10.102.245.41:8999"],
            "gray3": ["10.102.245.24:9988", "10.102.245.41:9988"],
            "gray4": ["10.102.245.24:9998", "10.102.245.41:9998"],
        }
        proxy = random.choice(proxy_map[env])
        logger.info("走代理请求:" + proxy + "环境变量:" + env)
        return proxy

    def mid_proxy(self, env):
        """中央代理"""

        proxy_map = {
            "gray": ["10.102.245.22:8899", "10.102.245.26:8899"],
            "gray2": ["10.102.245.22:8999", "10.102.245.26:8999"],
            "gray3": ["10.102.245.22:9988", "10.102.245.26:9988"],
            "gray4": ["10.102.245.22:9998", "10.102.245.26:9998"],
        }
        proxy = random.choice(proxy_map[env])
        logger.info("走代理请求:" + proxy + "环境变量:" + env)
        return proxy

    def get_site_proxy(self, site, env):
        """获取站点代理"""

        us = ["US", "US_ES"]
        eur = ["DK", "FR", "UK", "DE", "ES", "IT", "NL", "SE", "PL", "BE", "BG", "AT", "CH", "LI", "LU",
               "CZ", "EE", "FI", "HU", "LV", "LT", "PT", "SK", "SI", "IE", "NO", "SE_EN", "AT_FR", "LU_EN",
               "GR", "ROE", "EUQS", "BE_FR", "CH_FR", "RO"]
        if env not in ["gray", "gray2", "gray3", "gray4", "gray6", "gray8"]:
            assert False, "不支持该灰度环境"
        if site in us:
            return self.us_proxy(env)
        elif site in eur:
            return self.eur_proxy(env)
        else:
            return self.mid_proxy(env)
