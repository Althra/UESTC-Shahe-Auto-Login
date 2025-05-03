# 电子科技大学沙河校区有线网络自动认证脚本

## 概述

宿舍电信宽带隔几天就会自动下线，对路由器和需要长期联网的设备十分不友好。本脚本通过定时检测联网状态和自动登录确保设备能稳定连接到互联网。

基于 [AutoLoginUESTC](https://github.com/b71db892/AutoLoginUESTC) 修改而来。

## 更新

- 修改了`acid`，认证页面地址和登录页获取ip方法等，使其适用于沙河校区。

- 修改了断联检测方式，以防止开代理时`ping`不通。

- 添加了 Windows 下注册为任务计划程序的脚本。

- 添加了 Linux 下注册为systemd服务的脚本。

- 修改了输出和一些细节。

## 使用方式

0. 安装 `python` 并安装 `requests` 库。

1. 修改 `config.py` 中的学号、密码、网络类型。

2. 注销断网，运行 `python login_once.py` , 若成功连接，说明配置没有问题。

3. 注册为开机自启服务：

    - Windows: 在 PowerShell（管理员模式）中运行如下命令

    ```powerShell
    Set-ExecutionPolicy RemoteSigned # 允许用户运行本地脚本
    .\register_task.ps1
    ```

    - Linux: 终端中运行如下命令

    ```bash
    sudo ./register_systemd.sh
    ```

    > 或者直接一直运行 `always_online.py` .

4. 若要注销服务，运行不同平台对应的unregister脚本即可。

## 鸣谢

[b71db892/AutoLoginUESTC](https://github.com/b71db892/AutoLoginUESTC)

[coffeehat/BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)
