# -*- coding:utf-8 -*-
"""
# File       : utils.py
# Time       ：2024/2/23 13:53
# Author     ：andy
# version    ：python 3.9
"""
import jwt
import time
import base64

from tenacity import RetryCallState

token=None
effective_time=-1

def create_token(api_key: str, secret_key: str) -> str :
    """
    生成秘钥
    :return:
    """
    global token, effective_time
    payload = {
        "api_key": api_key,
        "exp": int(round(time.time() * 1000)) + 30 * 60 * 1000,  # 有效期30分钟
        "timestamp": int(round(time.time() * 1000)),
    }
    if int(round(time.time() * 1000)) > effective_time or token is None:
        token = jwt.encode(
                    payload,
                    secret_key,
                    algorithm="HS256",
                    headers={"alg": "HS256", "sign_type": "SIGN"},
                )
        effective_time = int(round(time.time() * 1000)) + 25 * 60 * 1000
    return token

def media_to_base64(path):
    with open(path, 'rb') as fr:
        return base64.b64encode(fr.read()).decode('utf-8')

class Retry:
    retry_num = 3

    def before(self, retry_status: RetryCallState) -> None:
        ...

    def before_sleep(self, retry_status: RetryCallState) -> None:
        ...

    def after(self, retry_status: RetryCallState) -> None:
        ...