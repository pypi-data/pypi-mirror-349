"""配置模块

这个模块负责管理应用程序的所有配置项，支持从环境变量和.env文件中读取配置。
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件中的环境变量（如果存在）
load_dotenv()

# API配置
PRIVATE_KEY: str = os.getenv("WEATHER_PRIVATE_KEY", "YOUR_PRIVATE_KEY")
PROJECT_ID: str = os.getenv("WEATHER_PROJECT_ID", "YOUR_PROJECT_ID")
KEY_ID: str = os.getenv("WEATHER_KEY_ID", "YOUR_KEY_ID")
WEATHER_API_HOST: str = os.getenv("WEATHER_API_HOST", "YOUR_URL_ADDRESS.caiyunapp.com")

# 安全配置
EXPECTED_BEARER_TOKEN: str = os.getenv("WEATHER_BEARER_TOKEN", "zishu.co")

# 服务器配置
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

# JWT配置
JWT_DEFAULT_EXPIRY: int = int(os.getenv("JWT_DEFAULT_EXPIRY", "900"))  # 默认15分钟

# 缓存配置
TOKEN_CACHE_ENABLED: bool = os.getenv("TOKEN_CACHE_ENABLED", "True").lower() in ("true", "1", "t")