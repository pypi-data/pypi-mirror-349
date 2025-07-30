import time

from selenium.common.exceptions import WebDriverException, TimeoutException


class Wait(object):
    def __init__(self, timeout, poll=0.5):
        self.timeout = timeout
        self.poll = poll

    def until(self, method, message=None, *args, **kwargs):
        end_time = time.time() + self.timeout
        while True:

            try:
                value = method(*args, **kwargs)
                if value:
                    return value
            except WebDriverException:
                time.sleep(self.poll)
            if time.time() > end_time:
                break
        if message:
            raise TimeoutException(message)
        else:
            return False

    def until_not(self, method, message=None, *args, **kwargs):
        end_time = time.time() + self.timeout
        while True:
            try:
                value = method(*args, **kwargs)
                if not value:
                    return value
            except WebDriverException:
                return True
            time.sleep(self.poll)
            if time.time() > end_time:
                break
        if message:
            raise TimeoutException(message)
        else:
            return False
#
