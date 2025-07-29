# -*- coding:utf-8 -*-
"""
# File       : comments.py
# Time       ：2024/2/23 13:48
# Author     ：andy
# version    ：python 3.9
"""
import os
from dataclasses import dataclass
from .utils import Retry


@dataclass
class Comments:
    BASE_URL = os.getenv("FENGCHAO_BASE_URL", "http://116.112.94.194:6000")
    LOCAL_URL = "/aigc/local_chat/"
    ONLINE_URL = "/aigc/chat/"
    MODELS_URL = "/aigc/models/"
    PROMPTS_URL = "/aigc/prompts/"
    KGS_URL = "/aigc/kgs"
    UPLOAD_URL = "/aigc/uploadfiles/"
    T2I_URL = "/aigc/t2i/"

    TIMEOUT = 600
    RETRY = Retry()

file_type = {
    ".txt": "text/plain",
    ".html": "text/html",
    ".css": "text/css",
    ".js": "text/javascript",
    ".json": "application/json",
    ".xml": "application/xml",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".xlsx": "application/vnd.ms-excel",
    ".xls": "application/vnd.ms-excel",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    "*": "application/octet-stream",
}