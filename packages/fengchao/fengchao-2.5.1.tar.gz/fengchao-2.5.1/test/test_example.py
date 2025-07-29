# -*- coding:utf-8 -*-
"""
# File       : test_example.py
# Time       ：2024/2/23 11:30
# Author     ：andy
# version    ：python 3.9
"""
import time
import json

import pytest
import requests

from fengchao import FengChao

api_key="7fb25a44c3d011eebddf80615f1e1c07"  # 请到安全中心注册或查看
secret_key="2fc28a69d0e8480188386031a226fa2f"  # 请到安全中心注册或查看
local_url = "http://192.168.1.233:5014/local_chat/"
online_url = "http://192.168.1.233:5014/chat/"
token_url = f"http://192.168.1.233:5014/token?api_key={api_key}&secret_key={secret_key}"
models_url = "http://192.168.1.233:5014/models/"
prompts_url = "http://192.168.1.233:5014/prompts/"
kgs_url = "http://192.168.1.233:5014/kgs/"
token=None
effective_time=-1
test_case = [("Qwen1.5-0.5B-Chat", local_url),
             ("Qwen1.5-1.8B-Chat", local_url),
             ("gpt-3.5-turbo", online_url),
             ("ERNIE-Bot-4", online_url),
             ("ERNIE-Bot-8k", online_url),
             ("ERNIE-Bot", online_url),
             ("ERNIE-Bot-turbo", online_url),
             ("BLOOMZ-7B", online_url),
             ("Llama-2-7b-chat", online_url),
             ("Llama-2-13b-chat", online_url),
             ("Llama-2-70b-chat", online_url),
             ("Mixtral-8x7B-Instruct", online_url),
             ("Qianfan-Chinese-Llama-2-7B", online_url),
             ("Qianfan-Chinese-Llama-2-13B", online_url)]

def generate_token():
    """
    生成秘钥
    :return:
    """
    global token, effective_time
    if int(round(time.time() * 1000)) > effective_time or token is None:
        response = requests.request("GET", token_url)
        response = json.loads(response.text)
        if response['status'] == 200:
            effective_time = int(round(time.time() * 1000)) + 30 * 60 * 1000
            token = response['token']
        else:
            print(response['msg'])
            token = None
    return token

def get_models():
    """
    查看支持的模型列表
    :return:
    """
    headers = {
        "content-type": "application/json"
    }
    response = requests.request("GET", models_url, headers=headers)
    return response

def get_prompts():
    """
    查看支持的模型列表
    :return:
    """
    headers = {
        "content-type": "application/json"
    }
    response = requests.request("GET", prompts_url, headers=headers)
    return response

def get_kgs():
    """
    查看支持的知识库列表
    :return:
    """
    headers = {
        "content-type": "application/json"
    }
    response = requests.request("GET", kgs_url, headers=headers)
    return response

def invoke(model, url):
    """
    同步调用接口示例
    :return:
    """
    payload = {
        "model": model,
        "query": "介绍一下北京",
        "is_sensitive": False,
        "max_tokens":10,
        "mode": "invoke"
    }
    token = generate_token()
    if token:
        headers = {
            "content-type": "application/json",
            "Authorization" : token
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        return response

def stream(model, url):
    """
    流式接口
    :return:
    """
    payload = {
        "model": model,
        "query": "介绍一下北京",
        "is_sensitive": False,
        "max_tokens":10,
        "mode": "stream"
    }
    token = generate_token()
    if token:
        headers = {
            "content-type": "application/json",
            "Authorization" : token
        }
        response = requests.request("POST", url, json=payload, headers=headers, stream=True)
        return response


class TestClass:
    def test_token(self):
        assert generate_token() is not None

    def test_models(self):
        response = get_models()
        assert response.status_code == 200

    def test_prompts(self):
        response = get_prompts()
        assert response.status_code == 200

    def test_kgs(self):
        response = get_kgs()
        assert response.status_code == 200

    @pytest.mark.parametrize("model,url", test_case)
    def test_invoke(self, model, url):
        response = invoke(model, url)
        assert response is not None
        assert response.status_code == 200
        response = json.loads(response.text)
        assert response['status'] == 200

    @pytest.mark.parametrize("model,url", test_case)
    def test_stream(self, model, url):
        response = stream(model, url)
        assert response is not None
        assert response.status_code == 200
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk.startswith(":") or not chunk:
                continue
            field, _p, value = chunk.partition(":")
            if field == "data":
                result = json.loads(value)
                assert result['status'] == 200

class TestSDK:
    fengchao = FengChao(api_key, secret_key)

    def test_models(self):
        result = self.fengchao.models()
        assert result.status == 200

    def test_prompts(self):
        result = self.fengchao.prompts()
        assert result.status == 200

    def test_kgs(self):
        result = self.fengchao.kgs()
        assert result.status == 200

    def test_invoke(self):
        result = self.fengchao.chat("Qwen1.5-0.5B-Chat", query="介绍一下北京", is_sensitive=False, mode='invoke')
        assert result.status == 200

    def test_stream(self):
        result = self.fengchao.chat("Qwen1.5-0.5B-Chat", query="介绍一下北京", is_sensitive=False, mode='stream')
        for r in result:
            assert r.status == 200