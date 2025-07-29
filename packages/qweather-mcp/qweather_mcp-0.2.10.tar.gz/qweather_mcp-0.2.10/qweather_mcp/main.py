"""天气查询API服务

这个模块实现了一个基于FastAPI的天气查询服务，同时支持MCP接口，可以被AI助手直接调用。
使用和风天气API作为数据源，通过JWT进行API认证。

作者: zishu.co
版本: 1.0.0
"""

# 标准库导入
import time
import base64
from datetime import datetime
from typing import List, Optional, Dict, Any

# 第三方库导入
import jwt
import requests
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# 本地模块导入
from fastapi_mcp import FastApiMCP, AuthConfig
from qweather_mcp import config  # 导入配置模块

app = FastAPI(title="天气查询API")

# 响应模型
class Location(BaseModel):
    name: str
    id: str
    lat: str
    lon: str
    adm2: str
    adm1: str
    country: str
    tz: str
    utcOffset: str
    isDst: str
    type: str
    rank: str
    fxLink: str

class LocationResponse(BaseModel):
    code: str
    location: List[Location]

class WeatherNow(BaseModel):
    obsTime: str
    temp: str
    feelsLike: str
    icon: str
    text: str
    wind360: str
    windDir: str
    windScale: str
    windSpeed: str
    humidity: str
    precip: str
    pressure: str
    vis: str
    cloud: str
    dew: str

class ReferSources(BaseModel):
    sources: List[str]
    license: List[str]

class WeatherResponse(BaseModel):
    code: str
    updateTime: str
    fxLink: str
    now: WeatherNow
    refer: ReferSources

class JWTRequest(BaseModel):
    expiry_seconds: Optional[int] = 900  # 默认15分钟
    custom_claims: Optional[dict] = None  # 允许添加自定义声明

class WeatherQuery(BaseModel):
    city: str = Field(..., description="城市名，如：北京")

# 解码并加载私钥
private_key = None
try:
    _der_key_bytes = base64.b64decode(config.PRIVATE_KEY)
    private_key = serialization.load_der_private_key(
        _der_key_bytes,
        password=None,
        backend=default_backend()
    )
except Exception as e:
    print(f"关键错误：无法从配置加载EdDSA私钥。错误: {e}")
    if private_key is None:
        raise RuntimeError(f"关键错误：EdDSA私钥加载失败，应用无法启动。错误: {e}")

# 令牌缓存（简单实现，生产环境应使用Redis等缓存系统）
token_cache = {
    "token": None,
    "expires_at": 0
} if config.TOKEN_CACHE_ENABLED else None

# Bearer Token 认证配置
token_auth_scheme = HTTPBearer()

# Bearer Token 验证依赖函数
async def verify_bearer_token(token_payload = Depends(token_auth_scheme)):
    """验证Bearer Token
    
    Args:
        token_payload: 从请求头中提取的Bearer Token信息
        
    Returns:
        str: 验证通过的Token
        
    Raises:
        HTTPException: 当Token无效时抛出401错误
    """
    if token_payload.credentials != config.EXPECTED_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_payload.credentials

# JWT令牌生成函数
def generate_jwt(expiry_seconds: int = config.JWT_DEFAULT_EXPIRY):
    """生成JWT令牌
    
    Args:
        expiry_seconds (int, optional): 令牌有效期，单位为秒. 默认为900秒(15分钟).
    
    Returns:
        str: 生成的JWT令牌
        
    Raises:
        ValueError: 当私钥未初始化或JWT生成失败时抛出
    """
    current_time = int(time.time())
    
    # 构建标准JWT载荷
    payload = {
        'iat': current_time - 30,  # 颁发时间（提前30秒，避免时钟偏差问题）
        'exp': current_time + expiry_seconds,  # 过期时间
        'sub': config.PROJECT_ID  # 主题（项目ID）
    }
    
    # JWT头部
    headers = {
        'kid': config.KEY_ID  # 密钥ID
    }
    
    if private_key is None:
        raise ValueError("JWT生成失败: 私钥未初始化或加载失败。")

    try:
        # 生成JWT
        encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)
        
        # 更新缓存（如果启用）
        if config.TOKEN_CACHE_ENABLED:
            token_cache["token"] = encoded_jwt
            token_cache["expires_at"] = current_time + expiry_seconds - 60  # 提前1分钟过期，确保安全
        
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"JWT生成失败: {str(e)}")

# 获取有效的JWT令牌函数
def get_valid_token():
    """获取有效的JWT令牌
    
    如果缓存中有有效令牌则使用缓存，否则生成新令牌。
    这种方式可以减少令牌生成的次数，提高性能。
    
    Returns:
        str: 有效的JWT令牌
    """
    current_time = int(time.time())
    
    # 如果缓存已启用，检查缓存中的令牌是否有效
    if config.TOKEN_CACHE_ENABLED and token_cache["token"] and token_cache["expires_at"] > current_time:
        return token_cache["token"]
    
    # 生成新令牌
    return generate_jwt()

@app.post("/generate-jwt", operation_id="generate_jwt", tags=["JWT"])
async def create_jwt(
    request: JWTRequest = JWTRequest()
):
    """
    生成JWT令牌的API端点
    
    参数:
        request (JWTRequest): JWT请求对象,包含过期时间等参数
    
    返回:
        dict: 包含以下字段的响应字典
            - jwt: 生成的JWT令牌
            - expires_at: 令牌过期时间(ISO格式)
            - issued_at: 令牌签发时间(ISO格式) 
            - valid_for_seconds: 令牌有效期(秒)
    
    异常:
        HTTPException: 生成JWT过程中发生错误时抛出500错误
    
    说明:
        - 使用EdDSA算法进行签名
        - 默认有效期为15分钟
        - 支持添加自定义声明
    """
    try:
        encoded_jwt = generate_jwt(request.expiry_seconds)
        current_time = int(time.time())
        
        return {
            "jwt": encoded_jwt,
            "expires_at": datetime.fromtimestamp(current_time + request.expiry_seconds).isoformat(),
            "issued_at": datetime.fromtimestamp(current_time - 30).isoformat(),
            "valid_for_seconds": request.expiry_seconds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 天气API请求函数
def fetch_weather_api(endpoint: str, params: Dict[str, Any]):
    """发送HTTP请求到天气API
    
    处理JWT认证、自动重试和错误处理。
    
    Args:
        endpoint (str): API端点路径
        params (Dict[str, Any]): 请求参数
        
    Returns:
        Dict: API响应的JSON数据
        
    Raises:
        HTTPException: 当API请求失败时抛出相应的HTTP错误
    """
    # 获取有效的JWT令牌
    token = get_valid_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept-Encoding': 'gzip'  # 请求gzip压缩以提高传输效率
    }
    
    url = f"https://{config.WEATHER_API_HOST}/{endpoint}"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # 检查响应状态
        if response.status_code != 200:
            # 如果是401或403，尝试刷新令牌并重试
            if response.status_code in [401, 403]:
                # 强制生成新令牌
                new_token = generate_jwt()
                # 更新请求头
                headers['Authorization'] = f'Bearer {new_token}'
                # 重试请求
                response = requests.get(url, headers=headers, params=params)
                
                # 如果还是失败，则抛出异常
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, 
                        detail=f"天气API请求失败: HTTP {response.status_code}"
                    )
            else:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"天气API请求失败: HTTP {response.status_code}"
                )
        
        # 依赖 requests 库自动处理Gzip解压缩，并直接解析JSON
        # 旧的Gzip处理逻辑已被移除
        return response.json()

    except requests.exceptions.JSONDecodeError as e:
        # 如果响应不是有效的JSON（即使在解压缩后），则捕获此特定错误
        raise HTTPException(status_code=500, detail=f"天气API响应解析失败: 无效的JSON内容 - {str(e)}")
    except HTTPException:
        # 重新抛出已捕获的HTTPException，以便FastAPI处理
        raise
    except Exception as e:
        # 捕获其他潜在错误
        raise HTTPException(status_code=500, detail=f"天气API请求时发生未知错误: {str(e)}")

@app.get("/city/lookup", response_model=LocationResponse, operation_id="lookup_city", tags=["天气查询"])
async def lookup_city(
    location: str = Query(..., description="城市名称，如：北京")
):
    """
    根据城市名称查询位置ID
    
    - 返回城市的详细信息和位置ID
    - 位置ID用于后续天气查询
    """
    try:
        data = fetch_weather_api("geo/v2/city/lookup", {"location": location})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/now", response_model=WeatherResponse, operation_id="get_weather_now", tags=["天气查询"])
async def get_weather_now(
    location: str = Query(..., description="位置ID，如：101010100")
):
    """
    获取指定位置的实时天气
    
    - 需要提供位置ID
    - 返回当前天气详情
    """
    try:
        data = fetch_weather_api("v7/weather/now", {"location": location})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weather/by-city", response_model=WeatherResponse, operation_id="get_weather_by_city", tags=["天气查询"])
async def get_weather_by_city(
    query: WeatherQuery
):
    """
    一站式查询城市天气
    
    - 只需提供城市名
    - 自动查询位置ID并获取天气
    """
    try:
        # 先查询城市ID
        location_data = fetch_weather_api("geo/v2/city/lookup", {"location": query.city})
        
        # 检查是否找到城市
        if location_data.get("code") != "200" or not location_data.get("location"):
            raise HTTPException(status_code=404, detail=f"找不到城市: {query.city}")
        
        # 获取第一个匹配城市的ID
        location_id = location_data["location"][0]["id"]
        
        # 查询天气
        weather_data = fetch_weather_api("v7/weather/now", {"location": location_id})
        
        return weather_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """主页 - 提供API简介"""
    return {
        "message": "天气查询API",
        "endpoints": [
            "/generate-jwt - 生成JWT令牌",
            "/city/lookup - 根据城市名查询位置ID", 
            "/weather/now - 根据位置ID查询当前天气",
            "/weather/by-city - 一站式查询城市天气"
        ],
        "docs": "/docs 查看完整API文档"
    }

# MCP (Machine Callable Program) 实现
# 这使得API可以被支持MCP的AI助手直接调用
mcp = FastApiMCP(
    app,
    name="My Weather MCP",
    description="天气查询API",
    include_operations=["get_weather_by_city"],  # 只开放城市天气查询接口给AI助手
    auth_config=AuthConfig(dependencies=[Depends(verify_bearer_token)])  # MCP使用Bearer Token验证
)
mcp.mount()

def run_app():
    """启动FastAPI应用
    
    配置并启动uvicorn服务器
    """
    import uvicorn
    uvicorn.run(
        "qweather_mcp.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )

# 启动服务器
if __name__ == "__main__":
    run_app()
