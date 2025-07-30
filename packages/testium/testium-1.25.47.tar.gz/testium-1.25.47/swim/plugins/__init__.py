from enum import Enum
from typing import NamedTuple


class PytestParser(NamedTuple):
    report: str = None
    terminal: str = None
    browser: str = None
    uuid: str = None
    local: str = None
    site: str = None
    password: str = None
    email: str = None
    host: str = None
    port: str = None
    wda_port: str = None
    device_version: str = None
    device_name: str = None
    bundle_id: str = None
    brand: str = None
    job_id: str = None
    task_id: str = None
    app_key: str = None
    user_proxy: str = None
    event_tracking: str = None
    tep_env: str = None
    extraParams: str = None
    coverage_enable: str = None
    app_pack: str = None
    app_activity: str = None


class Report(Enum):
    class_name = "className"
    method_name = "methodName"
    description = "description"
    important = "important"
    job_id = "jobId"
    app_key = "appKey"
    task_id = "taskId"
    start_date = "startDate"
    site = "site"
    logger = "logger"
    failure_messages = "failureMessages"
    images = "images"
    end_date = "endDate"
    status = "status"
    session = "session"  # 埋点相关参数
    etp_case_list = "etp_case_list"
    martet_link_data = "martetLinkData"


class FailureMessages(Enum):
    content = "content"
    cause = "cause"
    type_info = "type"


class StatusInt(Enum):
    fail = 1  # 默认状态1, 接口定义
    skip = 2
    success = 3


class WhenInfo(Enum):
    setup = "setup"
    failed = "failed"
    teardown = "teardown"
    call = "call"
