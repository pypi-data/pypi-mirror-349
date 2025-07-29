# -*- coding:utf-8 -*-
"""
# File       : examples.py
# Time       ：2024/3/6 10:56
# Author     ：andy
# version    ：python 3.9
"""
import asyncio

from tenacity import RetryCallState

from fengchao import FengChao, FengChaoAsync, Retry


def async_example():
    f = FengChaoAsync(api_key='', secret_key='')
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(f.chat('Qwen1.5-0.5B-Chat', query="请以北京为主题写一篇文章")) for _ in range(10)]
    wait_coro = asyncio.wait(tasks)
    loop.run_until_complete(wait_coro)
    for task in tasks:
        print(task.result())

class MyRetry(Retry):
    retry_num = 2

    def before(self, retry_status: RetryCallState) -> None:
        self.fun()
        return None

    def fun(self):
        print("测试效果")

def retry_example():
    f = FengChao(api_key='', secret_key='')
    result = f.chat('Qwen1.5-0.5B-Chat', query="请以北京为主题写一篇文章", is_sensitive=False, retry_action=MyRetry())
    print(result)