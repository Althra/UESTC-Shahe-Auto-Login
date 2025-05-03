#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ctypes
import os
import time
import platform
import requests

from logger import logger
from BitSrunLogin.LoginManager import LoginManager
from config import login_options

# 获取计算机名
host_name = platform.node()

if platform.system().lower().startswith('windows'):
    try:
        #  disable the QuickEdit and Insert mode for the current console
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
    except:
        pass

def is_connect_internet(test_urls=None):
    """
    检测是否真实联网，通过访问一个或多个可靠的公网网站。
    """
    if test_urls is None:
        test_urls = [
            "https://www.baidu.com",
            "https://www.qq.com",
            "https://www.uestc.edu.cn"
        ]
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for url in test_urls:
        try:
            res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False


def always_login(user=None, test_ip=None, delay=2, max_failed=3, **kwargs):
    time_now = lambda: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    org_delay = delay
    failed = 0
    logger.info(f'[{time_now()}] [{host_name}] NetWork Monitor StartUp.')
    while True:
        if not is_connect_internet():
            failed += 1
            delay = max(2., delay / 2)
            if failed >= max_failed:
                logger.info(f'[{time_now()}] [{host_name}] offline.')
                try:
                    LoginManager(**kwargs).login(username=user.user_id, password=user.passwd)
                except:
                    pass
        else:
            if failed >= max_failed:
                logger.info(f'[{time_now()}] [{host_name}] online now.')
            failed = 0
            delay = org_delay
        time.sleep(delay)


if __name__ == "__main__":

    while True:
        try:
            always_login(**login_options)
        except:
            import traceback

            error = traceback.format_exc()
            logger.error(error)
            time.sleep(15)
