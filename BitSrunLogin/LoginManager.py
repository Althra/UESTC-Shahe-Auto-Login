import base64

import requests
# import time
import re

from ._decorators import *

from .encryption.srun_md5 import *
from .encryption.srun_sha1 import *
from .encryption.srun_base64 import *
from .encryption.srun_xencode import *

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/63.0.3239.26 Safari/537.36'
}

timeout = 5

class LoginManager:

    @staticmethod
    def encode(s):
        return base64.b64encode(s.encode()).decode()

    @staticmethod
    def decode(s):
        return base64.b64decode(s).decode()

    def __init__(self, **kwargs):
        # urls
        self.args = {
            # urls
            'url': 'http://192.168.9.8',
            'url_login_page': "/",
            'url_get_challenge_api': "/cgi-bin/get_challenge",
            'url_login_api': "/cgi-bin/srun_portal",

            # other static parameters
            'n': "200",
            'vtype': "1",
            'ac_id': "6",
            'enc': "srun_bx1",
            'domain': "@dx",  # 沙河：电信:"@dx", 移动:"@cmccgx", 校园网:"@uestc"

            # tmp args,
            'username': None,
            'password': None,
            'ip': None
        }
        self.username = None
        self.password = None
        self.ip = None
        self.args.update(kwargs)
        self.args['url_login_page'] = self.args['url'] + self.args['url_login_page']
        self.args['url_get_challenge_api'] = self.args['url'] + self.args['url_get_challenge_api']
        self.args['url_login_api'] = self.args['url'] + self.args['url_login_api']
        # for k, v in self.args.items():
        #     self.__setattr__(k, v)

    def login(self, username, password, decode=False):
        if decode:
            username = LoginManager.decode(username)
            password = LoginManager.decode(password)
        self.username = str(username) + self.args['domain']
        self.password = str(password)

        self.get_ip()
        self.get_token()
        self.get_login_responce()

    def get_ip(self):
        print("\033[33mStep1: Get local ip returned from srun server.\033[0m")
        self._get_login_page()
        self._resolve_ip_from_login_page()
        print("----------------")

    def get_token(self):
        print("\033[33mStep2: Get token by resolving challenge result.\033[0m")
        self._get_challenge()
        self._resolve_token_from_challenge_response()
        print("----------------")

    def get_login_responce(self):
        print("\033[33mStep3: Login and resolve response.\033[0m")
        self._generate_encrypted_login_info()
        self._send_login_info()
        self._resolve_login_responce()
        if self._login_result == "ok":
            print(f"\033[32m[√] Login successful! IP: {self._online_ip}\033[0m")
        else:
            print(f"\033[31m[x] Login failed! Error: {self._login_result} Detail: {self._error_msg}\033[0m")
        print("----------------")

    def _is_defined(self, varname):
        """
        Check whether variable is defined in the object
        """
        allvars = vars(self)
        return varname in allvars

    @infomanage(
        callinfo="Getting login page",
        successinfo="Successfully get login page",
        errorinfo="Failed to get login page, maybe the login page url is not correct"
    )
    def _get_login_page(self):
        # Step1: Get login page
        self._page_response = requests.get(self.args['url_login_page'], headers=header, timeout=timeout)

    @checkvars(
        varlist="_page_response",
        errorinfo="Lack of login page html. Need to run '_get_login_page' in advance to get it"
    )
    @infomanage(
        callinfo="Resolving IP from login page html",
        successinfo="Successfully resolve IP",
        errorinfo="Failed to resolve IP"
    )
    def _resolve_ip_from_login_page(self):
        self.ip = re.search(r'ip\s*:\s*"([\d\.]+)"', self._page_response.text).group(1)

    @checkip
    @infomanage(
        callinfo="Begin getting challenge",
        successinfo="Challenge response successfully received",
        errorinfo="Failed to get challenge response, maybe the url_get_challenge_api is not correct. "
                  "Else check params_get_challenge"
    )
    def _get_challenge(self):
        """
        The 'get_challenge' request aims to ask the server to generate a token
        """
        params_get_challenge = {
            "callback": "jsonp1583251661367",  # This value can be any string, but cannot be absent
            "username": self.username,
            "ip": self.ip
        }

        self._challenge_response = requests.get(self.args['url_get_challenge_api'],
                                                params=params_get_challenge, headers=header, timeout=timeout)

    @checkvars(
        varlist="_challenge_response",
        errorinfo="Lack of challenge response. Need to run '_get_challenge' in advance"
    )
    @infomanage(
        callinfo="Resolving token from challenge response",
        successinfo="Successfully resolve token",
        errorinfo="Failed to resolve token"
    )
    def _resolve_token_from_challenge_response(self):
        self.token = re.search('"challenge":"(.*?)"', self._challenge_response.text).group(1)

    @checkip
    def _generate_info(self):
        info_params = {
            "username": self.username,
            "password": self.password,
            "ip": self.ip,
            "acid": self.args['ac_id'],
            "enc_ver": self.args['enc']
        }
        info = re.sub("'", '"', str(info_params))
        self.info = re.sub(" ", '', info)

    @checkinfo
    @checktoken
    def _encrypt_info(self):
        self.encrypted_info = "{SRBX1}" + get_base64(get_xencode(self.info, self.token))

    @checktoken
    def _generate_md5(self):
        self.md5 = get_md5(self.password, self.token)

    @checkmd5
    def _encrypt_md5(self):
        self.encrypted_md5 = "{MD5}" + self.md5

    @checktoken
    @checkip
    @checkencryptedinfo
    def _generate_chksum(self):
        self.chkstr = self.token + self.username
        self.chkstr += self.token + self.md5
        self.chkstr += self.token + self.args['ac_id']
        self.chkstr += self.token + self.ip
        self.chkstr += self.token + self.args['n']
        self.chkstr += self.token + self.args['vtype']
        self.chkstr += self.token + self.encrypted_info

    @checkchkstr
    def _encrypt_chksum(self):
        self.encrypted_chkstr = get_sha1(self.chkstr)

    def _generate_encrypted_login_info(self):
        self._generate_info()
        self._encrypt_info()
        self._generate_md5()
        self._encrypt_md5()

        self._generate_chksum()
        self.password = "{MD5}" + self.md5
        self._encrypt_chksum()

    @checkip
    @checkencryptedmd5
    @checkencryptedinfo
    @checkencryptedchkstr
    @infomanage(
        callinfo="Begin to send login info",
        successinfo="Login info send successfully",
        errorinfo="Failed to send login info"
    )
    def _send_login_info(self):
        login_info_params = {
            'callback': 'jQuery112407481914773997063_1631531125398',
            # This value can be any string, but cannot be absent
            'action': 'login',
            'username': self.username,
            'password': self.encrypted_md5,
            'ac_id': self.args['ac_id'],
            'ip': self.ip,
            'chksum': self.encrypted_chkstr,
            'info': self.encrypted_info,
            'n': self.args['n'],
            'type': self.args['vtype'],
            'os': "Windows 10",
            'name': "Windows",
            'double_stack': 0
        }
        self._login_responce = requests.get(self.args['url_login_api'], params=login_info_params, headers=header, timeout=timeout)

    @checkvars(
        varlist="_login_responce",
        errorinfo="Need _login_responce. Run _send_login_info in advance"
    )
    @infomanage(
        callinfo="Resolving login result",
        successinfo="Login result successfully resolved",
        errorinfo="Cannot resolve login result. Maybe the srun response format is changed"
    )
    def _resolve_login_responce(self):
        self._login_result = re.search('"error":"(.*?)"', self._login_responce.text).group(1)
        self._error_msg = re.search('"error_msg":"(.*?)"', self._login_responce.text).group(1)
        self._online_ip = re.search('"online_ip":"(.*?)"', self._login_responce.text).group(1)
        # print("Result: " + self._login_responce.text)

