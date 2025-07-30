#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import fcntl
import os

import requests
from loguru import logger

payload = {}
headers = {}


class IosShell(object):

    @staticmethod
    def ios_set_proxy(server_host, server_port, proxy_host, proxy_port, path_file, password, uuid):
        """
        设置手机代理服务
        :param server_port:
        :param server_host:
        :param proxy_host:
        :param proxy_port:
        :param path_file:
        :param password:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/setProxy'
        with open(f'{path_file}', 'rb') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            # 这样就把当前文件给锁了，
            # 此处写文件写入操作
            files = {
                'p12file': f,
                'proxyHost': (None, f'{proxy_host}'),
                'proxyPort': (None, f'{proxy_port}'),
                'proxyPassword': (None, f'{password}'),
            }
            response = requests.post(url, headers=headers, files=files).json()
            fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        logger.info(response)
        return response

    @staticmethod
    def ios_remove_proxy(server_host, server_port, uuid):
        """
        移除手机代理
        :param server_host:
        :param server_port:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/removeProxy'

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_install_ipa(server_host, server_port, upload_file, uuid):
        """
        安装App
        :param server_host:
        :param server_port:
        :param upload_file:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/install'
        with open(f'{upload_file}', 'rb') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            files = {
                'upload': f,
            }
            response = requests.post(url, headers=headers, files=files).json()
            fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        logger.info(response)
        return response

    @staticmethod
    def ios_add_profile(server_host, server_port, profile_file, path_file, password, uuid):
        """
        添加配置文件
        :param server_host:
        :param server_port:
        :param profile_file:
        :param path_file:
        :param password:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/addProfile'
        with open(f'{path_file}', 'rb') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            files = {
                'p12file': open(f'{path_file}', 'rb'),
                'profileFile': open(f'{profile_file}', 'rb'),
                'proxyPassword': (None, f'{password}'),
            }
            response = requests.post(url, headers=headers, files=files).json()
            fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        logger.info(response)
        return response

    @staticmethod
    def ios_profiles_list(server_host, server_port, uuid):
        """
        配置文件列表
        :param server_host:
        :param server_port:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/profiles'

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_remove_profiles(server_host, server_port, uuid, ident):
        """
        移除配置文件
        :param server_host:
        :param server_port:
        :param uuid:
        :param ident:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/removeProfile'

        headers = {'identifier': ident}

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_reboot(server_host, server_port, uuid):
        """
        设备重启
        :param server_host:
        :param server_port:
        :param uuid:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/reboot'

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_uninstall_package(server_host, server_port, package, uuid):
        """
        卸载App
        :param server_host:
        :param server_port:
        :param uuid:
        :param package:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/uninstall'

        headers = {'appName': package}

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_check_install_package(server_host, server_port, package, uuid):
        """
        检查App
        :param server_host:
        :param server_port:
        :param uuid:
        :param package:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/checkInstall'

        headers = {'appName': package}

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_apps(server_host, server_port, package, uuid):
        """
        App列表信息
        :param server_host:
        :param server_port:
        :param uuid:
        :param package:
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/device/{uuid}/apps'

        headers = {'appName': package}

        response = requests.get(url, headers=headers, data=payload).json()
        logger.info(response)
        return response

    @staticmethod
    def ios_list(server_host, server_port):
        """
        设备列表
        :return:
        """
        url = f'http://{server_host}:{server_port}/api/v1/list'

        response = requests.get(url, headers=headers, data=payload).json()
        # logger.info(response)
        return response

    @classmethod
    def get_path_info(cls, fi):
        """
        获取文件路径
        :param fi:
        :return:
        """
        current_work_dir = os.path.dirname(__file__)
        path_proxy = current_work_dir + f"/{fi}"
        return path_proxy


if __name__ == '__main__':
    # proxy_host = "127.0.0.1"
    proxy_host = "10.102.80.5"
    proxy_port = "8899"
    path_file = IosShell.get_path_info("wrc-ios.p12")  # p12的本地文件
    password = "wrc"
    uuid = "00008130-0011050A3083401C"
    server_host = "127.0.0.1"
    server_port = "8429"
    upload_file = IosShell.get_path_info("ZZKKO.ipa")  # 的本地文件
    crt_file = IosShell.get_path_info("rootCA.crt")  # 的本地文件
    package = 'zzkko.com.ZZKKO'
    # IosShell.ios_set_proxy(server_host, server_port, proxy_host, proxy_port, path_file, password, uuid)
    IosShell.ios_remove_proxy(server_host, server_port, uuid)
    # IosShell.ios_reboot(server_host, server_port, uuid)
    # IosShell.ios_proxy(server_host, server_port, uuid, package)
    # IosShell.ios_install_ipa(server_host, server_port, upload_file, uuid)
    # IosShell.ios_add_profile(server_host, server_port, crt_file, path_file, password, uuid)
    # IosShell.ios_profiles_list(server_host, server_port, uuid)
    # IosShell.ios_remove_profiles(server_host, server_port, uuid, ident="32132cd058f9a2ccd5146a3536f5d228df9896a5444d4e710d76d5a7023c3f64a")
    # IosShell.ios_uninstall_package(server_host, server_port, package, uuid)
    # IosShell.ios_install_ipa(server_host, server_port, upload_file, uuid)
