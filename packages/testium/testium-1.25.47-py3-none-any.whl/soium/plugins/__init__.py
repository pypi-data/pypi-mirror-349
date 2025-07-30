#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

from typing import NamedTuple



class PytestParser(NamedTuple):
    report: str = None
    brand: str = None
    site: str = None
    browser: str = None
    platform: str = None
    host: str = None
    port: str = None
    hub: str = None
    email: str = None
    password: str = None
    extendPort: str = None
    deviceName: str = None
    deviceVersion: str = None
    devicePlatform: str = None
    udid: str = None
    jobId: str = None
    taskId: str = None
    envTag: str = None
    appKey: str = None
    eventTracking: str = None
    tepEnv: str = None
    extraParams: str = None
