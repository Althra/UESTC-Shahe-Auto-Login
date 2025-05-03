#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import namedtuple

User = namedtuple('User', ['user_id', 'passwd', 'wechat_openid'])

# 登录校园网/寝室宽带的用户账号(学号, 密码, None)
#  例如： User('202912272625', '123456Abc@#$', None)


login_options = {
    'user': User('2023000000', '000000', None),  # 填上学号密码

    # 认证页面的地址
    'url': "http://192.168.9.8/",  # 沙河公寓认证地址

    # 认证页面的地址里的参数ac_id=???
    'ac_id': '6',  # 沙河公寓acid=6

    # 网络提供商的类型
    'domain': '@dx',  # 电信:"@dx", 移动:"@cmccgx", 校园网:"@uestc"

    # 下面的一般不用改
    'delay': 16,  # delay seconds
    'max_failed': 3,  # 连续连接失败n次, 认为断网
}
