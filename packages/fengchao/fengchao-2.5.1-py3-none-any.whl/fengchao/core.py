# -*- coding:utf-8 -*-
"""
# File       : core.py
# Time       ：2024/2/23 13:40
# Author     ：andy
# version    ：python 3.9
"""
import json
import os.path
import sys
import uuid
from typing import Union, Generator, Optional
from pathlib import Path
from urllib.parse import urljoin

import requests
from loguru import logger
from tenacity import retry, stop_after_attempt

from .comments import Comments, file_type
from .protocol import (
    ModelCard,
    ModelList,
    FinalResponse,
    PromptCard,
    PromptList,
    KGList,
    KGCard,
    ChatCompletionResponseChoice,
    ChatMessage,
    ChatCompletionResponseUsage,
    ChatCompletionResponse,
    ChatCompletionResponseSearch,
    ChatCompletionResponseAgg
)
from .utils import create_token, Retry, media_to_base64


class Base:
    def __init__(self, api_key: str, secret_key: str, base_url: str, logger_level: str):
        """
        初始化

        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level:  设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        logger.remove()
        self.logger = logger.add(sys.stderr, level=logger_level)
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url

    def do(self, method, url, payload=None, headers=None, stream=False) -> requests.Response:
        """
        请求远程服务，默认失败进行重试

        :param method:
        :param url:
        :param payload:
        :param headers:
        :param stream:
        :return:
        """
        _retry = retry(stop=stop_after_attempt(Comments.RETRY.retry_num), before=Comments.RETRY.before,
                       after=Comments.RETRY.after, before_sleep=Comments.RETRY.before_sleep)

        @_retry
        def _do():
            path_url = urljoin(self.base_url, url)
            response = requests.request(method, path_url, json=payload, headers=headers, stream=stream, timeout=Comments.TIMEOUT)
            return response
        return _do()

    @retry(stop=stop_after_attempt(Comments.RETRY.retry_num))
    def upload_file(self, files):
        if isinstance(files, str):
            files = [files]
        files = [('files', (Path(file).name, open(file, 'rb'), file_type.get(Path(file).suffix, file_type.get('*')))) for file in files]
        response = requests.post(urljoin(self.base_url, Comments.UPLOAD_URL), files=files)
        return json.loads(response.text)


    def models(self) -> FinalResponse:
        """
        查看支持的模型列表

        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.MODELS_URL, headers=headers)
        except Exception as e:
            logger.error("查看模型列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            model = json.loads(response.text)
            model_card = [ModelCard(id=m.get('id'), owned_by=m.get('owned_by'), mode=m.get('mode'),in_price=m.get('in_price'),
                                    out_price=m.get('out_price'), unit=m.get('unit'), max_input_token=m.get('max_input_token'),
                                    max_output_token=m.get('max_output_token'),channel=m.get('channel')) for m in model['data']]
            return FinalResponse(data=ModelList(data=model_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def prompts(self) -> FinalResponse:
        """
        查看支持的指令列表

        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.PROMPTS_URL, headers=headers)
        except Exception as e:
            logger.error("查看指令列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            prompt = json.loads(response.text)
            prompt_card = [PromptCard(id=p.get('id'), prefix=p.get('prefix'), prompt=p.get('prompt'),
                                    system=p.get('system')) for p in prompt['data']]
            return FinalResponse(data=PromptList(data=prompt_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def kgs(self) -> FinalResponse:
        """
        查看支持的知识库列表

        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.KGS_URL, headers=headers)
        except Exception as e:
            logger.error("查看知识库列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            kg = json.loads(response.text)
            kg_card = [KGCard(id=k.get('id'), desc=k.get('desc')) for k in kg['data']]
            return FinalResponse(data=KGList(data=kg_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def check_model_channel(self, model):
        """
        检查模型类型

        :param model:
        :return:
        """
        model_list = self.models()
        if model_list.status == 200:
            for model_card in model_list.data.data:
                if model_card.id == model:
                    return model_card.channel
        return None

    @staticmethod
    def prepare_chat_result(response):
        """
        格式化结果

        :param response:
        :return:
        """
        choices = []
        for choice in response['choices']:
            choices.append(ChatCompletionResponseChoice(
                        index=choice['index'],
                        message=ChatMessage(role=choice['message']['role'],
                                            content=choice['message']['content']),
                        finish_reason=choice['finish_reason']
                    ))
        usage = ChatCompletionResponseUsage(
            prompt_tokens=response['usage']['prompt_tokens'],
            completion_tokens=response['usage']['completion_tokens'],
            total_tokens=response['usage']['total_tokens'],
            cost=response['usage']['cost']
        )
        search_result = [ChatCompletionResponseSearch(title=search['title'], url=search['url']) for search in response['search']]
        agg_result = [ChatCompletionResponseAgg(model=agg['model'], content=agg['content']) for agg in response['agg']]
        chunk = ChatCompletionResponse(request_id=response['request_id'], model=response['model'], choices=choices,
                                       usage=usage, status=response['status'], msg=response['msg'], knowledge=response['knowledge'],
                                       search = search_result, agg=agg_result)
        return chunk

    def invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        """
        同步请求

        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers)
        except Exception as e:
            logger.error("同步接口服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            result = self.prepare_chat_result(result)
            if result.status == 200:  # 响应正常
                return FinalResponse(data=result)
            else:  # 响应异常
                return FinalResponse(status=result.status, msg=result.msg, data=result)
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    def async_invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        """
        异步请求

        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers)
        except Exception as e:
            logger.error("异步结果服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            if result['status'] == 200:  # 响应正常
                return FinalResponse(data=result['choices'][0]['message']['content'])
            else:  # 响应异常
                return FinalResponse(status=result['status'], msg=result['msg'])
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    def sse_chat(self, url:str, headers:dict, payload:dict) -> Generator:
        """
        同步请求

        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers, stream=True)
        except Exception as e:
            logger.error("流式服务异常：{}".format(e.__str__()))
            yield FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        else:
            if response.status_code == 200: # 请求正常
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk.startswith(":") or not chunk:
                        continue
                    field, _p, value = chunk.partition(":")
                    if field == "data":
                        result = json.loads(value)
                        result = self.prepare_chat_result(result)
                        if result.status == 200: # 响应正常
                            yield FinalResponse(data=result)
                        else: # 响应异常
                            yield FinalResponse(status=result.status, msg=result.msg, data=result)
            else: # 请求异常
                yield FinalResponse(status=response.status_code, msg=response.text)

    def prepare_args(self, model, query ,request_id ,system, prompt ,prompt_fill, is_sensitive, sensitive_replace, task_id,
                           history, response_format, do_sample ,temperature, top_p, max_tokens, mode, knowledge,
                           top_k, threshold, image, video, try_num, timeout, retry_action, files, agg_models, search_param):
        token = create_token(self.api_key, self.secret_key)
        if timeout is not None:
            Comments.TIMEOUT = timeout
        if try_num is not None:
            Comments.RETRY.retry_num = try_num
        if history is None:
            history = []
        if request_id is None:
            request_id = uuid.uuid1().__str__()
        if retry_action is not None:
            Comments.RETRY = retry_action
        if image and os.path.exists(image):
            image = media_to_base64(image)
        if video and os.path.exists(video):
            video = media_to_base64(video)
        if files:
            response = self.upload_file(files)
            if response['status'] == 200:
                files = response['files']
        if mode == 'async_result' and task_id is None: raise ValueError("task_id不能为空")
        headers = {
            "content-type": "application/json",
            "Authorization": token
        }
        payload = {
            'model': model,
            'query': query,
            'request_id': request_id,
            'system': system,
            'prompt': prompt,
            'prompt_fill': prompt_fill,
            'is_sensitive': is_sensitive,
            'sensitive_replace': sensitive_replace,
            'task_id': task_id,
            'history': history,
            'response_format': response_format,
            'do_sample': do_sample,
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens,
            'knowledge': knowledge,
            'top_k': top_k,
            'threshold': threshold,
            'mode': mode,
            'files': files,
            'image':image,
            'video':video,
            'agg_models': agg_models,
            'search_param': search_param
        }
        url = Comments.LOCAL_URL if self.check_model_channel(model) == "本地模型" else Comments.ONLINE_URL
        return headers, payload, url

    def prepare_t2i_args(self, model, query, request_id, task_id, prompt, negative_prompt, prompt_fill,
                                n, size, style, mode, try_num, timeout, retry_action):
        token = create_token(self.api_key, self.secret_key)
        if timeout is not None:
            Comments.TIMEOUT = timeout
        if try_num is not None:
            Comments.RETRY.retry_num = try_num
        if request_id is None:
            request_id = uuid.uuid1().__str__()
        if retry_action is not None:
            Comments.RETRY = retry_action
        headers = {
            "content-type": "application/json",
            "Authorization": token
        }
        payload = {
            'model': model,
            'query': query,
            'request_id': request_id,
            'task_id': task_id,
            'negative_prompt': negative_prompt,
            'prompt': prompt,
            'prompt_fill': prompt_fill,
            'n': n,
            'style': style,
            'size': size,
            'mode': mode
        }
        url = Comments.T2I_URL
        return headers, payload, url


class FengChao(Base):
    def __init__(self, api_key: str, secret_key: str, base_url: str = Comments.BASE_URL, logger_level: str = 'INFO'):
        """
        初始化

        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level: 设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        super().__init__(api_key, secret_key, base_url, logger_level)


    def chat(self,
             model: str,
             query: Optional[str] = None,
             request_id: Optional[str] = None,
             system: Optional[str]=None,
             prompt: Optional[str]=None,
             prompt_fill: dict=None,
             is_sensitive: bool=True,
             sensitive_replace: bool=False,
             task_id: Optional[str]=None,
             history: Optional[list]=None,
             response_format: Optional[str]='text',
             do_sample: bool=True,
             temperature: float =0.8,
             top_p: float =0.75,
             max_tokens: int =256,
             mode: str ='invoke',
             knowledge: Optional[str]=None,
             top_k: int =5,
             threshold: int=500,
             image: str=None,
             video: str=None,
             try_num: Optional[int] = None,
             timeout: Optional[int] = None,
             retry_action: Optional[Retry] = None,
             files: Optional[Union[list, str]] = None,
             agg_models: Optional[list] = None,
             search_param: Optional[dict] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务

        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param system: 系统描述信息
        :param prompt: 指令描述信息
        :param prompt_fill: prompt提示信息的额外参数
        :param is_sensitive: 是否过滤敏感词，默认：True
        :param sensitive_replace: 敏感词是否替换为*，只有is_sensitive为True时有效。流式传输时无效
        :param task_id: 异步请求返回的任务ID
        :param history: 历史对话数据
        :param response_format: 输出内容格式：text：默认，文本格式。json：以json格式输出，使用json模式时请注意以下注意事项：
                                1、在提示词中明确告知大模型以json格式输出，并给出输出示例，例：中国的首都是哪里？请以json的格式输出。例如：{"首都":""}
                                2、输出结果强依赖于大模型输出，请正确告知大模型json格式，如果大模型生成结果不符合预期，将返回空的json，如：{}
                                3、json格式输出不适用流式输出
        :param do_sample: 是否进行采样，默认：True
        :param temperature: 温度，默认：0.8
        :param top_p: 默认：0.75
        :param max_tokens: 最大输出长度。默认：256
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result，流式：stream。默认：invoke
        :param knowledge: 选择要使用的知识库，默认：None
        :param top_k: 知识库参数，命中知识数量
        :param threshold: 知识库参数，阈值，数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
        :param image: 上传图片的地址或base64
        :param video: 上传视频的地址或base64
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :param files: 需要上传的文件，文件地址
        :param agg_models: 聚合模型列表
        :param search_param: 网页搜索参数，默认不开启，参数类型为字典，
                top_k: 返回网页数量，默认为5
                score: 网页分数阈值，默认为0.1

                例如：{'top_k':5, 'score':0.1}
        :return:
        """
        if prompt_fill is None:
            prompt_fill = {}
        headers, payload, url = self.prepare_args(model, query ,request_id ,system, prompt , prompt_fill, is_sensitive, sensitive_replace,
                                                  task_id, history, response_format, do_sample ,temperature, top_p, max_tokens, mode, knowledge,
                                                top_k, threshold, image, video, try_num, timeout, retry_action, files, agg_models, search_param)
        if mode == 'invoke':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'async':
            return self.async_invoke_chat(url, headers, payload)
        elif mode == 'async_result':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'stream':
            return self.sse_chat(url, headers, payload)
        else:
            raise "{}不支持的模式".format(mode)

    def t2i(self,
            model: str,
            query: Optional[str],
            request_id: Optional[str] = None,
            task_id: str = None,
            prompt: Optional[str] = None,
            negative_prompt: Optional[str] = "",
            prompt_fill: dict = None,
            n: int = 1,
            size: str = "1024x1024",
            style: str = "Base",
            mode: str = 'invoke',
            try_num: Optional[int] = None,
            timeout: Optional[int] = None,
            retry_action: Optional[Retry] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务

        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param task_id: 异步请求返回的任务ID
        :param negative_prompt: 反向提示词，即用户希望图片不包含的元素。
        :param prompt: 指令描述信息
        :param prompt_fill: prompt提示信息的额外参数
        :param n: 生成图片数量，默认：1
        :param size: 生成图片长宽,默认：1024x1024
        :param style: 生成图片风格
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result。默认：invoke
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :return:
        """
        if prompt_fill is None:
            prompt_fill = {}
        headers, payload, url = self.prepare_t2i_args(model, query, request_id, task_id, prompt, negative_prompt, prompt_fill,
                                                      n, size, style, mode, try_num, timeout, retry_action)
        if mode == 'invoke':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'async':
            return self.async_invoke_chat(url, headers, payload)
        elif mode == 'async_result':
            return self.invoke_chat(url, headers, payload)
        else:
            raise "{}不支持的模式".format(mode)



class FengChaoAsync(Base):
    def __init__(self, api_key: str, secret_key: str, base_url: str = Comments.BASE_URL, logger_level: str = 'INFO'):
        """
        初始化

        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level: 设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        super().__init__(api_key, secret_key, base_url, logger_level)

    async def invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        return super().invoke_chat(url, headers, payload)

    async def async_invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        return super().async_invoke_chat(url, headers, payload)

    async def sse_chat(self, url:str, headers:dict, payload:dict) -> Generator:
        return super().sse_chat(url, headers, payload)

    async def chat(self,
             model: str,
             query: Optional[str] = None,
             request_id: Optional[str] = None,
             system: Optional[str]=None,
             prompt: Optional[str]=None,
             prompt_fill: dict=None,
             is_sensitive: bool=True,
             sensitive_replace: bool=False,
             task_id: Optional[str]=None,
             history: Optional[list]=None,
             response_format: Optional[str]='text',
             do_sample: bool=True,
             temperature: float =0.8,
             top_p: float =0.75,
             max_tokens: int =256,
             mode: str ='invoke',
             knowledge: Optional[str]=None,
             top_k: int =5,
             threshold: int=500,
             image: str=None,
             video: str=None,
             try_num: Optional[int] = None,
             timeout: Optional[int] = None,
             retry_action: Optional[Retry] = None,
             files: Optional[Union[list, str]] = None,
             agg_models: Optional[list] = None,
             search_param: Optional[dict] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务

        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param system: 系统描述信息
        :param prompt: 指令描述信息
        :param prompt_fill: prompt提示信息的额外参数
        :param is_sensitive: 是否过滤敏感词，默认：True
        :param sensitive_replace: 敏感词是否替换为*，只有is_sensitive为True时有效。流式传输时无效
        :param task_id: 异步请求返回的任务ID
        :param history: 历史对话数据
        :param response_format: 输出内容格式：text：默认，文本格式。json：以json格式输出，使用json模式时请注意以下注意事项：
                                1、在提示词中明确告知大模型以json格式输出，并给出输出示例，例：中国的首都是哪里？请以json的格式输出。例如：{"首都":""}
                                2、输出结果强依赖于大模型输出，请正确告知大模型json格式，如果大模型生成结果不符合预期，将返回空的json，如：{}
                                3、json格式输出不适用流式输出
        :param do_sample: 是否进行采样，默认：True
        :param temperature: 温度，默认：0.8
        :param top_p: 默认：0.75
        :param max_tokens: 最大输出长度。默认：256
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result，流式：stream。默认：invoke
        :param knowledge: 选择要使用的知识库，默认：None
        :param top_k: 知识库参数，命中知识数量
        :param threshold: 知识库参数，阈值，数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
        :param image: 上传图片的地址或base64
        :param video: 上传视频的地址或base64
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :param files: 需要上传的文件，文件地址
        :param agg_models: 聚合模型列表
        :param search_param: 网页搜索参数，默认不开启，参数类型为字典，
                top_k: 返回网页数量，默认为5
                score: 网页分数阈值，默认为0.1

                例如：{'top_k':5, 'score':0.1}
        :return:
        """
        if prompt_fill is None:
            prompt_fill = {}
        headers, payload, url = self.prepare_args(model, query, request_id, system, prompt, prompt_fill, is_sensitive, sensitive_replace,
                                                  task_id, history, response_format, do_sample, temperature, top_p, max_tokens, mode, knowledge,
                                                  top_k, threshold, image, video, try_num, timeout, retry_action, files, agg_models, search_param)
        if mode == 'invoke':
            result = await self.invoke_chat(url, headers, payload)
            return result
        elif mode == 'async':
            result = await self.async_invoke_chat(url, headers, payload)
            return result
        elif mode == 'async_result':
            result = await self.invoke_chat(url, headers, payload)
            return result
        elif mode == 'stream':
            result = await self.sse_chat(url, headers, payload)
            return result
        else:
            raise "{}不支持的模式".format(mode)

    async def t2i(self,
            model: str,
            query: Optional[str] = None,
            request_id: Optional[str] = None,
            task_id: str = None,
            prompt: Optional[str] = None,
            negative_prompt: Optional[str] = "",
            prompt_fill: dict = None,
            n: int = 1,
            size: str = "1024x1024",
            style: str = "Base",
            mode: str = 'invoke',
            try_num: Optional[int] = None,
            timeout: Optional[int] = None,
            retry_action: Optional[Retry] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务

        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param task_id: 异步请求返回的任务ID
        :param negative_prompt: 反向提示词，即用户希望图片不包含的元素。
        :param prompt: 指令描述信息
        :param prompt_fill: prompt提示信息的额外参数
        :param n: 生成图片数量，默认：1
        :param size: 生成图片长宽,默认：1024x1024
        :param style: 生成图片风格
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result。默认：invoke
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :return:
        """
        if prompt_fill is None:
            prompt_fill = {}
        headers, payload, url = self.prepare_t2i_args(model, query, request_id, task_id, prompt, negative_prompt, prompt_fill,
                                                      n, size, style, mode, try_num, timeout, retry_action)
        if mode == 'invoke':
            result = await self.invoke_chat(url, headers, payload)
            return result
        elif mode == 'async':
            result = await self.async_invoke_chat(url, headers, payload)
            return result
        elif mode == 'async_result':
            result = await self.invoke_chat(url, headers, payload)
            return result
        else:
            raise "{}不支持的模式".format(mode)