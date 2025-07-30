#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from time import sleep

import loguru
import paramiko


class ShellIosUtil(object):

    def __init__(self, _host, _username, _password):
        """初始化"""
        global _ssh_fd
        try:
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(_host, username=_username, password=_password)
        except Exception as e:
            loguru.logger.info('ssh %s@%s: %s' % (_username, _host, e))
            exit()
        self.fd = _ssh_fd
        self.shell = self.fd.invoke_shell()

    def set_ios_proxy(self, hostProxy, portProxy, path_file, password, uuid):
        """
        设置手机代理服务
        :param hostProxy:
        :param portProxy:
        :param path_file:
        :param password:
        :param uuid:
        :return:
        """

        self.shell.send(
            f'ios httpproxy {hostProxy} {portProxy} --p12file={path_file} --password={password} --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(1024)
        d = stdout.decode()
        d = d.split('{"')[-1].split('"}')[0]
        loguru.logger.info(d)
        return d

    def get_ios_ip(self, uuid):
        """
        获取手机的ip
        :param uuid:
        :return:
        """

        self.shell.send(f'ios ip --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(1024)
        d = stdout.decode()
        d = d.split('{"')[-1].split('"}')[0]
        loguru.logger.info(d)
        return d

    def set_ios_remove_proxy(self, uuid):
        """
        移除代理信息
        :param uuid:
        :return:
        """

        self.shell.send(f'ios httpproxy remove --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(1024)
        d = stdout.decode()
        d = d.split('{"')[-1].split('"}')[0]
        loguru.logger.info(d)
        return d

    def set_ios_install_ipa(self):
        """
        安装app
        :return:
        """

        self.shell.send(f'./install.sh /Users/wrc/Downloads/ZZKKO.ipa' + '\n')
        sleep(3)
        stdout = self.shell.recv(1024)
        d = stdout.decode()
        d = d.split('{"')[-1].split('"}')[0]
        loguru.logger.info(d)
        return d

    def get_ios_profile_list(self, uuid):
        """
        获取手机里面的配置文件信息
        :param uuid:
        :return:
        """

        self.shell.send(f'ios profile list --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(2048)
        key = '[{"'
        d = stdout.decode("UTF-8").split(f'{key}')[-1]
        value = f'{key}' + f'{d}'
        key1 = '"}]'
        all_value = value.split(f'{key1}')[0]
        value = f'{all_value}' + f'{key1}'
        loguru.logger.info(str(value))
        return value

    def set_ios_lang(self, uuid, language):
        """
        设置手机语言
        :param uuid:
        :param language:
        :return:
        """

        self.shell.send(f'ios lang --setlang={language} --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(2048)
        d = stdout.decode()
        d = str(d.split('>"')[-1])
        loguru.logger.info(d)
        return d

    def set_ios_reboot(self, uuid):
        """
        重启手机
        :param uuid:
        :return:
        """

        self.shell.send(f'ios reboot --udid={uuid}' + '\n')
        sleep(3)
        stdout = self.shell.recv(2048)
        d = stdout.decode()
        d = str(d.split('>"')[-1])
        loguru.logger.info(d)
        return d

    def put_ios_file(self, local_path_proxy, remote_path_proxy):
        """
        上传文件到远程服务
        :param local_path_proxy:
        :param remote_path_proxy:
        :return:
        """

        sftp = paramiko.SFTPClient.from_transport(self.fd.get_transport())
        loguru.logger.info("准备上传文件")
        sftp.put(f'{local_path_proxy}', remotepath=remote_path_proxy)
        loguru.logger.info("文件已经上传完成")
        sleep(1)

    def cmd_ios_rm(self, remote_path_proxy):
        """
        删除远程文件
        :param remote_path_proxy:
        :return:
        """
        self.fd.exec_command(f'rm -rf {remote_path_proxy}')
        loguru.logger.info("远程文件已经删除")
        sleep(1)


if __name__ == '__main__':
    # current_work_dir = os.path.dirname(__file__)
    # path_proxy = current_work_dir + "/tim.p12"
    # path_proxy_remote = "/Users/wrc/Downloads/she.p12"
    # host = "10.102.14.33"
    host = "10.102.14.29"

    # host = "10.102.14.5"
    # host = "10.102.40.196"
    # host_proxy = "10.102.14.22"
    # port_proxy = "8899"
    # password_file = "wrc"
    # username = "10000547"
    # password = "wrc365!"
    username = "wrc"
    password = "wrc"
    udid = "00008101-001054541A12001E"
    k = ShellIosUtil(_host=host, _username=username, _password=password)
    # k.get_ios_ip(udid)
    # k.get_ios_profile_list(udid)
    k.set_ios_remove_proxy(udid)
    k.fd.close()
    # k.get_ios_ip(udid)
    # k.put_ios_file(local_path_proxy=path_proxy, remote_path_proxy=path_proxy_remote)
    # k.set_ios_install_ipa()
    # k.get_ios_profile_list(udid)
    # k.set_ios_lang(udid, language="en")
    # k.set_ios_reboot(udid)
