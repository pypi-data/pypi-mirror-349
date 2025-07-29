# -*- coding:utf-8 -*-
"""
# File       : protocol.py
# Time       ：2024/2/1 10:00
# Author     ：andy
# version    ：python 3.9
"""
import time
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class ModelCard(BaseModel):
    """
    模型卡片
    """
    id: str = Field(default=None, description="模型名称")
    owned_by: Optional[str] = Field(default="owner", description="所有者")
    max_input_token: Optional[int] = Field(description="最大输入token长度")
    max_output_token: Optional[int] = Field(description="最大输出token长度")
    in_price: Optional[float] = Field(description="每输入千token的费用")
    out_price: Optional[float] = Field(description="每输出千token的费用")
    unit: Optional[str] = Field(description="单位")
    mode: Optional[list] = Field(description="支持的模式")
    channel: Optional[str] = Field(description="模型类型")
    created: Optional[str] = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   description="创建时间")


class ModelList(BaseModel):
    """
    模型列表
    """
    data: Optional[List[ModelCard]] = Field(default=[], description="模型列表")

class PromptCard(BaseModel):
    """
    指令卡片
    """
    id: str = Field(default=None, description="模型名称")
    prefix: Optional[str] = Field(default="", description="前置描述")
    prompt: Optional[str] = Field(default="", description="指令模板")
    system: Optional[str] = Field(default="", description="系统提示")
    created: Optional[str] = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   description="创建时间")


class PromptList(BaseModel):
    """
    指令列表
    """
    data: Optional[List[PromptCard]] = Field(default=[], description="指令列表")

class KGCard(BaseModel):
    """
    指令卡片
    """
    id: str = Field(default=None, description="知识库名称")
    desc: Optional[str] = Field(default="", description="描述")
    created: Optional[str] = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   description="创建时间")


class KGList(BaseModel):
    """
    指令列表
    """
    data: Optional[List[KGCard]] = Field(default=[], description="知识库列表")


class ChatMessage(BaseModel):
    """
    聊天信息
    """
    role: Optional[str] = Field(default=None, description="角色")
    content: str = Field(default=None, description="内容")

class ChatCompletionResponseChoice(BaseModel):
    """
    消息模块
    """
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = Field(default=None, description="结束原因")


class ChatCompletionResponseUsage(BaseModel):
    """
    token统计
    """
    prompt_tokens: int = Field(default=0, description="输入token数")
    completion_tokens: int = Field(default=0, description="输出token数")
    total_tokens: int = Field(default=0, description="总token数")
    cost: float = Field(default=0, description="费用")

class ChatCompletionResponseSearch(BaseModel):
    """
    token统计
    """
    title: str = Field(default=None, description="网页标题")
    url: str = Field(default=None, description="网页url")


class ChatCompletionResponseAgg(BaseModel):
    """
    token统计
    """
    model: str = Field(default=None, description="模型")
    content: str = Field(default=None, description="结果")


class ChatCompletionResponse(BaseModel):
    request_id: str = Field(default=None, description="请求ID")
    created: Optional[str] = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    model: str = Field(default=None, description="模型")
    choices: List[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage
    msg: str = Field(default=None, description="执行信息")
    knowledge: list = Field(default=[], description="命中的知识库列表")
    status: int = Field(default=None, description="执行状态")
    result_type: str = Field(default="text", description="结果类型")
    search: Optional[List[ChatCompletionResponseSearch]] = Field(default=None, description="在线搜索结果")
    agg: Optional[List[ChatCompletionResponseAgg]] = Field(default=None, description="聚合结果")

class FinalResponse(BaseModel):
    msg: str = Field(default="执行成功", description="执行信息")
    status: int = Field(default=200, description="执行状态")
    data: Optional[Union[str, ModelList, PromptList, KGList, ChatCompletionResponse]] = Field(default=None, description="结果数据")